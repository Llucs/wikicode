---
title: Sharding — Particionamento Horizontal de Banco de Dados para Escalabilidade
description: Um guia detalhado sobre sharding, uma técnica para particionar horizontalmente bancos de dados entre servidores para melhorar escalabilidade, desempenho e isolamento de falhas.
created: 2026-06-16
tags:
  - database
  - scalability
  - sharding
  - distributed-systems
  - performance
status: draft
---

# Sharding

**Sharding** é um padrão de arquitetura de banco de dados onde um conjunto de dados grande e logicamente unificado é particionado horizontalmente em bancos de dados menores e independentes chamados *shards*. Cada shard é hospedado em uma instância de servidor separada operando em uma arquitetura de "nada compartilhado" (shared-nothing). O Sharding supera os limites da escalabilidade vertical de uma única máquina ao distribuir dados e carga de trabalho entre muitos nós.

## O que é

Sharding divide os dados em pedaços com base em uma *chave de shard* determinística. Cada shard contém um subconjunto dos dados (ex.: todas as linhas para um determinado intervalo de `user_id`) e é responsável por atender leituras e gravações para sua partição. O sistema total aparece como um banco de dados lógico para os clientes através de uma camada de roteamento (lógica de aplicação, proxy ou roteador de banco de dados).

## Por que fazer Sharding?

| Benefício | Descrição |
|-----------|-----------|
| **Escalabilidade horizontal** | A taxa de transferência de gravação e leitura escala linearmente à medida que shards são adicionados. |
| **Alta disponibilidade e isolamento de falhas** | A falha de um único shard afeta apenas um subconjunto de usuários; outros shards continuam atendendo. |
| **Paralelismo** | Consultas que atingem múltiplos shards podem ser paralelizadas, melhorando a latência. |
| **Distribuição geográfica** | Os dados podem ser colocados mais perto de populações específicas de usuários, reduzindo viagens de ida e volta na rede. |
| **Isolamento operacional** | Manutenção, backups e alterações de esquema podem ser realizados em um shard por vez. |

O sharding é essencial quando um único banco de dados não consegue mais lidar com a carga — muitas vezes depois que a escalabilidade vertical (CPUs maiores, mais RAM) se torna proibitiva em termos de custo ou atinge os limites de hardware.

## Arquiteturas de Sharding

O sharding pode ser implementado em várias camadas:

### 1. Nível de Aplicação (Manual)

A aplicação contém lógica de roteamento (ex.: `hash(user_id) % num_shards`). Cada shard é um banco de dados padrão sem software extra.  
**Prós:** Simples de começar, sem middleware.  
**Contras:** Frágil; o resharing requer alterações no código; consultas entre shards são extremamente difíceis.  
**Status:** Hoje considerado um anti-padrão para novos projetos.

### 2. Nível de Middleware / Proxy (ex.: Vitess, Citus)

Um proxy transparente intercepta consultas SQL e as roteia para o shard apropriado.

- **Vitess** para MySQL: implanta `vtgate` (proxy) + `vttablet` por shard, gerenciado por uma topologia etcd/zk.
- **Citus** para PostgreSQL: uma extensão que transforma um cluster Postgres em um banco de dados distribuído.

**Prós:** Transparência SQL, resharing automatizado (Vitess), junções entre shards (Citus).  
**Contras:** Camada adicional de complexidade; algumas consultas se tornam impossíveis ou lentas.

### 3. Nativo do Banco de Dados (ex.: MongoDB, Cassandra, Druid)

O mecanismo do banco de dados lida com a distribuição internamente. O desenvolvedor fornece uma chave de shard, e o sistema gerencia o posicionamento e roteamento dos dados.

- **MongoDB**: clusters fragmentados com roteadores `mongos` e servidores de configuração.
- **Cassandra**: particionamento por uma chave de partição na definição da chave primária; hashing consistente distribui as linhas automaticamente.

**Prós:** Sem proxy externo; recursos como balanceamento automático.  
**Contras:** Deve-se projetar cuidadosamente o modelo de dados em torno da chave de shard; operações entre shards são limitadas ou inexistentes.

### 4. Gerenciado em Nuvem (ex.: Amazon DynamoDB, Azure Cosmos DB, Google Cloud Spanner)

O provedor abstrai completamente o gerenciamento de shards. Você escolhe uma chave de partição durante a criação da tabela; a plataforma de nuvem divide, migra e equilibra os dados automaticamente.

**Prós:** Nenhuma sobrecarga operacional; escalabilidade automática.  
**Contras:** Dependência de fornecedor; o custo pode ser maior para grandes cargas de trabalho; nenhum controle direto sobre o posicionamento dos shards.

## Instalação e Uso Básico

Abaixo estão exemplos concretos para duas das implementações de sharding mais comuns.

### Sharding no MongoDB

**Instalação / Configuração**

- Implante um **conjunto de réplicas de servidor de configuração** (CSRS) que armazena metadados do cluster.
- Implante **conjuntos de réplicas de shard** (cada shard é pelo menos um nó único, mas geralmente um conjunto de réplicas para alta disponibilidade).
- Implante um ou mais **roteadores `mongos`** que processam consultas de aplicação.

Os comandos a seguir (executados contra um `mongos`) ativam o sharding e fragmentam uma coleção:

```javascript
// Ativar sharding em um banco de dados
sh.enableSharding("ecommerce");

// Fragmentar uma coleção usando uma chave de shard hasheada (recomendada para distribuição uniforme)
sh.shardCollection(
  "ecommerce.orders",
  { "order_id": "hashed" }
);
```

Com uma chave de shard hasheada, os documentos são distribuídos uniformemente entre os shards. Consultas que incluem a chave de shard são roteadas diretamente para o shard correto:

```javascript
// Consulta eficiente – vai para um único shard
db.orders.find({ "order_id": UUID("123e4567-e89b-12d3-a456-426614174000") })
```

Consultas entre shards (ex.: agregações sem a chave de shard) serão dispersadas para todos os shards, potencialmente prejudicando o desempenho.

### Citus (Extensão PostgreSQL)

**Instalação**

1. Instale a extensão `citus` no nó coordenador e em todos os nós workers.
2. Adicione nós workers ao coordenador:
   ```sql
   SELECT citus_add_node('worker-node-1', 5432);
   SELECT citus_add_node('worker-node-2', 5432);
   ```

**Uso Básico**

Distribua uma tabela especificando sua coluna de distribuição (chave de shard):

```sql
-- Criar a tabela no coordenador
CREATE TABLE orders (
    order_id    BIGSERIAL,
    user_id     INT,
    product_id  INT,
    quantity    INT,
    PRIMARY KEY (order_id, user_id)
);

-- Distribuir a tabela nos workers com base em user_id
SELECT create_distributed_table('orders', 'user_id');
```

O Citus reescreve o SQL para atingir o shard relevante. Uma consulta que filtra por `user_id` irá para um único worker:

```sql
-- Consulta de shard único
SELECT * FROM orders WHERE user_id = 42;
```

Para junções entre duas tabelas que estão colocalizadas na mesma chave de distribuição, o Citus pode executá-las eficientemente:

```sql
-- Exemplo de colocalização: orders e order_items distribuídas por user_id
SELECT create_distributed_table('orders', 'user_id');
SELECT create_distributed_table('order_items', 'user_id');
-- JOIN agora ocorre localmente em cada shard
SELECT o.order_id, oi.product_id
FROM orders o JOIN order_items oi USING (order_id)
WHERE o.user_id = 42;
```

## Principais Decisões de Projeto

### 1. Escolha da Chave de Shard

A chave de shard é a decisão mais crítica. Ela deve:

- **Distribuir os dados uniformemente** para evitar pontos de acesso (hot spots).
- **Corresponder aos padrões de consulta** para que consultas comuns possam ser roteadas para um único shard.
- **Ter alta cardinalidade** (muitos valores distintos) para permitir uma divisão uniforme.

**Escolhas ruins:** Valores monotonicamente crescentes (ex.: timestamps, IDs auto-incrementados) fazem com que todas as novas gravações vão para o último shard.  
**Escolhas melhores:** IDs de usuário, colunas hasheadas ou chaves compostas que combinam alta cardinalidade e colunas frequentes de filtro.

### 2. Operações entre Shards

Junções (JOINs), transações e agregações que abrangem múltiplos shards são muito caras ou não suportadas. Estratégias de mitigação:

- **Desnormalização** para manter dados relacionados no mesmo shard.
- **Colocalização** (Citus) ou **incorporação de documentos** (MongoDB) para armazenar dados hierárquicos no mesmo shard.
- **Coordenação no lado da aplicação** para transações multi-shard (raramente recomendado).

### 3. Resharding (Redistribuição)

Adicionar ou remover shards requer redistribuição de dados. Os sistemas modernos oferecem mecanismos embutidos:

- **MongoDB Balancer** move automaticamente chunks entre shards.
- **Vitess Reshard** divide shards usando um workflow `MoveTables`.
- **Serviços em nuvem** lidam com divisões de forma transparente.

O resharing manual (em sharding no nível de aplicação) é notoriamente difícil e propenso a erros.

## Estado Atual

A indústria está se afastando do sharding manual. Bancos de dados **NewSQL** (CockroachDB, YugabyteDB, Google Spanner) abstraem completamente o gerenciamento de shards por trás de uma interface SQL padrão, fornecendo transações ACID e junções entre shards. A maioria dos bancos de dados em nuvem (DynamoDB, Cosmos DB) oferece sharding serverless. No entanto, o conceito central de sharding continua sendo o alicerce para todos os bancos de dados distribuídos horizontalmente escaláveis.

Para novos projetos, prefira uma dessas opções a construir sua própria camada de sharding. Se você precisa de SQL e consistência forte, considere Citus ou Spanner; se a flexibilidade orientada a documentos e a alta taxa de transferência são fundamentais, MongoDB ou DynamoDB são excelentes escolhas.

## Resumo

Sharding é uma ferramenta poderosa para alcançar desempenho em escala web, mas introduz complexidade. Ao entender as opções arquiteturais, escolher uma boa chave de shard e aproveitar ferramentas modernas de gerenciamento, você pode escalar sua camada de dados sem reinventar a roda.