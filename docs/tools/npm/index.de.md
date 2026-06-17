---
title: npm - Node-Paketmanager
description: Ein Paketmanager für Node.js, der ein grundlegendes Werkzeug zur Verwaltung von JavaScript-Abhängigkeiten ist.
created: 2026-06-14
tags:
  - package-manager
  - javascript
  - nodejs
  - cli
  - dependency-management
status: draft
ecosystem: javascript
---

# npm – Node Package Manager

npm (Node Package Manager) ist der standardmäßige Paketmanager für die Node.js-JavaScript-Laufzeitumgebung. Es besteht aus zwei Hauptkomponenten: einem **CLI** (Befehlszeilenschnittstelle) zur Verwaltung von Abhängigkeiten und der **npm Registry**, einer riesigen öffentlichen Datenbank von JavaScript-Paketen. Es hat sich zu einem unverzichtbaren Werkzeug im JavaScript-Ökosystem entwickelt, das es Entwicklern ermöglicht, Code effizient zu teilen, wiederzuverwenden und zu verwalten.

## Was ist npm?

npm bietet eine Möglichkeit, um:

- **Abhängigkeiten installieren und verwalten** – Pakete in `package.json` und Lock-Dateien nachverfolgen.
- **Pakete veröffentlichen** – eigene Bibliotheken mit der Community oder Organisation teilen.
- **Skripte ausführen** – Build-, Test- und Bereitstellungsworkflows automatisieren.
- **Monorepos verwalten** – mit Workspaces mehrere Pakete in einem Repository verwalten.

## Warum npm verwenden?

- **Standardisierung** – npm ist gebündelt mit Node.js, was es zur Standardwahl für die meisten JavaScript-Projekte macht.
- **Riesiges Ökosystem** – über 2 Millionen Pakete in der Registry, die praktisch jeden Bedarf abdecken.
- **Reproduzierbarkeit** – die Datei `package-lock.json` sorgt für deterministische Installationen in verschiedenen Umgebungen.
- **Sicherheit** – `npm audit` hilft dir, Schwachstellen in deinem Abhängigkeitsbaum zu finden und zu beheben.
- **Komfort** – `npx` ermöglicht das Ausführen von Paketen ohne globale Installation, und Skripte vereinfachen gängige Aufgaben.

## Installation

npm wird automatisch mit Node.js installiert. So erhältst du die neueste LTS-Version:

1. Lade Node.js von [nodejs.org](https://nodejs.org/) herunter.
2. Überprüfe die Installation:

```bash
node -v
npm -v
```

### Installation über Versionsverwaltung (nvm/fnm)

Die Verwendung eines Versionsmanagers ermöglicht es dir, zwischen Node.js-Versionen zu wechseln und npm für jede zu installieren:

```bash
# Example with nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install --lts
```

Nach der Installation ist npm einsatzbereit.

## Grundlegende Verwendung

### Ein Projekt initialisieren

Ein neues Projekt erstellen oder einen vorhandenen Ordner umwandeln:

```bash
npm init -y
```

Dies erzeugt eine `package.json`-Datei mit Standardwerten. Verwende `npm init` (ohne `-y`) für eine interaktive Abfrage.

### Abhängigkeiten installieren

```bash
# Production dependency
npm install lodash

# Dev-only dependency
npm install --save-dev jest

# Global package (use sparingly; prefer npx)
npm install -g nodemon

# Install all dependencies from package.json
npm install
```

### Bestimmte Versionen installieren

```bash
npm install react@18.2.0
npm install "express@>=4.17.0 <5.0.0"
```

### Skripte ausführen

Skripte werden unter dem Schlüssel `"scripts"` in `package.json` definiert. Häufige Abkürzungen:

```bash
npm start        # runs the "start" script
npm test         # runs the "test" script
npm run build    # custom script, e.g., "build"
```

### Pakete deinstallieren

```bash
npm uninstall lodash
```

### Pakete aktualisieren

```bash
npm update                # update all packages within version ranges
npm install lodash@latest # force a specific version update
```

### Auf Schwachstellen prüfen

```bash
npm audit
```

Um automatisch zu beheben (wo verfügbar):

```bash
npm audit fix
```

### Saubere Installation für CI

```bash
npm ci
```

`npm ci` ist schneller und entfernt `node_modules`, bevor es genau aus der `package-lock.json` installiert.

## Wichtige Funktionen

### npx – Pakete ohne Installation ausführen

`npx` wird mit npm ausgeliefert und ermöglicht es dir, Binärdateien aus der Registry ohne globale Installationen auszuführen:

```bash
npx create-react-app my-app
npx cowsay "Hello, npm!"
```

Wenn das Paket bereits lokal installiert ist, verwendet `npx` diese Version.

### Workspaces (Monorepo-Unterstützung)

npm-Workspaces ermöglichen es dir, mehrere Pakete in einem einzigen Repository zu verwalten:

```json
{
  "workspaces": [
    "packages/*"
  ]
}
```

Dann kannst du Befehle über alle Workspaces hinweg ausführen:

```bash
npm install              # installs dependencies for all workspaces
npm run test --workspaces
```

Die Verknüpfung zwischen Workspace-Paketen wird automatisch verwaltet.

### Lifecycle-Hooks für Skripte

npm stellt Pre/Post-Hooks für gängige Skripte bereit:

- `prepublish` / `postpublish`
- `preinstall` / `postinstall`
- `prebuild` / `postbuild`

Beispiel:

```json
{
  "scripts": {
    "prebuild": "rimraf dist",
    "build": "webpack --config webpack.prod.js"
  }
}
```

### package-lock.json

Diese Datei sperrt die exakte Version jeder Abhängigkeit und ihrer transitiven Abhängigkeiten. Sie stellt sicher, dass jeder, der `npm install` ausführt, denselben Abhängigkeitsbaum erhält, was Builds reproduzierbar macht.

### Overrides und Auflösungen

Du kannst bestimmte Versionen von transitiven Abhängigkeiten in der `package.json` erzwingen:

```json
{
  "overrides": {
    "graceful-fs": "4.2.11"
  }
}
```

Dies ist nützlich, wenn eine Unterabhängigkeit eine Schwachstelle aufweist, die du patchen musst, ohne auf die Veröffentlichung der übergeordneten Abhängigkeit zu warten.

### npm config

Passe das npm-Verhalten global oder pro Projekt an:

```bash
npm config set init-author-name "Your Name"
npm config get registry
npm config delete <key>
```

Du kannst auch eine `.npmrc`-Datei im Projektstammverzeichnis verwenden.

### Globale Pakete vs. npx

Globale Installationen sollten Werkzeugen vorbehalten sein, die du projektübergreifend verwendest (z. B. `npm`, `yarn`, `node-gyp`). Für einmalige Befehle bevorzuge `npx`, um den globalen Namensraum nicht zu überladen und sicherzustellen, dass du immer die vorgesehene Version verwendest.

## Fazit

npm ist ein leistungsstarkes und unverzichtbares Werkzeug für jeden JavaScript-Entwickler. Von der einfachen Installation von Abhängigkeiten bis hin zur komplexen Verwaltung von Monorepos hilft sein umfangreicher Funktionsumfang dabei, Projekte organisiert, sicher und reproduzierbar zu halten. Egal, ob du eine kleine Bibliothek oder eine große Anwendung erstellst, die Beherrschung von npm wird deinen Workflow erheblich verbessern.