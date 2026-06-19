---
title: CQRS (Command Query Responsibility Segregation)
description: Ein Architekturmuster, das Lese- und Schreibvorgänge in separate Modelle trennt, um Leistung, Skalierbarkeit und Wartbarkeit zu optimieren.
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

CQRS (Command Query Responsibility Segregation) ist ein Architekturmuster, das die Verantwortlichkeiten des Lesens von Daten (Abfragen) vom Aktualisieren von Daten (Befehlen) trennt. Durch die Verwendung unterschiedlicher Modelle und oft getrennter Datenspeicher für Lese- und Schreibvorgänge ermöglicht CQRS die unabhängige Optimierung jeder Seite, was die Skalierbarkeit, Leistung und Sicherheit in komplexen Systemen verbessert.

## Was es ist & Geschichte

Der Begriff CQRS wurde von Greg Young und Udi Dahan in den späten 2000er Jahren in der Domain-Driven-Design (DDD)-Community populär gemacht. Seine konzeptionelle Grundlage liegt im **Command-Query Separation (CQS)**-Prinzip von Bertrand Meyer, das besagt, dass eine Methode entweder ein *Befehl* (eine Aktion ausführen) oder eine *Abfrage* (Daten zurückgeben) sein sollte, aber nicht beides. CQRS hebt diese Idee von der Methodenebene auf die Architektur- und Datenspeicherebene.

In einer traditionellen CRUD-Architektur verwaltet ein einzelnes Modell Lese-, Schreib-, Aktualisierungs- und Löschvorgänge. CQRS teilt dies explizit in zwei verschiedene Seiten auf:

- **Schreibmodell (Befehle):** Verarbeitet zustandsändernde Operationen. Befehle sind imperativ, erzeugen Seiteneffekte und erzwingen Geschäftsinvarianten (typischerweise durch Aggregate in DDD).
- **Lesemodell (Abfragen):** Verarbeitet den Datenabruf. Abfragen sind deklarativ, nebenwirkungsfrei und für spezifische UI- oder API-Verträge optimiert. Sie sind oft denormalisiert, vorverbunden oder in verschiedenen Datenbanken gespeichert (z. B. Elasticsearch für die Suche, Redis für Caching).

CQRS wird häufig mit **Event Sourcing** kombiniert, wobei die Schreibseite einen Strom von Domain-Ereignissen erzeugt, die asynchron verarbeitet werden, um Lesemodelle zu erstellen und zu aktualisieren.

## Warum CQRS verwenden?

| Vorteil | Beschreibung |
|------------------|-------------|
| **Skalierbarkeit** | Lesereplikate können unabhängig von Schreibknoten skaliert werden. Unterschiedliche Infrastruktur (z. B. Lesecaches, Schreibwarteschlangen) kann nach Bedarf angewendet werden. |
| **Leistung** | Lesemodelle können für bestimmte Abfragen voroptimiert werden (denormalisiert, indiziert). Schreibmodelle konzentrieren sich ausschließlich auf transaktionale Konsistenz ohne Lese-Overhead. |
| **Sicherheit** | Getrennte Modelle ermöglichen unterschiedliche Zugriffskontrollen. Befehle erfordern typischerweise höhere Berechtigungen; Abfragen können breiter gefasst sein. |
| **Komplexitätsmanagement** | Isoliert komplexe Domänenlogik auf der Schreibseite und verhindert, dass sie in einfache Lesevorgänge eindringt. |
| **Flexibilität** | Unterschiedliche Lesemodelle können verschiedene Ansichten (mobil, Web, Analytik) aus demselben Schreibmodell bedienen. |

## Wann verwenden (und wann vermeiden)

### CQRS verwenden, wenn:

- Hohe Konkurrenz auf gemeinsamen Daten (z. B. Buchungs-, Logistik-, Handelssysteme).
- Ein Teil des Systems hat hohe Leselasten, die Schreibtransaktionen nicht blockieren dürfen.
- Unterschiedliche Darstellungen derselben Daten für verschiedene Verbraucher erforderlich sind.
- Vollständiger Prüfpfad und Ereigniswiederholung erforderlich sind (typischerweise mit Event Sourcing).

### CQRS vermeiden, wenn:

- Das System ein einfaches CRUD mit minimaler Logik ist.
- Starke Eventual Consistency für die meisten Operationen inakzeptabel ist.
- Das Team klein oder mit Eventual Consistency und Messaging-Mustern nicht vertraut ist.
- Die Kosten für die Wartung mehrerer Modelle den Nutzen überwiegen.

## Installation / Frameworks

CQRS ist ein Muster, keine Bibliothek. "Installation" umfasst die Auswahl einer Infrastrukturschicht zum Senden von Befehlen, Verwalten der Ereignisbehandlung und Verwalten von Leseprojektionen. Beliebte Frameworks sind:

- **Axon Framework (Java/Kotlin):** Voll ausgestattet mit Befehls-/Ereignis-/Abfrage-Bussen, Aggregatverwaltung und Event Sourcing out of the box.
- **MediatR (C#/F#):** Leichter In-Process-Mediator für .NET, hervorragend geeignet zur Implementierung von CQRS in einem Monolithen ohne vollständige Messaging-Infrastruktur.
- **EventStoreDB (EventStore):** Zweckgebauter Ereignisspeicher, der natürlich mit CQRS und Event Sourcing harmoniert.
- **Marten (.NET):** Dokumenten-DB / Ereignisspeicher auf PostgreSQL mit integrierter Projektionsunterstützung.
- **Dapr (Multi-Sprache):** Bietet Pub/Sub, Zustandsverwaltung und Actor-Bausteine, die zu einem verteilten CQRS-System zusammengesetzt werden können.
- **Lagom (Java/Scala):** Framework zur Erstellung reaktiver Microservices, enthält Befehls-/Abfrage-Trennung als primäres Muster.

## Nutzungsbeispiel (Konzeptionelles C# / MediatR)

### Schreibseite – Befehl

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

### Leseseite – Abfrage

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

### Projektor – Das Lesemodell aktualisieren

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

## Hauptmerkmale

- **Trennung der Belange:** Befehle und Abfragen werden unabhängig voneinander entwickelt, getestet und bereitgestellt.
- **Eventuale Konsistenz:** Die Schreibseite gibt Ereignisse aus; Lesemodelle werden asynchron aktualisiert. Dies ist ein grundlegender Kompromiss, ermöglicht jedoch einen hohen Durchsatz.
- **Optimierter Speicher:** Jede Seite kann ihre eigene Datenspeichertechnologie verwenden (z. B. Schreiben: RDBMS, Lesen: Elasticsearch, Redis, materialisierte Ansichten).
- **Audit & Wiederholung (mit Event Sourcing):** Der vollständige Ereignisstrom rekonstruiert jeden vergangenen Zustand und unterstützt das Debuggen oder Neuerstellen von Projektionen.
- **Unabhängige Skalierung:** Schreibknoten und Lesereplikate können basierend auf ihren jeweiligen Lasten horizontal skaliert werden.

## Wichtige Kompromisse & Fallstricke

- **Eventuale Konsistenz:** Benutzer sehen möglicherweise veraltete Daten, bis Projektionen abgeschlossen sind. Minderungsmaßnahmen umfassen Warnungen vor veralteten Daten, Idempotenz oder sofortige Konsistenz für kritische Pfade.
- **N+1 Lesemodelle:** Jede Projektion muss gewartet werden. Häufige UI-Änderungen können den Wartungsaufwand erhöhen.
- **Logikduplikation:** Geschäftsregeln dürfen **nur** auf der Schreibseite existieren. Die Leseseite darf niemals Domänenlogik enthalten.
- **Infrastrukturkomplexität:** Erfordert zuverlässige Nachrichtenverarbeitung (Warteschlangen, Ereignisbusse, Outbox-Muster) und Überwachung für Fehlerszenarien.
- **Lernkurve:** Das Team benötigt Verständnis für eventual consistency, ereignisgesteuerte Architektur und oft Event Sourcing.

## Fazit

CQRS ist ein leistungsstarkes Muster für Systeme, in denen Lese- und Schreibworkloads deutlich unterschiedliche Anforderungen an Leistung, Skalierbarkeit oder Sicherheit haben. Es ist kein Allheilmittel und fügt erhebliche Komplexität hinzu, insbesondere in Kombination mit Event Sourcing. Bei umsichtiger Anwendung – typischerweise in stark kollaborativen Bereichen mit komplexen Geschäftsregeln oder hoher Leselast – kann CQRS die Wartbarkeit, Leistung und Skalierbarkeit erheblich verbessern.