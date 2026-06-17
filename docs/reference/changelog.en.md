---
title: Changelog
description: Notable changes to WikiCode.
created: 2026-06-03
tags:
  - reference
  - meta
status: stable
---

# Changelog

Notable changes to WikiCode. Smaller, day-to-day edits are tracked
in git history; only structural and user-visible changes appear
here.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Created: 2026-06-03</span>
<span class="wikicode-meta-updated">Last updated: auto (git)</span>
</div>

## 1.0.0 — 2026-06-03 — Bootstrap

Initial production-oriented structure.

### Added

- **Site generation.** MkDocs (Material theme) with client-side
  search, automatic section indexes and a clean, custom CSS layer.
- **Repository-first publication.** The site is regenerated from
  the repository on every push to `main` via
  `.github/workflows/pages.yml`. Nothing in the published site is
  edited by hand.
- **AI agent (OpenCode API).** `.github/workflows/wikicode-agent.yml`
  runs the autonomous agent on the CI runner. Content generation via
  OpenCode API (`deepseek-v4-flash-free`), web research via Wikipedia
  and DuckDuckGo APIs. No external API keys needed.
- **GitHub Pages.** Enabled with the workflow build type and HTTPS
  enforced.
- **Content sections.**
  - `docs/` for articles, guides and reference pages.
  - `projects/` for self-contained, runnable projects.
  - `snippets/` for focused code snippets.
  - `blog/` for longer write-ups and announcements.
  - `memory/` for long-term agent context (mission, rules,
    knowledge, decisions).
  - `tasks/` for the work pipeline.
  - `reports/` for time-stamped execution reports.
- **Date metadata.** Every page shows a card with its **created**
  date (from frontmatter) and **last updated** date (from git
  history, via `mkdocs-git-revision-date-localized-plugin`).
- **Tag system.** Pages can declare tags in frontmatter; the
  Material theme renders per-tag index pages automatically.
- **Top-level guides.**
  - [Glossary](glossary.md)
  - [Architecture](architecture.md)
  - [Changelog](changelog.md) (this page)
  - [Learning paths](../learning-paths.md)
- **Root files.** `README.md`, `LICENSE`, `AGENT.md`,
  `CONTRIBUTING.md`, `CHANGELOG.md`, `ARCHITECTURE.md`,
  `.gitignore`.
- **Initial decisions.** Four numbered entries in
  `memory/decisions.md` (0001–0004).
- **Initial tasks.** Four queued items in `tasks/queue.md`.

### Notes

- The site is live at the URL provided by GitHub Pages once the
  first `pages.yml` run completes successfully.
- No external API keys are required. The agent uses `GITHUB_TOKEN`
  (built-in) for repository access and the OpenCode API for content
  generation.
