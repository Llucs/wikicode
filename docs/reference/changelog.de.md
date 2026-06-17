---
title: Änderungsprotokoll
description: Bemerkenswerte Änderungen an WikiCode.
created: 2026-06-03
tags:
  - reference
  - meta
status: stable
---

# Änderungsprotokoll

Bemerkenswerte Änderungen an WikiCode. Kleinere, alltägliche Bearbeitungen werden in der Git-Historie verfolgt; hier erscheinen nur strukturelle und für Benutzer sichtbare Änderungen.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Erstellt: 2026-06-03</span>
<span class="wikicode-meta-updated">Zuletzt aktualisiert: automatisch (git)</span>
</div>

## 1.0.0 — 2026-06-03 — Bootstrap

Anfängliche, produktionsorientierte Struktur.

### Hinzugefügt

- **Seitengenerierung.** MkDocs (Material Theme) mit client-seitiger Suche, automatischen Abschnittsindizes und einer sauberen, benutzerdefinierten CSS-Ebene.
- **Repository-zentrierte Veröffentlichung.** Die Seite wird bei jedem Push auf `main` aus dem Repository über `.github/workflows/pages.yml` neu generiert. Nichts auf der veröffentlichten Seite wird manuell bearbeitet.
- **KI-Agent (OpenCode API).** `.github/workflows/wikicode-agent.yml` führt den autonomen Agenten auf dem CI-Runner aus. Inhaltsgenerierung über die OpenCode API (`deepseek-v4-flash-free`), Web-Recherche über Wikipedia- und DuckDuckGo-APIs. Keine externen API-Schlüssel erforderlich.
- **GitHub Pages.** Aktiviert mit dem Workflow-Build-Typ und HTTPS erzwungen.
- **Inhaltsabschnitte.**
  - `docs/` für Artikel, Anleitungen und Referenzseiten.
  - `projects/` für eigenständige, ausführbare Projekte.
  - `snippets/` für fokussierte Code-Ausschnitte.
  - `blog/` für längere Beiträge und Ankündigungen.
  - `memory/` für langfristigen Agentenkontext (Mission, Regeln, Wissen, Entscheidungen).
  - `tasks/` für die Arbeitspipeline.
  - `reports/` für zeitgestempelte Ausführungsberichte.
- **Datumsmetadaten.** Jede Seite zeigt eine Karte mit ihrem **Erstellungsdatum** (aus dem Frontmatter) und **Änderungsdatum** (aus der Git-Historie, über `mkdocs-git-revision-date-localized-plugin`).
- **Tag-System.** Seiten können Tags im Frontmatter deklarieren; das Material Theme rendert automatisch Indexseiten pro Tag.
- **Übergeordnete Anleitungen.**
  - [Glossar](glossary.md)
  - [Architektur](architecture.md)
  - [Änderungsprotokoll](changelog.md) (diese Seite)
  - [Lernpfade](../learning-paths.md)
- **Root-Dateien.** `README.md`, `LICENSE`, `AGENT.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `ARCHITECTURE.md`, `.gitignore`.
- **Erste Entscheidungen.** Vier nummerierte Einträge in `memory/decisions.md` (0001–0004).
- **Erste Aufgaben.** Vier anstehende Einträge in `tasks/queue.md`.

### Anmerkungen

- Die Seite ist unter der von GitHub Pages bereitgestellten URL live, sobald der erste `pages.yml`-Lauf erfolgreich abgeschlossen ist.
- Es sind keine externen API-Schlüssel erforderlich. Der Agent verwendet `GITHUB_TOKEN` (integriert) für den Repository-Zugriff und die OpenCode API für die Inhaltsgenerierung.