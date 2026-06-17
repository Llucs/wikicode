---
title: Guides
description: Long-form, topic-oriented guides.
created: 2026-06-03
tags:
  - meta
status: stable
---

# Guides

Long-form guides grouped by topic. Each guide is a real Markdown
file under `docs/guides/` (or a subfolder).

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Created: 2026-06-03</span>
<span class="wikicode-meta-updated">Last updated: auto (git)</span>
</div>

## Conventions

- One folder or `.md` file per guide.
- Folder name: lowercase, hyphenated.
- Frontmatter should include `title`, `description`, `created` and
  `tags`.
- Tags help cross-linking: prefer reusing existing tags from
  [Tags](../tags.md) over inventing new ones.

## Suggested tags

| Tag             | Meaning                                                  |
| --------------- | -------------------------------------------------------- |
| `meta`          | Pages about WikiCode itself.                             |
| `guide`         | How-to content.                                          |
| `reference`     | Reference material (glossaries, lists).                  |
| `architecture`  | How the wiki is built and how it works.                  |
| `process`       | Workflow, contribution, governance.                     |
| `language-go`   | Content primarily about Go.                              |
| `language-py`   | Content primarily about Python.                          |
| `language-cpp`  | Content primarily about C++.                             |
| `language-rs`   | Content primarily about Rust.                            |
| `language-js`   | Content primarily about JavaScript / TypeScript.        |
| `backend`       | Backend engineering topics.                             |
| `frontend`      | Frontend engineering topics.                            |
| `devops`        | Build, deploy, observability.                            |
| `security`      | Security topics.                                         |
| `data`          | Databases, pipelines, analytics.                         |

Add tags to the frontmatter like this:

```yaml
---
title: My guide
tags:
  - guide
  - backend
---
```
