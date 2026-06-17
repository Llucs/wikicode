---
title: Glossar
description: Terminologie, die in WikiCode verwendet wird.
created: 2026-06-03
tags:
  - reference
  - meta
status: stable
---

# Glossar

Kanonische Terminologie, die in WikiCode verwendet wird. Definitionen
sind kurz und verlinken, wo nützlich, zur maßgeblichen Quelle.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Erstellt: 2026-06-03</span>
<span class="wikicode-meta-updated">Zuletzt aktualisiert: auto (git)</span>
</div>

## Kernkonzepte

<dl markdown>
<dt markdown>**WikiCode**</dt>
<dd markdown>Das Repository und die statische Website, die es erzeugt. «WikiCode»
bezieht sich je nach Kontext auf beides.</dd>

<dt markdown>**Article**</dt>
<dd markdown>Ein langer Markdown-Eintrag unter `docs/`. Artikel sind dazu
gedacht, vollständig gelesen zu werden.</dd>

<dt markdown>**Project**</dt>
<dd markdown>Ein in sich geschlossenes, ausführbares Software-Stück unter
`projects/`. Jedes Projekt hat sein eigenes `README.md`, `index.md` und
einen Quellbaum.</dd>

<dt markdown>**Snippet**</dt>
<dd markdown>Eine kleine, fokussierte, ausführbare Code-Einheit unter `snippets/`.
Snippets sind dazu gedacht, kopiert und angepasst zu werden.</dd>

<dt markdown>**Report**</dt>
<dd markdown>Eine mit Zeitstempel versehene Markdown-Datei unter `reports/`,
die eine einzelne Ausführung beschreibt. Format:
`YYYY-MM-DD-<slug>.md`.</dd>

<dt markdown>**Decision**</dt>
<dd markdown>Eine architektonische oder betriebliche Entscheidung, die in
`memory/decisions.md` mit einer vierstelligen Nummer und einem Status
festgehalten wird.</dd>

<dt markdown>**Agent**</dt>
<dd markdown>Jeder Prozess — menschlich oder autonom — der bei der Arbeit am
Repository `AGENT.md` befolgt.</dd>

<dt markdown>**Task**</dt>
<dd markdown>Eine einzelne Arbeitseinheit, die in `tasks/queue.md` aufgeführt ist.
Eine Aufgabe pro Ausführung.</dd>
</dl>

## Workflow-Begriffe

<dl markdown>
<dt markdown>**Push to `main`**</dt>
<dd markdown>Löst `pages.yml` aus, das die Website neu erstellt und bereitstellt.
Jede Änderung an der veröffentlichten Website erfolgt über diesen
Mechanismus.</dd>

<dt markdown>**Agent run**</dt>
<dd markdown>Eine ausgelöste Ausführung von `.github/workflows/wikicode-agent.yml`,
entweder durch `workflow_dispatch`, durch eine `@agent`-Erwähnung auf
einem Issue oder durch ein mit `agent` gekennzeichnetes Issue.</dd>

<dt markdown>**Frontmatter**</dt>
<dd markdown>YAML-Metadaten am Anfang einer Markdown-Datei, begrenzt durch `---`.
WikiCode erwartet mindestens `title`, `description` und `created`.</dd>

<dt markdown>**Tag**</dt>
<dd markdown>Ein im Frontmatter deklariertes Label, das verwandte Seiten gruppiert.
Material erstellt automatisch Indexseiten pro Tag.</dd>
</dl>

## Statuswerte

Seiten und Projekte können einen `status` in ihrem Frontmatter deklarieren:

| Status      | Bedeutung                                                         |
| ----------- | ---------------------------------------------------------------- |
| `draft`     | In Arbeit; möglicherweise unvollständig oder fehlerhaft.          |
| `stable`    | Überprüft und als korrekt erachtet. Kann sich noch weiterentwickeln. |
| `archived`  | Zur Referenz aufbewahrt; wird nicht mehr gewartet.                |
| `deprecated`| Durch etwas anderes ersetzt; aus historischem Kontext beibehalten.  |

`status: stable` ist die Standarderwartung für alle veröffentlichten
Inhalte.