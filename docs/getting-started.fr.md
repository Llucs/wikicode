---
title: Pour commencer
description: Disposition du dépôt, construction locale et conventions de contribution.
created: 2026-06-03
---

# Pour commencer

Tout ce dont vous avez besoin pour lire, construire et contribuer à WikiCode.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Créé : 2026-06-03</span>
<span class="wikicode-meta-updated">Dernière mise à jour : auto (git)</span>
</div>

## 1. Structure du dépôt

```
.
├── README.md            # Project overview
├── LICENSE              # MIT License
├── AGENT.md             # Operating contract for agents
├── mkdocs.yml           # Static site configuration
├── .gitignore
├── .github/
│   └── workflows/
│       ├── pages.yml    # Builds and deploys the site on push to main
│       └── wikicode-agent.yml# Autonomous agent workflow
├── docs/                # Site content (articles, guides)
│   ├── assets/css/      # Custom styling
│   ├── index.md
│   └── getting-started.md
├── projects/            # Self-contained developer projects
├── snippets/            # Reusable code snippets
├── memory/              # Long-term agent memory
│   ├── mission.md
│   ├── rules.md
│   ├── knowledge.md
│   └── decisions.md
├── tasks/               # Work pipeline
│   ├── queue.md
│   └── completed.md
└── reports/             # Time-stamped execution reports
```

## 2. La boucle « le wiki croît à partir du dépôt »

WikiCode est un site **d'abord le dépôt**. Rien dans `site/` (la sortie publiée) n'est modifié à la main.

1. Un changement est effectué dans le dépôt (un nouvel article, projet, extrait de code, rapport, décision, etc.).
2. Le changement est validé et poussé vers `main`.
3. `.github/workflows/pages.yml` s'exécute automatiquement lors du push.
4. MkDocs lit `docs/`, `projects/`, `snippets/` et reconstruit l'ensemble du site.
5. GitHub Pages sert la nouvelle construction.

L'agent IA local (ou tout contributeur) s'insère dans cette boucle en écrivant dans le dépôt. Le site récupère ensuite le changement sans intervention manuelle.

## 3. Exécuter le site localement

Vous avez besoin de Python 3.10+.

```bash
pip install mkdocs mkdocs-material \
            mkdocs-awesome-pages-plugin \
            mkdocs-git-revision-date-localized-plugin
mkdocs serve
```

Le site sera disponible à `http://127.0.0.1:8000`. Les modifications apportées à tout fichier Markdown dans `docs/`, `projects/` ou `snippets/` déclenchent un rechargement instantané.

## 4. Construire le site statique

```bash
mkdocs build --clean
```

La sortie est écrite dans `site/`. La CI utilise la même commande.

## 5. Ajouter du contenu

| Vous voulez ajouter… | Mettez-le dans…                              | Fichiers requis                      |
| -------------------- | -------------------------------------------- | ------------------------------------ |
| Un article           | `docs/<topic>/<slug>.md` ou `docs/`          | le fichier `.md` lui-même            |
| Un projet            | `projects/<slug>/`                            | `README.md` + `index.md` + source    |
| Un extrait de code   | `snippets/<slug>/`                            | le fichier de code + `index.md`      |
| Une décision         | `memory/decisions.md`                         | ajouter une nouvelle entrée          |
| Une tâche            | `tasks/queue.md`                              | ajouter une nouvelle entrée à cocher |
| Un rapport           | `reports/YYYY-MM-DD-<slug>.md`                | le fichier + mise à jour de l'index  |

Les sections qui ne font pas partie de `docs/` (projects, snippets) sont prises en charge automatiquement par le plugin MkDocs `awesome-pages` via leurs fichiers `index.md`.

## 6. Frontmatter

Chaque page du site a au moins :

```yaml
---
title: Page title
description: Short description.
created: YYYY-MM-DD
---
```

La date `created` est définie lorsque la page est ajoutée pour la première fois. La date **dernière mise à jour** est prise automatiquement à partir de l'historique git du fichier, donc elle est toujours précise sans modifications manuelles.

## 7. Travailler de manière autonome

Les agents doivent suivre `AGENT.md`. La version courte :

1. Lire `memory/mission.md` et `memory/rules.md`.
2. Choisir la prochaine tâche dans `tasks/queue.md`.
3. Faire exactement un changement significatif dans le dépôt.
4. Écrire un rapport dans `reports/`.
5. Déplacer la tâche vers `tasks/completed.md`.
6. Commiter et pousser. Le site se reconstruira automatiquement.

## 8. Recherche

WikiCode est entièrement interrogeable. L'index de recherche est construit au moment du déploiement et fonctionne entièrement dans le navigateur.

- Appuyez sur ++slash++ sur n'importe quelle page pour focaliser la barre de recherche.
- L'index couvre toutes les pages du site, y compris les blocs de code et les articles.
- Voir [Recherche](search.md) pour tous les détails et conseils.

## 9. Comment l'agent est déclenché

Le workflow wikicode-agent prend en charge les déclencheurs **automatiques et manuels** :

| Déclencheur          | Quand                                               | Cas d'utilisation                                |
| -------------------- | --------------------------------------------------- | ------------------------------------------------ |
| `schedule`           | Quotidiennement à 12:00 UTC.                        | Exécution par défaut « grandir un peu chaque jour ». |
| `workflow_dispatch`  | Manuellement depuis l'onglet Actions.               | Exécution à la demande, utile pour débloquer.    |
| `issue_comment`      | Lorsque quelqu'un écrit `@agent` sur un issue.      | Transformer un issue en contribution.            |
| `issues` avec label  | Lorsqu'un issue est étiqueté `agent`.               | Exécutions par lots organisées par l'opérateur.  |

Seulement **une** tâche est exécutée par exécution. L'IA utilise l'API OpenCode pour la génération de contenu — aucune clé API externe nécessaire.

## 10. Conventions

- Noms de fichiers Markdown : minuscules, avec traits d'union.
- Chaque dossier de projet, d'extrait de code et d'outil expose un `index.md` pour la navigation.
- Les décisions concernant l'architecture, les outils ou le workflow sont enregistrées dans `memory/decisions.md`.
- Aucun identifiant, jeton ou donnée privée n'est jamais commité.
- L'agent IA local utilise `secrets.GITHUB_TOKEN` (intégré) pour commiter et pousser. Aucune clé API externe n'est requise.