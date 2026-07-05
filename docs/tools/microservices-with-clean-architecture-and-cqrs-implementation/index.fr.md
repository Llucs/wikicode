---
title: Microservices avec une architecture propre et une mise en œuvre CQRS
description: Découvrez comment mettre en œuvre une architecture de microservices robuste, échelonnable et maintenable en utilisant une architecture propre et CQRS.
created: 2026-07-05
tags:
  - microservices
  - architecture propre
  - CQRS
  - .NET 8
  - .NET Core
status: brouillon
---

# Microservices avec une architecture propre et une mise en œuvre CQRS

L'architecture de microservices combinée à une architecture propre et CQRS offre une approche robuste, échelonnable et maintenable pour développer des applications complexes. Ce document vous guidera dans la mise en œuvre de telle une architecture en utilisant .NET 8.

## Qu'est-ce que les microservices ?

L'architecture de microservices est une approche de développement de logiciels qui structure l'application en un ensemble de services couplés de manière distante, chacun implémentant des capacités d'affaires. Chaque service est un processus indépendant et petit qui communique avec d'autres services via des API bien définies.

## Architecture propre

L'architecture propre est un modèle de conception de logiciel qui met l'accent sur la séparation des responsabilités, garantissant que la logique métier centrale est indépendante des frameworks et technologies externes. Elle se concentre sur la logique métier centrale, rendant l'application plus résiliente aux changements de technologies et d'infrastructure. Les composants clés incluent :

- **Entités** : Logique métier et règles.
- **Cas d'utilisation** : Définissent comment les entités interagissent avec le monde extérieur.
- **Répositories** : Abstractions pour accéder aux données.
- **Contrôleur** : Facilite l'interaction entre le monde extérieur et l'application.

## CQRS (Responsabilité de la commande et de la requête)

CQRS est un modèle de conception qui permet de construire des applications hautement échelonnables en séparant les opérations de lecture et d'écriture. Dans une architecture CQRS, la partie d'écriture (commandes) et la partie de lecture (requêtes) sont séparées, permettant des schémas de bases de données optimisés pour chaque partie.

## Histoire

- **Microservices** : Émergés au début des années 2010 en réponse aux limites des architectures monolithiques, en particulier en ce qui concerne la mise en échelle et le déploiement.
- **Architecture propre** : Proposée par Robert C. Martin (Uncle Bob) en 2012, mettant l'accent sur une approche structurée de conception logicielle.
- **CQRS** : Premièrement décrit par Eric Evans en 2010, est devenu populaire au milieu des années 2010, notamment dans le contexte des bases de données NoSQL.

## Caractéristiques clés

- **Microservices** :
  - **Échelonnabilité** : Chaque service peut être mis en échelle indépendamment.
  - **Résilience** : Les échecs dans un service n'entraînent pas nécessairement la panne du système.
  - **Flexibilité** : Les différents services peuvent être construits avec des technologies et langages différents.
- **Architecture propre** :
  - **Séparation des responsabilités** : Division claire des responsabilités.
  - **Testabilité** : Tests unitaires et d'intégration simplifiés en raison de la séparation des responsabilités.
  - **Évolution** : Plus facile de développer l'application sans briser la fonctionnalité existante.
- **CQRS** :
  - **Performance** : Optimisation des opérations de lecture et d'écriture.
  - **Flexibilité** : Permet des schémas de bases de données différents pour les opérations de lecture et d'écriture.
  - **Échelonnabilité** : Les opérations de lecture peuvent être mis en échelle indépendamment des opérations d'écriture.

## Cas d'utilisation

- **Microservices** : Convenable pour les applications complexes nécessitant une grande échelonnabilité et flexibilité, telles que les plateformes de commerce électronique, les services de streaming multimédia et les systèmes bancaires.
- **Architecture propre** : Idéale pour garantir la maintenabilité et la testabilité, surtout dans les projets à long terme.
- **CQRS** : Meilleur pour les applications ayant des opérations d'écriture complexes et des opérations de lecture élevées, telles que les systèmes de trading et la gestion des stocks.

## Installation et utilisation basiques

### Microservices

1. **Choix du framework** : Choisissez un framework de microservices comme Spring Boot, ASP.NET Core ou Node.js.
2. **Containerisation** : Utilisez Docker et Docker Compose pour gérer les services.
3. **Découverte de service** : Implémentez des mécanismes de découverte de service comme Consul ou Eureka.
4. **Porte-parole API** : Utilisez un porte-parole API comme Kong ou Zuul pour gérer le trafic entre les services.

### Architecture propre

1. **Structure du projet** : Organisez le projet en couches : entités, cas d'utilisation, répositories et contrôleurs.
2. **Frameworks** : Utilisez des frameworks comme Spring Boot ou ASP.NET Core qui soutiennent l'injection de dépendances et la testabilité.
3. **Tests** : Implémentez des tests unitaires et d'intégration pour assurer que la logique centrale fonctionne correctement.

### CQRS

1. **Configuration de la base de données** : Conçoivez des bases de données ou des schémas séparés pour les opérations de lecture et d'écriture.
2. **Événement sourcing** : Utilisez l'événement sourcing pour capturer tous les changements d'état.
3. **Couche de requêtes** : Implémentez des modèles de lecture pour optimiser les opérations de lecture.
4. **Couche de commandes** : Gérez les commandes pour mettre à jour les modèles de lecture.

### Exemple : Un microservice avec une architecture propre et CQRS

1. **Entité** :
   - Définir la logique métier centrale, par exemple `Commande`.

```csharp
public class Commande
{
    public int Id { get; set; }
    public string NomClient { get; set; }
    public DateTime DateCommande { get; set; }
    // Autres propriétés et logique métier
}
```

2. **Cas d'utilisation** :
   - Définir comment l'entité interagit avec le monde extérieur, par exemple `PlaceCommandeUseCase`.

```csharp
public interface IPlaceCommandeUseCase
{
    Task PlaceCommandeAsync(PlaceCommandeCommande commande);
}

public class PlaceCommandeUseCase : IPlaceCommandeUseCase
{
    private readonly ICommandeRepository _commandeRepository;

    public PlaceCommandeUseCase(ICommandeRepository commandeRepository)
    {
        _commandeRepository = commandeRepository;
    }

    public async Task PlaceCommandeAsync(PlaceCommandeCommande commande)
    {
        var commande = new Commande
        {
            NomClient = commande.NomClient,
            DateCommande = DateTime.UtcNow
        };

        await _commandeRepository.CreateAsync(commande);
    }
}
```

3. **Répository** :
   - Définir l'interface pour accéder à la base de données, par exemple `ICommandeRepository`.

```csharp
public interface ICommandeRepository
{
    Task<Commande> CreateAsync(Commande commande);
}
```

4. **Contrôleur** :
   - Facilite l'interaction entre le monde extérieur et l'application, par exemple `CommandeController`.

```csharp
[ApiController]
[Route("api/[controller]")]
public class CommandeController : ControllerBase
{
    private readonly IPlaceCommandeUseCase _placeCommandeUseCase;

    public CommandeController(IPlaceCommandeUseCase placeCommandeUseCase)
    {
        _placeCommandeUseCase = placeCommandeUseCase;
    }

    [HttpPost("place-commande")]
    public async Task<IActionResult> PlaceCommandeAsync([FromBody] PlaceCommandeCommande commande)
    {
        await _placeCommandeUseCase.PlaceCommandeAsync(commande);
        return Ok();
    }
}
```

5. **Commande** :
   - Définir la commande pour placer une commande, par exemple `PlaceCommandeCommande`.

```csharp
public class PlaceCommandeCommande
{
    public string NomClient { get; set; }
}
```

6. **Requête** :
   - Définir la requête pour récupérer une commande, par exemple `GetCommandeQuery`.

```csharp
public class GetCommandeQuery
{
    public int Id { get; set; }
}

public interface IGetCommandeQuery
{
    Task<Commande> GetAsync(GetCommandeQuery query);
}

public class GetCommandeQueryHandler : IGetCommandeQuery
{
    private readonly ICommandeRepository _commandeRepository;

    public GetCommandeQueryHandler(ICommandeRepository commandeRepository)
    {
        _commandeRepository = commandeRepository;
    }

    public async Task<Commande> GetAsync(GetCommandeQuery query)
    {
        return await _commandeRepository.GetAsync(query.Id);
    }
}
```

7. **Événement sourcing** :
   - Capturer tous les changements d'état, par exemple `CommandePlacéeEvent`.

```csharp
public class CommandePlacéeEvent
{
    public int CommandeId { get; set; }
    public string NomClient { get; set; }
    public DateTime DateCommande { get; set; }
}
```

En intégrant ces composants, vous pouvez construire une architecture robuste, échelonnable et maintenable utilisant les microservices, l'architecture propre et CQRS.

## Conclusion

L'implémentation de microservices avec une architecture propre et CQRS fournit une solide base pour développer des applications complexes et échelonnables. En suivant les directives et les exemples fournis, vous pouvez créer une architecture maintenable et testable qui s'aligne sur les meilleures pratiques de développement modernes.

## Références

- [DDG] Un échantillon de microservices en .NET 8 montrant l'architecture propre, le design dirigé par domaine (DDD) et CQRS avec des tests d'architecture automatisés, des tests d'intégration et une coordination distribuée événementielle.
- [DDG] Joydip Kanjilal explore le modèle de conception Responsabilité de la commande et de la requête (CQRS) et sa mise en œuvre dans les architectures de microservices construites avec ASP.NET Core.
- [DDG] Ce projet est une mise en œuvre de l'architecture propre avec le modèle de conception CQRS en utilisant .NET 9.