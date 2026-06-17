---
title: Grafana: オープンオブザーバビリティプラットフォーム
description: メトリクス、ログ、トレースに対する統合的な可視化、監視、アラート機能。
created: 2026-06-15
tags:
  - observability
  - monitoring
  - visualization
  - dashboards
  - open-source
status: draft
ecosystem: observability
---

# Grafana: オープンオブザーバビリティプラットフォーム

## Grafanaとは？

Grafanaは、オブザーバビリティのための主要なオープンソースの分析・インタラクティブ可視化プラットフォームです。時系列データベース（Prometheus、InfluxDB、Graphite）からログバックエンド（Loki、Elasticsearch）、トレーシングシステム（Tempo、Jaeger）、SQLストア（PostgreSQL、MySQL）、クラウドAPI（AWS CloudWatch、Azure Monitor）まで、あらゆるデータソースに接続します。メトリクス、ログ、トレースをクエリ、可視化、アラート設定、理解するための単一のビューを提供します。

Grafanaはオープンな標準規格に基づいて構築されているため、ベンダーロックインを回避できます。数十のソースからのデータを同じダッシュボードで混在させることができ、インフラストラクチャ監視、アプリケーションパフォーマンス管理、ビジネス分析、IoTテレメトリなど、同じプラットフォームが同様に機能します。

---

## Grafanaを選ぶ理由

- **統合オブザーバビリティ** – メトリクス、ログ、トレース、ビジネスデータを1つの場所にまとめます。
- **豊富なビジュアライゼーション** – 数十のパネルタイプ（時系列、統計、テーブル、ヒートマップ、ジオマップ、ローソク足、ログ、トレースなど）。
- **動的ダッシュボード** – テンプレート変数を使用してダッシュボードを再利用可能かつインタラクティブにします。
- **統合アラート通知** – 単一インターフェースからデータソース全体のすべてのアラートルールを管理します。
- **エクスプローラーモード** – ダッシュボードを保存せずにアドホックなトラブルシューティング。
- **拡張性** – データソース、パネル、アプリ向けのプラグインマーケットプレイス。
- **GitOps対応** – 設定ファイルでダッシュボード、データソース、アラートルールをプロビジョニング。
- **セキュリティとガバナンス** – 組織、チーム、きめ細かいRBAC、OAuth、APIキー。
- **セルフホストまたはクラウド** – 自分で運用するか、Grafana Cloud（無料枠充実）を利用。

---

## インストール

### 1. バイナリ / パッケージ

`.rpm`、`.deb`、またはスタンドアロンのtarballを[ダウンロードページ](https://grafana.com/grafana/download)からダウンロードしてインストールします。

```bash
# Debian / Ubuntu
sudo apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana_11.0.0_amd64.deb
sudo dpkg -i grafana_11.0.0_amd64.deb
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

```bash
# RHEL / CentOS / Fedora
sudo yum install -y https://dl.grafana.com/oss/release/grafana-11.0.0-1.x86_64.rpm
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

### 2. Docker

公式のDockerイメージを実行します（デフォルトポート3000）。永続データのためにボリュームをマウントします。

```bash
docker run -d \
  -p 3000:3000 \
  --name=grafana \
  -v grafana-storage:/var/lib/grafana \
  grafana/grafana:latest
```

### 3. Kubernetes (Helm)

GrafanaのHelmリポジトリを追加してデプロイします。

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install my-grafana grafana/grafana \
  --namespace monitoring --create-namespace \
  --set persistence.enabled=true \
  --set adminPassword='admin'
```

### 4. Grafana Cloud

[grafana.com](https://grafana.com)で無料アカウントを作成します。無料枠には10,000シリーズ、14日間の保持、全プラットフォームへのアクセスが含まれます。

---

## 基本的な使い方

Grafanaを起動したら、`http://localhost:3000`を開き、デフォルトの認証情報（`admin` / `admin`）でログインします。新しいパスワードの設定を求められます。

### ステップ1: データソースを追加

1. **Configuration → Data Sources** に移動。
2. **データソースの追加**をクリック。
3. タイプを選択（例：Prometheus）。
4. URLを入力（例：`http://prometheus:9090`）し、**保存 & テスト**をクリック。

### ステップ2: ダッシュボードを作成

1. サイドバーの**+**アイコンをクリック → **新しいダッシュボード**。
2. **新しいパネルを追加**をクリック。
3. クエリエディターでデータソース用のクエリを記述（例：PromQL式）。
4. ビジュアライゼーションタイプを選択（時系列、統計、ゲージ、テーブルなど）。
5. 軸、単位、色、しきい値、凡例をカスタマイズ。
6. **適用**をクリックしてパネルをダッシュボードに追加。
7. わかりやすい名前でダッシュボードを保存。

### ステップ3: Exploreでデータをクエリ

アドホックな調査には、**Explore**ビュー（サイドバーのコンパスアイコン）を使用します。ダッシュボードを保存または作成する必要なく、サンドボックス化されたクエリエディターを提供します。

```promql
# Example PromQL queries to run in Explore
rate(node_cpu_seconds_total[5m])
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
count by (job) (up == 0)
```

### ステップ4: アラートを設定

パネルエディターで、**アラート**タブに移動します：

1. **このパネルからアラートルールを作成**をクリック。
2. 条件を定義（例：`MAX() OF query (A) IS ABOVE 90`）。
3. 評価動作を設定（例：1分ごとに評価、保留期間5分）。
4. **通知先**を追加（Slack、PagerDuty、メール、webhookなど）。
5. ルールを保存。

アラートは**Alerting → Alert rules**で一元管理され、サイレンス、ミュートタイミング、通知ポリシーをサポートしています。

---

## 主な機能とコマンド例

### 1. 動的ダッシュボードとテンプレート変数

変数を使用するとダッシュボードをインタラクティブにできます。例えば、変数`$job`をPromQLクエリで使用できます。

```promql
rate(http_requests_total{job=~"$job"}[5m])
```

変数は**Dashboard settings → Variables**で定義します。タイプはQuery、Custom、Interval、Data sourceなどがあります。

### 2. プロビジョニング (GitOps)

Grafanaのプロビジョニングディレクトリ（`/etc/grafana/provisioning/`）に配置したYAMLファイルでデータソースとダッシュボードを自動化します。

**Datasource provision example** (`datasources.yaml`):

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://localhost:9090
    isDefault: true
```

**Dashboard provision example** (`dashboards.yaml`):

```yaml
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: 'Provisioned Dashboards'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: false
    options:
      path: /var/lib/grafana/dashboards
```

ダッシュボードのJSONファイルを指定されたパスに配置すると、Grafanaが自動的に同期します。

### 3. API & CLI

Grafanaは自動化のための包括的なREST APIを公開しています。

```bash
# List dashboards
curl -s -u admin:admin http://localhost:3000/api/search?type=dash-db | jq .

# Create a data source
curl -s -X POST -u admin:admin \
  -H "Content-Type: application/json" \
  -d '{
        "name":"MyPrometheus",
        "type":"prometheus",
        "url":"http://prometheus:9090",
        "access":"proxy"
      }' \
  http://localhost:3000/api/datasources
```

`grafana-cli`を使用してプラグインを管理します。

```bash
# Install a panel plugin
grafana-cli plugins install grafana-piechart-panel

# List installed plugins
grafana-cli plugins ls
```

### 4. Exploreモード (深掘りトラブルシューティング)

Exploreを使用すると、メトリクス、ログ、トレースにまたがるクエリを並行して実行できます。例えば、高レイテンシのメトリクスから関連するトレースやログエントリにジャンプできます。

### 5. 統合アラート通知

すべてのアラートルール（Prometheus、Loki、SQLデータベースなど）は一箇所で管理されます。APIによるルール定義の例：

```json
{
  "title": "High CPU alert",
  "condition": "A",
  "data": [
    {
      "refId": "A",
      "relativeTimeRange": { "from": 600, "to": 0 },
      "datasourceUid": "P010D9A9C2F1E4B8C",
      "model": {
        "expr": "avg(node_load1) > 2",
        "intervalMs": 1000,
        "maxDataPoints": 100,
        "refId": "A"
      }
    }
  ]
}
```

### 6. プラグインエコシステム

コミュニティおよび公式プラグインでGrafanaを拡張します。[Grafana Plugins](https://grafana.com/grafana/plugins/)カタログを参照してください。UI（Configuration → Plugins）またはCLIからインストールします。

### 7. セキュリティと認証

Grafanaは複数の認証方法をサポートしています：OAuth（GitHub、Google、GitLab、Okta）、SAML、LDAP、認証プロキシ。RBACはUIまたはプロビジョニングで設定できます。

設定例（`grafana.ini`）：

```ini
[auth.github]
enabled = true
allow_sign_up = true
client_id = YOUR_GITHUB_CLIENT_ID
client_secret = YOUR_GITHUB_CLIENT_SECRET
scopes = user:email,read:org
```

---

## まとめ

Grafanaはオブザーバビリティの事実上のオープンソース標準であり、チームがあらゆるソースからのデータを統合、可視化、アラート通知できるようにします。小規模クラスタでセルフホストする場合、Kubernetesに大規模デプロイする場合、クラウドサービスを利用する場合でも、Grafanaはシステムを健全に保つために必要な柔軟性と深みを提供します。その強力なコミュニティ、活発な開発、そして広範なプラグインエコシステムにより、現代のDevOpsおよびSREツールキットにおいて不可欠なツールとなっています。

---

> **詳細情報**
>
> - 公式ドキュメント: [https://grafana.com/docs/](https://grafana.com/docs/)
> - コミュニティフォーラム: [https://community.grafana.com/](https://community.grafana.com/)
> - Grafana Play（ライブデモ）: [https://play.grafana.org/](https://play.grafana.org/)
> - Grafana Labsブログ: [https://grafana.com/blog/](https://grafana.com/blog/)