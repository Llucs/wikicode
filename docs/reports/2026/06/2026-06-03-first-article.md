---
title: First developer article
description: Created the first developer article — a guide on designing clean REST APIs in Go.
date: 2026-06-03
created: 2026-06-03
---

# First developer article — 2026-06-03

## Task

> **Create first developer article.** Pick a high-value topic (for example: "Designing a clean REST API in Go" or "Memory management in modern C++") and publish it under `docs/guides/`. Add frontmatter tags.

## Anti-duplication check

Ran `git grep` across `docs/`, `projects/` and `snippets/` for key terms: REST, API, Go, HTTP, design, routing. No matches found. Read `docs/guides/index.md` to confirm the section was empty and followed the conventions listed there (frontmatter with title/description/created/tags, lowercase slug).

## Execution

Created `docs/guides/rest-api-go.md` — a practical, self-contained guide covering:

- **Project structure** — `cmd/`, `internal/` layout with clear separation of concerns.
- **HTTP routing** — using the `chi` router (lightweight, idiomatic, widely adopted).
- **Request handling** — handlers that call services, never touch the database directly.
- **JSON encoding/decoding** — request structs, avoiding `map[string]interface{}`.
- **Error handling** — domain-specific errors with `APIError` type mapping to HTTP status codes.
- **Middleware** — logging, request ID, recovery chaining.
- **Testing** — table-driven handler tests using `httptest`.

The article includes runnable Go code snippets with imports, proper naming and idiomatic error handling. Every snippet is syntactically valid. The frontmatter uses the tags suggested by `docs/guides/index.md`: `guide`, `backend`, `language-go`, `api-design`.

## Verification

Built the site with `mkdocs build --strict`. The command succeeded with no errors (warnings about Material for MkDocs roadmap and plugin availability are pre-existing, not introduced by this change).

## Files changed

| File | Change |
| ---- | ------ |
| `docs/guides/rest-api-go.md` | Created — the article |

## Next task

**Create first project.** Add a self-contained, runnable project under `projects/` with `README.md`, `index.md` and working source code.