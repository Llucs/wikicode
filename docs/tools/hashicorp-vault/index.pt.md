---
title: HashiCorp Vault
description: Uma ferramenta para gerenciar secrets com segurança, como chaves de API e credenciais de banco de dados, com recursos como secrets dinâmicos e rotação automatizada.
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

O HashiCorp Vault é um sistema de gerenciamento de secrets baseado em identidade, criptografia e gerenciamento de acesso privilegiado. Ele atua como um gateway criptográfico centralizado, permitindo que organizações armazenem secrets com segurança, controlem rigorosamente o acesso e realizem rotação automática de secrets (senhas de banco de dados, tokens de API, chaves SSH, certificados TLS, credenciais em nuvem). É o padrão da indústria para resolver a "dispersão de secrets" e eliminar credenciais estáticas e de longa duração em infraestruturas dinâmicas.

## Por que usar o Vault?

| Problema | Solução do Vault |
|---------|----------------|
| Dispersão de secrets – secrets armazenados em arquivos de configuração, variáveis de ambiente e wikis | Armazenamento centralizado, auditado e orientado por políticas de secrets |
| Credenciais estáticas e de longa duração sem rotação | Secrets dinâmicos e efêmeros gerados sob demanda com TTLs curtos |
| Chaves de criptografia codificadas em aplicações | Criptografia como Serviço – aplicativos criptografam/descriptografam sem ver a chave |
| Rotação manual de credenciais | Rotação automatizada via expiração de lease e revogação de credenciais |
| Nenhuma visibilidade sobre quem acessou o quê | Logs de auditoria imutáveis de cada solicitação de acesso a secrets |

## Principais Recursos

### Mecanismos de Secrets
Backends plugáveis que podem:
- **Armazenar** secrets estáticos (KV v1/v2)
- **Gerar** credenciais dinâmicas em tempo real (Banco de Dados, AWS, Azure, GCP)
- **Transformar** dados (Criptografia Transit, certificados PKI)

### Secrets Dinâmicos
Em vez de armazenar credenciais estáticas, o Vault as cria sob demanda para cada consumidor. Quando o lease expira, a credencial é automaticamente revogada. Isso elimina o risco de vazamento de credenciais estáticas.

### Criptografia como Serviço (Transit)
As aplicações podem criptografar/descriptografar dados sem nunca ter acesso direto às chaves de criptografia. O mecanismo Transit gerencia o ciclo de vida das chaves, rotação, versionamento e derivação de chaves.

### Gerenciamento de Identidade e Acesso
As políticas (escritas em HCL) são anexadas a **identidades** (entidades/grupos) que combinam múltiplos aliases de métodos de autenticação (LDAP, OIDC, Kubernetes, AppRole). Isso desacopla a identidade da autenticação e permite um RBAC rico.

### Leasing e Revogação
Cada secret no Vault tem um tempo de vida (TTL) expresso como um **lease**. Os leases são automaticamente revogados na expiração, ou podem ser revogados instantaneamente em todo o cluster para destruir a confiança de uma credencial comprometida.

### Registro de Auditoria
Todas as solicitações e autenticações são registradas em um ou mais dispositivos de auditoria (arquivo, syslog, socket). Os logs são imutáveis e contêm todas as operações realizadas no sistema.

### Backend de Armazenamento
- **Raft Integrado** (HA integrado, desde o Vault 1.0) – sem dependência externa.
- **Consul** – recomendado para grandes implantações.
- As edições Enterprise adicionam Réplicas de Performance e Recuperação de Desastres.

### Auto-Desvedação
A chave mestre pode ser automaticamente encapsulada usando um KMS em nuvem (AWS KMS, Azure Key Vault, GCP KMS) ou um HSM. Isso remove o processo manual de desvedação Shamir dos pipelines de automação.

## Instalação

### 1. Modo Dev (apenas para teste local)
```bash
vault server -dev -dev-root-token-id=root
```
Isso executa em memória, automaticamente desvedado. **Não use em produção.**

### 2. Binário de Produção
1. Baixe o [lançamento oficial](https://releases.hashicorp.com/vault/).
2. Escreva um arquivo de configuração `config.hcl`:
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
3. Inicie o servidor:
```bash
vault server -config=config.hcl
```
4. Inicialize se não estiver usando auto-unseal:
```bash
vault operator init   # prints 5 unseal keys and the root token
```
5. Desvede (sem auto-unseal):
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
Para produção, use o [gráfico Helm oficial](https://github.com/hashicorp/vault-helm) com armazenamento persistente e TLS.

### 4. Nuvem (HCP Vault)
Oferecimento SaaS totalmente gerenciado. Nenhum gerenciamento de cluster necessário.

## Uso Básico

Todos os exemplos assumem:
```bash
export VAULT_ADDR=http://127.0.0.1:8200
vault login root
```

### Secrets Estáticos (KV v2)
```bash
# Write a secret
vault kv put secret/myapp/config password=s3cret user=admin

# Read a specific field
vault kv get -field=password secret/myapp/config

# Delete a version
vault kv delete secret/myapp/config
```

### Secrets Dinâmicos (Exemplo com PostgreSQL)
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

A resposta inclui um nome de usuário e senha que são automaticamente destruídos após 1 hora.

### Criptografia como Serviço (Transit)
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

## Políticas e Autenticação

### Exemplo de Política (HCL)
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

### Métodos de Autenticação
- **Token** (integrado)
- **AppRole** (máquina a máquina)
- **Kubernetes** (vinculado a conta de serviço)
- **LDAP / OIDC** (usuários humanos)
- **AWS / Azure / GCP** (metadados de instância em nuvem)

Exemplo com AppRole:
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

## Casos de Uso

| Caso de Uso | Como o Vault Ajuda |
|----------|-----------------|
| **Credenciais dinâmicas de banco de dados** | Os aplicativos obtêm usuários de banco de dados únicos e com tempo limitado. Nenhuma senha estática em configurações. |
| **Credenciais em nuvem para CI/CD** | Gerar uma função IAM da AWS para uma única execução de pipeline. Automaticamente revogada após o job. |
| **PKI Interna** | Execute uma CA interna. O Vault emite certificados TLS de curta duração para mTLS entre serviços. |
| **Proteção de dados (PII)** | O mecanismo Transit criptografa campos sensíveis em bancos de dados legados. A aplicação nunca toca na chave. |
| **Armazenamento de secrets estáticos** | Armazene centralizadamente chaves de API, certificados e chaves SSH com controle de acesso granular e logs de auditoria. |

## Leitura Adicional

- [Documentação Oficial](https://developer.hashicorp.com/vault)
- [Trilhas de Aprendizado do Vault (Interativas)](https://learn.hashicorp.com/vault)
- [Referência da API do Vault](https://developer.hashicorp.com/vault/api-docs)
- [HashiCorp Vault Helm Chart](https://github.com/hashicorp/vault-helm)
- [OpenBao – Fork da Comunidade](https://openbao.org)

## Resumo

O HashiCorp Vault é uma pedra angular da segurança moderna nativa em nuvem. Ao centralizar o gerenciamento de secrets, habilitar credenciais dinâmicas e fornecer criptografia como serviço, ele elimina os riscos associados a secrets estáticos e dispersão de secrets. Seja executado on-premises, na nuvem ou no Kubernetes, o Vault se encaixa naturalmente em uma arquitetura de confiança zero, onde nenhuma credencial é confiada além de seu lease.