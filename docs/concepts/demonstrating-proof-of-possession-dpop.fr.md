---
title: Preuve de possession (DPoP) — Lier les jetons OAuth à l'émetteur avec le RFC 9449
description: Un guide développeur sur DPoP, le mécanisme du RFC 9449 qui lie les jetons d'accès et de rafraîchissement OAuth 2.0 à une paire de clés détenue par le client afin d'empêcher le rejeu et le vol de jetons.
created: 2026-08-07
tags:
  - oauth2
  - security
  - rfc-9449
  - dpop
  - identity
status: draft
---

# Preuve de possession (DPoP)

## Qu'est-ce que DPoP ?

La **preuve de possession (DPoP)** est une extension OAuth 2.0 de la couche application définie dans le **RFC 9449**. Elle *lie à l'émetteur* les jetons d'accès et de rafraîchissement en les rattachant à une paire de clés publique/privée générée et détenue par le client.

Au lieu d'envoyer un simple `Authorization: Bearer <token>`, un client compatible DPoP prouve au serveur de ressources qu'il détient toujours la clé privée utilisée lors de l'émission du jeton. Chaque requête transporte un JWT de preuve signé de courte durée dans un en-tête HTTP `DPoP`. Cette preuve est cryptographiquement liée à la méthode HTTP, à l'URL et au jeton d'accès exacts utilisés.

Comme le jeton d'accès n'est plus un jeton bearer — toute personne qui le possède peut l'utiliser — un jeton volé est inutile sans la clé privée correspondante.

## Pourquoi c'est important

Les jetons bearer OAuth 2.0 classiques présentent un problème fondamental : la possession du jeton est la seule preuve d'autorisation. Un jeton divulgué dans un journal serveur, un en-tête referrer, une extension de navigateur, ou intercepté après la compromission d'une application mobile, peut être rejoué par un attaquant.

DPoP répond à ce problème en modifiant le modèle de menace :

- Un jeton d'accès volé ne peut pas être rejoué à moins que l'attaquant ne vole également la clé privée du client.
- Le jeton d'accès est lié à une clé spécifique au niveau du serveur d'autorisation.
- Le serveur de ressources vérifie une preuve cryptographique à chaque appel API.
- Les jetons de rafraîchissement peuvent également être liés à l'émetteur, comblant ainsi la faille du « vol de jeton de rafraîchissement ».

DPoP est souvent exigé ou recommandé dans les écosystèmes à haute sécurité tels que les API conformes Open Banking / FAPI, les plateformes eHealth et les systèmes d'identité d'entreprise.

## Comment fonctionne DPoP

### 1. Le client génère une paire de clés

Le client crée une paire de clés asymétriques — généralement EC P-256 (ES256). La clé privée reste chez le client. La clé publique est représentée sous forme de JSON Web Key (JWK) et est incluse dans l'en-tête de chaque preuve DPoP.

Le serveur d'autorisation lie le jeton d'accès à cette clé publique en stockant son **empreinte JWK SHA-256** (`jkt`) dans la revendication `cnf` du jeton :

```text
jkt = base64url(SHA-256("<canonical JSON of public JWK>"))
```

### 2. Le client construit un JWT de preuve DPoP

Une preuve DPoP est un JWT avec ces paramètres d'en-tête JOSE :

| En-tête | Valeur |
|---|---|
| `typ` | `dpop+jwt` |
| `alg` | L'algorithme de signature, p. ex. `ES256` |
| `jwk` | La clé publique du client |

Et ces revendications :

| Revendication | Signification |
|---|---|
| `iat` | Heure de création de la preuve |
| `jti` | Identifiant unique de la preuve (prévention du rejeu) |
| `htm` | Méthode HTTP de la requête, p. ex. `GET` |
| `htu` | URI HTTP cible, y compris la chaîne de requête |
| `ath` | Base64url(SHA-256(access_token)) — présent uniquement lors d'un appel à un serveur de ressources |
| `nonce` | Nonce facultatif émis par le serveur |

### 3. Requêtes de jeton et requêtes API

Il existe deux situations où DPoP est utilisé :

**Requête de jeton** — Le client envoie sa preuve DPoP dans un en-tête `DPoP` lors de la requête vers le point de terminaison de jeton du serveur d'autorisation.

```http
POST /token HTTP/1.1
Host: auth.example.com
Content-Type: application/x-www-form-urlencoded
DPoP: <dpop-proof-jwt>

grant_type=authorization_code
&code=...
```

Le serveur d'autorisation vérifie la preuve, lie le jeton émis à l'empreinte JWK de la preuve et renvoie `token_type: "DPoP"` dans la réponse du jeton.

**Requête de ressource** — Le client utilise le jeton avec le schéma d'autorisation `DPoP` et inclut une preuve DPoP *fraîche* contenant `ath`.

```http
GET /reports HTTP/1.1
Host: api.example.com
Authorization: DPoP <access-token>
DPoP: <dpop-proof-jwt-with-ath>
```

### 4. Schéma du flux de requêtes

```text
Client                          Authorization Server                  Resource Server
  |                                     |                                     |
  | POST /token                         |                                     |
  | DPoP: proof(htm=POST, htu=/token)   |                                     |
  |------------------------------------>|                                     |
  |                                     | verify proof signature              |
  |                                     | bind token -> cnf.jkt = JKT(JWK)    |
  | access_token, token_type=DPoP       |                                     |
  |<------------------------------------|                                     |
  |                                     |                                     |
  | GET /reports                        |                                     |
  | Authorization: DPoP <token>         |                                     |
  | DPoP: proof(htm=GET, htu=/reports,  |                                     |
  |             ath=SHA256(token))      |                                     |
  |---------------------------------------------------------------------->    |
  |                                     |                                     | verify:
  |                                     |                                     |  - proof signature
  |                                     |                                     |  - JWK thumbprint == token cnf.jkt
  |                                     |                                     |  - htm/htu match actual request
  |                                     |                                     |  - jti not seen before
  |                                     |                                     |  - iat is fresh
  |                                 200 OK                                     |
  |<----------------------------------------------------------------------    |
```

### 5. Liste de contrôle de vérification côté serveur

Un serveur de ressources conforme devrait :

1. Vérifier que le schéma `Authorization` est `DPoP`, et non `Bearer`.
2. Analyser le JWT de preuve `DPoP`.
3. Vérifier la signature de la preuve à l'aide de la clé publique dans l'en-tête `jwk`.
4. Rejeter les algorithmes non pris en charge (p. ex., `none`).
5. Confirmer que l'empreinte JWK du `jwk` de la preuve correspond au `cnf.jkt` du jeton.
6. Vérifier que `htm` correspond à la méthode HTTP réelle.
7. Vérifier que `htu` correspond à l'URL complète réelle de la requête (schéma, hôte, port le cas échéant, chemin, requête).
8. Si un jeton d'accès est présenté, vérifier que `ath` est égal au hachage SHA-256 de la chaîne exacte de ce jeton.
9. Valider que `iat` se situe dans une fenêtre de fraîcheur acceptable (généralement 60 à 300 secondes).
10. Conserver un cache de courte durée des valeurs `jti` utilisées et rejeter les doublons.
11. Si le serveur est configuré pour exiger des nonces, valider que la preuve contient un nonce actuel émis par le serveur.

### 6. Défis liés aux nonces

De nombreux serveurs d'autorisation et serveurs de ressources exigent qu'une preuve contienne un `nonce` généré par le serveur. Cela empêche une preuve volée d'être rejouée pendant une longue période.

Si le client omet un nonce attendu, le serveur répond avec une erreur et un en-tête `DPoP-Nonce` :

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json
DPoP-Nonce: R5H6rE8sW

{
  "error": "use_dpop_nonce"
}
```

Le client doit créer une **nouvelle** preuve, inclure le nonce, puis réessayer. Il ne doit pas réutiliser l'ancienne preuve.

## Exemple concret — Client Python

L'exemple suivant utilise `cryptography`, `PyJWT` et `requests` pour démontrer le protocole à bas niveau. En production, préférez une bibliothèque OAuth/DPoP maintenue à de la cryptographie maison.

Prérequis :

```bash
pip install cryptography pyjwt requests
```

```python
import base64
import hashlib
import time
import uuid
from typing import Optional

import jwt
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec


def b64url(data: bytes) -> str:
    """Base64url encode without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def public_jwk(private_key: ec.EllipticCurvePrivateKey) -> dict:
    """Convert an EC P-256 public key to a JWK dictionary."""
    numbers = private_key.public_key().public_numbers()
    return {
        "kty": "EC",
        "crv": "P-256",
        "x": b64url(numbers.x.to_bytes(32, "big")),
        "y": b64url(numbers.y.to_bytes(32, "big")),
    }


def dpop_proof(
    private_key: ec.EllipticCurvePrivateKey,
    method: str,
    uri: str,
    access_token: Optional[str] = None,
    nonce: Optional[str] = None,
) -> str:
    """Create a DPoP proof JWT for the given HTTP request."""
    header = {
        "typ": "dpop+jwt",
        "alg": "ES256",
        "jwk": public_jwk(private_key),
    }

    payload = {
        "iat": int(time.time()),
        "jti": uuid.uuid4().hex,
        "htm": method.upper(),
        "htu": uri,
    }

    if access_token is not None:
        token_hash = hashlib.sha256(access_token.encode("utf-8")).digest()
        payload["ath"] = b64url(token_hash)

    if nonce is not None:
        payload["nonce"] = nonce

    return jwt.encode(payload, private_key, algorithm="ES256", headers=header)


def fetch_access_token(
    token_url: str,
    client_id: str,
    client_secret: Optional[str],
    private_key: ec.EllipticCurvePrivateKey,
) -> str:
    """Exchange credentials for an access token using DPoP."""
    data = {"grant_type": "client_credentials"}
    auth = None

    if client_secret:
        auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    else:
        data["client_id"] = client_id

    proof = dpop_proof(private_key, "POST", token_url)
    headers = {"DPoP": proof}

    resp = requests.post(token_url, data=data, headers=headers, auth=auth)

    if resp.status_code == 400 and resp.json().get("error") == "use_dpop_nonce":
        nonce = resp.headers.get("DPoP-Nonce")
        proof = dpop_proof(private_key, "POST", token_url, nonce=nonce)
        resp = requests.post(
            token_url,
            data=data,
            headers={"DPoP": proof},
            auth=auth,
        )

    resp.raise_for_status()
    return resp.json()["access_token"]


def fetch_resource(
    resource_url: str,
    access_token: str,
    private_key: ec.EllipticCurvePrivateKey,
) -> requests.Response:
    """Call a resource server with a DPoP-bound access token."""
    proof = dpop_proof(
        private_key,
        "GET",
        resource_url,
        access_token=access_token,
    )
    headers = {
        "Authorization": f"DPoP {access_token}",
        "DPoP": proof,
    }

    resp = requests.get(resource_url, headers=headers)

    if resp.status_code == 401 and "DPoP-Nonce" in resp.headers:
        nonce = resp.headers["DPoP-Nonce"]
        proof = dpop_proof(
            private_key,
            "GET",
            resource_url,
            access_token=access_token,
            nonce=nonce,
        )
        headers = {
            "Authorization": f"DPoP {access_token}",
            "DPoP": proof,
        }
        resp = requests.get(resource_url, headers=headers)

    return resp
```

Utilisation :

```python
client_private_key = ec.generate_private_key(ec.SECP256R1())

token = fetch_access_token(
    token_url="https://auth.example.com/token",
    client_id="my-public-client",
    client_secret=None,  # public client
    private_key=client_private_key,
)

response = fetch_resource(
    resource_url="https://api.example.com/reports",
    access_token=token,
    private_key=client_private_key,
)

print(response.status_code)
```

Détails importants dans cet exemple :

- Un nouveau `jti` est généré pour chaque preuve.
- La preuve de la requête de jeton ne contient pas d'`ath`.
- La preuve de la requête de ressource hache la chaîne exacte du jeton d'accès.
- Le client conserve la clé privée pendant toute la durée de la session.

## Esquisse de vérification côté serveur

Un serveur de ressources qui vérifie la preuve ci-dessus doit reconstruire la clé publique à partir de l'en-tête `jwk`, puis valider le JWT :

```python
def verify_dpop_proof(
    proof: str,
    method: str,
    uri: str,
    access_token: Optional[str] = None,
) -> dict:
    header = jwt.get_unverified_header(proof)

    if header.get("typ") != "dpop+jwt":
        raise ValueError("Invalid DPoP typ header")

    jwk = header.get("jwk")
    if jwk is None or jwk.get("kty") != "EC" or jwk.get("crv") != "P-256":
        raise ValueError("Unsupported DPoP key")

    x = int.from_bytes(base64.urlsafe_b64decode(jwk["x"] + "=="), "big")
    y = int.from_bytes(base64.urlsafe_b64decode(jwk["y"] + "=="), "big")

    public_key = ec.EllipticCurvePublicNumbers(x, y, ec.SECP256R1()).public_key()
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    claims = jwt.decode(proof, pem, algorithms=["ES256"])

    if claims["htm"] != method.upper():
        raise ValueError("DPoP proof method mismatch")
    if claims["htu"] != uri:
        raise ValueError("DPoP proof URI mismatch")
    if access_token is not None:
        expected_ath = b64url(hashlib.sha256(access_token.encode()).digest())
        if claims.get("ath") != expected_ath:
            raise ValueError("DPoP proof ath mismatch")

    # Additional checks in real code:
    # - Reject duplicate / stale jti
    # - Check iat freshness
    # - Validate nonce against server-issued nonce cache
    # - Verify the proof's JWK thumbprint matches the token's cnf.jkt

    return claims
```

Ce dernier point — faire correspondre le JWK de la preuve au `cnf` lié au jeton — est le cœur de DPoP. Pour les jetons d'accès opaques, le serveur de ressources doit obtenir `cnf` par introspection du jeton. Pour les jetons d'accès JWT, `cnf` est souvent inclus directement dans les revendications du jeton.

## Compromis et alternatives

### DPoP vs. jetons bearer

| Aspect | Jeton bearer | DPoP |
|---|---|---|
| Liaison | Aucune | Clé publique détenue par le client |
| Rejeu d'un jeton volé | Facile | Impossible sans la clé privée |
| Complexité côté client | Très faible | Moyenne : génération de clés, signature, gestion des nonces |
| Surcharge serveur | Minimale | Vérification de signature par requête |
| Norme | RFC 6750 | RFC 9449 |

Les jetons bearer sont adaptés aux API internes à faible risque. DPoP se justifie lorsqu'un jeton divulgué aurait un impact élevé.

### DPoP vs. TLS mutuel (mTLS)

| Aspect | mTLS (RFC 8705) | DPoP |
|---|---|---|
| Couche de liaison | Couche transport | Couche application |
| Gestion des certificats clients | Lourde (PKI, provisionnement) | Paire de clés, plus facile à déployer |
| Fonctionne dans les navigateurs / SPA | Difficile | Fonctionne avec WebCrypto |
| Fonctionne dans les applications mobiles | Difficile | Oui |
| Conformité FAPI | Souvent utilisé | De plus en plus utilisé |

DPoP est généralement plus facile à déployer pour les clients publics web et mobiles que l'infrastructure de certificats mTLS. mTLS reste une option solide pour les intégrations serveur à serveur où la gestion des certificats est déjà courante.

### Limites de DPoP

- **Le vol de la clé privée est fatal.** DPoP protège contre le vol de jetons, pas contre le vol de clés. Une clé privée compromise donne à l'attaquant les mêmes pouvoirs que le client légitime.
- **Coût de signature par requête.** Chaque requête API nécessite une signature et chaque requête vers un serveur de ressources nécessite une vérification.
- **Allers-retours liés aux nonces.** Si un serveur exige des nonces, la première requête après une rotation de nonce entraîne un aller-retour supplémentaire.
- **Charge de gestion des clés.** Les clients doivent créer, stocker et faire pivoter les clés de manière sécurisée. Perdre la clé signifie devoir se réauthentifier.
- **Nécessite un support de bout en bout.** Le serveur d'autorisation et chaque serveur de ressources doivent comprendre DPoP et respecter la liaison `cnf`.
- **Ne remplace pas PKCE.** DPoP n'empêche pas l'interception du code d'autorisation. Utilisez PKCE pour les clients publics.

## Bonnes pratiques

1. **Utilisez DPoP conjointement avec PKCE.** Ils répondent à des menaces différentes. PKCE protège l'échange du code d'autorisation ; DPoP protège les jetons qui en résultent.
2. **Utilisez P-256 / ES256.** C'est largement pris en charge, rapide et sécurisé. Évitez les algorithmes exotiques à moins que toutes les parties ne les prennent en charge.
3. **Générez une nouvelle paire de clés par session utilisateur.** Ne partagez pas une clé privée entre tous les utilisateurs d'une application.
4. **Stockez la clé privée de manière sécurisée.** Utilisez le trousseau du système d'exploitation, Android Keystore, la Secure Enclave d'iOS, un TPM ou une clé WebCrypto non exportable.
5. **Liez également les jetons de rafraîchissement.** Envoyez une preuve DPoP lorsque vous demandez un nouveau jeton d'accès à partir d'un jeton de rafraîchissement. Si le serveur d'autorisation prend en charge les jetons de rafraîchissement liés à l'émetteur, utilisez cette fonctionnalité.
6. **Échec sécurisé (fail closed).** Si le serveur renvoie `token_type: "Bearer"` après une requête DPoP, traitez cela comme une erreur de configuration plutôt que de revenir silencieusement au mode Bearer.
7. **Ne journalisez jamais les preuves DPoP.** Une preuve valide est limitée dans le temps mais reste potentiellement rejouable si le cache `jti` du serveur est de courte durée et que l'attaquant la capture rapidement.
8. **Utilisez une bibliothèque auditée** en production plutôt que d'implémenter le protocole brut. De nombreux SDK OAuth offrent un support DPoP :
   - **Python** — Authlib
   - **JavaScript** — oauth4webapi
   - **Java** — Nimbus OAuth 2.0 SDK / JOSE+JWT
   - **.NET** — IdentityModel
9. **Utilisez toujours HTTPS.** DPoP ne remplace pas TLS ; c'est une défense supplémentaire contre l'utilisation abusive des jetons bearer après qu'une requête a quitté le client.

## Références

- [RFC 9449 — OAuth 2.0 Demonstrating Proof of Possession (DPoP)](https://www.rfc-editor.org/rfc/rfc9449)
- [RFC 6749 — The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749)
- [RFC 7638 — JSON Web Key (JWK) Thumbprint](https://www.rfc-editor.org/rfc/rfc7638)
- [RFC 8705 — OAuth 2.0 Mutual TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705)
- [RFC 7636 — Proof Key for Code Exchange (PKCE)](https://www.rfc-editor.org/rfc/rfc7636)

## Résumé

DPoP transforme les jetons OAuth d'identifiants bearer en identifiants liés à l'émetteur. Le client prouve la possession d'une clé privée à chaque requête, et le serveur de ressources vérifie cette preuve par rapport à la clé liée au jeton lors de son émission. C'est un mécanisme pratique, au niveau de la couche application, qui réduit considérablement les dommages causés par le vol de jetons, en particulier pour les clients publics, les applications mobiles et les applications à page unique.

L'adoption de DPoP ajoute une réelle complexité — gestion des clés, nonces, caches anti-rejeu et vérification à chaque requête — mais pour les API qui transportent des données sensibles, l'amélioration de la sécurité justifie souvent le coût.