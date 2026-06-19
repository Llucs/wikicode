---
title: Padrão Factory
description: Um padrão de design criacional que encapsula a criação de objetos, desacoplando o código cliente de implementações concretas e promovendo flexibilidade.
created: 2026-06-19
tags:
  - design-patterns
  - creational
  - object-oriented
  - gof
status: draft
---

# Factory Pattern

## Visão Geral

O Factory Pattern é um **padrão de design criacional** que fornece uma interface ou método para criar objetos sem expor a lógica de instanciação ao cliente. Em vez de chamar diretamente um construtor com `new`, o código cliente delega a criação a uma **fábrica** – uma classe, método ou objeto separado – que decide qual classe concreta instanciar com base em parâmetros de entrada, configuração ou contexto.

Este padrão é um dos padrões de design do Gang of Four (GoF) e possui três variantes comuns:

- **Simple Factory** – Uma única classe/método estático que retorna diferentes produtos concretos com base em um parâmetro.
- **Factory Method** – Uma classe define um método abstrato para criação, e subclasses o sobrescrevem para produzir produtos específicos.
- **Abstract Factory** – Uma interface para criar famílias de objetos relacionados ou dependentes sem especificar suas classes concretas.

## Por que usar o Factory Pattern?

- **Desacoplamento**: O código cliente depende de abstrações (interfaces/classes abstratas), não de implementações concretas. Trocar um tipo de produto muitas vezes requer apenas alterar a lógica da fábrica, não o cliente.
- **Encapsulamento da Lógica de Construção**: Montagem complexa de objetos, configuração de dependências ou instanciação condicional são escondidas dentro da fábrica.
- **Princípio Open/Closed**: Novos tipos de produto podem ser introduzidos estendendo a fábrica (ou adicionando um novo criador concreto) sem modificar o código cliente existente.
- **Responsabilidade Única**: A lógica de criação é separada da lógica de negócio, tornando cada parte mais fácil de manter.
- **Polimorfismo na Criação**: O cliente interage com uma interface uniforme, sem conhecimento do tipo real em tempo de execução.

## Instalação / Pré-requisitos

O Factory Pattern **não é uma biblioteca ou pacote** – é uma metodologia de design construída inteiramente sobre recursos padrão de programação orientada a objetos (POO). Nenhuma instalação é necessária; pode ser implementado em qualquer linguagem que suporte:

- Interfaces, classes abstratas ou duck typing (Python)
- Herança e polimorfismo
- Encapsulamento

Disponível em todas as principais linguagens: Java, C#, C++, Python, TypeScript, Ruby, etc.

## Conceitos-chave

- **Product** – O tipo abstrato/interface que a fábrica retorna.
- **Concrete Product** – Uma classe que implementa a interface do produto.
- **Creator** – A classe que declara o método de fábrica ou contém a lógica da fábrica.
- **Concrete Creator** – (Factory Method) Uma subclasse do creator que sobrescreve o método de fábrica para produzir um produto concreto específico.
- **Client** – Código que usa o produto através da fábrica, nunca invocando construtores diretamente.

## Uso e Exemplos

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

## Principais Características

| Característica | Descrição |
|---------|-------------|
| **Encapsulamento da Criação** | Esconde lógica complexa de instanciação, gerenciamento de dependências e montagem de objetos. |
| **Desacoplamento** | O código cliente depende apenas de abstrações, não de classes concretas. |
| **Princípio Open/Closed** | Adicionar novos produtos geralmente requer apenas adicionar novas subclasses de fábrica (ou novas entradas em um registro), sem alterar o código cliente existente. |
| **Responsabilidade Única** | A lógica de criação é localizada na fábrica, não espalhada pela base de código. |
| **Polimorfismo na Construção** | O produto retornado é usado através de sua interface; a classe real pode variar em tempo de execução. |
| **Criação Condicional de Objetos** | As fábricas centralizam a lógica if-else ou switch que decide qual objeto criar, facilitando a manutenção e extensão. |

## Melhores Práticas

- **Dependa de abstrações, não de concreções.** O cliente deve sempre operar na interface do produto, nunca em uma classe concreta.
- **Mantenha as fábricas focadas.** Uma fábrica deve lidar apenas com criação de objetos; evite misturá-la com lógica de negócio.
- **Use um registro ou mapa** em sua fábrica para reduzir cadeias de if-else e tornar a adição de novos tipos trivial (veja o exemplo Python Simple Factory acima).
- **Considere fábricas parametrizadas** que aceitam um objeto `type` ou `config` para decidir qual produto concreto instanciar.
- **Combine com Injeção de Dependência.** As fábricas podem ser injetadas nos clientes para reduzir ainda mais o acoplamento e permitir testes.

## Armadilhas Comuns

- **Over‑engineering (Engenharia excessiva)**: Nem todo objeto precisa de uma fábrica; use-a apenas quando a lógica de criação é complexa, varia ou precisa ser centralizada.
- **Muitas fábricas**: Cada produto gerando sua própria fábrica pode levar a uma complexidade desnecessária. Avalie se uma fábrica mais simples (ou nenhuma fábrica) é suficiente.
- **A fábrica escondendo demais**: Se a fábrica dificulta o rastreamento dos ciclos de vida dos objetos ou introduz efeitos colaterais invisíveis, repense o design.
- **Misturar Simple Factory com Factory Method**: São padrões diferentes. Simple Factory usa um método estático; Factory Method usa herança e polimorfismo. Escolha a variante certa para o seu cenário.

## Padrões Relacionados

- **Abstract Factory** – Frequentemente construído sobre vários Factory Methods; lida com famílias de produtos.
- **Singleton** – Uma fábrica pode ser implementada como um singleton se apenas uma instância for necessária.
- **Prototype** – Em vez de criar objetos do zero, use um protótipo para clonar objetos existentes.
- **Builder** – Separa a construção de um objeto complexo de sua representação; contraste com Factory que geralmente retorna o produto em uma única etapa.
- **Template Method** – Factory Method é frequentemente usado dentro de um Template Method para permitir que subclasses definam o produto criado.

## Leitura Adicional

- *Design Patterns: Elements of Reusable Object-Oriented Software* – Gamma, Helm, Johnson, Vlissides (GoF).
- *Head First Design Patterns* – Freeman & Freeman.
- [Refactoring Guru – Factory Method](https://refactoring.guru/design-patterns/factory-method)
- [Wikipedia – Factory Method Pattern](https://en.wikipedia.org/wiki/Factory_method_pattern)
- [SourceMaking – Factory Design Pattern](https://sourcemaking.com/design_patterns/factory_method)