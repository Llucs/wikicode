---
---
title: CQRS (Segregación de Responsabilidad de Comandos y Consultas)
description: Un patrón arquitectónico que separa las operaciones de lectura y escritura en modelos distintos para optimizar el rendimiento, la escalabilidad y la mantenibilidad.
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

CQRS (Command Query Responsibility Segregation) es un patrón arquitectónico que separa las responsabilidades de lectura de datos (queries) de la actualización de datos (commands). Al usar modelos distintos y, a menudo, almacenes de datos separados para lecturas y escrituras, CQRS permite la optimización independiente de cada lado, mejorando la escalabilidad, el rendimiento y la seguridad en sistemas complejos.

## ¿Qué es y su Historia

El término CQRS fue popularizado por Greg Young y Udi Dahan a finales de la década de 2000 dentro de las comunidades de Domain-Driven Design (DDD). Su base conceptual reside en el principio **Command-Query Separation (CQS)** de Bertrand Meyer, que establece que un método debe ser un *command* (realizar una acción) o una *query* (devolver datos), pero no ambos. CQRS eleva esta idea del nivel de método al nivel arquitectónico y de almacenamiento de datos.

En una arquitectura CRUD tradicional, un único modelo maneja lecturas, escrituras, actualizaciones y eliminaciones. CQRS divide explícitamente esto en dos lados distintos:

- **Write Model (Commands):** Maneja operaciones que cambian el estado. Los Commands son imperativos, producen efectos secundarios y hacen cumplir los invariantes de negocio (típicamente a través de Aggregates en DDD).
- **Read Model (Queries):** Maneja la recuperación de datos. Las Queries son declarativas, sin efectos secundarios y optimizadas para contratos de UI o API específicos. A menudo están desnormalizadas, pre-unidas o almacenadas en diferentes bases de datos (por ejemplo, Elasticsearch para búsqueda, Redis para caché).

CQRS se combina frecuentemente con **Event Sourcing**, donde el lado de escritura produce un flujo de eventos de dominio que se consumen asincrónicamente para construir y actualizar los modelos de lectura.

## ¿Por qué usar CQRS?

| Beneficio          | Descripción |
|------------------|-------------|
| **Escalabilidad**  | Las réplicas de lectura pueden escalarse independientemente de los nodos de escritura. Se puede aplicar diferente infraestructura (por ejemplo, cachés de lectura, colas de escritura) según sea necesario. |
| **Rendimiento**  | Los modelos de lectura pueden pre-optimizarse para consultas específicas (desnormalizados, indexados). Los modelos de escritura se centran puramente en la consistencia transaccional sin sobrecarga de lectura. |
| **Seguridad**     | Los modelos separados permiten diferentes controles de acceso. Los Commands típicamente requieren privilegios más altos; las Queries pueden ser más amplias. |
| **Gestión de Complejidad** | Aísla la lógica de dominio compleja en el lado de escritura, evitando que se filtre en operaciones de lectura simples. |
| **Flexibilidad**  | Diferentes modelos de lectura pueden servir diferentes vistas (móvil, web, analítica) desde el mismo modelo de escritura. |

## Cuándo usarlo (y cuándo evitarlo)

### Usar CQRS cuando:

- Alta contención en datos compartidos (ej., sistemas de reservas, logística, trading).
- Una parte del sistema tiene cargas de lectura pesadas que no deben bloquear las transacciones de escritura.
- Se necesitan diferentes representaciones de los mismos datos para diferentes consumidores.
- Se requiere un registro de auditoría completo y reproducción de eventos (típicamente con Event Sourcing).

### Evitar CQRS cuando:

- El sistema es CRUD simple con lógica mínima.
- La consistencia eventual fuerte es inaceptable para la mayoría de las operaciones.
- El equipo es pequeño o no está familiarizado con la consistencia eventual y los patrones de mensajería.
- El costo de mantener múltiples modelos supera los beneficios.

## Instalación / Frameworks

CQRS es un patrón, no una librería. La "instalación" implica elegir una capa de infraestructura para despachar comandos, gestionar el manejo de eventos y mantener las proyecciones de lectura. Los frameworks populares incluyen:

- **Axon Framework (Java/Kotlin):** Completamente equipado con buses de Command/Event/Query, gestión de aggregates y Event Sourcing listo para usar.
- **MediatR (C#/F#):** Mediador ligero en proceso para .NET, excelente para implementar CQRS en un monolito sin una infraestructura de mensajería completa.
- **EventStoreDB (EventStore):** Almacén de eventos diseñado específicamente que se combina naturalmente con CQRS y Event Sourcing.
- **Marten (.NET):** Document DB / event store en PostgreSQL, con soporte de proyección incorporado.
- **Dapr (Multi-lenguaje):** Proporciona bloques de construcción de pub/sub, gestión de estado y actores que pueden componerse en un sistema CQRS distribuido.
- **Lagom (Java/Scala):** Framework para construir microservicios reactivos, incluye la separación command/query como un patrón primario.

## Ejemplo de Uso (Conceptual C# / MediatR)

### Lado de Escritura – Command

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

### Lado de Lectura – Query

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

### Projector – Manteniendo el Modelo de Lectura Actualizado

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

## Características Clave

- **Separación de Preocupaciones:** Los Commands y Queries se desarrollan, prueban e implementan de forma independiente.
- **Consistencia Eventual:** El lado de escritura emite eventos; los modelos de lectura se actualizan asincrónicamente. Esta es una compensación central pero permite un alto rendimiento.
- **Almacenamiento Optimizado:** Cada lado puede usar su propia tecnología de almacenamiento de datos (ej., escritura: RDBMS, lectura: Elasticsearch, Redis, vistas materializadas).
- **Auditoría y Reproducción (con Event Sourcing):** El flujo de eventos completo reconstruye cualquier estado pasado y admite depuración o reconstrucción de proyecciones.
- **Escalado Independiente:** Los nodos de escritura y las réplicas de lectura pueden escalar horizontalmente según sus respectivas cargas.

## Principales Compensaciones y Riesgos

- **Consistencia Eventual:** Los usuarios pueden ver datos obsoletos hasta que las proyecciones se completen. Las mitigaciones incluyen advertencias de datos obsoletos, idempotencia o consistencia inmediata para rutas críticas.
- **Modelos de Lectura N+1:** Cada proyección debe mantenerse. Los cambios frecuentes en la UI pueden aumentar la sobrecarga de mantenimiento.
- **Duplicación de Lógica:** Las reglas de negocio deben vivir solo en el lado de escritura. El lado de lectura nunca debe contener lógica de dominio.
- **Complejidad de Infraestructura:** Requiere manejo confiable de mensajes (colas, buses de eventos, patrones de outbox) y monitoreo para escenarios de fallo.
- **Curva de Aprendizaje:** El equipo requiere comprensión de consistencia eventual, arquitectura impulsada por eventos y, a menudo, Event Sourcing.

## Conclusión

CQRS es un patrón poderoso para sistemas donde las cargas de trabajo de lectura y escritura tienen requisitos de rendimiento, escalabilidad o seguridad notablemente diferentes. No es una bala de plata y agrega una complejidad significativa, especialmente cuando se combina con Event Sourcing. Cuando se aplica juiciosamente—típicamente en dominios de alta colaboración que involucran reglas de negocio complejas o cargas de lectura pesadas—CQRS puede mejorar drásticamente la mantenibilidad, el rendimiento y la escalabilidad.