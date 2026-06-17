---
title: Journal des modifications
description: Modifications notables de WikiCode.
created: 2026-06-03
tags:
  - reference
  - meta
status: stable
---

# Journal des modifications

Modifications notables de WikiCode. Les modifications plus petites et quotidiennes sont suivies dans l'historique git ; seules les modifications structurelles et visibles par l'utilisateur apparaissent ici.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Créé : 2026-06-03</span>
<span class="wikicode-meta-updated">Dernière mise à jour : auto (git)</span>
</div>

## 1.0.0 — 2026-06-03 — Bootstrap

Structure initiale orientée production.

### Ajouté

- **Génération du site.** MkDocs (thème Material) avec recherche côté client, index de sections automatiques et une couche CSS propre et personnalisée.
- **Publication à partir du dépôt.** Le site est régénéré à partir du dépôt à chaque push sur `main` via `.github/workflows/pages.yml`. Rien dans le site publié n'est édité à la main.
- **Agent IA (API OpenCode).** `.github/workflows/wikicode-agent.yml` exécute l'agent autonome sur le runner CI. Génération de contenu via l'API OpenCode (`deepseek-v4-flash-free`), recherche web via les API Wikipedia et DuckDuckGo. Aucune clé API externe nécessaire.
- **GitHub Pages.** Activé avec le type de build du workflow et HTTPS imposé.
- **Sections de contenu.**
  - `docs/` pour les articles, guides et pages de référence.
  - `projects/` pour les projets autonomes et exécutables.
  - `snippets/` pour des extraits de code ciblés.
  - `blog/` pour des articles plus longs et des annonces.
  - `memory/` pour le contexte à long terme de l'agent (mission, règles, connaissances, décisions).
  - `tasks/` pour le pipeline de travail.
  - `reports/` pour les rapports d'exécution horodatés.
- **Métadonnées de date.** Chaque page affiche une carte avec sa date de **création** (depuis le frontmatter) et sa date de **dernière mise à jour** (depuis l'historique git, via `mkdocs-git-revision-date-localized-plugin`).
- **Système de tags.** Les pages peuvent déclarer des tags dans le frontmatter ; le thème Material rend automatiquement les pages d'index par tag.
- **Guides de premier niveau.**
  - [Glossaire](glossary.md)
  - [Architecture](architecture.md)
  - [Journal des modifications](changelog.md) (cette page)
  - [Parcours d'apprentissage](../learning-paths.md)
- **Fichiers racine.** `README.md`, `LICENSE`, `AGENT.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `ARCHITECTURE.md`, `.gitignore`.
- **Décisions initiales.** Quatre entrées numérotées dans `memory/decisions.md` (0001–0004).
- **Tâches initiales.** Quatre éléments en file d'attente dans `tasks/queue.md`.

### Notes

- Le site est en ligne à l'URL fournie par GitHub Pages une fois que la première exécution de `pages.yml` est terminée avec succès.
- Aucune clé API externe n'est requise. L'agent utilise `GITHUB_TOKEN` (intégré) pour l'accès au dépôt et l'API OpenCode pour la génération de contenu.