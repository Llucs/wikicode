---
title: Leitfäden
description: Ausführliche, themenorientierte Anleitungen.
created: 2026-06-03
tags:
  - meta
status: stable
---

# Leitfäden

Ausführliche Leitfäden, gruppiert nach Thema. Jeder Leitfaden ist eine echte
Markdown-Datei unter `docs/guides/` (oder einem Unterordner).

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Erstellt: 2026-06-03</span>
<span class="wikicode-meta-updated">Zuletzt aktualisiert: automatisch (git)</span>
</div>

## Konventionen

- Ein Ordner oder eine `.md`-Datei pro Leitfaden.
- Ordnername: Kleinbuchstaben, mit Bindestrich.
- Das Frontmatter sollte `title`, `description`, `created` und `tags` enthalten.
- Tags helfen beim Querverweisen: Bevorzuge die Wiederverwendung vorhandener
  Tags aus [Tags](../tags.md) gegenüber dem Erfinden neuer Tags.

## Empfohlene Tags

| Tag             | Bedeutung                                                  |
| --------------- | ---------------------------------------------------------- |
| `meta`          | Seiten über WikiCode selbst.                               |
| `guide`         | How-to-Inhalte.                                            |
| `reference`     | Referenzmaterial (Glossare, Listen).                        |
| `architecture`  | Wie das Wiki aufgebaut ist und funktioniert.                |
| `process`       | Workflow, Beiträge, Governance.                            |
| `language-go`   | Inhalte hauptsächlich über Go.                              |
| `language-py`   | Inhalte hauptsächlich über Python.                          |
| `language-cpp`  | Inhalte hauptsächlich über C++.                             |
| `language-rs`   | Inhalte hauptsächlich über Rust.                            |
| `language-js`   | Inhalte hauptsächlich über JavaScript / TypeScript.         |
| `backend`       | Backend-Engineering-Themen.                                |
| `frontend`      | Frontend-Engineering-Themen.                               |
| `devops`        | Build, Deployment, Observability.                          |
| `security`      | Sicherheitsthemen.                                         |
| `data`          | Datenbanken, Pipelines, Analytik.                          |

Füge Tags wie folgt zum Frontmatter hinzu:

```yaml
---
title: My guide
tags:
  - guide
  - backend
---
```