---
title: Verhaltensdesignmuster
description: Fokussiert auf Objekteinträge und Kommunikation, einschließlich Mustern wie Beobachter und Strategie.
created: 2026-06-28
tags:
  - Designmuster
  - Softwareentwicklung
  - Objektorientierte Programmierung
status: entwurf
---

# Verhaltensdesignmuster

Verhaltensdesignmuster sind eine Kategorie von Softwaredesignmustern, die Algorithmen und Kommunikation zwischen Objekten behandeln. Diese Muster sind sich auf die Interaktionen zwischen Objekten und die Weise konzentriert, wie sie miteinander kommunizieren, um ein bestimmtes Verhalten zu erzielen. Sie helfen bei der Verwaltung komplexer Kontrollflüsse und vereinfachen die Kommunikation zwischen Objekten.

## Übersicht

Verhaltensdesignmuster sind sich auf die Interaktion und die Verantwortung von Objekten konzentriert. Diese Muster helfen bei der Verwaltung der Objekteinträge und Verantwortlichkeiten in einem System, indem sie es einfacher machen, das System zu verwalten und auszuführen. Sie fördern die Wiederverwendbarkeit des Codes durch die Verschachtelung von Verhalten in getrennten Klassen.

## Schlüsselverhaltensdesignmuster

### 1. Strategie-Muster

#### Definition
Das Strategie-Muster definiert eine Familie von Algorithmen, encapsuliert jede davon und macht sie austauschbar.

#### Schlüsselmerkmale
- Encapsuliert eine Familie von Algorithmen.
- Erlaubt die Auswahl von Algorithmen zur Laufzeit.
- Bietet eine Schnittstelle für Algorithmen, versteckt dabei ihre Implementierungsdetails.

#### Geschichte
Einführt in dem Buch "Design Patterns: Elemente wiederverwendbarer objektorientierter Software" von Erich Gamma et al., veröffentlicht 1994.

#### Einsatzfälle
- Verwendet in Systemen, in denen Algorithmen dynamisch geändert oder ausgewählt werden müssen, wie bei Sortieralgorithmen, Zahlungssystemen und verschiedenen Protokollniveaus.

#### Basiskonzept
Definiere eine Schnittstelle für einen Algorithmus, implementiere verschiedene Algorithmen und kapsülle jedes in einer separaten Klasse. Die Kontextklasse verwendet die Schnittstelle, um mit den Algorithmen zu interagieren.

```java
public interface Strategy {
    void algorithmInterface();
}

public class ConcreteStrategyA implements Strategy {
    public void algorithmInterface() {
        System.out.println("Führe Strategie A aus");
    }
}

public class ConcreteStrategyB implements Strategy {
    public void algorithmInterface() {
        System.out.println("Führe Strategie B aus");
    }
}

public class Context {
    private Strategy strategy;

    public void setStrategy(Strategy strategy) {
        this.strategy = strategy;
    }

    public void executeAlgorithm() {
        strategy.algorithmInterface();
    }
}

public class Main {
    public static void main(String[] args) {
        Context context = new Context();
        context.setStrategy(new ConcreteStrategyA());
        context.executeAlgorithm(); // Ausgabe: Führe Strategie A aus

        context.setStrategy(new ConcreteStrategyB());
        context.executeAlgorithm(); // Ausgabe: Führe Strategie B aus
    }
}
```

### 2. Beobachter-Muster

#### Definition
Das Beobachter-Muster definiert eine Abhängigkeit zwischen Objekten, sodass, wenn eines Objekts Zustand sich ändert, alle seine Abhängigen automatisch informiert und aktualisiert werden.

#### Schlüsselmerkmale
- Das Subjekt hält eine Liste von Beobachtern.
- Erlaubt eine Abonnement- und Abmeldung-Mechanik.
- Informiert die Beobachter, wenn das Zustand sich ändert.

#### Geschichte
Einführt ebenfalls in dem Buch "Design Patterns: Elemente wiederverwendbarer objektorientierter Software".

#### Einsatzfälle
- Verwendet in GUI-Systemen, Ereignishandlungs-Systemen und in jedem System, in dem Änderungen eines Objekts andere Objekte ändern sollten.

#### Basiskonzept
Definiere eine `Beobachter`-Schnittstelle, erstelle Beobachter-Klassen und implementiere ein `Subjekt`, das eine Liste von Beobachtern hält und sie bei Zustandsänderungen informiert.

```java
public interface Observer {
    void update(String message);
}

public class ConcreteObserver implements Observer {
    public void update(String message) {
        System.out.println("Beobachter erhielt Nachricht: " + message);
    }
}

public class Subject {
    private List<Observer> observers = new ArrayList<>();

    public void addObserver(Observer observer) {
        observers.add(observer);
    }

    public void removeObserver(Observer observer) {
        observers.remove(observer);
    }

    public void notifyObservers(String message) {
        for (Observer observer : observers) {
            observer.update(message);
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Subject subject = new Subject();
        Observer observer1 = new ConcreteObserver();
        Observer observer2 = new ConcreteObserver();

        subject.addObserver(observer1);
        subject.addObserver(observer2);

        subject.notifyObservers("Hallo, Beobachter-Muster!"); // Ausgabe: Beobachter erhielt Nachricht: Hallo, Beobachter-Muster!
                                                              //        Beobachter erhielt Nachricht: Hallo, Beobachter-Muster!
    }
}
```

### 3. Befehlsmuster

#### Definition
Das Befehlsmuster verwandelt eine Anfrage in eine eigenständige Instanz, die alle Informationen über die Anfrage enthält.

#### Schlüsselmerkmale
- Encapsuliert eine Anfrage als Objekt.
- Erlaubt die Verparameterisierung von Methoden durch unterschiedliche Anfragen, Verzögerung oder Wartung von Anfragen.
- Erlaubt unumkehrbare Operationen.

#### Geschichte
Einführt in dem Buch "Design Patterns: Elemente wiederverwendbarer objektorientierter Software".

#### Einsatzfälle
- Verwendet in GUIs, unumkehrbaren Operationen und in jedem System, in dem Anfragen verparameterisiert werden müssen.

#### Basiskonzept
Definiere eine `Befehl`-Schnittstelle, erstelle konkrete Befehl-Klassen und führe Befehle durch eine `Befehl`-Instanz aus.

```java
public interface Command {
    void execute();
}

public class ConcreteCommand implements Command {
    private Receiver receiver;

    public ConcreteCommand(Receiver receiver) {
        this.receiver = receiver;
    }

    public void execute() {
        receiver.action();
    }
}

public class Receiver {
    public void action() {
        System.out.println("Führe Receiver-Aktion aus");
    }
}

public class Invoker {
    private Command command;

    public void setCommand(Command command) {
        this.command = command;
    }

    public void executeCommand() {
        command.execute();
    }
}

public class Main {
    public static void main(String[] args) {
        Receiver receiver = new Receiver();
        Command command = new ConcreteCommand(receiver);
        Invoker invoker = new Invoker();
        invoker.setCommand(command);
        invoker.executeCommand(); // Ausgabe: Führe Receiver-Aktion aus
    }
}
```

### 4. Besucher-Muster

#### Definition
Das Besucher-Muster repräsentiert eine Operation, die auf den Elementen einer Objektstruktur durchgeführt wird.

#### Schlüsselmerkmale
- Encapsuliert eine Operation auf den Elementen einer Objektschicht.
- Erlaubt die Hinzufügung neuer Operationen ohne Änderung der Elementklassen.

#### Geschichte
Einführt in dem Buch "Design Patterns: Elemente wiederverwendbarer objektorientierter Software".

#### Einsatzfälle
- Verwendet in Systemen, in denen neue Operationen zu einer Klassenshicht hinzugefügt werden müssen, ohne dass vorhandene Klassen geändert werden, wie in AST-Durchläufen.

#### Basiskonzept
Definiere eine `Besucher`-Schnittstelle, implementiere die Operation in Besucher-Klassen und wende diese Besucher auf Elementen in der Struktur an.

```java
public interface Visitor {
    void visitConcreteElementA(ConcreteElementA element);
    void visitConcreteElementB(ConcreteElementB element);
}

public class ConcreteElementA {
    public void accept(Visitor visitor) {
        visitor.visitConcreteElementA(this);
    }
}

public class ConcreteElementB {
    public void accept(Visitor visitor) {
        visitor.visitConcreteElementB(this);
    }
}

public class ConcreteVisitorA implements Visitor {
    public void visitConcreteElementA(ConcreteElementA element) {
        System.out.println("Besuchte ConcreteElementA");
    }

    public void visitConcreteElementB(ConcreteElementB element) {
        System.out.println("Besuchte ConcreteElementB");
    }
}

public class Main {
    public static void main(String[] args) {
        ConcreteElementA elementA = new ConcreteElementA();
        ConcreteElementB elementB = new ConcreteElementB();
        Visitor visitor = new ConcreteVisitorA();

        elementA.accept(visitor); // Ausgabe: Besuchte ConcreteElementA
        elementB.accept(visitor); // Ausgabe: Besuchte ConcreteElementB
    }
}
```

### 5. Memento-Muster

#### Definition
Das Memento-Muster fängt das internen Zustand eines Objekts ein, ohne die Verpackung zu verletzen, und ermöglicht es dem Objekt, diesen Zustand wiederherzustellen.

#### Schlüsselmerkmale
- Encapsuliert das internen Zustand eines Objekts.
- Bietet ein Mechanismus, um diesen Zustand wiederherzustellen.

#### Geschichte
Einführt in dem Buch "Design Patterns: Elemente wiederverwendbarer objektorientierter Software".

#### Einsatzfälle
- Verwendet in Systemen, die einen Zustandsabzug benötigen, wie in Textbearbeitungsprogrammen oder Spielen.

#### Basiskonzept
Definiere eine `Memento`-Klasse, um den Zustand zu speichern, eine `Caretaker`-Klasse, um Mementos zu verwalten, und eine `Originator`-Klasse, die den Zustand hält und ihn von Mementos wiederherstellen kann.

```java
public class Originator {
    private String state;

    public void setState(String state) {
        this.state = state;
    }

    public Memento saveStateToMemento() {
        return new Memento(state);
    }

    public void restoreStateFromMemento(Memento memento) {
        this.state = memento.getState();
    }

    public String getState() {
        return state;
    }

    public class Memento {
        private String state;

        public Memento(String state) {
            this.state = state;
        }

        public String getState() {
            return state;
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Originator originator = new Originator();
        originator.setState("Anfangszustand");
        System.out.println("Derzeitiger Zustand: " + originator.getState()); // Ausgabe: Derzeitiger Zustand: Anfangszustand

        Memento memento = originator.saveStateToMemento();

        originator.setState("Neuer Zustand");
        System.out.println("Derzeitiger Zustand: " + originator.getState()); // Ausgabe: Derzeitiger Zustand: Neuer Zustand

        originator.restoreStateFromMemento(memento);
        System.out.println("Derzeitiger Zustand nach Wiederherstellung: " + originator.getState()); // Ausgabe: Derzeitiger Zustand nach Wiederherstellung: Anfangszustand
    }
}
```

### 6. Vorlagenmethode-Muster

#### Definition
Das Vorlagenmethode-Muster definiert den Rahmen eines Algorithmus in einer Methode, indem bestimmte Schritte an Unterklassen delegiert werden.

#### Schlüsselmerkmale
- Delegiert bestimmte Schritte an Unterklassen.
- Definiert einen Algorithmuskern in einer Oberklasse.
- Erlaubt Unterklassen, bestimmte Schritte zu überschreiben.

#### Geschichte
Einführt in dem Buch "Design Patterns: Elemente wiederverwendbarer objektorientierter Software".

#### Einsatzfälle
- Verwendet in Systemen, die einen Algorithmuskern definieren müssen, aber bestimmte Schritte anpassen können, wie in Systemen, die eine standardmäßige Verarbeitung schrittweise definieren.

#### Basiskonzept
Definiere eine Vorlagenmethode in einer Oberklasse, implementiere Schritte in der Vorlagenmethode und ermöglicht Unterklassen, bestimmte Schritte zu überschreiben.

```java
public abstract class Vorlagenmethode {
    public final void templateMethod() {
        step1();
        step2();
        step3();
    }

    protected abstract void step1();
    protected abstract void step2();
    protected abstract void step3();

    public void anotherOperation() {
        System.out.println("Eine andere Operation");
    }
}

public class KonkreteKlasse extends Vorlagenmethode {
    @Override
    protected void step1() {
        System.out.println("Exekutiere Schritt 1");
    }

    @Override
    protected void step2() {
        System.out.println("Exekutiere Schritt 2");
    }

    @Override
    protected void step3() {
        System.out.println("Exekutiere Schritt 3");
    }
}

public class Main {
    public static void main(String[] args) {
        Vorlagenmethode vorlagenmethode = new KonkreteKlasse();
        vorlagenmethode.templateMethod(); // Ausgabe: Exekutiere Schritt 1
                                          //        Exekutiere Schritt 2
                                          //        Exekutiere Schritt 3
    }
}
```

## Schluss

Verhaltensdesignmuster sind in der Softwareentwicklung wichtig, um übliche Designprobleme zu lösen und den Flexibilität und Wartbarkeit des Codes zu verbessern. Durch die Verwendung dieser Muster können Entwickler modulärere und anpassungsfähigere Systeme erstellen.

## Weiterführende Literatur

- [Design Patterns: Elemente wiederverwendbarer objektorientierter Software](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Verhaltensdesignmuster](https://refactoring.guru/design-patterns/behavioral-patterns)

---