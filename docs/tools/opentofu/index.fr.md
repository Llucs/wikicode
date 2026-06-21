---
title: OpenTofu
description: OpenTofu est l'outil open-source d'Infrastructure as Code (IaC), issu d'un fork de Terraform et gouverné par la Linux Foundation, permettant une gestion sûre et prévisible des ressources cloud, sur site et en périphérie.
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

## Qu'est-ce qu'OpenTofu ?

OpenTofu est un outil déclaratif d'Infrastructure as Code (IaC) qui vous permet de définir, provisionner et gérer l'infrastructure à l'aide d'un langage de configuration de haut niveau (HCL). Il gère les ressources sur les fournisseurs de cloud public (AWS, Azure, GCP), les centres de données privés et les services SaaS en construisant un graphe de dépendances pour garantir que les ressources sont créées, modifiées et détruites en toute sécurité et efficacement.

Il a été créé en 2023 en tant que fork direct et communautaire de Terraform en réponse au changement de licence de HashiCorp. OpenTofu est désormais un projet de la Linux Foundation, garantissant qu'il reste entièrement open-source sous la Mozilla Public License (MPL 2.0) pour toujours.

## Pourquoi OpenTofu ?

- **Garantie Open Source :** La licence MPL 2.0 empêche tout fournisseur unique de modifier les termes de la licence pour une licence restrictive (comme la BSL).
- **Gouvernance de la Linux Foundation :** Un foyer neutre et piloté par la communauté avec un ensemble diversifié de mainteneurs et de multiples soutiens corporatifs.
- **Compatibilité avec l'écosystème :** Fonctionne de manière transparente avec les fournisseurs, modules et fichiers d'état Terraform existants, rendant la migration sans effort.
- **Innovation :** La communauté a ajouté des fonctionnalités puissantes demandées depuis des années, telles que le chiffrement d'état de bout en bout, la prise en charge du registre OCI et le provisionnement sans code.
- **Neutralité vis-à-vis des fournisseurs :** Non lié à un seul fournisseur de cloud ou plateforme SaaS.

## Installation

OpenTofu fournit l'outil CLI `tofu` sur tous les principaux systèmes d'exploitation.

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

## Démarrage rapide / Flux de travail de base

Le flux de travail de base est identique à celui de Terraform, ce qui rend la transition simple. Vous écrivez la configuration dans des fichiers `.tf` et utilisez la commande `tofu`.

**Créez un fichier nommé `main.tf` :**

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

**Exécutez le flux de travail :**

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

## Fonctionnalités clés et différenciateurs

### 1. Chiffrement d'état côté client

OpenTofu peut chiffrer l'intégralité du fichier d'état côté client **avant** qu'il ne soit envoyé au backend (par exemple, S3, GCS, Azure Storage). Cela offre une « défense en profondeur » — l'opérateur du backend ne peut pas lire les données d'état sans la clé.

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

### 2. Prise en charge du registre OCI pour les fournisseurs et modules

Les fournisseurs et modules peuvent être récupérés depuis **n'importe quel** registre conforme à OCI (Docker Hub, AWS ECR, Harbor, GitHub Container Registry). Ceci est critique pour :
- **Environnements isolés (air-gapped) :** Héberger tous les fournisseurs dans un registre interne.
- **Fournisseurs privés :** Pas besoin d'exécuter un service de registre séparé.
- **Sécurité de la chaîne d'approvisionnement des artefacts :** Tirer parti de la signature et de l'analyse des conteneurs.

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

### 3. Provisionnement sans code

Les équipes d'ingénierie de plateforme peuvent construire des modules réutilisables et permettre aux utilisateurs finaux de les déployer directement depuis un registre sans écrire de configuration HCL. L'utilisateur fournit uniquement des variables d'entrée.

```bash
# Deploy a module from a registry directly
tofu init -from-module=my-org/vpc-module/aws
tofu plan -var="cidr_block=10.0.0.0/16"
tofu apply
```

### 4. Fonctions définies par les fournisseurs

OpenTofu permet aux fournisseurs d'exposer des fonctions personnalisées qui peuvent être appelées directement depuis HCL. Cela étend le langage et permet aux fournisseurs d'effectuer des opérations auparavant impossibles en HCL pur.

```hcl
# Example: Using an encryption function from a Vault provider
locals {
  encrypted_secret = provider::vault::encode_string(var.raw_secret)
}
```

### 5. Évaluation précoce des variables et des locals

Les variables et les locals peuvent être évalués pendant la phase d'analyse, avant que l'initialisation du fournisseur ne soit terminée. Cela permet des motifs puissants comme la construction dynamique de la configuration du backend en fonction des valeurs des variables.

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

### 6. Framework de test natif

Écrivez des tests unitaires et d'intégration pour vos modules en utilisant la commande `tofu test`.

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

Exécutez les tests :
```bash
tofu test
```

## Utilisation avancée

- **Backends distants :** Stockez l'état dans des backends S3, GCS, Azurerm ou HTTP avec support complet du verrouillage (par exemple, DynamoDB).
- **Mise en cache des fournisseurs :** Utilisez un miroir local ou partagé pour mettre en cache les plugins des fournisseurs, accélérant considérablement les flux de travail CI/CD.
- **Espaces de travail :** Gérez plusieurs environnements (dev, staging, prod) avec la même configuration.
- **Journalisation structurée :** Exécutez `tofu apply -json` pour une sortie lisible par machine adaptée aux systèmes CI/CD.

## Migration depuis Terraform

Migrer vers OpenTofu est une opération sûre et à faible risque :

1. **Installez OpenTofu.**
2. **Naviguez vers votre projet Terraform existant.**
3. **Exécutez `tofu init`.** OpenTofu reconnaîtra le répertoire `.terraform` existant et le fichier d'état et les migrera de manière transparente vers son propre répertoire `.tofu`.
4. **Exécutez `tofu plan`** pour vérifier qu'aucun changement n'est détecté.
5. **Standardisez vos commandes.** Remplacez `terraform` par `tofu` dans vos scripts et documentation.

> **Important :** Après la migration, exécuter à nouveau `terraform` pourrait réinitialiser le répertoire `.terraform/`, provoquant de la confusion. Il est recommandé de migrer tous les workflows d'équipe vers la commande `tofu` et de supprimer Terraform du PATH.

## Comparaison : OpenTofu vs. HashiCorp Terraform (2026)

| Fonctionnalité | OpenTofu | HashiCorp Terraform |
|---|---|---|
| **Licence** | MPL 2.0 (Open Source) | Business Source License (BUSL) |
| **Gouvernance** | Linux Foundation | HashiCorp, Inc. |
| **Chiffrement d'état** | Natif (côté client) | Partiel (Vault/Backend uniquement) |
| **Registre OCI** | Oui | Non |
| **Provisionnement sans code** | Oui (Open) | Oui (Cloud uniquement) |
| **Fonctions définies par les fournisseurs** | Oui | Non |
| **Framework de test** | Natif (`tofu test`) | Natif (`terraform test`) |
| **Langage de base** | HCL / JSON | HCL / JSON |
| **Sources des fournisseurs/modules** | Registre, OCI, HTTP, Git, etc. | Registre, HTTP, Git, etc. |

## Communauté et écosystème

- **Fournisseurs :** Tous les principaux écosystèmes de fournisseurs (AWS, Azure, GCP, Kubernetes, Vault) sont entièrement pris en charge.
- **Registre :** Le registre OpenTofu héberge des milliers de modules open-source.
- **Support de plateforme :** Un support de niveau entreprise est disponible auprès de partenaires de l'écosystème comme Spacelift, env0, Scalr et Harness.
- **Contributeurs :** OpenTofu est développé ouvertement sur GitHub par une communauté de centaines de contributeurs individuels et d'entreprises.

## Conclusion

OpenTofu est le principal outil open-source pour l'Infrastructure as Code en 2026. Sa communauté robuste, sa gouvernance neutre vis-à-vis des fournisseurs et ses fonctionnalités innovantes (chiffrement d'état, support OCI, provisionnement sans code, framework de test riche) fournissent une plateforme stable et tournée vers l'avenir pour gérer toute infrastructure à grande échelle.

## Ressources

- **Documentation officielle :** [https://opentofu.org/docs/](https://opentofu.org/docs/)
- **Dépôt GitHub :** [https://github.com/opentofu/opentofu](https://github.com/opentofu/opentofu)
- **Registre :** [https://github.com/opentofu/registry](https://github.com/opentofu/registry)
- **Téléchargements et installation :** [https://opentofu.org/downloads/](https://opentofu.org/downloads/)
- **Communauté OpenTofu :** [https://opentofu.org/community/](https://opentofu.org/community/)