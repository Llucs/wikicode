---
title: Vertical Slice Architecture
description: A software design approach that organizes code by business features rather than technical layers, improving cohesion and maintainability.
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

## What Is Vertical Slice Architecture?

Vertical Slice Architecture (VSA) is a software design pattern that structures an application around **business features** or **use cases** instead of horizontal technical layers (Controllers, Services, Repositories, Data Access). Each "vertical slice" captures all the concerns needed to deliver a single feature — from the HTTP endpoint or message handler down to database persistence — as a cohesive, self-contained unit.

> "In this style, my architecture is built around distinct requests, encapsulating and grouping all concerns from front‑end to back. You take a normal 'n‑tier' or hexagonal/whatever architecture and remove the gates and barriers across those layers, and couple ..." — Jimmy Bogard

VSA was popularized around **2016** by Jimmy Bogard (creator of MediatR) as a response to the accidental complexity of traditional Layered or Clean Architecture, where adding even a simple feature requires touching many files scattered across unrelated folders.

## Why Use It?

- **Feature Cohesion** — All code for a use case lives in one place. A developer can understand and modify the entire feature without hopping between projects or folders.
- **Loose Coupling** — Slices are independent; they interact only through a well-defined *shared kernel* (domain entities, base infrastructure, domain events). Changes in one slice rarely break another.
- **Simplified Developer Experience** — Navigation is trivial: locate the feature folder and all its files are right there.
- **CQRS Alignment** — Commands and Queries map naturally to individual slices, encouraging a clear separation of reads and writes.
- **Team Autonomy** — Teams can own entire slices, reducing merge conflicts and allowing parallel development.
- **Refactoring Friendliness** — Because boundaries match business capabilities, restructuring one feature has minimal impact on others.

## How It Differs from Layered Architecture

| Aspect | Layered Architecture | Vertical Slice Architecture |
|--------|---------------------|---------------------------|
| Organization | By technical layer (Controllers, Services, Repositories) | By business feature (e.g., `CreateOrder`, `ShipOrder`) |
| Cohesion | Low – one feature's code is scattered across layers | High – all feature code is together |
| Coupling | Layers depend on each other | Slices depend only on shared kernel |
| Change Impact | A simple change touches many files in many layers | Change is contained within one folder |
| Learning Curve | Familiar to most developers | Requires understanding of CQRS and mediator pattern |

## Key Concepts

### Feature Folder / Slice
Each slice is a directory containing everything a use case needs. A typical slice might include:

```
Features/
  Orders/
    CreateOrder/
      CreateOrderCommand.cs       # Input contract (immutable)
      CreateOrderHandler.cs       # Business logic + orchestration
      CreateOrderValidator.cs     # Input validation
      CreateOrderEndpoint.cs      # API endpoint (Minimal API, Controller, etc.)
```

Nothing outside the slice references these files except through a mediator interface (e.g., `IRequest<OrderDto>`).

### Shared Kernel
Common domain logic, base entities, value objects, and infrastructure (DbContext, logging, authentication) live outside slices in a `Shared` or `Core` project. Slices import from the shared kernel but never from each other.

### CQRS (Command Query Responsibility Segregation)
VSA naturally adopts CQRS. Each slice handles exactly one command (write operation) or one query (read operation), making the system’s intent clear.

### Mediator Pattern
An in-process mediator decouples the sender of a request from the handler. Libraries like **MediatR** or **Brighter** are commonly used to dispatch commands/queries and to apply cross-cutting concerns (validation, logging, transactions).

## When to Use Vertical Slice Architecture

- **Complex Business Domains** – Finance, logistics, healthcare, ERP — domains with many distinct workflows.
- **Large Development Teams** – Features can be assigned to different developers or teams with minimal coordination.
- **Modular Monoliths** – You want strong module boundaries within a single deployment.
- **Microservices** – Each microservice can be a single slice, or VSA can structure its internals.
- **Legacy Migration** – Incrementally replace old layers by slicing features one at a time.

## Installation (Supporting Libraries)

VSA is an architectural pattern, not a library. However, tooling like MediatR is almost always used to implement it in .NET.

### .NET (C#) – MediatR & FluentValidation Setup

```bash
# Create a new project
dotnet new webapi -n MyApp

# Add packages
dotnet add package MediatR
dotnet add package MediatR.Extensions.Microsoft.DependencyInjection  # For automatic registration (if not using latest)
dotnet add package FluentValidation
dotnet add package FluentValidation.DependencyInjectionExtensions
```

## Implementation Example (C# with MediatR)

Let’s build a `PlaceOrder` feature end‑to‑end.

### 1. Contract – Command (Input)

```csharp
// Features/Orders/PlaceOrder/PlaceOrderCommand.cs
using MediatR;

public record PlaceOrderCommand(int CustomerId, List<CartItem> Items) : IRequest<OrderDto>;
```

### 2. Handler – Business Logic + Data Access

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
        // 1. Load customer
        var customer = await _db.Customers
            .Include(c => c.Cart)
            .FirstOrDefaultAsync(c => c.Id == request.CustomerId, cancellationToken)
            ?? throw new NotFoundException("Customer not found");

        // 2. Domain logic – create order
        var order = new Order(customer);
        // ... pricing, validation, etc.

        _db.Orders.Add(order);
        await _db.SaveChangesAsync(cancellationToken);

        return new OrderDto(order.Id, order.Total);
    }
}
```

### 3. Validation (FluentValidation)

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

### 4. Endpoint – Minimal API

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

### 5. Registration & Wiring (Composition Root)

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Register MediatR (scans assembly for handlers)
builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(typeof(Program).Assembly));
builder.Services.AddValidatorsFromAssembly(typeof(Program).Assembly);

// Register DbContext etc.
builder.Services.AddDbContext<AppDbContext>(...);

var app = builder.Build();

// Map endpoints from each slice
app.MapPlaceOrder();

app.Run();
```

### Directory Tree (Simplified)

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

## Key Features with Command Examples (MediatR)

### Dispatch a Command from a Controller or Minimal API

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

### Custom Pipeline Behaviors (Cross-Cutting Concerns)

MediatR supports pipeline behaviors for logging, validation, transactions, etc.

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

### Dispatching a Query

```csharp
// GetOrderHistoryQuery.cs
public record GetOrderHistoryQuery(int CustomerId, int Page = 1, int PageSize = 20) : IRequest<PagedResult<OrderDto>>;

// Handler uses DbContext directly
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

## Best Practices

- **Define a Shared Kernel** – Place entities, value objects, base classes, and common infrastructure in a central location that every slice can reference. Do **not** let slices depend on each other.
- **Keep Slices Thin** – Each slice should contain exactly the logic for its use case. If logic is reused across slices, extract it into a domain service or shared helper, not into a slice.
- **Use Domain Events for Cross-Slice Communication** – When one slice needs to react to another’s action, publish a domain event from the handler and define a separate handler (even if it lives in another slice) that listens to that event.
- **Embrace Duplication over Premature Abstraction** – It’s okay if two slices have similar but slightly different code. Extract shared logic only when it’s truly identical and stable.
- **Standardize Validation** – Use a library like FluentValidation and a pipeline behavior to automatically validate all commands.
- **Avoid Anemic Slice Structures** – Ensure the handler contains real business logic; don’t just delegate to an external service. The handler is the place where the feature’s orchestration lives.
- **Document the Slice Contract** – The command/query record is the API for the slice. Keep it immutable and make its intent obvious.

## Drawbacks & Considerations

- **Duplication Risk** – Without discipline, the same validation or logic can be repeated across slices. A shared kernel and domain services help, but some duplication is accepted.
- **Learning Curve** – Teams new to CQRS, mediator, or VSA need time to adjust.
- **Tooling Overhead** – MediatR and similar libraries introduce indirection (though the in-process mediator is cheap).
- **Not for Simple CRUD Apps** – Applications with minimal business logic may not benefit from the overhead of slicing.

## Conclusion

Vertical Slice Architecture offers a practical, maintainable alternative to traditional layered architectures for complex business applications. By organizing code around features rather than technical layers, it improves cohesion, simplifies navigation, and makes it easier to evolve the system as business requirements change. When combined with CQRS and a mediator library, VSA provides a clean, self‑documenting structure that scales well with both codebase size and team size.

Start small: pick one feature, slice it, and experience the difference. Once you feel the cohesion and isolation, you’ll wonder why you ever tolerated cross‑layer scattering.

---

### Further Reading

- [Jimmy Bogard – Vertical Slice Architecture (Video)](https://www.youtube.com/watch?v=5kOzZz2vj4A)
- [Jimmy Bogard – From Inception to Production (Talk)](https://www.youtube.com/watch?v=Lx9fBkz_0QQ)
- [Vertical Slice Architecture – Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures#vertical-slice-architecture)
- [MediatR GitHub](https://github.com/jbogard/MediatR)