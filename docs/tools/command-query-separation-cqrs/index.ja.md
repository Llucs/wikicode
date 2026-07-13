---
title: コマンドとクエリの分離（CQRS）
description: ソフトウェアアーキテクチャでコマンド（書き込み操作）からクエリ（読み取り操作）を分離する設計パターンです。
created: 2026-07-13
tags:
  - ソフトウェアアーキテクチャ
  - デザインパターン
  - CQRS
  - コマンドとクエリの分離
status: 草稿
---

# コマンドとクエリの分離（CQRS）

コマンドとクエリの分離（CQRS）は、ソフトウェアアーキテクチャでコマンド（書き込み操作）からクエリ（読み取り操作）を分離する設計パターンです。この分離は、特に高なトランザクション量を持つ複雑なシステムや複雑なビジネスロジックを持つシステムにおいて、より Maintainable でスケーラブルなアプリケーションを作成するのに役立ちます。

## 什么是 CQRS

CQRSは、情報（クエリ）を求めることと、状態を変更すること（コマンド）を分離することを強調する設計パターンです。この分離は、特に高いトランザクション量を持つシステムや複雑なビジネスロジックを持つシステムにおいて、より Maintainable でスケーラブルなアプリケーションを作成するのに役立ちます。

## 主要特性

1. **コマンドの処理**: コマンドはシステムの状態を変更するために使用されます。これらは外部システムやユーザーによって発行され、データの作成、更新、削除などのアクションを実行するために使用されます。
2. **クエリの処理**: クエリはシステムから情報を取得するために使用されます。これらは読み取り専用の操作であり、システムの状態を変更しません。クエリは読み込み-heavy のワークロードを最適化できるため、单一データストアが読み込みと書き込みを両方処理するよりも効率的です。
3. **責任の分離**: CQRSは、書き込みと読み取り操作の責任を分離することで、システムをより Maintainable でスケーラブルにします。
4. **イベントソーシング**: エベントソーシングは CQRS と組み合わせてよく使用され、システムの変更はイベントのシーケンスとして記録されます。これらのイベントは、システムの現在の状態を再構築するために使用されるか、またはコマンドをトリガーするために使用されます。

## 历史

CQRSが普及したのは新しいアイデアではありません。コマンドとクエリを分離する概念は、長い間存在していましたが、2010年代前半に Greg Young と Udi Dahan によって推奨されたことにより、広く適用されるようになりました。彼らはこのアイデアを Various コンファレンスとワークショップで提示し、パターンの更なる採用を促進しました。

## 使用例

1. **オンライン取引処理（OLTP）**: 高い書き込み Throughput を必要とするシステム、例えば E-コマースプラットフォーム、金融システム、またはゲームアプリケーションなど、CQRSは特に有用です。
2. **データウェアハウジング**: CQRSは、書き込み-heavy の取引データと読み込み-heavy の分析データを分離することで、データウェアハウジングを構築するのに役立ちます。
3. **複雑なビジネスロジック**: 常に更新と変更を求められる複雑なビジネスロジックを備えたシステムは、コマンドとクエリの分離から大きく恩恵を受けることができます。

## インストール

CQRSは独自のフレームワークではなく、設計パターンです。そのため、直接インストールするものではありません。ただし、以下の一般的な手順に従って CQRS をアプリケーションに実装することができます。

1. **コマンドとクエリの定義**: 書き込み操作を処理するコマンドクラスと読み込み操作を処理するクエリクラスを作成します。
2. **コマンドハンドラの実装**: コマンドを処理するハンドラを書き、データに必要な操作を実行します。
3. **クエリハンドラの実装**: クエリを処理するハンドラを書き、必要なデータを返します。
4. **イベントソーシング（オプション）**: システムの変更をイベントのシーケンスとしてキャプチャし、これらのイベントを使用して読み取りモデルを更新します。

## 基本的な使用方法

### コマンドの処理

```csharp
public class OrderService {
    private readonly CommandBus _commandBus;

    public OrderService(CommandBus commandBus) {
        _commandBus = commandBus;
    }

    public void PlaceOrder(Order order) {
        _commandBus.Send(new PlaceOrderCommand(order));
    }
}
```

### クエリの処理

```csharp
public class OrderQueryService {
    private readonly QueryBus _queryBus;

    public OrderQueryService(QueryBus queryBus) {
        _queryBus = queryBus;
    }

    public Order GetOrderById(Guid orderId) {
        return _queryBus.Send(new GetOrderByIdQuery(orderId));
    }
}
```

### イベントソーシング

```csharp
public class OrderAggregate {
    private readonly IEventRepository _eventRepository;

    public OrderAggregate(IEventRepository eventRepository) {
        _eventRepository = eventRepository;
    }

    public void ApplyCommand(PlaceOrderCommand command) {
        // コマンドを適用し、イベントを保存
        _eventRepository.Save(new OrderPlacedEvent(command.Order.Id, command.Order.CustomerId));
    }
}
```

## 結論

CQRSは、複雑なアプリケーションのスケーラビリティとメンテナビリティを大幅に向上させる強力な設計パターンです。コマンドとクエリを分離することにより、システムを読み込みと書き込み操作の両方を最適化することができ、より効率的で堅牢なアプリケーションを作成します。ただし、効果的な実装には慎重な設計と実装が必要であり、すべての種類のアプリケーションには適さない場合もあります。