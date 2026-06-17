---
title: SonarQube
description: Ein Werkzeug zur Analyse der Codequalität und -sicherheit, das sich in CI/CD-Pipelines integriert, um Code-Reviews zu automatisieren und Schwachstellen zu erkennen.
created: 2026-06-16
tags:
  - code-quality
  - security
  - static-analysis
  - ci-cd
  - sonarqube
status: draft
---

# SonarQube

## Was ist SonarQube?

SonarQube ist eine Open-Source-Plattform von SonarSource zur kontinuierlichen Überprüfung der Codequalität und -sicherheit. Sie führt Static Application Security Testing (SAST) des Quellcodes durch, um **Bugs**, **Schwachstellen**, **Code Smells** und **Duplikationen** in über 30 Programmiersprachen zu erkennen, darunter Java, C#, JavaScript, TypeScript, Python, Go und viele weitere. SonarQube fungiert als zentraler Qualitätshub in Entwicklungsworkflows und setzt anpassbare Richtlinien (Quality Gates) durch, um die Auslieferung problematischen Codes zu verhindern.

## Warum SonarQube verwenden?

- **Probleme frühzeitig erkennen** – Integration in CI/CD-Pipelines, um automatisch jeden Commit und Pull-Request zu überprüfen.
- **Qualitätsstandards durchsetzen** – Definieren Sie Quality Gates, die bestanden werden müssen (z. B. keine neuen Fehler, Codeabdeckungsschwellwert), bevor ein Build erfolgreich sein kann.
- **Technische Schulden reduzieren** – Quantifizieren Sie den Aufwand zur Behebung vorhandener Probleme und verfolgen Sie Verbesserungen im Laufe der Zeit.
- **Sicherheit verbessern** – Identifizieren Sie OWASP Top 10- und CWE-Schwachstellen und markieren Sie Sicherheits-Hotspots zur manuellen Überprüfung.
- **Code-Reviews automatisieren** – Lagern Sie die Erkennung einfacher Probleme (Formatierung, Nullzeiger, Ressourcenlecks) von menschlichen Prüfern aus, damit diese sich auf Architektur und Logik konzentrieren können.

## Hauptfunktionen

### Statische Codeanalyse
SonarQube scannt den Quellcode auf Zuverlässigkeits-, Sicherheits- und Wartbarkeitsprobleme. Es führt erweiterte Datenfluss- und Kontrollflussanalysen durch, um Folgendes zu erkennen:
- Potentielle Nullzeiger-Dereferenzierungen
- Ressourcenlecks
- SQL-Injection- und Cross-Site-Scripting (XSS)-Schwachstellen
- Hartcodierte Anmeldeinformationen

### Quality Gates
Ein Quality Gate ist eine Sammlung von booleschen Bedingungen für Metriken (z. B. `New Coverage < 80%`, `New Bugs > 0`), die erfüllt sein müssen, damit ein Projekt besteht. SonarQube wird mit einem Standard-Gate ausgeliefert, und Sie können benutzerdefinierte Gates erstellen, die zu den Richtlinien Ihres Teams passen.

### Sicherheits-Hotspots
SonarQube hebt Code hervor, der eine manuelle Sicherheitsüberprüfung erfordert. Diese Hotspots werden nicht automatisch als Schwachstellen bestätigt, sondern sind Bereiche, in denen ein Angreifer potenziell bösartige Eingaben einschleusen könnte. Entwickler können sie überprüfen und als „Sicher“ oder „Überprüfung erforderlich“ markieren.

### Messung technischer Schulden
SonarQube übersetzt Probleme in eine **Technische Schulden**-Metrik, ausgedrückt in Tagen oder Kosten (z. B. USD). Dies hilft Teams, Refactoring zu budgetieren und zu priorisieren.

### Analyse von Branches und Pull-Requests
SonarQube kann Feature-Branches und Pull-Requests analysieren, sodass Sie Quality Gates nur auf neuen Code anwenden können. Dies fügt sich nahtlos in einen **Clean as You Code**-Workflow ein, bei dem der Fokus auf dem Diff und nicht auf der gesamten Codebasis liegt.

### DevOps-Integrationen
SonarQube integriert sich nativ in:
- **GitHub, GitLab, Bitbucket** – Pull-Request-Dekoration, Inline-Kommentare.
- **Jenkins, Azure DevOps, Travis CI, CircleCI** – Build-Pipeline-Integration.
- **Maven, Gradle, .NET, SonarScanner CLI** – Scan-Aufruf.

### SonarLint IDE-Erweiterung
SonarLint (für VS Code, IntelliJ, Eclipse, Visual Studio) verbindet sich mit einem SonarQube-Server und wendet dieselben Regeln lokal an, wodurch Echtzeit-Feedback beim Tippen gegeben wird.

---

## Installation

SonarQube benötigt **Java 17+** und eine dedizierte Datenbank (für Produktion wird PostgreSQL empfohlen). Es läuft als eigenständige Webanwendung.

### Docker (Schnellstart zur Evaluierung)

```bash
docker run -d --name sonarqube \
  -p 9000:9000 \
  -e SONAR_JDBC_URL=jdbc:postgresql://host:port/sonarqube \
  -e SONAR_JDBC_USERNAME=sonar \
  -e SONAR_JDBC_PASSWORD=sonar \
  sonarqube:community
```

> **Hinweis:** Die Community Edition enthält keine erweiterten Funktionen wie Branch-Analyse oder Pull-Request-Dekoration. Für diese sollten Sie die Developer Edition oder höher in Betracht ziehen.

### Manuelle Installation (Linux / macOS)

1. Laden Sie die neueste Version von [SonarSource Download](https://www.sonarsource.com/products/sonarqube/downloads/) herunter.
2. Entpacken Sie das Archiv.
3. Konfigurieren Sie die Datenbankverbindung in `conf/sonar.properties`:
   ```properties
   sonar.jdbc.url=jdbc:postgresql://localhost/sonarqube
   sonar.jdbc.username=sonar
   sonar.jdbc.password=sonar
   ```
4. Starten Sie den Server:
   ```bash
   # Linux/macOS
   bin/linux-x86-64/sonar.sh start
   # Windows
   bin/windows-x86-64/StartSonar.bat
   ```
5. Greifen Sie auf die Weboberfläche unter `http://localhost:9000` zu. Standard-Anmeldedaten: `admin` / `admin`.

---

## Grundlegende Verwendung

### 1. Ein Projekt konfigurieren

Melden Sie sich bei SonarQube an, klicken Sie auf **Neues Projekt erstellen**, vergeben Sie einen Schlüssel und wählen Sie ein Quality Profile und ein Quality Gate. Generieren Sie dann einen **Project Token** (z. B. `sqa_xxxx`). Dieser Token authentifiziert den Scanner.

### 2. Einen Scan durchführen

#### Mit Maven

```bash
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=my-project \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqa_xxxx
```

#### Mit Gradle

```groovy
// build.gradle
plugins {
    id "org.sonarqube" version "4.4.1.3373"
}

sonar {
    properties {
        property "sonar.projectKey", "my-project"
        property "sonar.host.url", "http://localhost:9000"
        property "sonar.token", "sqa_xxxx"
    }
}
```

```bash
./gradlew sonarqube
```

#### Mit der SonarScanner CLI

Installieren Sie den SonarScanner (Download von SonarSource), dann:

```bash
sonar-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqa_xxxx
```

### 3. Ergebnisse überprüfen

Nach Abschluss eines Scans zeigt das SonarQube-Dashboard Folgendes an:
- **Status des Quality Gates** – Bestanden oder Fehlgeschlagen.
- **Probleme** – Gruppiert nach Schweregrad (Blocker, Critical, Major, Minor, Info) und Typ (Bug, Vulnerability, Code Smell).
- **Sicherheits-Hotspots** – Codebereiche, die einer manuellen Überprüfung bedürfen.
- **Abdeckung** – Wenn Sie ein Tool wie JaCoCo oder dotCover verwenden, importieren Sie Abdeckungsberichte.
- **Duplikationen** – Hervorgehobene duplizierte Blöcke.

---

## Integration in CI/CD

### GitHub Actions

```yaml
name: SonarQube Scan
on: [push]
jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@v1.9.0
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    environment {
        SONAR_HOST_URL = 'http://sonarqube:9000'
        SONAR_AUTH_TOKEN = credentials('sonarqube-token')
    }
    stages {
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube Server') {
                    sh 'mvn clean verify sonar:sonar'
                }
            }
        }
    }
}
```

### GitLab CI/CD

```yaml
variables:
  SONAR_USER_HOME: "${CI_PROJECT_DIR}/.sonar"
  GIT_DEPTH: "0"

sonarqube-check:
  image: maven:3.8.6-openjdk-17
  script:
    - mvn clean verify sonar:sonar
      -Dsonar.projectKey=$CI_PROJECT_ID
      -Dsonar.host.url=$SONAR_HOST_URL
      -Dsonar.token=$SONAR_TOKEN
      -Dsonar.branch.name=$CI_COMMIT_REF_NAME
```

---

## Clean as You Code Methodik

SonarQube fördert einen **Clean as You Code**-Ansatz: Anstatt zu versuchen, jedes bestehende Problem zu beheben, konzentrieren Sie sich darauf, neue Probleme im heutigen Code zu vermeiden. Dies spiegelt sich wider in:

- **Fokus auf neuen Code** – Metriken und Quality Gates zielen auf neuen/geänderten Code.
- **Pull-Request-Dekoration** – Probleme werden direkt in den PR-Diffs gemeldet (GitHub, GitLab, Bitbucket).
- **SonarLint** – Entwickler erkennen Probleme bereits vor dem Commit in ihrer IDE.

Dies reduziert Reibungsverluste und macht Qualitätsverbesserung nachhaltig.

---

## Fazit

SonarQube ist ein ausgereiftes, weit verbreitetes Werkzeug für statische Analyse und Qualitätsgovernance. Durch die Integration in Ihre Entwicklungspipeline können Sie Code-Reviews automatisieren, Sicherheitsstandards durchsetzen und technische Schulden verwalten – und letztendlich zuverlässigere und sicherere Software liefern.

Für erweiterte Funktionen (Branch-Analyse, Portfoliomanagement, sprachspezifische Abdeckung) sollten Sie ein Upgrade auf die **Developer**, **Enterprise** oder **Data Center** Editionen von SonarQube Server in Betracht ziehen oder die cloudgehostete **SonarQube Cloud** (ehemals SonarCloud) nutzen.