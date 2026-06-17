---
title: Padrão de Design Observer
description: Um padrão de design comportamental que define uma dependência de um para muitos entre objetos, de modo que quando um objeto muda de estado, todos os seus dependentes são notificados e atualizados automaticamente.
created: 2026-06-16
tags:
  - design-patterns
  - behavioral
  - observer
  - publish-subscribe
  - event-driven
status: draft
---

# Padrão de Design Observer

## O Que É

O **padrão Observer** é um padrão de design comportamental onde um objeto, chamado **Sujeito** (ou **Observável**), mantém uma lista de seus dependentes, chamados **Observadores**, e os notifica automaticamente sobre quaisquer mudanças de estado, geralmente chamando um de seus métodos. Ele estabelece uma dependência de um para muitos, de modo que quando o sujeito muda de estado, todos os seus observadores são atualizados automaticamente. O padrão também é conhecido como *Publish-Subscribe*, *Event Listener* ou *Dependents*.

```plaintext
Subject ──→ Observer 1
         ├→ Observer 2
         └→ Observer 3
```

## Por Que Usar?

- **Acoplamento fraco** – O sujeito apenas sabe que os observadores implementam uma interface específica; ele não depende de classes de observador concretas.
- **Assinaturas dinâmicas** – Observadores podem ser adicionados ou removidos em tempo de execução sem modificar o sujeito.
- **Comunicação por transmissão** – Um único sujeito envia atualizações de forma eficiente para todos os observadores registrados.
- **Princípio Aberto/Fechado** – Novos observadores podem ser introduzidos sem alterar o código do sujeito.
- **Evita polling** – Observadores recebem atualizações automaticamente em vez de verificar repetidamente o estado do sujeito.

## Instalação

Como o padrão Observer é um conceito de design, ele é **implementado em código** em vez de instalado como um pacote. No entanto, muitas linguagens e bibliotecas fornecem suporte integrado:

| Linguagem / Plataforma | Integrado / Pacote |
|------------------------|--------------------|
| Node.js                | `EventEmitter` (módulo core `events`) |
| Python                 | `pip install rx` (ReactiveX) ou `Observable` via `asyncio` |
| JavaScript / TypeScript| `npm install rxjs` |
| Java                   | `java.beans.PropertyChangeSupport` ou `java.util.concurrent.Flow` |
| C#                     | Palavra-chave `event` e delegates da linguagem |

### Exemplos de comandos de instalação

```bash
# JavaScript/TypeScript (ReactiveX)
npm install rxjs

# Python (ReactiveX)
pip install rx

# For Node.js EventEmitter, no installation needed (core module)
```

## Principais Características

- **Notificação Um-para-Muitos** – Um único sujeito notifica vários observadores de forma consistente.
- **Acoplamento Fraco** – O sujeito depende apenas de uma interface de observador, não de implementações concretas.
- **Comunicação por Transmissão** – Mudanças de estado são enviadas a todos os observadores (ou puxadas via uma notificação).
- **Assinatura Dinâmica** – Observadores podem se inscrever ou cancelar a inscrição a qualquer momento.
- **Atualizações Automáticas** – Observadores permanecem sincronizados sem exigir polling.

## Exemplos de Uso

### Implementação Clássica em Python (Pura)

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

## Prós e Contras

### Prós

- **Acoplamento fraco** – Sujeito e observadores são independentes.
- **Reutilização** – Observadores podem ser reutilizados em diferentes sujeitos.
- **Relacionamentos dinâmicos** – As assinaturas podem mudar em tempo de execução.
- **Notificação automática** – Observadores são atualizados sem polling.

### Contras

- **Ordem imprevisível** – Observadores podem ser notificados em uma ordem arbitrária.
- **Vazamentos de memória** – Se os observadores não forem removidos corretamente, eles podem se acumular.
- **Cadeias de atualização complexas** – Atualizações reentrantes podem ser difíceis de depurar.
- **Sobrecarga de notificação** – Notificar muitos observadores pode ser custoso se não for projetado cuidadosamente.

## História e Contexto

O padrão Observer foi formalmente catalogado no livro de 1994 *Design Patterns: Elements of Reusable Object‑Oriented Software* pelo “Gang of Four” (Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides). Suas raízes conceituais estão na arquitetura **Model‑View‑Controller (MVC)** desenvolvida na Xerox PARC para Smalltalk no final dos anos 1970, onde as visões (observadores) escutam as mudanças no modelo (sujeito).

Hoje, o padrão é fundamental em:

- Programação orientada a eventos (eventos DOM, listeners GUI)
- Programação reativa (RxJS, Project Reactor)
- Frameworks de data binding (Vue.js, Knockout, JavaFX)
- Mensageria distribuída (Kafka, MQTT)

## Casos de Uso Comuns

- **Sistemas GUI** – Cliques de botão, movimentos do mouse, pressionamentos de tecla.
- **Data binding** – Atualizar automaticamente a UI quando um modelo muda.
- **Streams reativos** – Pipelines de dados assíncronos com contrapressão.
- **Registro de log** – Distribuir mensagens de log para vários destinos (console, arquivo, rede).
- **Sistemas financeiros** – Enviar atualizações de ticker de ações para múltiplos painéis.
- **Corretores de mensagens** – Publicador/assinante com corretores desacoplados.

---

*O padrão Observer permanece um pilar das arquiteturas orientadas a eventos, permitindo uma comunicação limpa e sustentável entre componentes fracamente acoplados.*