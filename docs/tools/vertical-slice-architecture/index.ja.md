---
title: 垂直スライスアーキテクチャ
description: ビジネス機能に基づいてコードを整理し、凝集性と保守性を向上させるソフトウェア設計アプローチです。
created: 2026-06-18
tags:
  - architecture
  - cqrs
  - feature-organization
  - dotnet
  - best-practices
status: draft
---

# Vertical Slice Architecture

## 垂直スライスアーキテクチャとは？

Vertical Slice Architecture（VSA）は、水平方向の技術レイヤー（Controllers、Services、Repositories、Data Access）ではなく、**ビジネス機能**や**ユースケース**を中心にアプリケーションを構成するソフトウェア設計パターンです。各「垂直スライス」は、単一の機能を提供するために必要なすべての関心事（HTTPエンドポイントやメッセージハンドラからデータベースの永続化まで）を、凝集性が高く自己完結した単位として捉えます。

> 「このスタイルでは、アーキテクチャは個別のリクエストを中心に構築され、フロントエンドからバックエンドまでのすべての関心事をカプセル化してグループ化します。通常のn層アーキテクチャやヘキサゴナルアーキテクチャなどから、それらのレイヤー間のゲートや障壁を取り除き、結合します…」— Jimmy Bogard

VSAは、従来のレイヤードアーキテクチャやクリーンアーキテクチャが持つ偶発的な複雑さ（単純な機能追加でさえ無関係なフォルダに散らばった多くのファイルを変更する必要がある）への対応として、Jimmy Bogard（MediatRの作成者）によって**2016年**頃に普及しました。

## なぜ使うのか？

- **機能の凝集性** — ユースケースのすべてのコードが一箇所にあります。開発者はプロジェクトやフォルダを行き来することなく、機能全体を理解し変更できます。
- **疎結合** — スライスは独立しており、明確に定義された*共有カーネル*（ドメインエンティティ、基本インフラストラクチャ、ドメインイベント）を介してのみ相互作用します。あるスライスの変更が他のスライスに影響を与えることはほとんどありません。
- **開発者体験の簡素化** — ナビゲーションが簡単です。機能フォルダを見つければ、そのすべてのファイルがそこにあります。
- **CQRSとの親和性** — コマンドとクエリが個々のスライスに自然にマッピングされ、読み取りと書き込みの明確な分離を促進します。
- **チームの自律性** — チームがスライス全体を所有できるため、マージコンフリクトが減り、並行開発が可能になります。
- **リファクタリングのしやすさ** — 境界がビジネス機能と一致するため、ある機能の再構築が他の機能に与える影響は最小限です。

## レイヤードアーキテクチャとの違い

| 観点 | レイヤードアーキテクチャ | 垂直スライスアーキテクチャ |
|--------|---------------------|---------------------------|
| 構成単位 | 技術レイヤー（Controllers、Services、Repositories）ごと | ビジネス機能ごと（例：`CreateOrder`、`ShipOrder`） |
| 凝集性 | 低い – 機能のコードがレイヤー全体に散らばる | 高い – すべての機能コードがまとまっている |
| 結合度 | レイヤーが互いに依存 | スライスは共有カーネルにのみ依存 |
| 変更の影響 | 単純な変更でも多くのレイヤーのファイルを変更する必要がある | 変更は一つのフォルダ内に収まる |
| 学習曲線 | ほとんどの開発者にとって馴染みがある | CQRSとメディエーターパターンの理解が必要 |

## 主要概念

### 機能フォルダ / スライス
各スライスは、ユースケースが必要とするすべてを含むディレクトリです。典型的なスライスは以下のようになります：

```
Features/
  Orders/
    CreateOrder/
      CreateOrderCommand.cs       # 入力コントラクト（不変）
      CreateOrderHandler.cs       # ビジネスロジック + オーケストレーション
      CreateOrderValidator.cs     # 入力検証
      CreateOrderEndpoint.cs      # APIエンドポイント（Minimal API、Controllerなど）
```

スライスの外部からこれらのファイルを参照することは、メディエーターインターフェース（例：`IRequest<OrderDto>`）を介する場合を除いてありません。

### 共有カーネル
共通のドメインロジック、基本エンティティ、値オブジェクト、インフラストラクチャ（DbContext、ロギング、認証など）は、`Shared`や`Core`プロジェクトとしてスライスの外部に置かれます。スライスは共有カーネルからインポートしますが、互いにインポートすることはありません。

### CQRS（コマンドクエリ責務分離）
VSAは自然にCQRSを採用します。各スライスは1つのコマンド（書き込み操作）または1つのクエリ（読み取り操作）のみを処理し、システムの意図を明確にします。

### メディエーターパターン
インプロセスメディエーターがリクエストの送信元とハンドラを分離します。**MediatR**や**Brighter**などのライブラリが、コマンド/クエリのディスパッチや横断的関心事（検証、ロギング、トランザクション）の適用に一般的に使用されます。

## 垂直スライスアーキテクチャを使用すべき場合

- **複雑なビジネスドメイン** – 金融、物流、ヘルスケア、ERPなど、多くの異なるワークフローを持つドメイン。
- **大規模な開発チーム** – 機能を異なる開発者やチームに最小限の調整で割り当てられる。
- **モジュラーモノリス** – 単一デプロイメント内で強力なモジュール境界を設けたい場合。
- **マイクロサービス** – 各マイクロサービスを単一のスライスとして定義するか、VSAで内部構造を整理する。
- **レガシー移行** – 古いレイヤーをスライス単位で段階的に置き換える。

## インストール（サポートライブラリ）

VSAはアーキテクチャパターンであり、ライブラリではありません。ただし、.NETで実装する際はほぼ常にMediatRなどのツールが使用されます。

### .NET（C#） – MediatR & FluentValidation のセットアップ

```bash
# 新しいプロジェクトを作成
dotnet new webapi -n MyApp

# パッケージを追加
dotnet add package MediatR
dotnet add package MediatR.Extensions.Microsoft.DependencyInjection  # 自動登録用（最新版でない場合）
dotnet add package FluentValidation
dotnet add package FluentValidation.DependencyInjectionExtensions
```

## 実装例（C# + MediatR）

`PlaceOrder`機能をエンドツーエンドで構築します。

### 1. コントラクト – コマンド（入力）

```csharp
// Features/Orders/PlaceOrder/PlaceOrderCommand.cs
using MediatR;

public record PlaceOrderCommand(int CustomerId, List<CartItem> Items) : IRequest<OrderDto>;
```

### 2. ハンドラ – ビジネスロジック + データアクセス

```csharp
// Features/Orders/PlaceOrder/PlaceOrderHandler.cs
using MediatR;
using Microsoft.EntityFrameworkCore;

public class PlaceOrderHandler : IRequestHandler<PlaceOrderCommand, OrderDto>
{
    private readonly AppDbContext _db;

    public PlaceOrderHandler(AppDbContext db) => _db = db;

    public async Task<OrderDto> Handle(PlaceOrderCommand request, CancellationToken cancellationToken)
    {
        // 1. 顧客を読み込む
        var customer = await _db.Customers
            .Include(c => c.Cart)
            .FirstOrDefaultAsync(c => c.Id == request.CustomerId, cancellationToken)
            ?? throw new NotFoundException("Customer not found");

        // 2. ドメインロジック – 注文を作成
        var order = new Order(customer);
        // ... 価格計算、検証など

        _db.Orders.Add(order);
        await _db.SaveChangesAsync(cancellationToken);

        return new OrderDto(order.Id, order.Total);
    }
}
```

### 3. 検証（FluentValidation）

```csharp
// Features/Orders/PlaceOrder/PlaceOrderValidator.cs
using FluentValidation;

public class PlaceOrderValidator : AbstractValidator<PlaceOrderCommand>
{
    public PlaceOrderValidator()
    {
        RuleFor(x => x.CustomerId).GreaterThan(0);
        RuleFor(x => x.Items).NotEmpty();
        RuleForEach(x => x.Items).ChildRules(item =>
        {
            item.RuleFor(i => i.Quantity).GreaterThan(0);
        });
    }
}
```

### 4. エンドポイント – Minimal API

```csharp
// Features/Orders/PlaceOrder/PlaceOrderEndpoint.cs
public static class PlaceOrderEndpoint
{
    public static void MapPlaceOrder(this WebApplication app)
    {
        app.MapPost("/orders", async (IMediator mediator, PlaceOrderCommand command, IValidator<PlaceOrderCommand> validator) =>
        {
            var validationResult = await validator.ValidateAsync(command);
            if (!validationResult.IsValid)
                return Results.ValidationProblem(validationResult.ToDictionary());

            var result = await mediator.Send(command);
            return Results.Ok(result);
        });
    }
}
```

### 5. 登録と配線（コンポジションルート）

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// MediatRの登録（アセンブリをスキャンしてハンドラを登録）
builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(typeof(Program).Assembly));
builder.Services.AddValidatorsFromAssembly(typeof(Program).Assembly);

// DbContextなどの登録
builder.Services.AddDbContext<AppDbContext>(...);

var app = builder.Build();

// 各スライスのエンドポイントをマッピング
app.MapPlaceOrder();

app.Run();
```

### ディレクトリ構成（簡略版）

```
MyApp/
  Features/
    Orders/
      PlaceOrder/
        PlaceOrderCommand.cs
        PlaceOrderHandler.cs
        PlaceOrderValidator.cs
        PlaceOrderEndpoint.cs
      GetOrderHistory/
        GetOrderHistoryQuery.cs
        GetOrderHistoryHandler.cs
        GetOrderHistoryEndpoint.cs
    Products/
      CreateProduct/
        ...
  Shared/
    Entities/
      Customer.cs
      Order.cs
    Exceptions/
      NotFoundException.cs
  Data/
    AppDbContext.cs
  Program.cs
```

## 主な機能とコマンド例（MediatR）

### コントローラーまたはMinimal APIからのコマンドディスパッチ

```csharp
[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    private readonly IMediator _mediator;

    public OrdersController(IMediator mediator) => _mediator = mediator;

    [HttpPost]
    public async Task<IActionResult> PlaceOrder([FromBody] PlaceOrderCommand command)
    {
        var orderId = await _mediator.Send(command);
        return Ok(orderId);
    }
}
```

### カスタムパイプラインビヘイビア（横断的関心事）

MediatRは、ロギング、検証、トランザクションなどのためのパイプラインビヘイビアをサポートしています。

```csharp
// Shared/Behaviors/ValidationBehavior.cs
public class ValidationBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;

    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators) => _validators = validators;

    public async Task<TResponse> Handle(TRequest request, RequestHandlerDelegate<TResponse> next, CancellationToken cancellationToken)
    {
        if (_validators.Any())
        {
            var context = new ValidationContext<TRequest>(request);
            var failures = _validators
                .Select(v => v.Validate(context))
                .SelectMany(result => result.Errors)
                .Where(f => f != null)
                .ToList();

            if (failures.Any())
                throw new ValidationException(failures);
        }

        return await next();
    }
}
```

### クエリのディスパッチ

```csharp
// GetOrderHistoryQuery.cs
public record GetOrderHistoryQuery(int CustomerId, int Page = 1, int PageSize = 20) : IRequest<PagedResult<OrderDto>>;

// ハンドラはDbContextを直接使用
public class GetOrderHistoryHandler : IRequestHandler<GetOrderHistoryQuery, PagedResult<OrderDto>>
{
    private readonly AppDbContext _db;

    public GetOrderHistoryHandler(AppDbContext db) => _db = db;

    public async Task<PagedResult<OrderDto>> Handle(GetOrderHistoryQuery request, CancellationToken ct)
    {
        var query = _db.Orders.Where(o => o.CustomerId == request.CustomerId);
        var total = await query.CountAsync(ct);
        var items = await query
            .OrderByDescending(o => o.CreatedAt)
            .Skip((request.Page - 1) * request.PageSize)
            .Take(request.PageSize)
            .Select(o => new OrderDto(o.Id, o.Total, o.Status))
            .ToListAsync(ct);

        return new PagedResult<OrderDto>(items, total, request.Page, request.PageSize);
    }
}
```

## ベストプラクティス

- **共有カーネルを定義する** – エンティティ、値オブジェクト、基本クラス、共通インフラストラクチャを中央の場所に配置し、すべてのスライスが参照できるようにします。スライス同士が依存し合わないようにしてください。
- **スライスを薄く保つ** – 各スライスには、そのユースケースのロジックのみを含めるべきです。ロジックが複数のスライスで再利用される場合は、スライスではなくドメインサービスや共有ヘルパーに抽出します。
- **スライス間の通信にはドメインイベントを使用する** – あるスライスが別のスライスのアクションに反応する必要がある場合、ハンドラからドメインイベントを発行し、そのイベントをリッスンする別のハンドラ（別のスライスにあっても構いません）を定義します。
- **時期尚早な抽象化よりも重複を受け入れる** – 2つのスライスに似ているが微妙に異なるコードがあっても構いません。本当に同一で安定している場合にのみ、共通ロジックを抽出します。
- **検証を標準化する** – FluentValidationのようなライブラリとパイプラインビヘイビアを使用して、すべてのコマンドを自動的に検証します。
- **スライス構造が貧弱にならないようにする** – ハンドラには実際のビジネスロジックを含めるようにし、単に外部サービスに委譲するだけにしないでください。ハンドラこそが機能のオーケストレーションが存在する場所です。
- **スライスのコントラクトを文書化する** – コマンド/クエリレコードはスライスのAPIです。不変に保ち、その意図が明確になるようにします。

## 欠点と考慮点

- **重複のリスク** – 規律がなければ、同じ検証やロジックが複数のスライスで繰り返される可能性があります。共有カーネルとドメインサービスが役立ちますが、ある程度の重複は許容されます。
- **学習曲線** – CQRS、メディエーター、VSAに新しいチームは適応に時間が必要です。
- **ツールのオーバーヘッド** – MediatRとその類似ライブラリは間接層を導入します（ただし、インプロセスメディエーターのコストは低いです）。
- **単純なCRUDアプリケーションには不向き** – ビジネスロジックが最小限のアプリケーションでは、スライス化のオーバーヘッドによる恩恵が得られない可能性があります。

## 結論

垂直スライスアーキテクチャは、複雑なビジネスアプリケーションにおいて、従来のレイヤードアーキテクチャに代わる実用的で保守性の高い選択肢を提供します。コードを技術レイヤーではなく機能単位で整理することで、凝集性が向上し、ナビゲーションが簡素化され、ビジネス要件の変化に応じてシステムを進化させやすくなります。CQRSとメディエーターライブラリを組み合わせることで、VSAはコードベースの規模とチーム規模の両方にうまくスケールする、クリーンで自己文書化された構造を提供します。

小さく始めましょう。1つの機能を選び、それをスライスして、その違いを体験してください。凝集性と独立性を実感すれば、なぜこれまでレイヤー間の散在に耐えていたのか不思議に思うでしょう。

---

### 参考資料

- [Jimmy Bogard – Vertical Slice Architecture（ビデオ）](https://www.youtube.com/watch?v=5kOzZz2vj4A)
- [Jimmy Bogard – From Inception to Production（トーク）](https://www.youtube.com/watch?v=Lx9fBkz_0QQ)
- [垂直スライスアーキテクチャ – Microsoft Docs](https://learn.microsoft.com/ja-jp/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures#vertical-slice-architecture)
- [MediatR GitHub](https://github.com/jbogard/MediatR)