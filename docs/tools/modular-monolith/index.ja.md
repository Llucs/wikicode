---
title: Modular Monolith
description: コードを明確な境界を持つ独立したモジュールに整理し、単一のデプロイユニット内でモノリスのシンプルさとマイクロサービスの論理的分離のバランスをとるアーキテクチャパターン。
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

# 概要（What & Why）

**Modular Monolith** は、アプリケーション全体を単一のユニット（モノリス）としてデプロイするソフトウェアアーキテクチャですが、コードベースを独立したドメイン駆動のモジュールに厳密に整理し、明確に定義された境界を持ちます。従来の「big ball of mud」モノリスとは異なり、モジュラーモノリスは、関連するインフラストラクチャコスト（ネットワークレイテンシ、サービスディスカバリ、分散トレーシング、複雑なCI/CD）を伴わずに、マイクロサービスの論理的な厳密さを強制します。

**なぜモジュラーモノリスを使うのか？**

- **運用のシンプルさ:** 単一デプロイ、単一ビルドパイプライン、モジュール間の分散トランザクションなし。
- **開発速度:** 単一コードベース内で機能を迅速に実装できます。モジュール境界をまたぐリファクタリングは、最初は分散サービス間よりも容易です。
- **強力なモジュール性:** モジュールは境界付けられたコンテキスト（Bounded Contexts, ドメイン駆動設計）に合わせられます。チームは互いに干渉することなく特定のモジュールを所有できます。
- **スケーラビリティへの道筋:** 明確に定義されたモジュールは、スケーリングや障害分離の必要性が本当に要求された場合、後で独立したマイクロサービスに抽出できます。
- **パフォーマンス:** モジュール間通信はインプロセスのメソッド呼び出しで処理されるため、ネットワークオーバーヘッドがありません。

**歴史と影響:**

この用語は2010年代後半に、マイクロサービスの運用負荷に対する実用的な反応として注目されるようになりました。これはドメイン駆動設計（Eric Evans, 2003）と「MonolithFirst」戦略（Martin Fowler, 2014）のパターンを形式化したものです。Simon Brown（C4モデル）、Kamil Grzybek、Oliver Drotbohm（Spring Modulith）などのリーダーが具体的な実装ガイダンスを提供し、Modular Monolith を単なるマイクロサービスへの足掛かりではなく、有効な第一級のアーキテクチャとして確立しました。Shopify、GitHub、Basecampなどの企業はこのパターンを使用して大規模なシステムを構築しています。

# コア原則

1. **単一デプロイユニット:** アプリケーション全体が1つのアーティファクトとしてビルド、テスト、デプロイされます。
2. **ドメイン駆動モジュール:** モジュールはビジネスサブドメイン（例：注文、請求、配送）に1:1でマッピングされます。
3. **厳格なカプセル化:** モジュールは厳格なパブリックAPIを公開します。内部エンティティ、データベーステーブル、リポジトリはプライベートであり、他のモジュールからの直接使用は禁止されています。
4. **明示的な依存関係:** モジュール間の依存関係は有向非巡回グラフ（DAG）を形成します。これはドキュメントだけでなく、コードとテストによって強制されます。
5. **データの所有:** 各モジュールは自身のデータベーステーブル（またはスキーマ）を所有し、APIを介してのみデータを公開します。

# インストール

Modular Monolith はアーキテクチャの慣習ですが、特定のツールを使用して実装および強制されます。以下の例では、このパターンで最も成熟したフレームワークである Java/Spring Boot エコシステム（Spring Modulith + ArchUnit）を使用しています。同様のツールが .NET（NetArchTest）にも存在します。

## Java / Spring Boot（Spring Modulith + ArchUnit）

次の依存関係を `pom.xml` または `build.gradle` に追加します。

**Maven（pom.xml）:**

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

**Gradle（build.gradle）:**

```gradle
dependencies {
    implementation 'org.springframework.modulith:spring-modulith-starter-core:1.2.0'
    testImplementation 'org.springframework.modulith:spring-modulith-starter-test:1.2.0'
    testImplementation 'com.tngtech.archunit:archunit-junit5:1.3.0'
}
```

# 使用法

## コードベースの構造化

アプリケーションを単一のアプリケーションルートの下に厳密に分離されたモジュールパッケージに整理します。`shared-kernel` パッケージには、すべてのモジュールが依存できるコア値オブジェクトと基本抽象化が含まれています。

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

## モジュールの定義

モジュールルートの `package-info.java` ファイルに `@ApplicationModule` アノテーションを使用します。これにより、Spring Modulith はこのパッケージ階層をモジュールとして扱います。

```java
// orders/package-info.java
@org.springframework.modulith.ApplicationModule(
    displayName = "Order Management",
    allowedDependencies = { "shared-kernel" }
)
package com.company.app.orders;
```

## モジュール間通信（イベント）

疎結合を維持するために、モジュールは非クリティカルなワークフローには直接サービス呼び出しではなく、アプリケーションイベントを介して通信します。

**イベントの公開:**

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

**イベントの消費:**

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

# 主要機能とコマンド例

## 1. アーキテクチャの自動検証

これらのツールの主な価値は、ビルド時に境界違反を検出することです。Spring Modulith はモジュール構造全体をスキャンし、不正なアクセス（例：別のモジュールのプライベートリポジトリへのアクセス）を検出します。

**テスト:**

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

**コマンド:**

```bash
# The build fails early if the architecture is violated.
./mvnw test
```

**違反出力の例:**

```bash
[ERROR] Module 'billing' depends on module 'ordering' through
[ERROR]   com.company.billing.service.InvoiceService -> com.company.ordering.repository.OrderRepository
[ERROR]   (I) Module 'billing' should not depend on Module 'ordering::infrastructure'
```

## 2. モジュール統合テストスライス（`@ModuleTest`）

単一のモジュールを分離して統合テストを実行します。他のモジュールからの依存関係は自動的にモックまたはスタブ化されます。

**テスト:**

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

**コマンド:**

```bash
# Runs only the billing module tests with its dependencies isolated
./mvnw test -Dtest=BillingModuleTest
```

## 3. 依存関係グラフと循環検出（ArchUnit）

DAG（有向非巡回グラフ）を強制し、モジュールが誤ったレイヤーに依存したり、循環を導入することを防ぎます。

**テスト:**

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

**コマンド:**

```bash
# Standard test command, runs arch unit tests alongside unit tests
./mvnw test
```

## 4. アウトボックスパターンの統合

モジュール境界を越えたトランザクションの信頼性のために、フレームワークはアウトボックスパターンをサポートしています。これにより、データベーストランザクションのコミット後にイベントハンドラが失敗した場合のデータ不整合を防ぎます。

**設定:**

```java
// application.yml
spring:
  modulith:
    events:
      outbox:
        enabled: true
```

**コマンド（検証）:**

```bash
# Run a test that verifies the outbox table is correctly polled
# and events are published.
./mvnw test -Dtest=OrderLifecycleTest
```

## 5. 実行時ドキュメントと可視化

Spring Modulith は、モジュール構造のC4スタイルのコンポーネント図とAPIドキュメントを生成できます。

**コマンド:**

```bash
# Generate documentation during the build
./mvnw package
```

**結果:**

`target/` に `modulith-docs` ディレクトリが生成されます。Spring Modulith Actuator を追加して実行時にこれを提供します:

```xml
<dependency>
    <groupId>org.springframework.modulith</groupId>
    <artifactId>spring-modulith-actuator</artifactId>
</dependency>
```

次のURLでドキュメントにアクセス: `http://localhost:8080/modulith-docs`

# モジュラーモノリスを使用すべき場合

**理想的な候補:**

- **ほとんどのエンタープライズアプリケーション**および2〜20人の開発者チームによるSaaS製品。
- **複雑なビジネスロジックを持つ**が、予測可能でモノリシックなトラフィックパターンを持つシステム。
- **スタートアップ**。初日から分散システムを構築することが不必要なリスクとコストを追加する場合。
- **レガシーモノリスの移行**。明確なモジュールへの段階的な解きほぐしは、マイクロサービスへの直接的な「strangler fig」パターンよりも安全です。

**マイクロサービスへの抽出を検討すべき場合:**

- **独立したスケーリングの必要性**。モジュールAは100インスタンス、モジュールBは2インスタンスが必要。
- **厳格な障害分離**。請求モジュールのクラッシュがWebサーバーをダウンさせてはならない。
- **ポリグロット要件**。モジュールが完全に異なるランタイムフレームワークやデータベースエンジンを必要とする。
- **組織の整合性**。チーム構造が完全に独立したマイクロサービスの所有を要求する（コンピューの法則）。

# まとめ

Modular Monolith は、モノリスのシンプルさとマイクロサービスのモジュール性の間のスイートスポットを提供する非常に効果的なアーキテクチャパターンです。主な課題は、時間の経過とともにアーキテクチャの規律を維持することです。これは、フレームワークのサポート（Spring Modulith）、自動化されたアーキテクチャテスト（ArchUnit, NetArchTest）、およびドメイン境界に焦点を当てた強力なチーム文化を通じて管理されます。これは戦略的な中間点を表し、現代のエンタープライズアプリケーションの推奨されるデフォルトの出発点です。