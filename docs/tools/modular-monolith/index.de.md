---
title: Modularer Monolith
description: Ein Architekturmuster, das Code in separate Module mit klaren Grenzen innerhalb einer einzelnen bereitstellbaren Einheit organisiert und die Einfachheit eines Monolithen mit der logischen Trennung von Microservices vereint.
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

# Überblick (Was & Warum)

Ein **Modularer Monolith** ist eine Softwarearchitektur, bei der die gesamte Anwendung als einzelne Einheit (ein Monolith) bereitgestellt wird, die Codebasis jedoch streng in unabhängige, domänengesteuerte Module mit klar definierten Grenzen organisiert ist. Im Gegensatz zu einem traditionellen „Big Ball of Mud“-Monolithen erzwingt ein modularer Monolith die logische Strenge von Microservices ohne die damit verbundenen Infrastrukturkosten (Netzwerklatenz, Service Discovery, verteiltes Tracing, komplexe CI/CD).

**Warum einen modularen Monolithen verwenden?**

- **Betriebliche Einfachheit:** Einzelne Bereitstellung, einzelne Build-Pipeline, keine verteilten Transaktionen über Module hinweg.
- **Entwicklungsgeschwindigkeit:** Funktionen werden schnell innerhalb einer einzigen Codebasis implementiert. Refaktorisierung über Modulgrenzen hinweg ist anfangs einfacher als über verteilte Dienste.
- **Starke Modularität:** Module sind an Bounded Contexts (Domain-Driven Design) ausgerichtet. Teams können bestimmte Module besitzen, ohne sich gegenseitig auf die Füße zu treten.
- **Skalierbarkeitspfad:** Gut definierte Module können später in unabhängige Microservices extrahiert werden, wenn Skalierungs- oder Fehlerisolierungsanforderungen dies wirklich erfordern.
- **Leistung:** Die Kommunikation zwischen Modulen erfolgt über prozessinterne Methodenaufrufe, wodurch Netzwerk-Overhead vermieden wird.

**Geschichte & Einflüsse:**

Der Begriff gewann in den späten 2010er Jahren als praktische Reaktion auf den operationellen Overhead von Microservices an Bedeutung. Er formalisierte Muster aus Domain-Driven Design (Eric Evans, 2003) und der „MonolithFirst“-Strategie (Martin Fowler, 2014). Wegbereiter wie Simon Brown (C4-Modell), Kamil Grzybek und Oliver Drotbohm (Spring Modulith) lieferten konkrete Implementierungsrichtlinien und etablierten den Modularen Monolithen als eine erstklassige Architektur, nicht nur als Zwischenschritt zu Microservices. Unternehmen wie Shopify, GitHub und Basecamp haben mit diesem Muster massive Systeme gebaut.

# Kernprinzipien

1. **Einzelne Bereitstellungseinheit:** Die gesamte Anwendung wird als ein Artefakt gebaut, getestet und bereitgestellt.
2. **Domänengesteuerte Module:** Module bilden 1:1 Geschäfts-Subdomänen ab (z.B. Bestellungen, Abrechnung, Versand).
3. **Strenge Kapselung:** Module legen eine strikte öffentliche API offen. Interne Entitäten, Datenbanktabellen und Repositories sind privat und dürfen von anderen Modulen nicht direkt verwendet werden.
4. **Explizite Abhängigkeiten:** Abhängigkeiten zwischen Modulen bilden einen gerichteten azyklischen Graphen (Directed Acyclic Graph, DAG). Dies wird durch Code und Tests erzwungen, nicht nur durch Dokumentation.
5. **Eigene Daten:** Jedes Modul besitzt seine eigenen Datenbanktabellen (oder Schemas) und gibt Daten nur über seine API frei.

# Installation

Ein Modularer Monolith ist eine architektonische Konvention, wird jedoch mit spezifischen Werkzeugen implementiert und erzwungen. Die folgenden Beispiele verwenden das Java/Spring-Boot-Ökosystem (Spring Modulith + ArchUnit), das das ausgereifteste Framework für dieses Muster darstellt. Ähnliche Werkzeuge existieren für .NET (NetArchTest).

## Java / Spring Boot (Spring Modulith + ArchUnit)

Fügen Sie die folgenden Abhängigkeiten zu Ihrer `pom.xml` oder `build.gradle` hinzu.

**Maven (pom.xml):**

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

**Gradle (build.gradle):**

```gradle
dependencies {
    implementation 'org.springframework.modulith:spring-modulith-starter-core:1.2.0'
    testImplementation 'org.springframework.modulith:spring-modulith-starter-test:1.2.0'
    testImplementation 'com.tngtech.archunit:archunit-junit5:1.3.0'
}
```

# Verwendung

## Strukturierung der Codebasis

Organisieren Sie Ihre Anwendung in streng getrennten Modulpaketen unter einer einzigen Anwendungswurzel. Ein `shared-kernel`-Paket enthält Kern-Value-Objekte und Basisabstraktionen, von denen alle Module abhängen können.

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

## Definieren eines Moduls

Verwenden Sie die `@ApplicationModule`-Annotation in der `package-info.java`-Datei des Modulstamms. Dies teilt Spring Modulith mit, diese Pakethierarchie als ein Modul zu behandeln.

```java
// orders/package-info.java
@org.springframework.modulith.ApplicationModule(
    displayName = "Order Management",
    allowedDependencies = { "shared-kernel" }
)
package com.company.app.orders;
```

## Kommunikation zwischen Modulen (Events)

Um lose Kopplung zu wahren, kommunizieren Module über Anwendungsereignisse anstatt über direkte Serviceaufrufe für nicht-kritische Arbeitsabläufe.

**Veröffentlichen eines Events:**
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

**Konsumieren eines Events:**
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

# Hauptfunktionen mit Befehlsbeispielen

## 1. Automatisierte Architekturverifikation

Der primäre Wert des Werkzeugs besteht darin, Grenzverletzungen zur Build-Zeit zu erkennen. Spring Modulith scannt die gesamte Modulstruktur und erkennt illegale Zugriffe (z.B. Zugriff auf ein privates Repository aus einem anderen Modul).

**Test:**
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

**Befehl:**
```bash
# The build fails early if the architecture is violated.
./mvnw test
```

**Beispiel für Verletzungsausgabe:**
```bash
[ERROR] Module 'billing' depends on module 'ordering' through
[ERROR]   com.company.billing.service.InvoiceService -> com.company.ordering.repository.OrderRepository
[ERROR]   (I) Module 'billing' should not depend on Module 'ordering::infrastructure'
```

## 2. Modul-Integrationstest-Slices (`@ModuleTest`)

Führen Sie Integrationstests gegen ein *einzelnes* Modul isoliert durch. Abhängigkeiten von anderen Modulen werden automatisch gemockt oder gestubt.

**Test:**
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

**Befehl:**
```bash
# Runs only the billing module tests with its dependencies isolated
./mvnw test -Dtest=BillingModuleTest
```

## 3. Abhängigkeitsgraph & Zyklenerkennung (ArchUnit)

Erzwingen Sie den DAG (Directed Acyclic Graph) und verhindern Sie, dass Module von den falschen Schichten abhängen oder Zyklen einführen.

**Test:**
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

**Befehl:**
```bash
# Standard test command, runs arch unit tests alongside unit tests
./mvnw test
```

## 4. Outbox-Pattern-Integration

Für transaktionale Zuverlässigkeit über Modulgrenzen hinweg unterstützt das Framework ein Outbox-Muster. Dies verhindert Dateninkonsistenzen, wenn ein Event-Handler fehlschlägt, nachdem die Datenbanktransaktion abgeschlossen wurde.

**Konfiguration:**
```java
// application.yml
spring:
  modulith:
    events:
      outbox:
        enabled: true
```

**Befehl (Verifikation):**
```bash
# Run a test that verifies the outbox table is correctly polled
# and events are published.
./mvnw test -Dtest=OrderLifecycleTest
```

## 5. Laufzeitdokumentation & Visualisierung

Spring Modulith kann C4-ähnliche Komponentendiagramme und API-Dokumentation für Ihre Modulstruktur generieren.

**Befehl:**
```bash
# Generate documentation during the build
./mvnw package
```

**Ergebnis:**
Ein Verzeichnis `modulith-docs` wird in `target/` generiert. Fügen Sie den Spring Modulith Actuator hinzu, um dies zur Laufzeit bereitzustellen:

```xml
<dependency>
    <groupId>org.springframework.modulith</groupId>
    <artifactId>spring-modulith-actuator</artifactId>
</dependency>
```

Greifen Sie auf die Dokumentation zu unter: `http://localhost:8080/modulith-docs`

# Wann man einen modularen Monolithen verwendet

**Ideale Kandidaten:**
- **Die meisten Unternehmensanwendungen** und SaaS-Produkte mit Teams von 2–20 Entwicklern.
- **Systeme mit komplexer Geschäftslogik**, aber vorhersehbaren, monolithischen Verkehrsmustern.
- **Startups**, bei denen der Aufbau eines verteilten Systems von Anfang an unnötiges Risiko und Kosten verursacht.
- **Migration eines Legacy-Monolithen.** Eine schrittweise Entwirrung in klare Module ist sicherer als eine direkte „Strangler Fig“-Migration zu Microservices.

**Wann eine Extraktion zu Microservices in Betracht gezogen werden sollte:**
- **Unabhängige Skalierungsanforderungen.** Modul A benötigt 100 Instanzen, Modul B benötigt 2.
- **Strenge Fehlerisolierung.** Ein Absturz im Abrechnungsmodul darf den Webserver nicht lahmlegen.
- **Polyglotte Anforderungen.** Ein Modul erfordert ein völlig anderes Laufzeit-Framework oder eine andere Datenbank-Engine.
- **Organisatorische Ausrichtung.** Die Teamstruktur erfordert vollständig unabhängige Microservice-Besitzverhältnisse (Conway's Law).

# Zusammenfassung

Der Modulare Monolith ist ein äußerst effektives Architekturmuster, das den Sweet Spot zwischen der Einfachheit eines Monolithen und der Modularität von Microservices bietet. Die größte Herausforderung besteht darin, die architektonische Disziplin im Laufe der Zeit aufrechtzuerhalten. Dies wird durch Framework-Unterstützung (Spring Modulith), automatisierte Architekturtests (ArchUnit, NetArchTest) und eine starke Teamkultur, die sich auf Domänengrenzen konzentriert, erreicht. Es stellt die strategische Mitte dar und ist der empfohlene Standardausgangspunkt für moderne Unternehmensanwendungen.