---
title: README
description: WikiCode project overview.
created: 2026-06-03
---

# WikiCode

WikiCode is a living developer wiki built and maintained over time.
It is a documentation-first repository that gathers technical
knowledge, real projects, code snippets and developer resources in a
single, searchable place.

The site is generated with [MkDocs](https://www.mkdocs.org/) (Material
theme) and published automatically through GitHub Pages.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Created: 2026-06-03</span>
<span class="wikicode-meta-updated">Last updated: auto (git)</span>
</div>

## What WikiCode is

- A long-form developer knowledge base written in Markdown.
- A catalogue of real, working projects and reusable snippets.
- A place where autonomous agents can read context, write content
  and evolve the wiki without losing track of decisions or history.

It is not a blog, not a portfolio, and not a tutorial mirror. Every
entry is meant to be self-contained, accurate and useful.

## Repository structure

```
.
├── README.md
├── LICENSE
├── AGENT.md
├── mkdocs.yml
├── .gitignore
├── .github/workflows/
│   ├── pages.yml
│   └── openhands.yml
├── docs/
│   ├── assets/css/extra.css
│   ├── index.md
│   └── getting-started.md
├── projects/
├── snippets/
├── memory/
│   ├── mission.md
│   ├── rules.md
│   ├── knowledge.md
│   └── decisions.md
├── tasks/
│   ├── queue.md
│   └── completed.md
└── reports/
```

| Path           | Purpose                                                                 |
| -------------- | ----------------------------------------------------------------------- |
| `docs/`        | Source for the static site (articles, guides, references).              |
| `projects/`    | End-to-end projects with their own README, structure and code.          |
| `snippets/`    | Small, focused, runnable code snippets grouped by language or topic.    |
| `memory/`      | Persistent context for autonomous agents (mission, rules, decisions).   |
| `tasks/`       | Pending and completed tasks; the single source of work.                 |
| `reports/`     | Time-stamped reports describing what an execution actually did.         |

## Autonomous workflow

WikiCode is designed to be evolved by autonomous agents, with a
human maintaining final review and merge rights.

1. An agent reads `memory/` to understand the mission and rules.
2. It picks **one** task from `tasks/queue.md`.
3. It performs the task, updates the wiki and writes a report in
   `reports/`.
4. It moves the task to `tasks/completed.md` and proposes a new
   entry in `memory/decisions.md` if an architectural choice was
   made.
5. The change is committed and pushed. The site rebuilds
   automatically through `.github/workflows/pages.yml`.
6. OpenHands is triggered manually (workflow dispatch) or by
   commenting `@openhands` on an issue.

The OpenHands workflow lives in `.github/workflows/openhands.yml`
and consumes its key from `secrets.OPENHANDS_API_KEY`, so no
credentials are stored in the repository.

## Contribution philosophy

- **Real over impressive.** No fake integrations, no placeholder
  demos.
- **One meaningful change at a time.** Small, reviewable commits.
- **Improve before expanding.** Quality of existing content matters
  more than volume of new content.
- **Document decisions.** If something is done a certain way, the
  reason lives in `memory/decisions.md`.
- **Stay readable.** The repository itself is the documentation of
  how the wiki is built.

## Running the site locally

```bash
pip install mkdocs mkdocs-material \
            mkdocs-awesome-pages-plugin \
            mkdocs-git-revision-date-localized-plugin
mkdocs serve
```

The site will be available at `http://127.0.0.1:8000`.

## Building the site

```bash
mkdocs build --clean
```

The static output is written to `site/`.

## License

Released under the MIT License. See [LICENSE](LICENSE).
