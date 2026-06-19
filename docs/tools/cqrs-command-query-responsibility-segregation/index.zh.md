---
title: CQRS（命令查询职责分离）
description: 一种将读取和写入操作分离到不同模型中的架构模式，以优化性能、可扩展性和可维护性。
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

CQRS（命令查询职责分离）是一种架构模式，它将读取数据（查询）与更新数据（命令）的职责分离。通过为读取和写入使用不同的模型（通常是独立的数据存储），CQRS 允许对两侧进行独立优化，从而提高复杂系统的可扩展性、性能和安全性。

## 什么是 CQRS 及其历史

CQRS 这一术语由 Greg Young 和 Udi Dahan 在 2000 年代末的领域驱动设计（DDD）社区中推广。其概念基础源于 Bertrand Meyer 的**命令-查询分离（CQS）**原则，该原则规定一个方法要么是*命令*（执行操作），要么是*查询*（返回数据），但不能同时是两者。CQRS 将此思想从方法级提升到架构和数据存储级。

在传统的 CRUD 架构中，单个模型处理读取、写入、更新和删除操作。CQRS 则明确地将其分为两个不同的方面：

- **写模型（命令）：** 处理状态变更操作。命令是命令式的，会产生副作用，并强制执行业务不变性（通常通过 DDD 中的聚合）。
- **读模型（查询）：** 处理数据检索。查询是声明式的，无副作用，并针对特定 UI 或 API 契约进行优化。它们通常是反规范化的、预连接的或存储在不同数据库中（例如，Elasticsearch 用于搜索，Redis 用于缓存）。

CQRS 通常与**事件溯源**结合使用，其中写入端生成一系列领域事件，这些事件被异步消费以构建和更新读模型。

## 为什么使用 CQRS？

| 好处         | 描述 |
|--------------|------|
| **可扩展性** | 读取副本可以独立于写入节点进行扩展。可以根据需要应用不同的基础设施（例如，读取缓存、写入队列）。 |
| **性能**     | 读模型可以针对特定查询进行预优化（反规范化、建立索引）。写模型专注于事务一致性，无需考虑读取开销。 |
| **安全性**   | 分离的模型允许不同的访问控制。通常命令需要更高的权限，而查询可以更宽泛。 |
| **复杂管理** | 将复杂的领域逻辑隔离在写入端，防止其渗透到简单的读取操作中。 |
| **灵活性**   | 不同的读模型可以从同一个写模型服务于不同的视图（移动端、网页端、分析系统）。 |

## 何时使用（及何时避免）

### 以下情况使用 CQRS：

- 共享数据上的高并发（例如，预订、物流、交易系统）。
- 系统的一部分有大量读取负载，且不能阻塞写入事务。
- 不同消费者需要同一数据的不同表示。
- 需要完整的审计跟踪和事件重放（通常与事件溯源一起使用）。

### 以下情况避免使用 CQRS：

- 系统是简单的 CRUD，逻辑很少。
- 强最终一致性对于大多数操作是不可接受的。
- 团队规模小或对最终一致性和消息传递模式不熟悉。
- 维护多个模型的成本超过了收益。

## 安装/框架

CQRS 是一种模式，而不是一个库。“安装”涉及选择一种基础设施层来分发命令、管理事件处理和维护读取投影。流行的框架包括：

- **Axon Framework（Java/Kotlin）：** 功能齐全，提供命令/事件/查询总线、聚合管理和内置事件溯源。
- **MediatR（C#/F#）：** 轻量级进程内中介器，适用于 .NET，非常适合在没有完整消息传递基础设施的单体应用中实现 CQRS。
- **EventStoreDB（Event Store）：** 专用事件存储，与 CQRS 和事件溯源自然结合。
- **Marten（.NET）：** 基于 PostgreSQL 的文档数据库/事件存储，内置投影支持。
- **Dapr（多语言）：** 提供发布/订阅、状态管理和 Actor 构建块，可组合成分布式 CQRS 系统。
- **Lagom（Java/Scala）：** 用于构建响应式微服务的框架，将命令/查询分离作为主要模式。

## 使用示例（概念性 C# / MediatR）

### 写入端 – 命令

```csharp
// 命令定义
public record PlaceOrderCommand(Guid UserId, List<OrderItem> Items);

// 命令处理器
public class PlaceOrderHandler : IRequestHandler<PlaceOrderCommand, Guid>
{
    private readonly IOrderRepository _writeRepo;

    public PlaceOrderHandler(IOrderRepository writeRepo)
    {
        _writeRepo = writeRepo;
    }

    public async Task<Guid> Handle(PlaceOrderCommand command, CancellationToken ct)
    {
        // 1. 验证业务规则（例如，检查库存、用户信用）
        // 2. 创建订单聚合，执行不变量
        var aggregate = Order.Create(command.UserId, command.Items);
        // 3. 将事件/状态持久化到写入存储
        await _writeRepo.Save(aggregate);
        // 4. 返回结果（事件将被发布以更新读取端）
        return aggregate.Id;
    }
}

// 由聚合发出的事件（用于事件溯源或发件箱模式）
public record OrderPlaced(
    Guid OrderId,
    Guid UserId,
    List<OrderItem> Items,
    decimal Total,
    DateTime PlacedAt
);
```

### 读取端 – 查询

```csharp
// 查询定义
public record GetOrderSummaryQuery(Guid OrderId);

// 查询处理器（从独立的、反规范化的数据库读取）
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

### 投影器 – 保持读模型更新

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
        // 将事件数据反规范化到针对读取优化的表中
        await _readDb.ExecuteAsync(@"
            INSERT INTO ReadModel_OrderSummaries (Id, UserId, Total, Status, PlacedAt)
            VALUES (@OrderId, @UserId, @Total, 'Pending', @PlacedAt)",
            @event);
    }
}
```

## 关键特性

- **关注点分离：** 命令和查询可以独立开发、测试和部署。
- **最终一致性：** 写入端发出事件；读模型异步更新。这是一个核心权衡，但能提供高吞吐量。
- **优化存储：** 每一侧都可以使用其自己的数据存储技术（例如，写入：RDBMS，读取：Elasticsearch、Redis、物化视图）。
- **审计与重放（使用事件溯源）：** 完整的事件流可以重建任何过去的状态，并支持调试或重建投影。
- **独立扩展：** 写入节点和读取副本可以根据各自的负载水平扩展。

## 关键权衡与陷阱

- **最终一致性：** 在投影完成之前，用户可能会看到过时数据。缓解措施包括过时数据警告、幂等性或对关键路径的即时一致性。
- **N+1 读模型：** 每个投影都必须被维护。频繁的 UI 变更会增加维护开销。
- **逻辑重复：** 业务规则必须**只**存在于写入端。读取端绝不能包含领域逻辑。
- **基础设施复杂性：** 需要可靠的消息处理（队列、事件总线、发件箱模式）以及对故障场景的监控。
- **学习曲线：** 团队需要理解最终一致性、事件驱动架构和通常的事件溯源。

## 结论

CQRS 是一种强大的模式，适用于读取和写入工作负载具有明显不同的性能、可扩展性或安全需求的系统。但它不是银弹，并且会显著增加复杂性，尤其是与事件溯源结合时。当审慎应用时——通常在涉及复杂业务规则或高读取负载的高协作领域——CQRS 可以极大地提高可维护性、性能和可扩展性。