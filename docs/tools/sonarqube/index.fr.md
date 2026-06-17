---
title: SonarQube
description: Un outil d'analyse de la qualité du code et de la sécurité qui s'intègre aux pipelines CI/CD pour automatiser les revues de code et détecter les vulnérabilités.
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

## Qu'est-ce que SonarQube ?

SonarQube est une plateforme open-source de SonarSource pour l'inspection continue de la qualité du code et de la sécurité. Elle effectue des tests de sécurité statiques d'applications (SAST) sur le code source pour détecter les **Bugs**, les **Vulnérabilités**, les **Code Smells** et les **Duplications** dans plus de 30 langages de programmation, notamment Java, C#, JavaScript, TypeScript, Python, Go, et bien d'autres. SonarQube agit comme un hub central de qualité dans les workflows de développement, en appliquant des politiques personnalisables (Quality Gates) pour empêcher la publication de code problématique.

## Pourquoi utiliser SonarQube ?

- **Détecter les problèmes tôt** – Intégrez-le dans les pipelines CI/CD pour examiner automatiquement chaque commit et pull request.
- **Appliquer les normes de qualité** – Définissez des Quality Gates qui doivent être respectés (par exemple, aucun nouveau bug, seuil de couverture) avant qu'une build puisse réussir.
- **Réduire la dette technique** – Quantifiez l'effort nécessaire pour corriger les problèmes existants et suivez les améliorations au fil du temps.
- **Améliorer la sécurité** – Identifiez les vulnérabilités OWASP Top 10 et CWE et signalez les zones de sécurité à examiner manuellement.
- **Automatiser les revues de code** – Déchargez la détection des problèmes simples (formatage, pointeurs nuls, fuites de ressources) des réviseurs humains, afin qu'ils puissent se concentrer sur l'architecture et la logique.

## Fonctionnalités clés

### Analyse statique du code
SonarQube scanne le code source pour détecter les problèmes de fiabilité, de sécurité et de maintenabilité. Il effectue des analyses avancées de flux de données et de flux de contrôle pour détecter :
- Les déréférencements potentiels de pointeurs nuls
- Les fuites de ressources
- Les failles d'injection SQL et de cross-site scripting (XSS)
- Les informations d'identification codées en dur

### Quality Gates
Un Quality Gate est un ensemble de conditions booléennes sur des métriques (par exemple, `New Coverage < 80%`, `New Bugs > 0`) qui doivent être remplies pour qu'un projet soit validé. SonarQube est livré avec un gate par défaut, et vous pouvez en créer des personnalisés pour correspondre aux politiques de votre équipe.

### Security Hotspots
SonarQube met en évidence le code qui nécessite une revue de sécurité manuelle. Ces hotspots ne sont pas automatiquement confirmés comme des vulnérabilités, mais ce sont des zones où un attaquant pourrait potentiellement injecter une entrée malveillante. Les développeurs peuvent les examiner et les marquer comme « Sûr » ou « À examiner ».

### Mesure de la dette technique
SonarQube traduit les problèmes en une métrique de **Dette technique**, exprimée en jours ou en coût (par exemple, USD). Cela aide les équipes à budgétiser et prioriser le refactoring.

### Analyse des branches et des pull requests
SonarQube peut analyser les branches de fonctionnalités et les pull requests, ce qui permet d'appliquer des Quality Gates uniquement sur le nouveau code. Cela s'intègre naturellement dans un workflow **Clean as You Code**, où l'accent est mis sur le diff plutôt que sur l'ensemble du codebase.

### Intégrations DevOps
SonarQube s'intègre nativement avec :
- **GitHub, GitLab, Bitbucket** – Décoration des pull requests, commentaires en ligne.
- **Jenkins, Azure DevOps, Travis CI, CircleCI** – Intégration dans les pipelines de build.
- **Maven, Gradle, .NET, SonarScanner CLI** – Invocation de scan.

### Extension IDE SonarLint
SonarLint (pour VS Code, IntelliJ, Eclipse, Visual Studio) se connecte à un serveur SonarQube et applique les mêmes règles localement, fournissant des retours en temps réel pendant la saisie.

---

## Installation

SonarQube nécessite **Java 17+** et une base de données dédiée (PostgreSQL est recommandé pour la production). Il fonctionne comme une application web autonome.

### Docker (démarrage rapide pour évaluation)

```bash
docker run -d --name sonarqube \
  -p 9000:9000 \
  -e SONAR_JDBC_URL=jdbc:postgresql://host:port/sonarqube \
  -e SONAR_JDBC_USERNAME=sonar \
  -e SONAR_JDBC_PASSWORD=sonar \
  sonarqube:community
```

> **Note :** L'édition Community ne comprend pas les fonctionnalités avancées comme l'analyse des branches ou la décoration des pull requests. Pour celles-ci, envisagez l'édition Developer ou supérieure.

### Installation manuelle (Linux / macOS)

1. Téléchargez la dernière version depuis [SonarSource Download](https://www.sonarsource.com/products/sonarqube/downloads/).
2. Extrayez l'archive.
3. Configurez la connexion à la base de données dans `conf/sonar.properties` :
   ```properties
   sonar.jdbc.url=jdbc:postgresql://localhost/sonarqube
   sonar.jdbc.username=sonar
   sonar.jdbc.password=sonar
   ```
4. Démarrez le serveur :
   ```bash
   # Linux/macOS
   bin/linux-x86-64/sonar.sh start
   # Windows
   bin/windows-x86-64/StartSonar.bat
   ```
5. Accédez à l'interface web à l'adresse `http://localhost:9000`. Identifiants par défaut : `admin` / `admin`.

---

## Utilisation de base

### 1. Configurer un projet

Connectez-vous à SonarQube, cliquez sur **Create new project**, donnez-lui une clé, et choisissez un Quality Profile et un Quality Gate. Générez ensuite un **Project Token** (par exemple, `sqa_xxxx`). Ce token authentifie le scanner.

### 2. Exécuter un scan

#### Avec Maven

```bash
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=my-project \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqa_xxxx
```

#### Avec Gradle

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

#### Avec SonarScanner CLI

Installez le SonarScanner (téléchargez-le depuis SonarSource), puis :

```bash
sonar-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqa_xxxx
```

### 3. Examiner les résultats

Après la fin d'un scan, le tableau de bord SonarQube affiche :
- **Statut du Quality Gate** – Réussi ou Échoué.
- **Issues** – Groupées par sévérité (Blocker, Critical, Major, Minor, Info) et par type (Bug, Vulnérabilité, Code Smell).
- **Security Hotspots** – Zones de code nécessitant une revue manuelle.
- **Couverture** – Si vous avez un outil comme JaCoCo ou dotCover, importez les rapports de couverture.
- **Duplications** – Blocs dupliqués mis en évidence.

---

## Intégration avec CI/CD

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

## Méthodologie Clean as You Code

SonarQube encourage une approche **Clean as You Code** : au lieu d'essayer de corriger tous les problèmes existants, concentrez-vous sur l'évitement de nouveaux problèmes dans le code que vous écrivez aujourd'hui. Cela se reflète dans :

- **Focus sur le nouveau code** – Les métriques et les Quality Gates ciblent le code nouveau ou modifié.
- **Décoration des pull requests** – Les issues sont signalées directement sur les diffs des PR (GitHub, GitLab, Bitbucket).
- **SonarLint** – Les développeurs détectent les issues dans leur IDE avant de les commettre.

Cela réduit les frictions et rend l'amélioration de la qualité durable.

---

## Conclusion

SonarQube est un outil mature et largement adopté pour l'analyse statique et la gouvernance de la qualité. En l'intégrant dans votre pipeline de développement, vous pouvez automatiser les revues de code, appliquer des normes de sécurité et gérer la dette technique, ce qui permet de livrer des logiciels plus fiables et plus sécurisés.

Pour les fonctionnalités avancées (analyse de branches, gestion de portefeuille, couverture par langage), envisagez de passer aux éditions **Developer**, **Enterprise** ou **Data Center** de SonarQube Server, ou utilisez la version cloud **SonarQube Cloud** (anciennement SonarCloud).