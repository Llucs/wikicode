---
title: Injection de secrets sans incorporer les identifiants de connexion dans les images Docker
description: Une méthode pour gérer de manière sécurisée et injecter des secrets dans les images de conteneurs sans les incorporer directement, assurant une meilleure sécurité et conformité dans les pipelines de déploiement.
created: 2026-07-04
tags:
  - DevOps
  - Docker
  - Kubernetes
  - Sécurité
  - Gestion des secrets
status: brouillon
---

# Injection de secrets sans incorporer les identifiants de connexion dans les images Docker

L'injection de secrets se réfère au processus de gestion sécurisée et d'injectation de données sensibles dans les applications containerisées en temps réel. Cela est réalisé en ne faisant pas figurer les identifiants ou les secrets directement dans l'image Docker, mais plutôt en les fournissant en temps réel ou pendant la phase de déploiement.

## Caractéristiques clés

1. **Sécurité en temps réel** : Les identifiants ne sont jamais incorporés dans l'image, réduisant le risque d'exposition lors de l'analyse de l'image ou de la fuite en raison de vulnérabilités.
2. **Flexibilité** : Permet des mises à jour faciles des secrets sans la nécessité de reconstruire et de redéployer l'image.
3. **Échelle** : Facilite la gestion sécurisée des secrets dans un environnement multi-conteneurs et microservices.
4. **Conformité** : Aide les organisations à respecter les normes réglementaires et les meilleures pratiques en matière de sécurité et de conformité.

## Cas d'utilisation

1. **Identifiants de base de données** : Gérer sécuritairement les noms d'utilisateur et les mots de passe de base de données.
2. **Clés d'API** : Stocker et injecter les clés d'API pour divers services.
3. **Gestion de la configuration** : Injecter des paramètres de configuration qui ne font pas partie du code de l'application.
4. **Clés de chiffrement** : Gérer les clés de chiffrement pour la protection des données en attente ou en transit.

## Installation

Le processus d'installation varie en fonction des outils ou solutions spécifiques utilisés pour la gestion des secrets. Voici des étapes générales pour quelques solutions courantes :

### Secrets Kubernetes

1. **Prérequis** : Cluster Kubernetes.
2. **Installation** : Aucune installation explicite n'est nécessaire ; les secrets sont une fonction intégrée de Kubernetes.
3. **Étapes** :
   1. Créez un secret en utilisant `kubectl` ou un panneau de contrôle Kubernetes.
   2. Référencez le secret dans votre fichier YAML de déploiement ou de manifeste Kubernetes.
   3. Montez le secret en tant que volume ou utilisez-le comme variable d'environnement dans vos pods.

```yaml
# Exemple YAML pour référencer un secret
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app-image
        env:
          - name: MY_SECRET_KEY
            valueFrom:
              secretKeyRef:
                name: my-secret
                key: my-key
```

### Secrets Docker

1. **Prérequis** : Docker Swarm.
2. **Installation** : Aucune installation explicite n'est nécessaire ; Docker Swarm prend en charge les secrets par défaut.
3. **Étapes** :
   1. Créez un secret Docker en utilisant la commande `docker swarm secret create`.
   2. Référencez le secret dans votre définition de service.

```bash
# Créez un secret Docker
docker swarm secret create my-secret my-value

# Référencez le secret dans une définition de service
services:
  my-service:
    secrets:
      - my-secret
    command: ["--my-key=$(MY_SECRET_KEY)"]
```

### Vault HashiCorp

1. **Prérequis** : Serveur HashiCorp Vault.
2. **Installation** : Téléchargez et installez HashiCorp Vault sur votre serveur ou utilisez un service géré.
3. **Étapes** :
   1. Initialisez et déchiffrez Vault.
   2. Créez et stockez des secrets dans Vault.
   3. Utilisez l'API Vault pour récupérer des secrets en temps réel.

```bash
# Initialisez et déchiffrez Vault
vault operator init
vault unseal <clé-de-déchiffrement>

# Créez et stockez un secret
vault kv put secret/my-secret key=my-value

# Récupérez le secret via l'API Vault
vault read secret/my-secret
```

## Utilisation de base

### Création d'un secret

1. **Kubernetes** : `kubectl create secret generic my-secret --from-literal=my-key=my-value`
2. **Docker Swarm** : `docker swarm secret create my-secret my-value`
3. **HashiCorp Vault** : `vault kv put secret/my-secret key=my-value`

### Référence d'un secret

1. **Kubernetes** :
   ```yaml
   spec:
     containers:
     - name: my-app
       image: my-app-image
       env:
         - name: MY_SECRET_KEY
           valueFrom:
             secretKeyRef:
               name: my-secret
               key: my-key
   ```

2. **Docker Swarm** :
   ```yaml
   services:
     my-service:
       secrets:
         - my-secret
       command: ["--my-key=$(MY_SECRET_KEY)"]
   ```

3. **HashiCorp Vault** :
   - Les secrets peuvent être récupérés via l'API Vault ou en utilisant la commande `vault read`.

En adoptant des pratiques d'injection de secrets, les organisations peuvent renforcer considérablement la posture de sécurité de leurs applications containerisées, assurant que les données sensibles demeurent protégées et gérables tout au long du cycle de développement et de déploiement.