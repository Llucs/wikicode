---
title: Microservices mit Clean Architecture und CQRS Implementierung
description: Lernen Sie, wie Sie eine robuste, skalierbare und pflegeleichte Microservices-Architektur mit Clean Architecture und CQRS implementieren.
created: 2026-07-05
tags:
  - microservices
  - clean architecture
  - cQRS
  - .NET 8
  - .NET Core
status: draft
---

# Microservices mit Clean Architecture und CQRS Implementierung

Microservices-Architektur, kombiniert mit Clean Architecture und CQRS, bietet einen robusten, skalierbaren und pflegeleichten Ansatz zur Entwicklung komplexer Anwendungen. Dieses Dokument wird Sie durch die Implementierung solcher Architekturen mit .NET 8 führen.

## Was sind Microservices?

Microservices-Architektur ist ein Entwurfsoptimer, der eine Anwendung als eine Sammlung von eng耦合的服务，通过明确定义的API进行通信的小型、独立的过程实现。

## Clean Architecture

Clean Architecture ist ein Software-Entwurfsmuster, das Fehlerseparation betont, was die Kerngeschäftslogik von externen Frameworks und Technologien unabhängig macht. Es konzentriert sich auf den Kernlogikbereich, was die Anwendung gegenüber Technologien- und Infrastruktur-Veränderungen robust macht. Schlüsselkomponenten sind:

- **Entities**: Geschäftliche Logik und Regeln.
- **Use Cases**: Definieren, wie Entities die äußere Welt mitwirken.
- **Repositories**: Zugriff auf Daten, die abstrahiert werden.
- **Controllers**: Facilitate die Interaktion zwischen der äußeren Welt und der Anwendung.

## CQRS (Command Query Responsibility Segregation)

CQRS ist ein Entwurfsmuster, das die Lesen und Schreibvorgänge in hochskalierbaren Anwendungen durch Separation in zwei Seiten realisiert. In einer CQRS-Architektur sind die Schreibseite (Commands) und die Leseseite (Queries) getrennt, was es ermöglicht, optimierte Datenbank-Schemata für jede Seite zu gestalten.

## Geschichte

- **Microservices**: Entstanden in den frühen 2010er Jahren als Reaktion auf die Einschränkungen von monolithischen Architekturen, insbesondere in Bezug auf Skalierung und Bereitstellung.
- **Clean Architecture**: Im Jahr 2012 von Robert C. Martin (Uncle Bob) vorgeschlagen, betont ein strukturierter Ansatz zur Softwareentwicklung.
- **CQRS**: Erst beschrieben von Eric Evans im Jahr 2010, erlangte in den Mitte 2010er Jahren an Popularität, insbesondere im Kontext von NoSQL-Datenbanken.

## Schlüsselmerkmale

- **Microservices**:
  - **Skalierbarkeit**: Jedes Service kann unabhängig skaliert werden.
  - **Resilienz**: Fehlern eines Services bringt das gesamte System nicht zwangsläufig nieder.
  - **Flexibilität**: Verschiedene Services können mit unterschiedlichen Technologien und Sprachen entwickelt werden.
- **Clean Architecture**:
  - **Fehlerseparation**: Klare Trennung der Verantwortlichkeiten.
  - **Testbarkeit**: Vereinfachte Einzelaufgaben durch die Verantwortlichkeitsseparation.
  - **Evolution**: Einfacher Umpflegungsansatz, ohne bestehende Funktionalität zu stören.
- **CQRS**:
  - **Performanz**: Optimierung von Schreib- und Lesebearbeitungen.
  - **Flexibilität**: Erlaubt unterschiedliche Datenbank-Schemata für Schreib- und Lesebearbeitungen.
  - **Skalierbarkeit**: Lesebearbeitungen können unabhängig von Schreibbearbeitungen skaliert werden.

## Nutzungsfälle

- **Microservices**: Passend für große, komplexe Anwendungen, die hohe Skalierbarkeit und Flexibilität erfordern, wie E-Commerce-Plattformen, Medienstreamingdienste und Bankensysteme.
- **Clean Architecture**: Ideal zur Gewährleistung von Pflegeleichtigkeit und Testbarkeit, besonders in langfristigen Projekten.
- **CQRS**: Vorteilhaft für Anwendungen mit komplexen Schreibvorgängen und hohen Lesebearbeitungen, wie Handelsysteme und Lagerverwaltung.

## Installation und grundlegende Nutzung

### Microservices

1. **Framework-Wahl**: Wählen Sie ein Microservices-Framework wie Spring Boot, ASP.NET Core oder Node.js.
2. **Containerisierung**: Verwenden Sie Docker und Docker Compose, um Services zu verwalten.
3. **Service-Entdeckung**: Implementieren Sie Service-Entdeckungsmechanismen wie Consul oder Eureka.
4. **API-Gateway**: Verwenden Sie einen API-Gateway wie Kong oder Zuul, um den Datenverkehr zwischen Services zu verwalten.

### Clean Architecture

1. **Projektstruktur**: Organisieren Sie das Projekt in Schichten: Entities, Use Cases, Repositories und Controllers.
2. **Frameworks**: Verwenden Sie Frameworks wie Spring Boot oder ASP.NET Core, die Dependency Injection und Testbarkeit unterstützen.
3. **Tests**: Implementieren Sie Einzelaufgaben- und Integrierungs-Tests, um die Kernlogik zu überprüfen.

### CQRS

1. **Datenbank-Setup**: Gestalten Sie separate Datenbanken oder Schemata für Lesen und Schreiben.
2. **Event Sourcing**: Verwenden Sie Event Sourcing, um alle Zustandsänderungen aufzufangen.
3. **Query Layer**: Implementieren Sie Lesemuster, um Lesebearbeitungen zu optimieren.
4. **Command Layer**: Behandeln Sie Befehle, um die Schreibmodelle zu aktualisieren.

### Beispiel: Ein Microservice mit Clean Architecture und CQRS

1. **Entity**:
   - Definieren Sie die Kerngeschäftslogik, z.B. `Order`.

```csharp
public class Order
{
    public int Id { get; set; }
    public string CustomerName { get; set; }
    public DateTime OrderDate { get; set; }
    // Weitere Eigenschaften und Geschäftslógik
}
```

2. **Use Case**:
   - Definieren Sie, wie die Entity die äußere Welt mitwirkt, z.B. `PlaceOrderUseCase`.

```csharp
public interface IPlaceOrderUseCase
{
    Task PlaceOrderAsync(PlaceOrderCommand command);
}

public class PlaceOrderUseCase : IPlaceOrderUseCase
{
    private readonly IOrderRepository _orderRepository;

    public PlaceOrderUseCase(IOrderRepository orderRepository)
    {
        _orderRepository = orderRepository;
    }

    public async Task PlaceOrderAsync(PlaceOrderCommand command)
    {
        var order = new Order
        {
            CustomerName = command.CustomerName,
            OrderDate = DateTime.UtcNow
        };

        await _orderRepository.CreateAsync(order);
    }
}
```

3. **Repository**:
   - Definieren Sie die Schnittstelle für den Zugriff auf den Datenspeicher, z.B. `IOrderRepository`.

```csharp
public interface IOrderRepository
{
    Task<Order> CreateAsync(Order order);
}
```

4. **Controller**:
   - Facilitate die Interaktion zwischen der äußeren Welt und der Anwendung, z.B. `OrderController`.

```csharp
[ApiController]
[Route("api/[controller]")]
public class OrderController : ControllerBase
{
    private readonly IPlaceOrderUseCase _placeOrderUseCase;

    public OrderController(IPlaceOrderUseCase placeOrderUseCase)
    {
        _placeOrderUseCase = placeOrderUseCase;
    }

    [HttpPost("place-order")]
    public async Task<IActionResult> PlaceOrderAsync([FromBody] PlaceOrderCommand command)
    {
        await _placeOrderUseCase.PlaceOrderAsync(command);
        return Ok();
    }
}
```

5. **Command**:
   - Definieren Sie den Befehl, um eine Bestellung zu platzieren, z.B. `PlaceOrderCommand`.

```csharp
public class PlaceOrderCommand
{
    public string CustomerName { get; set; }
}
```

6. **Query**:
   - Definieren Sie den Query, um eine Bestellung abzurufen, z.B. `GetOrderQuery`.

```csharp
public class GetOrderQuery
{
    public int Id { get; set; }
}

public interface IGetOrderQuery
{
    Task<Order> GetAsync(GetOrderQuery query);
}

public class GetOrderQueryHandler : IGetOrderQuery
{
    private readonly IOrderRepository _orderRepository;

    public GetOrderQueryHandler(IOrderRepository orderRepository)
    {
        _orderRepository = orderRepository;
    }

    public async Task<Order> GetAsync(GetOrderQuery query)
    {
        return await _orderRepository.GetAsync(query.Id);
    }
}
```

7. **Event Sourcing**:
   - Erfassen Sie alle Zustandsänderungen, z.B. `OrderPlacedEvent`.

```csharp
public class OrderPlacedEvent
{
    public int OrderId { get; set; }
    public string CustomerName { get; set; }
    public DateTime OrderDate { get; set; }
}
```

Durch die Integration dieser Komponenten können Sie eine robuste, skalierbare und pflegeleichte Anwendung mit Microservices, Clean Architecture und CQRS entwickeln.

## Schlussfolgerung

Die Implementierung von Microservices mit Clean Architecture und CQRS bietet eine solide Grundlage zur Entwicklung komplexer und skalierbarer Anwendungen. Durch das Folgen der von hier dargestellten Richtlinien und Beispiele können Sie eine pflegeleichte und testbare Architektur schaffen, die den modernen Entwicklungspraktiken entspricht.

## Referenzen

- [DDG] Eine .NET 8 Microservices-Architektur, die Clean Architecture, Domain-Driven Design (DDD) und CQRS mit automatisierten Architekturtests, Integrationstests und ereignisgetriebener verteilter Koordination demonstriert.
- [DDG] Joydip Kanjilal erforscht das Command Query Responsibility Segregation (CQRS) Entwurfsmuster und seine Anwendung in Microservices-Architekturen, die mit ASP.NET Core entwickelt werden.
- [DDG] Dieses Projekt ist eine Implementierung der Clean Architecture mit dem CQRS-Entwurfsmuster unter Verwendung von .NET 9.