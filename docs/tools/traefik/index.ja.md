---
title: Traefik – クラウドネイティブ環境のための動的リバースプロキシおよびロードバランサー
description: Traefikは、Docker、Kubernetes、その他のインフラストラクチャバックエンドにおいて、サービスを自動検出してルーティングを設定するクラウドネイティブなHTTPリバースプロキシ兼イングレスコントローラです。
created: 2026-06-16
tags:
  - reverse-proxy
  - load-balancer
  - traefik
  - docker
  - kubernetes
  - cloud-native
status: draft
---

# Traefik – エッジルーター、リバースプロキシ & ロードバランサー

## Traefikとは？

[Traefik](https://traefik.io/traefik/)（「トラフィック」と発音）は、最新のコンテナ化されたクラウドネイティブアーキテクチャ向けに設計された**オープンソースのHTTPリバースプロキシおよびロードバランサー**です。Goで書かれており、アプリケーションネットワークの単一エントリポイントとして機能し、HTTP、HTTPS、TCP、UDP、gRPCトラフィックを適切なバックエンドサービスに動的にルーティングします。

Traefikの最も特徴的な点は、**自動サービスディスカバリ**です。手動で保守する設定ファイル（`nginx.conf`など）を必要とする代わりに、Traefikはオーケストレーションレイヤー（Docker、Kubernetes、Nomad、Consulなど）をリッスンし、サービスが起動、停止、スケーリングされる際にルーティングルールを**自動構成**します。これにより、プロキシのリロードや再起動を必要とせず、ダウンタイムゼロでトポロジの変更が可能です。

Traefikは**Cloud Native Computing Foundation (CNCF) の卒業プロジェクト**（2022年以降）であり、API管理、APIゲートウェイ、AIゲートウェイ機能で拡張するTraefik Hubプラットフォームの中核です。現在のメジャーバージョンである**Traefik v3**（2024年リリース）では、ネイティブHTTP/3サポート、Kubernetes向けGateway API統合、拡張されたプラグインシステムが導入されました。

## Traefikを使う理由

| 課題 | Traefikの答え |
|-----------|------------------|
| 動的環境における手動プロキシ設定 | **自動ディスカバリ** – サービスはラベルまたはCRDを介して登録され、手動設定の更新は不要。 |
| SSL/TLS証明書管理のオーバーヘッド | **自動TLS** – HTTPまたはDNSチャレンジをサポートする組み込みACMEクライアント（Let's Encrypt、ZeroSSL）。 |
| DockerとKubernetes間で統一されたエントリポイントの必要性 | **マルチプロバイダーサポート** – Docker、Swarm、Kubernetes、Consulなどのサービスを同時に集約可能。 |
| 複雑なルーティングロジック（カナリアリリース、A/Bテスト、レート制限） | **ミドルウェアパイプライン** – レート制限、認証、ヘッダー操作などから構成可能なチェーン。 |
| 可観測性とデバッグ | **豊富なメトリクス**（Prometheus、Datadog）、**トレーシング**（OpenTelemetry、Jaeger）、**構造化アクセスログ**。 |
| 開発者体験 | **ライブダッシュボード** – ルーター、サービス、ミドルウェアを可視化するWeb UI。再起動なしのホットリロードも可能。 |

## インストール

Traefikは軽量で単一のバイナリとして実行されます。最も一般的な方法は、コンテナデプロイメントとKubernetes用のHelmチャートです。

### Docker（シングルノード）

```bash
docker run -d -p 80:80 -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name traefik \
  traefik:v3.0
```

上記のコマンドはDockerソケットをマウントし、Traefikがコンテナを検出できるようにします。ポート80はHTTPエントリポイント、ポート8080はダッシュボードを提供します。

### Kubernetes（Helmチャート）

```bash
helm repo add traefik https://traefik.github.io/charts
helm upgrade --install traefik traefik/traefik \
  --namespace traefik --create-namespace
```

このチャートは、サービスロードバランサー、RBAC、オプションのメトリクスを含む適切なデフォルト設定で、TraefikをIngress Controllerとしてデプロイします。

### バイナリ（Linux）

```bash
# Download the latest release (check for actual version)
wget https://github.com/traefik/traefik/releases/download/v3.0.0/traefik_v3.0.0_linux_amd64.tar.gz
tar -xzf traefik_v3.0.0_linux_amd64.tar.gz
./traefik --configFile=traefik.yml
```

## 主な機能

### 1. 自動サービスディスカバリ

Traefikは幅広い**プロバイダー**と統合します。

- Docker / Docker Swarm
- Kubernetes (Ingress, IngressRoute CRD, Gateway API)
- Consul, Consul Connect
- etcd, ZooKeeper
- Nomad
- Rancher, Amazon ECS, Marathon, etc.

ルートはラベル（Docker）またはカスタムリソース（Kubernetes）から動的に生成され、静的設定は不要です。

### 2. ミドルウェアパイプラインによる動的設定

Traefik v2/v3は、**静的設定**（エントリポイント、プロバイダー、ログ）と**動的設定**（ルーター、ミドルウェア、サービス）の明確な分離を強制します。ミドルウェアはプラグイン可能なチェーンコンポーネントで、リクエスト/レスポンスを変更します。

- **認証**: BasicAuth, DigestAuth, ForwardAuth
- **セキュリティ**: IPAllow/Deny、RedirectScheme、RedirectRegex、Headersカスタマイズ
- **トラフィック管理**: RateLimit、InFlightReq、CircuitBreaker、Retry
- **プロトコル処理**: AddPrefix、StripPrefix、ReplacePath
- **変換**: Buffering、ErrorPage、Compress

ミドルウェア定義の例（動的）：

```yaml
http:
  middlewares:
    rate-limit:
      rateLimit:
        average: 100
        burst: 200
```

### 3. ACMEによる自動TLS

Traefikには、証明書のプロビジョニングと更新を自動化する組み込みACMEクライアントが含まれています。

```yaml
# Static config (traefik.yml)
certificatesResolvers:
  letsencrypt:
    acme:
      email: admin@example.com
      storage: /acme.json
      httpChallenge:
        entryPoint: web
```

設定後、ルーターはリゾルバーを参照できます。

```yaml
# Dynamic config (file or label)
http:
  routers:
    api:
      rule: Host(`api.example.com`)
      tls:
        certResolver: letsencrypt
```

Traefikは手動介入なしに証明書を自動的に取得および更新します。

### 4. ネイティブHTTP/3（QUIC）

Traefik v3はHTTP/3を標準でサポートしています。エントリポイントで有効にします。

```yaml
entryPoints:
  websecure:
    address: ":443"
    http3: {}
```

HTTP/3をサポートするクライアント（例：最新のブラウザ）は、より高速なQUICプロトコルを自動的にネゴシエートします。

### 5. 可観測性

| 機能 | 統合先 |
|---------|-------------|
| メトリクス | Prometheus, Datadog, StatsD, InfluxDB, OpenTelemetry |
| トレーシング | OpenTelemetry, Jaeger, Zipkin, Instana |
| アクセスログ | Structured JSON or Common Log Format |
| ヘルスチェック | TCP, HTTP with custom intervals and conditions |

### 6. ダッシュボード

Traefikは、すべてのルーター、サービス、ミドルウェア、エントリポイントをリアルタイムで表示するWebダッシュボードを提供します。静的設定で有効にします。

```yaml
api:
  dashboard: true
  debug: true
```

その後、`http://<traefik-ip>:8080/dashboard/` にアクセスします。

### 7. トラフィック分割とカナリアデプロイメント

サービス間の重み付きラウンドロビン：

```yaml
http:
  services:
    api-canary:
      weighted:
        services:
          - name: api-v1
            weight: 90
          - name: api-v2
            weight: 10
```

### 8. プラグインシステム

Traefik v3は、ミドルウェア、プロバイダー、さらにはカスタムロジックを拡張するために、Goで書かれたカスタムプラグイン（プラグインカタログ経由）をサポートしています。プラグインはプラグインレジストリを通じて配布され、起動時にロードできます。

## 使用例

### Dockerクイックスタート（whoamiサービスを使用）

静的設定ファイル `traefik.yml` を作成します。

```yaml
api:
  dashboard: true

entryPoints:
  web:
    address: ":80"

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
```

Traefikを実行：

```bash
docker run -d -p 80:80 -p 8080:8080 \
  -v $(pwd)/traefik.yml:/etc/traefik/traefik.yml \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name traefik \
  traefik:v3.0
```

ラベルを使用してバックエンドサービスを起動：

```bash
docker run -d --name whoami \
  -l "traefik.enable=true" \
  -l "traefik.http.routers.whoami.rule=Host(\`whoami.localhost\`)" \
  -l "traefik.http.routers.whoami.entrypoints=web" \
  traefik/whoami
```

ルーティングをテスト：

```bash
curl -H "Host: whoami.localhost" http://localhost
```

whoamiレスポンスが返され、動的ルーティングが機能したことを確認できます。**プロキシのリロードは不要です。**

### Kubernetes IngressRoute（CRD）

Traefikのカスタムリソース`IngressRoute`は、標準のKubernetes Ingressよりも豊富な設定を提供します。

```yaml
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: webapp
spec:
  entryPoints:
    - web
  routes:
    - kind: Rule
      match: Host(`webapp.example.com`)
      services:
        - name: webapp-svc
          port: 80
      middlewares:
        - name: auth
---
apiVersion: traefik.containo.us/v1alpha1
kind: Middleware
metadata:
  name: auth
spec:
  basicAuth:
    secret: webauth
```

`IngressRoute`はTraefikのKubernetesプロバイダーによって自動的に検出され、すぐにアクティブになります。

## アーキテクチャ: 静的設定と動的設定

```
+-------------------+       +-----------------------+
|   Static Config   |       |   Dynamic Config      |
|  (traefik.yml)    |       |  (labels, CRDs, KV)   |
|                   |       |                       |
| - entryPoints     |       | - routers             |
| - providers       |       | - middlewares         |
| - logging         |       | - services            |
| - metrics         |       | - TLS options         |
| - plugins         |       | - etc.                |
+-------------------+       +-----------------------+
          |                           |
          |  Loaded at startup        |  Continuously watched
          |  (must restart to change) |  (hot-reloaded)
          v                           v
    +---------------------------------------+
    |        Traefik Proxy Engine            |
    |  (watches dynamic provider events)     |
    +---------------------------------------+
```

この分離により、共通のインフラストラクチャ設定（エントリポイント、プロバイダー）は安定し、ルーティングはサービスのスケーリングに応じて流動的に変更できます。

## Traefikを使うべきタイミング（代替案との比較）

| ユースケース | Traefikが優れる理由 |
|----------|-------------------|
| **Docker Compose開発** | ゼロ設定 – ラベルを追加するだけで、`nginx.conf`は不要。 |
| **複雑なルーティングを伴うKubernetes** | `IngressRoute` CRDにより、ミドルウェアチェーン、トラフィック分割、カスタムTLSを容易に実現。 |
| **ホームラボ / セルフホスティング** | Let's Encryptによるワイルドカード証明書の自動TLS、シンプルなUI。 |
| **サービスメッシュエッジプロキシ** | サービスメッシュ（例：Linkerd、Consul Connect）のイングレスゲートウェイとして機能。 |
| **マルチクラスター / ハイブリッドクラウド** | 異なるプロバイダー（Docker + K8s + Consul）のサービスを単一のエッジに集約可能。 |

## まとめ

Traefikは、ニッチなDockerプロキシから成熟したCNCF卒業のイングレスコントローラおよびエッジルーターへと進化しました。その特徴は、手動プロキシ設定を不要にする**自動・リアルタイムのサービスディスカバリ**であり、動的なコンテナベースのデプロイメントに最適です。HTTP/3のサポート、強力なミドルウェアシステム、自動TLS、深い可観測性により、Traefikは、インフラストラクチャに適応する堅牢で使いやすいリバースプロキシを求める開発者や運用者にとって最良の選択肢です。

---

### リソース

- [公式ドキュメント](https://doc.traefik.io/traefik/)
- [GitHubリポジトリ](https://github.com/traefik/traefik)
- [Traefik Hub（マネージドAPI管理アドオン）](https://traefik.io/traefik-hub/)
- [プレイグラウンド / デモ](https://play.traefik.io/)