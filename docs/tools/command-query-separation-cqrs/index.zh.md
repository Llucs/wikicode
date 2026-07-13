---
title: 命令查询分离 (CQRS)
description: 一种用于软件架构的设计模式，用于将命令（写操作）与查询（读操作）分离。
created: 2026-07-13
tags:
  - 软件架构
  - 设计模式
  - CQRS
  - 命令查询分离
status: 草稿
---

# 命令查询分离 (CQRS)

命令查询分离 (CQRS) 是一种用于软件架构的设计模式，用于将命令（写操作）与查询（读操作）分离。这种分离可以使应用程序更加易于维护和扩展，尤其是在复杂的现实场景中。

## 什么是CQRS？

CQRS 强调将获取信息的动作（查询）与修改状态的动作（命令）分开。这种分离可以使应用程序更加易于维护和扩展，尤其是在高事务量或复杂的业务逻辑系统中。

## 主要特性

1. **命令处理**：命令用于修改系统的状态。它们通常由外部系统或用户发出，并用于执行创建、更新或删除数据等操作。
2. **查询处理**：查询用于从系统中检索信息。它们是只读操作，不会修改系统的状态。查询可以通过优化读取密集型工作负载来提高效率，这通常比单一数据存储同时处理读取和写入更为高效。
3. **职责分离**：CQRS 有助于分离写操作和读操作的职责，使系统更加易于维护和扩展。
4. **事件溯源**：通常与 CQRS 结合使用，记录系统更改作为一系列事件的序列。这些事件可以用于重构系统的当前状态或触发命令。

## 历史

CQRS 并不是一个新的概念，当它首次流行时，并不是一个全新的想法。将命令和查询分开的概念早就存在，但直到 Greg Young 和 Udi Dahan 在 2010 年代早期倡导后，才得到了广泛的应用。他们在各种会议和研讨会中提出了他们的想法，导致该模式的更广泛应用。

## 使用场景

1. **在线事务处理 (OLTP)**：CQRS 在需要高写入吞吐量的系统中特别有用，例如电子商务平台、金融服务系统或游戏应用。
2. **数据仓库**：CQRS 可以帮助构建数据仓库，通过将写入密集型的事务数据与读取密集型的分析数据分开来。
3. **复杂业务逻辑**：具有复杂业务逻辑且需要频繁更新和修改的系统可以从命令和查询的分离中受益。

## 安装

CQRS 并不是一个独立的框架，而是一种设计模式。因此，它没有直接的安装步骤。然而，您可以按照以下一般步骤在应用程序中实现 CQRS：

1. **定义命令和查询**：创建一组处理写操作的命令类和处理读操作的查询类。
2. **实现命令处理器**：编写处理命令并执行数据操作的处理器。
3. **实现查询处理器**：编写处理查询并返回所需数据的处理器。
4. **事件溯源（可选）**：实现事件溯源以捕获系统的更改，并使用这些事件来更新读取模型。

## 基本用法

### 处理命令

```csharp
public class OrderService {
    private readonly CommandBus _commandBus;

    public OrderService(CommandBus commandBus) {
        _commandBus = commandBus;
    }

    public void PlaceOrder(Order order) {
        _commandBus.Send(new PlaceOrderCommand(order));
    }
}
```

### 处理查询

```csharp
public class OrderQueryService {
    private readonly QueryBus _queryBus;

    public OrderQueryService(QueryBus queryBus) {
        _queryBus = queryBus;
    }

    public Order GetOrderById(Guid orderId) {
        return _queryBus.Send(new GetOrderByIdQuery(orderId));
    }
}
```

### 事件溯源

```csharp
public class OrderAggregate {
    private readonly IEventRepository _eventRepository;

    public OrderAggregate(IEventRepository eventRepository) {
        _eventRepository = eventRepository;
    }

    public void ApplyCommand(PlaceOrderCommand command) {
        // 应用命令并保存事件
        _eventRepository.Save(new OrderPlacedEvent(command.Order.Id, command.Order.CustomerId));
    }
}
```

## 结论

CQRS 是一种强大的设计模式，可以显著提高复杂应用程序的可扩展性和可维护性。通过将命令和查询分离，开发人员可以优化系统的写入和读取操作，从而创建更高效和健壮的应用程序。然而，要有效地实现 CQRS，需要仔细的设计和实现，而且它可能并不适用于所有类型的应用程序。