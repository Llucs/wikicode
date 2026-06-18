---
title: Pulumi – Infraestrutura como Código com Linguagens de Propósito Geral
description: Pulumi é uma plataforma de Infraestrutura como Código de código aberto que permite aos usuários definir e gerenciar recursos de nuvem usando linguagens de programação familiares como TypeScript, Python, Go e C#.
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

Pulumi é uma plataforma de Infraestrutura como Código (IaC) de código aberto que utiliza linguagens de programação de propósito geral para definir, implantar e gerenciar recursos de nuvem. Em vez de aprender uma linguagem de domínio específico (DSL) proprietária, você usa linguagens padrão como TypeScript, Python, Go, C#, Java e YAML. Essa abordagem traz práticas familiares de engenharia de software — loops, funções, classes, testes e gerenciamento de pacotes — diretamente para o provisionamento de infraestrutura.

## Por que Pulumi?

- **Multi-linguagem & Multi-nuvem** – Gerencie recursos em AWS, Azure, GCP, Kubernetes e mais de 100 provedores com a mesma ferramenta.
- **Experiência do desenvolvedor** – Use sua linguagem preferida, IDE, depurador e estruturas de teste.
- **Automation API** – Incorpore operações de infraestrutura diretamente no código da aplicação ou em pipelines CI/CD sem precisar da CLI.
- **Policy as Code** – Imponha regras de segurança, conformidade e custo usando TypeScript ou OPA/Rego.
- **Gerenciamento de estado** – Gerencie o estado de forma segura via Pulumi Cloud ou backends auto-gerenciados (S3, GCS, Azure Blob). Segredos são criptografados por padrão.
- **Código aberto** – O motor principal e muitos provedores são licenciados sob Apache 2.0.

## Instalação

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

Após a instalação, verifique a versão:
```bash
pulumi version
```

> **Nota**: Você deve configurar as credenciais do seu provedor de nuvem (ex.: `aws configure`) antes de implantar recursos.

## Início Rápido

Crie um novo projeto usando um modelo (aqui AWS com TypeScript):

```bash
pulumi new aws-typescript
```

Isso gera um arquivo de projeto `Pulumi.yaml` e um `index.ts` onde você define a infraestrutura. Por exemplo, para criar um bucket S3:

```typescript
import * as aws from "@pulumi/aws";

const bucket = new aws.s3.Bucket("my-website-bucket", {
    website: {
        indexDocument: "index.html",
    },
});

export const bucketName = bucket.bucket;
```

Implante a stack:

```bash
pulumi up
```

Visualize as alterações e confirme. Após a implantação, veja as saídas:

```bash
pulumi stack output bucketName
```

Limpe os recursos quando terminar:

```bash
pulumi destroy
```

## Principais Recursos

### 1. Automation API

A Automation API empacota o motor do Pulumi como uma biblioteca, permitindo provisionar infraestrutura programaticamente a partir de qualquer aplicação sem chamar a CLI.

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

Defina políticas que são executadas durante `pulumi up` para impor governança. As políticas são escritas em TypeScript ou Rego/OPA.

```typescript
import { PolicyPack } from "@pulumi/policy";

const policies = new PolicyPack("aws-policies", {
    policies: [
        {
            name: "s3-no-public-read",
            description: "Proíbe acesso de leitura público em buckets S3.",
            enforcementLevel: "mandatory",
            validateResource: (args, reportViolation) => {
                if (args.type === "aws:s3/bucket:Bucket") {
                    // verifica acl ou política
                }
            },
        },
    ],
});
```

Execute com:

```bash
pulumi up --policy-pack ./policy
```

### 3. Gerenciamento de Estado

Por padrão, o estado é armazenado no Pulumi Cloud (plano gratuito disponível), que oferece versionamento, colaboração e criptografia de segredos. Alternativamente, use um backend auto-gerenciado:

```bash
pulumi login s3://my-state-bucket
```

Segredos (ex.: senhas de banco de dados) são automaticamente criptografados e podem ser definidos com:

```bash
pulumi config set --secret dbPassword mySecret123
```

### 4. Testes

O Pulumi integra-se com estruturas de teste padrão (Jest, Pytest, etc.). Você pode escrever testes unitários com recursos simulados, testes de integração em stacks efêmeras e testes baseados em propriedades.

**Exemplo: Teste unitário com Jest**

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

it("deve criar um bucket S3", async () => {
    const { bucketName } = await import("./index");
    const value = await bucketName.get();
    expect(value).toEqual("my-unique-bucket");
});
```

### 5. Kubernetes Operator

O Pulumi Kubernetes Operator permite gerenciar recursos de nuvem e Kubernetes nativamente a partir do seu cluster usando Custom Resource Definitions (CRDs).

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

## Exemplo: Implantando um Bucket S3 (Multi-linguagem)

| Linguagem   | Trecho de Código                                                    |
|-------------|---------------------------------------------------------------------|
| Python      | `bucket = aws.s3.Bucket("my-bucket")`                               |
| Go          | `bucket, err := s3.NewBucket(ctx, "my-bucket", nil)`               |
| C#          | `var bucket = new Aws.S3.Bucket("my-bucket");`                     |
| Java        | `var bucket = new Bucket("my-bucket");`                            |
| YAML        | Usa a linguagem de modelo YAML do Pulumi.                           |

## Leitura Adicional

- [Documentação Oficial](https://www.pulumi.com/docs/)
- [Repositório no GitHub](https://github.com/pulumi/pulumi)
- [Registro Pulumi](https://www.pulumi.com/registry/)
- [Exemplos de Automation API](https://github.com/pulumi/automation-api-examples)
- [Guia de Policy as Code](https://www.pulumi.com/crossguard/)