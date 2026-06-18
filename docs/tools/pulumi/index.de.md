---
title: Pulumi – Infrastructure as Code mit Allzweck-Programmiersprachen
description: Pulumi ist eine Open-Source-Infrastructure-as-Code-Plattform, die es Benutzern ermöglicht, Cloud-Ressourcen mit vertrauten Programmiersprachen wie TypeScript, Python, Go und C# zu definieren und zu verwalten.
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

Pulumi ist eine Open-Source-Infrastructure-as-Code-Plattform (IaC), die Allzweck-Programmiersprachen nutzt, um Cloud-Ressourcen zu definieren, bereitzustellen und zu verwalten. Anstatt eine proprietäre domänenspezifische Sprache (DSL) zu erlernen, verwenden Sie Standardsprachen wie TypeScript, Python, Go, C#, Java und YAML. Dieser Ansatz bringt vertraute Softwareentwicklungspraktiken – Schleifen, Funktionen, Klassen, Tests und Paketverwaltung – direkt in die Bereitstellung von Infrastruktur.

## Warum Pulumi?

- **Multi-Language & Multi-Cloud** – Verwalten Sie Ressourcen über AWS, Azure, GCP, Kubernetes und 100+ Anbieter hinweg mit demselben Tool.
- **Developer Experience** – Verwenden Sie Ihre bevorzugte Sprache, IDE, Debugger und Test-Frameworks.
- **Automation API** – Betten Sie Infrastrukturoperationen direkt in Anwendungscode oder CI/CD-Pipelines ein, ohne dass Sie die CLI benötigen.
- **Policy as Code** – Erzwingen Sie Sicherheits-, Compliance- und Kostenregeln mit TypeScript oder OPA/Rego.
- **State Management** – Verwalten Sie den Zustand sicher über Pulumi Cloud oder selbstverwaltete Backends (S3, GCS, Azure Blob). Geheimnisse werden standardmäßig verschlüsselt.
- **Open Source** – Die Kern-Engine und viele Anbieter sind unter Apache 2.0 lizenziert.

## Installation

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

Überprüfen Sie nach der Installation die Version:
```bash
pulumi version
```

> **Hinweis**: Sie müssen Ihre Cloud-Anbieter-Anmeldeinformationen konfigurieren (z. B. `aws configure`), bevor Sie Ressourcen bereitstellen.

## Quick Start

Erstellen Sie ein neues Projekt mit einer Vorlage (hier AWS mit TypeScript):

```bash
pulumi new aws-typescript
```

Dies erzeugt eine `Pulumi.yaml`-Projektdatei und eine `index.ts`, in der Sie die Infrastruktur definieren. Um beispielsweise einen S3-Bucket zu erstellen:

```typescript
import * as aws from "@pulumi/aws";

const bucket = new aws.s3.Bucket("my-website-bucket", {
    website: {
        indexDocument: "index.html",
    },
});

export const bucketName = bucket.bucket;
```

Stellen Sie den Stack bereit:

```bash
pulumi up
```

Vorschau der Änderungen, dann bestätigen. Nach der Bereitstellung sehen Sie die Ausgaben:

```bash
pulumi stack output bucketName
```

Räumen Sie Ressourcen nach Abschluss auf:

```bash
pulumi destroy
```

## Kernfunktionen

### 1. Automation API

Die Automation API verpackt die Pulumi-Engine als Bibliothek und ermöglicht es Ihnen, Infrastruktur programmatisch aus jeder Anwendung bereitzustellen, ohne auf die CLI zurückgreifen zu müssen.

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

Definieren Sie Richtlinien, die während `pulumi up` ausgeführt werden, um Governance durchzusetzen. Richtlinien werden in TypeScript oder Rego/OPA geschrieben.

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

Ausführen mit:

```bash
pulumi up --policy-pack ./policy
```

### 3. State Management

Standardmäßig wird der Zustand in Pulumi Cloud (kostenlose Stufe verfügbar) gespeichert, was Versionierung, Zusammenarbeit und Geheimnisverschlüsselung bietet. Alternativ können Sie ein selbstverwaltetes Backend verwenden:

```bash
pulumi login s3://my-state-bucket
```

Secrets (z. B. Datenbankpasswörter) werden automatisch verschlüsselt und können mit folgendem Befehl festgelegt werden:

```bash
pulumi config set --secret dbPassword mySecret123
```

### 4. Testing

Pulumi integriert sich in standard Test-Frameworks (Jest, Pytest, usw.). Sie können Unit-Tests mit gemockten Ressourcen, Integrationstests auf ephemeren Stacks und eigenschaftsbasierte Tests schreiben.

**Beispiel: Unit-Test mit Jest**

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

Der Pulumi Kubernetes Operator ermöglicht es Ihnen, Cloud- und Kubernetes-Ressourcen nativ aus Ihrem Cluster mithilfe von Custom Resource Definitions (CRDs) zu verwalten.

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

## Beispiel: Bereitstellen eines S3-Buckets (Multi-Language)

| Sprache       | Code-Auszug                                                      |
|---------------|------------------------------------------------------------------|
| Python        | `bucket = aws.s3.Bucket("my-bucket")`                            |
| Go            | `bucket, err := s3.NewBucket(ctx, "my-bucket", nil)`             |
| C#            | `var bucket = new Aws.S3.Bucket("my-bucket");`                   |
| Java          | `var bucket = new Bucket("my-bucket");`                          |
| YAML          | Verwendet die Pulumi YAML-Vorlagensprache.                       |

## Weiterführende Informationen

- [Offizielle Dokumentation](https://www.pulumi.com/docs/)
- [GitHub-Repository](https://github.com/pulumi/pulumi)
- [Pulumi Registry](https://www.pulumi.com/registry/)
- [Automation API-Beispiele](https://github.com/pulumi/automation-api-examples)
- [Policy as Code-Leitfaden](https://www.pulumi.com/crossguard/)