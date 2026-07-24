---
title: Déploiements sans interruption
description: Un guide complet pour mettre en œuvre des déploiements sans interruption avec les stratégies blue/green, canary et rolling updates.
created: 2026-07-24
tags:
  - DevOps
  - Déploiement
  - Sans Interruption
status: brouillon
---

# Déploiements sans interruption

Un déploiement sans interruption est une pratique de génie logiciel qui garantit que le service ou l'application reste disponible pour les utilisateurs pendant le processus de déploiement. Cette technique implique des stratégies pour minimiser ou éliminer toute perturbation de l'accessibilité du service lorsque de nouvelles versions de code ou de configurations sont déployées. L'objectif est de maintenir l'accessibilité du service, même pendant les mises à jour de logiciel ou les activités de maintenance.

## Caractéristiques clés

1. **Découverte de services et équilibrage de charge :** Utilise des mécanismes comme le DNS, le service mesh ou l'équilibrage de charge pour diriger le trafic vers différentes instances.
2. **Déploiements blue/green :** Déploie deux environnements identiques (bleu et vert), permettant de diriger le trafic entre eux sans interruption de service.
3. **Déploiements canary :** Déploie progressivement de nouvelles versions à un petit ensemble d'utilisateurs pour tester les problèmes avant de les déployer à l'ensemble de l'audience.
4. **Mises à jour en rafale :** Met à jour progressivement des instances individuelles ou des groupes d'instances pour s'assurer que nulle point de faiblesse ne soit atteint.
5. **Architecture microservices :** Décompose l'application en services plus petits, plus facilement déployables, pour assurer que les échecs dans un seul service ne perturbent pas les autres.

## Installation

L'installation de outils et de stratégies de déploiement sans interruption dépend de l'environnement et des technologies utilisées. Voici quelques étapes générales :

1. **Configuration de l'environnement :**
   - Mettre en place un équilibrage de charge ou un service mesh pour gérer la redirigation du trafic.
   - Configurer le DNS pour la découverte de services et le redoublement de service.

2. **Déploiements blue/green :**
   - Déploie une nouvelle version de l'application dans un nouvel environnement.
   - Utilisez l'équilibrage de charge pour diriger le trafic entre l'environnement existant et le nouvel environnement.
   - Une fois que le nouvel environnement a été vérifié, dirigez complètement le trafic.

3. **Déploiements canary :**
   - Déploie une nouvelle version à un petit ensemble d'utilisateurs ou à une région spécifique.
   - Surveillez la performance et les retours des utilisateurs.
   - Augmentez progressivement la proportion d'utilisateurs ou de régions recevant la nouvelle version.

4. **Mises à jour en rafale :**
   - Mettez à jour une instance à la fois ou par lots.
   - Surveillez les problèmes et effectuez un rollback si nécessaire.
   - Augmentez progressivement les instances mises à jour.

5. **Microservices :**
   - Utilisez un service mesh ou un outil d'orchestration (comme Kubernetes) pour gérer le déploiement des services individuels.
   - Assurez-vous que chaque service puisse être déployé et échelonné indépendamment.

## Utilisation de base

1. **Planifiez votre déploiement :**
   - Définissez la stratégie (blue/green, canary, mises à jour en rafale).
   - Prévoyez les problèmes potentiels et prévoyez des stratégies de rollback.

2. **Préparez la nouvelle version de déploiement :**
   - Testez la nouvelle version de manière exhaustive.
   - Assurez-vous que toutes les dépendances sont correctement configurées.

3. **Déploiez la nouvelle version :**
   - Utilisez la stratégie choisie pour déployer la nouvelle version.
   - Surveillez le processus de déploiement pour toute anomalie.

4. **Vérifiez et échelonnez :**
   - Surveillez la nouvelle version pour sa stabilité et sa performance.
   - Augmentez progressivement l'échelonnement de la nouvelle version et retirez progressivement l'ancienne version.

5. **Documentez et apprenez :**
   - Documentez le processus de déploiement et les leçons apprises.
   - Améliorez continuellement la stratégie de déploiement en fonction de l'expérience.

### Exemple : Déploiements blue/green avec Kubernetes

#### Prérequis
- Cluster Kubernetes avec `kubectl` installé et configuré.
- Deux environnements identiques : `bleu` et `vert`.

#### Étape 1 : Définir les manifests de déploiement

Créez deux fichiers de déploiement, un pour chaque environnement.

**Déploiement bleu :**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-bleu
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: bleu
  template:
    metadata:
      labels:
        app: my-app
        version: bleu
    spec:
      containers:
      - name: my-app
        image: my-app:bleu
        ports:
        - containerPort: 80
```

**Déploiement vert :**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-vert
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: vert
  template:
    metadata:
      labels:
        app: my-app
        version: vert
    spec:
      containers:
      - name: my-app
        image: my-app:vert
        ports:
        - containerPort: 80
```

#### Étape 2 : Déploiement de l'environnement bleu

```bash
kubectl apply -f bleu-deployment.yaml
```

#### Étape 3 : Créer un service pour l'équilibrage de charge

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: my-app
```

Appliquez le manifeste du service :

```bash
kubectl apply -f service.yaml
```

#### Étape 4 : Rediriger le trafic vers l'environnement vert

Mettez à jour le service pour diriger le trafic vers l'environnement vert :

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: my-app
    version: vert
```

Appliquez le manifeste mis à jour :

```bash
kubectl apply -f service.yaml
```

#### Étape 5 : Vérifiez le déploiement

Vérifiez les pods et le statut du service :

```bash
kubectl get pods
kubectl get services
```

Une fois vérifié, vous pouvez rediriger le trafic de nouveau vers l'environnement bleu si nécessaire.

### Exemple : Déploiements canary

#### Prérequis
- Cluster Kubernetes avec `kubectl` installé et configuré.
- Deux déploiements : `stables` et `canary`.

#### Étape 1 : Définir les manifests de déploiement

Créez deux fichiers de déploiement, un pour chaque environnement.

**Déploiement stable :**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-stable
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: stable
  template:
    metadata:
      labels:
        app: my-app
        version: stable
    spec:
      containers:
      - name: my-app
        image: my-app:stable
        ports:
        - containerPort: 80
```

**Déploiement canary :**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-canary
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: canary
  template:
    metadata:
      labels:
        app: my-app
        version: canary
    spec:
      containers:
      - name: my-app
        image: my-app:canary
        ports:
        - containerPort: 80
```

#### Étape 2 : Déploiement de l'environnement stable

```bash
kubectl apply -f stable-deployment.yaml
```

#### Étape 3 : Créer un service pour l'équilibrage de charge

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: my-app
```

Appliquez le manifeste du service :

```bash
kubectl apply -f service.yaml
```

#### Étape 4 : Déploiement de l'environnement canary

```bash
kubectl apply -f canary-deployment.yaml
```

#### Étape 5 : Rediriger le trafic vers l'environnement canary

Mettez à jour le service pour diriger le trafic vers l'environnement canary :

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: my-app
    version: canary
```

Appliquez le manifeste mis à jour :

```bash
kubectl apply -f service.yaml
```

#### Étape 6 : Vérifiez le déploiement

Vérifiez les pods et le statut du service :

```bash
kubectl get pods
kubectl get services
```

Une fois vérifié, augmentez progressivement le trafic canary :

```bash
kubectl patch service my-app-service -p '{"spec":{"selector":{"app":"my-app","version":"canary"}}}'
```

Surveillez l'environnement canary pour tout problème et augmentez progressivement le trafic canary jusqu'à ce qu'il atteigne 100%.

### Conclusion

Les déploiements sans interruption sont essentiels pour maintenir la fiabilité et l'accessibilité des systèmes distribués. En utilisant des stratégies efficaces, des techniques de mise en œuvre et les outils appropriés, les organisations peuvent réaliser des mises à jour sans interruption et sans interrompre l'expérience utilisateur. Ce guide fournit un aperçu complet des stratégies blue/green, canary et en rafale, ainsi que des exemples pratiques à l'aide de Kubernetes.

---