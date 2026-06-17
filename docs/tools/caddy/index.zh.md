---
title: Caddy：具有自动HTTPS功能的终极Web服务器
description: 一个企业级、开源、用Go编写的Web服务器，具有自动HTTPS、反向代理和Docker支持
created: 2026-06-16
tags:
  - web-server
  - reverse-proxy
  - automatic-https
  - go
  - docker
  - open-source
status: draft
---

# Caddy

Caddy 是一个功能强大、企业级、开源的 Web 服务器和反向代理，使用 Go 语言编写。它旨在易于使用，同时提供强大的安全性、自动 TLS 证书管理和现代化的配置 API。Caddy 由 Caddy 基金会维护，并广泛用于开发和生产环境。

## 主要特性

- **自动 HTTPS**：Caddy 自动为每个配置的域名获取和续期来自 Let’s Encrypt 或 ZeroSSL 的 TLS 证书。它默认管理 OCSP stapling、HTTP/2 和 HTTP/3 (QUIC)。
- **简单配置**：使用友好的 `Caddyfile` 或强大的 JSON API 进行动态配置。`Caddyfile` 是一个适配器，可转换为 JSON，提供简单性和灵活性。
- **反向代理和负载均衡**：完整的第7层反向代理，支持主动/被动健康检查、重试、断路器以及多种负载均衡策略（random、least connections、IP hash、header affinity）。
- **默认安全**：使用内存安全的 Go 编写，消除了缓冲区溢出漏洞。TLS 默认设置严格安全，Caddy 仅在必要时监听特权端口。
- **模块化架构**：核心最小化，功能通过模块扩展。使用 `xcaddy` 构建自定义二进制文件，只包含所需功能。
- **容器原生**：单一二进制文件，优雅关闭，平滑重载——非常适合 Docker 和 Kubernetes。

## 为什么使用 Caddy？

Caddy 消除了手动设置 HTTPS 的麻烦。它自动配置和续期证书，因此您无需担心 TLS 过期。其配置直观，是微服务、静态站点、API 和 SPA 的完美前端。JSON API 实现与自动化工具的无缝集成，而 `Caddyfile` 则提供了人性化的选择。一次编写，随处安全服务。

## 安装

Caddy 提供多种安装方式：

### 下载预构建的二进制文件

```bash
# Linux / macOS / Windows binary
curl -fsSL https://caddyserver.com/download/linux/amd64 -o caddy
chmod +x caddy
sudo mv caddy /usr/local/bin/
```

*或者从 [caddyserver.com/download](https://caddyserver.com/download) 下载*

### 包管理器

```bash
# Debian / Ubuntu
sudo apt install caddy

# macOS
brew install caddy

# Windows (winget)
winget install Caddy.Caddy
```

### Docker

```bash
docker pull caddy
```

### 使用 `xcaddy` 自定义构建

```bash
# Build Caddy with a specific plugin
xcaddy build --with github.com/caddyserver/transform-encoder

# Build with a custom version
xcaddy build v2.8.0 --with github.com/caddyserver/format-encoder
```

`xcaddy` 只编译包含您所需模块的单个二进制文件。

## 基本用法

### 静态文件服务器

```bash
# Serve the current directory on port 80 with automatic HTTPS
caddy file-server
```

### 快速反向代理

```bash
# Proxy traffic from yourdomain.com to a local backend
caddy reverse-proxy --from yourdomain.com --to localhost:8080
```

### Caddyfile 配置

在项目根目录创建一个 `Caddyfile`：

```caddyfile
example.com {
    root * /var/www/example
    file_server
}
```

然后运行：

```bash
caddy run
```

Caddy 会自动为 `example.com` 获取 TLS 证书并提供静态文件服务。

### JSON 配置

Caddy 的原生配置格式为 JSON。您可以通过管理 API 应用它：

```bash
caddy run

# In another terminal, POST the configuration
curl -X POST -H "Content-Type: application/json" -d '{
  "apps": {
    "http": {
      "servers": {
        "example": {
          "listen": [":443"],
          "routes": [
            {
              "match": [{"host": ["example.com"]}],
              "handle": [
                {
                  "handler": "subroute",
                  "routes": [
                    {
                      "handle": [
                        {"handler": "file_server", "root": "/var/www/example"}
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      }
    }
  }
}' http://localhost:2019/config/
```

JSON API 是事实的来源；`Caddyfile` 只是一个适配器。

## 深入主要特性

### 自动 HTTPS

```caddyfile
mydomain.com {
    tls you@email.com   # Optional email for Let's Encrypt notices
}
```

Caddy 自动处理证书颁发、续期以及 HTTP 到 HTTPS 的重定向。它支持通配符证书、自定义 ACME 端点（例如 ZeroSSL）以及按需 TLS。

### 带负载均衡的反向代理

```caddyfile
api.example.com {
    reverse_proxy api1:8080 api2:8080 api3:8080 {
        lb_policy least_conn
        health_uri /health
        health_interval 10s
    }
}
```

策略：`random`、`least_conn`、`ip_hash`、`uri_hash`、`header`、`first`、`round_robin`。

### 模板化与动态站点

Caddy 可以执行模板来生成动态内容，无需单独的后端：

```caddyfile
example.com {
    templates
    root * /var/www/example
}
```

### 认证

模块化认证（例如 JWT、basic auth）可以通过插件添加：

```caddyfile
example.com {
    basic_auth {
        admin $2a$14$hash...
    }
}
```

### HTTP/3 (QUIC)

在 `Caddyfile` 中启用 HTTP/3：

```caddyfile
{
    servers {
        protocol {
            quic
        }
    }
}
```

## Docker 集成

Caddy 是容器化环境中的一等公民。

### 从 Docker 容器提供静态文件服务

```dockerfile
FROM caddy:latest
COPY . /usr/share/caddy
```

运行：

```bash
docker build -t my-site .
docker run -d -p 80:80 -p 443:443 -e CADDY_INGRESS_NETWORKS=caddy my-site
```

### 在 Docker Compose 中用作反向代理

```yaml
version: "3.8"
services:
  caddy:
    image: caddy:latest
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
  app:
    image: my-app:latest
    expose:
      - "8080"
```

**Caddyfile**：

```caddyfile
mydomain.com {
    reverse_proxy app:8080
}
```

Caddy 通过 Docker 网络自动发现 `app` 容器。

### 在 Docker 中优雅重载

```bash
# After changing the Caddyfile, reload without downtime
docker exec -w /etc/caddy <container_name> caddy reload
```

## 生命周期管理

```bash
# Run in foreground
caddy run

# Run as background daemon
caddy start

# Stop the daemon
caddy stop

# Gracefully reload configuration (Linux)
caddy reload

# Validate a Caddyfile
caddy validate
```

## 结论

Caddy 通过自动化 HTTPS、提供简洁的配置模型以及与现代化技术栈无缝集成，简化了 Web 服务。无论您是在部署静态站点、微服务后端还是完整的 API 网关，Caddy 都能为您提供安全性、性能和易用性——全部包含在一个二进制文件中。凭借强大的 Docker 支持和活跃的插件生态系统，它同样是开发人员和运维团队的绝佳选择。