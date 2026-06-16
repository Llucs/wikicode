---
title: Rules
description: Permanent operational rules.
created: 2026-06-03
---

# Rules

Permanent operational rules. These are normative and override any
ad-hoc instructions that conflict with them.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Created: 2026-06-03</span>
<span class="wikicode-meta-updated">Last updated: auto (git)</span>
</div>

## Content

1. Build real content only. No placeholders, no fake integrations,
   no simulated data, no demo-only branches.
2. Never invent completed work. If something is not done, it is not
   in `tasks/completed.md`.
3. Never fabricate results. No fake benchmarks, screenshots or
   metrics.
4. Prefer improving existing content over expanding scope.

## Safety

5. Never expose secrets, tokens, keys or personal data.
6. Use GitHub Secrets for credentials. Never commit `.env` files.
7. Never delete content. Archive it first (move to an `archive/`
   folder inside the relevant section) and reference the move in a
   report.

## Process

8. One meaningful task per execution. Do not bundle unrelated
   changes.
9. Generate a report in `reports/` after every execution, even if
   the task was small.
10. Keep documentation synchronized with the code or content it
    describes.
11. Preserve structure consistency. New sections follow the same
    layout as existing ones.
12. Record architectural decisions in `memory/decisions.md`.

## Quality

13. Code snippets must be runnable or at least syntactically valid.
14. Projects must include a `README.md` and an `index.md` for the
    site.
15. Markdown must render cleanly. The CI runs `mkdocs build --clean`
    on every push; a broken build blocks deployment.

## Content integrity

16. **Never duplicate content.** Before adding a new page, project,
    snippet, tool or blog post, verify the topic is not already
    covered. Read the section's `index.md`, run `git grep` over the
    section for the planned slug or key terms, and cross-check the
    knowledge ledger. If a duplicate is found, improve the existing
    page instead of writing a new one.

## Tool documentation

17. **Document tools, not just concepts.** When researching a new
    tool, use web research to gather information from official
    docs and reputable sources, then record a summary under
    `docs/tools/<slug>/`.

## Execution scope

18. **Keep the daily loop healthy.** When triggered by the daily
    schedule, pick a small, scoped task and ship it. Large,
    multi-day refactors belong in dedicated tasks with their own
    reports.
