---
title: Factory Pattern
description: Un patrón de diseño creacional que encapsula la creación de objetos, desacoplando el código cliente de las implementaciones concretas y promoviendo la flexibilidad.
created: 2026-06-19
tags:
  - design-patterns
  - creational
  - object-oriented
  - gof
status: draft
---

# Factory Pattern

## Resumen El Factory Pattern es un **patrón de diseño creacional** que proporciona una interfaz o método para crear objetos sin exponer la lógica de instanciación al cliente. En lugar de llamar directamente a un constructor con `new`, el código cliente delega la creación a una **fábrica** – una clase, método u objeto separado – que decide qué clase concreta instanciar según los parámetros de entrada, la configuración o el contexto.

Este patrón es uno de los patrones de diseño de la Gang of Four (GoF) y se presenta en tres variantes comunes:

- **Simple Factory** – Una clase/método estático único que devuelve diferentes productos concretos basados en un parámetro.
- **Factory Method** – Una clase define un método abstracto para la creación, y las subclases lo sobrescriben para producir productos específicos.
- **Abstract Factory** – Una interfaz para crear familias de objetos relacionados o dependientes sin especificar sus clases concretas.

## ¿Por qué usar el Factory Pattern?

- **Desacoplamiento**: El código cliente depende de abstracciones (interfaces/clases abstractas), no de implementaciones concretas. Cambiar un tipo de producto a menudo solo requiere modificar la lógica de la fábrica, no el cliente.
- **Encapsulación de la lógica de construcción**: El ensamblaje complejo de objetos, la conexión de dependencias o la instanciación condicional se ocultan dentro de la fábrica.
- **Principio Abierto/Cerrado**: Se pueden introducir nuevos tipos de producto extendiendo la fábrica (o añadiendo un nuevo creador concreto) sin modificar el código cliente existente.
- **Responsabilidad Única**: La lógica de creación se separa de la lógica de negocio, haciendo que cada parte sea más mantenible.
- **Polimorfismo en la creación**: El cliente interactúa con una interfaz uniforme, sin conocer el tipo real en tiempo de ejecución.

## Instalación / Requisitos previos

El Factory Pattern **no es una librería o paquete** – es una metodología de diseño construida enteramente sobre características estándar de programación orientada a objetos (POO). No se requiere instalación; se puede implementar en cualquier lenguaje que soporte:

- Interfaces, clases abstractas o duck typing (Python)
- Herencia y polimorfismo
- Encapsulación

Disponible en todos los lenguajes principales: Java, C#, C++, Python, TypeScript, Ruby, etc.

## Conceptos clave

- **Product** – El tipo abstracto/interfaz que devuelve la fábrica.
- **Concrete Product** – Una clase que implementa la interfaz del producto.
- **Creator** – La clase que declara el método de fábrica o contiene la lógica de la fábrica.
- **Concrete Creator** – (Factory Method) Una subclase del creator que sobrescribe el método de fábrica para producir un producto concreto específico.
- **Client** – Código que utiliza el producto a través de la fábrica, sin invocar constructores directamente.

## Uso y ejemplos

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

## Características principales

| Característica | Descripción |
|---------|-------------|
| **Encapsulación de la creación** | Oculta la lógica compleja de instanciación, la gestión de dependencias y el ensamblaje de objetos. |
| **Desacoplamiento** | El código cliente depende solo de abstracciones, no de clases concretas. |
| **Principio Abierto/Cerrado** | Añadir nuevos productos a menudo solo requiere añadir nuevas subclases de fábrica (o nuevas entradas en un registro), sin alterar el código cliente existente. |
| **Responsabilidad Única** | La lógica de creación se localiza en la fábrica, no se dispersa por toda la base de código. |
| **Polimorfismo en la construcción** | El producto devuelto se utiliza a través de su interfaz; la clase real puede variar en tiempo de ejecución. |
| **Creación condicional de objetos** | Las fábricas centralizan la lógica if-else o switch que decide qué objeto crear, facilitando su mantenimiento y extensión. |

## Mejores prácticas

- **Depende de abstracciones, no de concreciones.** El cliente siempre debe operar sobre la interfaz del producto, nunca sobre una clase concreta.
- **Mantén las fábricas enfocadas.** Una fábrica solo debe encargarse de la creación de objetos; evita mezclarla con lógica de negocio.
- **Usa un registro o mapa** en tu fábrica para reducir las cadenas if-else y facilitar la adición de nuevos tipos (ver el ejemplo de Simple Factory en Python más arriba).
- **Considera fábricas parametrizadas** que acepten un objeto `type` o de configuración para decidir qué producto concreto instanciar.
- **Combínalo con Inyección de Dependencias.** Las fábricas pueden inyectarse en los clientes para reducir aún más el acoplamiento y facilitar las pruebas.

## Errores comunes

- **Sobreingeniería**: No todos los objetos necesitan una fábrica; úsala solo cuando la lógica de creación sea compleja, variable o necesite centralizarse.
- **Demasiadas fábricas**: Que cada producto tenga su propia fábrica puede llevar a una complejidad innecesaria. Evalúa si una fábrica más simple (o ninguna) es suficiente.
- **La fábrica oculta demasiado**: Si la fábrica dificulta el seguimiento de los ciclos de vida de los objetos o introduce efectos secundarios invisibles, reconsidera el diseño.
- **Mezclar Simple Factory con Factory Method**: Son patrones diferentes. Simple Factory usa un método estático; Factory Method usa herencia y polimorfismo. Elige la variante adecuada para tu escenario.

## Patrones relacionados

- **Abstract Factory** – A menudo se construye sobre múltiples Factory Methods; trabaja con familias de productos.
- **Singleton** – Una fábrica puede implementarse como singleton si solo se necesita una instancia.
- **Prototype** – En lugar de crear objetos desde cero, usa un prototipo para clonar los existentes.
- **Builder** – Separa la construcción de un objeto complejo de su representación; en contraste, Factory normalmente devuelve el producto en un solo paso.
- **Template Method** – Factory Method se usa a menudo dentro de un Template Method para que las subclases definan el producto creado.

## Lecturas adicionales

- *Design Patterns: Elements of Reusable Object-Oriented Software* – Gamma, Helm, Johnson, Vlissides (GoF).
- *Head First Design Patterns* – Freeman & Freeman.
- [Refactoring Guru – Factory Method](https://refactoring.guru/design-patterns/factory-method)
- [Wikipedia – Factory Method Pattern](https://en.wikipedia.org/wiki/Factory_method_pattern)
- [SourceMaking – Factory Design Pattern](https://sourcemaking.com/design_patterns/factory_method)