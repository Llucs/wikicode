---
title: 观察者设计模式
description: 一种行为型设计模式，定义对象之间的一对多依赖关系，使得当一个对象改变状态时，其所有依赖者都能自动收到通知并更新。
created: 2026-06-16
tags:
  - design-patterns
  - behavioral
  - observer
  - publish-subscribe
  - event-driven
status: draft
---

# 观察者设计模式

## 什么是观察者模式

**观察者模式**是一种行为型设计模式，其中一个称为**主题**（或**可观察对象**）的对象维护一个依赖者列表（称为**观察者**），并在状态发生变化时自动通知它们，通常通过调用观察者的某个方法。该模式建立了一对多的依赖关系，使得当主题状态变化时，所有观察者都能自动更新。此模式也被称为*发布-订阅*、*事件监听器*或*依赖者*。

```plaintext
主题 ──→ 观察者1
         ├→ 观察者2
         └→ 观察者3
```

## 为什么要用观察者模式？

- **松耦合** – 主题只了解观察者实现了特定接口，不依赖具体的观察者类。
- **动态订阅** – 可以在运行时添加或移除观察者，而无需修改主题。
- **广播通信** – 单个主题高效地向所有已注册的观察者推送更新。
- **开闭原则** – 可以在不修改主题代码的情况下引入新的观察者。
- **避免轮询** – 观察者自动接收更新，无需反复检查主题状态。

## 安装方式

由于观察者模式是一个设计概念，它是**在代码中实现**的，而不是作为包安装的。不过，许多语言和库都提供了内置支持：

| 语言/平台 | 内置/包 |
|-----------|----------|
| Node.js   | `EventEmitter`（核心模块 `events`） |
| Python    | `pip install rx`（ReactiveX）或通过 `asyncio` 使用核心 `Observable` |
| JavaScript/TypeScript | `npm install rxjs` |
| Java      | `java.beans.PropertyChangeSupport` 或 `java.util.concurrent.Flow` |
| C#        | 语言自带的 `event` 关键字和委托 |

### 安装命令示例

```bash
# JavaScript/TypeScript (ReactiveX)
npm install rxjs

# Python (ReactiveX)
pip install rx

# Node.js EventEmitter 无需安装（核心模块）
```

## 主要特性

- **一对多通知** – 单个主题一致地通知多个观察者。
- **松耦合** – 主题只依赖观察者接口，而非具体实现。
- **广播通信** – 状态变化被推送给所有观察者（或通过通知拉取）。
- **动态订阅** – 观察者可随时订阅或取消订阅。
- **自动更新** – 观察者无需轮询即可保持同步。

## 使用示例

### 经典 Python 实现（纯 Python）

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

### Node.js EventEmitter

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

### RxJS (JavaScript)

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

### Java (使用 `java.util.concurrent.Flow`)

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

## 优点与缺点

### 优点

- **松耦合** – 主题和观察者相互独立。
- **可复用性** – 观察者可在不同主题间复用。
- **动态关系** – 订阅可在运行时更改。
- **自动通知** – 观察者无需轮询即可更新。

### 缺点

- **顺序不可预测** – 观察者的通知顺序可能是任意的。
- **内存泄漏** – 如果观察者未被正确解绑，可能造成累积。
- **复杂的更新链** – 重入更新可能难以调试。
- **通知开销** – 若设计不当，通知大量观察者可能代价高昂。

## 历史与背景

观察者模式最初在 1994 年的《设计模式：可复用面向对象软件的基础》（GoF 四人组：Erich Gamma，Richard Helm，Ralph Johnson，John Vlissides）中正式编目。其概念根源可追溯到 1970 年代末 Xerox PARC 为 Smalltalk 开发的**模型-视图-控制器（MVC）** 架构，其中视图（观察者）监听模型（主题）的变化。

如今，该模式已成为以下领域的基础：

- 事件驱动编程（DOM 事件、GUI 监听器）
- 响应式编程（RxJS、Project Reactor）
- 数据绑定框架（Vue.js、Knockout、JavaFX）
- 分布式消息传递（Kafka、MQTT）

## 常见用例

- **GUI 系统** – 按钮点击、鼠标移动、按键事件。
- **数据绑定** – 当模型变化时自动更新 UI。
- **响应式流** – 支持背压的异步数据管道。
- **日志记录** – 将日志消息分发到多个输出（控制台、文件、网络）。
- **金融系统** – 将股票实时行情推送到多个仪表盘。
- **消息代理** – 通过解耦的中间件实现发布者/订阅者模式。

---

*观察者模式仍然是事件驱动架构的基石，支持松散耦合组件间清晰、可维护的通信。*