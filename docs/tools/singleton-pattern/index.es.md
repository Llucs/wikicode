---
title: Patrón Singleton – Asegurar que una clase tenga una única instancia
description: Singleton es un patrón de diseño creacional que restringe una clase a una única instancia y proporciona un punto de acceso global a ella, comúnmente utilizado para registro, configuración y gestión de recursos.
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

# Patrón Singleton

El **Patrón Singleton** es un patrón de diseño creacional del catálogo de la Gang of Four (GoF). Su propósito es **asegurar que una clase tenga una única instancia** y proporcionar un **punto de acceso global** a esa instancia. A diferencia de una clase de utilidad estática, un Singleton puede participar en herencia, implementar interfaces, soportar inicialización perezosa y ser pasado como referencia de objeto.

---

## ¿Por qué usar el Patrón Singleton?

Los Singletons se utilizan cuando se necesita exactamente un objeto para coordinar acciones en un sistema. Los casos de uso comunes incluyen:

- **Logging** – Centralizar la salida de logs en un único archivo o flujo.
- **Configuration** – Cargar la configuración de la aplicación una vez y compartirla.
- **Resource Pools** – Gestionar un conjunto fijo de conexiones de base de datos o pools de hilos.
- **Caching** – Mantener una única caché en memoria.
- **Hardware Controllers** – Interfaz con un único dispositivo físico (impresora, GPU).

**Beneficios:**
- Acceso controlado a una instancia única.
- La instanciación perezosa ahorra recursos si el objeto nunca se utiliza.
- Puede ser subclasado (aunque raramente) y utilizado polimórficamente.

---

## Características Clave (Definición de GoF)

1. **Constructor privado** – Previene la instanciación externa.
2. **Miembro estático** que contiene la instancia única.
3. **Método público estático** (`getInstance()`) – La única forma de obtener la instancia.
4. **Inicialización perezosa** – La instancia se crea solo cuando se solicita por primera vez (a menos que se use inicialización temprana).
5. **Seguridad en hilos** – Debe protegerse contra la creación concurrente de múltiples instancias.

---

## Implementación (Cómo Programarlo)

### Singleton Básico Perezoso (No Seguro para Hilos)

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

**Advertencia:** Esta versión falla en un entorno multihilo: dos hilos podrían ver `instance == null` y crear objetos separados.

### Singleton Seguro para Hilos (Accesor Sincronizado)

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

La palabra clave `synchronized` añade una sobrecarga de rendimiento, pero funciona.

### Inicialización Temprana (Depende del Cargador de Clases)

```java
public class Logger {
    private static final Logger INSTANCE = new Logger();

    private Logger() {}

    public static Logger getInstance() {
        return INSTANCE;
    }
}
```

- La instancia se crea cuando la clase se carga; es segura para hilos gracias al cargador de clases.
- Si el objeto nunca se usa, el recurso se asigna de todas formas.

### Double‑Checked Locking (con `volatile`)

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

- Reduce la sobrecarga después de que se crea la instancia.
- Requiere la palabra clave `volatile` (Java 5+) para evitar lecturas de construcción parcial.

### Enum Singleton (Mejor Práctica en Java)

```java
public enum Logger {
    INSTANCE;

    public void log(String message) {
        System.out.println(message);
    }
}
```

- **Inherentemente seguro para hilos** y protege contra ataques de reflexión, serialización y clonación.
- Este es el enfoque recomendado en Java (Effective Java, Item 3).

### Ejemplo en C# (Perezoso + Seguro para Hilos)

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

### Ejemplo en Python (Singleton a Nivel de Módulo)

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

## Instalación

**El patrón Singleton no es una biblioteca ni un paquete.** Es un diseño arquitectónico implementado directamente en tu código fuente. No se instala mediante npm, pip, Maven o NuGet. Para “adoptar” el patrón, escribes la clase necesaria como se muestra en los ejemplos anteriores.

---

## Ejemplos de Uso

### Registro con el Enum Singleton (Java)

```java
Logger.INSTANCE.log("Application started");

// In another class:
Logger.INSTANCE.log("User logged in");
```

### Gestor de Configuración (C#)

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

## Críticas (Por Qué Algunos lo Llaman un Anti‑Patrón)

- **Estado Global** – El Singleton introduce estado global mutable, lo que hace que las pruebas unitarias dependan del orden y sean frágiles.
- **Acoplamiento Fuerte** – `getInstance()` obliga al código a depender de la clase concreta, violando el Principio de Inversión de Dependencias.
- **Dependencias Ocultas** – Una clase que usa un Singleton no lo declara en su constructor; la dependencia está enterrada dentro de los métodos, haciendo la API poco clara.
- **Violación del Principio de Responsabilidad Única** – La clase debe gestionar su propio ciclo de vida (inicialización perezosa, seguridad en hilos) además de su lógica central.

---

## Alternativas Modernas

- **Inyección de Dependencias (DI)** – Un contenedor IoC (Spring, Guice, ASP.NET Core) gestiona los tiempos de vida de los objetos. Una clase puede registrarse con *ámbito singleton*, pero los consumidores dependen de una interfaz, permitiendo fácil mocking e intercambio.
- **Patrón Monostate** – Una variación donde la clase en sí no es un singleton, pero todos sus campos son estáticos. Múltiples instancias comparten el mismo estado.
- **Clase de Utilidad Estática** – Funciona para ayudantes sin estado pero no puede implementar interfaces ni beneficiarse del polimorfismo.

---

## Conclusión

El patrón Singleton es una herramienta poderosa cuando se usa deliberadamente. Las mejores prácticas modernas favorecen la inyección de dependencias sobre los singletons directos porque mejora la capacidad de prueba y el mantenimiento. Cuando debas imponer una única instancia, prefiere implementaciones basadas en **enum** (Java) o `Lazy<T>` (C#) para evitar problemas de seguridad en hilos. Recuerda que el “acceso global” también es acoplamiento global: usa Singletons con moderación y conciencia.

---

*Referencias:*  
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object‑Oriented Software*. Addison‑Wesley.  
- Bloch, J. (2008). *Effective Java* (2nd ed., Item 3). Addison‑Wesley.  
- Martin, R. C. (2003). *Agile Software Development, Principles, Patterns, and Practices*. Prentice Hall.