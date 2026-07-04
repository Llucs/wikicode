---
title: Secrets Injection Without Baking Credentials Into Docker Images
description: A method for securely managing and injecting secrets into container images without embedding them directly, ensuring better security and compliance in deployment pipelines.
created: 2026-07-04
tags:
  - DevOps
  - Docker
  - Kubernetes
  - Security
  - Secrets Management
status: draft
---

# Secrets Injection Without Baking Credentials Into Docker Images

Secrets injection refers to the process of securely managing and injecting sensitive data into containerized applications at runtime. This is achieved by not embedding credentials or secrets directly into the Docker image but rather by providing them at runtime or during the deployment phase.

## Key Features

1. **Runtime Security**: Credentials are never baked into the image, reducing the risk of exposure during image scanning or leakage due to vulnerabilities.
2. **Flexibility**: Allows for easy updates to secrets without the need to rebuild and redeploy the image.
3. **Scalability**: Facilitates secure management of secrets in a multi-container, microservices environment.
4. **Compliance**: Helps organizations adhere to regulatory standards and best practices for data security and compliance.

## Use Cases

1. **Database Credentials**: Securely managing database usernames and passwords.
2. **API Keys**: Safely storing and injecting API keys for various services.
3. **Configuration Management**: Injecting configuration settings that are not part of the application codebase.
4. **Encryption Keys**: Managing encryption keys for data-at-rest or in-transit protection.

## Installation

The installation process varies depending on the specific tool or solution used for secrets management. Here are general steps for some common solutions:

### Kubernetes Secrets

1. **Prerequisites**: Kubernetes cluster.
2. **Installation**: No explicit installation is needed; Kubernetes secrets are a built-in feature.
3. **Steps**:
   1. Create a secret using `kubectl` or a Kubernetes dashboard.
   2. Reference the secret in your deployment YAML or Kubernetes manifest.
   3. Mount the secret as a volume or use it as an environment variable in your pods.

```yaml
# Example YAML for referencing a secret
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

### Docker Secrets

1. **Prerequisites**: Docker Swarm.
2. **Installation**: No explicit installation needed; Docker Swarm supports secrets out of the box.
3. **Steps**:
   1. Create a Docker secret using the `docker swarm secret create` command.
   2. Reference the secret in your service definition.

```bash
# Create a Docker secret
docker swarm secret create my-secret my-value

# Reference the secret in a service definition
services:
  my-service:
    secrets:
      - my-secret
    command: ["--my-key=$(MY_SECRET_KEY)"]
```

### HashiCorp Vault

1. **Prerequisites**: HashiCorp Vault server.
2. **Installation**: Download and install HashiCorp Vault on your server or use a managed service.
3. **Steps**:
   1. Initialize and unseal the Vault.
   2. Create and store secrets in the Vault.
   3. Use the Vault API to retrieve secrets at runtime.

```bash
# Initialize and unseal Vault
vault operator init
vault unseal <unseal-key>

# Create and store a secret
vault kv put secret/my-secret key=my-value

# Retrieve the secret using the Vault API
vault read secret/my-secret
```

## Basic Usage

### Creating a Secret

1. **Kubernetes**: `kubectl create secret generic my-secret --from-literal=my-key=my-value`
2. **Docker Swarm**: `docker swarm secret create my-secret my-value`
3. **HashiCorp Vault**: `vault kv put secret/my-secret key=my-value`

### Referencing the Secret

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

2. **Docker Swarm**:
   ```yaml
   services:
     my-service:
       secrets:
         - my-secret
       command: ["--my-key=$(MY_SECRET_KEY)"]
   ```

3. **HashiCorp Vault**:
   - Secrets can be retrieved via the Vault API or using the `vault read` command.

By adopting secrets injection practices, organizations can significantly enhance the security posture of their containerized applications, ensuring that sensitive data remains protected and manageable throughout the development and deployment lifecycle.