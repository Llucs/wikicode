---
title: Patrones de Diseño Comportamental
description: Se centran en las interacciones entre objetos y la comunicación entre ellos, incluyendo patrones como Observer y Strategy.
created: 2026-06-28
tags:
  - Patrones de Diseño
  - Ingeniería de Software
  - Programación Orientada a Objetos
status: borrador
---

# Patrones de Diseño Comportamental

Los patrones de diseño comportamental son una categoría de patrones de diseño de software que se centran en algoritmos y la comunicación entre objetos. Estos patrones se centran en las interacciones entre objetos y cómo se comunican para lograr un cierto comportamiento. Ayudan a gestionar flujos de control complejos y simplifican la comunicación entre objetos.

## Resumen

Los patrones de diseño comportamental se preocupan por las interacciones y responsabilidades de los objetos. Estos patrones ayudan a gestionar las interacciones y responsabilidades en un sistema, lo que facilita el mantenimiento y la extensión. Promueven la reutilización del código al encapsular el comportamiento en clases separadas.

## Claves Patrones de Diseño Comportamental

### 1. Patrón Strategy

#### Definición
El patrón Strategy define una familia de algoritmos, encapsula cada uno y los hace intercambiables.

#### Características Principales
- Encapsula una familia de algoritmos.
- Permite seleccionar algoritmos en tiempo de ejecución.
- Proporciona una interfaz para los algoritmos pero mantiene ocultos sus detalles de implementación.

#### Historia
Introducido en el libro "Design Patterns: Elements of Reusable Object-Oriented Software" por Erich Gamma et al., publicado en 1994.

#### Casos de Uso
- Utilizado en sistemas donde se necesitan cambiar o seleccionar algoritmos dinámicamente, como algoritmos de ordenación, puertas de pago y diferentes niveles de registro.

#### Uso Básico
Define una interfaz para un algoritmo, implementa diferentes algoritmos y encapsula cada uno en una clase separada. La clase contexto usa la interfaz para interactuar con los algoritmos.

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

### 2. Patrón Observer

#### Definición
El patrón Observer define una dependencia entre objetos de manera que cuando un objeto cambia de estado, todos sus observadores son notificados y actualizados automáticamente.

#### Características Principales
- El sujeto mantiene una lista de observadores.
- Permite un mecanismo de suscripción y desuscripción.
- Notifica a los observadores cuando cambia su estado.

#### Historia
También introducido en el libro "Design Patterns: Elements of Reusable Object-Oriented Software".

#### Casos de Uso
- Utilizado en marcos de interfaz gráfica de usuario, manejo de eventos y cualquier sistema donde un cambio en un objeto debe provocar un cambio en otro.

#### Uso Básico
Define una interfaz `Observer`, crea clases observador y implementa un `Sujeto` que mantiene una lista de observadores y los notifica de cambios.

```java
public interface Observer {
    void update(String message);
}

public class ConcreteObserver implements Observer {
    public void update(String message) {
        System.out.println("Observer received message: " + message);
    }
}

public class Sujeto {
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
        Sujeto sujeto = new Sujeto();
        Observer observer1 = new ConcreteObserver();
        Observer observer2 = new ConcreteObserver();

        sujeto.addObserver(observer1);
        sujeto.addObserver(observer2);

        sujeto.notifyObservers("Hello, Observer Pattern!"); // Output: Observer received message: Hello, Observer Pattern!
                                                      //        Observer received message: Hello, Observer Pattern!
    }
}
```

### 3. Patrón Command

#### Definición
El patrón Command transforma una solicitud en un objeto independiente que contiene toda la información sobre la solicitud.

#### Características Principales
- Encapsula una solicitud como objeto.
- Permite parametrizar métodos con diferentes solicitudes, retrasar o programar la ejecución de solicitudes.
- Permite operaciones deshacibles.

#### Historia
Introducido en el libro "Design Patterns: Elements of Reusable Object-Oriented Software".

#### Casos de Uso
- Utilizado en interfaces gráficas de usuario, operaciones de deshacer / rehacer y cualquier sistema donde las solicitudes necesiten ser parametrizadas.

#### Uso Básico
Define una interfaz `Command`, crea clases concreta de comandos y ejecuta comandos mediante un objeto `Command`.

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

### 4. Patrón Visitor

#### Definición
El patrón Visitor representa una operación para ser realizada sobre los elementos de una estructura de objetos.

#### Características Principales
- Encapsula una operación sobre los elementos de una estructura de objetos.
- Permite agregar nuevas operaciones sin cambiar las clases de los elementos.

#### Historia
Introducido en el libro "Design Patterns: Elements of Reusable Object-Oriented Software".

#### Casos de Uso
- Utilizado en sistemas que necesitan agregar nuevas operaciones a una jerarquía de clases sin cambiar las existentes, como en recorridos de AST.

#### Uso Básico
Define una interfaz `Visitor`, implementa la operación en las clases visitante y aplica los visitantes a los objetos en la estructura.

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

### 5. Patrón Memento

#### Definición
El patrón Memento captura el estado interno de un objeto sin violar la encapsulación, luego permite que el objeto recupere ese estado anterior.

#### Características Principales
- Encapsula el estado interno de un objeto.
- Proporciona un mecanismo para restaurar ese estado.

#### Historia
Introducido en el libro "Design Patterns: Elements of Reusable Object-Oriented Software".

#### Casos de Uso
- Utilizado en sistemas que necesitan deshacer cambios, como en editores de texto o juegos.

#### Uso Básico
Define una clase `Memento` para almacenar el estado, una clase `Caretaker` para gestionar los mementos y una clase `Originator` que mantiene el estado y puede restaurarlo desde los mementos.

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
        originator.setState("Estado inicial");
        System.out.println("Estado actual: " + originator.getState()); // Output: Estado actual: Estado inicial

        Memento memento = originator.saveStateToMemento();

        originator.setState("Estado nuevo");
        System.out.println("Estado actual: " + originator.getState()); // Output: Estado actual: Estado nuevo

        originator.restoreStateFromMemento(memento);
        System.out.println("Estado actual después de la restauración: " + originator.getState()); // Output: Estado actual después de la restauración: Estado inicial
    }
}
```

### 6. Patrón Template Method

#### Definición
El patrón Template Method define el esqueleto de un algoritmo en un método, delegando algunos pasos a las subclases.

#### Características Principales
- Delega algunos pasos a las subclases.
- Define un esqueleto de algoritmo en una superclase.
- Permite que las subclases sobrescriban ciertos pasos.

#### Historia
Introducido en el libro "Design Patterns: Elements of Reusable Object-Oriented Software".

#### Casos de Uso
- Utilizado en sistemas que necesitan definir los pasos básicos de un algoritmo, pero permiten la personalización de ciertos pasos.

#### Uso Básico
Define un método template en una superclase, implementa pasos en el método template y permite que las subclases sobrescriban ciertos pasos.

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

    public void otraOperacion() {
        System.out.println("Otra operación");
    }
}

public class ConcreteClass extends TemplateMethod {
    @Override
    protected void step1() {
        System.out.println("Ejecutando paso 1");
    }

    @Override
    protected void step2() {
        System.out.println("Ejecutando paso 2");
    }

    @Override
    protected void step3() {
        System.out.println("Ejecutando paso 3");
    }
}

public class Main {
    public static void main(String[] args) {
        TemplateMethod templateMethod = new ConcreteClass();
        templateMethod.templateMethod(); // Output: Ejecutando paso 1
                                         //        Ejecutando paso 2
                                         //        Ejecutando paso 3
    }
}
```

## Conclusión

Los patrones de diseño comportamental son esenciales en el desarrollo de software para resolver problemas de diseño comunes e mejorar la flexibilidad y mantenibilidad del código. Al utilizar estos patrones, los desarrolladores pueden crear sistemas más modulares y adaptativos.

## Lectura Adicional

- [Design Patterns: Elements of Reusable Object-Oriented Software](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Patrones de Diseño Comportamental](https://refactoring.guru/design-patterns/behavioral-patterns)

---