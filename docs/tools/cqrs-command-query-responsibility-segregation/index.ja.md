---
title: CQRS（コマンドクエリ責務分離）
description: 読み取り操作と書き込み操作を別々のモデルに分離することで、パフォーマンス、スケーラビリティ、保守性を最適化するアーキテクチャパターンです。
created: 2026-06-19
tags:
  - architecture
  - design-pattern
  - cqrs
  - domain-driven-design
  - event-sourcing
  - microservices
status: draft
---

CQRS (Command Query Responsibility Segregation) は、データの読み取り（クエリ）と更新（コマンド）の責務を分離するアーキテクチャパターンです。読み取り用と書き込み用に異なるモデル、多くの場合は別々のデータストアを使用することで、各側面を独立して最適化でき、複雑なシステムにおけるスケーラビリティ、パフォーマンス、セキュリティを向上させます。

## 概要と歴史

CQRS という用語は、2000年代後半に Greg Young と Udi Dahan によって Domain-Driven Design (DDD) コミュニティ内で広められました。その概念的な基盤は、Bertrand Meyer の **Command-Query Separation (CQS)** 原則にあります。この原則は、メソッドは *コマンド*（アクションを実行する）か *クエリ*（データを返す）のいずれかであるべきで、両方であってはならないと述べています。CQRS はこのアイデアをメソッドレベルからアーキテクチャおよびデータストアレベルに引き上げます。

従来の CRUD アーキテクチャでは、単一のモデルが読み取り、書き込み、更新、削除を処理します。CQRS はこれを明示的に2つの異なる側面に分割します。

- **書き込み側（コマンド）：** 状態変更操作を扱います。コマンドは命令的であり、副作用を生じさせ、ビジネス不変条件を強制します（通常 DDD の集約を通じて）。
- **読み取り側（クエリ）：** データ取得を扱います。クエリは宣言的であり、副作用がなく、特定の UI や API 契約に合わせて最適化されます。しばしば非正規化、事前結合され、異なるデータベース（例：検索には Elasticsearch、キャッシュには Redis）に保存されます。

CQRS はしばしば **イベントソーシング** と組み合わされ、書き込み側がドメインイベントのストリームを生成し、それを非同期に消費して読み取りモデルを構築・更新します。

## CQRS を使用する理由

| 利点 | 説明 |
|------------------|-------------|
| **スケーラビリティ** | 読み取りレプリカは書き込みノードから独立してスケーリング可能。異なるインフラ（例：読み取りキャッシュ、書き込みキュー）を必要に応じて適用可能。 |
| **パフォーマンス** | 読み取りモデルは特定のクエリに事前最適化可能（非正規化、インデックス化）。書き込みモデルは読み取りのオーバーヘッドなしにトランザクションの一貫性に集中。 |
| **セキュリティ** | モデルを分離することで、異なるアクセス制御が可能。通常、コマンドはより高い権限を必要とし、クエリはより広範な権限で運用可能。 |
| **複雑性の管理** | 複雑なドメインロジックを書き込み側に隔離し、単純な読み取り操作にそのロジックが漏れ込むのを防止。 |
| **柔軟性** | 同じ書き込みモデルから、モバイル、ウェブ、分析など異なるビューに対応した複数の読み取りモデルを提供可能。 |

## 使用すべき場合（および避けるべき場合）

### CQRS を使用すべき場合

- 共有データへの高い競合（例：予約、物流、取引システム）。
- システムの一部で書き込みトランザクションをブロックしてはならない大量の読み取り負荷が発生する場合。
- 同じデータに対して異なるコンシューマーが異なる表現を必要とする場合。
- 完全な監査証跡とイベントリプレイが必要な場合（通常はイベントソーシングと組み合わせて）。

### CQRS を避けるべき場合

- システムが単純な CRUD でロジックが最小限の場合。
- 強い結果整合性がほとんどの操作で許容できない場合。
- チームが小さく、結果整合性やメッセージングパターンに精通していない場合。
- 複数のモデルを維持するコストがメリットを上回る場合。

## インストール / フレームワーク

CQRS はパターンであり、ライブラリではありません。「インストール」とは、コマンドをディスパッチし、イベント処理を管理し、読み取りプロジェクションを維持するためのインフラストラクチャ層を選択することを意味します。代表的なフレームワークは以下の通りです。

- **Axon Framework (Java/Kotlin):** コマンド/イベント/クエリバス、集約管理、イベントソーシングを標準で備えたフル機能のフレームワーク。
- **MediatR (C#/F#):** .NET 向けの軽量インプロセスメディエーターで、完全なメッセージングインフラなしでモノリス内に CQRS を実装するのに最適。
- **EventStoreDB (EventStore):** CQRS およびイベントソーシングと自然に組み合わせられる専用イベントストア。
- **Marten (.NET):** PostgreSQL 上のドキュメント DB / イベントストアで、組み込みのプロジェクションサポートを提供。
- **Dapr (Multi-language):** 分散 CQRS システムに構成可能な pub/sub、ステート管理、アクタービルディングブロックを提供。
- **Lagom (Java/Scala):** リアクティブマイクロサービスを構築するためのフレームワークで、主要パターンとしてコマンド/クエリ分離を含む。

## 使用例（概念的な C# / MediatR）

### 書き込み側 – コマンド

```csharp
// Command definition
public record PlaceOrderCommand(Guid UserId, List<OrderItem> Items);

// Command handler
public class PlaceOrderHandler : IRequestHandler<PlaceOrderCommand, Guid>
{
    private readonly IOrderRepository _writeRepo;

    public PlaceOrderHandler(IOrderRepository writeRepo)
    {
        _writeRepo = writeRepo;
    }

    public async Task<Guid> Handle(PlaceOrderCommand command, CancellationToken ct)
    {
        // 1. Validate business rules (e.g., check stock, user credit)
        // 2. Create Order Aggregate, enforce invariants
        var aggregate = Order.Create(command.UserId, command.Items);
        // 3. Persist events / state to Write Store
        await _writeRepo.Save(aggregate);
        // 4. Return result (events will be published to update read side)
        return aggregate.Id;
    }
}

// Domain event emitted by the aggregate (for event sourcing or outbox pattern)
public record OrderPlaced(
    Guid OrderId,
    Guid UserId,
    List<OrderItem> Items,
    decimal Total,
    DateTime PlacedAt
);
```

### 読み取り側 – クエリ

```csharp
// Query definition
public record GetOrderSummaryQuery(Guid OrderId);

// Query handler (reads from a separate, denormalized database)
public class GetOrderSummaryHandler : IRequestHandler<GetOrderSummaryQuery, OrderSummaryDto>
{
    private readonly IDbConnection _readDb;

    public GetOrderSummaryHandler(IDbConnection readDb)
    {
        _readDb = readDb;
    }

    public async Task<OrderSummaryDto> Handle(GetOrderSummaryQuery query, CancellationToken ct)
    {
        await _readDb.QuerySingleAsync<OrderSummaryDto>(
            "SELECT * FROM ReadModel_OrderSummaries WHERE Id = @Id",
            new { query.OrderId });
    }
}
```

### プロジェクター – 読み取りモデルの更新維持

```csharp
public class OrderProjector : IEventHandler<OrderPlaced>
{
    private readonly IDbConnection _readDb;

    public OrderProjector(IDbConnection readDb)
    {
        _readDb = readDb;
    }

    public async Task Handle(OrderPlaced @event)
    {
        // Denormalize the event data into a read-optimized table
        await _readDb.ExecuteAsync(@"
            INSERT INTO ReadModel_OrderSummaries (Id, UserId, Total, Status, PlacedAt)
            VALUES (@OrderId, @UserId, @Total, 'Pending', @PlacedAt)",
            @event);
    }
}
```

## 主な機能

- **関心の分離:** コマンドとクエリは独立して開発、テスト、デプロイ可能。
- **結果整合性:** 書き込み側はイベントを発行し、読み取りモデルは非同期に更新される。これは主要なトレードオフであるが、高いスループットを可能にする。
- **最適化されたストレージ:** 各側面で独自のデータストア技術を使用可能（例：書き込み：RDBMS、読み取り：Elasticsearch、Redis、マテリアライズドビュー）。
- **監査とリプレイ（イベントソーシングと組み合わせて）:** 完全なイベントストリームが過去の任意の状態を再構築し、デバッグやプロジェクションの再構築をサポート。
- **独立したスケーリング:** 書き込みノードと読み取りレプリカは、それぞれの負荷に基づいて水平方向にスケーリング可能。

## 主なトレードオフと落とし穴

- **結果整合性:** プロジェクションが完了するまで、ユーザーは古いデータを目にする可能性がある。対策としては、古いデータの警告、冪等性、または重要なパスでの即時整合性などがある。
- **N+1 読み取りモデル問題:** 各プロジェクションを維持する必要がある。UI の変更が頻繁だと保守のオーバーヘッドが増加する。
- **ロジックの重複:** ビジネスルールは **書き込み側のみ** に存在させるべき。読み取り側はドメインロジックを含んではならない。
- **インフラの複雑さ:** 信頼性の高いメッセージ処理（キュー、イベントバス、アウトボックスパターン）と障害シナリオの監視が必要。
- **学習曲線:** チームは結果整合性、イベント駆動アーキテクチャ、そして多くの場合イベントソーシングの理解が必要。

## まとめ

CQRS は、読み取りと書き込みのワークロードが明らかに異なるパフォーマンス、スケーラビリティ、またはセキュリティ要件を持つシステムにとって強力なパターンです。銀の弾丸ではなく、特にイベントソーシングと組み合わせるとかなりの複雑さをもたらします。適切に適用された場合（通常は複雑なビジネスルールや大量の読み取り負荷を伴う高度な連携を必要とするドメイン）、CQRS は保守性、パフォーマンス、スケーラビリティを劇的に向上させることができます。