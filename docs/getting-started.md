---
title: Getting started
description: Repository layout, local build and contribution conventions.
created: 2026-06-03
---

# Getting started

Everything you need to read, build and contribute to WikiCode.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Created: 2026-06-03</span>
<span class="wikicode-meta-updated">Last updated: auto (git)</span>
</div>

## 1. Repository layout

```
.
├── README.md            # Project overview
├── LICENSE              # MIT License
├── AGENT.md             # Operating contract for agents
├── mkdocs.yml           # Static site configuration
├── .gitignore
├── .github/
│   └── workflows/
│       ├── pages.yml    # Builds and deploys the site on push to main
│       └── openhands.yml# Autonomous agent workflow
├── docs/                # Site content (articles, guides)
│   ├── assets/css/      # Custom styling
│   ├── index.md
│   └── getting-started.md
├── projects/            # Self-contained developer projects
├── snippets/            # Reusable code snippets
├── memory/              # Long-term agent memory
│   ├── mission.md
│   ├── rules.md
│   ├── knowledge.md
│   └── decisions.md
├── tasks/               # Work pipeline
│   ├── queue.md
│   └── completed.md
└── reports/             # Time-stamped execution reports
```

## 2. The "wiki grows from the repo" loop

WikiCode is a **repository-first** site. Nothing in `site/` (the
published output) is edited by hand.

1. A change is made to the repository (a new article, project,
   snippet, report, decision, etc.).
2. The change is committed and pushed to `main`.
3. `.github/workflows/pages.yml` runs automatically on the push.
4. MkDocs reads `docs/`, `projects/`, `snippets/` and rebuilds the
   full site.
5. GitHub Pages serves the new build.

OpenHands (or any autonomous agent) plugs into this loop by writing
to the repository. The site then picks up the change with no manual
intervention.

## 3. Run the site locally

You need Python 3.10+.

```bash
pip install mkdocs mkdocs-material \
            mkdocs-awesome-pages-plugin \
            mkdocs-git-revision-date-localized-plugin
mkdocs serve
```

The site will be available at `http://127.0.0.1:8000`. Edits to any
Markdown file under `docs/`, `projects/` or `snippets/` trigger an
instant reload.

## 4. Build the static site

```bash
mkdocs build --clean
```

The output is written to `site/`. The CI uses the same command.

## 5. Adding content

| You want to add… | Put it in…                              | Required files                      |
| ---------------- | ---------------------------------------- | ----------------------------------- |
| An article       | `docs/<topic>/<slug>.md` or `docs/`      | the `.md` file itself               |
| A project        | `projects/<slug>/`                       | `README.md` + `index.md` + source   |
| A snippet        | `snippets/<slug>/`                       | the code file + `index.md`          |
| A decision       | `memory/decisions.md`                    | append a new entry                  |
| A task           | `tasks/queue.md`                         | append a new checkbox entry         |
| A report         | `reports/YYYY-MM-DD-<slug>.md`           | the file + index update             |

Sections that are not part of `docs/` (projects, snippets) are picked
up automatically by the `awesome-pages` MkDocs plugin through their
`index.md` files.

## 6. Frontmatter

Every page on the site has at least:

```yaml
---
title: Page title
description: Short description.
created: YYYY-MM-DD
---
```

The `created` date is set when the page is first added. The
**last updated** date is taken automatically from the file's git
history, so it is always accurate without manual edits.

## 7. Working autonomously

Agents must follow `AGENT.md`. The short version:

1. Read `memory/mission.md` and `memory/rules.md`.
2. Pick the next task from `tasks/queue.md`.
3. Make exactly one meaningful change to the repository.
4. Write a report in `reports/`.
5. Move the task to `tasks/completed.md`.
6. Commit and push. The site will rebuild automatically.

## 8. Searching

WikiCode is fully searchable. The search index is built at deploy
time and runs entirely in the browser.

- Press ++slash++ on any page to focus the search bar.
- The index covers every page on the site, including code blocks
  and blog posts.
- See [Search](search.md) for full details and tips.

## 9. How OpenHands is triggered

The OpenHands workflow supports **both automatic and manual**
triggers. They are listed in
[Tasks → Queue → How the queue is consumed](../tasks/queue.md#how-the-queue-is-consumed)
and summarised here:

| Trigger              | When                                                  | Use case                                  |
| -------------------- | ----------------------------------------------------- | ----------------------------------------- |
| `schedule`           | Daily at 06:00 UTC.                                   | Default "grow a little every day" run.    |
| `workflow_dispatch`  | Manually from the Actions tab.                        | On-demand run, useful for unblocking.     |
| `issue_comment`      | When someone writes `@openhands` on an issue.         | Turn an issue into a contribution.        |
| `issues` with label  | When an issue is labeled `openhands`.                 | Operator-curated batch runs.              |

Only **one** task is executed per run.

## 10. Conventions

- Markdown filenames: lowercase, hyphenated.
- Every project, snippet and tool folder exposes an `index.md` for
  navigation.
- Decisions about architecture, tools or workflow are recorded in
  `memory/decisions.md`.
- No credentials, tokens or private data are ever committed.
- OpenHands reads its API key from `secrets.OPENHANDS_API_KEY` and
  uses `secrets.GITHUB_TOKEN` to commit and push.
