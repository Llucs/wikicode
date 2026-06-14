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
theme) and published automatically through GitHub Pages. All content
is created by an autonomous AI agent that uses the OpenCode API for
intelligent content generation — no local LLM required, fast and reliable.

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
├── requirements.txt
├── .github/workflows/
│   ├── pages.yml
│   └── wikicode-agent.yml
├── scripts/
│   └── agent.py
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
| `scripts/`     | Agent orchestration (`agent.py` — the autonomous AI agent).             |
| `docs/`        | Source for the static site (articles, guides, references).              |
| `projects/`    | End-to-end projects with their own README, structure and code.          |
| `snippets/`    | Small, focused, runnable code snippets grouped by language or topic.    |
| `memory/`      | Persistent context for autonomous agents (mission, rules, decisions).   |
| `tasks/`       | Pending and completed tasks; the single source of work.                 |
| `reports/`     | Time-stamped reports describing what an execution actually did.         |

## Autonomous workflow

WikiCode is evolved by an autonomous AI agent that runs inside
GitHub Actions. It self-discovers what to document next.

1. The workflow (`wikicode-agent.yml`) runs twice daily (06:00 and
   18:00 UTC), or on push, or manually.
2. `scripts/agent.py` reads `memory/` for context, then checks the
   task queue. If the queue is empty, it proactively discovers new
   developer tools and projects to document using the OpenCode API.
3. It researches the topic via the API, generates content, and
   writes the files.
4. It validates with `mkdocs build --clean` before committing.
5. It moves the completed task to `tasks/completed.md`, commits,
   and pushes.
6. The Pages workflow (`pages.yml`) rebuilds and deploys the site.

Trigger the agent manually from the Actions tab by running the
**wikicode-agent** workflow, or by commenting `@agent` on an issue.

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

Released under the Apache License 2.0. See [LICENSE](LICENSE).
