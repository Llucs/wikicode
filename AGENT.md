# AGENT.md

Operating contract for any agent (human or autonomous) working on
WikiCode.

## Rules

The normative rules are defined in
[memory/rules.md](memory/rules.md) — the single source of truth.
AGENT.md does not duplicate them. Read `memory/rules.md` before
acting.

## Workflow

1. Read `memory/mission.md`, `memory/rules.md` and
   `memory/knowledge.md` before acting.
2. Consult `memory/decisions.md` to avoid contradicting past choices.
3. **Anti-duplication check.** For the planned topic, read the
   relevant section's `index.md`, search with `git grep` and
   cross-check the knowledge ledger. Confirm the topic is not
   already covered.
4. Pick the next task from `tasks/queue.md`. If the queue is empty,
   propose a new task instead of inventing work silently.
5. Execute exactly one task. Do not bundle unrelated changes.
6. Update `docs/`, `projects/`, `snippets/`, `docs/tools/` or
   `blog/` as required. Add frontmatter and tags.
7. Write a report in `reports/` after every execution.
8. Move the task to `tasks/completed.md` with the report reference.
9. Record any architectural decision in `memory/decisions.md`.
10. Commit with a clear, scoped message and push to `main`. The
    site rebuilds automatically through
    `.github/workflows/pages.yml`.

## Limits

- Do not modify the LICENSE.
- Do not rewrite history on the default branch.
- Do not run destructive automation (force push, mass delete,
  etc.).
- Do not store secrets in the repository.
- No external API keys are required. The agent uses the OpenCode API
  (free public key) and web research via Wikipedia / DuckDuckGo.

## Triggers

- `workflow_dispatch` — manual run from the Actions tab.
- `schedule` — twice daily at 06:00 and 18:00 UTC, the "grow a
  little every day" run.
- `push` to `main` — runs after every merge to keep the wiki
  evolving.
- `issue_comment` with `@agent` mention.
- `issues` labeled `agent`.
