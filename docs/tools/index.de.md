---
title: Werkzeuge
description: Entwicklerwerkzeuge dokumentiert in WikiCode.
created: 2026-06-03
tags:
  - meta
  - tools
status: stable
---

# Werkzeuge

Entwicklerwerkzeuge dokumentiert in WikiCode. Jedes Werkzeug hat seinen eigenen Ordner unter `docs/tools/<slug>/` mit einer `index.md` Zusammenfassung.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Erstellt: 2026-06-03</span>
<span class="wikicode-meta-updated">Zuletzt aktualisiert: auto (git)</span>
</div>

## Nach Ökosystem

Werkzeuge werden nach Ökosystem klassifiziert. Siehe den Tag‑Index für die vollständige Liste.

| Ökosystem   | Werkzeuge                    |
|-------------|------------------------------|
| Container   | Docker, Podman, Portainer    |
| CI/CD       | Jenkins, ArgoCD              |
| API         | Postman, cURL                |
| JavaScript  | npm, Jest                    |
| Editor      | Visual Studio Code           |
| CLI         | fzf                          |
| Android     | SpeedCool                    |
| Monitoring  | Grafana, Heimdall            |
| VCS         | Git                          |

## Wie Werkzeuge hinzugefügt werden

Sowohl der KI‑Agent als auch menschliche Mitwirkende folgen dem gleichen Rezept:

1. Recherchiere das Werkzeug mithilfe der Websuche (Wikipedia + DuckDuckGo).
2. Schreibe eine `docs/tools/<slug>/index.md` Zusammenfassung.
3. Füge Frontmatter mit `title`, `description`, `created`, `tags` und `ecosystem` hinzu.
4. Führe `mkdocs build --clean` zur Validierung aus.

## Aktuelle Werkzeuge

<!--awesome-pages:hide-->
<!--awesome-pages:reveal-->

## Konventionen

- Ein Ordner pro Werkzeug. Ordnername: Kleinbuchstaben, mit Bindestrich.
- `index.md` ist die öffentliche Zusammenfassung.
- Frontmatter muss `title`, `description`, `created`, `tags`, `ecosystem` und `status` enthalten.
- Eine Werkzeugseite sollte enthalten: einen Absatz „Was es ist“, Installation, grundlegende Verwendung und wichtigste Funktionen mit Beispielen.