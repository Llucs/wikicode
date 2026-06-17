---
title: Visual Studio Code
description: Ein schlanker, aber leistungsstarker Quellcode-Editor, entwickelt von Microsoft, der als integriertes Entwicklungstool dient.
created: 2026-06-14
tags:
  - editor
  - development
  - microsoft
  - open-source
status: draft
ecosystem: editors
---

# Visual Studio Code

## Was ist VS Code?

Visual Studio Code (häufig als VS Code bezeichnet) ist ein kostenloser Open-Source-Quellcode-Editor, der von Microsoft entwickelt wurde. Auf Basis des Electron-Frameworks läuft er unter Windows, macOS und Linux. VS Code vereint die Geschwindigkeit und Einfachheit eines leichten Editors mit den fortschrittlichen Fähigkeiten einer integrierten Entwicklungsumgebung (IDE) durch eine umfangreiche Erweiterungsarchitektur.

## Warum VS Code?

- **Leistung**: Startet schnell und bleibt auch bei großen Projekten reaktionsschnell.
- **Erweiterbarkeit**: Tausende Erweiterungen fügen Sprachen, Designs, Debugger und Workflow-Tools hinzu.
- **Plattformunabhängigkeit**: Gleiche Erfahrung auf allen gängigen Betriebssystemen.
- **Integrierte Werkzeuge**: Git-Steuerung, Terminal, Debugging – alles im Editor.
- **Intelligente Bearbeitung**: IntelliSense bietet kontextbezogene Vervollständigungen, Parameterinformationen und Dokumentation.
- **Integrierte Unterstützung für moderne Workflows**: Docker, Remote-Entwicklung, Jupyter-Notebooks und mehr.

## Installation

### Download des Installers
Der einfachste Weg ist, das Installationsprogramm von der [offiziellen Website](https://code.visualstudio.com) herunterzuladen.

| Plattform | Installationstyp |
|-----------|-----------------|
| Windows   | `.exe` (Benutzer oder System) |
| macOS     | `.dmg` (in Programme ziehen) |
| Linux     | `.deb` (Debian/Ubuntu) oder `.rpm` (Fedora/RHEL) |

### Paketmanager

**macOS (Homebrew)**
```bash
brew install --cask visual-studio-code
```

**Linux (Snap)**
```bash
snap install code --classic
```

**Windows (winget)**
```bash
winget install Microsoft.VisualStudioCode
```

### Portabler Modus
Erstellen Sie einen `data`-Ordner im selben Verzeichnis wie die VS Code‑Ausführungsdatei. Der Editor speichert alle Konfigurationen, Erweiterungen und Benutzerdaten in diesem Ordner, was ihn vollständig portabel macht.

### Insiders Build
Für frühen Zugang zu Funktionen und tägliche Builds installieren Sie [VS Code Insiders](https://code.visualstudio.com/insiders). Es kann parallel zur stabilen Version installiert werden.

## Grundlegende Nutzung

### Ein Projekt öffnen
Starten Sie VS Code und verwenden Sie **Datei → Ordner öffnen** (oder `Ctrl+K Ctrl+O` / `Cmd+K Cmd+O`), um Ihr Projektverzeichnis zu öffnen.

### Befehlspalette
Die Befehlspalette bietet Zugriff auf jede Aktion in VS Code.

```text
Ctrl+Shift+P   (Windows/Linux)
Cmd+Shift+P    (macOS)
```

Häufige Befehle: `>Format Document`, `>Preferences: Open Settings`, `>Extensions: Install Extensions`.

### Dateien bearbeiten
- Die Syntaxhervorhebung erfolgt automatisch basierend auf der Dateierweiterung.
- **Multi-Cursor**: `Alt+Klick` (Windows/Linux) oder `Option+Klick` (macOS), um Cursor hinzuzufügen.
- **Klammernpaare**: Bewegen Sie den Cursor innerhalb der Klammern, das passende Paar wird hervorgehoben.
- **IntelliSense**: Manuell auslösen mit `Ctrl+Space`.

### Versionskontrolle
Öffnen Sie die Ansicht 'Quellcodeverwaltung' (`Strg+Umschalt+G` unter Windows/Linux, `Cmd+Umschalt+G` unter macOS), um Änderungen zu sehen, Dateien zu indexieren, Commits durchzuführen und Push/Pull auszuführen. Nutzen Sie das integrierte Terminal für komplexere Vorgänge.

### Integriertes Terminal
Starten Sie das Terminal mit `` Strg+` `` (Backtick). Das Terminal verwendet standardmäßig Ihre System-Shell (PowerShell, Bash, Zsh usw.).

### Erweiterungen
Öffnen Sie die Ansicht 'Erweiterungen' mit `Strg+Umschalt+X`. Suchen Sie nach einer beliebigen Erweiterung (z. B. „Python", „Prettier", „Docker") und installieren Sie sie mit einem Klick.

### Debugging
Setzen Sie Haltepunkte durch Klicken auf den Rand (Bereich der Zeilennummern) oder durch Drücken von `F9`. Drücken Sie `F5`, um das Debuggen mit der aktuell aktiven Konfiguration zu starten. Erstellen Sie eine `launch.json`-Datei, um die Debug-Einstellungen für Ihr Projekt zu konfigurieren.

## Hauptfunktionen mit Befehlsbeispielen

### IntelliSense
VS Code bietet intelligente Vervollständigungen basierend auf Sprachdiensten, Variablentypen und Funktionsdefinitionen.

```javascript
// Example: Typing "console." then using Ctrl+Space shows methods like log, warn, error
console.log("Hello, VS Code!");
```

**IntelliSense manuell auslösen**: `Ctrl+Space` (Windows/Linux) oder `Cmd+Space` (macOS).

**Parameterhinweise**: Beim Aufrufen einer Funktion zeigt VS Code die erwarteten Parameter an.

### Integriertes Debugging
Vollständige Debugging-Unterstützung mit Startkonfigurationen.

**launch.json-Beispiel für Node.js:**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "node",
            "request": "launch",
            "name": "Launch Program",
            "skipFiles": ["<node_internals>/**"],
            "program": "${workspaceFolder}/app.js"
        }
    ]
}
```

**Wichtige Debugging-Befehle:**
| Action | Keys |
|--------|------|
| Start/Continue | `F5` |
| Step Over | `F10` |
| Step Into | `F11` |
| Step Out | `Shift+F11` |
| Toggle Breakpoint | `F9` |

### Integriertes Git
Visuelle Quellcodeverwaltung mit Staging, Committing, Branching und mehr.

**Befehlspaletten-Entsprechungen:**
- `>Git: Commit` – übernimmt bereitgestellte Änderungen.
- `>Git: Create Branch` – erstellt einen neuen Branch.
- `>Git: Clone` – klont ein entferntes Repository.
- `>Git: Pull` / `>Git: Push` – synchronisiert Änderungen.

### Erweiterungs-Marktplatz
Installieren Sie Erweiterungen, um Sprachen, Linter, Designs, Snippets und Debugger hinzuzufügen.

**Beispiel: Python-Erweiterung installieren**
1. Öffnen Sie die Ansicht 'Erweiterungen' (`Strg+Umschalt+X`).
2. Suchen Sie nach „Python" (von Microsoft).
3. Klicken Sie auf **Installieren**.

**Beliebte Erweiterungen:**
- Python
- Prettier – Code formatter
- ESLint
- Docker
- Live Server
- GitLens
- Jupyter

### Integriertes Terminal
Führen Sie Shell-Befehle aus, ohne VS Code zu verlassen.

```bash
# Example: inside the integrated terminal
npm install && npm start
```

Öffnen/Schließen Sie das Terminal mit `` Strg+` ``. Es können mehrere Terminals erstellt werden (z. B. eines für den Build, eines für Git).

### Remote-Entwicklung
Verbinden Sie sich mit entfernten Umgebungen wie:
- **WSL** (Windows-Subsystem für Linux)
- **SSH**-Remote-Rechner
- **Dev Containers** (Docker)
- **GitHub Codespaces**

**Beispiele für die Befehlspalette:**
- `>Remote‑SSH: Connect to Host…`
- `>Dev Containers: Reopen in Container`

Sie müssen den Editor nicht verlassen – Ihre gesamte Entwicklungsumgebung wird lokal erreicht.

## Weitere Tipps

### Einstellungen synchronisieren
Melden Sie sich mit einem Microsoft- oder GitHub-Konto an, und Ihre Einstellungen, Tastenkombinationen und Erweiterungen werden geräteübergreifend synchronisiert.

**Befehlspalette**: `>Turn on Settings Sync…`

### Snippets
Erstellen Sie benutzerdefinierte Code-Snippets für wiederkehrende Muster.

**Datei → Einstellungen → Benutzersnippets konfigurieren** → Sprache auswählen.

```json
// Example JavaScript snippet (in javascript.json)
{
    "Arrow Function": {
        "prefix": "arr",
        "body": ["const ${1:name} = (${2:params}) => {", "\t${3:body}", "};"],
        "description": "Create an arrow function"
    }
}
```

### Multi-Cursor-Bearbeitung
- `Alt+Klick` – Cursor hinzufügen.
- `Strg+Alt+Nach oben/unten` – Cursor oberhalb/unterhalb einfügen.
- `Strg+D` – nächstes Vorkommen der aktuellen Auswahl auswählen.

### Zen-Modus
Konzentrieren Sie sich auf den Code ohne Ablenkungen: `Strg+K Z` (Windows/Linux) oder `Cmd+K Z` (macOS). Umschalten mit `Esc Esc`.

## Fazit

Visual Studio Code ist ein vielseitiger Editor, der Geschwindigkeit, Leistung und Anpassungsfähigkeit vereint. Durch die Beherrschung seiner Kernfunktionen – IntelliSense, Debugging, Git-Integration, das Terminal und das Erweiterungsökosystem – können Sie Ihren Entwicklungsworkflow für jede Sprache oder Plattform optimieren.

Für tiefere Einblicke lesen Sie die [offizielle VS Code-Dokumentation](https://code.visualstudio.com/docs).