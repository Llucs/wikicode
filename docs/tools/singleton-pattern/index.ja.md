---
title: Singletonパターン – クラスが単一のインスタンスのみを持つことを保証する
description: Singletonは、生成に関するデザインパターンであり、クラスを単一のインスタンスに制限し、そのインスタンスへのグローバルなアクセスポイントを提供します。ロギング、設定、リソース管理などで一般的に使用されます。
created: 2026-06-18
tags:
  - singleton
  - design-patterns
  - creational
  - gang-of-four
  - java
  - csharp
  - python
  - software-engineering
status: draft
---

# Singletonパターン

**Singletonパターン**は、GoF（Gang of Four）のカタログに掲載された生成に関するデザインパターンです。その目的は、**クラスが単一のインスタンスしか持たないことを保証**し、そのインスタンスへの**グローバルなアクセスポイント**を提供することです。静的なユーティリティクラスとは異なり、Singletonは継承に参加したり、インターフェースを実装したり、lazy initializationをサポートしたり、オブジェクト参照として渡したりすることができます。

---

## なぜSingletonパターンを使うのか？

Singletonは、システム全体でアクションを調整するために厳密に1つのオブジェクトが必要な場合に使用されます。一般的な使用例は以下の通りです：

- **ロギング** – ログ出力を単一のファイルまたはストリームに集中化する。
- **設定** – アプリケーション設定を一度ロードして共有する。
- **リソースプール** – データベース接続やスレッドプールの固定セットを管理する。
- **キャッシュ** – 単一のインメモリキャッシュを維持する。
- **ハードウェアコントローラー** – 単一の物理デバイス（プリンター、GPU）とのインターフェース。

**利点:**

- ユニークなインスタンスへの制御されたアクセス。
- オブジェクトが使用されない場合、lazy instantiationによりリソースを節約。
- サブクラス化（まれではあるが）が可能で、ポリモーフィックに使用可能。

---

## 主要な特性（GoFの定義）

1. **プライベートコンストラクタ** – 外部からのインスタンス化を防ぐ。
2. **静的メンバ** – 単一のインスタンスを保持する。
3. **パブリック静的メソッド**（`getInstance()`）– インスタンスを取得する唯一の方法。
4. **Lazy initialization** – インスタンスは初めて要求されたときにのみ作成される（eager initializationが使用されていない限り）。
5. **Thread safety** – 複数のインスタンスが同時に作成されないように保護する必要がある。

---

## 実装（コーディング方法）

### 基本的な遅延Singleton (Not Thread‑Safe)

```java
public class Logger {
    private static Logger instance;

    private Logger() {}

    public static Logger getInstance() {
        if (instance == null) {
            instance = new Logger();
        }
        return instance;
    }

    public void log(String message) {
        System.out.println(message);
    }
}
```

**警告:** このバージョンはマルチスレッド環境では壊れます—2つのスレッドがそれぞれ `instance == null` を確認し、別々のオブジェクトを作成する可能性があります。

### Thread‑Safe Singleton (Synchronized Accessor)

```java
public class Logger {
    private static Logger instance;

    private Logger() {}

    public static synchronized Logger getInstance() {
        if (instance == null) {
            instance = new Logger();
        }
        return instance;
    }
}
```

`synchronized`キーワードはパフォーマンスオーバーヘッドを追加しますが、機能します。

### Eager Initialization (Relies on Class Loader)

```java
public class Logger {
    private static final Logger INSTANCE = new Logger();

    private Logger() {}

    public static Logger getInstance() {
        return INSTANCE;
    }
}
```

- インスタンスはクラスがロードされたときに作成され、class loader によって thread-safe です。
- オブジェクトが使用されない場合でも、リソースは割り当てられます。

### Double‑Checked Locking（`volatile`使用）

```java
public class Logger {
    private static volatile Logger instance;

    private Logger() {}

    public static Logger getInstance() {
        if (instance == null) {
            synchronized (Logger.class) {
                if (instance == null) {
                    instance = new Logger();
                }
            }
        }
        return instance;
    }
}
```

- インスタンス作成後のオーバーヘッドを削減します。
- `volatile`キーワード（Java 5+）が必要です。部分的な構築読み取りを防ぐため。

### Enum Singleton (Java Best Practice)

```java
public enum Logger {
    INSTANCE;

    public void log(String message) {
        System.out.println(message);
    }
}
```

- **本質的に thread-safe** であり、リフレクション、シリアライゼーション、クローン攻撃から保護します。
- これはJavaで推奨されるアプローチです（Effective Java、項目3）。

### C# の例 (Lazy + Thread‑Safe)

```csharp
public sealed class Logger
{
    private static readonly Lazy<Logger> lazy =
        new Lazy<Logger>(() => new Logger());

    public static Logger Instance => lazy.Value;

    private Logger() {}

    public void Log(string message) => Console.WriteLine(message);
}
```

### Python の例 (Module‑Level Singleton)

```python
class _Logger:
    def log(self, msg):
        print(msg)

# Module-level variable acts as the single instance
logger = _Logger()
```

```python
# More explicit approach using __new__
class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def log(self, msg):
        print(msg)
```

---

## インストール

**Singletonパターンはライブラリやパッケージではありません。** ソースコードに直接実装するアーキテクチャデザインです。npm、pip、Maven、NuGetなどを介してインストールすることはありません。パターンを「採用」するには、上記の例のように必要なクラスを記述します。

---

## 使用例

### Enum Singletonを使用したロギング（Java）

```java
Logger.INSTANCE.log("Application started");

// In another class:
Logger.INSTANCE.log("User logged in");
```

### 設定マネージャー (C#)

```csharp
public sealed class AppConfig
{
    private static readonly Lazy<AppConfig> lazy =
        new Lazy<AppConfig>(() => new AppConfig());

    public static AppConfig Instance => lazy.Value;

    public string DbConnectionString { get; private set; }
    public int MaxThreads { get; private set; }

    private AppConfig()
    {
        // Load from appsettings.json or environment
        DbConnectionString = "Server=myServer;Database=myDB;";
        MaxThreads = 10;
    }
}
```

**使用例:**

```csharp
string connStr = AppConfig.Instance.DbConnectionString;
```

---

## 批判（なぜ一部ではアンチパターンと呼ばれるのか）

- **グローバルステート** – Singletonは変更可能なグローバル状態を導入し、単体テストを順序依存で脆弱にします。
- **Tight Coupling（密結合）** – `getInstance()` はコードを具象クラスに依存させ、Dependency Inversion Principle（依存関係逆転の原則）に違反します。
- **Hidden Dependencies（隠れた依存関係）** – Singletonを使用するクラスはコンストラクタでそれを宣言せず、依存関係がメソッド内部に埋もれ、APIが不明確になります。
- **Single Responsibility Violation（単一責任の違反）** – クラスはコアロジックに加えて、自身のライフサイクル（lazy initialization, thread safety）を管理しなければなりません。

---

## 現代的な代替案

- **Dependency Injection（DI）** – IoCコンテナ（Spring、Guice、ASP.NET Core）がオブジェクトのライフタイムを管理します。クラスは *singleton scope* で登録できますが、コンシューマーはインターフェースに依存するため、モック化や差し替えが容易です。
- **Monostateパターン** – クラス自体はシングルトンではありませんが、すべてのフィールドが静的であるバリエーション。複数のインスタンスが同じ状態を共有します。
- **静的ユーティリティクラス** – ステートレスなヘルパーに適していますが、インターフェースを実装したりポリモーフィズムを利用したりすることはできません。

---

## 結論

Singletonパターンは、意図的に使用された場合に強力なツールです。現代のベストプラクティスでは、テスト容易性と保守性が向上するため、直接的なSingletonよりもDependency Injection（依存性注入）が好まれます。単一のインスタンスを強制する必要がある場合は、thread‑safetyの落とし穴を避けるために、**enumベース**（Java）または `Lazy<T>`（C#）の実装を優先してください。「グローバルアクセス」はグローバル結合でもあることを忘れずに、Singletonは控えめかつ意識的に使用してください。

---

*参考文献:*  
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object‑Oriented Software*. Addison‑Wesley.  
- Bloch, J. (2008). *Effective Java* (2nd ed., Item 3). Addison‑Wesley.  
- Martin, R. C. (2003). *Agile Software Development, Principles, Patterns, and Practices*. Prentice Hall.