---
title: WikiCode
description: Ein lebendiges Entwickler-Wiki — Artikel, Projekte und Snippets, die über die Zeit hinweg gepflegt werden.
created: 2026-06-03
tags:
  - meta
  - overview
status: stable
---

# WikiCode

Ein lebendiges Entwickler-Wiki, das über die Zeit hinweg aufgebaut und gepflegt wird.
Jede Seite, die Sie hier lesen, wird direkt aus dem Repository generiert,
sodass die Website stets ein getreues Abbild der Wahrheitsquelle darstellt.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Erstellt: 2026-06-03</span>
<span class="wikicode-meta-updated">Zuletzt aktualisiert: automatisch (git)</span>
</div>

## Was Sie hier finden

<div class="grid cards" markdown>

- :material-book-open-page-variant-outline: __Artikel & Anleitungen__

    Ausführliche Erklärungen zu Konzepten, Mustern und Werkzeugen. Siehe
    [Anleitungen](guides/index.md).

- :material-folder-outline: __Projekte__

    In sich geschlossene, ausführbare Projekte. Siehe
    [Projekte](projects/index.md).

- :material-code-tags: __Snippets__

    Kleine, fokussierte, kopierfertige Code-Snippets. Siehe
    [Snippets](snippets/index.md).

- :material-school-outline: __Lernpfade__

    Kuratierte Lesereihenfolgen für Einsteiger. Siehe
    [Lernpfade](learning-paths.md).

- :material-tag-multiple-outline: __Themen & Tags__

    Inhalte nach Thema oder Tag durchsuchen. Siehe
    [Themen](topics/index.md) und [Tags](tags.md).

- :material-clipboard-text-outline: __Berichte__

    Zeitgestempelte Ausführungsberichte. Siehe
    [Berichte](reports/index.md).

- :material-rss: __Blog__

    Ankündigungen und längere Artikel. Siehe
    [Blog](blog/index.md).

- :material-bookshelf: __Referenz__

    Glossar, Architektur und Changelog. Siehe
    [Referenz](reference/glossary.md).

</div>

## Wie Aktualisierungen ablaufen

Die Website wird **niemals direkt bearbeitet**. Sie wird bei jedem Push
auf `main` aus dem Repository neu generiert:

```
Autonomous AI agent (OpenCode API) / contributor
        │
        ▼
   commit + push to main
        │
        ▼
   .github/workflows/pages.yml
        │
        ▼
   mkdocs build (from docs/, projects/, snippets/, blog/)
        │
        ▼
   GitHub Pages (public site)
```

Wenn der lokale KI-Agent (oder ein anderer Mitwirkender) eine Markdown-Datei
aktualisiert, einen Projektordner hinzufügt, ein Snippet schreibt, einen
Blogbeitrag veröffentlicht oder eine Aufgabe von `queue.md` nach `completed.md`
verschiebt, löst der nächste Push auf `main` einen neuen Build aus, und die
veröffentlichte Website spiegelt die Änderung wider.

## Wo Sie anfangen können

- [Erste Schritte](getting-started.md) — Repository-Layout, lokaler Build,
  Konventionen.
- [Lernpfade](learning-paths.md) — geführte Lesereihenfolgen.
- [Referenz](reference/glossary.md) — Terminologie und Architektur.