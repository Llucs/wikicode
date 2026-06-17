---
title: SonarQube
description: A code quality and security analysis tool that integrates with CI/CD pipelines to automate code reviews and catch vulnerabilities.
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

## What is SonarQube?

SonarQube is an open-source platform by SonarSource for continuous inspection of code quality and security. It performs Static Application Security Testing (SAST) on source code to detect **Bugs**, **Vulnerabilities**, **Code Smells**, and **Duplications** across 30+ programming languages, including Java, C#, JavaScript, TypeScript, Python, Go, and many more. SonarQube acts as a central quality hub in development workflows, enforcing customizable policies (Quality Gates) to prevent problematic code from being released.

## Why Use SonarQube?

- **Catch Issues Early** – Integrate into CI/CD pipelines to automatically review every commit and pull request.
- **Enforce Quality Standards** – Define Quality Gates that must pass (e.g., no new bugs, coverage threshold) before a build can succeed.
- **Reduce Technical Debt** – Quantify the effort needed to fix existing issues and track improvements over time.
- **Improve Security** – Identify OWASP Top 10 and CWE vulnerabilities and flag security hotspots for manual review.
- **Automate Code Reviews** – Offload detection of simple issues (formatting, null pointers, resource leaks) from human reviewers, so they can focus on architecture and logic.

## Key Features

### Static Code Analysis
SonarQube scans source code for reliability, security, and maintainability issues. It runs advanced dataflow and control flow analyses to detect:
- Potential null pointer dereferences
- Resource leaks
- SQL injection and cross-site scripting (XSS) flaws
- Hard-coded credentials

### Quality Gates
A Quality Gate is a set of boolean conditions on metrics (e.g., `New Coverage < 80%`, `New Bugs > 0`) that must be met for a project to pass. SonarQube ships with a default gate, and you can create custom ones to match your team’s policies.

### Security Hotspots
SonarQube highlights code that requires manual security review. These hotspots are not automatically confirmed as vulnerabilities but are areas where an attacker could potentially inject malicious input. Developers can review and mark them as "Safe" or "Needs Review."

### Technical Debt Measurement
SonarQube translates issues into a **Technical Debt** metric, expressed in days or cost (e.g., USD). This helps teams budget and prioritize refactoring.

### Branch and Pull Request Analysis
SonarQube can analyze feature branches and pull requests, allowing you to enforce Quality Gates on new code only. This fits naturally into a **Clean as You Code** workflow, where the focus is on the diff rather than the entire codebase.

### DevOps Integrations
SonarQube integrates natively with:
- **GitHub, GitLab, Bitbucket** – Pull request decoration, inline comments.
- **Jenkins, Azure DevOps, Travis CI, CircleCI** – Build pipeline integration.
- **Maven, Gradle, .NET, SonarScanner CLI** – Scan invocation.

### SonarLint IDE Extension
SonarLint (for VS Code, IntelliJ, Eclipse, Visual Studio) connects to a SonarQube server and applies the same rules locally, giving real-time feedback as you type.

---

## Installation

SonarQube requires **Java 17+** and a dedicated database (PostgreSQL recommended for production). It runs as a standalone web application.

### Docker (quick start for evaluation)

```bash
docker run -d --name sonarqube \
  -p 9000:9000 \
  -e SONAR_JDBC_URL=jdbc:postgresql://host:port/sonarqube \
  -e SONAR_JDBC_USERNAME=sonar \
  -e SONAR_JDBC_PASSWORD=sonar \
  sonarqube:community
```

> **Note:** The Community Edition does not include advanced features like branch analysis or pull request decoration. For those, consider the Developer Edition or above.

### Manual Installation (Linux / macOS)

1. Download the latest version from [SonarSource Download](https://www.sonarsource.com/products/sonarqube/downloads/).
2. Extract the archive.
3. Configure database connection in `conf/sonar.properties`:
   ```properties
   sonar.jdbc.url=jdbc:postgresql://localhost/sonarqube
   sonar.jdbc.username=sonar
   sonar.jdbc.password=sonar
   ```
4. Start the server:
   ```bash
   # Linux/macOS
   bin/linux-x86-64/sonar.sh start
   # Windows
   bin/windows-x86-64/StartSonar.bat
   ```
5. Access the web UI at `http://localhost:9000`. Default credentials: `admin` / `admin`.

---

## Basic Usage

### 1. Configure a Project

Log into SonarQube, click **Create new project**, give it a key, and choose a Quality Profile and Quality Gate. Then generate a **Project Token** (e.g., `sqa_xxxx`). This token authenticates the scanner.

### 2. Run a Scan

#### Using Maven

```bash
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=my-project \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqa_xxxx
```

#### Using Gradle

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

#### Using SonarScanner CLI

Install the SonarScanner (download from SonarSource), then:

```bash
sonar-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqa_xxxx
```

### 3. Review Results

After a scan completes, the SonarQube dashboard shows:
- **Quality Gate status** – Passed or Failed.
- **Issues** – Grouped by severity (Blocker, Critical, Major, Minor, Info) and type (Bug, Vulnerability, Code Smell).
- **Security Hotspots** – Code areas needing manual review.
- **Coverage** – If you have a tool like JaCoCo or dotCover, import coverage reports.
- **Duplications** – Highlighted duplicated blocks.

---

## Integration with CI/CD

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

## Clean as You Code Methodology

SonarQube encourages a **Clean as You Code** approach: instead of trying to fix every existing issue, focus on avoiding new ones in the code you write today. This is reflected in:

- **Focus on New Code** – Metrics and Quality Gates target new/changed code.
- **Pull Request Decoration** – Issues are reported directly on PR diffs (GitHub, GitLab, Bitbucket).
- **SonarLint** – Developers catch issues in their IDE before committing.

This reduces friction and makes quality improvement sustainable.

---

## Conclusion

SonarQube is a mature, widely adopted tool for static analysis and quality governance. By integrating it into your development pipeline, you can automate code reviews, enforce security standards, and manage technical debt—ultimately delivering more reliable and secure software.

For advanced features (branch analysis, portfolio management, language-specific coverage), consider upgrading to the **Developer**, **Enterprise**, or **Data Center** editions of SonarQube Server, or use the cloud-hosted **SonarQube Cloud** (formerly SonarCloud).