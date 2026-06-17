---
title: Servidor de Automatización Jenkins CI/CD
description: Un servidor de automatización para Continuous Integration y Continuous Delivery de proyectos de software.
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

# Servidor de Automatización Jenkins CI/CD

## Qué Es

Jenkins es un servidor de automatización de código abierto escrito en Java. Se utiliza para automatizar la construcción, las pruebas y el despliegue de software, habilitando Continuous Integration (CI) y Continuous Delivery (CD). Originalmente bifurcado del proyecto Hudson, Jenkins es ahora el estándar de la industria para la orquestación de pipelines.

## ¿Por Qué Jenkins?

- **Extensibilidad:** Más de 1800 plugins permiten la integración con prácticamente cualquier herramienta DevOps (Git, Docker, Kubernetes, AWS, Azure, Slack, etc.).
- **Flexibilidad:** Soporta desde trabajos simples (freestyle) hasta pipelines multi‑etapa complejos definidos como código.
- **Construcciones Distribuidas:** La arquitectura Master/agent permite distribuir cargas de trabajo en múltiples máquinas.
- **Código Abierto y Maduro:** Gratuito (licencia MIT) con una gran comunidad y documentación extensa.
- **Ecosistema Rico:** Plugins para SCM, herramientas de construcción, informes de pruebas, gestión de artefactos, despliegue y notificación.

## Instalación

Jenkins requiere Java 8, 11 o 17 (LTS recomendado). Existen múltiples métodos de instalación:

### Archivo WAR

```bash
java -jar jenkins.war
```

Ejecuta Jenkins de forma independiente en el puerto 8080. Excelente para pruebas rápidas.

### Paquetes Nativos

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

Después de la instalación, accede a Jenkins en `http://localhost:8080` y obtén la contraseña de administrador inicial de los registros o del archivo (`/var/lib/jenkins/secrets/initialAdminPassword`).

## Uso Básico

### 1. Crear un Trabajo

- **Freestyle project:** Tareas simples con pocos pasos.
- **Pipeline:** Define el ciclo de vida de la construcción en un `Jenkinsfile`.

### 2. Configurar el Código Fuente

- Conéctate a un repositorio Git usando credenciales (usuario/contraseña o clave SSH).

### 3. Configurar Disparadores

- **Poll SCM:** `* * * * *` (cada minuto)
- **Webhook:** Desde GitHub/GitLab al hacer push.
- **Cron:** por ejemplo, `H 2 * * 1-5` (días laborables a las 2 AM)

### 4. Agregar Pasos de Construcción

- Ejecutar comandos shell/batch.
- Ejecutar objetivos de Maven/Gradle.
- Construir imágenes Docker.
- Invocar otras herramientas de construcción.

### 5. Acciones Posteriores a la Construcción

- Archivar artefactos (por ejemplo, JARs, informes).
- Publicar resultados de pruebas (JUnit, informes HTML).
- Desplegar en servidores.
- Enviar notificaciones (Slack, email).

## Características Clave con Ejemplos

### Pipeline como Código

`Jenkinsfile` declarativo en el repositorio de código fuente:

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

Este pipeline se ejecuta automáticamente en cada commit, compila código, ejecuta pruebas, archiva resultados de pruebas y despliega desde `main`.

### Pipeline Multirrama

Crea automáticamente un pipeline para cada rama y pull request en un repositorio.

```groovy
// In Jenkins UI: New Item → Multibranch Pipeline → add Git source
// The Jenkinsfile from the branch controls execution.
```

### Construcciones Distribuidas con Agentes

Jenkins puede etiquetar agentes (por ejemplo, "linux", "docker", "high-mem") y asignarles trabajos:

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

### Librerías Compartidas

Código de pipeline reutilizable entre repositorios. Definir en un repositorio Git de librerías compartidas:

**vars/buildApp.groovy:**

```groovy
def call(String project) {
    sh "mvn -f ${project}/pom.xml clean package"
}
```

Luego en cualquier `Jenkinsfile`:

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

### Integración con Kubernetes

Usa el plugin de Kubernetes para levantar dinámicamente agentes de construcción:

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

### API REST

Jenkins proporciona una API REST completa para automatización. Ejemplo con curl para disparar un trabajo:

```bash
curl -X POST http://jenkins-url/job/my-job/build \
  --user username:api-token
```

Listar trabajos:

```bash
curl http://jenkins-url/api/json
```

### Interfaz Blue Ocean

Interfaz moderna y visual para pipelines (requiere el plugin Blue Ocean). Proporciona una vista gráfica de construcciones, registros y etapas del pipeline.

## Configuración como Código (JCasC)

Gestiona la configuración de Jenkins de forma declarativa con YAML usando el plugin `configuration-as-code`.

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

Aplicar al inicio o mediante el endpoint `reload-configuration-as-code`.

## Plugins

- **SCM:** Git, GitHub, GitLab, Bitbucket, Subversion.
- **Build:** Maven, Gradle, Ant, NodeJS, Docker Pipeline.
- **Test:** JUnit, HTML Publisher, Allure, Cucumber Reports.
- **Deploy:** Kubernetes, AWS CodeDeploy, Ansible, SSH.
- **Notification:** Slack, Email Extension, PagerDuty.
- **Utility:** Credentials Binding, Pipeline Utility Steps, Job DSL.

## Mejores Prácticas

- **Usa Pipeline como Código** – Almacena el `Jenkinsfile` en SCM junto con el proyecto.
- **Usa Librerías Compartidas** – Evita duplicar la lógica del pipeline.
- **Mantén los Agentes sin Estado** – Usa agentes Docker o Kubernetes.
- **Asegura las Credenciales** – Usa el plugin Credentials, no texto plano.
- **Respaldar JENKINS_HOME** – Realiza copias de seguridad periódicas de las configuraciones de trabajos y datos de plugins.
- **Limita la Concurrencia** – Usa `properties([disableConcurrentBuilds()])` para trabajos sensibles a recursos.
- **Usa Blue Ocean** para una mejor visualización de pipelines.
- **Monitorea con Prometheus** a través del plugin Prometheus Metrics.

## Solución de Problemas

- **Revisa los registros:** `tail -f /var/log/jenkins/jenkins.log`
- **Recargar configuración:** `Manage Jenkins → Reload Configuration from Disk`
- **Limpiar la cola de construcción:** Haz clic en el elemento de la cola de construcción → "Cancel"
- **Ejecutar Script Groovy:** `Manage Jenkins → Script Console` para diagnósticos.
- **Aumentar el tamaño del heap:** Configura `JAVA_OPTS="-Xmx2048m -Xms1024m"` en el inicio.

## Enlaces

- [Documentación Oficial de Jenkins](https://www.jenkins.io/doc/)
- [Índice de Plugins](https://plugins.jenkins.io/)
- [Generador de Sintaxis de Pipeline](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Documentación de JCasC](https://www.jenkins.io/projects/jcasc/)

---

*Esta página fue creada como parte de la documentación de WikiCode para equipos de desarrollo.*