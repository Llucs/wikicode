---
title: Teorema CAP (Teorema de Brewer)
description: Um princípio fundamental de trade-off em sistemas distribuídos que afirma que é impossível para um armazenamento de dados distribuído garantir simultaneamente Consistência, Disponibilidade e Tolerância a Partições.
created: 2026-06-21
tags:
  - distributed-systems
  - cap-theorem
  - consistency
  - availability
  - partition-tolerance
  - brewers-theorem
  - system-design
  - database-architecture
status: draft
---

# Teorema CAP (Teorema de Brewer)

## O que é o Teorema CAP?

O Teorema CAP é um princípio fundamental no design de sistemas distribuídos. Foi introduzido pela primeira vez por **Eric Brewer** no Simpósio ACM sobre Princípios de Computação Distribuída (PODC) em **2000** e formalmente provado por **Seth Gilbert** e **Nancy Lynch** em **2002**.

O teorema afirma que um armazenamento de dados distribuído pode fornecer apenas **duas de três** garantias a qualquer momento:
- **Consistência (C)**
- **Disponibilidade (A)**
- **Tolerância a Partições (P)**

Embora muitas vezes simplificado como uma escolha estrita de "escolha dois", a interpretação correta é: **na presença de uma partição de rede, você deve escolher entre Consistência e Disponibilidade**. Como as partições de rede são inevitáveis em sistemas distribuídos, você não pode ter todas as três simultaneamente.

---

## As Três Propriedades

### Consistência (C)
Toda leitura recebe a **escrita mais recente** ou um erro. Todos os nós no sistema veem os mesmos dados ao mesmo tempo lógico. Isso implica uma ordem total de operações (linearizabilidade).

- **Impacto:** Consistência mais forte geralmente requer sincronização entre nós antes de confirmar escritas.
- **Exemplo:** Uma leitura de qualquer nó deve retornar o mesmo resultado que uma leitura do nó primário.

### Disponibilidade (A)
Toda solicitação recebida por um nó não falho no sistema **deve resultar em uma resposta**. A resposta pode não conter os dados mais recentes, mas não será um erro (por exemplo, timeout ou 503).

- **Impacto:** O sistema permanece ativo e aceitando tráfego, mesmo que algumas réplicas estejam dessincronizadas.
- **Exemplo:** Uma aplicação web continua a servir um catálogo de produtos mesmo que um nó de banco de dados downstream esteja inacessível.

### Tolerância a Partições (P)
O sistema continua a operar apesar de **um número arbitrário de mensagens serem perdidas ou atrasadas** pela rede entre os nós. Isso inclui divisões de rede, cortes de cabo e perda de pacotes.

- **Impacto:** O sistema deve funcionar corretamente mesmo quando os nós não conseguem se comunicar.
- **Realidade:** Partições são inevitáveis em qualquer sistema geograficamente distribuído. Portanto, **todo sistema distribuído deve ser tolerante a partições**.

---

## O Trade-off Real: CP vs AP

Como as partições de rede (P) são inevitáveis em um sistema distribuído, alcançar **CA** (Consistência + Disponibilidade) sem Tolerância a Partições é impossível em um contexto distribuído. A escolha real é:

### Sistemas CP (Consistência + Tolerância a Partições)
- **Sacrifica:** Disponibilidade durante uma partição.
- **Comportamento:** Nós que não podem garantir consistência com o resto do cluster se recusam a responder a solicitações (tornam-se indisponíveis) até que a partição seja resolvida.
- **Casos de Uso:** Registros bancários, gerenciamento de inventário, registros de saúde — situações onde dados desatualizados são inaceitáveis.
- **Exemplos Notáveis:**
  - **Apache ZooKeeper** (eleição de líder, dados de configuração)
  - **Apache HBase** (modelo de consistência forte)
  - **MongoDB** (com write concern `w: "majority"` e leituras do primário)
  - **Redis** (modo cluster com garantias estritas de consistência)

### Sistemas AP (Disponibilidade + Tolerância a Partições)
- **Sacrifica:** Consistência durante uma partição.
- **Comportamento:** Todos os nós permanecem disponíveis para atender solicitações, mesmo que aceitem escritas independentemente. O sistema depende de mecanismos de resolução de conflitos (por exemplo, última escrita vence, CRDTs) para reconciliar dados quando a partição é curada.
- **Casos de Uso:** Feeds de redes sociais, entrega de conteúdo, dados de sensores IoT, catálogos de produtos — ambientes onde o tempo de atividade é crítico.
- **Exemplos Notáveis:**
  - **Apache Cassandra** (consistência ajustável, consistência eventual por padrão)
  - **Amazon DynamoDB** (leituras eventualmente consistentes em múltiplas regiões)
  - **CouchDB / Couchbase** (replicação multi-mestre)
  - **Riak**

### Sistemas CA (Consistência + Disponibilidade)
- **Contexto:** Só é possível em um sistema não distribuído (mononó) ou em um sistema que simplesmente ignora partições (o que é perigoso).
- **Exemplos Notáveis:**
  - Uma instância **MySQL** ou **PostgreSQL** autónoma.
  - SGBDs tradicionais compatíveis com ACID em execução em um único servidor.
  - *Nota:* Em uma implantação distribuída, esses sistemas devem replicar dados e inevitavelmente encontram partições, forçando-os a se comportar como CP ou AP.

---

## Principais Características e Nuances

### 1. O "P" Não é Opcional
Um erro comum de iniciante é projetar um sistema distribuído "CA". Uma vez que os dados são replicados por uma rede, você está sujeito a partições. Qualquer sistema distribuído real **deve** tolerar partições, tornando a seleção real **CP vs AP** quando ocorre uma partição.

### 2. Ajustabilidade
Bancos de dados modernos não estão presos a uma única classificação. Você pode frequentemente trocar consistência por disponibilidade (ou vice-versa) por consulta.

- **Cassandra:** Alterne entre `QUORUM` (consistência forte) e `ONE` (consistência eventual) por requisição.
- **MongoDB:** Configure `writeConcern` e `readPreference` para mudar entre consistência forte e fraca.
- **DynamoDB:** Escolha `ConsistentRead` como `true` ou `false` nas leituras.

### 3. A Falácia do "2 de 3"
O teorema CAP não diz "o sistema deve sempre escolher dois de três". Ele diz que **durante uma partição de rede**, você deve escolher **C** ou **A**. No resto do tempo (quando a rede está saudável), o sistema pode buscar tanto consistência forte quanto alta disponibilidade.

É aqui que o **Teorema PACELC** entra em jogo.

---

## A Extensão PACELC (A Visão Moderna)

Introduzido por **Daniel J. Abadi**, o PACELC estende o CAP ao considerar explicitamente os trade-offs quando o sistema está **saudável** (sem partição).

**PACELC significa:**
- Se uma **P**artição ocorre → trade-off entre **A**vailability e **C**onsistency.
- **E**lse (quando a rede está saudável) → trade-off entre **L**atency e **C**onsistency.

### Por que o PACELC é Importante
- **Trade-offs em Estado Saudável:** Mesmo sem partições, você pode optar por esperar que as réplicas concordem (alta latência, consistência forte) ou responder rapidamente com dados potencialmente desatualizados (baixa latência, consistência eventual).
- **Configuração no Mundo Real:**
  - **Sistema CP (durante partição):** Sacrifica disponibilidade.
    - **E** (Else): Pode também sacrificar latência por consistência (por exemplo, replicação síncrona).
  - **Sistema AP (durante partição):** Sacrifica consistência.
    - **E** (Else): Pode sacrificar consistência por baixa latência (por exemplo, replicação assíncrona, réplicas de leitura).

---

## Aplicação Prática e Configuração

Você não "instala" o teorema CAP, mas configura seus armazenamentos de dados distribuídos para gerenciar seus trade-offs.

### Lógica de Decisão Conceitual (Pseudocódigo)

```python
# High-level logic for handling a request during a detected partition

import config

def handle_write_during_partition(data):
    partition_detected = check_network_health()
    
    if partition_detected:
        if config.CAP_MODE == "CP":
            # Refuse the write to maintain consistency
            raise ServiceUnavailable("Cannot guarantee consistency during partition.")
        elif config.CAP_MODE == "AP":
            # Accept the write locally; resolve conflicts later
            store_with_timestamp(data, node_id=config.NODE_ID)
            return {"status": "accepted", "note": "Eventual consistency in effect."}
    else:
        # Network is healthy -> standard operation
        return normal_write_operation(data)
```

### MongoDB: Ajuste CP/AP por Consulta

```javascript
// CP behavior: Ensure writes are committed to majority before acknowledging
db.inventory.insertOne(
   { item: "journal", qty: 25, status: "A" },
   { writeConcern: { w: "majority", wtimeout: 5000 } }
);

// CP behavior: Read from the primary (strongest consistency)
db.inventory.find({ status: "A" }).readPref("primary");

// AP behavior: Read from any secondary (potential stale data)
db.inventory.find({ status: "A" }).readPref("secondary");

// AP behavior: Allow reads from secondaries if primary is unreachable
db.inventory.find({ status: "A" }).readPref("secondaryPreferred");
```

### Apache Cassandra: Níveis de Consistência Ajustáveis

```cql
-- Strong Consistency (towards CP)
-- Ensures all replicas in the quorum have the same data
SELECT * FROM users WHERE user_id = 123 CONSISTENCY QUORUM;

-- Write with strong consistency
INSERT INTO users (user_id, name) VALUES (123, 'Alice') USING TIMESTAMP 1000;
-- Ensure quorum acknowledged the write
-- Requires consistency level QUORUM or ALL

-- Eventual Consistency (towards AP, lower latency)
SELECT * FROM users WHERE user_id = 123 CONSISTENCY ONE;

-- High Availability, low consistency (AP)
-- Writes acknowledged by just one node
INSERT INTO users (user_id, name) VALUES (456, 'Bob') CONSISTENCY ANY;
```

---

## Quando Escolher CP vs AP

| Cenário | Abordagem Recomendada | Justificativa |
|---|---|---|
| Processamento de pagamentos / Registros financeiros | **CP** | Contagens ou saldos inconsistentes causam perdas financeiras e problemas legais. Indisponibilidade temporária durante uma partição é preferível a gastos duplicados. |
| Registros de saúde / Dados médicos | **CP** | Decisões críticas para a vida dependem de dados completos e precisos. A indisponibilidade é mais segura do que diagnósticos conflitantes ou desatualizados. |
| Dados de sessão de usuário (e-commerce) | **AP** | Os usuários devem poder navegar e adicionar itens ao carrinho mesmo que um datacenter fique offline. Contagens de inventário desatualizadas são um trade-off temporário aceitável. |
| Feeds de redes sociais | **AP** | Os usuários esperam que o site esteja no ar. Um like ausente ou um comentário atrasado é aceitável se significa que o aplicativo permanece responsivo. |
| Entrega de conteúdo / CDNs | **AP** | Servir uma versão em cache ligeiramente desatualizada de uma página é muito preferível a uma página de erro. |
| Armazenamento de metadados / Configuração (ZooKeeper, etcd) | **CP** | A configuração deve ser autoritativa e consistente em todo o cluster. Dividir o cluster em visões inconsistentes é perigoso (split-brain). |

---

## História e Impacto

### Linha do Tempo
- **1998:** Eric Brewer apresenta pela primeira vez a ideia das três propriedades.
- **2000:** Brewer postula formalmente a conjectura no PODC.
- **2002:** Seth Gilbert e Nancy Lynch do MIT publicam "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services", provando formalmente o teorema.
- **Final dos anos 2000:** O teorema influenciou diretamente a arquitetura do **Amazon DynamoDB**, **Google Bigtable**, **Apache Cassandra** e **MongoDB**.
- **Década de 2010:** O movimento NoSQL adota o teorema CAP como princípio primário de design. O PACELC é introduzido para clarificar os trade-offs "sempre", não apenas durante partições.
- **Década de 2020:** Bancos de dados SQL distribuídos modernos (Spanner, CockroachDB, YugabyteDB) tentam ultrapassar os limites, buscando "C e A" na maior parte do tempo, reduzindo agressivamente a probabilidade e duração das partições (por exemplo, usando TrueTime / sincronização rigorosa de relógios).

### Insight Chave
O teorema CAP foi revolucionário porque deu aos arquitetos uma linguagem formal para discutir trade-offs. Antes do CAP, os operadores esperavam que bancos de dados distribuídos se comportassem exatamente como os monolíticos. O teorema forçou a indústria a admitir que **consistência forte tem um custo**, e esse custo é muitas vezes pago em disponibilidade durante falhas.

---

## Limitações e Críticas

1.  **Falso Binário:** Críticos argumentam que "C, A, P" não são propriedades binárias. Existem graus de consistência (forte, causal, eventual, leia-suas-escritas) e disponibilidade.
2.  **Ignorando Latência:** O teorema CAP original não aborda explicitamente os trade-offs quando a rede está saudável (isso é tratado pelo PACELC).
3.  **CA é uma Armadilha:** Muitos engenheiros procuram sistemas "CA" distribuídos. Na realidade, qualquer sistema que replica dados por uma rede é tolerante a partições por necessidade. Rotular um sistema puramente como "CA" é muitas vezes marketing, não arquitetura.
4.  **Mitigação Moderna:** Bancos de dados como **Google Spanner** usam relógios atômicos e a API TrueTime para alcançar consistência forte e alta disponibilidade simultaneamente *na maioria do tempo*, reduzindo o cenário de "escolha 2 de 3" a um caso extremo raro.

---

## Veja Também

- **Teorema PACELC** — A extensão moderna do CAP incluindo trade-offs de latência.
- **Consistência Eventual** — O modelo de consistência no qual a maioria dos sistemas AP se baseia.
- **ACID vs BASE** — ACID (Atomicidade, Consistência, Isolamento, Durabilidade) vs BASE (Basicamente Disponível, Estado Flexível, Consistência Eventual).
- **Eric Brewer** — Propositor original do teorema.
- **Design de Sistemas Distribuídos** — Sharding, replicação, algoritmos de consenso (Raft, Paxos).
- **CRDTs (Conflict-free Replicated Data Types)** — Estruturas de dados que resolvem conflitos naturalmente em sistemas AP.