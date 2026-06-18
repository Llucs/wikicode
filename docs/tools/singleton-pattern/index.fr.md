---
title: Singleton Pattern – Assurer qu’une classe n’a qu’une seule instance
description: Le Singleton est un design pattern de création qui restreint une classe à une seule instance et fournit un point d’accès global à celle-ci, couramment utilisé pour la journalisation, la configuration et la gestion des ressources.
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

Le **Singleton Pattern** est un design pattern de création du catalogue Gang of Four (GoF). Son but est de **garantir qu’une classe n’a qu’une seule instance** et de fournir un **point d’accès global** à cette instance. Contrairement à une classe utilitaire statique, un Singleton peut participer à l’héritage, implémenter des interfaces, supporter l’initialisation paresseuse et être passé comme référence d’objet.

---

## Pourquoi utiliser le Singleton Pattern ?

Les Singletons sont utilisés lorsqu’exactement un objet est nécessaire pour coordonner des actions à travers un système. Les cas d’utilisation courants incluent :

- **Journalisation** – Centraliser la sortie des logs dans un seul fichier ou flux.
- **Configuration** – Charger les paramètres de l’application une fois et les partager.
- **Pools de ressources** – Gérer un ensemble fixe de connexions à la base de données ou de pools de threads.
- **Mise en cache** – Maintenir un seul cache en mémoire.
- **Contrôleurs matériels** – Interface avec un seul périphérique physique (imprimante, GPU).

**Avantages :**
- Accès contrôlé à une instance unique.
- L’instanciation paresseuse économise des ressources si l’objet n’est jamais utilisé.
- Peut être sous-classé (bien que rarement) et utilisé de manière polymorphe.

---

## Caractéristiques clés (définition GoF)

1. **Constructeur privé** – Empêche l’instanciation externe.
2. **Membre statique** qui contient l’instance unique.
3. **Méthode statique publique** (`getInstance()`) – La seule façon d’obtenir l’instance.
4. **Initialisation paresseuse** – L’instance n’est créée que lors de la première demande (sauf si une initialisation immédiate est utilisée).
5. **Sécurité des threads** – Doit se prémunir contre la création concurrente de plusieurs instances.

---

## Implémentation (Comment le coder)

### Singleton paresseux de base (non thread‑safe)

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

**Avertissement :** Cette version échoue dans un environnement multithreadé – deux threads pourraient chacun voir `instance == null` et créer des objets séparés.

### Singleton thread‑safe (Accesseur synchronisé)

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

Le mot-clé `synchronized` ajoute un surcoût de performance, mais cela fonctionne.

### Initialisation immédiate (repose sur le chargeur de classe)

```java
public class Logger {
    private static final Logger INSTANCE = new Logger();

    private Logger() {}

    public static Logger getInstance() {
        return INSTANCE;
    }
}
```

- L’instance est créée lorsque la classe est chargée ; thread‑safe grâce au chargeur de classe.
- Si l’objet n’est jamais utilisé, la ressource est quand même allouée.

### Double vérification avec verrouillage (avec `volatile`)

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

- Réduit le surcoût après la création de l’instance.
- Nécessite le mot-clé `volatile` (Java 5+) pour empêcher les lectures de construction partielle.

### Singleton par énumération (meilleure pratique Java)

```java
public enum Logger {
    INSTANCE;

    public void log(String message) {
        System.out.println(message);
    }
}
```

- **Intrinsèquement thread‑safe** et protège contre les attaques par réflexion, sérialisation et clonage.
- C’est l’approche recommandée en Java (Effective Java, Item 3).

### Exemple en C# (paresseux + thread‑safe)

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

### Exemple en Python (Singleton au niveau du module)

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

## Installation

**Le Singleton pattern n’est pas une bibliothèque ou un paquet.** C’est un design pattern architectural implémenté directement dans votre code source. Vous ne l’installez pas via npm, pip, Maven ou NuGet. Pour « adopter » le pattern, vous écrivez la classe nécessaire comme montré dans les exemples ci-dessus.

---

## Exemples d’utilisation

### Journalisation avec le Singleton par énumération (Java)

```java
Logger.INSTANCE.log("Application started");

// In another class:
Logger.INSTANCE.log("User logged in");
```

### Gestionnaire de configuration (C#)

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

**Utilisation :**

```csharp
string connStr = AppConfig.Instance.DbConnectionString;
```

---

## Critiques (Pourquoi certains l’appellent un anti‑pattern)

- **État global** – Le Singleton introduit un état global mutable, ce qui rend les tests unitaires dépendants de l’ordre et fragiles.
- **Couplage fort** – `getInstance()` force le code à dépendre de la classe concrète, violant le principe d’inversion des dépendances.
- **Dépendances cachées** – Une classe qui utilise un Singleton ne le déclare pas dans son constructeur ; la dépendance est enterrée à l’intérieur des méthodes, rendant l’API peu claire.
- **Violation du principe de responsabilité unique** – La classe doit gérer son propre cycle de vie (initialisation paresseuse, sécurité des threads) en plus de sa logique principale.

---

## Alternatives modernes

- **Injection de dépendances (DI)** – Un conteneur IoC (Spring, Guice, ASP.NET Core) gère les durées de vie des objets. Une classe peut être enregistrée avec une *portée singleton*, mais les consommateurs dépendent d’une interface, ce qui permet un mockage et un échange faciles.
- **Patron Monostate** – Une variante où la classe elle-même n’est pas un singleton, mais tous ses champs sont statiques. Plusieurs instances partagent le même état.
- **Classe utilitaire statique** – Fonctionne pour des auxiliaires sans état mais ne peut pas implémenter d’interfaces ni bénéficier du polymorphisme.

---

## Conclusion

Le Singleton pattern est un outil puissant lorsqu’il est utilisé délibérément. Les meilleures pratiques modernes favorisent l’injection de dépendances plutôt que les singletons directs car cela améliore la testabilité et la maintenabilité. Lorsque vous devez imposer une instance unique, préférez les implémentations **basées sur une énumération** (Java) ou `Lazy<T>` (C#) pour éviter les pièges de la sécurité des threads. Rappelez-vous que « l’accès global » est aussi un couplage global : utilisez les Singletons avec parcimonie et conscience.

---

*Références :*  
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object‑Oriented Software*. Addison‑Wesley.  
- Bloch, J. (2008). *Effective Java* (2nd ed., Item 3). Addison‑Wesley.  
- Martin, R. C. (2003). *Agile Software Development, Principles, Patterns, and Practices*. Prentice Hall.