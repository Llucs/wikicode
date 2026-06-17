---
title: Trivy
description: Trivy is an open-source all-in-one security scanner for detecting vulnerabilities, misconfigurations, secrets, and licenses in containers, Kubernetes, code repositories, and cloud.
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

## What is Trivy?

Trivy (pronounced **"tri-vee"**, a play on "trivial") is an open‑source security scanner created by Aqua Security. Designed to make security scanning trivial for DevOps teams, it detects vulnerabilities, misconfigurations, secrets, and license issues across container images, file systems, Git repositories, Kubernetes clusters, and cloud environments.

Written in Go and distributed as a single static binary, Trivy is the most popular open‑source security scanner according to the community, known for its speed, accuracy, and simplicity.

**History**  
Trivy was created in 2019 by Teppei Fukuda (knqyf263) at Aqua Security as a lightweight CLI for container image vulnerabilities. It rapidly expanded to cover infrastructure‑as‑code (IaC), secrets, Kubernetes, and Software Bill of Materials (SBOM) generation, becoming a unified standard in DevSecOps workflows.

## Why Trivy?

Developers and security teams choose Trivy because it:

- **Unifies multiple scanners** – one tool for vulnerabilities, misconfigurations, secrets, licenses, and SBOM.
- **Is easy to install** – a single command or binary, no database setup required.
- **Is fast and accurate** – combines multiple vulnerability databases (NVD, GHSA, OSV, RedHat, etc.), caches results, and checks exploitation status (EPSS, CVSS) to minimise false positives.
- **Integrates everywhere** – native support for CI/CD (GitHub Actions, GitLab CI, Jenkins, CircleCI), container registries (Harbor, AWS ECR, GCR), and Kubernetes.

## Installation

Trivy can be installed via package managers, Docker, Go, or directly from GitHub releases.

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

For other systems (Windows, static binary, etc.) see the [official installation guide](https://trivy.dev/latest/getting-started/installation/).

## Basic Usage

Trivy provides several subcommands (`image`, `fs`, `repo`, `config`, `k8s`). Here are the most common ones:

### Scan a container image for vulnerabilities

```bash
trivy image nginx:alpine
```

### Scan with severity filter and JSON output

```bash
trivy image --severity CRITICAL,HIGH --format json nginx:alpine
```

### Scan local filesystem (vulnerabilities, secrets, misconfigurations)

```bash
# Default: scans for OS packages and language dependencies
trivy fs .

# Specify multiple scanners
trivy fs --scanners vuln,secret,config .
```

### Scan a remote Git repository

```bash
trivy repo https://github.com/knqyf263/vuln-image
```

### Scan IaC templates (Terraform, Dockerfile, Kubernetes YAML, CloudFormation, Helm)

```bash
trivy config ./my-terraform-project/
```

### Scan a Kubernetes cluster

```bash
trivy k8s cluster     # entire cluster
trivy k8s node        # specific node
trivy k8s deployment  # deployment scanning
```

### Generate a Software Bill of Materials (SBOM)

```bash
# CycloneDX format
trivy image --format cyclonedx --output alpine.cdx.json alpine:3.15

# SPDX format
trivy image --format spdx-json --output alpine.spdx.json alpine:3.15
```

### Scan for secrets in a repository

```bash
trivy fs --scanners secret --severity HIGH,CRITICAL .
```

## Key Features

### 1. Vulnerability scanning
Trivy covers OS packages (Alpine, Debian, Ubuntu, CentOS, RHEL, etc.) and application dependencies (npm, pip, bundler, cargo, Maven, Go modules, NuGet, Composer, and more). It updates its vulnerability database automatically.

```bash
# Scan an image and only show fixable vulnerabilities
trivy image --ignore-unfixed alpine:3.15
```

### 2. Infrastructure as Code (IaC) scanning
Detects misconfigurations in Terraform, Dockerfiles, Kubernetes YAML, CloudFormation, and Helm charts using a rich set of built‑in policies.

```bash
# Scan a directory of Terraform files
trivy config --tf-exclude-downloaded-modules ./terraform/
```

### 3. Secret detection
Identifies hardcoded credentials, API keys, tokens, and other secrets using pattern matching and entropy analysis.

```bash
# Scan local directory for secrets with high confidence
trivy fs --scanners secret --secret-config trivy-secret.yaml .
```

### 4. SBOM generation and license compliance
Export a Software Bill of Materials in CycloneDX or SPDX format, and audit dependency licenses.

```bash
# Generate SBOM and check licenses
trivy image --format cyclonedx --licenses alpine:3.15
```

### 5. Kubernetes security auditing
Scan your entire cluster for vulnerable images, insecure RBAC configurations, and exposed secrets.

```bash
# Full cluster scan
trivy k8s cluster --report summary
```

### 6. High performance and caching
Trivy caches vulnerability database updates and image layer analysis, making repeated scans extremely fast.

```bash
# Clear cache and scan fresh
trivy image --clear-cache --no-cache alpine:latest
```

### 7. Multiple output formats
Supports table, JSON, SARIF, HTML, CycloneDX, SPDX, and more for integration with other tools.

```bash
# SARIF output (useful for GitHub Code Scanning)
trivy image --format sarif --output results.sarif nginx:alpine
```

## Integration Example: GitHub Actions

Trivy integrates natively with GitHub Actions. The workflow below scans every push for critical vulnerabilities and secrets.

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

## Resources

- **Official documentation:** <https://trivy.dev>
- **GitHub repository:** <https://github.com/aquasecurity/trivy>
- **Release notes:** <https://github.com/aquasecurity/trivy/releases>

---

*Trivy makes security scanning trivial – one binary, no setup, and a unified view of your software supply chain risks.*