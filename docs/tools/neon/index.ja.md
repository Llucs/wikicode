---
title: Neon – サーバーレスPostgreSQLプラットフォーム
description: Neonは、コンピュートとストレージを分離するオープンソースのサーバーレスPostgreSQLデータベースであり、最新のアプリケーション向けにインスタントブランチング、スケール・トゥ・ゼロ、およびボトムレスストレージを提供します。
created: 2026-06-18
tags:
  - serverless
  - postgres
  - database
  - branching
  - cloud
status: draft
---

# Neon – サーバーレスPostgreSQLプラットフォーム

Neonは、オープンソースのサーバーレスPostgreSQLプラットフォームであり、クラウドネイティブ基盤の上に従来のデータベースアーキテクチャを再構築します。コンピュート（クエリ処理）とストレージ（データ永続化）を完全に分離することで、NeonはAmazon Auroraのようなプロプライエタリシステムでのみ利用可能だった機能を、Postgresエコシステム全体に提供します。インスタントブランチング、自動スケール・トゥ・ゼロ、およびボトムレスストレージにより、Neonは最新の開発ワークフローとサーバーレスアプリケーション向けに設計されています。

---

## Why Neon?

| 課題 | Neonの解決策 |
|-----------|---------------|
| **アイドル状態のデータベースのコスト高** | コンピュートエンドポイントは非アクティブ後にゼロにスケールダウンし、アクティブなコンピュートに対してのみ課金されます。 |
| **開発サイクルの遅さ** | インスタントブランチングにより、各開発者やPRに完全なデータベースフォークが提供されます。 |
| **ストレージのプロビジョニングとコスト** | オブジェクトストア（例：S3）をバックエンドとするボトムレスストレージにより、手動の容量計画が不要。 |
| **サーバーレス/エッジ互換性** | コールドスタート時間約500ミリ秒、PgBouncerプーリングと組み合わせてエフェメラルコンピュートに最適。 |
| **ベクトルワークロード** | `pgvector`とPostGISを完全サポート。AIエンベディングをPostgres内で直接実行。 |

---

## 主な機能

### 1. インスタントブランチング

コピー・オン・ライト技術を使用して、Neonはテラバイト規模のデータベースのブランチをミリ秒で作成できます。これは以下に非常に役立ちます：

- **開発サンドボックス** – 各開発者が本番環境の独立したクローンを取得。
- **CI/CDパイプライン** – 本番データをミラーリングしたブランチに対して統合テストを実行。
- **スキーママイグレーション** – リスクなく破壊的な変更をテスト。

```bash
# Create a new branch from the main branch
npx neonctl branches create --name feature/ai-search
```

### 2. スケール・トゥ・ゼロ

コンピュートエンドポイントは非アクティブ期間が続くと自動的に停止します。新しい接続が来ると、エンドポイントは約500ミリ秒（コールドスタート）で再開します。これにより、アイドル状態や低トラフィックのデータベースのコストを排除します。

```sql
-- No configuration needed – scale‑to‑zero is automatic.
-- Connect and the endpoint wakes up transparently.
```

### 3. ボトムレスストレージ

ストレージは、安価なオブジェクトストレージでバックアップされた別のエンジン（Pageserver + Safekeepers）によって処理されます。ディスクをプロビジョニングしたり、容量不足を心配する必要はありません。

### 4. 完全なPostgreSQL互換性

NeonはPostgreSQL 14～17をサポートし、主要な拡張機能をすべて含みます：

- `pgvector` – エンベディングのベクトル類似検索。
- `PostGIS` – 地理空間クエリ。
- `pg_cron`、`pg_stat_statements`など。

既存のツールやドライバーは変更不要で動作します。

### 5. 透過的な接続プーリング

PgBouncerはプロキシレベルで統合されているため、アプリケーション設定なしで効率的な接続処理が得られます。

---

## クイックスタート

### オプションA: クラウド（マネージド）

1. [console.neon.tech](https://console.neon.tech) にサインアップします（豊富な無料枠を含む）。
2. UIまたはCLIでプロジェクトを作成します：

   ```bash
   # Install the Neon CLI
   npx neonctl

   # Create a project (first time: interactive)
   npx neonctl create-project

   # Get the connection string for the main branch
   npx neonctl connection-string
   ```

### オプションB: セルフホスティング

オープンソースリポジトリをクローンし、Docker ComposeまたはHelmを使用してデプロイします。

```bash
git clone https://github.com/neondatabase/neon.git
cd neon
docker compose up -d
```

本番環境のデプロイについては、[公式セルフホスティングガイド](https://neon.tech/docs/self-host) を参照してください。

---

## 使用例

### 接続してクエリを実行

```bash
psql "postgresql://user:pass@ep-cool-123456.us-east-2.aws.neon.tech/neondb"
```

```sql
-- Standard Postgres – everything works
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    payload JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- pgvector example
CREATE EXTENSION vector;
CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    embedding vector(1024)
);
```

### ブランチの作成と切り替え

```bash
# List branches
npx neonctl branches list

# Create a branch from a specific point in time (time travel)
npx neonctl branches create --from main --time "2026-06-17T12:00:00Z"

# Use a branch: get its connection string
npx neonctl connection-string --branch feature/ai-search
```

### Vercel / Netlifyとの統合

Neonは`@neondatabase/serverless`を介したHTTP接続をサポートしているため、エッジ関数から接続できます：

```javascript
// Example: Next.js API route
import { neon } from '@neondatabase/serverless';

export default async function handler(req, res) {
  const sql = neon(process.env.DATABASE_URL);
  const result = await sql`SELECT * FROM events`;
  res.json(result);
}
```

---

## アーキテクチャ概要

```
 Application
    |
    | (PostgreSQL protocol)
    |
 Proxy  ─── PgBouncer (connection pooling)
    |
 Compute Node (Stateless Postgres process)
    |
 Pageserver (Storage engine)
    |
 Safekeeper (WAL persistence)
    |
 Object Store (S3, GCS, etc.)
```

- **Compute nodes（コンピュートノード）**はステートレスであり、水平スケーリングが可能です。
- **Pageserver**はページ提供、チェックポイント、ブランチング（コピー・オン・ライト）を処理します。
- **Safekeeper**は確認応答前にWALの耐久性を保証します。

---

## 料金モデル

Neonは**使用量ベース**です：

| リソース | 無料枠 | 有料枠 |
|----------|-----------|-----------|
| コンピュート（アクティブ） | 10時間/月 | コンピュート時間ごとの課金 |
| ストレージ | 500MB | $0.12/GB/月 |
| ブランチング | 無制限 | 無制限 |
| 接続プーリング | あり | あり |

スケール・トゥ・ゼロは、アプリケーションが実際にクエリを処理しているときのみコンピュートに対して課金されることを意味します。

---

## 制限事項と注意点

- **コールドスタートレイテンシ** – 約500ミリ秒ですが、レイテンシに敏感な関数では顕著になる可能性があります。クリティカルなパスではキープアライブ接続または常時オンエンドポイントを使用してください。
- **機能のパリティ** – シングルサーバーデプロイのみ（ネイティブシャーディングなし）。マルチリージョンアクティブ-アクティブには、外部レプリケーション戦略が必要な場合があります。
- **無料枠の制限** – 複数のプロジェクトがアクティブな場合、10コンピュート時間の制限はすぐに消費される可能性があります。

---

## リソース

- [公式ドキュメント](https://neon.tech/docs)
- [GitHub リポジトリ](https://github.com/neondatabase/neon)
- [Neon Discord コミュニティ](https://discord.gg/neon)
- [ブログ – Neonのアーキテクチャを理解する](https://neon.tech/blog/architecture)

NeonはPostgreSQLを真のサーバーレスデータベースに変革し、最新のアプリケーション、CI/CD、AI/ベクトルワークロードに理想的な選択肢にしています。インスタントブランチング、スケール・トゥ・ゼロ、完全なPostgres互換性の組み合わせにより、2024年から2026年にかけて最も人気のあるインフラストラクチャプロジェクトの1つとなっています。