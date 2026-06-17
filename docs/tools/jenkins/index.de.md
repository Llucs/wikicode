---
title: Jenkins CI/CD-Automatisierungsserver
description: Ein Automatisierungsserver für kontinuierliche Integration und kontinuierliche Auslieferung von Softwareprojekten.
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

# Jenkins CI/CD-Automatisierungsserver

## Was es ist

Jenkins ist ein quelloffener Automatisierungsserver, der in Java geschrieben ist. Er wird verwendet, um das Erstellen, Testen und Bereitstellen von Software zu automatisieren und ermöglicht Continuous Integration (CI) und Continuous Delivery (CD). Ursprünglich aus dem Hudson-Projekt hervorgegangen, ist Jenkins heute der Industriestandard für Pipeline-Orchestrierung.

## Warum Jenkins?

- **Erweiterbarkeit:** Über 1.800 Plugins ermöglichen die Integration mit nahezu jedem DevOps-Tool (Git, Docker, Kubernetes, AWS, Azure, Slack, usw.).
- **Flexibilität:** Unterstützt einfache Freestyle-Jobs bis hin zu komplexen mehrstufigen Pipelines, die als Code definiert sind.
- **Verteilte Builds:** Die Master/Agent-Architektur ermöglicht die Verteilung von Arbeitslasten auf viele Maschinen.
- **Open Source und ausgereift:** Kostenlos (MIT-Lizenz) mit einer riesigen Community und umfangreicher Dokumentation.
- **Reichhaltiges Ökosystem:** Plugins für SCM, Build-Tools, Testberichte, Artefaktverwaltung, Bereitstellung und Benachrichtigungen.

## Installation

Jenkins erfordert Java 8, 11 oder 17 (LTS empfohlen). Es gibt mehrere Installationsmethoden:

### WAR-Datei

```bash
java -jar jenkins.war
```
Führt Jenkins eigenständig auf Port 8080 aus. Ideal für schnelle Tests.

### Native Pakete

**Debian/Ubuntu:**

```bash
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins
```

**Red Hat/CentOS:**

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

Nach der Installation greifen Sie auf Jenkins unter `http://localhost:8080` zu und holen Sie das anfängliche Admin-Passwort aus den Logs oder der Datei (`/var/lib/jenkins/secrets/initialAdminPassword`) ab.

## Grundlegende Verwendung

### 1. Einen Job erstellen

- **Freestyle-Projekt:** Einfache Aufgaben mit wenigen Schritten.
- **Pipeline:** Definieren Sie den Build-Lebenszyklus in einer `Jenkinsfile`.

### 2. Quellcode konfigurieren

- Verbinden Sie sich mit einem Git-Repository unter Verwendung von Anmeldeinformationen (Benutzername/Passwort oder SSH-Schlüssel).

### 3. Trigger einstellen

- **Poll SCM:** `* * * * *` (jede Minute)
- **Webhook:** Von GitHub/GitLab bei Push.
- **Cron:** z.B. `H 2 * * 1-5` (werktags um 2 Uhr morgens)

### 4. Build-Schritte hinzufügen

- Shell-/Batch-Befehle ausführen.
- Maven/Gradle-Ziele ausführen.
- Docker-Images erstellen.
- Andere Build-Werkzeuge aufrufen.

### 5. Post-Build-Aktionen

- Artefakte archivieren (z.B. JARs, Berichte).
- Testergebnisse veröffentlichen (JUnit, HTML-Berichte).
- Auf Server bereitstellen.
- Benachrichtigungen senden (Slack, E-Mail).

## Wichtige Funktionen mit Beispielen

### Pipeline as Code

Deklarative `Jenkinsfile` im Quellcode-Repository:

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

Diese Pipeline wird bei jedem Commit automatisch ausgeführt, kompiliert Code, führt Tests aus, archiviert Testergebnisse und stellt von `main` bereit.

### Multibranch-Pipeline

Erstellt automatisch eine Pipeline für jeden Branch und Pull-Request in einem Repository.

```groovy
// In Jenkins UI: New Item → Multibranch Pipeline → add Git source
// The Jenkinsfile from the branch controls execution.
```

### Verteilte Builds mit Agents

Jenkins kann Agents labeln (z.B. "linux", "docker", "high-mem") und Jobs ihnen zuweisen:

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

Wiederverwendbarer Pipeline-Code über Repositories hinweg. Definieren Sie in einem Shared-Library-Git-Repo:

**vars/buildApp.groovy:**

```groovy
def call(String project) {
    sh "mvn -f ${project}/pom.xml clean package"
}
```

Dann in jeder `Jenkinsfile`:

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

### Integration mit Kubernetes

Verwenden Sie das Kubernetes-Plugin, um Build-Agents dynamisch zu starten:

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

### REST-API

Jenkins bietet eine umfassende REST-API für die Automatisierung. Beispiel curl zum Auslösen eines Jobs:

```bash
curl -X POST http://jenkins-url/job/my-job/build \
  --user username:api-token
```

Jobs auflisten:

```bash
curl http://jenkins-url/api/json
```

### Blue Ocean UI

Moderne, visuelle Oberfläche für Pipelines (erfordert das Blue Ocean-Plugin). Bietet eine grafische Ansicht von Builds, Logs und Pipeline-Stufen.

## Configuration as Code (JCasC)

Verwalten Sie die Jenkins-Konfiguration deklarativ mit YAML unter Verwendung des `configuration-as-code`-Plugins.

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

Anwenden beim Start oder über den `reload-configuration-as-code`-Endpunkt.

## Plugins

Wichtige Plugin-Kategorien:

- **SCM:** Git, GitHub, GitLab, Bitbucket, Subversion.
- **Build:** Maven, Gradle, Ant, NodeJS, Docker Pipeline.
- **Test:** JUnit, HTML Publisher, Allure, Cucumber Reports.
- **Deploy:** Kubernetes, AWS CodeDeploy, Ansible, SSH.
- **Benachrichtigung:** Slack, Email Extension, PagerDuty.
- **Dienstprogramme:** Credentials Binding, Pipeline Utility Steps, Job DSL.

## Best Practices

- **Verwenden Sie Pipeline as Code** – Speichern Sie `Jenkinsfile` im SCM mit dem Projekt.
- **Verwenden Sie Shared Libraries** – Vermeiden Sie Duplikate von Pipeline-Logik.
- **Halten Sie Agents zustandslos** – Verwenden Sie Docker- oder Kubernetes-Agents.
- **Sichern Sie Anmeldeinformationen** – Verwenden Sie das Credentials-Plugin, nicht Klartext.
- **Sichern Sie JENKINS_HOME** – Regelmäßiges Backup von Job-Konfigurationen und Plugin-Daten.
- **Begrenzen Sie die Parallelität** – Verwenden Sie `properties([disableConcurrentBuilds()])` für ressourcenintensive Jobs.
- **Verwenden Sie Blue Ocean** für eine bessere Pipeline-Visualisierung.
- **Überwachen Sie mit Prometheus** über das Prometheus-Metrics-Plugin.

## Fehlerbehebung

- **Logs prüfen:** `tail -f /var/log/jenkins/jenkins.log`
- **Konfiguration neu laden:** `Manage Jenkins → Reload Configuration from Disk`
- **Build-Warteschlange leeren:** Klicken Sie auf das Element in der Build-Warteschlange → "Abbrechen"
- **Groovy-Skript ausführen:** `Manage Jenkins → Script Console` für Diagnosen.
- **Heap-Größe erhöhen:** Setzen Sie `JAVA_OPTS="-Xmx2048m -Xms1024m"` beim Start.

## Links

- [Offizielle Jenkins-Dokumentation](https://www.jenkins.io/doc/)
- [Plugin-Index](https://plugins.jenkins.io/)
- [Pipeline-Syntax-Generator](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [JCasC-Dokumentation](https://www.jenkins.io/projects/jcasc/)

---

*Diese Seite wurde im Rahmen der WikiCode-Dokumentation für Entwicklungsteams erstellt.*