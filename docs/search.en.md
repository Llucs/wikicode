---
title: Search the wiki
description: How to search WikiCode.
created: 2026-06-03
tags:
  - meta
  - reference
status: stable
---

# Search the wiki

WikiCode is fully searchable. The search index is built at deploy
time and runs entirely in the browser, so queries are instant and
no data leaves your machine.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Created: 2026-06-03</span>
<span class="wikicode-meta-updated">Last updated: auto (git)</span>
</div>

## How to search

<div class="grid cards" markdown>

- :material-magnify: __Search bar__

    Click the magnifying glass icon in the top right of any page
    (or press ++slash++ on the keyboard) to open the search modal.

- :material-keyboard: __Keyboard shortcut__

    - ++slash++ — focus the search bar.
    - ++esc++ — close the search modal.
    - ++arrow-up++ / ++arrow-down++ — move through results.
    - ++enter++ — open the highlighted result.

- :material-format-letter-case: __Tips__

    - Search is **substring-based**. Typing `mkdocs` matches any
      page containing "mkdocs".
    - Search is **case-insensitive** by default.
    - Quoted phrases match exact substrings: `"open hands"`.
    - Multiple words match pages that contain all of them.

</div>

## What is indexed

The search index covers every Markdown page rendered on the site:

- Articles, guides and reference pages under `docs/`.
- Project summaries under `projects/`.
- Snippet descriptions under `snippets/`.
- Tool pages under `docs/tools/`.
- Blog posts under `blog/`.
- The text of code blocks (so you can search for a function name
  or a CLI flag).

The index is regenerated on every push to `main`, so it is always
in sync with the published content.

## Why client-side

- **Privacy.** No queries are sent to a remote service.
- **Speed.** Results appear as you type.
- **Cost.** There is nothing to host beyond the static site.
- **Offline.** Once the site has loaded, the index is in the
  browser cache and continues to work without a network.

## Adding a custom search shortcut

If you want a deep link that opens the search modal pre-filled,
append `?q=<query>` to the site URL after the search has been
focused once. The exact behavior depends on the Material theme
version; the recommended way is to use the keyboard shortcut
(++slash++) and type the query.
