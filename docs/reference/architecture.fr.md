---
title: Architecture
description: Comment WikiCode est construit et comment il reste à jour.
created: 2026-06-03
tags:
  - reference
  - architecture
  - meta
status: stable
---

# Architecture

Comment WikiCode est construit, comment il reste à jour, et comment les
agents autonomes s'intègrent dans la boucle.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Créé : 2026-06-03</span>
<span class="wikicode-meta-updated">Dernière mise à jour : auto (git)</span>
</div>

## Diagramme de haut niveau

```
┌──────────────────────────────────────────────────────────────┐
│                       Repository                             │
│                                                              │
│   docs/        projects/    snippets/                        │
│   memory/      tasks/       reports/                         │
│   blog/        scripts/     mkdocs.yml                       │
│                                                              │
└─────────────┬──────────────────────────────┬────────────────┘
              │                              │
              │  push to main                │  Agent run
              │                              │  (manual, schedule,
              │                              │   @agent, label)
              ▼                              ▼
      ┌──────────────────┐         ┌──────────────────────┐
      │  pages.yml       │         │  wikicode-agent.yml  │
      │  ─ mkdocs build  │         │  ─ install deps      │
      │  ─ upload Pages  │         │  ─ read context      │
      │    artifact      │         │  ─ web research*     │
      └────────┬─────────┘         │  ─ generate content  │
               │                  │  ─ validate build    │
               │                  │  ─ commit & push     │
               │                  └──────────┬───────────┘
               │                             │
               ▼                             │
       GitHub Pages                          │
       (public site)                         │
                                             │
       new commit on main  ◄─────────────────┘
```

`*` L'agent utilise les API Wikipedia et DuckDuckGo pour la recherche web,
aucune clé API requise.

## Couches

### 1. Contenu

Markdown simple. La rédaction ne nécessite pas d'outillage spécifique.

| Chemin           | Objectif                                                         |
| ---------------- | ---------------------------------------------------------------- |
| `docs/`          | Articles, guides, références, ce que vous lisez sur le site.     |
| `docs/concepts/` | Modèles d'architecture, principes de conception, concepts techniques. |
| `docs/guides/`   | Guides longs, orientés par sujet.                                |
| `docs/tools/`    | Un dossier par outil de développement documenté.                 |
| `docs/analyses/` | Analyses techniques et études architecturales de plateformes/bibliothèques. |
| `docs/reference/`| Glossaire, architecture, journal des modifications.              |
| `docs/topics/`   | Index des sujets.                                                |
| `projects/`      | Projets réels et exécutables. Chacun est une unité autonome.     |
| `snippets/`      | Petits extraits de code ciblés et exécutables.                   |
| `blog/`          | Articles longs, annonces, post-mortem.                           |
| `memory/`        | Contexte à long terme pour les agents (mission, règles, décisions). |
| `tasks/`         | Pipeline de travail (file d'attente + terminé).                  |
| `reports/`       | Rapports d'exécution horodatés, organisés par année/mois.         |

### 2. Génération

- **MkDocs** avec le thème **Material** transforme l'arborescence Markdown
  en un site statique.
- Plugins :
  - `search` — recherche en texte intégral côté client.
  - `awesome-pages` — index de sections automatiques.
  - `git-revision-date-localized` — date de dernière mise à jour depuis git.
  - `blog` — support de blog intégré de Material.
  - `git-committers` — optionnel, contrôlé par variable d'environnement.

### 3. Déploiement

- `pages.yml` s'exécute à chaque push sur `main`. Il construit le site et
  le déploie sur **GitHub Pages** en utilisant les actions Pages officielles
  (`actions/upload-pages-artifact` + `actions/deploy-pages`).
- Pages est configuré avec `build_type: workflow` et HTTPS activé.

### 4. Automatisation

#### Croissance quotidienne

`wikicode-agent.yml` s'exécute selon une **planification bi-quotidienne** (`0 6,18 * * *`,
06:00 et 18:00 UTC) et sur déclencheurs manuels. Chaque exécution est un
changement unique et ciblé, de sorte que le wiki grandisse un peu chaque jour.

La boucle attendue par exécution :

1. Le workflow démarre. Les dépendances Python sont installées.
2. `scripts/agent.py` lit `memory/` pour le contexte. Si la file d'attente des tâches
   est vide, il découvre de manière proactive de nouveaux outils et projets à
   documenter. Il effectue ensuite des recherches sur le sujet choisi via les API
   Wikipedia + DuckDuckGo.
3. L'API OpenCode génère le contenu (Markdown avec frontmatter).
4. L'agent écrit les fichiers, exécute `mkdocs build --clean` pour
   valider, puis commit et push.
5. `pages.yml` reconstruit et déploie le site.
6. L'exécution suivante voit un wiki légèrement plus grand et continue.

#### Déclencheurs

| Déclencheur              | Cas d'utilisation                                         |
| ------------------------ | --------------------------------------------------------- |
| `schedule`               | L'exécution de croissance par défaut (06:00 et 18:00 UTC).|
| `workflow_dispatch`      | Exécution manuelle depuis l'onglet Actions.               |
| `issue_comment`          | Mention `@agent` sur un commentaire d'issue ou de PR.    |
| `issues` avec label      | Issues étiquetées `agent`.                                |

#### Concurrence

`concurrency: wikicode-agent` est défini avec `cancel-in-progress: true`
afin que les exécutions qui se chevauchent n'écrivent pas deux fois dans le dépôt.

### 5. Anti-duplication

WikiCode ne veut pas documenter la même chose deux fois. Le
mécanisme de déduplication comporte trois parties :

1. **Pages d'index de section.** Chaque section a un `index.md` qui
   liste son contenu actuel. Le plugin `awesome-pages`
   découvre automatiquement la liste à partir du système de fichiers, donc elle est toujours
   exacte.
2. **Recours à `git grep`.** Le script de l'agent analyse les index des sections
   et la liste des tâches, puis utilise `git grep` pour confirmer qu'un sujet est
   nouveau avant de générer du contenu.
3. **Registre de connaissances.** `memory/knowledge.md` liste les principales
   pièces de contenu et les règles pour en ajouter de nouvelles.

Si un doublon est détecté, l'agent doit améliorer la page existante
au lieu d'en écrire une nouvelle (règle 16 dans `memory/rules.md`).

### 6. Recherche web

L'agent utilise les API Wikipedia et DuckDuckGo pour rassembler des informations
sur tout sujet qu'il doit documenter. C'est le mécanisme qui
maintient le contenu généré factuel et à jour :

1. `research_topic()` dans `scripts/agent.py` exécute à la fois une recherche
   Wikipedia et une requête Instant Answer de DuckDuckGo pour le sujet.
2. Wikipedia renvoie les titres des articles + des extraits introductifs (texte
   brut, jusqu'à 2000 caractères).
3. DuckDuckGo renvoie le résumé et les sujets connexes.
4. Si les deux renvoient vide, l'agent se rabat sur les connaissances d'entraînement du LLM.
5. Le texte de recherche rassemblé est injecté dans l'invite de génération de contenu
   afin que le LLM écrive à partir d'informations du monde réel.

## Taxonomie du contenu v2

Chaque document de WikiCode appartient exactement à l'une de ces catégories :

| Catégorie    | Chemin                | Ce qui y va                                               |
| ------------ | --------------------- | --------------------------------------------------------- |
| **Concept**  | `docs/concepts/<slug>/` | Modèle d'architecture, principe de conception ou concept technique. |
| **Outil**    | `docs/tools/<slug>/`  | Documentation d'outil de développement (installation, utilisation, fonctionnalités). |
| **Analyse**  | `docs/analyses/<slug>/` | Étude architecturale d'une plateforme, d'un framework ou d'une bibliothèque. |
| **Projet**   | `projects/<slug>/`    | Projet open source réel et exécutable avec guide d'installation. |
| **Guide**    | `docs/guides/`        | Tutoriel long et orienté sujet ou procédure.              |
| **Rapport**  | `reports/YYYY/MM/`    | Enregistrement d'exécution horodaté, immuable après commit. |
| **Mémoire**  | `memory/`             | Contexte de l'agent : mission, règles, décisions, connaissances, état, qualité. |

La séparation est sémantique, pas cosmétique :

- **Concepts vs Guides** — une page de concept explique un modèle,
  principe ou technique (ex. microservices, CQRS, OAuth).
  Un guide est un parcours narratif qui peut couvrir plusieurs
  concepts ou outils.
- **Outils vs Analyses** — une page d'outil apprend *comment utiliser* quelque chose
  (installer → configurer → exécuter). Une analyse étudie *l'architecture et les
  compromis* (comparer des alternatives, évaluer des décisions de conception).
- **Guides vs Outils** — un guide est un parcours narratif à travers
  plusieurs outils ou concepts. Une page d'outil est une fiche de référence unique.
- **Les rapports comme enregistrements** — les rapports sont immuables après le commit. Ils
  sont organisés par `YYYY/MM/` pour éviter l'enflure du répertoire plat et
  permettre la navigation chronologique.
- **La mémoire comme contrat d'agent** — chaque fichier dans `memory/` a un rôle
  distinct (déclaré dans `memory/knowledge.md`). L'agent les lit tous
  au démarrage ; `state.md` est également écrit après chaque exécution.

## Contrat du frontmatter

Chaque page du site devrait avoir :

```yaml
---
title: Human-readable title
description: One-sentence summary.
created: YYYY-MM-DD
tags: [tag1, tag2]
status: draft | stable | archived | deprecated
---
```

`title` et `description` sont utilisés dans la navigation et la recherche.
`created` alimente la carte de métadonnées ; `git-revision-date-localized`
remplit automatiquement la date de "dernière mise à jour". `tags` permet la
navigation basée sur les étiquettes. `status` signale la maturité de la page.

## Secrets et sécurité

| Secret              | Objectif                                            | Source                |
| ------------------- | --------------------------------------------------- | --------------------- |
| `GITHUB_TOKEN`      | Accès au dépôt dans les workflows.                  | Intégré.              |

Aucun identifiant n'est stocké dans le dépôt.

## Comment faire évoluer l'architecture

Tout changement qui affecte la façon dont le site est construit, déployé ou
automatisé devrait :

1. Être enregistré comme une nouvelle entrée dans `memory/decisions.md` avec le prochain
   numéro disponible.
2. Être reflété dans cette page si cela modifie le diagramme de haut niveau.
3. Conserver le contrat de primauté du dépôt : ne jamais modifier le site publié
   directement.