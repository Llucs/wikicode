---
title: Architektur
description: Wie WikiCode aufgebaut ist und wie es aktuell bleibt.
created: 2026-06-03
tags:
  - reference
  - architecture
  - meta
status: stable
---

# Architektur

Wie WikiCode aufgebaut ist, wie es aktuell bleibt und wie autonome
Agenten in den Ablauf integriert sind.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Erstellt: 2026-06-03</span>
<span class="wikicode-meta-updated">Zuletzt aktualisiert: automatisch (git)</span>
</div>

## Übersichtsdiagramm

```
┌──────────────────────────────────────────────────────────────┐
│                       Repository                             │
│                                                              │
│   docs/        projects/    snippets/                        │
│   memory/      tasks/       reports/                         │
│   blog/        scripts/     mkdocs.yml                       │
│                                                              │
└─────────────┬──────────────────────────────┬────────────────┘
              │                              │
              │  push to main                │  Agent run
              │                              │  (manual, schedule,
              │                              │   @agent, label)
              ▼                              ▼
      ┌──────────────────┐         ┌──────────────────────┐
      │  pages.yml       │         │  wikicode-agent.yml  │
      │  ─ mkdocs build  │         │  ─ install deps      │
      │  ─ upload Pages  │         │  ─ read context      │
      │    artifact      │         │  ─ web research*     │
      └────────┬─────────┘         │  ─ generate content  │
               │                  │  ─ validate build    │
               │                  │  ─ commit & push     │
               ▼                  └──────────┬───────────┘
       GitHub Pages                          │
       (public site)                         │
                                             │
       new commit on main  ◄─────────────────┘
```

`*` Der Agent verwendet die Wikipedia- und DuckDuckGo-APIs für die
Web-Recherche, es sind keine API-Schlüssel erforderlich.

## Schichten

### 1. Inhalt

Reines Markdown. Zum Verfassen ist keine spezielle Werkzeugunterstützung
erforderlich.

| Pfad             | Zweck                                                             |
| ---------------- | ----------------------------------------------------------------- |
| `docs/`          | Artikel, Anleitungen, Referenz – die Inhalte, die du auf der Seite liest. |
| `docs/concepts/` | Architekturmuster, Designprinzipien, technische Konzepte.         |
| `docs/guides/`   | Langformatige, themenorientierte Leitfäden.                       |
| `docs/tools/`    | Ein Ordner pro dokumentiertem Entwicklerwerkzeug.                  |
| `docs/analyses/` | Technische Analysen und Architekturstudien von Plattformen/Bibliotheken. |
| `docs/reference/`| Glossar, Architektur, Changelog.                                  |
| `docs/topics/`   | Themenindex.                                                      |
| `projects/`      | Echte, ausführbare Projekte. Jedes ist eine in sich geschlossene Einheit. |
| `snippets/`      | Kleine, fokussierte, ausführbare Code-Ausschnitte.                |
| `blog/`          | Längere Artikel, Ankündigungen, Post-Mortems.                     |
| `memory/`        | Langzeitkontext für Agenten (Mission, Regeln, Entscheidungen).    |
| `tasks/`         | Arbeitspipeline (Warteschlange + erledigt).                       |
| `reports/`       | Zeitgestempelte Ausführungsberichte, organisiert nach Jahr/Monat. |

### 2. Generierung

- **MkDocs** mit dem **Material**-Theme wandelt den Markdown-Baum in
  eine statische Website um.
- Plugins:
  - `search` — clientseitige Volltextsuche.
  - `awesome-pages` — automatische Abschnittsindizes.
  - `git-revision-date-localized` — Datum der letzten Aktualisierung
    aus Git.
  - `blog` — Material’s integrierte Blog-Unterstützung.
  - `git-committers` — optional, gesteuert durch Umgebungsvariable.

### 3. Bereitstellung

- `pages.yml` wird bei jedem Push auf `main` ausgeführt. Es erstellt
  die Website und stellt sie mit den offiziellen Pages-Aktionen
  (`actions/upload-pages-artifact` + `actions/deploy-pages`) auf
  **GitHub Pages** bereit.
- Pages ist mit `build_type: workflow` konfiguriert und HTTPS wird
  erzwungen.

### 4. Automatisierung

#### Tägliches Wachstum

`wikicode-agent.yml` läuft nach einem **zweimal täglichen Zeitplan**
(`0 6,18 * * *`, 06:00 und 18:00 UTC) und bei manuellen Auslösern.
Jeder Durchlauf ist eine einzelne, abgegrenzte Änderung, sodass das
Wiki jeden Tag ein wenig wächst.

Der erwartete Ablauf pro Durchlauf:

1. Der Workflow startet. Python-Abhängigkeiten werden installiert.
2. `scripts/agent.py` liest `memory/` für Kontext. Wenn die
   Aufgabenwarteschlange leer ist, entdeckt es proaktiv neue Werkzeuge
   und Projekte zur Dokumentation. Anschließend recherchiert es das
   ausgewählte Thema über Wikipedia- und DuckDuckGo-APIs.
3. Die OpenCode API generiert den Inhalt (Markdown mit Frontmatter).
4. Der Agent schreibt die Dateien, führt `mkdocs build --clean` zur
   Validierung aus, committet und pusht dann.
5. `pages.yml` erstellt die Website neu und stellt sie bereit.
6. Die Ausführung des nächsten Durchlaufs sieht ein etwas größeres
   Wiki und setzt fort.

#### Auslöser

| Auslöser                | Anwendungsfall                                           |
| ----------------------- | -------------------------------------------------------- |
| `schedule`              | Der standardmäßige Wachstumsdurchlauf (06:00 und 18:00 UTC). |
| `workflow_dispatch`     | Manueller Durchlauf aus dem Actions-Tab.                 |
| `issue_comment`         | `@agent`-Erwähnung in einem Issue- oder PR-Kommentar.    |
| `issues` mit Label      | Issues mit dem Label `agent`.                            |

#### Nebenläufigkeit

`concurrency: wikicode-agent` ist mit `cancel-in-progress: true`
gesetzt, sodass sich überschneidende Durchläufe das Repository nicht
doppelt beschreiben.

### 5. Anti-Duplizierung

WikiCode möchte nicht dieselbe Sache zweimal dokumentieren. Der
Anti-Duplizierungsmechanismus besteht aus drei Teilen:

1. **Abschnittsindex-Seiten.** Jeder Abschnitt hat eine `index.md`,
   die seine aktuellen Inhalte auflistet. Das `awesome-pages`-Plugin
   entdeckt die Liste automatisch aus dem Dateisystem, sodass sie
   immer aktuell ist.
2. **`git grep`-Rückfall.** Das Agentenskript durchsucht
   Abschnittsindizes und die Aufgabenliste und verwendet dann
   `git grep`, um zu bestätigen, dass ein Thema neu ist, bevor es
   Inhalt generiert.
3. **Wissensverzeichnis.** `memory/knowledge.md` listet die
   wichtigsten Inhalte und die Regeln zum Hinzufügen neuer auf.

Wenn ein Duplikat erkannt wird, muss der Agent die vorhandene Seite
verbessern, anstatt eine neue zu schreiben (Regel 16 in
`memory/rules.md`).

### 6. Web-Recherche

Der Agent verwendet Wikipedia- und DuckDuckGo-APIs, um Informationen
zu jedem Thema zu sammeln, das er dokumentieren muss. Dies ist der
Mechanismus, der sicherstellt, dass der generierte Inhalt sachlich und
aktuell bleibt:

1. `research_topic()` in `scripts/agent.py` führt sowohl eine
   Wikipedia-Suche als auch eine DuckDuckGo-Instant-Answer-Abfrage
   für das Thema durch.
2. Wikipedia gibt Artikeltitel + einleitende Auszüge (Klartext, bis
   zu 2000 Zeichen) zurück.
3. DuckDuckGo gibt die Zusammenfassung und verwandte Themen zurück.
4. Wenn beide leer zurückkommen, greift der Agent auf das
   Trainingswissen des LLM zurück.
5. Der gesammelte Recherchetext wird in den
   Content-Generierungs-Prompt eingefügt, sodass das LLM auf Basis
   realer Informationen schreibt.

## Inhalts-Taxonomie v2

Jedes Dokument in WikiCode gehört genau zu einer dieser Kategorien:

| Kategorie     | Pfad                 | Was dort hingehört                                        |
| ------------- | -------------------- | --------------------------------------------------------- |
| **Konzept**   | `docs/concepts/<slug>/` | Architekturmuster, Designprinzip oder technisches Konzept. |
| **Werkzeug**  | `docs/tools/<slug>/`  | Entwicklerwerkzeug-Dokumentation (Installation, Verwendung, Funktionen). |
| **Analyse**   | `docs/analyses/<slug>/` | Architekturstudie einer Plattform, eines Frameworks oder einer Bibliothek. |
| **Projekt**   | `projects/<slug>/`    | Echtes, ausführbares Open-Source-Projekt mit Einrichtungsanleitung. |
| **Leitfaden** | `docs/guides/`        | Langformatiges, themenorientiertes Tutorial oder Anleitung. |
| **Bericht**   | `reports/YYYY/MM/`    | Zeitgestempelter Ausführungsbericht, nach Commit unveränderbar. |
| **Gedächtnis**| `memory/`             | Agentenkontext: Mission, Regeln, Entscheidungen, Wissen, Zustand, Qualität. |

Die Trennung ist semantisch, nicht kosmetisch:

- **Konzepte vs. Leitfäden** — eine Konzeptseite erklärt ein Muster,
  Prinzip oder eine Technik (z. B. Microservices, CQRS, OAuth).
  Ein Leitfaden ist eine erzählerische Durchführung, die mehrere
  Konzepte oder Werkzeuge umfassen kann.
- **Werkzeuge vs. Analysen** — eine Werkzeugseite lehrt, *wie man
  etwas verwendet* (Installation → Konfiguration → Ausführung).
  Eine Analyse untersucht *Architektur und Kompromisse* (Alternativen
  vergleichen, Designentscheidungen bewerten).
- **Leitfäden vs. Werkzeuge** — ein Leitfaden ist eine erzählerische
  Durchführung über mehrere Werkzeuge oder Konzepte hinweg. Eine
  Werkzeugseite ist eine einzelne Referenzkarte.
- **Berichte als Aufzeichnungen** — Berichte sind nach dem Commit
  unveränderbar. Sie sind nach `YYYY/MM/` organisiert, um eine
  Aufblähung des flachen Verzeichnisses zu verhindern und
  chronologisches Durchsuchen zu ermöglichen.
- **Gedächtnis als Agentenvertrag** — jede Datei in `memory/` hat
  eine bestimmte Rolle (deklariert in `memory/knowledge.md`). Der
  Agent liest alle beim Start; `state.md` wird auch nach jedem
  Durchlauf geschrieben.

## Frontmatter-Vertrag

Jede Seite auf der Website sollte Folgendes haben:

```yaml
---
title: Human-readable title
description: One-sentence summary.
created: YYYY-MM-DD
tags: [tag1, tag2]
status: draft | stable | archived | deprecated
---
```

`title` und `description` werden in der Navigation und Suche
verwendet. `created` speist die Metadatenkarte;
`git-revision-date-localized` füllt das Datum "zuletzt aktualisiert"
automatisch. `tags` ermöglicht das tag-basierte Durchsuchen. `status`
signalisiert den Reifegrad der Seite.

## Geheimnisse und Sicherheit

| Geheimnis           | Zweck                                              | Quelle                |
| ------------------- | -------------------------------------------------- | --------------------- |
| `GITHUB_TOKEN`      | Repository-Zugriff innerhalb von Workflows.        | Integriert.           |

Es werden keine Anmeldeinformationen im Repository gespeichert.

## Wie die Architektur weiterentwickelt wird

Jede Änderung, die sich darauf auswirkt, wie die Website erstellt,
bereitgestellt oder automatisiert wird, sollte:

1. Als neuer Eintrag in `memory/decisions.md` mit der nächsten
   verfügbaren Nummer aufgezeichnet werden.
2. In dieser Seite widergespiegelt werden, wenn sie das
   Übersichtsdiagramm ändert.
3. Den Repository-First-Vertrag einhalten: niemals die
   veröffentlichte Website direkt bearbeiten.