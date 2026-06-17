---
title: Navigation Audit for WikiCode
description: Analysis and proposed improvements to the WikiCode site navigation.
created: 2026-06-14
tags:
  - meta
  - guide
status: draft
---

# Navigation Audit

## Current structure

The main navigation is defined in `mkdocs.yml` and currently includes:

- Home
- Search
- Getting started
- Learning paths
- Guides
- Reference (Glossary, Architecture, Changelog)
- Topics
- Tools
- Tags
- Blog
- Projects
- Snippets
- Reports

## Proposed improvements

1. **Group meta sections** under a single "About" or "WikiCode" menu item (Reports, Changelog, Architecture)
2. **Move Tags inside Topics** since they are related concepts
3. **Add visual indicators** for recently updated content
4. **Ensure breadcrumbs** are active on all navigation levels

## Implementation

All changes should be made to the `nav:` block in `mkdocs.yml`.
