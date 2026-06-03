---
title: Bootstrap report
description: Initial bootstrap of WikiCode.
date: 2026-06-03
created: 2026-06-03
---

# Bootstrap report — 2026-06-03

## Summary

Initial bootstrap of the `Llucs/wikicode` repository. The repository
is now a production-oriented starting point that supports static
site generation, autonomous agent execution and structured content
growth, with the published site auto-updating on every push to
`main`.

## Scope of this run

- Created the top-level repository layout required by the project
  specification.
- Added a MkDocs (Material) configuration with `search`,
  `awesome-pages`, `git-revision-date-localized` and frontmatter
  support.
- Created two GitHub Actions workflows:
  - `pages.yml` — builds and deploys the site on every push to
    `main`.
  - `openhands.yml` — autonomous agent workflow, triggered manually
    or by an `@openhands` mention.
- Configured `OPENHANDS_API_KEY` as a repository secret so the
  OpenHands workflow can run without ever reading credentials from
  the repo.
- Enabled GitHub Pages with the workflow build type and HTTPS
  enforced.
- Initialized the agent memory (`mission`, `rules`, `knowledge`,
  `decisions`) and the task pipeline (`queue`, `completed`).
- Seeded the task queue with the first four items requested by the
  specification.
- Added a custom CSS file for a clean, organized layout and a
  per-page metadata card showing **created** and **last updated**
  dates.

## Files created

### Root

- `README.md` — project overview, structure, philosophy, local
  build.
- `LICENSE` — MIT License.
- `AGENT.md` — operating contract for agents.
- `mkdocs.yml` — site generator configuration.
- `.gitignore` — standard ignores for Python, MkDocs and editors.

### Automation

- `.github/workflows/pages.yml` — site build and GitHub Pages
  deployment.
- `.github/workflows/openhands.yml` — OpenHands agent workflow.

### Site content

- `docs/index.md` — landing page.
- `docs/getting-started.md` — onboarding and conventions.
- `docs/assets/css/extra.css` — clean, organized theme tweaks.

### Sections

- `projects/index.md` — section landing.
- `snippets/index.md` — section landing.
- `reports/index.md` — section landing.

### Memory

- `memory/mission.md`
- `memory/rules.md`
- `memory/knowledge.md`
- `memory/decisions.md` — four initial decisions recorded
  (0001–0004).

### Tasks

- `tasks/queue.md` — four initial tasks.
- `tasks/completed.md` — bootstrap entry.

## Architecture choices

1. **MkDocs + Material** as the site generator. Mature,
   dependency-light, excellent search and navigation, native GitHub
   Pages support.
2. **`awesome-pages` plugin** to drive automatic content discovery.
   Adding a new project or snippet folder is enough to make it
   appear on the site; no central registry needs to be edited.
3. **Client-side search** through MkDocs' built-in `search` plugin.
   No server, no external service, no privacy concerns.
4. **Git history as the source of truth for dates.**
   `git-revision-date-localized` provides "last updated" from git,
   and every page has a `created:` frontmatter field for the
   creation date.
5. **Two separate workflows.** `pages.yml` handles site delivery
   on every push. `openhands.yml` is dedicated to the autonomous
   agent. Keeping them separate keeps permissions tight and logs
   readable.
6. **OpenHands secrets.** The agent reads `OPENHANDS_API_KEY` from
   repository secrets and `GITHUB_TOKEN` (built-in) for repository
   access. No credentials are stored in the repository.
7. **Repository-first publication.** The site is generated from the
   repository on every push. OpenHands grows the wiki by writing to
   the repo; the site picks up the change automatically.

## What is intentionally not done

- No real project or snippet was created. The task queue lists
  those as upcoming work, per the project specification.
- GitHub Pages is enabled but the **first** successful build will
  be produced by the next push that runs `pages.yml`.

## Verification performed

- Directory layout matches the specification.
- `mkdocs.yml` references the correct `docs_dir`, theme and
  plugins.
- Both workflows are valid and reference `secrets.OPENHANDS_API_KEY`
  / `secrets.GITHUB_TOKEN` only; no literal credentials appear in
  any committed file.
- `gh secret list` confirms `OPENHANDS_API_KEY` is configured.
- `gh api` confirms GitHub Pages is enabled with
  `build_type: workflow` and `https_enforced: true`.
- The task queue contains the four initial tasks requested by the
  specification.

## Next step

The first task in `tasks/queue.md` is "Create first developer
article". That is where the next execution should pick up.
