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

## 0003 — Use OpenCode API for AI generation

**Date:** 2026-06-03
**Status:** Superseded by 0005

**Context**
The autonomous agent needs to generate high-quality technical
content without requiring external API keys or paid services.

**Decision**
Use the OpenCode API (`deepseek-v4-flash-free`) as the AI provider
for content generation, research, and task analysis. The API is
free, requires no API key, and provides a capable model for
technical content.

**Consequences**
- No API keys or secrets needed in the repository.
- Content generation depends on cloud API availability.
- Limited to the capabilities of the free-tier model.

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

---

## 0005 — Qwen3.6-27B local inference (replaces OpenCode API)

**Date:** 2026-06-25
**Status:** Accepted
**Supersedes:** 0003

**Context**
The OpenCode API (`deepseek-v4-flash-free`) required a cloud
dependency. To make the agent fully self-contained and run entirely
on GitHub Actions free tier, replace the cloud API with a local
model running on the CI runner itself.

**Decision**
Run Qwen3.6-27B-MTP at IQ2_M quantization (10.8 GB) inside the
GitHub Actions runner using llama.cpp server:

1. **Model:** Qwen3.6-27B-MTP GGUF (IQ2_M, 10.8 GB) — 77.2%
   SWE-bench Verified, multilingual (201 languages), dense 27B.
2. **Runtime:** llama.cpp `llama-server` with mmap + 16 GB swap.
3. **API:** OpenAI-compatible endpoint at `http://127.0.0.1:8080/v1`.
4. **Cache:** Model cached via `actions/cache` to avoid re-download.

**Consequences**
- Zero external dependencies — no cloud API required.
- Maximum quality for code and technical content (Qwen3.6-27B).
- Slower inference (~1-3 tok/s on CPU) increases workflow time.
- 10.8 GB model file requires disk cleanup and swap on the runner.
- Model cached between runs via GitHub Actions cache.

---

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
