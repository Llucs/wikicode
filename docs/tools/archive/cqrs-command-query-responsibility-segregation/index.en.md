---
title: CQRS (Command Query Responsibility Segregation)
description: An architectural pattern that separates read and write operations into distinct models to optimize performance, scalability, and maintainability.
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

CQRS (Command Query Responsibility Segregation) is an architectural pattern that separates the responsibilities of reading data (queries) from updating data (commands). By using distinct models and often separate data stores for reads and writes, CQRS enables independent optimization of each side, improving scalability, performance, and security in complex systems.

## What It Is & History

The term CQRS was popularized by Greg Young and Udi Dahan in the late 2000s within Domain-Driven Design (DDD) communities. Its conceptual foundation lies in Bertrand Meyer's **Command-Query Separation (CQS)** principle, which states that a method should either be a *command* (perform an action) or a *query* (return data), but not both. CQRS elevates this idea from the method level to the architectural and data-store level.

In a traditional CRUD architecture, a single model handles reads, writes, updates, and deletes. CQRS explicitly splits this into two distinct sides:

- **Write Model (Commands):** Handles state-changing operations. Commands are imperative, produce side effects, and enforce business invariants (typically through Aggregates in DDD).
- **Read Model (Queries):** Handles data retrieval. Queries are declarative, side-effect-free, and optimized for specific UI or API contracts. They are often denormalized, pre-joined, or stored in different databases (e.g., Elasticsearch for search, Redis for caching).

CQRS is frequently combined with **Event Sourcing**, where the write side produces a stream of domain events that are consumed asynchronously to build and update read models.

## Why Use CQRS?

| Benefit          | Description |
|------------------|-------------|
| **Scalability**  | Read replicas can be scaled independently from write nodes. Different infrastructure (e.g., read caches, write queues) can be applied per need. |
| **Performance**  | Read models can be pre-optimized for specific queries (denormalized, indexed). Write models focus purely on transactional consistency without read overhead. |
| **Security**     | Separate models allow different access controls. Commands typically require higher privileges; queries can be broader. |
| **Complexity Management** | Isolates complex domain logic on the write side, preventing it from bleeding into simple read operations. |
| **Flexibility**  | Different read models can serve different views (mobile, web, analytics) from the same write model. |

## When to Use (and When to Avoid)

### Use CQRS when:

- High contention on shared data (e.g., booking, logistics, trading systems).
- One part of the system has heavy read loads that must not block write transactions.
- Different representations of the same data are needed for different consumers.
- Full audit trail and event replay are required (typically with Event Sourcing).

### Avoid CQRS when:

- The system is simple CRUD with minimal logic.
- Strong eventual consistency is unacceptable for most operations.
- The team is small or unfamiliar with eventual consistency and messaging patterns.
- The cost of maintaining multiple models outweighs the benefits.

## Installation / Frameworks

CQRS is a pattern, not a library. "Installation" involves choosing an infrastructure layer to dispatch commands, manage event handling, and maintain read projections. Popular frameworks include:

- **Axon Framework (Java/Kotlin):** Full-featured with Command/Event/Query buses, aggregate management, and Event Sourcing out of the box.
- **MediatR (C#/F#):** Lightweight in-process mediator for .NET, excellent for implementing CQRS in a monolith without a full messaging infrastructure.
- **EventStoreDB (EventStore):** Purpose-built event store that pairs naturally with CQRS and Event Sourcing.
- **Marten (.NET):** Document DB / event store on PostgreSQL, with built-in projection support.
- **Dapr (Multi-language):** Provides pub/sub, state management, and actor building blocks that can be composed into a distributed CQRS system.
- **Lagom (Java/Scala):** Framework for building reactive microservices, includes command/query separation as a primary pattern.

## Usage Example (Conceptual C# / MediatR)

### Write Side – Command

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

### Read Side – Query

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

### Projector – Keeping the Read Model Updated

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

## Key Features

- **Separation of Concerns:** Commands and queries are developed, tested, and deployed independently.
- **Eventual Consistency:** Write side emits events; read models are updated asynchronously. This is a core trade-off but enables high throughput.
- **Optimized Storage:** Each side can use its own data store technology (e.g., write: RDBMS, read: Elasticsearch, Redis, materialized views).
- **Audit & Replay (with Event Sourcing):** Full event stream reconstructs any past state and supports debugging or rebuilding projections.
- **Independent Scaling:** Write nodes and read replicas can scale horizontally based on their respective loads.

## Key Trade-offs & Pitfalls

- **Eventual Consistency:** Users may see stale data until projections complete. Mitigations include stale-data warnings, idempotency, or immediate consistency for critical paths.
- **N+1 Read Models:** Each projection must be maintained. Frequent UI changes can increase maintenance overhead.
- **Logic Duplication:** Business rules must live **only** on the write side. The read side must never contain domain logic.
- **Infrastructure Complexity:** Requires reliable message handling (queues, event buses, outbox patterns) and monitoring for failure scenarios.
- **Learning Curve:** Team requires understanding of eventual consistency, event-driven architecture, and often Event Sourcing.

## Conclusion

CQRS is a powerful pattern for systems where read and write workloads have distinctly different performance, scalability, or security requirements. It is not a silver bullet and adds significant complexity, especially when combined with Event Sourcing. When applied judiciously—typically in high-collaboration domains involving complex business rules or heavy read load—CQRS can dramatically improve maintainability, performance, and scalability.