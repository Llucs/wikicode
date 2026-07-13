---
title: Meilleures pratiques pour OAuth 2.1 avec PKCE
description: Des directives détaillées pour sécuriser les implémentations OAuth 2.1 en utilisant le Proof Key for Code Exchange (PKCE) pour prévenir les attaques d'injection de code d'autorisation.
created: 2026-07-13
tags:
  - OAuth
  - PKCE
  - Sécurité
  - API
status: brouillon
---

# Meilleures pratiques pour OAuth 2.1 avec PKCE

OAuth 2.1 avec Proof Key for Code Exchange (PKCE) est une extension de protocole qui améliore la sécurité du cadre d'autorisation OAuth 2.0. PKCE est spécifiquement conçu pour atténuer le risque d'interception du code d'autorisation, qui peut se produire chez les clients publics (par exemple, les applications mobiles ou les applications uniques) qui ne disposent pas d'une façon sûre de conserver les secrets de client.

## Fonctionnalités clés

1. **Code Verifier/Challenge** : Une chaîne de caractères aléatoirement générée utilisée par le client pour générer le défi PKCE. Le code verificateur est gardé secret et ne passe pas par le réseau.
2. **Code Challenge** : Un hachage du code verificateur, qui est envoyé au serveur d'autorisation.
3. **Flot d'échange de code d'autorisation** : Ce flot reste le plus souvent le même, mais avec l'ajout de PKCE.

## Histoire

OAuth 2.1 avec PKCE a été introduit comme une extension de OAuth 2.0 pour répondre aux préoccupations de sécurité dans l'authentification des clients. Il a été proposé pour la première fois dans le RFC 7636 et a ensuite été intégré dans la spécification OAuth 2.1.

## Cas d'utilisation

- **Clients publics** : Applications mobiles, applications uniques et tout client qui ne peut pas stocker les secrets de client de manière sécurisée.
- **Sécurité des API** : Améliorer la sécurité de l'accès et de l'authentification des API pour les applications web et mobiles.
- **Applications web** : Améliorer la sécurité des applications web qui utilisent OAuth pour l'authentification.

## Installation

Bien que OAuth 2.1 avec PKCE soit une extension de protocole, son implémentation implique généralement les étapes suivantes :

1. **Implémentation côté client** :
   - Générer un code verificateur et un défi de code.
   - Utiliser le défi de code dans la demande d'autorisation.
   - Gérer la réponse d'autorisation et échanger le code d'autorisation pour un jeton d'accès.

2. **Implémentation côté serveur** :
   - Valider le défi de code contre le code verificateur.
   - Gérer la réponse d'autorisation et échanger le code d'autorisation pour un jeton d'accès.

### Utilisation de base

1. **Authentification du client** :
   - Le client génère un code verificateur et un défi de code.
   - Le défi de code est inclus dans la demande d'autorisation.

2. **Réponse d'autorisation** :
   - L'utilisateur accorde ou refuse l'accès.
   - Le serveur d'autorisation répond avec un code d'autorisation.

3. **Demande de jeton** :
   - Le client échange le code d'autorisation pour un jeton d'accès en utilisant le code verificateur.

4. **Validation** :
   - Le serveur d'autorisation vérifie le défi de code et le code verificateur pour s'assurer de l'authenticité du client.

## Meilleures pratiques

1. **Utiliser des verificateurs de code forts** :
   - Générer des verificateurs de code à l'aide d'un générateur de nombres pseudorandoms cryptographiquement sécurisé (CSPRNG).
   - Assurer que le verificateur de code est au moins de 43 caractères de long pour minimiser les attaques de temps.

2. **Méthodes de défi de code** :
   - Utiliser la méthode `S256` pour hacher le code verificateur. Cette méthode est conçue pour résister aux attaques de temps.

3. **Authentification du client** :
   - Utiliser des méthodes d'authentification de client appropriées pour le type de client (par exemple, `client_secret_basic` pour les clients confidentiels, `none` pour les clients publics).

4. **Sécurité de la transmission** :
   - Assurer que toutes les communications se font par HTTPS pour protéger le défi de code et d'autres informations sensibles.

5. **Gestion des sessions** :
   - Implémenter une gestion des sessions appropriée pour s'assurer que le code d'autorisation ne soit pas réutilisé.

6. **Examens réguliers et mises à jour** :
   - Examiner régulièrement et mettre à jour votre implémentation pour rester à jour avec les dernières pratiques et normes de sécurité.

7. **Délimiter les demandes** :
   - Implémenter la délimitation des demandes pour empêcher l'abus et les attaques par force brute.

8. **Log et surveillance** :
   - Logguer et surveiller les demandes et réponses d'autorisation pour détecter et répondre rapidement aux activités suspectes.

En adhérant à ces meilleures pratiques, vous pouvez améliorer la sécurité de votre implémentation OAuth 2.1 avec PKCE, assurant ainsi la protection des informations sensibles et la sécurité de votre application.

## Exemple : Implémentation en Python

Voici un exemple de base d'implémentation de PKCE en Python utilisant la bibliothèque `requests` :

```python
import requests
import string
import random
import hashlib

# Générer un code verificateur
def generate_code_verifier(length=43):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Générer un code challenge
def generate_code_challenge(verifier):
    sha256 = hashlib.sha256()
    sha256.update(verifier.encode('utf-8'))
    return sha256.hexdigest()[:43]

# Exemple d'authentification client
def authenticate_client(authorization_url, client_id, redirect_uri, code_verifier):
    # Générer le défi de code
    code_challenge = generate_code_challenge(code_verifier)

    # Demande d'autorisation
    auth_params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge
    }

    response = requests.get(authorization_url, params=auth_params)
    if response.status_code != 200:
        raise Exception("Échec de l'authentification du client")

    # Gérer l'interaction de l'utilisateur et obtenir le code d'autorisation

    # Demande de jeton
    token_params = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri,
        'code_verifier': code_verifier
    }

    token_response = requests.post(token_url, data=token_params, auth=(client_id, 'client_secret'))
    if token_response.status_code != 200:
        raise Exception("Échec de l'obtention du jeton d'accès")

    return token_response.json()

# Utilisation
client_id = 'votre_client_id'
redirect_uri = 'http://votre-redirect-uri'
authorization_url = 'https://votre-serveur-d-autorisation'
code_verifier = generate_code_verifier()
code_challenge = generate_code_challenge(code_verifier)
access_token = authenticate_client(authorization_url, client_id, redirect_uri, code_verifier)
print("Token d'accès :", access_token['access_token'])
```

Cet exemple montre comment générer un code verificateur et un défi de code, effectuer la demande d'autorisation et échanger le code d'autorisation pour un jeton d'accès.

## Conclusion

OAuth 2.1 avec PKCE est une amélioration de sécurité cruciale pour les implémentations OAuth 2.0. En suivant les meilleures pratiques énoncées dans ce guide, vous pouvez considérablement améliorer la sécurité de vos applications basées sur OAuth.