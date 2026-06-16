---
title: Quality Criteria
description: Quality standards and validation rules for WikiCode content.
created: 2026-06-15
---
# Quality Criteria

Quality standards that all content must meet.

## Required frontmatter
- `title` — descriptive title
- `description` — one-sentence summary
- `created` — ISO date
- `tags` — at least one category tag
- `status` — draft, stable, archived, or deprecated

## Tools
- Must include `ecosystem` field
- Must include installation instructions
- Must include at least one usage example

## Analyses
- Must cover architecture or design rationale
- Must compare with at least one alternative

## Pages
- No broken internal links
- No orphan pages (every page reachable via nav or index)
- `mkdocs build --clean` must pass
