---
title: Trivy
description: Trivyは、コンテナ、Kubernetes、コードリポジトリ、クラウドにおける脆弱性、設定ミス、シークレット、ライセンスを検出するためのオープンソースのオールインワンセキュリティスキャナです。
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

## Trivyとは？

Trivy（発音は **"tri-vee"**、"trivial" をもじったもの）は、Aqua Security によって作成されたオープンソースのセキュリティスキャナです。DevOps チームにとってセキュリティスキャンを簡単にするよう設計されており、コンテナイメージ、ファイルシステム、Git リポジトリ、Kubernetes クラスタ、クラウド環境にわたって脆弱性、設定ミス、シークレット、ライセンスの問題を検出します。

Go で書かれ、単一の静的バイナリとして配布される Trivy は、コミュニティによると最も人気のあるオープンソースセキュリティスキャナであり、その速度、正確性、シンプルさで知られています。

**歴史**  
Trivy は 2019 年に Aqua Security の Teppei Fukuda (knqyf263) によって、コンテナイメージの脆弱性のための軽量 CLI として作成されました。その後急速に拡大し、Infrastructure as Code (IaC)、シークレット、Kubernetes、ソフトウェア部品表 (SBOM) 生成をカバーするようになり、DevSecOps ワークフローにおける統一された標準となりました。

## Trivy を選ぶ理由

開発者とセキュリティチームが Trivy を選ぶ理由は以下の通りです。

- **複数のスキャナを統合** – 脆弱性、設定ミス、シークレット、ライセンス、SBOM のための単一のツール。
- **インストールが簡単** – 単一のコマンドまたはバイナリで、データベースのセットアップは不要。
- **高速かつ正確** – 複数の脆弱性データベース（NVD、GHSA、OSV、RedHat など）を組み合わせ、結果をキャッシュし、悪用状況（EPSS、CVSS）をチェックして誤検知を最小化。
- **あらゆる場所に統合** – CI/CD（GitHub Actions、GitLab CI、Jenkins、CircleCI）、コンテナレジストリ（Harbor、AWS ECR、GCR）、Kubernetes をネイティブサポート。

## インストール

Trivy はパッケージマネージャ、Docker、Go、または GitHub リリースから直接インストールできます。

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

他のシステム（Windows、静的バイナリなど）については、[公式インストールガイド](https://trivy.dev/latest/getting-started/installation/) を参照してください。

## 基本的な使用方法

Trivy はいくつかのサブコマンド（`image`、`fs`、`repo`、`config`、`k8s`）を提供します。最も一般的なものを以下に示します。

### コンテナイメージの脆弱性スキャン

```bash
trivy image nginx:alpine
```

### 重大度フィルタと JSON 出力によるスキャン

```bash
trivy image --severity CRITICAL,HIGH --format json nginx:alpine
```

### ローカルファイルシステムのスキャン（脆弱性、シークレット、設定ミス）

```bash
# Default: scans for OS packages and language dependencies
trivy fs .

# Specify multiple scanners
trivy fs --scanners vuln,secret,config .
```

### リモート Git リポジトリのスキャン

```bash
trivy repo https://github.com/knqyf263/vuln-image
```

### IaC テンプレートのスキャン（Terraform、Dockerfile、Kubernetes YAML、CloudFormation、Helm）

```bash
trivy config ./my-terraform-project/
```

### Kubernetes クラスタのスキャン

```bash
trivy k8s cluster     # entire cluster
trivy k8s node        # specific node
trivy k8s deployment  # deployment scanning
```

### Software Bill of Materials (SBOM) の生成

```bash
# CycloneDX format
trivy image --format cyclonedx --output alpine.cdx.json alpine:3.15

# SPDX format
trivy image --format spdx-json --output alpine.spdx.json alpine:3.15
```

### リポジトリ内のシークレットのスキャン

```bash
trivy fs --scanners secret --severity HIGH,CRITICAL .
```

## 主な機能

### 1. 脆弱性スキャン
Trivy は OS パッケージ（Alpine、Debian、Ubuntu、CentOS、RHEL など）とアプリケーション依存関係（npm、pip、bundler、cargo、Maven、Go modules、NuGet、Composer など）をカバーします。脆弱性データベースは自動的に更新されます。

```bash
# Scan an image and only show fixable vulnerabilities
trivy image --ignore-unfixed alpine:3.15
```

### 2. Infrastructure as Code (IaC) スキャン
豊富な組み込みポリシーを使用して、Terraform、Dockerfile、Kubernetes YAML、CloudFormation、Helm チャートの設定ミスを検出します。

```bash
# Scan a directory of Terraform files
trivy config --tf-exclude-downloaded-modules ./terraform/
```

### 3. シークレット検出
パターンマッチングとエントロピー分析を使用して、ハードコードされた認証情報、API キー、トークン、その他のシークレットを特定します。

```bash
# Scan local directory for secrets with high confidence
trivy fs --scanners secret --secret-config trivy-secret.yaml .
```

### 4. SBOM 生成とライセンス準拠
Software Bill of Materials を CycloneDX または SPDX 形式でエクスポートし、依存関係のライセンスを監査します。

```bash
# Generate SBOM and check licenses
trivy image --format cyclonedx --licenses alpine:3.15
```

### 5. Kubernetes セキュリティ監査
クラスタ全体をスキャンして、脆弱なイメージ、安全でない RBAC 設定、露出したシークレットを検出します。

```bash
# Full cluster scan
trivy k8s cluster --report summary
```

### 6. 高性能とキャッシング
Trivy は脆弱性データベースの更新とイメージレイヤー分析をキャッシュし、繰り返しのスキャンを非常に高速にします。

```bash
# Clear cache and scan fresh
trivy image --clear-cache --no-cache alpine:latest
```

### 7. 複数の出力形式
テーブル、JSON、SARIF、HTML、CycloneDX、SPDX など、他のツールとの統合のための複数の出力形式をサポートします。

```bash
# SARIF output (useful for GitHub Code Scanning)
trivy image --format sarif --output results.sarif nginx:alpine
```

## 統合例: GitHub Actions

Trivy は GitHub Actions とネイティブに統合されます。以下のワークフローは、プッシュごとに重大な脆弱性とシークレットをスキャンします。

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

## リソース

- **公式ドキュメント:** <https://trivy.dev>
- **GitHub リポジトリ:** <https://github.com/aquasecurity/trivy>
- **リリースノート:** <https://github.com/aquasecurity/trivy/releases>

---

*Trivy はセキュリティスキャンを簡単にします – 単一のバイナリ、セットアップ不要、ソフトウェアサプライチェーンリスクの統合ビュー。*