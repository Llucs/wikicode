---
title: WikiCode
description: Un wiki de développeur vivant — articles, projets et snippets maintenus au fil du temps.
created: 2026-06-03
tags:
  - meta
  - overview
status: stable
---

# WikiCode

Un wiki de développeur vivant construit et maintenu au fil du temps. Chaque page
que vous lisez ici est générée directement depuis le dépôt, de sorte que le site
est toujours un miroir fidèle de la source de vérité.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Créé : 2026-06-03</span>
<span class="wikicode-meta-updated">Dernière mise à jour : auto (git)</span>
</div>

## Ce que vous trouverez

<div class="grid cards" markdown>

- :material-book-open-page-variant-outline: __Articles et guides__

    Explications détaillées des concepts, modèles et outils. Voir
    [Guides](guides/index.md).

- :material-folder-outline: __Projets__

    Projets autonomes et exécutables. Voir [Projets](projects/index.md).

- :material-code-tags: __Snippets__

    Petits snippets de code ciblés, prêts à copier-coller. Voir
    [Snippets](snippets/index.md).

- :material-school-outline: __Parcours d'apprentissage__

    Parcours de lecture organisés pour les nouveaux arrivants. Voir
    [Parcours d'apprentissage](learning-paths.md).

- :material-tag-multiple-outline: __Sujets et tags__

    Parcourez le contenu par sujet ou par tag. Voir
    [Sujets](topics/index.md) et [Tags](tags.md).

- :material-clipboard-text-outline: __Rapports__

    Rapports d'exécution horodatés. Voir [Rapports](reports/index.md).

- :material-rss: __Blog__

    Annonces et articles plus longs. Voir [Blog](blog/index.md).

- :material-bookshelf: __Référence__

    Glossaire, architecture et changelog. Voir
    [Référence](reference/glossary.md).

</div>

## Comment les mises à jour circulent

Le site n'est **jamais édité directement**. Il est régénéré à partir du dépôt
à chaque push sur `main` :

```
Autonomous AI agent (OpenCode API) / contributor
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

Lorsque l'agent AI local (ou tout contributeur) met à jour un fichier Markdown,
ajoute un dossier de projet, écrit un snippet, publie un article de blog ou
déplace une tâche de `queue.md` vers `completed.md`, le prochain push sur
`main` déclenche une reconstruction et le site publié reflète le changement.

## Par où commencer

- [Pour commencer](getting-started.md) — disposition du dépôt, construction locale,
  conventions.
- [Parcours d'apprentissage](learning-paths.md) — parcours de lecture guidés.
- [Référence](reference/glossary.md) — terminologie et architecture.