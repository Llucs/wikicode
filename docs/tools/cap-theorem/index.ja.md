---
title: CAP定理 (ブルワーの定理)
description: 分散システムにおける基本的なトレードオフの原則であり、分散データストアがConsistency、Availability、Partition Toleranceを同時に保証することは不可能であることを述べています。
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

# CAP定理 (ブルワーの定理)

## CAP定理とは？

CAP定理は、分散システム設計における基本原則です。2000年にACM Symposium on Principles of Distributed Computing (PODC) で**Eric Brewer**によって初めて提唱され、2002年に**Seth Gilbert**と**Nancy Lynch**によって正式に証明されました。

この定理は、分散データストアは常に3つの保証のうち**2つ**しか提供できないと述べています。
- **Consistency (C)**
- **Availability (A)**
- **Partition Tolerance (P)**

厳密な「2つを選ぶ」選択として単純化されることが多いですが、正しい解釈は次のとおりです。**ネットワークパーティションが存在する場合、ConsistencyとAvailabilityのどちらかを選択しなければなりません**。分散システムではネットワークパーティションは避けられないため、3つすべてを同時に持つことはできません。

---

## 3つの特性

### Consistency (C)
すべての読み取りは**最新の書き込み**またはエラーを受け取ります。システム内のすべてのノードは同じ論理時刻に同じデータを認識します。これは操作の完全な順序付け（線形化可能性）を意味します。

- **影響:** より強い一貫性は、書き込みを確認する前にノード間の同期を必要とすることがよくあります。
- **例:** 任意のノードからの読み取りは、プライマリノードからの読み取りと同じ結果を返す必要があります。

### Availability (A)
システム内の故障していないノードが受信したすべてのリクエストは、**応答を返さなければなりません**。応答には最新のデータが含まれていない可能性がありますが、エラー（例：タイムアウトや503）にはなりません。

- **影響:** 一部のレプリカが同期していなくても、システムは稼働し続け、トラフィックを受け入れます。
- **例:** 下流のデータベースノードが到達不能でも、Webアプリケーションは製品カタログを提供し続けます。

### Partition Tolerance (P)
システムは、ノード間のネットワークによって**任意の数のメッセージがドロップまたは遅延**しても動作し続けます。これには、ネットワーク分割、ケーブルの切断、パケットロスが含まれます。

- **影響:** ノードが通信できない場合でも、システムは正しく機能する必要があります。
- **現実:** パーティションは、地理的に分散したシステムでは避けられません。したがって、**すべての分散システムはP-tolerantでなければなりません**。

---

## 実際のトレードオフ：CP vs AP

分散システムではネットワークパーティション (P) は避けられないため、分散コンテキストでPartition Toleranceなしに**CA** (Consistency + Availability) を達成することは不可能です。実際の選択は次のとおりです。

### CP Systems (Consistency + Partition Tolerance)
- **犠牲にするもの:** パーティション中の可用性。
- **動作:** クラスターの残りとの一貫性を保証できないノードは、パーティションが解決されるまでリクエストへの応答を拒否します（利用不可になります）。
- **ユースケース:** 銀行の元帳、在庫管理、健康記録 — 古いデータが許容されない状況。
- **代表的な例:**
  - **Apache ZooKeeper** (leader election, configuration data)
  - **Apache HBase** (strong consistency model)
  - **MongoDB** (with `w: "majority"` write concern and reads from primary)
  - **Redis** (cluster mode with strict consistency guarantees)

### AP Systems (Availability + Partition Tolerance)
- **犠牲にするもの:** パーティション中の一貫性。
- **動作:** すべてのノードは、独立して書き込みを受け入れても、リクエストを提供できる状態を維持します。システムは、パーティションが回復したときにデータを調整するために、競合解決メカニズム（例：last-write-wins、CRDT）に依存します。
- **ユースケース:** ソーシャルメディアフィード、コンテンツ配信、IoTセンサーデータ、製品カタログ — 稼働時間が重要な環境。
- **代表的な例:**
  - **Apache Cassandra** (tunable consistency, eventual consistency by default)
  - **Amazon DynamoDB** (multi-region eventually consistent reads)
  - **CouchDB / Couchbase** (multi-master replication)
  - **Riak**

### CA Systems (Consistency + Availability)
- **文脈:** 非分散（シングルノード）システム、または単にパーティションを無視するシステム（危険）でのみ可能です。
- **代表的な例:**
  - A standalone **MySQL** or **PostgreSQL** instance.
  - Traditional ACID-compliant RDBMS running on a single server.
  - *注:* 分散デプロイメントでは、これらのシステムはデータをレプリケートする必要があり、必然的にパーティションに直面し、CPまたはAPの動作を強いられます。

---

## 主要な機能とニュアンス

### 1. 「P」はオプションではない
初心者がよく犯す間違いは、「CA」分散システムを設計することです。データがネットワーク経由でレプリケートされると、パーティションの影響を受けやすくなります。実際の分散システムはパーティションに**耐える必要があり**、パーティションが発生した場合の実際の選択は**CP vs AP**となります。

### 2. 調整可能性
最新のデータベースは単一の分類に固定されていません。多くの場合、クエリごとに一貫性と可用性をトレードオフできます（またはその逆）。

- **Cassandra:** リクエストごとに`QUORUM`（強い一貫性）と`ONE`（結果整合性）を切り替えます。
- **MongoDB:** `writeConcern`と`readPreference`を設定して、強い一貫性と弱い一貫性を切り替えます。
- **DynamoDB:** 読み取り時に`ConsistentRead`を`true`または`false`に選択します。

### 3. 「3つから2つ」の誤解
CAP定理は「システムは常に3つから2つを選ばなければならない」と言っているわけではありません。**ネットワークパーティション中**には、**C**または**A**を選択しなければならないと言っています。それ以外の時間（ネットワークが正常な場合）は、システムは強い一貫性と高可用性の両方を追求できます。

ここで**PACELC定理**が登場します。

---

## PACELC拡張 (現代の視点)

**Daniel J. Abadi**によって導入されたPACELCは、システムが**正常**（パーティションなし）な場合のトレードオフを明示的に考慮することでCAPを拡張します。

**PACELCの意味:**
- If a **P**artition occurs → trade-off between **A**vailability and **C**onsistency.
- **E**lse (when the network is healthy) → trade-off between **L**atency and **C**onsistency.

### PACELCの重要性
- **正常状態のトレードオフ:** パーティションがなくても、レプリカが合意するのを待つ（高レイテンシ、強い一貫性）か、潜在的に古いデータで迅速に応答する（低レイテンシ、結果整合性）かを選択できます。
- **実際の設定:**
  - **CP system (during partition):** 可用性を犠牲にします。
    - **E** (その他): 一貫性のためにレイテンシを犠牲にする場合があります（例：同期レプリケーション）。
  - **AP system (during partition):** 一貫性を犠牲にします。
    - **E** (その他): 低レイテンシのために一貫性を犠牲にする場合があります（例：非同期レプリケーション、読み取りレプリカ）。

---

## 実用的な適用と設定

CAP定理を「インストール」するわけではありませんが、分散データストアを設定してそのトレードオフを管理します。

### 概念的な決定ロジック（疑似コード）

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

### MongoDB: クエリごとのCP/APチューニング

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

### Apache Cassandra: 調整可能な一貫性レベル

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

## CP vs APの選択基準

| シナリオ | 推奨アプローチ | 根拠 |
|---|---|---|
| 支払い処理 / 元帳 | **CP** | 一貫性のないカウントや残高は、金銭的損失や法的問題を引き起こします。パーティション中の一時的なダウンタイムは、二重支払いよりも望ましいです。 |
| 健康記録 / 医療データ | **CP** | 生命に関わる判断は、完全で正確なデータに依存します。ダウンタイムは、矛盾した診断や古い診断よりも安全です。 |
| ユーザーセッションデータ（eコマース） | **AP** | データセンターがオフラインになっても、ユーザーは閲覧してカートに商品を追加できる必要があります。古い在庫数は許容可能な一時的なトレードオフです。 |
| ソーシャルメディアフィード | **AP** | ユーザーはサイトが稼働していることを期待します。アプリの応答性が維持されるのであれば、いいねの欠落やコメントの遅延は許容されます。 |
| コンテンツ配信 / CDN | **AP** | わずかに古いキャッシュバージョンのページを提供することは、エラーページよりもはるかに好まれます。 |
| メタデータ / 設定ストア (ZooKeeper, etcd) | **CP** | 設定はクラスター全体で信頼でき、一貫している必要があります。クラスターを一貫性のないビューに分割することは危険です（スプリットブレイン）。 |

---

## 歴史と影響

### タイムライン
- **1998:** Eric Brewerが3つの特性のアイデアを初めて発表。
- **2000:** BrewerがPODCで正式に予想を提唱。
- **2002:** MITのSeth GilbertとNancy Lynchが「Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services」を発表し、定理を正式に証明。
- **2000年代後半:** この定理は、**Amazon DynamoDB**、**Google Bigtable**、**Apache Cassandra**、**MongoDB**のアーキテクチャに直接影響を与えました。
- **2010年代:** NoSQL運動はCAP定理を主要な設計原則として採用。PACELCは、パーティション時だけでなく「常に」のトレードオフを明確にするために導入されました。
- **2020年代:** 最新の分散SQLデータベース（Spanner、CockroachDB、YugabyteDB）は、パーティションの確率と期間を積極的に削減することで（例：TrueTime/高精度のクロック同期）、ほとんどの場合に「CとA」を目指して限界に挑戦しています。

### 重要な洞察
CAP定理は、アーキテクトにトレードオフを議論するための正式な言語を提供したため、革新的でした。CAP以前は、運用者は分散データベースがモノリシックなデータベースとまったく同じように動作することを期待していました。この定理は、業界に**強い一貫性にはコストが伴う**こと、そしてそのコストは障害時に可用性で支払われることが多いことを認めさせました。

---

## 限界と批判

1.  **誤った二分法:** 批評家は、「C、A、P」は二値の特性ではないと主張しています。一貫性（strong、causal、eventual、read-your-writes）と可用性には程度があります。
2.  **レイテンシの無視:** 元のCAP定理は、ネットワークが正常な場合のトレードオフを明示的に扱っていません（これはPACELCで扱われています）。
3.  **CAは罠:** 多くのエンジニアはCAの「分散」システムを探し求めます。実際には、ネットワーク経由でデータをレプリケートするシステムは、必然的にP-tolerantです。システムを単に「CA」とラベリングすることは、アーキテクチャではなくマーケティングであることがよくあります。
4.  **現代の緩和策:** **Google Spanner**のようなデータベースは、原子時計とTrueTime APIを使用して、*ほとんどの場合*、強い一貫性と高可用性を同時に実現し、「3つから2つ選ぶ」シナリオをまれなエッジケースに減らしています。

---

## 関連項目

- **PACELC Theorem** — CAPの最新の拡張であり、レイテンシのトレードオフを含みます。
- **Eventual Consistency** — ほとんどのAPシステムが依存する一貫性モデル。
- **ACID vs BASE** — ACID (Atomicity, Consistency, Isolation, Durability) と BASE (Basically Available, Soft state, Eventual consistency) の比較。
- **Eric Brewer** — 定理の最初の提唱者。
- **Distributed System Design** — シャーディング、レプリケーション、合意アルゴリズム (Raft, Paxos)。
- **CRDTs (Conflict-free Replicated Data Types)** — APシステムで自然に競合を解決するデータ構造。