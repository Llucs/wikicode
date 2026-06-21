---
title: OpenTofu
description: OpenTofu é a ferramenta de Infrastructure as Code (IaC) de código aberto, derivada do Terraform e governada pela Linux Foundation, permitindo o gerenciamento seguro e previsível de recursos em nuvem, locais (on-premises) e de borda.
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

## O que é OpenTofu?

OpenTofu é uma ferramenta declarativa de Infrastructure as Code (IaC) que permite definir, provisionar e gerenciar infraestrutura usando uma linguagem de configuração de alto nível (HCL). Ele gerencia recursos em provedores de nuvem pública (AWS, Azure, GCP), data centers privados e serviços SaaS, construindo um grafo de dependências para garantir que os recursos sejam criados, modificados e destruídos de forma segura e eficiente.

Foi criado em 2023 como um fork direto e conduzido pela comunidade do Terraform em resposta à mudança de licença da HashiCorp. OpenTofu é agora um projeto da Linux Foundation, garantindo que permaneça totalmente de código aberto sob a Mozilla Public License (MPL 2.0) para sempre.

## Por que OpenTofu?

- **Garantia de Código Aberto:** A licença MPL 2.0 impede que qualquer fornecedor único altere os termos de licenciamento para uma licença restritiva (como a BSL).
- **Governança da Linux Foundation:** Um lar neutro e conduzido pela comunidade, com um conjunto diversificado de mantenedores e vários apoiadores corporativos.
- **Compatibilidade com Ecossistema:** Funciona perfeitamente com provedores, módulos e arquivos de estado existentes do Terraform, tornando a migração fácil.
- **Inovação:** A comunidade adicionou recursos poderosos solicitados há anos, como criptografia de estado de ponta a ponta, suporte a registro OCI e provisionamento sem código.
- **Neutralidade de Fornecedor:** Não vinculado a nenhum provedor de nuvem ou plataforma SaaS específica.

## Instalação

OpenTofu fornece a ferramenta CLI `tofu` em todos os principais sistemas operacionais.

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

## Início Rápido / Fluxo de Trabalho Básico

O fluxo de trabalho principal é idêntico ao do Terraform, tornando a transição simples. Você escreve a configuração em arquivos `.tf` e usa o comando `tofu`.

**Crie um arquivo chamado `main.tf`:**

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

**Execute o fluxo de trabalho:**

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

## Principais Características e Diferenciais

### 1. Criptografia do Estado no Lado do Cliente

OpenTofu pode criptografar todo o arquivo de estado no lado do cliente **antes** de enviá-lo ao backend (por exemplo, S3, GCS, Azure Storage). Isso fornece "defesa em profundidade" — o operador do backend não pode ler os dados do estado sem a chave.

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

### 2. Suporte a Registro OCI para Providers e Módulos

Providers e módulos podem ser obtidos de **qualquer** registro compatível com OCI (Docker Hub, AWS ECR, Harbor, GitHub Container Registry). Isso é crítico para:
- **Ambientes isolados (air-gapped):** Hospedar todos os providers em um registro interno.
- **Providers privados:** Não há necessidade de executar um serviço de registro separado.
- **Segurança da cadeia de suprimentos de artefatos:** Aproveitar a assinatura e varredura de contêineres.

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

### 3. Provisionamento Sem Código

Equipes de engenharia de plataforma podem construir módulos reutilizáveis e permitir que usuários finais os implantem diretamente de um registro sem escrever nenhuma configuração HCL. O usuário fornece apenas variáveis de entrada.

```bash
# Deploy a module from a registry directly
tofu init -from-module=my-org/vpc-module/aws
tofu plan -var="cidr_block=10.0.0.0/16"
tofu apply
```

### 4. Funções Definidas pelo Provider

OpenTofu permite que providers exponham funções personalizadas que podem ser chamadas diretamente do HCL. Isso estende a linguagem e permite que providers realizem operações que antes eram impossíveis em HCL puro.

```hcl
# Example: Using an encryption function from a Vault provider
locals {
  encrypted_secret = provider::vault::encode_string(var.raw_secret)
}
```

### 5. Avaliação Antecipada de Variáveis e Locals

Variáveis e locals podem ser avaliados durante a fase de parsing, antes que a inicialização do provider esteja completa. Isso permite padrões poderosos, como construir dinamicamente a configuração do backend com base nos valores das variáveis.

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

### 6. Framework de Teste Nativo

Escreva testes unitários e de integração para seus módulos usando o comando `tofu test`.

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

Execute os testes:
```bash
tofu test
```

## Uso Avançado

- **Backends Remotos:** Armazene o estado em backends S3, GCS, Azurerm ou HTTP com suporte total a bloqueio (por exemplo, DynamoDB).
- **Cache de Providers:** Use um mirror local ou compartilhado para armazenar em cache plugins de provider, acelerando significativamente os fluxos de trabalho de CI/CD.
- **Workspaces:** Gerencie múltiplos ambientes (dev, staging, prod) com a mesma configuração.
- **Logs Estruturados:** Execute `tofu apply -json` para obter saída legível por máquina, adaptada para sistemas de CI/CD.

## Migrando do Terraform

Migrar para OpenTofu é uma operação segura e de baixo risco:

1. **Instale o OpenTofu.**
2. **Navegue até o seu projeto existente do Terraform.**
3. **Execute `tofu init`.** OpenTofu reconhecerá o diretório `.terraform` existente e o arquivo de estado e os migrará perfeitamente para seu próprio diretório `.tofu`.
4. **Execute `tofu plan`** para verificar se nenhuma alteração é detectada.
5. **Padronize seus comandos.** Substitua `terraform` por `tofu` em seus scripts e documentação.

> **Importante:** Após a migração, executar `terraform` novamente pode reinicializar o diretório `.terraform/`, causando confusão. É uma boa prática migrar todos os fluxos de trabalho da equipe para o comando `tofu` e remover o Terraform do PATH.

## Comparação: OpenTofu vs. HashiCorp Terraform (2026)

| Característica | OpenTofu | HashiCorp Terraform |
|---|---|---|
| **Licença** | MPL 2.0 (Código Aberto) | Business Source License (BUSL) |
| **Governança** | Linux Foundation | HashiCorp, Inc. |
| **Criptografia do Estado** | Nativo (Lado do Cliente) | Parcial (apenas Vault/Backend) |
| **Registro OCI** | Sim | Não |
| **Provisionamento Sem Código** | Sim (Aberto) | Sim (apenas Cloud) |
| **Funções Definidas pelo Provider** | Sim | Não |
| **Framework de Teste** | Nativo (`tofu test`) | Nativo (`terraform test`) |
| **CLI** | `tofu` | `terraform` |
| **Linguagem Principal** | HCL / JSON | HCL / JSON |
| **Fontes de Providers/Módulos** | Registry, OCI, HTTP, Git, etc. | Registry, HTTP, Git, etc. |

## Comunidade e Ecossistema

- **Providers:** Todos os principais ecossistemas de providers (AWS, Azure, GCP, Kubernetes, Vault) são totalmente suportados.
- **Registro:** O Registro OpenTofu hospeda milhares de módulos de código aberto.
- **Suporte de Plataforma:** Suporte de nível empresarial está disponível por meio de parceiros do ecossistema como Spacelift, env0, Scalr e Harness.
- **Contribuidores:** OpenTofu é desenvolvido abertamente no GitHub por uma comunidade de centenas de contribuidores individuais e corporativos.

## Conclusão

OpenTofu é a principal ferramenta de código aberto para Infrastructure as Code em 2026. Sua comunidade robusta, governança neutra de fornecedores e recursos inovadores (criptografia de estado, suporte a OCI, provisionamento sem código, framework de teste rico) fornecem uma plataforma estável e com visão de futuro para gerenciar qualquer infraestrutura em escala.

## Recursos

- **Documentação Oficial:** [https://opentofu.org/docs/](https://opentofu.org/docs/)
- **Repositório GitHub:** [https://github.com/opentofu/opentofu](https://github.com/opentofu/opentofu)
- **Registro:** [https://github.com/opentofu/registry](https://github.com/opentofu/registry)
- **Downloads e Instalação:** [https://opentofu.org/downloads/](https://opentofu.org/downloads/)
- **Comunidade OpenTofu:** [https://opentofu.org/community/](https://opentofu.org/community/)