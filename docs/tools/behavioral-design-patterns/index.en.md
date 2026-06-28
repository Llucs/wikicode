---
title: Behavioral Design Patterns
description: Focuses on object interactions and communication, including patterns like Observer and Strategy.
created: 2026-06-28
tags:
  - Design Patterns
  - Software Engineering
  - Object-Oriented Programming
status: draft
---

# Behavioral Design Patterns

Behavioral design patterns are a category of software design patterns that deal with algorithms and communication between objects. These patterns are focused on the interactions between objects and how they communicate to achieve a certain behavior. They help in managing complex control flows and simplify the communication between objects.

## Overview

Behavioral design patterns are concerned with the interaction and responsibility of objects. These patterns help in managing object interactions and responsibilities in a system, making it easier to maintain and extend. They promote code reusability by encapsulating behavior in separate classes.

## Key Behavioral Design Patterns

### 1. Strategy Pattern

#### Definition
The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable.

#### Key Features
- Encapsulates a family of algorithms.
- Allows the selection of algorithms at runtime.
- Provides an interface for algorithms but keeps their implementation details hidden.

#### History
Introduced in the book "Design Patterns: Elements of Reusable Object-Oriented Software" by Erich Gamma et al., published in 1994.

#### Use Cases
- Used in systems where algorithms need to be changed or selected dynamically, such as sorting algorithms, payment gateways, and different logging levels.

#### Basic Usage
Define an interface for an algorithm, implement different algorithms, and encapsulate each in a separate class. The context class uses the interface to interact with the algorithms.

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
        context.executeAlgorithm(); // Output: Executing Strategy A

        context.setStrategy(new ConcreteStrategyB());
        context.executeAlgorithm(); // Output: Executing Strategy B
    }
}
```

### 2. Observer Pattern

#### Definition
The Observer pattern defines a dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

#### Key Features
- Subject maintains a list of observers.
- Allows for a subscription and unsubscription mechanism.
- Notifies observers when its state changes.

#### History
Also introduced in the book "Design Patterns: Elements of Reusable Object-Oriented Software".

#### Use Cases
- Used in GUI frameworks, event handling, and any system where changes in one object should trigger changes in another.

#### Basic Usage
Define an `Observer` interface, create observer classes, and implement a `Subject` that maintains a list of observers and notifies them of changes.

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

        subject.notifyObservers("Hello, Observer Pattern!"); // Output: Observer received message: Hello, Observer Pattern!
                                                      //        Observer received message: Hello, Observer Pattern!
    }
}
```

### 3. Command Pattern

#### Definition
The Command pattern turns a request into a stand-alone object that contains all information about the request.

#### Key Features
- Encapsulates a request as an object.
- Allows for parameterizing methods with different requests, delay or queue the execution of requests.
- Allows for undoable operations.

#### History
Introduced in the book "Design Patterns: Elements of Reusable Object-Oriented Software".

#### Use Cases
- Used in GUIs, undo/redo operations, and any system where requests need to be parameterized.

#### Basic Usage
Define a `Command` interface, create concrete command classes, and execute commands via a `Command` object.

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
        invoker.executeCommand(); // Output: Executing receiver action
    }
}
```

### 4. Visitor Pattern

#### Definition
The Visitor pattern represents an operation to be performed on the elements of an object structure.

#### Key Features
- Encapsulates an operation on the elements of an object structure.
- Allows for adding new operations without changing the classes of the elements.

#### History
Introduced in the book "Design Patterns: Elements of Reusable Object-Oriented Software".

#### Use Cases
- Used in systems that need to add new operations to a class hierarchy without changing existing classes, such as in AST traversals.

#### Basic Usage
Define a `Visitor` interface, implement the operation in visitor classes, and apply the visitors to objects in the structure.

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

        elementA.accept(visitor); // Output: Visiting ConcreteElementA
        elementB.accept(visitor); // Output: Visiting ConcreteElementB
    }
}
```

### 5. Memento Pattern

#### Definition
The Memento pattern captures the internal state of an object without violating encapsulation, then lets the object restore that previous state.

#### Key Features
- Encapsulates the internal state of an object.
- Provides a mechanism to restore that state.

#### History
Introduced in the book "Design Patterns: Elements of Reusable Object-Oriented Software".

#### Use Cases
- Used in systems that need to undo changes, such as in text editors or games.

#### Basic Usage
Define a `Memento` class to store state, a `Caretaker` class to manage mementos, and a `Originator` class that maintains state and can restore it from mementos.

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
        System.out.println("Current state: " + originator.getState()); // Output: Current state: Initial State

        Memento memento = originator.saveStateToMemento();

        originator.setState("New State");
        System.out.println("Current state: " + originator.getState()); // Output: Current state: New State

        originator.restoreStateFromMemento(memento);
        System.out.println("Current state after restore: " + originator.getState()); // Output: Current state after restore: Initial State
    }
}
```

### 6. Template Method Pattern

#### Definition
The Template Method pattern defines the skeleton of an algorithm in a method, deferring some steps to subclasses.

#### Key Features
- Delegates some steps to subclasses.
- Defines a skeleton algorithm in a superclass.
- Allows subclasses to override certain steps.

#### History
Introduced in the book "Design Patterns: Elements of Reusable Object-Oriented Software".

#### Use Cases
- Used in systems that need to define the basic steps of an algorithm, but allow for customization of certain steps.

#### Basic Usage
Define a template method in a superclass, implement steps in the template method, and allow subclasses to override certain steps.

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
        System.out.println("Executing step 1");
    }

    @Override
    protected void step2() {
        System.out.println("Executing step 2");
    }

    @Override
    protected void step3() {
        System.out.println("Executing step 3");
    }
}

public class Main {
    public static void main(String[] args) {
        TemplateMethod templateMethod = new ConcreteClass();
        templateMethod.templateMethod(); // Output: Executing step 1
                                         //        Executing step 2
                                         //        Executing step 3
    }
}
```

## Conclusion

Behavioral design patterns are essential in software development to solve common design problems and improve the flexibility and maintainability of code. By using these patterns, developers can create more modular and adaptable systems.

## Further Reading

- [Design Patterns: Elements of Reusable Object-Oriented Software](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Behavioral Design Patterns](https://refactoring.guru/design-patterns/behavioral-patterns)

---