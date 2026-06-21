---
title: CAP-Theorem (Brewers Theorem)
description: Ein grundlegendes Abwägungsprinzip in verteilten Systemen, das besagt, dass es für einen verteilten Datenspeicher unmöglich ist, gleichzeitig Konsistenz, Verfügbarkeit und Partitionstoleranz zu garantieren.
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

# CAP-Theorem (Brewers Theorem)

## Was ist das CAP-Theorem?

Das CAP-Theorem ist ein grundlegendes Prinzip beim Entwurf verteilter Systeme. Es wurde erstmals **2000** von **Eric Brewer** auf dem ACM Symposium on Principles of Distributed Computing (PODC) vorgestellt und **2002** von **Seth Gilbert** und **Nancy Lynch** formal bewiesen.

Das Theorem besagt, dass ein verteilter Datenspeicher zu jedem Zeitpunkt nur **zwei von drei** Garantien bieten kann:
- **Konsistenz (C)**
- **Verfügbarkeit (A)**
- **Partitionstoleranz (P)**

Obwohl es oft als strenge „Wähle zwei“-Entscheidung vereinfacht wird, lautet die korrekte Interpretation: **Bei Vorliegen einer Netzwerkpartition muss man sich zwischen Konsistenz und Verfügbarkeit entscheiden**. Da Netzwerkpartitionen in verteilten Systemen unvermeidbar sind, können nicht alle drei Eigenschaften gleichzeitig erreicht werden.

---

## Die drei Eigenschaften

### Konsistenz (C)
Jede Leseoperation erhält den **aktuellsten Schreibvorgang** oder einen Fehler. Alle Knoten im System sehen zur gleichen logischen Zeit dieselben Daten. Dies impliziert eine totale Ordnung der Operationen (Linearizability).

- **Auswirkung:** Stärkere Konsistenz erfordert oft eine Synchronisation zwischen den Knoten, bevor Schreibvorgänge bestätigt werden.
- **Beispiel:** Eine Leseoperation von einem beliebigen Knoten muss dasselbe Ergebnis liefern wie eine Leseoperation vom primären Knoten.

### Verfügbarkeit (A)
Jede Anfrage, die von einem nicht ausfallenden Knoten des Systems empfangen wird, **muss zu einer Antwort führen**. Die Antwort enthält möglicherweise nicht die aktuellsten Daten, aber sie wird kein Fehler sein (z. B. Timeout oder 503).

- **Auswirkung:** Das System bleibt betriebsbereit und nimmt Anfragen entgegen, selbst wenn einige Replikate nicht synchron sind.
- **Beispiel:** Eine Webanwendung zeigt weiterhin einen Produktkatalog an, selbst wenn ein nachgelagerter Datenbankknoten nicht erreichbar ist.

### Partitionstoleranz (P)
Das System arbeitet trotz **einer beliebigen Anzahl von Nachrichten, die im Netzwerk zwischen Knoten verloren gehen oder verzögert werden**, weiter. Dies umfasst Netzwerktrennungen, Kabelbrüche und Paketverluste.

- **Auswirkung:** Das System muss auch dann korrekt funktionieren, wenn Knoten nicht miteinander kommunizieren können.
- **Realität:** Partitionen sind in jedem geografisch verteilten System unvermeidbar. Daher **muss jedes verteilte System P-tolerant sein**.

---

## Der eigentliche Kompromiss: CP vs. AP

Da Netzwerkpartitionen (P) in einem verteilten System unvermeidbar sind, ist die Erreichung von **CA** (Konsistenz + Verfügbarkeit) ohne Partitionstoleranz in einem verteilten Kontext unmöglich. Die tatsächliche Wahl lautet:

### CP-Systeme (Konsistenz + Partitionstoleranz)
- **Opfert:** Verfügbarkeit während einer Partition.
- **Verhalten:** Knoten, die keine Konsistenz mit dem Rest des Clusters garantieren können, lehnen Anfragen ab (werden unverfügbar), bis die Partition behoben ist.
- **Anwendungsfälle:** Bankkonten, Bestandsverwaltung, Gesundheitsakten – Situationen, in denen veraltete Daten inakzeptabel sind.
- **Bekannte Beispiele:**
  - **Apache ZooKeeper** (Leader-Wahl, Konfigurationsdaten)
  - **Apache HBase** (starkes Konsistenzmodell)
  - **MongoDB** (mit `w: "majority"` Schreibanliegen und Lesezugriffen vom Primary)
  - **Redis** (Cluster-Modus mit strengen Konsistenzgarantien)

### AP-Systeme (Verfügbarkeit + Partitionstoleranz)
- **Opfert:** Konsistenz während einer Partition.
- **Verhalten:** Alle Knoten bleiben für Anfragen verfügbar, auch wenn sie Schreibvorgänge unabhängig voneinander akzeptieren. Das System verlässt sich auf Konfliktlösungsmechanismen (z. B. Last-Write-Wins, CRDTs), um die Daten zu harmonisieren, sobald die Partition geheilt ist.
- **Anwendungsfälle:** Social-Media-Feeds, Content Delivery, IoT-Sensordaten, Produktkataloge – Umgebungen, in denen Betriebszeit entscheidend ist.
- **Bekannte Beispiele:**
  - **Apache Cassandra** (abstimmbare Konsistenz, standardmäßig Eventual Consistency)
  - **Amazon DynamoDB** (Multi-Region, Eventual Consistency)
  - **CouchDB / Couchbase** (Multi-Master-Replikation)
  - **Riak**

### CA-Systeme (Konsistenz + Verfügbarkeit)
- **Kontext:** Nur in einem nicht verteilten (Einzelknoten-)System oder einem System möglich, das Partitionen einfach ignoriert (was gefährlich ist).
- **Bekannte Beispiele:**
  - Eine eigenständige **MySQL**- oder **PostgreSQL**-Instanz.
  - Traditionelle ACID-konforme RDBMS auf einem einzelnen Server.
  - *Hinweis:* In einer verteilten Bereitstellung müssen diese Systeme Daten replizieren und stoßen unweigerlich auf Partitionen, was sie in ein CP- oder AP-Verhalten zwingt.

---

## Wichtige Eigenschaften und Nuancen

### 1. Das „P“ ist nicht optional
Ein häufiger Anfängerfehler ist der Entwurf eines „CA“-verteilten Systems. Sobald Daten über ein Netzwerk repliziert werden, ist man anfällig für Partitionen. Jedes echte verteilte System **muss** Partitionen tolerieren, sodass die eigentliche Entscheidung bei Auftreten einer Partition **CP vs. AP** lautet.

### 2. Abstimmbarkeit
Moderne Datenbanken sind nicht auf eine einzige Klassifizierung festgelegt. Man kann oft die Konsistenz gegen die Verfügbarkeit (oder umgekehrt) pro Abfrage eintauschen.

- **Cassandra:** Wechsel zwischen `QUORUM` (starke Konsistenz) und `ONE` (Eventual Consistency) pro Anfrage.
- **MongoDB:** Konfiguration von `writeConcern` und `readPreference`, um zwischen starker und schwacher Konsistenz zu wechseln.
- **DynamoDB:** Wahl zwischen `ConsistentRead` als `true` oder `false` bei Lesevorgängen.

### 3. Der „2 von 3“-Trugschluss
Das CAP-Theorem besagt nicht, „das System muss immer zwei von drei auswählen“. Es besagt: **Während einer Netzwerkpartition** muss man sich für **C** oder **A** entscheiden. Die restliche Zeit (wenn das Netzwerk intakt ist) kann das System sowohl starke Konsistenz als auch hohe Verfügbarkeit anstreben.

Hier kommt das **PACELC-Theorem** ins Spiel.

---

## Die PACELC-Erweiterung (die moderne Sicht)

Eingeführt von **Daniel J. Abadi**, erweitert PACELC das CAP-Theorem, indem es explizit die Kompromisse betrachtet, wenn das System **intakt** ist (keine Partition).

**PACELC steht für:**
- Wenn eine **P**artition auftritt → Kompromiss zwischen **A**vailability und **C**onsistency.
- **E**lse (wenn das Netzwerk intakt ist) → Kompromiss zwischen **L**atency und **C**onsistency.

### Warum PACELC wichtig ist
- **Kompromisse im intakten Zustand:** Auch ohne Partitionen kann man wählen, ob man auf die Zustimmung der Replikate wartet (hohe Latenz, starke Konsistenz) oder schnell mit potenziell veralteten Daten antwortet (geringe Latenz, Eventual Consistency).
- **Konfiguration in der Praxis:**
  - **CP-System (während Partition):** Opfert Verfügbarkeit.
    - **E** (Else): Opfert möglicherweise auch Latenz für Konsistenz (z. B. synchrone Replikation).
  - **AP-System (während Partition):** Opfert Konsistenz.
    - **E** (Else): Opfert möglicherweise Konsistenz für geringe Latenz (z. B. asynchrone Replikation, Read Replicas).

---

## Praktische Anwendung und Konfiguration

Man „installiert“ das CAP-Theorem nicht, aber man konfiguriert seine verteilten Datenspeicher, um mit den Kompromissen umzugehen.

### Konzeptionelle Entscheidungslogik (Pseudocode)

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

### MongoDB: CP/AP-Abstimmung pro Abfrage

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

### Apache Cassandra: Abstimmbare Konsistenzstufen

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

## Wann CP vs. AP wählen

| Szenario | Empfohlener Ansatz | Begründung |
|---|---|---|
| Zahlungsabwicklung / Hauptbücher | **CP** | Inkonsistente Zählungen oder Kontostände verursachen finanzielle Verluste und rechtliche Probleme. Vorübergehende Ausfallzeiten während einer Partition sind besser als Doppelausgaben. |
| Gesundheitsakten / medizinische Daten | **CP** | Lebenswichtige Entscheidungen hängen von vollständigen und genauen Daten ab. Ausfallzeiten sind sicherer als widersprüchliche oder veraltete Diagnosen. |
| Benutzersitzungsdaten (E-Commerce) | **AP** | Benutzer müssen in der Lage sein, zu browsen und Artikel in den Warenkorb zu legen, selbst wenn ein Rechenzentrum offline ist. Veraltete Bestandszahlen sind ein akzeptabler vorübergehender Kompromiss. |
| Social-Media-Feeds | **AP** | Benutzer erwarten, dass die Seite verfügbar ist. Ein fehlender „Gefällt mir“-Angabe oder ein verzögerter Kommentar ist akzeptabel, wenn die App reaktionsfähig bleibt. |
| Content Delivery / CDNs | **AP** | Die Auslieferung einer leicht veralteten gecachten Version einer Seite wird einem Fehler deutlich vorgezogen. |
| Metadaten-/Konfigurationsspeicher (ZooKeeper, etcd) | **CP** | Die Konfiguration muss autoritativ und konsistent im gesamten Cluster sein. Die Aufteilung des Clusters in inkonsistente Ansichten ist gefährlich (Split-Brain). |

---

## Geschichte und Auswirkungen

### Zeitleiste
- **1998:** Eric Brewer stellt die Idee der drei Eigenschaften erstmals vor.
- **2000:** Brewer formuliert die Vermutung auf der PODC.
- **2002:** Seth Gilbert und Nancy Lynch vom MIT veröffentlichen „Brewer’s Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services“ und beweisen das Theorem formal.
- **Späte 2000er:** Das Theorem beeinflusste direkt die Architektur von **Amazon DynamoDB**, **Google Bigtable**, **Apache Cassandra** und **MongoDB**.
- **2010er:** Die NoSQL-Bewegung nimmt das CAP-Theorem als zentrales Entwurfsprinzip auf. PACELC wird eingeführt, um die „immerwährenden“ Kompromisse zu klären, nicht nur während Partitionen.
- **2020er:** Moderne verteilte SQL-Datenbanken (Spanner, CockroachDB, YugabyteDB) versuchen, die Grenzen zu verschieben, indem sie die meiste Zeit „C und A“ anstreben, indem sie die Wahrscheinlichkeit und Dauer von Partitionen aggressiv reduzieren (z. B. durch TrueTime / enge Takt-Synchronisation).

### Wichtige Erkenntnis
Das CAP-Theorem war revolutionär, weil es Architekten eine formale Sprache gab, um Kompromisse zu diskutieren. Vor CAP erwarteten Betreiber, dass sich verteilte Datenbanken genau wie monolithische verhalten. Das Theorem zwang die Branche zu der Erkenntnis, dass **starke Konsistenz einen Preis hat** und dieser Preis oft in Form von Verfügbarkeit während Ausfällen gezahlt wird.

---

## Einschränkungen und Kritik

1.  **Falsche Binärität:** Kritiker argumentieren, dass „C, A, P“ keine binären Eigenschaften sind. Es gibt Abstufungen der Konsistenz (stark, kausal, Eventual, Read-Your-Writes) und der Verfügbarkeit.
2.  **Ignorieren von Latenz:** Das ursprüngliche CAP-Theorem geht nicht explizit auf Kompromisse ein, wenn das Netzwerk intakt ist (dies wird von PACELC adressiert).
3.  **CA ist eine Falle:** Viele Ingenieure suchen nach CA-„verteilten“ Systemen. In der Realität ist jedes System, das Daten über ein Netzwerk repliziert, notwendigerweise P-tolerant. Ein System als rein „CA“ zu bezeichnen, ist oft Marketing, nicht Architektur.
4.  **Moderne Abmilderung:** Datenbanken wie **Google Spanner** verwenden Atomuhren und die TrueTime-API, um gleichzeitig starke Konsistenz und hohe Verfügbarkeit zu erreichen *die meiste Zeit*, wodurch das „Wähle 2 von 3“-Szenario zu einem seltenen Grenzfall wird.

---

## Siehe auch

- **PACELC-Theorem** — Die moderne Erweiterung von CAP, die Latenzkompromisse einschließt.
- **Eventual Consistency** — Das Konsistenzmodell, auf das die meisten AP-Systeme angewiesen sind.
- **ACID vs. BASE** — ACID (Atomicity, Consistency, Isolation, Durability) vs. BASE (Basically Available, Soft state, Eventual consistency).
- **Eric Brewer** — Ursprünglicher Vorschlag des Theorems.
- **Entwurf verteilter Systeme** — Sharding, Replikation, Konsensalgorithmen (Raft, Paxos).
- **CRDTs (Conflict-free Replicated Data Types)** — Datenstrukturen, die Konflikte in AP-Systemen auf natürliche Weise lösen.