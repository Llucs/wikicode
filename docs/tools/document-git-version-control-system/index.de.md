---
title: Git - Versionskontrollsystem
description: Git ist ein verteiltes Versionskontrollsystem, das Änderungen im Quellcode während Softwareentwicklungsprojekten verfolgt.
created: 2026-06-13
tags:
  - Source_Control
  - Versioning
status: draft
ecosystem: vcs
---

Git ist ein leistungsstarkes und weit verbreitetes verteiltes Versionskontrollsystem (VCS), das entwickelt wurde, um alles von kleinen bis zu sehr großen Projekten mit Geschwindigkeit und Effizienz zu bewältigen. Es wurde 2005 von Linus Torvalds für das Linux-Kernel-Entwicklungsteam entwickelt, hat sich aber seitdem zu einem Industriestandardwerkzeug für die Verwaltung von Änderungen an Softwarecode entwickelt.

### Was ist Git?

Git ist ein Versionskontrollsystem, das es Entwicklern ermöglicht, Änderungen an Dateien im Laufe der Zeit zu verfolgen, mit anderen an Projekten zusammenzuarbeiten und bei Bedarf zu früheren Versionen zurückzukehren. Es verwendet ein "verteiltes" Modell, bei dem jeder Entwickler seine eigene Kopie des Repositorys hat, von/zu dem er Änderungen mit anderen Repositorys austauschen kann.

### Warum Git verwenden?

1. **Geschwindigkeit**: Git ist auf Geschwindigkeit und Effizienz optimiert und eignet sich daher für große Projekte.
2. **Flexibilität**: Dank seiner verteilten Natur können Entwickler unabhängig arbeiten und dabei eine gemeinsame Historie der Projektentwicklung bewahren.
3. **Funktionsreich**: Git unterstützt komplexe Arbeitsabläufe wie Branching und Merging sowie erweiterte Funktionen wie Submodule und Hooks.

### Git installieren

Um Git auf Ihrem System zu installieren:

- **Windows**: Laden Sie das Installationsprogramm von der offiziellen Git-Website herunter und folgen Sie den Installationsanweisungen.
- **macOS**: Verwenden Sie Homebrew, um Git mit `brew install git` zu installieren.
- **Linux**: Die meisten Linux-Distributionen haben Git in ihren Paketverwaltern. Auf Ubuntu können Sie zum Beispiel `sudo apt-get install git` verwenden.

### Grundlegende Verwendung

Hier sind einige grundlegende Befehle für den Einstieg:

```sh
# Initialize a new repository (create .git directory)
git init

# Add files to staging area
git add filename.txt

# Commit changes with message
git commit -m "Initial commit"

# View the list of untracked files
git status

# Create a new branch and switch to it
git checkout -b feature-branch

# Merge changes from another branch into your current branch
git merge other-branch

# Push local commits to remote repository (e.g., GitHub)
git push origin main
```

### Hauptfunktionen

Git bietet mehrere Funktionen, die es zu einem unverzichtbaren Werkzeug für die Softwareentwicklung machen:

1. **Branching und Merging**: Erstellen Sie einfach Branches, arbeiten Sie unabhängig daran und führen Sie die Änderungen später wieder in den ursprünglichen Branch zusammen.
2. **Submodule**: Ermöglichen es Ihnen, andere Git-Repositorys als Teil der Abhängigkeiten Ihres Projekts einzubinden.
3. **Hooks**: Benutzerdefinierte Skripte, die an verschiedenen Stellen während Git-Operationen ausgeführt werden (z. B. Pre-Commit-Hooks).
4. **Reflog**: Stellt eine Aufzeichnung aller im Repository ausgeführten Befehle bereit, nützlich für die Fehlersuche.

### Fazit

Git ist ein robustes und flexibles Versionskontrollsystem, das für viele Softwareentwicklungsteams unverzichtbar geworden ist. Seine leistungsstarken Funktionen, gepaart mit seiner Effizienz und Flexibilität, machen es zu einer ausgezeichneten Wahl für die Verwaltung von Quellcodeänderungen in Projekten.

Für detailliertere Informationen zur Git-Nutzung und Best Practices finden Sie in der offiziellen Git-Dokumentation oder in Online-Ressourcen.