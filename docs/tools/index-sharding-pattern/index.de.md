---
title: Index-Sperrungs-Muster
description: Ein Technik, die in verteilten Systemen verwendet wird, um große Indexe in kleinere, besser verwaltbare Teile zu teilen, um Leistung und Skalierbarkeit zu verbessern.
created: 2026-07-21
tags:
  - Sperrung
  - Datenbank
  - Skalierbarkeit
  - verteilte Systeme
  - große Daten
status: Entwurf
---

# Index-Sperrungs-Muster

## Einführung

Das Index-Sperrungs-Muster ist eine grundlegende Strategie, die in verteilten Systemen verwendet wird, um große Datensätze in kleinere, besser verwaltbare Teile zu teilen, die als Schrenken bezeichnet werden. Dieses Muster wird in NoSQL-Datenbanken, Suchmaschinen und großen Datenbearbeitungssystemen weit verbreitet, um Skalierbarkeit, Verfügbarkeit und Leistung zu gewährleisten. Die Sperrung hilft, den Lastenausgleich über mehrere Maschinen zu verteilen, verbessert die Abfragespeichereffizienz und stellt sicher, dass Daten effizient gespeichert und abgerufen werden können.

## Kernpunkte

1. **Datenverteilung**: Die Sperrung verteilt Daten über mehrere Knoten oder Schrenke.
2. **Lastausgleich**: Jeder Schrank bearbeitet einen Teil des Lastenauflaufs, was zur Lastenausgleichsfähigkeit beiträgt.
3. **Skalierbarkeit**: Durch Hinzufügen von mehr Schrenken kann das System mehr Daten und mehr Abfragen verarbeiten.
4. **Fehlertoleranz**: Wenn ein Schrank fehlschlägt, kann das System mit anderen Schrenken weiterarbeiten.
5. **Leistung**: Die Sperrung kann die Abfragespeichereffizienz verbessern, indem sie die Anzahl der zu durchsuchenden Daten reduziert.

## Geschichte

Das Konzept der Sperrung existiert seit Jahrzehnten und wurde in frühen Implementierungen relationaler Datenbankmanagementsysteme (RDBMS) wie MySQL und PostgreSQL gefunden. Allerdings gewann es in den Kontexten von NoSQL-Datenbanken und modernen verteilten Systemen an Popularität und Komplexität, insbesondere mit der Aufstieg von großen Daten und verteilten Suchmaschinen wie Elasticsearch und Apache Solr.

## Einsatzfälle

1. **Datenbanken**: NoSQL-Datenbanken wie MongoDB und Cassandra verwenden die Sperrung, um große Datensätze und hohe Lasten zu verwalten.
2. **Suchmaschinen**: Elasticsearch nutzt die Sperrung, um Suchanfragen über mehrere Knoten zu verteilen, was die Suchleistung und Skalierbarkeit verbessert.
3. **Größere Datenbearbeitungssysteme**: Systeme wie Apache Hadoop und Apache Spark verwenden die Sperrung, um große Datensätze über mehrere Knoten zu verwalten und zu bearbeiten.

## Installation

Die Installation und die Einrichtung des Index-Sperrungsmusters erfolgen typischerweise in folgenden Schritten:

1. **Wählen Sie eine Sperrungsmethode**: Bestimmen Sie, wie Sie die Daten sprenkeln werden (z. B. nach Intervallen, nach Hash, nach Schlüssel).
2. **Installieren und Konfigurieren der Datenbank**: Installieren Sie die Datenbank oder das System, das die Sperrung unterstützt, wie z. B. MongoDB oder Elasticsearch.
3. **Konfigurieren der Sperrung**:
   - **MongoDB**: Verwenden Sie den Befehl `sharding` zum Sprenken Ihrer Datenbank und Sammlungen. Sie müssen einen Konfigurationsserver, einen Schrank und einen Router (mongos) einrichten.
   - **Elasticsearch**: Verwenden Sie den Befehlszeilenwerkzeug oder die REST-API, um die Sperrung zu konfigurieren. Sie müssen mehrere Knoten einrichten und die Anzahl der Schrenke und Replikate konfigurieren.
4. **Daten verteilen**: Verteilen Sie Daten über Schrenke, um eine gleichmäßige Lastverteilung sicherzustellen.
5. **Testen und Optimieren**: Testen Sie das System, um sicherzustellen, dass es die Leistungsanforderungen erfüllt, und optimieren Sie die Sperrungsmethode, wenn nötig.

### Beispielsweise: MongoDB-Sperrungseinstellungen

1. **Konfigurationsserver starten**:
   ```bash
   mongod --configsvr --dbpath /data/configdb
   ```

2. **Konfigurationsserver konfigurieren**:
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

3. **Knoten starten**:
   ```bash
   mongod --shardsvr --dbpath /data/shard0001
   ```

4. **Knoten konfigurieren**:
   ```bash
   mongo
   > sh.addShard("localhost:27018")
   ```

5. **Datenbank sprenken aktivieren**:
   ```bash
   sh.shardDatabase("myDatabase", {_id: "hashed"})
   ```

6. **Sammlung sprenken**:
   ```bash
   sh.shardCollection("myDatabase.myCollection", { shardKey: "key" })
   ```

### Beispielsweise: Elasticsearch-Sperrungseinstellungen

1. **Elasticsearch-Knoten installieren**:
   ```bash
   sudo apt-get install -y elasticsearch
   ```

2. **Elasticsearch konfigurieren**:
   ```json
   PUT /my_index
   {
     "settings": {
       "number_of_shards": 3,
       "number_of_replicas": 1
     }
   }
   ```

3. **Schrenke überprüfen**:
   ```bash
   GET /_cat/shards
   ```

## Grundlegende Nutzung

1. **Datenbanken sprenken**:
   - **MongoDB**:
     ```javascript
     sh.shardCollection("myDatabase.myCollection", { shardKey: "key" });
     ```
   - **Elasticsearch**:
     ```json
     PUT /my_index
     {
       "settings": {
         "number_of_shards": 3,
         "number_of_replicas": 1
       }
     }
     ```

2. **Abfragen und Daten abrufen**:
   - **MongoDB**:
     ```javascript
     db.myCollection.find({ shardKey: "value" });
     ```
   - **Elasticsearch**:
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

3. **Schrenke pflegen**:
   - **MongoDB**:
     ```javascript
     sh.status()
     sh.moveChunk("myCollection", { shardKey: "fromKey" }, { shardKey: "toKey" })
     ```
   - **Elasticsearch**:
     ```bash
     curl -X POST "localhost:9200/_cluster/reroute" -H 'Content-Type: application/json' -d'
     {
       "commands": [
         { "allocate_new_shard": { "index": "my_index", "current_state": "UNASSIGNED" } }
       ]
     }
     '
     ```

4. **System skalieren**:
   - **MongoDB**:
     ```bash
     sh.addShard("new_shard_host:27018")
     ```
   - **Elasticsearch**:
     ```bash
     curl -X POST "localhost:9200/_cluster/reroute" -H 'Content-Type: application/json' -d'
     {
       "commands": [
         { "allocate_new_shard": { "index": "my_index", "current_state": "UNASSIGNED" } }
       ]
     }
     '
     ```

Durch die Verständnis und Implementierung des Index-Sperrungsmusters können Sie hochskalierbare und performante verteilte Systeme aufbauen, die große Datenmengen und hohe Lasten verarbeiten können.