---
title: Trivy
description: Trivy 是一个开源的全能安全扫描器，用于检测容器、Kubernetes、代码仓库和云中的漏洞、配置错误、密钥和许可证。
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

## 什么是 Trivy?

Trivy（读作 **"tri-vee"**，是 "trivial" 的双关）是由 Aqua Security 创建的一款开源安全扫描器。它旨在让 DevOps 团队的安全扫描变得简单，可检测容器镜像、文件系统、Git 仓库、Kubernetes 集群和云环境中的漏洞、配置错误、密钥和许可问题。

Trivy 使用 Go 编写，并作为单一静态二进制文件分发，根据社区反馈，它是最受欢迎的开源安全扫描器，以其速度、准确性和简单性而闻名。

**历史**  
Trivy 于 2019 年由 Teppei Fukuda (knqyf263) 在 Aqua Security 创建，最初是一个用于容器镜像漏洞的轻量级 CLI 工具。它迅速扩展到覆盖基础设施即代码（IaC）、密钥、Kubernetes 和软件物料清单（SBOM）生成，成为 DevSecOps 工作流程中的统一标准。

## 为什么选择 Trivy?

开发者和安全团队选择 Trivy 是因为它：

- **统一多个扫描器** – 一个工具即可检测漏洞、配置错误、密钥、许可和 SBOM。
- **安装简单** – 只需一个命令或二进制文件，无需设置数据库。
- **快速且准确** – 结合多个漏洞数据库（NVD、GHSA、OSV、RedHat 等），缓存结果，并检查利用状态（EPSS、CVSS）以最大限度地减少误报。
- **随处集成** – 原生支持 CI/CD（GitHub Actions、GitLab CI、Jenkins、CircleCI）、容器镜像仓库（Harbor、AWS ECR、GCR）和 Kubernetes。

## 安装

Trivy 可以通过包管理器、Docker、Go 或直接从 GitHub 发布版本安装。

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

对于其他系统（Windows、静态二进制文件等），请参阅[官方安装指南](https://trivy.dev/latest/getting-started/installation/)。

## 基本用法

Trivy 提供多个子命令（`image`、`fs`、`repo`、`config`、`k8s`）。以下是最常用的几个：

### 扫描容器镜像漏洞

```bash
trivy image nginx:alpine
```

### 按严重程度过滤并以 JSON 格式输出

```bash
trivy image --severity CRITICAL,HIGH --format json nginx:alpine
```

### 扫描本地文件系统（漏洞、密钥、配置错误）

```bash
# Default: scans for OS packages and language dependencies
trivy fs .

# Specify multiple scanners
trivy fs --scanners vuln,secret,config .
```

### 扫描远程 Git 仓库

```bash
trivy repo https://github.com/knqyf263/vuln-image
```

### 扫描 IaC 模板（Terraform、Dockerfile、Kubernetes YAML、CloudFormation、Helm）

```bash
trivy config ./my-terraform-project/
```

### 扫描 Kubernetes 集群

```bash
trivy k8s cluster     # entire cluster
trivy k8s node        # specific node
trivy k8s deployment  # deployment scanning
```

### 生成软件物料清单 (SBOM)

```bash
# CycloneDX format
trivy image --format cyclonedx --output alpine.cdx.json alpine:3.15

# SPDX format
trivy image --format spdx-json --output alpine.spdx.json alpine:3.15
```

### 扫描仓库中的密钥

```bash
trivy fs --scanners secret --severity HIGH,CRITICAL .
```

## 主要特性

### 1. 漏洞扫描
Trivy 覆盖操作系统包（Alpine、Debian、Ubuntu、CentOS、RHEL 等）和应用程序依赖（npm、pip、bundler、cargo、Maven、Go 模块、NuGet、Composer 等）。它会自动更新漏洞数据库。

```bash
# Scan an image and only show fixable vulnerabilities
trivy image --ignore-unfixed alpine:3.15
```

### 2. 基础设施即代码（IaC）扫描
使用丰富的内置策略检测 Terraform、Dockerfile、Kubernetes YAML、CloudFormation 和 Helm Chart 中的配置错误。

```bash
# Scan a directory of Terraform files
trivy config --tf-exclude-downloaded-modules ./terraform/
```

### 3. 密钥检测
通过模式匹配和熵分析识别硬编码的凭据、API 密钥、令牌和其他密钥。

```bash
# Scan local directory for secrets with high confidence
trivy fs --scanners secret --secret-config trivy-secret.yaml .
```

### 4. SBOM 生成与许可证合规
以 CycloneDX 或 SPDX 格式导出软件物料清单，并审计依赖许可证。

```bash
# Generate SBOM and check licenses
trivy image --format cyclonedx --licenses alpine:3.15
```

### 5. Kubernetes 安全审计
扫描整个集群，查找存在漏洞的镜像、不安全的 RBAC 配置和暴露的密钥。

```bash
# Full cluster scan
trivy k8s cluster --report summary
```

### 6. 高性能与缓存
Trivy 会缓存漏洞数据库更新和镜像层分析结果，使重复扫描极快。

```bash
# Clear cache and scan fresh
trivy image --clear-cache --no-cache alpine:latest
```

### 7. 多种输出格式
支持表格、JSON、SARIF、HTML、CycloneDX、SPDX 等，便于与其他工具集成。

```bash
# SARIF output (useful for GitHub Code Scanning)
trivy image --format sarif --output results.sarif nginx:alpine
```

## 集成示例：GitHub Actions

Trivy 原生集成 GitHub Actions。以下工作流会在每次推送时扫描关键漏洞和密钥。

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

## 资源

- **官方文档：** <https://trivy.dev>
- **GitHub 仓库：** <https://github.com/aquasecurity/trivy>
- **发布说明：** <https://github.com/aquasecurity/trivy/releases>

---

*Trivy 让安全扫描变得简单——一个二进制文件，无需设置，即可统一查看您的软件供应链风险。*