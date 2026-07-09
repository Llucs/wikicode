---
title: Saga 模式
description: 在微服务架构中管理跨多个服务或资源的分布式事务的设计模式。
created: 2026-07-09
tags:
  - 微服务
  - 分布式事务
  - 设计模式
  - saga 模式
status: 草稿
---

# Saga 模式

## 概览

Saga 模式是一种用于分布式系统中管理跨多个服务或资源的事务的设计模式。它通过维护一个必须成功完成的操作序列来确保操作的一致性和可靠性。如果任何操作失败，该模式允许回滚所有已完成的操作，以保持系统的完整性。

## 关键特性

1. **补偿操作**: 为每个工作单元（操作），定义一个相应的补偿操作，可以撤销该工作单元所做的更改。这样，如果操作失败，系统可以恢复到其先前的状态。
2. **顺序执行**: 操作按照特定顺序执行，每个操作都依赖于前一个操作的成功。
3. **最终一致性**: 该模式确保系统随着时间的推移逐渐达到一致状态，即使个别事务失败。
4. **幂等性**: Saga 中的操作应具有幂等性，以确保如果相同操作被多次调用，系统的状态不会改变。

## 历史

Saga 模式是为了解决在微服务架构中管理分布式事务的挑战而开发的。在微服务出现之前，单体应用程序通常在数据库级别管理事务。然而，随着应用程序变得更加分布化，跨多个服务管理事务的复杂性增加了。Saga 模式被引入来处理这些复杂性。

Sagas 的概念可以追溯到 1970 年代 Jim Gray 在事务处理方面的研究，但在 2010 年代在微服务和分布式系统领域中变得更为突出。

## 使用场景

1. **金融交易**: 处理转账、支付和退款等交易需要确保资金正确地在账户之间转移。Saga 可以管理这些操作，确保如果转账失败，原始余额可以恢复。
2. **订单处理**: 在电子商务中，处理订单涉及多个步骤，如创建产品预留、更新库存和向客户收费。Saga 可以确保所有这些操作成功完成或如果任何操作失败则回滚。
3. **医疗系统**: 在医疗领域，交易如账单、预约安排和处方管理需要确保所有步骤成功完成或如果任何步骤失败则回滚，以保持患者数据的完整性。
4. **保险索赔**: 处理保险索赔涉及多个步骤，如索赔处理、支付和文档验证。Saga 可以管理这些操作，确保索赔正确处理或如果流程中的任何部分失败则回滚。

## 安装和设置

Saga 模式通常通过应用程序编程和中间件服务的组合来实现。以下是如何设置 Saga 的基本概述：

1. **定义操作**: 识别作为 Saga 部分需要执行的操作。对于每个操作，定义补偿动作。
2. **使用消息队列**: 实现消息队列以管理操作的执行。这可以是 RabbitMQ、Kafka 或 AWS SQS 等消息代理。
3. **Saga 管理器**: 创建一个 Saga 管理器来协调操作序列。管理器应处理操作的执行、跟踪 Saga 的状态以及如果操作失败则管理补偿逻辑。
4. **补偿动作**: 实现补偿动作以在操作失败时将系统的状态恢复到其先前的状态。

### 基本使用

1. **启动 Saga**: 通过启动序列中的第一个操作开始 Saga。
2. **执行操作**: 按顺序执行每个操作。如果操作失败，Saga 应停止并执行补偿动作。
3. **跟踪状态**: 保持 Saga 的有状态记录以跟踪进度并确保操作按正确的顺序完成。
4. **补偿**: 如果操作失败，Saga 应执行补偿动作以将系统恢复到一致状态。
5. **完成 Saga**: 一旦所有操作成功完成，Saga 可以标记为完成。

### 示例

以下是一个 Python 示例，演示了 Saga 的基本结构，其中操作入队并按顺序执行，定义了补偿动作以处理失败：

```python
from queue import Queue

# 定义操作和补偿动作
def create_product_reservation(product_id, quantity):
    # 实现创建产品预留
    pass

def update_inventory(product_id, quantity):
    # 实现更新库存
    pass

def charge_customer(customer_id, amount):
    # 实现向客户收费
    pass

def cancel_reservation(product_id, quantity):
    # 实现取消预留
    pass

def refund_customer(customer_id, amount):
    # 实现向客户退款
    pass

# 定义 Saga
def process_order(saga_id, product_id, quantity, customer_id, amount):
    saga_queue = Queue()

    try:
        saga_queue.put(create_product_reservation(product_id, quantity))
        saga_queue.put(update_inventory(product_id, quantity))
        saga_queue.put(charge_customer(customer_id, amount))
        
        while not saga_queue.empty():
            operation = saga_queue.get()
            operation()
        
        # 标记 Saga 完成
        print(f"Saga {saga_id} 完成成功。")
    except Exception as e:
        # 执行补偿动作
        while not saga_queue.empty():
            operation = saga_queue.get()
            operation()
        print(f"Saga {saga_id} 失败。执行了补偿动作。")
        
# 启动 Saga
process_order(1, "P123", 10, "C12345", 100)
```

此示例演示了 Saga 的基本结构，其中操作按顺序入队并执行，定义了补偿动作以处理失败。

## 结论

Saga 模式是管理分布式系统中跨多个服务的事务的稳健解决方案。通过确保操作按特定顺序执行并提供补偿动作来处理失败，该模式帮助保持系统的完整性。理解 Saga 模式对于开发可靠和可扩展的微服务架构至关重要。