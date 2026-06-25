---
title: CQRS (Segregação de Responsabilidade de Comando e Consulta)
description: Um padrão arquitetural que separa operações de leitura e escrita em modelos distintos para otimizar desempenho, escalabilidade e manutenibilidade.
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

CQRS (Segregação de Responsabilidade de Comando e Consulta) é um padrão arquitetural que separa as responsabilidades de leitura de dados (consultas) da atualização de dados (comandos). Ao usar modelos distintos e, frequentemente, armazenamentos de dados separados para leituras e escritas, o CQRS permite a otimização independente de cada lado, melhorando escalabilidade, desempenho e segurança em sistemas complexos.

## O Que É & História

O termo CQRS foi popularizado por Greg Young e Udi Dahan no final dos anos 2000 nas comunidades de Domain-Driven Design (DDD). Sua base conceitual está no princípio **Command‑Query Separation (CQS)** de Bertrand Meyer, que afirma que um método deve ser ou um *comando* (realizar uma ação) ou uma *consulta* (retornar dados), mas não ambos. O CQRS eleva essa ideia do nível do método para o nível arquitetural e de armazenamento de dados.

Em uma arquitetura CRUD tradicional, um único modelo lida com leituras, escritas, atualizações e exclusões. O CQRS divide explicitamente isso em dois lados distintos:

- **Modelo de Escrita (Comandos):** Lida com operações de mudança de estado. Comandos são imperativos, produzem efeitos colaterais e impõem invariantes de negócio (tipicamente por meio de Agregados em DDD).
- **Modelo de Leitura (Consultas):** Lida com recuperação de dados. Consultas são declarativas, sem efeitos colaterais e otimizadas para contratos específicos de UI ou API. Frequentemente são desnormalizadas, pré‑agrupadas ou armazenadas em bancos de dados diferentes (ex.: Elasticsearch para busca, Redis para cache).

O CQRS é frequentemente combinado com **Event Sourcing**, onde o lado de escrita produz um fluxo de eventos de domínio que são consumidos assincronamente para construir e atualizar os modelos de leitura.

## Por Que Usar CQRS?

| Benefício | Descrição |
|-----------|-----------|
| **Escalabilidade** | Réplicas de leitura podem ser escaladas independentemente dos nós de escrita. Infraestrutura diferente (ex.: caches de leitura, filas de escrita) pode ser aplicada conforme a necessidade. |
| **Desempenho** | Modelos de leitura podem ser pré‑otimizados para consultas específicas (desnormalizados, indexados). Modelos de escrita focam puramente em consistência transacional sem sobrecarga de leitura. |
| **Segurança** | Modelos separados permitem controles de acesso diferentes. Comandos tipicamente exigem privilégios mais altos; consultas podem ser mais amplas. |
| **Gerenciamento de Complexidade** | Isola a lógica de domínio complexa no lado de escrita, impedindo que ela se infiltre em operações simples de leitura. |
| **Flexibilidade** | Diferentes modelos de leitura podem atender a diferentes visualizações (mobile, web, analytics) a partir do mesmo modelo de escrita. |

## Quando Usar (e Quando Evitar)

### Use CQRS quando:

- Alta contenção em dados compartilhados (ex.: sistemas de reserva, logística, negociação).
- Uma parte do sistema tem cargas pesadas de leitura que não devem bloquear transações de escrita.
- Diferentes representações dos mesmos dados são necessárias para diferentes consumidores.
- Trilha de auditoria completa e reprodução de eventos são necessárias (tipicamente com Event Sourcing).

### Evite CQRS quando:

- O sistema é CRUD simples com lógica mínima.
- Consistência eventual forte é inaceitável para a maioria das operações.
- A equipe é pequena ou não está familiarizada com consistência eventual e padrões de mensageria.
- O custo de manter múltiplos modelos supera os benefícios.

## Instalação / Frameworks

CQRS é um padrão, não uma biblioteca. "Instalação" envolve escolher uma camada de infraestrutura para despachar comandos, gerenciar manipulação de eventos e manter projeções de leitura. Frameworks populares incluem:

- **Axon Framework (Java/Kotlin):** Completo, com barramentos de Comando/Evento/Consulta, gerenciamento de agregados e Event Sourcing pronto para uso.
- **MediatR (C#/F#):** Mediator leve em processo para .NET, excelente para implementar CQRS em um monólito sem uma infraestrutura de mensageria completa.
- **EventStoreDB (EventStore):** Armazenamento de eventos construído para esse fim, que se combina naturalmente com CQRS e Event Sourcing.
- **Marten (.NET):** Banco de documentos / armazenamento de eventos em PostgreSQL, com suporte interno a projeções.
- **Dapr (Multi‑idioma):** Fornece blocos de construção de pub/sub, gerenciamento de estado e atores que podem ser compostos em um sistema CQRS distribuído.
- **Lagom (Java/Scala):** Framework para construir microsserviços reativos, inclui separação comando/consulta como um padrão principal.

## Exemplo de Uso (Conceitual C# / MediatR)

### Lado de Escrita – Comando

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

### Lado de Leitura – Consulta

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

### Projetor – Mantendo o Modelo de Leitura Atualizado

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

## Características Principais

- **Separação de Preocupações:** Comandos e consultas são desenvolvidos, testados e implantados independentemente.
- **Consistência Eventual:** O lado de escrita emite eventos; os modelos de leitura são atualizados assincronamente. Este é um compromisso central, mas permite alta taxa de transferência.
- **Armazenamento Otimizado:** Cada lado pode usar sua própria tecnologia de armazenamento de dados (ex.: escrita: RDBMS, leitura: Elasticsearch, Redis, visões materializadas).
- **Auditoria e Reprodução (com Event Sourcing):** O fluxo completo de eventos reconstrói qualquer estado passado e suporta depuração ou reconstrução de projeções.
- **Escalonamento Independente:** Nós de escrita e réplicas de leitura podem escalar horizontalmente com base em suas respectivas cargas.

## Principais Compensações & Armadilhas

- **Consistência Eventual:** Os usuários podem ver dados desatualizados até que as projeções sejam concluídas. Mitigações incluem avisos de dados desatualizados, idempotência ou consistência imediata para caminhos críticos.
- **N+1 Modelos de Leitura:** Cada projeção deve ser mantida. Mudanças frequentes na interface do usuário podem aumentar a sobrecarga de manutenção.
- **Duplicação de Lógica:** As regras de negócio devem viver **apenas** no lado de escrita. O lado de leitura nunca deve conter lógica de domínio.
- **Complexidade de Infraestrutura:** Requer manipulação confiável de mensagens (filas, barramentos de eventos, padrões outbox) e monitoramento para cenários de falha.
- **Curva de Aprendizado:** A equipe precisa entender consistência eventual, arquitetura orientada a eventos e, frequentemente, Event Sourcing.

## Conclusão

CQRS é um padrão poderoso para sistemas onde as cargas de trabalho de leitura e escrita têm requisitos de desempenho, escalabilidade ou segurança distintamente diferentes. Não é uma bala de prata e adiciona complexidade significativa, especialmente quando combinado com Event Sourcing. Quando aplicado criteriosamente — tipicamente em domínios de alta colaboração envolvendo regras de negócio complexas ou carga pesada de leitura — o CQRS pode melhorar drasticamente a mantibilidade, o desempenho e a escalabilidade.