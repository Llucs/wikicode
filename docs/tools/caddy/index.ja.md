---
title: Caddy: 自動HTTPSを備えた究極のWebサーバー
description: エンタープライズ対応のオープンソースWebサーバーで、自動HTTPS、リバースプロキシ、Dockerサポートを備え、Goで書かれています。
created: 2026-06-16
tags:
  - web-server
  - reverse-proxy
  - automatic-https
  - go
  - docker
  - open-source
status: draft
---

# Caddy

Caddyは、Goで書かれた強力でエンタープライズ対応のオープンソースWebサーバーおよびリバースプロキシです。シンプルに使用できるように設計されながら、堅牢なセキュリティ、自動TLS証明書管理、そしてモダンな設定APIを提供します。CaddyはCaddy Foundationによってメンテナンスされており、開発環境と本番環境の両方で広く採用されています。

## 主な機能

- **自動HTTPS**: Caddyは設定されたすべてのドメインに対してLet's EncryptまたはZeroSSLからTLS証明書を自動的に取得して更新します。OCSPステープリング、HTTP/2、HTTP/3 (QUIC) を標準で管理します。
- **シンプルな設定**: 親しみやすい `Caddyfile` または強力なJSON APIを使用して動的設定が可能です。`Caddyfile` はJSONに変換するアダプターであり、シンプルさと柔軟性を提供します。
- **リバースプロキシ＆ロードバランシング**: アクティブ/パッシブヘルスチェック、リトライ、サーキットブレーカー、および複数のロードバランシングポリシー（ランダム、最小接続数、IPハッシュ、ヘッダーアフィニティ）を備えた完全なレイヤー7リバースプロキシ。
- **デフォルトでのセキュリティ**: メモリセーフなGoで書かれており、バッファオーバーフローの脆弱性を排除。TLSのデフォルトは厳格に安全で、Caddyは必要な場合にのみ特権ポートでリッスンします。
- **モジュラーアーキテクチャ**: コアは最小限で、モジュールによって機能が拡張されます。`xcaddy` を使用して必要な機能のみを含むカスタムバイナリをビルドできます。
- **コンテナネイティブ**: 単一バイナリ、クリーンなシャットダウン、グレースフルリロード – DockerおよびKubernetesに最適。

## なぜCaddyを使うのか？

Caddyは手動でのHTTPS設定の面倒を排除します。証明書を自動的にプロビジョニングおよび更新するため、TLSの有効期限切れを心配する必要がありません。設定は直感的で、マイクロサービス、静的サイト、API、SPAの完璧なフロントエンドとして機能します。JSON APIは自動化ツールとのシームレスな統合を可能にし、`Caddyfile`は人間に優しい代替手段を提供します。一度書けば、どこでも安全に配信できます。

## インストール

Caddyは複数のインストール方法を提供しています:

### プリビルドバイナリのダウンロード

```bash
# Linux / macOS / Windows binary
curl -fsSL https://caddyserver.com/download/linux/amd64 -o caddy
chmod +x caddy
sudo mv caddy /usr/local/bin/
```

*または [caddyserver.com/download](https://caddyserver.com/download) からダウンロード*

### パッケージマネージャー

```bash
# Debian / Ubuntu
sudo apt install caddy

# macOS
brew install caddy

# Windows (winget)
winget install Caddy.Caddy
```

### Docker

```bash
docker pull caddy
```

### `xcaddy` を使用したカスタムビルド

```bash
# Build Caddy with a specific plugin
xcaddy build --with github.com/caddyserver/transform-encoder

# Build with a custom version
xcaddy build v2.8.0 --with github.com/caddyserver/format-encoder
```

`xcaddy` は必要なモジュールのみを含む単一のバイナリをコンパイルします。

## 基本的な使い方

### 静的ファイルサーバー

```bash
# Serve the current directory on port 80 with automatic HTTPS
caddy file-server
```

### クイックリバースプロキシ

```bash
# Proxy traffic from yourdomain.com to a local backend
caddy reverse-proxy --from yourdomain.com --to localhost:8080
```

### Caddyfile 設定

プロジェクトルートに `Caddyfile` を作成します:

```caddyfile
example.com {
    root * /var/www/example
    file_server
}
```

次に実行します:

```bash
caddy run
```

Caddyは自動的に `example.com` のTLS証明書を取得し、静的ファイルを提供します。

### JSON 設定

Caddyのネイティブな設定形式はJSONです。管理APIを介して適用できます:

```bash
caddy run

# In another terminal, POST the configuration
curl -X POST -H "Content-Type: application/json" -d '{
  "apps": {
    "http": {
      "servers": {
        "example": {
          "listen": [":443"],
          "routes": [
            {
              "match": [{"host": ["example.com"]}],
              "handle": [
                {
                  "handler": "subroute",
                  "routes": [
                    {
                      "handle": [
                        {"handler": "file_server", "root": "/var/www/example"}
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      }
    }
  }
}' http://localhost:2019/config/
```

JSON APIが信頼できる情報源です。`Caddyfile` は単なるアダプターです。

## 主要機能の詳細

### 自動HTTPS

```caddyfile
mydomain.com {
    tls you@email.com   # Let's Encrypt通知用のオプションのメール
}
```

Caddyは証明書の発行、更新、HTTPからHTTPSへのリダイレクトを自動的に処理します。ワイルドカード証明書、カスタムACMEエンドポイント（例: ZeroSSL）、オンデマンドTLSをサポートしています。

### リバースプロキシとロードバランシング

```caddyfile
api.example.com {
    reverse_proxy api1:8080 api2:8080 api3:8080 {
        lb_policy least_conn
        health_uri /health
        health_interval 10s
    }
}
```

ポリシー: `random`、`least_conn`、`ip_hash`、`uri_hash`、`header`、`first`、`round_robin`。

### テンプレートと動的サイト

Caddyは別のバックエンドなしで動的コンテンツのテンプレートを実行できます:

```caddyfile
example.com {
    templates
    root * /var/www/example
}
```

### 認証

モジュラー認証（例: JWT、ベーシック認証）はプラグイン経由で追加できます:

```caddyfile
example.com {
    basic_auth {
        admin $2a$14$hash...
    }
}
```

### HTTP/3 (QUIC)

`Caddyfile` でHTTP/3を有効にする:

```caddyfile
{
    servers {
        protocol {
            quic
        }
    }
}
```

## Docker との統合

Caddyはコンテナ環境において第一級のサポートを提供します。

### Dockerコンテナから静的ファイルを提供する

```dockerfile
FROM caddy:latest
COPY . /usr/share/caddy
```

次のコマンドで実行:

```bash
docker build -t my-site .
docker run -d -p 80:80 -p 443:443 -e CADDY_INGRESS_NETWORKS=caddy my-site
```

### Docker Composeでリバースプロキシとして使用する

```yaml
version: "3.8"
services:
  caddy:
    image: caddy:latest
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
  app:
    image: my-app:latest
    expose:
      - "8080"
```

**Caddyfile**:

```caddyfile
mydomain.com {
    reverse_proxy app:8080
}
```

CaddyはDockerネットワーキングを介して自動的に `app` コンテナを検出します。

### Dockerでのグレースフルリロード

```bash
# After changing the Caddyfile, reload without downtime
docker exec -w /etc/caddy <container_name> caddy reload
```

## ライフサイクル管理

```bash
# Run in foreground
caddy run

# Run as background daemon
caddy start

# Stop the daemon
caddy stop

# Gracefully reload configuration (Linux)
caddy reload

# Validate a Caddyfile
caddy validate
```

## まとめ

CaddyはHTTPSを自動化し、クリーンな設定モデルを提供し、最新のスタックとシームレスに統合することでWebサーバー運用を簡素化します。静的サイト、マイクロサービスのバックエンド、あるいは本格的なAPIゲートウェイをデプロイする場合でも、Caddyはセキュリティ、パフォーマンス、使いやすさを単一のバイナリで提供します。強力なDockerサポートと活気あるプラグインエコシステムにより、開発者と運用チームの両方にとって優れた選択肢です。