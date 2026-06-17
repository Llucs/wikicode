---
title: SonarQube
description: Una herramienta de análisis de calidad y seguridad de código que se integra con pipelines de CI/CD para automatizar revisiones de código y detectar vulnerabilidades.
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

## ¿Qué es SonarQube?

SonarQube es una plataforma de código abierto de SonarSource para la inspección continua de la calidad y seguridad del código. Realiza pruebas estáticas de seguridad de aplicaciones (SAST) en el código fuente para detectar **Bugs**, **Vulnerabilities**, **Code Smells** y **Duplications** en más de 30 lenguajes de programación, incluyendo Java, C#, JavaScript, TypeScript, Python, Go, y muchos más. SonarQube actúa como un centro de calidad central en los flujos de trabajo de desarrollo, aplicando políticas personalizables (Quality Gates) para evitar que código problemático sea liberado.

## ¿Por qué usar SonarQube?

- **Detección temprana de Issues** – Se integra con pipelines de CI/CD para revisar automáticamente cada commit y pull request.
- **Hacer cumplir estándares de calidad** – Definir Quality Gates que deben pasar (por ejemplo, sin nuevos bugs, umbral de cobertura) antes de que una compilación pueda tener éxito.
- **Reducir la Deuda Técnica** – Cuantificar el esfuerzo necesario para corregir Issues existentes y realizar un seguimiento de las mejoras a lo largo del tiempo.
- **Mejorar la Seguridad** – Identificar vulnerabilidades del OWASP Top 10 y CWE, y marcar puntos críticos (Security Hotspots) para revisión manual.
- **Automatizar Revisiones de Código** – Delegar la detección de Issues simples (formato, punteros nulos, fugas de recursos) de los revisores humanos, para que puedan centrarse en la arquitectura y la lógica.

## Características clave

### Análisis Estático de Código
SonarQube escanea el código fuente en busca de Issues de fiabilidad, seguridad y mantenibilidad. Realiza análisis avanzados de flujo de datos y flujo de control para detectar:
- Posibles desreferencias de puntero nulo
- Fugas de recursos
- Fallos de inyección SQL y Cross-Site Scripting (XSS)
- Credenciales codificadas

### Quality Gates
Un Quality Gate es un conjunto de condiciones booleanas sobre métricas (por ejemplo, `New Coverage < 80%`, `New Bugs > 0`) que deben cumplirse para que un proyecto pase. SonarQube incluye un gate por defecto, y puedes crear personalizados para adaptarlos a las políticas de tu equipo.

### Security Hotspots
SonarQube resalta código que requiere revisión de seguridad manual. Estos hotspots no se confirman automáticamente como vulnerabilidades, sino que son áreas donde un atacante podría potencialmente inyectar entrada maliciosa. Los desarrolladores pueden revisarlos y marcarlos como "Safe" o "Needs Review".

### Medición de Deuda Técnica
SonarQube traduce los Issues en una métrica de **Deuda Técnica**, expresada en días o costo (ej., USD). Esto ayuda a los equipos a presupuestar y priorizar la refactorización.

### Análisis de Ramas y Pull Requests
SonarQube puede analizar ramas de características (feature branches) y pull requests, permitiéndote aplicar Quality Gates solo en código nuevo. Esto encaja naturalmente en un flujo de trabajo **Clean as You Code**, donde el enfoque está en el diff en lugar de todo el código base.

### Integraciones DevOps
SonarQube se integra de forma nativa con:
- **GitHub, GitLab, Bitbucket** – Decoración de pull requests, comentarios en línea.
- **Jenkins, Azure DevOps, Travis CI, CircleCI** – Integración con pipelines de compilación.
- **Maven, Gradle, .NET, SonarScanner CLI** – Invocación de análisis.

### Extensión SonarLint para IDE
SonarLint (para VS Code, IntelliJ, Eclipse, Visual Studio) se conecta a un servidor SonarQube y aplica las mismas reglas localmente, brindando retroalimentación en tiempo real mientras escribes.

---

## Instalación

SonarQube requiere **Java 17+** y una base de datos dedicada (PostgreSQL recomendado para producción). Se ejecuta como una aplicación web independiente.

### Docker (inicio rápido para evaluación)

```bash
docker run -d --name sonarqube \
  -p 9000:9000 \
  -e SONAR_JDBC_URL=jdbc:postgresql://host:port/sonarqube \
  -e SONAR_JDBC_USERNAME=sonar \
  -e SONAR_JDBC_PASSWORD=sonar \
  sonarqube:community
```

> **Nota:** La Community Edition no incluye funciones avanzadas como análisis de ramas o decoración de pull requests. Para esas, considera la Developer Edition o superior.

### Instalación Manual (Linux / macOS)

1. Descarga la última versión desde [SonarSource Download](https://www.sonarsource.com/products/sonarqube/downloads/).
2. Extrae el archivo.
3. Configura la conexión a la base de datos en `conf/sonar.properties`:
   ```properties
   sonar.jdbc.url=jdbc:postgresql://localhost/sonarqube
   sonar.jdbc.username=sonar
   sonar.jdbc.password=sonar
   ```
4. Inicia el servidor:
   ```bash
   # Linux/macOS
   bin/linux-x86-64/sonar.sh start
   # Windows
   bin/windows-x86-64/StartSonar.bat
   ```
5. Accede a la interfaz web en `http://localhost:9000`. Credenciales por defecto: `admin` / `admin`.

---

## Uso Básico

### 1. Configurar un Proyecto

Inicia sesión en SonarQube, haz clic en **Create new project**, asígnale una clave y elige un Quality Profile y un Quality Gate. Luego genera un **Project Token** (ej., `sqa_xxxx`). Este token autentica al escáner.

### 2. Ejecutar un Análisis

#### Usando Maven

```bash
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=my-project \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqa_xxxx
```

#### Usando Gradle

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

#### Usando la CLI de SonarScanner

Instala el SonarScanner (descárgalo de SonarSource), luego:

```bash
sonar-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqa_xxxx
```

### 3. Revisar Resultados

Después de que se completa el análisis, el panel de SonarQube muestra:
- **Estado del Quality Gate** – Passed o Failed.
- **Issues** – Agrupados por severidad (Blocker, Critical, Major, Minor, Info) y tipo (Bug, Vulnerability, Code Smell).
- **Security Hotspots** – Áreas de código que necesitan revisión manual.
- **Coverage (Cobertura)** – Si tienes una herramienta como JaCoCo o dotCover, importa los informes de cobertura.
- **Duplications (Duplicaciones)** – Bloques duplicados resaltados.

---

## Integración con CI/CD

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

### Pipeline de Jenkins

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

## Metodología Clean as You Code

SonarQube fomenta un enfoque **Clean as You Code**: en lugar de intentar corregir cada Issue existente, concéntrate en evitar nuevos en el código que escribes hoy. Esto se refleja en:
- **Enfoque en Código Nuevo** – Las métricas y Quality Gates se centran en código nuevo/modificado.
- **Decoración de Pull Requests** – Los Issues se reportan directamente en los diffs de PR (GitHub, GitLab, Bitbucket).
- **SonarLint** – Los desarrolladores detectan Issues en su IDE antes de realizar el commit.

---

## Conclusión

SonarQube es una herramienta madura y ampliamente adoptada para el análisis estático y la gobernanza de calidad. Al integrarla en tu pipeline de desarrollo, puedes automatizar revisiones de código, hacer cumplir estándares de seguridad y gestionar la deuda técnica, lo que en última instancia permite entregar software más fiable y seguro.

Para funciones avanzadas (análisis de ramas, gestión de portafolios, cobertura específica por lenguaje), considera actualizar a las ediciones **Developer**, **Enterprise** o **Data Center** de SonarQube Server, o utiliza **SonarQube Cloud** (antes SonarCloud) alojado en la nube.