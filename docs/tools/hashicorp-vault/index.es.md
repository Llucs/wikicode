---
title: HashiCorp Vault
description: Una herramienta para gestionar secretos de forma segura, como API keys y database credentials, con características como dynamic secrets y automated rotation.
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

HashiCorp Vault es un sistema de gestión de secretos basado en identidad, cifrado y gestión de acceso privilegiado. Actúa como una puerta de enlace criptográfica centralizada, permitiendo a las organizaciones almacenar de forma segura, controlar estrictamente el acceso y rotar automáticamente secretos (contraseñas de bases de datos, tokens de API, claves SSH, certificados TLS, credenciales de nube). Es el estándar de la industria para resolver el "secret sprawl" y eliminar las credenciales estáticas y de larga duración en infraestructuras dinámicas.

## ¿Por qué usar Vault?

| Problema | Solución de Vault |
|---------|----------------|
| Secret sprawl – secretos almacenados en archivos de configuración, env vars y wikis | Almacén de secretos centralizado, auditado y basado en políticas |
| Credenciales estáticas y de larga duración sin rotación | Secretos dinámicos y efímeros generados bajo demanda con TTLs cortos |
| Claves de cifrado hardcodeadas en aplicaciones | Cifrado como Servicio – las aplicaciones cifran/descifran sin ver la clave |
| Rotación manual de credenciales | Rotación automatizada mediante expiración de arrendamiento y revocación de credenciales |
| Sin visibilidad de quién accedió a qué | Registros de auditoría inmutables de cada solicitud de acceso a secretos |

## Características Principales

### Motores de Secretos
Backends conectables que pueden:
- **Almacenar** secretos estáticos (KV v1/v2)
- **Generar** credenciales dinámicas sobre la marcha (Database, AWS, Azure, GCP)
- **Transformar** datos (cifrado Transit, certificados PKI)

### Secretos Dinámicos
En lugar de almacenar credenciales estáticas, Vault las crea bajo demanda para cada consumidor. Cuando el arrendamiento expira, la credencial se revoca automáticamente. Esto elimina el riesgo de filtración de credenciales estáticas.

### Cifrado como Servicio (Transit)
Las aplicaciones pueden cifrar/descifrar datos sin tener acceso directo a las claves de cifrado. El motor Transit maneja el ciclo de vida de las claves, la rotación, el versionado y la derivación de claves.

### Gestión de Identidad y Acceso
Las políticas (escritas en HCL) se adjuntan a **identidades** (entidades/grupos) que combinan múltiples alias de métodos de autenticación (LDAP, OIDC, Kubernetes, AppRole). Esto desacopla la identidad de la autenticación y permite un RBAC enriquecido.

### Arrendamiento y Revocación
Cada secreto en Vault tiene un tiempo de vida (TTL) expresado como un **arrendamiento**. Los arrendamientos se revocan automáticamente al expirar, o se pueden revocar instantáneamente en todo el clúster para destruir la confianza de una credencial comprometida.

### Registro de Auditoría
Todas las solicitudes y autenticaciones se registran en uno o más dispositivos de auditoría (file, syslog, socket). Los registros son inmutables y contienen todas las operaciones realizadas contra el sistema.

### Backend de Almacenamiento
- **Raft integrado** (HA incorporado, desde Vault 1.0) – sin dependencia externa.
- **Consul** – recomendado para grandes despliegues.
- Las ediciones Enterprise añaden Réplicas de Rendimiento y Recuperación ante Desastres.

### Auto-Unseal
La clave maestra se puede envolver automáticamente usando un KMS en la nube (AWS KMS, Azure Key Vault, GCP KMS) o un HSM. Esto elimina el proceso manual de desellado Shamir de los pipelines de automatización.

## Instalación

### 1. Modo Dev (solo pruebas locales)
```bash
vault server -dev -dev-root-token-id=root
```
Esto se ejecuta en memoria, automáticamente desellado. **No usar en producción.**

### 2. Binario de Producción
1. Descarga la [versión oficial](https://releases.hashicorp.com/vault/).
2. Escribe un archivo de configuración `config.hcl`:
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
3. Inicia el servidor:
```bash
vault server -config=config.hcl
```
4. Inicializa si no se usa auto-unseal:
```bash
vault operator init   # prints 5 unseal keys and the root token
```
5. Desella (sin auto-unseal):
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
Para producción, usa el [chart oficial de Helm](https://github.com/hashicorp/vault-helm) con almacenamiento persistente y TLS.

### 4. Nube (HCP Vault)
Oferta SaaS completamente gestionada. No requiere gestión de clúster.

## Uso Básico

Todos los ejemplos asumen:
```bash
export VAULT_ADDR=http://127.0.0.1:8200
vault login root
```

#### Secretos Estáticos (KV v2)
```bash
# Write a secret
vault kv put secret/myapp/config password=s3cret user=admin

# Read a specific field
vault kv get -field=password secret/myapp/config

# Delete a version
vault kv delete secret/myapp/config
```

#### Secretos Dinámicos (Ejemplo con PostgreSQL)
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

#### Cifrado como Servicio (Transit)
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

## Políticas y Autenticación

### Ejemplo de Política (HCL)
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

### Métodos de Autenticación
- **Token** (integrado)
- **AppRole** (máquina a máquina)
- **Kubernetes** (vinculado a service account)
- **LDAP / OIDC** (usuarios humanos)
- **AWS / Azure / GCP** (metadatos de instancia en la nube)

Ejemplo con AppRole:
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

| Caso de Uso | Cómo Ayuda Vault |
|----------|-----------------|
| **Credenciales dinámicas de bases de datos** | Las aplicaciones obtienen usuarios de base de datos únicos con tiempo limitado. Sin contraseñas estáticas en configuraciones. |
| **Credenciales de nube para CI/CD** | Genera un rol de AWS IAM para una sola ejecución de pipeline. Se revoca automáticamente después del trabajo. |
| **PKI interna** | Ejecuta una CA interna. Vault emite certificados TLS de corta duración para mTLS entre servicios. |
| **Protección de datos (PII)** | El motor Transit cifra campos sensibles en bases de datos heredadas. La aplicación nunca toca la clave. |
| **Almacenamiento de secretos estáticos** | Almacena centralmente claves API, certificados y claves SSH con control de acceso detallado y registros de auditoría. |

## Lecturas Adicionales

- [Documentación Oficial](https://developer.hashicorp.com/vault)
- [Rutas de Aprendizaje de Vault (Interactivo)](https://learn.hashicorp.com/vault)
- [Referencia de la API de Vault](https://developer.hashicorp.com/vault/api-docs)
- [Helm Chart de HashiCorp Vault](https://github.com/hashicorp/vault-helm)
- [OpenBao – Fork de la Comunidad](https://openbao.org)

## Resumen

HashiCorp Vault es una piedra angular de la seguridad moderna nativa en la nube. Al centralizar la gestión de secretos, habilitar credenciales dinámicas y proporcionar cifrado como servicio, elimina los riesgos asociados con los secretos estáticos y la dispersión de secretos. Ya sea que se ejecute on-premises, en la nube o en Kubernetes, Vault encaja naturalmente en una arquitectura de confianza cero donde ninguna credencial es confiable más allá de su arrendamiento.