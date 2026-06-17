---
title: Portainer
description: Un outil de gestion de conteneurs et d'orchestration auto-hébergé qui centralise la gouvernance, le contrôle RBAC/SSO et le contrôle opérationnel sur plusieurs environnements.
created: 2026-06-15
tags:
  - docker
  - kubernetes
  - container-management
  - devops
  - open-source
  - orchestration
  - self-hosted
  - portainer-ce
status: draft
ecosystem: containers
---

# Portainer

## Overview

Portainer est le standard de l'industrie, une interface unique (single pane of glass) open-source pour la gestion d'environnements conteneurisés. Conçu par Neil Cresswell et fork de DockerUI en 2017, Portainer vise à éliminer la courbe d'apprentissage abrupte et la charge opérationnelle de Docker, Docker Swarm, Kubernetes, Azure ACI et Hashicorp Nomad. Il s'exécute lui-même sous forme d'un conteneur léger (ou via un chart Helm) et expose une interface web puissante soutenue par une API REST complète.

Portainer est sous licence AGPLv3 pour la Community Edition (CE), avec une Business Edition (BE) commerciale qui ajoute des fonctionnalités d'entreprise comme la conformité FIPS, un contrôle RBAC granulaire et un support dédié.

## Why Portainer?

- **Plan de contrôle unifié :** Gérez tous les moteurs de conteneurs de votre parc depuis une seule interface web, sans avoir à changer de contexte entre plusieurs CLI.
- **Complexité réduite :** Les équipes non spécialistes peuvent déployer et gérer des applications sans apprendre des commandes complexes `kubectl` ou `docker-compose`.
- **Prêt pour le GitOps :** Les stacks peuvent être liées directement à des dépôts Git. Tout push sur le dépôt déclenche un redéploiement automatique.
- **Edge Compute :** Gérez en toute sécurité des milliers d'appareils derrière un NAT ou des pare-feux en utilisant des Edge Agents.
- **Léger et non intrusif :** Portainer ne remplace pas votre orchestrateur existant ; il se place à côté, lisant l'API Docker/Kubernetes via un socket ou un conteneur Agent dédié.

## Architecture

Portainer utilise un modèle standard serveur-agent :

1.  **Portainer Server (portainer/portainer-ce) :** L'application principale. Elle sert l'interface Web et l'API REST. C'est le nœud vers lequel vous pointez votre navigateur.
2.  **Portainer Agent (portainer/agent) :** Un conteneur sidecar léger déployé sur chaque hôte Docker ou nœud Kubernetes que vous souhaitez gérer à distance. L'Agent communique avec le socket Docker local et expose une API sécurisée sur le port 9001.
3.  **Edge Agent :** Une variante de l'agent standard conçue pour les sites distants. Il initie un tunnel *sortant* vers le Portainer Server, permettant la gestion à travers des pare-feux stricts sans ouvrir de ports entrants.

```text
[Admin Browser] <--> [Portainer Server :9443]
                         |
            +------------+-------------+
            |            |             |
    [Docker Agent 1] [Docker Agent 2] [K8s Cluster (Helm)]
            |            |
    [Docker Daemon] [Docker Daemon]
```

## Installation

### Docker Autonome (Démarrage rapide)

Il s'agit de la méthode la plus courante pour gérer un hôte Docker local ou un petit nombre d'hôtes Docker.

```bash
# Create a persistent volume for Portainer data
docker volume create portainer_data

# Run the Portainer Server container
docker run -d -p 8000:8000 -p 9443:9443 --name portainer \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v portainer_data:/data \
    portainer/portainer-ce:lts
```

- `-p 9443:9443` : Interface Web et API (HTTPS).
- `-p 8000:8000` : (Optionnel) Tunnel TCP pour les connexions Edge Agent.
- `-v /var/run/docker.sock` : Permet à Portainer de gérer l'hôte sur lequel il s'exécute.
- `:lts` : Le tag Long Term Support. **Utilisez toujours `:lts` en production.**

### Docker Swarm

Déployez Portainer en tant que service global sur votre cluster Swarm.

```bash
curl -L https://downloads.portainer.io/ce2-19/portainer-agent-stack.yml -o portainer-agent-stack.yml

docker stack deploy -c portainer-agent-stack.yml portainer
```

### Kubernetes (Helm)

Déployez Portainer dans votre cluster Kubernetes à l'aide du chart Helm officiel.

```bash
helm repo add portainer https://portainer.github.io/k8s/
helm repo update

helm upgrade --install portainer portainer/portainer \
    --namespace portainer --create-namespace \
    --set service.type=LoadBalancer \
    --set service.httpPort=9000 \
    --set service.httpsPort=9443
```

### Installation Air-Gapped

Pour les environnements sans accès Internet, pré-tirez les images.

```bash
# On a machine with internet access
docker pull portainer/portainer-ce:lts
docker pull portainer/agent:lts

# Tag and push to your internal registry
docker tag portainer/portainer-ce:lts <internal-registry>/portainer-ce:lts
docker tag portainer/agent:lts <internal-registry>/agent:lts
docker push <internal-registry>/portainer-ce:lts
docker push <internal-registry>/agent:lts
```

## Initial Setup

1.  Ouvrez un navigateur à l'adresse `https://<SERVER_IP>:9443`.
2.  Créez un mot de passe fort pour l'utilisateur `admin`.
3.  L'assistant de configuration rapide apparaît. Sélectionnez **Docker** et choisissez **Socket** pour vous connecter au daemon Docker local.
4.  Cliquez sur **Connect**. Vous êtes maintenant sur la page **Home** — c'est votre sélecteur d'environnement.

## Key Features & Command Examples

### 1. Multi-Environment Management

Connectez des hôtes Docker distants en déployant le Portainer Agent.

**Sur l'hôte distant (cible) :**
```bash
docker run -d -p 9001:9001 --name portainer_agent \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /var/lib/docker/volumes:/var/lib/docker/volumes \
    portainer/agent:lts
```

**Sur l'interface du Portainer Server :**
Naviguez jusqu'à **Environments** > **Add Environment** > **Docker Agent**.
Saisissez l'IP et le port (9001) de l'hôte distant. Cliquez sur **Connect**.

### 2. App Templates (Déploiement en un clic)

Portainer inclut un catalogue d'applications prédéfinies (Nginx, MySQL, WordPress, etc.).

**Flux de travail :**
1. Barre latérale > **App Templates**.
2. Cliquez sur un modèle (par ex. **Nginx**).
3. Personnalisez le nom, les ports, les variables d'environnement.
4. Cliquez sur **Deploy the stack**.

### 3. Stacks & GitOps

Déployez des applications complexes à l'aide de fichiers Docker Compose ou de manifestes Kubernetes. Les stacks peuvent être liées à un dépôt Git pour des workflows GitOps.

**Déploiement manuel Compose :**
Collez ceci dans **Stacks** > **Add Stack** > **Web Editor** :
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
  db:
    image: postgres:13
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: example
volumes:
  pgdata:
```

**Configuration GitOps :**
1. **Stacks** > **Add Stack** > **Repository**.
2. Saisissez l'URL du dépôt Git et le chemin vers le fichier Compose.
3. Activez **Automatic Updates**.
4. Cliquez sur **Deploy the stack**. Tout `git push` déclenche un redéploiement.

### 4. Kubernetes Management

Portainer abstrait la complexité de `kubectl`. Vous pouvez créer des Namespaces, Deployments, Services et Ingresses via un formulaire ou du YAML.

**Exemple :** Déploiement d'une charge de travail nginx simple.
1. **Environments** > Sélectionnez votre **Kubernetes cluster**.
2. **Kubernetes** > **Workloads** > **Add Workload**.
3. Remplissez le formulaire (Name: `nginx`, Image: `nginx:alpine`, Port: `80`).
4. Cliquez sur **Deploy**.

### 5. Registries

Gérez centralement les identifiants pour Docker Hub, GitLab, Quay, Amazon ECR et Google Container Registry.

1. **Registries** > **Add Registry**.
2. Choisissez votre fournisseur (par ex. **Docker Hub**).
3. Saisissez vos identifiants (nom d'utilisateur/jeton d'accès).

### 6. Edge Compute

Gérez des appareils distants (IoT, commerce de détail, sites distants) derrière un NAT ou des pare-feux. Le serveur génère un `EDGE_ID` et une `EDGE_KEY`.

**Sur l'appareil Edge :**
```bash
docker run -d \
  -e EDGE=1 \
  -e EDGE_ID=<EDGE_ID> \
  -e EDGE_KEY=<EDGE_KEY> \
  -e CAP_HOST_MANAGEMENT=1 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name portainer_edge_agent \
  portainer/agent:lts
```

### 7. REST API

Portainer dispose d'une API REST riche. Générez une clé API dans **Settings** > **Security**.

```bash
# List all environments
curl -X GET 'https://<SERVER_IP>:9443/api/endpoints' \
    -H 'X-API-Key: ptr_xxxxxxxxxxxx' | jq .

# Deploy a stack
curl -X POST 'https://<SERVER_IP>:9443/api/stacks' \
    -H 'X-API-Key: ptr_xxxxxxxxxxxx' \
    -H 'Content-Type: application/json' \
    -d '{
      "Name": "my-api-stack",
      "StackFileContent": "version: \"3.8\"\nservices:\n  web:\n    image: nginx:alpine",
      "SwarmID": "",
      "EndpointID": 1
    }'
```

## Editions Compared

| Fonctionnalité | Community Edition (CE) | Business Edition (BE) |
|---|---|---|
| Licence | AGPLv3 | Commerciale |
| Multi-environnement | Illimité | Illimité |
| GitOps | Oui | Oui |
| Edge Compute | Limité | Complet (Edge Groups, Stacks, Jobs) |
| RBAC / SSO | Basique | Avancé (AD/LDAP/OAuth, Team Roles, Resource Controls) |
| Gestion des registres | Manuelle | Centralisée avec gouvernance |
| Support | Communauté | Commercial (24/7/365) |
| Conformité FIPS | Non | Oui |

## Best Practices

1.  **Utilisez les versions `:lts`.** N'utilisez pas le tag `:latest` en production ; il correspond à des versions de pointe sujettes à des changements rapides.
2.  **Dédiez le nœud Server.** N'exécutez pas des dizaines de charges de travail sur le conteneur Portainer Server. Utilisez-le strictement comme point de gestion.
3.  **Sauvegardez régulièrement `portainer_data`.** Exécutez ceci pour sauvegarder le volume :
    ```bash
    docker run --rm -v portainer_data:/data -v $(pwd):/backup alpine tar cvf /backup/portainer_backup.tar /data
    ```
4.  **Sécurisez avec un TLS approprié.** Remplacez le certificat auto-signé en production.
    ```bash
    docker run -d -p 9443:9443 --name portainer \
        -v /path/to/fullchain.pem:/certs/portainer.crt \
        -v /path/to/privkey.pem:/certs/portainer.key \
        -v portainer_data:/data \
        portainer/portainer-ce:lts
    ```

## Troubleshooting

### Échecs de connexion de l'Agent
- Assurez-vous que le port `9001` est ouvert sur la machine cible.
- Vérifiez que le conteneur Portainer Agent est en cours d'exécution.
- Si vous utilisez un pare-feu, assurez-vous que le Server peut initier des connexions sortantes vers l'Agent.

### Mot de passe admin oublié
Un conteneur d'assistance génère un hash que vous pouvez définir de manière sécurisée.
```bash
docker run --rm -v portainer_data:/data portainer/helper-reset-password
```

### Portainer ne démarre pas
Consultez les logs :
```bash
docker logs portainer
```
Les problèmes courants incluent des données de volume corrompues, des versions de Portainer incompatibles, ou des erreurs de permissions du daemon Docker hôte.

## References

- **Site officiel :** [https://www.portainer.io/](https://www.portainer.io/)
- **GitHub :** [https://github.com/portainer/portainer](https://github.com/portainer/portainer)
- **Documentation officielle :** [https://docs.portainer.io/](https://docs.portainer.io/)
- **Docker Hub :** [portainer/portainer-ce](https://hub.docker.com/r/portainer/portainer-ce)
- **Communauté Slack :** [Portainer Slack](https://portainer.io/slack)