---
title: マイクロサービスにおけるリザリエンスパターン
description: リザリエンスパターンは、マイクロサービスアーキテクチャが故障を処理し、高可用性を維持するための設計戦略と実践を提供します。これらのパターンは、システムの一部がダウンしても故障からの回復、滑らかな劣化、ユーザーにとって価値を提供し続けることが重要なシステムで不可欠です。
created: 2026-07-17
tags:
  - microservices
  - resilience
  - architecture
status: draft
---

# マイクロサービスにおけるリザリエンスパターン

リザリエンスパターンは、システムが故障を処理し、高可用性を維持するための設計戦略と実践です。これらのパターンは、故障からの回復、滑らかな劣化、ユーザーにとって価値を提供し続けることが重要なシステムにおいて不可欠です。

## リザリエンスパターンの主な特徴

1. **故障耐性**: システムの一部が故障しても動作を続ける能力。
2. **ロードバランス**: 要求を複数のインスタンス間で分散し、単一のサービスに過負荷を避ける。
3. **Circuit Breaker**: 失敗したサービスに対してリクエストを停止し、連鎖的な故障を防ぐメカニズム。
4. **バックファール**: メインサービスが失敗したときに既定の応答を返す。
5. **タイムアウト**: リクエストが完了するまでの時間を制限する。
6. **リトライメカニズム**: 失敗したリクエストを短い期間後に自動的に再試行する。
7. **劣化**: 全機能が利用できない場合、簡略化されたまたは制限されたサービスを提供する。
8. **ヘルスチェック**: サービスの健康状態を監視し、事前に問題を検出し対処する。

## 歴史

リザリエンスパターンの概念は、マイクロサービスアーキテクチャが普及したときに注目を集めるようになりました。これらのパターンは、マイクロサービスがより複雑で分散されたシステムを導入したときに必要となりました。故障耐性とロードバランスに関する早期の作業は、分散システムの研究に遡りますが、マイクロサービスとクラウドコンピューティングの現代的な文脈においては、その重要性が大きく拡大しました。

## 使用例

1. **金融サービス**: 高可用性と故障耐性は、金融損失を避けるために重要です。
2. **電子商取引**: 支払い処理と在庫管理システムがピークロードと故障を処理できるようにすること。
3. **医療**: サービスの可用性を維持することは、患者データの損失や誤った治療を避けるために重要です。
4. **リアルタイムデータ処理**: ストリーミングデータのリアルタイム処理と分析を必要とするシステム。
5. **クラウドサービス**: クラウドリソースの動的な予測不能な性質を管理します。

## インストールと設定

リザリエンスパターンを設定するには、ソフトウェアとインフラストラクチャの両方のコンポーネントが必要です。

1. **ソフトウェアライブラリとツール**:
   - **Netflix Hystrix**: パスワードブレーカー、バックファール、タイムアウト、リトライを管理するライブラリ。
   - **Resilience4j**: Javaベースのリザリエンスライブラリで、リザリエンスパターンを実装するためのシンプルなAPIを提供します。
   - **Spring Cloud Circuit Breaker**: Springエコシステム内のHystrixの実装。

2. **インフラストラクチャソリューション**:
   - **ロードバランサ**: NGINX、AWS Elastic Load Balancer、HAProxyなどのサービスを構成してトラフィックを分散します。
   - **サービスメッシュ**: IstioやLinkerdなどのツールは、故障挿入、パスワードブレーカー、リトライをより高度な抽象化レベルで提供します。

### 例の設定

次は、JavaアプリケーションでResilience4jを使用してパスワードブレーカーを設定する方法の例です：

```java
import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;

public class Example {

    private final CircuitBreakerRegistry circuitBreakerRegistry;

    public Example(CircuitBreakerRegistry circuitBreakerRegistry) {
        this.circuitBreakerRegistry = circuitBreakerRegistry;
    }

    @CircuitBreaker(name = "exampleService", fallbackMethod = "fallbackMethod")
    public String callExampleService() {
        // exampleServiceへの呼び出し
        return "exampleServiceから結果";
    }

    public String fallbackMethod() {
        return "バックファール応答";
    }
}
```

## 基本的な使用例

### パスワードブレーカー

1. **実装**: HystrixやResilience4jを使用してパスワードブレーカーを実装します。
2. **設定**: カットオフの閾値を定義します（例：1分間50回の失敗）、リセット時間も定義します（例：30秒）。
3. **使用**: サービス呼び出しをパスワードブレーカーで囲み、故障を検出し、故障しているサービスに対してさらなる呼び出しを停止します。

### Resilience4jを使用した例

```java
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;

public class Example {

    private final CircuitBreakerRegistry circuitBreakerRegistry;

    public Example(CircuitBreakerRegistry circuitBreakerRegistry) {
        this.circuitBreakerRegistry = circuitBreakerRegistry;
    }

    @CircuitBreaker(name = "exampleService", fallbackMethod = "fallbackMethod")
    public String callExampleService() {
        // exampleServiceへの呼び出し
        return "exampleServiceから結果";
    }

    public String fallbackMethod() {
        return "バックファール応答";
    }
}
```

### タイムアウト

1. **設定**: サービス呼び出しのタイムアウトを設定します（例：データベース要求は500ミリ秒）。
2. **使用**: すべてのサービス呼び出しをタイムアウトで囲み、無限の待ち時間を避けることを確認します。

### Resilience4jを使用した例

```java
import io.github.resilience4j.ratelimiter.RateLimiter;
import io.github.resilience4j.ratelimiter.RateLimiterRegistry;
import io.github.resilience4j.ratelimiter.annotation.RateLimiter;

public class Example {

    private final RateLimiterRegistry rateLimiterRegistry;

    public Example(RateLimiterRegistry rateLimiterRegistry) {
        this.rateLimiterRegistry = rateLimiterRegistry;
    }

    @RateLimiter(name = "exampleService", fallbackMethod = "fallbackMethod")
    public String callExampleService() {
        // exampleServiceへの呼び出し
        return "exampleServiceから結果";
    }

    public String fallbackMethod() {
        return "バックファール応答";
    }
}
```

### バックファールメカニズム

1. **実装**: メインサービスが失敗したときに既定の応答や制限されたサービスを提供します。
2. **使用**: バックファールを使用してメインサービスが利用できない場合にデフォルトまたは制限されたサービスを提供します。

### Resilience4jを使用した例

```java
import io.github.resilience4j.ratelimiter.RateLimiter;
import io.github.resilience4j.ratelimiter.RateLimiterRegistry;
import io.github.resilience4j.ratelimiter.annotation.RateLimiter;

public class Example {

    private final RateLimiterRegistry rateLimiterRegistry;

    public Example(RateLimiterRegistry rateLimiterRegistry) {
        this.rateLimiterRegistry = rateLimiterRegistry;
    }

    @RateLimiter(name = "exampleService", fallbackMethod = "fallbackMethod")
    public String callExampleService() {
        // exampleServiceへの呼び出し
        return "exampleServiceから結果";
    }

    public String fallbackMethod() {
        return "バックファール応答";
    }
}
```

### リトライメカニズム

1. **設定**: 再試行の回数とバックオフ戦略（例：指数的バックオフ）を定義します。
2. **使用**: サービス呼び出しをリトライメカニズムで囲み、失敗したリクエストを自動的に再試行します。

### Resilience4jを使用した例

```java
import io.github.resilience4j.retry.Retry;
import io.github.resilience4j.retry.RetryRegistry;
import io.github.resilience4j.retry.annotation.Retry;

public class Example {

    private final RetryRegistry retryRegistry;

    public Example(RetryRegistry retryRegistry) {
        this.retryRegistry = retryRegistry;
    }

    @Retry(name = "exampleService", fallbackMethod = "fallbackMethod")
    public String callExampleService() {
        // exampleServiceへの呼び出し
        return "exampleServiceから結果";
    }

    public String fallbackMethod() {
        return "バックファール応答";
    }
}
```

### ヘルスチェック

1. **実装**: PrometheusやKubernetesのライブネスプローブを使用してサービスの健康状態を監視します。
2. **使用**: ヘルスチェックを構成して故障を検出し、適切なアクションを実行します（例：サービスを再起動）。

### Kubernetesを使用した例

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: example-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: example-service
  template:
    metadata:
      labels:
        app: example-service
    spec:
      containers:
      - name: example-service
        image: example-service:latest
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
```

## 結論

リザリエンスパターンは、堅牢なマイクロサービスアーキテクチャを構築するための不可欠な要素です。これらのパターンを実装することで、開発者はシステムが故障を処理し、高負荷を処理し、ユーザーが困難な状況下でも価値を提供できるように確保できます。