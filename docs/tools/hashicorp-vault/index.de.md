---
title: HashiCorp Vault
description: Ein Werkzeug zur sicheren Verwaltung von Geheimnissen wie API-Schlüsseln und Datenbankanmeldeinformationen mit Funktionen wie dynamischen Geheimnissen und automatischer Rotation.
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

HashiCorp Vault ist ein identitätsbasiertes System zur Verwaltung von Geheimnissen (Secrets), Verschlüsselung und privilegiertem Zugriff. Es fungiert als zentrales kryptografisches Gateway und ermöglicht es Organisationen, Geheimnisse (Datenbankpasswörter, API-Tokens, SSH-Schlüssel, TLS-Zertifikate, Cloud-Anmeldeinformationen) sicher zu speichern, den Zugriff streng zu kontrollieren und automatisch zu rotieren. Es ist der Industriestandard zur Lösung des „Secret Sprawl“ (der unkontrollierten Verbreitung von Geheimnissen) und zur Eliminierung von statischen, langlebigen Anmeldeinformationen in dynamischer Infrastruktur.

## Warum Vault verwenden?

| Problem | Vault-Lösung |
|---------|--------------|
| Secret Sprawl – Geheimnisse in Konfigurationsdateien, Umgebungsvariablen und Wikis gespeichert | Zentraler, geprüfter, richtlinienbasierter Geheimnisspeicher |
| Statische, langlebige Anmeldeinformationen ohne Rotation | Dynamische, kurzlebige Geheimnisse, die bei Bedarf mit kurzen TTLs generiert werden |
| Verschlüsselungsschlüssel, die fest in Anwendungen codiert sind | Verschlüsselung als Dienst – Anwendungen verschlüsseln/entschlüsseln, ohne den Schlüssel zu sehen |
| Manuelle Rotation von Anmeldeinformationen | Automatische Rotation durch Leasing-Ablauf und Sperrung von Anmeldeinformationen |
| Keine Transparenz darüber, wer worauf zugegriffen hat | Unveränderliche Prüfprotokolle aller Zugriffsanfragen auf Geheimnisse |

## Hauptfunktionen

### Secret Engines
Steckbare Backends, die Folgendes können:
- **Statische Geheimnisse speichern** (KV v1/v2)
- **Dynamische Anmeldeinformationen spontan generieren** (Datenbank, AWS, Azure, GCP)
- **Daten transformieren** (Transit-Verschlüsselung, PKI-Zertifikate)

### Dynamische Geheimnisse (Dynamic Secrets)
Anstatt statische Anmeldeinformationen zu speichern, erstellt Vault sie bei Bedarf für jeden Verbraucher. Wenn das Lease abläuft, wird die Anmeldeinformation automatisch widerrufen. Dadurch wird das Risiko von durchgesickerten statischen Anmeldeinformationen eliminiert.

### Verschlüsselung als Dienst (Transit)
Anwendungen können Daten verschlüsseln/entschlüsseln, ohne jemals direkten Zugriff auf Verschlüsselungsschlüssel zu haben. Die Transit-Engine verwaltet den Schlüssellebenszyklus, Rotation, Versionierung und Schlüsselableitung.

### Identitäts- und Zugriffsmanagement
Richtlinien (in HCL geschrieben) werden an Identitäten (Entitäten/Gruppen) gebunden, die mehrere Aliasse von Authentifizierungsmethoden (LDAP, OIDC, Kubernetes, AppRole) kombinieren. Dies entkoppelt die Identität von der Authentifizierung und ermöglicht ein umfangreiches RBAC.

### Leasing und Widerruf
Jedes Geheimnis in Vault hat eine Lebensdauer (TTL), die als Lease ausgedrückt wird. Leases werden bei Ablauf automatisch widerrufen, oder können sofort clusterweit widerrufen werden, um das Vertrauen in eine kompromittierte Anmeldeinformation zu zerstören.

### Prüfprotokollierung
Alle Anfragen und Authentifizierungen werden in einem oder mehreren Audit-Geräten (Datei, Syslog, Socket) protokolliert. Protokolle sind unveränderlich und enthalten jeden Vorgang, der gegen das System ausgeführt wurde.

### Speicher-Backend
- **Integriertes Raft** (eingebaute Hochverfügbarkeit, seit Vault 1.0) – keine externe Abhängigkeit.
- **Consul** – empfohlen für große Bereitstellungen.
- Enterprise-Editionen fügen Performance Replicas und Disaster Recovery hinzu.

### Auto-Unseal
Der Hauptschlüssel kann mithilfe eines Cloud-KMS (AWS KMS, Azure Key Vault, GCP KMS) oder eines HSM automatisch verpackt werden. Dadurch wird der manuelle Shamir-Entsiegelungsprozess aus Automatisierungspipelines entfernt.

## Installation

### 1. Entwicklermodus (nur lokale Tests)
```bash
vault server -dev -dev-root-token-id=root
```
Dies läuft im Speicher, automatisch entsiegelt. **Nicht in der Produktion verwenden.**

### 2. Produktions-Binärdatei
1. Laden Sie die [offizielle Version](https://releases.hashicorp.com/vault/) herunter.
2. Schreiben Sie eine Konfigurationsdatei `config.hcl`:
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
3. Starten Sie den Server:
```bash
vault server -config=config.hcl
```
4. Initialisieren Sie, wenn Sie kein Auto-Unseal verwenden:
```bash
vault operator init   # prints 5 unseal keys and the root token
```
5. Entsiegelung (ohne Auto-Unseal):
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
Für die Produktion verwenden Sie das [offizielle Helm-Diagramm](https://github.com/hashicorp/vault-helm) mit persistentem Speicher und TLS.

### 4. Cloud (HCP Vault)
Vollständig verwaltetes SaaS-Angebot. Kein Cluster-Management erforderlich.

## Grundlegende Verwendung

Alle Beispiele gehen von Folgendem aus:
```bash
export VAULT_ADDR=http://127.0.0.1:8200
vault login root
```

### Statische Geheimnisse (KV v2)
```bash
# Write a secret
vault kv put secret/myapp/config password=s3cret user=admin

# Read a specific field
vault kv get -field=password secret/myapp/config

# Delete a version
vault kv delete secret/myapp/config
```

### Dynamische Geheimnisse (Datenbank – PostgreSQL-Beispiel)
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

Die Antwort enthält einen Benutzernamen und ein Passwort, die nach 1 Stunde automatisch gelöscht werden.

### Verschlüsselung als Dienst (Transit)
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

## Richtlinien und Authentifizierung

### Richtlinienbeispiel (HCL)
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

### Authentifizierungsmethoden
- **Token** (built-in)
- **AppRole** (Machine-to-Machine)
- **Kubernetes** (an Service Account gebunden)
- **LDAP / OIDC** (menschliche Benutzer)
- **AWS / Azure / GCP** (Cloud-Instanz-Metadaten)

Beispiel mit AppRole:
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

## Anwendungsfälle

| Anwendungsfall | Wie Vault hilft |
|----------------|-----------------|
| **Dynamische Datenbankanmeldeinformationen** | Apps erhalten eindeutige, zeitlich begrenzte Datenbankbenutzer. Keine statischen Passwörter in Konfigurationen. |
| **CI/CD-Cloud-Anmeldeinformationen** | Generiert eine AWS-IAM-Rolle für einen einzelnen Pipeline-Lauf. Wird nach dem Job automatisch widerrufen. |
| **Interne PKI** | Betreiben Sie eine interne CA. Vault stellt kurzlebige TLS-Zertifikate für mTLS zwischen Diensten aus. |
| **Datenschutz (PII)** | Die Transit-Engine verschlüsselt sensible Felder in Legacy-Datenbanken. Die Anwendung kommt nie mit dem Schlüssel in Berührung. |
| **Speicherung statischer Geheimnisse** | Zentrale Speicherung von API-Schlüsseln, Zertifikaten und SSH-Schlüsseln mit feingranularer Zugriffskontrolle und Prüfprotokollen. |

## Weiterführende Literatur

- [Offizielle Dokumentation](https://developer.hashicorp.com/vault)
- [Vault Learn Tracks (Interaktiv)](https://learn.hashicorp.com/vault)
- [Vault API-Referenz](https://developer.hashicorp.com/vault/api-docs)
- [HashiCorp Vault Helm Chart](https://github.com/hashicorp/vault-helm)
- [OpenBao – Community-Fork](https://openbao.org)

## Zusammenfassung

HashiCorp Vault ist ein Eckpfeiler der modernen Cloud-native Sicherheit. Durch die Zentralisierung der Geheimnisverwaltung, die Ermöglichung dynamischer Anmeldeinformationen und die Bereitstellung von Verschlüsselung als Dienst werden die Risiken statischer Geheimnisse und des Secret Sprawl eliminiert. Ob on-premises, in der Cloud oder auf Kubernetes – Vault fügt sich nahtlos in eine Zero-Trust-Architektur ein, in der keine Anmeldeinformation über ihr Lease hinaus vertrauenswürdig ist.