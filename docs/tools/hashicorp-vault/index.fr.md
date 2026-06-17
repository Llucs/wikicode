---
title: HashiCorp Vault
description: Un outil pour gérer en toute sécurité les secrets, tels que les clés API et les identifiants de base de données, avec des fonctionnalités comme les secrets dynamiques et la rotation automatisée.
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

HashiCorp Vault est un système de gestion des secrets, de chiffrement et de gestion des accès privilégiés basé sur l'identité. Il agit comme une passerelle cryptographique centralisée, permettant aux organisations de stocker en toute sécurité, de contrôler strictement l'accès et de faire automatiquement la rotation des secrets (mots de passe de base de données, jetons API, clés SSH, certificats TLS, identifiants cloud). Il est la norme de l'industrie pour résoudre la « dispersion des secrets » et éliminer les identifiants statiques et à longue durée de vie dans une infrastructure dynamique.

## Pourquoi utiliser Vault ?

| Problème | Solution Vault |
|---------|----------------|
| Dispersion des secrets – secrets stockés dans des fichiers de configuration, variables d'environnement et wikis | Stockage centralisé, audité et basé sur des politiques pour les secrets |
| Identifiants statiques et à longue durée de vie sans rotation | Secrets dynamiques et éphémères générés à la demande avec des TTL courts |
| Clés de chiffrement codées en dur dans les applications | Chiffrement en tant que service – les applications chiffrent/déchiffrent sans voir la clé |
| Rotation manuelle des identifiants | Rotation automatisée via l'expiration des leases et la révocation des identifiants |
| Aucune visibilité sur qui a accédé à quoi | Journaux d'audit immuables de chaque demande d'accès aux secrets |

## Fonctionnalités clés

### Moteurs de secrets
Des backends enfichables capables de :
- **Stocker** les secrets statiques (KV v1/v2)
- **Générer** des identifiants dynamiques à la volée (Database, AWS, Azure, GCP)
- **Transformer** les données (chiffrement Transit, certificats PKI)

### Secrets dynamiques
Au lieu de stocker des identifiants statiques, Vault les crée à la demande pour chaque consommateur. Lorsque le lease expire, l'identifiant est automatiquement révoqué. Cela élimine le risque de fuite d'identifiants statiques.

### Chiffrement en tant que service (Transit)
Les applications peuvent chiffrer/déchiffrer des données sans jamais avoir un accès direct aux clés de chiffrement. Le moteur Transit gère le cycle de vie des clés, la rotation, le versioning et la dérivation des clés.

### Gestion des identités et des accès
Les politiques (écrites en HCL) sont attachées aux **identités** (entités/groupes) qui combinent plusieurs alias de méthodes d'authentification (LDAP, OIDC, Kubernetes, AppRole). Cela découple l'identité de l'authentification et permet un RBAC riche.

### Leasing et révocation
Chaque secret dans Vault a une durée de vie (TTL) exprimée sous forme de **lease**. Les leases sont automatiquement révoqués à l'expiration, ou peuvent être révoqués instantanément à l'échelle du cluster pour détruire la confiance d'un identifiant compromis.

### Journalisation d'audit
Toutes les demandes et authentifications sont journalisées sur un ou plusieurs périphériques d'audit (fichier, syslog, socket). Les journaux sont immuables et contiennent chaque opération effectuée sur le système.

### Backend de stockage
- **Raft intégré** (HA intégré, depuis Vault 1.0) – aucune dépendance externe.
- **Consul** – recommandé pour les déploiements importants.
- Les éditions Enterprise ajoutent les Réplicas de performance et la Reprise après sinistre.

### Auto-déscellage
La clé maître peut être automatiquement enveloppée en utilisant un KMS cloud (AWS KMS, Azure Key Vault, GCP KMS) ou un HSM. Cela supprime le processus manuel de déscellage Shamir des pipelines d'automatisation.

## Installation

### 1. Mode Dev (test local uniquement)
```bash
vault server -dev -dev-root-token-id=root
```
Cela s'exécute en mémoire, automatiquement déscellé. **Ne pas utiliser en production.**

### 2. Binaire de production
1. Téléchargez la [version officielle](https://releases.hashicorp.com/vault/).
2. Écrivez un fichier de configuration `config.hcl` :
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
3. Démarrez le serveur :
```bash
vault server -config=config.hcl
```
4. Initialisez si vous n'utilisez pas l'auto-déscellage :
```bash
vault operator init   # prints 5 unseal keys and the root token
```
5. Déscellez (sans auto-déscellage) :
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
Pour la production, utilisez le [chart Helm officiel](https://github.com/hashicorp/vault-helm) avec stockage persistant et TLS.

### 4. Cloud (HCP Vault)
Offre SaaS entièrement gérée. Aucune gestion de cluster requise.

## Utilisation de base

Tous les exemples supposent :
```bash
export VAULT_ADDR=http://127.0.0.1:8200
vault login root
```

### Secrets statiques (KV v2)
```bash
# Write a secret
vault kv put secret/myapp/config password=s3cret user=admin

# Read a specific field
vault kv get -field=password secret/myapp/config

# Delete a version
vault kv delete secret/myapp/config
```

### Secrets dynamiques (Base de données – exemple PostgreSQL)
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

La réponse inclut un nom d'utilisateur et un mot de passe qui sont automatiquement détruits après 1 heure.

### Chiffrement en tant que service (Transit)
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

## Politiques et authentification

### Exemple de politique (HCL)
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

### Méthodes d'authentification
- **Token** (intégré)
- **AppRole** (machine à machine)
- **Kubernetes** (lié au compte de service)
- **LDAP / OIDC** (utilisateurs humains)
- **AWS / Azure / GCP** (métadonnées d'instance cloud)

Exemple avec AppRole :
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

## Cas d'utilisation

| Cas d'utilisation | Comment Vault aide |
|----------|-----------------|
| **Identifiants de base de données dynamiques** | Les applications obtiennent des utilisateurs de base de données uniques et limités dans le temps. Pas de mots de passe statiques dans les configurations. |
| **Identifiants cloud CI/CD** | Générer un rôle IAM AWS pour une seule exécution de pipeline. Automatiquement révoqué après le travail. |
| **PKI interne** | Exécuter une autorité de certification interne. Vault émet des certificats TLS à courte durée de vie pour le mTLS entre services. |
| **Protection des données (PII)** | Le moteur Transit chiffre les champs sensibles dans les bases de données héritées. L'application ne touche jamais à la clé. |
| **Stockage de secrets statiques** | Stocker de manière centralisée les clés API, les certificats et les clés SSH avec un contrôle d'accès fin et des journaux d'audit. |

## Pour en savoir plus

- [Documentation officielle](https://developer.hashicorp.com/vault)
- [Parcours d'apprentissage Vault (interactif)](https://learn.hashicorp.com/vault)
- [Référence de l'API Vault](https://developer.hashicorp.com/vault/api-docs)
- [Chart Helm HashiCorp Vault](https://github.com/hashicorp/vault-helm)
- [OpenBao – Fork communautaire](https://openbao.org)

## Résumé

HashiCorp Vault est une pierre angulaire de la sécurité cloud-native moderne. En centralisant la gestion des secrets, en permettant des identifiants dynamiques et en fournissant le chiffrement en tant que service, il élimine les risques associés aux secrets statiques et à la dispersion des secrets. Qu'il soit exécuté sur site, dans le cloud ou sur Kubernetes, Vault s'intègre naturellement dans une architecture zero-trust où aucun identifiant n'est approuvé au-delà de son lease.