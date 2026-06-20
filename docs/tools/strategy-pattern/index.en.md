---
title: Strategy Pattern
description: A behavioral design pattern that defines a family of algorithms, encapsulates each one, and makes them interchangeable at runtime.
created: 2026-06-20
tags:
  - design-patterns
  - behavioral
  - oop
  - gang-of-four
status: draft
---

# Strategy Pattern

The **Strategy Pattern** is a behavioral design pattern from the Gang of Four (GoF). It defines a family of algorithms, encapsulates each one in its own class, and makes them interchangeable. The strategy object lets the algorithm vary independently from the clients that use it (the Context), promoting flexibility and code reuse through composition.

---

## What is the Strategy Pattern?

At its core, the Strategy Pattern is about encapsulating different ways to do the same thing so you can pick and choose without messing up the rest of your code. Rather than embedding multiple algorithms in a single class with conditional logic, you extract each algorithm into its own *strategy* class. The Context (the class that uses an algorithm) holds a reference to one of these strategies and delegates the actual work to it.

The pattern follows the **composition over inheritance** philosophy and satisfies the **Open/Closed Principle**—you can introduce new strategies without altering existing code.

### UML Structure

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

## Why Use the Strategy Pattern?

- **Eliminates conditionals** – Replaces `if/else` or `switch` blocks with polymorphic delegation.
- **Open for extension, closed for modification** – Add new strategies without touching existing code.
- **Promotes composition** – The Context has a Strategy, rather than being locked into an inheritance hierarchy.
- **Single Responsibility** – Each algorithm is isolated in its own class, easier to test and maintain.
- **Runtime flexibility** – Change an object’s behavior at runtime by swapping its strategy.

### When to Use

- When you have multiple algorithms that differ only in their implementation.
- When you want to avoid exposing complex, algorithm-specific data structures to the client.
- When a class has a massive conditional that switches between variants of the same operation.
- When you need to dynamically change behavior (e.g., payment method, sorting order, route calculation).

---

## How to Implement (Install the Pattern)

No library or package installation is required—it’s a design pattern you implement in code. Follow these three steps:

1. **Define a Strategy Interface or Abstract Class**  
   Declares the common method(s) that all concrete strategies must implement.

2. **Create Concrete Strategies**  
   Implement the interface with specific algorithms. Each strategy is a self-contained class.

3. **Modify the Context**  
   - Add a field to hold a reference to a Strategy.  
   - Provide a setter (or constructor injection) to change the strategy at runtime.  
   - Delegate the algorithm execution to the strategy object.

---

## Basic Usage Examples

### Java (Classic OOP)

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

### Python (First-class Functions)

Thanks to Python’s first-class functions, strategies can be plain functions or lambdas, reducing boilerplate.

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

### C# (Delegates / Lambda Strategies)

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

## Key Features (with Code Demonstration)

### 1. Runtime Swap of Algorithm

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

### 2. Eliminates Conditional Logic (Before vs After)

**Before (bad):**
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

**After (Strategy pattern):**
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

No `if/else`—just set the appropriate strategy object.

### 3. Open/Closed Principle – Adding New Strategies

You can add a `DroneShipping` strategy without changing `ShippingCalculator`:

```java
public class DroneShipping implements ShippingStrategy {
    @Override
    public double calculate(Order order) {
        return order.getWeight() * 2.0 + 5; // flat fee
    }
}
```

The existing code remains unchanged.

---

## Common Pitfalls

| Pitfall | How to Avoid |
|---------|--------------|
| **Over-engineering** – Creating strategies when one stable algorithm suffices. | Start simple; introduce strategies only when you have or foresee multiple variants. |
| **Client knowledge** – The client must know which strategy to choose. | Combine with a Factory or a Registry to automate strategy selection based on conditions. |
| **Increased number of classes** – Each strategy adds a new file. | Use lambdas, functions, or delegates for short-lived or one-off strategies. |
| **Stateful strategies** – Shared mutable state in a strategy can cause bugs, especially in multithreaded contexts. | Prefer stateless strategies; if state is needed, encapsulate it in the strategy instance and manage its lifecycle carefully. |

---

## Related Patterns

- **State Pattern** – Very similar structure, but State is used to change behavior based on internal state, whereas Strategy allows the client to choose an algorithm externally. State transitions are often managed inside the Context; Strategy selection is typically external.
- **Template Method** – Defines the skeleton of an algorithm, letting subclasses override steps. Strategy achieves the same goal via composition instead of inheritance.
- **Factory Pattern** – Often used to create the appropriate strategy object based on input or configuration.
- **Decorator Pattern** – Can be combined with Strategy to add responsibilities to a strategy object without modifying it.

---

## Summary

The Strategy Pattern is a powerful tool for managing families of related algorithms. By encapsulating each algorithm in a separate class (or function), you gain flexibility, maintainability, and adherence to SOLID principles. Use it when you have multiple interchangeable behaviors and want to avoid stiff conditional logic. Remember: **favor composition over inheritance**—and let strategies do the heavy lifting.