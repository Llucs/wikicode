---
title: Neon – Plataforma PostgreSQL Serverless
description: Neon é um banco de dados PostgreSQL serverless de código aberto que separa computação do armazenamento, oferecendo branching instantâneo, scale‑to‑zero e armazenamento ilimitado para aplicações modernas.
created: 2026-06-18
tags:
  - serverless
  - postgres
  - database
  - branching
  - cloud
status: draft
---

# Neon – Plataforma PostgreSQL Serverless

Neon é uma plataforma PostgreSQL serverless e de código aberto que reconstrói a arquitetura clássica de banco de dados sobre uma fundação cloud‑native. Ao desacoplar completamente a computação (processamento de consultas) do armazenamento (persistência de dados), a Neon oferece recursos anteriormente disponíveis apenas em sistemas proprietários como Amazon Aurora – mas para todo o ecossistema Postgres. Com instant branching, scale‑to‑zero automático e bottomless storage, a Neon foi projetada para fluxos de trabalho modernos de desenvolvimento e aplicações serverless.

---

## Por que Neon?

| Desafio | Solução Neon |
|---------|--------------|
| **Bancos de dados ociosos caros** | Os endpoints de computação escalam a zero após inatividade; você paga apenas pela computação ativa. |
| **Ciclos de desenvolvimento lentos** | O instant branching dá a cada desenvolvedor/PR seu próprio fork de banco de dados com fidelidade total. |
| **Provisionamento e custo de armazenamento** | Bottomless storage apoiado por object stores (ex.: S3); sem planejamento manual de capacidade. |
| **Compatibilidade com Serverless/Edge** | Tempos de cold start ~500 ms, combinados com pooling PgBouncer para computação efêmera. |
| **Cargas de trabalho vetoriais** | Suporte completo para `pgvector` e PostGIS; execute embeddings de IA diretamente no Postgres. |

---

## Principais Recursos

### 1. Branching Instantâneo

Usando tecnologia copy‑on‑write, a Neon pode criar um branch de um banco de dados em escala de terabyte em milissegundos. Isso é inestimável para:

- **Sandboxes de desenvolvimento** – cada desenvolvedor obtém um clone isolado da produção.
- **Pipelines CI/CD** – execute testes de integração contra um branch que espelha os dados de produção.
- **Migrações de esquema** – teste alterações significativas sem risco.

```bash
# Create a new branch from the main branch
npx neonctl branches create --name feature/ai-search
```

### 2. Scale‑to‑Zero

Os endpoints de computação suspendem automaticamente após um período de inatividade. Quando uma nova conexão chega, o endpoint retoma em aproximadamente 500 ms (cold start). Isso elimina custos para bancos de dados ociosos ou com baixo tráfego.

```sql
-- No configuration needed – scale‑to‑zero is automatic.
-- Connect and the endpoint wakes up transparently.
```

### 3. Bottomless Storage

O armazenamento é gerenciado por um motor separado (Pageserver + Safekeepers) apoiado por object storage barato. Você nunca precisa provisionar discos ou se preocupar em ficar sem espaço.

### 4. Compatibilidade Total com PostgreSQL

A Neon oferece suporte ao PostgreSQL 14–17, incluindo todas as principais extensões:

- `pgvector` – busca de similaridade vetorial para embeddings.
- `PostGIS` – consultas geoespaciais.
- `pg_cron`, `pg_stat_statements`, etc.

Suas ferramentas e drivers existentes funcionam sem alterações.

### 5. Pooling de Conexões Transparente

O PgBouncer é integrado no nível do proxy, então você obtém um gerenciamento eficiente de conexões sem nenhuma configuração na aplicação.

---

## Início Rápido

### Opção A: Nuvem (Gerenciada)

1. Cadastre-se em [console.neon.tech](https://console.neon.tech) (inclui um generoso nível gratuito).
2. Crie um projeto via interface ou CLI:

   ```bash
   # Install the Neon CLI
   npx neonctl

   # Create a project (first time: interactive)
   npx neonctl create-project

   # Get the connection string for the main branch
   npx neonctl connection-string
   ```

### Opção B: Auto‑hospedado

Clone o repositório de código aberto e implante usando Docker Compose ou Helm.

```bash
git clone https://github.com/neondatabase/neon.git
cd neon
docker compose up -d
```

Consulte o [guia oficial de auto‑hospedagem](https://neon.tech/docs/self-host) para implantações em produção.

---

## Exemplos de Uso

### Conectar e Executar Consultas

```bash
psql "postgresql://user:pass@ep-cool-123456.us-east-2.aws.neon.tech/neondb"
```

```sql
-- Standard Postgres – everything works
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    payload JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- pgvector example
CREATE EXTENSION vector;
CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    embedding vector(1024)
);
```

### Criar e Alternar Branches

```bash
# List branches
npx neonctl branches list

# Create a branch from a specific point in time (time travel)
npx neonctl branches create --from main --time "2026-06-17T12:00:00Z"

# Use a branch: get its connection string
npx neonctl connection-string --branch feature/ai-search
```

### Integrar com Vercel / Netlify

Como a Neon suporta conexões HTTP via `@neondatabase/serverless`, você pode conectar a partir de edge functions:

```javascript
// Example: Next.js API route
import { neon } from '@neondatabase/serverless';

export default async function handler(req, res) {
  const sql = neon(process.env.DATABASE_URL);
  const result = await sql`SELECT * FROM events`;
  res.json(result);
}
```

---

## Arquitetura Resumida

```
 Application
    |
    | (PostgreSQL protocol)
    |
 Proxy  ─── PgBouncer (connection pooling)
    |
 Compute Node (Stateless Postgres process)
    |
 Pageserver (Storage engine)
    |
 Safekeeper (WAL persistence)
    |
 Object Store (S3, GCS, etc.)
```

- **Nós de computação** são stateless e podem ser escalados horizontalmente.
- **Pageserver** lida com serviço de páginas, checkpointing e branching (copy‑on‑write).
- **Safekeeper** garante a durabilidade do WAL antes da confirmação.

---

## Modelo de Preços

Neon é **baseado em uso**:

| Recurso | Nível Gratuito | Nível Pago |
|---------|----------------|------------|
| Computação (ativa) | 10 horas/mês | Pague por hora de computação |
| Armazenamento | 500 MB | $0.12/GB/mês |
| Branching | Ilimitado | Ilimitado |
| Pooling de conexões | Sim | Sim |

Scale‑to‑zero significa que você paga apenas pela computação quando sua aplicação está realmente servindo consultas.

---

## Limitações e Armadilhas

- **Latência de cold start** – Embora ~500 ms, pode ser perceptível em funções sensíveis à latência. Use conexões keep‑alive ou endpoints sempre ativos para caminhos críticos.
- **Paridade de recursos** – Apenas implantações de servidor único (sem sharding nativo). Para active‑active multirregião, você ainda pode precisar de estratégias de replicação externas.
- **Limite do nível gratuito** – O limite de 10 horas de computação pode ser consumido rapidamente se vários projetos permanecerem ativos.

---

## Recursos

- [Documentação Oficial](https://neon.tech/docs)
- [Repositório no GitHub](https://github.com/neondatabase/neon)
- [Comunidade Neon no Discord](https://discord.gg/neon)
- [Blog – Entendendo a Arquitetura da Neon](https://neon.tech/blog/architecture)

A Neon transforma o PostgreSQL em um banco de dados verdadeiramente serverless, tornando‑o uma escolha ideal para aplicações modernas, CI/CD e workloads de IA/vetoriais. Sua combinação de instant branching, scale‑to‑zero e compatibilidade total com Postgres fez dela um dos projetos de infraestrutura mais populares de 2024–2026.