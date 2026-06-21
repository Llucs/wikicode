---
title: CAP Theorem (Brewer's Theorem)
description: A fundamental trade-off principle in distributed systems stating that it is impossible for a distributed data store to simultaneously guarantee Consistency, Availability, and Partition Tolerance.
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

# CAP Theorem (Brewer's Theorem)

## What Is the CAP Theorem?

The CAP Theorem is a foundational principle in distributed system design. It was first introduced by **Eric Brewer** at the ACM Symposium on Principles of Distributed Computing (PODC) in **2000** and formally proven by **Seth Gilbert** and **Nancy Lynch** in **2002**.

The theorem states that a distributed data store can only provide **two out of three** guarantees at any given time:
- **Consistency (C)**
- **Availability (A)**
- **Partition Tolerance (P)**

While often oversimplified as a strict "pick two" choice, the correct interpretation is: **in the presence of a network partition, you must choose between Consistency and Availability**. Since network partitions are inevitable in distributed systems, you cannot have all three simultaneously.

---

## The Three Properties

### Consistency (C)
Every read receives the **most recent write** or an error. All nodes in the system see the same data at the same logical time. This implies a total order of operations (linearizability).

- **Impact:** Stronger consistency often requires synchronization between nodes before acknowledging writes.
- **Example:** A read from any node must return the same result as a read from the primary node.

### Availability (A)
Every request received by a non-failing node in the system **must result in a response**. The response may not contain the latest data, but it will not be an error (e.g., timeout or 503).

- **Impact:** The system stays up and accepting traffic, even if some replicas are out of sync.
- **Example:** A web application continues to serve a product catalog even if a downstream database node is unreachable.

### Partition Tolerance (P)
The system continues to operate despite **an arbitrary number of messages being dropped or delayed** by the network between nodes. This includes network splits, cable cuts, and packet loss.

- **Impact:** The system must function correctly even when nodes cannot communicate.
- **Reality:** Partitions are unavoidable in any geographically distributed system. Therefore, **every distributed system must be P-tolerant**.

---

## The Real Trade-off: CP vs AP

Because network partitions (P) are unavoidable in a distributed system, achieving **CA** (Consistency + Availability) without Partition Tolerance is impossible in a distributed context. The actual choice is:

### CP Systems (Consistency + Partition Tolerance)
- **Sacrifices:** Availability during a partition.
- **Behavior:** Nodes that cannot guarantee consistency with the rest of the cluster refuse to respond to requests (become unavailable) until the partition is resolved.
- **Use Cases:** Banking ledgers, inventory management, health records — situations where stale data is unacceptable.
- **Notable Examples:**
  - **Apache ZooKeeper** (leader election, configuration data)
  - **Apache HBase** (strong consistency model)
  - **MongoDB** (with `w: "majority"` write concern and reads from primary)
  - **Redis** (cluster mode with strict consistency guarantees)

### AP Systems (Availability + Partition Tolerance)
- **Sacrifices:** Consistency during a partition.
- **Behavior:** All nodes remain available to serve requests, even if they accept writes independently. The system relies on conflict resolution mechanisms (e.g., last-write-wins, CRDTs) to reconcile data when the partition heals.
- **Use Cases:** Social media feeds, content delivery, IoT sensor data, product catalogs — environments where uptime is critical.
- **Notable Examples:**
  - **Apache Cassandra** (tunable consistency, eventual consistency by default)
  - **Amazon DynamoDB** (multi-region eventually consistent reads)
  - **CouchDB / Couchbase** (multi-master replication)
  - **Riak**

### CA Systems (Consistency + Availability)
- **Context:** Only possible in a non-distributed (single-node) system or a system that simply ignores partitions (which is dangerous).
- **Notable Examples:**
  - A standalone **MySQL** or **PostgreSQL** instance.
  - Traditional ACID-compliant RDBMS running on a single server.
  - *Note:* In a distributed deployment, these systems must replicate data and inevitably encounter partitions, forcing them into either CP or AP behavior.

---

## Key Features & Nuances

### 1. The "P" is Not Optional
A common beginner mistake is designing a "CA" distributed system. Once data is replicated across a network, you are susceptible to partitions. Any real distributed system **must** tolerate partitions, making the real selection **CP vs AP** when a partition occurs.

### 2. Tunability
Modern databases are not locked into a single classification. You can often trade consistency for availability (or vice versa) on a per-query basis.

- **Cassandra:** Switch between `QUORUM` (strong consistency) and `ONE` (eventual consistency) per request.
- **MongoDB:** Configure `writeConcern` and `readPreference` to shift between strong and weak consistency.
- **DynamoDB:** Choose `ConsistentRead` as `true` or `false` on reads.

### 3. The "2 of 3" Fallacy
The CAP theorem does not say "the system must always pick two of three". It says **during a network partition**, you must choose **C** or **A**. The rest of the time (when the network is healthy), the system can strive for both strong consistency and high availability.

This is where the **PACELC Theorem** comes into play.

---

## The PACELC Extension (The Modern View)

Introduced by **Daniel J. Abadi**, PACELC extends CAP by explicitly considering trade-offs when the system is **healthy** (no partition).

**PACELC stands for:**
- If a **P**artition occurs → trade-off between **A**vailability and **C**onsistency.
- **E**lse (when the network is healthy) → trade-off between **L**atency and **C**onsistency.

### Why PACELC Matters
- **Healthy State Trade-offs:** Even without partitions, you can choose to wait for replicas to agree (high latency, strong consistency) or respond quickly with potentially stale data (low latency, eventual consistency).
- **Real-World Configuration:**
  - **CP system (during partition):** Sacrifices availability.
    - **E** (Else): Might also sacrifice latency for consistency (e.g., synchronous replication).
  - **AP system (during partition):** Sacrifices consistency.
    - **E** (Else): Might sacrifice consistency for low latency (e.g., asynchronous replication, read replicas).

---

## Practical Application & Configuration

You do not "install" the CAP theorem, but you configure your distributed data stores to manage its trade-offs.

### Conceptual Decision Logic (Pseudocode)

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

### MongoDB: Per-Query CP/AP Tuning

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

### Apache Cassandra: Tunable Consistency Levels

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

## When to Choose CP vs AP

| Scenario | Recommended Approach | Rationale |
|---|---|---|
| Payment processing / Ledgers | **CP** | Inconsistent counts or balances cause financial loss and legal issues. Temporary downtime during a partition is preferable to double-spending. |
| Health records / Medical data | **CP** | Life-critical decisions depend on complete, accurate data. Downtime is safer than conflicting or stale diagnoses. |
| User session data (e-commerce) | **AP** | Users must be able to browse and add items to their cart even if a datacenter goes offline. Stale inventory counts are an acceptable temporary trade-off. |
| Social media feeds | **AP** | Users expect the site to be up. A missing like or a delayed comment is acceptable if it means the app stays responsive. |
| Content delivery / CDNs | **AP** | Serving a slightly stale cached version of a page is vastly preferred over an error page. |
| Metadata / Configuration stores (ZooKeeper, etcd) | **CP** | Configuration must be authoritative and consistent across the cluster. Splitting the cluster into inconsistent views is dangerous (split-brain). |

---

## History & Impact

### Timeline
- **1998:** Eric Brewer first presents the idea of the three properties.
- **2000:** Brewer formally postulates the conjecture at PODC.
- **2002:** Seth Gilbert and Nancy Lynch of MIT publish "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services", formally proving the theorem.
- **Late 2000s:** The theorem directly influenced the architecture of **Amazon DynamoDB**, **Google Bigtable**, **Apache Cassandra**, and **MongoDB**.
- **2010s:** The NoSQL movement embraces the CAP theorem as a primary design principle. PACELC is introduced to clarify the "always" trade-offs, not just during partitions.
- **2020s:** Modern distributed SQL databases (Spanner, CockroachDB, YugabyteDB) attempt to push the boundaries, striving for "C and A" most of the time by aggressively reducing the probability and duration of partitions (e.g., using TrueTime / tight clock synchronization).

### Key Insight
The CAP theorem was revolutionary because it gave architects a formal language to discuss trade-offs. Before CAP, operators expected distributed databases to behave exactly like monolithic ones. The theorem forced the industry to admit that **strong consistency has a cost**, and that cost is often paid in availability during failures.

---

## Limitations & Criticism

1.  **False Binary:** Critics argue "C, A, P" are not binary properties. There are degrees of consistency (strong, causal, eventual, read-your-writes) and availability.
2.  **Ignoring Latency:** The original CAP theorem does not explicitly address trade-offs when the network is healthy (this is addressed by PACELC).
3.  **CA is a Trap:** Many engineers look for CA "distributed" systems. In reality, any system replicating data across a network is P-tolerant by necessity. Labeling a system purely "CA" is often marketing, not architecture.
4.  **Modern Mitigation:** Databases like **Google Spanner** use atomic clocks and the TrueTime API to achieve strong consistency and high availability simultaneously *most of the time*, reducing the "pick 2 of 3" scenario to a rare edge case.

---

## See Also

- **PACELC Theorem** — The modern extension of CAP including latency trade-offs.
- **Eventual Consistency** — The consistency model most AP systems rely on.
- **ACID vs BASE** — ACID (Atomicity, Consistency, Isolation, Durability) vs BASE (Basically Available, Soft state, Eventual consistency).
- **Eric Brewer** — Original proposer of the theorem.
- **Distributed System Design** — Sharding, replication, consensus algorithms (Raft, Paxos).
- **CRDTs (Conflict-free Replicated Data Types)** — Data structures that naturally resolve conflicts in AP systems.