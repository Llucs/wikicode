---
title: HAProxy
description: HAProxy is a high-performance, open-source TCP/HTTP load balancer and reverse proxy that delivers extreme reliability, performance, and control for modern distributed systems.
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

HAProxy (High Availability Proxy) is the de‑facto standard open-source TCP and HTTP load balancer and proxy server. Written in C by Willy Tarreau, it is purpose‑built for distributing traffic across backend servers with extreme performance, reliability, and a minimal memory footprint. HAProxy powers many of the busiest websites and services on the internet, including GitHub, Reddit, Twitter/X, and Docker Hub.

## What is HAProxy?

HAProxy is a free, very fast, and reliable reverse proxy that offers high availability, load balancing, and proxying for TCP and HTTP-based applications. It runs on Linux, macOS, and FreeBSD. Its most common use is to improve the performance and reliability of a server environment by distributing the workload across multiple servers (e.g., web, application, database). Beyond basic load balancing, HAProxy provides advanced traffic management, SSL/TLS termination, content switching, health checks, session persistence, deep observability, and security features such as rate limiting and protocol hardening.

## Why HAProxy?

In modern infrastructure, services must handle millions of concurrent connections with zero downtime. General‑purpose web servers like Nginx or Apache can act as load balancers, but HAProxy is **designed specifically** for this role. It excels at:

- **Performance:** Can handle millions of concurrent connections on modest hardware thanks to an event‑driven, single‑threaded (or multi‑threaded) architecture.
- **Reliability:** Built with aggressive sanity checks; impossible conditions or endless loops result in an immediate crash with a dump, preventing silent data corruption.
- **Feature set:** Native SSL termination, HTTP/2, gRPC, QUIC/HTTP/3, advanced ACLs, stick‑tables, Prometheus metrics, and seamless reloads.
- **Security:** Protects backends from slow‑loris attacks, DDoS, and protocol‑level exploits.

## Installation

HAProxy is available in most package repositories, can be run via Docker, and can be compiled from source for custom builds.

### From Official Repositories

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

### Using Docker

```bash
docker run --name my-haproxy \
  -v /path/to/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro \
  -p 80:80 \
  -p 443:443 \
  haproxy:lts
```

### Compiling from Source (for custom features)

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

## Basic Configuration

HAProxy configuration is written in a single text file, typically located at `/etc/haproxy/haproxy.cfg`. The file is composed of logical sections:

| Section     | Purpose                                                  |
|-------------|----------------------------------------------------------|
| `global`    | Process‑wide settings (user, group, max connections, stats socket). |
| `defaults`  | Shared parameters for all frontends/backends (mode, timeouts, logging options). |
| `frontend`  | Traffic entry points: define IP/port bindings, ACLs, and default backends. |
| `backend`   | Pools of servers to forward traffic to. Defines load balancing algorithm, health checks, and persistence. |
| `listen`    | Convenience wrapper that combines frontend and backend for simple setups. |

### Example: Simple HTTP Load Balancer

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

### Example: TCP Load Balancer (e.g., MySQL)

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

### Enabling the Statistics Page

```cfg
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 10s
    # optionally restrict access
    stats auth admin:password
```

## Key Features with Command Examples

### 1. Load Balancing Algorithms

HAProxy supports dozens of balancing algorithms. Some of the most common:

| Algorithm          | Description                                             |
|--------------------|---------------------------------------------------------|
| `roundrobin`       | Distributes requests sequentially across servers.       |
| `leastconn`        | Sends requests to the server with fewest connections.   |
| `source`           | Hashes the source IP, ensuring a client hits the same server (useful for persistence). |
| `uri`              | Hashes the request URI, useful for caching setups.      |
| `hdr(name)`        | Hashes the value of a header (e.g., `X-Session-ID`).    |

Example configuration:

```cfg
backend webservers
    balance hdr(host)
    server web1 192.168.1.10:80 check
    server web2 192.168.1.11:80 check
```

### 2. Health Checks

Active health checks are configured with the `check` keyword on each server line. You can fine‑tune them:

```cfg
server web1 192.168.1.10:80 check inter 2s fall 3 rise 2
# inter    – check interval
# fall     – number of failures before marking server down
# rise     – number of successes before marking server up
```

You can also perform layer‑7 checks (`option httpchk`) for HTTP backends:

```cfg
backend webservers
    option httpchk HEAD /health HTTP/1.1\r\nHost:\ localhost
    server web1 192.168.1.10:80 check
```

### 3. SSL/TLS Offloading

Terminate HTTPS at the load balancer and forward plain HTTP to backends:

```cfg
frontend https-in
    bind *:443 ssl crt /etc/ssl/certs/example.pem
    default_backend webservers

backend webservers
    server web1 192.168.1.10:80 check
```

You can also re‑encrypt to backends (SSL bridging) or verify client certificates.

### 4. Content Switching with ACLs

Use ACLs to route traffic based on headers, URL paths, TLS SNI, etc.

```cfg
frontend http-in
    bind *:80

    # Define ACLs
    acl is_api path_beg /api/
    acl is_static path_end .jpg .png .css .js

    # Use ACLs to choose backend
    use_backend api_servers if is_api
    use_backend static_servers if is_static
    default_backend webservers
```

### 5. Session Persistence (Stickiness)

Ensure a user’s requests always go to the same backend server:

```cfg
backend webservers
    balance roundrobin
    cookie SERVERID insert indirect nocache
    server web1 192.168.1.10:80 check cookie w1
    server web2 192.168.1.11:80 check cookie w2
```

Alternatively, use `stick‑table` persistence based on IP or a header.

### 6. Zero‑Downtime Reloads

Apply configuration changes without dropping connections:

```bash
haproxy -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid -sf $(cat /run/haproxy.pid)
```

Or via systemd:

```bash
systemctl reload haproxy
```

## Advanced Features

### Rate Limiting

```cfg
frontend http-in
    bind *:80

    # Allow 10 requests per second per IP, burst to 20
    stick-table type ip size 1m expire 10s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 20 }
    default_backend webservers
```

### HTTP/2 and gRPC

HAProxy supports HTTP/2 and can proxy gRPC without any special configuration beyond enabling `alpn`:

```cfg
frontend https-in
    bind *:443 ssl crt /etc/ssl/certs/example.pem alpn h2,http/1.1
    default_backend grpc_servers

backend grpc_servers
    server grpc1 10.0.0.1:50051 check
```

### QUIC / HTTP/3

Recent versions (≥2.5) include experimental QUIC support for UDP‑based HTTP/3:

```cfg
frontend quic-in
    bind quic4@:443 ssl crt /etc/ssl/certs/example.pem
    default_backend webservers
```

### Observability

- **Statistics page:** built‑in HTML/JSON endpoint (see earlier example).
- **Prometheus metrics:** use the `stats prometheus` option:

```cfg
frontend stats
    bind *:8405
    stats enable
    stats uri /metrics
    stats prometheus
```

- **Raw logging:** HAProxy outputs detailed logs (to syslog or a separate log file) that can be analyzed by tools like `tail`, `grep`, or shipped to ELK/Loki.

## Command‑Line Management

HAProxy provides a rich runtime API via a Unix socket or TCP socket. The `socat` utility is commonly used to send commands:

```bash
echo "show info" | socat stdio unix-connect:/run/haproxy.sock
echo "show stat" | socat stdio unix-connect:/run/haproxy.sock
echo "enable server webservers/web1" | socat stdio unix-connect:/run/haproxy.sock
```

The runtime API also supports dynamic server addition/removal, which is crucial for container environments.

## Security Considerations

- **Run as non‑root:** HAProxy drops privileges after binding ports. The `user` and `group` directives in `global` are mandatory.
- **Enable chroot:** Set `chroot /var/lib/haproxy` to isolate the process from the filesystem.
- **Restrict stats:** Use authentication, ACLs, or bind stats on a private interface.
- **Tune timeouts:** Prevents slow clients from exhausting connection pools.
- **Enable SYN flood protection:** Use the `tcp-smart-connect` and `tcp-smart-accept` options.

## Conclusion

HAProxy is a mature, battle‑tested component that forms the backbone of many high‑traffic, critical systems. Its laser focus on load balancing and proxying delivers unmatched performance, stability, and granular control. Whether you’re running a small blog or a globe‑spanning SaaS, HAProxy is an essential tool for any infrastructure engineer’s toolkit.

For further reading, consult the [official HAProxy documentation](https://www.haproxy.org/documentation/) or the [HAProxy Technologies site](https://www.haproxy.com/).