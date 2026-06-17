---
title: Sharding — Horizontale Datenbankpartitionierung für Skalierbarkeit
description: Ein ausführlicher Leitfaden zu Sharding, einer Technik zur horizontalen Partitionierung von Datenbanken über Server hinweg, um Skalierbarkeit, Leistung und Fehlerisolation zu verbessern.
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

**Sharding** ist ein Datenbankarchitekturmuster, bei dem ein großer, logisch einheitlicher Datensatz horizontal in kleinere, unabhängige Datenbanken, sogenannte *Shards*, partitioniert wird. Jeder Shard wird auf einer separaten Serverinstanz gehostet, die in einer „shared-nothing“-Architektur arbeitet. Sharding überwindet die Grenzen der vertikalen Skalierung einer einzelnen Maschine, indem Daten und Arbeitslast auf viele Knoten verteilt werden.

## Was es ist

Sharding unterteilt Daten basierend auf einem deterministischen *Shard-Key* in Blöcke. Jeder Shard enthält eine Teilmenge der Daten (z. B. alle Zeilen für eine bestimmte `user_id`-Range) und ist für die Bearbeitung von Lese- und Schreibvorgängen für seine Partition verantwortlich. Das gesamte System erscheint Clients über eine Routing-Schicht (Anwendungslogik, Proxy oder Datenbank-Router) als eine logische Datenbank.

## Warum Sharding?

| Vorteil | Beschreibung |
|---------|-------------|
| **Horizontale Skalierbarkeit** | Lese- und Schreibdurchsatz skalieren linear mit dem Hinzufügen von Shards. |
| **Hohe Verfügbarkeit & Fehlerisolation** | Ein einzelner Shard-Ausfall betrifft nur eine Teilmenge der Benutzer; andere Shards bedienen weiterhin Anfragen. |
| **Parallelisierung** | Abfragen, die mehrere Shards betreffen, können parallelisiert werden, was die Latenz verbessert. |
| **Geografische Verteilung** | Daten können näher an bestimmten Benutzerpopulationen platziert werden, was Netzwerk-Roundtrips reduziert. |
| **Betriebliche Isolation** | Wartungsarbeiten, Backups und Schemaänderungen können jeweils auf einem einzelnen Shard durchgeführt werden. |

Sharding ist unerlässlich, wenn eine einzelne Datenbank die Last nicht mehr bewältigen kann – oft nachdem vertikale Skalierung (größere CPUs, mehr RAM) unwirtschaftlich wird oder an Hardware-Grenzen stößt.

## Sharding-Architekturen

Sharding kann auf mehreren Ebenen implementiert werden:

### 1. Anwendungsebene (Manuell)

Die Anwendung enthält Routing-Logik (z. B. `hash(user_id) % num_shards`). Jeder Shard ist eine Standarddatenbank ohne zusätzliche Software.  
**Vorteile:** Einfach zu starten, keine Middleware.  
**Nachteile:** Starr; Resharding erfordert Codeänderungen; shardübergreifende Abfragen sind extrem schwierig.  
**Status:** Heute als Anti-Pattern für neue Projekte betrachtet.

### 2. Middleware / Proxy-Ebene (z. B. Vitess, Citus)

Ein transparenter Proxy fängt SQL-Abfragen ab und leitet sie an den entsprechenden Shard weiter.

- **Vitess** für MySQL: setzt `vtgate` (Proxy) + `vttablet` pro Shard ein, verwaltet durch eine etcd/zk-Topologie.
- **Citus** für PostgreSQL: eine Erweiterung, die einen Postgres-Cluster in eine verteilte Datenbank verwandelt.

**Vorteile:** SQL-Transparenz, automatisiertes Resharding (Vitess), shardübergreifende Joins (Citus).  
**Nachteile:** Zusätzliche Komplexitätsebene; einige Abfragen werden unmöglich oder langsam.

### 3. Datenbank‑Nativ (z. B. MongoDB, Cassandra, Druid)

Die Datenbank-Engine übernimmt die Verteilung intern. Der Entwickler gibt einen Shard-Key an, und das System verwaltet Datenplatzierung und Routing.

- **MongoDB**: Sharded-Cluster mit `mongos`-Routern und Konfigurationsservern.
- **Cassandra**: Partitionierung über einen Partitionsschlüssel in der Primärschlüsseldefinition; konsistentes Hashing verteilt Zeilen automatisch.

**Vorteile:** Kein externer Proxy; Funktionen wie automatischer Ausgleich.  
**Nachteile:** Datenmodell muss sorgfältig um den Shard-Key herum entworfen werden; shardübergreifende Operationen sind eingeschränkt oder nicht vorhanden.

### 4. Cloud‑Managed (z. B. Amazon DynamoDB, Azure Cosmos DB, Google Cloud Spanner)

Der Anbieter abstrahiert das Shard-Management vollständig. Sie wählen beim Tabellenerstellen einen Partitionsschlüssel aus; die Cloud-Plattform teilt, migriert und balanciert Daten automatisch.

**Vorteile:** Kein betrieblicher Overhead; Auto-Scale.  
**Nachteile:** Vendor Lock-In; Kosten können bei großen Workloads höher sein; keine direkte Kontrolle über die Shard-Platzierung.

## Installation & grundlegende Nutzung

Im Folgenden finden Sie konkrete Beispiele für zwei der gängigsten Sharding-Implementierungen.

### MongoDB Sharding

**Installation / Einrichtung**

- Stellen Sie einen **Konfigurationsserver-Replikatsatz** (CSRS) bereit, der Cluster-Metadaten speichert.
- Stellen Sie **Shard-Replikatsätze** bereit (jeder Shard besteht aus mindestens einem Knoten, aber normalerweise einem Replikatsatz für hohe Verfügbarkeit).
- Stellen Sie einen oder mehrere **`mongos`-Router** bereit, die Anwendungsabfragen verarbeiten.

Die folgenden Befehle (ausgeführt gegen einen `mongos`) aktivieren Sharding und sharden eine Collection:

```javascript
// Enable sharding on a database
sh.enableSharding("ecommerce");

// Shard a collection using a hashed shard key (recommended for uniform distribution)
sh.shardCollection(
  "ecommerce.orders",
  { "order_id": "hashed" }
);
```

Mit einem gehashten Shard-Key werden Dokumente gleichmäßig über Shards verteilt. Abfragen, die den Shard-Key enthalten, werden direkt an den richtigen Shard weitergeleitet:

```javascript
// Efficient query – goes to a single shard
db.orders.find({ "order_id": UUID("123e4567-e89b-12d3-a456-426614174000") })
```

Shardübergreifende Abfragen (z. B. Aggregationen ohne den Shard-Key) werden an alle Shards gestreut, was die Leistung potenziell beeinträchtigt.

### Citus (PostgreSQL Extension)

**Installation**

1. Installieren Sie die `citus`-Erweiterung auf dem Koordinatorknoten und allen Workerknoten.
2. Fügen Sie Workerknoten zum Koordinator hinzu:
   ```sql
   SELECT citus_add_node('worker-node-1', 5432);
   SELECT citus_add_node('worker-node-2', 5432);
   ```

**Grundlegende Nutzung**

Verteilen Sie eine Tabelle, indem Sie ihre Verteilungsspalte (Shard-Key) angeben:

```sql
-- Create the table on the coordinator
CREATE TABLE orders (
    order_id    BIGSERIAL,
    user_id     INT,
    product_id  INT,
    quantity    INT,
    PRIMARY KEY (order_id, user_id)
);

-- Distribute the table across workers based on user_id
SELECT create_distributed_table('orders', 'user_id');
```

Citus schreibt SQL um, um den relevanten Shard zu treffen. Eine Abfrage, die nach `user_id` filtert, wird an einen einzelnen Worker gesendet:

```sql
-- Single‑shard query
SELECT * FROM orders WHERE user_id = 42;
```

Für Joins zwischen zwei Tabellen, die auf demselben Verteilungsschlüssel ko-lokalisiert sind, kann Citus sie effizient ausführen:

```sql
-- Co‑location example: orders and order_items distributed on user_id
SELECT create_distributed_table('orders', 'user_id');
SELECT create_distributed_table('order_items', 'user_id');
-- JOIN now happens locally on each shard
SELECT o.order_id, oi.product_id
FROM orders o JOIN order_items oi USING (order_id)
WHERE o.user_id = 42;
```

## Wichtige Entwurfsentscheidungen

### 1. Auswahl des Shard-Keys

Der Shard-Key ist die kritischste Entscheidung. Er muss:

- **Daten gleichmäßig verteilen**, um Hot Spots zu vermeiden.
- **Abfragemustern entsprechen**, damit häufige Abfragen an einen einzelnen Shard weitergeleitet werden können.
- **Hohe Kardinalität aufweisen** (viele unterschiedliche Werte), um eine gleichmäßige Aufteilung zu ermöglichen.

**Schlechte Wahl:** Monoton steigende Werte (z. B. Zeitstempel, automatisch inkrementierende IDs) führen dazu, dass alle neuen Schreibvorgänge an den letzten Shard gehen.  
**Bessere Wahl:** Benutzer-IDs, gehashte Spalten oder zusammengesetzte Schlüssel, die hohe Kardinalität und häufige Filterspalten kombinieren.

### 2. Shardübergreifende Operationen

JOINs, Transaktionen und Aggregationen, die sich über mehrere Shards erstrecken, sind entweder sehr teuer oder werden nicht unterstützt. Strategien zur Minderung:

- **Denormalisierung**, um zusammengehörige Daten im selben Shard zu behalten.
- **Co‑Location** (Citus) oder **Document Embedding** (MongoDB), um hierarchische Daten im selben Shard zu speichern.
- **Anwendungsseitige Koordination** für Multi‑Shard‑Transaktionen (selten empfohlen).

### 3. Resharding

Das Hinzufügen oder Entfernen von Shards erfordert eine Neuverteilung der Daten. Moderne Systeme bieten integrierte Mechanismen:

- **MongoDB Balancer** verschiebt automatisch Chunks zwischen Shards.
- **Vitess Reshard** teilt Shards mit einem `MoveTables`-Workflow.
- **Cloud-Dienste** führen Aufteilungen transparent durch.

Manuelles Resharding (bei Sharding auf Anwendungsebene) ist bekanntermaßen schwierig und fehleranfällig.

## Aktueller Stand

Die Industrie bewegt sich weg vom manuellen Sharding. **NewSQL**-Datenbanken (CockroachDB, YugabyteDB, Google Spanner) abstrahieren das Shard-Management vollständig hinter einer standardmäßigen SQL-Schnittstelle und bieten ACID-Transaktionen und Joins über Shards hinweg. Die meisten Cloud-Datenbanken (DynamoDB, Cosmos DB) bieten serverloses Sharding. Das Kernkonzept des Shardings bleibt jedoch die Grundlage aller horizontal skalierbaren verteilten Datenbanken.

Für neue Projekte bevorzugen Sie eine dieser Lösungen gegenüber dem Bau einer eigenen Sharding-Schicht. Wenn Sie SQL und starke Konsistenz benötigen, ziehen Sie Citus oder Spanner in Betracht; wenn dokumentorientierte Flexibilität und massiver Durchsatz im Vordergrund stehen, sind MongoDB oder DynamoDB ausgezeichnete Optionen.

## Zusammenfassung

Sharding ist ein leistungsstarkes Werkzeug, um Web-Scale-Performance zu erreichen, bringt aber Komplexität mit sich. Indem Sie die Architekturoptionen verstehen, einen guten Shard-Key auswählen und moderne Verwaltungswerkzeuge nutzen, können Sie Ihre Datenebene skalieren, ohne das Rad neu zu erfinden.