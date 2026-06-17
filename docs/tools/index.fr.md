---
title: Outils
description: Outils de développement documentés dans WikiCode.
created: 2026-06-03
tags:
  - meta
  - tools
status: stable
---

# Outils

Outils de développement documentés dans WikiCode. Chaque outil possède son propre dossier
sous `docs/tools/<slug>/` avec un résumé `index.md`.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Créé : 2026-06-03</span>
<span class="wikicode-meta-updated">Dernière mise à jour : auto (git)</span>
</div>

## Par écosystème

Les outils sont classés par écosystème. Voir l'index des étiquettes pour la liste complète.

| Écosystème | Outils |
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

## Comment les outils sont ajoutés

L'agent IA et les contributeurs humains suivent la même procédure :

1. Recherchez l'outil via une recherche web (Wikipedia + DuckDuckGo).
2. Rédigez un résumé `docs/tools/<slug>/index.md`.
3. Ajoutez un frontmatter avec `title`, `description`, `created`, `tags`,
   et `ecosystem`.
4. Exécutez `mkdocs build --clean` pour valider.

## Outils actuels

<!--awesome-pages:hide-->
<!--awesome-pages:reveal-->

## Conventions

- Un dossier par outil. Nom du dossier : minuscules, avec traits d'union.
- `index.md` est le résumé public.
- Le frontmatter doit inclure `title`, `description`, `created`,
  `tags`, `ecosystem`, et `status`.
- Une page d'outil doit inclure : un paragraphe « qu'est-ce que c'est »,
  l'installation, l'utilisation de base, et les fonctionnalités clés
  avec des exemples.