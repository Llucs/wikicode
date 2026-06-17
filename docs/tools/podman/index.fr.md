---
title: Podman - Gestion de conteneurs sans démon
description: Un guide complet sur Podman, le moteur de conteneurs sans démon pour gérer les conteneurs, les pods et les images.
created: 2026-06-15
tags:
  - containers
  - podman
  - docker-alternative
  - devops
  - linux
status: draft
ecosystem: containers
---

# Podman - Gestion de conteneurs sans démon

Podman est un moteur de conteneurs open-source et sans démon développé par Red Hat. Il fournit une interface en ligne de commande entièrement compatible avec Docker, tout en offrant des fonctionnalités uniques telles que la prise en charge native des pods, le fonctionnement sans privilèges (rootless) et une intégration transparente avec systemd. Podman respecte les normes OCI (Open Container Initiative) et est un composant clé de la chaîne d'outils de conteneurs de Red Hat aux côtés de Buildah et Skopeo.

## Qu'est-ce que Podman ?

Podman (abréviation de **Pod Manager**) est un outil de gestion des conteneurs, images, volumes et pods OCI. Contrairement à Docker, Podman ne repose **pas** sur un démon d'arrière-plan central (`dockerd`). Au lieu de cela, les conteneurs s'exécutent en tant que processus enfants directs de la commande Podman, ce qui les rend plus faciles à gérer avec les outils de processus Linux standard et systemd.

## Pourquoi Podman ?

- **Architecture sans démon** – Pas de démon persistant signifie une utilisation moindre des ressources, un dépannage simplifié et une intégration plus facile avec les systèmes d'init.
- **Sans privilèges par défaut (Rootless)** – Podman peut exécuter des conteneurs sans privilèges root en utilisant des espaces de noms utilisateur, réduisant considérablement la surface d'attaque.
- **Prise en charge des pods** – La prise en charge intégrée des pods (groupes de conteneurs partageant des espaces de noms) reflète les concepts de Kubernetes, permettant le développement local de manifests de pods.
- **Compatibilité avec Docker** – Les commandes comme `podman run`, `podman build` et `podman ps` correspondent directement à leurs équivalents Docker ; un alias `alias docker=podman` fonctionne parfaitement pour la plupart des flux de travail.
- **Intégration avec systemd** – Générez des fichiers d'unité systemd pour n'importe quel conteneur, permettant le démarrage automatique, la relance en cas d'échec et l'intégration avec la gestion des services Linux moderne.
- **Open Source et communauté** – Propriété de Red Hat et faisant partie de l'écosystème CNCF, avec une communauté solide et un support entreprise.

## Installation

Podman est disponible sur tous les principaux systèmes d'exploitation. La façon la plus simple de commencer dépend de votre plateforme.

### Linux

**Fedora / RHEL / CentOS**
```bash
sudo dnf install podman
```

**Debian / Ubuntu**
```bash
sudo apt-get update && sudo apt-get install podman
```

**Arch Linux**
```bash
sudo pacman -S podman
```

### macOS

En utilisant [Homebrew](https://brew.sh/) :
```bash
brew install podman
podman machine init       # Create a Linux VM
podman machine start      # Start the VM
```

### Windows

En utilisant [Winget](https://learn.microsoft.com/en-us/windows/package-manager/) :
```bash
winget install RedHat.Podman
```
Ou téléchargez l'installateur depuis la [page des versions de Podman](https://github.com/containers/podman/releases).

Après l'installation, exécutez `podman machine init` et `podman machine start` pour configurer la VM gérée (requis sur macOS et Windows).

## Fonctionnalités clés

### Conteneurs sans démon et sans privilèges (Daemonless & Rootless)

Podman élimine le besoin d'un démon central. Chaque invocation de `podman run` ou `podman exec` fork directement le processus du conteneur sous l'UID de l'utilisateur appelant. Le mode sans privilèges (rootless) est le mode par défaut ; l'espace de noms utilisateur de Podman mappe l'utilisateur non privilégié de l'hôte en root à l'intérieur du conteneur. La sécurité est encore renforcée avec les politiques SELinux et seccomp.

### Pods (Regroupement natif de style Kubernetes)

Un pod est un ensemble de conteneurs partageant le même espace de noms réseau, la même adresse IP et le même espace de ports. Les pods facilitent la modélisation d'applications multi-conteneurs qui doivent être déployées ensemble.

```bash
# Create a pod with an exposed port
podman pod create --name mypod -p 8080:80

# Run an nginx container inside the pod
podman run --pod mypod -d --name web nginx:alpine

# Run a helper container (e.g., sidecar) in the same pod
podman run --pod mypod -d --name logger busybox tail -f /dev/null

# List pods
podman pod ps
```

### Intégration avec systemd

Les conteneurs peuvent être gérés comme des services systemd natifs, garantissant un redémarrage automatique au démarrage ou en cas d'échec.

```bash
# Run a container in the background
podman run -d --name myapp my-image

# Generate systemd unit files
podman generate systemd --new --files --name myapp

# Copy the generated file to the systemd directory and enable it
sudo cp container-myapp.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now container-myapp.service
```

### Compatibilité avec Docker et `podman-compose`

Podman accepte la plupart des commandes Docker directement. Pour les fichiers Docker Compose, vous pouvez utiliser `podman compose` (nécessite `podman-compose` ou le plugin Docker Compose installé séparément).

```yaml
# Example docker-compose.yml works with podman-compose
version: '3'
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
```

Exécutez avec :
```bash
podman-compose up -d
```

### Construire des images avec Buildah

Bien que `podman build` soit disponible, l'outil dédié Buildah offre un contrôle plus précis sur la construction d'images, y compris la capacité de créer des images sans environnement d'exécution de conteneur.

```bash
podman build -t my-app .
```

## Utilisation de base

Les commandes suivantes reflètent la syntaxe de Docker et peuvent être apprises en toute sécurité pour les environnements Podman et Docker.

```bash
# Pull an image
podman pull docker.io/library/alpine:latest

# List images
podman images

# Run a container in the foreground, interactive shell
podman run -it --rm alpine /bin/sh

# Run a detached web server
podman run -d --name web -p 8080:80 nginx:alpine

# List running containers
podman ps

# List all containers (including stopped)
podman ps -a

# Execute a command inside a running container
podman exec -it web /bin/sh

# View logs
podman logs web

# Stop and remove a container
podman stop web && podman rm web

# Remove all unused images
podman image prune -a
```

## Migration depuis Docker

Pour ceux qui utilisent actuellement Docker, la transition est simple :

- **Alias pour la CLI** : `alias docker=podman` (ajoutez à votre profil shell).
- **Docker Compose** : Installez `podman-compose` ou utilisez le plugin Docker Compose avec l'activation de socket de Podman (`podman system service`).
- **Volumes et réseaux** : Podman prend en charge les volumes de style Docker et les réseaux CNI/Netavark.
- **Dockerfiles** : `podman build` fonctionne avec n'importe quel Dockerfile standard.

> ⚠️ *Note* : Certaines fonctionnalités spécifiques à Docker (comme le mode Swarm et les contextes Docker) ne sont pas implémentées dans Podman. Pour Swarm, envisagez des alternatives comme Nomad ou Kubernetes.

## Ressources supplémentaires

- [Documentation officielle de Podman](https://docs.podman.io/)
- [Dépôt GitHub de Podman](https://github.com/containers/podman)
- [Outils de conteneurs Red Hat](https://www.redhat.com/en/topics/containers)
- [Conteneurs sans privilèges avec Podman](https://rootlesscontaine.rs/getting-started/podman/)
- [Podman vs Docker : une comparaison complète](https://developers.redhat.com/articles/2023/08/29/why-podman-replaces-docker)

---

Podman est un moteur de conteneurs moderne, sécurisé et flexible qui s'intègre bien dans les flux de travail de développement et de production. Son architecture sans démon et son intégration profonde avec systemd en font un excellent choix pour les environnements centrés sur Linux, tandis que son API compatible avec Docker garantit une courbe d'apprentissage douce pour les utilisateurs existants. Que vous exécutiez un seul conteneur sur un ordinateur portable ou que vous orchestriez une flotte de pods dans un pipeline CI, Podman fournit les outils dont vous avez besoin sans la surcharge d'un démon central.