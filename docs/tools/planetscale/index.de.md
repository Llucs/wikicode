---
title: PlanetScale: Serverless MySQL-Datenbankplattform
description: Eine vollständig verwaltete MySQL-kompatible Datenbankplattform, die auf Vitess basiert und Datenbank-Branching sowie nicht-blockierende Schemaänderungen für moderne Entwicklungsworkflows einführt.
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

## Einführung

PlanetScale, 2018 von den Kernentwicklern von Vitess (Sugu Sougoumarane, Jiten Vaidya und Morgan Goeller) gegründet, ist die MySQL-kompatible Datenbankplattform, die auf dem Open-Source-Datenbank-Clustering-System aufbaut, das YouTube antreibt. Sie denkt Datenbankmanagement neu, indem sie **Git-ähnliche Workflows** – Datenbank-Branching und Deploy Requests – auf Schemata und Daten anwendet.

Dieser Ansatz beseitigt die traditionellen Engpässe und Ausfallzeiten, die mit Schema-Migrationen verbunden sind, und macht Datenbankänderungen so sicher, überprüfbar und iterativ wie Codeänderungen. PlanetScale ist ein vollständig verwalteter Dienst, der Replikation, Backups, Sharding und Hochverfügbarkeit übernimmt und gleichzeitig eine Serverless-Compute-Ebene unterstützt, die auf Null herunterskaliert und bei Verbindung sofort aufwacht.

## Kernkonzepte

### Datenbank-Branching
Genau wie `git branch` isolierte Codeentwicklung ermöglicht, erstellt `pscale branch create` eine isolierte, voll funktionsfähige Kopie Ihrer Datenbank (einschließlich Daten und Schema) auf der Infrastruktur von PlanetScale.

- **Branch von jedem Punkt:** Erstellen Sie einen Branch von `main` oder einem vorherigen Snapshot.
- **Daten und Schema:** Der Branch enthält einen vollständigen Snapshot und ermöglicht so äußerst realistische Tests.
- **Ephemere Natur:** Branches sind dazu gedacht, verworfen zu werden, sobald ihr Zweck erfüllt ist, um Schema-Drift zu verhindern.

### Deploy Requests (DRs)
PlanetScales Gegenstück zu einem Pull Request. Wenn Sie mit den Schemaänderungen auf einem Branch zufrieden sind, öffnen Sie einen Deploy Request. Dieser erzeugt einen Diff, ermöglicht eine Überprüfung und führt den Merge als **nicht-blockierende Online-Schema-Migration** (unter Verwendung von Vitess VReplication) durch.

### Serverless Compute
PlanetScale entkoppelt Compute und Storage. Datenbanken haben einen „Schlaf“-Zustand, wenn keine Verbindungen aktiv sind. Verbindungen wecken die Datenbank sofort auf und vermeiden so Kosten für ungenutzte Compute-Ressourcen.

## Erste Schritte

### Installation
Die primäre Entwicklerschnittstelle ist die `pscale` CLI.

**macOS:**
```bash
brew install planetscale/tap/pscale
```

**Linux / Windows:**
```bash
curl -fsSL https://planetscale.com/install.sh | sh
```

### Authentifizierung
```bash
pscale auth login
```

### Eine Datenbank erstellen
```bash
pscale database create my-app
```

### Mit Branches arbeiten

**Einen Feature-Branch erstellen (kopiert Schema und Daten von main):**
```bash
pscale branch create my-app feature-user-profile
```

**Mit dem Branch verbinden:**
```bash
pscale connect my-app feature-user-profile --port 3309
```
Dies startet einen lokalen Proxy. Ihre Anwendung verbindet sich mit `127.0.0.1:3309`. Der Proxy übernimmt die Authentifizierung automatisch.

**Schema-Migrationen gegen Ihren Branch ausführen:**
Verwenden Sie einen beliebigen MySQL-Client, ein ORM oder ein Migrationstool (z. B. `mysql2`, `Prisma`, `SQLAlchemy`).
```sql
ALTER TABLE users ADD COLUMN bio TEXT;
```

### Der Deploy-Request-Ablauf
Sobald Sie die Schemaänderungen auf dem Branch gründlich getestet haben:

```bash
# Deploy Request erstellen
pscale deploy-request create my-app feature-user-profile

# Deploy Requests auflisten
pscale deploy-request list my-app

# Request bereitstellen (nach Überprüfung)
pscale deploy-request deploy my-app <deploy-number>

# Branch bereinigen
pscale branch delete my-app feature-user-profile --force
```

Die Bereitstellung wendet die Schemaänderung auf `main` an, *ohne die Tabelle zu sperren oder Ausfallzeiten zu verursachen*.

## Schlüsselfunktionen im Detail

### Nicht blockierende Schemaänderungen (Online DDL)
Traditionelle `ALTER TABLE`-Anweisungen in MySQL sperren oft Tabellen. PlanetScale verwendet Vitess’ **Online DDL** über VReplication. Es erstellt eine Schattentabelle, kopiert Daten inkrementell und wechselt transparent um.

**Befehlsbeispiel:**
```bash
pscale deploy-request deploy my-app 1
```
Die Produktion bleibt auch während großer, langlaufender Migrationen voll funktionsfähig.

### Connection Pooling
Integriertes serverseitiges Connection Pooling verwaltet Verbindungsspitzen. Bei Verwendung von `pscale connect` poolt der lokale Proxy ebenfalls Verbindungen. Für die Produktion stellen Sie direkt eine Verbindung zur PlanetScale-Serveradresse her.

### Horizontales Sharding (Vitess)
Für extrem große Datensätze verwendet PlanetScale Vitess’ Key-Range-Sharding, um Daten transparent auf viele MySQL-Instanzen zu verteilen. Keine Anwendungsänderungen erforderlich.

### Hochverfügbarkeit und globale Replikation
Hochverfügbarkeit ist integriert. PlanetScale bietet regionsübergreifende Replikate und automatisches Failover mit einer 99,99 % Uptime-SLA.

## Praktische Anwendungsfälle

### CI/CD-Integration
Starten Sie für jeden Pull-Request einen isolierten Datenbank-Branch, um Integrationstests mit echten Produktionsdaten durchzuführen.
```bash
pscale branch create my-app ci-pr-123 --from main
pscale connect my-app ci-pr-123 --port 3309 &
# Integrationstests hier ausführen
pscale branch delete my-app ci-pr-123 --force
```

### Pre-Production-Tests
Lassen Sie QA destruktive oder Lasttests auf einem vollständig realistischen Branch ausführen, ohne Produktionsdaten zu beschädigen.

### Schema-Review
Teammitglieder überprüfen den genauen SQL-Diff in einem Deploy Request vor dem Merge, was „Database as Code“-Workflows ermöglicht.

### Ephemere Umgebungen
Kombinieren Sie `pscale branch create/destroy` mit Platform-Engineering-Tools (z. B. Kubernetes-Operatoren, Terraform), um eine Full-Stack-Umgebung pro Entwickler oder pro Feature bereitzustellen.

## Einschränkungen und Hinweise

Obwohl leistungsstark, bringt PlanetScales Vitess-Grundlage einige MySQL-Kompatibilitätsbesonderheiten mit sich:

- **Keine Stored Procedures oder Trigger:** Die Vitess-Proxy-Ebene unterstützt diese nicht.
- **Fremdschlüssel:** In der Beta-Phase (muss pro Datenbank aktiviert werden). Noch nicht für kritische Produktionspfade empfohlen.
- **`LOCK TABLES` / `UNLOCK TABLES`:** Nicht unterstützt.
- **`GET_LOCK()` / `RELEASE_LOCK()`:** Nicht unterstützt.
- **Subqueries und `JOIN`s:** Die meisten werden unterstützt, aber sehr komplexe korrelierte Subqueries oder nicht-deterministische Anweisungen können sich anders verhalten.
- **Direktes `ALTER TABLE` in der Produktion:** Der Deploy-Request-Workflow ist der *einzige* sichere Weg, Schemaänderungen in der Produktion vorzunehmen. Die direkte Ausführung von `ALTER TABLE` auf einem Produktions-Branch über `pscale connect` wird dringend empfohlen.

> **Entwicklerhinweis:** Verwenden Sie für **Produktions**-Schemaänderungen immer den Deploy-Request-Workflow. Für Entwicklungs-Branches ist direktes `ALTER TABLE` sicher und schnell.

## Preismodell

PlanetScale wird als SaaS-Produkt mit einem großzügigen Free-Tier betrieben. Die Preisgestaltung basiert auf Zeilenspeicher und Zeilen-Lese-/Schreibvorgängen.

| Stufe | Preis | Zeilenspeicher | Compute | Branches |
|---|---|---|---|---|
| **Kostenlos** | $0/Monat | 5 GB | 10 Mio. Zeilen-Lesevorgänge/Monat, 1 Mio. Zeilen-Schreibvorgänge/Monat | Bis zu 3 |
| **Scaler** | $39/Monat (Basis) | 10 GB | 100 Mio. Zeilen-Lesevorgänge, 10 Mio. Zeilen-Schreibvorgänge | Bis zu 10 |
| **Business** | Individuell | Individuell | Individuell | Individuell |

*Die Preisdetails können sich ändern; überprüfen Sie immer die [PlanetScale-Preisseite](https://planetscale.com/pricing).*

## Bewährte Vorgehensweisen

- **Branch-Benennung:** Verwenden Sie einen konsistenten Namespace (z. B. `feature/*`, `hotfix/*`, `ci/*`).
- **Veraltete Branches löschen:** Bereinigen Sie regelmäßig Branches, um Speicherkosten zu vermeiden.
  ```bash
  pscale branch delete my-app stale-branch --force
  ```
- **Leistung überwachen:** Verwenden Sie das PlanetScale-Dashboard, um die Abfrageleistung, langsame Abfragen und die Verbindungsnutzung zu überwachen. Die Funktionen zur Abfrageerklärung und -analyse sind leistungsstark.
- **Umgebungsparität:** Halten Sie `main` als saubere Produktionsumgebung. Entwicklungsteams arbeiten ausschließlich auf Branches.
- **Vermeiden Sie schwere Abfragen auf Produktions-Branch-Proxys:** Obwohl ein Branch ein Snapshot ist, kann das Ausführen massiver analytischer Abfragen auf einem Branch, der mit demselben zugrunde liegenden Cluster wie die Produktion verbunden ist, das gemeinsam genutzte I/O beeinträchtigen.

## Fehlerbehebung

**Verbindung vom Proxy abgelehnt:**
```bash
pscale connect my-app main
```
Stellen Sie sicher, dass kein anderer Dienst auf dem Port läuft. Verwenden Sie `--port`, um einen alternativen Port anzugeben.

**Schemaänderung fehlgeschlagen:**
Überprüfen Sie die Deploy-Request-Protokolle im PlanetScale-Dashboard oder verwenden Sie:
```bash
pscale deploy-request show my-app <deploy-number>
```

**Hohe Abfragelatenz:**
Überprüfen Sie die Grenzen des Connection Pooling. Erwägen Sie, dem Branch vor dem Merge einen Index hinzuzufügen:
```sql
ALTER TABLE users ADD INDEX idx_email (email);
```

## Vergleich mit Alternativen

| Funktion | PlanetScale | Neon (Postgres) | Supabase (Postgres) | RDS (MySQL) |
|---|---|---|---|---|
| **Branching** | Sofortig, vollständige Daten | Sofortig, vollständige Daten | Branching über SQL | Manuelle Snapshots |
| **Serverless** | Ja (Schlaf/Aufwachen) | Ja (Schlaf/Aufwachen) | Ja (automatische Aussetzung) | Nein (immer an) |
| **Schema-Migrationen** | Nicht blockierend (Online DDL) | Branching + `pgroll` | Branching + Migrationen | Manuell |
| **Sharding** | Automatisch (Vitess) | Nein | Nein | Manuell (Sharding) |
| **Migrations-CI-Workflow** | Hervorragend (Deploy Requests) | Hervorragend | Gut | Schlecht |

**Wann sollte man PlanetScale wählen:**
Sie benötigen MySQL-Kompatibilität, Datenbank-Branching für komplexe Schemaänderungen und Tests sowie automatische horizontale Skalierung.

**Wann sollte man PlanetScale vermeiden:**
Sie sind stark auf Stored Procedures, Trigger oder erweiterte MySQL-Interna (z. B. `GET_LOCK()`) angewiesen. In diesem Fall sind RDS oder eine standardmäßig verwaltete MySQL-Lösung möglicherweise besser geeignet.

## Zusammenfassung

PlanetScale revolutioniert die MySQL-Entwicklungserfahrung, indem es Git-ähnliche Workflows auf die Datenbankebene bringt. Die Fähigkeit, Daten und Schema sofort zu branchen, gepaart mit nicht-blockierenden Deploy Requests, ermöglicht es Teams, Datenbankschemata mit der gleichen Sicherheit und Geschwindigkeit wie ihren Anwendungscode zu iterieren. Basierend auf der bewährten Vitess-Engine bietet es YouTube-taugliche Skalierbarkeit ohne den operativen Overhead.