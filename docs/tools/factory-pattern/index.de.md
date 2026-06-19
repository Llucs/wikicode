---
title: Fabrikmuster
description: Ein Erzeugungsmuster, das die Objekterstellung kapselt, den Client-Code von konkreten Implementierungen entkoppelt und Flexibilität fördert.
created: 2026-06-19
tags:
  - design-patterns
  - creational
  - object-oriented
  - gof
status: draft
---

# Factory Pattern

## Übersicht

Das Factory Pattern ist ein **Erzeugungsmuster** (creational design pattern), das eine Schnittstelle oder Methode zum Erstellen von Objekten bereitstellt, ohne die Instanziierungslogik gegenüber dem Client offenzulegen. Anstatt einen Konstruktor direkt mit `new` aufzurufen, delegiert der Client-Code die Erstellung an eine **Factory** – eine separate Klasse, Methode oder ein Objekt – die bzw. das basierend auf Eingabeparametern, Konfiguration oder Kontext entscheidet, welche konkrete Klasse instanziiert wird.

Dieses Muster ist eines der Entwurfsmuster der Gang of Four (GoF) und kommt in drei gängigen Varianten vor:

- **Simple Factory** – Eine einzelne Klasse/statische Methode, die basierend auf einem Parameter unterschiedliche konkrete Produkte zurückgibt.
- **Factory Method** – Eine Klasse definiert eine abstrakte Methode zur Erzeugung, und Unterklassen überschreiben sie, um spezifische Produkte zu erzeugen.
- **Abstract Factory** – Eine Schnittstelle zum Erstellen von Familien verwandter oder abhängiger Objekte, ohne deren konkrete Klassen festzulegen.

## Warum das Factory Pattern verwenden?

- **Entkopplung**: Der Client-Code hängt von Abstraktionen (Schnittstellen/abstrakten Klassen) ab, nicht von konkreten Implementierungen. Das Austauschen eines Produkttyps erfordert oft nur die Änderung der Factory-Logik, nicht des Clients.
- **Kapselung der Konstruktionslogik**: Komplexe Objektzusammenstellung, Abhängigkeitsverkabelung oder bedingte Instanziierung sind innerhalb der Factory verborgen.
- **Open/Closed-Prinzip**: Neue Produkttypen können durch Erweitern der Factory (oder Hinzufügen eines neuen konkreten Erzeugers) eingeführt werden, ohne vorhandenen Client-Code zu ändern.
- **Einzelverantwortung**: Die Erstellungslogik ist von der Geschäftslogik getrennt, wodurch jeder Teil wartbarer wird.
- **Polymorphismus bei der Erstellung**: Der Client interagiert mit einer einheitlichen Schnittstelle, ohne den tatsächlichen Laufzeittyp zu kennen.

## Installation / Voraussetzungen

Das Factory Pattern ist **keine Bibliothek oder kein Paket** – es ist eine Entwurfsmethodik, die vollständig auf standardmäßigen objektorientierten Programmierfunktionen (OOP) basiert. Es ist keine Installation erforderlich; es kann in jeder Sprache implementiert werden, die Folgendes unterstützt:

- Schnittstellen, abstrakte Klassen oder Duck Typing (Python)
- Vererbung und Polymorphismus
- Kapselung

Verfügbar in allen gängigen Sprachen: Java, C#, C++, Python, TypeScript, Ruby, etc.

## Schlüsselkonzepte

- **Produkt** – Der abstrakte/Schnittstellentyp, den die Factory zurückgibt.
- **Konkretes Produkt** – Eine Klasse, die die Produktschnittstelle implementiert.
- **Erzeuger** (Creator) – Die Klasse, die die Factory-Methode deklariert oder die Factory-Logik enthält.
- **Konkreter Erzeuger** – (Factory Method) Eine Unterklasse des Erzeugers, die die Factory-Methode überschreibt, um ein bestimmtes konkretes Produkt zu erzeugen.
- **Client** – Code, der das Produkt über die Factory verwendet, ohne jemals direkt Konstruktoren aufzurufen.

## Verwendung und Beispiele

### Simple Factory (Python)

```python
from abc import ABC, abstractmethod

# Abstract product
class Document(ABC):
    @abstractmethod
    def open(self) -> str:
        pass

# Concrete products
class PDFDocument(Document):
    def open(self) -> str:
        return "Opening PDF document..."

class WordDocument(Document):
    def open(self) -> str:
        return "Opening Word document..."

class HTMLDocument(Document):
    def open(self) -> str:
        return "Opening HTML document..."

# Factory (Simple Factory)
class DocumentFactory:
    @staticmethod
    def create_document(doc_type: str) -> Document:
        factories = {
            "pdf": PDFDocument,
            "word": WordDocument,
            "html": HTMLDocument,
        }
        if doc_type not in factories:
            raise ValueError(f"Unknown document type: {doc_type}")
        return factories[doc_type]()

# Client code
doc = DocumentFactory.create_document("pdf")
print(doc.open())  # Opening PDF document...
```

### Factory Method (C#)

```csharp
// Product
public abstract class Logger
{
    public abstract void Log(string message);
}

// Concrete Products
public class ConsoleLogger : Logger
{
    public override void Log(string message) =>
        Console.WriteLine($"[Console] {message}");
}

public class FileLogger : Logger
{
    public override void Log(string message)
    {
        File.AppendAllText("log.txt", $"[File] {message}\n");
    }
}

// Creator
public abstract class LoggerFactory
{
    public abstract Logger CreateLogger();

    public void LogMessage(string message)
    {
        var logger = CreateLogger();
        logger.Log(message);
    }
}

// Concrete Creators
public class ConsoleLoggerFactory : LoggerFactory
{
    public override Logger CreateLogger() => new ConsoleLogger();
}

public class FileLoggerFactory : LoggerFactory
{
    public override Logger CreateLogger() => new FileLogger();
}

// Client
class Client
{
    static void Main()
    {
        LoggerFactory factory = new ConsoleLoggerFactory();
        factory.LogMessage("Factory Method pattern in action");
    }
}
```

### Abstract Factory (Java)

```java
// Abstract product - Button
interface Button {
    void paint();
}

// Concrete product classes
class WindowsButton implements Button {
    public void paint() {
        System.out.println("Rendering a Windows-style button");
    }
}

class MacOSButton implements Button {
    public void paint() {
        System.out.println("Rendering a macOS-style button");
    }
}

// Abstract product – Checkbox
interface Checkbox {
    void check();
}

class WindowsCheckbox implements Checkbox {
    public void check() {
        System.out.println("Checked Windows checkbox");
    }
}

class MacOSCheckbox implements Checkbox {
    public void check() {
        System.out.println("Checked macOS checkbox");
    }
}

// Abstract factory
interface GUIFactory {
    Button createButton();
    Checkbox createCheckbox();
}

// Concrete factories for each OS
class WindowsFactory implements GUIFactory {
    public Button createButton() {
        return new WindowsButton();
    }
    public Checkbox createCheckbox() {
        return new WindowsCheckbox();
    }
}

class MacOSFactory implements GUIFactory {
    public Button createButton() {
        return new MacOSButton();
    }
    public Checkbox createCheckbox() {
        return new MacOSCheckbox();
    }
}

// Client
public class Application {
    private GUIFactory factory;

    public Application(GUIFactory factory) {
        this.factory = factory;
    }

    public void renderUI() {
        Button button = factory.createButton();
        button.paint();
        Checkbox checkbox = factory.createCheckbox();
        checkbox.check();
    }

    public static void main(String[] args) {
        String osName = System.getProperty("os.name").toLowerCase();
        GUIFactory factory;
        if (osName.contains("win")) {
            factory = new WindowsFactory();
        } else {
            factory = new MacOSFactory();
        }
        Application app = new Application(factory);
        app.renderUI();
    }
}
```

## Hauptmerkmale

| Merkmal | Beschreibung |
|---------|--------------|
| **Kapselung der Erstellung** | Verbirgt komplexe Instanziierungslogik, Abhängigkeitsverwaltung und Objektzusammenstellung. |
| **Entkopplung** | Der Client-Code hängt nur von Abstraktionen ab, nicht von konkreten Klassen. |
| **Open/Closed-Prinzip** | Das Hinzufügen neuer Produkte erfordert oft nur das Hinzufügen neuer Factory-Unterklassen (oder neuer Einträge in einer Registrierung), ohne vorhandenen Client-Code zu ändern. |
| **Einzelverantwortung** | Die Erstellungslogik ist in der Factory lokalisiert und nicht über die Codebasis verstreut. |
| **Polymorphismus in der Konstruktion** | Das zurückgegebene Produkt wird über seine Schnittstelle verwendet; die tatsächliche Klasse kann zur Laufzeit variieren. |
| **Bedingte Objekterstellung** | Fabriken zentralisieren if-else- oder switch-Logik, die entscheidet, welches Objekt erstellt werden soll, was die Wartung und Erweiterung erleichtert. |

## Best Practices

- **Abhängigkeiten von Abstraktionen, nicht von Konkretionen.** Der Client sollte immer über die Produktschnittstelle operieren, niemals über eine konkrete Klasse.
- **Halte Fabriken fokussiert.** Eine Factory sollte nur die Objekterstellung übernehmen; vermeide die Vermischung mit Geschäftslogik.
- **Verwende ein Register oder eine Map** in deiner Factory, um if-else-Ketten zu reduzieren und das Hinzufügen neuer Typen trivial zu machen (siehe das Python Simple Factory Beispiel oben).
- **Erwäge parametrisierte Fabriken**, die ein `type`- oder `config`-Objekt akzeptieren, um zu entscheiden, welches konkrete Produkt instanziiert werden soll.
- **Kombiniere mit Dependency Injection.** Fabriken können in Clients injiziert werden, um die Kopplung weiter zu reduzieren und Tests zu ermöglichen.

## Häufige Fallstricke

- **Over‑Engineering**: Nicht jedes Objekt benötigt eine Factory; verwende sie nur, wenn die Erstellungslogik komplex ist, variiert oder zentralisiert werden muss.
- **Zu viele Fabriken**: Jedes Produkt, das seine eigene Factory hervorbringt, kann zu unnötiger Komplexität führen. Bewerte, ob eine einfachere Factory (oder keine Factory) ausreicht.
- **Die Factory verbirgt zu viel**: Wenn die Factory es schwieriger macht, Objektlebenszyklen zu verfolgen oder unsichtbare Seiteneffekte einführt, überdenke das Design.
- **Mischen von Simple Factory und Factory Method**: Es sind unterschiedliche Muster. Simple Factory verwendet eine statische Methode; Factory Method verwendet Vererbung und Polymorphismus. Wähle die richtige Variante für dein Szenario.

## Verwandte Muster

- **Abstract Factory** – Oft auf Basis mehrerer Factory Methods aufgebaut; befasst sich mit Produktfamilien.
- **Singleton** – Eine Factory kann als Singleton implementiert werden, wenn nur eine Instanz benötigt wird.
- **Prototyp** – Anstatt Objekte von Grund auf neu zu erstellen, wird ein Prototyp verwendet, um vorhandene zu klonen.
- **Erbauer** (Builder) – Trennt die Konstruktion eines komplexen Objekts von seiner Darstellung; im Gegensatz zur Factory, die das Produkt typischerweise in einem Schritt zurückgibt.
- **Schablonenmethode** (Template Method) – Die Factory Method wird oft innerhalb einer Template Method verwendet, damit Unterklassen das erstellte Produkt definieren können.

## Weiterführende Literatur

- *Design Patterns: Elements of Reusable Object-Oriented Software* – Gamma, Helm, Johnson, Vlissides (GoF).
- *Head First Design Patterns* – Freeman & Freeman.
- [Refactoring Guru – Factory Method](https://refactoring.guru/design-patterns/factory-method)
- [Wikipedia – Factory Method Pattern](https://en.wikipedia.org/wiki/Factory_method_pattern)
- [SourceMaking – Factory Design Pattern](https://sourcemaking.com/design_patterns/factory_method)