---
title: Pulumi – 使用通用编程语言的基础设施即代码
description: Pulumi 是一个开源的基础设施即代码平台，允许用户使用熟悉的编程语言（如 TypeScript、Python、Go 和 C#）来定义和管理云资源。
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

Pulumi 是一个开源的基础设施即代码（IaC）平台，利用通用编程语言来定义、部署和管理云资源。无需学习专有的领域特定语言（DSL），您可以使用 TypeScript、Python、Go、C#、Java 和 YAML 等标准语言。这种方法将熟悉的软件工程实践——循环、函数、类、测试和包管理——直接引入到基础设施配置中。

## 为什么选择 Pulumi？

- **多语言与多云** – 使用同一种工具管理 AWS、Azure、GCP、Kubernetes 以及 100 多个提供商的资源。
- **开发者体验** – 使用您偏好的语言、IDE、调试器和测试框架。
- **Automation API** – 将基础设施操作直接嵌入应用程序代码或 CI/CD 管道中，无需使用 CLI。
- **Policy as Code** – 使用 TypeScript 或 OPA/Rego 执行安全、合规和成本规则。
- **状态管理** – 通过 Pulumi Cloud 或自管理后端（S3、GCS、Azure Blob）安全管理状态。密钥默认加密。
- **开源** – 核心引擎和许多提供程序基于 Apache 2.0 许可。

## 安装

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

安装后，验证版本：
```bash
pulumi version
```

> **注意**：在部署资源之前，您必须配置您的云提供商凭证（例如 `aws configure`）。

## 快速开始

使用模板创建一个新项目（此处为 AWS 与 TypeScript）：

```bash
pulumi new aws-typescript
```

这将生成一个 `Pulumi.yaml` 项目文件和一个 `index.ts`，您可以在其中定义基础设施。例如，创建一个 S3 存储桶：

```typescript
import * as aws from "@pulumi/aws";

const bucket = new aws.s3.Bucket("my-website-bucket", {
    website: {
        indexDocument: "index.html",
    },
});

export const bucketName = bucket.bucket;
```

部署堆栈：

```bash
pulumi up
```

预览更改，然后确认。部署后，查看输出：

```bash
pulumi stack output bucketName
```

完成后清理资源：

```bash
pulumi destroy
```

## 关键特性

### 1. Automation API

Automation API 将 Pulumi 引擎封装为库，使您能够以编程方式从任何应用程序配置基础设施，无需调用 CLI。

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

定义在执行 `pulumi up` 时运行的策略，以强制执行治理。策略使用 TypeScript 或 Rego/OPA 编写。

```typescript
import { PolicyPack } from "@pulumi/policy";

const policies = new PolicyPack("aws-policies", {
    policies: [
        {
            name: "s3-no-public-read",
            description: "禁止 S3 存储桶公共读取访问。",
            enforcementLevel: "mandatory",
            validateResource: (args, reportViolation) => {
                if (args.type === "aws:s3/bucket:Bucket") {
                    // 检查 acl 或 policy
                }
            },
        },
    ],
});
```

运行方式：

```bash
pulumi up --policy-pack ./policy
```

### 3. 状态管理

默认情况下，状态存储在 Pulumi Cloud（提供免费层级）中，它提供版本控制、协作和密钥加密。或者，使用自管理后端：

```bash
pulumi login s3://my-state-bucket
```

密钥（例如数据库密码）会自动加密，并可以通过以下方式设置：

```bash
pulumi config set --secret dbPassword mySecret123
```

### 4. 测试

Pulumi 与标准测试框架（Jest、Pytest 等）集成。您可以使用模拟资源编写单元测试、在临时堆栈上编写集成测试以及基于属性的测试。

**示例：使用 Jest 进行单元测试**

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

Pulumi Kubernetes Operator 允许您使用自定义资源定义（CRD）从集群中本地管理云和 Kubernetes 资源。

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

## 示例：部署 S3 存储桶（多语言）

| 语言        | 关键代码段                                                         |
|------------|--------------------------------------------------------------------|
| Python     | `bucket = aws.s3.Bucket("my-bucket")`                              |
| Go         | `bucket, err := s3.NewBucket(ctx, "my-bucket", nil)`              |
| C#         | `var bucket = new Aws.S3.Bucket("my-bucket");`                    |
| Java       | `var bucket = new Bucket("my-bucket");`                           |
| YAML       | 使用 Pulumi YAML 模板语言。                                        |

## 进一步阅读

- [官方文档](https://www.pulumi.com/docs/)
- [GitHub 仓库](https://github.com/pulumi/pulumi)
- [Pulumi 注册中心](https://www.pulumi.com/registry/)
- [Automation API 示例](https://github.com/pulumi/automation-api-examples)
- [Policy as Code 指南](https://www.pulumi.com/crossguard/)