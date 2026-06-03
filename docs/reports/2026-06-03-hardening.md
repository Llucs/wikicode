---
title: Hardening report
description: End-to-end CI hardening of WikiCode.
date: 2026-06-03
created: 2026-06-03
tags:
  - report
status: stable
---

# Hardening report — 2026-06-03

## Summary

After the initial bootstrap, the OpenHands workflow's strict MkDocs
build was failing on a handful of configuration warnings, and the
`git-committers` plugin was missing from the install step. This
report covers the fixes that brought both `pages.yml` and
`openhands.yml` to a clean, fully passing state.

## Issues found and fixed

1. **`git-committers` plugin not installed.**
   `pages.yml` failed with
   `Config value 'plugins': The "git-committers" plugin is not
   installed`. Fixed by adding it to `requirements.txt` and
   installing the full requirements file in both workflows.

2. **Wrong version constraint for `git-committers`.**
   `mkdocs-git-committers-plugin>=1.1` had no matching
   distribution (latest is 0.2.3). Pinned to `>=0.2`.

3. **Python caching needed a manifest.**
   `actions/setup-python` cache only works when a
   `requirements.txt` or `pyproject.toml` exists at the repo
   root. Added `requirements.txt` and switched the install step
   to `pip install -r requirements.txt`.

4. **Material 9.4+ deprecation banner about MkDocs 2.0.**
   The banner is informational but flagged as a build warning.
   Pinned `mkdocs-material>=9.3,<9.4` so the banner does not
   appear.

5. **`pymdownx.emoji` not available in Material 9.3.**
   The `material.extensions.emoji` module is not present in
   Material 9.3.x. Removed the `pymdownx.emoji` block from
   `mkdocs.yml` (emoji rendering is a nice-to-have, not a
   requirement).

6. **Blog plugin: unsupported `tags` option.**
   The blog plugin in Material 9.3 does not recognize `tags` as
   a configuration name. Removed it. (Per-page tags already work
   via the Material theme's `tags` extension without an explicit
   blog option.)

7. **`nav` references to non-existent files.**
   `nav` listed `docs/tools/index.md`, `projects/index.md`,
   `snippets/index.md`, `reports/index.md`. With `docs_dir: docs`,
   the correct references are `tools/index.md`, etc. Fixed the
   nav block.

8. **Cross-folder links in `learning-paths.md` and
   `getting-started.md`.**
   Several links pointed to files that live outside `docs/`
   (`../memory/...`, `../tasks/...`, `../AGENT.md`,
   `../CONTRIBUTING.md`). Replaced those with GitHub URLs that
   resolve to the canonical file in the repository.

9. **Relative path resolution in
   `docs/reference/architecture.md`.**
   Links to `tags.md` and `topics/index.md` were relative to the
   file's own folder (`docs/reference/`). Updated to `../tags.md`
   and `../topics/index.md`.

10. **Embedded git repos in the workspace.**
    The bootstrap workspace contained unrelated git repositories
    (`brokkr/`, `heimdall/`, `prootkit/`, `thor/`) that were
    accidentally staged by `git add -A`. Removed them from the
    index, added them to `.gitignore`, and amended the commit
    with `--force-with-lease`.

## Final state

| Workflow            | Result   | Notes                                                          |
| ------------------- | -------- | -------------------------------------------------------------- |
| `pages.yml`         | success  | Build and deploy pass cleanly.                                 |
| `openhands.yml`     | success  | All 8 steps pass, including `mkdocs build --strict --clean`.   |
| GitHub Pages        | enabled  | `build_type: workflow`, `https_enforced: true`.                |
| `OPENHANDS_API_KEY` | set      | Configured as a repository secret.                             |
| Site                | live     | https://llucs.github.io/wikicode/                              |

The only remaining annotations on the workflows are platform-level
notices from GitHub about the `actions/checkout@v4` and
`actions/setup-python@v5` actions targeting Node.js 20. They are
forced onto Node.js 24 through the workflow `env`, and the message
is informational only. There are no errors, no warnings about
WikiCode's own code or configuration, and no deprecation banners
from the documentation stack.
