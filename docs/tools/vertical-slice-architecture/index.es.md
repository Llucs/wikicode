---
title: Arquitectura de Corte Vertical
description: Un enfoque de diseño de software que organiza el código por funcionalidades de negocio en lugar de por capas técnicas, mejorando la cohesión y la mantenibilidad.
created: 2026-06-18
tags:
  - architecture
  - cqrs
  - feature-organization
  - dotnet
  - best-practices
status: draft
---

# Arquitectura de Corte Vertical

## ¿Qué es la Arquitectura de Corte Vertical?

La Arquitectura de Corte Vertical (VSA) es un patrón de diseño de software que estructura una aplicación en torno a **funcionalidades de negocio** o **casos de uso** en lugar de capas técnicas horizontales (Controladores, Servicios, Repositorios, Acceso a Datos). Cada "corte vertical" captura todas las preocupaciones necesarias para entregar una única funcionalidad, desde el endpoint HTTP o el manejador de mensajes hasta la persistencia en la base de datos, como una unidad cohesiva y autocontenida.

> "En este estilo, mi arquitectura se construye en torno a solicitudes distintas, encapsulando y agrupando todas las preocupaciones desde el front‑end hasta el back. Tomas una arquitectura normal de 'n‑capas' o hexagonal/como sea y eliminas las puertas y barreras entre esas capas, y acoplas ..." — Jimmy Bogard

La VSA fue popularizada alrededor de **2016** por Jimmy Bogard (creador de MediatR) como respuesta a la complejidad accidental de la Arquitectura en Capas o Clean Architecture tradicional, donde agregar incluso una funcionalidad simple requiere tocar muchos archivos dispersos en carpetas no relacionadas.

## ¿Por qué usarla?

- **Cohesión de funcionalidad** — Todo el código para un caso de uso vive en un solo lugar.
- **Acoplamiento débil** — Los cortes son independientes; interactúan solo a través de un *kernel compartido* bien definido (entidades de dominio, infraestructura base, eventos de dominio). Los cambios en un corte rara vez afectan a otro.
- **Experiencia de desarrollador simplificada** — La navegación es trivial: localiza la carpeta de la funcionalidad y todos sus archivos están allí.
- **Alineación con CQRS** — Los Comandos y Consultas se asignan naturalmente a cortes individuales, fomentando una clara separación de lecturas y escrituras.
- **Autonomía del equipo** — Los equipos pueden ser dueños de cortes completos, reduciendo conflictos de fusión y permitiendo desarrollo en paralelo.
- **Facilidad de refactorización** — Debido a que los límites coinciden con las capacidades del negocio, reestructurar una funcionalidad tiene un impacto mínimo en las demás.

## Cómo se diferencia de la Arquitectura en Capas

| Aspecto | Arquitectura en Capas | Arquitectura de Corte Vertical |
|--------|----------------------|-------------------------------|
| Organización | Por capa técnica (Controladores, Servicios, Repositorios) | Por funcionalidad de negocio (p. ej., `CreateOrder`, `ShipOrder`) |
| Cohesión | Baja – el código de una funcionalidad está disperso entre capas | Alta – todo el código de la funcionalidad está junto |
| Acoplamiento | Las capas dependen unas de otras | Los cortes dependen solo del kernel compartido |
| Impacto del cambio | Un cambio simple toca muchos archivos en muchas capas | El cambio se contiene dentro de una carpeta |
| Curva de aprendizaje | Familiar para la mayoría de desarrolladores | Requiere entender CQRS y el patrón mediador |

## Conceptos clave

### Carpeta de funcionalidad / Corte
Cada corte es un directorio que contiene todo lo que un caso de uso necesita. Un corte típico podría incluir:

```
Features/
  Orders/
    CreateOrder/
      CreateOrderCommand.cs       # Input contract (immutable)
      CreateOrderHandler.cs       # Business logic + orchestration
      CreateOrderValidator.cs     # Input validation
      CreateOrderEndpoint.cs      # API endpoint (Minimal API, Controller, etc.)
```

Nada fuera del corte referencia estos archivos excepto a través de una interfaz mediadora (p. ej., `IRequest<OrderDto>`).

### Kernel compartido
La lógica de dominio común, entidades base, objetos de valor e infraestructura (DbContext, logging, autenticación) viven fuera de los cortes en un proyecto `Shared` o `Core`. Los cortes importan del kernel compartido pero nunca entre sí.

### CQRS (Segregación de Responsabilidades de Comando y Consulta)
VSA adopta naturalmente CQRS. Cada corte maneja exactamente un comando (operación de escritura) o una consulta (operación de lectura), haciendo clara la intención del sistema.

### Patrón Mediador
Un mediador en proceso desacopla el emisor de una solicitud del manejador. Bibliotecas como **MediatR** o **Brighter** se usan comúnmente para enviar comandos/consultas y aplicar preocupaciones transversales (validación, logging, transacciones).

## Cuándo usar la Arquitectura de Corte Vertical

- **Dominios de negocio complejos** – Finanzas, logística, salud, ERP — dominios con muchos flujos de trabajo distintos.
- **Equipos de desarrollo grandes** – Las funcionalidades pueden asignarse a diferentes desarrolladores o equipos con mínima coordinación.
- **Monolitos modulares** – Deseas límites de módulo fuertes dentro de una sola implementación.
- **Microservicios** – Cada microservicio puede ser un solo corte, o VSA puede estructurar su interior.
- **Migración de legado** – Reemplazar incrementalmente capas antiguas cortando funcionalidades una por una.

## Instalación (Bibliotecas de apoyo)

VSA es un patrón arquitectónico, no una biblioteca. Sin embargo, herramientas como MediatR se usan casi siempre para implementarlo en .NET.

### .NET (C#) – Configuración de MediatR y FluentValidation

```bash
# Create a new project
dotnet new webapi -n MyApp

# Add packages
dotnet add package MediatR
dotnet add package MediatR.Extensions.Microsoft.DependencyInjection  # For automatic registration (if not using latest)
dotnet add package FluentValidation
dotnet add package FluentValidation.DependencyInjectionExtensions
```

## Ejemplo de Implementación (C# con MediatR)

Construyamos una funcionalidad `PlaceOrder` de extremo a extremo.

### 1. Contrato – Comando (Entrada)

```csharp
// Features/Orders/PlaceOrder/PlaceOrderCommand.cs
using MediatR;

public record PlaceOrderCommand(int CustomerId, List<CartItem> Items) : IRequest<OrderDto>;
```

### 2. Manejador – Lógica de negocio + Acceso a datos

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

### 3. Validación (FluentValidation)

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

### 4. Endpoint – API Mínima

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

### 5. Registro y Cableado (Raíz de Composición)

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

### Árbol de Directorios (Simplificado)

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

## Características Clave con Ejemplos de Comandos (MediatR)

### Enviar un Comando desde un Controlador o API Mínima

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

### Comportamientos de Pipeline Personalizados (Preocupaciones Transversales)

MediatR admite comportamientos de pipeline para logging, validación, transacciones, etc.

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

### Enviar una Consulta

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

## Mejores Prácticas

- **Definir un Kernel Compartido** – Colocar entidades, objetos de valor, clases base e infraestructura común en una ubicación central que cada corte pueda referenciar. **No** permitir que los cortes dependan unos de otros.
- **Mantener los Cortes Delgados** – Cada corte debe contener exactamente la lógica para su caso de uso. Si la lógica se reutiliza entre cortes, extraerla en un servicio de dominio o helper compartido, no en un corte.
- **Usar Eventos de Dominio para Comunicación entre Cortes** – Cuando un corte necesita reaccionar a la acción de otro, publicar un evento de dominio desde el manejador y definir un manejador separado (incluso si vive en otro corte) que escuche ese evento.
- **Aceptar la duplicación sobre la abstracción prematura** – Está bien si dos cortes tienen código similar pero ligeramente diferente. Extraer lógica compartida solo cuando sea realmente idéntica y estable.
- **Estandarizar la validación** – Usar una biblioteca como FluentValidation y un comportamiento de pipeline para validar automáticamente todos los comandos.
- **Evitar estructuras de corte anémicas** – Asegurarse de que el manejador contenga lógica de negocio real; no delegar simplemente a un servicio externo. El manejador es el lugar donde reside la orquestación de la funcionalidad.
- **Documentar el Contrato del Corte** – El registro de comando/consulta es la API para el corte. Mantenerlo inmutable y hacer su intención obvia.

## Desventajas y Consideraciones

- **Riesgo de duplicación** – Sin disciplina, la misma validación o lógica puede repetirse entre cortes. Un kernel compartido y servicios de dominio ayudan, pero se acepta cierta duplicación.
- **Curva de aprendizaje** – Los equipos nuevos en CQRS, mediador o VSA necesitan tiempo para adaptarse.
- **Sobrecarga de herramientas** – MediatR y bibliotecas similares introducen indirección (aunque el mediador en proceso es económico).
- **No para aplicaciones CRUD simples** – Las aplicaciones con lógica de negocio mínima pueden no beneficiarse de la sobrecarga del corte.

## Conclusión

La Arquitectura de Corte Vertical ofrece una alternativa práctica y mantenible a las arquitecturas en capas tradicionales para aplicaciones de negocio complejas. Al organizar el código en torno a funcionalidades en lugar de capas técnicas, mejora la cohesión, simplifica la navegación y facilita la evolución del sistema a medida que cambian los requisitos de negocio. Cuando se combina con CQRS y una biblioteca mediadora, VSA proporciona una estructura limpia y autodocumentada que escala bien tanto con el tamaño del código base como con el tamaño del equipo.

Empieza pequeño: elige una funcionalidad, córtala y experimenta la diferencia. Una vez que sientas la cohesión y el aislamiento, te preguntarás por qué toleraste la dispersión entre capas.

---

### Lecturas Adicionales

- [Jimmy Bogard – Arquitectura de Corte Vertical (Video)](https://www.youtube.com/watch?v=5kOzZz2vj4A)
- [Jimmy Bogard – Desde la Concepción hasta la Producción (Charla)](https://www.youtube.com/watch?v=Lx9fBkz_0QQ)
- [Arquitectura de Corte Vertical – Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures#vertical-slice-architecture)
- [MediatR GitHub](https://github.com/jbogard/MediatR)