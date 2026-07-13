---
title: Séparation des commandes et des requêtes (CQRS)
description: Un patron de conception utilisé dans l'architecture logicielle pour séparer les commandes (opérations en écriture) des requêtes (opérations en lecture).
created: 2026-07-13
tags:
  - architecture logicielle
  - patrons de conception
  - CQRS
  - séparation des commandes et des requêtes
status: brouillon
---

# Séparation des commandes et des requêtes (CQRS)

La Séparation des commandes et des requêtes (CQRS) est un patron de conception utilisé dans l'architecture logicielle pour séparer les commandes (opérations en écriture) des requêtes (opérations en lecture). Cette séparation peut conduire à des applications plus maintenables et plus échelonnables, en particulier dans des scénarios complexes et réels.

## Qu'est-ce que le CQRS ?

Le CQRS est un patron de conception qui met l'accent sur la séparation des actions qui demandent des informations (requêtes) de celles qui modifient l'état (commandes). Cette séparation peut conduire à des applications plus maintenables et plus échelonnables, en particulier dans les systèmes à haut volume de transactions ou dotés de logique d'affaires complexe.

## Caractéristiques clés

1. **Gestion des commandes** : Les commandes sont utilisées pour modifier l'état du système. Elles sont généralement émises par des systèmes externes ou des utilisateurs et servent à exécuter des actions, telles que la création, la mise à jour ou la suppression de données.
2. **Gestion des requêtes** : Les requêtes sont utilisées pour récupérer des informations du système. Elles sont des opérations en lecture seule qui ne modifient pas l'état du système. Les requêtes peuvent être optimisées pour des charges en lecture lourdes, ce qui est souvent plus efficace que d'avoir une seule base de données qui gère à la fois les lectures et les écritures.
3. **Séparation des préoccupations** : Le CQRS aide à séparer les préoccupations des opérations d'écriture et de lecture, rendant le système plus maintenable et échelonnable.
4. **Évolutivité par événements** : Souvent utilisé en conjonction avec le CQRS, où les changements dans le système sont enregistrés sous forme d'une séquence d'événements. Ces événements peuvent être utilisés pour reconstruire l'état actuel du système ou pour déclencher des commandes.

## Histoire

Le CQRS n'était pas une nouvelle idée lorsqu'il a été popularisé pour la première fois. Le concept de séparation des commandes et des requêtes a existé depuis longtemps, mais il n'a été appliqué largement que lorsque Greg Young et Udi Dahan l'ont promu dans les premières années 2010. Ils ont présenté leurs idées à diverses conférences et ateliers, ce qui a conduit à une adoption plus large du patron.

## Cas d'utilisation

1. **Traitement en ligne des transactions (OLTP)** : Le CQRS est particulièrement utile dans les systèmes nécessitant un haut volume d'écritures, tels que les plateformes d'e-commerce, les systèmes financiers ou les applications de jeu.
2. **Data Warehouse** : Le CQRS peut aider à construire des data warehouses en séparant les données transactionnelles lourdes en écriture des données analytiques lourdes en lecture.
3. **Logique d'affaires complexe** : Les systèmes dotés de logique d'affaires complexe nécessitant des mises à jour et des modifications fréquentes peuvent bénéficier de la séparation des commandes et des requêtes.

## Installation

Le CQRS n'est pas un framework autonome, mais un patron de conception. Par conséquent, il n'est pas fourni avec une installation directe. Cependant, vous pouvez implémenter CQRS dans votre application en suivant ces étapes générales :

1. **Définir des commandes et des requêtes** : Créez un ensemble de classes de commandes pour gérer les opérations en écriture et des classes de requêtes pour gérer les opérations en lecture.
2. **Implémenter des gestionnaires de commandes** : Écrivez des gestionnaires pour traiter les commandes et effectuer les opérations nécessaires sur les données.
3. **Implémenter des gestionnaires de requêtes** : Écrivez des gestionnaires pour traiter les requêtes et retourner les données requises.
4. **Évolutivité par événements (facultatif)** : Implémentez l'évolutivité par événements pour capturer les changements dans le système et utiliser ces événements pour mettre à jour le modèle de lecture.

## Utilisation de base

### Gestion des commandes

```csharp
public class ServiceCommande {
    private readonly BusCommande _busCommande;

    public ServiceCommande(BusCommande busCommande) {
        _busCommande = busCommande;
    }

    public void PasserUneCommande(Commande commande) {
        _busCommande.Envoyer(new CommandePlaceeCommande(commande));
    }
}
```

### Gestion des requêtes

```csharp
public class ServiceRequeteCommande {
    private readonly BusRequete _busRequete;

    public ServiceRequeteCommande(BusRequete busRequete) {
        _busRequete = busRequete;
    }

    public Commande ObtenirCommandeParId(Guid idCommande) {
        return _busRequete.Envoyer(new RequeteObtenirCommandeParId(idCommande));
    }
}
```

### Évolutivité par événements

```csharp
public class AggrégatCommande {
    private readonly RepositoryEvenement _repositoryEvenement;

    public AggrégatCommande(RepositoryEvenement repositoryEvenement) {
        _repositoryEvenement = repositoryEvenement;
    }

    public void AppliquerCommande(CommandePlaceeCommande commande) {
        // Appliquer la commande et enregistrer les événements
        _repositoryEvenement.EnregistrerNouvelEvenement(new EvenementCommandePlacee(commande.IdCommande, commande.IdClient));
    }
}
```

## Conclusion

Le CQRS est un patron de conception puissant qui peut considérablement améliorer la scalabilité et la maintenabilité des applications complexes. En séparant les commandes et les requêtes, les développeurs peuvent optimiser leurs systèmes pour des opérations en écriture et en lecture, conduisant à des applications plus efficaces et robustes. Cependant, une conception et une implémentation soignées sont nécessaires pour être efficaces, et il ne convient pas à toutes les types d'applications.