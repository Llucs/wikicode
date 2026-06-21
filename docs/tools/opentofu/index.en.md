---
title: OpenTofu
description: OpenTofu is the open-source Infrastructure as Code (IaC) tool, forked from Terraform and governed by the Linux Foundation, enabling safe and predictable management of cloud, on-premises, and edge resources.
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

## What is OpenTofu?

OpenTofu is a declarative Infrastructure as Code (IaC) tool that allows you to define, provision, and manage infrastructure using a high-level configuration language (HCL). It manages resources across public cloud providers (AWS, Azure, GCP), private data centers, and SaaS services by building a dependency graph to ensure resources are created, modified, and destroyed safely and efficiently.

It was created in 2023 as a direct, community-driven fork of Terraform in response to HashiCorp's license change. OpenTofu is now a Linux Foundation project, ensuring it remains fully open-source under the Mozilla Public License (MPL 2.0) forever.

## Why OpenTofu?

- **Open Source Guarantee:** The MPL 2.0 license prevents any single vendor from changing the licensing terms to a restrictive license (like the BSL).
- **Linux Foundation Governance:** A neutral, community-driven home with a diverse set of maintainers and multiple corporate backers.
- **Ecosystem Compatibility:** Works seamlessly with existing Terraform providers, modules, and state files, making migration effortless.
- **Innovation:** The community has added powerful features requested for years, such as end-to-end state encryption, OCI registry support, and no-code provisioning.
- **Vendor Neutrality:** Not tied to any single cloud provider or SaaS platform.

## Installation

OpenTofu provides the `tofu` CLI tool across all major operating systems.

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

## Quick Start / Basic Workflow

The core workflow is identical to that of Terraform, making the transition straightforward. You write configuration in `.tf` files and use the `tofu` command.

**Create a file named `main.tf`:**

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

**Run the workflow:**

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

## Key Features & Differentiators

### 1. Client-Side State Encryption

OpenTofu can encrypt the entire state file client-side **before** it is sent to the backend (e.g., S3, GCS, Azure Storage). This provides "defense in depth" — the backend operator cannot read the state data without the key.

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

### 2. OCI Registry Support for Providers and Modules

Providers and modules can be fetched from **any** OCI-compliant registry (Docker Hub, AWS ECR, Harbor, GitHub Container Registry). This is critical for:
- **Air-gapped environments:** Host all providers in an internal registry.
- **Private providers:** No need to run a separate registry service.
- **Artifact supply chain security:** Leverage container signing and scanning.

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

### 3. No-Code Provisioning

Platform engineering teams can build reusable modules and allow end-users to deploy them directly from a registry without writing any HCL configuration. The user only provides input variables.

```bash
# Deploy a module from a registry directly
tofu init -from-module=my-org/vpc-module/aws
tofu plan -var="cidr_block=10.0.0.0/16"
tofu apply
```

### 4. Provider-Defined Functions

OpenTofu allows providers to expose custom functions that can be called directly from HCL. This extends the language and allows providers to perform operations that were previously impossible in pure HCL.

```hcl
# Example: Using an encryption function from a Vault provider
locals {
  encrypted_secret = provider::vault::encode_string(var.raw_secret)
}
```

### 5. Early Variable and Locals Evaluation

Variables and locals can be evaluated during the parsing phase, before provider initialization is complete. This enables powerful patterns like dynamically constructing the backend configuration based on variable values.

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

### 6. Native Test Framework

Write unit and integration tests for your modules using the `tofu test` command.

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

Run the tests:
```bash
tofu test
```

## Advanced Usage

- **Remote Backends:** Store state in S3, GCS, Azurerm, or HTTP backends with full locking support (e.g., DynamoDB).
- **Provider Caching:** Use a local or shared mirror to cache provider plugins, greatly speeding up CI/CD workflows.
- **Workspaces:** Manage multiple environments (dev, staging, prod) with the same configuration.
- **Structured Logging:** Run `tofu apply -json` for machine-readable output tailored for CI/CD systems.

## Migrating from Terraform

Migrating to OpenTofu is a safe, low-risk operation:

1. **Install OpenTofu.**
2. **Navigate to your existing Terraform project.**
3. **Run `tofu init`.** OpenTofu will recognize the existing `.terraform` directory and state file and migrate them seamlessly to its own `.tofu` directory.
4. **Run `tofu plan`** to verify no changes are detected.
5. **Standardize your commands.** Replace `terraform` with `tofu` in your scripts and documentation.

> **Important:** After migrating, running `terraform` again may re-initialize the `.terraform/` directory, causing confusion. It is best practice to migrate all team workflows to the `tofu` command and remove Terraform from the PATH.

## Comparison: OpenTofu vs. HashiCorp Terraform (2026)

| Feature | OpenTofu | HashiCorp Terraform |
|---|---|---|
| **License** | MPL 2.0 (Open Source) | Business Source License (BUSL) |
| **Governance** | Linux Foundation | HashiCorp, Inc. |
| **State Encryption** | Native (Client-Side) | Partial (Vault/Backend only) |
| **OCI Registry** | Yes | No |
| **No-Code Provisioning** | Yes (Open) | Yes (Cloud only) |
| **Provider-Defined Functions** | Yes | No |
| **Testing Framework** | Native (`tofu test`) | Native (`terraform test`) |
| **CLI** | `tofu` | `terraform` |
| **Core Language** | HCL / JSON | HCL / JSON |
| **Provider/Module Sources** | Registry, OCI, HTTP, Git, etc. | Registry, HTTP, Git, etc. |

## Community and Ecosystem

- **Providers:** All major provider ecosystems (AWS, Azure, GCP, Kubernetes, Vault) are fully supported.
- **Registry:** The OpenTofu Registry hosts thousands of open-source modules.
- **Platform Support:** Enterprise-grade support is available from ecosystem partners like Spacelift, env0, Scalr, and Harness.
- **Contributors:** OpenTofu is developed openly on GitHub by a community of hundreds of individual and corporate contributors.

## Conclusion

OpenTofu is the premier open-source tool for Infrastructure as Code in 2026. Its robust community, vendor-neutral governance, and innovative features (state encryption, OCI support, no-code provisioning, rich testing framework) provide a stable and forward-looking platform for managing any infrastructure at scale.

## Resources

- **Official Documentation:** [https://opentofu.org/docs/](https://opentofu.org/docs/)
- **GitHub Repository:** [https://github.com/opentofu/opentofu](https://github.com/opentofu/opentofu)
- **Registry:** [https://github.com/opentofu/registry](https://github.com/opentofu/registry)
- **Downloads & Installation:** [https://opentofu.org/downloads/](https://opentofu.org/downloads/)
- **OpenTofu Community:** [https://opentofu.org/community/](https://opentofu.org/community/)