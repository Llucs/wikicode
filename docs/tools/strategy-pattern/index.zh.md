---
title: 策略模式
description: 一种行为设计模式，定义一系列算法，将每个算法封装起来，并使它们可以在运行时互换。
created: 2026-06-20
tags:
  - design-patterns
  - behavioral
  - oop
  - gang-of-four
status: draft
---

# Strategy Pattern

**Strategy Pattern** 是 Gang of Four (GoF) 提出的一种行为设计模式。它定义一系列算法，将每个算法封装到自己的类中，并使它们可以互换。策略对象允许算法独立于使用它的客户端（Context）变化，通过组合促进灵活性和代码复用。

---

## 什么是 Strategy Pattern？

其核心在于，Strategy Pattern 将做同一件事的不同方法封装起来，以便你可以挑选和切换，而不会搞乱其他代码。与其将多个算法嵌入一个类中使用条件逻辑，不如将每个算法提取到自己的 *策略* 类中。Context（使用算法的类）持有对其中一个策略的引用，并将实际工作委托给它。

该模式遵循**组合优于继承**的哲学，并满足**开闭原则**——你可以引入新策略而不改变现有代码。

### UML 结构

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

## 为什么使用 Strategy Pattern？

- **消除条件语句** – 用多态委托替换 `if/else` 或 `switch` 代码块。
- **对扩展开放，对修改关闭** – 添加新策略无需修改现有代码。
- **促进组合** – Context 拥有一个 Strategy，而不是被锁定在继承层次结构中。
- **单一职责** – 每个算法被隔离在自己的类中，更易于测试和维护。
- **运行时灵活性** – 通过切换策略在运行时改变对象的行为。

### 何时使用

- 当你有多个算法仅在实现上有所不同时。
- 当你希望避免向客户端暴露复杂的、算法特定的数据结构时。
- 当一个类中有大量条件语句在同一个操作的多个变体之间切换时。
- 当你需要动态改变行为时（例如，支付方式、排序顺序、路线计算）。

---

## 如何实现（安装该模式）

不需要安装任何库或包——它是一个用代码实现的设计模式。请遵循以下三个步骤：

1. **定义一个 Strategy 接口或抽象类**  
   声明所有具体策略必须实现的公共方法。

2. **创建具体策略（Concrete Strategies）**  
   用特定算法实现接口。每个策略是一个独立的类。

3. **修改 Context**  
   - 添加一个字段来持有对 Strategy 的引用。  
   - 提供 setter（或构造函数注入）以在运行时更改策略。  
   - 将算法执行委托给策略对象。

---

## 基本用法示例

### Java（经典面向对象）

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

### Python（一等函数）

得益于 Python 的一等函数，策略可以是普通的函数或 lambda，减少了样板代码。

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

### C#（委托 / Lambda 策略）

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

## 主要特性（代码演示）

### 1. 运行时算法切换

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

### 2. 消除条件逻辑（改写前 vs 改写后）

**改写前（不良）：**
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

**改写后（Strategy 模式）：**
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

没有 `if/else`——只需设置适当的策略对象。

### 3. 开闭原则 – 添加新策略

你可以添加一个 `DroneShipping` 策略而不需要改变 `ShippingCalculator`：

```java
public class DroneShipping implements ShippingStrategy {
    @Override
    public double calculate(Order order) {
        return order.getWeight() * 2.0 + 5; // flat fee
    }
}
```

现有代码保持不变。

---

## 常见陷阱

| 陷阱 | 如何避免 |
|---------|--------------|
| **过度工程** – 当一个稳定的算法足够时创建策略。 | 从简单开始；仅当您拥有或预见多种变体时才引入策略。 |
| **客户端知识** – 客户端必须知道选择哪个策略。 | 与 Factory 或 Registry 结合，基于条件自动选择策略。 |
| **类数量增加** – 每个策略都增加一个新文件。 | 对于短暂或一次性的策略，使用 lambdas、函数或委托。 |
| **有状态策略** – 策略中的共享可变状态可能导致错误，特别是在多线程环境中。 | 首选无状态策略；如果需要状态，将其封装在策略实例中并小心管理其生命周期。 |

---

## 相关模式

- **State Pattern** – 结构非常相似，但 State 用于基于内部状态改变行为，而 Strategy 允许客户端从外部选择算法。状态转换通常在 Context 内部管理；策略选择通常是外部的。
- **Template Method** – 定义算法的骨架，让子类覆盖步骤。Strategy 通过组合而非继承达到同样目的。
- **Factory Pattern** – 常用于根据输入或配置创建适当的策略对象。
- **Decorator Pattern** – 可与 Strategy 结合，为策略对象添加职责而不修改它。

---

## 总结

Strategy Pattern 是管理相关算法族的强大工具。通过将每个算法封装在单独的类（或函数）中，你获得了灵活性、可维护性，并遵守 SOLID 原则。当你有多个可互换的行为并希望避免僵化的条件逻辑时使用它。记住：**优先使用组合而非继承**——并让策略承担重任。