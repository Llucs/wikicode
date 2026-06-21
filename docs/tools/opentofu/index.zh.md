---
title: OpenTofu
description: OpenTofu 是一款开源的基础设施即代码（IaC）工具，源自 Terraform 的分支，由 Linux 基金会管理，能够安全且可预测地管理云、本地和边缘资源。
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

## 什么是 OpenTofu？

OpenTofu 是一种声明式基础设施即代码（IaC）工具，它允许你使用高级配置语言（HCL）来定义、配置和管理基础设施。它通过构建依赖图来管理公有云提供商（AWS、Azure、GCP）、私有数据中心和 SaaS 服务的资源，确保资源被安全高效地创建、修改和销毁。

它创建于 2023 年，是 Terraform 的直接社区驱动分支，以回应 HashiCorp 的许可证变更。OpenTofu 现在是 Linux 基金会的一个项目，确保其始终在 Mozilla Public License（MPL 2.0）下完全开源。

## 为什么选择 OpenTofu？

- **开源保证：** MPL 2.0 许可证防止任何单一供应商将许可条款更改为限制性许可证（如 BSL）。
- **Linux 基金会治理：** 一个中立的、社区驱动的家园，拥有多样化的维护者和多个企业支持者。
- **生态兼容性：** 无缝兼容现有的 Terraform 提供商、模块和状态文件，使迁移轻松。
- **创新：** 社区添加了多年来一直需要的强大功能，如端到端状态加密、OCI 注册表支持和无代码配置。
- **供应商中立：** 不绑定于任何单一云提供商或 SaaS 平台。

## 安装

OpenTofu 在所有主要操作系统上提供 `tofu` CLI 工具。

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

## 快速开始 / 基本工作流

核心工作流与 Terraform 完全相同，使过渡变得简单。你在 `.tf` 文件中编写配置，并使用 `tofu` 命令。

**创建一个名为 `main.tf` 的文件：**

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

**运行工作流：**

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

## 主要特性与差异化

### 1. 客户端状态加密

OpenTofu 可以在状态文件发送到后端（例如 S3、GCS、Azure 存储）之前，在客户端对整个状态文件进行加密。这提供了"纵深防御"——后端操作员在没有密钥的情况下无法读取状态数据。

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

### 2. 提供商和模块的 OCI 注册表支持

提供商和模块可以从**任何**符合 OCI 标准的注册表（Docker Hub、AWS ECR、Harbor、GitHub Container Registry）获取。这对于以下场景至关重要：
- **离线环境：** 将所有提供商托管在内部注册表中。
- **私有提供商：** 无需运行单独的注册表服务。
- **工件供应链安全：** 利用容器签名和扫描。

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

### 3. 无代码配置

平台工程团队可以构建可复用的模块，并允许最终用户从注册表直接部署它们，而无需编写任何 HCL 配置。用户只需提供输入变量。

```bash
# Deploy a module from a registry directly
tofu init -from-module=my-org/vpc-module/aws
tofu plan -var="cidr_block=10.0.0.0/16"
tofu apply
```

### 4. 提供商定义的函数

OpenTofu 允许提供商公开自定义函数，这些函数可以直接从 HCL 中调用。这扩展了语言，并允许提供商执行以前在纯 HCL 中无法完成的操作。

```hcl
# Example: Using an encryption function from a Vault provider
locals {
  encrypted_secret = provider::vault::encode_string(var.raw_secret)
}
```

### 5. 早期变量和本地值求值

变量和本地值可以在解析阶段、提供商初始化完成之前进行评估。这使得可以实现强大的模式，例如基于变量值动态构建后端配置。

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

### 6. 原生测试框架

使用 `tofu test` 命令为模块编写单元测试和集成测试。

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

运行测试：
```bash
tofu test
```

## 高级用法

- **远程后端：** 在 S3、GCS、Azurerm 或 HTTP 后端中存储状态，并支持完整的锁定（例如 DynamoDB）。
- **提供商缓存：** 使用本地或共享镜像缓存提供商插件，大大加快 CI/CD 工作流。
- **工作区：** 使用相同配置管理多个环境（开发、预发布、生产）。
- **结构化日志：** 运行 `tofu apply -json` 以获取针对 CI/CD 系统优化的机器可读输出。

## 从 Terraform 迁移

迁移到 OpenTofu 是一项安全、低风险的操作：

1. **安装 OpenTofu。**
2. **导航到你现有的 Terraform 项目。**
3. **运行 `tofu init`。** OpenTofu 会识别现有的 `.terraform` 目录和状态文件，并将其无缝迁移到自己的 `.tofu` 目录。
4. **运行 `tofu plan`** 以验证未检测到任何更改。
5. **标准化你的命令。** 在脚本和文档中将 `terraform` 替换为 `tofu`。

> **重要：** 迁移后，再次运行 `terraform` 可能会重新初始化 `.terraform/` 目录，导致混乱。最佳实践是将所有团队工作流迁移到 `tofu` 命令，并从 PATH 中移除 Terraform。

## 比较：OpenTofu vs. HashiCorp Terraform（2026）

| 特性 | OpenTofu | HashiCorp Terraform |
|---|---|---|
| **许可证** | MPL 2.0（开源） | Business Source License (BUSL) |
| **治理** | Linux 基金会 | HashiCorp, Inc. |
| **状态加密** | 原生（客户端） | 部分（仅 Vault/后端） |
| **OCI 注册表** | 是 | 否 |
| **无代码配置** | 是（开放） | 是（仅 Cloud） |
| **提供商定义的函数** | 是 | 否 |
| **测试框架** | 原生（`tofu test`） | 原生（`terraform test`） |
| **CLI** | `tofu` | `terraform` |
| **核心语言** | HCL / JSON | HCL / JSON |
| **提供商/模块来源** | 注册表、OCI、HTTP、Git 等 | 注册表、HTTP、Git 等 |

## 社区与生态

- **提供商：** 所有主要提供商生态系统（AWS、Azure、GCP、Kubernetes、Vault）都得到完全支持。
- **注册表：** OpenTofu 注册表托管了数千个开源模块。
- **平台支持：** 生态合作伙伴如 Spacelift、env0、Scalr 和 Harness 提供企业级支持。
- **贡献者：** OpenTofu 在 GitHub 上由一个由数百名个人和企业贡献者组成的社区公开开发。

## 结论

OpenTofu 是 2026 年基础设施即代码领域首屈一指的开源工具。其强大的社区、供应商中立的治理以及创新功能（状态加密、OCI 支持、无代码配置、丰富的测试框架）为大规模管理任何基础设施提供了一个稳定且前瞻的平台。

## 资源

- **官方文档：** [https://opentofu.org/docs/](https://opentofu.org/docs/)
- **GitHub 仓库：** [https://github.com/opentofu/opentofu](https://github.com/opentofu/opentofu)
- **注册表：** [https://github.com/opentofu/registry](https://github.com/opentofu/registry)
- **下载与安装：** [https://opentofu.org/downloads/](https://opentofu.org/downloads/)
- **OpenTofu 社区：** [https://opentofu.org/community/](https://opentofu.org/community/)