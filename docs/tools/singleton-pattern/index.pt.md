---
title: Singleton Pattern – Garantir que uma Classe Tenha Apenas Uma Instância
description: O Singleton é um padrão de design criacional que restringe uma classe a uma única instância e fornece um ponto de acesso global a ela, comumente usado para logging, configuração e gerenciamento de recursos.
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

# Singleton Pattern

O **Singleton Pattern** é um padrão de design criacional do catálogo Gang of Four (GoF). Seu propósito é **garantir que uma classe tenha apenas uma instância** e fornecer um **ponto de acesso global** a essa instância. Diferente de uma classe utilitária estática, um Singleton pode participar de herança, implementar interfaces, suportar inicialização lazy e ser passado como referência de objeto.

---

## Por que Usar o Singleton Pattern?

Singletons são usados quando exatamente um objeto é necessário para coordenar ações em todo o sistema. Casos de uso comuns incluem:

- **Logging** – Centralizar a saída de log em um único arquivo ou stream.
- **Configuration** – Carregar as configurações da aplicação uma vez e compartilhá-las.
- **Resource Pools** – Gerenciar um conjunto fixo de conexões de banco de dados ou pools de threads.
- **Caching** – Manter um único cache em memória.
- **Hardware Controllers** – Interfacear com um único dispositivo físico (impressora, GPU).

**Benefícios:**
- Acesso controlado a uma instância única.
- Instanciação lazy economiza recursos se o objeto nunca for usado.
- Pode ser subclassificado (embora raramente) e usado polimorficamente.

---

## Características Principais (Definição GoF)

1. **Construtor privado** – Impede instanciação externa.
2. **Membro estático** que mantém a instância única.
3. **Método público estático** (`getInstance()`) – A única maneira de obter a instância.
4. **Inicialização lazy** – A instância é criada somente quando solicitada pela primeira vez (a menos que inicialização eager seja usada).
5. **Thread safety** – Deve proteger contra criação concorrente de múltiplas instâncias.

---

## Implementação (Como Codificar)

### Singleton Lazy Básico (Não Thread‑Safe)

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

**Aviso:** Esta versão quebra em um ambiente multithread—duas threads podem cada uma ver `instance == null` e criar objetos separados.

### Singleton Thread‑Safe (Acessor Sincronizado)

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

A palavra-chave `synchronized` adiciona uma sobrecarga de performance, mas funciona.

### Inicialização Eager (Depende do Class Loader)

```java
public class Logger {
    private static final Logger INSTANCE = new Logger();

    private Logger() {}

    public static Logger getInstance() {
        return INSTANCE;
    }
}
```

- A instância é criada quando a classe é carregada; thread‑safe pelo class loader.
- Se o objeto nunca for usado, o recurso ainda é alocado.

### Double‑Checked Locking (com `volatile`)

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

- Reduz a sobrecarga após a instância ser criada.
- Requer a palavra-chave `volatile` (Java 5+) para evitar leituras de construção parcial.

### Enum Singleton (Melhor Prática Java)

```java
public enum Logger {
    INSTANCE;

    public void log(String message) {
        System.out.println(message);
    }
}
```

- **Inerentemente thread‑safe** e protege contra ataques de reflexão, serialização e clonagem.
- Esta é a abordagem recomendada em Java (Effective Java, Item 3).

### Exemplo em C# (Lazy + Thread‑Safe)

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

### Exemplo em Python (Singleton em Nível de Módulo)

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

## Instalação

**O Singleton pattern não é uma biblioteca ou pacote.** É um design arquitetural implementado diretamente em seu código fonte. Você não o instala via npm, pip, Maven, ou NuGet. Para “adotar” o padrão, você escreve a classe necessária conforme mostrado nos exemplos acima.

---

## Exemplos de Uso

### Logging com o Enum Singleton (Java)

```java
Logger.INSTANCE.log("Application started");

// In another class:
Logger.INSTANCE.log("User logged in");
```

### Configuration Manager (C#)

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

**Uso:**

```csharp
string connStr = AppConfig.Instance.DbConnectionString;
```

---

## Críticas (Por que Alguns o Chamam de Anti‑Pattern)

- **Estado Global** – O Singleton introduz estado global mutável, que torna os testes unitários dependentes de ordem e frágeis.
- **Acoplamento Forte** – `getInstance()` força o código a depender da classe concreta, violando o Princípio da Inversão de Dependência.
- **Dependências Ocultas** – Uma classe que usa um Singleton não o declara em seu construtor; a dependência fica enterrada dentro dos métodos, tornando a API obscura.
- **Violação da Responsabilidade Única** – A classe deve gerenciar seu próprio ciclo de vida (inicialização lazy, thread safety) além de sua lógica central.

---

## Alternativas Modernas

- **Injeção de Dependência (DI)** – Um contêiner IoC (Spring, Guice, ASP.NET Core) gerencia os tempos de vida dos objetos. Uma classe pode ser registrada com *escopo singleton*, mas os consumidores dependem de uma interface, permitindo fácil mocking e substituição.
- **Monostate Pattern** – Uma variação onde a classe em si não é um singleton, mas todos os seus campos são estáticos. Múltiplas instâncias compartilham o mesmo estado.
- **Classe Utilitária Estática** – Funciona para helpers sem estado, mas não pode implementar interfaces ou se beneficiar do polimorfismo.

---

## Conclusão

O Singleton pattern é uma ferramenta poderosa quando usada deliberadamente. As melhores práticas modernas favorecem a injeção de dependência em vez de singletons diretos porque melhora a testabilidade e a manutenibilidade. Quando você precisa garantir uma única instância, prefira implementações **baseadas em enum** (Java) ou `Lazy<T>` (C#) para evitar armadilhas de thread safety. Lembre-se que “acesso global” também é acoplamento global—use Singletons com moderação e consciência.

---

*Referências:*  
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object‑Oriented Software*. Addison‑Wesley.  
- Bloch, J. (2008). *Effective Java* (2nd ed., Item 3). Addison‑Wesley.  
- Martin, R. C. (2003). *Agile Software Development, Principles, Patterns, and Practices*. Prentice Hall.