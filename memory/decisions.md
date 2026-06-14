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

## 0003 — API-based agent via OpenCode API (replaces Ollama)

**Date:** 2026-06-14
**Status:** Superseded
**Supersedes:** 0003 (original Ollama decision)

**Context**
The original agent used a local Ollama inference stack inside the CI
runner, which required a ~4.5 GB model download on first run, had
slow CPU-only inference, and consumed significant CI time and memory.

**Decision**
Replace Ollama with the OpenCode API (`opencode.ai/zen/v1`) for all
content generation:

1. **OpenCode API** serves as the AI backend with the
   `deepseek-v4-flash-free` model.
2. **`scripts/agent.py`** orchestrates the agent loop: read memory →
   discover/probe queue → research (web + API) → generate content →
   validate → commit → push.
3. Web research is performed through DuckDuckGo Instant Answer and
   Wikipedia APIs — no additional tokens needed.

**Consequences**
- No model download or caching required; inference is instant.
- Faster execution: runs complete in minutes instead of 20+ minutes.
- The agent proactively discovers tools and projects when the queue
  is empty, making the wiki truly self-evolving.
- The agent no longer depends on local CPU inference.

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
- The local AI agent grows the wiki by writing to the repo; the site
  picks up the change automatically on the next push.
