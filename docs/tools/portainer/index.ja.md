---
title: Portainer
description: 複数の環境にわたるガバナンス、RBAC/SSO、および運用管理を一元化する、セルフホスト型のコンテナおよびオーケストレーション管理ツール。
created: 2026-06-15
tags:
  - docker
  - kubernetes
  - container-management
  - devops
  - open-source
  - orchestration
  - self-hosted
  - portainer-ce
status: draft
ecosystem: containers
---

# Portainer

## 概要

Portainer は、コンテナ化環境を管理するための業界標準のオープンソース「単一の管理画面」です。Neil Cresswell によって設計され、2017 年に DockerUI からフォークされた Portainer は、Docker、Docker Swarm、Kubernetes、Azure ACI、Hashicorp Nomad の急な学習曲線と運用オーバーヘッドを排除することを目的としています。Portainer 自体は軽量コンテナとして（または Helm チャートを介して）実行され、完全な機能を備えた REST API によって支えられた強力な Web UI を公開します。

Portainer は、コミュニティエディション（CE）では AGPLv3 のライセンスが適用され、商用のビジネスエディション（BE）では FIPS 準拠、きめ細かい RBAC、専用サポートなどのエンタープライズ機能が追加されています。

## Portainer を選ぶ理由

- **統一管理画面：** CLI 間のコンテキストスイッチの代わりに、単一の Web インターフェースからフリート内のすべてのコンテナエンジンを管理します。
- **複雑さの軽減：** 専門外のチームでも、複雑な `kubectl` や `docker-compose` コマンドを学習することなく、アプリケーションのデプロイと管理が可能です。
- **GitOps 対応：** スタックを Git リポジトリに直接リンクできます。リポジトリへのプッシュは自動再デプロイをトリガーします。
- **エッジコンピューティング：** Edge Agent を使用して、NAT やファイアウォールの内側にある数千のデバイスを安全に管理します。
- **軽量で非侵入的：** Portainer は既存のオーケストレーターを置き換えるものではなく、その横に配置され、ソケットまたは専用の Agent コンテナを介して Docker/Kubernetes API を読み取ります。

## アーキテクチャ

Portainer は標準的なサーバー・エージェントモデルを使用します：

1.  **Portainer Server (portainer/portainer-ce):** メインアプリケーションです。Web UI と REST API を提供します。ブラウザでアクセスするノードです。
2.  **Portainer Agent (portainer/agent):** リモート管理するすべての Docker ホストまたは Kubernetes ノードにデプロイされる軽量のサイドカーコンテナです。Agent はローカルの Docker ソケットと通信し、ポート 9001 でセキュアな API を公開します。
3.  **Edge Agent:** リモートロケーション向けに設計された標準エージェントの変形です。Portainer Server への*アウトバウンド*トンネルを開始し、インバウンドポートを開くことなく厳格なファイアウォール越しの管理を可能にします。

```text
[Admin Browser] <--> [Portainer Server :9443]
                         |
            +------------+-------------+
            |            |             |
    [Docker Agent 1] [Docker Agent 2] [K8s Cluster (Helm)]
            |            |
    [Docker Daemon] [Docker Daemon]
```

## インストール

### Docker スタンドアロン（クイックスタート）

これは、ローカルまたは少数の Docker ホストを管理するための最も一般的な方法です。

```bash
# Create a persistent volume for Portainer data
docker volume create portainer_data

# Run the Portainer Server container
docker run -d -p 8000:8000 -p 9443:9443 --name portainer \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v portainer_data:/data \
    portainer/portainer-ce:lts
```

- `-p 9443:9443`: Web UI と API（HTTPS）。
- `-p 8000:8000`: （オプション）Edge Agent 接続用の TCP トンネル。
- `-v /var/run/docker.sock`: Portainer が実行中のホストを管理できるようにします。
- `:lts`: 長期サポートタグ。本番環境では**常に `:lts` を使用してください**。

### Docker Swarm

Portainer を Swarm クラスタ全体にグローバルサービスとしてデプロイします。

```bash
curl -L https://downloads.portainer.io/ce2-19/portainer-agent-stack.yml -o portainer-agent-stack.yml

docker stack deploy -c portainer-agent-stack.yml portainer
```

### Kubernetes（Helm）

公式 Helm チャートを使用して Portainer を Kubernetes クラスタにデプロイします。

```bash
helm repo add portainer https://portainer.github.io/k8s/
helm repo update

helm upgrade --install portainer portainer/portainer \
    --namespace portainer --create-namespace \
    --set service.type=LoadBalancer \
    --set service.httpPort=9000 \
    --set service.httpsPort=9443
```

### エアギャップインストール

インターネットアクセスのない環境向けに、イメージを事前にプルします。

```bash
# On a machine with internet access
docker pull portainer/portainer-ce:lts
docker pull portainer/agent:lts

# Tag and push to your internal registry
docker tag portainer/portainer-ce:lts <internal-registry>/portainer-ce:lts
docker tag portainer/agent:lts <internal-registry>/agent:lts
docker push <internal-registry>/portainer-ce:lts
docker push <internal-registry>/agent:lts
```

## 初期セットアップ

1.  ブラウザで `https://<SERVER_IP>:9443` を開きます。
2.  `admin` ユーザーの強力なパスワードを作成します。
3.  クイックセットアップウィザードが表示されます。**Docker** を選択し、**Socket** を選択してローカルの Docker デーモンに接続します。
4.  **Connect** をクリックします。**Home** ページに移動します。ここが環境セレクターです。

## 主な機能とコマンド例

### 1. マルチ環境管理

Portainer Agent をデプロイしてリモートの Docker ホストに接続します。

**リモートホスト（ターゲット）側：**
```bash
docker run -d -p 9001:9001 --name portainer_agent \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /var/lib/docker/volumes:/var/lib/docker/volumes \
    portainer/agent:lts
```

**Portainer Server UI 側：**
**Environments** > **Add Environment** > **Docker Agent** に移動します。リモートホストの IP とポート（9001）を入力し、**Connect** をクリックします。

### 2. アプリテンプレート（ワンクリックデプロイ）

Portainer には、事前定義されたアプリケーション（Nginx、MySQL、WordPress など）のカタログが含まれています。

**ワークフロー：**
1. サイドバー > **App Templates**。
2. テンプレート（例：**Nginx**）をクリックします。
3. 名前、ポート、環境変数をカスタマイズします。
4. **Deploy the stack** をクリックします。

### 3. スタックと GitOps

Docker Compose または Kubernetes マニフェストファイルを使用して複雑なアプリケーションをデプロイします。スタックは GitOps ワークフローのために Git リポジトリにリンクできます。

**手動 Compose デプロイ：**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
  db:
    image: postgres:13
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: example
volumes:
  pgdata:
```

**GitOps セットアップ：**
1. **Stacks** > **Add Stack** > **Repository** に移動します。
2. Git リポジトリの URL と Compose ファイルへのパスを入力します。
3. **Automatic Updates** を有効にします。
4. **Deploy the stack** をクリックします。`git push` が再デプロイをトリガーします。

### 4. Kubernetes 管理

Portainer は `kubectl` の複雑さを抽象化します。フォームまたは YAML を使用して Namespace、Deployment、Service、Ingress を作成できます。

**例：** シンプルな nginx ワークロードのデプロイ。
1. **Environments** > 使用する **Kubernetes cluster** を選択します。
2. **Kubernetes** > **Workloads** > **Add Workload** に移動します。
3. フォームに記入します（Name: `nginx`、Image: `nginx:alpine`、Port: `80`）。
4. **Deploy** をクリックします。

### 5. レジストリ

Docker Hub、GitLab、Quay、Amazon ECR、Google Container Registry の認証情報を一元管理します。

1. **Registries** > **Add Registry** に移動します。
2. プロバイダー（例：**Docker Hub**）を選択します。
3. 認証情報（ユーザー名/アクセストークン）を入力します。

### 6. エッジコンピューティング

NAT/ファイアウォールの内側にあるリモートデバイス（IoT、小売、フィールドサイト）を管理します。サーバーが `EDGE_ID` と `EDGE_KEY` を生成します。

**Edge デバイス側：**
```bash
docker run -d \
  -e EDGE=1 \
  -e EDGE_ID=<EDGE_ID> \
  -e EDGE_KEY=<EDGE_KEY> \
  -e CAP_HOST_MANAGEMENT=1 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name portainer_edge_agent \
  portainer/agent:lts
```

### 7. REST API

Portainer は豊富な REST API を備えています。**Settings** > **Security** で API キーを生成します。

```bash
# List all environments
curl -X GET 'https://<SERVER_IP>:9443/api/endpoints' \
    -H 'X-API-Key: ptr_xxxxxxxxxxxx' | jq .

# Deploy a stack
curl -X POST 'https://<SERVER_IP>:9443/api/stacks' \
    -H 'X-API-Key: ptr_xxxxxxxxxxxx' \
    -H 'Content-Type: application/json' \
    -d '{
      "Name": "my-api-stack",
      "StackFileContent": "version: \"3.8\"\nservices:\n  web:\n    image: nginx:alpine",
      "SwarmID": "",
      "EndpointID": 1
    }'
```

## エディションの比較

| 機能 | コミュニティエディション（CE） | ビジネスエディション（BE） |
|---|---|---|
| ライセンス | AGPLv3 | 商用 |
| マルチ環境 | 無制限 | 無制限 |
| GitOps | 対応 | 対応 |
| エッジコンピューティング | 制限あり | フル（Edge Groups、Stacks、Jobs） |
| RBAC / SSO | 基本 | 高度（AD/LDAP/OAuth、Team Roles、Resource Controls） |
| レジストリ管理 | 手動 | ガバナンスによる一元管理 |
| サポート | コミュニティ | 商用（24時間365日） |
| FIPS 準拠 | 非対応 | 対応 |

## ベストプラクティス

1. **`:lts` リリースを使用してください。** 本番環境では `:latest` タグを使用しないでください。これは最先端のビルドに対応します。
2. **サーバーノードを専用にします。** Portainer Server コンテナ上で多数のワークロードを実行しないでください。管理ポイントとしてのみ使用します。
3. **`portainer_data` を定期的にバックアップします。** 以下のコマンドでボリュームをバックアップします：
    ```bash
    docker run --rm -v portainer_data:/data -v $(pwd):/backup alpine tar cvf /backup/portainer_backup.tar /data
    ```
4. **適切な TLS でセキュリティを確保します。** 本番環境では自己署名証明書を置き換えます。
    ```bash
    docker run -d -p 9443:9443 --name portainer \
        -v /path/to/fullchain.pem:/certs/portainer.crt \
        -v /path/to/privkey.pem:/certs/portainer.key \
        -v portainer_data:/data \
        portainer/portainer-ce:lts
    ```

## トラブルシューティング

### Agent の接続障害
- ターゲットマシンでポート `9001` が開いていることを確認します。
- Portainer Agent コンテナが実行中であることを確認します。
- ファイアウォールを使用している場合は、サーバーが Agent へのアウトバウンド接続を開始できることを確認します。

### 管理者パスワードを忘れた場合
ヘルパーコンテナがハッシュを生成し、安全に設定できます。
```bash
docker run --rm -v portainer_data:/data portainer/helper-reset-password
```

### Portainer が起動しない
ログを確認します：
```bash
docker logs portainer
```
よくある問題としては、ボリュームデータの破損、Portainer バージョンの不一致、ホストの Docker デーモンの権限エラーなどがあります。

## 参考文献

- **公式ウェブサイト:** [https://www.portainer.io/](https://www.portainer.io/)
- **GitHub:** [https://github.com/portainer/portainer](https://github.com/portainer/portainer)
- **公式ドキュメント:** [https://docs.portainer.io/](https://docs.portainer.io/)
- **Docker Hub:** [portainer/portainer-ce](https://hub.docker.com/r/portainer/portainer-ce)
- **Slack コミュニティ:** [Portainer Slack](https://portainer.io/slack)