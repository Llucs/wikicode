---
title: Lazygit – Die Terminal-Git-UI, die Ihre Produktivität steigert
description: Ein umfassender Leitfaden zu lazygit, einer terminalbasierten Git-UI, die komplexe Git-Operationen wie Staging, Rebasing und Konfliktlösung über eine intuitive, tastaturgesteuerte Oberfläche vereinfacht.
created: 2026-06-20
tags:
  - git
  - tui
  - productivity
  - terminal
status: draft
---

# Lazygit – Die Terminal-Git-UI, die Ihre Produktivität steigert

**Lazygit** ist eine plattformübergreifende, tastaturgesteuerte Terminal-Benutzeroberfläche (TUI) für Git. Erstellt von Jesse Duffield im Jahr 2018 und in Go geschrieben, verpackt es Gits komplexeste – und oft fehleranfällige – Operationen in ein intuitives, panelbasiertes Layout, das vollständig in Ihrem Terminal lebt.

> „Hören Sie auf, Git-Befehle auswendig zu lernen. Nutzen Sie Git intuitiv."

---

## Warum Lazygit?

Gits Befehlszeilenschnittstelle ist leistungsstark, aber bekanntermaßen unverzeihlich. Interaktives Rebasing, Staging von Hunks, Auflösen von Konflikten und Verwalten von Branches erfordern alle präzise Befehlsketten. Lazygit löst dies durch:

- **Visualisierung Ihres Repositorys** – Sie sehen Branches, Tags, den Commit-Graph, den Arbeitsbaum und das Stash auf einen Blick.
- **Beschleunigung der täglichen Arbeit** – Stagen, Commit, Push und Pull ohne Eingabe eines einzigen `git`-Befehls.
- **Reduzierung von Fehlern** – Interaktives Rebasing, Cherry-Picking und Konfliktlösung werden menügeführt und rückgängig machbar.
- **Senkung der Lernkurve** – Neue Teammitglieder können sofort fortgeschrittene Git-Operationen ausführen, ohne sich esoterische Syntax merken zu müssen.
- **Plattformübergreifend arbeiten** – Läuft auf Linux, macOS und Windows mit derselben Oberfläche und denselben Tastenkombinationen.

---

## Installation

Lazygit ist über die meisten Paketmanager verfügbar. Wählen Sie Ihre Plattform:

```bash
# macOS (Homebrew)
brew install lazygit

# Ubuntu / Debian
sudo add-apt-repository ppa:lazygit-team/release
sudo apt update
sudo apt install lazygit

# Arch Linux
pacman -S lazygit

# Windows
winget install lazygit
# or
scoop install lazygit

# Go (requires Go 1.16+)
go install github.com/jesseduffield/lazygit@latest

# Binary downloads (all platforms)
# https://github.com/jesseduffield/lazygit/releases
```

---

## Grundlegende Nutzung

Navigieren Sie in ein beliebiges Git-Repository und starten Sie:

```bash
cd my-project
lazygit
```

Lazygit öffnet sich mit einem geteilten Panel-Layout. Die linke Spalte zeigt (von oben nach unten) die Panels **Status**, **Files**, **Branches**, **Commits** und **Stash**. Die rechte Seite zeigt den Diff oder Log für das ausgewählte Element.

### Panel-Navigation

| Taste | Aktion |
|-------|--------|
| `←` / `→` | Zwischen Panels bewegen |
| `Tab` | Panels vorwärts durchlaufen |
| `Shift + Tab` | Panels rückwärts durchlaufen |
| `j` / `k` | Innerhalb eines Panels nach oben/unten bewegen |
| `J` / `K` | Haupt-Diff-Panel scrollen |
| `?` | Vollständige Tastenkürzelhilfe anzeigen/ausblenden |

### Schnellstart (täglicher Workflow)

1. **Starten** – Führen Sie `lazygit` in einem Repository aus.
2. **Datei stagen** – Drücken Sie `Space` auf einer Datei im Files-Panel.
3. **Einen bestimmten Hunk stagen** – Drücken Sie `Enter`, um den Diff anzusehen, dann `Space` auf einzelnen Hunks.
4. **Committen** – Drücken Sie `c`, geben Sie eine Nachricht ein und drücken Sie `Enter`.
5. **Pushen** – Drücken Sie `P` (Großbuchstabe), um zu pushen.
6. **Pullen** – Drücken Sie `p` (Kleinbuchstabe), um zu pullen.
7. **Beenden** – Drücken Sie `q`, um zu beenden.

---

## Hauptfunktionen (mit Befehlsbeispielen)

### 🎯 Interaktives Staging (Besser als `git add -p`)

Sehen Sie sich den Diff einer Datei an und stagen/entstagen Sie einzelne Zeilen oder Hunks visuell. Schluss mit dem Zählen von Cursorpositionen.

```bash
# Inside the Files panel:
# Enter  → open the file diff
# Space  → stage the selected hunk
# a      → stage all changes
# Enter on a specific hunk → stage individual lines
```

### 🔁 Interaktives Rebasing (Die Killerfunktion)

Ordnen Sie Commits neu an, squashen Sie sie, fixupen Sie, bearbeiten Sie sie oder löschen Sie sie mit einem einzigen Tastendruck.

```bash
# Switch to the Commits panel (press 4):
# i       → start interactive rebase
# s       → squash commit into previous
# f       → fixup (squash, discard message)
# d       → drop commit entirely
# e       → edit commit (pause rebase)
# r       → reword commit message
# Ctrl+j  → move commit down in order
# Ctrl+k  → move commit up in order
```

Nach dem Markieren drücken Sie `Enter`, um zu bestätigen. Lazygit führt das Rebasing aus und zeigt den Fortschritt an. Treten Konflikte auf, springt es zum Konfliktlösungs-Panel.

### ↩️ Rückgängig / Wiederherstellen (Sicherheitsnetz)

Lazygit verfolgt seine eigene interne Aktionshistorie. Einen Fehler während eines Rebasing gemacht oder versehentlich einen Commit gelöscht? Machen Sie es rückgängig.

```bash
# z  → undo last action
# Z (Shift+z)  → redo
```

### 🌳 Branch-Verwaltung

Wechseln, mergen, rebasen, umbenennen und löschen Sie Branches, ohne die UI zu verlassen.

```bash
# Press 3 to enter the Branches panel:
# Space    → checkout selected branch
# n        → create a new branch (optionally from current HEAD)
# m        → merge selected branch into current
# r        → rebase current branch onto selected
# R        → rename branch
# d        → delete branch (with confirmation)
# Ctrl+r   → update remote branch references
```

### 🍒 Cherry-Pick von Commits

Kopieren Sie Commits von einem Branch zu einem anderen, ohne `git log` oder Commit-Hash-Suche.

```bash
# In the Commits panel:
# c        → start cherry-pick mode
# Space    → toggle selection of a commit
# Shift+c  → complete cherry-pick
```

### 🧩 Stash-Verwaltung

Benennen Sie Stashes, wenden Sie sie an, poppen Sie sie und erstellen Sie sogar Branches aus Stashes.

```bash
# Press 5 to enter the Stash panel:
# g        → toggle stash view
# s        → stash staged changes
# Shift+s  → stash all changes (including untracked files)
# Space    → apply selected stash
# d        → drop stash
# n        → name a new stash
# b        → create branch from stash
```

### ⚔️ Konfliktlösung

Wenn ein Rebasing oder Merge Konflikte erzeugt, zeigt Lazygit einen Drei-Wege-Diff mit Inline-Konfliktmarkern an. Lösen Sie sie visuell.

```bash
# Conflict panel will open automatically:
# Ctrl+o → open file in external merge tool
# Space  → stage resolved file
# Enter  → edit file manually
# /      → search for remaining conflict markers
```

### 🌳 Worktree-Unterstützung

Lazygit bietet erstklassige Unterstützung für Git-Worktrees, sodass Sie sie hinzufügen, entfernen und zwischen ihnen wechseln können.

```bash
# In the Branches panel (or dedicated Worktrees panel):
# w        → open worktree management
# a        → add a new worktree
# d        → remove a worktree
# Space    → switch to a worktree
```

### 🧹 Benutzerdefinierte Befehle

Erweitern Sie Lazygit mit Ihren eigenen Shell-Befehlen oder Skripten, die in der UI erscheinen.

```bash
# In ~/.config/lazygit/config.yml:
customCommands:
  - key: "C"
    command: "git cz"
    description: "Commit with Commitizen"
    context: "files"
    loadingText: "Opening commitizen..."
```

---

## Profi-Tipps

1. **Vim-ähnliche Tastenkombinationen** – `j/k` zum Navigieren, `J/K` zum Scrollen von Diffs, `/` zum Suchen innerhalb von Panels.
2. **Dateien filtern** – Geben Sie `/` im Files-Panel ein, um nach Dateinamen zu filtern.
3. **Diff gegen einen bestimmten Commit** – Drücken Sie im Commits-Panel `d` auf einem Commit, um zu sehen, was sich in diesem Commit geändert hat.
4. **Diff-Sichtbarkeit umschalten** – Drücken Sie `Ctrl+d`, um durch die Diff-Anzeigemodi zu wechseln.
5. **Mit Ihrer bestehenden Git-Konfiguration verwenden** – Lazygit berücksichtigt Ihre Aliase, difftool und merge tool Einstellungen.

---

## Konfiguration

Lazygit ist hochgradig konfigurierbar. Eine vollständige Konfigurationsdatei befindet sich unter:

- **Linux/macOS:** `~/.config/lazygit/config.yml`
- **Windows:** `%APPDATA%\lazygit\config.yml`

Generieren Sie eine Vorlage mit:

```bash
lazygit --print-config
```

Häufige Einstellungen umfassen Tastenkombinationsüberschreibungen, Themenfarben, benutzerdefinierte Befehle und UI-Layout.

---

## Wann Sie zu Lazygit greifen sollten

| Szenario | Warum Lazygit hervorsticht |
|----------|----------------------------|
| Interaktives Rebasing | Visuelle Commit-Auswahl und -Neuordnung; Rückgängig verfügbar |
| Staging partieller Änderungen | Zeilenweise Hunk-Auswahl mit sofortigem Diff |
| Onboarding neuer Entwickler | Keine Notwendigkeit, komplexe Git-Befehle auswendig zu lernen |
| Code-Review-Vorbereitung | Erstellen Sie in Minuten saubere, logische Commit-Serien |
| Konfliktlösung | Drei-Wege-Diff-Betrachter mit Inline-Aktion |
| Repository-Übersicht | Siehe Branches, Tags, Remotes, Stash und Commit-Graph auf einen Blick |

---

## Ressourcen

- **GitHub:** [jesseduffield/lazygit](https://github.com/jesseduffield/lazygit)
- **Dokumentation:** [Lazygit Wiki](https://github.com/jesseduffield/lazygit/wiki)
- **Konfigurationsreferenz:** [lazygit Configuration](https://github.com/jesseduffield/lazygit/blob/master/docs/Config.md)
- **Die „lazy"-Produkte des Autors:** Lazygit, Lazydocker, Lazynpm – alle folgen der gleichen TUI-Philosophie.

---

Lazygit ersetzt Git nicht; es macht es zugänglich, visuell und schnell. Egal, ob Sie ein erfahrener Git-Power-User oder ein Entwickler sind, der einfach nur wieder Code schreiben möchte, Lazygit wird Ihnen jede Woche Stunden sparen. Geben Sie ihm einen Tag – Sie werden nie wieder zu einfachem `git rebase -i` zurückkehren wollen.