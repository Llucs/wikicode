---
title: Trivy
description: Trivy es un escáner de seguridad todo-en-uno open-source para detectar vulnerabilidades, configuraciones erróneas, secretos y licencias en contenedores, Kubernetes, repositorios de código y la nube.
created: 2026-06-17
tags:
  - security
  - devsecops
  - scanning
  - container-security
  - kubernetes
  - opensource
status: draft
---

# Trivy

## ¿Qué es Trivy?

Trivy (pronunciado **"tri-vee"**, un juego de palabras con "trivial") es un escáner de seguridad open‑source creado por Aqua Security. Diseñado para hacer que el escaneo de seguridad sea trivial para los equipos DevOps, detecta vulnerabilidades, configuraciones erróneas, secretos y problemas de licencias en imágenes de contenedores, sistemas de archivos, repositorios Git, clústeres de Kubernetes y entornos en la nube.

Escrito en Go y distribuido como un único binario estático, Trivy es el escáner de seguridad open‑source más popular según la comunidad, conocido por su velocidad, precisión y simplicidad.

**Historia**  
Trivy fue creado en 2019 por Teppei Fukuda (knqyf263) en Aqua Security como un CLI ligero para vulnerabilidades de imágenes de contenedores. Rápidamente se expandió para cubrir infraestructura como código (IaC), secretos, Kubernetes y generación de listas de materiales de software (SBOM), convirtiéndose en un estándar unificado en los flujos de trabajo DevSecOps.

## ¿Por qué Trivy?

Los desarrolladores y los equipos de seguridad eligen Trivy porque:

- **Unifica múltiples escáneres** – una herramienta para vulnerabilidades, configuraciones erróneas, secretos, licencias y SBOM.
- **Es fácil de instalar** – un solo comando o binario, no requiere configuración de base de datos.
- **Es rápido y preciso** – combina múltiples bases de datos de vulnerabilidades (NVD, GHSA, OSV, RedHat, etc.), almacena en caché los resultados y verifica el estado de explotación (EPSS, CVSS) para minimizar falsos positivos.
- **Se integra en todas partes** – soporte nativo para CI/CD (GitHub Actions, GitLab CI, Jenkins, CircleCI), registros de contenedores (Harbor, AWS ECR, GCR) y Kubernetes.

## Instalación

Trivy se puede instalar a través de gestores de paquetes, Docker, Go o directamente desde las releases de GitHub.

```bash
# macOS (Homebrew)
brew install trivy

# Debian/Ubuntu (añadir repositorio oficial)
sudo apt-get install trivy

# RHEL/CentOS (añadir repositorio oficial)
sudo yum install trivy

# Docker
docker pull aquasec/trivy

# Go
go install github.com/aquasecurity/trivy/cmd/trivy@latest
```

Para otros sistemas (Windows, binario estático, etc.) consulte la [guía de instalación oficial](https://trivy.dev/latest/getting-started/installation/).

## Uso básico

Trivy proporciona varios subcomandos (`image`, `fs`, `repo`, `config`, `k8s`). Aquí están los más comunes:

### Escanear una imagen de contenedor en busca de vulnerabilidades

```bash
trivy image nginx:alpine
```

### Escanear con filtro de severidad y salida JSON

```bash
trivy image --severity CRITICAL,HIGH --format json nginx:alpine
```

### Escanear el sistema de archivos local (vulnerabilidades, secretos, configuraciones erróneas)

```bash
# Por defecto: escanea paquetes del SO y dependencias de lenguajes
trivy fs .

# Especificar múltiples escáneres
trivy fs --scanners vuln,secret,config .
```

### Escanear un repositorio Git remoto

```bash
trivy repo https://github.com/knqyf263/vuln-image
```

### Escanear plantillas IaC (Terraform, Dockerfile, YAML de Kubernetes, CloudFormation, Helm)

```bash
trivy config ./my-terraform-project/
```

### Escanear un clúster de Kubernetes

```bash
trivy k8s cluster     # clúster completo
trivy k8s node        # nodo específico
trivy k8s deployment  # escaneo de deployments
```

### Generar una lista de materiales de software (SBOM)

```bash
# Formato CycloneDX
trivy image --format cyclonedx --output alpine.cdx.json alpine:3.15

# Formato SPDX
trivy image --format spdx-json --output alpine.spdx.json alpine:3.15
```

### Escanear en busca de secretos en un repositorio

```bash
trivy fs --scanners secret --severity HIGH,CRITICAL .
```

## Características principales

### 1. Escaneo de vulnerabilidades

Trivy cubre paquetes del SO (Alpine, Debian, Ubuntu, CentOS, RHEL, etc.) y dependencias de aplicaciones (npm, pip, bundler, cargo, Maven, módulos de Go, NuGet, Composer, y más). Actualiza su base de datos de vulnerabilidades automáticamente.

```bash
# Escanear una imagen y mostrar solo vulnerabilidades corregibles
trivy image --ignore-unfixed alpine:3.15
```

### 2. Escaneo de infraestructura como código (IaC)

Detecta configuraciones erróneas en Terraform, Dockerfiles, YAML de Kubernetes, CloudFormation y charts de Helm utilizando un rico conjunto de políticas integradas.

```bash
# Escanear un directorio de archivos Terraform
trivy config --tf-exclude-downloaded-modules ./terraform/
```

### 3. Detección de secretos

Identifica credenciales hardcodeadas, claves de API, tokens y otros secretos mediante coincidencia de patrones y análisis de entropía.

```bash
# Escanear directorio local en busca de secretos con alta confianza
trivy fs --scanners secret --secret-config trivy-secret.yaml .
```

### 4. Generación de SBOM y cumplimiento de licencias

Exporta una lista de materiales de software en formato CycloneDX o SPDX, y audita las licencias de dependencias.

```bash
# Generar SBOM y verificar licencias
trivy image --format cyclonedx --licenses alpine:3.15
```

### 5. Auditoría de seguridad de Kubernetes

Escanea todo tu clúster en busca de imágenes vulnerables, configuraciones RBAC inseguras y secretos expuestos.

```bash
# Escaneo completo del clúster
trivy k8s cluster --report summary
```

### 6. Alto rendimiento y almacenamiento en caché

Trivy almacena en caché las actualizaciones de la base de datos de vulnerabilidades y el análisis de capas de imágenes, haciendo que los escaneos repetidos sean extremadamente rápidos.

```bash
# Limpiar caché y escanear de nuevo
trivy image --clear-cache --no-cache alpine:latest
```

### 7. Múltiples formatos de salida

Soporta table, JSON, SARIF, HTML, CycloneDX, SPDX, y más para integración con otras herramientas.

```bash
# Salida SARIF (útil para GitHub Code Scanning)
trivy image --format sarif --output results.sarif nginx:alpine
```

## Ejemplo de integración: GitHub Actions

Trivy se integra de forma nativa con GitHub Actions. El flujo de trabajo a continuación escanea cada push en busca de vulnerabilidades críticas y secretos.

```yaml
name: Trivy Scan
on: [push]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Trivy filesystem scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
```

## Recursos

- **Documentación oficial:** <https://trivy.dev>
- **Repositorio en GitHub:** <https://github.com/aquasecurity/trivy>
- **Notas de lanzamiento:** <https://github.com/aquasecurity/trivy/releases>

---

*Trivy hace que el escaneo de seguridad sea trivial: un solo binario, sin configuración y una vista unificada de los riesgos de tu cadena de suministro de software.*