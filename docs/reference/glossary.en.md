---
title: Glossary
description: Terminology used across WikiCode.
created: 2026-06-03
tags:
  - reference
  - meta
status: stable
---

# Glossary

Canonical terminology used across WikiCode. Definitions are short
and link to the authoritative source where useful.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Created: 2026-06-03</span>
<span class="wikicode-meta-updated">Last updated: auto (git)</span>
</div>

## Core concepts

<dl markdown>
<dt markdown>**WikiCode**</dt>
<dd markdown>The repository and the static site it produces. "WikiCode"
refers to both, depending on context.</dd>

<dt markdown>**Article**</dt>
<dd markdown>A long-form Markdown page under `docs/`. Articles are
intended to be read in full.</dd>

<dt markdown>**Project**</dt>
<dd markdown>A self-contained, runnable piece of software under
`projects/`. Each project has its own `README.md`, `index.md` and
source tree.</dd>

<dt markdown>**Snippet**</dt>
<dd markdown>A small, focused, runnable code unit under `snippets/`.
Snippets are intended to be copied and adapted.</dd>

<dt markdown>**Report**</dt>
<dd markdown>A time-stamped Markdown file under `reports/` that
describes a single execution. Format:
`YYYY-MM-DD-<slug>.md`.</dd>

<dt markdown>**Decision**</dt>
<dd markdown>An architectural or operational choice recorded in
`memory/decisions.md` with a four-digit number and a status.</dd>

<dt markdown>**Agent**</dt>
<dd markdown>Any process — human or autonomous — that follows
`AGENT.md` when working on the repository.</dd>

<dt markdown>**Task**</dt>
<dd markdown>A single unit of work listed in `tasks/queue.md`. One
task per execution.</dd>
</dl>

## Workflow terms

<dl markdown>
<dt markdown>**Push to `main`**</dt>
<dd markdown>Triggers `pages.yml`, which rebuilds and deploys the
site. Every change to the published site happens via this
mechanism.</dd>

<dt markdown>**Agent run**</dt>
<dd markdown>A triggered execution of `.github/workflows/wikicode-agent.yml`,
either by `workflow_dispatch`, by an `@agent` mention on an
issue, or by an issue labeled `agent`.</dd>

<dt markdown>**Frontmatter**</dt>
<dd markdown>YAML metadata at the top of a Markdown file, delimited
by `---`. WikiCode expects at least `title`, `description` and
`created`.</dd>

<dt markdown>**Tag**</dt>
<dd markdown>A label declared in frontmatter that groups related
pages. Material renders per-tag index pages automatically.</dd>
</dl>

## Status values

Pages and projects can declare a `status` in their frontmatter:

| Status      | Meaning                                                         |
| ----------- | --------------------------------------------------------------- |
| `draft`     | Work in progress; may be incomplete or wrong.                   |
| `stable`    | Reviewed and considered correct. May still evolve.              |
| `archived`  | Kept for reference; no longer maintained.                      |
| `deprecated`| Superseded by something else; kept for historical context.      |

`status: stable` is the default expectation for any published
content.
