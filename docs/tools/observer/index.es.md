---
title: Patrón de Diseño Observer
description: Un patrón de diseño de comportamiento que define una dependencia de uno a muchos entre objetos, de modo que cuando un objeto cambia de estado, todos sus dependientes son notificados y actualizados automáticamente.
created: 2026-06-16
tags:
  - design-patterns
  - behavioral
  - observer
  - publish-subscribe
  - event-driven
status: draft
---

# Patrón de Diseño Observer

## Qué Es

El patrón **Observer** es un patrón de diseño de comportamiento en el que un objeto, llamado **Sujeto** (u **Observable**), mantiene una lista de sus dependientes, llamados **Observadores**, y los notifica automáticamente de cualquier cambio de estado, generalmente llamando a uno de sus métodos. Establece una dependencia de uno a muchos de manera que cuando el sujeto cambia de estado, todos sus observadores se actualizan automáticamente. El patrón también se conoce como *Publicar-Suscribir*, *Escuchador de Eventos* o *Dependientes*.

```plaintext
Subject ──→ Observer 1
         ├→ Observer 2
         └→ Observer 3
```

## Por Qué Usarlo?

- **Acoplamiento débil** – El sujeto solo sabe que los observadores implementan una interfaz específica; no depende de clases concretas de observadores.
- **Suscripciones dinámicas** – Los observadores pueden agregarse o eliminarse en tiempo de ejecución sin modificar el sujeto.
- **Comunicación por difusión** – Un solo sujeto envía actualizaciones de manera eficiente a todos los observadores registrados.
- **Principio Abierto/Cerrado** – Se pueden introducir nuevos observadores sin cambiar el código del sujeto.
- **Evita el sondeo** – Los observadores reciben actualizaciones automáticamente en lugar de verificar repetidamente el estado del sujeto.

## Instalación

Debido a que el patrón Observer es un concepto de diseño, se **implementa en código** en lugar de instalarse como un paquete. Sin embargo, muchos lenguajes y bibliotecas ofrecen soporte integrado:

| Lenguaje / Plataforma | Integrado / Paquete |
|---------------------|----------------------|
| Node.js | `EventEmitter` (módulo central `events`) |
| Python | `pip install rx` (ReactiveX) o `Observable` central mediante `asyncio` |
| JavaScript / TypeScript | `npm install rxjs` |
| Java | `java.beans.PropertyChangeSupport` o `java.util.concurrent.Flow` |
| C# | Palabra clave `event` del lenguaje y delegados |

### Ejemplo de comandos de instalación

```bash
# JavaScript/TypeScript (ReactiveX)
npm install rxjs

# Python (ReactiveX)
pip install rx

# For Node.js EventEmitter, no installation needed (core module)
```

## Características Principales

- **Notificación de uno a muchos** – Un solo sujeto notifica a múltiples observadores de manera consistente.
- **Acoplamiento débil** – El sujeto solo depende de una interfaz de observador, no de implementaciones concretas.
- **Comunicación por difusión** – Los cambios de estado se envían a todos los observadores (o se obtienen mediante una notificación).
- **Suscripción dinámica** – Los observadores pueden suscribirse o cancelar la suscripción en cualquier momento.
- **Actualizaciones automáticas** – Los observadores se mantienen sincronizados sin necesidad de sondeo.

## Ejemplos de Uso

### Implementación Clásica en Python (Pura)

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

### EventEmitter de Node.js

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

### Java (usando `java.util.concurrent.Flow`)

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

## Pros y Contras

### Pros

- **Acoplamiento débil** – El sujeto y los observadores son independientes.
- **Reutilización** – Los observadores pueden reutilizarse en diferentes sujetos.
- **Relaciones dinámicas** – Las suscripciones pueden cambiar en tiempo de ejecución.
- **Notificación automática** – Los observadores se actualizan sin sondeo.

### Contras

- **Orden impredecible** – Los observadores pueden notificarse en un orden arbitrario.
- **Fugas de memoria** – Si los observadores no se desvinculan correctamente, pueden acumularse.
- **Cadenas de actualización complejas** – Las actualizaciones reentrantes pueden ser difíciles de depurar.
- **Sobrecarga de notificación** – Notificar a muchos observadores puede ser costoso si no se diseñan cuidadosamente.

## Historia y Contexto

El patrón Observer fue catalogado formalmente en el libro de 1994 *Design Patterns: Elements of Reusable Object‑Oriented Software* de la “Gang of Four” (Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides). Sus raíces conceptuales se encuentran en la arquitectura **Model‑View‑Controller (MVC)** desarrollada en Xerox PARC para Smalltalk a finales de la década de 1970, donde las vistas (observadores) escuchan los cambios en el modelo (sujeto).

Hoy en día, el patrón es fundamental en:

- Programación basada en eventos (eventos DOM, listeners de GUI)
- Programación reactiva (RxJS, Project Reactor)
- Frameworks de enlace de datos (Vue.js, Knockout, JavaFX)
- Mensajería distribuida (Kafka, MQTT)

## Casos de Uso Comunes

- **Sistemas GUI** – Clics de botón, movimientos del ratón, pulsaciones de teclas.
- **Enlace de datos** – Actualización automática de la interfaz de usuario cuando un modelo cambia.
- **Flujos reactivos** – Tuberías de datos asincrónicas con contrapresión.
- **Registro (logging)** – Distribución de mensajes de registro a múltiples destinos (consola, archivo, red).
- **Sistemas financieros** – Envío de actualizaciones de cotizaciones bursátiles a múltiples paneles.
- **Brokers de mensajería** – Publicador/suscriptor con brokers desacoplados.

---

*El patrón Observer sigue siendo una piedra angular de las arquitecturas basadas en eventos, permitiendo una comunicación limpia y mantenible entre componentes débilmente acoplados.*