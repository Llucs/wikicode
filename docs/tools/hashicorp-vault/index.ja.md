---
title: HashiCorp Vault
description: APIキーやデータベース認証情報などのシークレットを安全に管理し、dynamic secretsやautomated rotationなどの機能を提供するツールです。
created: 2026-06-17
tags:
  - hashicorp
  - vault
  - secrets-management
  - security
  - devops
status: draft
---

# HashiCorp Vault

HashiCorp Vaultは、アイデンティティベースのsecrets management、暗号化、privileged access managementシステムです。中央集権的な暗号化ゲートウェイとして機能し、組織がシークレット（データベースパスワード、APIトークン、SSHキー、TLS証明書、クラウド認証情報）を安全に保存し、アクセスを厳密に制御し、自動的にローテーションできるようにします。これは、"secret sprawl"を解決し、動的インフラストラクチャにおける静的で長期間有効な認証情報を排除するための業界標準です。

## Vaultを使う理由

| 問題 | Vaultの解決策 |
|---------|----------------|
| Secret sprawl – 設定ファイル、env vars、wikisに保存されたシークレット | 中央集権的で監査され、ポリシーに基づいたsecret store |
| 静的で長期間有効な認証情報、ローテーションなし | 短いTTLを持つオンデマンドで生成される動的で一時的な認証情報 |
| アプリケーションにハードコードされた暗号化キー | Encryption as a Service – アプリケーションはキーを見ずに暗号化/復号化 |
| 手動による認証情報のローテーション | leaseの有効期限と認証情報のrevocationによる自動ローテーション |
| 誰が何にアクセスしたかの可視性なし | すべてのシークレットアクセスリクエストの不変のaudit log |

## 主な機能

### Secret Engines
プラグイン可能なバックエンドで、以下のことが可能です：
- **Store** static secrets（KV v1/v2）
- **Generate** dynamic credentials on the fly（Database、AWS、Azure、GCP）
- **Transform** data（Transit encryption、PKI certificates）

### Dynamic Secrets
静的な認証情報を保存する代わりに、Vaultは各コンシューマーごとにオンデマンドで作成します。leaseが期限切れになると、認証情報は自動的にrevokeされます。これにより、静的な認証情報の漏洩リスクがなくなります。

### Encryption as a Service (Transit)
アプリケーションは暗号化キーに直接アクセスすることなく、データを暗号化/復号化できます。Transit engineは、キーのライフサイクル、ローテーション、バージョニング、キー派生を処理します。

### Identity & Access Management
ポリシー（HCLで記述）は、複数のauth methodエイリアス（LDAP、OIDC、Kubernetes、AppRole）を組み合わせた**identities**（entities/groups）にアタッチされます。これにより、アイデンティティと認証が分離され、リッチなRBACが可能になります。

### Leasing & Revocation
Vaultのすべてのシークレットには、**lease**として表されるtime-to-live（TTL）があります。leaseは有効期限が切れると自動的にrevokeされるか、クラスタ全体で即座にrevokeして、侵害された認証情報への信頼を破棄できます。

### Audit Logging
すべてのリクエストと認証は、1つ以上のaudit device（file、syslog、socket）にログ記録されます。ログは不変であり、システムに対して実行されたすべての操作が含まれます。

### Storage Backend
- **Integrated Raft**（組み込みHA、Vault 1.0以降） – 外部依存不要。
- **Consul** – 大規模デプロイメントに推奨。
- エンタープライズエディションでは、Performance ReplicasとDisaster Recoveryが追加されます。

### Auto-Unseal
マスターキーは、クラウドKMS（AWS KMS、Azure Key Vault、GCP KMS）またはHSMを使用して自動的にラップできます。これにより、自動化パイプラインから手動のShamir unsealプロセスが不要になります。

## インストール

### 1. 開発モード（ローカルテストのみ）
```bash
vault server -dev -dev-root-token-id=root
```
これはメモリ内で実行され、自動的にunsealされます。**本番環境では使用しないでください。**

### 2. 本番用バイナリ
1. [公式リリース](https://releases.hashicorp.com/vault/)をダウンロードします。
2. 設定ファイル `config.hcl` を作成します：
```hcl
storage "raft" {
  path = "/opt/vault/data"
  node_id = "node1"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = true
}

seal "awskms" {
  region     = "us-west-2"
  kms_key_id = "alias/vault"
}
```
3. サーバーを起動します：
```bash
vault server -config=config.hcl
```
4. auto-unsealを使用しない場合はinitします：
```bash
vault operator init   # 5つのunseal keysとroot tokenが出力されます
```
5. Unseal（auto-unsealを使用しない場合）：
```bash
vault operator unseal <key-1>
vault operator unseal <key-2>
vault operator unseal <key-3>
```

### 3. Kubernetes (Helm)
```bash
helm repo add hashicorp https://helm.releases.hashicorp.com
helm install vault hashicorp/vault --namespace vault --create-namespace \
  --set server.dev.enabled=true
```
本番環境では、永続ストレージとTLSを備えた[公式Helm chart](https://github.com/hashicorp/vault-helm)を使用してください。

### 4. Cloud (HCP Vault)
フルマネージドのSaaSサービスです。クラスタ管理は不要です。

## 基本的な使い方

すべての例では以下を前提としています：
```bash
export VAULT_ADDR=http://127.0.0.1:8200
vault login root
```

### Static Secrets (KV v2)
```bash
# シークレットを書き込み
vault kv put secret/myapp/config password=s3cret user=admin

# 特定のフィールドを読み取り
vault kv get -field=password secret/myapp/config

# バージョンを削除
vault kv delete secret/myapp/config
```

### Dynamic Secrets (データベース – PostgreSQLの例)
```bash
# database secrets engineを有効化
vault secrets enable database

# PostgreSQLプラグインを設定
vault write database/config/postgres \
    plugin_name=postgresql-database-plugin \
    connection_url="postgresql://{{username}}:{{password}}@postgres:5432/mydb" \
    allowed_roles="readonly" \
    username="vault" \
    password="vaultpass"

# 1時間有効な読み取り専用ユーザーを作成するロールを定義
vault write database/roles/readonly \
    db_name=postgres \
    creation_statements="CREATE USER \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
                         GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="24h"

# 認証情報をリクエスト
vault read database/creds/readonly
```

レスポンスにはユーザー名とパスワードが含まれ、1時間後に自動的に破棄されます。

### Encryption as a Service (Transit)
```bash
# transit engineを有効化
vault secrets enable transit

# 新しい暗号化キーを作成
vault write -f transit/keys/my-key

# データを暗号化（plaintextはbase64エンコードが必要）
echo -n "SensitiveData" | base64 | vault write transit/encrypt/my-key plaintext=-

# データを復号化
vault write -field=plaintext transit/decrypt/my-key ciphertext=vault:v1:abc... | base64 -d
```

## Policies & Authentication

### ポリシー例 (HCL)
`myapp-policy.hcl`:
```hcl
path "secret/data/myapp/*" {
  capabilities = ["read", "list"]
}

path "database/creds/readonly" {
  capabilities = ["read"]
}
```

```bash
vault policy write myapp myapp-policy.hcl
```

### Authentication Methods
- **Token**（組み込み）
- **AppRole**（マシン間）
- **Kubernetes**（service accountバインド）
- **LDAP / OIDC**（人間のユーザー）
- **AWS / Azure / GCP**（クラウドインスタンスメタデータ）

AppRoleの例：
```bash
# AppRoleを有効化して設定
vault auth enable approle
vault write auth/approle/role/myapp secret_id_ttl=10m token_policies=myapp

# RoleIDとSecretIDを取得
vault read auth/approle/role/myapp/role-id
vault write -f auth/approle/role/myapp/secret-id

# ログイン
vault write auth/approle/login role_id=... secret_id=...
```

## ユースケース

| ユースケース | Vaultの助け方 |
|----------|-----------------|
| **動的データベース認証情報** | アプリは一意で一時的なデータベースユーザーを取得します。設定ファイルに静的なパスワードはありません。 |
| **CI/CDクラウド認証情報** | 単一パイプライン実行のためのAWS IAMロールを生成します。ジョブ後に自動的にrevokeされます。 |
| **内部PKI** | 社内CAを運用します。Vaultはサービス間mTLSのための短期間有効なTLS証明書を発行します。 |
| **データ保護（PII）** | Transit engineがレガシーデータベースの機密フィールドを暗号化します。アプリケーションはキーに触れません。 |
| **静的シークレットストレージ** | APIキー、証明書、SSHキーを、きめ細かいアクセス制御とaudit logとともに一元保存します。 |

## 参考文献

- [公式ドキュメント](https://developer.hashicorp.com/vault)
- [Vault Learn Tracks（インタラクティブ）](https://learn.hashicorp.com/vault)
- [Vault APIリファレンス](https://developer.hashicorp.com/vault/api-docs)
- [HashiCorp Vault Helm Chart](https://github.com/hashicorp/vault-helm)
- [OpenBao – コミュニティフォーク](https://openbao.org)

## まとめ

HashiCorp Vaultは、現代のクラウドネイティブセキュリティの基盤です。secrets managementを一元化し、dynamic credentialsを可能にし、encryption as a serviceを提供することで、static secretsやsecret sprawlに関連するリスクを排除します。オンプレミス、クラウド、Kubernetesのいずれで実行する場合でも、Vaultはゼロトラストアーキテクチャに自然に適合し、どの認証情報もそのleaseを超えて信頼されることはありません。