---
title: HAProxy
description: HAProxyは、高性能なオープンソースのTCP/HTTPロードバランサー兼リバースプロキシであり、モダンな分散システムに極めて高い信頼性、パフォーマンス、および制御を提供します。
created: 2026-06-17
tags:
  - load-balancer
  - proxy
  - tcp
  - http
  - haproxy
  - devops
status: draft
---

# HAProxy

HAProxy（High Availability Proxy）は、デファクトスタンダードのオープンソースTCP/HTTPロードバランサー兼プロキシサーバーです。Willy Tarreau氏によってC言語で書かれており、非常に高いパフォーマンス、信頼性、そして最小限のメモリフットプリントでバックエンドサーバーにトラフィックを分散するために設計されています。HAProxyは、GitHub、Reddit、Twitter/X、Docker Hubなど、インターネット上で最もトラフィックの多いWebサイトやサービスの多くを支えています。

## HAProxyとは？

HAProxyは、無料で非常に高速かつ信頼性の高いリバースプロキシであり、TCPおよびHTTPベースのアプリケーションに対して高可用性、ロードバランシング、およびプロキシ機能を提供します。Linux、macOS、FreeBSDで動作します。最も一般的な用途は、複数のサーバー（Web、アプリケーション、データベースなど）にワークロードを分散することで、サーバー環境のパフォーマンスと信頼性を向上させることです。基本的なロードバランシングに加えて、HAProxyは高度なトラフィック管理、SSL/TLS終端、コンテンツスイッチング、ヘルスチェック、セッション永続性、深い可観測性、そしてレート制限やプロトコル強化などのセキュリティ機能を提供します。

## HAProxyを選ぶ理由

現代のインフラストラクチャでは、サービスはゼロダウンタイムで数百万の同時接続を処理する必要があります。NginxやApacheのような汎用Webサーバーもロードバランサーとして機能できますが、HAProxyは**この役割のために特別に設計**されています。以下の点で優れています：

- **パフォーマンス:** イベント駆動型のシングルスレッド（またはマルチスレッド）アーキテクチャにより、控えめなハードウェアでも数百万の同時接続を処理できます。
- **信頼性:** 積極的なサニティチェックを備えて構築されており、不可能な条件や無限ループは即座にダンプ付きでクラッシュし、無言のデータ破損を防ぎます。
- **機能セット:** ネイティブのSSL終端、HTTP/2、gRPC、QUIC/HTTP/3、高度なACL、スティックテーブル、Prometheusメトリクス、シームレスなリロード。
- **セキュリティ:** スローリーディス攻撃、DDoS、プロトコルレベルのエクスプロイトからバックエンドを保護します。

## インストール

HAProxyはほとんどのパッケージリポジトリで利用可能であり、Dockerを介して実行することも、カスタムビルドのためにソースからコンパイルすることもできます。

### 公式リポジトリから

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install haproxy

# RHEL / CentOS / Fedora
sudo yum install haproxy

# Alpine
apk add haproxy

# FreeBSD
pkg install haproxy
```

### Dockerを使用する

```bash
docker run --name my-haproxy \
  -v /path/to/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro \
  -p 80:80 \
  -p 443:443 \
  haproxy:lts
```

### ソースからコンパイル（カスタム機能向け）

```bash
# Install build dependencies (example for Debian)
sudo apt install build-essential libssl-dev libpcre3-dev zlib1g-dev liblua5.3-dev

# Download and build
wget https://www.haproxy.org/download/3.0/src/haproxy-3.0.0.tar.gz
tar xzf haproxy-3.0.0.tar.gz
cd haproxy-3.0.0
make TARGET=linux-glibc USE_OPENSSL=1 USE_PCRE=1 USE_ZLIB=1 USE_LUA=1
sudo make install
```

## 基本設定

HAProxyの設定は単一のテキストファイル（通常は `/etc/haproxy/haproxy.cfg`）に記述します。ファイルは論理的なセクションで構成されています：

| Section     | Purpose                                                  |
|-------------|----------------------------------------------------------|
| `global`    | プロセス全体の設定（ユーザー、グループ、最大接続数、統計ソケット）。 |
| `defaults`  | すべてのフロントエンド/バックエンドで共有されるパラメータ（モード、タイムアウト、ログオプション）。 |
| `frontend`  | トラフィックのエントリポイント：IP/ポートバインディング、ACL、デフォルトのバックエンドを定義。 |
| `backend`   | トラフィックを転送するサーバーのプール。ロードバランシングアルゴリズム、ヘルスチェック、永続性を定義。 |
| `listen`    | シンプルなセットアップのためにフロントエンドとバックエンドを組み合わせた便利なラッパー。 |

### 例：シンプルなHTTPロードバランサー

```cfg
global
    maxconn 4096
    user haproxy
    group haproxy

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms
    option httplog

frontend http-in
    bind *:80
    default_backend webservers

backend webservers
    balance roundrobin
    server web1 192.168.1.10:80 check
    server web2 192.168.1.11:80 check
```

### 例：TCPロードバランサー（例：MySQL）

```cfg
frontend mysql-in
    bind *:3306
    mode tcp
    default_backend mysql_servers

backend mysql_servers
    mode tcp
    balance leastconn
    server db1 10.0.0.1:3306 check
    server db2 10.0.0.2:3306 check
```

### 統計ページの有効化

```cfg
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 10s
    # optionally restrict access
    stats auth admin:password
```

## 主要機能とコマンド例

### 1. ロードバランシングアルゴリズム

HAProxyは多数のバランシングアルゴリズムをサポートしています。最も一般的なものは次のとおりです：

| Algorithm          | Description                                             |
|--------------------|---------------------------------------------------------|
| `roundrobin`       | リクエストをサーバーに順番に分散します。       |
| `leastconn`        | 最も接続数の少ないサーバーにリクエストを送信します。   |
| `source`           | ソースIPをハッシュ化し、クライアントが常に同じサーバーに接続されるようにします（永続性に便利）。 |
| `uri`              | リクエストURIをハッシュ化し、キャッシュ設定に便利です。      |
| `hdr(name)`        | ヘッダーの値をハッシュ化します（例：`X-Session-ID`）。    |

設定例：

```cfg
backend webservers
    balance hdr(host)
    server web1 192.168.1.10:80 check
    server web2 192.168.1.11:80 check
```

### 2. ヘルスチェック

アクティブヘルスチェックは、各サーバー行に `check` キーワードを追加して設定します。細かい調整も可能です：

```cfg
server web1 192.168.1.10:80 check inter 2s fall 3 rise 2
# inter    – check interval
# fall     – number of failures before marking server down
# rise     – number of successes before marking server up
```

HTTPバックエンドにはレイヤ7チェック（`option httpchk`）も使用できます：

```cfg
backend webservers
    option httpchk HEAD /health HTTP/1.1\r\nHost:\ localhost
    server web1 192.168.1.10:80 check
```

### 3. SSL/TLSオフローディング

ロードバランサーでHTTPSを終端し、バックエンドには平文のHTTPを転送します：

```cfg
frontend https-in
    bind *:443 ssl crt /etc/ssl/certs/example.pem
    default_backend webservers

backend webservers
    server web1 192.168.1.10:80 check
```

バックエンドへの再暗号化（SSLブリッジ）やクライアント証明書の検証も可能です。

### 4. ACLを使用したコンテンツスイッチング

ACLを使用して、ヘッダー、URLパス、TLS SNIなどに基づいてトラフィックをルーティングします。

```cfg
frontend http-in
    bind *:80

    # Define ACLs
    acl is_api path_beg /api/
    acl is_static path_end .jpg .png .css .js

    # Use ACLs to choose backend
    use_backend api_servers if is_api
    use_backend static_servers if is_static
    default_backend webservers
```

### 5. セッション永続性（スティッキネス）

ユーザーのリクエストが常に同じバックエンドサーバーに送られるようにします：

```cfg
backend webservers
    balance roundrobin
    cookie SERVERID insert indirect nocache
    server web1 192.168.1.10:80 check cookie w1
    server web2 192.168.1.11:80 check cookie w2
```

または、IPやヘッダーに基づいた `stick-table` 永続性も使用できます。

### 6. ゼロダウンタイムリロード

接続を切断せずに設定変更を適用します：

```bash
haproxy -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid -sf $(cat /run/haproxy.pid)
```

またはsystemd経由：

```bash
systemctl reload haproxy
```

## 高度な機能

### レート制限

```cfg
frontend http-in
    bind *:80

    # Allow 10 requests per second per IP, burst to 20
    stick-table type ip size 1m expire 10s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 20 }
    default_backend webservers
```

### HTTP/2とgRPC

HAProxyはHTTP/2をサポートしており、`alpn` を有効にするだけで特別な設定なしでgRPCをプロキシできます：

```cfg
frontend https-in
    bind *:443 ssl crt /etc/ssl/certs/example.pem alpn h2,http/1.1
    default_backend grpc_servers

backend grpc_servers
    server grpc1 10.0.0.1:50051 check
```

### QUIC / HTTP/3

最近のバージョン（≥2.5）では、UDPベースのHTTP/3のために実験的なQUICサポートが含まれています：

```cfg
frontend quic-in
    bind quic4@:443 ssl crt /etc/ssl/certs/example.pem
    default_backend webservers
```

### 可観測性

- **統計ページ：** 組み込みのHTML/JSONエンドポイント（前述の例を参照）。
- **Prometheusメトリクス：** `stats prometheus` オプションを使用：

```cfg
frontend stats
    bind *:8405
    stats enable
    stats uri /metrics
    stats prometheus
```

- **生ログ：** HAProxyは詳細なログ（syslogまたは個別のログファイルに）を出力し、`tail` や `grep` などのツールで分析したり、ELK/Lokiに送信したりできます。

## コマンドライン管理

HAProxyは、UnixソケットまたはTCPソケットを介してリッチなランタイムAPIを提供します。コマンドを送信するには、`socat` ユーティリティが一般的に使用されます：

```bash
echo "show info" | socat stdio unix-connect:/run/haproxy.sock
echo "show stat" | socat stdio unix-connect:/run/haproxy.sock
echo "enable server webservers/web1" | socat stdio unix-connect:/run/haproxy.sock
```

ランタイムAPIは動的なサーバーの追加/削除もサポートしており、これはコンテナ環境にとって重要です。

## セキュリティに関する考慮事項

- **非rootで実行：** HAProxyはポートバインド後に権限をドロップします。`global` セクションの `user` および `group` ディレクティブは必須です。
- **chrootを有効にする：** `chroot /var/lib/haproxy` を設定して、プロセスをファイルシステムから隔離します。
- **統計を制限する：** 認証、ACLを使用するか、統計をプライベートインターフェースにバインドします。
- **タイムアウトの調整：** 低速なクライアントが接続プールを枯渇させるのを防ぎます。
- **SYNフラッド保護を有効にする：** `tcp-smart-connect` および `tcp-smart-accept` オプションを使用します。

## まとめ

HAProxyは、成熟した実戦で試されたコンポーネントであり、多くの高トラフィックで重要なシステムのバックボーンを形成しています。ロードバランシングとプロキシに焦点を絞ることで、比類のないパフォーマンス、安定性、そしてきめ細かな制御を提供します。小さなブログを運営している場合でも、世界中に展開するSaaSを運営している場合でも、HAProxyはインフラエンジニアのツールキットに不可欠なツールです。

詳細については、[公式HAProxyドキュメント](https://www.haproxy.org/documentation/)または[HAProxy Technologiesサイト](https://www.haproxy.com/)を参照してください。