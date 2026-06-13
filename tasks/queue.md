---
title: Tasks queue
description: Pending work for WikiCode.
created: 2026-06-03
tags:
  - meta
  - process
status: stable
---

# Tasks — Queue

Pending work. An agent should pick the **first** task, execute it
following `AGENT.md`, write a report in `reports/`, then move the
task to `tasks/completed.md` with a reference to the report.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Created: 2026-06-03</span>
<span class="wikicode-meta-updated">Last updated: auto (git)</span>
</div>

## How the queue is consumed

The wikicode-agent workflow consumes the queue through the
following triggers:

| Trigger              | When                                                  | Use case                                  |
| -------------------- | ----------------------------------------------------- | ----------------------------------------- |
| `schedule`           | Daily at 12:00 UTC.                                   | Default "grow a little every day" run.    |
| `workflow_dispatch`  | Manually from the Actions tab.                        | On-demand run, useful for unblocking.     |
| `issue_comment`      | When someone writes `@agent` on an issue.             | Turn an issue into a contribution.        |
| `issues` with label  | When an issue is labeled `agent`.                     | Operator-curated batch runs.              |

Only **one** task is executed per run, no matter the trigger.

## Pending tasks

- [ ] **Create a real-world REST API project in Go.** Build a complete,
      self-contained REST API in Go under `projects/go-rest-api/`. It
      must include a `README.md`, `index.md`, working source code with
      handlers, models, tests, and a Makefile. Use the `net/http` standard
      library or a lightweight router like `chi`. Document the architecture,
      endpoints, and how to run it with `go run`.

- [ ] **Add a first snippet.** Add a focused, runnable snippet
      under `snippets/`. It should be short enough to be read in
      under a minute and copy-paste-ready.

- [ ] **Document first tool.** Pick a developer tool that is
      **not yet covered** under `docs/tools/`. Use web research
      to gather information from the official docs, then write a
      `docs/tools/<slug>/index.md` summary and, if there is
      enough material, `install.md` and `usage.md`.

- [ ] **Document second tool.** Same as above, for a different
      tool. Pick from a different category (e.g. CLI vs. build
      tool vs. runtime) to broaden coverage.

- [ ] **Improve navigation.** Audit the site and ensure the top
      navigation, side navigation and section indexes make sense.
      Add cross-links between related pages.

- [ ] **Expand documentation.** Flesh out `docs/guides/` with a
      small set of foundational guides (architecture overview,
      contribution workflow, glossary). Update `mkdocs.yml`
      accordingly.

## How to add a task

Append a new entry using the existing format:

```markdown
- [ ] **Short title.** One-paragraph description of what "done"
      looks like, including which directories will change.
```

Tasks should be specific, scoped and verifiable. New tasks must
pass the anti-duplication check in `AGENT.md` and
`memory/knowledge.md`.
