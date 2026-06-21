---
title: OpenTofu
description: OpenTofu ist das Open-Source-Infrastructure-as-Code (IaC)-Tool, das von Terraform abgespalten wurde und unter der Leitung der Linux Foundation steht, um eine sichere und vorhersagbare Verwaltung von Cloud-, On-Premises- und Edge-Ressourcen zu ermöglichen.
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

## Was ist OpenTofu?

OpenTofu ist ein deklaratives Infrastructure-as-Code (IaC)-Tool, mit dem Sie Infrastruktur mithilfe einer hochgradigen Konfigurationssprache (HCL) definieren, bereitstellen und verwalten können. Es verwaltet Ressourcen über öffentliche Cloud-Anbieter (AWS, Azure, GCP), private Rechenzentren und SaaS-Dienste, indem es einen Abhängigkeitsgraphen erstellt, um sicherzustellen, dass Ressourcen sicher und effizient erstellt, geändert und zerstört werden.

Es wurde 2023 als direkter, von der Community getriebener Fork von Terraform als Reaktion auf die Lizenzänderung von HashiCorp erstellt. OpenTofu ist jetzt ein Projekt der Linux Foundation, das sicherstellt, dass es unter der Mozilla Public License (MPL 2.0) dauerhaft vollständig quelloffen bleibt.

## Warum OpenTofu?

- **Open-Source-Garantie:** Die MPL-2.0-Lizenz verhindert, dass ein einzelner Anbieter die Lizenzbedingungen in eine restriktive Lizenz (wie die BSL) ändert.
- **Linux Foundation Governance:** Ein neutrales, von der Community getriebenes Zuhause mit einem vielfältigen Team von Maintainern und mehreren Unternehmensunterstützern.
- **Ökosystem-Kompatibilität:** Funktioniert nahtlos mit bestehenden Terraform-Providern, Modulen und Statusdateien, was die Migration mühelos macht.
- **Innovation:** Die Community hat leistungsstarke Funktionen hinzugefügt, die jahrelang gefordert wurden, wie z. B. Ende-zu-Ende-Verschlüsselung des Zustands, OCI-Registry-Unterstützung und No-Code-Provisioning.
- **Anbieterneutralität:** Nicht an einen einzelnen Cloud-Anbieter oder eine SaaS-Plattform gebunden.

## Installation

OpenTofu stellt das CLI-Tool `tofu` für alle gängigen Betriebssysteme zur Verfügung.

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

## Schnellstart / Grundlegender Workflow

Der Kernworkflow ist identisch mit dem von Terraform, was den Übergang unkompliziert macht. Sie schreiben Konfigurationen in `.tf`-Dateien und verwenden den Befehl `tofu`.

**Erstellen Sie eine Datei mit dem Namen `main.tf`:**

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

**Führen Sie den Workflow aus:**

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

## Hauptfunktionen und Unterscheidungsmerkmale

### 1. Clientseitige Zustandsverschlüsselung

OpenTofu kann die gesamte Zustandsdatei clientseitig verschlüsseln, **bevor** sie an das Backend gesendet wird (z. B. S3, GCS, Azure Storage). Dies bietet eine „mehrschichtige Verteidigung" (Defense in Depth) – der Backend-Betreiber kann die Zustandsdaten ohne den Schlüssel nicht lesen.

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

### 2. OCI-Registry-Unterstützung für Provider und Module

Provider und Module können von **jeder** OCI-konformen Registry bezogen werden (Docker Hub, AWS ECR, Harbor, GitHub Container Registry). Dies ist entscheidend für:
- **Abgeschottete Umgebungen (Air-Gapped):** Hosten Sie alle Provider in einer internen Registry.
- **Private Provider:** Keine Notwendigkeit, einen separaten Registry-Dienst zu betreiben.
- **Sicherheit der Artefakt-Lieferkette:** Nutzen Sie Container-Signing und -Scanning.

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

### 3. No-Code-Provisioning

Plattform-Ingenieurteams können wiederverwendbare Module erstellen und Endbenutzern ermöglichen, sie direkt aus einer Registry bereitzustellen, ohne HCL-Konfiguration schreiben zu müssen. Der Benutzer gibt nur Eingabevariablen an.

```bash
# Deploy a module from a registry directly
tofu init -from-module=my-org/vpc-module/aws
tofu plan -var="cidr_block=10.0.0.0/16"
tofu apply
```

### 4. Vom Provider definierte Funktionen

OpenTofu ermöglicht es Providern, benutzerdefinierte Funktionen bereitzustellen, die direkt von HCL aus aufgerufen werden können. Dies erweitert die Sprache und ermöglicht es Providern, Operationen durchzuführen, die zuvor in reinem HCL unmöglich waren.

```hcl
# Example: Using an encryption function from a Vault provider
locals {
  encrypted_secret = provider::vault::encode_string(var.raw_secret)
}
```

### 5. Frühe Auswertung von Variablen und Locals

Variablen und Locals können während der Parsingphase ausgewertet werden, bevor die Provider-Initialisierung abgeschlossen ist. Dies ermöglicht leistungsstarke Muster wie das dynamische Erstellen der Backend-Konfiguration basierend auf Variablenwerten.

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

### 6. Natives Test-Framework

Schreiben Sie Komponenten- und Integrationstests für Ihre Module mit dem Befehl `tofu test`.

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

Führen Sie die Tests aus:
```bash
tofu test
```

## Fortgeschrittene Nutzung

- **Remote-Backends:** Speichern Sie den Zustand in S3-, GCS-, Azurerm- oder HTTP-Backends mit voller Sperrunterstützung (z. B. DynamoDB).
- **Provider-Caching:** Verwenden Sie einen lokalen oder gemeinsamen Mirror, um Provider-Plugins zwischenzuspeichern, was CI/CD-Workflows erheblich beschleunigt.
- **Workspaces:** Verwalten Sie mehrere Umgebungen (dev, staging, prod) mit derselben Konfiguration.
- **Strukturierte Protokollierung:** Führen Sie `tofu apply -json` für maschinenlesbare Ausgaben aus, die für CI/CD-Systeme angepasst sind.

## Migration von Terraform

Die Migration zu OpenTofu ist ein sicherer, risikoarmer Vorgang:

1. **Installieren Sie OpenTofu.**
2. **Navigieren Sie zu Ihrem bestehenden Terraform-Projekt.**
3. **Führen Sie `tofu init` aus.** OpenTofu erkennt das vorhandene `.terraform`-Verzeichnis und die Statusdatei und migriert sie nahtlos in das eigene `.tofu`-Verzeichnis.
4. **Führen Sie `tofu plan` aus**, um zu überprüfen, dass keine Änderungen festgestellt werden.
5. **Standardisieren Sie Ihre Befehle.** Ersetzen Sie in Ihren Skripten und Dokumentationen `terraform` durch `tofu`.

> **Wichtig:** Nach der Migration kann das erneute Ausführen von `terraform` das `.terraform/`-Verzeichnis neu initialisieren, was zu Verwirrung führt. Es ist empfohlen, alle Team-Workflows auf den Befehl `tofu` zu migrieren und Terraform aus dem PATH zu entfernen.

## Vergleich: OpenTofu vs. HashiCorp Terraform (2026)

| Merkmal | OpenTofu | HashiCorp Terraform |
|---|---|---|
| **Lizenz** | MPL 2.0 (Open Source) | Business Source License (BUSL) |
| **Governance** | Linux Foundation | HashiCorp, Inc. |
| **State-Verschlüsselung** | Nativ (Clientseitig) | Teilweise (nur Vault/Backend) |
| **OCI Registry** | Ja | Nein |
| **No-Code-Provisioning** | Ja (Offen) | Ja (nur Cloud) |
| **Vom Provider definierte Funktionen** | Ja | Nein |
| **Test-Framework** | Nativ (`tofu test`) | Nativ (`terraform test`) |
| **CLI** | `tofu` | `terraform` |
| **Kernsprache** | HCL / JSON | HCL / JSON |
| **Provider-/Modulquellen** | Registry, OCI, HTTP, Git, etc. | Registry, HTTP, Git, etc. |

## Community und Ökosystem

- **Provider:** Alle wichtigen Provider-Ökosysteme (AWS, Azure, GCP, Kubernetes, Vault) werden vollständig unterstützt.
- **Registry:** Die OpenTofu-Registry hostet Tausende von Open-Source-Modulen.
- **Plattformunterstützung:** Enterprise-Support ist von Ökosystempartnern wie Spacelift, env0, Scalr und Harness erhältlich.
- **Mitwirkende:** OpenTofu wird offen auf GitHub von einer Gemeinschaft von Hunderten von Einzelpersonen und Unternehmen entwickelt.

## Fazit

OpenTofu ist das führende Open-Source-Tool für Infrastructure as Code im Jahr 2026. Seine robuste Community, die anbieterneutrale Governance und die innovativen Funktionen (State-Verschlüsselung, OCI-Unterstützung, No-Code-Provisioning, umfangreiches Test-Framework) bieten eine stabile und zukunftsorientierte Plattform für die Verwaltung jeder Infrastruktur in großem Maßstab.

## Ressourcen

- [Offizielle Dokumentation](https://opentofu.org/docs/)
- [GitHub-Repository](https://github.com/opentofu/opentofu)
- [Registry](https://github.com/opentofu/registry)
- [Downloads & Installation](https://opentofu.org/downloads/)
- [OpenTofu Community](https://opentofu.org/community/)