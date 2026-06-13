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

## 0003 — Local LLM agent via Ollama (replaces OpenHands Cloud)

**Date:** 2026-06-13
**Status:** Accepted
**Supersedes:** 0003 (original OpenHands decision)

**Context**
The original agent integration relied on the OpenHands Cloud REST API,
which required a paid API key, depended on an external cloud service,
and ran asynchronously (fire-and-forget). The agent had no ability
to validate content before pushing.

**Decision**
Replace the OpenHands Cloud API with a fully local inference stack
running inside the GitHub Actions runner:

1. **Ollama** serves as the local LLM server.
2. **Qwen2.5:7b** provides the intelligence (CPU-optimized 4-bit
   quantized model, ~4.5 GB RAM).
3. **`scripts/agent.py`** orchestrates the agent loop: read memory →
   pick task → research (web) → generate content → validate →
   commit → push.

The model is cached via `actions/cache` so subsequent runs skip the
download. Web research is performed through DuckDuckGo Instant
Answer and Wikipedia APIs — no additional tokens needed.

**Consequences**
- Zero API costs. The agent runs entirely on the CI runner's CPU and
  RAM (standard GitHub-hosted runner: 7 GB RAM; larger runner: 16 GB).
- Synchronous execution: the agent validates the MkDocs build before
  pushing, preventing broken commits.
- The model file is cached across runs (GitHub Actions cache), so
  only the first run downloads the full model (~4.5 GB).
- Smaller models can be used by setting the `OLLAMA_MODEL` env var
  (e.g., `qwen2.5:3b` for faster inference on standard runners).
- The agent no longer depends on any external AI service.

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
