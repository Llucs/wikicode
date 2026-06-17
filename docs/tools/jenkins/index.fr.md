---
title: Serveur d'automatisation Jenkins CI/CD
description: Un serveur d'automatisation pour l'intégration continue et la livraison continue de projets logiciels.
created: 2026-06-15
tags:
  - jenkins
  - ci
  - cd
  - devops
  - automation
  - java
status: draft
ecosystem: ci-cd
---

# Serveur d'automatisation Jenkins CI/CD

## Qu'est-ce que c'est ?

Jenkins est un serveur d'automatisation open-source écrit en Java. Il est utilisé pour automatiser la construction, les tests et le déploiement de logiciels, permettant l'intégration continue (CI) et la livraison continue (CD). Initialement issu d'un fork du projet Hudson, Jenkins est désormais la norme industrielle pour l'orchestration de pipelines.

## Pourquoi Jenkins ?

- **Extensibilité :** Plus de 1 800 plugins permettent l'intégration avec pratiquement tous les outils DevOps (Git, Docker, Kubernetes, AWS, Azure, Slack, etc.).
- **Flexibilité :** Prend en charge les tâches freestyle simples jusqu'aux pipelines multi-étapes complexes définis comme du code.
- **Constructions distribuées :** L'architecture master/agent permet de répartir les charges de travail sur plusieurs machines.
- **Open Source et mature :** Gratuit (licence MIT) avec une énorme communauté et une documentation complète.
- **Écosystème riche :** Plugins pour SCM, outils de construction, rapports de tests, gestion des artefacts, déploiement et notification.

## Installation

Jenkins nécessite Java 8, 11 ou 17 (LTS recommandé). Plusieurs méthodes d'installation existent :

### Fichier WAR

```bash
java -jar jenkins.war
```
Exécute Jenkins de manière autonome sur le port 8080. Idéal pour des tests rapides.

### Paquets natifs

**Debian/Ubuntu :**

```bash
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins
```

**Red Hat/CentOS :**

```bash
sudo wget -O /etc/yum.repos.d/jenkins.repo \
  https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
sudo yum install jenkins
```

### Docker

```bash
docker run -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

### Kubernetes (Helm Chart)

```bash
helm repo add jenkins https://charts.jenkins.io
helm repo update
helm install jenkins jenkins/jenkins --namespace jenkins --create-namespace
```

Après l'installation, accédez à Jenkins à l'adresse `http://localhost:8080` et récupérez le mot de passe administrateur initial depuis les logs ou le fichier (`/var/lib/jenkins/secrets/initialAdminPassword`).

## Utilisation de base

### 1. Créer un Job

- **Freestyle project :** Tâches simples avec quelques étapes.
- **Pipeline :** Définir le cycle de vie de construction dans un `Jenkinsfile`.

### 2. Configurer le code source

- Connectez-vous à un dépôt Git en utilisant des credentials (nom d'utilisateur/mot de passe ou clé SSH).

### 3. Définir les déclencheurs

- **Poll SCM :** `* * * * *` (chaque minute)
- **Webhook :** Depuis GitHub/GitLab lors d'un push.
- **Cron :** par ex., `H 2 * * 1-5` (les jours de semaine à 2h du matin)

### 4. Ajouter des étapes de construction

- Exécuter des commandes shell/batch.
- Lancer des goals Maven/Gradle.
- Construire des images Docker.
- Invoquer d'autres outils de construction.

### 5. Actions post-construction

- Archiver les artefacts (par ex., JARs, rapports).
- Publier les résultats de tests (JUnit, rapports HTML).
- Déployer sur des serveurs.
- Envoyer des notifications (Slack, email).

## Fonctionnalités clés avec exemples

### Pipeline as Code

`Jenkinsfile` déclaratif dans le dépôt source :

```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                sh 'mvn clean compile'
            }
        }
        stage('Test') {
            steps {
                sh 'mvn test'
            }
            post {
                always {
                    junit 'target/surefire-reports/*.xml'
                }
            }
        }
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh 'mvn deploy'
            }
        }
    }
    post {
        failure {
            slackSend channel: '#ops', message: "Build failed."
        }
    }
}
```

Ce pipeline s'exécute automatiquement à chaque commit, compile le code, exécute les tests, archive les résultats des tests et déploie depuis `main`.

### Multibranch Pipeline

Crée automatiquement un pipeline pour chaque branche et pull request dans un repository.

```groovy
// In Jenkins UI: New Item → Multibranch Pipeline → add Git source
// The Jenkinsfile from the branch controls execution.
```

### Constructions distribuées avec des Agents

Jenkins peut étiqueter des agents (par ex., "linux", "docker", "high-mem") et leur assigner des jobs :

```groovy
pipeline {
    agent { label 'linux && docker' }
    stages {
        stage('Test') {
            steps {
                sh 'docker build -t myapp .'
            }
        }
    }
}
```

### Shared Libraries

Code de pipeline réutilisable dans plusieurs dépôts. Définir dans un dépôt Git de shared library :

**vars/buildApp.groovy:**

```groovy
def call(String project) {
    sh "mvn -f ${project}/pom.xml clean package"
}
```

Puis dans n'importe quel `Jenkinsfile` :

```groovy
library identifier: 'my-lib@master', retriever: modernSCM(...)
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                buildApp('my-service')
            }
        }
    }
}
```

### Intégration avec Kubernetes

Utiliser le plugin Kubernetes pour créer dynamiquement des agents de construction :

```groovy
pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: maven
    image: maven:3.8.4-openjdk-11
    command: ['cat']
    tty: true
"""
        }
    }
    stages {
        stage('Build') {
            steps {
                container('maven') {
                    sh 'mvn clean install'
                }
            }
        }
    }
}
```

### REST API

Jenkins fournit une API REST complète pour l'automatisation. Exemple curl pour déclencher un job :

```bash
curl -X POST http://jenkins-url/job/my-job/build \
  --user username:api-token
```

Lister les jobs :

```bash
curl http://jenkins-url/api/json
```

### Blue Ocean UI

Interface visuelle moderne pour les pipelines (nécessite le plugin Blue Ocean). Fournit une vue graphique des constructions, logs et étapes de pipeline.

## Configuration as Code (JCasC)

Gérez la configuration de Jenkins de manière déclarative avec YAML en utilisant le plugin `configuration-as-code`.

**jenkins.yaml:**

```yaml
jenkins:
  systemMessage: "Managed by JCasC"
  numExecutors: 2
  globalNodeProperties:
  - envVars:
      env:
      - key: VARIABLE1
        value: "value1"
security:
  globalMatrixAuthorizationStrategy:
    grantedPermissions:
      - "Overall/Administer:admin"
      - "Job/Build:developer"
jobs:
  - script: >
      multibranchPipelineJob('my-pipeline') {
        branchSources {
          git {
            remote('https://github.com/org/repo.git')
            credentialsId('github-creds')
          }
        }
      }
```

Appliquez au démarrage ou via le endpoint `reload-configuration-as-code`.

## Plugins

Catégories de plugins clés :

- **SCM :** Git, GitHub, GitLab, Bitbucket, Subversion.
- **Build :** Maven, Gradle, Ant, NodeJS, Docker Pipeline.
- **Test :** JUnit, HTML Publisher, Allure, Cucumber Reports.
- **Deploy :** Kubernetes, AWS CodeDeploy, Ansible, SSH.
- **Notification :** Slack, Email Extension, PagerDuty.
- **Utility :** Credentials Binding, Pipeline Utility Steps, Job DSL.

## Bonnes pratiques

- **Utiliser Pipeline as Code** – Stockez le `Jenkinsfile` dans le SCM avec le projet.
- **Utiliser les Shared Libraries** – Évitez de dupliquer la logique des pipelines.
- **Garder les Agents sans état** – Utilisez des agents Docker ou Kubernetes.
- **Sécuriser les Credentials** – Utilisez le plugin Credentials, pas de texte en clair.
- **Sauvegarder JENKINS_HOME** – Sauvegardez régulièrement les configurations de jobs et les données des plugins.
- **Limiter la concurrence** – Utilisez `properties([disableConcurrentBuilds()])` pour les jobs sensibles aux ressources.
- **Utiliser Blue Ocean** pour une meilleure visualisation des pipelines.
- **Surveiller avec Prometheus** via le plugin Prometheus Metrics.

## Dépannage

- **Vérifier les logs :** `tail -f /var/log/jenkins/jenkins.log`
- **Recharger la configuration :** `Manage Jenkins → Reload Configuration from Disk`
- **Vider la file d'attente des constructions :** Cliquez sur l'élément de la file d'attente → "Cancel"
- **Exécuter un script Groovy :** `Manage Jenkins → Script Console` pour le diagnostic.
- **Augmenter la taille du tas :** Définissez `JAVA_OPTS="-Xmx2048m -Xms1024m"` au démarrage.

## Liens

- [Documentation officielle Jenkins](https://www.jenkins.io/doc/)
- [Index des plugins](https://plugins.jenkins.io/)
- [Générateur de syntaxe Pipeline](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Documentation JCasC](https://www.jenkins.io/projects/jcasc/)

---

*Cette page a été créée dans le cadre de la documentation WikiCode pour les équipes de développement.*