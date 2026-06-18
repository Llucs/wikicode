---
title: 垂直切片架构
description: 一种按业务特性而非技术层组织代码的软件设计方法，提高内聚性和可维护性。
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

## 什么是 Vertical Slice Architecture？

Vertical Slice Architecture (VSA) 是一种软件设计模式，它将应用程序结构围绕**业务特性**或**用例**组织，而不是水平的技术层（Controllers、Services、Repositories、Data Access）。每个“垂直切片”捕获交付单个特性所需的所有关注点——从 HTTP 端点或消息处理器一直到数据库持久化——作为一个内聚、自包含的单元。

> “在这种风格中，我的架构围绕不同的请求构建，封装并分组从前端到后端的所有关注点。你使用一个普通的‘n 层’或六边形/任何架构，移除这些层之间的门和障碍，并耦合……” — Jimmy Bogard

VSA 大约在 **2016 年**由 Jimmy Bogard（MediatR 的创建者）推广，作为对传统分层架构或整洁架构中意外复杂性的回应，在这些架构中，即使添加一个简单特性也需要触及许多分散在不相关文件夹中的文件。

## 为什么使用它？

- **特性内聚** — 一个用例的所有代码位于同一处。开发者无需在不同项目或文件夹之间跳转即可理解和修改整个特性。
- **松散耦合** — 切片相互独立；它们仅通过定义良好的*共享内核*（领域实体、基础基础设施、领域事件）进行交互。一个切片的变更很少会破坏其他切片。
- **简化的开发者体验** — 导航变得简单：找到特性文件夹，所有文件都在那里。
- **CQRS 对齐** — 命令和查询自然而然地映射到各个切片，鼓励清晰的读写分离。
- **团队自主权** — 团队可以拥有整个切片，减少合并冲突并允许并行开发。
- **重构友好** — 因为边界与业务能力匹配，重构一个特性的影响很小。

## 它与分层架构有何不同

| 方面 | 分层架构 | Vertical Slice Architecture |
|--------|---------------------|---------------------------|
| 组织方式 | 按技术层（Controllers、Services、Repositories） | 按业务特性（例如 `CreateOrder`、`ShipOrder`） |
| 内聚性 | 低——一个特性的代码分散在各个层 | 高——所有特性代码在一起 |
| 耦合性 | 层之间相互依赖 | 切片仅依赖共享内核 |
| 变更影响 | 一个简单变更触及多个层的许多文件 | 变更包含在一个文件夹内 |
| 学习曲线 | 大多数开发者熟悉 | 需要理解 CQRS 和中介者模式 |

## 关键概念

### 特性文件夹 / 切片
每个切片是一个目录，包含用例所需的一切。一个典型切片可能包括：

```
Features/
  Orders/
    CreateOrder/
      CreateOrderCommand.cs       # 输入契约（不可变）
      CreateOrderHandler.cs       # 业务逻辑 + 编排
      CreateOrderValidator.cs     # 输入验证
      CreateOrderEndpoint.cs      # API 端点（Minimal API、Controller 等）
```

外部没有任何东西引用这些文件，除非通过中介者接口（例如 `IRequest<OrderDto>`）。

### 共享内核
公共领域逻辑、基础实体、值对象和基础设施（DbContext、日志、身份验证）位于 `Shared` 或 `Core` 项目中的切片之外。切片从共享内核导入，但从不相互导入。

### CQRS（命令查询职责分离）
VSA 自然采用 CQRS。每个切片精确处理一个命令（写入操作）或一个查询（读取操作），使系统的意图清晰。

### 中介者模式
进程内中介者将请求的发送者与处理者解耦。像 **MediatR** 或 **Brighter** 这样的库通常用于分派命令/查询以及应用横切关注点（验证、日志、事务）。

## 何时使用 Vertical Slice Architecture

- **复杂的业务领域** – 金融、物流、医疗、ERP——具有许多不同工作流的领域。
- **大型开发团队** – 可以将特性分配给不同的开发者或团队，只需最小协调。
- **模块化单体** – 希望在单个部署中拥有强模块边界。
- **微服务** – 每个微服务可以是一个切片，或者 VSA 可以组织其内部结构。
- **遗留系统迁移** – 一次一个特性地切片，增量替换旧层。

## 安装（支持库）

VSA 是一种架构模式，而不是一个库。然而，像 MediatR 这样的工具几乎总是在 .NET 中实现它。

### .NET (C#) – MediatR & FluentValidation 设置

```bash
# 创建一个新项目
dotnet new webapi -n MyApp

# 添加包
dotnet add package MediatR
dotnet add package MediatR.Extensions.Microsoft.DependencyInjection  # 用于自动注册（如果未使用最新版本）
dotnet add package FluentValidation
dotnet add package FluentValidation.DependencyInjectionExtensions
```

## 实现示例（C# 配合 MediatR）

我们来构建一个端到端的 `PlaceOrder` 特性。

### 1. 契约 – 命令（输入）

```csharp
// Features/Orders/PlaceOrder/PlaceOrderCommand.cs
using MediatR;

public record PlaceOrderCommand(int CustomerId, List<CartItem> Items) : IRequest<OrderDto>;
```

### 2. 处理程序 – 业务逻辑 + 数据访问

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
        // 1. 加载客户
        var customer = await _db.Customers
            .Include(c => c.Cart)
            .FirstOrDefaultAsync(c => c.Id == request.CustomerId, cancellationToken)
            ?? throw new NotFoundException("Customer not found");

        // 2. 领域逻辑 – 创建订单
        var order = new Order(customer);
        // ... 定价、验证等

        _db.Orders.Add(order);
        await _db.SaveChangesAsync(cancellationToken);

        return new OrderDto(order.Id, order.Total);
    }
}
```

### 3. 验证（FluentValidation）

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

### 4. 端点 – Minimal API

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

### 5. 注册与连线（组合根）

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// 注册 MediatR（扫描程序集以查找处理程序）
builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(typeof(Program).Assembly));
builder.Services.AddValidatorsFromAssembly(typeof(Program).Assembly);

// 注册 DbContext 等
builder.Services.AddDbContext<AppDbContext>(...);

var app = builder.Build();

// 映射每个切片的端点
app.MapPlaceOrder();

app.Run();
```

### 目录树（简化）

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

## 关键特性及命令示例（MediatR）

### 从 Controller 或 Minimal API 分派命令

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

### 自定义管道行为（横切关注点）

MediatR 支持用于日志、验证、事务等的管道行为。

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

### 分派查询

```csharp
// GetOrderHistoryQuery.cs
public record GetOrderHistoryQuery(int CustomerId, int Page = 1, int PageSize = 20) : IRequest<PagedResult<OrderDto>>;

// 处理程序直接使用 DbContext
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

## 最佳实践

- **定义共享内核** – 将实体、值对象、基类和公共基础设施放在一个中央位置，每个切片都可以引用。**不要**让切片相互依赖。
- **保持切片精简** – 每个切片应只包含其用例的确切逻辑。如果逻辑在切片间复用，将其提取到领域服务或共享帮助类中，而不是放入切片。
- **使用领域事件进行跨切片通信** – 当一个切片需要对另一个切片的操作做出反应时，从处理程序中发布领域事件，并定义一个单独的处理程序（即使位于其他切片中）来监听该事件。
- **拥抱重复而非过早抽象** – 如果两个切片有相似但不完全相同的代码，这是可以的。只有在代码真正相同且稳定时才提取共享逻辑。
- **标准化验证** – 使用像 FluentValidation 这样的库和管道行为来自动验证所有命令。
- **避免贫血切片结构** – 确保处理程序包含真实的业务逻辑；不要仅仅委托给外部服务。处理程序是特性编排所在的位置。
- **记录切片契约** – 命令/查询记录是切片的 API。保持不可变并使其意图明确。

## 缺点与考虑

- **重复风险** – 如果没有纪律，相同的验证或逻辑会在切片间重复。共享内核和领域服务有所帮助，但一些重复是可以接受的。
- **学习曲线** – 刚接触 CQRS、中介者或 VSA 的团队需要时间来适应。
- **工具开销** – MediatR 和类似的库引入了间接性（尽管进程内中介者成本很低）。
- **不适用于简单的 CRUD 应用程序** – 业务逻辑很少的应用程序可能不会从切片开销中受益。

## 结论

Vertical Slice Architecture 为复杂的业务应用程序提供了一种实用、可维护的替代传统分层架构的方案。通过围绕特性而非技术层组织代码，它提高了内聚性，简化了导航，并使系统更容易随业务需求变化而演进。当与 CQRS 和中介者库结合使用时，VSA 提供了一种清晰、自文档化的结构，能很好地随着代码库规模和团队规模扩展。

从小处着手：选择一个特性，将其切片，体验其中的差异。一旦你感受到内聚和隔离，你会奇怪为什么曾容忍跨层分散。

---

### 延伸阅读

- [Jimmy Bogard – Vertical Slice Architecture (Video)](https://www.youtube.com/watch?v=5kOzZz2vj4A)
- [Jimmy Bogard – From Inception to Production (Talk)](https://www.youtube.com/watch?v=Lx9fBkz_0QQ)
- [Vertical Slice Architecture – Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures#vertical-slice-architecture)
- [MediatR GitHub](https://github.com/jbogard/MediatR)