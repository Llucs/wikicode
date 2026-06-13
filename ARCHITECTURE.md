# Architecture

> The full, rendered version of this document lives on the site at
> [Reference → Architecture](docs/reference/architecture.md). The
> copy below is the same text, kept at the root of the repository
> for quick offline reference.

## High-level diagram

```
┌──────────────────────────────────────────────────────────────┐
│                       Repository                             │
│                                                              │
│   docs/        projects/    snippets/                        │
│   memory/      tasks/       reports/                         │
│   blog/        AGENT.md     mkdocs.yml                       │
│                                                              │
└─────────────┬──────────────────────────────┬────────────────┘
              │                              │
              │  push to main                │  OpenHands run
              ▼                              ▼
      ┌──────────────────┐         ┌──────────────────────┐
      │  pages.yml       │         │  openhands.yml       │
      │  ─ mkdocs build  │         │  ─ read context      │
      │  ─ upload Pages  │         │  ─ execute one task  │
      │    artifact      │         │  ─ commit & push     │
      └────────┬─────────┘         └──────────┬───────────┘
               │                              │
               ▼                              │
       GitHub Pages                           │
       (public site)                          │
                                              │
       new commit on main  ◄──────────────────┘
```

## Layers

### 1. Content

Plain Markdown. Authoring requires no special tooling.

| Path          | Purpose                                                            |
| ------------- | ------------------------------------------------------------------ |
| `docs/`       | Articles, guides, reference, the things you read on the site.      |
| `projects/`   | Real, runnable projects. Each one is a self-contained unit.        |
| `snippets/`   | Small, focused, runnable code snippets.                            |
| `blog/`       | Longer write-ups, announcements, post-mortems.                     |
| `memory/`     | Long-term context for agents (mission, rules, decisions).         |
| `tasks/`      | Work pipeline (queue + completed).                                 |
| `reports/`    | Time-stamped execution reports.                                    |

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
  deploys it to **GitHub Pages** using the official Pages actions.

### 4. Automation

- `wikicode-agent.yml` is the autonomous agent workflow. It installs
  Ollama, pulls the Qwen2.5 model, and runs `scripts/agent.py` to
  read `memory/`, pick a task from `tasks/queue.md`, research the
  topic, generate content, validate with `mkdocs build`, and push.

## Secrets

| Secret              | Purpose                                            | Source                |
| ------------------- | -------------------------------------------------- | --------------------- |
| `GITHUB_TOKEN`      | Repository access inside workflows.                | Built-in.             |


No credentials are stored in the repository.
