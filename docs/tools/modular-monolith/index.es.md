---
title: Monolito Modular
description: Un patrón arquitectónico que organiza el código en módulos separados con límites claros dentro de una única unidad desplegable, equilibrando la simplicidad de un monolito con la separación lógica de los microservicios.
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

# Visión General (Qué y Por Qué)

Un **Monolito Modular** es una arquitectura de software donde toda la aplicación se despliega como una unidad única (un monolito), pero el código está estrictamente organizado en módulos independientes y dirigidos por el dominio, con límites bien definidos. A diferencia de un monolito tradicional "big ball of mud", un monolito modular impone el rigor lógico de los microservicios sin el costo de infraestructura asociado (latencia de red, descubrimiento de servicios, trazabilidad distribuida, CI/CD complejo).

**¿Por qué usar un Monolito Modular?**

- **Simplicidad Operativa:** Un solo despliegue, un solo pipeline de construcción, sin transacciones distribuidas entre módulos.
- **Velocidad de Desarrollo:** Las funcionalidades se implementan rápidamente dentro de un único código base. La refactorización a través de los límites de los módulos es inicialmente más fácil que a través de servicios distribuidos.
- **Modularidad Fuerte:** Los módulos están alineados con los Contextos Delimitados (Domain-Driven Design). Los equipos pueden ser propietarios de módulos específicos sin pisarse los pies.
- **Camino de Escalabilidad:** Los módulos bien definidos pueden extraerse como microservicios independientes más adelante si las necesidades de escalado o aislamiento de fallos realmente lo requieren.
- **Rendimiento:** La comunicación entre módulos se maneja mediante llamadas a métodos dentro del mismo proceso, eliminando la sobrecarga de red.

**Historia e Influencias:**

El término ganó prominencia a finales de la década de 2010 como una reacción práctica a la sobrecarga operativa de los microservicios. Formalizó patrones del Domain-Driven Design (Eric Evans, 2003) y la estrategia "MonolithFirst" (Martin Fowler, 2014). Líderes como Simon Brown (modelo C4), Kamil Grzybek y Oliver Drotbohm (Spring Modulith) proporcionaron una guía de implementación concreta, estableciendo el Monolito Modular como una arquitectura de primera clase válida, no meramente un trampolín hacia los microservicios. Empresas como Shopify, GitHub y Basecamp han construido sistemas masivos utilizando este patrón.

# Principios Fundamentales

1. **Unidad de Despliegue Única:** Toda la aplicación se construye, prueba y despliega como un solo artefacto.
2. **Módulos Dirigidos por el Dominio:** Los módulos se corresponden 1:1 con los subdominios del negocio (por ejemplo, Pedidos, Facturación, Envío).
3. **Encapsulamiento Estricto:** Los módulos exponen una API pública estricta. Las entidades internas, tablas de base de datos y repositorios son privados y está prohibido su uso directo por otros módulos.
4. **Dependencias Explícitas:** Las dependencias entre módulos forman un Grafo Acíclico Dirigido (DAG). Esto se impone mediante código y pruebas, no solo documentación.
5. **Datos Propios:** Cada módulo es propietario de sus tablas de base de datos (o esquemas) y solo expone datos a través de su API.

# Instalación

Un Monolito Modular es una convención arquitectónica, pero se implementa y refuerza utilizando herramientas específicas. Los ejemplos a continuación utilizan el ecosistema Java/Spring Boot (Spring Modulith + ArchUnit), que es el marco más maduro para este patrón. Existen herramientas similares para .NET (NetArchTest).

## Java / Spring Boot (Spring Modulith + ArchUnit)

Añade las siguientes dependencias a tu `pom.xml` o `build.gradle`.

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

# Uso

## Estructuración del Código Base

Organiza tu aplicación en paquetes de módulos estrictamente separados bajo una raíz de aplicación única. Un paquete `shared-kernel` contiene objetos valor centrales y abstracciones base de los que todos los módulos pueden depender.

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

## Definición de un Módulo

Usa la anotación `@ApplicationModule` en el archivo `package-info.java` de la raíz del módulo. Esto le indica a Spring Modulith que trate esta jerarquía de paquetes como un módulo.

```java
// orders/package-info.java
@org.springframework.modulith.ApplicationModule(
    displayName = "Order Management",
    allowedDependencies = { "shared-kernel" }
)
package com.company.app.orders;
```

## Comunicación entre Módulos (Eventos)

Para mantener un acoplamiento flexible, los módulos se comunican a través de eventos de aplicación en lugar de llamadas directas a servicios para flujos de trabajo no críticos.

**Publicación de un Evento:**
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

**Consumo de un Evento:**
```java
// BillingEventListener.java
@Component
public class BillingEventListener {
    private final BillingService billingService;

    @TransactionalEventListener
    public void handle(OrderPlacedEvent event) {
        billingService.createInvoiceForEvent(event.orderId());
    }
}
```

# Características Clave con Ejemplos de Comandos

## 1. Verificación Automatizada de Arquitectura

El valor principal de las herramientas es detectar violaciones de límites en tiempo de compilación. Spring Modulith escanea toda la estructura del módulo y detecta accesos ilegales (por ejemplo, acceder a un repositorio privado desde otro módulo).

**Prueba:**
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

**Comando:**
```bash
# The build fails early if the architecture is violated.
./mvnw test
```

**Ejemplo de Salida de Violación:**
```bash
[ERROR] Module 'billing' depends on module 'ordering' through
[ERROR]   com.company.billing.service.InvoiceService -> com.company.ordering.repository.OrderRepository
[ERROR]   (I) Module 'billing' should not depend on Module 'ordering::infrastructure'
```

## 2. Test Slices de Integración de Módulos (`@ModuleTest`)

Ejecuta pruebas de integración contra un *solo* módulo de forma aislada. Las dependencias de otros módulos se simulan o se sustituyen automáticamente.

**Prueba:**
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

**Comando:**
```bash
# Runs only the billing module tests with its dependencies isolated
./mvnw test -Dtest=BillingModuleTest
```

## 3. Grafo de Dependencias y Detección de Ciclos (ArchUnit)

Impone el DAG (Grafo Acíclico Dirigido) y evita que los módulos dependan de las capas incorrectas o introduzcan ciclos.

**Prueba:**
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

**Comando:**
```bash
# Standard test command, runs arch unit tests alongside unit tests
./mvnw test
```

## 4. Integración del Patrón Outbox

Para la fiabilidad transaccional a través de los límites de los módulos, el framework soporta un patrón Outbox. Esto previene la inconsistencia de datos si un manejador de eventos falla después de que se confirme la transacción de la base de datos.

**Configuración:**
```yaml
# application.yml
spring:
  modulith:
    events:
      outbox:
        enabled: true
```

**Comando (Verificación):**
```bash
# Run a test that verifies the outbox table is correctly polled
# and events are published.
./mvnw test -Dtest=OrderLifecycleTest
```

## 5. Documentación y Visualización en Tiempo de Ejecución

Spring Modulith puede generar diagramas de componentes estilo C4 y documentación de la API para tu estructura de módulos.

**Comando:**
```bash
# Generate documentation during the build
./mvnw package
```

**Resultado:**
Se genera un directorio `modulith-docs` en `target/`. Añade el Actuador de Spring Modulith para servir esto en tiempo de ejecución:

```xml
<dependency>
    <groupId>org.springframework.modulith</groupId>
    <artifactId>spring-modulith-actuator</artifactId>
</dependency>
```

Accede a la documentación en: `http://localhost:8080/modulith-docs`

# Cuándo Usar un Monolito Modular

**Candidatos ideales:**
- **La mayoría de las aplicaciones empresariales** y productos SaaS con equipos de 2 a 20 desarrolladores.
- **Sistemas con lógica de negocio compleja** pero patrones de tráfico monolíticos predecibles.
- **Startups** donde construir un sistema distribuido desde el primer día añade riesgo y coste innecesarios.
- **Transición de un monolito heredado.** Un desenredo paso a paso en módulos claros es más seguro que una "higuera estranguladora" directa hacia microservicios.

**Cuándo considerar la extracción a microservicios:**
- **Necesidades de escalado independiente.** El Módulo A necesita 100 instancias, el Módulo B necesita 2.
- **Aislamiento estricto de fallos.** Un fallo en el módulo de facturación no debe derribar el servidor web.
- **Requisitos políglotas.** Un módulo requiere un marco de ejecución o motor de base de datos completamente diferente.
- **Alineación organizativa.** La estructura del equipo exige una propiedad de microservicios completamente independiente (Ley de Conway).

# Resumen

El Monolito Modular es un patrón arquitectónico altamente efectivo que proporciona el punto óptimo entre la simplicidad de un monolito y la modularidad de los microservicios. El desafío principal es mantener la disciplina arquitectónica a lo largo del tiempo. Esto se gestiona mediante el soporte del framework (Spring Modulith), pruebas automatizadas de arquitectura (ArchUnit, NetArchTest) y una fuerte cultura de equipo centrada en los límites del dominio. Representa el punto medio estratégico y es el punto de partida predeterminado recomendado para aplicaciones empresariales modernas.