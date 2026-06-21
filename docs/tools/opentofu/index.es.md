---
title: OpenTofu
description: OpenTofu es la herramienta de código abierto de Infraestructura como Código (IaC), bifurcada de Terraform y gobernada por la Linux Foundation, que permite la gestión segura y predecible de recursos en la nube, on-premises y edge.
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

## ¿Qué es OpenTofu?

OpenTofu es una herramienta declarativa de Infraestructura como Código (IaC) que permite definir, aprovisionar y gestionar infraestructura utilizando un lenguaje de configuración de alto nivel (HCL). Gestiona recursos a través de proveedores de nube pública (AWS, Azure, GCP), centros de datos privados y servicios SaaS mediante la construcción de un gráfico de dependencias para garantizar que los recursos se creen, modifiquen y destruyan de manera segura y eficiente.

Fue creado en 2023 como una bifurcación directa, impulsada por la comunidad, de Terraform en respuesta al cambio de licencia de HashiCorp. OpenTofu es ahora un proyecto de la Linux Foundation, lo que garantiza que permanezca completamente como código abierto bajo la Mozilla Public License (MPL 2.0) para siempre.

## ¿Por qué OpenTofu?

- **Garantía de Código Abierto:** La licencia MPL 2.0 evita que un solo proveedor cambie los términos de la licencia a una licencia restrictiva (como la BSL).
- **Gobernanza de la Linux Foundation:** Un hogar neutral, impulsado por la comunidad, con un conjunto diverso de mantenedores y múltiples patrocinadores corporativos.
- **Compatibilidad con el Ecosistema:** Funciona sin problemas con los proveedores, módulos y archivos de estado existentes de Terraform, lo que facilita la migración.
- **Innovación:** La comunidad ha añadido potentes características solicitadas durante años, como el cifrado de estado de extremo a extremo, soporte para registros OCI y aprovisionamiento sin código.
- **Neutralidad del Proveedor:** No está vinculado a ningún proveedor de nube o plataforma SaaS en particular.

## Instalación

OpenTofu proporciona la herramienta CLI `tofu` en todos los sistemas operativos principales.

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

## Inicio Rápido / Flujo de Trabajo Básico

El flujo de trabajo central es idéntico al de Terraform, lo que hace que la transición sea sencilla. Escribes la configuración en archivos `.tf` y usas el comando `tofu`.

**Crea un archivo llamado `main.tf`:**

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

**Ejecuta el flujo de trabajo:**

```bash
# Inicializa el directorio y descarga los proveedores
tofu init

# Formatea y valida la configuración
tofu fmt
tofu validate

# Crea un plan de ejecución
tofu plan -out=tfplan

# Aplica el plan
tofu apply tfplan

# Destruye los recursos
tofu destroy
```

## Características Clave y Diferenciadores

### 1. Cifrado de Estado del Lado del Cliente

OpenTofu puede cifrar todo el archivo de estado del lado del cliente **antes** de que se envíe al backend (por ejemplo, S3, GCS, Azure Storage). Esto proporciona "defensa en profundidad": el operador del backend no puede leer los datos de estado sin la clave.

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

### 2. Soporte para Registros OCI para Proveedores y Módulos

Los proveedores y módulos se pueden obtener de **cualquier** registro compatible con OCI (Docker Hub, AWS ECR, Harbor, GitHub Container Registry). Esto es crítico para:

- **Entornos aislados (air-gapped):** Aloja todos los proveedores en un registro interno.
- **Proveedores privados:** No es necesario ejecutar un servicio de registro separado.
- **Seguridad de la cadena de suministro de artefactos:** Aprovecha la firma y el escaneo de contenedores.

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

### 3. Aprovisionamiento Sin Código

Los equipos de ingeniería de plataforma pueden construir módulos reutilizables y permitir que los usuarios finales los desplieguen directamente desde un registro sin escribir ninguna configuración HCL. El usuario solo proporciona variables de entrada.

```bash
# Despliega un módulo desde un registro directamente
tofu init -from-module=my-org/vpc-module/aws
tofu plan -var="cidr_block=10.0.0.0/16"
tofu apply
```

### 4. Funciones Definidas por el Proveedor

OpenTofu permite que los proveedores expongan funciones personalizadas que se pueden llamar directamente desde HCL. Esto extiende el lenguaje y permite a los proveedores realizar operaciones que antes eran imposibles en HCL puro.

```hcl
# Ejemplo: Usando una función de cifrado de un proveedor de Vault
locals {
  encrypted_secret = provider::vault::encode_string(var.raw_secret)
}
```

### 5. Evaluación Temprana de Variables y Locales

Las variables y los locales se pueden evaluar durante la fase de análisis, antes de que se complete la inicialización del proveedor. Esto permite patrones potentes como la construcción dinámica de la configuración del backend basada en los valores de las variables.

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

### 6. Marco de Pruebas Nativo

Escribe pruebas unitarias y de integración para tus módulos usando el comando `tofu test`.

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

Ejecuta las pruebas:

```bash
tofu test
```

## Uso Avanzado

- **Backends Remotos:** Almacena el estado en backends S3, GCS, Azurerm o HTTP con soporte completo de bloqueo (por ejemplo, DynamoDB).
- **Caché de Proveedores:** Usa un espejo local o compartido para almacenar en caché los complementos de los proveedores, lo que acelera enormemente los flujos de trabajo de CI/CD.
- **Espacios de Trabajo:** Gestiona múltiples entornos (dev, staging, prod) con la misma configuración.
- **Registro Estructurado:** Ejecuta `tofu apply -json` para obtener una salida legible por máquina adaptada para sistemas CI/CD.

## Migrando desde Terraform

Migrar a OpenTofu es una operación segura y de bajo riesgo:

1. **Instala OpenTofu.**
2. **Navega a tu proyecto existente de Terraform.**
3. **Ejecuta `tofu init`.** OpenTofu reconocerá el directorio `.terraform` existente y el archivo de estado y los migrará sin problemas a su propio directorio `.tofu`.
4. **Ejecuta `tofu plan`** para verificar que no se detectan cambios.
5. **Estandariza tus comandos.** Reemplaza `terraform` con `tofu` en tus scripts y documentación.

> **Importante:** Después de migrar, ejecutar `terraform` nuevamente puede reinicializar el directorio `.terraform/`, causando confusión. Es una buena práctica migrar todos los flujos de trabajo del equipo al comando `tofu` y eliminar Terraform del PATH.

## Comparación: OpenTofu vs. HashiCorp Terraform (2026)

| Característica | OpenTofu | HashiCorp Terraform |
|---|---|---|
| **Licencia** | MPL 2.0 (Código Abierto) | Business Source License (BUSL) |
| **Gobernanza** | Linux Foundation | HashiCorp, Inc. |
| **Cifrado de Estado** | Nativo (Lado del Cliente) | Parcial (solo Vault/Backend) |
| **Registro OCI** | Sí | No |
| **Aprovisionamiento Sin Código** | Sí (Abierto) | Sí (solo Cloud) |
| **Funciones Definidas por el Proveedor** | Sí | No |
| **Marco de Pruebas** | Nativo (`tofu test`) | Nativo (`terraform test`) |
| **CLI** | `tofu` | `terraform` |
| **Lenguaje Principal** | HCL / JSON | HCL / JSON |
| **Fuentes de Proveedores/Módulos** | Registro, OCI, HTTP, Git, etc. | Registro, HTTP, Git, etc. |

## Comunidad y Ecosistema

- **Proveedores:** Todos los ecosistemas principales de proveedores (AWS, Azure, GCP, Kubernetes, Vault) son completamente compatibles.
- **Registro:** El Registro OpenTofu alberga miles de módulos de código abierto.
- **Soporte de Plataforma:** Hay soporte de nivel empresarial disponible a través de socios del ecosistema como Spacelift, env0, Scalr y Harness.
- **Contribuyentes:** OpenTofu se desarrolla abiertamente en GitHub por una comunidad de cientos de contribuyentes individuales y corporativos.

## Conclusión

OpenTofu es la principal herramienta de código abierto para Infraestructura como Código en 2026. Su sólida comunidad, gobernanza neutral respecto al proveedor y características innovadoras (cifrado de estado, soporte OCI, aprovisionamiento sin código, marco de pruebas enriquecido) proporcionan una plataforma estable y con visión de futuro para gestionar cualquier infraestructura a escala.

## Recursos

- **Documentación Oficial:** [https://opentofu.org/docs/](https://opentofu.org/docs/)
- **Repositorio de GitHub:** [https://github.com/opentofu/opentofu](https://github.com/opentofu/opentofu)
- **Registro:** [https://github.com/opentofu/registry](https://github.com/opentofu/registry)
- **Descargas e Instalación:** [https://opentofu.org/downloads/](https://opentofu.org/downloads/)
- **Comunidad de OpenTofu:** [https://opentofu.org/community/](https://opentofu.org/community/)