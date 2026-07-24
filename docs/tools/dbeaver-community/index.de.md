---
title: DBeaver Community
description: Eine kostenlose, offene-Quelltext-Entwicklungsplattform zur Datenbankverwaltung, die für persönliche Projekte empfohlen wird. Verwalten und erkunden Sie SQL-Datenbanken wie MySQL, MariaDB, PostgreSQL, SQLite, Apache-Produkte und vieles mehr.
created: 2026-07-24
tags:
  - database
  - sql
  - management
  - development
  - tool
status: draft
---

# DBeaver Community

DBeaver ist eine offene-Quelltext-Plattform zur universellen Datenbankverwaltung, die eine Vielzahl von Datenbanken unterstützt, einschließlich SQL Server, MySQL, PostgreSQL, Oracle, SQLite und vieles mehr. Sie wurde 2013 veröffentlicht und ist seitdem ein beliebter Wahl für Entwickler, Datenbankadministratoren und Datenanalytiker zur Datenbankverwaltung, -entwicklung und -administration.

## Kernfunktionen

1. **Datenbankverwaltung**: DBeaver unterstützt eine breite Palette von Datenbanken und deren Tools, wie SQL-Abfragesammler, Datenbanken-Explorer, Schemaberichtigungsprogramme und Abfragehistorien.
2. **Datenmodellierung und -Design**: DBeaver ermöglicht es Nutzern, Schemata durch ein grafisches Benutzeroberfläche zu designen, zu verwalten und zu modifizieren.
3. **Datenbankverbindung**: Es kann zu verschiedenen Datenbanken mithilfe verschiedener Protokolle und Treiber verbunden werden.
4. **SQL-Editor**: Der SQL-Editor bietet Syntaxhervorhebung, Codevollständigung und einen automatischen Vorschlag.
5. **Datenexport und -import**: DBeaver bietet Werkzeuge zum Exportieren von Daten in CSV, Excel und andere Formate sowie zum Importieren von Daten aus diesen Formaten.
6. **Datenbanksynchronisierung**: Es unterstützt die Synchronisierung und Vergleich von Datenbankschema.
7. **Datenbankadministration**: DBeaver enthält Funktionen zur Verwaltung von Benutzern, Rollen und Berechtigungen und anderen administrativen Aufgaben.
8. **Grafisches Benutzeroberfläche**: Das Programm hat ein modernes, intuitives Oberfläche, das both Dark- und Light-Themen unterstützt.
9. **Plugins und Erweiterungen**: Nutzer können die Funktionalität von DBeaver durch Plugins erweitern, die von der DBeaver Marketplace installiert werden können.

## Geschichte

DBeaver wurde ursprünglich von Yvan Volckaert entwickelt und wurde 2013 als Community-Projekt veröffentlicht. Das Projekt wurde später vom DBeaver Community übernommen und gepflegt. 2017 wurde das Projekt zu einem kommerziellen Unternehmen, DBeaver GmbH, umgewandelt, das das Softwareprodukt weiter unterstützt und entwickelt.

## Nutzungsbereiche

1. **Datenbankentwicklung**: Entwickler können DBeaver für das Schreiben, Testen und Ausführen von SQL-Anfragen sowie das Verwalten von Datenbank-Strukturen verwenden.
2. **Datenanalyse**: Datenanalytiker können DBeaver verwenden, um große Datensätze zu abfragen und zu manipulieren, komplexe SQL-Anfragen auszuführen und Berichte zu erzeugen.
3. **Datenbankadministration**: Datenbankadministratoren können DBeaver verwenden, um Benutzerrechte, Rollen und andere administrative Aufgaben zu verwalten.
4. **Datenmigration**: Nutzer können DBeaver verwenden, um Daten zwischen verschiedenen Datenbanken zu migrieren, insbesondere wenn die Ziel-Datenbank eine andere Struktur hat.

## Installation

1. **Download**: Besuchen Sie den offiziellen DBeaver-Website (https://dbeaver.io/) um die neueste Version von DBeaver herunterzuladen.
2. **Installation**: Der Installationsprozess ist einfach. Auf Windows klicken Sie auf den Installer und folgen den Anweisungen auf dem Bildschirm. Auf macOS öffnen Sie das `.dmg`-Datei und fügen Sie das Programm in den Anwendungsordner hinzu. Auf Linux führen Sie das `.deb`- oder `.rpm`-Datei mit dem Paketverwaltungssystem aus.
3. **Starten**: Nach der Installation öffnen Sie DBeaver aus Ihrem Anwendungs-Menü.

### BeispielsKommando für Windows-Installer

```sh
sh DBeaver-<version>-win32-installer.exe
```

### BeispielsKommando für macOS-Installer

```sh
open DBeaver-<version>-macOS.dmg
```

### BeispielsKommando für Linux-Installer

```sh
sudo dpkg -i DBeaver-<version>.deb
```

oder

```sh
sudo rpm -i DBeaver-<version>.rpm
```

## Grundlegende Nutzung

1. **Verbindungsverwaltung**: Öffnen Sie DBeaver, klicken Sie auf "Datei" > "Neu" > "Datenbankverbindung", und konfigurieren Sie die Verbindungseinstellungen für Ihre Datenbank (Server, Port, Benutzername, Passwort).
2. **SQL-Editor**: Nach der Verbindung verwenden Sie den SQL-Editor, um SQL-Anfragen zu schreiben, auszuführen und zu verwalten.
3. **Schemabericht**: Verwenden Sie den Schemabericht, um die Datenbankstruktur zu erkunden, Tabellen, Views und andere Datenbankobjekte zu navigieren.
4. **Datenimport/Export**: Nutzen Sie die Import- und Exportfunktionen, um Daten zwischen verschiedenen Formaten oder Datenbanken zu bewegen.

## Befehlszeileninterface (dbvr)

DBeaver CLI (dbvr) ist ein Befehlszeileninterface zur Arbeit mit Datenbanken. Es kann als eigenständiges CLI-Programm oder in Verbindung mit DBeaver und CloudBeaver verwendet werden. Es bietet eine scriptbare Möglichkeit, Datenbankprojekte und Datenquellen zu verwalten, Metadaten abzurufen und SQL aus dem Terminal auszuführen.

### BeispielsKommando zur Verbindung mit einer Datenbank

```sh
dbvr connect --url jdbc:mysql://localhost:3306/mydb --username myuser --password mypassword
```

### BeispielsKommando zur Ausführung einer SQL-Anfrage

```sh
dbvr sql -c "SELECT * FROM mytable" -o results.csv
```

## Schlussfolgerung

DBeaver ist eine leistungsstarke und vielseitige Entwicklungstools, das eine breite Palette von Datenbankverwaltungsfunktionen bietet. Seine open-source-Natur und die aktive Community tragen dazu bei, dass es robust ist und regelmäßig aktualisiert wird, was es zu einem wertvollen Ressourcen für Datenbankprofis macht.