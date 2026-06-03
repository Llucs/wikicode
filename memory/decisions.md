---
title: Decisions
description: Architectural and operational decisions for WikiCode.
created: 2026-06-03
---

# Decisions

Architectural and operational decisions for WikiCode. Each entry
follows a short, consistent shape so they can be searched and
compared.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Created: 2026-06-03</span>
<span class="wikicode-meta-updated">Last updated: auto (git)</span>
</div>

---

## 0001 — Use MkDocs (Material) as the static site generator

**Date:** 2026-06-03
**Status:** Accepted

**Context**
WikiCode must be a documentation-first site with internal search,
navigation, categories and automatic content discovery. The site
should be hosted on GitHub Pages and require minimal maintenance.

**Decision**
Adopt MkDocs with the Material theme as the static site generator.
Use the `search` plugin for client-side full-text search and the
`awesome-pages` plugin for automatic section indexes (projects,
snippets).

**Consequences**
- All content is plain Markdown, easy to author and review.
- The site is regenerated on every push to `main`.
- The build keeps the published site free of broken configuration.

---

## 0002 — Documentation-first repository layout

**Date:** 2026-06-03
**Status:** Accepted

**Context**
The repository must host articles, projects and snippets in a single,
readable tree while remaining simple enough for autonomous agents to
navigate.

**Decision**
Adopt the following top-level layout:

```
docs/      articles and guides
projects/  self-contained projects
snippets/  focused code snippets
memory/    long-term agent memory
tasks/     work pipeline
reports/   execution reports
```

**Consequences**
- Each section has a single, obvious purpose.
- New agents can find context (`memory/`) and work (`tasks/`)
  without prior knowledge of the project.

---

## 0003 — OpenHands integration through GitHub Secrets

**Date:** 2026-06-03
**Status:** Accepted

**Context**
Autonomous agents must be able to run through GitHub Actions. Any
token used by the agent is sensitive and must not be committed.

**Decision**
The OpenHands workflow (`.github/workflows/openhands.yml`) reads its
API key from `secrets.OPENHANDS_API_KEY` and uses
`secrets.GITHUB_TOKEN` for repository access. Neither value is ever
written to the repository or logged.

**Consequences**
- A missing or invalid secret fails the workflow loudly.
- The repository remains safe to fork and audit.

---

## 0004 — Repository-first site generation

**Date:** 2026-06-03
**Status:** Accepted

**Context**
The published site must always reflect the source of truth, and
autonomous agents must be able to grow the wiki without manual
publishing steps.

**Decision**
The site is generated exclusively from the repository contents
(`docs/`, `projects/`, `snippets/`, `memory/`, `tasks/`, `reports/`).
There is no separate database, no CMS, and no manual editing of the
published site. Every push to `main` triggers
`.github/workflows/pages.yml`, which rebuilds and deploys the site
through the official GitHub Pages actions.

**Consequences**
- Contributors (humans or agents) only ever edit the repository.
- The published site is always derived state and never drifts.
- OpenHands grows the wiki by writing to the repo; the site picks up
  the change automatically on the next push.
