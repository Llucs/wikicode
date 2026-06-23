---
title: OAuth 2.1 avec PKCE : Guide d'implémentation
description: Une méthode d'authentification sécurisée qui combine OAuth 2.1 avec Proof Key for Code Exchange pour protéger contre les attaques d'interception de code d'autorisation.
created: 2026-06-23
tags:
  - oauth2.1
  - pkce
  - authentication
  - security
  - authorization-code-flow
status: draft
---

# OAuth 2.1 avec PKCE : Guide d'implémentation

## Aperçu

OAuth 2.1 est une consolidation axée sur la sécurité du framework OAuth 2.0 (RFC 6749) et de ses nombreux amendements. Il simplifie la spécification de base tout en renforçant la sécurité en rendant les pratiques auparavant recommandées **obligatoires**. **Proof Key for Code Exchange (PKCE)**, défini à l'origine dans RFC 7636 pour les applications mobiles et natives, est désormais un composant requis du flux de code d'autorisation pour **tous** les clients dans OAuth 2.1.

Ce guide couvre la justification, les étapes de mise en œuvre, les principales fonctionnalités et les stratégies de migration pour adopter OAuth 2.1 avec PKCE dans les applications modernes.

---

## Historique et évolution

| Année | Événement | Impact |
|------|-------|--------|
| 2012 | OAuth 2.0 (RFC 6749) | A introduit plusieurs types d'octroi, notamment les octrois Implicit et Password, qui se sont ensuite avérés non sécurisés. |
| 2015 | PKCE (RFC 7636) | Créé pour prévenir les attaques d'interception de code d'autorisation, principalement pour les clients publics. |
| 2020 | OAuth Security BCP (RFC 9700) | A officiellement déprécié les octrois Implicit et Password ; a rendu obligatoire le PKCE pour tous les clients publics utilisant le flux de code d'autorisation. |
| 2023+ | OAuth 2.1 | Consolide les recommandations du BCP en une seule spécification de base, rendant le PKCE obligatoire pour **tous** les clients et supprimant complètement les octrois non sécurisés. |

---

## Pourquoi OAuth 2.1 + PKCE est important

OAuth 2.1 élimine des catégories entières d'attaques par conception plutôt que par configuration :

- **Interception du code d'autorisation** – PKCE garantit que la partie échangeant le code d'autorisation est la même que celle qui l'a demandé, même si le code est intercepté.
- **Mix-Up Attacks** – La correspondance stricte des URI de redirection empêche les attaquants de substituer leurs propres redirections.
- **CSRF sur le code** – Le `code_verifier` agit comme un nonce sécurisé qui ne peut pas être deviné.
- **Suppression des flux non sécurisés** – L'octroi implicite (Implicit Grant) et l'octroi du mot de passe du propriétaire de la ressource (Resource Owner Password Grant) sont supprimés, fermant des vecteurs d'attaque courants.

**Les déploiements en production** comme les serveurs MCP (par exemple, Azure Container Apps) exigent désormais OAuth 2.1 + PKCE comme méthode d'authentification standard.

---

## Principales fonctionnalités d'OAuth 2.1

### 1. PKCE obligatoire

Le flux de code d'autorisation **doit** inclure un `code_challenge` et un `code_verifier`. Même les clients confidentiels avec un `client_secret` bénéficient d'une défense en profondeur.

### 2. Suppression des octrois Implicit et Password

Seuls les octrois Authorization Code, Client Credentials et Refresh Token subsistent. Tous les autres octrois sont dépréciés.

### 3. Validation stricte des URI de redirection

Les URI de redirection doivent être comparées en utilisant une correspondance exacte de chaîne. Aucun caractère générique ou correspondance de modèle n'est autorisé.

### 4. Rotation des Refresh Tokens

Les refresh tokens doivent être à usage unique. Si un refresh token est réutilisé, il est automatiquement révoqué, signalant une compromission.

### 5. Jetons d'accès liés à l'expéditeur (Sender-Constrained)

Les jetons doivent être liés au client via mTLS (TLS mutuel) ou DPoP (Demonstration of Proof-of-Possession), remplaçant les simples bearer tokens lorsque possible.

---

## Flux de mise en œuvre (étape par étape)

### 1. Préparation du client : génération des paramètres PKCE

Le client doit générer un `code_verifier` cryptographiquement aléatoire et calculer son hachage SHA-256 comme `code_challenge`.

**Exemple avec Node.js (nécessite Node 15+)**

```javascript
import crypto from 'crypto';

// Generate a secure random code_verifier (43-128 characters)
const codeVerifier = crypto.randomBytes(32)
  .toString('base64url')
  .slice(0, 128);

// Compute S256 code_challenge
const codeChallenge = crypto
  .createHash('sha256')
  .update(codeVerifier)
  .digest('base64url');

console.log({ codeVerifier, codeChallenge });
```

**Sortie (masquée) :**
```json
{
  "codeVerifier": "fdb8...d2a9",
  "codeChallenge": "EbZ6...7Qxw"
}
```

### 2. Demande d'autorisation

Redirigez l'utilisateur vers le point de terminaison `/authorize` du serveur d'autorisation avec les paramètres suivants :

```
GET /authorize?
  response_type=code
  &client_id=YOUR_CLIENT_ID
  &redirect_uri=https://yourapp.com/callback
  &scope=openid%20profile%20email
  &code_challenge=EbZ6...7Qxw
  &code_challenge_method=S256
  &state=OPAQUE_STATE_VALUE
```

- `code_challenge_method` **doit** être `S256`. La méthode plain n'est pas autorisée.

### 3. Réception du code d'autorisation

Après l'authentification et le consentement de l'utilisateur, le serveur d'autorisation redirige vers le `redirect_uri` avec un `?code=AUTHORIZATION_CODE`.

```
GET /callback?code=AUTHORIZATION_CODE&state=OPAQUE_STATE_VALUE
```

Validez le paramètre `state` pour prévenir les attaques CSRF.

### 4. Demande de jeton (backchannel)

Le client envoie une requête POST au point de terminaison `/token` avec le `code_verifier`.

**Exemple utilisant `oauth4webapi` (recommandé pour OAuth 2.1)**

```javascript
import * as oauth from 'oauth4webapi';

const issuer = new URL('https://authorization-server.com');
const clientId = 'YOUR_CLIENT_ID';
const clientSecret = undefined; // public client

const as = await oauth.discoveryRequest(issuer);
const { authorization_server } = oauth.processDiscoveryResponse(as, {});

const client = {
  client_id: clientId,
  token_endpoint_auth_method: 'none',
};

const authCode = 'AUTHORIZATION_CODE';
const codeVerifier = 'fdb8...d2a9'; // from step 1

const response = await oauth.authorizationCodeGrantRequest(
  authorization_server,
  client,
  authCode,
  issuer + '/redirect_uri',
  codeVerifier,
);

const tokens = await oauth.processAuthorizationCodeResponse(
  authorization_server,
  client,
  response,
  { expectedNonce: 'NONCE_FROM_ID_TOKEN' },
);
```

**Représentation Curl :**

```bash
curl -X POST https://authorization-server.com/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=AUTHORIZATION_CODE" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "redirect_uri=https://yourapp.com/callback" \
  -d "code_verifier=fdb8...d2a9"
```

### 5. Validation du serveur

Le point de terminaison de jeton effectue :

```
HASH(code_verifier) == code_challenge
```

Si le hachage correspond, le code est valide. Sinon, la requête échoue.

### 6. Réponse du jeton

Une réponse réussie inclut `access_token`, `refresh_token` (si `offline_access` est demandé), et éventuellement `id_token`.

```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "DPoP",
  "expires_in": 3600,
  "refresh_token": "dGhpcyBp...",
  "scope": "openid profile email"
}
```

---

## Prise en charge des bibliothèques

### Côté serveur (serveur d'autorisation)

| Bibliothèque / Plateforme | Support OAuth 2.1 |
|-------------------|-------------------|
| Keycloak          | Oui (PKCE obligatoire par défaut) |
| Entra ID (Azure AD) | Oui (code d'autorisation avec PKCE) |
| Auth0             | Oui (nécessite une configuration) |
| Okta              | Oui |
| Curity            | Oui |
| Spring Security 6+ | Oui (`oauth2Client` avec PKCE) |

### Côté client (application)

| Langage | Bibliothèque | Notes |
|----------|---------|-------|
| Node.js  | [`oauth4webapi`](https://github.com/panva/oauth4webapi) | Spécifique à l'auteur, prêt pour OAuth 2.1 |
| Python   | [`Authlib`](https://authlib.org/) | Prend en charge PKCE et les motifs OAuth 2.1 |
| Java     | Spring Security 6+ | Intégré `NimbusJwtDecoder` avec PKCE |
| Mobile   | AppAuth (Android/iOS) | Support natif PKCE |
| Web SPA  | BFF pattern or Web Workers | Pas de PKCE direct dans le navigateur, utilisez Backend-for-Frontend |

---

## Migration depuis OAuth 2.0

### Liste de contrôle

1. **Remplacez l'octroi Implicit** par Authorization Code + PKCE.
2. **Remplacez l'octroi Password** par Authorization Code + PKCE ou Client Credentials (pour machine à machine).
3. **Appliquez PKCE** pour chaque échange de code d'autorisation.
4. **Activez la rotation des Refresh Token** (jetons à usage unique).
5. **Mettez à jour la comparaison des URI de redirection** pour une correspondance exacte de chaîne.
6. **Passez à la méthode de défi S256** si vous utilisiez auparavant `plain`.

### Exemple : Migration d'un flux de code d'autorisation hérité

**Avant (OAuth 2.0 – PKCE optionnel)**

```
step 1: client_id + redirect_uri → get code
step 2: code + client_secret → get token
```

**Après (OAuth 2.1 – PKCE obligatoire)**

```
step 1: client_id + redirect_uri + code_challenge (S256) → get code
step 2: code + code_verifier → get token
```

---

## Exemple concret : Serveur MCP sur Azure Container Apps

La spécification du Model Context Protocol (MCP) (en date du 2026-03-15) exige OAuth 2.1 + PKCE pour l'autorisation lors de l'interaction avec les serveurs d'agents. Voici une configuration condensée :

1. **Définissez PRM (Protected Resource Metadata)** – exposez `.well-known/oauth-authorization-server`
2. **Implémentez l'enregistrement dynamique des clients** (RFC 7591) pour les clients.
3. **Conception des scopes** – définissez des scopes granulaires par ressource (par exemple, `files:read`, `compute:execute`).
4. **Validation des jetons** – chaque requête API doit vérifier la signature du jeton d'accès et la clé liée.

Exemple de configuration AZ CLI (concept) :

```bash
az containerapp create \
  --name mcp-server \
  --environment MyEnv \
  --image myregistry.azurecr.io/mcp:v1 \
  --secrets oauth-jwks-secret="$(cat jwks.json)" \
  --env-vars OAUTH_AUTHORIZATION_URL="https://login.contoso.com/authorize" \
             OAUTH_TOKEN_URL="https://login.contoso.com/token" \
             OAUTH_CLIENT_ID="mcp-server" \
  --ingress 'external'
```

Le client (par exemple, l'extension VSCode Azure MCP) effectue ensuite le flux PKCE avant d'invoquer les outils MCP.

---

## Meilleures pratiques de sécurité

- **Utilisez un paramètre d'état (state)** – Liez la demande d'autorisation à la session utilisateur.
- **Stockez le `code_verifier` de manière sécurisée** – Dans la session backend ou un stockage client sécurisé (pas dans l'URL).
- **Validez chaque jeton** – Vérifiez la signature, l'émetteur, l'audience et l'expiration.
- **Faites tourner les refresh tokens** – Chaque rafraîchissement produit un nouveau jeton et invalide le précédent.
- **Implémentez DPoP** – Ajoutez la revendication `cnf` aux jetons d'accès pour le support de contrainte d'expéditeur.
- **Enregistrez la réutilisation des jetons** – Détectez un vol potentiel de jetons.

---

## Dépannage des problèmes courants

| Problème | Cause probable | Solution |
|---------|--------------|----------|
| `invalid_grant` lors de l'échange de jeton | Le `code_verifier` ne correspond pas au `code_challenge` | Re-hachez le verifier exactement comme lors de la création (même algorithme, même encodage de caractères) |
| `redirect_uri_mismatch` | La comparaison d'URL n'est pas exacte | Assurez-vous que `redirect_uri` correspond exactement, y compris les barres obliques finales |
| Code d'autorisation expiré | Délai d'attente supérieur à 10 minutes | Recommencez le flux complet |
| Refresh token rejeté après rotation | Rejeu de jeton détecté | Le client doit jeter les anciens refresh tokens ; implémentez correctement la rotation à usage unique |

---

## Références

- [OAuth 2.1 Draft Specification](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)
- [PKCE RFC 7636](https://datatracker.ietf.org/doc/html/rfc7636)
- [OAuth Security BCP (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [oauth4webapi – Official Implementation](https://github.com/panva/oauth4webapi)
- [Authlib – OAuth 2.1 for Python](https://authlib.org/)
- [Spring Security 6 OAuth 2.1 Client](https://docs.spring.io/spring-security/reference/servlet/oauth2/client/index.html)

---

## Conclusion

Adopter OAuth 2.1 avec PKCE n'est pas seulement une exigence de conformité : c'est une amélioration fondamentale de la posture de sécurité. En rendant PKCE obligatoire, en supprimant les flux faibles et en imposant une validation stricte, OAuth 2.1 garantit que les applications modernes sont résilientes face aux attaques d'autorisation les plus courantes. Que vous construisiez un nouveau serveur MCP, migriez des applications mobiles héritées ou renforciez une application monopage (SPA), cette spécification offre une voie claire et sécurisée.