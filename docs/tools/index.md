---
title: Tools
description: Developer tools documented in WikiCode.
created: 2026-06-03
tags:
  - meta
  - tools
status: stable
---

# Tools

Developer tools documented in WikiCode. Each tool has its own folder
under `docs/tools/<slug>/` with an `index.md` summary.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Created: 2026-06-03</span>
<span class="wikicode-meta-updated">Last updated: auto (git)</span>
</div>

## By ecosystem

Tools are classified by ecosystem. See the tag index for the full list.

| Ecosystem | Tools |
|-----------|-------|
| Container | Docker, Podman, Portainer |
| CI/CD     | Jenkins, ArgoCD |
| API       | Postman, cURL |
| JavaScript| npm, Jest |
| Editor    | Visual Studio Code |
| CLI       | fzf |
| Android   | SpeedCool |
| Monitoring| Grafana, Heimdall |
| VCS       | Git |

## How tools are added

Both the AI agent and human contributors follow the same recipe:

1. Research the tool using web search (Wikipedia + DuckDuckGo).
2. Write a `docs/tools/<slug>/index.md` summary.
3. Add frontmatter with `title`, `description`, `created`, `tags`,
   and `ecosystem`.
4. Run `mkdocs build --clean` to validate.

## Current tools

<!--awesome-pages:hide-->
<!--awesome-pages:reveal-->

## Conventions

- One folder per tool. Folder name: lowercase, hyphenated.
- `index.md` is the public summary.
- Frontmatter must include `title`, `description`, `created`,
  `tags`, `ecosystem`, and `status`.
- A tool page should include: one-paragraph "what it is",
  installation, basic usage, and key features with examples.
