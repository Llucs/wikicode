---
title: Pulumi – Infrastructure as Code with General-Purpose Languages
description: Pulumi is an open-source Infrastructure as Code platform that allows users to define and manage cloud resources using familiar programming languages like TypeScript, Python, Go, and C#.
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

Pulumi is an open-source Infrastructure as Code (IaC) platform that leverages general-purpose programming languages to define, deploy, and manage cloud resources. Instead of learning a proprietary domain-specific language (DSL), you use standard languages such as TypeScript, Python, Go, C#, Java, and YAML. This approach brings familiar software engineering practices — loops, functions, classes, testing, and package management — directly to infrastructure provisioning.

## Why Pulumi?

- **Multi-Language & Multi-Cloud** – Manage resources across AWS, Azure, GCP, Kubernetes, and 100+ providers with the same tool.
- **Developer Experience** – Use your preferred language, IDE, debugger, and test frameworks.
- **Automation API** – Embed infrastructure operations directly into application code or CI/CD pipelines without requiring the CLI.
- **Policy as Code** – Enforce security, compliance, and cost rules using TypeScript or OPA/Rego.
- **State Management** – Securely manage state via Pulumi Cloud or self-managed backends (S3, GCS, Azure Blob). Secrets are encrypted by default.
- **Open Source** – Core engine and many providers are Apache 2.0 licensed.

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

After installation, verify the version:
```bash
pulumi version
```

> **Note**: You must configure your cloud provider credentials (e.g., `aws configure`) before deploying resources.

## Quick Start

Create a new project using a template (here AWS with TypeScript):

```bash
pulumi new aws-typescript
```

This generates a `Pulumi.yaml` project file and an `index.ts` where you define infrastructure. For example, to create an S3 bucket:

```typescript
import * as aws from "@pulumi/aws";

const bucket = new aws.s3.Bucket("my-website-bucket", {
    website: {
        indexDocument: "index.html",
    },
});

export const bucketName = bucket.bucket;
```

Deploy the stack:

```bash
pulumi up
```

Preview changes, then confirm. After deployment, view outputs:

```bash
pulumi stack output bucketName
```

Clean up resources when done:

```bash
pulumi destroy
```

## Key Features

### 1. Automation API

The Automation API packages the Pulumi engine as a library, enabling you to provision infrastructure programmatically from any application without shelling out to the CLI.

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

Define policies that run during `pulumi up` to enforce governance. Policies are written in TypeScript or Rego/OPA.

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

Run with:

```bash
pulumi up --policy-pack ./policy
```

### 3. State Management

By default, state is stored in Pulumi Cloud (free tier available), which provides versioning, collaboration, and secret encryption. Alternatively, use a self-managed backend:

```bash
pulumi login s3://my-state-bucket
```

Secrets (e.g., database passwords) are automatically encrypted and can be set with:

```bash
pulumi config set --secret dbPassword mySecret123
```

### 4. Testing

Pulumi integrates with standard test frameworks (Jest, Pytest, etc.). You can write unit tests with mocked resources, integration tests on ephemeral stacks, and property-based tests.

**Example: Unit test with Jest**

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

The Pulumi Kubernetes Operator allows you to manage cloud and Kubernetes resources natively from your cluster using Custom Resource Definitions (CRDs).

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

## Example: Deploying an S3 Bucket (Multi-Language)

| Language      | Key Snippet                                                        |
|---------------|--------------------------------------------------------------------|
| Python        | `bucket = aws.s3.Bucket("my-bucket")`                              |
| Go            | `bucket, err := s3.NewBucket(ctx, "my-bucket", nil)`              |
| C#            | `var bucket = new Aws.S3.Bucket("my-bucket");`                    |
| Java          | `var bucket = new Bucket("my-bucket");`                           |
| YAML          | Uses Pulumi YAML template language.                                |

## Further Reading

- [Official Documentation](https://www.pulumi.com/docs/)
- [GitHub Repository](https://github.com/pulumi/pulumi)
- [Pulumi Registry](https://www.pulumi.com/registry/)
- [Automation API Examples](https://github.com/pulumi/automation-api-examples)
- [Policy as Code Guide](https://www.pulumi.com/crossguard/)