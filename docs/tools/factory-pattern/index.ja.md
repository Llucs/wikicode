---
title: Factory Pattern
description: オブジェクト生成をカプセル化し、クライアントコードを具象実装から切り離して柔軟性を高める生成系デザインパターン。
created: 2026-06-19
tags:
  - design-patterns
  - creational
  - object-oriented
  - gof
status: draft
---

# Factory Pattern

## 概要
Factory Patternは**生成系デザインパターン**であり、インスタンス化ロジックをクライアントに公開せずにオブジェクトを作成するためのインターフェースまたはメソッドを提供します。`new`でコンストラクタを直接呼び出す代わりに、クライアントコードは作成処理を**ファクトリ**と呼ばれる別のクラス、メソッド、またはオブジェクトに委譲し、ファクトリが入力パラメータ、構成、またはコンテキストに基づいてインスタンス化する具象クラスを決定します。

このパターンはGang of Four (GoF)のデザインパターンの1つであり、一般的に以下の3つの亜種があります。

- **Simple Factory** – パラメータに基づいて異なる具象プロダクトを返す単一のクラスまたは静的メソッド。
- **Factory Method** – クラスが作成のための抽象メソッドを定義し、サブクラスがそれをオーバーライドして特定のプロダクトを生成する。
- **Abstract Factory** – 具象クラスを指定せずに関連オブジェクト群や依存オブジェクト群を生成するためのインターフェース。

## Factory Patternを使用する理由

- **疎結合**: クライアントコードは具体的な実装ではなく抽象（インターフェース/抽象クラス）に依存します。製品タイプを変更するには、多くの場合ファクトリのロジックを変更するだけで済み、クライアントを変更する必要はありません。
- **構築ロジックのカプセル化**: 複雑なオブジェクトアセンブリ、依存関係の配線、条件付きインスタンス化がファクトリ内部に隠蔽されます。
- **オープン/クローズドの原則**: 既存のクライアントコードを変更することなく、ファクトリを拡張（または新しい具象クリエイターを追加）することで、新しい製品タイプを導入できます。
- **単一責任**: 生成ロジックはビジネスロジックから分離され、各部分の保守性が向上します。
- **生成におけるポリモーフィズム**: クライアントは統一されたインターフェースを介して対話し、実際のランタイム型を意識しません。

## インストール / 前提条件

Factory Patternは**ライブラリやパッケージではありません** – 標準的なオブジェクト指向プログラミング（OOP）機能に完全に基づいた設計方法論です。インストールは不要で、以下の機能をサポートする任意の言語で実装できます。

- インターフェース、抽象クラス、またはダックタイピング（Python）
- 継承とポリモーフィズム
- カプセル化

主要な言語すべてで利用可能：Java、C#、C++、Python、TypeScript、Rubyなど。

## 主要な概念

- **Product（プロダクト）** – ファクトリが返す抽象的な型（インターフェース）。
- **Concrete Product（具象プロダクト）** – プロダクトインターフェースを実装するクラス。
- **Creator（クリエイター）** – ファクトリメソッドを宣言する、またはファクトリロジックを含むクラス。
- **Concrete Creator（具象クリエイター）** – (Factory Method) クリエイターのサブクラスで、ファクトリメソッドをオーバーライドして特定の具象プロダクトを生成する。
- **Client（クライアント）** – ファクトリを介してプロダクトを使用するコード。コンストラクタを直接呼び出すことはない。

## 使用法と例

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

## 主要機能

| 機能 | 説明 |
|---------|-------------|
| **生成のカプセル化** | 複雑なインスタンス化ロジック、依存関係管理、オブジェクトアセンブリを隠蔽します。 |
| **疎結合** | クライアントコードは抽象にのみ依存し、具象クラスには依存しません。 |
| **オープン/クローズドの原則** | 新しい製品を追加するには、既存のクライアントコードを変更せずに、新しいファクトリサブクラス（またはレジストリへの新しいエントリ）を追加するだけで済むことが多い。 |
| **単一責任** | 生成ロジックはファクトリに局所化され、コードベース全体に散らばらない。 |
| **生成におけるポリモーフィズム** | 返されたプロダクトはそのインターフェースを介して使用され、実際のクラスは実行時に変化し得る。 |
| **条件付きオブジェクト生成** | ファクトリは、どのオブジェクトを生成するかを決定するif-elseやswitchロジックを一元化し、保守と拡張を容易にする。 |

## ベストプラクティス

- **抽象に依存し、具象に依存しない。** クライアントは常にプロダクトインターフェースを介して操作すべきであり、具象クラスを直接使用すべきではありません。
- **ファクトリの責務に集中する。** ファクトリはオブジェクト作成のみを扱うべきであり、ビジネスロジックと混在させないでください。
- **ファクトリ内でレジストリまたはマップを使用する**ことで、if-elseの連鎖を減らし、新しい型の追加を簡単にします（上記のPythonのSimple Factoryの例を参照）。
- **パラメータ化されたファクトリ**を検討してください。`type`または`config`オブジェクトを受け取り、どの具象プロダクトをインスタンス化するかを決定します。
- **依存性注入と組み合わせる。** ファクトリをクライアントに注入することで、さらに結合度を下げ、テストを容易にします。

## よくある落とし穴

- **過度なエンジニアリング（Over-engineering）**: すべてのオブジェクトにファクトリが必要なわけではありません。生成ロジックが複雑である、変化する、または集中化する必要がある場合にのみ使用してください。
- **ファクトリの過剰**: 各プロダクトに専用のファクトリを用意すると、不必要な複雑さを招く可能性があります。よりシンプルなファクトリ（またはファクトリなし）で十分かどうかを評価してください。
- **ファクトリが隠しすぎる**: ファクトリがオブジェクトのライフサイクルの追跡を困難にしたり、目に見えない副作用を導入する場合は、設計を見直してください。
- **Simple FactoryとFactory Methodの混同**: これらは異なるパターンです。Simple Factoryは静的メソッドを使用します。Factory Methodは継承とポリモーフィズムを使用します。シナリオに適したバリエーションを選択してください。

## 関連パターン

- **Abstract Factory** – 複数のFactory Methodの上に構築されることが多く、製品群を扱います。
- **Singleton** – ファクトリは、インスタンスが1つだけでよい場合にシングルトンとして実装できます。
- **Prototype** – オブジェクトをゼロから作成する代わりに、プロトタイプを使用して既存のオブジェクトをクローンします。
- **Builder** – 複雑なオブジェクトの構築とその表現を分離します。通常は製品を1ステップで返すFactoryとは対照的です。
- **Template Method** – Factory MethodはTemplate Method内で使用されることが多く、サブクラスが作成する製品を定義できるようにします。

## 参考資料

- *Design Patterns: Elements of Reusable Object-Oriented Software* – Gamma, Helm, Johnson, Vlissides (GoF).
- *Head First Design Patterns* – Freeman & Freeman.
- [Refactoring Guru – Factory Method](https://refactoring.guru/design-patterns/factory-method)
- [Wikipedia – Factory Method Pattern](https://en.wikipedia.org/wiki/Factory_method_pattern)
- [SourceMaking – Factory Design Pattern](https://sourcemaking.com/design_patterns/factory_method)