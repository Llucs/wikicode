---
title: Befehl-Aufruf-Trennung (CQRS)
description: Ein Entwurfsmuster, das in der Softwarearchitektur verwendet wird, um Befehle (Schreiboperatoren) von Aufrufen (Leseelemente) zu trennen.
created: 2026-07-13
tags:
  - Softwarearchitektur
  - Entwurfsmuster
  - CQRS
  - Befehl-Aufruf-Trennung
status: Entwurf
---

# Befehl-Aufruf-Trennung (CQRS)

Befehl-Aufruf-Trennung (CQRS) ist ein Entwurfsmuster, das in der Softwarearchitektur verwendet wird, um Befehle (Schreiboperatoren) von Aufrufen (Leseelemente) zu trennen. Diese Trennung kann zu mehr wartbaren und skalierbaren Anwendungen führen, besonders in komplexen, realen Szenarien.

## Was ist CQRS?

CQRS ist ein Entwurfsmuster, das die Trennung der Aktionen, die Informationen abfragen (Aufrufe) von denen, die den Zustand ändern (Befehle), betont. Diese Trennung kann zu mehr wartbaren und skalierbaren Anwendungen führen, insbesondere in Systemen mit hohen Transaktionsvolumina oder komplexer Geschäftslogik.

## Hauptmerkmale

1. **Befehlshandhabung**: Befehle werden verwendet, um den Zustand des Systems zu ändern. Sie werden normalerweise von externen Systemen oder Benutzern eingeleitet und werden verwendet, um Aktionen wie das Erstellen, Aktualisieren oder Löschen von Daten auszuführen.
2. **Aufrufshandhabung**: Aufrufe werden verwendet, um Informationen aus dem System abzurufen. Sie sind lesende Operatoren, die den Zustand des Systems nicht ändern. Aufrufe können für Leseverkehr optimiert werden, was oft effizienter ist als eine einzelne Datenbank, die sowohl Lesen als auch Schreiben verwalten kann.
3. **Trennung der Sorgen**: CQRS hilft, die Sorgen von Schreib- und Leseelementen zu trennen, was das System mehr wartbar und skalierbar macht.
4. **Ereignisquellen**: In Verbindung mit CQRS häufig verwendet, wo Änderungen an dem System als Folge von Ereignissen aufgezeichnet werden. Diese Ereignisse können verwendet werden, um den aktuellen Zustand des Systems zu rekonstruieren oder um Befehle auszulösen.

## Geschichte

CQRS war keine neue Idee, als es zum ersten Mal populär wurde. Der Begriff der Trennung von Befehlen und Aufrufen existiert schon lange, wurde aber nicht weit verbreitet, bis es von Greg Young und Udi Dahan in den frühen 2010er Jahren gepflegt wurde. Sie präsentierten ihre Ideen bei verschiedenen Konferenzen und Workshops, was zu einem breiteren Einsatz des Musters führte.

## Anwendungsfälle

1. **Online-Transaktionsverarbeitung (OLTP)**: CQRS ist besonders nützlich für Systeme, die hohe Schreibdurchschnitte erfordern, wie E-Commerce-Plattformen, Finanzsysteme oder Spielanwendungen.
2. **Datenbanken**: CQRS kann bei der Erstellung von Datenbanken helfen, indem es die Schreibdominanten transaktionalen Daten von den Lesedominanten analytischer Daten trennt.
3. **Komplexe Geschäftslogik**: Systeme mit komplexer Geschäftslogik, die häufig aktualisiert und verändert werden, können von der Trennung von Befehlen und Aufrufen profitieren.

## Installation

CQRS ist kein eigenständiges Framework, sondern ein Entwurfsmuster. Daher gibt es keine direkte Installation. Sie können CQRS in Ihrer Anwendung implementieren, indem Sie diese allgemeinen Schritte folgen:

1. **Befehle und Aufrufe definieren**: Erstellen Sie eine Menge von Befehlsklassen, um Schreiboperatoren zu verwalten, und Aufrufsklassen, um Leseelemente zu verwalten.
2. **Befehlshandler implementieren**: Schreiben Sie Handler, um die Befehle zu verarbeiten und die notwendigen Operationen auf den Daten auszuführen.
3. **Aufrufshandler implementieren**: Schreiben Sie Handler, um die Aufrufe zu verarbeiten und die erforderlichen Daten zurückzugeben.
4. **Ereignisquellen (optional)**: Implementieren Sie Ereignisquellen, um Änderungen an dem System aufzunehmen und diese Ereignisse zu verwenden, um das Lesemodell zu aktualisieren.

## Basisanwendung

### Befehlshandhabung

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

### Aufrufshandhabung

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

### Ereignisquellen

```csharp
public class OrderAggregate {
    private readonly IEventRepository _eventRepository;

    public OrderAggregate(IEventRepository eventRepository) {
        _eventRepository = eventRepository;
    }

    public void ApplyCommand(PlaceOrderCommand command) {
        // Befehl anwenden und Events speichern
        _eventRepository.Save(new OrderPlacedEvent(command.Order.Id, command.Order.CustomerId));
    }
}
```

## Zusammenfassung

CQRS ist ein mächtiges Entwurfsmuster, das die Skalierbarkeit und Wartbarkeit komplexer Anwendungen erheblich verbessern kann. Durch die Trennung von Befehlen und Aufrufen können Entwickler ihre Systeme für beide Schreib- und Leseelemente optimieren, was zu effizienteren und robusteren Anwendungen führt. Allerdings erfordert eine effektive Implementierung sorgfältige Planung und Implementierung und mag nicht für alle Anwendungen geeignet sein.