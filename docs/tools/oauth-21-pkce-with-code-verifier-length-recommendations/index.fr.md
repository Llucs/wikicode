---
title: Recommendations pour la longueur du vérificateur de code dans OAuth 2.1 PKCE
description: Guide sur la mise en œuvre de OAuth 2.1 PKCE avec des recommandations concernant la longueur du vérificateur de code pour améliorer la sécurité.
created: 2026-07-12
tags:
  - OAuth
  - PKCE
  - Sécurité
status: brouillon
---

# Recommendations pour la longueur du vérificateur de code dans OAuth 2.1 PKCE

## Qu'est-ce que le PKCE ?

PKCE (Proof Key for Code Exchange) est une mécanique de sécurité utilisée dans OAuth 2.0 pour empêcher les attaquants de récupérer le code d'autorisation. Il ajoute un autre niveau de sécurité en demandant une clé unique et non réutilisable (le vérificateur de code) à être échangée entre le client et le serveur d'autorisation.

## Caractéristiques clés de OAuth 2.1 PKCE

- **Vérificateur de code** : Une chaîne aléatoire utilisée comme secret entre le client et le serveur d'autorisation.
- **Chalenge de code** : Un hachage du vérificateur de code, utilisé pour prévenir l'écouter de la toile.
- **Nonce** : Une valeur unique incluse dans la demande d'autorisation pour s'assurer que le code est utilisé qu'une seule fois.

## Histoire du PKCE

PKCE a été introduit comme une mécanique optionnelle dans OAuth 2.0 pour améliorer la sécurité. Cependant, il est devenu une partie obligatoire de la spécification OAuth 2.1 pour assurer un niveau de sécurité plus élevé, en particulier pour les clients publics.

## Cas d'utilisation du PKCE

- **Clients publics** : Des clients qui ne peuvent pas stocker de secrets de manière sécurisée, tels que les applications web et mobiles.
- **Flux hybrides** : Appropriate pour les scénarios où le client a besoin d'échanger le code d'autorisation pour un jeton d'accès.
- **Flux d'autorisation par code** : Améliore la sécurité dans les scénarios où le client redirige l'utilisateur vers un serveur d'autorisation.

## Recommendations pour la longueur du vérificateur de code

La longueur du vérificateur de code est un aspect crucial de la sécurité PKCE. Le vérificateur de code doit être assez long pour résister aux attaques par force brute mais court pour être gérable dans les implémentations de client.

### Longueurs recommandées

- **Longueur minimale** : 43 caractères
- **Longueur recommandée** : 128 caractères ou plus

La longueur plus longue du vérificateur de code offre une marge de sécurité plus grande contre les attaques par force brute. La longueur minimale de 43 caractères est recommandée par la spécification OAuth 2.1 pour fournir un niveau raisonnable de sécurité. Cependant, l'utilisation d'un vérificateur de code plus long, tel que 128 caractères, offre une marge de sécurité significativement plus grande.

## Installation et utilisation de base

### Étape 1 : Générer le vérificateur de code

```python
import random
import string

def generate_code_verifier(length=128):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
```

### Étape 2 : Générer le chalenge de code

```python
import hashlib
import base64

def generate_code_challenge(code_verifier):
    code_challenge = hashlib.sha256(code_verifier.encode()).digest()
    return base64.urlsafe_b64encode(code_challenge).rstrip(b'=').decode()
```

### Étape 3 : Inclure PKCE dans le flux d'OAuth 2.0

1. **Demande d'autorisation** :
   - Inclure le `code_challenge` et `code_challenge_method` dans la demande d'autorisation.
   - Exemple :
     ```http
     GET /authorize?response_type=code&client_id=your_client_id&redirect_uri=https%3A%2F%2Fyourapp.com%2Fcallback&code_challenge=your_code_challenge&code_challenge_method=S256&state=some_state_value&nonce=some_nonce_value
     ```

2. **Demande de jeton** :
   - Inclure le `code_verifier` dans la demande de jeton.
   - Exemple :
     ```http
     POST /token HTTP/1.1
     Host: your_authorization_server.com
     Content-Type: application/x-www-form-urlencoded

     grant_type=authorization_code&code=your_authorization_code&redirect_uri=https%3A%2F%2Fyourapp.com%2Fcallback&code_verifier=your_code_verifier
     ```

## Conclusion

L'utilisation de PKCE avec une longueur suffisamment longue du vérificateur de code (au moins 128 caractères) est cruciale pour améliorer la sécurité des flux d'OAuth 2.0, en particulier dans les scénarios de clients publics. En suivant les meilleures pratiques recommandées, les développeurs peuvent assurer un niveau de sécurité plus élevé pour leurs applications.