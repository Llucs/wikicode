---
title: オブザーバーデザインパターン
description: オブジェクト間の一対多の依存関係を定義する行動デザインパターンであり、あるオブジェクトの状態が変化すると、そのすべての依存オブジェクトに対して自動的に通知と更新が行われます。
created: 2026-06-16
tags:
  - design-patterns
  - behavioral
  - observer
  - publish-subscribe
  - event-driven
status: draft
---

# オブザーバーデザインパターン

## 概要

**Observer パターン**は、行動デザインパターンの一種です。**Subject**（または**Observable**）と呼ばれるオブジェクトが、自身の依存オブジェクト（**Observer**）のリストを保持し、状態が変化すると、Observer のメソッドを呼び出すことで自動的に通知を行います。これにより、一対多の依存関係が確立され、Subject の状態が変わるとすべての Observer が自動的に更新されます。このパターンは *Publish-Subscribe*、*Event Listener*、または *Dependents* としても知られています。

```plaintext
Subject ──→ Observer 1
         ├→ Observer 2
         └→ Observer 3
```

## なぜ使用するのか

- **疎結合** – Subject は Observer が特定のインターフェースを実装していることだけを知っており、具体的な Observer クラスに依存しません。
- **動的な購読** – 実行時に Subject を変更することなく Observer を追加または削除できます。
- **ブロードキャスト通信** – 1つの Subject が効率的に全購読 Observer に更新をプッシュします。
- **オープン/クローズドの原則** – Subject のコードを変更せずに新しい Observer を導入できます。
- **ポーリング不要** – Observer は Subject の状態を繰り返しチェックするのではなく、自動的に更新を受け取ります。

## インストール

Observer パターンは設計概念であるため、**コード内で実装**するものであり、パッケージとしてインストールするものではありません。ただし、多くの言語やライブラリに組み込みサポートがあります。

| 言語 / プラットフォーム | 組み込み / パッケージ |
|-------------------------|------------------------|
| Node.js                 | `EventEmitter`（コアモジュール `events`） |
| Python                  | `pip install rx`（ReactiveX）または `asyncio` の `Observable` |
| JavaScript / TypeScript | `npm install rxjs` |
| Java                    | `java.beans.PropertyChangeSupport` または `java.util.concurrent.Flow` |
| C#                      | 言語の `event` キーワードとデリゲート |

### インストールコマンド例

```bash
# JavaScript/TypeScript (ReactiveX)
npm install rxjs

# Python (ReactiveX)
pip install rx

# For Node.js EventEmitter, no installation needed (core module)
```

## 主な機能

- **一対多の通知** – 単一の Subject が複数の Observer に一貫して通知します。
- **疎結合** – Subject は Observer インターフェースのみに依存し、具体的な実装には依存しません。
- **ブロードキャスト通信** – 状態変化がすべての Observer にプッシュされます（通知を介したプルも可能）。
- **動的な購読** – Observer はいつでも購読/購読解除が可能です。
- **自動更新** – ポーリングを必要とせずに Observer は同期を保ちます。

## 使用例

### クラシックな Python 実装（純粋）

```python
# Subject
class NewsAgency:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, news):
        for observer in self._observers:
            observer.update(news)

# Observer interface
class Observer:
    def update(self, news):
        raise NotImplementedError

# Concrete observers
class EmailNotifier(Observer):
    def update(self, news):
        print(f"Email sent with: {news}")

class SMSNotifier(Observer):
    def update(self, news):
        print(f"SMS sent with: {news}")

# Usage
news = NewsAgency()
news.attach(EmailNotifier())
news.attach(SMSNotifier())
news.notify("Breaking: Stock market hits new high!")
# Output:
# Email sent with: Breaking: Stock market hits new high!
# SMS sent with: Breaking: Stock market hits new high!
```

### Node.js EventEmitter の例

```javascript
const EventEmitter = require('events');

class NewsAgency extends EventEmitter {
    publish(news) {
        this.emit('news', news);
    }
}

// Observers (listeners)
const agency = new NewsAgency();

agency.on('news', (news) => console.log(`Email: ${news}`));
agency.on('news', (news) => console.log(`SMS: ${news}`));

agency.publish('Breaking: Stock market hits new high!');
// Output:
// Email: Breaking: Stock market hits new high!
// SMS: Breaking: Stock market hits new high!
```

### RxJS（JavaScript）

```javascript
import { Subject } from 'rxjs';

const subject = new Subject();

// Observer A
subject.subscribe(val => console.log(`Observer A: ${val}`));
// Observer B
subject.subscribe(val => console.log(`Observer B: ${val}`));

subject.next("Hello World");
// Output:
// Observer A: Hello World
// Observer B: Hello World
```

### Java（`java.util.concurrent.Flow` を使用）

```java
import java.util.concurrent.Flow.*;
import java.util.concurrent.SubmissionPublisher;

public class ObserverExample {
    public static void main(String[] args) {
        SubmissionPublisher<String> publisher = new SubmissionPublisher<>();

        Subscriber<String> subscriber1 = new Subscriber<>() {
            private Subscription sub;
            public void onSubscribe(Subscription sub) { this.sub = sub; sub.request(1); }
            public void onNext(String item) { System.out.println("Subscriber1: " + item); sub.request(1); }
            public void onError(Throwable t) { t.printStackTrace(); }
            public void onComplete() { System.out.println("Done"); }
        };

        publisher.subscribe(subscriber1);
        publisher.submit("Hello");
        publisher.submit("World");
        publisher.close();
    }
}
```

## メリットとデメリット

### メリット

- **疎結合** – Subject と Observer は独立しています。
- **再利用性** – Observer は異なる Subject 間で再利用できます。
- **動的な関係** – 購読は実行時に変更可能です。
- **自動通知** – ポーリングなしで Observer が更新されます。

### デメリット

- **通知順序が不確定** – Observer への通知順序は不定です。
- **メモリリーク** – Observer が適切にデタッチされないと蓄積される可能性があります。
- **複雑な更新連鎖** – 再入可能な更新はデバッグが困難になることがあります。
- **通知オーバーヘッド** – 多数の Observer への通知は、設計を注意しないとコストがかかる可能性があります。

## 歴史と背景

Observer パターンは、1994 年の書籍『Design Patterns: Elements of Reusable Object‑Oriented Software』（通称 GoF: Gang of Four）によって体系化されました。その概念的なルーツは、1970 年代後半に Xerox PARC で Smalltalk 向けに開発された **Model‑View‑Controller（MVC）** アーキテクチャにあり、View（Observer）が Model（Subject）の変更を待ち受けます。

現在では、このパターンは以下の分野で基本となっています。

- イベント駆動プログラミング（DOM イベント、GUI リスナー）
- リアクティブプログラミング（RxJS、Project Reactor）
- データバインディングフレームワーク（Vue.js、Knockout、JavaFX）
- 分散メッセージング（Kafka、MQTT）

## 一般的なユースケース

- **GUI システム** – ボタンクリック、マウス移動、キー押下。
- **データバインディング** – モデルが変更されたときに UI を自動更新。
- **リアクティブストリーム** – バックプレッシャーを備えた非同期データパイプライン。
- **ロギング** – ログメッセージを複数の出力先（コンソール、ファイル、ネットワーク）に配信。
- **金融システム** – 株価ティッカーの更新を複数のダッシュボードにプッシュ。
- **メッセージングブローカー** – デカップリングされたパブリッシャー/サブスクライバー。

---

*Observer パターンはイベント駆動アーキテクチャの基盤であり、疎結合なコンポーネント間のクリーンで保守しやすい通信を可能にします。*