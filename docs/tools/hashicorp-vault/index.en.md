---
title: HashiCorp Vault
description: A tool for securely managing secrets, such as API keys and database credentials, with features like dynamic secrets and automated rotation.
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

HashiCorp Vault is an identity-based secrets management, encryption, and privileged access management system. It acts as a centralized cryptographic gateway, allowing organizations to securely store, tightly control access to, and automatically rotate secrets (database passwords, API tokens, SSH keys, TLS certificates, cloud credentials). It is the industry standard for solving "secret sprawl" and eliminating static, long-lived credentials in dynamic infrastructure.

## Why Use Vault?

| Problem | Vault Solution |
|---------|----------------|
| Secret sprawl – secrets stored in config files, env vars, and wikis | Centralised, audited, policy-driven secret store |
| Static, long-lived credentials with no rotation | Dynamic, ephemeral secrets generated on demand with short TTLs |
| Encryption keys hardcoded in applications | Encryption as a Service – apps encrypt/decrypt without seeing the key |
| Manual rotation of credentials | Automated rotation via lease expiry and credential revocation |
| No visibility into who accessed what | Immutable audit logs of every secret access request |

## Key Features

### Secret Engines
Pluggable backends that can:
- **Store** static secrets (KV v1/v2)
- **Generate** dynamic credentials on the fly (Database, AWS, Azure, GCP)
- **Transform** data (Transit encryption, PKI certificates)

### Dynamic Secrets
Instead of storing static credentials, Vault creates them on demand for each consumer. When the lease expires, the credential is automatically revoked. This eliminates the risk of leaked static credentials.

### Encryption as a Service (Transit)
Applications can encrypt/decrypt data without ever having direct access to encryption keys. The Transit engine handles key lifecycle, rotation, versioning, and key derivation.

### Identity & Access Management
Policies (written in HCL) attach to **identities** (entities/groups) that combine multiple auth method aliases (LDAP, OIDC, Kubernetes, AppRole). This decouples identity from authentication and enables rich RBAC.

### Leasing & Revocation
Every secret in Vault has a time-to-live (TTL) expressed as a **lease**. Leases are automatically revoked at expiry, or can be revoked instantly cluster-wide to destroy trust for a compromised credential.

### Audit Logging
All requests and authentications are logged to one or more audit devices (file, syslog, socket). Logs are immutable and contain every operation performed against the system.

### Storage Backend
- **Integrated Raft** (built-in HA, since Vault 1.0) – no external dependency.
- **Consul** – recommended for large deployments.
- Enterprise editions add Performance Replicas and Disaster Recovery.

### Auto-Unseal
The master key can be automatically wrapped using a cloud KMS (AWS KMS, Azure Key Vault, GCP KMS) or an HSM. This removes the manual Shamir unseal process from automation pipelines.

## Installation

### 1. Dev Mode (local testing only)
```bash
vault server -dev -dev-root-token-id=root
```
This runs in memory, automatically unsealed. **Do not use in production.**

### 2. Production Binary
1. Download the [official release](https://releases.hashicorp.com/vault/).
2. Write a configuration file `config.hcl`:
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
3. Start the server:
```bash
vault server -config=config.hcl
```
4. Initialize if not using auto-unseal:
```bash
vault operator init   # prints 5 unseal keys and the root token
```
5. Unseal (without auto-unseal):
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
For production, use the [official Helm chart](https://github.com/hashicorp/vault-helm) with persistent storage and TLS.

### 4. Cloud (HCP Vault)
Fully managed SaaS offering. No cluster management required.

## Basic Usage

All examples assume:
```bash
export VAULT_ADDR=http://127.0.0.1:8200
vault login root
```

### Static Secrets (KV v2)
```bash
# Write a secret
vault kv put secret/myapp/config password=s3cret user=admin

# Read a specific field
vault kv get -field=password secret/myapp/config

# Delete a version
vault kv delete secret/myapp/config
```

### Dynamic Secrets (Database – PostgreSQL example)
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

The response includes a username and password that are automatically destroyed after 1 hour.

### Encryption as a Service (Transit)
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

## Policies & Authentication

### Policy Example (HCL)
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
- **Token** (built-in)
- **AppRole** (machine-to-machine)
- **Kubernetes** (service account bound)
- **LDAP / OIDC** (human users)
- **AWS / Azure / GCP** (cloud instance metadata)

Example with AppRole:
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

## Use Cases

| Use Case | How Vault Helps |
|----------|-----------------|
| **Dynamic database credentials** | Apps get unique, time-limited database users. No static passwords in configs. |
| **CI/CD cloud credentials** | Generate an AWS IAM role for a single pipeline run. Automatically revoked after the job. |
| **Internal PKI** | Run an in-house CA. Vault issues short-lived TLS certificates for mTLS between services. |
| **Data protection (PII)** | Transit engine encrypts sensitive fields in legacy databases. The application never touches the key. |
| **Static secret storage** | Centrally store API keys, certificates, and SSH keys with fine-grained access control and audit logs. |

## Further Reading

- [Official Documentation](https://developer.hashicorp.com/vault)
- [Vault Learn Tracks (Interactive)](https://learn.hashicorp.com/vault)
- [Vault API Reference](https://developer.hashicorp.com/vault/api-docs)
- [HashiCorp Vault Helm Chart](https://github.com/hashicorp/vault-helm)
- [OpenBao – Community Fork](https://openbao.org)

## Summary

HashiCorp Vault is a cornerstone of modern cloud-native security. By centralising secrets management, enabling dynamic credentials, and providing encryption as a service, it eliminates the risks associated with static secrets and secret sprawl. Whether running on-premises, in the cloud, or on Kubernetes, Vault fits naturally into a zero-trust architecture where no credential is trusted beyond its lease.