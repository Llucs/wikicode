---
title: PlanetScale: Serverless MySQL Database Platform
description: A fully managed MySQL-compatible database platform built on Vitess that introduces database branching and non-blocking schema changes for modern development workflows.
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

## Introduction

PlanetScale, founded in 2018 by the core creators of Vitess (Sugu Sougoumarane, Jiten Vaidya, and Morgan Goeller), is the MySQL-compatible database platform built on the open-source database clustering system that powers YouTube. It reimagines database management by applying **Git-style workflows**—database branching and Deploy Requests—to schemas and data.

This approach eliminates the traditional bottlenecks and downtime associated with schema migrations, making database changes as safe, reviewable, and iterative as code changes. PlanetScale is a fully managed service that handles replication, backups, sharding, and high availability, while supporting a serverless compute layer that scales to zero and instantly wakes upon connection.

## Core Concepts

### Database Branching
Just as `git branch` allows isolated code development, `pscale branch create` creates an isolated, fully functional copy of your database (including data and schema) on PlanetScale’s infrastructure.

- **Branch from any point:** Create a branch from `main` or a previous snapshot.
- **Data & Schema:** The branch contains a complete snapshot, enabling highly realistic testing.
- **Ephemeral Nature:** Branches are designed to be thrown away once their purpose is fulfilled, preventing schema drift.

### Deploy Requests (DRs)
PlanetScale’s counterpart to a Pull Request. When you are satisfied with schema changes on a branch, you open a Deploy Request. This generates a diff, enables review, and performs the merge as a **non-blocking online schema migration** (using Vitess VReplication).

### Serverless Compute
PlanetScale decouples compute from storage. Databases have a "sleep" state when no connections are active. Connections wake the database instantly, eliminating idle compute costs.

## Getting Started

### Installation
The primary developer interface is the `pscale` CLI.

**macOS:**
```bash
brew install planetscale/tap/pscale
```

**Linux / Windows:**
```bash
curl -fsSL https://planetscale.com/install.sh | sh
```

### Authentication
```bash
pscale auth login
```

### Creating a Database
```bash
pscale database create my-app
```

### Working with Branches

**Create a feature branch (copies schema and data from main):**
```bash
pscale branch create my-app feature-user-profile
```

**Connect to the branch:**
```bash
pscale connect my-app feature-user-profile --port 3309
```
This runs a local proxy. Your application connects to `127.0.0.1:3309`. The proxy handles authentication automatically.

**Run schema migrations against your branch:**
Use any MySQL client, ORM, or migration tool (e.g., `mysql2`, `Prisma`, `SQLAlchemy`).
```sql
ALTER TABLE users ADD COLUMN bio TEXT;
```

### The Deploy Request Flow
Once you’ve thoroughly tested schema changes on the branch:

```bash
# Create the Deploy Request
pscale deploy-request create my-app feature-user-profile

# List deploy requests
pscale deploy-request list my-app

# Deploy the request (after review)
pscale deploy-request deploy my-app <deploy-number>

# Clean up the branch
pscale branch delete my-app feature-user-profile --force
```

The deployment applies the schema change to `main` *without locking the table or causing downtime*.

## Key Features in Depth

### Non-Blocking Schema Changes (Online DDL)
Traditional `ALTER TABLE` statements in MySQL often lock tables. PlanetScale uses Vitess’s **Online DDL** via VReplication. It creates a shadow table, copies data incrementally, and switches over transparently.

**Command Example:**
```bash
pscale deploy-request deploy my-app 1
```
Production remains fully operational even during large, long-running migrations.

### Connection Pooling
Built-in server-side connection pooling manages connection spikes. When using `pscale connect`, the local proxy also pools connections. For production, connect directly to the PlanetScale server address.

### Horizontal Sharding (Vitess)
For extremely large datasets, PlanetScale uses Vitess’s key-range sharding to distribute data across many MySQL instances transparently. No application changes are needed.

### High Availability & Global Replication
High availability is built-in. PlanetScale provides cross-region replicas and automatic failover with a 99.99% uptime SLA.

## Practical Use Cases

### CI/CD Integration
Spin up an isolated database branch for every pull request to run integration tests against real production data.
```bash
pscale branch create my-app ci-pr-123 --from main
pscale connect my-app ci-pr-123 --port 3309 &
# Run integration tests here
pscale branch delete my-app ci-pr-123 --force
```

### Pre-Production Testing
Let QA run destructive or load tests on a fully realistic branch without corrupting production data.

### Schema Review
Team members review the exact SQL diff in a Deploy Request before merge, enabling "database as code" workflows.

### Ephemeral Environments
Combine `pscale branch create/destroy` with platform engineering tools (e.g., Kubernetes operators, Terraform) to provide a full-stack environment per developer or per feature.

## Limitations and Caveats

While powerful, PlanetScale’s Vitess foundation introduces some MySQL-compatibility quirks:

- **No Stored Procedures or Triggers:** The Vitess proxy layer does not support these.
- **Foreign Keys:** In beta (must be enabled per-database). Not recommended for critical production paths yet.
- **`LOCK TABLES` / `UNLOCK TABLES`:** Not supported.
- **`GET_LOCK()` / `RELEASE_LOCK()`:** Not supported.
- **Subqueries and `JOIN`s:** Most are supported, but highly complex correlated subqueries or non-deterministic statements may behave differently.
- **Direct `ALTER TABLE` on Production:** The Deploy Request workflow is the *only* safe way to make schema changes on production. Running `ALTER TABLE` directly on a production branch via `pscale connect` is heavily discouraged.

> **Developer Note:** Always use the Deploy Request workflow for **production** schema changes. For development branches, direct `ALTER TABLE` is safe and fast.

## Pricing Model

PlanetScale operates as a SaaS product with a generous free tier. Pricing is based on row storage and row reads/writes.

| Tier | Price | Row Storage | Compute | Branches |
|---|---|---|---|---|
| **Free** | $0/mo | 5 GB | 10M row reads/mo, 1M row writes/mo | Up to 3 |
| **Scaler** | $39/mo (base) | 10 GB | 100M row reads, 10M row writes | Up to 10 |
| **Business** | Custom | Custom | Custom | Custom |

*Pricing specifics can change; always verify on the [PlanetScale pricing page](https://planetscale.com/pricing).*

## Best Practices

- **Branch Naming:** Use a consistent namespace (e.g., `feature/*`, `hotfix/*`, `ci/*`).
- **Destroy Stale Branches:** Regularly clean up branches to avoid storage costs.
  ```bash
  pscale branch delete my-app stale-branch --force
  ```
- **Monitor Performance:** Use the PlanetScale dashboard to monitor query performance, slow queries, and connection usage. The query explain and insights features are powerful.
- **Environment Parity:** Keep `main` as a pristine production environment. Dev teams work exclusively on branches.
- **Avoid Heavy Queries on Production Branch Proxies:** While a branch is a snapshot, running massive analytical queries on a branch connected to the same underlying cluster as production can impact shared I/O.

## Troubleshooting

**Connection refused in proxy:**
```bash
pscale connect my-app main
```
Ensure no other service is running on the port. Use `--port` to specify an alternative.

**Schema change failed:**
Check the Deploy Request logs in the PlanetScale dashboard, or use:
```bash
pscale deploy-request show my-app <deploy-number>
```

**High query latency:**
Verify connection pooling limits. Consider adding an index to the branch before merging:
```sql
ALTER TABLE users ADD INDEX idx_email (email);
```

## Comparison to Alternatives

| Feature | PlanetScale | Neon (Postgres) | Supabase (Postgres) | RDS (MySQL) |
|---|---|---|---|---|
| **Branching** | Instant, full data | Instant, full data | Branching via SQL | Manual snapshots |
| **Serverless** | Yes (sleep/wake) | Yes (sleep/wake) | Yes (auto-suspend) | No (Always On) |
| **Schema Migrations** | Non-blocking (Online DDL) | Branching + `pgroll` | Branching + migrations | Manual |
| **Sharding** | Automatic (Vitess) | No | No | Manual (Sharding) |
| **Migration CI Flow** | Excellent (Deploy Requests) | Excellent | Good | Poor |

**When to choose PlanetScale:**
You need MySQL compatibility, database branching for complex schema changes and testing, and automatic horizontal scaling.

**When to avoid PlanetScale:**
You heavily rely on stored procedures, triggers, or advanced MySQL internals (e.g., `GET_LOCK()`). In that case, RDS or a standard managed MySQL solution might be a better fit.

## Summary

PlanetScale revolutionizes the MySQL development experience by bringing Git-like workflows to the database layer. Its ability to instantly branch data and schema, coupled with non-blocking Deploy Requests, allows teams to iterate on database schemas with the same safety and velocity as their application code. Built on the battle-tested Vitess engine, it provides YouTube-grade scalability without the operational overhead.