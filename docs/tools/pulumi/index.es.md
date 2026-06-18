---
title: Pulumi – Infraestructura como Código con Lenguajes de Propósito General
description: Pulumi es una plataforma de Infraestructura como Código de código abierto que permite a los usuarios definir y gestionar recursos en la nube utilizando lenguajes de programación familiares como TypeScript, Python, Go y C#.
created: 2026-06-18
tags:
  - infrastructure-as-code
  - cloud
  - devops
  - iac
  - kubernetes
status: draft
---

# Pulumi

Pulumi es una plataforma de Infraestructura como Código (IaC) de código abierto que utiliza lenguajes de programación de propósito general para definir, desplegar y gestionar recursos en la nube. En lugar de aprender un lenguaje de dominio específico (DSL) propietario, usas lenguajes estándar como TypeScript, Python, Go, C#, Java y YAML. Este enfoque trae prácticas familiares de ingeniería de software — bucles, funciones, clases, pruebas y gestión de paquetes — directamente al aprovisionamiento de infraestructura.

## ¿Por qué Pulumi?

- **Multi-Language & Multi-Cloud** – Gestiona recursos en AWS, Azure, GCP, Kubernetes y más de 100 proveedores con la misma herramienta.
- **Developer Experience** – Usa tu lenguaje, IDE, depurador y frameworks de pruebas preferidos.
- **Automation API** – Integra operaciones de infraestructura directamente en el código de la aplicación o en pipelines de CI/CD sin necesidad de la CLI.
- **Policy as Code** – Aplica reglas de seguridad, cumplimiento y costos usando TypeScript u OPA/Rego.
- **State Management** – Gestiona el estado de forma segura a través de Pulumi Cloud o backends autogestionados (S3, GCS, Azure Blob). Los secretos están cifrados por defecto.
- **Open Source** – El motor central y muchos proveedores tienen licencia Apache 2.0.

## Instalación

### macOS / Linux
```bash
curl -fsSL https://get.pulumi.com | sh
```

### macOS (Homebrew)
```bash
brew install pulumi
```

### Windows (Chocolatey)
```powershell
choco install pulumi
```

Después de la instalación, verifica la versión:
```bash
pulumi version
```

> **Nota**: Debes configurar las credenciales de tu proveedor de nube (por ejemplo, `aws configure`) antes de desplegar recursos.

## Inicio Rápido

Crea un nuevo proyecto usando una plantilla (aquí AWS con TypeScript):

```bash
pulumi new aws-typescript
```

Esto genera un archivo de proyecto `Pulumi.yaml` y un `index.ts` donde defines la infraestructura. Por ejemplo, para crear un bucket de S3:

```typescript
import * as aws from "@pulumi/aws";

const bucket = new aws.s3.Bucket("my-website-bucket", {
    website: {
        indexDocument: "index.html",
    },
});

export const bucketName = bucket.bucket;
```

Despliega el stack:

```bash
pulumi up
```

Previsualiza los cambios, luego confirma. Después del despliegue, mira las salidas:

```bash
pulumi stack output bucketName
```

Limpia los recursos cuando termines:

```bash
pulumi destroy
```

## Características Principales

### 1. Automation API

La Automation API empaqueta el motor de Pulumi como una biblioteca, permitiéndote aprovisionar infraestructura programáticamente desde cualquier aplicación sin necesidad de usar la CLI.

```typescript
import { LocalWorkspace } from "@pulumi/pulumi/automation";
import * as aws from "@pulumi/aws";

const stack = await LocalWorkspace.createOrSelectStack({
    stackName: "dev",
    projectName: "my-project",
    program: async () => {
        const bucket = new aws.s3.Bucket("automated-bucket");
        return { bucketName: bucket.bucket };
    },
});

await stack.up();
```

### 2. Policy as Code (CrossGuard)

Define políticas que se ejecutan durante `pulumi up` para aplicar gobernanza. Las políticas se escriben en TypeScript o Rego/OPA.

```typescript
import { PolicyPack } from "@pulumi/policy";

const policies = new PolicyPack("aws-policies", {
    policies: [
        {
            name: "s3-no-public-read",
            description: "Prohibits S3 bucket public read access.",
            enforcementLevel: "mandatory",
            validateResource: (args, reportViolation) => {
                if (args.type === "aws:s3/bucket:Bucket") {
                    // check acl or policy
                }
            },
        },
    ],
});
```

Ejecuta con:

```bash
pulumi up --policy-pack ./policy
```

### 3. State Management

Por defecto, el estado se almacena en Pulumi Cloud (nivel gratuito disponible), que proporciona versionado, colaboración y cifrado de secretos. Alternativamente, usa un backend autogestionado:

```bash
pulumi login s3://my-state-bucket
```

Los secretos (por ejemplo, contraseñas de bases de datos) se cifran automáticamente y se pueden configurar con:

```bash
pulumi config set --secret dbPassword mySecret123
```

### 4. Testing

Pulumi se integra con frameworks de pruebas estándar (Jest, Pytest, etc.). Puedes escribir pruebas unitarias con recursos simulados, pruebas de integración en stacks efímeros y pruebas basadas en propiedades.

**Ejemplo: Prueba unitaria con Jest**

```typescript
import { describe, it, expect } from "@jest/globals";
import * as pulumi from "@pulumi/pulumi";
import { Mocks, ResourceArgs } from "@pulumi/pulumi/runtime";

pulumi.runtime.setMocks({
    newResource: (type: string, name: string, inputs: any): ResourceArgs => {
        return { id: `${name}`, ...inputs };
    },
    call: (token: string, args: any) => args,
});

it("should create an S3 bucket", async () => {
    const { bucketName } = await import("./index");
    const value = await bucketName.get();
    expect(value).toEqual("my-unique-bucket");
});
```

### 5. Kubernetes Operator

El Pulumi Kubernetes Operator te permite gestionar recursos en la nube y de Kubernetes de forma nativa desde tu clúster utilizando Definiciones de Recursos Personalizados (CRDs).

```yaml
apiVersion: pulumi.com/v1
kind: Stack
metadata:
  name: my-k8s-stack
spec:
  stack: dev
  projectRepo: https://github.com/org/repo
  branch: main
  destroyOnFinalize: true
```

## Ejemplo: Desplegando un Bucket S3 (Multi-Lenguaje)

| Lenguaje      | Fragmento Clave                                                        |
|---------------|--------------------------------------------------------------------|
| Python        | `bucket = aws.s3.Bucket("my-bucket")`                              |
| Go            | `bucket, err := s3.NewBucket(ctx, "my-bucket", nil)`              |
| C#            | `var bucket = new Aws.S3.Bucket("my-bucket");`                    |
| Java          | `var bucket = new Bucket("my-bucket");`                           |
| YAML          | Usa el lenguaje de plantillas YAML de Pulumi.                     |

## Lecturas Adicionales

- [Documentación Oficial](https://www.pulumi.com/docs/)
- [Repositorio de GitHub](https://github.com/pulumi/pulumi)
- [Registro de Pulumi](https://www.pulumi.com/registry/)
- [Ejemplos de Automation API](https://github.com/pulumi/automation-api-examples)
- [Guía de Policy as Code](https://www.pulumi.com/crossguard/)