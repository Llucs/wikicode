---
title: API バージョニング戦略
description: 既存のクライアントを壊さずにAPIを長期間にわたって変更管理するための必須のテクニックとベストプラクティス。URIベース、ヘッダーベース、クエリパラメータ、スキーマベースのアプローチを含みます。
created: 2026-06-24
tags:
  - api-design
  - rest
  - versioning
  - architecture
  - backend
status: draft
---

# API バージョニング戦略

APIバージョニングとは、公開または内部のAPI契約に対する変更を管理する実践であり、プロバイダーが既存のコンシューマーを混乱させることなくインターフェースを進化させることを可能にします。これにより、同じリソースの複数の表現を並行して実行でき、革新と安定性のバランスを取ることができます。適切な戦略を選択し、一貫して実装することは、API設計において最も重要な決定の一つです。

このガイドでは、最も一般的なバージョニング手法、そのトレードオフ、実際のユースケース、主要なフレームワーク向けの実装例について説明します。また、適切なライフサイクルヘッダーを使用して非推奨化と廃止を処理する方法についても学びます。

---

## なぜバージョンが重要なのか

バージョニングがなければ、APIへのすべての変更はリスクを伴います：

- 必須フィールドを追加すると、古いペイロードを送信するクライアントが壊れる可能性があります。
- エンドポイントを削除すると、本番環境で障害が発生する可能性があります。
- レスポンスフィールドの形式を変更する（例えば、文字列から整数）と、すべてのコンシューマーが同時に更新する必要が生じます。

バージョニング戦略は**契約**を提供します。バージョン`v1`のクライアントは安定したインターフェースが保証され、プロバイダーは`v2`で破壊的変更を導入できます。これにより、チームはコンシューマーとの信頼を維持しながら迅速にリリースできます。

### 歴史的背景

- **初期のREST API（2000年代半ば）：** Flickr、Twitterなどは、明確にするためにURIに`/v1/`を付け始めました。SOAPは厳格なWSDLスキーマに依存していました。
- **Roy Fieldingの論文**は、ハイパーメディア（HATEOAS）を「自然な」バージョニングメカニズムとして提唱しました。リンクがクライアントを状態間で導く方式です。しかし、複雑さからURIバージョニングが事実上の標準となりました。
- **GraphQL（2015）**は、破壊的変更の代わりにフィールドの非推奨化を使用する「バージョンレス」アプローチを推進しました。
- **gRPC**は、契約の進化のためにProtobufパッケージとスキーマレジストリを使用します。
- **OpenAPI仕様**は、現在1つの仕様ファイルに複数のバージョンを文書化できるようになり、バージョンの作成と比較が容易になりました。

---

## 主要な戦略

すべての戦略は、**明示的なバージョン識別子**（コンシューマーにとって簡単）から**暗黙的な契約**（プロバイダーにとってクリーン）までのスペクトルに沿っています。エコシステムの成熟度と破壊的変更に対する許容度に基づいて選択してください。

### 1. URI / パスバージョニング

バージョンがURLパスに直接埋め込まれており、最も一般的で簡単なアプローチです。

```
GET /v1/users
GET /v2/users
```

**利点**
- 実装とルーティングが簡単。
- 発見可能性が高い ― コンシューマーはすぐにバージョンを確認できる。
- 優れたキャッシング：異なるバージョンを独立してキャッシュできる。
- APIゲートウェイやCDNへのデプロイが容易。

**欠点**
- RESTセマンティクスに違反する：URIはリソースを識別すべきであり、バージョンではない（Fieldingによる）。
- レイヤーで設計しないとサーバーコードのフォークを促進する。
- 表現ごとにバージョンを付けることができない（例：`Accept`ヘッダーに基づく同じリソースの異なるバージョン）。

**実装例 (Express.js)**

```javascript
// v1 router
const v1Router = require('./routes/v1');
app.use('/v1', v1Router);

// v2 router
const v2Router = require('./routes/v2');
app.use('/v2', v2Router);
```

**実装例 (ASP.NET Core)**

```csharp
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/[controller]")]
public class UsersController : ControllerBase
{
    [HttpGet]
    public IActionResult Get() => Ok("Users from v1");
}
```

### 2. クエリパラメータバージョニング

クエリパラメータでバージョンを指定します。

```
GET /users?version=1
GET /users?version=2
```

**利点**
- ルートを変更せずに簡単に追加できる。
- URLパターンがバージョン間で一貫している。

**欠点**
- クエリセマンティクスを汚染する―`version`はフィルタやクエリ用語ではない。
- パラメータがキャッシュキーを変更するため、キャッシングが複雑になる。
- クライアントが含めるのを忘れやすく、意図しないバージョンのフォールバックにつながる。

**実装例 (Express.js)**

```javascript
app.get('/users', (req, res) => {
  const version = req.query.version || 1;
  switch(version) {
    case '1': return handleV1(req, res);
    case '2': return handleV2(req, res);
    default:  return res.status(400).json({ error: 'Invalid version' });
  }
});
```

### 3. ヘッダーバージョニング

バージョン情報はHTTPヘッダーで運ばれます。2つの一般的なアプローチ：

| アプローチ               | ヘッダー例                                   |
|------------------------|--------------------------------------------------|
| カスタムヘッダー          | `X-API-Version: 1`                               |
| Acceptヘッダー（ベンダーMIMEタイプ） | `Accept: application/vnd.myapi.v1+json` |

**利点**
- 最もRESTful ― URLはリソースを識別し、ヘッダーは表現を識別する。
- 決して変更されないクリーンなURI。
- 細かい制御：メディアタイプごとにバージョンを付けることができる（例：`v1` JSON、`v2` XML）。

**欠点**
- 発見可能性が低い ― ヘッダーを変更せずにブラウザやcurlでテストするのが難しい。
- ヘッダーに基づくルーティングのためにサーバー側で複雑さが生じる。
- 適切に`Vary`ヘッダーが設定されないとキャッシングが難しい。

**実装例 (ASP.NET Core with Accept Header)**

```csharp
// In Startup.cs
services.AddApiVersioning(options =>
{
    options.ApiVersionReader = new MediaTypeApiVersionReader();
    options.AssumeDefaultVersionWhenUnspecified = true;
});

// Controller
[ApiVersion("1.0")]
[Route("api/users")]
public class UsersV1Controller : ControllerBase {}
```

**実装例 (Spring Boot)**

```java
@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v1+json")
public class UserControllerV1 { ... }

@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v2+json")
public class UserControllerV2 { ... }
```

### 4. コード / スキーマバージョニング（明示的なバージョンなし）

しばしば「バージョンレス」または「契約ファースト」と呼ばれます。バージョン識別子を公開する代わりに、APIプロバイダーはフィールドまたはエンドポイントのみを追加することで後方互換性を維持します。破壊的変更はスキーマレジストリ（例：Protobuf、Avro）を通じて伝達されるか、新しいエンドポイント/操作を導入することで行われます。

```
// Protobuf package versioning
package myapi.v1;
message User {
  string name = 1;
}

// Later, in v2:
message User {
  string name = 1;
  string email = 2;
}
```

**利点**
- 複数のルーティングパスを維持する必要がない。
- 継続的な後方互換性を促進する。
- 内部マイクロサービスやイベント駆動型システムに適している。

**欠点**
- バージョンインジケーターなしでは意図的な破壊的変更を伝えられない。
- 後方互換性が意図せずに壊れた場合、メンテナンスの負担になる。

**最適な用途:**
- コンシューマーとプロバイダーが同じ組織内にいる内部マイクロサービス。
- `@deprecated`ディレクティブを使用したGraphQLスキーマ。
- スキーマレジストリを持つイベント駆動型システム（Confluent Schema Registry、AWS Glue）。

---

## 業界別のユースケース

| ユースケース | 推奨戦略 | 根拠 |
|----------|-------------------|-----------|
| **公開API（Stripe、Twilio）** | URIバージョニング | クライアントは明示的で安定した契約を必要とする。キャッシングが簡単。 |
| **モバイルバックエンド（Facebook、Twitter）** | ヘッダーバージョニング（カスタム） | アプリはコンパイル時のバージョンを送信。URLは決して変更されず、アプリアップデートの圧力を回避。 |
| **内部マイクロサービス** | バージョンレス / Protobuf | スキーマレジストリが互換性を強制。複数のエンドポイントバージョンを維持する必要なし。 |
| **イベント駆動型システム** | スキーマレジストリ（Avro/Protobuf） | データ契約は独立して進化。コンシューマーはスキーマIDに対して検証。 |

---

## インストールとセットアップ

バージョニングは**設計パターン**ですが、ルーティング、検証、ドキュメントを強制するためのツールが必要です。以下は一般的な環境向けのインストール手順です。

### ASP.NET Core

`Microsoft.AspNetCore.Mvc.Versioning` NuGetパッケージを追加して設定します：

```csharp
// Installation: dotnet add package Microsoft.AspNetCore.Mvc.Versioning
// In Startup.cs:
public void ConfigureServices(IServiceCollection services)
{
    services.AddControllers();
    services.AddApiVersioning(options =>
    {
        options.DefaultApiVersion = new ApiVersion(1, 0);
        options.AssumeDefaultVersionWhenUnspecified = true;
        options.ReportApiVersions = true;
    });
}
```

### Express.js

ライブラリは不要です。バージョンごとにルーターを作成し、マウントします：

```javascript
// Installation: npm i express (no extra lib needed)
const express = require('express');
const app = express();

const v1Router = require('./routes/v1');
const v2Router = require('./routes/v2');

app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

app.listen(3000);
```

### Spring Boot

Spring Bootは`@RequestMapping`を介してヘッダーバージョニングとURIバージョニングをネイティブにサポートしています。Acceptヘッダーバージョニングでは、異なる`produces`属性を持つ個別のコントローラーを定義できます。

```java
// POM dependency: spring-boot-starter-web (includes Spring MVC)
// For media type versioning, controllers produce different vendor MIME types:
@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v1+json")
public class UserControllerV1 { ... }
```

### API Gateways (Kong, AWS API Gateway)

アプリケーションコードの上流でルーティングルールを設定します：

- **Kong:** 特定のパス（`/v1/`、`/v2/`）を持つサービスとルートを定義します。バックエンドに転送する前にパスプレフィックスを削除することもできます。
- **AWS API Gateway:** `{proxy+}`のようなパスパラメータを持つステージまたはリソースを作成し、パスにバージョンを含めます。または、`version`ヘッダーを使用し、マッピングテンプレートでルーティングします。

```yaml
# Kong declarative config (YAML)
services:
  - name: users-api
    routes:
      - name: users-v1
        paths:
          - /v1/users
        strip_path: true
        service: users-api-v1-upstream
      - name: users-v2
        paths:
          - /v2/users
        strip_path: true
        service: users-api-v2-upstream
```

---

## ベストプラクティス

### 1. 一貫性を保つ

APIサーフェス領域ごとに1つの戦略を選択してください。エンドポイント間でURIバージョニングとヘッダーバージョニングを混在させると混乱を招きます。

### 2. 実装ではなく契約をバージョニングする

OpenAPI仕様（または同等のもの）を信頼できる唯一の情報源とすべきです。契約の変更には新しいバージョンが必要であり、内部コードの変更ではありません。

### 3. 後方互換性を優先する（ただし破壊的変更を恐れない）

可能な場合、既存のフィールドを削除または名前変更するのではなく、新しいフィールドを追加してください。仕様で`@deprecated`マーカーを使用します。ただし、破壊的変更が必要な場合もあります。バージョニングがセーフティネットです。

### 4. 明示的なライフサイクルヘッダーを使用する

バージョンが非推奨になった場合、RFCに着想を得た以下のヘッダーを返します：

- `Deprecation: Sat, 01 Jan 2025 00:00:00 GMT` – バージョンが非推奨であることを示します。
- `Sunset: Wed, 01 Jul 2026 00:00:00 GMT` – バージョンが削除される日時を示します。
- `Link: </v2/users>; rel="successor-version"` – 置き換え先を示します。

**レスポンスヘッダーの例：**

```http
HTTP/1.1 200 OK
Content-Type: application/json
Deprecation: true
Sunset: Wed, 01 Jul 2026 00:00:00 GMT
Link: </v2/users>; rel="successor-version"
```

### 5. API契約にセマンティックバージョニングを適用する

`MAJOR.MINOR.PATCH`セマンティクスを使用します：

- **Major:** 破壊的変更 → 新しいバージョン（例：`/v2/`）。
- **Minor:** 追加的で後方互換性のある変更（例：ボディの新しいフィールド、新しいエンドポイント）。
- **Patch:** 修正または機能改善を伴わない改良。

### 6. すべてを文書化する

OpenAPI仕様の`info.version`フィールドにバージョニング戦略を含め、バージョン間の移行ガイドを提供します。

```yaml
openapi: 3.0.0
info:
  title: My API
  version: 2.0.0
  description: |
    ## Versioning
    This API uses URI path versioning. All requests must include the version in the URL path, e.g., `/v2/users`.
    See the [migration guide](/docs/migration) for changes from v1 to v2.
```

### 7. サンセット施行を自動化する

APIゲートウェイまたはミドルウェアを使用して、期限切れ日以降に非推奨バージョンへの呼び出しを拒否します。最新バージョンへのリンクとともに`410 Gone`を返します。

---

## 非推奨化のライフサイクル

完全に管理されたバージョン付きAPIは以下の段階を経ます：

1. **アクティブ** – バージョンはデフォルトまたは明示的に呼び出し可能。
2. **非推奨** – バージョンはまだ動作するが`Deprecation`ヘッダーを返す。コンシューマーはドキュメントにバナーを表示すべき。
3. **サンセット** – バージョンは特定の日付に削除される。`Deprecation`と`Sunset`の両方のヘッダーを返す。
4. **削除済み** – エンドポイントは`410 Gone`（`404`ではない）を返す。`Sunset`日付が経過している。

**自動非推奨ヘッダーのミドルウェア例 (Express.js):**

```javascript
const deprecatedVersions = {
  v1: { deprecatedAt: new Date('2025-01-01'), sunsetAt: new Date('2026-07-01'), successor: '/v2/users' }
};

app.use((req, res, next) => {
  const match = req.path.match(/^\/v(\d+)/);
  if (match && deprecatedVersions[`v${match[1]}`]) {
    const info = deprecatedVersions[`v${match[1]}`];
    res.set('Deprecation', info.deprecatedAt.toUTCString());
    res.set('Sunset', info.sunsetAt.toUTCString());
    if (info.successor) {
      res.set('Link', `<${info.successor}>; rel="successor-version"`);
    }
  }
  next();
});
```

---

## 結論

APIバージョニングは、APIのすべてのコンシューマーに影響を与える戦略的な決定です。万能の戦略はありません。正しい選択は、コンシューマーベース、エコシステム、リスク許容度によって異なります。

| 戦略 | 選択するタイミング |
|----------|----------------|
| **URI / パス** | 公開API。発見可能性とキャッシングが最も重要。 |
| **クエリパラメータ** | 内部コンシューマーとの単純なユースケース。柔軟性が必要な場合。 |
| **ヘッダー（Accept / カスタム）** | モバイルアプリ、長期稼働クライアント、またはクリーンなURIが必要な場合。 |
| **バージョンレス / スキーマ** | 内部サービス、イベント駆動型アーキテクチャ、またはGraphQL。 |

戦略に関係なく、明確なドキュメント、ライフサイクルヘッダー、段階的な非推奨化に投資してください。適切にバージョニングされたAPIは信頼を構築し、プラットフォームが依存するエコシステムを壊すことなく進化することを可能にします。

> **参考資料**
> - [MicrosoftによるREST APIバージョニング](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design#versioning)
> - [OpenAPI仕様](https://spec.openapis.org/oas/latest.html)
> - [RFC 8594: Sunset Header](https://tools.ietf.org/html/rfc8594)
> - [API設計パターン – バージョニングの章](https://www.manning.com/books/api-design-patterns)
```