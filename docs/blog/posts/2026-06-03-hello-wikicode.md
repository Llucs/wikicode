---
title: "Hello, WikiCode"
date: 2026-06-03
authors:
  - llucs
categories:
  - announcements
tags:
  - meta
  - announcement
---

# Hello, WikiCode

WikiCode is a living developer wiki. It is built from the
repository and published automatically on every push to `main`.

## What you can do here

- Read articles and guides under `docs/`.
- Browse self-contained, runnable projects under `projects/`.
- Copy small, focused snippets under `snippets/`.
- Track what changed and why in `reports/`.

## How it stays up to date

There is no CMS and no separate database. The site is generated
from the repository by MkDocs and deployed by GitHub Pages.
Autonomous agents (Ollama + Qwen2.5 today) grow the wiki
by writing to the repository.

## What is next

The first task in [tasks/queue.md](https://github.com/Llucs/wikicode/blob/main/tasks/queue.md)
is to publish the first developer article. Watch this space.
