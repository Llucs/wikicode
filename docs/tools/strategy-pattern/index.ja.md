---
title: ストラテジーパターン
description: 振る舞いに関するデザインパターンの一つで、アルゴリズムの一族を定義し、それぞれをカプセル化し、実行時に交換可能にするものです。
created: 2026-06-20
tags:
  - design-patterns
  - behavioral
  - oop
  - gang-of-four
status: draft
---

# Strategy Pattern

**Strategy Pattern**は、Gang of Four（GoF）による振る舞いに関するデザインパターンです。このパターンは、アルゴリズムの一族を定義し、それぞれを独自のクラスにカプセル化し、交換可能にします。Strategyオブジェクトにより、アルゴリズムをそれを使用するクライアント（Context）から独立して変更できるようになり、コンポジションによる柔軟性とコードの再利用性を促進します。

---

## Strategy Patternとは？

Strategy Patternの核心は、同じことを行う異なる方法をカプセル化し、コードの他の部分に影響を与えずに選択できるようにすることです。複数のアルゴリズムを条件分岐で単一のクラスに埋め込む代わりに、各アルゴリズムを個別の*strategy*クラスに抽出します。Context（アルゴリズムを使用するクラス）はこれらのstrategyのいずれかへの参照を保持し、実際の処理をそのstrategyに委譲します。

このパターンは**継承よりもコンポジション**の考え方に従い、**オープン・クローズドの原則**を満たします。既存のコードを変更することなく、新しいストラテジを導入できます。

### UML構造

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

## なぜStrategy Patternを使うのか？

- **条件分岐の排除** – `if/else`や`switch`をポリモーフィックな委譲に置き換えます。
- **拡張に対して開かれ、修正に対して閉じている** – 既存のコードに触れずに新しい戦略を追加できます。
- **コンポジションの促進** – ContextはStrategyを保持するため、継承階層に固定されません。
- **単一責任** – 各アルゴリズムが独自のクラスに分離され、テストや保守が容易になります。
- **実行時の柔軟性** – 戦略を切り替えることで、オブジェクトの振る舞いを実行時に変更できます。

### 使用すべき場合

- 実装のみが異なる複数のアルゴリズムがある場合。
- アルゴリズム固有の複雑なデータ構造をクライアントに公開したくない場合。
- クラスに同一操作のバリエーションを切り替える大規模な条件分岐がある場合。
- 振る舞いを動的に変更する必要がある場合（例：支払い方法、並べ替え順序、経路計算）。

---

## 実装方法（パターンの導入）

ライブラリやパッケージのインストールは必要ありません。コードで実装するデザインパターンです。以下の3つのステップに従います。

1. **Strategyインターフェースまたは抽象クラスを定義する**  
   すべての具象Strategyが実装する共通メソッドを宣言します。

2. **具体的なStrategyを作成する**  
   インターフェースを実装し、特定のアルゴリズムを提供します。各Strategyは自己完結型のクラスです。

3. **Contextを修正する**  
   - Strategyへの参照を保持するフィールドを追加します。  
   - 実行時にStrategyを変更するためのセッター（またはコンストラクタインジェクション）を用意します。  
   - アルゴリズムの実行をStrategyオブジェクトに委譲します。

---

## 基本的な使用例

### Java（古典的なOOP）

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

### Python（第一級関数）

Pythonの第一級関数により、Strategyはプレーンな関数やラムダとして実装でき、ボイラープレートが減ります。

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

### C#（デリゲート / ラムダStrategy）

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

## 主要な機能（コードデモ付き）

### 1. アルゴリズムの実行時交換

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

### 2. 条件分岐ロジックの排除（Before vs After）

**Before（悪い例）:**
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

**After（Strategyパターン適用後）:**
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

`if/else`はなくなり、適切なStrategyオブジェクトを設定するだけです。

### 3. オープン・クローズドの原則 – 新しいStrategyの追加

`ShippingCalculator`を変更することなく、`DroneShipping`戦略を追加できます。

```java
public class DroneShipping implements ShippingStrategy {
    @Override
    public double calculate(Order order) {
        return order.getWeight() * 2.0 + 5; // flat fee
    }
}
```

既存のコードは変更されません。

---

## よくある落とし穴

| 落とし穴 | 回避方法 |
|---------|--------------|
| **過剰な設計** – 1つの安定したアルゴリズムで十分な場合に戦略を作成してしまう。 | シンプルに始め、複数のバリエーションがある場合または予見される場合にのみ戦略を導入する。 |
| **クライアントの知識** – クライアントがどの戦略を選ぶべきかを知っている必要がある。 | FactoryやRegistryと組み合わせて、条件に基づいて戦略選択を自動化する。 |
| **クラス数の増加** – 各戦略が新しいファイルを追加する。 | 短命または一回限りの戦略には、ラムダ、関数、デリゲートを使用する。 |
| **状態を持つStrategy** – 戦略内の共有可変状態は、特にマルチスレッド環境でバグを引き起こす可能性がある。 | ステートレスな戦略を推奨。状態が必要な場合は、戦略インスタンス内にカプセル化し、ライフサイクルを慎重に管理する。 |

---

## 関連パターン

- **Stateパターン** – 非常に似た構造だが、Stateは内部状態に基づいて振る舞いを変更するために使用され、Strategyはクライアントが外部からアルゴリズムを選択できるようにする。Stateの遷移は通常Context内で管理され、Strategyの選択は通常外部で行われる。
- **Template Methodパターン** – アルゴリズムの骨格を定義し、サブクラスがステップをオーバーライドできるようにする。Strategyは継承ではなくコンポジションで同じ目標を達成する。
- **Factoryパターン** – 入力や設定に基づいて適切なStrategyオブジェクトを作成するためによく使用される。
- **Decoratorパターン** – Strategyと組み合わせて、Strategyオブジェクトを変更せずに責務を追加できる。

---

## まとめ

Strategy Patternは、関連するアルゴリズムの一族を管理するための強力なツールです。各アルゴリズムを個別のクラス（または関数）にカプセル化することで、柔軟性、保守性、SOLID原則への準拠が得られます。複数の交換可能な振る舞いがあり、硬直した条件ロジックを避けたい場合に使用してください。覚えておいてください：**継承よりもコンポジションを優先し**、戦略に重い処理を任せましょう。