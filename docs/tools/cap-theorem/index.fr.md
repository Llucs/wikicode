---
title: Théorème CAP (Théorème de Brewer)
description: Un principe fondamental de compromis dans les systèmes distribués stipulant qu'il est impossible pour un magasin de données distribué de garantir simultanément la Cohérence, la Disponibilité et la Tolérance au partitionnement.
created: 2026-06-21
tags:
  - distributed-systems
  - cap-theorem
  - consistency
  - availability
  - partition-tolerance
  - brewers-theorem
  - system-design
  - database-architecture
status: draft
---

# Théorème CAP (Théorème de Brewer)

## Qu'est-ce que le théorème CAP ?

Le théorème CAP est un principe fondamental dans la conception des systèmes distribués. Il a été introduit pour la première fois par **Eric Brewer** lors du symposium ACM sur les principes du calcul distribué (PODC) en **2000** et formellement prouvé par **Seth Gilbert** et **Nancy Lynch** en **2002**.

Le théorème stipule qu'un magasin de données distribué ne peut fournir que **deux des trois** garanties à un moment donné :
- **Cohérence (C)**
- **Disponibilité (A)**
- **Tolérance au partitionnement (P)**

Bien que souvent simplifié à tort comme un choix strict "choisir deux", l'interprétation correcte est : **en présence d'une partition réseau, vous devez choisir entre la Cohérence et la Disponibilité**. Étant donné que les partitions réseau sont inévitables dans les systèmes distribués, vous ne pouvez pas avoir les trois simultanément.

---

## Les trois propriétés

### Cohérence (C)
Chaque lecture reçoit la **dernière écriture** ou une erreur. Tous les nœuds du système voient les mêmes données au même moment logique. Cela implique un ordre total des opérations (linéarisabilité).

- **Impact :** Une cohérence plus forte nécessite souvent une synchronisation entre les nœuds avant d'accuser réception des écritures.
- **Exemple :** Une lecture à partir de n'importe quel nœud doit retourner le même résultat qu'une lecture à partir du nœud primaire.

### Disponibilité (A)
Chaque requête reçue par un nœud non défaillant du système **doit aboutir à une réponse**. La réponse peut ne pas contenir les données les plus récentes, mais elle ne sera pas une erreur (par exemple, timeout ou 503).

- **Impact :** Le système reste actif et accepte le trafic, même si certains réplicas ne sont pas synchronisés.
- **Exemple :** Une application web continue de servir un catalogue de produits même si un nœud de base de données en aval est inaccessible.

### Tolérance au partitionnement (P)
Le système continue de fonctionner malgré **un nombre arbitraire de messages perdus ou retardés** par le réseau entre les nœuds. Cela inclut les scissions réseau, les coupures de câble et la perte de paquets.

- **Impact :** Le système doit fonctionner correctement même lorsque les nœuds ne peuvent pas communiquer.
- **Réalité :** Les partitions sont inévitables dans tout système géographiquement distribué. Par conséquent, **tout système distribué doit être tolérant au partitionnement (P)**.

---

## Le vrai compromis : CP vs AP

Comme les partitions réseau (P) sont inévitables dans un système distribué, atteindre **CA** (Cohérence + Disponibilité) sans tolérance au partitionnement est impossible dans un contexte distribué. Le choix réel est :

### Systèmes CP (Cohérence + Tolérance au partitionnement)
- **Sacrifice :** Disponibilité pendant une partition.
- **Comportement :** Les nœuds qui ne peuvent pas garantir la cohérence avec le reste du cluster refusent de répondre aux requêtes (deviennent indisponibles) jusqu'à ce que la partition soit résolue.
- **Cas d'utilisation :** Registres bancaires, gestion des stocks, dossiers médicaux — les situations où des données obsolètes sont inacceptables.
- **Exemples notables :**
  - **Apache ZooKeeper** (élection de leader, données de configuration)
  - **Apache HBase** (modèle de cohérence forte)
  - **MongoDB** (avec le souci d'écriture `w: "majority"` et lectures à partir du primaire)
  - **Redis** (mode cluster avec garanties de cohérence strictes)

### Systèmes AP (Disponibilité + Tolérance au partitionnement)
- **Sacrifice :** Cohérence pendant une partition.
- **Comportement :** Tous les nœuds restent disponibles pour servir les requêtes, même s'ils acceptent les écritures de manière indépendante. Le système repose sur des mécanismes de résolution de conflits (par exemple, last-write-wins, CRDTs) pour réconcilier les données lorsque la partition est résolue.
- **Cas d'utilisation :** Flux de médias sociaux, diffusion de contenu, données de capteurs IoT, catalogues de produits — des environnements où la disponibilité est critique.
- **Exemples notables :**
  - **Apache Cassandra** (cohérence réglable, cohérence éventuelle par défaut)
  - **Amazon DynamoDB** (lectures éventuellement cohérentes multi-région)
  - **CouchDB / Couchbase** (réplication multi-maître)
  - **Riak**

### Systèmes CA (Cohérence + Disponibilité)
- **Contexte :** Uniquement possible dans un système non distribué (un seul nœud) ou un système qui ignore simplement les partitions (ce qui est dangereux).
- **Exemples notables :**
  - Une instance autonome **MySQL** ou **PostgreSQL**.
  - SGBDR traditionnels conformes ACID fonctionnant sur un seul serveur.
  - *Note :* Dans un déploiement distribué, ces systèmes doivent répliquer les données et rencontrer inévitablement des partitions, les forçant à adopter un comportement CP ou AP.

---

## Caractéristiques clés et nuances

### 1. Le "P" n'est pas optionnel

Une erreur courante de débutant est de concevoir un système distribué "CA". Une fois que les données sont répliquées sur un réseau, vous êtes susceptible de rencontrer des partitions. Tout système distribué réel **doit** tolérer les partitions, ce qui rend le véritable choix **CP vs AP** lorsqu'une partition se produit.

### 2. Réglabilité

Les bases de données modernes ne sont pas enfermées dans une seule classification. Vous pouvez souvent échanger de la cohérence contre de la disponibilité (ou vice versa) par requête.

- **Cassandra :** Passer de `QUORUM` (cohérence forte) à `ONE` (cohérence éventuelle) par requête.
- **MongoDB :** Configurer `writeConcern` et `readPreference` pour basculer entre cohérence forte et faible.
- **DynamoDB :** Choisir `ConsistentRead` à `true` ou `false` lors des lectures.

### 3. L'erreur du "2 sur 3"

Le théorème CAP ne dit pas "le système doit toujours choisir deux des trois". Il dit que **pendant une partition réseau**, vous devez choisir **C** ou **A**. Le reste du temps (lorsque le réseau est sain), le système peut viser à la fois une cohérence forte et une haute disponibilité.

C'est là qu'intervient le **théorème PACELC**.

---

## L'extension PACELC (La vision moderne)

Introduite par **Daniel J. Abadi**, PACELC étend CAP en considérant explicitement les compromis lorsque le système est **sain** (pas de partition).

**PACELC signifie :**
- Si une **P**artition se produit → compromis entre **A**vailability (Disponibilité) et **C**onsistency (Cohérence).
- **E**lse (sinon, lorsque le réseau est sain) → compromis entre **L**atency (Latence) et **C**onsistency (Cohérence).

### Pourquoi PACELC est important
- **Compromis en état sain :** Même sans partitions, vous pouvez choisir d'attendre que les réplicas soient d'accord (latence élevée, cohérence forte) ou de répondre rapidement avec des données potentiellement obsolètes (faible latence, cohérence éventuelle).
- **Configuration réelle :**
  - **Système CP (pendant une partition) :** Sacrifie la disponibilité.
    - **E** (Else) : Peut aussi sacrifier la latence pour la cohérence (par exemple, réplication synchrone).
  - **Système AP (pendant une partition) :** Sacrifie la cohérence.
    - **E** (Else) : Peut sacrifier la cohérence pour une faible latence (par exemple, réplication asynchrone, réplicas en lecture).

---

## Application pratique et configuration

Vous n'installez pas le théorème CAP, mais vous configurez vos magasins de données distribués pour gérer ses compromis.

### Logique de décision conceptuelle (pseudo-code)

```python
# High-level logic for handling a request during a detected partition

import config

def handle_write_during_partition(data):
    partition_detected = check_network_health()
    
    if partition_detected:
        if config.CAP_MODE == "CP":
            # Refuse the write to maintain consistency
            raise ServiceUnavailable("Cannot guarantee consistency during partition.")
        elif config.CAP_MODE == "AP":
            # Accept the write locally; resolve conflicts later
            store_with_timestamp(data, node_id=config.NODE_ID)
            return {"status": "accepted", "note": "Eventual consistency in effect."}
    else:
        # Network is healthy -> standard operation
        return normal_write_operation(data)
```

### MongoDB : Ajustement CP/AP par requête

```javascript
// CP behavior: Ensure writes are committed to majority before acknowledging
db.inventory.insertOne(
   { item: "journal", qty: 25, status: "A" },
   { writeConcern: { w: "majority", wtimeout: 5000 } }
);

// CP behavior: Read from the primary (strongest consistency)
db.inventory.find({ status: "A" }).readPref("primary");

// AP behavior: Read from any secondary (potential stale data)
db.inventory.find({ status: "A" }).readPref("secondary");

// AP behavior: Allow reads from secondaries if primary is unreachable
db.inventory.find({ status: "A" }).readPref("secondaryPreferred");
```

### Apache Cassandra : Niveaux de cohérence réglables

```cql
-- Strong Consistency (towards CP)
-- Ensures all replicas in the quorum have the same data
SELECT * FROM users WHERE user_id = 123 CONSISTENCY QUORUM;

-- Write with strong consistency
INSERT INTO users (user_id, name) VALUES (123, 'Alice') USING TIMESTAMP 1000;
-- Ensure quorum acknowledged the write
-- Requires consistency level QUORUM or ALL

-- Eventual Consistency (towards AP, lower latency)
SELECT * FROM users WHERE user_id = 123 CONSISTENCY ONE;

-- High Availability, low consistency (AP)
-- Writes acknowledged by just one node
INSERT INTO users (user_id, name) VALUES (456, 'Bob') CONSISTENCY ANY;
```

---

## Quand choisir CP vs AP

| Scénario | Approche recommandée | Justification |
|---|---|---|
| Traitement des paiements / Registres | **CP** | Des comptes ou soldes incohérents entraînent des pertes financières et des problèmes juridiques. Un temps d'arrêt temporaire pendant une partition est préférable à une double dépense. |
| Dossiers médicaux / Données de santé | **CP** | Les décisions vitales dépendent de données complètes et exactes. Un temps d'arrêt est plus sûr que des diagnostics contradictoires ou obsolètes. |
| Données de session utilisateur (e-commerce) | **AP** | Les utilisateurs doivent pouvoir naviguer et ajouter des articles à leur panier même si un centre de données est hors ligne. Des stocks obsolètes sont un compromis temporaire acceptable. |
| Flux de médias sociaux | **AP** | Les utilisateurs s'attendent à ce que le site soit opérationnel. Un like manquant ou un commentaire retardé est acceptable si cela signifie que l'application reste réactive. |
| Diffusion de contenu / CDN | **AP** | Servir une version légèrement obsolète d'une page en cache est largement préférable à une page d'erreur. |
| Métadonnées / Stockage de configuration (ZooKeeper, etcd) | **CP** | La configuration doit être faisant autorité et cohérente dans tout le cluster. Diviser le cluster en vues incohérentes est dangereux (split-brain). |

---

## Histoire et impact

### Chronologie
- **1998 :** Eric Brewer présente pour la première fois l'idée des trois propriétés.
- **2000 :** Brewer postule formellement la conjecture à PODC.
- **2002 :** Seth Gilbert et Nancy Lynch du MIT publient "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services", prouvant formellement le théorème.
- **Fin des années 2000 :** Le théorème a directement influencé l'architecture de **Amazon DynamoDB**, **Google Bigtable**, **Apache Cassandra** et **MongoDB**.
- **Années 2010 :** Le mouvement NoSQL adopte le théorème CAP comme principe de conception principal. PACELC est introduit pour clarifier les compromis "toujours", pas seulement pendant les partitions.
- **Années 2020 :** Les bases de données SQL distribuées modernes (Spanner, CockroachDB, YugabyteDB) tentent de repousser les limites, visant "C et A" la plupart du temps en réduisant agressivement la probabilité et la durée des partitions (par exemple, en utilisant TrueTime / une synchronisation d'horloge serrée).

### Point clé
Le théorème CAP a été révolutionnaire car il a donné aux architectes un langage formel pour discuter des compromis. Avant CAP, les opérateurs s'attendaient à ce que les bases de données distribuées se comportent exactement comme des bases monolithiques. Le théorème a forcé l'industrie à admettre que **la cohérence forte a un coût**, et que ce coût est souvent payé en disponibilité lors des pannes.

---

## Limites et critiques

1.  **Faux binaire :** Les critiques soutiennent que "C, A, P" ne sont pas des propriétés binaires. Il existe des degrés de cohérence (forte, causale, éventuelle, lecture-écritures) et de disponibilité.
2.  **Ignorer la latence :** Le théorème CAP original ne traite pas explicitement des compromis lorsque le réseau est sain (ceci est abordé par PACELC).
3.  **CA est un piège :** De nombreux ingénieurs recherchent des systèmes "CA" distribués. En réalité, tout système répliquant des données sur un réseau est tolérant au partitionnement (P) par nécessité. Étiqueter un système comme purement "CA" est souvent du marketing, pas de l'architecture.
4.  **Atténuation moderne :** Les bases de données comme **Google Spanner** utilisent des horloges atomiques et l'API TrueTime pour atteindre simultanément une cohérence forte et une haute disponibilité *la plupart du temps*, réduisant le scénario "choisir 2 sur 3" à un cas rare.

---

## Voir aussi

- **Théorème PACELC** — L'extension moderne de CAP incluant les compromis de latence.
- **Cohérence éventuelle** — Le modèle de cohérence sur lequel la plupart des systèmes AP s'appuient.
- **ACID vs BASE** — ACID (Atomicité, Cohérence, Isolation, Durabilité) vs BASE (Basically Available, Soft state, Cohérence éventuelle).
- **Eric Brewer** — Proposant original du théorème.
- **Conception de systèmes distribués** — Partitionnement, réplication, algorithmes de consensus (Raft, Paxos).
- **CRDTs (Conflict-free Replicated Data Types)** — Structures de données qui résolvent naturellement les conflits dans les systèmes AP.