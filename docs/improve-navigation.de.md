---
title: Navigation-Audit für WikiCode
description: Analyse und vorgeschlagene Verbesserungen für die Seitennavigation von WikiCode.
created: 2026-06-14
tags:
  - meta
  - guide
status: draft
---

# Navigation-Audit

## Aktuelle Struktur

Die Hauptnavigation ist in `mkdocs.yml` definiert und umfasst derzeit:

- Startseite
- Suche
- Erste Schritte
- Lernpfade
- Leitfäden
- Referenz (Glossar, Architektur, Changelog)
- Themen
- Werkzeuge
- Tags
- Blog
- Projekte
- Snippets
- Berichte

## Vorgeschlagene Verbesserungen

1. Meta-Abschnitte unter einem einzigen Menüpunkt 'About' oder 'WikiCode' zusammenfassen (Berichte, Changelog, Architektur)
2. Tags innerhalb von Themen verschieben, da verwandte Konzepte
3. Visuelle Indikatoren für kürzlich aktualisierte Inhalte hinzufügen
4. Breadcrumbs auf allen Navigationsebenen aktiv halten

## Umsetzung

Alle Änderungen sollten im `nav:`-Block in `mkdocs.yml` vorgenommen werden.