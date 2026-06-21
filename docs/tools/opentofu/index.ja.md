---
title: OpenTofu
description: OpenTofuは、オープンソースのInfrastructure as Code (IaC)ツールであり、Terraformからフォークされ、Linux Foundationによって運営されており、クラウド、オンプレミス、エッジリソースの安全で予測可能な管理を実現します。
created: 2026-06-21
tags:
  - infrastructure-as-code
  - opentofu
  - linux-foundation
  - cloud-provisioning
  - devops
  - terraform-fork
status: draft
---

# OpenTofu

## OpenTofuとは？

OpenTofuは、宣言的なInfrastructure as Code (IaC)ツールであり、高水準の設定言語（HCL）を使用してインフラストラクチャを定義、プロビジョニング、管理することができます。依存関係グラフを構築することで、パブリッククラウドプロバイダー（AWS、Azure、GCP）、プライベートデータセンター、SaaSサービス全体のリソースを安全かつ効率的に作成、変更、削除できるようにします。

OpenTofuは、2023年にHashiCorpのライセンス変更に対応して、コミュニティ主導でTerraformを直接フォークしたものです。現在はLinux Foundationのプロジェクトであり、Mozilla Public License（MPL 2.0）の下で永久に完全なオープンソースであり続けることが保証されています。

## OpenTofuを選ぶ理由

- **オープンソースの保証:** MPL 2.0ライセンスにより、単一のベンダーがライセンス条項を制限的なライセンス（BSLなど）に変更することを防ぎます。
- **Linux Foundationによるガバナンス:** 多様なメンテナーと複数の企業支援者を擁する、中立的でコミュニティ主導の拠点です。
- **エコシステムとの互換性:** 既存のTerraformプロバイダー、モジュール、ステートファイルとシームレスに連携し、移行を容易にします。
- **革新性:** コミュニティは、エンドツーエンドのステート暗号化、OCIレジストリサポート、ノーコードプロビジョニングなど、長年にわたって要望されてきた強力な機能を追加しています。
- **ベンダー中立的:** 特定のクラウドプロバイダーやSaaSプラットフォームに依存しません。

## インストール

OpenTofuは、主要なオペレーティングシステム向けに`tofu` CLIツールを提供しています。

```bash
# macOS (Homebrew)
brew install opentofu

# Debian / Ubuntu
wget -O- https://packages.opentofu.org/opentofu/tofu/gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/opentofu.gpg
echo "deb [signed-by=/etc/apt/keyrings/opentofu.gpg] https://packages.opentofu.org/opentofu/tofu/debian stable main" | sudo tee /etc/apt/sources.list.d/opentofu.list
sudo apt-get update && sudo apt-get install opentofu

# RHEL / Fedora
sudo dnf install -y dnf-plugins-core
sudo dnf config-manager --add-repo https://packages.opentofu.org/opentofu/tofu/rpm/opentofu.repo
sudo dnf install -y opentofu

# Windows (Winget)
winget install opentofu

# Docker
docker pull ghcr.io/opentofu/opentofu:latest
```

## クイックスタート / 基本的なワークフロー

コアワークフローはTerraformと同じであり、移行は簡単です。`.tf`ファイルに設定を記述し、`tofu`コマンドを使用します。

**`main.tf`という名前のファイルを作成します:**

```hcl
terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

resource "random_pet" "server_name" {
  length = 2
}

output "name" {
  value = random_pet.server_name.id
}
```

**ワークフローを実行します:**

```bash
# Initialize the directory and download providers
tofu init

# Format and validate the configuration
tofu fmt
tofu validate

# Create an execution plan
tofu plan -out=tfplan

# Apply the plan
tofu apply tfplan

# Destroy the resources
tofu destroy
```

## 主要機能と差別化ポイント

### 1. クライアント側ステート暗号化

OpenTofuは、ステートファイル全体をバックエンド（例：S3、GCS、Azure Storage）に送信する**前**にクライアント側で暗号化できます。これにより「多層防御」が提供され、バックエンドの運用者はキーなしではステートデータを読み取ることができません。

```hcl
terraform {
  encryption {
    key_provider "pbkdf2" "my_passphrase" {
      passphrase = var.encryption_passphrase
    }
    method "aes_gcm" "my_method" {
      keys = key_provider.pbkdf2.my_passphrase
    }
    state {
      method = method.aes_gcm.my_method
    }
    plan {
      method = method.aes_gcm.my_method
    }
  }
}
```

### 2. プロバイダーとモジュールのOCIレジストリサポート

プロバイダーとモジュールは、**あらゆる**OCI準拠レジストリ（Docker Hub、AWS ECR、Harbor、GitHub Container Registry）から取得できます。これは以下の場合に重要です：

- **エアギャップ環境:** すべてのプロバイダーを内部レジストリでホストします。
- **プライベートプロバイダー:** 別のレジストリサービスを実行する必要がありません。
- **アーティファクトサプライチェーンセキュリティ:** コンテナの署名とスキャンを活用します。

```hcl
terraform {
  required_providers {
    my_internal = {
      source  = "oci://ghcr.io/my-org/my-provider"
      version = ">= 1.0.0"
    }
  }
}
```

### 3. ノーコードプロビジョニング

プラットフォームエンジニアリングチームは、再利用可能なモジュールを構築し、エンドユーザーがHCL設定を記述することなくレジストリから直接デプロイできるようにします。ユーザーは入力変数のみを提供します。

```bash
# Deploy a module from a registry directly
tofu init -from-module=my-org/vpc-module/aws
tofu plan -var="cidr_block=10.0.0.0/16"
tofu apply
```

### 4. プロバイダー定義関数

OpenTofuは、プロバイダーがHCLから直接呼び出せるカスタム関数を公開することを可能にします。これにより言語が拡張され、プロバイダーは従来の純粋なHCLでは不可能だった操作を実行できるようになります。

```hcl
# Example: Using an encryption function from a Vault provider
locals {
  encrypted_secret = provider::vault::encode_string(var.raw_secret)
}
```

### 5. 変数とローカルの早期評価

変数とローカルは、プロバイダーの初期化が完了する前の解析フェーズ中に評価できます。これにより、変数の値に基づいてバックエンド設定を動的に構築するなどの強力なパターンが可能になります。

```hcl
variable "region" {
  type    = string
  default = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "my-state-${var.region}"
    key    = "infra/terraform.tfstate"
  }
}
```

### 6. ネイティブテストフレームワーク

`tofu test`コマンドを使用して、モジュールのユニットテストと統合テストを記述します。

```hcl
# tests/default.tftest.hcl
run "test_vpc_creation" {
  command = apply

  variables {
    vpc_cidr = "10.0.0.0/16"
  }

  assert {
    condition     = output.vpc_cidr == "10.0.0.0/16"
    error_message = "The VPC CIDR block did not match the expected value."
  }
}
```

テストを実行します：
```bash
tofu test
```

## 高度な使用方法

- **リモートバックエンド:** 完全なロックサポート（例：DynamoDB）を備えたS3、GCS、Azurerm、またはHTTPバックエンドにステートを保存します。
- **プロバイダーキャッシング:** ローカルまたは共有ミラーを使用してプロバイダープラグインをキャッシュし、CI/CDワークフローを大幅に高速化します。
- **ワークスペース:** 同じ設定で複数の環境（dev、staging、prod）を管理します。
- **構造化ログ:** CI/CDシステム向けの機械可読な出力を得るために`tofu apply -json`を実行します。

## Terraformからの移行

OpenTofuへの移行は安全でリスクの低い操作です：

1. **OpenTofuをインストールします。**
2. **既存のTerraformプロジェクトに移動します。**
3. **`tofu init`を実行します。** OpenTofuは既存の`.terraform`ディレクトリとステートファイルを認識し、それらを自身の`.tofu`ディレクトリにシームレスに移行します。
4. **`tofu plan`を実行して**、変更が検出されないことを確認します。
5. **コマンドを標準化します。** スクリプトとドキュメント内の`terraform`を`tofu`に置き換えます。

> **重要:** 移行後、再度`terraform`を実行すると`.terraform/`ディレクトリが再初期化され、混乱を引き起こす可能性があります。すべてのチームワークフローを`tofu`コマンドに移行し、PATHからTerraformを削除することをお勧めします。

## 比較：OpenTofu vs HashiCorp Terraform（2026）

| 機能 | OpenTofu | HashiCorp Terraform |
|---|---|---|
| **ライセンス** | MPL 2.0（オープンソース） | Business Source License（BUSL） |
| **ガバナンス** | Linux Foundation | HashiCorp, Inc. |
| **ステート暗号化** | ネイティブ（クライアント側） | 部分的（Vault/バックエンドのみ） |
| **OCIレジストリ** | はい | いいえ |
| **ノーコードプロビジョニング** | はい（オープン） | はい（Cloudのみ） |
| **プロバイダー定義関数** | はい | いいえ |
| **テストフレームワーク** | ネイティブ（`tofu test`） | ネイティブ（`terraform test`） |
| **CLI** | `tofu` | `terraform` |
| **コア言語** | HCL / JSON | HCL / JSON |
| **プロバイダー/モジュールソース** | レジストリ、OCI、HTTP、Gitなど | レジストリ、HTTP、Gitなど |

## コミュニティとエコシステム

- **プロバイダー:** 主要なプロバイダーエコシステム（AWS、Azure、GCP、Kubernetes、Vault）はすべて完全にサポートされています。
- **レジストリ:** OpenTofu Registryは、数千のオープンソースモジュールをホストしています。
- **プラットフォームサポート:** Spacelift、env0、Scalr、Harnessなどのエコシステムパートナーからエンタープライズグレードのサポートが利用可能です。
- **コントリビューター:** OpenTofuは、何百人もの個人および企業のコントリビューターからなるコミュニティによってGitHub上でオープンに開発されています。

## まとめ

OpenTofuは、2026年におけるInfrastructure as Codeのための最高のオープンソースツールです。その強固なコミュニティ、ベンダー中立的なガバナンス、そして革新的な機能（ステート暗号化、OCIサポート、ノーコードプロビジョニング、充実したテストフレームワーク）は、あらゆるインフラストラクチャを大規模に管理するための安定した先進的なプラットフォームを提供します。

## リソース

- **公式ドキュメント:** [https://opentofu.org/docs/](https://opentofu.org/docs/)
- **GitHubリポジトリ:** [https://github.com/opentofu/opentofu](https://github.com/opentofu/opentofu)
- **レジストリ:** [https://github.com/opentofu/registry](https://github.com/opentofu/registry)
- **ダウンロードとインストール:** [https://opentofu.org/downloads/](https://opentofu.org/downloads/)
- **OpenTofuコミュニティ:** [https://opentofu.org/community/](https://opentofu.org/community/)