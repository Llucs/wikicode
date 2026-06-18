---
title: Neon – Serverless PostgreSQL Platform
description: Neon is an open-source serverless PostgreSQL database that separates compute from storage, providing instant branching, scale‑to‑zero, and bottomless storage for modern applications.
created: 2026-06-18
tags:
  - serverless
  - postgres
  - database
  - branching
  - cloud
status: draft
---

# Neon – Serverless PostgreSQL Platform

Neon is an open‑source, serverless PostgreSQL platform that rebuilds the classic database architecture on a cloud‑native foundation. By completely decoupling compute (query processing) from storage (data persistence), Neon offers features previously available only in proprietary systems like Amazon Aurora – but for the entire Postgres ecosystem. With instant branching, automatic scale‑to‑zero, and bottomless storage, Neon is designed for modern development workflows and serverless applications.

---

## Why Neon?

| Challenge | Neon Solution |
|-----------|---------------|
| **Expensive idle databases** | Compute endpoints scale to zero after inactivity; you only pay for active compute. |
| **Slow development cycles** | Instant branching gives every developer/PR its own full‑fidelity database fork. |
| **Storage provisioning & cost** | Bottomless storage backed by object stores (e.g., S3); no manual capacity planning. |
| **Serverless/edge compatibility** | Cold‑start times ~500 ms, paired with PgBouncer pooling for ephemeral compute. |
| **Vector workloads** | Full support for `pgvector` and PostGIS; run AI embeddings directly in Postgres. |

---

## Key Features

### 1. Instant Branching

Using copy‑on‑write technology, Neon can create a branch of a terabyte‑scale database in milliseconds. This is invaluable for:

- **Development sandboxes** – each developer gets an isolated clone of production.
- **CI/CD pipelines** – run integration tests against a branch that mirrors production data.
- **Schema migrations** – test breaking changes without risk.

```bash
# Create a new branch from the main branch
npx neonctl branches create --name feature/ai-search
```

### 2. Scale‑to‑Zero

Compute endpoints automatically suspend after a period of inactivity. When a new connection arrives, the endpoint resumes in approximately 500 ms (cold start). This eliminates costs for idle or low‑traffic databases.

```sql
-- No configuration needed – scale‑to‑zero is automatic.
-- Connect and the endpoint wakes up transparently.
```

### 3. Bottomless Storage

Storage is handled by a separate engine (Pageserver + Safekeepers) backed by cheap object storage. You never need to provision disks or worry about filling up.

### 4. Full PostgreSQL Compatibility

Neon supports PostgreSQL 14–17, including all major extensions:

- `pgvector` – vector similarity search for embeddings.
- `PostGIS` – geospatial queries.
- `pg_cron`, `pg_stat_statements`, etc.

Your existing tools and drivers work unchanged.

### 5. Transparent Connection Pooling

PgBouncer is integrated at the proxy level, so you get efficient connection handling without any application configuration.

---

## Quick Start

### Option A: Cloud (Managed)

1. Sign up at [console.neon.tech](https://console.neon.tech) (generous free tier included).
2. Create a project via the UI or CLI:

   ```bash
   # Install the Neon CLI
   npx neonctl

   # Create a project (first time: interactive)
   npx neonctl create-project

   # Get the connection string for the main branch
   npx neonctl connection-string
   ```

### Option B: Self‑Hosted

Clone the open‑source repository and deploy using Docker Compose or Helm.

```bash
git clone https://github.com/neondatabase/neon.git
cd neon
docker compose up -d
```

Refer to the [official self‑hosting guide](https://neon.tech/docs/self-host) for production deployments.

---

## Usage Examples

### Connect and Run Queries

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

### Create and Switch Branches

```bash
# List branches
npx neonctl branches list

# Create a branch from a specific point in time (time travel)
npx neonctl branches create --from main --time "2026-06-17T12:00:00Z"

# Use a branch: get its connection string
npx neonctl connection-string --branch feature/ai-search
```

### Integrate with Vercel / Netlify

Because Neon supports HTTP connections via `@neondatabase/serverless`, you can connect from edge functions:

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

## Architecture in Brief

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

- **Compute nodes** are stateless and can be scaled horizontally.
- **Pageserver** handles page serving, checkpointing, and branching (copy‑on‑write).
- **Safekeeper** ensures WAL durability before acknowledgment.

---

## Pricing Model

Neon is **usage‑based**:

| Resource | Free Tier | Paid Tier |
|----------|-----------|-----------|
| Compute (active) | 10 hours/month | Pay per compute‑hour |
| Storage | 500 MB | $0.12/GB/month |
| Branching | Unlimited | Unlimited |
| Connection pooling | Yes | Yes |

Scale‑to‑zero means you only pay for compute when your application is actually serving queries.

---

## Limitations & Gotchas

- **Cold start latency** – Although ~500 ms, it can be noticeable in latency‑sensitive functions. Use keep‑alive connections or always‑on endpoints for critical paths.
- **Feature parity** – Single‑server deployments only (no native sharding). For multi‑region active‑active, you may still need external replication strategies.
- **Free tier cap** – The 10 compute‑hour cap can be consumed quickly if several projects remain active.

---

## Resources

- [Official Documentation](https://neon.tech/docs)
- [GitHub Repository](https://github.com/neondatabase/neon)
- [Neon Discord Community](https://discord.gg/neon)
- [Blog – Understanding Neon’s Architecture](https://neon.tech/blog/architecture)

Neon transforms PostgreSQL into a true serverless database, making it an ideal choice for modern applications, CI/CD, and AI/vector workloads. Its combination of instant branching, scale‑to‑zero, and full Postgres compatibility has made it one of the most popular infrastructure projects of 2024–2026.