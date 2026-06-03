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
- **Navigation:** `awesome-pages` plugin for automatic section
  indexes.
- **Dates:** `mkdocs-git-revision-date-localized-plugin` for
  created / last updated.
- **Blog:** Material's built-in `blog` plugin.
- **Hosting:** GitHub Pages (workflow deployment).
- **Automation:** GitHub Actions, OpenHands agent.

## OpenHands capabilities

The OpenHands agent has access to several capabilities that shape
how it should work on this repository:

- **Shell access.** It can run `git`, `mkdocs`, `python`, etc. to
  build, validate and inspect the repository.
- **File editing.** It can create, edit and delete files inside
  the repository.
- **Web research.** It can browse the public web to gather
  information about tools, languages, libraries and patterns.
  This is the mechanism used to document tools in `docs/tools/`.
- **Issue / PR interaction.** It can read issues, leave comments
  and open pull requests.
- **Git operations.** Combined with `GITHUB_TOKEN`, it can commit
  and push the changes it makes.

## Anti-duplication

Before adding a new article, project, snippet, tool or blog post,
the agent **must** verify that the topic is not already covered.
The procedure is:

1. Read the relevant section's `index.md` (the `awesome-pages`
   plugin renders an auto-discovered list there).
2. If the section is large, run `git grep` over the section for
   the planned title, slug or key terms.
3. For tools, check `docs/tools/<slug>/` for an existing folder.
4. If a duplicate is found, either:
   - Improve the existing page, or
   - Pick a different topic from `tasks/queue.md`.
5. If the topic is genuinely new, proceed and add a short
   "neighbouring topics" note in the new page so future agents
   notice the relationship.

This is encoded in `AGENT.md` and in the daily workflow's
`Detect existing content for the planned task` step.

## Conventions

- Markdown filenames: lowercase, hyphenated.
- Every project / snippet / tool folder exposes an `index.md`.
- Every Markdown page has frontmatter (`title`, `description`,
  `created`, `tags`, `status`).
- Reports are timestamped: `reports/YYYY-MM-DD-<slug>.md`.

## Daily execution loop

The OpenHands workflow runs on a daily schedule (`0 6 * * *`,
06:00 UTC) and on manual triggers. The expected loop is:

1. The workflow runs.
2. It checks out the repository and lists the current state of
   every section, the task queue and the knowledge ledger.
3. The agent reads the queue, picks the next task (or proposes a
   new one if the queue is empty), verifies it is not duplicated,
   and executes it.
4. The agent commits the change and pushes it. `pages.yml`
   rebuilds and deploys the site.
5. The next day's run sees a slightly larger wiki and continues
   the loop.

This is what makes the wiki "grow a little every day".

## Glossary

| Term       | Meaning                                                                 |
| ---------- | ----------------------------------------------------------------------- |
| WikiCode   | The repository and the site it produces.                                |
| Agent      | Any autonomous process (human or AI) that follows `AGENT.md`.           |
| Task       | A single unit of work listed in `tasks/queue.md`.                       |
| Report     | A time-stamped Markdown file in `reports/` describing an execution.     |
| Decision   | An architectural or operational choice recorded in `decisions.md`.      |
| Tool       | A developer tool documented under `docs/tools/<slug>/`.                |
| Frontmatter| YAML metadata at the top of a Markdown file.                           |
| Tag        | A label in frontmatter that groups related pages.                      |

## External references

- MkDocs documentation: https://www.mkdocs.org/
- Material for MkDocs: https://squidfunk.github.io/mkdocs-material/
- GitHub Pages: https://docs.github.com/en/pages
- OpenHands: https://github.com/All-Hands-AI/OpenHands
- GitHub Actions cron syntax: https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule
