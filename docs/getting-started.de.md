---
title: Erste Schritte
description: Repository-Layout, lokaler Build und Beitragskonventionen.
created: 2026-06-03
---

# Erste Schritte

Alles, was du lesen, erstellen und zu WikiCode beitragen musst.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Erstellt: 2026-06-03</span>
<span class="wikicode-meta-updated">Zuletzt aktualisiert: auto (git)</span>
</div>

## 1. Repository-Layout

```
.
├── README.md            # Project overview
├── LICENSE              # MIT License
├── AGENT.md             # Operating contract for agents
├── mkdocs.yml           # Static site configuration
├── .gitignore
├── .github/
│   └── workflows/
│       ├── pages.yml    # Builds and deploys the site on push to main
│       └── wikicode-agent.yml# Autonomous agent workflow
├── docs/                # Site content (articles, guides)
│   ├── assets/css/      # Custom styling
│   ├── index.md
│   └── getting-started.md
├── projects/            # Self-contained developer projects
├── snippets/            # Reusable code snippets
├── memory/              # Long-term agent memory
│   ├── mission.md
│   ├── rules.md
│   ├── knowledge.md
│   └── decisions.md
├── tasks/               # Work pipeline
│   ├── queue.md
│   └── completed.md
└── reports/             # Time-stamped execution reports
```

## 2. Der "Wiki wächst aus dem Repo"-Kreislauf

WikiCode ist eine **repository-first**-Site. Nichts in `site/` (der veröffentlichte Output) wird von Hand bearbeitet.

1. Eine Änderung wird am Repository vorgenommen (ein neuer Artikel, ein neues Projekt, Snippet, Bericht, Entscheidung usw.).
2. Die Änderung wird committed und nach `main` gepusht.
3. `.github/workflows/pages.yml` wird automatisch beim Push ausgeführt.
4. MkDocs liest `docs/`, `projects/`, `snippets/` und erstellt die gesamte Site neu.
5. GitHub Pages stellt den neuen Build bereit.

Der lokale KI-Agent (oder jeder Mitwirkende) steigt in diesen Kreislauf ein, indem er in das Repository schreibt. Die Site übernimmt die Änderung dann ohne manuellen Eingriff.

## 3. Die Site lokal ausführen

Du benötigst Python 3.10+.

```bash
pip install mkdocs mkdocs-material \
            mkdocs-awesome-pages-plugin \
            mkdocs-git-revision-date-localized-plugin
mkdocs serve
```

Die Site ist unter `http://127.0.0.1:8000` verfügbar. Änderungen an einer Markdown-Datei in `docs/`, `projects/` oder `snippets/` lösen sofortiges Neuladen aus.

## 4. Die statische Site erstellen

```bash
mkdocs build --clean
```

Die Ausgabe wird in `site/` geschrieben. Die CI verwendet denselben Befehl.

## 5. Inhalte hinzufügen

| Du möchtest hinzufügen… | Lege es ab in…                              | Erforderliche Dateien                      |
| ------------------------ | -------------------------------------------- | ----------------------------------------- |
| Einen Artikel            | `docs/<topic>/<slug>.md` oder `docs/`        | die `.md`-Datei selbst                    |
| Ein Projekt              | `projects/<slug>/`                           | `README.md` + `index.md` + Quellcode     |
| Ein Snippet              | `snippets/<slug>/`                           | die Codedatei + `index.md`                |
| Eine Entscheidung        | `memory/decisions.md`                        | füge einen neuen Eintrag hinzu            |
| Eine Aufgabe             | `tasks/queue.md`                             | füge einen neuen Kontrollkästchen-Eintrag hinzu |
| Einen Bericht            | `reports/YYYY-MM-DD-<slug>.md`               | die Datei + Index-Aktualisierung          |

Abschnitte, die nicht Teil von `docs/` sind (Projekte, Snippets), werden automatisch vom MkDocs-Plugin `awesome-pages` über ihre `index.md`-Dateien erfasst.

## 6. Frontmatter

Jede Seite der Site hat mindestens:

```yaml
---
title: Page title
description: Short description.
created: YYYY-MM-DD
---
```

Das `created`-Datum wird gesetzt, wenn die Seite zum ersten Mal hinzugefügt wird. Das **Zuletzt aktualisiert**-Datum wird automatisch aus der Git-Historie der Datei übernommen, sodass es ohne manuelle Bearbeitung immer korrekt ist.

## 7. Autonomes Arbeiten

Agenten müssen `AGENT.md` befolgen. Die Kurzfassung:

1. Lese `memory/mission.md` und `memory/rules.md`.
2. Wähle die nächste Aufgabe aus `tasks/queue.md`.
3. Nimm genau eine sinnvolle Änderung am Repository vor.
4. Schreibe einen Bericht in `reports/`.
5. Verschiebe die Aufgabe nach `tasks/completed.md`.
6. Committe und pushe. Die Site wird automatisch neu erstellt.

## 8. Suche

WikiCode ist vollständig durchsuchbar. Der Suchindex wird zur Bereitstellungszeit erstellt und läuft vollständig im Browser.

- Drücke ++slash++ auf jeder Seite, um die Suchleiste zu fokussieren.
- Der Index deckt jede Seite der Site ab, einschließlich Codeblöcke und Blogbeiträge.
- Siehe [Suche](search.md) für vollständige Details und Tipps.

## 9. Wie der Agent ausgelöst wird

Der Workflow `wikicode-agent` unterstützt **sowohl automatische als auch manuelle** Auslöser:

| Auslöser             | Wann                                                  | Anwendungsfall                           |
| -------------------- | ----------------------------------------------------- | ---------------------------------------- |
| `schedule`           | Täglich um 12:00 UTC.                                 | Standard "jeden Tag ein bisschen wachsen"-Lauf. |
| `workflow_dispatch`  | Manuell über den Actions-Tab.                         | Bedarfsgesteuerter Lauf, nützlich zum Entblocken. |
| `issue_comment`      | Wenn jemand `@agent` in einem Issue schreibt.         | Ein Issue in einen Beitrag verwandeln.   |
| `issues` with label  | Wenn ein Issue mit `agent` gekennzeichnet ist.        | Vom Betreiber kuratierte Batch-Läufe.    |

Pro Lauf wird nur **eine** Aufgabe ausgeführt. Die KI verwendet die OpenCode API zur Inhaltsgenerierung — es werden keine externen API-Schlüssel benötigt.

## 10. Konventionen

- Markdown-Dateinamen: Kleinbuchstaben, Bindestriche.
- Jeder Projekt-, Snippet- und Tool-Ordner stellt ein `index.md` für die Navigation bereit.
- Entscheidungen über Architektur, Tools oder Workflow werden in `memory/decisions.md` festgehalten.
- Es werden niemals Anmeldeinformationen, Token oder private Daten committet.
- Der lokale KI-Agent verwendet `secrets.GITHUB_TOKEN` (integriert) zum Committen und Pushen. Es werden keine externen API-Schlüssel benötigt.