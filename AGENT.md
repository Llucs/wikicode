# AGENT.md

Operating contract for any agent (human or autonomous) working on
WikiCode. This file is normative: rules defined here must be
followed.

## Mission

Build and maintain WikiCode as a living, high-quality developer
wiki that grows a little every day.

## Rules

1. Build real content only.
2. Never invent completed work.
3. Never fabricate results or metrics.
4. Never expose secrets, tokens or credentials.
5. Never delete content without archiving it first.
6. Prefer improving existing content over expanding scope.
7. Generate a report in `reports/` after every execution.
8. Keep documentation synchronized with the code that describes it.
9. Take one meaningful task per execution.
10. Preserve structure consistency across the repository.
11. **Never duplicate content.** Before adding a new page, project,
    snippet, tool or blog post, verify that the topic is not
    already covered. Read the section's `index.md`, run
    `git grep` over the section for the planned slug or key
    terms, and cross-check the knowledge ledger. If a duplicate
    is found, improve the existing page instead of writing a new
    one.
12. **Document tools, not just concepts.** When researching a new
    tool, use web research to gather information from official
    docs and reputable sources, then record a summary under
    `docs/tools/<slug>/`.
13. **Keep the daily loop healthy.** When triggered by the daily
    schedule, pick a small, scoped task and ship it. Large,
    multi-day refactors belong in dedicated tasks with their own
    reports.

## Workflow

1. Read `memory/mission.md`, `memory/rules.md` and
   `memory/knowledge.md` before acting.
2. Consult `memory/decisions.md` to avoid contradicting past
   choices.
3. **Anti-duplication check.** For the planned topic, read the
   relevant section's `index.md`, search with `git grep` and
   cross-check the knowledge ledger. Confirm the topic is not
   already covered.
4. Pick the next task from `tasks/queue.md`. If the queue is
   empty, propose a new task instead of inventing work silently.
5. Execute exactly one task. Do not bundle unrelated changes.
6. Update `docs/`, `projects/`, `snippets/`, `docs/tools/` or
   `blog/` as required. Add frontmatter and tags.
7. Write a report in `reports/YYYY-MM-DD-<slug>.md`.
8. Move the task to `tasks/completed.md` with the report
   reference.
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
- No external API keys are required. The agent uses the OpenCode
  API with a public key for content generation.

## Triggers

- `workflow_dispatch` — manual run from the Actions tab.
- `schedule` — twice daily at 06:00 and 18:00 UTC, the "grow a
  little every day" run.
- `push` to `main` — runs after every merge to keep the wiki
  evolving.
- `issue_comment` with `@agent` mention.
- `issues` labeled `agent`.
