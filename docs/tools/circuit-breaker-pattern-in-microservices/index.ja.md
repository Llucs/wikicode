---
title: マイクロサービスにおける回路切断パターン
description: リモート呼び出しの失敗を適切に処理し、システム内の Cascade 故障を防止するためにマイクロサービスアーキテクチャで使用される設計パターンです。
created: 2026-07-15
tags:
  - microservices
  - 再生性
  - 回路切断
  - 設計パターン
status: draft
---

### マイクロサービスにおける回路切断パターン

#### 回路切断パターンとは何でしょうか？
回路切断パターンは、分散システムや特にマイクロサービスアーキテクチャでのリザリントと信頼性を管理するためのソフトウェアエンジニアリングにおける設計パターンです。リモート呼び出しの失敗を処理するメカニズムとして機能し、サービスが失敗するときの一時的な停止とリカバリーを可能にします。

#### キー機能
1. **失敗の検出**: 回路切断は、事前に設定された失敗の閾値を通過したときにサービスまたはAPI呼び出しの失敗を検出します。
2. **回路切断**: 閾値が通過したとき、回路切断はトリップし、失敗しているサービスにリクエストを送信しないように回路を切断します。
3. **フォールバックメカニズム**: リクエストが失敗する前に潜在的に失敗するサービスから応答を待つのではなく、回路切断は既定の応答またはエラーメッセージを呼び出し元に返却するためのフォールバックメカニズムをトリガーします。
4. **タイムアウトとリトライ**: 回路切断は一時的な失敗に対処するためにタイムアウトとリトライメカニズムを構成することができます。
5. **回路リセット**: サービスが再び正常に動作すると、回路切断はリセットされ、サービスにトラフィックを送信するようになります。

#### 歴史
回路切断の概念は、ハードウェアおよび電気工学の分野で最初に導入されました。その後、Martin FowlerとJames Lewisによって2010年に「マイクロサービス：細粒度のサービス設計」という記事でソフトウェア工学、特に分散システムの文脈でアドапテッドされました。記事はMartinFowler.comで公開されています。

#### 使用例
1. **サービスのダウンハンドリング**: マイクロサービスアーキテクチャで、ダウンストリームサービスが失敗した場合、回路切断は他のサービスがそのサービスと通信を試みないようにすることができ、このためCascade失敗を避けることができます。
2. **パフォーマンス最適化**: 回路を切断することで、不要な処理を防ぎ、全体的なシステムパフォーマンスを改善することができます。
3. **エラー処理**: 失敗を適切に処理するためのメカニズムを提供し、全体的なシステムの影響を軽減します。
4. **リアルタイム監視**: サービスの健康状態を監視し、システムの状態に関するリアルタイムフィードバックを提供するために回路切断を使用できます。

#### インストール
回路切断パターンは、使用されているプログラミング言語とフレームワークによって異なるライブラリとフレームワークを使って実装することができます。以下に一部を示します：

- **Java**: Hystrix (Netflix), Resilience4j, OpenHystrix
- **.NET**: Polly
- **Python**: CircuitBreaker
- **JavaScript**: @liarnp/circuitbreaker

例として、JavaでResilience4jを使用する場合：

```java
import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;

public class CircuitBreakerExample {
    private final CircuitBreakerRegistry circuitBreakerRegistry;
    private final CircuitBreaker circuitBreaker;

    public CircuitBreakerExample() {
        circuitBreakerRegistry = CircuitBreakerRegistry.of("exampleCircuitBreaker");
        circuitBreaker = circuitBreakerRegistry.circuitBreaker("exampleCircuitBreaker");
    }

    public void performCall() {
        if (circuitBreaker.isOpen()) {
            System.out.println("Circuit breaker is open, falling back...");
            return;
        }
        try {
            // サービス呼び出しを実行
        } catch (Exception e) {
            circuitBreakerRegistry.fail(CircuitBreaker.of("exampleCircuitBreaker"));
        }
    }
}
```

#### 基本的な使用法
1. **初期化**: 欲しい構成とともに回路切断を初期化し、回路切断レジストリに登録します。
2. **使用**: サービス呼び出しを回路切断で包みます。呼び出しが失敗した場合、回路切断は回路を切断し、その後の呼び出しはフォールバックメカニズムを使用します。
3. **リセット**: サービスが再び正常に動作するとき、回路切断は自己リセットします。

回路切断パターンを実装することで、開発者はマイクロサービスの再生性と信頼性を向上させ、システムが失敗を適切に処理し、高い可用性を維持できるようにすることができます。

---