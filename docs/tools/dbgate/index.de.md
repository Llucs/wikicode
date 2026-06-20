---
title: DBGate
description: DBGate ist ein Open-Source-, plattformübergreifendes, webbasiertes Datenbankverwaltungstool für MySQL, PostgreSQL, SQL Server, MongoDB, SQLite und mehr, das eine moderne Oberfläche für die Datenbankadministration und -entwicklung bietet.
created: 2026-06-20
tags:
  - database
  - open-source
  - web-based
  - tool
  - management
status: draft
---

# DBGate

DBGate ist ein Open-Source (MIT), webbasiertes Datenbankverwaltungstool, das als moderne Alternative zu klassischen Tools wie phpMyAdmin, Adminer, DBeaver oder DataGrip entwickelt wurde. Es wurde mit einem Node.js/Express-Backend und einem React-Frontend erstellt und bietet eine saubere, zeitgemäße Benutzeroberfläche, die vollständig in einem Webbrowser läuft. Dadurch ist es plattformübergreifend und ideal für Cloud-, Server- und Container-Umgebungen.

## Warum DBGate?

Traditionelle Datenbank-Clients erfordern oft eine Installation auf dem Betriebssystem, was zu Fragmentierung zwischen Teams und Umgebungen führt. DBGate löst dies, indem es vollständig browserbasiert ist und Ihnen ermöglicht:

- **Datenbanken remote zu verwalten**, ohne SSH-Tunnel oder native Clients zu benötigen.
- **In Docker-Stacks zu integrieren**, für sofortigen Datenbankzugriff in der Entwicklung.
- **Verbindungen und Skripte zu teilen** über eine zentralisierte Instanz (mit Authentifizierung).
- **Nahtlos unter Windows, macOS und Linux zu arbeiten** mit derselben Weboberfläche.

## Hauptfunktionen

| Funktion                    | Beschreibung                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| Multi-Datenbank-Unterstützung| Stellen Sie gleichzeitig eine Verbindung zu MySQL, MariaDB, PostgreSQL, SQL Server, MongoDB, SQLite, CockroachDB, Amazon Redshift und Redis her. |
| Erweiterter SQL-Editor      | Syntaxhervorhebung, intelligente Autovervollständigung, Abfragen mit mehreren Registerkarten und umfassender Abfrageverlauf. |
| Schema-/Datenbrowser        | Datenbankobjekte durchsuchen, erstellen, ändern und löschen. Inline-Datenbearbeitung mit leistungsstarker Sortierung und Filterung. |
| ER-Diagramme                | Automatische Generierung von Entity-Relationship-Diagrammen zur Visualisierung von Datenbankschemata. |
| Export/Import               | Export nach CSV, JSON, SQL, Markdown, Excel; Import aus CSV- und SQL-Dateien. |
| Fremdschlüsselnavigation    | Direkt in verwandte Datensätze aus dem Datenbrowser einsteigen.                  |
| Serverüberwachung           | Aktive Prozesse, Serverstatus und Variablenkonfigurationen anzeigen.           |
| Docker-optimiert            | Offizielles Docker-Image für die einfache Bereitstellung auf jedem Server.   |
| Desktop-App                 | Gebündelte Electron-Version für den eigenständigen Einsatz unter Windows, macOS und Linux. |

## Installation

DBGate kann auf verschiedene Arten installiert und ausgeführt werden:

### 1. Docker (Empfohlen für Server)

```bash
docker run -d -p 3000:3000 --name dbgate dbgate/dbgate
```

Anschließend Zugriff über `http://localhost:3000`.

Für ein `docker-compose.yml`-Setup:

```yaml
version: '3'
services:
  dbgate:
    image: dbgate/dbgate
    ports:
      - "3000:3000"
    restart: unless-stopped
```

### 2. Node Package Manager (NPM)

```bash
npm install -g dbgate
dbgate
```

Zugriff über `http://localhost:3000`.

### 3. Desktop-Installationsprogramm

Laden Sie vorgefertigte Installationsprogramme für Windows, macOS und Linux von der [GitHub-Releases-Seite](https://github.com/dbgate/dbgate/releases) herunter.

### 4. Cloud-Bereitstellungen

Ein-Klick-Bereitstellungsoptionen sind für Heroku, Railway und ähnliche Plattformen verfügbar.

## Schnellstart / Verwendung

### 1. DBGate starten

Navigieren Sie in Ihrem Browser zu `http://localhost:3000`.

### 2. Eine Verbindung hinzufügen

Klicken Sie auf das **+**-Symbol neben **Verbindungen**. Wählen Sie Ihre Datenbank-Engine (z. B. PostgreSQL) und geben Sie die Verbindungsdaten ein: Host, Port, Benutzername, Passwort, Datenbank.

### 3. Daten durchsuchen

Klicken Sie auf die gespeicherte Verbindung, um einen Baum der Datenbanken/Tabellen anzuzeigen. Klicken Sie auf eine Tabelle, um ihre Zeilen anzuzeigen.

### 4. Datenbank abfragen

Klicken Sie auf die Schaltfläche **Abfrage**, um den SQL-Editor zu öffnen. Schreiben Sie Ihre SQL und drücken Sie **Ausführen** (oder `Strg+Eingabe`).

### 5. Schema visualisieren

Klicken Sie mit der rechten Maustaste auf eine Datenbank oder Tabelle und wählen Sie **ER-Diagramm**, um ein visuelles Schema zu generieren.

### 6. Daten exportieren

Klicken Sie mit der rechten Maustaste auf eine Tabelle oder ein Ergebnisset und wählen Sie **Exportieren**, um Daten in Ihrem bevorzugten Format (CSV, JSON, SQL usw.) herunterzuladen.

## Befehlsbeispiele

**DBGate mit Docker starten und Daten dauerhaft speichern:**

```bash
docker run -d \
  -p 3000:3000 \
  -v dbgate-data:/home/app/.dbgate \
  --name dbgate \
  dbgate/dbgate
```

**Verwendung mit einer lokalen PostgreSQL-Instanz in einem Entwicklungsstack:**

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: example
  dbgate:
    image: dbgate/dbgate
    ports:
      - "3000:3000"
    depends_on:
      - postgres
```

**Mit npm installieren und ausführen:**

```bash
npm install -g dbgate
dbgate
```

**Verbindung mit Umgebungsvariablen herstellen (fortgeschritten):**

```bash
docker run -d \
  -e DBGATE_SERVER_NAME=myPostgres \
  -e DBGATE_SERVER_TYPE=postgres \
  -e DBGATE_SERVER_HOST=192.168.1.100 \
  -e DBGATE_SERVER_PORT=5432 \
  -e DBGATE_SERVER_USER=admin \
  -e DBGATE_SERVER_PASSWORD=secret \
  -p 3000:3000 \
  dbgate/dbgate
```

## Anwendungsfälle

1. **Remoteserver-Verwaltung** – Verwalten Sie Datenbanken auf einem VPS oder einer Cloud-Instanz ohne SSH-Tunneling oder Installation nativer Clients.
2. **Entwicklungsumgebungen** – Fügen Sie DBGate in einen `docker-compose.yml`-Stack ein, um Entwicklern sofortigen GUI-Zugriff auf ihre lokalen Datenbanken zu geben.
3. **Team-Tools** – Stellen Sie eine zentralisierte DBGate-Instanz (mit entsprechender Authentifizierung) bereit, damit ein Team Zugriff auf Entwicklungs- oder Staging-Datenbanken teilen kann.
4. **Bildung und Schulung** – Stellen Sie Schülern schnell eine SQL-Oberfläche zur Verfügung, ohne Client-Installationen verwalten zu müssen.
5. **Plattformübergreifende Workflows** – Wechseln Sie nahtlos zwischen Betriebssystemen mit derselben Weboberfläche.

## Architektur

DBGate besteht aus:

- **Backend:** Node.js/Express-Server, der Datenbankverbindungen, Abfrageausführung und API-Endpunkte verwaltet.
- **Frontend:** React-basierte SPA, die die Benutzeroberfläche bereitstellt, einschließlich SQL-Editor, Datenbrowser und Schema-Viewer.
- **Datenbanktreiber:** Unterstützt mehrere Datenbank-Engines über native Node.js-Treiber oder ODBC/JDBC-Brücken.

Die Anwendung speichert Verbindungen, SQL-Skripte und andere Objekte im lokalen Speicher (oder optionalem Cloud-Speicher für die gehostete Version). Das Docker-Image bündelt alle Abhängigkeiten für eine Ein-Port-Bereitstellung.

## Einschränkungen

- **Erweiterte IDE-Funktionen:** Es fehlen möglicherweise einige Funktionen, die in IntelliJ DataGrip zu finden sind (z. B. verteiltes Refactoring, erweiterte Codeanalyse).
- **Leistung:** Das Rendern sehr großer Datensätze (>100 Tsd. Zeilen) im Browser kann langsamer sein als bei nativen Apps. Exportvorgänge werden serverseitig für eine bessere Leistung durchgeführt.
- **Authentifizierung:** Die Open-Source-Version enthält keine integrierte Benutzerauthentifizierung; Sie müssen sie für den Teameinsatz mit einem Reverse-Proxy (wie nginx + auth_basic) vorschalten.

## Zusammenfassung

DBGate ist ein leistungsstarkes, flexibles und Open-Source-Datenbankverwaltungstool, das die Lücke zwischen leichten Webclients (wie phpMyAdmin) und schweren nativen IDEs (wie DataGrip) schließt. Seine plattformübergreifende Natur, das containerfreundliche Design und der wachsende Funktionsumfang machen es zu einer ausgezeichneten Wahl für Entwickler, DBAs und Teams, die einen modernen, webbasierten Datenbankclient suchen.

---

*Dokument erstellt am 2026-06-20. Besuchen Sie das [offizielle Repository](https://github.com/dbgate/dbgate) für die neuesten Aktualisierungen.*