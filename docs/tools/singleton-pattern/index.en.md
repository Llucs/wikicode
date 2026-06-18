---
title: Singleton Pattern – Ensure a Class Has Only One Instance
description: The Singleton is a creational design pattern that restricts a class to a single instance and provides a global point of access to it, commonly used for logging, configuration, and resource management.
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

The **Singleton Pattern** is a creational design pattern from the Gang of Four (GoF) catalog. Its purpose is to **ensure that a class has only one instance** and to provide a **global access point** to that instance. Unlike a static utility class, a Singleton can participate in inheritance, implement interfaces, support lazy initialization, and be passed as an object reference.

---

## Why Use the Singleton Pattern?

Singletons are used when exactly one object is needed to coordinate actions across a system. Common use cases include:

- **Logging** – Centralize log output to a single file or stream.
- **Configuration** – Load application settings once and share them.
- **Resource Pools** – Manage a fixed set of database connections or thread pools.
- **Caching** – Maintain a single in-memory cache.
- **Hardware Controllers** – Interface with a single physical device (printer, GPU).

**Benefits:**
- Controlled access to a unique instance.
- Lazy instantiation saves resources if the object is never used.
- Can be subclassed (though rarely) and used polymorphically.

---

## Key Characteristics (GoF Definition)

1. **Private constructor** – Prevents external instantiation.
2. **Static member** that holds the single instance.
3. **Public static method** (`getInstance()`) – The sole way to obtain the instance.
4. **Lazy initialization** – The instance is created only when first requested (unless eager initialization is used).
5. **Thread safety** – Must guard against concurrent creation of multiple instances.

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

**Warning:** This version breaks in a multithreaded environment—two threads could each see `instance == null` and create separate objects.

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

The `synchronized` keyword adds a performance overhead, but it works.

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

- Instance is created when the class is loaded; thread‑safe by the class loader.
- If the object is never used, resource is still allocated.

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

- Reduces overhead after the instance is created.
- Requires `volatile` keyword (Java 5+) to prevent partial construction reads.

### Enum Singleton (Java Best Practice)

```java
public enum Logger {
    INSTANCE;

    public void log(String message) {
        System.out.println(message);
    }
}
```

- **Inherently thread‑safe** and protects against reflection, serialization, and cloning attacks.
- This is the recommended approach in Java (Effective Java, Item 3).

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

**The Singleton pattern is not a library or package.** It is an architectural design implemented directly in your source code. You do not install it via npm, pip, Maven, or NuGet. To “adopt” the pattern, you write the necessary class as shown in the examples above.

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

**Usage:**

```csharp
string connStr = AppConfig.Instance.DbConnectionString;
```

---

## Criticisms (Why Some Call It an Anti‑Pattern)

- **Global State** – The Singleton introduces mutable global state, which makes unit tests order‑dependent and brittle.
- **Tight Coupling** – `getInstance()` forces code to depend on the concrete class, violating the Dependency Inversion Principle.
- **Hidden Dependencies** – A class that uses a Singleton does not declare it in its constructor; the dependency is buried inside methods, making the API unclear.
- **Single Responsibility Violation** – The class must manage its own lifecycle (lazy initialization, thread safety) in addition to its core logic.

---

## Modern Alternatives

- **Dependency Injection (DI)** – An IoC container (Spring, Guice, ASP.NET Core) manages object lifetimes. A class can be registered with *singleton scope*, but consumers depend on an interface, allowing easy mocking and swapping.
- **Monostate Pattern** – A variation where the class itself is not a singleton, but all its fields are static. Multiple instances share the same state.
- **Static Utility Class** – Works for stateless helpers but cannot implement interfaces or benefit from polymorphism.

---

## Conclusion

The Singleton pattern is a powerful tool when used deliberately. Modern best practices favor dependency injection over direct singletons because it improves testability and maintainability. When you must enforce a single instance, prefer **enum‑based** (Java) or `Lazy<T>` (C#) implementations to avoid thread‑safety pitfalls. Remember that “global access” is also global coupling—use Singletons sparingly and consciously.

---

*References:*  
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object‑Oriented Software*. Addison‑Wesley.  
- Bloch, J. (2008). *Effective Java* (2nd ed., Item 3). Addison‑Wesley.  
- Martin, R. C. (2003). *Agile Software Development, Principles, Patterns, and Practices*. Prentice Hall.