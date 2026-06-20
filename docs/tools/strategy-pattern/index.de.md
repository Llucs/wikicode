---
title: Strategie-Muster
description: Ein verhaltensorientiertes Entwurfsmuster, das eine Familie von Algorithmen definiert, jeden einzelnen kapselt und sie zur Laufzeit austauschbar macht.
created: 2026-06-20
tags:
  - design-patterns
  - behavioral
  - oop
  - gang-of-four
status: draft
---

# Strategie-Muster

Das **Strategie-Muster** ist ein verhaltensorientiertes Entwurfsmuster der Gang of Four (GoF). Es definiert eine Familie von Algorithmen, kapselt jeden einzelnen in einer eigenen Klasse und macht sie austauschbar. Das Strategieobjekt lässt den Algorithmus unabhängig von den Clients, die ihn verwenden (dem Context), variieren und fördert so Flexibilität und Code-Wiederverwendung durch Komposition.

---

## Was ist das Strategie-Muster?

Im Kern geht es beim Strategie-Muster darum, verschiedene Möglichkeiten zur Durchführung derselben Aufgabe zu kapseln, sodass Sie auswählen können, ohne den Rest Ihres Codes zu beeinträchtigen. Anstatt mehrere Algorithmen in einer einzigen Klasse mit bedingter Logik zu verschachteln, extrahieren Sie jeden Algorithmus in eine eigene *Strategie*-Klasse. Der Context (die Klasse, die einen Algorithmus verwendet) hält eine Referenz auf eine dieser Strategien und delegiert die eigentliche Arbeit an sie.

Das Muster folgt der **Komposition vor Vererbung**-Philosophie und erfüllt das **Open/Closed-Prinzip** – Sie können neue Strategien einführen, ohne vorhandenen Code zu ändern.

### UML-Struktur

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

## Warum das Strategie-Muster verwenden?

- **Beseitigt Konditionale** – Ersetzt `if/else`- oder `switch`-Blöcke durch polymorphe Delegation.
- **Offen für Erweiterungen, geschlossen für Änderungen** – Fügen Sie neue Strategien hinzu, ohne vorhandenen Code zu berühren.
- **Fördert Komposition** – Der Context hat eine Strategie, anstatt in einer Vererbungshierarchie festgelegt zu sein.
- **Einzelne Verantwortung** – Jeder Algorithmus ist in seiner eigenen Klasse isoliert, einfacher zu testen und zu warten.
- **Laufzeitflexibilität** – Ändern Sie das Verhalten eines Objekts zur Laufzeit, indem Sie seine Strategie austauschen.

### Wann anwenden

- Wenn Sie mehrere Algorithmen haben, die sich nur in ihrer Implementierung unterscheiden.
- Wenn Sie vermeiden möchten, komplexe, algorithmusspezifische Datenstrukturen gegenüber dem Client offenzulegen.
- Wenn eine Klasse eine umfangreiche Konditionale aufweist, die zwischen Varianten derselben Operation wechselt.
- Wenn Sie das Verhalten dynamisch ändern müssen (z. B. Zahlungsmethode, Sortierreihenfolge, Routenberechnung).

---

## Wie implementiert man das Muster (Installation des Musters)

Es ist keine Bibliotheks- oder Paketinstallation erforderlich – es ist ein Entwurfsmuster, das Sie im Code implementieren. Folgen Sie diesen drei Schritten:

1. **Definieren Sie eine Strategie-Schnittstelle oder abstrakte Klasse** – Deklariert die gemeinsame(n) Methode(n), die alle konkreten Strategien implementieren müssen.
2. **Erstellen Sie konkrete Strategien** – Implementieren Sie die Schnittstelle mit spezifischen Algorithmen. Jede Strategie ist eine in sich geschlossene Klasse.
3. **Modifizieren Sie den Context** – Fügen Sie ein Feld hinzu, das eine Referenz auf eine Strategie hält. Stellen Sie einen Setter (oder Konstruktorinjektion) bereit, um die Strategie zur Laufzeit zu ändern. Delegieren Sie die Ausführung des Algorithmus an das Strategieobjekt.

---

## Grundlegende Anwendungsbeispiele

### Java (Klassische OOP)

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

Dank Pythons First-Class-Funktionen können Strategien als einfache Funktionen oder Lambdas implementiert werden, was den Code reduziert.

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

### C# (Delegaten / Lambda-Strategien)

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

## Schlüsselfunktionen (mit Code-Demonstration)

### 1. Austausch des Algorithmus zur Laufzeit

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

### 2. Beseitigt konditionale Logik (Vorher vs. Nachher)

**Vorher (schlecht):**
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

**Nachher (Strategie-Muster):**
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

Kein `if/else` – setzen Sie einfach das entsprechende Strategieobjekt.

### 3. Open/Closed-Prinzip – Hinzufügen neuer Strategien

Sie können eine `DroneShipping`-Strategie hinzufügen, ohne `ShippingCalculator` zu ändern:

```java
public class DroneShipping implements ShippingStrategy {
    @Override
    public double calculate(Order order) {
        return order.getWeight() * 2.0 + 5; // flat fee
    }
}
```

Der vorhandene Code bleibt unverändert.

---

## Häufige Fallstricke

| Fallstrick | Vermeidungsstrategie |
|------------|----------------------|
| **Über-Engineering** – Strategien erstellen, wenn ein stabiler Algorithmus ausreicht. | Einfach beginnen; Strategien nur einführen, wenn Sie mehrere Varianten haben oder absehen. |
| **Client-Wissen** – Der Client muss wissen, welche Strategie auszuwählen ist. | Mit einer Factory oder einem Registry kombinieren, um die Strategieauswahl basierend auf Bedingungen zu automatisieren. |
| **Erhöhte Anzahl von Klassen** – Jede Strategie fügt eine neue Datei hinzu. | Lambdas, Funktionen oder Delegaten für kurzlebige oder einmalige Strategien verwenden. |
| **Zustandsbehaftete Strategien** – Gemeinsamer veränderlicher Zustand in einer Strategie kann Fehler verursachen, insbesondere in Multithreading-Umgebungen. | Zustandslose Strategien bevorzugen; wenn Zustand benötigt wird, kapseln Sie ihn in der Strategieinstanz und verwalten Sie den Lebenszyklus sorgfältig. |

---

## Verwandte Muster

- **State Pattern** – Sehr ähnliche Struktur, aber das State-Muster wird verwendet, um das Verhalten basierend auf dem internen Zustand zu ändern, während das Strategie-Muster dem Client ermöglicht, einen Algorithmus extern auszuwählen. Zustandsübergänge werden oft im Context verwaltet; die Strategieauswahl erfolgt typischerweise extern.
- **Template Method** – Definiert das Skelett eines Algorithmus und erlaubt Unterklassen, Schritte zu überschreiben. Das Strategie-Muster erreicht dasselbe Ziel durch Komposition anstelle von Vererbung.
- **Factory Pattern** – Wird oft verwendet, um das passende Strategieobjekt basierend auf Eingabe oder Konfiguration zu erstellen.
- **Decorator Pattern** – Kann mit dem Strategie-Muster kombiniert werden, um einem Strategieobjekt ohne Modifikation zusätzliche Verantwortlichkeiten hinzuzufügen.

---

## Zusammenfassung

Das Strategie-Muster ist ein mächtiges Werkzeug zur Verwaltung von Familien verwandter Algorithmen. Durch die Kapselung jedes Algorithmus in einer separaten Klasse (oder Funktion) gewinnen Sie Flexibilität, Wartbarkeit und Einhaltung der SOLID-Prinzipien. Verwenden Sie es, wenn Sie mehrere austauschbare Verhaltensweisen haben und starre konditionale Logik vermeiden möchten. Denken Sie daran: **Komposition vor Vererbung bevorzugen** – und lassen Sie die Strategien die Hauptarbeit erledigen.