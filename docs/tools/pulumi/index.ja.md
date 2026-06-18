---
title: Pulumi – 汎用プログラミング言語を使用した Infrastructure as Code
description: Pulumi はオープンソースの Infrastructure as Code プラットフォームで、TypeScript、Python、Go、C# などの身近なプログラミング言語を使用してクラウドリソースを定義および管理できます。
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

Pulumi は、汎用プログラミング言語を活用してクラウドリソースを定義、デプロイ、管理するためのオープンソースの Infrastructure as Code (IaC) プラットフォームです。独自のドメイン固有言語 (DSL) を学習する代わりに、TypeScript、Python、Go、C#、Java、YAML などの標準的な言語を使用します。このアプローチにより、ループ、関数、クラス、テスト、パッケージ管理といった使い慣れたソフトウェアエンジニアリングのプラクティスを、インフラストラクチャのプロビジョニングに直接適用できます。

## Why Pulumi?

- **マルチ言語＆マルチクラウド** – 同じツールで AWS、Azure、GCP、Kubernetes、および100以上のプロバイダーのリソースを管理できます。
- **開発者エクスペリエンス** – 好みの言語、IDE、デバッガ、テストフレームワークを使用できます。
- **Automation API** – CLI を必要とせずに、アプリケーションコードや CI/CD パイプラインに直接インフラストラクチャ操作を組み込むことができます。
- **Policy as Code** – TypeScript または OPA/Rego を使用してセキュリティ、コンプライアンス、コストルールを適用します。
- **状態管理** – Pulumi Cloud または自己管理バックエンド（S3、GCS、Azure Blob）を介して状態を安全に管理します。シークレットはデフォルトで暗号化されます。
- **オープンソース** – コアエンジンと多くのプロバイダーは Apache 2.0 ライセンスです。

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

インストール後、バージョンを確認します:
```bash
pulumi version
```

> **注**: リソースをデプロイする前に、クラウドプロバイダーの認証情報を設定する必要があります（例：`aws configure`）。

## Quick Start

テンプレートを使用して新しいプロジェクトを作成します（ここでは AWS と TypeScript）:

```bash
pulumi new aws-typescript
```

これにより、`Pulumi.yaml` プロジェクトファイルと `index.ts` が生成され、そこでインフラストラクチャを定義します。例えば、S3 バケットを作成する場合:

```typescript
import * as aws from "@pulumi/aws";

const bucket = new aws.s3.Bucket("my-website-bucket", {
    website: {
        indexDocument: "index.html",
    },
});

export const bucketName = bucket.bucket;
```

スタックをデプロイします:

```bash
pulumi up
```

変更をプレビューし、確認します。デプロイ後、出力を表示:

```bash
pulumi stack output bucketName
```

リソースをクリーンアップする場合:

```bash
pulumi destroy
```

## Key Features

### 1. Automation API

Automation API は Pulumi エンジンをライブラリとしてパッケージ化し、CLI を呼び出さずに任意のアプリケーションからプログラムによってインフラストラクチャをプロビジョニングできるようにします。

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

`pulumi up` 実行時にポリシーを定義してガバナンスを強制します。ポリシーは TypeScript または Rego/OPA で記述します。

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

次のように実行します:

```bash
pulumi up --policy-pack ./policy
```

### 3. State Management

デフォルトでは、状態は Pulumi Cloud に保存されます（無料枠あり）。バージョン管理、コラボレーション、シークレット暗号化が提供されます。代わりに、自己管理バックエンドを使用することもできます:

```bash
pulumi login s3://my-state-bucket
```

シークレット（例：データベースパスワード）は自動的に暗号化され、次のように設定できます:

```bash
pulumi config set --secret dbPassword mySecret123
```

### 4. Testing

Pulumi は標準的なテストフレームワーク（Jest、Pytest など）と統合します。モックされたリソースを使った単体テスト、一時的なスタックに対する統合テスト、プロパティベースのテストを記述できます。

**例: Jest を使った単体テスト**

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

Pulumi Kubernetes Operator を使用すると、カスタムリソース定義 (CRD) を使用してクラスター内からクラウドおよび Kubernetes リソースをネイティブに管理できます。

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

| 言語          | コードスニペット                                                    |
|---------------|--------------------------------------------------------------------|
| Python        | `bucket = aws.s3.Bucket("my-bucket")`                              |
| Go            | `bucket, err := s3.NewBucket(ctx, "my-bucket", nil)`              |
| C#            | `var bucket = new Aws.S3.Bucket("my-bucket");`                    |
| Java          | `var bucket = new Bucket("my-bucket");`                           |
| YAML          | Pulumi YAML テンプレート言語を使用します。                            |

## Further Reading

- [公式ドキュメント](https://www.pulumi.com/docs/)
- [GitHub リポジトリ](https://github.com/pulumi/pulumi)
- [Pulumi レジストリ](https://www.pulumi.com/registry/)
- [Automation API の例](https://github.com/pulumi/automation-api-examples)
- [Policy as Code ガイド](https://www.pulumi.com/crossguard/)