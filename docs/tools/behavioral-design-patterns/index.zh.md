---
title: 行为设计模式
description: 专注于对象间的交互和通信，包括观察者模式和策略模式等。
created: 2026-06-28
tags:
  - 设计模式
  - 软件工程
  - 面向对象编程
status: 草稿
---

# 行为设计模式

行为设计模式是一类软件设计模式，处理算法和对象间的通信。这些模式集中在对象间的交互和它们如何通信以实现特定行为上。它们有助于管理复杂的控制流，并简化对象间的通信。

## 概述

行为设计模式关注对象间的交互和责任。这些模式有助于管理系统中的对象交互和责任，使其更容易维护和扩展。它们通过封装行为在独立的类中来促进代码复用。

## 关键行为设计模式

### 1. 策略模式

#### 定义
策略模式定义了一组算法，封装每个算法，并使其可以互相替换。

#### 核心特点
- 封装一组算法。
- 允许在运行时选择算法。
- 为算法提供接口，但隐藏其实现细节。

#### 历史
在Erich Gamma等人的著作《设计模式：可复用面向对象软件的基础》一书中介绍，该书于1994年出版。

#### 使用场景
- 在需要动态选择或更改算法的系统中使用，如排序算法、支付网关和不同的日志级别。

#### 基本用法
定义一个算法的接口，实现不同的算法，并将每个算法封装在单独的类中。上下文类使用接口与算法进行交互。

```java
public interface Strategy {
    void algorithmInterface();
}

public class ConcreteStrategyA implements Strategy {
    public void algorithmInterface() {
        System.out.println("Executing Strategy A");
    }
}

public class ConcreteStrategyB implements Strategy {
    public void algorithmInterface() {
        System.out.println("Executing Strategy B");
    }
}

public class Context {
    private Strategy strategy;

    public void setStrategy(Strategy strategy) {
        this.strategy = strategy;
    }

    public void executeAlgorithm() {
        strategy.algorithmInterface();
    }
}

public class Main {
    public static void main(String[] args) {
        Context context = new Context();
        context.setStrategy(new ConcreteStrategyA());
        context.executeAlgorithm(); // 输出: Executing Strategy A

        context.setStrategy(new ConcreteStrategyB());
        context.executeAlgorithm(); // 输出: Executing Strategy B
    }
}
```

### 2. 观察者模式

#### 定义
观察者模式定义了一种对象之间的依赖关系，使得当一个对象的状态发生变化时，所有依赖于它的对象都会自动通知并更新。

#### 核心特点
- 主体维护一个观察者列表。
- 允许订阅和退订机制。
- 当其状态发生变化时通知观察者。

#### 历史
也在Erich Gamma等人的著作《设计模式：可复用面向对象软件的基础》一书中介绍。

#### 使用场景
- 在GUI框架、事件处理和任何需要一个对象的状态变化触发另一个对象变化的系统中使用。

#### 基本用法
定义一个`Observer`接口，创建观察者类，并实现一个`Subject`，该`Subject`维护一个观察者列表并在其状态发生变化时通知观察者。

```java
public interface Observer {
    void update(String message);
}

public class ConcreteObserver implements Observer {
    public void update(String message) {
        System.out.println("Observer received message: " + message);
    }
}

public class Subject {
    private List<Observer> observers = new ArrayList<>();

    public void addObserver(Observer observer) {
        observers.add(observer);
    }

    public void removeObserver(Observer observer) {
        observers.remove(observer);
    }

    public void notifyObservers(String message) {
        for (Observer observer : observers) {
            observer.update(message);
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Subject subject = new Subject();
        Observer observer1 = new ConcreteObserver();
        Observer observer2 = new ConcreteObserver();

        subject.addObserver(observer1);
        subject.addObserver(observer2);

        subject.notifyObservers("Hello, Observer Pattern!"); // 输出: Observer received message: Hello, Observer Pattern!
                                                              //        Observer received message: Hello, Observer Pattern!
    }
}
```

### 3. 命令模式

#### 定义
命令模式将请求转换为一个独立的对象，该对象包含请求的所有信息。

#### 核心特点
- 封装一个请求为一个对象。
- 允许用不同的请求参数化方法、延迟或排队执行请求。
- 允许执行不可撤销的操作。

#### 历史
在Erich Gamma等人的著作《设计模式：可复用面向对象软件的基础》一书中介绍。

#### 使用场景
- 在GUI、撤销/重做操作以及任何需要参数化请求的系统中使用。

#### 基本用法
定义一个`Command`接口，创建具体的命令类，并通过`Command`对象执行命令。

```java
public interface Command {
    void execute();
}

public class ConcreteCommand implements Command {
    private Receiver receiver;

    public ConcreteCommand(Receiver receiver) {
        this.receiver = receiver;
    }

    public void execute() {
        receiver.action();
    }
}

public class Receiver {
    public void action() {
        System.out.println("Executing receiver action");
    }
}

public class Invoker {
    private Command command;

    public void setCommand(Command command) {
        this.command = command;
    }

    public void executeCommand() {
        command.execute();
    }
}

public class Main {
    public static void main(String[] args) {
        Receiver receiver = new Receiver();
        Command command = new ConcreteCommand(receiver);
        Invoker invoker = new Invoker();
        invoker.setCommand(command);
        invoker.executeCommand(); // 输出: Executing receiver action
    }
}
```

### 4. 访问者模式

#### 定义
访问者模式表示对对象结构中元素的操作。

#### 核心特点
- 封装对象结构中元素的操作。
- 允许在不更改现有类的情况下添加新操作。

#### 历史
在Erich Gamma等人的著作《设计模式：可复用面向对象软件的基础》一书中介绍。

#### 使用场景
- 在需要向类层次结构添加新操作但不更改现有类的系统中使用，例如在AST遍历中。

#### 基本用法
定义一个`Visitor`接口，在访问者类中实现操作，并将访问者应用于结构中的对象。

```java
public interface Visitor {
    void visitConcreteElementA(ConcreteElementA element);
    void visitConcreteElementB(ConcreteElementB element);
}

public class ConcreteElementA {
    public void accept(Visitor visitor) {
        visitor.visitConcreteElementA(this);
    }
}

public class ConcreteElementB {
    public void accept(Visitor visitor) {
        visitor.visitConcreteElementB(this);
    }
}

public class ConcreteVisitorA implements Visitor {
    public void visitConcreteElementA(ConcreteElementA element) {
        System.out.println("Visiting ConcreteElementA");
    }

    public void visitConcreteElementB(ConcreteElementB element) {
        System.out.println("Visiting ConcreteElementB");
    }
}

public class Main {
    public static void main(String[] args) {
        ConcreteElementA elementA = new ConcreteElementA();
        ConcreteElementB elementB = new ConcreteElementB();
        Visitor visitor = new ConcreteVisitorA();

        elementA.accept(visitor); // 输出: Visiting ConcreteElementA
        elementB.accept(visitor); // 输出: Visiting ConcreteElementB
    }
}
```

### 5. 事务模式

#### 定义
事务模式捕获对象的内部状态，而不违反封装，然后让对象恢复到该之前的状态。

#### 核心特点
- 封装对象的内部状态。
- 提供恢复该状态的机制。

#### 历史
在Erich Gamma等人的著作《设计模式：可复用面向对象软件的基础》一书中介绍。

#### 使用场景
- 在需要撤销更改的系统中使用，例如在文本编辑器或游戏中。

#### 基本用法
定义一个`Memento`类来存储状态，一个`Caretaker`类来管理事务，以及一个`Originator`类来维护状态并可以从事务中恢复。

```java
public class Originator {
    private String state;

    public void setState(String state) {
        this.state = state;
    }

    public Memento saveStateToMemento() {
        return new Memento(state);
    }

    public void restoreStateFromMemento(Memento memento) {
        this.state = memento.getState();
    }

    public String getState() {
        return state;
    }

    public class Memento {
        private String state;

        public Memento(String state) {
            this.state = state;
        }

        public String getState() {
            return state;
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Originator originator = new Originator();
        originator.setState("Initial State");
        System.out.println("当前状态: " + originator.getState()); // 输出: 当前状态: Initial State

        Memento memento = originator.saveStateToMemento();

        originator.setState("New State");
        System.out.println("当前状态: " + originator.getState()); // 输出: 当前状态: New State

        originator.restoreStateFromMemento(memento);
        System.out.println("恢复状态后的当前状态: " + originator.getState()); // 输出: 恢复状态后的当前状态: Initial State
    }
}
```

### 6. 模板方法模式

#### 定义
模板方法模式在方法中定义算法的框架，将某些步骤委托给子类。

#### 核心特点
- 委托某些步骤给子类。
- 在超类中定义一个算法框架。
- 允许子类覆盖某些步骤。

#### 历史
在Erich Gamma等人的著作《设计模式：可复用面向对象软件的基础》一书中介绍。

#### 使用场景
- 在需要定义算法的基本步骤但允许自定义某些步骤的系统中使用。

#### 基本用法
在超类中定义一个模板方法，实现模板方法中的步骤，允许子类覆盖某些步骤。

```java
public abstract class TemplateMethod {
    public final void templateMethod() {
        step1();
        step2();
        step3();
    }

    protected abstract void step1();
    protected abstract void step2();
    protected abstract void step3();

    public void anotherOperation() {
        System.out.println("Another operation");
    }
}

public class ConcreteClass extends TemplateMethod {
    @Override
    protected void step1() {
        System.out.println("执行步骤1");
    }

    @Override
    protected void step2() {
        System.out.println("执行步骤2");
    }

    @Override
    protected void step3() {
        System.out.println("执行步骤3");
    }
}

public class Main {
    public static void main(String[] args) {
        TemplateMethod templateMethod = new ConcreteClass();
        templateMethod.templateMethod(); // 输出: 执行步骤1
                                         //        执行步骤2
                                         //        执行步骤3
    }
}
```

## 结论

行为设计模式在软件开发中是必不可少的，用于解决常见设计问题并提高代码的灵活性和可维护性。通过使用这些模式，开发人员可以创建更模块化和适应性更强的系统。

## 进一步阅读

- [设计模式：可复用面向对象软件的基础](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [行为设计模式](https://refactoring.guru/design-patterns/behavioral-patterns)

---