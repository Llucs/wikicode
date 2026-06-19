---
title: 工厂模式
description: 一种创建型设计模式，封装对象创建，将客户端代码与具体实现解耦，并提高灵活性。
created: 2026-06-19
tags:
  - design-patterns
  - creational
  - object-oriented
  - gof
status: draft
---

# 工厂模式

## 概述
工厂模式是一种**创建型设计模式**，它提供创建对象的接口或方法，而不将实例化逻辑暴露给客户端。客户端代码不是直接使用 `new` 调用构造函数，而是将创建委托给**工厂**——一个独立的类、方法或对象——根据输入参数、配置或上下文决定要实例化的具体类。

此模式是四人组（Gang of Four, GoF）设计模式之一，有三种常见变体：

- **简单工厂（Simple Factory）** – 一个类/静态方法，根据参数返回不同的具体产品。
- **工厂方法（Factory Method）** – 一个类定义一个抽象的创建方法，子类覆盖它以生成特定产品。
- **抽象工厂（Abstract Factory）** – 用于创建相关或依赖对象家族的接口，而不指定其具体类。

## 为什么要使用工厂模式？

- **解耦（Decoupling）**：客户端代码依赖抽象（接口/抽象类），而非具体实现。切换产品类型通常只需更改工厂逻辑，无需改动客户端。
- **封装构造逻辑（Encapsulation of Construction Logic）**：复杂的对象组装、依赖注入或条件实例化隐藏在工厂内部。
- **开闭原则（Open/Closed Principle）**：通过扩展工厂（或添加新的具体创建者）可以引入新产品类型，而无需修改现有客户端代码。
- **单一职责（Single Responsibility）**：创建逻辑与业务逻辑分离，使各部分更易于维护。
- **创建中的多态（Polymorphism in Creation）**：客户端通过统一接口交互，对实际运行时类型无感知。

## 安装/先决条件

工厂模式**不是库或包**——它是一种完全基于标准面向对象编程（OOP）特性的设计方法论。无需安装；它可以在任何支持以下特性的语言中实现：

- 接口、抽象类或鸭子类型（Python）
- 继承和多态
- 封装

适用于所有主流语言：Java、C#、C++、Python、TypeScript、Ruby 等。

## 关键概念

- **产品（Product）** – 工厂返回的抽象/接口类型。
- **具体产品（Concrete Product）** – 实现产品接口的类。
- **创建者（Creator）** – 声明工厂方法或包含工厂逻辑的类。
- **具体创建者（Concrete Creator）** – （工厂方法）创建者的子类，重写工厂方法以生成特定的具体产品。
- **客户端（Client）** – 通过工厂使用产品，从不直接调用构造函数的代码。

## 用法与示例

### 简单工厂（Python）

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

### 工厂方法（C#）

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

### 抽象工厂（Java）

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

## 关键特性

| 特性 | 描述 |
|------|------|
| **封装创建（Encapsulation of Creation）** | 隐藏复杂的实例化逻辑、依赖管理和对象组装。 |
| **解耦（Decoupling）** | 客户端代码仅依赖抽象，而非具体类。 |
| **开闭原则（Open/Closed Principle）** | 添加新产品通常只需添加新的工厂子类（或注册表中的新条目），而无需更改现有客户端代码。 |
| **单一职责（Single Responsibility）** | 创建逻辑集中在工厂中，不会遍布整个代码库。 |
| **构造中的多态（Polymorphism in Construction）** | 返回的产品通过其接口使用；实际类可以在运行时变化。 |
| **条件对象创建（Conditional Object Creation）** | 工厂集中化 if-else 或 switch 逻辑以决定创建哪个对象，更易于维护和扩展。 |

## 最佳实践

- **依赖抽象，而非具体实现。** 客户端应始终通过产品接口操作，绝不依赖具体类。
- **保持工厂专注。** 工厂应仅处理对象创建；避免混合业务逻辑。
- **在工厂中使用注册表或映射** 以减少 if-else 链，并使添加新类型变得简单（参见上面的 Python 简单工厂示例）。
- **考虑参数化工厂**，接受 `type` 或 `config` 对象来决定实例化哪个具体产品。
- **与依赖注入结合。** 工厂可以注入到客户端，以进一步减少耦合并支持测试。

## 常见陷阱

- **过度工程（Over‑engineering）**：并非每个对象都需要工厂；仅在创建逻辑复杂、多变或需要集中化时使用。
- **工厂过多**：每个产品都有自己的工厂会导致不必要的复杂度。评估是否更简单的工厂（或不需要工厂）就足够了。
- **工厂隐藏太多**：如果工厂使得跟踪对象生命周期更困难或引入不可见的副作用，请重新考虑设计。
- **混淆简单工厂和工厂方法**：它们是不同的模式。简单工厂使用静态方法；工厂方法使用继承和多态。根据场景选择正确的变体。

## 相关模式

- **抽象工厂（Abstract Factory）** – 通常基于多个工厂方法构建；处理产品家族。
- **单例（Singleton）** – 如果只需要一个实例，工厂可以实现为单例。
- **原型（Prototype）** – 不从头创建对象，而是使用原型克隆现有对象。
- **构建器（Builder）** – 将复杂对象的构造与其表示分离；与工厂（通常一步返回产品）形成对比。
- **模板方法（Template Method）** – 工厂方法通常用在模板方法内部，让子类定义创建的产品。

## 进一步阅读

- *设计模式：可复用面向对象软件的基础* – Gamma, Helm, Johnson, Vlissides (GoF)。
- *Head First 设计模式* – Freeman & Freeman。
- [Refactoring Guru – 工厂方法](https://refactoring.guru/design-patterns/factory-method)
- [维基百科 – 工厂方法模式](https://en.wikipedia.org/wiki/Factory_method_pattern)
- [SourceMaking – 工厂设计模式](https://sourcemaking.com/design_patterns/factory_method)