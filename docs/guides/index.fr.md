---
title: Guides
description: Guides longs, orientés par sujet.
created: 2026-06-03
tags:
  - meta
status: stable
---

# Guides

Guides longs regroupés par sujet. Chaque guide est un vrai fichier Markdown
dans `docs/guides/` (ou un sous-dossier).

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Créé : 2026-06-03</span>
<span class="wikicode-meta-updated">Dernière mise à jour : automatique (git)</span>
</div>

## Conventions

- Un dossier ou un fichier `.md` par guide.
- Nom du dossier : minuscules, avec traits d'union.
- Le frontmatter doit inclure `title`, `description`, `created` et `tags`.
- Les tags aident au cross-linking : privilégiez la réutilisation des tags existants depuis [Tags](../tags.md) plutôt que d'en inventer de nouveaux.

## Tags suggérés

| Tag             | Signification                                        |
| --------------- | ---------------------------------------------------- |
| `meta`          | Pages à propos de WikiCode lui-même.                 |
| `guide`         | Contenu de type tutoriel.                            |
| `reference`     | Matériel de référence (glossaires, listes).          |
| `architecture`  | Comment le wiki est construit et comment il fonctionne. |
| `process`       | Workflow, contribution, gouvernance.                 |
| `language-go`   | Contenu principalement sur Go.                       |
| `language-py`   | Contenu principalement sur Python.                   |
| `language-cpp`  | Contenu principalement sur C++.                      |
| `language-rs`   | Contenu principalement sur Rust.                     |
| `language-js`   | Contenu principalement sur JavaScript / TypeScript. |
| `backend`       | Sujets d'ingénierie backend.                         |
| `frontend`      | Sujets d'ingénierie frontend.                        |
| `devops`        | Build, déploiement, observabilité.                   |
| `security`      | Sujets de sécurité.                                  |
| `data`          | Bases de données, pipelines, analyses.               |

Ajoutez des tags dans le frontmatter comme ceci :

```yaml
---
title: My guide
tags:
  - guide
  - backend
---
```