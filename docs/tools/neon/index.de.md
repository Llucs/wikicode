---
title: Neon – Serverlose PostgreSQL-Plattform
description: Neon ist eine quelloffene serverlose PostgreSQL-Datenbank, die Rechenleistung von Speicher trennt und sofortige Verzweigung, Skalierung auf Null und unbegrenzten Speicher für moderne Anwendungen bietet.
created: 2026-06-18
tags:
  - serverless
  - postgres
  - database
  - branching
  - cloud
status: draft
---

# Neon – Serverlose PostgreSQL-Plattform

Neon ist eine quelloffene, serverlose PostgreSQL-Plattform, die die klassische Datenbankarchitektur auf eine cloud-native Grundlage stellt. Durch die vollständige Entkopplung von Compute (Abfrageverarbeitung) und Storage (Datenpersistenz) bietet Neon Funktionen, die bisher nur in proprietären Systemen wie Amazon Aurora verfügbar waren – jedoch für das gesamte Postgres-Ökosystem. Mit sofortiger Verzweigung, automatischer Skalierung auf Null und unbegrenztem Speicher ist Neon für moderne Entwicklungsworkflows und serverlose Anwendungen konzipiert.

---

## Warum Neon?

| Herausforderung | Lösung von Neon |
|----------------|-----------------|
| **Teure Leerlauf-Datenbanken** | Compute-Endpunkte skalieren nach Inaktivität auf Null; Sie zahlen nur für aktive Rechenleistung. |
| **Langsame Entwicklungszyklen** | Sofortige Verzweigung gibt jedem Entwickler/PR einen eigenen vollständigen Datenbank-Fork. |
| **Speicherbereitstellung & Kosten** | Unbegrenzter Speicher, unterstützt durch Objektspeicher (z.B. S3); keine manuelle Kapazitätsplanung. |
| **Serverless/Edge-Kompatibilität** | Kaltstartzeiten von ~500 ms, kombiniert mit PgBouncer-Pooling für kurzlebige Compute-Ressourcen. |
| **Vektor-Workloads** | Volle Unterstützung für `pgvector` und PostGIS; Ausführung von KI-Embeddings direkt in Postgres. |

---

## Hauptfunktionen

### 1. Sofortige Verzweigung

Mithilfe der Copy‑on‑Write-Technologie kann Neon einen Zweig einer terabytegroßen Datenbank in Millisekunden erstellen. Dies ist unschätzbar für:

- **Entwicklungssandkästen** – jeder Entwickler erhält einen isolierten Klon der Produktion.
- **CI/CD-Pipelines** – führen Integrationstests gegen einen Zweig durch, der die Produktionsdaten spiegelt.
- **Schema-Migrationen** – testen Sie Breaking Changes ohne Risiko.

```bash
# Create a new branch from the main branch
npx neonctl branches create --name feature/ai-search
```

### 2. Skalierung auf Null

Compute-Endpunkte werden nach einer Inaktivitätsdauer automatisch ausgesetzt. Wenn eine neue Verbindung eingeht, wird der Endpunkt in etwa 500 ms (Kaltstart) wieder aufgenommen. Dies eliminiert Kosten für inaktive oder verkehrsarme Datenbanken.

```sql
-- No configuration needed – scale‑to‑zero is automatic.
-- Connect and the endpoint wakes up transparently.
```

### 3. Unbegrenzter Speicher

Der Speicher wird von einer separaten Engine (Pageserver + Safekeepers) verwaltet, die auf kostengünstigen Objektspeicher zurückgreift. Sie müssen nie Speicherplatz bereitstellen oder sich Sorgen machen, dass er voll wird.

### 4. Vollständige PostgreSQL-Kompatibilität

Neon unterstützt PostgreSQL 14–17, einschließlich aller wichtigen Erweiterungen:

- `pgvector` – Vektor-Ähnlichkeitssuche für Embeddings.
- `PostGIS` – Geodatenabfragen.
- `pg_cron`, `pg_stat_statements`, usw.

Ihre vorhandenen Werkzeuge und Treiber funktionieren unverändert.

### 5. Transparentes Verbindungspooling

PgBouncer ist auf Proxy-Ebene integriert, sodass Sie effizientes Verbindungsmanagement ohne Anwendungskonfiguration erhalten.

---

## Schnellstart

### Option A: Cloud (Managed)

1. Registrieren Sie sich unter [console.neon.tech](https://console.neon.tech) (großzügiges kostenloses Kontingent inklusive).
2. Erstellen Sie ein Projekt über die Benutzeroberfläche oder die CLI:

   ```bash
   # Install the Neon CLI
   npx neonctl

   # Create a project (first time: interactive)
   npx neonctl create-project

   # Get the connection string for the main branch
   npx neonctl connection-string
   ```

### Option B: Selbst gehostet

Klonen Sie das quelloffene Repository und stellen Sie es mit Docker Compose oder Helm bereit.

```bash
git clone https://github.com/neondatabase/neon.git
cd neon
docker compose up -d
```

Für Produktionsbereitstellungen lesen Sie bitte die [offizielle Self-Hosting-Anleitung](https://neon.tech/docs/self-host).

---

## Verwendungsbeispiele

### Verbinden und Abfragen ausführen

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

### Zweige erstellen und wechseln

```bash
# List branches
npx neonctl branches list

# Create a branch from a specific point in time (time travel)
npx neonctl branches create --from main --time "2026-06-17T12:00:00Z"

# Use a branch: get its connection string
npx neonctl connection-string --branch feature/ai-search
```

### Integration mit Vercel / Netlify

Da Neon HTTP-Verbindungen über `@neondatabase/serverless` unterstützt, können Sie von Edge-Funktionen aus eine Verbindung herstellen:

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

## Architektur in Kürze

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

- **Compute-Knoten** sind zustandslos und können horizontal skaliert werden.
- **Pageserver** übernimmt die Seitenbereitstellung, Checkpointing und Verzweigung (Copy‑on‑Write).
- **Safekeeper** stellt die WAL-Haltbarkeit sicher, bevor eine Bestätigung erfolgt.

---

## Preismodell

Neon ist **nutzungsbasiert**:

| Ressource | Kostenloser Tarif | Bezahlter Tarif |
|-----------|-------------------|-----------------|
| Compute (aktiv) | 10 Stunden/Monat | Zahlung pro Compute-Stunde |
| Speicher | 500 MB | 0,12 $/GB/Monat |
| Verzweigung | Unbegrenzt | Unbegrenzt |
| Verbindungspooling | Ja | Ja |

Scale‑to‑zero bedeutet, dass Sie nur für Compute bezahlen, wenn Ihre Anwendung tatsächlich Abfragen bedient.

---

## Einschränkungen & Fallstricke

- **Kaltstartlatenz** – Obwohl ~500 ms, kann sie bei latenzempfindlichen Funktionen spürbar sein. Verwenden Sie Keep-Alive-Verbindungen oder Always-On-Endpunkte für kritische Pfade.
- **Funktionsparität** – Nur Einzel-Server-Bereitstellungen (kein natives Sharding). Für Multi-Region-Active-Active sind möglicherweise externe Replikationsstrategien erforderlich.
- **Grenze des kostenlosen Tarifs** – Die Obergrenze von 10 Compute-Stunden kann schnell verbraucht sein, wenn mehrere Projekte aktiv bleiben.

---

## Ressourcen

- [Offizielle Dokumentation](https://neon.tech/docs)
- [GitHub-Repository](https://github.com/neondatabase/neon)
- [Neon Discord-Community](https://discord.gg/neon)
- [Blog – Neon's Architektur verstehen](https://neon.tech/blog/architecture)

Neon verwandelt PostgreSQL in eine echte serverlose Datenbank und ist damit eine ideale Wahl für moderne Anwendungen, CI/CD und KI/Vektor-Workloads. Die Kombination aus sofortiger Verzweigung, Skalierung auf Null und vollständiger Postgres-Kompatibilität hat es zu einem der beliebtesten Infrastrukturprojekte der Jahre 2024–2026 gemacht.