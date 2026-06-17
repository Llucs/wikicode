---
title: Servidor de Automação CI/CD Jenkins
description: Um servidor de automação para integração contínua e entrega contínua de projetos de software.
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

# Servidor de Automação CI/CD Jenkins

## O Que É

Jenkins é um servidor de automação de código aberto escrito em Java. Ele é usado para automatizar a construção, teste e implantação de software, permitindo Integração Contínua (CI) e Entrega Contínua (CD). Originalmente bifurcado do projeto Hudson, Jenkins é agora o padrão da indústria para orquestração de pipelines.

## Por que Jenkins?

- **Extensibilidade:** Mais de 1.800 plugins permitem integração com praticamente todas as ferramentas DevOps (Git, Docker, Kubernetes, AWS, Azure, Slack, etc.).
- **Flexibilidade:** Suporta desde trabalhos freestyle simples até pipelines complexos de múltiplos estágios definidos como código.
- **Builds Distribuídos:** A arquitetura mestre/agente permite distribuir cargas de trabalho em várias máquinas.
- **Open Source e Maduro:** Gratuito (licença MIT) com uma enorme comunidade e documentação extensa.
- **Ecossistema Rico:** Plugins para SCM, ferramentas de build, relatórios de teste, gerenciamento de artefatos, implantação e notificação.

## Instalação

Jenkins requer Java 8, 11 ou 17 (LTS recomendado). Existem vários métodos de instalação:

### Arquivo WAR

```bash
java -jar jenkins.war
```
Executa Jenkins de forma autônoma na porta 8080. Ótimo para testes rápidos.

### Pacotes Nativos

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

Após a instalação, acesse Jenkins em `http://localhost:8080` e recupere a senha de administrador inicial dos logs ou do arquivo (`/var/lib/jenkins/secrets/initialAdminPassword`).

## Uso Básico

### 1. Criar um Job

- **Projeto Freestyle:** Tarefas simples com poucos passos.
- **Pipeline:** Defina o ciclo de vida do build em um `Jenkinsfile`.

### 2. Configurar Código Fonte

- Conecte-se a um repositório Git usando credenciais (usuário/senha ou chave SSH).

### 3. Configurar Gatilhos

- **Poll SCM:** `* * * * *` (a cada minuto)
- **Webhook:** Do GitHub/GitLab ao fazer push.
- **Cron**: por ex., `H 2 * * 1-5` (dias úteis às 2 AM)

### 4. Adicionar Passos de Build

- Execute comandos shell/batch.
- Execute objetivos do Maven/Gradle.
- Construa imagens Docker.
- Invoque outras ferramentas de build.

### 5. Ações Pós-Build

- Arquive artefatos (ex.: JARs, relatórios).
- Publique resultados de teste (JUnit, relatórios HTML).
- Implante em servidores.
- Envie notificações (Slack, email).

## Principais Recursos com Exemplos

### Pipeline como Código

`Jenkinsfile` declarativo no repositório de código-fonte:

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

Este pipeline é executado automaticamente a cada commit, compila o código, executa testes, arquiva resultados de teste e implanta a partir de `main`.

### Pipeline Multibranch

Cria automaticamente um pipeline para cada branch e pull request em um repositório.

```groovy
// In Jenkins UI: New Item → Multibranch Pipeline → add Git source
// The Jenkinsfile from the branch controls execution.
```

### Builds Distribuídos com Agentes

Jenkins pode rotular agentes (ex.: "linux", "docker", "high-mem") e atribuir trabalhos a eles:

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

### Bibliotecas Compartilhadas

Código de pipeline reutilizável entre repositórios. Defina em um repositório Git de biblioteca compartilhada:

**vars/buildApp.groovy:**

```groovy
def call(String project) {
    sh "mvn -f ${project}/pom.xml clean package"
}
```

Então em qualquer `Jenkinsfile`:

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

### Integração com Kubernetes

Use o plugin Kubernetes para iniciar dinamicamente agentes de build:

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

Jenkins fornece uma API REST abrangente para automação. Exemplo de curl para acionar um job:

```bash
curl -X POST http://jenkins-url/job/my-job/build \
  --user username:api-token
```

Listar jobs:

```bash
curl http://jenkins-url/api/json
```

### Blue Ocean UI

Interface visual moderna para pipelines (requer o plugin Blue Ocean). Fornece uma visão gráfica dos builds, logs e estágios do pipeline.

## Configuração como Código (JCasC)

Gerencie a configuração do Jenkins de forma declarativa com YAML usando o plugin `configuration-as-code`.

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

Aplique na inicialização ou via endpoint `reload-configuration-as-code`.

## Plugins

Categorias principais de plugins:

- **SCM:** Git, GitHub, GitLab, Bitbucket, Subversion.
- **Build:** Maven, Gradle, Ant, NodeJS, Docker Pipeline.
- **Test:** JUnit, HTML Publisher, Allure, Cucumber Reports.
- **Deploy:** Kubernetes, AWS CodeDeploy, Ansible, SSH.
- **Notification:** Slack, Email Extension, PagerDuty.
- **Utility:** Credentials Binding, Pipeline Utility Steps, Job DSL.

## Melhores Práticas

- **Use Pipeline como Código** – Armazene o `Jenkinsfile` no SCM com o projeto.
- **Use Bibliotecas Compartilhadas** – Evite duplicar lógica de pipeline.
- **Mantenha Agentes Sem Estado** – Use agentes Docker ou Kubernetes.
- **Proteja Credenciais** – Use o plugin Credentials, não texto puro.
- **Faça Backup do JENKINS_HOME** – Faça backup regular das configurações de jobs e dados de plugins.
- **Limite Concorrência** – Use `properties([disableConcurrentBuilds()])` para jobs sensíveis a recursos.
- **Use Blue Ocean** para melhor visualização de pipelines.
- **Monitore com Prometheus** através do plugin Prometheus Metrics.

## Solução de Problemas

- **Verifique logs:** `tail -f /var/log/jenkins/jenkins.log`
- **Recarregue configuração:** `Manage Jenkins → Reload Configuration from Disk`
- **Limpe a fila de builds:** Clique no item da fila de builds → "Cancel"
- **Execute Script Groovy:** `Manage Jenkins → Script Console` para diagnósticos.
- **Aumente o tamanho da heap:** Defina `JAVA_OPTS="-Xmx2048m -Xms1024m"` na inicialização.

## Links

- [Documentação Oficial do Jenkins](https://www.jenkins.io/doc/)
- [Índice de Plugins](https://plugins.jenkins.io/)
- [Gerador de Sintaxe de Pipeline](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Documentação do JCasC](https://www.jenkins.io/projects/jcasc/)

---

*Esta página foi criada como parte da documentação WikiCode para equipes de desenvolvimento.*