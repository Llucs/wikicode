---
title: Patrón Strategy
description: Un patrón de diseño de comportamiento que define una familia de algoritmos, encapsula cada uno y los hace intercambiables en tiempo de ejecución.
created: 2026-06-20
tags:
  - design-patterns
  - behavioral
  - oop
  - gang-of-four
status: draft
---

# Patrón Strategy

El **Patrón Strategy** es un patrón de diseño de comportamiento del Gang of Four (GoF). Define una familia de algoritmos, encapsula cada uno en su propia clase y los hace intercambiables. El objeto de estrategia permite que el algoritmo varíe independientemente de los clientes que lo usan (el Contexto), promoviendo flexibilidad y reutilización de código mediante composición.

---

## ¿Qué es el Patrón Strategy?

En esencia, el Patrón Strategy consiste en encapsular diferentes formas de hacer lo mismo para que puedas elegir sin alterar el resto de tu código. En lugar de incrustar múltiples algoritmos en una sola clase con lógica condicional, extraes cada algoritmo en su propia clase de *estrategia*. El Contexto (la clase que usa un algoritmo) mantiene una referencia a una de estas estrategias y delega el trabajo real en ella.

El patrón sigue la filosofía de **composición sobre herencia** y cumple con el **Principio Abierto/Cerrado**: puedes introducir nuevas estrategias sin modificar el código existente.

### Estructura UML

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

## ¿Por qué usar el Patrón Strategy?

- **Elimina condicionales** – Reemplaza bloques `if/else` o `switch` con delegación polimórfica.
- **Abierto para extensión, cerrado para modificación** – Agrega nuevas estrategias sin tocar el código existente.
- **Promueve la composición** – El Contexto tiene una Estrategia, en lugar de estar atado a una jerarquía de herencia.
- **Responsabilidad Única** – Cada algoritmo está aislado en su propia clase, más fácil de probar y mantener.
- **Flexibilidad en tiempo de ejecución** – Cambia el comportamiento de un objeto en tiempo de ejecución intercambiando su estrategia.

### Cuándo usarlo

- Cuando tienes múltiples algoritmos que difieren solo en su implementación.
- Cuando quieres evitar exponer al cliente estructuras de datos complejas y específicas del algoritmo.
- Cuando una clase tiene un condicional enorme que alterna entre variantes de la misma operación.
- Cuando necesitas cambiar el comportamiento dinámicamente (ej: método de pago, orden de ordenamiento, cálculo de ruta).

---

## Cómo implementar (Instalar el Patrón)

No se requiere instalación de librerías o paquetes: es un patrón de diseño que se implementa en código. Sigue estos tres pasos:

1. **Define una interfaz o clase abstracta de Strategy**  
   Declara el/los método(s) común(es) que todas las estrategias concretas deben implementar.

2. **Crea estrategias concretas**  
   Implementa la interfaz con algoritmos específicos. Cada estrategia es una clase autocontenida.

3. **Modifica el Contexto**  
   - Agrega un campo para almacenar una referencia a una Estrategia.  
   - Proporciona un setter (o inyección por constructor) para cambiar la estrategia en tiempo de ejecución.  
   - Delega la ejecución del algoritmo al objeto de estrategia.

---

## Ejemplos Básicos de Uso

### Java (POO Clásica)

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

### Python (Funciones de Primera Clase)

Gracias a las funciones de primera clase de Python, las estrategias pueden ser funciones simples o lambdas, reduciendo código repetitivo.

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

### C# (Delegados / Estrategias Lambda)

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

## Características Clave (con Demostración de Código)

### 1. Intercambio en Tiempo de Ejecución del Algoritmo

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

### 2. Elimina la Lógica Condicional (Antes vs Después)

**Antes (malo):**
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

**Después (Patrón Strategy):**
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

Sin `if/else` — solo asigna el objeto de estrategia adecuado.

### 3. Principio Abierto/Cerrado – Agregar Nuevas Estrategias

Puedes agregar una estrategia `DroneShipping` sin modificar `ShippingCalculator`:

```java
public class DroneShipping implements ShippingStrategy {
    @Override
    public double calculate(Order order) {
        return order.getWeight() * 2.0 + 5; // flat fee
    }
}
```

El código existente permanece sin cambios.

---

## Errores Comunes

| Error Común | Cómo Evitarlo |
|-------------|---------------|
| **Sobreingeniería** – Crear estrategias cuando un solo algoritmo estable es suficiente. | Comienza simple; introduce estrategias solo cuando tengas o anticipes múltiples variantes. |
| **Conocimiento del cliente** – El cliente debe saber qué estrategia elegir. | Combínalo con un Factory o un Registry para automatizar la selección de estrategias según condiciones. |
| **Aumento en el número de clases** – Cada estrategia agrega un nuevo archivo. | Usa lambdas, funciones o delegados para estrategias de corta duración o únicas. |
| **Estrategias con estado** – El estado mutable compartido en una estrategia puede causar errores, especialmente en contextos multi-hilo. | Prefiere estrategias sin estado; si se necesita estado, encapsúlalo en la instancia de la estrategia y gestiona su ciclo de vida cuidadosamente. |

---

## Patrones Relacionados

- **State Pattern** – Estructura muy similar, pero State se usa para cambiar el comportamiento según el estado interno, mientras que Strategy permite al cliente elegir un algoritmo externamente. Las transiciones de estado a menudo se gestionan dentro del Contexto; la selección de Strategy es típicamente externa.
- **Template Method** – Define el esqueleto de un algoritmo, permitiendo que las subclases sobrescriban pasos. Strategy logra el mismo objetivo mediante composición en lugar de herencia.
- **Factory Pattern** – Se usa a menudo para crear el objeto de estrategia adecuado según la entrada o configuración.
- **Decorator Pattern** – Se puede combinar con Strategy para añadir responsabilidades a un objeto de estrategia sin modificarlo.

---

## Resumen

El Patrón Strategy es una herramienta poderosa para gestionar familias de algoritmos relacionados. Al encapsular cada algoritmo en una clase (o función) separada, obtienes flexibilidad, mantenibilidad y adherencia a los principios SOLID. Úsalo cuando tengas múltiples comportamientos intercambiables y quieras evitar una lógica condicional rígida. Recuerda: **favorece la composición sobre la herencia** — y deja que las estrategias hagan el trabajo pesado.