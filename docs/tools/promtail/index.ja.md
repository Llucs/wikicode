---
title: Promtail - ログシッパーのための Prometheus
description: Promtailは、さまざまなソースからログを収集し、Prometheusサーバーやその他の互換性のあるストレージシステムに転送するための軽量で柔軟な、および高度にカスタマイズ可能なロギング・シッパーです。
created: 2026-06-26
tags:
  - logging
  - prometheus
  - grafana
status: draft
---

# Promtail - ログシッパーのための Prometheus

PromtailはPrometheus用のログシッパーであり、Grafana Labsによって開発および維持されています。これは、さまざまなソースからログを収集し、Prometheusサーバーやその他の互換性のあるストレージシステムに転送するための軽量で柔軟で、高度にカスタマイズ可能なツールです。

## キー機能

1. **ハイアビリティと障害耐性**: Promtailは、失敗を優雅に処理できるように設計されています。失敗したログエントリの自動リトライをサポートし、ログエントリの再処理のための構成をサポートしています。
2. **柔軟性**: PromtailはJSON、syslog、plain textなど、さまざまなログ形式をサポートしており、ログから関連情報を抽出するために規則表現を使用して構成できます。
3. **スケーラビリティ**: Promtailは高頻度のログ処理を最適化しており、大量のデータを効率的に処理できます。
4. **セキュリティ**: TLSをサポートしており、PromtailとPrometheusサーバー間の通信を安全にします。
5. **構成**: 設定はYAMLファイルに保存され、管理と維持が容易です。
6. **統合**: Promtailは既存のログインフラストラクチャと容易に統合でき、多くのログシステムと互換性があります。

## 歴史

Promtailは2018年にGrafana Labsプロジェクトの一環として最初に導入されました。これは、Prometheusモニタリングシステムと統合するための軽量で効率的なログシッパーを提供することによって開発されました。数年間、Promtailは信頼性の高い広く使用されているツールとして発展しました。

## 使用例

1. **アプリケーションログ**: Promtailはサーバー、コンテナなどからアプリケーションログを収集し、Prometheusに転送してモニタリングとアラートを実施することができます。
2. **セキュリティ監視**: ログデータを収集および解析することで、Promtailはセキュリティ侵害、異常、その他のセキュリティ関連のイベントを検出できます。
3. **診断サポート**: 生産システムの問題を診断するための詳細なログを提供し、トラブルシューティングに分析できます。
4. **コンプライアンス**: ログデータを規制要件に適合するように収集および保存するためにPromtailを使用できます。
5. **監視**: PromtailはPrometheusとの統合により、ログをリアルタイムで監視し、ログデータに基づくアラートを実施できます。

## インストール

### 前提条件
- Go (ソースからビルドするため)
- Docker (コンテナ化インストールのため)

### ソースからビルド
1. **リポジトリクローン**:
   ```sh
   git clone https://github.com/grafana/promtail.git
   cd promtail
   ```

2. **バイナリビルド**:
   ```sh
   make build
   ```

3. **Promtailを実行**:
   ```sh
   ./promtail
   ```

### Dockerインストール
1. **Dockerイメージをプル**:
   ```sh
   docker pull grafana/promtail
   ```

2. **DockerでPromtailを実行**:
   ```sh
   docker run -d --name promtail \
     -v /path/to/config.yml:/promtail/promtail.yml \
     grafana/promtail -config.file=/promtail/promtail.yml
   ```

## 基本的な使用方法

### Promtailの構成
PromtailはYAML構成ファイルを使用してログソース、パースルール、および出力先を指定します。以下は例の構成です：

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://localhost:9091/log

scrape_configs:
  - job_name: server
    static_configs:
      - targets:
          - localhost
        labels:
          job: server
```

### Promtailを実行
構成ファイルが設定されたら、Promtailを実行してログを収集することができます。

```sh
promtail -config.file=/path/to/config.yml
```

### ログの監視
Promtailは収集されたログを指定されたPrometheusサーバーに転送します。その後、Prometheusを使用してログデータをクエリおよび可視化することができます。

## 結論

PromtailはPrometheusへのログデータの収集と転送のための強力なツールであり、モニタリングとアラートの統合をスムーズに行うことができます。その柔軟性と使いやすさは、ログとモニタリングインフラストラクチャにとって価値のある追加機能となります。

---