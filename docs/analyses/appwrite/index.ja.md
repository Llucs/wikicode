---
title: "Appwrite: セルフホスト型バックエンド・アズ・ア・サービスプラットフォーム"
description: "認証、データベース、ストレージ、サーバーレス関数、メッセージングのためのAPIを提供するオープンソースのBaaS – あなたが制御できるFirebaseの代替品。"
created: 2026-06-15
tags:
  - analysis
  - backend-as-a-service
  - self-hosted
  - firebase-alternative
  - serverless
  - platform-study
status: draft
---

# Appwrite: セルフホスト型バックエンド・アズ・ア・サービスプラットフォーム

Appwriteは、Web、モバイル、AIアプリケーションを迅速に構築するための完全なサーバーAPIとツールを提供する**オープンソースのBackend-as-a-Service（BaaS）**プラットフォームです。2019年にEldad Fuxによって作成され、現在は大規模なコミュニティ（40k以上のGitHubスター）に支えられており、データの所有権、プライバシー、柔軟なデプロイを優先するFirebaseのセルフホスト代替として設計されています。

個別のマイクロサービスを配線する代わりに、Appwriteは認証、データベース、ストレージ、サーバーレス関数、メッセージング、リアルタイムイベントのための統合APIを提供します。これらはすべて自分のインフラストラクチャ上で実行されます。

---

## なぜAppwriteか？

- **データ所有権** – データの保存場所と方法を自分で制御。GDPR、HIPAA、または内部コンプライアンスに重要。
- **ベンダーロックインなし** – セルフホストまたはクラウド提供を利用。コードはポータブルなまま。
- **豊富なサービスセット** – 認証（OAuth2、MFA、JWT、マジックURL）、NoSQLデータベース、ファイルストレージ、サーバーレス関数、プッシュ/メール/SMSメッセージング、リアルタイムサブスクリプションなど、すべて1つに。
- **シンプルで統合されたAPI** – Web（JavaScript/TypeScript）、Flutter、Android、iOS、サーバーサイドコード全体で同じSDKパターン。
- **活発なオープンソースエコシステム** – 活発なコミュニティ、公式SDK、CLI、成長するインテグレーションライブラリ（Stripe、Twilio、SendGrid、関数を介したGPT-4oなど）に支えられています。
- **ラピッドプロトタイピングから本番環境へ** – 管理コンソールでノーコードセットアップを行い、SDKを組み込んで完全制御。

---

## 主な機能とコマンド例

### 認証
電子メール/パスワード、電話（SMS）、OAuth2（Google、GitHub、Discordなど）、マジックURL、JWT、匿名セッション、多要素認証（MFA）をサポートしています。

```javascript
import { Client, Account, ID } from 'appwrite';

// Initialize client
const client = new Client()
    .setEndpoint('https://<HOST>/v1')
    .setProject('<PROJECT_ID>');

const account = new Account(client);

// Register a user
await account.create(ID.unique(), 'user@example.com', 'password123', 'Jane Doe');

// Log in
await account.createEmailPasswordSession('user@example.com', 'password123');

// Get current user
const user = await account.get();
```

### データベース（NoSQL）
高度なクエリ、全文検索、リアルタイムリスナー、リレーションシップを備えたドキュメントベースのストレージ。

```javascript
import { Databases, ID } from 'appwrite';

const databases = new Databases(client);

// Create a document
await databases.createDocument(
    '<DATABASE_ID>',
    '<COLLECTION_ID>',
    ID.unique(),
    { title: 'My Post', body: 'Hello, world!', tags: ['appwrite'] }
);

// List documents
const results = await databases.listDocuments(
    '<DATABASE_ID>',
    '<COLLECTION_ID>',
    [Query.equal('tags', ['appwrite'])]
);
```

### ストレージ
組み込みの画像プレビュー、リサイズ、トリミング、マルウェアスキャンを備えたファイルアップロード。

```javascript
import { Storage, ID } from 'appwrite';

const storage = new Storage(client);

// Upload a file
const uploaded = await storage.createFile(
    '<BUCKET_ID>',
    ID.unique(),
    myFile
);
```

### サーバーレス関数
イベント（データベース、ストレージ、認証、スケジュール）に応答してコードを実行します。サポートされているランタイム：Node.js、Python、Ruby、PHP、Dart、Deno、Kotlin、Swift、.NET。

```bash
# Create a function via CLI
appwrite functions create \
  --name='sendWelcomeEmail' \
  --runtime='node-18.0' \
  --execute='any' \
  --entrypoint='index.js'

# Deploy code
appwrite functions deploy \
  --functionId='<FUNCTION_ID>' \
  --path='./my-function'
```

```javascript
// Index function code (Node.js)
export default async ({ req, res, log, error }) => {
    log('Function triggered');
    return res.json({ message: 'Hello from Appwrite Functions!' });
};
```

### メッセージング
プッシュ通知（FCM/APNS）、電子メール（SMTP、SendGrid、Mailgun）、SMS（Twilio、Vonage、TextMagic）。すべて管理コンソールまたはAPIで管理されます。

```javascript
import { Messaging } from 'appwrite';

const messaging = new Messaging(client);
await messaging.createEmail(
    '<MESSAGE_ID>',
    '<SUBJECT>',
    '<CONTENT>',
    [userEmail]
);
```

### リアルタイム
データベース、ストレージ、関数のイベントを（WebSocketベースで）購読します。

```javascript
import { Client } from 'appwrite';

const client = new Client()
    .setEndpoint('https://<HOST>/v1')
    .setProject('<PROJECT_ID>');

client.subscribe('databases.<DB_ID>.collections.<COLL_ID>.documents', response => {
    console.log('Document changed:', response.payload);
});
```

### GraphQL API
Appwriteは完全なGraphQLエンドポイントを公開しており、GraphQLとうまく連携するフロントエンドフレームワークに適しています。

```graphql
query {
  usersList(limit: 10) {
    users {
      name
      email
      $id
    }
  }
}
```

### 管理コンソール
すべてのサービスを管理するための完全なWebインターフェース。データベース、コレクション、ユーザー、ストレージバケット、トリガーの作成にコーディングは不要です。

---

## アーキテクチャ

AppwriteはDockerでオーケストレーションされた**マイクロサービスアーキテクチャ**を使用しています。各サービスは分離されたコンテナとして実行されます。

- **MariaDB** – メタデータストア（プロジェクト、ユーザーなど）
- **Redis** – キャッシュおよびジョブキュー
- **InfluxDB** – 使用状況のメトリクスと分析
- **Kafka** – メッセージおよびイベントストリーミング
- **Workers** – バックグラウンドタスク（電子メール、関数、ウェブフック、移行）

専用のワーカーが非同期処理を処理し、メインAPIの応答性を維持します。スタック全体は単一のインストールコマンドで起動されます。

---

## インストール

### セルフホスト（Docker）

Appwriteを自分のサーバーで稼働させる最も簡単な方法：

```bash
docker run -it --rm \
    --volume /var/run/docker.sock:/var/run/docker.sock \
    --volume "$(pwd)"/appwrite:/storage/config:rw \
    --entrypoint="install" \
    appwrite/appwrite:latest
```

これにより、必要なすべてのコンテナをプルして設定する対話型インストーラが起動します。デフォルトでは、Appwriteは`http://0.0.0.0`で実行されます。

### クラウド（マネージド）

[cloud.appwrite.io](https://cloud.appwrite.io)にサインアップ – 利用制限付きの無料ティアがあり、プロトタイピングに最適です。

### コンソールのセットアップ

インストール後（セルフホストまたはクラウド）、コンソールでプロジェクトを作成し、プロジェクトIDとエンドポイントをメモし、APIキーを生成します。

---

## 基本的な使用方法（JavaScript SDK）

1. **クライアントの初期化と認証**

   ```javascript
   import { Client, Account, ID } from 'appwrite';

   const client = new Client()
       .setEndpoint('https://<HOST>/v1')
       .setProject('<PROJECT_ID>');

   const account = new Account(client);

   // Register & Login
   await account.create(ID.unique(), 'user@test.com', 'password123', 'Jane Doe');
   await account.createEmailPasswordSession('user@test.com', 'password123');
   ```

2. **ドキュメントの作成とクエリ**

   ```javascript
   import { Databases, Query } from 'appwrite';

   const databases = new Databases(client);

   // Create
   await databases.createDocument(
       '<DATABASE_ID>',
       '<COLLECTION_ID>',
       ID.unique(),
       { name: 'Task', status: 'backlog' }
   );

   // Query
   const tasks = await databases.listDocuments(
       '<DATABASE_ID>',
       '<COLLECTION_ID>',
       [Query.equal('status', 'backlog'), Query.limit(25)]
   );
   ```

3. **CLI経由での関数のデプロイ**

   ```bash
   appwrite functions create --name='processOrder' --runtime='node-18.0' --execute='any'
   appwrite functions deploy --functionId='<ID>' --path='./functions/process-order'
   ```

4. **リアルタイムイベントのリッスン**

   ```javascript
   client.subscribe('databases.*.collections.*.documents', event => {
       console.log(`${event.events[0]} –`, event.payload);
   });
   ```

---

## ユースケース

- **MVPとラピッドプロトタイプの構築** – バックエンドのセットアップをスキップし、フロントエンドロジックに集中。
- **フルスタックWebアプリ** – React、Vue、Next.js、Svelte、Nuxt、Angular。
- **クロスプラットフォームモバイルアプリ** – Flutter、Android、iOS（SwiftUI）、React Native。
- **AI対応機能** – サーバーレス関数を介してGPT-4oやその他のLLMを統合。
- **内部ツール** – 管理コンソールとリアルタイム更新を管理ダッシュボードに活用。
- **GDPR/HIPAA準拠アプリ** – 自社のデータセンターでセルフホスト。

---

## 類似ツールとの比較

| 機能                | Appwrite                        | Supabase                          | PocketBase                        |
|---------------------|----------------------------------|-----------------------------------|-----------------------------------|
| データベースモデル  | NoSQL (ドキュメント)               | SQL (PostgreSQL)                  | SQLite                            |
| セルフホスト        | はい (Docker)                     | はい (Docker)                      | はい (単一バイナリ)               |
| サーバーレス関数    | はい (Node, Python, Ruby など)   | はい (PostgreSQL関数 + エッジ)     | はい (JavaScript/Go)               |
| リアルタイム        | WebSocket (DB, ストレージ, イベント) | PostgreSQLレプリケーション         | WebSocket (DB)                    |
| 認証                | OAuth2, MFA, マジックURL, SMS      | OAuth2, MFA, SSO                  | OAuth2, MFA                       |
| メッセージング      | プッシュ, メール, SMS                | メール (pgmq経由)                 | –                                 |
| ストレージ          | 画像プレビュー, リサイズ, スキャン      | はい (S3互換)                     | はい                               |
| 管理UI              | フル機能のWebコンソール             | Webコンソール                     | 最小限のWeb UI                    |
| クライアントSDK     | Web, Flutter, Android, iOS, CLI  | Web, Flutter, Swift, Kotlin など  | Web, Dart, Android, iOS, Go       |

統合された、意見を持つNoSQLプラットフォーム（組み込みのメッセージング、GraphQL、リッチな管理コンソール）が必要で、データを自分のDockerスタックに保持したい場合は、**Appwriteを選択**してください。

---

## コミュニティとエコシステム

- **GitHub** – [github.com/appwrite/appwrite](https://github.com/appwrite/appwrite)
- **Discord** – 活発な開発者コミュニティ
- **テンプレートとオープンプロジェクト** – [builtwith.appwrite.network](https://builtwith.appwrite.network) を参照
- **インテグレーション** – AI、センサー、不正検出などのためのAppwrite MCP
- **ハッカソン** – Hacktoberfest、Dev.toのチャレンジで頻繁に取り上げられています

---

## 結論

Appwriteは、ロックインなしでFirebaseの力を提供する成熟したオープンソースのBaaSです。セルフホスティング機能、豊富な機能セット、活発なコミュニティにより、ハッカソンから規制のあるエンタープライズ環境まで、あらゆる場面で優れた選択肢となります。クラウドバージョンを使用するか、自分で実行するかにかかわらず、Appwriteはバックエンドの複雑さを抽象化し、アプリの構築に集中できるようにします。

**今すぐ始めましょう：**

```bash
docker run -it --rm --volume /var/run/docker.sock:/var/run/docker.sock --volume $(pwd)/appwrite:/storage/config:rw --entrypoint="install" appwrite/appwrite:latest
```
または、[cloud.appwrite.io](https://cloud.appwrite.io)にサインアップしてください。