---
title: Padrão Strategy
description: Um padrão de design comportamental que define uma família de algoritmos, encapsula cada um deles e os torna intercambiáveis em tempo de execução.
created: 2026-06-20
tags:
  - design-patterns
  - behavioral
  - oop
  - gang-of-four
status: draft
---

# Padrão Strategy

O **Strategy Pattern** é um padrão de design comportamental do Gang of Four (GoF). Ele define uma família de algoritmos, encapsula cada um em sua própria classe e os torna intercambiáveis. O objeto de estratégia permite que o algoritmo varie independentemente dos clientes que o utilizam (o Contexto), promovendo flexibilidade e reuso de código através da composição.

---

## O que é o Padrão Strategy?

Em sua essência, o Strategy Pattern consiste em encapsular diferentes maneiras de fazer a mesma coisa para que você possa escolher sem bagunçar o resto do seu código. Em vez de incorporar múltiplos algoritmos em uma única classe com lógica condicional, você extrai cada algoritmo para sua própria classe de *estratégia*. O Contexto (a classe que usa um algoritmo) mantém uma referência a uma dessas estratégias e delega o trabalho real a ela.

O padrão segue a filosofia **composição em vez de herança** e satisfaz o **Princípio Aberto/Fechado** — você pode introduzir novas estratégias sem alterar o código existente.

### Estrutura UML

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

## Por que usar o Padrão Strategy?

- **Elimina condicionais** – Substitui blocos `if/else` ou `switch` por delegação polimórfica.
- **Aberto para extensão, fechado para modificação** – Adicione novas estratégias sem tocar no código existente.
- **Promove composição** – O Contexto possui uma Estratégia, em vez de estar preso a uma hierarquia de herança.
- **Responsabilidade Única** – Cada algoritmo é isolado em sua própria classe, mais fácil de testar e manter.
- **Flexibilidade em tempo de execução** – Altere o comportamento de um objeto em tempo de execução trocando sua estratégia.

### Quando usar

- Quando você tem múltiplos algoritmos que diferem apenas em sua implementação.
- Quando você deseja evitar expor estruturas de dados complexas e específicas do algoritmo ao cliente.
- Quando uma classe tem uma condicional enorme que alterna entre variantes da mesma operação.
- Quando você precisa alterar o comportamento dinamicamente (ex.: método de pagamento, ordem de classificação, cálculo de rota).

---

## Como implementar (Instale o padrão)

Nenhuma instalação de biblioteca ou pacote é necessária — é um padrão de design que você implementa no código. Siga estes três passos:

1. **Defina uma interface de Estratégia ou Classe Abstrata**  
   Declara o(s) método(s) comum(ns) que todas as estratégias concretas devem implementar.

2. **Crie Estratégias Concretas**  
   Implemente a interface com algoritmos específicos. Cada estratégia é uma classe autocontida.

3. **Modifique o Contexto**  
   - Adicione um campo para manter uma referência a uma Estratégia.  
   - Forneça um setter (ou injeção pelo construtor) para alterar a estratégia em tempo de execução.  
   - Delegue a execução do algoritmo ao objeto de estratégia.

---

## Exemplos de uso básico

### Java (OOP Clássico)

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

### Python (Funções de primeira classe)

Graças às funções de primeira classe do Python, as estratégias podem ser funções simples ou lambdas, reduzindo a verbosidade.

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

### C# (Delegados / Estratégias Lambda)

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

## Principais Características (com demonstração de código)

### 1. Troca de algoritmo em tempo de execução

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

### 2. Elimina lógica condicional (Antes vs Depois)

**Antes (ruim):**
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

**Depois (padrão Strategy):**
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

Sem `if/else` — basta definir o objeto de estratégia apropriado.

### 3. Princípio Aberto/Fechado – Adicionando novas estratégias

Você pode adicionar uma estratégia `DroneShipping` sem alterar `ShippingCalculator`:

```java
public class DroneShipping implements ShippingStrategy {
    @Override
    public double calculate(Order order) {
        return order.getWeight() * 2.0 + 5; // flat fee
    }
}
```

O código existente permanece inalterado.

---

## Armadilhas comuns

| Armadilha | Como evitar |
|-----------|-------------|
| **Excesso de engenharia** – Criar estratégias quando um algoritmo estável é suficiente. | Comece simples; introduza estratégias apenas quando você tiver ou prever múltiplas variantes. |
| **Conhecimento do cliente** – O cliente precisa saber qual estratégia escolher. | Combine com um Factory ou um Registry para automatizar a seleção da estratégia com base em condições. |
| **Número aumentado de classes** – Cada estratégia adiciona um novo arquivo. | Use lambdas, funções ou delegados para estratégias de curta duração ou únicas. |
| **Estratégias com estado** – Estado mutável compartilhado em uma estratégia pode causar bugs, especialmente em contextos multithread. | Prefira estratégias sem estado; se o estado for necessário, encapsule-o na instância da estratégia e gerencie seu ciclo de vida cuidadosamente. |

---

## Padrões Relacionados

- **State Pattern** – Estrutura muito semelhante, mas State é usado para alterar o comportamento com base no estado interno, enquanto Strategy permite que o cliente escolha um algoritmo externamente. As transições de estado geralmente são gerenciadas dentro do Contexto; a seleção da Strategy geralmente é externa.
- **Template Method** – Define o esqueleto de um algoritmo, permitindo que subclasses substituam etapas. Strategy atinge o mesmo objetivo por meio de composição em vez de herança.
- **Factory Pattern** – Frequentemente usado para criar o objeto de estratégia apropriado com base em entrada ou configuração.
- **Decorator Pattern** – Pode ser combinado com Strategy para adicionar responsabilidades a um objeto de estratégia sem modificá-lo.

---

## Resumo

O Strategy Pattern é uma ferramenta poderosa para gerenciar famílias de algoritmos relacionados. Ao encapsular cada algoritmo em uma classe (ou função) separada, você ganha flexibilidade, facilidade de manutenção e adesão aos princípios SOLID. Use-o quando tiver múltiplos comportamentos intercambiáveis e quiser evitar lógica condicional rígida. Lembre-se: **prefira composição em vez de herança** — e deixe as estratégias fazerem o trabalho pesado.