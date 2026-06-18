---
title: Vertical Slice Architecture
description: Ein Softwareentwurfsansatz, der Code nach Geschäftsfunktionen statt nach technischen Schichten organisiert und so Kohäsion und Wartbarkeit verbessert.
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

## Was ist die Vertical Slice Architecture?

Vertical Slice Architecture (VSA) ist ein Softwareentwurfsmuster, das eine Anwendung um **Geschäftsfunktionen** oder **Anwendungsfälle** herum strukturiert, anstatt um horizontale technische Schichten (Controller, Services, Repositories, Datenzugriff). Jeder „vertikale Slice“ erfasst alle Belange, die zur Bereitstellung einer einzelnen Funktion erforderlich sind – vom HTTP‑Endpoint oder Nachrichtenhandler bis zur Datenbankpersistenz – als kohärente, in sich geschlossene Einheit.

> „In diesem Stil ist meine Architektur um einzelne Anfragen herum aufgebaut, die alle Belange vom Front‑End bis zum Back‑End kapseln und gruppieren. Man nimmt eine normale 'n‑tier' oder hexagonale/welche Architektur auch immer und entfernt die Tore und Barrieren zwischen diesen Schichten, und koppelt …“ – Jimmy Bogard

VSA wurde um **2016** von Jimmy Bogard (Erfinder von MediatR) populär gemacht, als Reaktion auf die unbeabsichtigte Komplexität traditioneller Schichten‑ oder Clean Architecture, bei der selbst für eine einfache Funktion zahlreiche Dateien in verschiedenen Ordnern geändert werden müssen.

## Warum sollte man es verwenden?

- **Feature‑Kohäsion** – Der gesamte Code für einen Anwendungsfall befindet sich an einem Ort. Ein Entwickler kann die vollständige Funktion verstehen und ändern, ohne zwischen Projekten oder Ordnern wechseln zu müssen.
- **Lockere Kopplung** – Slices sind unabhängig; sie interagieren nur über einen klar definierten *Shared Kernel* (Domain‑Entitäten, Basis‑Infrastruktur, Domain‑Events). Änderungen in einem Slice wirken sich selten auf andere aus.
- **Vereinfachte Entwicklererfahrung** – Die Navigation ist trivial: Den Feature‑Ordner lokalisieren und alle zugehörigen Dateien sind sofort sichtbar.
- **CQRS‑Ausrichtung** – Commands und Queries lassen sich auf natürliche Weise einzelnen Slices zuordnen, was eine klare Trennung von Lese‑ und Schreiboperationen fördert.
- **Team‑Autonomie** – Teams können ganze Slices eigenständig bearbeiten, was Merge‑Konflikte reduziert und parallele Entwicklung ermöglicht.
- **Refactoring‑Freundlichkeit** – Da die Grenzen den Geschäftsfunktionen entsprechen, hat die Umstrukturierung einer Funktion nur minimale Auswirkungen auf andere.

## Wie unterscheidet es sich von der Schichtenarchitektur?

| Aspekt | Schichtenarchitektur | Vertical Slice Architecture |
|--------|----------------------|-----------------------------|
| Organisation | Nach technischer Schicht (Controller, Services, Repositories) | Nach Geschäftsfunktion (z. B. `CreateOrder`, `ShipOrder`) |
| Kohäsion | Niedrig – Der Code einer Funktion ist über mehrere Schichten verstreut | Hoch – Der gesamte Funktionscode ist beisammen |
| Kopplung | Schichten hängen voneinander ab | Slices hängen nur vom Shared Kernel ab |
| Änderungsauswirkung | Eine einfache Änderung betrifft viele Dateien in vielen Schichten | Die Änderung bleibt auf einen Ordner beschränkt |
| Lernkurve | Den meisten Entwicklern vertraut | Erfordert Verständnis von CQRS und dem Mediator‑Pattern |

## Schlüsselkonzepte

### Feature‑Ordner / Slice
Jeder Slice ist ein Verzeichnis, das alles enthält, was ein Anwendungsfall benötigt. Ein typischer Slice könnte so aussehen:

```
Features/
  Orders/
    CreateOrder/
      CreateOrderCommand.cs       # Eingabevertrag (unveränderlich)
      CreateOrderHandler.cs       # Geschäftslogik + Orchestrierung
      CreateOrderValidator.cs     # Eingabevalidierung
      CreateOrderEndpoint.cs      # API‑Endpoint (Minimal API, Controller, etc.)
```

Außerhalb des Slices wird auf diese Dateien nur über eine Mediator‑Schnittstelle (z. B. `IRequest<OrderDto>`) verwiesen.

### Shared Kernel
Gemeinsame Domain‑Logik, Basis‑Entitäten, Value Objects und Infrastruktur (DbContext, Logging, Authentifizierung) befinden sich außerhalb der Slices in einem `Shared`‑ oder `Core`‑Projekt. Slices importieren aus dem Shared Kernel, aber niemals voneinander.

### CQRS (Command Query Responsibility Segregation)
VSA übernimmt auf natürliche Weise CQRS. Jeder Slice behandelt genau einen Command (Schreiboperation) oder eine Query (Leseoperation), was die Absicht des Systems klar macht.

### Mediator‑Pattern
Ein prozessinterner Mediator entkoppelt den Absender einer Anfrage vom Handler. Bibliotheken wie **MediatR** oder **Brighter** werden üblicherweise verwendet, um Commands/Queries zu dispatchen und Querschnittsbelange (Validierung, Logging, Transaktionen) anzuwenden.

## Wann sollte man Vertical Slice Architecture verwenden?

- **Komplexe Geschäftsdomänen** – Finanzen, Logistik, Gesundheitswesen, ERP – Domänen mit vielen unterschiedlichen Arbeitsabläufen.
- **Große Entwicklungsteams** – Funktionen können verschiedenen Entwicklern oder Teams mit minimalem Koordinationsaufwand zugewiesen werden.
- **Modulare Monolithen** – Starke Modulgrenzen innerhalb einer einzigen Bereitstellung.
- **Microservices** – Jeder Microservice kann ein einzelner Slice sein, oder VSA kann dessen Interna strukturieren.
- **Legacy‑Migration** – Schrittweises Ersetzen alter Schichten durch schrittweises Slicen von Funktionen.

## Installation (unterstützende Bibliotheken)

VSA ist ein Architekturmuster, keine Bibliothek. Für die Implementierung in .NET wird jedoch fast immer MediatR verwendet.

### .NET (C#) – MediatR‑ und FluentValidation‑Setup

```bash
# Neues Projekt erstellen
dotnet new webapi -n MyApp

# Pakete hinzufügen
dotnet add package MediatR
dotnet add package MediatR.Extensions.Microsoft.DependencyInjection  # Für automatische Registrierung (falls nicht neueste Version)
dotnet add package FluentValidation
dotnet add package FluentValidation.DependencyInjectionExtensions
```

## Implementierungsbeispiel (C# mit MediatR)

Wir erstellen die Funktion `PlaceOrder` durchgängig.

### 1. Vertrag – Command (Eingabe)

```csharp
// Features/Orders/PlaceOrder/PlaceOrderCommand.cs
using MediatR;

public record PlaceOrderCommand(int CustomerId, List<CartItem> Items) : IRequest<OrderDto>;
```

### 2. Handler – Geschäftslogik + Datenzugriff

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
        // 1. Kunde laden
        var customer = await _db.Customers
            .Include(c => c.Cart)
            .FirstOrDefaultAsync(c => c.Id == request.CustomerId, cancellationToken)
            ?? throw new NotFoundException("Customer not found");

        // 2. Domänenlogik – Bestellung erstellen
        var order = new Order(customer);
        // ... Preisberechnung, Validierung, etc.

        _db.Orders.Add(order);
        await _db.SaveChangesAsync(cancellationToken);

        return new OrderDto(order.Id, order.Total);
    }
}
```

### 3. Validierung (FluentValidation)

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

### 5. Registrierung und Verdrahtung (Composition Root)

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// MediatR registrieren (durchsucht Assembly nach Handlern)
builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(typeof(Program).Assembly));
builder.Services.AddValidatorsFromAssembly(typeof(Program).Assembly);

// DbContext usw. registrieren
builder.Services.AddDbContext<AppDbContext>(...);

var app = builder.Build();

// Endpoints von jedem Slice zuordnen
app.MapPlaceOrder();

app.Run();
```

### Verzeichnisbaum (vereinfacht)

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

## Hauptfunktionen mit Befehlsbeispielen (MediatR)

### Senden eines Commands aus einem Controller oder einer Minimal API

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

### Benutzerdefinierte Pipeline‑Verhaltensweisen (Querschnittsbelange)

MediatR unterstützt Pipeline‑Verhalten für Logging, Validierung, Transaktionen usw.

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

### Senden einer Query

```csharp
// GetOrderHistoryQuery.cs
public record GetOrderHistoryQuery(int CustomerId, int Page = 1, int PageSize = 20) : IRequest<PagedResult<OrderDto>>;

// Handler verwendet DbContext direkt
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

## Bewährte Methoden

- **Definieren Sie einen Shared Kernel** – Platzieren Sie Entitäten, Value Objects, Basisklassen und gemeinsame Infrastruktur an einem zentralen Ort, auf den jeder Slice zugreifen kann. Lassen Sie **keine** Slices voneinander abhängen.
- **Halten Sie Slices schlank** – Jeder Slice sollte genau die Logik für seinen Anwendungsfall enthalten. Wenn Logik von mehreren Slices verwendet wird, extrahieren Sie sie in einen Domain‑Service oder einen gemeinsamen Helfer, nicht in einen Slice.
- **Verwenden Sie Domain‑Events für die Kommunikation zwischen Slices** – Wenn ein Slice auf eine Aktion eines anderen reagieren muss, veröffentlichen Sie ein Domain‑Event im Handler und definieren Sie einen separaten Handler (auch wenn er in einem anderen Slice lebt), der auf dieses Event hört.
- **Duplizieren Sie lieber, anstatt vorzeitig zu abstrahieren** – Es ist in Ordnung, wenn zwei Slices ähnlichen, aber leicht unterschiedlichen Code haben. Extrahieren Sie gemeinsame Logik nur dann, wenn sie wirklich identisch und stabil ist.
- **Standardisieren Sie die Validierung** – Verwenden Sie eine Bibliothek wie FluentValidation und ein Pipeline‑Verhalten, um alle Commands automatisch zu validieren.
- **Vermeiden Sie anämische Slice‑Strukturen** – Stellen Sie sicher, dass der Handler echte Geschäftslogik enthält; delegieren Sie nicht nur an einen externen Service. Der Handler ist der Ort, an dem die Orchestrierung der Funktion lebt.
- **Dokumentieren Sie den Slice‑Vertrag** – Der Command/Query‑Record ist die API des Slices. Halten Sie ihn unveränderlich und machen Sie seine Absicht offensichtlich.

## Nachteile und Überlegungen

- **Risiko der Duplizierung** – Ohne Disziplin kann dieselbe Validierung oder Logik in mehreren Slices wiederholt werden. Ein Shared Kernel und Domain‑Services helfen, aber ein gewisses Maß an Duplizierung wird akzeptiert.
- **Lernkurve** – Teams, die neu bei CQRS, Mediator oder VSA sind, brauchen Zeit, um sich anzupassen.
- **Werkzeug‑Overhead** – MediatR und ähnliche Bibliotheken führen eine Indirektion ein (obwohl der prozessinterne Mediator günstig ist).
- **Nicht für einfache CRUD‑Apps** – Anwendungen mit minimaler Geschäftslogik ziehen möglicherweise keinen Nutzen aus dem Mehraufwand des Slicens.

## Fazit

Die Vertical Slice Architecture bietet eine praktische, wartbare Alternative zu traditionellen Schichtenarchitekturen für komplexe Geschäftsanwendungen. Indem der Code um Funktionen statt um technische Schichten organisiert wird, verbessert sie die Kohäsion, vereinfacht die Navigation und erleichtert die Weiterentwicklung des Systems bei sich ändernden Geschäftsanforderungen. In Kombination mit CQRS und einer Mediator‑Bibliothek bietet VSA eine saubere, selbst dokumentierende Struktur, die sowohl mit der Codebasis‑ als auch mit der Teamgröße gut skaliert.

Fangen Sie klein an: Wählen Sie eine Funktion aus, slicen Sie sie und erleben Sie den Unterschied. Sobald Sie die Kohäsion und Isolation spüren, werden Sie sich fragen, warum Sie jemals die schichtübergreifende Streuung toleriert haben.

---

### Weiterführende Literatur

- [Jimmy Bogard – Vertical Slice Architecture (Video)](https://www.youtube.com/watch?v=5kOzZz2vj4A)
- [Jimmy Bogard – From Inception to Production (Talk)](https://www.youtube.com/watch?v=Lx9fBkz_0QQ)
- [Vertical Slice Architecture – Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures#vertical-slice-architecture)
- [MediatR GitHub](https://github.com/jbogard/MediatR)