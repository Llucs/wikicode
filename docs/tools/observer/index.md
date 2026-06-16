---
title: Observer Design Pattern
description: A behavioral design pattern that defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.
created: 2026-06-16
tags:
  - design-patterns
  - behavioral
  - observer
  - publish-subscribe
  - event-driven
status: draft
---

# Observer Design Pattern

## What It Is

The **Observer pattern** is a behavioral design pattern where an object, called the **Subject** (or **Observable**), maintains a list of its dependents, called **Observers**, and automatically notifies them of any state changes, usually by calling one of their methods. It establishes a one-to-many dependency so that when the subject changes state, all its observers are updated automatically. The pattern is also known as *Publish-Subscribe*, *Event Listener*, or *Dependents*.

```plaintext
Subject ──→ Observer 1
         ├→ Observer 2
         └→ Observer 3
```

## Why Use It?

- **Loose coupling** – The subject only knows that observers implement a specific interface; it does not depend on concrete observer classes.
- **Dynamic subscriptions** – Observers can be added or removed at runtime without modifying the subject.
- **Broadcast communication** – A single subject efficiently pushes updates to all registered observers.
- **Open/Closed Principle** – New observers can be introduced without changing the subject’s code.
- **Avoids polling** – Observers receive updates automatically instead of repeatedly checking the subject’s state.

## Installation

Because the Observer pattern is a design concept, it is **implemented in code** rather than installed as a package. However, many languages and libraries provide built‑in support:

| Language / Platform | Built‑in / Package |
|---------------------|----------------------|
| Node.js             | `EventEmitter` (core module `events`) |
| Python              | `pip install rx` (ReactiveX) or core `Observable` via `asyncio` |
| JavaScript / TypeScript | `npm install rxjs` |
| Java                | `java.beans.PropertyChangeSupport` or `java.util.concurrent.Flow` |
| C#                  | Language `event` keyword and delegates |

### Example installation commands

```bash
# JavaScript/TypeScript (ReactiveX)
npm install rxjs

# Python (ReactiveX)
pip install rx

# For Node.js EventEmitter, no installation needed (core module)
```

## Key Features

- **One‑to‑Many Notification** – A single subject notifies multiple observers consistently.
- **Loose Coupling** – The subject relies only on an observer interface, not concrete implementations.
- **Broadcast Communication** – State changes are pushed to all observers (or pulled via a notification).
- **Dynamic Subscription** – Observers can subscribe or unsubscribe at any time.
- **Automatic Updates** – Observers stay synchronized without requiring polling.

## Usage Examples

### Classic Python Implementation (Pure)

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

### Java (using `java.util.concurrent.Flow`)

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

## Pros and Cons

### Pros

- **Loose coupling** – Subject and observers are independent.
- **Reusability** – Observers can be reused across different subjects.
- **Dynamic relationships** – Subscriptions can change at runtime.
- **Automatic notification** – Observers are updated without polling.

### Cons

- **Unpredictable order** – Observers may be notified in an arbitrary order.
- **Memory leaks** – If observers are not properly detached, they can accumulate.
- **Complex update chains** – Re‑entrant updates can be difficult to debug.
- **Notification overhead** – Notifying many observers can be costly if not designed carefully.

## History & Context

The Observer pattern was formally cataloged in the 1994 book *Design Patterns: Elements of Reusable Object‑Oriented Software* by the “Gang of Four” (Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides). Its conceptual roots lie in the **Model‑View‑Controller (MVC)** architecture developed at Xerox PARC for Smalltalk in the late 1970s, where views (observers) listen for changes in the model (subject).

Today, the pattern is fundamental in:

- Event‑driven programming (DOM events, GUI listeners)
- Reactive programming (RxJS, Project Reactor)
- Data binding frameworks (Vue.js, Knockout, JavaFX)
- Distributed messaging (Kafka, MQTT)

## Common Use Cases

- **GUI systems** – Button clicks, mouse moves, key presses.
- **Data binding** – Automatically updating UI when a model changes.
- **Reactive streams** – Asynchronous data pipelines with backpressure.
- **Logging** – Distributing log messages to multiple sinks (console, file, network).
- **Financial systems** – Pushing stock ticker updates to multiple dashboards.
- **Messaging brokers** – Publisher/subscriber with decoupled brokers.

---

*The Observer pattern remains a cornerstone of event‑driven architectures, enabling clean, maintainable communication between loosely coupled components.*