# Contributing to WikiCode

Thank you for your interest in WikiCode. This file explains how
contributions — human or autonomous — flow through the project.

## Ground rules

1. **Real content only.** No placeholders, no fake integrations, no
   demo-only data. See `memory/rules.md` for the full rule set.
2. **One meaningful change per contribution.** Do not bundle
   unrelated edits in a single commit.
3. **Document decisions.** Architectural or workflow changes are
   recorded in `memory/decisions.md` with a four-digit number and a
   status (`proposed`, `accepted`, `rejected`, `superseded`).
4. **Generate reports.** Every execution writes a time-stamped
   report in `reports/YYYY-MM-DD-<slug>.md`.
5. **Never commit secrets.** Use GitHub Secrets.

## How to add a new article

1. Create a Markdown file under `docs/`, `docs/guides/` or a
   topic-specific subfolder.
2. Add frontmatter:

   ```yaml
   ---
   title: Article title
   description: One-sentence summary.
   created: YYYY-MM-DD
   tags: [guide, backend]
   status: draft
   ---
   ```

3. Reference the page from `mkdocs.yml` if it is not picked up by
   `awesome-pages` (articles under `docs/` not under a section with
   an `index.md` need to be in the `nav` block).
4. Run `mkdocs build --clean` locally to catch broken links.
5. Open a pull request. A Pages preview is not configured yet, but
   the build will run on CI.

## How to add a new project

1. Create a folder under `projects/<slug>/`.
2. Add a `README.md` (developer-facing) and an `index.md`
   (site-facing).
3. Put the source code inside the project folder. The
   `awesome-pages` plugin will surface the project on the site
   automatically through `index.md`.

## How to add a new snippet

1. Create a folder under `snippets/<slug>/`.
2. Add the snippet file and a short `index.md` describing the
   problem, the approach and how to adapt the code.

## How to publish a blog post

1. Create a file under `blog/posts/YYYY-MM-DD-<slug>.md`.
2. Add frontmatter including `title`, `date`, `authors` and
   `categories`.
3. The blog plugin picks the post up automatically.

## How to record a decision

Append a new entry to `memory/decisions.md`:

```markdown
## NNNN — Short title

**Date:** YYYY-MM-DD
**Status:** proposed | accepted | rejected | superseded

**Context**
What was the situation?

**Decision**
What did we choose?

**Consequences**
What becomes easier, what becomes harder?
```

## Commit and review

- Commit messages should be imperative and scoped:
  `Add REST API article`, `Fix navigation in getting-started`,
  `Record decision 0005 on blog plugin`, etc.
- Push to a topic branch and open a pull request against `main`.
- The CI runs `mkdocs build --clean` on the PR.
- Once merged to `main`, `pages.yml` rebuilds and deploys the site.

## Reporting a problem

Open an issue with a clear, minimal reproduction. For agent-related
problems, include the relevant report from `reports/` and the
output of the wikicode-agent workflow run.
