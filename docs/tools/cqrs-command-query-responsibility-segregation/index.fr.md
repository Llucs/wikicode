---
title: CQRS (Command Query Responsibility Segregation)
description: Un modèle architectural qui sépare les opérations de lecture et d'écriture en modèles distincts pour optimiser les performances, l'évolutivité et la maintenabilité.
created: 2026-06-19
tags:
  - architecture
  - design-pattern
  - cqrs
  - domain-driven-design
  - event-sourcing
  - microservices
status: draft
---

# CQRS (Command Query Responsibility Segregation)

CQRS (Command Query Responsibility Segregation) est un modèle architectural qui sépare les responsabilités de lecture des données (requêtes) de la mise à jour des données (commandes). En utilisant des modèles distincts et souvent des magasins de données séparés pour les lectures et les écritures, CQRS permet une optimisation indépendante de chaque côté, améliorant ainsi l'évolutivité, les performances et la sécurité dans les systèmes complexes.

## Définition et historique

Le terme CQRS a été popularisé par Greg Young et Udi Dahan à la fin des années 2000 au sein des communautés Domain-Driven Design (DDD). Son fondement conceptuel réside dans le principe **Command-Query Separation (CQS)** de Bertrand Meyer, qui stipule qu'une méthode doit être soit une *commande* (effectuer une action) soit une *requête* (retourner des données), mais pas les deux. CQRS élève cette idée du niveau de la méthode au niveau architectural et au niveau du magasin de données.

Dans une architecture CRUD traditionnelle, un modèle unique gère les lectures, les écritures, les mises à jour et les suppressions. CQRS divise explicitement cela en deux côtés distincts :

- **Modèle d'écriture (Commandes) :** Gère les opérations de changement d'état. Les commandes sont impératives, produisent des effets secondaires et appliquent les invariants métier (généralement via des Agrégats en DDD).
- **Modèle de lecture (Requêtes) :** Gère la récupération des données. Les requêtes sont déclaratives, sans effet secondaire, et optimisées pour des contrats d'interface utilisateur ou d'API spécifiques. Elles sont souvent dénormalisées, pré-jointes ou stockées dans différentes bases de données (e.g., Elasticsearch pour la recherche, Redis pour le cache).

CQRS est fréquemment combiné avec **Event Sourcing**, où le côté écriture produit un flux d'événements métier qui sont consommés de manière asynchrone pour construire et mettre à jour les modèles de lecture.

## Pourquoi utiliser CQRS ?

| Avantage          | Description |
|------------------|-------------|
| **Évolutivité**  | Les réplicas de lecture peuvent être mis à l'échelle indépendamment des nœuds d'écriture. Différentes infrastructures (e.g., caches de lecture, files d'écriture) peuvent être appliquées selon les besoins. |
| **Performances**  | Les modèles de lecture peuvent être pré-optimisés pour des requêtes spécifiques (dénormalisés, indexés). Les modèles d'écriture se concentrent purement sur la cohérence transactionnelle sans surcharge de lecture. |
| **Sécurité**     | Des modèles séparés permettent différents contrôles d'accès. Les commandes nécessitent généralement des privilèges plus élevés ; les requêtes peuvent être plus larges. |
| **Gestion de la complexité** | Isole la logique métier complexe du côté écriture, l'empêchant de se répercuter dans les opérations de lecture simples. |
| **Flexibilité**  | Différents modèles de lecture peuvent servir différentes vues (mobile, web, analytique) à partir du même modèle d'écriture. |

## Quand utiliser (et quand éviter)

### Utilisez CQRS lorsque :

- Forte contention sur des données partagées (e.g., systèmes de réservation, logistique, trading).
- Une partie du système a de lourdes charges de lecture qui ne doivent pas bloquer les transactions d'écriture.
- Différentes représentations des mêmes données sont nécessaires pour différents consommateurs.
- Une piste d'audit complète et une relecture des événements sont requises (généralement avec Event Sourcing).

### Évitez CQRS lorsque :

- Le système est un CRUD simple avec une logique minimale.
- Une forte cohérence éventuelle est inacceptable pour la plupart des opérations.
- L'équipe est petite ou peu familière avec la cohérence éventuelle et les modèles de messagerie.
- Le coût de maintenance de multiples modèles dépasse les avantages.

## Installation / Frameworks

CQRS est un modèle, pas une bibliothèque. « Installation » implique de choisir une couche d'infrastructure pour distribuer les commandes, gérer le traitement des événements et maintenir les projections de lecture. Les frameworks populaires incluent :

- **Axon Framework (Java/Kotlin) :** Complet avec des bus de commandes, d'événements et de requêtes, gestion des agrégats et Event Sourcing prêt à l'emploi.
- **MediatR (C#/F#) :** Médiateur léger intra-processus pour .NET, excellent pour implémenter CQRS dans un monolithe sans infrastructure de messagerie complète.
- **EventStoreDB (EventStore) :** Magasin d'événements spécialisé qui s'associe naturellement avec CQRS et Event Sourcing.
- **Marten (.NET) :** Base de données document / magasin d'événements sur PostgreSQL, avec support de projection intégré.
- **Dapr (Multi-langage) :** Fournit des blocs de construction pub/sub, gestion d'état et acteurs qui peuvent être composés en un système CQRS distribué.
- **Lagom (Java/Scala) :** Framework pour construire des microservices réactifs, inclut la séparation commande/requête comme modèle principal.

## Exemple d'utilisation (C# conceptuel / MediatR)

### Côté écriture – Commande

```csharp
// Command definition
public record PlaceOrderCommand(Guid UserId, List<OrderItem> Items);

// Command handler
public class PlaceOrderHandler : IRequestHandler<PlaceOrderCommand, Guid>
{
    private readonly IOrderRepository _writeRepo;

    public PlaceOrderHandler(IOrderRepository writeRepo)
    {
        _writeRepo = writeRepo;
    }

    public async Task<Guid> Handle(PlaceOrderCommand command, CancellationToken ct)
    {
        // 1. Validate business rules (e.g., check stock, user credit)
        // 2. Create Order Aggregate, enforce invariants
        var aggregate = Order.Create(command.UserId, command.Items);
        // 3. Persist events / state to Write Store
        await _writeRepo.Save(aggregate);
        // 4. Return result (events will be published to update read side)
        return aggregate.Id;
    }
}

// Domain event emitted by the aggregate (for event sourcing or outbox pattern)
public record OrderPlaced(
    Guid OrderId,
    Guid UserId,
    List<OrderItem> Items,
    decimal Total,
    DateTime PlacedAt
);
```

### Côté lecture – Requête

```csharp
// Query definition
public record GetOrderSummaryQuery(Guid OrderId);

// Query handler (reads from a separate, denormalized database)
public class GetOrderSummaryHandler : IRequestHandler<GetOrderSummaryQuery, OrderSummaryDto>
{
    private readonly IDbConnection _readDb;

    public GetOrderSummaryHandler(IDbConnection readDb)
    {
        _readDb = readDb;
    }

    public async Task<OrderSummaryDto> Handle(GetOrderSummaryQuery query, CancellationToken ct)
    {
        await _readDb.QuerySingleAsync<OrderSummaryDto>(
            "SELECT * FROM ReadModel_OrderSummaries WHERE Id = @Id",
            new { query.OrderId });
    }
}
```

### Projecteur – Maintenir le modèle de lecture à jour

```csharp
public class OrderProjector : IEventHandler<OrderPlaced>
{
    private readonly IDbConnection _readDb;

    public OrderProjector(IDbConnection readDb)
    {
        _readDb = readDb;
    }

    public async Task Handle(OrderPlaced @event)
    {
        // Denormalize the event data into a read-optimized table
        await _readDb.ExecuteAsync(@"
            INSERT INTO ReadModel_OrderSummaries (Id, UserId, Total, Status, PlacedAt)
            VALUES (@OrderId, @UserId, @Total, 'Pending', @PlacedAt)",
            @event);
    }
}
```

## Fonctionnalités clés

- **Séparation des préoccupations :** Les commandes et les requêtes sont développées, testées et déployées indépendamment.
- **Cohérence éventuelle :** Le côté écriture émet des événements ; les modèles de lecture sont mis à jour de manière asynchrone. C'est un compromis fondamental mais permet un débit élevé.
- **Stockage optimisé :** Chaque côté peut utiliser sa propre technologie de magasin de données (e.g., écriture : RDBMS, lecture : Elasticsearch, Redis, materialized views).
- **Audit et relecture (avec Event Sourcing) :** Le flux complet d'événements reconstitue tout état passé et prend en charge le débogage ou la reconstruction des projections.
- **Mise à l'échelle indépendante :** Les nœuds d'écriture et les réplicas de lecture peuvent être mis à l'échelle horizontalement en fonction de leurs charges respectives.

## Compromis clés et pièges

- **Cohérence éventuelle :** Les utilisateurs peuvent voir des données obsolètes jusqu'à ce que les projections soient terminées. Les atténuations incluent des avertissements de données obsolètes, l'idempotence ou la cohérence immédiate pour les chemins critiques.
- **Modèles de lecture N+1 :** Chaque projection doit être maintenue. Les changements fréquents de l'interface utilisateur peuvent augmenter la charge de maintenance.
- **Duplication de logique :** Les règles métier doivent résider **uniquement** du côté écriture. Le côté lecture ne doit jamais contenir de logique métier.
- **Complexité de l'infrastructure :** Nécessite une gestion fiable des messages (files d'attente, bus d'événements, patterns outbox) et une surveillance pour les scénarios de défaillance.
- **Courbe d'apprentissage :** L'équipe doit comprendre la cohérence éventuelle, l'architecture événementielle et souvent Event Sourcing.

## Conclusion

CQRS est un modèle puissant pour les systèmes où les charges de travail de lecture et d'écriture ont des exigences nettement différentes en termes de performances, d'évolutivité ou de sécurité. Ce n'est pas une solution miracle et il ajoute une complexité significative, surtout lorsqu'il est combiné avec Event Sourcing. Appliqué judicieusement – généralement dans des domaines de haute collaboration impliquant des règles métier complexes ou une charge de lecture élevée – CQRS peut considérablement améliorer la maintenabilité, les performances et l'évolutivité.