---
title: Monólito Modular
description: Um padrão arquitetural que organiza o código em módulos separados com limites claros dentro de uma única unidade implantável, equilibrando a simplicidade de um monólito com a separação lógica de microsserviços.
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

# Overview (What & Why)

A **Modular Monolith** is a software architecture where the entire application is deployed as a single unit (a monolith), but the codebase is strictly organized into independent, domain-driven modules with well-defined boundaries. Unlike a traditional "big ball of mud" monolith, a modular monolith enforces the logical rigor of microservices without the associated infrastructure cost (network latency, service discovery, distributed tracing, complex CI/CD).

**Why use a Modular Monolith?**

- **Operational Simplicity:** Single deployment, single build pipeline, no distributed transactions across modules.
- **Development Speed:** Features are implemented quickly within a single codebase. Refactoring across module boundaries is initially easier than across distributed services.
- **Strong Modularity:** Modules are aligned to Bounded Contexts (Domain-Driven Design). Teams can own specific modules without stepping on each other's toes.
- **Scalability Path:** Well-defined modules can be extracted into independent microservices later if scaling or fault isolation needs truly demand it.
- **Performance:** Inter-module communication is handled via in-process method calls, eliminating network overhead.

**History & Influences:**

The term gained prominence in the late 2010s as a practical reaction to the operational overhead of microservices. It formalized patterns from Domain-Driven Design (Eric Evans, 2003) and the "MonolithFirst" strategy (Martin Fowler, 2014). Leaders like Simon Brown (C4 model), Kamil Grzybek, and Oliver Drotbohm (Spring Modulith) provided concrete implementation guidance, establishing the Modular Monolith as a valid first-class architecture, not merely a stepping stone to microservices. Companies like Shopify, GitHub, and Basecamp have built massive systems using this pattern.

# Core Principles

1. **Single Deployment Unit:** The entire application is built, tested, and deployed as one artifact.
2. **Domain-Driven Modules:** Modules map 1:1 to business subdomains (e.g., Orders, Billing, Shipping).
3. **Strict Encapsulation:** Modules expose a strict public API. Internal entities, database tables, and repositories are private and forbidden from direct use by other modules.
4. **Explicit Dependencies:** Dependencies between modules form a Directed Acyclic Graph (DAG). This is enforced by code and tests, not just documentation.
5. **Owned Data:** Each module owns its database tables (or schemas) and only exposes data through its API.

# Installation

A Modular Monolith is an architectural convention, but it is implemented and enforced using specific tooling. The examples below use the Java/Spring Boot ecosystem (Spring Modulith + ArchUnit), which is the most mature framework for this pattern. Similar tooling exists for .NET (NetArchTest).

## Java / Spring Boot (Spring Modulith + ArchUnit)

Add the following dependencies to your `pom.xml` or `build.gradle`.

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

# Usage

## Structuring the Codebase

Organize your application into strictly separated module packages under a single application root. A `shared-kernel` package contains core value objects and base abstractions that all modules can depend on.

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

## Defining a Module

Use the `@ApplicationModule` annotation on the `package-info.java` file of the module root. This tells Spring Modulith to treat this package hierarchy as a module.

```java
// orders/package-info.java
@org.springframework.modulith.ApplicationModule(
    displayName = "Order Management",
    allowedDependencies = { "shared-kernel" }
)
package com.company.app.orders;
```

## Cross-Module Communication (Events)

To maintain loose coupling, modules communicate via application events rather than direct service calls for non-critical workflows.

**Publishing an Event:**
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

**Consuming an Event:**
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

# Key Features with Command Examples

## 1. Automated Architecture Verification

The primary value of the tooling is catching boundary violations at build time. Spring Modulith scans the entire module structure and detects illegal access (e.g., accessing a private repository from another module).

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

**Command:**
```bash
# The build fails early if the architecture is violated.
./mvnw test
```

**Example Violation Output:**
```bash
[ERROR] Module 'billing' depends on module 'ordering' through
[ERROR]   com.company.billing.service.InvoiceService -> com.company.ordering.repository.OrderRepository
[ERROR]   (I) Module 'billing' should not depend on Module 'ordering::infrastructure'
```

## 2. Module Integration Test Slices (`@ModuleTest`)

Run integration tests against a *single* module in isolation. Dependencies from other modules are automatically mocked or stubbed.

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

**Command:**
```bash
# Runs only the billing module tests with its dependencies isolated
./mvnw test -Dtest=BillingModuleTest
```

## 3. Dependency Graph & Cycle Detection (ArchUnit)

Enforce the DAG (Directed Acyclic Graph) and prevent modules from depending on the wrong layers or introducing cycles.

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

**Command:**
```bash
# Standard test command, runs arch unit tests alongside unit tests
./mvnw test
```

## 4. Outbox Pattern Integration

For transactional reliability across module boundaries, the framework supports an Outbox pattern. This prevents data inconsistency if an event handler fails after the database transaction commits.

**Configuration:**
```java
// application.yml
spring:
  modulith:
    events:
      outbox:
        enabled: true
```

**Command (Verification):**
```bash
# Run a test that verifies the outbox table is correctly polled
# and events are published.
./mvnw test -Dtest=OrderLifecycleTest
```

## 5. Runtime Documentation & Visualization

Spring Modulith can generate C4-style component diagrams and API documentation for your module structure.

**Command:**
```bash
# Generate documentation during the build
./mvnw package
```

**Result:**
A `modulith-docs` directory is generated in `target/`. Add the Spring Modulith Actuator to serve this at runtime:

```xml
<dependency>
    <groupId>org.springframework.modulith</groupId>
    <artifactId>spring-modulith-actuator</artifactId>
</dependency>
```

Access the docs at: `http://localhost:8080/modulith-docs`

# When to Use a Modular Monolith

**Ideal candidates:**
- **Most enterprise applications** and SaaS products with teams of 2–20 developers.
- **Systems with complex business logic** but predictable, monolithic traffic patterns.
- **Startups** where building a distributed system from day one adds unnecessary risk and cost.
- **Transitioning a legacy monolith.** A step-by-step untangling into clear modules is safer than a direct "strangler fig" into microservices.

**When to consider extracting to microservices:**
- **Independent scaling needs.** Module A needs 100 instances, Module B needs 2.
- **Strict fault isolation.** A crash in the billing module must not bring down the web server.
- **Polyglot requirements.** A module requires a completely different runtime framework or database engine.
- **Organizational alignment.** The team structure demands fully independent microservice ownership (Conway's Law).

# Summary

The Modular Monolith is a highly effective architectural pattern that provides the sweet spot between the simplicity of a monolith and the modularity of microservices. The primary challenge is maintaining architectural discipline over time. This is managed through framework support (Spring Modulith), automated architecture tests (ArchUnit, NetArchTest), and a strong team culture focused on domain boundaries. It represents the strategic middle ground and is the recommended default starting point for modern enterprise applications.