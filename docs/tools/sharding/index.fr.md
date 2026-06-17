---
title: Sharding — Partitionnement horizontal de bases de données pour la scalabilité
description: Un guide approfondi sur le sharding, une technique de partitionnement horizontal de bases de données entre serveurs pour améliorer la scalabilité, les performances et l'isolation des pannes.
created: 2026-06-16
tags:
  - database
  - scalability
  - sharding
  - distributed-systems
  - performance
status: draft
---

# Sharding

**Sharding** est un modèle d'architecture de base de données où un ensemble de données logiquement unifié et volumineux est partitionné horizontalement en bases de données plus petites et indépendantes appelées *shards*. Chaque shard est hébergé sur une instance de serveur distincte fonctionnant dans une architecture « shared-nothing ». Le sharding dépasse les limites de la mise à l'échelle verticale d'une seule machine en distribuant les données et la charge de travail sur de nombreux nœuds.

## Ce que c'est

Le sharding divise les données en morceaux basés sur une *clé de shard* déterministe. Chaque shard contient un sous-ensemble des données (par exemple, toutes les lignes pour une plage donnée de `user_id`) et est responsable du service des lectures et écritures pour sa partition. Le système global apparaît comme une seule base de données logique aux clients via une couche de routage (logique applicative, proxy ou routeur de base de données).

## Pourquoi sharder ?

| Bénéfice | Description |
|---------|-------------|
| **Scalabilité horizontale** | Le débit en lecture et écriture augmente linéairement à mesure que les shards sont ajoutés. |
| **Haute disponibilité et isolation des pannes** | La défaillance d'un seul shard n'affecte qu'un sous-ensemble d'utilisateurs ; les autres shards continuent de servir. |
| **Parallélisme** | Les requêtes qui touchent plusieurs shards peuvent être parallélisées, améliorant la latence. |
| **Distribution géographique** | Les données peuvent être placées plus près de populations d'utilisateurs spécifiques, réduisant les allers-retours réseau. |
| **Isolation opérationnelle** | La maintenance, les sauvegardes et les changements de schéma peuvent être effectués sur un seul shard à la fois. |

Le sharding est essentiel lorsqu'une seule base de données ne peut plus gérer la charge — souvent après que la mise à l'échelle verticale (CPU plus gros, plus de RAM) devient prohibitive en termes de coût ou atteint les limites matérielles.

## Architectures de sharding

Le sharding peut être implémenté à plusieurs niveaux :

### 1. Application‑Level (Manual)

L'application contient la logique de routage (par exemple, `hash(user_id) % num_shards`). Chaque shard est une base de données standard sans logiciel supplémentaire.  
**Avantages :** Simple à démarrer, aucun middleware.  
**Inconvénients :** Fragile ; le resharding nécessite des modifications de code ; les requêtes cross‑shard sont extrêmement difficiles.  
**Statut :** Aujourd'hui considéré comme un anti‑pattern pour les nouveaux projets.

### 2. Middleware / Proxy Level (e.g., Vitess, Citus)

Un proxy transparent intercepte les requêtes SQL et les achemine vers le shard approprié.

- **Vitess** pour MySQL : déploie `vtgate` (proxy) + `vttablet` par shard, géré par une topologie etcd/zk.
- **Citus** pour PostgreSQL : une extension qui transforme un cluster Postgres en base de données distribuée.

**Avantages :** Transparence SQL, resharding automatisé (Vitess), jointures cross‑shard (Citus).  
**Inconvénients :** Couche de complexité supplémentaire ; certaines requêtes deviennent impossibles ou lentes.

### 3. Database‑Native (e.g., MongoDB, Cassandra, Druid)

Le moteur de base de données gère la distribution en interne. Le développeur fournit une clé de shard, et le système gère le placement et le routage des données.

- **MongoDB** : clusters shardés avec des routeurs `mongos` et des serveurs de configuration.
- **Cassandra** : partitionnement par une clé de partition dans la définition de la clé primaire ; le hachage cohérent distribue les lignes automatiquement.

**Avantages :** Pas de proxy externe ; fonctionnalités comme l'auto‑équilibrage.  
**Inconvénients :** Doit soigneusement concevoir le modèle de données autour de la clé de shard ; opérations cross‑shard limitées ou absentes.

### 4. Cloud‑Managed (e.g., Amazon DynamoDB, Azure Cosmos DB, Google Cloud Spanner)

Le fournisseur abstrait complètement la gestion des shards. Vous choisissez une clé de partition lors de la création de la table ; la plateforme cloud divise, migre et équilibre les données automatiquement.

**Avantages :** Aucune surcharge opérationnelle ; mise à l'échelle automatique.  
**Inconvénients :** Dépendance vis-à-vis du fournisseur ; coût potentiellement plus élevé pour les charges de travail importantes ; aucun contrôle direct sur le placement des shards.

## Installation et utilisation de base

Voici des exemples concrets pour deux des implémentations de sharding les plus courantes.

### MongoDB Sharding

**Installation / Configuration**

- Déployez un **ensemble de réplicas de serveur de configuration** (CSRS) qui stocke les métadonnées du cluster.
- Déployez des **ensembles de réplicas de shards** (chaque shard est au moins un nœud unique, mais généralement un ensemble de réplicas pour une haute disponibilité).
- Déployez un ou plusieurs **routeurs `mongos`** qui traitent les requêtes des applications.

Les commandes suivantes (exécutées contre un `mongos`) activent le sharding et shardent une collection :

```javascript
// Activation du sharding sur une base de données
sh.enableSharding("ecommerce");

// Sharding d'une collection avec une clé de shard hachée (recommandée pour une distribution uniforme)
sh.shardCollection(
  "ecommerce.orders",
  { "order_id": "hashed" }
);
```

Avec une clé de shard hachée, les documents sont répartis uniformément sur les shards. Les requêtes qui incluent la clé de shard sont routées directement vers le shard correct :

```javascript
// Requête efficace – va vers un seul shard
db.orders.find({ "order_id": UUID("123e4567-e89b-12d3-a456-426614174000") })
```

Les requêtes cross‑shard (par exemple, les agrégations sans la clé de shard) se disperseront sur tous les shards, ce qui peut nuire aux performances.

### Citus (extension PostgreSQL)

**Installation**

1. Installez l'extension `citus` sur le nœud coordinateur et tous les nœuds workers.
2. Ajoutez les nœuds workers au coordinateur :
   ```sql
   SELECT citus_add_node('worker-node-1', 5432);
   SELECT citus_add_node('worker-node-2', 5432);
   ```

**Utilisation de base**

Distribuez une table en spécifiant sa colonne de distribution (clé de shard) :

```sql
-- Création de la table sur le coordinateur
CREATE TABLE orders (
    order_id    BIGSERIAL,
    user_id     INT,
    product_id  INT,
    quantity    INT,
    PRIMARY KEY (order_id, user_id)
);

-- Distribution de la table sur les workers en fonction de user_id
SELECT create_distributed_table('orders', 'user_id');
```

Citus réécrit le SQL pour atteindre le shard pertinent. Une requête qui filtre sur `user_id` ira vers un seul worker :

```sql
-- Requête mono‑shard
SELECT * FROM orders WHERE user_id = 42;
```

Pour les jointures entre deux tables qui sont colocalisées sur la même clé de distribution, Citus peut les exécuter efficacement :

```sql
-- Exemple de colocalisation : orders et order_items distribués sur user_id
SELECT create_distributed_table('orders', 'user_id');
SELECT create_distributed_table('order_items', 'user_id');
-- La jointure s'effectue maintenant localement sur chaque shard
SELECT o.order_id, oi.product_id
FROM orders o JOIN order_items oi USING (order_id)
WHERE o.user_id = 42;
```

## Décisions de conception clés

### 1. Choix de la clé de shard

La clé de shard est la décision la plus critique. Elle doit :

- **Distribuer les données uniformément** pour éviter les points chauds.
- **Correspondre aux modèles de requêtes** afin que les requêtes courantes puissent être routées vers un seul shard.
- **Avoir une cardinalité élevée** (de nombreuses valeurs distinctes) pour permettre un fractionnement équilibré.

**Mauvais choix :** Les valeurs croissantes de manière monotone (par exemple, horodatages, ID auto‑incrémentés) font que toutes les nouvelles écritures vont vers le dernier shard.
**Meilleurs choix :** ID utilisateurs, colonnes hachées ou clés composites qui combinent une cardinalité élevée et des colonnes de filtrage fréquentes.

### 2. Opérations cross‑shard

Les jointures, transactions et agrégations qui s'étendent sur plusieurs shards sont soit très coûteuses, soit non supportées. Stratégies d'atténuation :

- **Dénormalisation** pour conserver les données connexes dans le même shard.
- **Colocalisation** (Citus) ou **incorporation de documents** (MongoDB) pour stocker les données hiérarchiques dans le même shard.
- **Coordination côté application** pour les transactions multi‑shard (rarement recommandé).

### 3. Resharding

Ajouter ou supprimer des shards nécessite une redistribution des données. Les systèmes modernes offrent des mécanismes intégrés :

- **MongoDB Balancer** déplace automatiquement les chunks entre les shards.
- **Vitess Reshard** divise les shards à l'aide d'un workflow `MoveTables`.
- **Les services cloud** gèrent les divisions de manière transparente.

Le resharding manuel (dans le sharding au niveau de l'application) est notoirement difficile et sujet aux erreurs.

## État actuel

L'industrie s'éloigne du sharding manuel. Les bases de données **NewSQL** (CockroachDB, YugabyteDB, Google Spanner) abstraient complètement la gestion des shards derrière une interface SQL standard, offrant des transactions ACID et des jointures cross‑shard. La plupart des bases de données cloud (DynamoDB, Cosmos DB) proposent un sharding serverless. Cependant, le concept central du sharding reste le fondement de toutes les bases de données distribuées horizontalement.

Pour les nouveaux projets, préférez l'un de ces systèmes plutôt que de construire votre propre couche de sharding. Si vous avez besoin de SQL et de forte cohérence, envisagez Citus ou Spanner ; si la flexibilité orientée document et le débit massif sont primordiaux, MongoDB ou DynamoDB sont d'excellents choix.

## Résumé

Le sharding est un outil puissant pour atteindre des performances à l'échelle du web, mais il introduit de la complexité. En comprenant les options architecturales, en choisissant une bonne clé de shard et en tirant parti des outils de gestion modernes, vous pouvez mettre à l'échelle votre couche de données sans réinventer la roue.