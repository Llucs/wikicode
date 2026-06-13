---
title: Tools
description: Developer tools documented in WikiCode.
created: 2026-06-03
tags:
  - meta
  - tools
status: stable
---

# Tools

Developer tools documented in WikiCode. Each tool is a real
Markdown folder under `docs/tools/<slug>/` with an `index.md`
(summary) and optional subpages (install, usage, internals,
gotchas).

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Created: 2026-06-03</span>
<span class="wikicode-meta-updated">Last updated: auto (git)</span>
</div>

## How tools are added

Both the local AI agent and human contributors follow the same recipe:

2. Research the tool. The agent uses DuckDuckGo and Wikipedia
   capability to fetch the official docs, release notes and
   reputable third-party write-ups.
3. Write a `docs/tools/<slug>/index.md` summary.
4. Add subpages only when there is enough material:
   - `install.md` — install / upgrade / uninstall.
   - `usage.md` — common workflows, copy-paste examples.
   - `internals.md` — how it works under the hood.
   - `gotchas.md` — known footguns and sharp edges.
5. Add frontmatter including the tool's name, category and tags.
6. Open a pull request (or, for agents, commit directly when
   triggered by the daily workflow).

## Current tools

The list below is generated automatically by the `awesome-pages`
plugin.

<!--awesome-pages:hide-->
<!--awesome-pages:reveal-->

## Conventions

- One folder per tool. Folder name: lowercase, hyphenated.
- `index.md` is the public summary; subpages are optional and
  named after their content (`install.md`, `usage.md`, etc.).
- Frontmatter must include `title`, `description`, `created`,
  `tags` and (when applicable) a `status`.
- Tags should include the tool's category
  (`tool-cli`, `tool-build`, `tool-runtime`, etc.) so they show
  up in the tag index.
- A tool page should be useful on its own: include a one-paragraph
  "what it is", a "when to reach for it" note, and at least one
  runnable example.

## Anti-duplication

Before adding a tool, the contributor must verify that the tool is
not already covered. The `awesome-pages` plugin auto-renders the
list above from the `index.md` files in each subfolder, so the
authoritative list of "covered tools" is the file system itself.
