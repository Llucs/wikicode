---
title: Jenkins CI/CD Automation Server
description: An automation server for continuous integration and continuous delivery of software projects.
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

# Jenkins CI/CD Automation Server

## What It Is

Jenkins is an open-source automation server written in Java. It is used to automate the building, testing, and deployment of software, enabling Continuous Integration (CI) and Continuous Delivery (CD). Originally forked from the Hudson project, Jenkins is now the industry standard for pipeline orchestration.

## Why Jenkins?

- **Extensibility:** Over 1,800 plugins allow integration with virtually every DevOps tool (Git, Docker, Kubernetes, AWS, Azure, Slack, etc.).
- **Flexibility:** Supports simple freestyle jobs to complex multi-stage pipelines defined as code.
- **Distributed Builds:** Master/agent architecture lets you distribute workloads across many machines.
- **Open Source & Mature:** Free (MIT license) with a huge community and extensive documentation.
- **Rich Ecosystem:** Plugins for SCM, build tools, test reporting, artifact management, deployment, and notification.

## Installation

Jenkins requires Java 8, 11, or 17 (LTS recommended). Multiple installation methods exist:

### WAR File

```bash
java -jar jenkins.war
```
Runs Jenkins standalone on port 8080. Great for quick testing.

### Native Packages

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

After installation, access Jenkins at `http://localhost:8080` and retrieve the initial admin password from the logs or file (`/var/lib/jenkins/secrets/initialAdminPassword`).

## Basic Usage

### 1. Create a Job

- **Freestyle project:** Simple tasks with a few steps.
- **Pipeline:** Define the build lifecycle in a `Jenkinsfile`.

### 2. Configure Source Code

- Connect to a Git repository using credentials (username/password or SSH key).

### 3. Set Triggers

- **Poll SCM:** `* * * * *` (every minute)
- **Webhook:** From GitHub/GitLab on push.
- **Cron**: e.g., `H 2 * * 1-5` (weekdays at 2 AM)

### 4. Add Build Steps

- Execute shell/batch commands.
- Run Maven/Gradle goals.
- Build Docker images.
- Invoke other build tools.

### 5. Post-Build Actions

- Archive artifacts (e.g., JARs, reports).
- Publish test results (JUnit, HTML reports).
- Deploy to servers.
- Send notifications (Slack, email).

## Key Features with Examples

### Pipeline as Code

Declarative `Jenkinsfile` in source repository:

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

This pipeline automatically runs on every commit, compiles code, runs tests, archives test results, and deploys from `main`.

### Multibranch Pipeline

Automatically creates a pipeline for each branch and pull request in a repository.

```groovy
// In Jenkins UI: New Item → Multibranch Pipeline → add Git source
// The Jenkinsfile from the branch controls execution.
```

### Distributed Builds with Agents

Jenkins can label agents (e.g., "linux", "docker", "high-mem") and assign jobs to them:

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

Reusable pipeline code across repositories. Define in a shared library Git repo:

**vars/buildApp.groovy:**

```groovy
def call(String project) {
    sh "mvn -f ${project}/pom.xml clean package"
}
```

Then in any `Jenkinsfile`:

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

### Integration with Kubernetes

Use the Kubernetes plugin to dynamically spin up build agents:

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

Jenkins provides a comprehensive REST API for automation. Example curl to trigger a job:

```bash
curl -X POST http://jenkins-url/job/my-job/build \
  --user username:api-token
```

List jobs:

```bash
curl http://jenkins-url/api/json
```

### Blue Ocean UI

Modern, visual interface for pipelines (requires Blue Ocean plugin). Provides a graphical view of builds, logs, and pipeline stages.

## Configuration as Code (JCasC)

Manage Jenkins configuration declaratively with YAML using the `configuration-as-code` plugin.

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

Apply on startup or via `reload-configuration-as-code` endpoint.

## Plugins

Key plugin categories:

- **SCM:** Git, GitHub, GitLab, Bitbucket, Subversion.
- **Build:** Maven, Gradle, Ant, NodeJS, Docker Pipeline.
- **Test:** JUnit, HTML Publisher, Allure, Cucumber Reports.
- **Deploy:** Kubernetes, AWS CodeDeploy, Ansible, SSH.
- **Notification:** Slack, Email Extension, PagerDuty.
- **Utility:** Credentials Binding, Pipeline Utility Steps, Job DSL.

## Best Practices

- **Use Pipeline as Code** – Store `Jenkinsfile` in SCM with the project.
- **Use Shared Libraries** – Avoid duplicating pipeline logic.
- **Keep Agents Stateless** – Use Docker or Kubernetes agents.
- **Secure Credentials** – Use the Credentials plugin, not plain text.
- **Backup JENKINS_HOME** – Regularly backup job configurations and plugin data.
- **Limit Concurrency** – Use `properties([disableConcurrentBuilds()])` for resource-sensitive jobs.
- **Use Blue Ocean** for better pipeline visualisation.
- **Monitor with Prometheus** via the Prometheus Metrics plugin.

## Troubleshooting

- **Check logs:** `tail -f /var/log/jenkins/jenkins.log`
- **Reload configuration:** `Manage Jenkins → Reload Configuration from Disk`
- **Clear build queue:** Click on the build queue item → "Cancel"
- **Run Groovy Script:** `Manage Jenkins → Script Console` for diagnostics.
- **Increase heap size:** Set `JAVA_OPTS="-Xmx2048m -Xms1024m"` in startup.

## Links

- [Official Jenkins Documentation](https://www.jenkins.io/doc/)
- [Plugins Index](https://plugins.jenkins.io/)
- [Pipeline Syntax Generator](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [JCasC Documentation](https://www.jenkins.io/projects/jcasc/)

---

*This page was created as part of WikiCode documentation for development teams.*