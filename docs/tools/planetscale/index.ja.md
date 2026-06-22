---
title: PlanetScale: Serverless MySQL データベースプラットフォーム
description: Vitess 上に構築されたフルマネージドな MySQL 互換データベースプラットフォーム。database branching と non-blocking schema changes を導入し、最新の開発ワークフローに対応します。
created: 2026-06-22
tags:
  - database
  - mysql
  - vitess
  - serverless
  - schema-migration
  - devops
  - dbaas
  - branching
status: draft
---

# PlanetScale

## Introduction

PlanetScale は、Vitess のコア開発者（Sugu Sougoumarane、Jiten Vaidya、Morgan Goeller）によって 2018 年に設立された、YouTube を支えるオープンソースのデータベースクラスタリングシステムをベースとした MySQL 互換データベースプラットフォームです。データベース管理に **Git スタイルのワークフロー**（データベースブランチングと Deploy Requests）を適用することで、従来のスキーママイグレーションに伴うボトルネックやダウンタイムを排除します。

このアプローチにより、データベースの変更をコード変更と同じように安全でレビュー可能かつ反復的に行うことができます。PlanetScale はフルマネージドサービスであり、レプリケーション、バックアップ、シャーディング、高可用性を処理し、ゼロにスケールダウンして接続時に即座に起動するサーバーレスコンピュートレイヤーをサポートします。

## Core Concepts

### Database Branching

データベースブランチングは、`git branch` が独立したコード開発を可能にするように、`pscale branch create` は PlanetScale のインフラ上に分離された完全に機能するデータベースのコピー（データとスキーマを含む）を作成します。

- **任意の時点からブランチを作成:** `main` または以前のスナップショットからブランチを作成できます。
- **データとスキーマ:** ブランチには完全なスナップショットが含まれ、非常に現実的なテストが可能です。
- **一時的な性質:** ブランチは目的が達成され次第破棄されることを前提としており、スキーマの乖離を防ぎます。

### Deploy Requests (DRs)

Deploy Requests は PlanetScale における Pull Request に相当します。ブランチでのスキーマ変更に満足したら、Deploy Request を開きます。これにより差分が生成され、レビューが可能になり、**ノンブロッキングなオンラインスキーママイグレーション**（Vitess VReplication を使用）としてマージが実行されます。

### Serverless Compute

PlanetScale はコンピュートとストレージを分離しています。アクティブな接続がない場合、データベースは「スリープ」状態になります。接続があるとデータベースは即座に起動し、アイドルコンピュートコストを排除します。

## Getting Started

はじめに

### Installation

インストール

**macOS:**
```bash
brew install planetscale/tap/pscale
```

**Linux / Windows:**
```bash
curl -fsSL https://planetscale.com/install.sh | sh
```

### Authentication

認証

```bash
pscale auth login
```

### Creating a Database

データベースの作成

```bash
pscale database create my-app
```

### Working with Branches

ブランチの操作

**フィーチャーブランチを作成する（main からスキーマとデータをコピー）:**
```bash
pscale branch create my-app feature-user-profile
```

**ブランチに接続する:**
```bash
pscale connect my-app feature-user-profile --port 3309
```

これはローカルプロキシを実行します。アプリケーションは `127.0.0.1:3309` に接続します。プロキシが認証を自動的に処理します。

**ブランチに対してスキーママイグレーションを実行する:**

任意の MySQL クライアント、ORM、マイグレーションツール（例：`mysql2`、`Prisma`、`SQLAlchemy`）を使用します。
```sql
ALTER TABLE users ADD COLUMN bio TEXT;
```

### The Deploy Request Flow

Deploy Request のフロー

ブランチでスキーマ変更を十分にテストしたら：

```bash
# Create the Deploy Request
pscale deploy-request create my-app feature-user-profile

# List deploy requests
pscale deploy-request list my-app

# Deploy the request (after review)
pscale deploy-request deploy my-app <deploy-number>

# Clean up the branch
pscale branch delete my-app feature-user-profile --force
```

デプロイは、*テーブルをロックしたりダウンタイムを発生させることなく*、スキーマ変更を `main` に適用します。

## Key Features in Depth

主要機能の詳細

### Non-Blocking Schema Changes (Online DDL)

ノンブロッキングなスキーマ変更 (Online DDL)

従来の MySQL の `ALTER TABLE` 文はテーブルをロックすることがよくあります。PlanetScale は VReplication を介して Vitess の **Online DDL** を使用します。シャドウテーブルを作成し、データを増分的にコピーし、透過的に切り替えます。

**コマンド例:**
```bash
pscale deploy-request deploy my-app 1
```

大規模で長時間のマイグレーション中でも、本番環境は完全に動作し続けます。

### Connection Pooling

コネクションプーリング

組み込みのサーバーサイドコネクションプーリングが接続スパイクを管理します。`pscale connect` を使用する場合、ローカルプロキシも接続をプールします。本番環境では、PlanetScale サーバーアドレスに直接接続します。

### Horizontal Sharding (Vitess)

水平シャーディング (Vitess)

非常に大規模なデータセットの場合、PlanetScale は Vitess のキーレンジシャーディングを使用して、データを透過的に複数の MySQL インスタンスに分散します。アプリケーションの変更は必要ありません。

### High Availability & Global Replication

高可用性とグローバルレプリケーション

高可用性は組み込まれています。PlanetScale はクロスリージョンレプリカと自動フェイルオーバーを提供し、99.99% のアップタイム SLA を保証します。

## Practical Use Cases

実用的なユースケース

### CI/CD Integration

CI/CD 統合

プルリクエストごとに分離されたデータベースブランチを起動し、実際の本番データに対して統合テストを実行します。

```bash
pscale branch create my-app ci-pr-123 --from main
pscale connect my-app ci-pr-123 --port 3309 &
# Run integration tests here
pscale branch delete my-app ci-pr-123 --force
```

### Pre-Production Testing

プレプロダクションテスト

QA チームは本番データを破損することなく、完全に現実的なブランチで破壊的テストや負荷テストを実行できます。

### Schema Review

スキーマレビュー

チームメンバーはマージ前に Deploy Request 内の正確な SQL 差分をレビューし、「データベースをコードとして」扱うワークフローを実現します。

### Ephemeral Environments

一時的な環境

`pscale branch create/destroy` をプラットフォームエンジニアリングツール（例：Kubernetes オペレーター、Terraform）と組み合わせて、開発者またはフィーチャーごとにフルスタック環境を提供します。

## Limitations and Caveats

制限事項と注意点

強力ですが、PlanetScale の Vitess 基盤にはいくつかの MySQL 互換性に関する癖があります：

- **No Stored Procedures or Triggers:** Vitess プロキシレイヤーはこれらをサポートしていません。
- **外部キー:** ベータ版（データベースごとに有効にする必要があります）。重要な本番環境での使用はまだ推奨されません。
- **`LOCK TABLES` / `UNLOCK TABLES`:** サポートされていません。
- **`GET_LOCK()` / `RELEASE_LOCK()`:** サポートされていません。
- **サブクエリと `JOIN`:** ほとんどサポートされていますが、非常に複雑な相関サブクエリや非決定的なステートメントは異なる動作をする可能性があります。
- **本番環境での直接の `ALTER TABLE`:** Deploy Request ワークフローが本番環境でスキーマ変更を行う *唯一の* 安全な方法です。`pscale connect` 経由で本番ブランチに直接 `ALTER TABLE` を実行することは強く推奨されません。

> **開発者ノート:** 本番環境のスキーマ変更には常に Deploy Request ワークフローを使用してください。開発ブランチでは、直接の `ALTER TABLE` は安全で高速です。

## Pricing Model

価格モデル

PlanetScale は、手厚い無料枠を備えた SaaS 製品として運営されています。料金は行ストレージと行の読み取り/書き込みに基づきます。

| Tier | Price | Row Storage | Compute | Branches |
|---|---|---|---|---|
| **Free** | $0/mo | 5 GB | 10M row reads/mo, 1M row writes/mo | Up to 3 |
| **Scaler** | $39/mo (base) | 10 GB | 100M row reads, 10M row writes | Up to 10 |
| **Business** | Custom | Custom | Custom | Custom |

*価格の詳細は変更される可能性があります。必ず [PlanetScale 価格ページ](https://planetscale.com/pricing) で確認してください。*

## Best Practices

ベストプラクティス

- **ブランチの命名:** 一貫した名前空間を使用する（例：`feature/*`、`hotfix/*`、`ci/*`）。
- **古いブランチの削除:** ストレージコストを避けるために定期的にブランチをクリーンアップする。
  ```bash
  pscale branch delete my-app stale-branch --force
  ```
- **パフォーマンスの監視:** PlanetScale ダッシュボードを使用して、クエリパフォーマンス、スロークエリ、接続使用率を監視します。クエリ explain と insights 機能は強力です。
- **環境の均一性:** `main` を常に本番環境として清潔に保ちます。開発チームはブランチ上でのみ作業します。
- **本番ブランチのプロキシでの重いクエリを避ける:** ブランチはスナップショットですが、本番と同じ基盤クラスタに接続されたブランチで大規模な分析クエリを実行すると、共有 I/O に影響を与える可能性があります。

## Troubleshooting

トラブルシューティング

**プロキシで接続が拒否された場合:**
```bash
pscale connect my-app main
```
ポートで他のサービスが実行されていないことを確認してください。代替ポートを指定するには `--port` を使用します。

**スキーマ変更に失敗した場合:**
PlanetScale ダッシュボードの Deploy Request ログを確認するか、以下を使用します：
```bash
pscale deploy-request show my-app <deploy-number>
```

**クエリレイテンシが高い場合:**
接続プールの制限を確認してください。マージ前にブランチにインデックスを追加することを検討します：
```sql
ALTER TABLE users ADD INDEX idx_email (email);
```

## Comparison to Alternatives

代替サービスとの比較

| Feature | PlanetScale | Neon (Postgres) | Supabase (Postgres) | RDS (MySQL) |
|---|---|---|---|---|
| **Branching** | Instant, full data | Instant, full data | Branching via SQL | Manual snapshots |
| **Serverless** | Yes (sleep/wake) | Yes (sleep/wake) | Yes (auto-suspend) | No (Always On) |
| **Schema Migrations** | Non-blocking (Online DDL) | Branching + `pgroll` | Branching + migrations | Manual |
| **Sharding** | Automatic (Vitess) | No | No | Manual (Sharding) |
| **Migration CI Flow** | Excellent (Deploy Requests) | Excellent | Good | Poor |

**PlanetScale を選ぶべき場合:**
MySQL 互換性、複雑なスキーマ変更とテストのためのデータベースブランチング、自動水平スケーリングが必要な場合。

**PlanetScale を避けるべき場合:**
ストアドプロシージャ、トリガー、高度な MySQL 内部機能（例：`GET_LOCK()`）に大きく依存している場合。その場合は、RDS や標準のマネージド MySQL ソリューションの方が適している可能性があります。

## Summary

まとめ

PlanetScale は、データベースレイヤーに Git のようなワークフローをもたらすことで、MySQL 開発体験に革命を起こします。データとスキーマを即座にブランチ化する機能と、ノンブロッキングな Deploy Requests により、チームはアプリケーションコードと同じ安全性と速度でデータベーススキーマを反復的に改善できます。実績のある Vitess エンジン上に構築されており、運用オーバーヘッドなしで YouTube レベルのスケーラビリティを提供します。