---
title: Neon – Plateforme PostgreSQL Serverless
description: Neon est une base de données PostgreSQL serverless open‑source qui sépare le compute du storage, offrant l'instant branching, le scale‑to‑zero et le bottomless storage pour les applications modernes.
created: 2026-06-18
tags:
  - serverless
  - postgres
  - database
  - branching
  - cloud
status: draft
---

# Neon – Plateforme PostgreSQL Serverless

Neon est une plateforme PostgreSQL serverless open‑source qui reconstruit l'architecture classique des bases de données sur une base cloud‑native. En découplant complètement le compute (traitement des requêtes) du storage (persistance des données), Neon offre des fonctionnalités auparavant disponibles uniquement dans des systèmes propriétaires comme Amazon Aurora – mais pour l'ensemble de l'écosystème Postgres. Avec l'instant branching, le scale‑to‑zero automatique et le bottomless storage, Neon est conçu pour les flux de développement modernes et les applications serverless.

---

## Pourquoi Neon ?

| Challenge | Solution Neon |
|-----------|---------------|
| **Bases de données inactives coûteuses** | Les endpoints de compute se réduisent à zéro après inactivité ; vous ne payez que pour le compute actif. |
| **Cycles de développement lents** | L'instant branching donne à chaque développeur/PR sa propre fork de base de données full‑fidelity. |
| **Provisionnement et coût du stockage** | Bottomless storage soutenu par des object stores (ex. S3) ; aucune planification manuelle de capacité. |
| **Compatibilité Serverless/edge** | Temps de cold‑start ~500 ms, associé au pooling PgBouncer pour le compute éphémère. |
| **Charges de travail vectorielles** | Support complet de `pgvector` et PostGIS ; exécutez des embeddings AI directement dans Postgres. |

---

## Key Features

### 1. Instant Branching

Grâce à la technologie copy‑on‑write, Neon peut créer une branche d'une base de données à l'échelle du téraoctet en quelques millisecondes. Cela est inestimable pour :

- **Bacs à sable de développement** – chaque développeur obtient un clone isolé de la production.
- **Pipelines CI/CD** – exécutez des tests d'intégration sur une branche qui reflète les données de production.
- **Migrations de schéma** – testez des modifications potentiellement cassantes sans risque.

```bash
# Create a new branch from the main branch
npx neonctl branches create --name feature/ai-search
```

### 2. Scale‑to‑Zero

Les endpoints de compute se suspendent automatiquement après une période d'inactivité. Lorsqu'une nouvelle connexion arrive, l'endpoint reprend en environ 500 ms (cold start). Cela élimine les coûts pour les bases de données inactives ou à faible trafic.

```sql
-- No configuration needed – scale‑to‑zero is automatic.
-- Connect and the endpoint wakes up transparently.
```

### 3. Bottomless Storage

Le storage est géré par un moteur séparé (Pageserver + Safekeepers) soutenu par un object storage peu coûteux. Vous n'avez jamais besoin de provisionner des disques ni de vous soucier de leur saturation.

### 4. Compatibilité PostgreSQL Complète

Neon prend en charge PostgreSQL 14–17, y compris toutes les extensions majeures :

- `pgvector` – recherche de similarité vectorielle pour les embeddings.
- `PostGIS` – requêtes géospatiales.
- `pg_cron`, `pg_stat_statements`, etc.

Vos outils et pilotes existants fonctionnent sans modification.

### 5. Pooling de Connexions Transparent

PgBouncer est intégré au niveau du proxy, ce qui vous permet d'obtenir une gestion efficace des connexions sans configuration d'application.

---

## Démarrage Rapide

### Option A : Cloud (Managed)

1. Inscrivez-vous sur [console.neon.tech](https://console.neon.tech) (généreux free tier inclus).
2. Créez un projet via l'interface utilisateur ou la CLI :

   ```bash
   # Install the Neon CLI
   npx neonctl

   # Create a project (first time: interactive)
   npx neonctl create-project

   # Get the connection string for the main branch
   npx neonctl connection-string
   ```

### Option B : Auto‑Hébergé

Clonez le dépôt open‑source et déployez à l'aide de Docker Compose ou Helm.

```bash
git clone https://github.com/neondatabase/neon.git
cd neon
docker compose up -d
```

Référez-vous au [guide officiel d'auto‑hébergement](https://neon.tech/docs/self-host) pour les déploiements en production.

---

## Exemples d'Utilisation

### Connexion et Exécution de Requêtes

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

### Création et Changement de Branches

```bash
# List branches
npx neonctl branches list

# Create a branch from a specific point in time (time travel)
npx neonctl branches create --from main --time "2026-06-17T12:00:00Z"

# Use a branch: get its connection string
npx neonctl connection-string --branch feature/ai-search
```

### Intégration avec Vercel / Netlify

Parce que Neon prend en charge les connexions HTTP via `@neondatabase/serverless`, vous pouvez vous connecter depuis les edge functions :

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

## Architecture en Bref

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

- **Les nœuds de compute** sont sans état et peuvent être mis à l'échelle horizontalement.
- **Pageserver** gère le service des pages, le checkpointing et le branching (copy‑on‑write).
- **Safekeeper** garantit la durabilité du WAL avant l'accusé de réception.

---

## Modèle de Tarification

Neon est **basé sur la consommation** :

| Resource | Free Tier | Paid Tier |
|----------|-----------|-----------|
| Compute (active) | 10 hours/month | Pay per compute‑hour |
| Storage | 500 MB | $0.12/GB/month |
| Branching | Unlimited | Unlimited |
| Connection pooling | Yes | Yes |

Scale‑to‑zero signifie que vous ne payez pour le compute que lorsque votre application sert effectivement des requêtes.

---

## Limitations et Pièges

- **Latence du cold start** – Bien qu'environ 500 ms, elle peut être perceptible dans les fonctions sensibles à la latence. Utilisez des connexions keep‑alive ou des endpoints toujours actifs pour les chemins critiques.
- **Parité des fonctionnalités** – Déploiements mono‑serveur uniquement (pas de sharding natif). Pour un multi‑région actif‑actif, vous pourriez encore avoir besoin de stratégies de réplication externes.
- **Plafond du niveau gratuit** – Le plafond de 10 heures de compute peut être consommé rapidement si plusieurs projets restent actifs.

---

## Ressources

- [Documentation officielle](https://neon.tech/docs)
- [Dépôt GitHub](https://github.com/neondatabase/neon)
- [Communauté Discord Neon](https://discord.gg/neon)
- [Blog – Comprendre l'architecture de Neon](https://neon.tech/blog/architecture)

Neon transforme PostgreSQL en une véritable base de données serverless, ce qui en fait un choix idéal pour les applications modernes, les pipelines CI/CD et les charges de travail AI/vectorielles. Sa combinaison d'instant branching, de scale‑to‑zero et de compatibilité totale avec Postgres en a fait l'un des projets d'infrastructure les plus populaires de 2024–2026.