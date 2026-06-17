---
title: Trivy
description: Trivy ist ein quelloffener All-in-One-Sicherheitsscanner zur Erkennung von Schwachstellen, Fehlkonfigurationen, Geheimnissen und Lizenzen in Containern, Kubernetes, Code-Repositories und der Cloud.
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

## Was ist Trivy?

Trivy (ausgesprochen **"tri-vee"**, ein Wortspiel mit "trivial") ist ein quelloffener Sicherheitsscanner, der von Aqua Security entwickelt wurde. Es wurde entwickelt, um Sicherheitsscans für DevOps-Teams trivial zu machen, und erkennt Schwachstellen, Fehlkonfigurationen, Geheimnisse und Lizenzprobleme in Container-Images, Dateisystemen, Git-Repositories, Kubernetes-Clustern und Cloud-Umgebungen.

Trivy ist in Go geschrieben und wird als einzelne statische Binärdatei verteilt. Es ist laut der Community der beliebteste quelloffene Sicherheitsscanner und bekannt für seine Geschwindigkeit, Genauigkeit und Einfachheit.

**Geschichte**  
Trivy wurde 2019 von Teppei Fukuda (knqyf263) bei Aqua Security als leichtgewichtiges CLI für Schwachstellen in Container-Images entwickelt. Es erweiterte sich schnell auf Infrastructure-as-Code (IaC), Geheimnisse, Kubernetes und die Generierung von Software-Stücklisten (SBOM) und wurde zu einem einheitlichen Standard in DevSecOps-Workflows.

## Warum Trivy?

Entwickler und Sicherheitsteams wählen Trivy, weil es:

- **Vereint mehrere Scanner** – ein Werkzeug für Schwachstellen, Fehlkonfigurationen, Geheimnisse, Lizenzen und SBOM.
- **Ist einfach zu installieren** – ein einzelner Befehl oder eine Binärdatei, keine Datenbankeinrichtung erforderlich.
- **Ist schnell und genau** – kombiniert mehrere Schwachstellendatenbanken (NVD, GHSA, OSV, RedHat usw.), speichert Ergebnisse zwischen und prüft den Ausnutzungsstatus (EPSS, CVSS), um Fehlalarme zu minimieren.
- **Integriert überall** – native Unterstützung für CI/CD (GitHub Actions, GitLab CI, Jenkins, CircleCI), Container-Registries (Harbor, AWS ECR, GCR) und Kubernetes.

## Installation

Trivy kann über Paketmanager, Docker, Go oder direkt über GitHub-Releases installiert werden.

```bash
# macOS (Homebrew)
brew install trivy

# Debian/Ubuntu (offizielles Repository hinzufügen)
sudo apt-get install trivy

# RHEL/CentOS (offizielles Repository hinzufügen)
sudo yum install trivy

# Docker
docker pull aquasec/trivy

# Go
go install github.com/aquasecurity/trivy/cmd/trivy@latest
```

Für andere Systeme (Windows, statische Binärdatei usw.) siehe die [offizielle Installationsanleitung](https://trivy.dev/latest/getting-started/installation/).

## Grundlegende Verwendung

Trivy bietet mehrere Unterbefehle (`image`, `fs`, `repo`, `config`, `k8s`). Hier sind die gängigsten:

### Ein Container-Image auf Schwachstellen scannen

```bash
trivy image nginx:alpine
```

### Mit Schweregradfilter und JSON-Ausgabe scannen

```bash
trivy image --severity CRITICAL,HIGH --format json nginx:alpine
```

### Lokales Dateisystem scannen (Schwachstellen, Geheimnisse, Fehlkonfigurationen)

```bash
# Standard: scannt nach Betriebssystempaketen und Sprachabhängigkeiten
trivy fs .

# Mehrere Scanner angeben
trivy fs --scanners vuln,secret,config .
```

### Ein entferntes Git-Repository scannen

```bash
trivy repo https://github.com/knqyf263/vuln-image
```

### IaC-Vorlagen scannen (Terraform, Dockerfile, Kubernetes YAML, CloudFormation, Helm)

```bash
trivy config ./my-terraform-project/
```

### Einen Kubernetes-Cluster scannen

```bash
trivy k8s cluster     # gesamter Cluster
trivy k8s node        # bestimmter Knoten
trivy k8s deployment  # Deployment-Scan
```

### Eine Software-Stückliste (SBOM) generieren

```bash
# CycloneDX-Format
trivy image --format cyclonedx --output alpine.cdx.json alpine:3.15

# SPDX-Format
trivy image --format spdx-json --output alpine.spdx.json alpine:3.15
```

### Nach Geheimnissen in einem Repository scannen

```bash
trivy fs --scanners secret --severity HIGH,CRITICAL .
```

## Hauptfunktionen

### 1. Schwachstellenscan
Trivy deckt Betriebssystempakete (Alpine, Debian, Ubuntu, CentOS, RHEL usw.) und Anwendungsabhängigkeiten (npm, pip, bundler, cargo, Maven, Go-Module, NuGet, Composer und mehr) ab. Es aktualisiert seine Schwachstellendatenbank automatisch.

```bash
# Ein Image scannen und nur behebbare Schwachstellen anzeigen
trivy image --ignore-unfixed alpine:3.15
```

### 2. Infrastructure as Code (IaC)-Scan
Erkennt Fehlkonfigurationen in Terraform, Dockerfiles, Kubernetes YAML, CloudFormation und Helm-Charts mithilfe einer umfangreichen Sammlung integrierter Richtlinien.

```bash
# Ein Verzeichnis mit Terraform-Dateien scannen
trivy config --tf-exclude-downloaded-modules ./terraform/
```

### 3. Geheimniserkennung
Identifiziert hartcodierte Anmeldeinformationen, API-Schlüssel, Tokens und andere Geheimnisse mittels Mustervergleich und Entropieanalyse.

```bash
# Lokales Verzeichnis auf Geheimnisse mit hoher Vertrauenswürdigkeit scannen
trivy fs --scanners secret --secret-config trivy-secret.yaml .
```

### 4. SBOM-Generierung und Lizenzkonformität
Exportiert eine Software-Stückliste im CycloneDX- oder SPDX-Format und prüft die Lizenzen von Abhängigkeiten.

```bash
# SBOM generieren und Lizenzen prüfen
trivy image --format cyclonedx --licenses alpine:3.15
```

### 5. Kubernetes-Sicherheitsprüfung
Scannen Sie Ihren gesamten Cluster nach anfälligen Images, unsicheren RBAC-Konfigurationen und offengelegten Geheimnissen.

```bash
# Kompletter Clusterscan
trivy k8s cluster --report summary
```

### 6. Hohe Leistung und Caching
Trivy speichert Aktualisierungen der Schwachstellendatenbank und die Analyse von Image-Layern zwischen, wodurch wiederholte Scans extrem schnell werden.

```bash
# Cache leeren und frisch scannen
trivy image --clear-cache --no-cache alpine:latest
```

### 7. Mehrere Ausgabeformate
Unterstützt Tabelle, JSON, SARIF, HTML, CycloneDX, SPDX und mehr für die Integration mit anderen Werkzeugen.

```bash
# SARIF-Ausgabe (nützlich für GitHub Code Scanning)
trivy image --format sarif --output results.sarif nginx:alpine
```

## Integrationsbeispiel: GitHub Actions

Trivy integriert sich nativ in GitHub Actions. Der folgende Workflow scannt jeden Push nach kritischen Schwachstellen und Geheimnissen.

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

## Ressourcen

- **Offizielle Dokumentation:** <https://trivy.dev>
- **GitHub-Repository:** <https://github.com/aquasecurity/trivy>
- **Versionshinweise:** <https://github.com/aquasecurity/trivy/releases>

---

*Trivy macht Sicherheitsscans trivial – eine Binärdatei, keine Einrichtung und eine einheitliche Ansicht der Risiken Ihrer Softwarelieferkette.*