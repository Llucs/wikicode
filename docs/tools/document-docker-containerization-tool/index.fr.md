---
title: Docker - Outil de conteneurisation
description: Docker est une plateforme pour développer, empaqueter et déployer des applications dans des conteneurs.
created: 2026-06-13
tags:
  - containerization
  - development
  - deployment
status: draft
ecosystem: containers
---

## Qu'est-ce que Docker ?

Docker est une plateforme qui permet aux développeurs d'empaqueter leur application avec toutes ses dépendances dans une unité standardisée appelée conteneur. Les conteneurs permettent de déployer les applications rapidement et de manière cohérente dans différents environnements, tels que le développement, les tests, la préproduction et la production.

## Pourquoi utiliser Docker ?

1. **Portabilité** : Les conteneurs Docker sont légers et portables, ce qui facilite le déploiement d'applications dans n'importe quel environnement.
2. **Isolation** : Chaque conteneur s'exécute dans son propre environnement isolé, garantissant que l'application n'est pas affectée par d'autres processus en cours.
3. **Cohérence** : Les conteneurs assurent un environnement de développement cohérent à travers les différentes étapes du cycle de vie d'une application.

## Installation

Docker peut être installé sur différents systèmes d'exploitation, notamment Windows, macOS et Linux. Le processus d'installation varie selon le système d'exploitation :

### Pour Ubuntu (Linux) :
```sh
# Update package lists
sudo apt-get update

# Install Docker Engine
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### Pour Windows :
1. Téléchargez Docker Desktop depuis le site officiel.
2. Suivez les instructions d'installation fournies par l'installateur.

### Pour macOS :
```sh
# Download and run the Docker Quickstart Terminal
curl -fsSL https://download.docker.com/mac/stable/Docker.dmg | sudo hdiutil attach -mountpoint /Volumes/docker -noverify -nobrowse /dev/rdiski
cd /Volumes/docker/Docker.app/Contents/Resources/etc/docker.conf.d/
sudo curl -L https://github.com/moby/buildkit/releases/download/v0.14.2/bazelisk_v1.37.2_Linux_x86_64.tar.gz | sudo tar -C . -xzvf -
```

## Utilisation de base

### Téléchargement d'une image
```sh
# Pull the official Nginx image from Docker Hub
docker pull nginx
```

### Exécution d'un conteneur
```sh
# Run a container using the pulled Nginx image
docker run -d --name my-nginx nginx
```

### Liste des conteneurs
```sh
# List all running containers
docker ps

# List all stopped containers
docker ps -a
```

## Principales fonctionnalités

1. **Images** : Les images Docker sont les blocs de construction d'un conteneur, contenant tout ce qui est nécessaire pour exécuter une application.
2. **Volumes** : Stockage persistant pour les données dans un conteneur.
3. **Réseautage** : Permet aux conteneurs de communiquer entre eux et avec des services extérieurs à leur réseau.
4. **Mode Swarm** : Active le clustering et l'orchestration de plusieurs hôtes Docker.

## Conclusion

Docker simplifie le processus de construction, de distribution et d'exécution des applications en fournissant un environnement isolé pour votre code. Cela facilite la gestion des dépendances et garantit des environnements cohérents à travers les différentes étapes de développement et de déploiement.