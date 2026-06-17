---
title: HashiCorp Vault
description: 一种用于安全管理密钥的工具，例如 API 密钥和数据库凭证，具有动态密钥和自动轮换等特性。
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

HashiCorp Vault 是一个基于身份的密钥管理、加密和特权访问管理系统。它充当集中的加密网关，使组织能够安全地存储、严格控制访问权限并自动轮换密钥（数据库密码、API 令牌、SSH 密钥、TLS 证书、云凭证）。它是解决“密钥扩散”和消除动态基础设施中静态、长期凭证的行业标准。

## 为什么使用 Vault？

| 问题 | Vault 解决方案 |
|---------|----------------|
| 密钥扩散——密钥存储在配置文件中、环境变量中和 Wiki 中 | 集中式、可审计、基于策略的密钥存储 |
| 没有轮换的静态、长期凭证 | 按需生成的动态、临时密钥，具有较短的 TTL |
| 应用程序中硬编码的加密密钥 | 加密即服务——应用程序在不接触密钥的情况下进行加密/解密 |
| 手动轮换凭证 | 通过租约到期和凭证撤销实现自动轮换 |
| 无法了解谁访问了什么 | 每次密钥访问请求的不可变审计日志 |

## 主要特性

### 密钥引擎
可插拔后端，可以：
- **存储** 静态密钥（KV v1/v2）
- **按需生成** 动态凭证（数据库、AWS、Azure、GCP）
- **转换** 数据（Transit 加密、PKI 证书）

### 动态密钥
Vault 不是存储静态凭证，而是为每个消费者按需创建凭证。当租约到期时，凭证会自动撤销。这消除了静态凭证泄露的风险。

### 加密即服务 (Transit)
应用程序可以在不直接接触加密密钥的情况下加密/解密数据。Transit 引擎处理密钥生命周期、轮换、版本控制和密钥派生。

### 身份与访问管理
策略（用 HCL 编写）附加到组合多个认证方法别名（LDAP、OIDC、Kubernetes、AppRole）的**身份**（实体/组）。这将身份与认证解耦，并实现丰富的 RBAC。

### 租赁与撤销
Vault 中的每个密钥都有一个表示为**租约**的生存时间 (TTL)。租约在到期时自动撤销，或者可以在集群范围内立即撤销，以破坏对受损凭证的信任。

### 审计日志
所有请求和认证都记录到一个或多个审计设备（文件、syslog、socket）。日志是不可变的，包含对系统执行的每个操作。

### 存储后端
- **集成 Raft**（内置高可用，自 Vault 1.0 起）——无需外部依赖。
- **Consul**——建议用于大型部署。
- 企业版增加了性能副本和灾难恢复。

### 自动解封
主密钥可以使用云 KMS（AWS KMS、Azure Key Vault、GCP KMS）或 HSM 自动包装。这样可以从自动化流程中移出手动的 Shamir 解封过程。

## 安装

### 1. 开发模式（仅限本地测试）
```bash
vault server -dev -dev-root-token-id=root
```
这在内存中运行，自动解封。**请勿在生产中使用。**

### 2. 生产二进制文件
1. 下载[官方发布版](https://releases.hashicorp.com/vault/)。
2. 编写配置文件 `config.hcl`：
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
3. 启动服务器：
```bash
vault server -config=config.hcl
```
4. 如果未使用自动解封，则初始化：
```bash
vault operator init   # prints 5 unseal keys and the root token
```
5. 解封（未使用自动解封）：
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
对于生产环境，请使用带有持久存储和 TLS 的[官方 Helm Chart](https://github.com/hashicorp/vault-helm)。

### 4. 云 (HCP Vault)
完全托管的 SaaS 产品。无需集群管理。

## 基本用法

所有示例假定：
```bash
export VAULT_ADDR=http://127.0.0.1:8200
vault login root
```

### 静态密钥 (KV v2)
```bash
# Write a secret
vault kv put secret/myapp/config password=s3cret user=admin

# Read a specific field
vault kv get -field=password secret/myapp/config

# Delete a version
vault kv delete secret/myapp/config
```

### 动态密钥 (数据库 – PostgreSQL 示例)
```bash
# Enable the database secrets engine
vault secrets enable database

# Configure the PostgreSQL plugin
vault write database/config/postgres \
    plugin_name=postgresql-database-plugin \
    connection_url="postgresql://{{username}}:{{password}}@postgres:5432/mydb" \
    allowed_roles="readonly" \
    username="vault" \
    password="vaultpass"

# Define a role that creates a read-only user for 1 hour
vault write database/roles/readonly \
    db_name=postgres \
    creation_statements="CREATE USER \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
                         GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="24h"

# Request a credential
vault read database/creds/readonly
```
响应中包含一个用户名和密码，这些凭证会在 1 小时后自动销毁。

### 加密即服务 (Transit)
```bash
# Enable the transit engine
vault secrets enable transit

# Create a new encryption key
vault write -f transit/keys/my-key

# Encrypt data (plaintext must be base64 encoded)
echo -n "SensitiveData" | base64 | vault write transit/encrypt/my-key plaintext=-

# Decrypt data
vault write -field=plaintext transit/decrypt/my-key ciphertext=vault:v1:abc... | base64 -d
```

## 策略与认证

### 策略示例 (HCL)
`myapp-policy.hcl`：
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

### 认证方法
- **Token**（内置）
- **AppRole**（机器对机器）
- **Kubernetes**（服务账户绑定）
- **LDAP / OIDC**（人类用户）
- **AWS / Azure / GCP**（云实例元数据）

AppRole 示例：
```bash
# Enable and configure AppRole
vault auth enable approle
vault write auth/approle/role/myapp secret_id_ttl=10m token_policies=myapp

# Get RoleID and SecretID
vault read auth/approle/role/myapp/role-id
vault write -f auth/approle/role/myapp/secret-id

# Login
vault write auth/approle/login role_id=... secret_id=...
```

## 使用场景

| 使用场景 | Vault 如何帮助 |
|----------|----------------|
| **动态数据库凭证** | 应用程序获得唯一的、有时间限制的数据库用户。配置中没有静态密码。 |
| **CI/CD 云凭证** | 为单个流水线运行生成 AWS IAM 角色。作业完成后自动撤销。 |
| **内部 PKI** | 运行内部 CA。Vault 为服务之间的 mTLS 签发短期 TLS 证书。 |
| **数据保护 (PII)** | Transit 引擎加密遗留数据库中的敏感字段。应用程序从不接触密钥。 |
| **静态密钥存储** | 集中存储 API 密钥、证书和 SSH 密钥，具有细粒度的访问控制和审计日志。 |

## 延伸阅读

- [官方文档](https://developer.hashicorp.com/vault)
- [Vault 学习路径（交互式）](https://learn.hashicorp.com/vault)
- [Vault API 参考](https://developer.hashicorp.com/vault/api-docs)
- [HashiCorp Vault Helm Chart](https://github.com/hashicorp/vault-helm)
- [OpenBao – 社区分支](https://openbao.org)

## 总结

HashiCorp Vault 是现代云原生安全的基石。通过集中管理密钥、启用动态凭证以及提供加密即服务，它消除了与静态密钥和密钥扩散相关的风险。无论是在本地、云中还是 Kubernetes 上运行，Vault 都能自然地融入零信任架构，在该架构中，没有凭证在其租约之外被信任。