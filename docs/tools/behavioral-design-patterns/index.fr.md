---
title: Modèles de conception comportementaux
description: Concentre sur les interactions entre les objets et la communication, y compris des modèles comme Observateur et Stratégie.
created: 2026-06-28
tags:
  - Modèles de conception
  - Informatique logicielle
  - Programmation orientée objet
status: brouillon
---

# Modèles de conception comportementaux

Les modèles de conception comportementaux sont une catégorie de modèles de conception de logiciel qui traitent avec les algorithmes et la communication entre les objets. Ces modèles se concentrent sur les interactions entre les objets et la manière dont ils communiquent pour atteindre un certain comportement. Ils aident à gérer les flux de contrôle complexes et simplifient la communication entre les objets.

## Vue d'ensemble

Les modèles de conception comportementaux s'occupent des interactions et des responsabilités des objets. Ces modèles aident à gérer les interactions et les responsabilités des objets dans un système, ce qui rend le maintien et l'extension du système plus facile. Ils favorisent la réutilisabilité du code en encapsulant le comportement dans des classes distinctes.

## Modèles de conception comportementaux clés

### 1. Modèle de stratégie

#### Définition
Le modèle de stratégie définit une famille d'algorithmes, les encapsule et les rend interchangeable.

#### Caractéristiques clés
- Encapsule une famille d'algorithmes.
- Permet la sélection d'algorithmes en temps de exécution.
- fournit une interface pour les algorithmes tout en masquant les détails de leur implémentation.

#### Histoire
Introduit dans le livre "Modèles de conception : éléments de logiciels réutilisables" par Erich Gamma et al., publié en 1994.

#### Cas d'utilisation
- Utilisé dans les systèmes où les algorithmes doivent être changés ou sélectionnés dynamiquement, tels que les algorithmes de tri, les portails de paiement et différents niveaux de journalisation.

#### Utilisation de base
Définissez une interface pour un algorithme, implémentez différents algorithmes et encapsulez chaque un dans une classe distincte. La classe contexte utilise l'interface pour interagir avec les algorithmes.

```java
public interface Strategy {
    void algorithmInterface();
}

public class ConcreteStrategyA implements Strategy {
    public void algorithmInterface() {
        System.out.println("Exécuter la stratégie A");
    }
}

public class ConcreteStrategyB implements Strategy {
    public void algorithmInterface() {
        System.out.println("Exécuter la stratégie B");
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
        context.executeAlgorithm(); // Output: Exécuter la stratégie A

        context.setStrategy(new ConcreteStrategyB());
        context.executeAlgorithm(); // Output: Exécuter la stratégie B
    }
}
```

### 2. Modèle de observateur

#### Définition
Le modèle de observateur définit une dépendance entre les objets de sorte que lorsque l'un d'eux change d'état, tous ses observateurs sont notifiés et mis à jour automatiquement.

#### Caractéristiques clés
- Le sujet maintient une liste d'observateurs.
- Permet une mécanique d'abonnement et d'annulation d'abonnement.
- Notifie les observateurs lorsque son état change.

#### Histoire
Introduit également dans le livre "Modèles de conception : éléments de logiciels réutilisables".

#### Cas d'utilisation
- Utilisé dans les frameworks de interface graphique, les gestionnaires d'événements et tout système où un changement dans un objet devrait provoquer un changement dans un autre.

#### Utilisation de base
Définissez une interface `Observateur`, créez des classes observateurs et implémentez un `Sujet` qui maintient une liste d'observateurs et les informe des changements.

```java
public interface Observer {
    void update(String message);
}

public class ConcreteObserver implements Observer {
    public void update(String message) {
        System.out.println("Observateur a reçu le message : " + message);
    }
}

public class Sujet {
    private List<Observer> observateurs = new ArrayList<>();

    public void addObserver(Observer observateur) {
        observateurs.add(observateur);
    }

    public void removeObserver(Observer observateur) {
        observateurs.remove(observateur);
    }

    public void notifyObservers(String message) {
        for (Observer observateur : observateurs) {
            observateur.update(message);
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Sujet sujet = new Sujet();
        Observer observateur1 = new ConcreteObserver();
        Observer observateur2 = new ConcreteObserver();

        sujet.addObserver(observateur1);
        sujet.addObserver(observateur2);

        sujet.notifyObservers("Bonjour, Modèle de observateur!"); // Output: Observateur a reçu le message : Bonjour, Modèle de observateur!
                                                                 //        Observateur a reçu le message : Bonjour, Modèle de observateur!
    }
}
```

### 3. Modèle de commande

#### Définition
Le modèle de commande transforme une demande en un objet indépendant qui contient toutes les informations sur la demande.

#### Caractéristiques clés
- Encapsule une demande en un objet.
- Permet de paramétrer les méthodes avec des demandes différentes, de différer ou de retarder l'exécution des demandes.
- Permet les opérations réversibles.

#### Histoire
Introduit dans le livre "Modèles de conception : éléments de logiciels réutilisables".

#### Cas d'utilisation
- Utilisé dans les interfaces graphiques, les opérations undo/redo, et tout système où les demandes doivent être paramétrées.

#### Utilisation de base
Définissez une interface `Commande`, créez des classes de commande concrètes et exécutez les commandes via une objet `Commande`.

```java
public interface Commande {
    void execute();
}

public class ConcreteCommande implements Commande {
    private Recepteur recepteur;

    public ConcreteCommande(Recepteur recepteur) {
        this.recepteur = recepteur;
    }

    public void execute() {
        recepteur.action();
    }
}

public class Recepteur {
    public void action() {
        System.out.println("Exécuter l'action du recepteur");
    }
}

public class CommandeExécutrice {
    private Commande commande;

    public void setCommande(Commande commande) {
        this.commande = commande;
    }

    public void executeCommande() {
        commande.execute();
    }
}

public class Main {
    public static void main(String[] args) {
        Recepteur recepteur = new Recepteur();
        Commande commande = new ConcreteCommande(recepteur);
        CommandeExécutrice commandeeXécutrice = new CommandeExécutrice();
        commandeeXécutrice.setCommande(commande);
        commandeeXécutrice.executeCommande(); // Output: Exécuter l'action du recepteur
    }
}
```

### 4. Modèle de visiteur

#### Définition
Le modèle de visiteur représente une opération à effectuer sur les éléments d'une structure d'objet.

#### Caractéristiques clés
- Encapsule une opération sur les éléments d'une structure d'objet.
- Permet d'ajouter de nouvelles opérations sans modifier les classes des éléments.

#### Histoire
Introduit dans le livre "Modèles de conception : éléments de logiciels réutilisables".

#### Cas d'utilisation
- Utilisé dans les systèmes qui ont besoin d'ajouter de nouvelles opérations à une hiérarchie de classes sans modifier les classes existantes, comme dans les parcours d'AST.

#### Utilisation de base
Définissez une interface `Visiteur`, implémentez l'opération dans les classes visiteur, et appliquez les visiteurs aux objets dans la structure.

```java
public interface Visiteur {
    void visitConcreteElementA(ConcreteElementA element);
    void visitConcreteElementB(ConcreteElementB element);
}

public class ConcreteElementA {
    public void accept(Visiteur visiteur) {
        visiteur.visitConcreteElementA(this);
    }
}

public class ConcreteElementB {
    public void accept(Visiteur visiteur) {
        visiteur.visitConcreteElementB(this);
    }
}

public class VisiteurConcrète implements Visiteur {
    public void visitConcreteElementA(ConcreteElementA element) {
        System.out.println("Visiter le ConcreteElementA");
    }

    public void visitConcreteElementB(ConcreteElementB element) {
        System.out.println("Visiter le ConcreteElementB");
    }
}

public class Main {
    public static void main(String[] args) {
        ConcreteElementA elementA = new ConcreteElementA();
        ConcreteElementB elementB = new ConcreteElementB();
        Visiteur visiteur = new VisiteurConcrète();

        elementA.accept(visiteur); // Output: Visiter le ConcreteElementA
        elementB.accept(visiteur); // Output: Visiter le ConcreteElementB
    }
}
```

### 5. Modèle de mémoire

#### Définition
Le modèle de mémoire capture l'état interne d'un objet sans violate l'encapsulation, puis permet à l'objet de restaurer cet état précédent.

#### Caractéristiques clés
- Encapsule l'état interne d'un objet.
- fournit un mécanisme pour restaurer cet état.

#### Histoire
Introduit dans le livre "Modèles de conception : éléments de logiciels réutilisables".

#### Cas d'utilisation
- Utilisé dans les systèmes qui ont besoin de révoquer des changements, tels que dans des éditeurs de texte ou des jeux.

#### Utilisation de base
Définissez une classe `Memento` pour stocker l'état, une classe `Gardien` pour gérer les mémoires, et une classe `Originateur` qui maintient l'état et peut le restaurer à partir de mémoires.

```java
public class Originateur {
    private String etat;

    public void setEtat(String etat) {
        this.etat = etat;
    }

    public Memento sauvegarderEtatAuMemento() {
        return new Memento(etat);
    }

    public void restaurerEtatAuMemento(Memento memento) {
        this.etat = memento.getEtat();
    }

    public String getEtat() {
        return etat;
    }

    public class Memento {
        private String etat;

        public Memento(String etat) {
            this.etat = etat;
        }

        public String getEtat() {
            return etat;
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Originateur originateur = new Originateur();
        originateur.setEtat("État initial");
        System.out.println("État courant : " + originateur.getEtat()); // Output: État courant : État initial

        Memento memento = originateur.sauvegarderEtatAuMemento();

        originateur.setEtat("État nouveau");
        System.out.println("État courant : " + originateur.getEtat()); // Output: État courant : État nouveau

        originateur.restaurerEtatAuMemento(memento);
        System.out.println("État courant après la restauration : " + originateur.getEtat()); // Output: État courant après la restauration : État initial
    }
}
```

### 6. Modèle de méthode templet

#### Définition
Le modèle de méthode templet définit le squelette d'un algorithme dans une méthode, déléguant certaines étapes aux sous-classes.

#### Caractéristiques clés
- Délegue certaines étapes aux sous-classes.
- Définit un squelette d'algorithmes dans une classe mère.
- Permet aux sous-classes d'overrides certaines étapes.

#### Histoire
Introduit dans le livre "Modèles de conception : éléments de logiciels réutilisables".

#### Cas d'utilisation
- Utilisé dans les systèmes qui ont besoin de définir les étapes d'un algorithme, mais permettent la personnalisation de certaines étapes.

#### Utilisation de base
Définissez une méthode templet dans une classe mère, implémentez les étapes dans la méthode templet, et permettez aux sous-classes d'override certaines étapes.

```java
public abstract class MéthodeTemplet {
    public final void méthodetemplet() {
        étape1();
        étape2();
        étape3();
    }

    protected abstract void étape1();
    protected abstract void étape2();
    protected abstract void étape3();

    public void autreOpération() {
        System.out.println("Autre opération");
    }
}

public class ClasseConcrète extends MéthodeTemplet {
    @Override
    protected void étape1() {
        System.out.println("Exécuter l'étape 1");
    }

    @Override
    protected void étape2() {
        System.out.println("Exécuter l'étape 2");
    }

    @Override
    protected void étape3() {
        System.out.println("Exécuter l'étape 3");
    }
}

public class Main {
    public static void main(String[] args) {
        MéthodeTemplet méthodeTemplet = new ClasseConcrète();
        méthodeTemplet.méthodetemplet(); // Output: Exécuter l'étape 1
                                         //        Exécuter l'étape 2
                                         //        Exécuter l'étape 3
    }
}
```

## Conclusion

Les modèles de conception comportementaux sont essentiels dans le développement de logiciels pour résoudre les problèmes de conception courants et améliorer la flexibilité et la maintenabilité du code. En utilisant ces modèles, les développeurs peuvent créer des systèmes plus modulaires et adaptables.

## Lecture supplémentaire

- [Modèles de conception : éléments de logiciels réutilisables](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Modèles de conception comportementaux](https://refactoring.guru/design-patterns/behavioral-patterns)

---