---
title: HAProxy
description: HAProxy是一个高性能、开源的TCP/HTTP负载均衡器和反向代理，为现代分布式系统提供极高的可靠性、性能和控制力。
created: 2026-06-17
tags:
  - load-balancer
  - proxy
  - tcp
  - http
  - haproxy
  - devops
status: draft
---

# HAProxy

HAProxy（高可用性代理）是事实上的标准开源TCP和HTTP负载均衡器和代理服务器。由Willy Tarreau用C语言编写，它专门设计用于以极高的性能、可靠性和最小的内存占用在服务器间分发流量。HAProxy为互联网上许多最繁忙的网站和服务提供支持，包括GitHub、Reddit、Twitter/X和Docker Hub。

## 什么是HAProxy？

HAProxy是一个免费、非常快速且可靠的反向代理，为基于TCP和HTTP的应用程序提供高可用性、负载均衡和代理功能。它运行在Linux、macOS和FreeBSD上。其最常见的用途是通过将工作负载分发到多台服务器（例如Web、应用、数据库）来提高服务器环境的性能和可靠性。除了基本的负载均衡，HAProxy还提供高级流量管理、SSL/TLS终止、内容交换、健康检查、会话持久性、深度可观测性以及限流和协议加固等安全功能。

## 为什么选择HAProxy？

在现代化基础设施中，服务必须能够处理数百万并发连接且零停机。通用Web服务器如Nginx或Apache也可以充当负载均衡器，但HAProxy是**专门设计**用于此角色的。它在以下方面表现出色：

- **性能：** 采用事件驱动、单线程（或多线程）架构，即使在普通硬件上也能处理数百万并发连接。
- **可靠性：** 内置严格的完整性检查；不可能的条件或无限循环会立即导致崩溃并转储，防止静默数据损坏。
- **功能集：** 原生SSL终止、HTTP/2、gRPC、QUIC/HTTP/3、高级ACL、stick-table、Prometheus指标和无缝重载。
- **安全性：** 保护后端免受Slowloris攻击、DDoS和协议级漏洞。

## 安装

HAProxy在大多数软件包仓库中可用，可以通过Docker运行，也可以从源代码编译以定制构建。

### 从官方仓库安装

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install haproxy

# RHEL / CentOS / Fedora
sudo yum install haproxy

# Alpine
apk add haproxy

# FreeBSD
pkg install haproxy
```

### 使用Docker

```bash
docker run --name my-haproxy \
  -v /path/to/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro \
  -p 80:80 \
  -p 443:443 \
  haproxy:lts
```

### 从源代码编译（用于自定义功能）

```bash
# Install build dependencies (example for Debian)
sudo apt install build-essential libssl-dev libpcre3-dev zlib1g-dev liblua5.3-dev

# Download and build
wget https://www.haproxy.org/download/3.0/src/haproxy-3.0.0.tar.gz
tar xzf haproxy-3.0.0.tar.gz
cd haproxy-3.0.0
make TARGET=linux-glibc USE_OPENSSL=1 USE_PCRE=1 USE_ZLIB=1 USE_LUA=1
sudo make install
```

## 基本配置

HAProxy配置写在一个文本文件中，通常位于`/etc/haproxy/haproxy.cfg`。该文件由以下逻辑段组成：

| 段         | 用途                                                  |
|------------|------------------------------------------------------|
| `global`   | 进程级设置（用户、组、最大连接数、统计套接字）。          |
| `defaults` | 所有前端/后端的共享参数（模式、超时、日志选项）。         |
| `frontend` | 流量入口点：定义IP/端口绑定、ACL和默认后端。             |
| `backend`  | 转发流量到服务器的池。定义负载均衡算法、健康检查和持久性。 |
| `listen`   | 便捷封装，将前端和后端组合在一起，用于简单设置。          |

### 示例：简单HTTP负载均衡器

```cfg
global
    maxconn 4096
    user haproxy
    group haproxy

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms
    option httplog

frontend http-in
    bind *:80
    default_backend webservers

backend webservers
    balance roundrobin
    server web1 192.168.1.10:80 check
    server web2 192.168.1.11:80 check
```

### 示例：TCP负载均衡器（例如MySQL）

```cfg
frontend mysql-in
    bind *:3306
    mode tcp
    default_backend mysql_servers

backend mysql_servers
    mode tcp
    balance leastconn
    server db1 10.0.0.1:3306 check
    server db2 10.0.0.2:3306 check
```

### 启用统计页面

```cfg
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 10s
    # optionally restrict access
    stats auth admin:password
```

## 带命令示例的关键功能

### 1. 负载均衡算法

HAProxy支持数十种负载均衡算法。一些最常用的：

| 算法              | 描述                                                 |
|-------------------|----------------------------------------------------|
| `roundrobin`      | 按顺序在服务器之间分发请求。                          |
| `leastconn`       | 将请求发送到连接数最少的服务器。                      |
| `source`          | 对源IP进行哈希，确保客户端始终到达同一台服务器（用于持久性）。 |
| `uri`             | 对请求URI进行哈希，适用于缓存设置。                   |
| `hdr(name)`       | 对标头值（例如 `X-Session-ID`）进行哈希。             |

配置示例：

```cfg
backend webservers
    balance hdr(host)
    server web1 192.168.1.10:80 check
    server web2 192.168.1.11:80 check
```

### 2. 健康检查

主动健康检查通过在每个服务器行上使用`check`关键字进行配置。可以对其进行微调：

```cfg
server web1 192.168.1.10:80 check inter 2s fall 3 rise 2
# inter    – 检查间隔
# fall     – 将服务器标记为离线所需的失败次数
# rise     – 将服务器标记为在线所需的成功次数
```

您还可以为HTTP后端执行7层检查（`option httpchk`）：

```cfg
backend webservers
    option httpchk HEAD /health HTTP/1.1\r\nHost:\ localhost
    server web1 192.168.1.10:80 check
```

### 3. SSL/TLS卸载

在负载均衡器处终止HTTPS，并将明文HTTP转发到后端：

```cfg
frontend https-in
    bind *:443 ssl crt /etc/ssl/certs/example.pem
    default_backend webservers

backend webservers
    server web1 192.168.1.10:80 check
```

您还可以对后端进行重新加密（SSL桥接）或验证客户端证书。

### 4. 使用ACL进行内容交换

使用ACL基于标头、URL路径、TLS SNI等路由流量。

```cfg
frontend http-in
    bind *:80

    # 定义ACL
    acl is_api path_beg /api/
    acl is_static path_end .jpg .png .css .js

    # 使用ACL选择后端
    use_backend api_servers if is_api
    use_backend static_servers if is_static
    default_backend webservers
```

### 5. 会话持久性（粘性）

确保用户的请求始终发送到同一台后端服务器：

```cfg
backend webservers
    balance roundrobin
    cookie SERVERID insert indirect nocache
    server web1 192.168.1.10:80 check cookie w1
    server web2 192.168.1.11:80 check cookie w2
```

或者，使用基于IP或标头的`stick-table`持久性。

### 6. 零停机重载

应用配置更改而不断开连接：

```bash
haproxy -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid -sf $(cat /run/haproxy.pid)
```

或者通过systemd：

```bash
systemctl reload haproxy
```

## 高级功能

### 限速

```cfg
frontend http-in
    bind *:80

    # 每个IP每秒允许10个请求，突发可达20个
    stick-table type ip size 1m expire 10s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 20 }
    default_backend webservers
```

### HTTP/2 和 gRPC

HAProxy支持HTTP/2，只需启用`alpn`即可代理gRPC，无需特殊配置：

```cfg
frontend https-in
    bind *:443 ssl crt /etc/ssl/certs/example.pem alpn h2,http/1.1
    default_backend grpc_servers

backend grpc_servers
    server grpc1 10.0.0.1:50051 check
```

### QUIC / HTTP/3

近期的版本（≥2.5）包含基于UDP的HTTP/3的实验性QUIC支持：

```cfg
frontend quic-in
    bind quic4@:443 ssl crt /etc/ssl/certs/example.pem
    default_backend webservers
```

### 可观测性

- **统计页面：** 内置HTML/JSON端点（参见前面的示例）。
- **Prometheus指标：** 使用`stats prometheus`选项：

```cfg
frontend stats
    bind *:8405
    stats enable
    stats uri /metrics
    stats prometheus
```

- **原始日志：** HAProxy输出详细的日志（到syslog或单独的日志文件），可以使用`tail`、`grep`等工具分析，或发送到ELK/Loki。

## 命令行管理

HAProxy通过Unix套接字或TCP套接字提供丰富的运行时API。通常使用`socat`工具发送命令：

```bash
echo "show info" | socat stdio unix-connect:/run/haproxy.sock
echo "show stat" | socat stdio unix-connect:/run/haproxy.sock
echo "enable server webservers/web1" | socat stdio unix-connect:/run/haproxy.sock
```

运行时API还支持动态添加/移除服务器，这对于容器环境至关重要。

## 安全考虑

- **以非root身份运行：** HAProxy在绑定端口后丢弃权限。`global`配置段中的`user`和`group`指令是强制性的。
- **启用chroot：** 设置`chroot /var/lib/haproxy`以将进程与文件系统隔离。
- **限制统计访问：** 使用身份验证、ACL或将统计页面绑定在私有接口上。
- **调整超时：** 防止慢客户端耗尽连接池。
- **启用SYN洪水保护：** 使用`tcp-smart-connect`和`tcp-smart-accept`选项。

## 结论

HAProxy是一个成熟、久经考验的组件，构成许多高流量、关键系统的骨干。它对负载均衡和代理的专注提供了无与伦比的性能、稳定性和精细控制。无论您是在运营一个小型博客还是一个全球范围的SaaS，HAProxy都是任何基础设施工程师工具箱中的必备工具。

有关更多信息，请参考[官方HAProxy文档](https://www.haproxy.org/documentation/)或[HAProxy技术网站](https://www.haproxy.com/)。