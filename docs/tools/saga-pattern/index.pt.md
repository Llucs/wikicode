---
title: Padrão Saga
description: Um padrão de design para gerenciar transações distribuídas em múltiplos serviços ou recursos em arquiteturas de microserviços.
created: 2026-07-09
tags:
  - microserviços
  - transações distribuídas
  - padrões de design
  - padrão saga
status: rascunho
---

# Padrão Saga

## Visão Geral

O Padrão Saga é um padrão de design utilizado em sistemas distribuídos para gerenciar transações em múltiplos serviços ou recursos. Garante a consistência e a confiabilidade das operações mantendo uma sequência de operações que devem ser concluídas com sucesso para que a transação seja considerada válida. Se alguma operação falhar, o padrão permite o reverter de todas as operações concluídas para manter a integridade do sistema.

## Características Principais

1. **Operações de Compensação**: Para cada unidade de trabalho (operação), é definida uma operação de compensação correspondente que pode reverter as alterações feitas pela unidade de trabalho. Isso assegura que, se uma operação falhar, o sistema possa reverter para seu estado anterior.
2. **Execução Sequencial**: As operações são executadas em um ordem específica e cada operação depende do sucesso da operação anterior.
3. **Convergência Eventual**: O padrão garante que o sistema se mova para um estado consistente ao longo do tempo, mesmo que transações individuais falhem.
4. **Idempotência**: As operações dentro de um saga devem ser idempotentes para garantir que o estado do sistema não mude se a mesma operação for chamada várias vezes.

## Histórico

O Padrão Saga foi desenvolvido para resolver os desafios de gerenciar transações distribuídas em arquiteturas de microserviços. Antes da era dos microserviços, as aplicações monolíticas normalmente gerenciavam transações no nível do banco de dados. No entanto, à medida que as aplicações se tornaram mais distribuídas, a complexidade de gerenciar transações entre múltiplos serviços aumentou. O Padrão Saga foi introduzido como uma solução para lidar com essas complexidades.

O conceito de Sagas pode ser rastreado até os anos 1970, com o trabalho de Jim Gray em processamento de transações, mas ganhou destaque no contexto de microserviços e sistemas distribuídos nos anos 2010.

## Casos de Uso

1. **Transações Financeiras**: O processamento de transações como transferências, pagamentos e devoluções requer garantir que os fundos sejam corretamente movidos entre contas. Um saga pode gerenciar essas operações, garantindo que, se uma transferência falhar, o saldo original seja restaurado.
2. **Processamento de Pedidos**: Em comércio eletrônico, o processamento de um pedido envolve várias etapas, como reservar o produto, atualizar o estoque e cobrar o cliente. Um saga pode garantir que todas essas operações sejam concluídas com sucesso ou revertidas se falharem.
3. **Sistemas de Saúde**: Em sistemas de saúde, transações como cobrança, agendamento de consultas e gerenciamento de prescrições requerem garantir que todas as etapas sejam concluídas ou revertidas se falharem, para manter a integridade dos dados do paciente.
4. **Reclamações de Seguro**: O gerenciamento de reclamações de seguro envolve várias etapas, como processamento de reclamação, pagamento e validação de documentos. Um saga pode gerenciar essas operações para garantir que a reclamação seja processada corretamente ou revertida se alguma etapa do processo falhar.

## Instalação e Configuração

O Padrão Saga é típicomente implementado usando uma combinação de programação de aplicativos e serviços de middleware. Aqui está uma visão geral básica de como configurar um saga:

1. **Definir Operações**: Identifique as operações que precisam ser realizadas como parte do saga. Para cada operação, defina a ação de compensação.
2. **Uso de uma Fila de Mensagens**: Implemente uma fila de mensagens para gerenciar a execução das operações. Isso pode ser um provedor de mensagens como RabbitMQ, Kafka ou AWS SQS.
3. **Gerenciador de Saga**: Crie um gerenciador de saga que orchestre a sequência de operações. O gerenciador deve controlar a execução das operações, rastrear o estado do saga e gerenciar a lógica de compensação se uma operação falhar.
4. **Ações de Compensação**: Implemente as ações de compensação que podem reverter o estado do sistema para seu estado anterior se uma operação falhar.

### Uso Básico

1. **Iniciar o Saga**: Inicie o saga iniciando a primeira operação na sequência.
2. **Executar Operações**: Execute cada operação na sequência. Se uma operação falhar, o saga deve parar e executar as ações de compensação.
3. **Rastrear Estado**: Mantenha um registro estado do saga para rastrear o progresso e garantir que as operações sejam concluídas na ordem correta.
4. **Compensar**: Se uma operação falhar, o saga deve executar as ações de compensação para reverter o sistema para um estado consistente.
5. **Concluir o Saga**: Uma vez que todas as operações são concluídas com sucesso, o saga pode ser marcado como concluído.

### Exemplo

Aqui está um exemplo em Python demonstrando a estrutura básica de um saga, onde as operações são enfileiradas e executadas em sequência, com ações de compensação definidas para lidar com falhas:

```python
from queue import Queue

# Definir operações e ações de compensação
def create_product_reservation(product_id, quantity):
    # Implementação para criar uma reserva de produto
    pass

def update_inventory(product_id, quantity):
    # Implementação para atualizar o estoque
    pass

def charge_customer(customer_id, amount):
    # Implementação para cobrar o cliente
    pass

def cancel_reservation(product_id, quantity):
    # Implementação para cancelar a reserva
    pass

def refund_customer(customer_id, amount):
    # Implementação para reembolsar o cliente
    pass

# Definir o saga
def process_order(saga_id, product_id, quantity, customer_id, amount):
    saga_queue = Queue()

    try:
        saga_queue.put(create_product_reservation(product_id, quantity))
        saga_queue.put(update_inventory(product_id, quantity))
        saga_queue.put(charge_customer(customer_id, amount))
        
        while not saga_queue.empty():
            operation = saga_queue.get()
            operation()
        
        # Marcar o saga como concluído
        print(f"Saga {saga_id} concluída com sucesso.")
    except Exception as e:
        # Executar ações de compensação
        while not saga_queue.empty():
            operation = saga_queue.get()
            operation()
        print(f"Saga {saga_id} falhou. Ações de compensação executadas.")
        
# Iniciar o saga
process_order(1, "P123", 10, "C12345", 100)
```

Este exemplo demonstra a estrutura básica de um saga, onde as operações são enfileiradas e executadas em sequência, com ações de compensação definidas para lidar com falhas.

## Conclusão

O Padrão Saga é uma solução robusta para gerenciar transações em múltiplos serviços em sistemas distribuídos. Ao garantir que as operações sejam executadas em uma ordem específica e fornecendo ações de compensação para lidar com falhas, o padrão ajuda a manter a integridade do sistema. Entender o Padrão Saga é crucial para desenvolver arquiteturas de microserviços confiáveis e escaláveis.