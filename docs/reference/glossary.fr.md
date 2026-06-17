---
title: Glossaire
description: Terminologie utilisée dans WikiCode.
created: 2026-06-03
tags:
  - reference
  - meta
status: stable
---

# Glossaire

Terminologie canonique utilisée dans WikiCode. Les définitions sont brèves
et renvoient vers la source faisant autorité lorsque c'est utile.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Créé : 2026-06-03</span>
<span class="wikicode-meta-updated">Dernière mise à jour : auto (git)</span>
</div>

## Concepts de base

<dl markdown>
<dt markdown>**WikiCode**</dt>
<dd markdown>Le dépôt et le site statique qu'il produit. « WikiCode »
désigne les deux, selon le contexte.</dd>

<dt markdown>**Article**</dt>
<dd markdown>Une page Markdown détaillée sous `docs/`. Les articles sont
destinés à être lus en intégralité.</dd>

<dt markdown>**Project**</dt>
<dd markdown>Un logiciel autonome et exécutable sous `projects/`.
Chaque projet a son propre `README.md`, `index.md` et
arborescence source.</dd>

<dt markdown>**Snippet**</dt>
<dd markdown>Une unité de code petite, ciblée et exécutable sous
`snippets/`. Les snippets sont destinés à être copiés et adaptés.</dd>

<dt markdown>**Report**</dt>
<dd markdown>Un fichier Markdown horodaté sous `reports/` qui
décrit une seule exécution. Format :
`YYYY-MM-DD-<slug>.md`.</dd>

<dt markdown>**Decision**</dt>
<dd markdown>Un choix architectural ou opérationnel enregistré dans
`memory/decisions.md` avec un numéro à quatre chiffres et un statut.</dd>

<dt markdown>**Agent**</dt>
<dd markdown>Tout processus — humain ou autonome — qui suit
`AGENT.md` lorsqu'il travaille sur le dépôt.</dd>

<dt markdown>**Task**</dt>
<dd markdown>Une unité de travail unique listée dans `tasks/queue.md`.
Une tâche par exécution.</dd>
</dl>

## Termes de workflow

<dl markdown>
<dt markdown>**Push to `main`**</dt>
<dd markdown>Déclenche `pages.yml`, qui reconstruit et déploie le site.
Toute modification du site publié s'effectue via ce mécanisme.</dd>

<dt markdown>**Agent run**</dt>
<dd markdown>Une exécution déclenchée de `.github/workflows/wikicode-agent.yml`,
soit via `workflow_dispatch`, soit par une mention `@agent` dans un
issue, soit par un issue étiqueté `agent`.</dd>

<dt markdown>**Frontmatter**</dt>
<dd markdown>Métadonnées YAML en haut d'un fichier Markdown, délimitées
par `---`. WikiCode attend au moins `title`, `description` et
`created`.</dd>

<dt markdown>**Tag**</dt>
<dd markdown>Une étiquette déclarée dans le frontmatter qui regroupe les pages
connexes. Material génère automatiquement des pages d'index par tag.</dd>
</dl>

## Valeurs de statut

Les pages et les projets peuvent déclarer un `status` dans leur frontmatter :

| Statut        | Signification                                                     |
| ------------- | ----------------------------------------------------------------- |
| `draft`       | Travail en cours ; peut être incomplet ou erroné.                 |
| `stable`      | Révisé et considéré comme correct. Peut encore évoluer.           |
| `archived`    | Conservé pour référence ; n'est plus maintenu.                    |
| `deprecated`  | Remplacé par autre chose ; conservé pour contexte historique.     |

`status: stable` est l'attente par défaut pour tout contenu publié.