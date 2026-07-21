---
title: Schéma de partage des indices
description: Une technique utilisée dans les systèmes distribués pour diviser les grands indices en morceaux plus petits, plus gérables, afin d'améliorer la performance et l'échelle.
created: 2026-07-21
tags:
  - partage
  - base de données
  - échelle
  - systèmes distribués
  - grande données
status: brouillon
---

# Schéma de partage des indices

## Vue d'ensemble

Le schéma de partage des indices est une stratégie fondamentale utilisée dans les systèmes distribués pour gérer les grands ensembles de données en les divisant en morceaux plus petits, plus gérables appelés partitions. Ce schéma est largement utilisé dans les bases de données NoSQL, les moteurs de recherche et les systèmes de traitement de grande taille pour assurer l'échelle, l'availability et la performance. Le partage des indices aide à distribuer le chargement sur plusieurs machines, améliore la performance des requêtes et assure que les données peuvent être stockées et récupérées efficacement.

## Caractéristiques clés

1. **Distribution des données** : Le partage des indices distribue les données sur plusieurs nœuds ou partitions.
2. **Equilibre du chargement** : Chaque partition gère une partie du travail, ce qui aide à équilibrer le chargement.
3. **Échelle** : L'ajout de partitions permet au système de gérer plus de données et de plus de requêtes.
4. **Tolérance aux pannes** : Si une partition échoue, le système peut continuer à fonctionner avec les autres partitions.
5. **Performance** : Le partage des indices peut améliorer la performance des requêtes en réduisant la quantité de données à analyser.

## Histoire

Le concept de partage des indices a existé pendant des décennies, avec des implémentations précoce trouvées dans les systèmes de gestion de base de données relationnelle (RDBMS) comme MySQL et PostgreSQL. Cependant, il a gagné en popularité et en sophistication dans le contexte des bases de données NoSQL et des systèmes distribués modernes, en particulier avec l'essor de la grande data et des moteurs de recherche distribués comme Elasticsearch et Apache Solr.

## Cas d'utilisation

1. **Bases de données** : Les bases de données NoSQL comme MongoDB et Cassandra utilisent le partage des indices pour gérer les grands ensembles de données et le trafic élevé.
2. **Moteurs de recherche** : Elasticsearch utilise le partage des indices pour distribuer les requêtes de recherche sur plusieurs nœuds, améliorant la performance et l'échelle des recherches.
3. **Traitement de grande taille** : Les systèmes comme Apache Hadoop et Apache Spark utilisent le partage des indices pour gérer et traiter les grands ensembles de données sur plusieurs nœuds.

## Installation

L'installation et la configuration du partage des indices impliquent généralement les étapes suivantes :

1. **Choisir une stratégie de partage** : Déterminer comment vous partagerez vos données (par intervalle, par hachage, par clé).
2. **Installer et configurer la base de données** : Installer la base de données ou le système qui supporte le partage, comme MongoDB ou Elasticsearch.
3. **Configurer le partage** :
   - **MongoDB** : Utiliser la commande `sharding` pour partager votre base de données et les collections. Vous devez configurer un serveur de configuration, une partition et un router (mongos).
   - **Elasticsearch** : Utiliser l'outil de ligne de commande `elasticsearch` ou l'API REST pour configurer le partage. Vous devez configurer plusieurs nœuds et définir le nombre de partitions et de répliques.
4. **Distribuer les données** : Distribuer les données sur les partitions pour assurer une distribution de charge équilibrée.
5. **Tester et optimiser** : Tester le système pour assurer qu'il répond aux exigences de performance et optimiser la stratégie de partage en fonction des besoins.

### Exemple : Configuration de partage des indices MongoDB

1. **Démarrer les serveurs de configuration** :
   ```bash
   mongod --configsvr --dbpath /data/configdb
   ```

2. **Configurer le serveur de configuration** :
   ```bash
   mongo
   > config = {
   ...   _id: "config",
   ...   configsvrs: [
   ...     { _id: 0, host: "localhost:27019" }
   ...   ]
   ... }
   > configsvrReconfig(config)
   ```

3. **Démarrer les partitions** :
   ```bash
   mongod --shardsvr --dbpath /data/shard0001
   ```

4. **Configurer les partitions** :
   ```bash
   mongo
   > sh.addShard("localhost:27018")
   ```

5. **Activer le partage d'une base de données** :
   ```bash
   sh.shardDatabase("myDatabase", {_id: "hashed"})
   ```

6. **Partitionner une collection** :
   ```bash
   sh.shardCollection("myDatabase.myCollection", { shardKey: "key" })
   ```

### Exemple : Configuration de partage des indices Elasticsearch

1. **Installer des nœuds Elasticsearch** :
   ```bash
   sudo apt-get install -y elasticsearch
   ```

2. **Configurer Elasticsearch** :
   ```json
   PUT /my_index
   {
     "settings": {
       "number_of_shards": 3,
       "number_of_replicas": 1
     }
   }
   ```

3. **Vérifier les partitions** :
   ```bash
   GET /_cat/shards
   ```

## Utilisation de base

1. **Partitionner une collection** :
   - **MongoDB** :
     ```javascript
     sh.shardCollection("myDatabase.myCollection", { shardKey: "key" });
     ```
   - **Elasticsearch** :
     ```json
     PUT /my_index
     {
       "settings": {
         "number_of_shards": 3,
         "number_of_replicas": 1
       }
     }
     ```

2. **Requêter et récupérer des données** :
   - **MongoDB** :
     ```javascript
     db.myCollection.find({ shardKey: "value" });
     ```
   - **Elasticsearch** :
     ```json
     GET /my_index/_search
     {
       "query": {
         "match": {
           "shardKey": "value"
         }
       }
     }
     ```

3. **Gérer les partitions** :
   - **MongoDB** :
     ```javascript
     sh.status()
     sh.moveChunk("myCollection", { shardKey: "fromKey" }, { shardKey: "toKey" })
     ```
   - **Elasticsearch** :
     ```bash
     curl -X POST "localhost:9200/_cluster/reroute" -H 'Content-Type: application/json' -d'
     {
       "commands": [
         { "allocate_new_shard": { "index": "my_index", "current_state": "UNASSIGNED" } }
       ]
     }
     '
     ```

4. **Éscalader le système** :
   - **MongoDB** :
     ```bash
     sh.addShard("new_shard_host:27018")
     ```
   - **Elasticsearch** :
     ```bash
     curl -X POST "localhost:9200/_cluster/reroute" -H 'Content-Type: application/json' -d'
     {
       "commands": [
         { "allocate_new_shard": { "index": "my_index", "current_state": "UNASSIGNED" } }
       ]
     }
     '
     ```

En comprenant et en mettant en œuvre le schéma de partage des indices, vous pouvez construire des systèmes distribués hautement échelonnés et performants capables de gérer de grands volumes de données et de trafic.