---
title: Portainer
description: 一款自托管的容器与编排管理工具，集中管理跨多个环境的治理、RBAC/SSO 和运维控制。
created: 2026-06-15
tags:
  - docker
  - kubernetes
  - container-management
  - devops
  - open-source
  - orchestration
  - self-hosted
  - portainer-ce
status: draft
ecosystem: containers
---

# Portainer

## 概述

Portainer 是行业标准的开源“单一管理界面”，用于管理容器化环境。由 Neil Cresswell 设计，于 2017 年从 DockerUI 分支而来，Portainer 旨在消除 Docker、Docker Swarm、Kubernetes、Azure ACI 和 Hashicorp Nomad 的陡峭学习曲线和运维开销。它本身以轻量级容器运行（或通过 Helm chart），并提供一个功能强大的 Web UI，底层由功能完整的 REST API 支持。

Portainer 在社区版 (CE) 下使用 AGPLv3 许可，另有商业版 Business Edition (BE)，增加了企业功能，如 FIPS 合规性、细粒度 RBAC 和专属支持。

## 为什么选择 Portainer？

- **统一控制平面：** 通过单一 Web 界面管理你的所有容器引擎，无需在多个 CLI 之间切换上下文。
- **降低复杂性：** 非专业团队无需学习复杂的 `kubectl` 或 `docker-compose` 命令即可部署和管理应用程序。
- **GitOps 就绪：** 堆栈可直接链接到 Git 仓库。任何推送到仓库的操作都会触发自动重新部署。
- **边缘计算：** 使用 Edge Agents 安全地管理位于 NAT 或防火墙之后的数千台设备。
- **轻量且非侵入式：** Portainer 不会取代你现有的编排器；它与之并行，通过套接字或专用的 Agent 容器读取 Docker/Kubernetes API。

## 架构

Portainer 采用标准的服务器-代理模型：

1.  **Portainer Server (portainer/portainer-ce)：** 主应用程序。提供 Web UI 和 REST API。这是你浏览器指向的节点。
2.  **Portainer Agent (portainer/agent)：** 轻量级边车容器，部署在每个你想远程管理的 Docker 主机或 Kubernetes 节点上。Agent 与本地 Docker 套接字通信，并在 9001 端口暴露一个安全的 API。
3.  **Edge Agent：** 标准代理的变体，专为远程位置设计。它向 Portainer Server 发起一个*出站*隧道，允许通过严格的防火墙进行管理，无需打开入站端口。

```text
[Admin Browser] <--> [Portainer Server :9443]
                         |
            +------------+-------------+
            |            |             |
    [Docker Agent 1] [Docker Agent 2] [K8s Cluster (Helm)]
            |            |
    [Docker Daemon] [Docker Daemon]
```

## 安装

### Docker 独立部署（快速开始）

这是用于管理本地或少量 Docker 主机的最常用方法。

```bash
# 为 Portainer 数据创建持久卷
docker volume create portainer_data

# 运行 Portainer Server 容器
docker run -d -p 8000:8000 -p 9443:9443 --name portainer \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v portainer_data:/data \
    portainer/portainer-ce:lts
```

- `-p 9443:9443`：Web UI 和 API (HTTPS)。
- `-p 8000:8000`：（可选）用于 Edge Agent 连接的 TCP 隧道。
- `-v /var/run/docker.sock`：允许 Portainer 管理其运行的主机。
- `:lts`：长期支持标签。**生产环境中始终使用 `:lts`。**

### Docker Swarm

将 Portainer 作为全局服务部署到你的 Swarm 集群。

```bash
curl -L https://downloads.portainer.io/ce2-19/portainer-agent-stack.yml -o portainer-agent-stack.yml

docker stack deploy -c portainer-agent-stack.yml portainer
```

### Kubernetes (Helm)

使用官方 Helm chart 将 Portainer 部署到你的 Kubernetes 集群。

```bash
helm repo add portainer https://portainer.github.io/k8s/
helm repo update

helm upgrade --install portainer portainer/portainer \
    --namespace portainer --create-namespace \
    --set service.type=LoadBalancer \
    --set service.httpPort=9000 \
    --set service.httpsPort=9443
```

### 离线安装

对于没有互联网访问的环境，预先拉取镜像。

```bash
# 在有互联网访问的机器上
docker pull portainer/portainer-ce:lts
docker pull portainer/agent:lts

# 标记并推送到你的内部仓库
docker tag portainer/portainer-ce:lts <internal-registry>/portainer-ce:lts
docker tag portainer/agent:lts <internal-registry>/agent:lts
docker push <internal-registry>/portainer-ce:lts
docker push <internal-registry>/agent:lts
```

## 初始设置

1.  打开浏览器访问 `https://<SERVER_IP>:9443/`。
2.  为 `admin` 用户创建一个强密码。
3.  将出现快速设置向导。选择 **Docker**，然后选择 **Socket** 连接到本地 Docker 守护进程。
4.  点击 **Connect**。你现在位于 **Home** 页面——这是你的环境选择器。

## 主要功能与命令示例

### 1. 多环境管理

通过部署 Portainer Agent 连接远程 Docker 主机。

**在远程主机（目标）上：**
```bash
docker run -d -p 9001:9001 --name portainer_agent \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /var/lib/docker/volumes:/var/lib/docker/volumes \
    portainer/agent:lts
```

**在 Portainer Server UI 中：**
导航到 **Environments** > **Add Environment** > **Docker Agent**。
输入远程主机的 IP 和端口 (9001)。点击 **Connect**。

### 2. 应用模板（一键部署）

Portainer 包含一个预定义应用程序的目录（如 Nginx、MySQL、WordPress 等）。

**工作流程：**
1. 侧边栏 > **App Templates**。
2. 点击一个模板（例如 **Nginx**）。
3. 自定义名称、端口、环境变量。
4. 点击 **Deploy the stack**。

### 3. 堆栈与 GitOps

使用 Docker Compose 或 Kubernetes 清单文件部署复杂应用程序。堆栈可以链接到 Git 仓库以支持 GitOps 工作流程。

**手动 Compose 部署：**
将以下内容粘贴到 **Stacks** > **Add Stack** > **Web Editor** 中：
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
  db:
    image: postgres:13
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: example
volumes:
  pgdata:
```

**GitOps 设置：**
1. **Stacks** > **Add Stack** > **Repository**。
2. 输入 Git 仓库 URL 和 Compose 文件的路径。
3. 启用 **Automatic Updates**。
4. 点击 **Deploy the stack**。任何 `git push` 都会触发重新部署。

### 4. Kubernetes 管理

Portainer 抽象了 `kubectl` 的复杂性。你可以通过表单或 YAML 创建 Namespace、Deployment、Service 和 Ingress。

**示例：** 部署一个简单的 nginx 工作负载。
1. **Environments** > 选择你的 **Kubernetes cluster**。
2. **Kubernetes** > **Workloads** > **Add Workload**。
3. 填写表单（Name: `nginx`, Image: `nginx:alpine`, Port: `80`）。
4. 点击 **Deploy**。

### 5. 注册表

集中管理 Docker Hub、GitLab、Quay、Amazon ECR 和 Google Container Registry 的凭据。

1. **Registries** > **Add Registry**。
2. 选择你的提供商（例如 **Docker Hub**）。
3. 输入你的凭据（用户名/访问令牌）。

### 6. 边缘计算

管理位于 NAT/防火墙之后的远程设备（IoT、零售、现场站点）。服务器会生成一个 `EDGE_ID` 和 `EDGE_KEY`。

**在边缘设备上：**
```bash
docker run -d \
  -e EDGE=1 \
  -e EDGE_ID=<EDGE_ID> \
  -e EDGE_KEY=<EDGE_KEY> \
  -e CAP_HOST_MANAGEMENT=1 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name portainer_edge_agent \
  portainer/agent:lts
```

### 7. REST API

Portainer 拥有丰富的 REST API。在 **Settings** > **Security** 中生成一个 API 密钥。

```bash
# 列出所有环境
curl -X GET 'https://<SERVER_IP>:9443/api/endpoints' \
    -H 'X-API-Key: ptr_xxxxxxxxxxxx' | jq .

# 部署一个堆栈
curl -X POST 'https://<SERVER_IP>:9443/api/stacks' \
    -H 'X-API-Key: ptr_xxxxxxxxxxxx' \
    -H 'Content-Type: application/json' \
    -d '{
      "Name": "my-api-stack",
      "StackFileContent": "version: \"3.8\"\nservices:\n  web:\n    image: nginx:alpine",
      "SwarmID": "",
      "EndpointID": 1
    }'
```

## 版本对比

| 功能 | Community Edition (CE) | Business Edition (BE) |
|---|---|---|
| 许可协议 | AGPLv3 | Commercial |
| 多环境 | 无限制 | 无限制 |
| GitOps | 是 | 是 |
| 边缘计算 | 受限 | 完整 (Edge Groups, Stacks, Jobs) |
| RBAC / SSO | 基础 | 高级 (AD/LDAP/OAuth, 团队角色, 资源控制) |
| 注册表管理 | 手动 | 集中治理 |
| 支持 | 社区 | 商业 (7x24x365) |
| FIPS 合规性 | 否 | 是 |

## 最佳实践

1.  **使用 `:lts` 版本。** 不要在生产环境中使用 `:latest` 标签；它对应的是前沿构建版本。
2.  **专用 Server 节点。** 不要将大量工作负载运行在 Portainer Server 容器上。仅将其用作管理节点。
3.  **定期备份 `portainer_data`。** 运行以下命令备份卷：
    ```bash
    docker run --rm -v portainer_data:/data -v $(pwd):/backup alpine tar cvf /backup/portainer_backup.tar /data
    ```
4.  **使用合适的 TLS 进行安全保护。** 替换生产环境中的自签名证书。
    ```bash
    docker run -d -p 9443:9443 --name portainer \
        -v /path/to/fullchain.pem:/certs/portainer.crt \
        -v /path/to/privkey.pem:/certs/portainer.key \
        -v portainer_data:/data \
        portainer/portainer-ce:lts
    ```

## 故障排除

### Agent 连接失败
- 确保目标机器上的 `9001` 端口是开放的。
- 验证 Portainer Agent 容器正在运行。
- 如果使用了防火墙，确保 Server 能够向 Agent 发起出站连接。

### 忘记管理员密码
一个辅助容器会生成一个哈希值，你可以安全地设置它。
```bash
docker run --rm -v portainer_data:/data portainer/helper-reset-password
```

### Portainer 无法启动
检查日志：
```bash
docker logs portainer
```
常见问题包括卷数据损坏、Portainer 版本不匹配或主机 Docker 守护进程权限错误。

## 参考资源

- **官方网站：** [https://www.portainer.io/](https://www.portainer.io/)
- **GitHub：** [https://github.com/portainer/portainer](https://github.com/portainer/portainer)
- **官方文档：** [https://docs.portainer.io/](https://docs.portainer.io/)
- **Docker Hub：** [portainer/portainer-ce](https://hub.docker.com/r/portainer/portainer-ce)
- **Slack 社区：** [Portainer Slack](https://portainer.io/slack)