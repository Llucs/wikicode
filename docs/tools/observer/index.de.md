---
title: Observer-Entwurfsmuster
description: Ein Verhaltensentwurfsmuster, das eine Eins-zu-Viele-Abhängigkeit zwischen Objekten definiert, sodass wenn ein Objekt seinen Zustand ändert, alle seine Abhängigen automatisch benachrichtigt und aktualisiert werden.
created: 2026-06-16
tags:
  - design-patterns
  - behavioral
  - observer
  - publish-subscribe
  - event-driven
status: draft
---

# Observer-Entwurfsmuster

## Was es ist

Der **Observer-Entwurfsmuster** (oder **Beobachter-Entwurfsmuster**) ist ein Verhaltensentwurfsmuster, bei dem ein Objekt, genannt das **Subjekt** (oder **Observable**), eine Liste seiner Abhängigen, genannt **Beobachter** (Observers), verwaltet und sie automatisch über Zustandsänderungen benachrichtigt, normalerweise durch Aufruf einer ihrer Methoden. Es stellt eine Eins-zu-Viele-Abhängigkeit her, sodass wenn das Subjekt seinen Zustand ändert, alle seine Beobachter automatisch aktualisiert werden. Das Muster ist auch bekannt als *Publish-Subscribe*, *Event Listener* oder *Dependents*.

```plaintext
Subject ──→ Observer 1
         ├→ Observer 2
         └→ Observer 3
```

## Warum es verwenden?

- **Lose Kopplung** – Das Subjekt weiß nur, dass Beobachter ein bestimmtes Interface implementieren; es hängt nicht von konkreten Beobachterklassen ab.
- **Dynamische Abonnements** – Beobachter können zur Laufzeit hinzugefügt oder entfernt werden, ohne das Subjekt zu ändern.
- **Broadcast-Kommunikation** – Ein einzelnes Subjekt schiebt Aktualisierungen effizient an alle registrierten Beobachter.
- **Open/Closed-Prinzip** – Neue Beobachter können eingeführt werden, ohne den Code des Subjekts zu ändern.
- **Vermeidung von Polling** – Beobachter erhalten Aktualisierungen automatisch, anstatt den Zustand des Subjekts wiederholt zu überprüfen.

## Installation

Da das Observer-Entwurfsmuster ein Entwurfskonzept ist, wird es **im Code implementiert** und nicht als Paket installiert. Viele Sprachen und Bibliotheken bieten jedoch integrierte Unterstützung:

| Sprache / Plattform | Integriert / Paket |
|---------------------|----------------------|
| Node.js             | `EventEmitter` (Kernmodul `events`) |
| Python              | `pip install rx` (ReactiveX) oder Kern-`Observable` via `asyncio` |
| JavaScript / TypeScript | `npm install rxjs` |
| Java                | `java.beans.PropertyChangeSupport` oder `java.util.concurrent.Flow` |
| C#                  | Sprache `event`-Schlüsselwort und Delegates |

### Beispiel-Installationsbefehle

```bash
# JavaScript/TypeScript (ReactiveX)
npm install rxjs

# Python (ReactiveX)
pip install rx

# For Node.js EventEmitter, no installation needed (core module)
```

## Hauptmerkmale

- **Eins-zu-Viele-Benachrichtigung** – Ein einzelnes Subjekt benachrichtigt mehrere Beobachter konsistent.
- **Lose Kopplung** – Das Subjekt verlässt sich nur auf ein Beobachter-Interface, nicht auf konkrete Implementierungen.
- **Broadcast-Kommunikation** – Zustandsänderungen werden an alle Beobachter gepusht (oder per Benachrichtigung gepullt).
- **Dynamisches Abonnement** – Beobachter können jederzeit abonnieren oder kündigen.
- **Automatische Aktualisierungen** – Beobachter bleiben ohne Polling synchronisiert.

## Verwendungsbeispiele

### Klassische Python-Implementierung (Pure)

```python
# Subject
class NewsAgency:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, news):
        for observer in self._observers:
            observer.update(news)

# Observer interface
class Observer:
    def update(self, news):
        raise NotImplementedError

# Concrete observers
class EmailNotifier(Observer):
    def update(self, news):
        print(f"Email sent with: {news}")

class SMSNotifier(Observer):
    def update(self, news):
        print(f"SMS sent with: {news}")

# Usage
news = NewsAgency()
news.attach(EmailNotifier())
news.attach(SMSNotifier())
news.notify("Breaking: Stock market hits new high!")
# Output:
# Email sent with: Breaking: Stock market hits new high!
# SMS sent with: Breaking: Stock market hits new high!
```

### Node.js EventEmitter

```javascript
const EventEmitter = require('events');

class NewsAgency extends EventEmitter {
    publish(news) {
        this.emit('news', news);
    }
}

// Observers (listeners)
const agency = new NewsAgency();

agency.on('news', (news) => console.log(`Email: ${news}`));
agency.on('news', (news) => console.log(`SMS: ${news}`));

agency.publish('Breaking: Stock market hits new high!');
// Output:
// Email: Breaking: Stock market hits new high!
// SMS: Breaking: Stock market hits new high!
```

### RxJS (JavaScript)

```javascript
import { Subject } from 'rxjs';

const subject = new Subject();

// Observer A
subject.subscribe(val => console.log(`Observer A: ${val}`));
// Observer B
subject.subscribe(val => console.log(`Observer B: ${val}`));

subject.next("Hello World");
// Output:
// Observer A: Hello World
// Observer B: Hello World
```

### Java (mit `java.util.concurrent.Flow`)

```java
import java.util.concurrent.Flow.*;
import java.util.concurrent.SubmissionPublisher;

public class ObserverExample {
    public static void main(String[] args) {
        SubmissionPublisher<String> publisher = new SubmissionPublisher<>();

        Subscriber<String> subscriber1 = new Subscriber<>() {
            private Subscription sub;
            public void onSubscribe(Subscription sub) { this.sub = sub; sub.request(1); }
            public void onNext(String item) { System.out.println("Subscriber1: " + item); sub.request(1); }
            public void onError(Throwable t) { t.printStackTrace(); }
            public void onComplete() { System.out.println("Done"); }
        };

        publisher.subscribe(subscriber1);
        publisher.submit("Hello");
        publisher.submit("World");
        publisher.close();
    }
}
```

## Vor- und Nachteile

### Vorteile

- **Lose Kopplung** – Subjekt und Beobachter sind unabhängig.
- **Wiederverwendbarkeit** – Beobachter können über verschiedene Subjekte hinweg wiederverwendet werden.
- **Dynamische Beziehungen** – Abonnements können zur Laufzeit geändert werden.
- **Automatische Benachrichtigung** – Beobachter werden ohne Polling aktualisiert.

### Nachteile

- **Unvorhersehbare Reihenfolge** – Beobachter können in beliebiger Reihenfolge benachrichtigt werden.
- **Speicherlecks** – Wenn Beobachter nicht ordnungsgemäß abgemeldet werden, können sie sich ansammeln.
- **Komplexe Aktualisierungsketten** – Rekursive Aktualisierungen können schwer zu debuggen sein.
- **Benachrichtigungsaufwand** – Das Benachrichtigen vieler Beobachter kann kostspielig sein, wenn es nicht sorgfältig entworfen wird.

## Geschichte & Kontext

Das Observer-Entwurfsmuster wurde 1994 im Buch *Design Patterns: Elements of Reusable Object‑Oriented Software* der "Gang of Four" (Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides) formal katalogisiert. Seine konzeptionellen Wurzeln liegen in der **Model‑View‑Controller (MVC)**-Architektur, die in den späten 1970er Jahren bei Xerox PARC für Smalltalk entwickelt wurde, bei der Ansichten (Beobachter) auf Änderungen im Modell (Subjekt) warten.

Heute ist das Muster grundlegend in:

- **Ereignisgesteuerte Programmierung** (DOM-Ereignisse, GUI-Listener)
- **Reaktive Programmierung** (RxJS, Project Reactor)
- **Datenbindungsframeworks** (Vue.js, Knockout, JavaFX)
- **Verteilte Nachrichtenübermittlung** (Kafka, MQTT)

## Häufige Anwendungsfälle

- **GUI-Systeme** – Schaltflächenklicks, Mausbewegungen, Tastendrücke.
- **Datenbindung** – Automatische Aktualisierung der Benutzeroberfläche bei Änderungen eines Modells.
- **Reaktive Streams** – Asynchrone Datenpipelines mit Backpressure.
- **Protokollierung** – Verteilung von Protokollmeldungen an mehrere Senken (Konsole, Datei, Netzwerk).
- **Finanzsysteme** – Übertragung von Börsenticker-Updates an mehrere Dashboards.
- **Nachrichtenbroker** – Publisher/Subscriber mit entkoppelten Brokern.

---

*Das Observer-Entwurfsmuster bleibt ein Eckpfeiler ereignisgesteuerter Architekturen und ermöglicht eine saubere, wartbare Kommunikation zwischen lose gekoppelten Komponenten.*