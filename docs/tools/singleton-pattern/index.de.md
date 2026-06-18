---
title: Singleton-Pattern – Sicherstellen, dass eine Klasse nur eine Instanz hat
description: Das Singleton ist ein Erzeugungsmuster, das eine Klasse auf eine einzige Instanz beschränkt und einen globalen Zugriffspunkt darauf bereitstellt. Es wird häufig für Logging, Konfiguration und Ressourcenverwaltung verwendet.
created: 2026-06-18
tags:
  - singleton
  - design-patterns
  - creational
  - gang-of-four
  - java
  - csharp
  - python
  - software-engineering
status: draft
---

# Singleton Pattern

Das **Singleton Pattern** ist ein Erzeugungsmuster (Creational Design Pattern) aus dem Katalog der Gang of Four (GoF). Sein Zweck ist es, **sicherzustellen, dass eine Klasse nur eine Instanz hat**, und einen **globalen Zugriffspunkt** auf diese Instanz bereitzustellen. Im Gegensatz zu einer statischen Hilfsklasse kann ein Singleton an Vererbung teilnehmen, Schnittstellen implementieren, Lazy Initialization unterstützen und als Objektreferenz übergeben werden.

---

## Why Use the Singleton Pattern?

Singletons werden verwendet, wenn genau ein Objekt benötigt wird, um Aktionen über ein System hinweg zu koordinieren. Häufige Anwendungsfälle sind:

- **Logging** – Zentralisieren der Logausgabe in einer einzigen Datei oder einem Stream.
- **Configuration** – Anwendungseinstellungen einmal laden und gemeinsam nutzen.
- **Resource Pools** – Verwalten eines festen Satzes von Datenbankverbindungen oder Threadpools.
- **Caching** – Verwalten eines einzigen Caches im Arbeitsspeicher.
- **Hardware Controllers** – Schnittstelle zu einem einzelnen physischen Gerät (Drucker, GPU).

**Vorteile:**
- Kontrollierter Zugriff auf eine eindeutige Instanz.
- Lazy Instantierung spart Ressourcen, falls das Objekt nie verwendet wird.
- Kann (wenn auch selten) Unterklassen bilden und polymorph verwendet werden.

---

## Key Characteristics (GoF Definition)

1. **Privater Konstruktor** – Verhindert externe Instantiierung.
2. **Statisches Element** (Member), das die einzige Instanz hält.
3. **Öffentliche statische Methode** (`getInstance()`) – Der einzige Weg, die Instanz zu erhalten.
4. **Lazy Initialization** – Die Instanz wird nur erstellt, wenn sie zum ersten Mal angefordert wird (es sei denn, es wird Eager Initialization verwendet).
5. **Thread-Sicherheit** – Muss vor gleichzeitiger Erstellung mehrerer Instanzen schützen.

---

## Implementation (How to Code It)

### Basic Lazy Singleton (Not Thread‑Safe)

```java
public class Logger {
    private static Logger instance;

    private Logger() {}

    public static Logger getInstance() {
        if (instance == null) {
            instance = new Logger();
        }
        return instance;
    }

    public void log(String message) {
        System.out.println(message);
    }
}
```

**Warnung:** Diese Version funktioniert in einer Multithread-Umgebung nicht korrekt – zwei Threads könnten jeweils `instance == null` sehen und separate Objekte erstellen.

### Thread‑Safe Singleton (Synchronized Accessor)

```java
public class Logger {
    private static Logger instance;

    private Logger() {}

    public static synchronized Logger getInstance() {
        if (instance == null) {
            instance = new Logger();
        }
        return instance;
    }
}
```

Das `synchronized`-Schlüsselwort verursacht einen Performance-Overhead, funktioniert aber.

### Eager Initialization (Relies on Class Loader)

```java
public class Logger {
    private static final Logger INSTANCE = new Logger();

    private Logger() {}

    public static Logger getInstance() {
        return INSTANCE;
    }
}
```

- Die Instanz wird beim Laden der Klasse erstellt; Thread‑Sicherheit wird durch den Class Loader gewährleistet.
- Wenn das Objekt nie verwendet wird, wird trotzdem Ressource belegt.

### Double‑Checked Locking (with `volatile`)

```java
public class Logger {
    private static volatile Logger instance;

    private Logger() {}

    public static Logger getInstance() {
        if (instance == null) {
            synchronized (Logger.class) {
                if (instance == null) {
                    instance = new Logger();
                }
            }
        }
        return instance;
    }
}
```

- Reduziert den Overhead nach der Erstellung der Instanz.
- Erfordert das Schlüsselwort `volatile` (Java 5+), um das Lesen teilweise konstruierter Instanzen zu verhindern.

### Enum Singleton (Java Best Practice)

```java
public enum Logger {
    INSTANCE;

    public void log(String message) {
        System.out.println(message);
    }
}
```

- **Inhärent Thread‑sicher** und schützt vor Reflection‑, Serialisierungs- und Klonangriffen.
- Dies ist der empfohlene Ansatz in Java (Effective Java, Item 3).

### C# Example (Lazy + Thread‑Safe)

```csharp
public sealed class Logger
{
    private static readonly Lazy<Logger> lazy =
        new Lazy<Logger>(() => new Logger());

    public static Logger Instance => lazy.Value;

    private Logger() {}

    public void Log(string message) => Console.WriteLine(message);
}
```

### Python Example (Module‑Level Singleton)

```python
class _Logger:
    def log(self, msg):
        print(msg)

# Module-level variable acts as the single instance
logger = _Logger()
```

```python
# More explicit approach using __new__
class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def log(self, msg):
        print(msg)
```

---

## Installation

**Das Singleton-Pattern ist keine Bibliothek oder kein Paket.** Es ist ein architektonisches Entwurfsmuster, das direkt in Ihrem Quellcode implementiert wird. Sie installieren es nicht über npm, pip, Maven oder NuGet. Um das Pattern zu „übernehmen“, schreiben Sie die notwendige Klasse wie in den obigen Beispielen gezeigt.

---

## Usage Examples

### Logging with the Enum Singleton (Java)

```java
Logger.INSTANCE.log("Application started");

// In another class:
Logger.INSTANCE.log("User logged in");
```

### Configuration Manager (C#)

```csharp
public sealed class AppConfig
{
    private static readonly Lazy<AppConfig> lazy =
        new Lazy<AppConfig>(() => new AppConfig());

    public static AppConfig Instance => lazy.Value;

    public string DbConnectionString { get; private set; }
    public int MaxThreads { get; private set; }

    private AppConfig()
    {
        // Load from appsettings.json or environment
        DbConnectionString = "Server=myServer;Database=myDB;";
        MaxThreads = 10;
    }
}
```

**Verwendung:**

```csharp
string connStr = AppConfig.Instance.DbConnectionString;
```

---

## Criticisms (Why Some Call It an Anti‑Pattern)

- **Globaler Zustand (Global State)** – Das Singleton führt einen veränderlichen globalen Zustand ein, der Komponententests reihenfolgeabhängig und fragil macht.
- **Enge Kopplung (Tight Coupling)** – `getInstance()` zwingt den Code dazu, von der konkreten Klasse abzuhängen, was das Dependency Inversion Principle verletzt.
- **Versteckte Abhängigkeiten (Hidden Dependencies)** – Eine Klasse, die ein Singleton verwendet, deklariert es nicht in ihrem Konstruktor; die Abhängigkeit ist in Methoden versteckt, was die API unklar macht.
- **Verletzung der einzigen Verantwortlichkeit (Single Responsibility Violation)** – Die Klasse muss neben ihrer Kernlogik auch ihren eigenen Lebenszyklus verwalten (Lazy Initialization, Thread‑Sicherheit).

---

## Modern Alternatives

- **Dependency Injection (DI)** – Ein IoC‑Container (Spring, Guice, ASP.NET Core) verwaltet die Lebensdauer von Objekten. Eine Klasse kann mit *Singleton Scope* registriert werden, aber die Konsumenten hängen von einem Interface ab, was einfaches Mocking und Austauschen ermöglicht.
- **Monostate Pattern** – Eine Variante, bei der die Klasse selbst kein Singleton ist, aber alle ihre Felder statisch sind. Mehrere Instanzen teilen sich denselben Zustand.
- **Static Utility Class** – Funktioniert für zustandslose Helfer, kann aber keine Schnittstellen implementieren oder von Polymorphie profitieren.

---

## Conclusion

Das Singleton-Pattern ist ein mächtiges Werkzeug, wenn es bewusst eingesetzt wird. Moderne Best Practices bevorzugen Dependency Injection gegenüber direkten Singletons, da dies die Testbarkeit und Wartbarkeit verbessert. Wenn Sie eine einzige Instanz erzwingen müssen, bevorzugen Sie **enum‑basierte** (Java) oder `Lazy<T>`- (C#) Implementierungen, um Fallstricke bei der Thread‑Sicherheit zu vermeiden. Denken Sie daran, dass „globaler Zugriff“ auch globale Kopplung bedeutet – verwenden Sie Singletons sparsam und bewusst.

---

*References:*  
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object‑Oriented Software*. Addison‑Wesley.  
- Bloch, J. (2008). *Effective Java* (2nd ed., Item 3). Addison‑Wesley.  
- Martin, R. C. (2003). *Agile Software Development, Principles, Patterns, and Practices*. Prentice Hall.