---
title: Suche im Wiki
description: Wie man WikiCode durchsucht.
created: 2026-06-03
tags:
  - meta
  - reference
status: stable
---

# Suche im Wiki

WikiCode ist vollständig durchsuchbar. Der Suchindex wird zur Bereitstellungszeit erstellt und läuft vollständig im Browser, sodass Abfragen sofort erfolgen und keine Daten Ihren Rechner verlassen.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Erstellt: 2026-06-03</span>
<span class="wikicode-meta-updated">Zuletzt aktualisiert: automatisch (git)</span>
</div>

## So suchen Sie

<div class="grid cards" markdown>

- :material-magnify: __Suchleiste__

    Klicken Sie auf das Lupensymbol in der oberen rechten Ecke einer beliebigen Seite (oder drücken Sie ++slash++ auf der Tastatur), um das Suchmodul zu öffnen.

- :material-keyboard: __Tastenkombination__

    - ++slash++ — Suchleiste fokussieren.
    - ++esc++ — Suchmodul schließen.
    - ++arrow-up++ / ++arrow-down++ — durch Ergebnisse navigieren.
    - ++enter++ — markiertes Ergebnis öffnen.

- :material-format-letter-case: __Tipps__

    - Die Suche erfolgt **teilzeichenfolgenbasiert**. Die Eingabe von `mkdocs` findet jede Seite, die „mkdocs“ enthält.
    - Die Suche ist standardmäßig **nicht case-sensitiv**.
    - In Anführungszeichen gesetzte Phrasen suchen nach exakten Teilzeichenfolgen: `"open hands"`.
    - Mehrere Wörter finden Seiten, die alle enthalten.

</div>

## Was wird indiziert

Das Suchverzeichnis deckt jede auf der Site gerenderte Markdown-Seite ab:

- Artikel, Anleitungen und Referenzseiten unter `docs/`.
- Projektzusammenfassungen unter `projects/`.
- Snippet-Beschreibungen unter `snippets/`.
- Werkzeugseiten unter `docs/tools/`.
- Blogbeiträge unter `blog/`.
- Der Text von Codeblöcken (so können Sie nach einem Funktionsnamen oder einem CLI-Flag suchen).

Der Index wird bei jedem Push auf `main` neu generiert, sodass er immer mit dem veröffentlichten Inhalt synchron ist.

## Warum clientseitig

- **Datenschutz.** Es werden keine Anfragen an einen entfernten Dienst gesendet.
- **Geschwindigkeit.** Ergebnisse erscheinen während der Eingabe.
- **Kosten.** Es muss nichts über die statische Seite hinaus gehostet werden.
- **Offline.** Sobald die Seite geladen ist, befindet sich der Index im Browser-Cache und funktioniert weiterhin ohne Netzwerk.

## Hinzufügen einer benutzerdefinierten Suchverknüpfung

Wenn Sie einen Deep-Link wünschen, der das Suchmodul vorausgefüllt öffnet, hängen Sie `?q=<query>` an die Site-URL an, nachdem die Suche einmal fokussiert wurde. Das genaue Verhalten hängt von der Version des Material-Themes ab; empfohlen wird die Verwendung der Tastenkombination (++slash++) und die Eingabe der Abfrage.