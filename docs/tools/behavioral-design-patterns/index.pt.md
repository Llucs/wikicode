---
title: Patrões de Design Comportamentais
description: Focusa-se nas interações entre objetos e comunicação, incluindo padrões como Observer e Strategy.
created: 2026-06-28
tags:
  - Patrões de Design
  - Engenharia de Software
  - Programação Orientada a Objeto
status: rascunho
---

# Patrões de Design Comportamentais

Patrões de design comportamentais são uma categoria de padrões de design de software que lidam com algoritmos e comunicação entre objetos. Esses padrões se concentraram nas interações entre objetos e na comunicação para alcançar um determinado comportamento. Eles ajudam a gerenciar fluxos de controle complexos e simplificar a comunicação entre objetos.

## Visão Geral

Patrões de design comportamentais se preocupam com as interações e responsabilidades dos objetos. Esses padrões ajudam a gerenciar as interações e responsabilidades de um sistema, tornando-o mais fácil de manter e estender. Promovem a reusabilidade do código ao encapsular o comportamento em classes separadas.

## Principais Patrões de Design Comportamentais

### 1. Padrão Strategy

#### Definição
O Padrão Strategy define uma família de algoritmos, encapsula cada um e torna-os intercambiáveis.

#### Características Chave
- Encapsula uma família de algoritmos.
- Permite a seleção de algoritmos em tempo de execução.
- Fornece uma interface para os algoritmos, mantendo seus detalhes de implementação ocultos.

#### Histórico
Introduzido no livro "Design Patterns: Elements of Reusable Object-Oriented Software" por Erich Gamma et al., publicado em 1994.

#### Casos de Uso
- Usado em sistemas onde os algoritmos precisam ser alterados ou selecionados dinamicamente, como algoritmos de ordenação, portais de pagamento e diferentes níveis de logging.

#### Uso Básico
Defina uma interface para um algoritmo, implemente diferentes algoritmos e encapsule cada um em uma classe separada. A classe Context usa a interface para interagir com os algoritmos.

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

### 2. Padrão Observer

#### Definição
O Padrão Observer define uma dependência entre objetos de modo que, quando um objeto muda de estado, todos seus dependentes são notificados e atualizados automaticamente.

#### Características Chave
- O Sujeito mantém uma lista de observadores.
- Permite a mecanismos de assinatura e desassinatura.
- Notifica observadores quando seu estado muda.

#### Histórico
Também introduzido no livro "Design Patterns: Elements of Reusable Object-Oriented Software".

#### Casos de Uso
- Usado em frameworks GUI, tratamento de eventos e qualquer sistema onde mudanças em um objeto devem disparar mudanças em outro.

#### Uso Básico
Defina uma interface `Observer`, crie classes de observador e implemente uma classe `Sujeito` que mantém uma lista de observadores e notifica-os de mudanças.

```java
public interface Observer {
    void update(String message);
}

public class ConcreteObserver implements Observer {
    public void update(String message) {
        System.out.println("Observer received message: " + message);
    }
}

public class Sujeito {
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
        Sujeito subject = new Sujeito();
        Observer observer1 = new ConcreteObserver();
        Observer observer2 = new ConcreteObserver();

        subject.addObserver(observer1);
        subject.addObserver(observer2);

        subject.notifyObservers("Hello, Observer Pattern!"); // Output: Observer received message: Hello, Observer Pattern!
                                                              //        Observer received message: Hello, Observer Pattern!
    }
}
```

### 3. Padrão Command

#### Definição
O Padrão Command transforma uma solicitação em um objeto isolado que contém todas as informações sobre a solicitação.

#### Características Chave
- Encapsula uma solicitação como um objeto.
- Permite a parametrização de métodos com diferentes solicitações, atrasar ou colocar em fila a execução de solicitações.
- Permite operações reaisizáveis.

#### Histórico
Introduzido no livro "Design Patterns: Elements of Reusable Object-Oriented Software".

#### Casos de Uso
- Usado em interfaces gráficas, operações de undo/redo e qualquer sistema onde solicitações precisam ser parametrizadas.

#### Uso Básico
Defina uma interface `Command`, crie classes de comando concretas e execute comandos por meio de um objeto `Command`.

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

### 4. Padrão Visitor

#### Definição
O Padrão Visitor representa uma operação a ser executada em elementos de uma estrutura de objetos.

#### Características Chave
- Encapsula uma operação em elementos de uma estrutura de objetos.
- Permite a adição de novas operações sem alterar as classes de elementos existentes.

#### Histórico
Introduzido no livro "Design Patterns: Elements of Reusable Object-Oriented Software".

#### Casos de Uso
- Usado em sistemas que precisam adicionar novas operações a uma hierarquia de classes sem alterar as classes existentes, como em varreduras de árvore de expressão sintática.

#### Uso Básico
Defina uma interface `Visitor`, implemente a operação em classes de visitante e aplique os visitantes a objetos na estrutura.

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

### 5. Padrão Memento

#### Definição
O Padrão Memento captura o estado interno de um objeto sem violar a encapsulamento, permitindo que o objeto recupere esse estado anterior.

#### Características Chave
- Encapsula o estado interno de um objeto.
- Fornece um mecanismo para restaurar esse estado.

#### Histórico
Introduzido no livro "Design Patterns: Elements of Reusable Object-Oriented Software".

#### Casos de Uso
- Usado em sistemas que precisam desfazer alterações, como em editores de texto ou jogos.

#### Uso Básico
Defina uma classe `Memento` para armazenar o estado, uma classe `Caretaker` para gerenciar os mementos e uma classe `Originator` que mantém o estado e pode restaurá-lo a partir de mementos.

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

### 6. Padrão Template Method

#### Definição
O Padrão Template Method define o esqueleto de um algoritmo em um método, delegando alguns passos para subclasses.

#### Características Chave
- Delega alguns passos para subclasses.
- Define um esqueleto de algoritmo em uma superclasse.
- Permite que subclasses sobrescrevam alguns passos.

#### Histórico
Introduzido no livro "Design Patterns: Elements of Reusable Object-Oriented Software".

#### Casos de Uso
- Usado em sistemas que precisam definir os passos básicos de um algoritmo, mas permitem a personalização de alguns passos.

#### Uso Básico
Defina um método Template Method em uma superclasse, implemente passos em um método Template Method e permita que as subclasses sobrescrevam certos passos.

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

## Conclusão

Os patrões de design comportamentais são essenciais no desenvolvimento de software para resolver problemas de design comuns e melhorar a flexibilidade e a manutenibilidade do código. Ao usar esses padrões, os desenvolvedores podem criar sistemas mais modulares e adaptáveis.

## Leitura Recomendada

- [Design Patterns: Elements of Reusable Object-Oriented Software](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Patrões de Design Comportamentais](https://refactoring.guru/design-patterns/behavioral-patterns)

---