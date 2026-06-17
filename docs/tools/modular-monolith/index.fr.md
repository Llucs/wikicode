---
title: Monolithe Modulaire
description: Un patron architectural qui organise le code en modules séparés avec des limites claires au sein d'une unité déployable unique, équilibrant la simplicité d'un monolithe avec la séparation logique des microservices.
created: 2026-06-17
tags:
  - architecture
  - design-patterns
  - domain-driven-design
  - monolith
  - microservices
  - spring-modulith
  - archunit
  - modularity
status: draft
---

# Aperçu (Quoi & Pourquoi)

Un **Monolithe Modulaire** est une architecture logicielle où l'ensemble de l'application est déployé comme une unité unique (un monolithe), mais la base de code est strictement organisée en modules indépendants, pilotés par le domaine, avec des limites bien définies. Contrairement à un monolithe « gros tas de boue » traditionnel, un monolithe modulaire applique la rigueur logique des microservices sans le coût d'infrastructure associé (latence réseau, découverte de services, traçage distribué, CI/CD complexe).

**Pourquoi utiliser un Monolithe Modulaire ?**

- **Simplicité Opérationnelle :** Déploiement unique, pipeline de construction unique, pas de transactions distribuées entre les modules.
- **Vitesse de Développement :** Les fonctionnalités sont implémentées rapidement dans une seule base de code. Le refactoring entre les limites des modules est initialement plus facile qu'entre des services distribués.
- **Modularité Forte :** Les modules sont alignés sur des Contextes Bornés (Domain-Driven Design). Les équipes peuvent posséder des modules spécifiques sans se marcher sur les pieds.
- **Chemin de Passage à l'Échelle :** Les modules bien définis peuvent être extraits en microservices indépendants plus tard si les besoins de mise à l'échelle ou d'isolation des pannes le nécessitent vraiment.
- **Performance :** La communication entre modules est gérée via des appels de méthode en processus, éliminant la surcharge réseau.

**Histoire & Influences :**

Le terme a gagné en importance à la fin des années 2010 en tant que réaction pratique aux frais généraux opérationnels des microservices. Il a formalisé les patrons du Domain-Driven Design (Eric Evans, 2003) et de la stratégie « MonolithFirst » (Martin Fowler, 2014). Des leaders comme Simon Brown (modèle C4), Kamil Grzybek et Oliver Drotbohm (Spring Modulith) ont fourni des conseils de mise en œuvre concrets, établissant le Monolithe Modulaire comme une architecture de première classe valide, et non simplement un tremplin vers les microservices. Des entreprises comme Shopify, GitHub et Basecamp ont construit des systèmes massifs en utilisant ce patron.

# Principes Fondamentaux

1. **Unité de Déploiement Unique :** L'ensemble de l'application est construit, testé et déployé comme un seul artefact.
2. **Modules Pilotés par le Domaine :** Les modules correspondent 1:1 aux sous-domaines métier (ex. : Commandes, Facturation, Expédition).
3. **Encapsulation Stricte :** Les modules exposent une API publique stricte. Les entités internes, les tables de base de données et les référentiels sont privés et interdits d'utilisation directe par d'autres modules.
4. **Dépendances Explicites :** Les dépendances entre modules forment un Graphe Orienté Acyclique (DAG). Ceci est appliqué par le code et les tests, et non par la simple documentation.
5. **Données Possédées :** Chaque module possède ses propres tables de base de données (ou schémas) et n'expose les données qu'à travers son API.

# Installation

Un Monolithe Modulaire est une convention architecturale, mais il est implémenté et appliqué à l'aide d'outils spécifiques. Les exemples ci-dessous utilisent l'écosystème Java/Spring Boot (Spring Modulith + ArchUnit), qui est le framework le plus mature pour ce patron. Des outils similaires existent pour .NET (NetArchTest).

## Java / Spring Boot (Spring Modulith + ArchUnit)

Ajoutez les dépendances suivantes à votre `pom.xml` ou `build.gradle`.

**Maven (pom.xml) :**

```xml
<dependency>
    <groupId>org.springframework.modulith</groupId>
    <artifactId>spring-modulith-starter-core</artifactId>
    <version>1.2.0</version>
</dependency>
<dependency>
    <groupId>org.springframework.modulith</groupId>
    <artifactId>spring-modulith-starter-test</artifactId>
    <version>1.2.0</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>com.tngtech.archunit</groupId>
    <artifactId>archunit-junit5</artifactId>
    <version>1.3.0</version>
    <scope>test</scope>
</dependency>
```

**Gradle (build.gradle) :**

```gradle
dependencies {
    implementation 'org.springframework.modulith:spring-modulith-starter-core:1.2.0'
    testImplementation 'org.springframework.modulith:spring-modulith-starter-test:1.2.0'
    testImplementation 'com.tngtech.archunit:archunit-junit5:1.3.0'
}
```

# Utilisation

## Structuration de la Base de Code

Organisez votre application en packages de modules strictement séparés sous une racine d'application unique. Un package `shared-kernel` contient les objets-valeurs de base et les abstractions fondamentales dont tous les modules peuvent dépendre.

```text
src/main/java/com/company/app/
├── shared-kernel/              # Shared Value Objects (Money, Address, OrderId)
├── orders/                     # Module A: Order Management
│   ├── domain/                 # Entities, Value Objects (private)
│   ├── application/            # Public API / Use Cases
│   ├── infrastructure/         # Repositories, DB Access (private)
│   └── package-info.java       # @ApplicationModule annotation
├── billing/                    # Module B: Billing
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── package-info.java
├── shipping/                   # Module C: Shipping
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── package-info.java
└── App.java                    # Main Application / Composition Root
```

## Définition d'un Module

Utilisez l'annotation `@ApplicationModule` sur le fichier `package-info.java` de la racine du module. Cela indique à Spring Modulith de traiter cette hiérarchie de packages comme un module.

```java
// orders/package-info.java
@org.springframework.modulith.ApplicationModule(
    displayName = "Order Management",
    allowedDependencies = { "shared-kernel" }
)
package com.company.app.orders;
```

## Communication entre Modules (Événements)

Pour maintenir un couplage lâche, les modules communiquent via des événements applicatifs plutôt que par des appels de service directs pour les workflows non critiques.

**Publication d'un événement :**
```java
// OrderService.java
@Service
public class OrderService {
    private final ApplicationEventPublisher events;

    @Transactional
    public void placeOrder(Order order) {
        // ... business logic ...
        events.publishEvent(new OrderPlacedEvent(order.getId(), order.getCustomerId()));
    }
}
```

**Consommation d'un événement :**
```java
// BillingEventListener.java
@Component
public class BillingEventListener {
    private final BillingService billingService;

    @TransactionalEventListener
    public void handle(OrderPlacedEvent event) {
        billingService.createInvoiceForOrder(event.orderId());
    }
}
```

# Fonctionnalités Clés avec Exemples de Commandes

## 1. Vérification Automatisée de l'Architecture

La valeur principale de l'outillage est de détecter les violations de limites au moment de la construction. Spring Modulith analyse toute la structure du module et détecte les accès illégaux (par exemple, l'accès à un dépôt privé depuis un autre module).

**Test :**
```java
// ApplicationModuleTest.java
@ApplicationModuleTest
class ApplicationModuleTest {
    @Test
    void verifiesModularStructure() {
        // The test fails on startup if a module accesses
        // internal classes of another module.
    }
}
```

**Commande :**
```bash
# The build fails early if the architecture is violated.
./mvnw test
```

**Exemple de sortie de violation :**
```bash
[ERROR] Module 'billing' depends on module 'ordering' through
[ERROR]   com.company.billing.service.InvoiceService -> com.company.ordering.repository.OrderRepository
[ERROR]   (I) Module 'billing' should not depend on Module 'ordering::infrastructure'
```

## 2. Tranches de Test d'Intégration de Module (`@ModuleTest`)

Exécutez des tests d'intégration contre un *seul* module en isolation. Les dépendances des autres modules sont automatiquement simulées ou remplacées par des bouchons.

**Test :**
```java
// BillingModuleTest.java
@ModuleTest
class BillingModuleTest {
    @Autowired
    BillingService billingService;

    @Test
    void shouldCreateInvoice() {
        var command = new CreateInvoiceCommand("order-123");
        var result = billingService.createInvoice(command);
        assertThat(result).isNotNull();
    }
}
```

**Commande :**
```bash
# Runs only the billing module tests with its dependencies isolated
./mvnw test -Dtest=BillingModuleTest
```

## 3. Graphe de Dépendances & Détection de Cycles (ArchUnit)

Appliquez le DAG (Graphe Orienté Acyclique) et empêchez les modules de dépendre des mauvaises couches ou d'introduire des cycles.

**Test :**
```java
// ArchitectureTest.java
@AnalyzeClasses(packages = "com.company.app")
class ArchitectureTest {

    @Test
    void billingModuleShouldNotDependOnShippingModule() {
        classes()
            .that().resideInAPackage("..billing..")
            .should().onlyAccessClassesThat()
            .resideInAnyPackage("..billing..", "..shared..", "java..")
            .check(importedClasses);
    }

    @Test
    void modulesShouldBeFreeOfCycles() {
        slices()
            .matching("..company.(*)..")
            .should().beFreeOfCycles();
    }

    @Test
    void domainShouldNotDependOnInfrastructure() {
        noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
            .resideInAPackage("..infrastructure..");
    }
}
```

**Commande :**
```bash
# Standard test command, runs arch unit tests alongside unit tests
./mvnw test
```

## 4. Intégration du Pattern Outbox

Pour la fiabilité transactionnelle entre les limites des modules, le framework prend en charge un pattern Outbox. Cela évite les incohérences de données si un gestionnaire d'événements échoue après la validation de la transaction en base de données.

**Configuration :**
```java
// application.yml
spring:
  modulith:
    events:
      outbox:
        enabled: true
```

**Commande (Vérification) :**
```bash
# Run a test that verifies the outbox table is correctly polled
# and events are published.
./mvnw test -Dtest=OrderLifecycleTest
```

## 5. Documentation et Visualisation à l'Exécution

Spring Modulith peut générer des diagrammes de composants de style C4 et de la documentation API pour votre structure de modules.

**Commande :**
```bash
# Generate documentation during the build
./mvnw package
```

**Résultat :**
Un répertoire `modulith-docs` est généré dans `target/`. Ajoutez l'actuator Spring Modulith pour servir ce contenu à l'exécution :

```xml
<dependency>
    <groupId>org.springframework.modulith</groupId>
    <artifactId>spring-modulith-actuator</artifactId>
</dependency>
```

Accédez à la documentation à l'adresse : `http://localhost:8080/modulith-docs`

# Quand Utiliser un Monolithe Modulaire

**Candidats idéaux :**
- **La plupart des applications d'entreprise** et des produits SaaS avec des équipes de 2 à 20 développeurs.
- **Les systèmes avec une logique métier complexe** mais des modèles de trafic monolithiques prévisibles.
- **Les startups** où la construction d'un système distribué dès le premier jour ajoute des risques et des coûts inutiles.
- **La transition d'un monolithe legacy.** Un démêlage progressif en modules clairs est plus sûr qu'un « figuier étrangleur » direct vers les microservices.

**Quand envisager l'extraction vers des microservices :**
- **Des besoins de mise à l'échelle indépendants.** Le module A a besoin de 100 instances, le module B de 2.
- **Un isolement strict des pannes.** Un crash dans le module de facturation ne doit pas faire tomber le serveur web.
- **Des besoins polyglottes.** Un module nécessite un framework d'exécution ou un moteur de base de données complètement différent.
- **Un alignement organisationnel.** La structure de l'équipe exige une propriété de microservice totalement indépendante (Loi de Conway).

# Résumé

Le Monolithe Modulaire est un patron architectural très efficace qui offre le juste équilibre entre la simplicité d'un monolithe et la modularité des microservices. Le principal défi est de maintenir la discipline architecturale dans le temps. Cela est géré grâce au support du framework (Spring Modulith), aux tests d'architecture automatisés (ArchUnit, NetArchTest) et à une culture d'équipe forte axée sur les limites du domaine. Il représente le juste milieu stratégique et est le point de départ par défaut recommandé pour les applications d'entreprise modernes.