---
title: PlanetScale: Plataforma de Banco de Dados MySQL Serverless
description: Uma plataforma de banco de dados totalmente gerenciada e compatível com MySQL, construída sobre o Vitess, que introduz branch de banco de dados e mudanças de esquema sem bloqueio para fluxos de trabalho de desenvolvimento modernos.
created: 2026-06-22
tags:
  - database
  - mysql
  - vitess
  - serverless
  - schema-migration
  - devops
  - dbaas
  - branching
status: draft
---

# PlanetScale

## Introdução

PlanetScale, fundado em 2018 pelos principais criadores do Vitess (Sugu Sougoumarane, Jiten Vaidya e Morgan Goeller), é a plataforma de banco de dados compatível com MySQL construída sobre o sistema de cluster de banco de dados de código aberto que alimenta o YouTube. Ela reimagina o gerenciamento de banco de dados aplicando **fluxos de trabalho no estilo Git** — branch de banco de dados e Deploy Requests — a esquemas e dados.

Essa abordagem elimina os gargalos tradicionais e o tempo de inatividade associados a migrações de esquema, tornando as alterações de banco de dados tão seguras, revisáveis e iterativas quanto as alterações de código. PlanetScale é um serviço totalmente gerenciado que lida com replicação, backups, sharding e alta disponibilidade, além de oferecer suporte a uma camada de computação serverless que escala a zero e desperta instantaneamente ao receber uma conexão.

## Conceitos Principais

### Branch de Banco de Dados
Assim como `git branch` permite o desenvolvimento isolado de código, `pscale branch create` cria uma cópia isolada e totalmente funcional do seu banco de dados (incluindo dados e esquema) na infraestrutura do PlanetScale.

- **Crie branch de qualquer ponto:** Crie um branch a partir de `main` ou de um snapshot anterior.
- **Dados e Esquema:** O branch contém um snapshot completo, permitindo testes altamente realistas.
- **Natureza Efêmera:** Os branches são projetados para serem descartados assim que seu propósito é cumprido, evitando desvio de esquema.

### Deploy Requests (DRs)
A contrapartida do PlanetScale para um Pull Request. Quando você estiver satisfeito com as alterações de esquema em um branch, você abre um Deploy Request. Isso gera um diff, permite a revisão e realiza a mesclagem como uma **migração de esquema online sem bloqueio** (usando Vitess VReplication).

### Computação Serverless
PlanetScale desacopla computação do armazenamento. Os bancos de dados têm um estado de suspensão quando nenhuma conexão está ativa. As conexões ativam o banco de dados instantaneamente, eliminando custos de computação ociosa.

## Começando

### Instalação
A principal interface do desenvolvedor é a CLI `pscale`.

**macOS:**
```bash
brew install planetscale/tap/pscale
```

**Linux / Windows:**
```bash
curl -fsSL https://planetscale.com/install.sh | sh
```

### Autenticação
```bash
pscale auth login
```

### Criando um Banco de Dados
```bash
pscale database create my-app
```

### Trabalhando com Branches

**Criar um branch de funcionalidade (copia esquema e dados do main):**
```bash
pscale branch create my-app feature-user-profile
```

**Conectar ao branch:**
```bash
pscale connect my-app feature-user-profile --port 3309
```
Isso executa um proxy local. Sua aplicação se conecta a `127.0.0.1:3309`. O proxy lida com a autenticação automaticamente.

**Executar migrações de esquema no seu branch:**
Use qualquer cliente MySQL, ORM ou ferramenta de migração (ex.: `mysql2`, `Prisma`, `SQLAlchemy`).
```sql
ALTER TABLE users ADD COLUMN bio TEXT;
```

### O Fluxo do Deploy Request
Depois de testar completamente as alterações de esquema no branch:

```bash
# Cria o Deploy Request
pscale deploy-request create my-app feature-user-profile

# Lista os deploy requests
pscale deploy-request list my-app

# Implanta o request (após revisão)
pscale deploy-request deploy my-app <deploy-number>

# Limpa o branch
pscale branch delete my-app feature-user-profile --force
```

A implantação aplica a alteração de esquema ao `main` *sem travar a tabela ou causar tempo de inatividade*.

## Recursos Principais em Detalhes

### Mudanças de Esquema Sem Bloqueio (DDL Online)
As instruções tradicionais `ALTER TABLE` no MySQL frequentemente travam as tabelas. PlanetScale usa o **Online DDL** do Vitess via VReplication. Ele cria uma tabela sombra, copia dados incrementalmente e faz a transição de forma transparente.

**Exemplo de Comando:**
```bash
pscale deploy-request deploy my-app 1
```
A produção permanece totalmente operacional mesmo durante migrações grandes e de longa duração.

### Pool de Conexões
O pool de conexões integrado no lado do servidor gerencia picos de conexão. Ao usar o `pscale connect`, o proxy local também faz pooling de conexões. Para produção, conecte-se diretamente ao endereço do servidor do PlanetScale.

### Sharding Horizontal (Vitess)
Para conjuntos de dados extremamente grandes, o PlanetScale usa o sharding por intervalo de chaves do Vitess para distribuir dados de forma transparente entre várias instâncias MySQL. Nenhuma alteração na aplicação é necessária.

### Alta Disponibilidade e Replicação Global
A alta disponibilidade é integrada. O PlanetScale oferece réplicas entre regiões e failover automático com um SLA de disponibilidade de 99,99%.

## Casos de Uso Práticos

### Integração CI/CD
Crie um branch de banco de dados isolado para cada pull request para executar testes de integração com dados reais de produção.
```bash
pscale branch create my-app ci-pr-123 --from main
pscale connect my-app ci-pr-123 --port 3309 &
# Execute os testes de integração aqui
pscale branch delete my-app ci-pr-123 --force
```

### Testes de Pré-Produção
Permita que o QA execute testes destrutivos ou de carga em um branch totalmente realista sem corromper dados de produção.

### Revisão de Esquema
Os membros da equipe revisam o diff SQL exato em um Deploy Request antes da mesclagem, permitindo fluxos de trabalho "banco de dados como código".

### Ambientes Efêmeros
Combine `pscale branch create/destroy` com ferramentas de engenharia de plataforma (ex.: operadores Kubernetes, Terraform) para fornecer um ambiente full-stack por desenvolvedor ou por funcionalidade.

## Limitações e Advertências

Embora poderoso, a fundação Vitess do PlanetScale introduz algumas peculiaridades de compatibilidade com MySQL:

- **Sem Stored Procedures ou Triggers:** A camada de proxy do Vitess não oferece suporte a esses recursos.
- **Chaves Estrangeiras:** Em beta (devem ser habilitadas por banco de dados). Ainda não recomendadas para caminhos críticos de produção.
- **`LOCK TABLES` / `UNLOCK TABLES`:** Não suportado.
- **`GET_LOCK()` / `RELEASE_LOCK()`:** Não suportado.
- **Subconsultas e `JOIN`s:** A maioria é suportada, mas subconsultas correlacionadas altamente complexas ou instruções não determinísticas podem se comportar de forma diferente.
- **`ALTER TABLE` direto em Produção:** O fluxo de trabalho do Deploy Request é a *única* maneira segura de fazer alterações de esquema em produção. Executar `ALTER TABLE` diretamente em um branch de produção via `pscale connect` é fortemente desencorajado.

> **Nota do Desenvolvedor:** Sempre use o fluxo de trabalho Deploy Request para alterações de esquema em **produção**. Para branches de desenvolvimento, o `ALTER TABLE` direto é seguro e rápido.

## Modelo de Preços

PlanetScale opera como um produto SaaS com um plano gratuito generoso. O preço é baseado em armazenamento de linhas e leituras/gravações de linhas.

| Plano | Preço | Armazenamento de Linhas | Computação | Branches |
|---|---|---|---|---|
| **Free** | $0/mês | 5 GB | 10M leituras de linhas/mês, 1M gravações de linhas/mês | Até 3 |
| **Scaler** | $39/mês (base) | 10 GB | 100M leituras de linhas, 10M gravações de linhas | Até 10 |
| **Business** | Custom | Custom | Custom | Custom |

*Os preços podem mudar; sempre verifique na [página de preços do PlanetScale](https://planetscale.com/pricing).*

## Melhores Práticas

- **Nomeação de Branches:** Use um namespace consistente (ex.: `feature/*`, `hotfix/*`, `ci/*`).
- **Destruir Branches Obsoletos:** Limpe regularmente os branches para evitar custos de armazenamento.
  ```bash
  pscale branch delete my-app stale-branch --force
  ```
- **Monitorar Desempenho:** Use o painel do PlanetScale para monitorar o desempenho de consultas, consultas lentas e uso de conexões. Os recursos de query explain e insights são poderosos.
- **Paridade de Ambiente:** Mantenha o `main` como um ambiente de produção imaculado. As equipes de desenvolvimento trabalham exclusivamente em branches.
- **Evitar Consultas Pesadas em Proxies de Branches de Produção:** Embora um branch seja um snapshot, executar consultas analíticas massivas em um branch conectado ao mesmo cluster subjacente que a produção pode impactar o I/O compartilhado.

## Solução de Problemas

**Conexão recusada no proxy:**
```bash
pscale connect my-app main
```
Certifique-se de que nenhum outro serviço está em execução na porta. Use `--port` para especificar uma alternativa.

**Falha na alteração de esquema:**
Verifique os logs do Deploy Request no painel do PlanetScale ou use:
```bash
pscale deploy-request show my-app <deploy-number>
```

**Alta latência de consulta:**
Verifique os limites do pool de conexões. Considere adicionar um índice ao branch antes de mesclar:
```sql
ALTER TABLE users ADD INDEX idx_email (email);
```

## Comparação com Alternativas

| Recurso | PlanetScale | Neon (Postgres) | Supabase (Postgres) | RDS (MySQL) |
|---|---|---|---|---|
| **Branch de Dados** | Instantâneo, dados completos | Instantâneo, dados completos | Branching via SQL | Snapshots manuais |
| **Serverless** | Sim (sleep/wake) | Sim (sleep/wake) | Sim (auto-suspend) | Não (Sempre Ativo) |
| **Migrações de Esquema** | Sem bloqueio (DDL Online) | Branching + `pgroll` | Branching + migrations | Manual |
| **Sharding** | Automático (Vitess) | Não | Não | Manual (Sharding) |
| **Fluxo CI de Migração** | Excelente (Deploy Requests) | Excelente | Bom | Ruim |

**Quando escolher o PlanetScale:**
Você precisa de compatibilidade com MySQL, branch de banco de dados para alterações e testes de esquema complexos e escalonamento horizontal automático.

**Quando evitar o PlanetScale:**
Você depende muito de stored procedures, triggers ou recursos avançados do MySQL (ex.: `GET_LOCK()`). Nesse caso, RDS ou uma solução MySQL gerenciada padrão pode ser mais adequada.

## Resumo

O PlanetScale revoluciona a experiência de desenvolvimento MySQL ao trazer fluxos de trabalho no estilo Git para a camada de banco de dados. Sua capacidade de criar branches instantâneos de dados e esquema, combinada com Deploy Requests sem bloqueio, permite que as equipes iterem sobre esquemas de banco de dados com a mesma segurança e velocidade que o código da aplicação. Construído sobre o motor Vitess testado em batalha, ele fornece escalabilidade de nível YouTube sem a sobrecarga operacional.