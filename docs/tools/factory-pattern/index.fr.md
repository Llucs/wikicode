---
title: Pattern Fabrique
description: Un patron de conception créationnel qui encapsule la création d'objets, découplant le code client des implémentations concrètes et favorisant la flexibilité.
created: 2026-06-19
tags:
  - design-patterns
  - creational
  - object-oriented
  - gof
status: draft
---

# Factory Pattern

## Aperçu

Le **Factory Pattern** (ou Pattern Fabrique) est un **patron de conception créationnel** qui fournit une interface ou une méthode pour créer des objets sans exposer la logique d'instanciation au client. Au lieu d'appeler directement un constructeur avec `new`, le code client délègue la création à une **fabrique** (factory) – une classe, méthode ou objet séparé – qui décide quelle classe concrète instancier en fonction de paramètres d'entrée, de la configuration ou du contexte.

Ce patron est l'un des patrons de conception du Gang of Four (GoF) et se décline en trois variantes courantes :

- **Simple Factory** (Fabrique Simple) – Une seule classe/méthode statique qui retourne différents produits concrets selon un paramètre.
- **Factory Method** (Méthode de Fabrique) – Une classe définit une méthode abstraite pour la création, et les sous-classes la surchargent pour produire des produits spécifiques.
- **Abstract Factory** (Fabrique Abstraite) – Une interface pour créer des familles d'objets liés ou dépendants sans spécifier leurs classes concrètes.

## Pourquoi utiliser le Factory Pattern ?

- **Découplage** : Le code client dépend d'abstractions (interfaces/classes abstraites), et non d'implémentations concrètes. Changer un type de produit nécessite souvent seulement de modifier la logique de la fabrique, pas le client.
- **Encapsulation de la logique de construction** : L'assemblage complexe d'objets, le câblage des dépendances ou l'instanciation conditionnelle sont cachés à l'intérieur de la fabrique.
- **Principe Ouvert/Fermé** (Open/Closed) : De nouveaux types de produits peuvent être introduits en étendant la fabrique (ou en ajoutant un nouveau créateur concret) sans modifier le code client existant.
- **Responsabilité Unique** (Single Responsibility) : La logique de création est séparée de la logique métier, rendant chaque partie plus maintenable.
- **Polymorphisme dans la création** : Le client interagit avec une interface uniforme, ignorant le type réel à l'exécution.

## Installation / Prérequis

Le **Factory Pattern** n'est **pas une bibliothèque ou un paquet** – c'est une méthodologie de conception entièrement basée sur les fonctionnalités standard de la programmation orientée objet (POO). Aucune installation n'est nécessaire ; il peut être implémenté dans tout langage prenant en charge :

- Les interfaces, les classes abstraites ou le duck typing (Python)
- L'héritage et le polymorphisme
- L'encapsulation

Disponible dans tous les langages majeurs : Java, C#, C++, Python, TypeScript, Ruby, etc.

## Concepts Clés

- **Product** (Produit) – Le type abstrait/interface que la fabrique retourne.
- **Concrete Product** (Produit Concret) – Une classe qui implémente l'interface du produit.
- **Creator** (Créateur) – La classe qui déclare la méthode de fabrique ou contient la logique de la fabrique.
- **Concrete Creator** (Créateur Concret) – (Factory Method) Une sous-classe du créateur qui surcharge la méthode de fabrique pour produire un produit concret spécifique.
- **Client** – Le code qui utilise le produit via la fabrique, sans jamais invoquer directement les constructeurs.

## Usage & Exemples

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

## Fonctionnalités Clés

| Fonctionnalité | Description |
|----------------|-------------|
| **Encapsulation de la création** | Cache la logique d'instanciation complexe, la gestion des dépendances et l'assemblage des objets. |
| **Découplage** | Le code client dépend uniquement des abstractions, pas des classes concrètes. |
| **Principe Ouvert/Fermé** | L'ajout de nouveaux produits nécessite souvent seulement l'ajout de nouvelles sous-classes de fabrique (ou de nouvelles entrées dans un registre), sans modifier le code client existant. |
| **Responsabilité Unique** | La logique de création est localisée dans la fabrique, non dispersée dans la base de code. |
| **Polymorphisme dans la construction** | Le produit retourné est utilisé via son interface ; la classe réelle peut varier à l'exécution. |
| **Création conditionnelle d'objets** | Les fabriques centralisent la logique conditionnelle (if-else ou switch) qui décide quel objet créer, facilitant la maintenance et l'extension. |

## Bonnes Pratiques

- **Dépendre des abstractions, pas des concrétions.** Le client doit toujours opérer sur l'interface du produit, jamais sur une classe concrète.
- **Garder les fabriques concentrées.** Une fabrique ne devrait gérer que la création d'objets ; évitez de la mélanger avec la logique métier.
- **Utiliser un registre ou une map** dans votre fabrique pour réduire les chaînes de if-else et rendre l'ajout de nouveaux types trivial (voir l'exemple Simple Factory en Python ci-dessus).
- **Envisager des fabriques paramétrées** qui acceptent un objet `type` ou `config` pour décider quel produit concret instancier.
- **Combiner avec l'Injection de Dépendances.** Les fabriques peuvent être injectées dans les clients pour réduire encore plus le couplage et faciliter les tests.

## Pièges Courants

- **Surgénération** (Over-engineering) : Tous les objets n'ont pas besoin d'une fabrique ; utilisez-la uniquement lorsque la logique de création est complexe, variable ou nécessite d'être centralisée.
- **Trop de fabriques** : Chaque produit engendrant sa propre fabrique peut entraîner une complexité inutile. Évaluez si une fabrique plus simple (ou pas de fabrique) suffit.
- **La fabrique cache trop de choses** : Si la fabrique rend plus difficile le suivi des cycles de vie des objets ou introduit des effets de bord invisibles, reconsidérez la conception.
- **Mélanger Simple Factory et Factory Method** : Ce sont des patrons différents. Simple Factory utilise une méthode statique ; Factory Method utilise l'héritage et le polymorphisme. Choisissez la variante adaptée à votre scénario.

## Patrons Associés

- **Abstract Factory** (Fabrique Abstraite) – Souvent construite sur plusieurs Factory Methods ; traite des familles de produits.
- **Singleton** – Une fabrique peut être implémentée en singleton si une seule instance est nécessaire.
- **Prototype** (Prototype) – Au lieu de créer des objets à partir de zéro, utilisez un prototype pour cloner des objets existants.
- **Builder** (Monteur) – Sépare la construction d'un objet complexe de sa représentation ; à contraster avec Factory qui retourne généralement le produit en une étape.
- **Template Method** (Méthode Template) – Factory Method est souvent utilisée à l'intérieur d'une Template Method pour laisser les sous-classes définir le produit créé.

## Pour Aller Plus Loin

- *Design Patterns: Elements of Reusable Object-Oriented Software* – Gamma, Helm, Johnson, Vlissides (GoF).
- *Head First Design Patterns* – Freeman & Freeman.
- [Refactoring Guru – Factory Method](https://refactoring.guru/design-patterns/factory-method)
- [Wikipedia – Factory Method Pattern](https://en.wikipedia.org/wiki/Factory_method_pattern)
- [SourceMaking – Factory Design Pattern](https://sourcemaking.com/design_patterns/factory_method)