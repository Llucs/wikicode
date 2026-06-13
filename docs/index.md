---
title: WikiCode
description: A living developer wiki — articles, projects and snippets maintained over time.
created: 2026-06-03
tags:
  - meta
  - overview
status: stable
---

# WikiCode

A living developer wiki built and maintained over time. Every page
you read here is generated directly from the repository, so the site
is always a faithful mirror of the source of truth.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Created: 2026-06-03</span>
<span class="wikicode-meta-updated">Last updated: auto (git)</span>
</div>

## What you will find

<div class="grid cards" markdown>

- :material-book-open-page-variant-outline: __Articles & guides__

    Long-form explanations of concepts, patterns and tools. See
    [Guides](guides/index.md).

- :material-folder-outline: __Projects__

    Self-contained, runnable projects. See [Projects](projects/index.md).

- :material-code-tags: __Snippets__

    Small, focused, copy-paste-ready code snippets. See
    [Snippets](snippets/index.md).

- :material-school-outline: __Learning paths__

    Curated reading orders for newcomers. See
    [Learning paths](learning-paths.md).

- :material-tag-multiple-outline: __Topics & tags__

    Browse content by topic or by tag. See
    [Topics](topics/index.md) and [Tags](tags.md).

- :material-clipboard-text-outline: __Reports__

    Time-stamped execution reports. See [Reports](reports/index.md).

- :material-rss: __Blog__

    Announcements and longer write-ups. See [Blog](blog/index.md).

- :material-bookshelf: __Reference__

    Glossary, architecture and changelog. See
    [Reference](reference/glossary.md).

</div>

## How updates flow

The site is **never edited directly**. It is regenerated from the
repository on every push to `main`:

```
Local AI agent (Ollama + Qwen2.5) / contributor
        │
        ▼
   commit + push to main
        │
        ▼
   .github/workflows/pages.yml
        │
        ▼
   mkdocs build (from docs/, projects/, snippets/, blog/)
        │
        ▼
   GitHub Pages (public site)
```

When the local AI agent (or any contributor) updates a Markdown file,
adds a project folder, writes a snippet, publishes a blog post or
moves a task from `queue.md` to `completed.md`, the next push to
`main` triggers a fresh build and the published site reflects the
change.

## Where to start

- [Getting started](getting-started.md) — repository layout, local
  build, conventions.
- [Learning paths](learning-paths.md) — guided reading orders.
- [Reference](reference/glossary.md) — terminology and architecture.
