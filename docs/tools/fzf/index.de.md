---
title: fzf - Kommandozeilen-Fuzzy-Finder
description: Ein Fuzzy-Finder für die Kommandozeile, der die Datei- und Textsuche im Terminal verbessert.
created: 2026-06-15
tags:
  - command-line
  - fuzzy-finder
  - fzf
  - productivity
  - terminal
status: draft
ecosystem: cli
---

# fzf – Allgemeiner Fuzzy-Finder für die Kommandozeile

fzf ist ein interaktiver **Fuzzy-Finder**, der die Leistungsfähigkeit der inkrementellen Suche auf jede Liste anwendet, die in der Kommandozeile dargestellt wird. Ursprünglich in Ruby geschrieben und später in Go neu geschrieben von [Junegunn Choi](https://github.com/junegunn), ist es zu einem unverzichtbaren Werkzeug für Entwickler, Systemadministratoren und Power-User geworden, die Dateien, Befehle, Prozesse und mehr blitzschnell durchsuchen und auswählen möchten.

Anstatt exakte Namen zu tippen oder sich auf die Tab-Vervollständigung zu verlassen, können Sie mit fzf einen beliebigen Teilstring (oder sogar eine unscharfe Sequenz) eingeben, und es filtert sofort die Eingabe. Es funktioniert mit allen Daten, die über stdin gestreamt werden, und gibt das ausgewählte Element auf stdout aus, was es perfekt für Unix-Pipelines macht.

---

## Warum fzf verwenden?

- **Geschwindigkeit**: Verarbeitet Hunderttausende von Einträgen nahezu in Echtzeit.
- **Unscharfe Suche (Fuzzy Matching)**: Finden Sie Dateien und Befehle, ohne sich an genaue Namen erinnern zu müssen.
- **Interaktivität**: Live-Filterung mit sofortigem visuellem Feedback.
- **Kombinierbarkeit**: Funktioniert mit jedem Befehl, der Text erzeugt oder verbraucht.
- **Anpassbarkeit**: Designs, Tastenkombinationen, Vorschaufenster und mehr.

---

## Installation

### macOS
```bash
brew install fzf
# Install useful key bindings and fuzzy auto-completion
$(brew --prefix)/opt/fzf/install
```

### Linux (Debian/Ubuntu)
```bash
sudo apt install fzf           # Often outdated – prefer building from source
# Or from the official repository:
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

### Arch Linux
```bash
sudo pacman -S fzf
```

### Windows (WSL / Git Bash / Scoop)
```bash
scoop install fzf
# Or with Chocolatey
choco install fzf
```

### Go (any platform)
```bash
go install github.com/junegunn/fzf@latest
```

---

## Grundlegende Verwendung

### Eine Liste an fzf übergeben
```bash
# Search through all files in the current directory
find . -type f | fzf
```

### Eine Datei auswählen und in einem Editor öffnen
```bash
vim "$(find . -type f | fzf)"
```

### Dateiinhalte in der Vorschau anzeigen
```bash
fzf --preview 'cat {}'       # {} is the path of the current item
```

### Umgekehrtes Layout (Suche unten)
```bash
fzf --reverse
```

### Mehrfachauswahl (mit Tab)
```bash
fzf --multi
```

### Benutzerdefinierte Eingabeaufforderung
```bash
fzf --prompt="Pick a file> "
```

---

## Hauptmerkmale

### Fuzzy-Suchmodi
fzf unterstützt mehrere Suchmodi, um Ihre Suche zu verfeinern:

- **Fuzzy (Standard)**: `abc` passt auf `alphabet.txt` – jede beliebige Teilzeichenfolge funktioniert.
- **Exakte Übereinstimmung**: vorangestelltes `'` → `'abc` entspricht nur Zeilen, die genau „abc" enthalten.
- **Präfix-Übereinstimmung**: nachgestelltes `^` → `^abc` entspricht Zeilen, die mit „abc" beginnen.
- **Suffix-Übereinstimmung**: vorangestelltes `$` → `abc$` entspricht Zeilen, die mit „abc" enden.
- **Regulärer Ausdruck**: `!` vorangestellt für Negation, oder Integration von `rg`.

### Vorschaufenster
Das Vorschaufenster zeigt kontextbezogene Informationen für das hervorgehobene Element an. Es kann externe Befehle wie `cat`, `bat`, `head` oder sogar benutzerdefinierte Skripte verwenden:

```bash
fzf --preview 'bat --color=always --style=numbers {}'
```

### Shell-Integration
Das offizielle `install`-Skript richtet drei praktische Tastenkombinationen ein (Bash, Zsh, Fish):

| Shortcut | Aktion |
|----------|--------|
| `Ctrl+R` | Befehlshistorie durchsuchen |
| `Ctrl+T` | Dateien/Verzeichnisse durchsuchen und ihre Pfade einfügen |
| `Alt+C`  | In ein Unterverzeichnis springen (fuzzy cd) |

### Vim / Neovim-Plugin
fzf bietet ein natives Vim-Plugin. Die beliebteste Erweiterung ist [fzf.vim](https://github.com/junegunn/fzf.vim), die Befehle wie die folgenden hinzufügt:

| Befehl | Zweck |
|--------|-------|
| `:Files [path]` | Dateien durchsuchen |
| `:Rg [pattern]` | Dateiinhalte durchsuchen (benötigt ripgrep) |
| `:Buffers` | Zwischen geöffneten Puffern wechseln |
| `:GFiles?` | Unversionierte Dateien in einem Git-Repository durchsuchen |
| `:Commands` | Vim-Befehle auflisten |
| `:Maps` | Tastenzuordnungen anzeigen |

### Erweiterbarkeit
Da fzf auf stdin/stdout arbeitet, lässt es sich nahtlos in jeden Workflow integrieren. Sie können es in Shell-Funktionen oder Skripte einbetten, um Ihre eigenen interaktiven Menüs zu erstellen.

---

## Fortgeschrittene Anwendungsfälle

### Prozess-Killer
```bash
ps aux | fzf | awk '{print $2}' | xargs kill -9
```

### Ein Git-Branch auschecken
```bash
git branch -a | fzf | tr -d ' *' | xargs git checkout
```

### Per SSH in Hosts aus der Konfiguration einloggen
```bash
cat ~/.ssh/config | grep -i '^host ' | awk '{print $2}' | fzf | xargs ssh
```

### Dateiinhalte mit Vorschau durchsuchen
```bash
rg --line-number . | fzf --delimiter : \
    --preview 'bat --color=always --highlight-line {2} {1}'
```

### Interaktiv das Verzeichnis wechseln (mit fd)
```bash
cd "$(fd --type d | fzf)"
```

### Docker-Container suchen
```bash
docker ps | fzf | awk '{print $NF}'
```

---

## Tipps und Tricks

- **Verwenden Sie die Option `--header`**, um Anweisungen anzuzeigen:
  ```bash
  fzf --header "Press Ctrl-R for history, Ctrl-T for files"
  ```
- **Ausgewählte Elemente in einer Variable speichern** für Batch-Operationen.
- **Eine farbige Vorschau hinzufügen** durch Verwendung von `bat` oder `highlight` mit ANSI-Unterstützung.
- **Mit `tmux` kombinieren**, um das Vorschaufenster in einem separaten Split zu öffnen.
- **Passen Sie das Farbschema über die Umgebungsvariable `FZF_DEFAULT_OPTS` an**:
  ```bash
  export FZF_DEFAULT_OPTS='--color=bg+:#383838,fg+:#f0f0f0'
  ```

---

## Fazit

fzf ist ein Goldstandard-Werkzeug für die interaktive Terminalsuche. Seine unscharfe Suche, Geschwindigkeit und Kombinierbarkeit machen es unverzichtbar für jeden, der in der Kommandozeile lebt. Ob Sie Dateien durchstöbern, Prozesse jagen oder benutzerdefinierte Workflows erstellen – fzf verwandelt mühsame Suchaufgaben in ein flüssiges, fast magisches Erlebnis.

Eine vollständige Dokumentation finden Sie im [GitHub-Repository](https://github.com/junegunn/fzf).