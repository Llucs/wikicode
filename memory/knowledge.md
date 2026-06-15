---
title: Knowledge
description: Long-term knowledge accumulated by WikiCode.
created: 2026-06-03
tags:
  - reference
  - meta
status: stable
---

# Knowledge

Long-term knowledge accumulated by WikiCode and its agents. Entries
should be small, factual and reference the source of truth (commit,
issue, article).

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Created: 2026-06-03</span>
<span class="wikicode-meta-updated">Last updated: auto (git)</span>
</div>

## Stack

- **Static site generator:** MkDocs + Material theme.
- **Search:** MkDocs built-in `search` plugin (client-side index).
- **Navigation:** `awesome-pages` plugin for automatic section indexes.
- **Dates:** `mkdocs-git-revision-date-localized-plugin` for created / last updated.
- **Blog:** Material's built-in `blog` plugin.
- **Hosting:** GitHub Pages (workflow deployment).
- **Automation:** GitHub Actions + OpenCode API (deepseek-v4-flash-free).

## Agent capabilities

The AI agent (`scripts/agent.py`) runs inside the GitHub Actions runner
using the OpenCode API. It has:

- **Content generation** via OpenCode API (`deepseek-v4-flash-free` model).
- **Web research** via Wikipedia API and DuckDuckGo Instant Answer API — no API keys needed.
- **Shell access** to run `git`, `mkdocs`, `python`, etc.
- **File editing.** It creates and modifies Markdown files inside the repository.
- **Git operations** to commit and push changes back to the repository.
- **Validation.** It runs `mkdocs build --clean` before every commit to ensure nothing is broken.

## Anti-duplication

Before adding a new article, project, snippet, tool or blog post,
the agent **must** verify that the topic is not already covered.
The procedure is:

1. Read the relevant section's `index.md`.
2. If the section is large, run `git grep` over the section for
   the planned title, slug or key terms.
3. For tools, check `docs/tools/<slug>/` for an existing folder.
4. If a duplicate is found, either improve the existing page or
   pick a different topic from `tasks/queue.md`.
5. If the topic is genuinely new, proceed and add a "neighbouring
   topics" note in the new page so future agents notice the
   relationship.

## Conventions

- Markdown filenames: lowercase, hyphenated.
- Every project / snippet / tool folder exposes an `index.md`.
- Every Markdown page has frontmatter (`title`, `description`,
  `created`, `tags`, `status`).
- Reports are timestamped: `reports/YYYY-MM-DD-<slug>.md`.

## Daily execution loop

The wikicode-agent workflow runs twice daily (`0 6,18 * * *`,
06:00 and 18:00 UTC) and on manual / push triggers. The expected loop is:

1. The workflow runs.
2. It checks out the repository and installs dependencies.
3. The agent reads memory, checks the queue, and researches the
   topic via Wikipedia + DuckDuckGo APIs.
4. The agent generates content using the OpenCode API, writes the
   content, validates with `mkdocs build`, commits, and pushes.
5. The Pages workflow rebuilds and deploys the site.
6. The next run continues the loop.

This is what makes the wiki "grow a little every day".

## Glossary

| Term       | Meaning                                                                 |
| ---------- | ----------------------------------------------------------------------- |
| WikiCode   | The repository and the site it produces.                                |
| Agent      | The autonomous `scripts/agent.py` process that follows `AGENT.md`.      |
| OpenCode   | Cloud LLM API (deepseek-v4-flash-free) used for content generation.    |
| Task       | A single unit of work listed in `tasks/queue.md`.                       |
| Report     | A time-stamped Markdown file in `reports/` describing an execution.     |
| Decision   | An architectural or operational choice recorded in `decisions.md`.      |
| Frontmatter| YAML metadata at the top of a Markdown file.                           |
| Tag        | A label in frontmatter that groups related pages.                      |

## External references

- MkDocs documentation: https://www.mkdocs.org/
- Material for MkDocs: https://squidfunk.github.io/mkdocs-material/
- GitHub Pages: https://docs.github.com/en/pages
- OpenCode: https://opencode.ai/
- GitHub Actions: https://docs.github.com/en/actions
