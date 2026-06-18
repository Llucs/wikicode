---
title: Vertical Slice Architecture
description: Uma abordagem de design de software que organiza o código por funcionalidades de negócio em vez de camadas técnicas, melhorando coesão e manutenibilidade.
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

## O que é Vertical Slice Architecture?

Vertical Slice Architecture (VSA) é um padrão de design de software que estrutura uma aplicação em torno de **funcionalidades de negócio** ou **casos de uso**, em vez de camadas técnicas horizontais (Controllers, Services, Repositories, Data Access). Cada "fatia vertical" captura todas as preocupações necessárias para entregar uma única funcionalidade — desde o endpoint HTTP ou manipulador de mensagens até a persistência no banco de dados — como uma unidade coesa e autocontida.

> "Nesse estilo, minha arquitetura é construída em torno de requisições distintas, encapsulando e agrupando todas as preocupações do front‑end ao back‑end. Você pega uma arquitetura normal em 'n‑camadas' ou hexagonal/qualquer outra e remove os portões e barreiras entre essas camadas, e acopla ..." — Jimmy Bogard

VSA foi popularizada por volta de **2016** por Jimmy Bogard (criador do MediatR) como uma resposta à complexidade acidental das arquiteturas tradicionais em Camadas ou Clean Architecture, onde adicionar até mesmo uma funcionalidade simples exige tocar em muitos arquivos espalhados por pastas não relacionadas.

## Por que usar?

- **Coesão de Funcionalidade** — Todo o código para um caso de uso vive em um só lugar. Um desenvolvedor pode entender e modificar a funcionalidade completa sem precisar saltar entre projetos ou pastas.
- **Baixo Acoplamento** — As fatias são independentes; elas interagem apenas através de um *núcleo compartilhado* bem definido (entidades de domínio, infraestrutura base, eventos de domínio). Mudanças em uma fatia raramente quebram outra.
- **Experiência Simplificada do Desenvolvedor** — A navegação é trivial: localize a pasta da funcionalidade e todos os seus arquivos estão ali.
- **Alinhamento com CQRS** — Commands e Queries mapeiam naturalmente para fatias individuais, incentivando uma separação clara entre leituras e escritas.
- **Autonomia da Equipe** — Equipes podem ser donas de fatias inteiras, reduzindo conflitos de merge e permitindo desenvolvimento paralelo.
- **Facilidade para Refatoração** — Como os limites coincidem com as capacidades de negócio, reestruturar uma funcionalidade tem impacto mínimo nas outras.

## Como se Diferencia da Arquitetura em Camadas

| Aspecto | Arquitetura em Camadas | Vertical Slice Architecture |
|---------|------------------------|----------------------------|
| Organização | Por camada técnica (Controllers, Services, Repositories) | Por funcionalidade de negócio (ex.: `CreateOrder`, `ShipOrder`) |
| Coesão | Baixa – código de uma funcionalidade está espalhado entre camadas | Alta – todo o código da funcionalidade está junto |
| Acoplamento | Camadas dependem umas das outras | Fatias dependem apenas do núcleo compartilhado |
| Impacto de Mudança | Uma simples mudança afeta muitos arquivos em várias camadas | Mudança contida em uma única pasta |
| Curva de Aprendizado | Familiar para a maioria dos desenvolvedores | Requer entendimento de CQRS e padrão mediator |

## Conceitos Principais

### Pasta de Funcionalidade / Fatia
Cada fatia é um diretório contendo tudo o que um caso de uso precisa. Uma fatia típica pode incluir:

```
Features/
  Orders/
    CreateOrder/
      CreateOrderCommand.cs       # Input contract (immutable)
      CreateOrderHandler.cs       # Business logic + orchestration
      CreateOrderValidator.cs     # Input validation
      CreateOrderEndpoint.cs      # API endpoint (Minimal API, Controller, etc.)
```

Nada fora da fatia referencia esses arquivos, exceto através de uma interface de mediador (ex.: `IRequest<OrderDto>`).

### Núcleo Compartilhado
Lógicas de domínio comuns, entidades base, objetos de valor e infraestrutura (DbContext, logging, autenticação) ficam fora das fatias, em um projeto `Shared` ou `Core`. As fatias importam do núcleo compartilhado, mas nunca umas das outras.

### CQRS (Command Query Responsibility Segregation)
VSA adota naturalmente o CQRS. Cada fatia lida exatamente com um comando (operação de escrita) ou uma query (operação de leitura), tornando a intenção do sistema clara.

### Padrão Mediator
Um mediator em processo desacopla o remetente de uma requisição do manipulador. Bibliotecas como **MediatR** ou **Brighter** são comumente usadas para despachar commands/queries e para aplicar preocupações transversais (validação, logging, transações).

## Quando Usar Vertical Slice Architecture

- **Domínios de Negócio Complexos** – Finanças, logística, saúde, ERP — domínios com muitos fluxos de trabalho distintos.
- **Grandes Equipes de Desenvolvimento** – Funcionalidades podem ser atribuídas a diferentes desenvolvedores ou equipes com mínima coordenação.
- **Monólitos Modulares** – Você deseja limites de módulo fortes dentro de uma única implantação.
- **Microsserviços** – Cada microsserviço pode ser uma única fatia, ou o VSA pode estruturar seus internos.
- **Migração de Legado** – Substitua incrementalmente camadas antigas fatiando funcionalidades uma de cada vez.

## Instalação (Bibliotecas de Apoio)

VSA é um padrão arquitetural, não uma biblioteca. No entanto, ferramentas como MediatR são quase sempre usadas para implementá-lo em .NET.

### .NET (C#) – Configuração do MediatR e FluentValidation

```bash
# Create a new project
dotnet new webapi -n MyApp

# Add packages
dotnet add package MediatR
dotnet add package MediatR.Extensions.Microsoft.DependencyInjection  # For automatic registration (if not using latest)
dotnet add package FluentValidation
dotnet add package FluentValidation.DependencyInjectionExtensions
```

## Exemplo de Implementação (C# com MediatR)

Vamos construir uma funcionalidade `PlaceOrder` de ponta a ponta.

### 1. Contrato – Command (Entrada)

```csharp
// Features/Orders/PlaceOrder/PlaceOrderCommand.cs
using MediatR;

public record PlaceOrderCommand(int CustomerId, List<CartItem> Items) : IRequest<OrderDto>;
```

### 2. Handler – Lógica de Negócio + Acesso a Dados

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
        // 1. Load customer
        var customer = await _db.Customers
            .Include(c => c.Cart)
            .FirstOrDefaultAsync(c => c.Id == request.CustomerId, cancellationToken)
            ?? throw new NotFoundException("Customer not found");

        // 2. Domain logic – create order
        var order = new Order(customer);
        // ... pricing, validation, etc.

        _db.Orders.Add(order);
        await _db.SaveChangesAsync(cancellationToken);

        return new OrderDto(order.Id, order.Total);
    }
}
```

### 3. Validação (FluentValidation)

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

### 4. Endpoint – Minimal API

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

### 5. Registro e Conexão (Composition Root)

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Register MediatR (scans assembly for handlers)
builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(typeof(Program).Assembly));
builder.Services.AddValidatorsFromAssembly(typeof(Program).Assembly);

// Register DbContext etc.
builder.Services.AddDbContext<AppDbContext>(...);

var app = builder.Build();

// Map endpoints from each slice
app.MapPlaceOrder();

app.Run();
```

### Árvore de Diretórios (Simplificada)

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

## Funcionalidades Principais com Exemplos de Comandos (MediatR)

### Despachar um Command de um Controller ou Minimal API

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

### Behaviors Personalizados de Pipeline (Preocupações Transversais)

MediatR suporta behaviors de pipeline para logging, validação, transações etc.

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

### Despachar uma Query

```csharp
// GetOrderHistoryQuery.cs
public record GetOrderHistoryQuery(int CustomerId, int Page = 1, int PageSize = 20) : IRequest<PagedResult<OrderDto>>;

// Handler uses DbContext directly
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

## Melhores Práticas

- **Defina um Núcleo Compartilhado** – Coloque entidades, objetos de valor, classes base e infraestrutura comum em um local central que cada fatia possa referenciar. **Não** permita que fatias dependam umas das outras.
- **Mantenha as Fatias Enxutas** – Cada fatia deve conter exatamente a lógica para seu caso de uso. Se a lógica for reutilizada entre fatias, extraia-a para um serviço de domínio ou helper compartilhado, não para uma fatia.
- **Use Eventos de Domínio para Comunicação Entre Fatias** – Quando uma fatia precisar reagir à ação de outra, publique um evento de domínio a partir do handler e defina um handler separado (mesmo que viva em outra fatia) que escute esse evento.
- **Abrace a Duplicação em vez da Abstração Prematura** – Não há problema se duas fatias tiverem código semelhante, mas ligeiramente diferente. Extraia lógica compartilhada apenas quando ela for verdadeiramente idêntica e estável.
- **Padronize a Validação** – Use uma biblioteca como FluentValidation e um behavior de pipeline para validar automaticamente todos os commands.
- **Evite Estruturas de Fatia Anêmicas** – Garanta que o handler contenha lógica de negócio real; não delegue apenas para um serviço externo. O handler é o lugar onde a orquestração da funcionalidade vive.
- **Documente o Contrato da Fatia** – O registro do command/query é a API da fatia. Mantenha-o imutável e torne sua intenção óbvia.

## Desvantagens e Considerações

- **Risco de Duplicação** – Sem disciplina, a mesma validação ou lógica pode ser repetida entre fatias. Um núcleo compartilhado e serviços de domínio ajudam, mas alguma duplicação é aceita.
- **Curva de Aprendizado** – Equipes novas em CQRS, mediator ou VSA precisam de tempo para se ajustar.
- **Sobrecarga de Ferramentas** – MediatR e bibliotecas similares introduzem indireção (embora o mediator em processo seja barato).
- **Não para Aplicações CRUD Simples** – Aplicações com lógica de negócio mínima podem não se beneficiar da sobrecarga de fatiamento.

## Conclusão

Vertical Slice Architecture oferece uma alternativa prática e sustentável às arquiteturas tradicionais em camadas para aplicações de negócio complexas. Ao organizar o código em torno de funcionalidades em vez de camadas técnicas, melhora a coesão, simplifica a navegação e facilita a evolução do sistema à medida que os requisitos de negócio mudam. Quando combinada com CQRS e uma biblioteca de mediator, a VSA fornece uma estrutura limpa e autodocumentada que escala bem tanto com o tamanho da base de código quanto com o tamanho da equipe.

Comece pequeno: escolha uma funcionalidade, fatie-a e experimente a diferença. Depois que sentir a coesão e o isolamento, você se perguntará como tolerou a dispersão entre camadas.

---

### Leitura Adicional

- [Jimmy Bogard – Vertical Slice Architecture (Vídeo)](https://www.youtube.com/watch?v=5kOzZz2vj4A)
- [Jimmy Bogard – From Inception to Production (Palestra)](https://www.youtube.com/watch?v=Lx9fBkz_0QQ)
- [Vertical Slice Architecture – Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures#vertical-slice-architecture)
- [MediatR GitHub](https://github.com/jbogard/MediatR)