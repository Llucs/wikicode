---
title: Patron de conception Observateur
description: Un patron de conception comportemental qui définit une dépendance de un à plusieurs entre objets, de sorte que lorsqu'un objet change d'état, tous ses dépendants sont notifiés et mis à jour automatiquement.
created: 2026-06-16
tags:
  - design-patterns
  - behavioral
  - observer
  - publish-subscribe
  - event-driven
status: draft
---

# Patron de conception Observateur

## Qu'est-ce que c'est ?

Le **patron Observateur** est un patron de conception comportemental où un objet, appelé le **Sujet** (ou **Observable**), tient une liste de ses dépendants, appelés **Observateurs**, et les notifie automatiquement de tout changement d'état, généralement en appelant l'une de leurs méthodes. Il établit une dépendance un‑à‑plusieurs de sorte que lorsque le sujet change d'état, tous ses observateurs sont mis à jour automatiquement. Ce patron est également connu sous les noms de *Publish‑Subscribe*, *Event Listener* ou *Dependents*.

```plaintext
Subject ──→ Observer 1
         ├→ Observer 2
         └→ Observer 3
```

## Pourquoi l'utiliser ?

- **Couplage faible** – Le sujet sait seulement que les observateurs implémentent une interface spécifique ; il ne dépend pas de classes d'observateurs concrètes.
- **Abonnements dynamiques** – Les observateurs peuvent être ajoutés ou supprimés à l'exécution sans modifier le sujet.
- **Communication par diffusion** – Un seul sujet pousse efficacement les mises à jour vers tous les observateurs enregistrés.
- **Principe Open/Closed** – De nouveaux observateurs peuvent être introduits sans modifier le code du sujet.
- **Évite la scrutation** – Les observateurs reçoivent les mises à jour automatiquement au lieu de vérifier régulièrement l'état du sujet.

## Installation

Comme le patron Observateur est un concept de conception, il est **implémenté dans le code** plutôt qu'installé comme un package. Cependant, de nombreux langages et bibliothèques offrent un support intégré :

| Langage / Plateforme | Intégré / Paquet |
|---------------------|----------------------|
| Node.js             | `EventEmitter` (module central `events`) |
| Python              | `pip install rx` (ReactiveX) ou noyau `Observable` via `asyncio` |
| JavaScript / TypeScript | `npm install rxjs` |
| Java                | `java.beans.PropertyChangeSupport` ou `java.util.concurrent.Flow` |
| C#                  | Mot‑clé `event` du langage et délégués |

### Exemples de commandes d'installation

```bash
# JavaScript/TypeScript (ReactiveX)
npm install rxjs

# Python (ReactiveX)
pip install rx

# Pour Node.js EventEmitter, aucune installation nécessaire (module central)
```

## Fonctionnalités clés

- **Notification un‑à‑plusieurs** – Un seul sujet notifie plusieurs observateurs de manière cohérente.
- **Couplage faible** – Le sujet repose uniquement sur une interface d'observateur, pas sur des implémentations concrètes.
- **Communication par diffusion** – Les changements d'état sont poussés vers tous les observateurs (ou tirés via une notification).
- **Abonnement dynamique** – Les observateurs peuvent s'abonner ou se désabonner à tout moment.
- **Mises à jour automatiques** – Les observateurs restent synchronisés sans nécessiter de scrutation.

## Exemples d'utilisation

### Implémentation Python classique (pure)

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

### Java (utilisant `java.util.concurrent.Flow`)

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

## Avantages et inconvénients

### Avantages

- **Couplage faible** – Le sujet et les observateurs sont indépendants.
- **Réutilisabilité** – Les observateurs peuvent être réutilisés avec différents sujets.
- **Relations dynamiques** – Les abonnements peuvent changer à l'exécution.
- **Notification automatique** – Les observateurs sont mis à jour sans scrutation.

### Inconvénients

- **Ordre imprévisible** – Les observateurs peuvent être notifiés dans n'importe quel ordre.
- **Fuite de mémoire** – Si les observateurs ne sont pas correctement détachés, ils peuvent s'accumuler.
- **Chaînes de mise à jour complexes** – Les mises à jour réentrantes peuvent être difficiles à déboguer.
- **Surcharge de notification** – Notifier de nombreux observateurs peut être coûteux s'il n'est pas conçu avec soin.

## Historique et contexte

Le patron Observateur a été formellement catalogué dans le livre de 1994 *Design Patterns: Elements of Reusable Object‑Oriented Software* par le « Gang of Four » (Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides). Ses racines conceptuelles se trouvent dans l'architecture **Modèle‑Vue‑Contrôleur (MVC)** développée au Xerox PARC pour Smalltalk à la fin des années 1970, où les vues (observateurs) écoutent les changements du modèle (sujet).

Aujourd'hui, le patron est fondamental dans :

- La programmation événementielle (événements DOM, écouteurs d'interface graphique)
- La programmation réactive (RxJS, Project Reactor)
- Les frameworks de liaison de données (Vue.js, Knockout, JavaFX)
- La messagerie distribuée (Kafka, MQTT)

## Cas d'utilisation courants

- **Systèmes d'interface graphique** – Clics de boutons, mouvements de souris, pressions de touches.
- **Liaison de données** – Mise à jour automatique de l'interface utilisateur lorsqu'un modèle change.
- **Flux réactifs** – Pipelines de données asynchrones avec backpressure.
- **Journalisation** – Distribution de messages de journal vers plusieurs destinations (console, fichier, réseau).
- **Systèmes financiers** – Envoi de mises à jour des cours boursiers à plusieurs tableaux de bord.
- **Courtiers de messages** – Publieur/souscripteur avec courtiers découplés.

---

*Le patron Observateur reste une pierre angulaire des architectures événementielles, permettant une communication propre et maintenable entre des composants faiblement couplés.*