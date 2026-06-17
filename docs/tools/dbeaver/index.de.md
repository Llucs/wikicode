---
title: DBeaver - Universelles Datenbankverwaltungstool
description: Ein kostenloses, quelloffenes, plattformunabhängiges Datenbankverwaltungstool und SQL-Client für Entwickler, DBAs und Datenanalysten.
created: 2026-06-17
tags:
  - database
  - sql
  - management
  - tools
  - open-source
status: draft
---

# DBeaver - Universelles Datenbankverwaltungstool

## Übersicht

DBeaver ist ein **kostenloses, quelloffenes, plattformunabhängiges** Datenbankverwaltungstool und SQL-Client. Es bietet eine umfangreiche grafische Oberfläche zur Interaktion mit jeder Datenbank, die JDBC- oder ODBC-Treiber unterstützt, und ist somit ein universelles Werkzeug für Entwickler, Datenbankadministratoren und Datenanalysten.

- **Lizenz**: Die Community Edition (CE) wird unter der **Apache 2.0**-Lizenz veröffentlicht; kommerzielle Pro/Enterprise/Team-Editionen sind ebenfalls erhältlich.
- **Plattform**: Windows, macOS, Linux (auch als portable Anwendung verfügbar).
- **Architektur**: Basierend auf der Eclipse Rich Client Platform (RCP) unter Verwendung von Java.
- **Geschichte**: Gestartet im Jahr 2010 von Serge Rielau, einem Datenbankexperten, der zuvor an Apache Derby und Oracle beteiligt war. Das Projekt gewann schnell breite Akzeptanz, was zur Gründung von DBeaver Corp. führte.

DBeaver ist ideal für:
- **Anwendungsentwicklung** – SQL-Abfragen schreiben, debuggen und optimieren.
- **Datenbankverwaltung** – Schemas, Benutzer, Sitzungen und Indizes verwalten.
- **Datenanalyse** – Analytische Abfragen ausführen und Ergebnisse in verschiedenen Formaten exportieren.
- **Datenengineering** – Daten zwischen verschiedenen Datenbanken ohne aufwändige Skripterstellung übertragen.
- **Bildung** – SQL und relationale Datenbankkonzepte durch eine intuitive grafische Benutzeroberfläche erlernen.

## Hauptmerkmale

| Feature | Beschreibung |
|---------|-------------|
| **Umfassende Datenbankunterstützung** | Verbindet sich standardmäßig mit über 100 Datenbanken, darunter MySQL/MariaDB, PostgreSQL, Oracle, SQL Server, SQLite, DB2, Snowflake, Redshift, ClickHouse und viele mehr. |
| **Erweiterter SQL-Editor** | Syntaxhervorhebung, Code-Vervollständigung, Abfrageausführung mit mehreren Ergebnisregistern, Ausführungsplanvisualisierung (grafisch), SQL-Formatierung und parametrisierte Abfragen. |
| **Datenbrowser / Tabellenansicht** | Leistungsstarke Inline-Bearbeitung, erweiterte Filterung, Sortierung und Handhabung von BLOB/CLOB-Daten direkt in einer Rasteroberfläche. |
| **ER-Diagramme** | Automatische Generierung von Entity-Relationship-Diagrammen mit Reverse Engineering (Rechtsklick auf ein Schema oder eine Tabelle). |
| **Schemaverwaltung** | Objektbrowser zum Durchsuchen, Erstellen und Bearbeiten von Tabellen, Ansichten, Indizes, Prozeduren und Funktionen. |
| **Datentransfer** | Massenexport/-import zwischen Datenbanken und Dateiformaten (CSV, JSON, XML, Excel, SQL, Markdown, HTML). |
| **Verwaltungswerkzeuge** | Sitzungsmanager, Aufgabenplaner (Pro), Benutzer-/Rollenverwaltung und integrierte SSH/SSL/Proxy-Tunnelung. |
| **Erweiterbarkeit** | Plugin-Architektur; verfügbares Plugin für zusätzliche Treiber, Versionskontrolle (Git) und Diagrammanpassungen. |
| **Plattformunabhängigkeit** | Läuft auf Windows, macOS und Linux. |

## Installation

DBeaver ist über mehrere Kanäle verfügbar. Wählen Sie die Methode, die zu Ihrer Umgebung passt.

### Offizieller Installer (Alle Plattformen)

Laden Sie das Installationsprogramm für Ihr Betriebssystem von [dbeaver.io](https://dbeaver.io) (Community Edition) oder [dbeaver.com](https://dbeaver.com) (Enterprise) herunter.

### Paketverwalter

**macOS (Homebrew)**
```bash
brew install --cask dbeaver-community
```

**Linux (Snap)**
```bash
sudo snap install dbeaver-ce
```

**Linux (APT / YUM – Offizielle Debian/RPM-Repositorys)**
```bash
# Debian/Ubuntu
wget -O - https://dbeaver.io/debs/dbeaver.gpg.key | sudo apt-key add -
echo "deb https://dbeaver.io/debs/dbeaver-ce /" | sudo tee /etc/apt/sources.list.d/dbeaver.list
sudo apt update && sudo apt install dbeaver-ce

# RHEL/CentOS/Fedora
sudo rpm --import https://dbeaver.io/rpms/dbeaver.gpg.key
sudo yum install dbeaver-ce
```

**Windows (winget / Chocolatey)**
```powershell
# winget (Windows 10 / 11)
winget install DBeaver.DBeaverCE

# Chocolatey
choco install dbeaver
```

**Portable Windows-Version**

Eine portable ausführbare Datei ist auf der offiziellen Website erhältlich, ideal zum Ausführen von einem USB-Laufwerk ohne Installation.

## Erste Schritte – Grundlegende Nutzung

### 1. Datenbankverbindung erstellen

1. Starten Sie DBeaver.
2. Klicken Sie auf die Schaltfläche **Neue Datenbankverbindung** (Steckersymbol) in der Symbolleiste.
3. Wählen Sie Ihren Datenbanktyp (z. B. **PostgreSQL**).
4. Geben Sie die Verbindungsdetails ein:
   - Host, Port, Datenbankname, Benutzername, Passwort.
5. Klicken Sie auf **Verbindung testen**. DBeaver fordert automatisch zum Herunterladen des erforderlichen JDBC-Treibers auf, falls dieser noch nicht zwischengespeichert ist.
6. Klicken Sie auf **Fertigstellen**. Die Verbindung erscheint im Bereich **Datenbanknavigator**.

![Beispiel für den Verbindungsassistenten](https://dbeaver.com/docs/images/connection-wizard.png) <!-- Placeholder URL; actual docs provide screenshots -->

### 2. Daten durchsuchen und abfragen

- Im **Datenbanknavigator** erweitern Sie eine Verbindung, um Schemas, Tabellen, Ansichten usw. anzuzeigen.
- Klicken Sie mit der rechten Maustaste auf eine Tabelle und wählen Sie **Daten anzeigen**, um ein Datenraster zu öffnen.
- Um benutzerdefiniertes SQL zu schreiben, drücken Sie `Ctrl + ]` (Windows/Linux) oder `Cmd + ]` (macOS), um einen neuen **SQL-Editor** zu öffnen.

**Beispiel-SQL-Abfrage:**
```sql
-- Select users with their latest order
SELECT u.id, u.name, o.order_date
FROM users u
JOIN (
    SELECT user_id, MAX(order_date) AS order_date
    FROM orders
    GROUP BY user_id
) o ON u.id = o.user_id
ORDER BY o.order_date DESC;
```

- Führen Sie die Abfrage mit `Ctrl + Enter` (Win/Lin) oder `Cmd + Enter` (macOS) aus.
- Die Ergebnisse erscheinen im Ergebnisraster unter dem Editor.

### 3. Daten bearbeiten und exportieren

- Klicken Sie direkt auf einen Zellenwert im Ergebnisraster, um ihn zu bearbeiten (erfordert **Bearbeitungs**berechtigung für die Tabelle).
- Klicken Sie mit der rechten Maustaste auf das Ergebnisraster und wählen Sie **Daten exportieren**.
- Wählen Sie das gewünschte Format (CSV, Excel, JSON, SQL INSERT, XML, Markdown usw.) und konfigurieren Sie die Optionen.

## Erweiterte Nutzung

### Entity‑Relationship (ER)-Diagramme

DBeaver kann ER-Diagramme für ein Schema oder bestimmte Tabellen generieren.

1. Klicken Sie mit der rechten Maustaste auf ein Schema im Datenbanknavigator.
2. Wählen Sie **Diagramm anzeigen** (oder öffnen Sie den Tab **ER-Diagramm**).
3. Das Diagramm zeigt Tabellen, Spalten, Beziehungen und Indizes an.
4. Sie können Elemente neu anordnen, das Diagramm als Bild exportieren oder es ausdrucken.

### Datentransfer / Migration

Verwenden Sie den Assistenten **Daten übertragen**, um Daten zwischen Datenbanken zu kopieren oder Daten in Dateien zu extrahieren.

1. Klicken Sie mit der rechten Maustaste auf eine Tabelle oder ein Schema.
2. Wählen Sie **Daten > Daten übertragen**.
3. Wählen Sie die Quelle (z. B. eine Tabelle) und das Ziel (eine andere Datenbankverbindung oder Datei).
4. Konfigurieren Sie Spaltenzuordnungen und Transformationsregeln.
5. Führen Sie die Übertragung aus.

### Ausführungsplan (EXPLAIN)

Visualisieren Sie den Abfrageausführungsplan für die SQL-Optimierung.

1. Schreiben Sie im SQL-Editor eine Abfrage.
2. Klicken Sie auf die Schaltfläche **Plan erklären** (oder Rechtsklick → **Plan erklären**).
3. DBeaver zeigt einen grafischen Plan mit Kostendetails und Indexnutzung an.

### Vergleichswerkzeug (Pro/Enterprise)

Mit den Werkzeugen **Struktur vergleichen** und **Daten vergleichen** können Sie Schemas oder Daten zwischen zwei Datenbanken oder Umgebungen vergleichen.

- Verfügbar in den kommerziellen Editionen.

## Konfiguration und Anpassung

### Verbindungseinstellungen

- **Treibereigenschaften**: Ändern Sie JDBC-Treiberattribute (z. B. Timeouts, SSL-Modus, Blockgrößen) im Verbindungseditor.
- **SSH-Tunnel**: Konfigurieren Sie SSH-Tunneling für den sicheren Zugriff auf entfernte Datenbanken (im **SSH**-Tab der Verbindungseinstellungen).
- **SSL**: Aktivieren Sie SSL und importieren Sie Zertifikate über den **SSL**-Tab.

### Globale Einstellungen

- `Window → Preferences` (Windows/Linux) oder `DBeaver → Preferences` (macOS).
- **Erscheinungsbild**: Wechseln Sie zwischen hellen/dunklen Themen, passen Sie Schriftgrößen an.
- **Editoren**: Konfigurieren Sie SQL-Formatierungsstil, Autovervollständigungsverhalten und Ausführungsoptionen.
- **Verbindungen**: Legen Sie Standard-Transaktionsisolationsstufen, Auto-Commit und Leerlauf-Timeouts fest.

### Treiberverwaltung

- **Treibermanager**: `Database → Driver Manager`. Zeigen Sie benutzerdefinierte JDBC-Treiber an, bearbeiten Sie sie oder fügen Sie sie hinzu.
- Laden Sie fehlende Treiber direkt aus dem DBeaver-Treiberrepository herunter, wenn Sie zum ersten Mal eine Verbindung zu einer Datenbank herstellen.

## Automatisierung und Skripterstellung

### DBeaver CLI (nur Pro/Enterprise)

DBeaver Pro/Enterprise enthält ein Befehlszeilentool (`dbeaver-cli`) zum Ausführen von SQL-Skripten, Exportieren von Daten oder Ausführen von Aufgaben ohne GUI.

```bash
# Connect and run a script against a PostgreSQL instance
dbeaver-cli -driver postgresql -url jdbc:postgresql://localhost:5432/mydb \
            -user myuser -password mypass -script query.sql
```

### Aufgabenplaner (Pro/Enterprise)

Planen Sie wiederkehrende Exporte, Datentransfers oder SQL-Skripte mit dem integrierten Planer (cron-ähnliche Oberfläche).

## Integrationen

- **Versionskontrolle**: Git-Integrationsplugin (in Community verfügbar) – SQL-Skripte committen oder mit committeten Versionen vergleichen.
- **Docker**: DBeaver direkt in einem Container für CI/CD-Pipelines auszuführen ist mit der CLI-Edition möglich.
- **Cloud-Datenbanken**: Vorkonfigurierte Treiber für Snowflake, Amazon Redshift, Google BigQuery, Azure SQL usw.
- **SSH/SSL**: Integrierte Unterstützung für sichere Verbindungen und Proxy-Authentifizierung.

## Kompatibilität und Leistung

| Aspekt | Details |
|--------|---------|
| **Unterstützte Betriebssysteme** | Windows 10+, macOS 10.15+, Linux (x64, amd64, aarch64) |
| **Java-Anforderungen** | JDK 11 oder höher (in den Installern enthalten) |
| **Datenbankunterstützung** | Über 100 Datenbanken über JDBC/ODBC (einschließlich relationale, NoSQL-ähnliche, Cloud) |
| **Leistungstipps** | - Verwenden Sie Indizes für große Abfragen.<br>- Schließen Sie im Leerlauf befindliche Verbindungen in den Einstellungen.<br>- Aktivieren Sie **„Batch-Updates verwenden“** für Massenvorgänge.<br>- Verwenden Sie bei extrem großen Datensätzen den Export in Blöcken oder dedizierte Migrationswerkzeuge. |

## Fehlerbehebung und FAQ

### Häufige Probleme

1. **„Treiber nicht gefunden“ / „Verbindung kann nicht hergestellt werden“**
   - DBeaver fordert zum Herunterladen des Treibers auf. Wenn der automatische Download fehlschlägt, gehen Sie zu `Database → Driver Manager`, wählen Sie Ihre Datenbank aus und klicken Sie auf **Herunterladen/Aktualisieren**.
   - Stellen Sie sicher, dass Sie Internetzugang haben, oder platzieren Sie die JAR-Datei manuell im Treiberverzeichnis.

2. **Verbindung hängt oder Zeitüberschreitung**
   - Überprüfen Sie die Netzwerkkonnektivität und Firewall-Regeln.
   - Überprüfen Sie die SSH/SSL-Einstellungen; ein falsch konfigurierter Tunnel kann Verbindungen blockieren.
   - Erhöhen Sie das Verbindungs-Timeout in den Treibereigenschaften.

3. **Leistung des SQL-Editors ist langsam**
   - Deaktivieren Sie das automatische Laden von Metadaten: `Preferences → Database → Navigator → Disable lazy metadata reading`.
   - Reduzieren Sie das Ergebnislimit in der Editor-Symbolleiste.

4. **BLOB/CLOB kann nicht bearbeitet werden**
   - DBeaver unterstützt Inline-Bearbeitung für kleine Objekte. Verwenden Sie für große Objekte den Dialog **Wert anzeigen/bearbeiten** (Rechtsklick auf Zelle → **Wert anzeigen**).

### Häufig gestellte Fragen

**F: Ist DBeaver vollständig kostenlos?**
A: Die Community Edition ist kostenlos und quelloffen (Apache 2.0). Die Pro-, Enterprise- und Team-Editionen sind kommerziell und bieten zusätzliche Funktionen wie NoSQL-Unterstützung, KI-Assistenz und eine CLI.

**F: Kann ich DBeaver für Produktionsdatenbanken verwenden?**
A: Ja, die Community Edition ist produktionsreif für Entwicklungs- und DBA-Aufgaben. Für sicherheitskritische Umgebungen sollten Sie die Enterprise-Edition mit zusätzlichem Support und Auditing in Betracht ziehen.

**F: Arbeitet DBeaver mit MongoDB oder anderen NoSQL-Datenbanken?**
A: Die Community Edition bietet grundlegende MongoDB-Unterstützung. Vollständige NoSQL- und Cloud-DB-Unterstützung (einschließlich MongoDB, Cassandra und DynamoDB) sind in der Enterprise-Edition verfügbar.

**F: Wie deinstalliere ich DBeaver vollständig?**
A: Verwenden Sie den Paketmanager Ihres Systems (z. B. `brew uninstall --cask dbeaver-community`, `snap remove dbeaver-ce`) oder den Deinstaller des Betriebssystems. Benutzereinstellungen werden unter `~/.dbeaver` auf macOS/Linux oder `%APPDATA%\DBeaver` unter Windows gespeichert; löschen Sie diese Verzeichnisse, um alle Konfigurationen zu entfernen.

## Fazit

DBeaver ist ein leistungsstarkes, flexibles und benutzerfreundliches Datenbanktool, das sich nahtlos in den Workflow jedes Entwicklers einfügt. Sein quelloffener Kern, die umfangreiche Datenbankunterstützung und der reiche Funktionsumfang machen es zu einem unverzichtbaren Werkzeug für alle, die mit Daten arbeiten.

Weitere Informationen finden Sie in der offiziellen Dokumentation unter [dbeaver.com/docs](https://dbeaver.com/docs/) oder tragen Sie zur Community auf [GitHub](https://github.com/dbeaver/dbeaver) bei.