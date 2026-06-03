# Changelog

Notable changes to WikiCode. Smaller, day-to-day edits are tracked
in git history; only structural and user-visible changes appear
here.

The full changelog is also rendered on the site at
[Reference → Changelog](https://llucs.github.io/wikicode/reference/changelog/).

## 1.0.0 — 2026-06-03 — Bootstrap

Initial production-oriented structure. See
[reports/2026-06-03-bootstrap.md](reports/2026-06-03-bootstrap.md)
for the full bootstrap report.

### Added

- MkDocs (Material) site generation with `search`, `awesome-pages`,
  `git-revision-date-localized` and `blog` plugins.
- `pages.yml` workflow: build + deploy on every push to `main`.
- `openhands.yml` workflow: autonomous agent, secret-based.
- GitHub Pages enabled with workflow build type and HTTPS enforced.
- Content sections: `docs/`, `projects/`, `snippets/`, `blog/`,
  `memory/`, `tasks/`, `reports/`.
- Top-level guides: glossary, architecture, changelog, learning
  paths.
- Tag system, frontmatter contract, per-page date card.
- `OPENHANDS_API_KEY` configured as a repository secret.
- Initial decisions 0001–0004 recorded.
- Initial task queue with four items.
