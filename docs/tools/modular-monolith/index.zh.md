---
title: 模块化单体
description: 一种架构模式，将代码组织到具有清晰边界的独立模块中，并部署为单个单元，在单体的简单性与微服务的逻辑分离之间取得平衡。
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

# 概述（是什么 & 为什么）

**模块化单体**是一种软件架构，整个应用程序以单个单元（单体）部署，但代码库被严格组织成独立的、领域驱动的模块，并具有明确的边界。与传统的“大泥球”单体不同，模块化单体强制实施微服务的逻辑严谨性，而无需相关的基础设施成本（网络延迟、服务发现、分布式追踪、复杂CI/CD）。

**为什么使用模块化单体？**

- **运维简单性：** 单次部署、单个构建管道，模块间无分布式事务。
- **开发速度：** 在单一代码库中快速实现功能。与分布式服务相比，跨模块的重构初期更容易。
- **强模块化：** 模块与限界上下文（领域驱动设计）对齐。团队可以拥有特定模块而互不干扰。
- **可扩展路径：** 定义良好的模块可以在以后根据需要进行扩展或提取为独立的微服务，如果确实需要扩展或隔离故障的话。
- **性能：** 模块间通信通过进程内方法调用处理，消除了网络开销。

**历史与影响：**

该术语在2010年代末作为对微服务运维开销的实用反应而变得突出。它形式化了领域驱动设计（Eric Evans, 2003）和“Monolith首先”策略（Martin Fowler, 2014）的模式。Simon Brown（C4模型）、Kamil Grzybek 和 Oliver Drotbohm（Spring Modulith）等领导者提供了具体的实施指导，将模块化单体确立为一流的有效架构，而不仅仅是微服务的垫脚石。Shopify、GitHub 和 Basecamp 等公司已经使用这种模式构建了大型系统。

# 核心原则

1. **单一部署单元：** 整个应用程序作为一个工件构建、测试和部署。
2. **领域驱动模块：** 模块与业务子领域一一对应（例如，订单、计费、发货）。
3. **严格封装：** 模块公开严格的公共API。内部实体、数据库表和存储库是私有的，禁止其他模块直接使用。
4. **显式依赖：** 模块之间的依赖关系形成有向无环图（DAG）。这通过代码和测试强制实施，而不仅仅是文档。
5. **自有数据：** 每个模块拥有自己的数据库表（或模式），并且仅通过其API公开数据。

# 安装

模块化单体是一种架构约定，但通过特定的工具来实现和强制实施。下面的示例使用了Java/Spring Boot生态系统（Spring Modulith + ArchUnit），这是该模式最成熟的框架。类似工具也存在于.NET（NetArchTest）中。

## Java / Spring Boot（Spring Modulith + ArchUnit）

将以下依赖添加到 `pom.xml` 或 `build.gradle`。

**Maven（pom.xml）：**

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

**Gradle（build.gradle）：**

```gradle
dependencies {
    implementation 'org.springframework.modulith:spring-modulith-starter-core:1.2.0'
    testImplementation 'org.springframework.modulith:spring-modulith-starter-test:1.2.0'
    testImplementation 'com.tngtech.archunit:archunit-junit5:1.3.0'
}
```

# 使用

## 组织代码库

在单个应用程序根目录下，将应用程序组织成严格分离的模块包。`shared-kernel` 包包含所有模块可以依赖的核心值对象和基本抽象。

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

## 定义模块

在模块根目录的 `package-info.java` 文件上使用 `@ApplicationModule` 注解。这告诉 Spring Modulith 将此包层次结构视为一个模块。

```java
// orders/package-info.java
@org.springframework.modulith.ApplicationModule(
    displayName = "Order Management",
    allowedDependencies = { "shared-kernel" }
)
package com.company.app.orders;
```

## 跨模块通信（事件）

为了保持松散耦合，模块通过应用程序事件而不是直接服务调用来进行非关键工作流的通信。

**发布事件：**
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

**消费事件：**
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

# 核心特性与命令示例

## 1. 自动架构验证

工具的主要价值是在构建时捕获边界违规。Spring Modulith 扫描整个模块结构并检测非法访问（例如，从另一个模块访问私有存储库）。

**测试：**
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

**命令：**
```bash
# The build fails early if the architecture is violated.
./mvnw test
```

**违规输出示例：**
```bash
[ERROR] Module 'billing' depends on module 'ordering' through
[ERROR]   com.company.billing.service.InvoiceService -> com.company.ordering.repository.OrderRepository
[ERROR]   (I) Module 'billing' should not depend on Module 'ordering::infrastructure'
```

## 2. 模块集成测试切片（`@ModuleTest`）

针对*单个*模块在隔离环境中运行集成测试。其他模块的依赖项会自动模拟或存根。

**测试：**
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

**命令：**
```bash
# Runs only the billing module tests with its dependencies isolated
./mvnw test -Dtest=BillingModuleTest
```

## 3. 依赖图与循环检测（ArchUnit）

强制实施有向无环图（DAG），防止模块依赖错误的层次或引入循环。

**测试：**
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

**命令：**
```bash
# Standard test command, runs arch unit tests alongside unit tests
./mvnw test
```

## 4. Outbox模式集成

为了跨模块边界的事务可靠性，框架支持 Outbox 模式。这可以防止在数据库事务提交后事件处理程序失败时出现数据不一致。

**配置：**
```java
// application.yml
spring:
  modulith:
    events:
      outbox:
        enabled: true
```

**命令（验证）：**
```bash
# Run a test that verifies the outbox table is correctly polled
# and events are published.
./mvnw test -Dtest=OrderLifecycleTest
```

## 5. 运行时文档与可视化

Spring Modulith 可以为您的模块结构生成 C4 风格的组件图和 API 文档。

**命令：**
```bash
# Generate documentation during the build
./mvnw package
```

**结果：**
在 `target/` 中生成 `modulith-docs` 目录。添加 Spring Modulith Actuator 以在运行时提供该目录：

```xml
<dependency>
    <groupId>org.springframework.modulith</groupId>
    <artifactId>spring-modulith-actuator</artifactId>
</dependency>
```

访问文档：`http://localhost:8080/modulith-docs`

# 何时使用模块化单体

**理想适用场景：**
- **大多数企业应用程序**以及由 2-20 名开发者组成的团队使用的 SaaS 产品。
- **具有复杂业务逻辑**但具有可预测的单体流量模式的系统。
- **初创公司**，从一开始就构建分布式系统会增加不必要的风险和成本。
- **迁移遗留单体。** 逐步理清到清晰模块比直接使用“绞杀者模式”迁移到微服务更安全。

**何时考虑提取为微服务：**
- **独立的扩展需求。** 模块 A 需要 100 个实例，模块 B 需要 2 个。
- **严格的故障隔离。** 计费模块的崩溃不能导致 Web 服务器宕机。
- **多语言需求。** 模块需要完全不同的运行时框架或数据库引擎。
- **组织匹配。** 团队结构需要完全独立的微服务所有权（康威定律）。

# 总结

模块化单体是一种非常有效的架构模式，它在单体的简单性和微服务的模块化之间提供了最佳平衡点。主要挑战是长期保持架构纪律。这通过框架支持（Spring Modulith）、自动架构测试（ArchUnit, NetArchTest）以及专注于领域边界的强大团队文化来管理。它代表了战略性的中间立场，是现代企业应用程序推荐的默认起点。