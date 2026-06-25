---
title: Database Sharding
description: A horizontal scaling technique that distributes data across multiple database servers to improve performance and handle large datasets efficiently.
created: 2026-06-17
tags:
  - database
  - scalability
  - sharding
  - architecture
  - distributed-systems
status: draft
---

# Database Sharding

## Overview

Database sharding is a horizontal partitioning architecture that splits a large dataset into smaller, independent subsets called **shards**, each hosted on a separate database server node. The collection of shards behaves as a single logical database to the application. This technique enables a system to scale beyond the limits of a single machine by distributing both the data volume and the query load across many commodity servers.

---

## What is Sharding?

Sharding is a **scale-out** strategy. Instead of upgrading a single machine (vertical scaling) to handle more data and traffic, you add more servers and split the data among them. Each shard is a complete, independent database that contains only a portion of the total data. A **shard key** determines how data is distributed among the shards.

The term originates from the late 1990s, coined by the developers of *Ultima Online* to describe partitioned game world servers. It was later adopted by early internet giants (eBay, Amazon, Google) to overcome the limits of monolithic databases.

---

## Why Use Sharding? (Benefits)

- **Horizontal Scalability:** Add more servers to handle increasing data volume or read/write throughput without downtime.
- **Improved Query Performance:** Queries that filter by the shard key hit only a single shard, reducing latency and resource contention.
- **Increased Storage Capacity:** Total storage is the sum of all shard capacities, far exceeding a single node.
- **Geographic Distribution:** Place shards close to users in different regions to reduce latency and comply with data residency regulations (e.g., GDPR).

## When Not to Shard

- The dataset is small (<1–2 TB) and fits comfortably on one server.
- The workload is read-heavy and can be handled with caching or read replicas.
- The application relies heavily on cross-shard joins, complex transactions, or global consistency – sharding severely impacts these operations.

---

## How Sharding Works

Sharding requires a **shard key**: a column or field that determines which shard stores each record. The shard key is used by a routing mechanism to direct queries to the correct shard.

### Sharding Strategies

| Strategy | Description | Pros | Cons |
|----------|-------------|------|------|
| **Range-Based** | Data split by key ranges (e.g., A–F → shard 1, G–M → shard 2) | Efficient for range scans | Prone to hotspots if data distribution is uneven |
| **Hash-Based** | Hashed value of shard key determines shard (e.g., `shard_id = hash(key) % N`) | Even distribution; avoids hotspots | Range queries become scatter-gather; re-sharding is harder |
| **Directory-Based** | Lookup service maps every key to a shard | Flexible; fine-grained control | Lookup service becomes a potential bottleneck/SPOF |

### Routing Approaches

1. **Application-Level:** The application code contains the routing logic (e.g., modulo or a lookup table). Simple but couples the code to the sharding scheme.
2. **Middleware / Proxy:** A service like Vitess, ProxySQL, or MongoDB `mongos` routes queries transparently, insulating the application.
3. **Native Database Support:** Some databases (MongoDB, Citus for PostgreSQL, CockroachDB) manage sharding internally, including data distribution, rebalancing, and query routing.

---

## Installation / Setup

Sharding is not a standalone tool; it is an architecture pattern implemented within a database system. Below are setup examples for two popular sharded databases.

### MongoDB Sharded Cluster

MongoDB provides native sharding through a cluster of `mongos` routers and `config servers`.

1. **Start config servers** (a replica set for metadata).
2. **Start shard servers** (each can be a standalone or replica set).
3. **Start `mongos` router(s)** pointing to the config servers.
4. **Connect via `mongos`** and enable sharding.

```bash
# Step 1: Config server (3-node replica set example)
mongod --configsvr --replSet configRS --port 27019 --dbpath /data/configdb
# Initialize replica set via mongo shell

# Step 2: Shard servers (each shard can be a replica set)
mongod --shardsvr --replSet shard1RS --port 27018 --dbpath /data/shard1

# Step 3: Mongos router
mongos --configdb configRS/localhost:27019 --port 27017

# Step 4: Enable sharding on a database and collection
mongo --port 27017
```

### Citus (PostgreSQL Extension)

Citus transforms PostgreSQL into a distributed database. Install the extension and define the shard key.

```sql
-- Install on each worker node
CREATE EXTENSION citus;

-- On the coordinator node, add workers
SELECT citus_add_node('worker1', 5432);
SELECT citus_add_node('worker2', 5432);

-- Distribute a table by a shard key
SELECT create_distributed_table('orders', 'customer_id');
```

---

## Usage Examples

All examples below use MongoDB syntax, but the concepts apply universally.

### Defining a Sharded Collection

```javascript
// Connect via mongos
sh.enableSharding("ecommerce");

// Shard the 'orders' collection using a hashed shard key on customer_id
sh.shardCollection("ecommerce.orders", { "customer_id": "hashed" });
```

### Querying with the Shard Key

Queries that include the shard key are routed to exactly one shard, making them fast.

```javascript
// Fast: Mongos knows only shard A has customer_id = 12345
db.orders.find({ customer_id: 12345 });
```

### Queries Without the Shard Key (Scatter-Gather)

If the shard key is missing, the query must be sent to all shards and the results merged – much slower.

```javascript
// Slow: Mongos must ask every shard for orders > $100
db.orders.find({ total: { $gt: 100 } });
```

### Inserting Data

Inserts are automatically routed to the correct shard.

```javascript
// Inserts are automatically routed to the correct shard based on customer_id
db.orders.insertMany([
  { _id: 1, customer_id: 12345, total: 29.99 },
  { _id: 2, customer_id: 67890, total: 49.99 }
]);
```

### Updating and Deleting

The same routing logic applies: include the shard key for targeted operations.

```javascript
db.orders.updateOne(
  { customer_id: 12345, _id: 1 },
  { $set: { status: "shipped" } }
);
```

---

## Key Features

- **Horizontal Scale-Out:** Add servers linearly to double capacity.
- **Shared-Nothing Architecture:** Each shard independently manages its own CPU, memory, and storage – no contention.
- **Data Isolation:** Failures are contained to one shard; others continue operating.
- **Geographic Distribution:** Place shards in different data centers to meet latency or legal requirements.

---

## Best Practices

1. **Choose the shard key carefully.** It must:
   - Have **high cardinality** (many unique values).
   - Support your **most common query patterns** (to avoid scatter-gather).
   - Distribute **write load evenly** (avoid monotonically increasing keys like timestamps, which create hotspots).
2. **Denormalize to avoid cross-shard joins.** Joins across shards are extremely slow or impossible; design your data model accordingly.
3. **Plan for resharding.** Adding or removing shards is the hardest part. Use hash-based sharding or tools that support online rebalancing (e.g., MongoDB's sharded cluster balancer).
4. **Monitor shard imbalances.** Use your database's monitoring tools to ensure data and load are evenly distributed.

---

## Challenges and Trade-offs

- **Complexity:** Sharding adds significant operational overhead: managing multiple servers, routing, backups, and rebalancing.
- **Cross-Shard Operations:** Transactions across shards require a distributed transaction coordinator (e.g., Two-Phase Commit), which is slow and not supported by all databases.
- **Resharding Difficulty:** Changing the shard key or redistributing data is risky and often requires downtime or sophisticated migration procedures.
- **Limited Query Support:** Many databases lose support for global indexes, multi-shard joins, and strong consistency when sharded.

---

## Conclusion

Database sharding is a powerful technique for achieving massive scalability when vertical scaling, caching, and read replicas are no longer sufficient. It allows you to scale out your database across many servers, handling petabytes of data and millions of writes per second. However, it introduces significant complexity and trade-offs. Sharding should be adopted only after careful planning and when the workload truly demands it. Modern NewSQL databases (CockroachDB, Google Spanner) and distributed SQL extensions (Citus) aim to provide transparent sharding with fewer operational burdens, but the fundamental principles remain the same.