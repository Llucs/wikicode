---
title: Architecture
description: How WikiCode is built and how it stays up to date.
created: 2026-06-03
tags:
  - reference
  - architecture
  - meta
status: stable
---

# Architecture

How WikiCode is built, how it stays up to date, and how autonomous
agents fit into the loop.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Created: 2026-06-03</span>
<span class="wikicode-meta-updated">Last updated: auto (git)</span>
</div>

## High-level diagram

```
┌──────────────────────────────────────────────────────────────┐
│                       Repository                             │
│                                                              │
│   docs/        projects/    snippets/                        │
│   memory/      tasks/       reports/                         │
│   blog/        scripts/     mkdocs.yml                       │
│                                                              │
└─────────────┬──────────────────────────────┬────────────────┘
              │                              │
              │  push to main                │  Agent run
              │                              │  (manual, schedule,
              │                              │   @agent, label)
              ▼                              ▼
      ┌──────────────────┐         ┌──────────────────────┐
      │  pages.yml       │         │  wikicode-agent.yml  │
      │  ─ mkdocs build  │         │  ─ install deps      │
      │  ─ upload Pages  │         │  ─ read context      │
      │    artifact      │         │  ─ web research*     │
      └────────┬─────────┘         │  ─ generate content  │
               │                  │  ─ validate build    │
               │                  │  ─ commit & push     │
               │                  └──────────┬───────────┘
               │                             │
               ▼                             │
       GitHub Pages                          │
       (public site)                         │
                                             │
       new commit on main  ◄─────────────────┘
```

`*` The agent uses Wikipedia and DuckDuckGo APIs for web research,
no API keys required.

## Layers

### 1. Content

Plain Markdown. Authoring requires no special tooling.

| Path             | Purpose                                                            |
| ---------------- | ------------------------------------------------------------------ |
| `docs/`          | Articles, guides, reference, the things you read on the site.      |
| `docs/guides/`   | Long-form, topic-oriented guides.                                  |
| `docs/tools/`    | One folder per documented developer tool.                          |
| `docs/reference/`| Glossary, architecture, changelog.                                 |
| `docs/topics/`   | Topic index.                                                       |
| `projects/`      | Real, runnable projects. Each one is a self-contained unit.        |
| `snippets/`      | Small, focused, runnable code snippets.                            |
| `blog/`          | Longer write-ups, announcements, post-mortems.                     |
| `memory/`        | Long-term context for agents (mission, rules, decisions).         |
| `tasks/`         | Work pipeline (queue + completed).                                 |
| `reports/`       | Time-stamped execution reports.                                    |

### 2. Generation

- **MkDocs** with the **Material** theme turns the Markdown tree
  into a static site.
- Plugins:
  - `search` — client-side full-text search.
  - `awesome-pages` — automatic section indexes.
  - `git-revision-date-localized` — last-updated date from git.
  - `blog` — Material's built-in blog support.
  - `git-committers` — optional, controlled by env var.

### 3. Deployment

- `pages.yml` runs on every push to `main`. It builds the site and
  deploys it to **GitHub Pages** using the official Pages actions
  (`actions/upload-pages-artifact` + `actions/deploy-pages`).
- Pages is configured with `build_type: workflow` and HTTPS
  enforced.

### 4. Automation

#### Daily growth

`wikicode-agent.yml` runs on a **twice-daily schedule** (`0 6,18 * * *`,
06:00 and 18:00 UTC) and on manual triggers. Each run is a single,
scoped change so the wiki grows a little every day.

The expected loop per run:

1. The workflow starts. Python dependencies are installed.
2. `scripts/agent.py` reads `memory/` for context. If the task queue
   is empty, it proactively discovers new tools and projects to
   document. It then researches the chosen topic via Wikipedia +
   DuckDuckGo APIs.
3. The OpenCode API generates the content (Markdown with frontmatter).
4. The agent writes the files, runs `mkdocs build --clean` to
   validate, then commits and pushes.
5. `pages.yml` rebuilds and deploys the site.
6. The next run's execution sees a slightly larger wiki and continues.

#### Triggers

| Trigger                  | Use case                                                |
| ------------------------ | ------------------------------------------------------- |
| `schedule`               | The default growth run (06:00 and 18:00 UTC).          |
| `workflow_dispatch`      | Manual run from the Actions tab.                         |
| `issue_comment`          | `@agent` mention on an issue or PR comment.             |
| `issues` with label      | Issues labeled `agent`.                                 |

#### Concurrency

`concurrency: wikicode-agent` is set with `cancel-in-progress: true`
so that overlapping runs do not double-write the repository.

### 5. Anti-duplication

WikiCode does not want to document the same thing twice. The
deduplication mechanism has three parts:

1. **Section index pages.** Every section has an `index.md` that
   lists its current contents. The `awesome-pages` plugin
   auto-discovers the list from the file system, so it is always
   accurate.
2. **`git grep` fallback.** The agent script scans section indexes
   and the task list, then uses `git grep` to confirm a topic is
   new before generating content.
3. **Knowledge ledger.** `memory/knowledge.md` lists the major
   pieces of content and the rules for adding new ones.

If a duplicate is detected, the agent must improve the existing
page instead of writing a new one (rule 11 in `AGENT.md`).

### 6. Web research

The agent uses Wikipedia and DuckDuckGo APIs to gather information
about any topic it needs to document. This is the mechanism that
keeps the generated content factual and up-to-date:

1. `research_topic()` in `scripts/agent.py` runs both a Wikipedia
   search and a DuckDuckGo Instant Answer query for the topic.
2. Wikipedia returns article titles + introductory extracts (plain
   text, up to 2000 chars).
3. DuckDuckGo returns the abstract and related topics.
4. If both return empty, the agent falls back to the LLM's training
   knowledge.
5. The gathered research text is injected into the content generation
   prompt so the LLM writes from real-world information.

## Frontmatter contract

Every page on the site should have:

```yaml
---
title: Human-readable title
description: One-sentence summary.
created: YYYY-MM-DD
tags: [tag1, tag2]
status: draft | stable | archived | deprecated
---
```

`title` and `description` are used in navigation and search.
`created` feeds the metadata card; `git-revision-date-localized`
fills the "last updated" date automatically. `tags` enables the
tag-based browsing. `status` signals the maturity of the page.

## Secrets and security

| Secret              | Purpose                                            | Source                |
| ------------------- | -------------------------------------------------- | --------------------- |
| `GITHUB_TOKEN`      | Repository access inside workflows.                | Built-in.             |

No credentials are stored in the repository.

## How to evolve the architecture

Any change that affects how the site is built, deployed or
automated should:

1. Be recorded as a new entry in `memory/decisions.md` with the next
   available number.
2. Be reflected in this page if it changes the high-level diagram.
3. Keep the repository-first contract: never edit the published site
   directly.
