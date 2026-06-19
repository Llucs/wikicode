---
title: Factory Pattern
description: A creational design pattern that encapsulates object creation, decoupling client code from concrete implementations and promoting flexibility.
created: 2026-06-19
tags:
  - design-patterns
  - creational
  - object-oriented
  - gof
status: draft
---

# Factory Pattern

## Overview The Factory Pattern is a **creational design pattern** that provides an interface or method for creating objects without exposing the instantiation logic to the client. Instead of directly calling a constructor with `new`, client code delegates creation to a **factory** – a separate class, method, or object – which decides which concrete class to instantiate based on input parameters, configuration, or context.

This pattern is one of the Gang of Four (GoF) design patterns and comes in three common variants:

- **Simple Factory** – A single class/static method that returns different concrete products based on a parameter.
- **Factory Method** – A class defines an abstract method for creation, and subclasses override it to produce specific products.
- **Abstract Factory** – An interface for creating families of related or dependent objects without specifying their concrete classes.

## Why Use the Factory Pattern?

- **Decoupling**: Client code depends on abstractions (interfaces/abstract classes), not on concrete implementations. Swapping a product type often requires only changing the factory logic, not the client.
- **Encapsulation of Construction Logic**: Complex object assembly, dependency wiring, or conditional instantiation is hidden inside the factory.
- **Open/Closed Principle**: New product types can be introduced by extending the factory (or adding a new concrete creator) without modifying existing client code.
- **Single Responsibility**: Creation logic is separated from business logic, making each part more maintainable.
- **Polymorphism in Creation**: The client interacts with a uniform interface, unaware of the actual runtime type.

## Installation / Prerequisites

The Factory Pattern is **not a library or package** – it is a design methodology built entirely on standard object-oriented programming (OOP) features. No installation is required; it can be implemented in any language that supports:

- Interfaces, abstract classes, or duck typing (Python)
- Inheritance and polymorphism
- Encapsulation

Available in all major languages: Java, C#, C++, Python, TypeScript, Ruby, etc.

## Key Concepts

- **Product** – The abstract/interface type that the factory returns.
- **Concrete Product** – A class that implements the product interface.
- **Creator** – The class that declares the factory method or contains the factory logic.
- **Concrete Creator** – (Factory Method) A subclass of the creator that overrides the factory method to produce a specific concrete product.
- **Client** – Code that uses the product via the factory, never directly invoking constructors.

## Usage & Examples

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

## Key Features

| Feature | Description |
|---------|-------------|
| **Encapsulation of Creation** | Hides complex instantiation logic, dependency management, and object assembly. |
| **Decoupling** | Client code depends only on abstractions, not concrete classes. |
| **Open/Closed Principle** | Adding new products often requires only adding new factory subclasses (or new entries in a registry), without altering existing client code. |
| **Single Responsibility** | Creation logic is localized in the factory, not scattered across the codebase. |
| **Polymorphism in Construction** | The returned product is used through its interface; the actual class can vary at runtime. |
| **Conditional Object Creation** | Factories centralize if-else or switch logic that decides which object to create, making it easier to maintain and extend. |

## Best Practices

- **Depend on abstractions, not concretions.** The client should always operate on the product interface, never on a concrete class.
- **Keep factories focused.** A factory should only handle object creation; avoid mixing it with business logic.
- **Use a registry or map** in your factory to reduce if-else chains and make adding new types trivial (see the Python Simple Factory example above).
- **Consider parameterized factories** that accept a `type` or `config` object to decide which concrete product to instantiate.
- **Combine with Dependency Injection.** Factories can be injected into clients to further reduce coupling and enable testing.

## Common Pitfalls

- **Over‑engineering**: Not every object needs a factory; only use it when the creation logic is complex, varies, or needs to be centralized.
- **Too many factories**: Each product spawning its own factory can lead to unnecessary complexity. Evaluate whether a simpler factory (or no factory) suffices.
- **The factory hiding too much**: If the factory makes it harder to track object lifecycles or introduces invisible side effects, reconsider the design.
- **Mixing Simple Factory with Factory Method**: They are different patterns. Simple Factory uses a static method; Factory Method uses inheritance and polymorphism. Choose the right variant for your scenario.

## Related Patterns

- **Abstract Factory** – Often built on top of multiple Factory Methods; deals with families of products.
- **Singleton** – A factory can be implemented as a singleton if only one instance is needed.
- **Prototype** – Instead of creating objects from scratch, use a prototype to clone existing ones.
- **Builder** – Separates construction of a complex object from its representation; contrast with Factory which typically returns the product in one step.
- **Template Method** – Factory Method is often used inside a Template Method to let subclasses define the product created.

## Further Reading

- *Design Patterns: Elements of Reusable Object-Oriented Software* – Gamma, Helm, Johnson, Vlissides (GoF).
- *Head First Design Patterns* – Freeman & Freeman.
- [Refactoring Guru – Factory Method](https://refactoring.guru/design-patterns/factory-method)
- [Wikipedia – Factory Method Pattern](https://en.wikipedia.org/wiki/Factory_method_pattern)
- [SourceMaking – Factory Design Pattern](https://sourcemaking.com/design_patterns/factory_method)