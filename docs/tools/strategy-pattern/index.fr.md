---
title: Patron de conception Stratégie
description: Un patron de conception comportemental qui définit une famille d'algorithmes, encapsule chacun d'eux et les rend interchangeables à l'exécution.
created: 2026-06-20
tags:
  - design-patterns
  - behavioral
  - oop
  - gang-of-four
status: draft
---

# Strategy Pattern

Le **Strategy Pattern** est un patron de conception comportemental du Gang of Four (GoF). Il définit une famille d'algorithmes, encapsule chacun d'eux dans sa propre classe et les rend interchangeables. L'objet stratégie permet à l'algorithme de varier indépendamment des clients qui l'utilisent (le Contexte), favorisant la flexibilité et la réutilisation du code via la composition.

---

## Qu'est-ce que le Strategy Pattern ?

Au cœur, le Strategy Pattern consiste à encapsuler différentes façons de faire la même chose afin que vous puissiez choisir sans perturber le reste de votre code. Plutôt que d'intégrer plusieurs algorithmes dans une seule classe avec une logique conditionnelle, vous extrayez chaque algorithme dans sa propre classe *stratégie*. Le Contexte (la classe qui utilise un algorithme) détient une référence à l'une de ces stratégies et lui délègue le travail réel.

Le pattern suit la philosophie de la **composition plutôt que de l'héritage** et satisfait le **principe Open/Closed**—vous pouvez introduire de nouvelles stratégies sans modifier le code existant.

### Structure UML

```
┌─────────────┐          ┌──────────────────┐
│   Context   │          │   Strategy       │
│─────────────│          │ (interface/ABC)  │
│ - strategy  │─────────▶│ + execute()      │
│─────────────│          └────────┬─────────┘
│ + setStrategy(s) │               │
│ + doSomething()  │      ┌────────┴────────┐
└─────────────────┘      │                 │
                    ┌────┴─────┐    ┌────┴─────┐
                    │Concrete  │    │Concrete  │
                    │StrategyA │    │StrategyB │
                    │ + execute│    │ + execute│
                    └──────────┘    └──────────┘
```

---

## Pourquoi utiliser le Strategy Pattern ?

- **Élimine les conditionnelles** – Remplace les blocs `if/else` ou `switch` par une délégation polymorphique.
- **Ouvert à l'extension, fermé à la modification** – Ajoutez de nouvelles stratégies sans toucher au code existant.
- **Favorise la composition** – Le Contexte a une Stratégie, plutôt que d'être enfermé dans une hiérarchie d'héritage.
- **Responsabilité unique** – Chaque algorithme est isolé dans sa propre classe, plus facile à tester et à maintenir.
- **Flexibilité à l'exécution** – Modifiez le comportement d'un objet à l'exécution en échangeant sa stratégie.

### Quand l'utiliser

- Quand vous avez plusieurs algorithmes qui diffèrent uniquement par leur implémentation.
- Quand vous voulez éviter d'exposer au client des structures de données complexes spécifiques à un algorithme.
- Quand une classe a une condition massive qui commute entre des variantes de la même opération.
- Quand vous avez besoin de changer dynamiquement le comportement (par exemple, méthode de paiement, ordre de tri, calcul d'itinéraire).

---

## Comment implémenter (Install the Pattern)

Aucune installation de bibliothèque ou de package n'est requise – c'est un patron de conception que vous implémentez dans le code. Suivez ces trois étapes :

1. **Définissez une interface de stratégie ou une classe abstraite**  
   Déclare la ou les méthodes communes que toutes les stratégies concrètes doivent implémenter.

2. **Créez des stratégies concrètes**  
   Implémentez l'interface avec des algorithmes spécifiques. Chaque stratégie est une classe autonome.

3. **Modifiez le Contexte**  
   - Ajoutez un champ pour contenir une référence vers une Stratégie.  
   - Fournissez un setter (ou injection par constructeur) pour changer la stratégie à l'exécution.  
   - Déléguez l'exécution de l'algorithme à l'objet stratégie.

---

## Exemples d'utilisation de base

### Java (POO classique)

```java
// 1. Strategy Interface
interface SortingStrategy {
    void sort(int[] numbers);
}

// 2. Concrete Strategies
class BubbleSort implements SortingStrategy {
    @Override
    public void sort(int[] numbers) {
        // bubble sort implementation
        System.out.println("Sorting using BubbleSort");
    }
}

class QuickSort implements SortingStrategy {
    @Override
    public void sort(int[] numbers) {
        // quick sort implementation
        System.out.println("Sorting using QuickSort");
    }
}

// 3. Context
class Sorter {
    private SortingStrategy strategy;

    public Sorter(SortingStrategy strategy) {
        this.strategy = strategy;
    }

    public void setStrategy(SortingStrategy strategy) {
        this.strategy = strategy;
    }

    public void executeSort(int[] numbers) {
        strategy.sort(numbers);
    }
}

// Client usage
public class Main {
    public static void main(String[] args) {
        int[] data = {5, 3, 1, 4, 2};
        Sorter sorter = new Sorter(new BubbleSort());
        sorter.executeSort(data);

        sorter.setStrategy(new QuickSort());
        sorter.executeSort(data);
    }
}
```

### Python (Fonctions de première classe)

```python
from typing import List, Callable

# 1. Strategy is just a callable type hint
SortingStrategy = Callable[[List[int]], None]

# 2. Concrete strategies as functions
def bubble_sort(numbers: List[int]) -> None:
    print("Sorting using BubbleSort")

def quick_sort(numbers: List[int]) -> None:
    print("Sorting using QuickSort")

# 3. Context
class Sorter:
    def __init__(self, strategy: SortingStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortingStrategy):
        self._strategy = strategy

    def execute_sort(self, numbers: List[int]) -> None:
        self._strategy(numbers)

# Client usage
sorter = Sorter(bubble_sort)
sorter.execute_sort([5, 3, 1, 4, 2])

sorter.set_strategy(quick_sort)
sorter.execute_sort([5, 3, 1, 4, 2])
```

### C# (Délégués / Stratégies Lambda)

```csharp
using System;

// 1. Delegate as strategy type
delegate void SortingStrategy(int[] numbers);

// 2. Concrete strategies (lambda or methods)
SortingStrategy bubbleSort = data => Console.WriteLine("BubbleSort");
SortingStrategy quickSort = data => Console.WriteLine("QuickSort");

// 3. Context
class Sorter {
    private SortingStrategy strategy;

    public Sorter(SortingStrategy strategy) => this.strategy = strategy;
    public void SetStrategy(SortingStrategy strategy) => this.strategy = strategy;
    public void ExecuteSort(int[] data) => strategy(data);
}

// Client
var sorter = new Sorter(bubbleSort);
sorter.ExecuteSort(new[] {5, 3, 1, 4, 2});
sorter.SetStrategy(quickSort);
sorter.ExecuteSort(new[] {5, 3, 1, 4, 2});
```

---

## Points clés (avec démonstration de code)

### 1. Changement d'algorithme en cours d'exécution

```java
// Strategy interface
public interface CompressionStrategy {
    byte[] compress(String data);
}

public class ZipCompression implements CompressionStrategy { ... }
public class GzipCompression implements CompressionStrategy { ... }

// Context
public class FileCompressor {
    private CompressionStrategy strategy;

    public FileCompressor(CompressionStrategy s) { this.strategy = s; }
    public void setStrategy(CompressionStrategy s) { this.strategy = s; }
    public byte[] compress(String data) { return strategy.compress(data); }
}

// Client: choose compression at runtime based on file extension
FileCompressor compressor = new FileCompressor(new ZipCompression());
if (fileName.endsWith(".gz")) {
    compressor.setStrategy(new GzipCompression());
}
```

### 2. Élimine la logique conditionnelle (Avant vs Après)

**Avant (mauvais) :**
```java
public double calculateShipping(Order order, String method) {
    if ("standard".equals(method)) {
        return order.getWeight() * 0.5;
    } else if ("express".equals(method)) {
        return order.getWeight() * 1.5 + 10;
    } else if ("overnight".equals(method)) {
        return order.getWeight() * 3.0 + 20;
    }
    throw new IllegalArgumentException("Unknown method");
}
```

**Après (Strategy pattern) :**
```java
interface ShippingStrategy {
    double calculate(Order order);
}

class StandardShipping implements ShippingStrategy {
    public double calculate(Order order) { return order.getWeight() * 0.5; }
}
class ExpressShipping implements ShippingStrategy {
    public double calculate(Order order) { return order.getWeight() * 1.5 + 10; }
}
// OvernightShipping similarly...

// Context delegates to strategy:
public ShippingCalculator(ShippingStrategy strategy) { ... }
public double calculate(Order order) { return strategy.calculate(order); }
```

### 3. Principe d'ouverture/fermeture – Ajout de nouvelles stratégies

Vous pouvez ajouter une stratégie `DroneShipping` sans modifier `ShippingCalculator` :

```java
public class DroneShipping implements ShippingStrategy {
    @Override
    public double calculate(Order order) {
        return order.getWeight() * 2.0 + 5; // flat fee
    }
}
```

Le code existant reste inchangé.

---

## Pièges courants

| Piège | Comment éviter |
|---------|--------------|
| **Sur-ingénierie** – Créer des stratégies alors qu'un seul algorithme stable suffit. | Commencez simple ; n'introduisez des stratégies que lorsque vous avez ou prévoyez plusieurs variantes. |
| **Connaissance du client** – Le client doit savoir quelle stratégie choisir. | Combinez avec une Fabrique (Factory) ou un Registre pour automatiser la sélection de stratégie en fonction des conditions. |
| **Nombre accru de classes** – Chaque stratégie ajoute un nouveau fichier. | Utilisez des lambdas, des fonctions ou des délégués pour des stratégies temporaires ou ponctuelles. |
| **Stratégies avec état** – Un état mutable partagé dans une stratégie peut provoquer des bogues, en particulier dans des contextes multi-threads. | Préférez des stratégies sans état ; si un état est nécessaire, encapsulez-le dans l'instance de stratégie et gérez son cycle de vie avec attention. |

---

## Patterns associés

- **State Pattern** – Structure très similaire, mais State est utilisé pour changer le comportement en fonction de l'état interne, tandis que Strategy permet au client de choisir un algorithme en externe. Les transitions d'état sont souvent gérées à l'intérieur du Contexte ; la sélection de la stratégie est généralement externe.
- **Template Method** – Définit le squelette d'un algorithme, permettant aux sous-classes de redéfinir certaines étapes. Strategy atteint le même objectif via la composition plutôt que l'héritage.
- **Factory Pattern** – Souvent utilisé pour créer l'objet stratégie approprié en fonction de l'entrée ou de la configuration.
- **Decorator Pattern** – Peut être combiné avec Strategy pour ajouter des responsabilités à un objet stratégie sans le modifier.

---

## Résumé

Le Strategy Pattern est un outil puissant pour gérer des familles d'algorithmes apparentés. En encapsulant chaque algorithme dans une classe (ou une fonction) séparée, vous gagnez en flexibilité, en maintenabilité et en adhérence aux principes SOLID. Utilisez-le lorsque vous avez plusieurs comportements interchangeables et que vous souhaitez éviter une logique conditionnelle rigide. Rappelez-vous : **privilégiez la composition à l'héritage**—et laissez les stratégies faire le travail lourd.