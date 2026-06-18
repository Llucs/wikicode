---
title: Architecture en Tranches Verticales
description: Une approche de conception logicielle qui organise le code par fonctionnalités métier plutôt que par couches techniques, améliorant la cohésion et la maintenabilité.
created: 2026-06-18
tags:
  - architecture
  - cqrs
  - feature-organization
  - dotnet
  - best-practices
status: draft
---

# Vertical Slice Architecture

## What Is Vertical Slice Architecture?

Vertical Slice Architecture (VSA) est un modèle de conception logicielle qui structure une application autour de **fonctionnalités métier** ou de **cas d'utilisation** plutôt qu'autour de couches techniques horizontales (Contrôleurs, Services, Dépôts, Accès aux données). Chaque « tranche verticale » capture tous les aspects nécessaires pour délivrer une fonctionnalité unique – du point d'entrée HTTP ou du gestionnaire de messages jusqu'à la persistance en base de données – en tant qu'unité cohérente et autonome.

> « Dans ce style, mon architecture est construite autour de requêtes distinctes, encapsulant et regroupant tous les aspects du front‑end au back‑end. Vous prenez une architecture ‘n‑tier’ ou hexagonale/quelconque normale et supprimez les barrières entre ces couches, et couplez … » — Jimmy Bogard

VSA a été popularisée autour de **2016** par Jimmy Bogard (créateur de MediatR) en réponse à la complexité accidentelle des architectures en couches ou Clean Architecture traditionnelles, où ajouter une simple fonctionnalité nécessite de toucher de nombreux fichiers dispersés dans des dossiers sans rapport.

## Pourquoi l'utiliser ?

- **Cohésion des fonctionnalités** — Tout le code pour un cas d'utilisation vit au même endroit. Un développeur peut comprendre et modifier la fonctionnalité entière sans naviguer entre plusieurs projets ou dossiers.
- **Faible couplage** — Les tranches sont indépendantes ; elles n'interagissent qu'à travers un *noyau partagé* bien défini (entités du domaine, infrastructure de base, événements du domaine). Les modifications dans une tranche cassent rarement une autre.
- **Expérience développeur simplifiée** — La navigation est triviale : localisez le dossier de la fonctionnalité et tous ses fichiers s'y trouvent.
- **Alignement avec CQRS** — Les commandes et les requêtes se mappent naturellement aux tranches individuelles, encourageant une séparation claire des lectures et des écritures.
- **Autonomie des équipes** — Les équipes peuvent posséder des tranches entières, réduisant les conflits de fusion et permettant un développement parallèle.
- **Aide au refactoring** — Comme les limites correspondent aux capacités métier, la restructuration d'une fonctionnalité a un impact minimal sur les autres.

## En quoi cela diffère de l'architecture en couches

| Aspect | Architecture en couches | Architecture en tranches verticales |
|--------|------------------------|--------------------------------------|
| Organisation | Par couche technique (Contrôleurs, Services, Dépôts) | Par fonctionnalité métier (p. ex., `CreateOrder`, `ShipOrder`) |
| Cohésion | Faible – le code d'une fonctionnalité est dispersé entre les couches | Haute – tout le code de la fonctionnalité est regroupé |
| Couplage | Les couches dépendent les unes des autres | Les tranches dépendent uniquement du noyau partagé |
| Impact des changements | Une modification simple touche plusieurs fichiers dans plusieurs couches | Le changement est contenu dans un seul dossier |
| Courbe d'apprentissage | Familière pour la plupart des développeurs | Nécessite la compréhension de CQRS et du pattern Médiateur |

## Concepts clés

### Dossier de fonctionnalité / Tranche
Chaque tranche est un répertoire contenant tout ce dont un cas d'utilisation a besoin. Une tranche typique peut inclure :

```
Features/
  Orders/
    CreateOrder/
      CreateOrderCommand.cs       # Contrat d'entrée (immuable)
      CreateOrderHandler.cs       # Logique métier + orchestration
      CreateOrderValidator.cs     # Validation des entrées
      CreateOrderEndpoint.cs      # Point d'API (Minimal API, Controller, etc.)
```

Rien en dehors de la tranche ne référence ces fichiers, sauf via une interface de médiateur (p. ex., `IRequest<OrderDto>`).

### Noyau partagé
La logique du domaine commune, les entités de base, les objets de valeur et l'infrastructure (DbContext, journalisation, authentification) vivent en dehors des tranches dans un projet `Shared` ou `Core`. Les tranches importent depuis le noyau partagé mais jamais les unes des autres.

### CQRS (Command Query Responsibility Segregation)
VSA adopte naturellement CQRS. Chaque tranche gère exactement une commande (opération d'écriture) ou une requête (opération de lecture), rendant l'intention du système claire.

### Pattern Médiateur
Un médiateur intra-processus découple l'expéditeur d'une requête de son gestionnaire. Des bibliothèques comme **MediatR** ou **Brighter** sont couramment utilisées pour distribuer les commandes/requêtes et appliquer des préoccupations transversales (validation, journalisation, transactions).

## Quand utiliser Vertical Slice Architecture

- **Domaines métier complexes** – Finance, logistique, santé, ERP — des domaines avec de nombreux flux de travail distincts.
- **Grandes équipes de développement** – Les fonctionnalités peuvent être assignées à différents développeurs ou équipes avec un minimum de coordination.
- **Monolithes modulaires** – Vous voulez des frontières de module solides au sein d'un seul déploiement.
- **Microservices** – Chaque microservice peut être une seule tranche, ou VSA peut structurer son interne.
- **Migration d'héritage** – Remplacer progressivement les anciennes couches en découpant les fonctionnalités une par une.

## Installation (Bibliothèques de support)

VSA est un pattern architectural, pas une bibliothèque. Cependant, des outils comme MediatR sont presque toujours utilisés pour l'implémenter en .NET.

### .NET (C#) – Configuration de MediatR & FluentValidation

```bash
# Créer un nouveau projet
dotnet new webapi -n MyApp

# Ajouter les packages
dotnet add package MediatR
dotnet add package MediatR.Extensions.Microsoft.DependencyInjection  # Pour enregistrement automatique (si vous n'utilisez pas la dernière version)
dotnet add package FluentValidation
dotnet add package FluentValidation.DependencyInjectionExtensions
```

## Exemple d'implémentation (C# avec MediatR)

Construisons une fonctionnalité `PlaceOrder` de bout en bout.

### 1. Contrat – Commande (Entrée)

```csharp
// Features/Orders/PlaceOrder/PlaceOrderCommand.cs
using MediatR;

public record PlaceOrderCommand(int CustomerId, List<CartItem> Items) : IRequest<OrderDto>;
```

### 2. Gestionnaire – Logique métier + Accès aux données

```csharp
// Features/Orders/PlaceOrder/PlaceOrderHandler.cs
using MediatR;
using Microsoft.EntityFrameworkCore;

public class PlaceOrderHandler : IRequestHandler<PlaceOrderCommand, OrderDto>
{
    private readonly AppDbContext _db;

    public PlaceOrderHandler(AppDbContext db) => _db = db;

    public async Task<OrderDto> Handle(PlaceOrderCommand request, CancellationToken cancellationToken)
    {
        // 1. Charger le client
        var customer = await _db.Customers
            .Include(c => c.Cart)
            .FirstOrDefaultAsync(c => c.Id == request.CustomerId, cancellationToken)
            ?? throw new NotFoundException("Client non trouvé");

        // 2. Logique métier – créer la commande
        var order = new Order(customer);
        // ... tarification, validation, etc.

        _db.Orders.Add(order);
        await _db.SaveChangesAsync(cancellationToken);

        return new OrderDto(order.Id, order.Total);
    }
}
```

### 3. Validation (FluentValidation)

```csharp
// Features/Orders/PlaceOrder/PlaceOrderValidator.cs
using FluentValidation;

public class PlaceOrderValidator : AbstractValidator<PlaceOrderCommand>
{
    public PlaceOrderValidator()
    {
        RuleFor(x => x.CustomerId).GreaterThan(0);
        RuleFor(x => x.Items).NotEmpty();
        RuleForEach(x => x.Items).ChildRules(item =>
        {
            item.RuleFor(i => i.Quantity).GreaterThan(0);
        });
    }
}
```

### 4. Point de terminaison – API minimale

```csharp
// Features/Orders/PlaceOrder/PlaceOrderEndpoint.cs
public static class PlaceOrderEndpoint
{
    public static void MapPlaceOrder(this WebApplication app)
    {
        app.MapPost("/orders", async (IMediator mediator, PlaceOrderCommand command, IValidator<PlaceOrderCommand> validator) =>
        {
            var validationResult = await validator.ValidateAsync(command);
            if (!validationResult.IsValid)
                return Results.ValidationProblem(validationResult.ToDictionary());

            var result = await mediator.Send(command);
            return Results.Ok(result);
        });
    }
}
```

### 5. Enregistrement & câblage (Racine de composition)

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Enregistrer MediatR (scanne l'assembly pour les gestionnaires)
builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(typeof(Program).Assembly));
builder.Services.AddValidatorsFromAssembly(typeof(Program).Assembly);

// Enregistrer DbContext, etc.
builder.Services.AddDbContext<AppDbContext>(...);

var app = builder.Build();

// Mapper les points de terminaison de chaque tranche
app.MapPlaceOrder();

app.Run();
```

### Arborescence des répertoires (simplifiée)

```
MyApp/
  Features/
    Orders/
      PlaceOrder/
        PlaceOrderCommand.cs
        PlaceOrderHandler.cs
        PlaceOrderValidator.cs
        PlaceOrderEndpoint.cs
      GetOrderHistory/
        GetOrderHistoryQuery.cs
        GetOrderHistoryHandler.cs
        GetOrderHistoryEndpoint.cs
    Products/
      CreateProduct/
        ...
  Shared/
    Entities/
      Customer.cs
      Order.cs
    Exceptions/
      NotFoundException.cs
  Data/
    AppDbContext.cs
  Program.cs
```

## Fonctionnalités clés avec exemples de commandes (MediatR)

### Distribuer une commande depuis un Controller ou une API minimale

```csharp
[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    private readonly IMediator _mediator;

    public OrdersController(IMediator mediator) => _mediator = mediator;

    [HttpPost]
    public async Task<IActionResult> PlaceOrder([FromBody] PlaceOrderCommand command)
    {
        var orderId = await _mediator.Send(command);
        return Ok(orderId);
    }
}
```

### Comportements de pipeline personnalisés (Préoccupations transversales)

MediatR prend en charge les comportements de pipeline pour la journalisation, la validation, les transactions, etc.

```csharp
// Shared/Behaviors/ValidationBehavior.cs
public class ValidationBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;

    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators) => _validators = validators;

    public async Task<TResponse> Handle(TRequest request, RequestHandlerDelegate<TResponse> next, CancellationToken cancellationToken)
    {
        if (_validators.Any())
        {
            var context = new ValidationContext<TRequest>(request);
            var failures = _validators
                .Select(v => v.Validate(context))
                .SelectMany(result => result.Errors)
                .Where(f => f != null)
                .ToList();

            if (failures.Any())
                throw new ValidationException(failures);
        }

        return await next();
    }
}
```

### Distribuer une requête

```csharp
// GetOrderHistoryQuery.cs
public record GetOrderHistoryQuery(int CustomerId, int Page = 1, int PageSize = 20) : IRequest<PagedResult<OrderDto>>;

// Le gestionnaire utilise directement DbContext
public class GetOrderHistoryHandler : IRequestHandler<GetOrderHistoryQuery, PagedResult<OrderDto>>
{
    private readonly AppDbContext _db;

    public GetOrderHistoryHandler(AppDbContext db) => _db = db;

    public async Task<PagedResult<OrderDto>> Handle(GetOrderHistoryQuery request, CancellationToken ct)
    {
        var query = _db.Orders.Where(o => o.CustomerId == request.CustomerId);
        var total = await query.CountAsync(ct);
        var items = await query
            .OrderByDescending(o => o.CreatedAt)
            .Skip((request.Page - 1) * request.PageSize)
            .Take(request.PageSize)
            .Select(o => new OrderDto(o.Id, o.Total, o.Status))
            .ToListAsync(ct);

        return new PagedResult<OrderDto>(items, total, request.Page, request.PageSize);
    }
}
```

## Bonnes pratiques

- **Définir un noyau partagé** – Placez les entités, les objets de valeur, les classes de base et l'infrastructure commune dans un emplacement central que chaque tranche peut référencer. Ne laissez **pas** les tranches dépendre les unes des autres.
- **Garder les tranches légères** – Chaque tranche doit contenir exactement la logique pour son cas d'utilisation. Si une logique est réutilisée entre tranches, extrayez-la dans un service de domaine ou un utilitaire partagé, pas dans une tranche.
- **Utiliser les événements de domaine pour la communication inter-tranches** – Lorsqu'une tranche doit réagir à l'action d'une autre, publiez un événement de domaine depuis le gestionnaire et définissez un gestionnaire séparé (même s'il vit dans une autre tranche) qui écoute cet événement.
- **Accepter la duplication plutôt que l'abstraction prématurée** – Il est acceptable que deux tranches aient un code similaire mais légèrement différent. N'extrayez une logique partagée que lorsqu'elle est vraiment identique et stable.
- **Standardiser la validation** – Utilisez une bibliothèque comme FluentValidation et un comportement de pipeline pour valider automatiquement toutes les commandes.
- **Éviter les structures de tranches anémiques** – Assurez-vous que le gestionnaire contienne une vraie logique métier ; ne déléguez pas simplement à un service externe. Le gestionnaire est l'endroit où se trouve l'orchestration de la fonctionnalité.
- **Documenter le contrat de la tranche** – L'enregistrement de commande/requête est l'API de la tranche. Gardez-le immuable et rendez son intention évidente.

## Inconvénients et considérations

- **Risque de duplication** – Sans discipline, la même validation ou logique peut être répétée entre les tranches. Un noyau partagé et des services de domaine aident, mais une certaine duplication est acceptée.
- **Courbe d'apprentissage** – Les équipes nouvelles avec CQRS, le médiateur ou VSA ont besoin de temps pour s'adapter.
- **Surcharge d'outillage** – MediatR et les bibliothèques similaires introduisent une indirection (bien que le médiateur intra-processus soit peu coûteux).
- **Pas pour les applications CRUD simples** – Les applications avec une logique métier minimale peuvent ne pas bénéficier de la surcharge du découpage.

## Conclusion

Vertical Slice Architecture offre une alternative pratique et maintenable aux architectures en couches traditionnelles pour les applications métier complexes. En organisant le code autour des fonctionnalités plutôt que des couches techniques, elle améliore la cohésion, simplifie la navigation et facilite l'évolution du système à mesure que les exigences métier changent. Combinée à CQRS et à une bibliothèque de médiateur, VSA fournit une structure propre et auto-documentée qui passe à l'échelle tant pour la taille du codebase que pour celle de l'équipe.

Commencez petit : choisissez une fonctionnalité, découpez-la, et expérimentez la différence. Une fois que vous ressentez la cohésion et l'isolation, vous vous demanderez pourquoi vous avez toléré la dispersion entre couches.

---

### Lectures complémentaires

- [Jimmy Bogard – Vertical Slice Architecture (Vidéo)](https://www.youtube.com/watch?v=5kOzZz2vj4A)
- [Jimmy Bogard – From Inception to Production (Talk)](https://www.youtube.com/watch?v=Lx9fBkz_0QQ)
- [Vertical Slice Architecture – Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures#vertical-slice-architecture)
- [MediatR GitHub](https://github.com/jbogard/MediatR)