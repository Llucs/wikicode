---
title: 单例模式 – 确保一个类只有一个实例
description: 单例是一种创建型设计模式，它限制一个类只有一个实例，并为其提供一个全局访问点，通常用于日志记录、配置和资源管理。
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

# 单例模式

**单例模式**是来自四人组（GoF）目录中的一种创建型设计模式。其目的是**确保一个类只有一个实例**，并提供一个**全局访问点**访问该实例。与静态工具类不同，单例可以参与继承、实现接口、支持懒加载，并且可以作为对象引用传递。

---

## 为什么使用单例模式？

当系统需要恰好一个对象来协调动作时，会使用单例。常见用例包括：

- **日志记录** – 将日志输出集中到单个文件或流。
- **配置** – 加载一次应用程序设置并共享。
- **资源池** – 管理一组固定的数据库连接或线程池。
- **缓存** – 维护单个内存缓存。
- **硬件控制器** – 与单个物理设备（打印机、GPU）交互。

**优点：**
- 对唯一实例的受控访问。
- 懒加载节省资源，如果对象从未使用的话。
- 可以被子类化（尽管很少见）并以多态方式使用。

---

## 关键特征（GoF定义）

1. **私有构造函数** – 防止外部实例化。
2. **持有唯一实例的静态成员**。
3. **公共静态方法（`getInstance()`）** – 获取实例的唯一方式。
4. **懒加载** – 仅在首次请求时创建实例（除非使用饿汉式初始化）。
5. **线程安全** – 必须防止并发创建多个实例。

---

## 实现（如何编码）

### 基础懒汉单例（非线程安全）

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

**警告：** 该版本在多线程环境中会失效——两个线程都可能看到 `instance == null` 并创建不同的对象。

### 线程安全的单例（同步访问器）

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

`synchronized` 关键字会增加性能开销，但它是有效的。

### 饿汉式初始化（依赖类加载器）

```java
public class Logger {
    private static final Logger INSTANCE = new Logger();

    private Logger() {}

    public static Logger getInstance() {
        return INSTANCE;
    }
}
```

- 实例在类加载时创建；由类加载器保证线程安全。
- 如果对象从未使用，资源仍会被分配。

### 双重检查锁定（使用 `volatile`）

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

- 在实例创建后减少开销。
- 需要 `volatile` 关键字（Java 5+）以防止部分构造的读取。

### 枚举单例（Java最佳实践）

```java
public enum Logger {
    INSTANCE;

    public void log(String message) {
        System.out.println(message);
    }
}
```

- **天生线程安全**，并防止反射、序列化和克隆攻击。
- 这是Java中推荐的方法（Effective Java，第3条）。

### C#示例（懒加载+线程安全）

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

### Python示例（模块级单例）

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

## 安装

**单例模式不是一个库或包。** 它是一种架构设计，直接在源代码中实现。你不能通过 npm、pip、Maven 或 NuGet 安装它。要“采用”这个模式，你只需像上面的示例那样编写必要的类。

---

## 使用示例

### 使用枚举单例进行日志记录（Java）

```java
Logger.INSTANCE.log("Application started");

// In another class:
Logger.INSTANCE.log("User logged in");
```

### 配置管理器（C#）

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

**使用：**

```csharp
string connStr = AppConfig.Instance.DbConnectionString;
```

---

## 批评（为什么有些人称它为反模式）

- **全局状态** – 单例引入了可变的全局状态，使得单元测试依赖于顺序且脆弱。
- **紧耦合** – `getInstance()` 强制代码依赖于具体类，违反了依赖倒置原则。
- **隐藏依赖** – 使用单例的类没有在其构造函数中声明该依赖；依赖隐藏在方法内部，使得API不清晰。
- **单一职责违反** – 该类必须管理自己的生命周期（懒加载、线程安全），同时还要处理核心逻辑。

---

## 现代替代方案

- **依赖注入（DI）** – IoC容器（Spring、Guice、ASP.NET Core）管理对象生命周期。一个类可以注册为*单例作用域*，但使用者依赖于接口，从而可以轻松模拟和替换。
- ***单态模式*（Monostate Pattern）** – 一种变体，类本身不是单例，但其所有字段都是静态的。多个实例共享同一状态。
- **静态工具类** – 适用于无状态的辅助类，但不能实现接口或利用多态。

---

## 结论

单例模式在审慎使用时是一种强大的工具。现代最佳实践倾向于使用依赖注入而不是直接的单例，因为它提高了可测试性和可维护性。当必须强制执行单个实例时，优先选择**基于枚举**（Java）或 `Lazy<T>`（C#）的实现，以避免线程安全陷阱。记住，“全局访问”也是全局耦合——谨慎而有意识地使用单例。

---

*参考文献：*  
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object‑Oriented Software*. Addison‑Wesley.  
- Bloch, J. (2008). *Effective Java* (2nd ed., Item 3). Addison‑Wesley.  
- Martin, R. C. (2003). *Agile Software Development, Principles, Patterns, and Practices*. Prentice Hall.