---
title: Trivy
description: Trivy est un scanner de sécurité tout-en-un open-source pour détecter les vulnérabilités, les erreurs de configuration, les secrets et les licences dans les conteneurs, Kubernetes, les dépôts de code et le cloud.
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

## Qu'est-ce que Trivy ?

Trivy (prononcé **"tri-vee"**, un jeu de mots sur "trivial") est un scanner de sécurité open‑source créé par Aqua Security. Conçu pour rendre le scan de sécurité trivial pour les équipes DevOps, il détecte les vulnérabilités, les erreurs de configuration, les secrets et les problèmes de licence à travers les images de conteneurs, les systèmes de fichiers, les dépôts Git, les clusters Kubernetes et les environnements cloud.

Écrit en Go et distribué en tant que binaire statique unique, Trivy est le scanner de sécurité open‑source le plus populaire selon la communauté, connu pour sa rapidité, sa précision et sa simplicité.

**Histoire**  
Trivy a été créé en 2019 par Teppei Fukuda (knqyf263) chez Aqua Security en tant qu'outil CLI léger pour les vulnérabilités des images de conteneurs. Il s'est rapidement étendu pour couvrir l'infrastructure‑en‑tant‑que‑code (IaC), les secrets, Kubernetes et la génération de Software Bill of Materials (SBOM), devenant ainsi un standard unifié dans les workflows DevSecOps.

## Pourquoi Trivy ?

Les développeurs et les équipes de sécurité choisissent Trivy car il :

- **Unifie plusieurs scanners** – un seul outil pour les vulnérabilités, les erreurs de configuration, les secrets, les licences et les SBOM.
- **Est facile à installer** – une seule commande ou binaire, aucune configuration de base de données requise.
- **Est rapide et précis** – combine plusieurs bases de données de vulnérabilités (NVD, GHSA, OSV, RedHat, etc.), met en cache les résultats et vérifie le statut d'exploitation (EPSS, CVSS) pour minimiser les faux positifs.
- **S'intègre partout** – support natif pour les CI/CD (GitHub Actions, GitLab CI, Jenkins, CircleCI), les registres de conteneurs (Harbor, AWS ECR, GCR) et Kubernetes.

## Installation

Trivy peut être installé via les gestionnaires de paquets, Docker, Go, ou directement depuis les releases GitHub.

```bash
# macOS (Homebrew)
brew install trivy

# Debian/Ubuntu (add official repository)
sudo apt-get install trivy

# RHEL/CentOS (add official repository)
sudo yum install trivy

# Docker
docker pull aquasec/trivy

# Go
go install github.com/aquasecurity/trivy/cmd/trivy@latest
```

Pour d'autres systèmes (Windows, binaire statique, etc.) consultez le [guide d'installation officiel](https://trivy.dev/latest/getting-started/installation/).

## Utilisation de base

Trivy fournit plusieurs sous-commandes (`image`, `fs`, `repo`, `config`, `k8s`). Voici les plus courantes :

### Scanner une image de conteneur pour les vulnérabilités

```bash
trivy image nginx:alpine
```

### Scanner avec filtre de sévérité et sortie JSON

```bash
trivy image --severity CRITICAL,HIGH --format json nginx:alpine
```

### Scanner le système de fichiers local (vulnérabilités, secrets, erreurs de configuration)

```bash
# Default: scans for OS packages and language dependencies
trivy fs .

# Specify multiple scanners
trivy fs --scanners vuln,secret,config .
```

### Scanner un dépôt Git distant

```bash
trivy repo https://github.com/knqyf263/vuln-image
```

### Scanner les modèles IaC (Terraform, Dockerfile, Kubernetes YAML, CloudFormation, Helm)

```bash
trivy config ./my-terraform-project/
```

### Scanner un cluster Kubernetes

```bash
trivy k8s cluster     # entire cluster
trivy k8s node        # specific node
trivy k8s deployment  # deployment scanning
```

### Générer un Software Bill of Materials (SBOM)

```bash
# CycloneDX format
trivy image --format cyclonedx --output alpine.cdx.json alpine:3.15

# SPDX format
trivy image --format spdx-json --output alpine.spdx.json alpine:3.15
```

### Scanner les secrets dans un dépôt

```bash
trivy fs --scanners secret --severity HIGH,CRITICAL .
```

## Fonctionnalités clés

### 1. Scan des vulnérabilités
Trivy couvre les paquets OS (Alpine, Debian, Ubuntu, CentOS, RHEL, etc.) et les dépendances applicatives (npm, pip, bundler, cargo, Maven, Go modules, NuGet, Composer, et plus). Il met à jour sa base de données de vulnérabilités automatiquement.

```bash
# Scan an image and only show fixable vulnerabilities
trivy image --ignore-unfixed alpine:3.15
```

### 2. Scan de l'infrastructure en tant que code (IaC)
Détecte les erreurs de configuration dans les fichiers Terraform, Dockerfiles, Kubernetes YAML, CloudFormation et Helm en utilisant un ensemble riche de politiques intégrées.

```bash
# Scan a directory of Terraform files
trivy config --tf-exclude-downloaded-modules ./terraform/
```

### 3. Détection de secrets
Identifie les informations d'identification codées en dur, les clés API, les jetons et autres secrets en utilisant la correspondance de motifs et l'analyse d'entropie.

```bash
# Scan local directory for secrets with high confidence
trivy fs --scanners secret --secret-config trivy-secret.yaml .
```

### 4. Génération de SBOM et conformité des licences
Exportez un Software Bill of Materials au format CycloneDX ou SPDX, et auditez les licences des dépendances.

```bash
# Generate SBOM and check licenses
trivy image --format cyclonedx --licenses alpine:3.15
```

### 5. Audit de sécurité Kubernetes
Scannez l'intégralité de votre cluster pour les images vulnérables, les configurations RBAC non sécurisées et les secrets exposés.

```bash
# Full cluster scan
trivy k8s cluster --report summary
```

### 6. Haute performance et mise en cache
Trivy met en cache les mises à jour de la base de données de vulnérabilités et l'analyse des couches d'images, rendant les scans répétés extrêmement rapides.

```bash
# Clear cache and scan fresh
trivy image --clear-cache --no-cache alpine:latest
```

### 7. Formats de sortie multiples
Prend en charge les formats table, JSON, SARIF, HTML, CycloneDX, SPDX, et plus encore pour l'intégration avec d'autres outils.

```bash
# SARIF output (useful for GitHub Code Scanning)
trivy image --format sarif --output results.sarif nginx:alpine
```

## Exemple d'intégration : GitHub Actions

Trivy s'intègre nativement avec GitHub Actions. Le workflow ci-dessous scanne chaque push pour les vulnérabilités critiques et les secrets.

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

## Ressources

- **Documentation officielle :** <https://trivy.dev>
- **Dépôt GitHub :** <https://github.com/aquasecurity/trivy>
- **Notes de version :** <https://github.com/aquasecurity/trivy/releases>

---

*Trivy rend le scan de sécurité trivial – un binaire, aucune configuration, et une vue unifiée des risques de votre chaîne d'approvisionnement logicielle.*