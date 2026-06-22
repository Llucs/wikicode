---
title: PlanetScale: Plateforme de base de données MySQL serverless
description: Une plateforme de base de données entièrement gérée, compatible MySQL, construite sur Vitess, qui introduit le branchement de bases de données et les modifications de schéma non bloquantes pour les workflows de développement modernes.
created: 2026-06-22
tags:
  - database
  - mysql
  - vitess
  - serverless
  - schema-migration
  - devops
  - dbaas
  - branching
status: draft
---

# PlanetScale

## Introduction

PlanetScale, fondée en 2018 par les principaux créateurs de Vitess (Sugu Sougoumarane, Jiten Vaidya et Morgan Goeller), est la plateforme de base de données compatible MySQL construite sur le système de clustering de bases de données open source qui alimente YouTube. Elle réinvente la gestion des bases de données en appliquant des **workflows de type Git**—le branchement de bases de données et les Deploy Requests—aux schémas et aux données.

Cette approche élimine les goulots d'étranglement traditionnels et les temps d'arrêt associés aux migrations de schéma, rendant les modifications de base de données aussi sûres, vérifiables et itératives que les modifications de code. PlanetScale est un service entièrement géré qui gère la réplication, les sauvegardes, le sharding et la haute disponibilité, tout en prenant en charge une couche de calcul serverless qui passe à zéro et se réveille instantanément lors de la connexion.

## Concepts clés

### Branchement de bases de données

Tout comme `git branch` permet un développement de code isolé, `pscale branch create` crée une copie isolée et entièrement fonctionnelle de votre base de données (incluant les données et le schéma) sur l'infrastructure de PlanetScale.

- **Branchement à partir de n'importe quel point :** Créez une branche à partir de `main` ou d'un instantané précédent.
- **Données et schéma :** La branche contient un instantané complet, permettant des tests très réalistes.
- **Nature éphémère :** Les branches sont conçues pour être jetées une fois leur objectif atteint, évitant la dérive du schéma.

### Deploy Requests (DRs)

L'équivalent chez PlanetScale d'une Pull Request. Lorsque vous êtes satisfait des modifications de schéma sur une branche, vous ouvrez une Deploy Request. Cela génère un diff, permet la révision et effectue la fusion sous forme de **migration de schéma en ligne non bloquante** (à l'aide de Vitess VReplication).

### Calcul serverless

PlanetScale dissocie le calcul du stockage. Les bases de données ont un état « sommeil » lorsqu'aucune connexion n'est active. Les connexions réveillent instantanément la base de données, éliminant les coûts de calcul inactifs.

## Pour commencer

### Installation

L'interface principale pour les développeurs est l'interface en ligne de commande `pscale`.

**macOS :**
```bash
brew install planetscale/tap/pscale
```

**Linux / Windows :**
```bash
curl -fsSL https://planetscale.com/install.sh | sh
```

### Authentification

```bash
pscale auth login
```

### Création d'une base de données

```bash
pscale database create my-app
```

### Travailler avec les branches

**Créer une branche de fonctionnalité (copie le schéma et les données de main) :**
```bash
pscale branch create my-app feature-user-profile
```

**Se connecter à la branche :**
```bash
pscale connect my-app feature-user-profile --port 3309
```
Cela exécute un proxy local. Votre application se connecte à `127.0.0.1:3309`. Le proxy gère l'authentification automatiquement.

**Exécuter des migrations de schéma sur votre branche :**
Utilisez n'importe quel client MySQL, ORM ou outil de migration (par exemple, `mysql2`, `Prisma`, `SQLAlchemy`).
```sql
ALTER TABLE users ADD COLUMN bio TEXT;
```

### Le flux des Deploy Requests

Une fois que vous avez minutieusement testé les modifications de schéma sur la branche :

```bash
# Create the Deploy Request
pscale deploy-request create my-app feature-user-profile

# List deploy requests
pscale deploy-request list my-app

# Deploy the request (after review)
pscale deploy-request deploy my-app <deploy-number>

# Clean up the branch
pscale branch delete my-app feature-user-profile --force
```

Le déploiement applique la modification de schéma à `main` *sans verrouiller la table ni entraîner de temps d'arrêt*.

## Fonctionnalités clés en détail

### Modifications de schéma non bloquantes (Online DDL)

Les instructions `ALTER TABLE` traditionnelles dans MySQL verrouillent souvent les tables. PlanetScale utilise l'**Online DDL** de Vitess via VReplication. Il crée une table fantôme, copie les données de manière incrémentielle et bascule de manière transparente.

**Exemple de commande :**
```bash
pscale deploy-request deploy my-app 1
```
La production reste pleinement opérationnelle même pendant les migrations volumineuses et de longue durée.

### Pool de connexions

Le pool de connexions intégré côté serveur gère les pics de connexions. Lors de l'utilisation de `pscale connect`, le proxy local regroupe également les connexions. Pour la production, connectez-vous directement à l'adresse du serveur PlanetScale.

### Sharding horizontal (Vitess)

Pour des ensembles de données extrêmement volumineux, PlanetScale utilise le sharding par plage de clés de Vitess pour distribuer les données sur plusieurs instances MySQL de manière transparente. Aucune modification d'application n'est nécessaire.

### Haute disponibilité et réplication globale

La haute disponibilité est intégrée. PlanetScale fournit des réplicas interrégions et un basculement automatique avec un SLA de disponibilité de 99,99 %.

## Cas d'utilisation pratiques

### Intégration CI/CD

Lancez une branche de base de données isolée pour chaque pull request afin d'exécuter des tests d'intégration sur des données de production réelles.
```bash
pscale branch create my-app ci-pr-123 --from main
pscale connect my-app ci-pr-123 --port 3309 &
# Run integration tests here
pscale branch delete my-app ci-pr-123 --force
```

### Tests de pré-production

Laissez l'équipe QA exécuter des tests destructifs ou de charge sur une branche parfaitement réaliste sans corrompre les données de production.

### Revue de schéma

Les membres de l'équipe examinent le diff SQL exact dans une Deploy Request avant la fusion, permettant des workflows « base de données en tant que code ».

### Environnements éphémères

Combinez `pscale branch create/destroy` avec des outils de plateforme engineering (par exemple, opérateurs Kubernetes, Terraform) pour fournir un environnement full-stack par développeur ou par fonctionnalité.

## Limitations et mises en garde

Bien que puissant, le fondement Vitess de PlanetScale introduit quelques particularités de compatibilité MySQL :

- **Pas de procédures stockées ni de déclencheurs :** La couche proxy Vitess ne les prend pas en charge.
- **Clés étrangères :** En version bêta (doit être activé par base de données). Pas encore recommandé pour les chemins critiques de production.
- **`LOCK TABLES` / `UNLOCK TABLES` :** Non pris en charge.
- **`GET_LOCK()` / `RELEASE_LOCK()` :** Non pris en charge.
- **Sous-requêtes et `JOIN` :** La plupart sont pris en charge, mais les sous-requêtes corrélées très complexes ou les instructions non déterministes peuvent se comporter différemment.
- **`ALTER TABLE` direct sur la production :** Le workflow Deploy Request est le *seul* moyen sûr d'apporter des modifications de schéma en production. L'exécution directe de `ALTER TABLE` sur une branche de production via `pscale connect` est fortement déconseillée.

> **Note pour les développeurs :** Utilisez toujours le workflow Deploy Request pour les modifications de schéma en **production**. Pour les branches de développement, `ALTER TABLE` direct est sûr et rapide.

## Modèle de tarification

PlanetScale fonctionne comme un produit SaaS avec un généreux niveau gratuit. La tarification est basée sur le stockage de lignes et les lectures/écritures de lignes.

| Niveau | Prix | Stockage de lignes | Calcul | Branches |
|---|---|---|---|---|
| **Gratuit** | 0 $/mois | 5 Go | 10 M de lectures de lignes/mois, 1 M d'écritures de lignes/mois | Jusqu'à 3 |
| **Scaler** | 39 $/mois (de base) | 10 Go | 100 M de lectures de lignes, 10 M d'écritures de lignes | Jusqu'à 10 |
| **Entreprise** | Personnalisé | Personnalisé | Personnalisé | Personnalisé |

*Les détails de tarification peuvent changer ; vérifiez toujours sur la [page de tarification PlanetScale](https://planetscale.com/pricing).*

## Bonnes pratiques

- **Nommage des branches :** Utilisez un espace de noms cohérent (par exemple, `feature/*`, `hotfix/*`, `ci/*`).
- **Détruire les branches obsolètes :** Nettoyez régulièrement les branches pour éviter les coûts de stockage.
  ```bash
  pscale branch delete my-app stale-branch --force
  ```
- **Surveiller les performances :** Utilisez le tableau de bord PlanetScale pour surveiller les performances des requêtes, les requêtes lentes et l'utilisation des connexions. Les fonctionnalités d'explication de requêtes et d'analyses sont puissantes.
- **Parité des environnements :** Conservez `main` comme un environnement de production vierge. Les équipes de développement travaillent exclusivement sur des branches.
- **Évitez les requêtes lourdes sur les proxys de branche de production :** Bien qu'une branche soit un instantané, l'exécution de requêtes analytiques massives sur une branche connectée au même cluster sous-jacent que la production peut avoir un impact sur les E/S partagées.

## Dépannage

**Connexion refusée dans le proxy :**
```bash
pscale connect my-app main
```
Assurez-vous qu'aucun autre service n'écoute sur ce port. Utilisez `--port` pour spécifier un autre port.

**Échec de la modification de schéma :**
Consultez les journaux de la Deploy Request dans le tableau de bord PlanetScale, ou utilisez :
```bash
pscale deploy-request show my-app <deploy-number>
```

**Latence élevée des requêtes :**
Vérifiez les limites du pool de connexions. Envisagez d'ajouter un index à la branche avant de fusionner :
```sql
ALTER TABLE users ADD INDEX idx_email (email);
```

## Comparaison avec les alternatives

| Fonctionnalité | PlanetScale | Neon (Postgres) | Supabase (Postgres) | RDS (MySQL) |
|---|---|---|---|---|
| **Branchement** | Instantané, données complètes | Instantané, données complètes | Branchement via SQL | Instantanés manuels |
| **Serverless** | Oui (veille/réveil) | Oui (veille/réveil) | Oui (suspension automatique) | Non (toujours actif) |
| **Migrations de schéma** | Non bloquant (Online DDL) | Branchement + `pgroll` | Branchement + migrations | Manuel |
| **Sharding** | Automatique (Vitess) | Non | Non | Manuel (sharding) |
| **Flux CI de migration** | Excellent (Deploy Requests) | Excellent | Bon | Faible |

**Quand choisir PlanetScale :**
Vous avez besoin de la compatibilité MySQL, du branchement de bases de données pour des modifications de schéma et des tests complexes, et de la mise à l'échelle horizontale automatique.

**Quand éviter PlanetScale :**
Vous dépendez fortement des procédures stockées, des déclencheurs ou des mécanismes internes MySQL avancés (par exemple, `GET_LOCK()`). Dans ce cas, RDS ou une solution MySQL gérée standard pourrait être mieux adaptée.

## Résumé

PlanetScale révolutionne l'expérience de développement MySQL en apportant des workflows de type Git à la couche base de données. Sa capacité à créer instantanément des branches de données et de schéma, associée à des Deploy Requests non bloquantes, permet aux équipes d'itérer sur les schémas de base de données avec la même sécurité et la même vélocité que sur leur code applicatif. Construit sur le moteur Vitess éprouvé, il offre une scalabilité de niveau YouTube sans la surcharge opérationnelle.