---
title: Dockerイメージにクレデンシャルを直接埋め込まずにシークレットの注入
description: 容器化アプリケーションにセキュアなデータ（特にクレデンシャル）を実行時に注入する方法について説明します。これには、Dockerイメージに直接クレデンシャルを埋め込むことなく、実行時やデプロイフェーズで提供することを含みます。
created: 2026-07-04
tags:
  - DevOps
  - Docker
  - Kubernetes
  - Security
  - Secrets Management
status: draft
---

# Dockerイメージにクレデンシャルを直接埋め込まずにシークレットの注入

シークレットの注入とは、容器化アプリケーションに敏感なデータを実行時に管理して注入することを指します。これには、Dockerイメージにクレデンシャルやシークレットを直接埋め込むことなく、実行時やデプロイフェーズで提供することを含みます。

## 主な機能

1. **実行時のセキュリティ**: クレデンシャルはイメージに直接埋め込まれることはありません。そのため、イメージスキャン中に露出されるリスクや脆弱性により漏洩するリスクが低減されます。
2. **柔軟性**: シークレットを容易に更新できるため、イメージの再ビルドや再デプロイは必要ありません。
3. **スケーラビリティ**: マイクロサービス環境でのシークレットのセキュアな管理を容易にします。
4. **準拠**: 組織がデータセキュリティと準拠に関する監視要件とベストプラクティスに準拠するのを助けることができます。

## 使用例

1. **データベースクレデンシャル**: データベースのユーザー名とパスワードを安全に管理します。
2. **APIキー**: 複数のサービス用のAPIキーを安全に保存・注入します。
3. **構成管理**: アプリケーションコードベースに含まれない構成設定を注入します。
4. **暗号化キー**: 静態や動態保護用の暗号化キーを管理します。

## インストール

シークレット管理の具体的なツールやソリューションにより、インストールプロセスは異なります。以下は、一般的な手順をいくつかの一般的なソリューションについて示します：

### Kubernetesシークレット

1. **前提条件**: Kubernetesクラスター。
2. **インストール**: Kubernetesシークレットは既に組み込まれているため、明示的なインストールは必要ありません。
3. **手順**:
   1. `kubectl`またはKubernetesダッシュボードを使用してシークレットを作成します。
   2. デプロイメントのYAMLまたはKubernetes宣言内でシークレットを参照します。
   3. パッドでシークレットをボリュームとしてマウントしたり、環境変数として使用したりします。

```yaml
# シークレットを参照するための例YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app-image
        env:
          - name: MY_SECRET_KEY
            valueFrom:
              secretKeyRef:
                name: my-secret
                key: my-key
```

### Dockerシークレット

1. **前提条件**: Dockerスwarm。
2. **インストール**: Dockerスwarmはシークレットを内蔵していますので、明示的なインストールは必要ありません。
3. **手順**:
   1. `docker swarm secret create` コマンドを使用してDockerシークレットを作成します。
   2. サービス定義内でシークレットを参照します。

```bash
# Dockerシークレットを作成する
docker swarm secret create my-secret my-value

# サービス定義内でシークレットを参照する
services:
  my-service:
    secrets:
      - my-secret
    command: ["--my-key=$(MY_SECRET_KEY)"]
```

### HashiCorp Vault

1. **前提条件**: HashiCorp Vaultサーバー。
2. **インストール**: HashiCorp Vaultをサーバー上にダウンロードまたはインストールします。または、マネージドサービスを使用します。
3. **手順**:
   1. Vaultを初期化し、シークルします。
   2. シークレットをVaultに作成し、保存します。
   3. Vault APIを使用して実行時にシークレットを取得します。

```bash
# Vaultを初期化し、シークルします
vault operator init
vault unseal <unseal-key>

# シークレットを保存する
vault kv put secret/my-secret key=my-value

# Vault APIを使用してシークレットを取得する
vault read secret/my-secret
```

## 基本的な使用法

### シークレットの作成

1. **Kubernetes**: `kubectl create secret generic my-secret --from-literal=my-key=my-value`
2. **Dockerスwarm**: `docker swarm secret create my-secret my-value`
3. **HashiCorp Vault**: `vault kv put secret/my-secret key=my-value`

### シークレットの参照

1. **Kubernetes**:
   ```yaml
   spec:
     containers:
     - name: my-app
       image: my-app-image
       env:
         - name: MY_SECRET_KEY
           valueFrom:
             secretKeyRef:
               name: my-secret
               key: my-key
   ```

2. **Dockerスwarm**:
   ```yaml
   services:
     my-service:
       secrets:
         - my-secret
       command: ["--my-key=$(MY_SECRET_KEY)"]
   ```

3. **HashiCorp Vault**:
   - シークレットはVault APIまたは`vault read`コマンドを使用して取得できます。

シークレットの注入の採用により、組織は容器化アプリケーションのセキュリティポリシーを著しく強化し、開発およびデプロイライフサイクル全体を通じて敏感なデータを保護し、管理することができます。