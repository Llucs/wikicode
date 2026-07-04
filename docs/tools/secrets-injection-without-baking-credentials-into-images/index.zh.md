---
title: 无嵌入凭据的 Docker 镜像密钥注入
description: 一种在容器镜像中安全管理和注入密钥的方法，而不直接嵌入凭据，确保部署管道中的更好安全性和合规性。
created: 2026-07-04
tags:
  - DevOps
  - Docker
  - Kubernetes
  - 安全
  - 密钥管理
status: 草稿
---

# 无嵌入凭据的 Docker 镜像密钥注入

密钥注入指的是安全管理和在运行时注入容器化应用程序中的敏感数据的过程。这通过不在 Docker 镜像中直接嵌入凭据或密钥来实现，而是提供这些凭据或密钥在运行时或部署阶段。

## 关键特性

1. **运行时安全**：凭据从未嵌入镜像中，减少了镜像扫描期间或因漏洞而导致泄露的风险。
2. **灵活性**：无需重建和重新部署镜像即可轻松更新密钥。
3. **可扩展性**：在多容器、微服务环境中安全地管理密钥。
4. **合规性**：帮助组织遵循数据安全和合规性的监管标准和最佳实践。

## 使用场景

1. **数据库凭据**：安全地管理数据库用户名和密码。
2. **API密钥**：安全地存储和注入各种服务的API密钥。
3. **配置管理**：注入不属于应用程序代码库的配置设置。
4. **加密密钥**：管理用于数据静止或传输保护的加密密钥。

## 安装

根据所使用的特定密钥管理工具或解决方案的安装过程有所不同。以下是几种常见解决方案的一般步骤：

### Kubernetes 密钥

1. **前提条件**：Kubernetes 集群。
2. **安装**：不需要显式安装，Kubernetes 密钥是内置功能。
3. **步骤**：
   1. 使用 `kubectl` 或 Kubernetes 控制台创建密钥。
   2. 在部署 YAML 或 Kubernetes 模板中引用密钥。
   3. 将密钥作为卷挂载或在 pod 中作为环境变量使用。

```yaml
# 示例 YAML 用于引用密钥
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

### Docker 密钥

1. **前提条件**：Docker Swarm。
2. **安装**：不需要显式安装，Docker Swarm 支持密钥作为内置功能。
3. **步骤**：
   1. 使用 `docker swarm secret create` 命令创建 Docker 密钥。
   2. 在服务定义中引用密钥。

```bash
# 创建 Docker 密钥
docker swarm secret create my-secret my-value

# 在服务定义中引用密钥
services:
  my-service:
    secrets:
      - my-secret
    command: ["--my-key=$(MY_SECRET_KEY)"]
```

### HashiCorp Vault

1. **前提条件**：HashiCorp Vault 服务器。
2. **安装**：在服务器上下载并安装 HashiCorp Vault，或使用托管服务。
3. **步骤**：
   1. 初始化并解封 Vault。
   2. 在 Vault 中创建并存储密钥。
   3. 使用 Vault API 在运行时检索密钥。

```bash
# 初始化并解封 Vault
vault operator init
vault unseal <解封密钥>

# 在 Vault 中创建并存储密钥
vault kv put secret/my-secret key=my-value

# 使用 Vault API 检索密钥
vault read secret/my-secret
```

## 基本用法

### 创建密钥

1. **Kubernetes**：`kubectl create secret generic my-secret --from-literal=my-key=my-value`
2. **Docker Swarm**：`docker swarm secret create my-secret my-value`
3. **HashiCorp Vault**：`vault kv put secret/my-secret key=my-value`

### 引用密钥

1. **Kubernetes**：
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

2. **Docker Swarm**：
   ```yaml
   services:
     my-service:
       secrets:
         - my-secret
       command: ["--my-key=$(MY_SECRET_KEY)"]
   ```

3. **HashiCorp Vault**：
   - 通过 Vault API 或使用 `vault read` 命令检索密钥。

通过采用密钥注入实践，组织可以显著增强其容器化应用程序的安全状况，确保在整个开发和部署生命周期中敏感数据的安全和可管理性。