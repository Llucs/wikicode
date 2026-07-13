---
title: Separação de Comando e Consulta (CQRS)
description: Um padrão de design usado na arquitetura de software para separar comandos (operações de gravação) de consultas (operações de leitura).
created: 2026-07-13
tags:
  - arquitetura de software
  - padrões de design
  - CQRS
  - separação de comando e consulta
status: rascunho
---

# Separação de Comando e Consulta (CQRS)

Separação de Comando e Consulta (CQRS) é um padrão de design usado na arquitetura de software para separar comandos (operações de gravação) de consultas (operações de leitura). Esta separação pode levar a aplicativos mais manutáveis e escaláveis, especialmente em cenários complexos e do mundo real.

## O que é CQRS?

CQRS é um padrão de design que enfatiza a separação das ações que solicitam informações (consultas) das que modificam o estado (comandos). Esta separação pode levar a aplicativos mais manutáveis e escaláveis, especialmente em sistemas com altos volumes de transações ou lógica de negócios complexa.

## Características Principais

1. **Tratamento de Comandos**: Comandos são usados para modificar o estado do sistema. Geralmente são emitidos por sistemas externos ou usuários e são usados para realizar ações, como criar, atualizar ou excluir dados.
2. **Tratamento de Consultas**: Consultas são usadas para recuperar informações do sistema. São operações de leitura apenas que não modificam o estado do sistema. As consultas podem ser otimizadas para cargas de trabalho de leitura intensivas, que são geralmente mais eficientes do que ter um único armazenamento de dados que trata tanto as leituras quanto as gravações.
3. **Separação de Responsabilidades**: CQRS ajuda a separar as responsabilidades de operações de escrita e leitura, tornando o sistema mais manutável e escalável.
4. **Fonte de Eventos**: Geralmente usado em conjunto com CQRS, onde as alterações no sistema são registradas como uma sequência de eventos. Estes eventos podem ser usados para reconstruir o estado atual do sistema ou para acionar comandos.

## Histórico

CQRS não era uma nova ideia quando foi popularizado pela primeira vez. O conceito de separar comandos e consultas tem sido usado há muito tempo, mas não foi amplamente aplicado até ser apoiado por Greg Young e Udi Dahan nos anos iniciais da década de 2010. Eles apresentaram suas ideias em conferências e workshops, levando a uma adoção mais ampla do padrão.

## Casos de Uso

1. **Processamento Transacional Online (OLTP)**: CQRS é especialmente útil em sistemas que requerem alto fluxo de escritas, como plataformas de comércio eletrônico, sistemas financeiros ou aplicações de jogos.
2. **Data Warehousing**: CQRS pode ajudar na construção de data warehouses separando os dados de alta escrita transacionais dos dados de alta leitura analíticos.
3. **Lógica de Negócios Complexa**: Sistemas com lógica de negócios complexa que exigem atualizações e modificações frequentes podem beneficiar da separação de comandos e consultas.

## Instalação

CQRS não é um framework independente, mas um padrão de design. Portanto, ele não vem com uma instalação direta. No entanto, você pode implementar CQRS em sua aplicação seguindo estes passos gerais:

1. **Definir Comandos e Consultas**: Crie conjuntos de classes de comando para lidar com operações de escrita e classes de consulta para lidar com operações de leitura.
2. **Implementar Manipuladores de Comandos**: Escreva manipuladores para processar os comandos e realizar as operações necessárias nos dados.
3. **Implementar Manipuladores de Consultas**: Escreva manipuladores para processar as consultas e retornar os dados necessários.
4. **Fonte de Eventos (Opcional)**: Implemente a fonte de eventos para capturar mudanças no sistema e usar esses eventos para atualizar o modelo de leitura.

## Uso Básico

### Lidando com Comandos

```csharp
public class OrderService {
    private readonly CommandBus _commandBus;

    public OrderService(CommandBus commandBus) {
        _commandBus = commandBus;
    }

    public void PlaceOrder(Order order) {
        _commandBus.Send(new PlaceOrderCommand(order));
    }
}
```

### Lidando com Consultas

```csharp
public class OrderQueryService {
    private readonly QueryBus _queryBus;

    public OrderQueryService(QueryBus queryBus) {
        _queryBus = queryBus;
    }

    public Order GetOrderById(Guid orderId) {
        return _queryBus.Send(new GetOrderByIdQuery(orderId));
    }
}
```

### Fonte de Eventos

```csharp
public class OrderAggregate {
    private readonly IEventRepository _eventRepository;

    public OrderAggregate(IEventRepository eventRepository) {
        _eventRepository = eventRepository;
    }

    public void ApplyCommand(PlaceOrderCommand command) {
        // Aplicar comando e salvar eventos
        _eventRepository.Save(new OrderPlacedEvent(command.Order.Id, command.Order.CustomerId));
    }
}
```

## Conclusão

CQRS é um poderoso padrão de design que pode significativamente aumentar a escalabilidade e a manutibilidade de aplicativos complexos. Ao separar comandos e consultas, os desenvolvedores podem otimizar seus sistemas para operações de escrita e leitura, levando a aplicativos mais eficientes e robustos. No entanto, exige um design e implementação cuidadosas para ser eficaz, e pode não ser adequado para todos os tipos de aplicativos.