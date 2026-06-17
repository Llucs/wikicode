---
title: ArgoCD – Livraison continue GitOps pour Kubernetes
description: ArgoCD est un outil de livraison continue déclaratif et piloté par GitOps qui synchronise les applications Kubernetes avec des dépôts Git comme source unique de vérité.
created: 2026-06-15
tags:
  - gitops
  - kubernetes
  - continuous-delivery
  - argocd
  - devops-tools
status: draft
ecosystem: kubernetes
---

# ArgoCD – Livraison continue GitOps pour Kubernetes

## Qu'est-ce qu'ArgoCD ?

ArgoCD est un outil de livraison continue (CD) déclaratif, **GitOps**, conçu spécifiquement pour Kubernetes. Il traite les dépôts Git comme la **source unique de vérité** pour les définitions d'applications et les manifests Kubernetes. ArgoCD surveille en permanence l'état en direct du cluster et le rapproche de l'état souhaité défini dans Git, permettant des déploiements entièrement automatisés, audités et reproductibles.

## Pourquoi ArgoCD ?

- **Déclaratif et versionné** – Toutes les configurations d'infrastructure et d'application résident dans Git. Les modifications sont effectuées via des pull requests, et non par des commandes impératives.
- **Auto‑réparation automatique** – Le système corrige automatiquement la dérive de configuration en annulant toute modification manuelle pour revenir à ce qui est défini dans Git.
- **Piste d'audit** – Chaque déploiement est capturé dans l'historique Git, fournissant un journal d'audit immuable.
- **Gestion multi‑cluster** – Une seule instance d'ArgoCD peut gérer des applications sur des centaines de clusters Kubernetes.
- **Agnostique en gestion de configuration** – Fonctionne avec YAML simple, Helm, Kustomize, Jsonnet, etc.

## Installation

ArgoCD peut être installé sur n'importe quel cluster Kubernetes en quelques minutes.

### 1. Créer le namespace et appliquer le manifest

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. Accéder au serveur API (port‑forward)

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Vous pouvez maintenant accéder à l'interface web à l'adresse `https://localhost:8080`.

### 3. Récupérer le mot de passe admin initial

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

### 4. Se connecter via la CLI

```bash
argocd login localhost:8080
```

Utilisez le nom d'utilisateur `admin` et le mot de passe de l'étape précédente.

## Utilisation de base

### Connecter un dépôt Git

```bash
argocd repo add https://github.com/my-org/my-app.git
```

### Enregistrer un cluster cible

Si le cluster cible n'est pas le même que celui sur lequel ArgoCD s'exécute, enregistrez-le :

```bash
argocd cluster add <kube-context-name>
```

### Définir une application (YAML déclaratif)

Créez un fichier `nginx-app.yaml` :

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: nginx-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/my-org/nginx.git'
    path: production
    targetRevision: HEAD
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

Appliquez-le :

```bash
kubectl apply -f nginx-app.yaml
```

### Synchroniser une application

Synchronisation manuelle (ou la politique de synchronisation automatique s'en chargera) :

```bash
argocd app sync nginx-prod
```

Une synchronisation peut également être déclenchée depuis l'interface web ou via un webhook provenant de votre fournisseur Git.

## Fonctionnalités clés et commandes

### Synchronisation automatique et auto‑réparation

- **Auto‑Sync** – ArgoCD peut automatiquement lancer une synchronisation à chaque nouveau commit poussé sur la branche suivie.
- **Self‑Heal** – Si quelqu'un modifie manuellement des ressources dans le cluster, ArgoCD les ramène à l'état défini dans Git.

Configurez dans le YAML sous `syncPolicy.automated` ou via la CLI :

```bash
argocd app set nginx-prod --sync-policy automated --auto-prune --self-heal
```

### Gestion multi‑cluster

Utilisez une seule instance d'ArgoCD pour déployer sur de nombreux clusters avec des namespaces différents. Lister les clusters :

```bash
argocd cluster list
```

### Application Sets (CRD)

Génération dynamique d'applications basée sur des paramètres (par exemple, pour chaque cluster, pour chaque branche, ou à partir d'une liste de générateurs). Exemple utilisant un générateur Git :

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: my-apps
spec:
  generators:
  - git:
      repoURL: 'https://github.com/my-org/deploy-config.git'
      revision: HEAD
      files:
        - path: "clusters/*/config.json"
  template:
    metadata:
      name: '{{ cluster }}-my-app'
    spec:
      project: default
      source:
        repoURL: 'https://github.com/my-org/my-app.git'
        targetRevision: HEAD
        path: '{{ env }}'
      destination:
        server: '{{ server }}'
        namespace: '{{ namespace }}'
```

### Outils de gestion de configuration

ArgoCD génère nativement les manifests à partir de :

- **Helm** – Utilisez `helm.parameters` ou `helm.valueFiles`
- **Kustomize** – Pointez simplement vers le répertoire de superposition Kustomize
- **Jsonnet** – Via un fichier `jsonnet.libsonnet`

### Vagues de synchronisation et hooks

Contrôlez l'ordre du déploiement des ressources :

- **Sync Waves** – Définissez l'annotation `argocd.argoproj.io/sync-wave` avec un entier (les nombres plus petits se déploient en premier).
- **Sync Hooks** – Exécutez des jobs (pre‑sync, sync, post‑sync, etc.) pour les migrations de base de données ou la validation.

### Notifications et webhooks

- **Notifications intégrées** – Envoyez des alertes vers Slack, par e-mail ou vers des points de terminaison personnalisés lorsque l'état de synchronisation change.
- **Déclencheurs webhook** – Intégrez-vous avec GitHub/GitLab/Bitbucket pour une synchronisation quasi instantanée lors d'un push.

### Image Updater (composant optionnel)

Mettez automatiquement à jour le tag de l'image conteneur dans Git lorsqu'une nouvelle image est poussée vers un registre. Ce composant (Argo CD Image Updater) surveille votre registre de conteneurs et commit le nouveau tag dans la source Git.

## Architecture – Composants de haut niveau

- **Serveur API** – Expose les points de terminaison de l'API, de l'interface web et de la CLI ; gère l'authentification, le RBAC et la gestion de projets.
- **Serveur de dépôt** – Met en cache les dépôts Git et génère les manifests Kubernetes (par exemple, rend les charts Helm, les superpositions Kustomize).
- **Contrôleur d'application** – Surveille en permanence l'état en direct des applications et le compare à l'état souhaité provenant du serveur de dépôt ; déclenche les opérations de synchronisation, de nettoyage et d'auto‑réparation.

## Résumé

ArgoCD transforme les déploiements Kubernetes en un workflow entièrement automatisé et piloté par Git. En faisant de Git la source de vérité, il élimine la dérive de configuration, fournit une piste d'audit immuable et permet une infrastructure auto‑réparatrice. Avec la prise en charge intégrée de Helm, Kustomize, la gestion multi‑cluster et les Application Sets dynamiques, il est le standard de facto pour GitOps sur Kubernetes.

Pour la documentation officielle, visitez [argoproj.github.io/argo-cd](https://argoproj.github.io/argo-cd/).