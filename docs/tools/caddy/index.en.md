---
title: Caddy: The Ultimate Web Server with Automatic HTTPS
description: An enterprise-ready, open-source web server with automatic HTTPS, reverse proxy, and Docker support, written in Go.
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

Caddy is a powerful, enterprise-ready, open-source web server and reverse proxy written in Go. It is designed to be simple to use while providing robust security, automatic TLS certificate management, and a modern configuration API. Caddy is maintained by the Caddy Foundation and widely adopted for both development and production environments.

## Key Features

- **Automatic HTTPS**: Caddy automatically obtains and renews TLS certificates from Let’s Encrypt or ZeroSSL for every domain configured. It manages OCSP stapling, HTTP/2, and HTTP/3 (QUIC) out of the box.
- **Simple Configuration**: Use either a friendly `Caddyfile` or a powerful JSON API for dynamic configuration. The `Caddyfile` is an adapter that translates to JSON, giving you simplicity and flexibility.
- **Reverse Proxy & Load Balancing**: Full Layer 7 reverse proxy with active/passive health checks, retries, circuit breakers, and multiple load-balancing policies (random, least connections, IP hash, header affinity).
- **Security by Default**: Written in memory-safe Go, eliminating buffer overflow vulnerabilities. TLS defaults are strictly secure, and Caddy listens on privileged ports only when necessary.
- **Modular Architecture**: The core is minimal; functionality is extended via modules. Build custom binaries with `xcaddy` to include only the features you need.
- **Container Native**: Single binary, clean shutdowns, graceful reloads – ideal for Docker and Kubernetes.

## Why Use Caddy?

Caddy eliminates the pain of manual HTTPS setup. It automatically provisions and renews certificates, so you never have to worry about expiring TLS. Its configuration is intuitive, and it serves as a perfect front-end for microservices, static sites, APIs, and SPAs. The JSON API enables seamless integration with automation tools, while the `Caddyfile` offers a human-friendly alternative. Write once, serve securely everywhere.

## Installation

Caddy offers multiple installation methods:

### Download a Pre-built Binary

```bash
# Linux / macOS / Windows binary
curl -fsSL https://caddyserver.com/download/linux/amd64 -o caddy
chmod +x caddy
sudo mv caddy /usr/local/bin/
```

*Or download from [caddyserver.com/download](https://caddyserver.com/download)*

### Package Managers

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

### Custom Build with `xcaddy`

```bash
# Build Caddy with a specific plugin
xcaddy build --with github.com/caddyserver/transform-encoder

# Build with a custom version
xcaddy build v2.8.0 --with github.com/caddyserver/format-encoder
```

`xcaddy` compiles a single binary with only the modules you want.

## Basic Usage

### Static File Server

```bash
# Serve the current directory on port 80 with automatic HTTPS
caddy file-server
```

### Quick Reverse Proxy

```bash
# Proxy traffic from yourdomain.com to a local backend
caddy reverse-proxy --from yourdomain.com --to localhost:8080
```

### Caddyfile Configuration

Create a `Caddyfile` in your project root:

```caddyfile
example.com {
    root * /var/www/example
    file_server
}
```

Then run:

```bash
caddy run
```

Caddy will automatically obtain a TLS certificate for `example.com` and serve the static files.

### JSON Configuration

Caddy’s native config format is JSON. You can apply it via the admin API:

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

The JSON API is the source of truth; the `Caddyfile` is just an adapter.

## Key Features in Depth

### Automatic HTTPS

```caddyfile
mydomain.com {
    tls you@email.com   # Optional email for Let's Encrypt notices
}
```

Caddy handles certificate issuance, renewal, and HTTP-to-HTTPS redirects automatically. It supports wildcard certificates, custom ACME endpoints (e.g., ZeroSSL), and on‑demand TLS.

### Reverse Proxy with Load Balancing

```caddyfile
api.example.com {
    reverse_proxy api1:8080 api2:8080 api3:8080 {
        lb_policy least_conn
        health_uri /health
        health_interval 10s
    }
}
```

Policies: `random`, `least_conn`, `ip_hash`, `uri_hash`, `header`, `first`, `round_robin`.

### Templating & Dynamic Sites

Caddy can execute templates for dynamic content without a separate backend:

```caddyfile
example.com {
    templates
    root * /var/www/example
}
```

### Authentication

Modular auth (e.g., JWT, basic auth) can be added via plugins:

```caddyfile
example.com {
    basic_auth {
        admin $2a$14$hash...
    }
}
```

### HTTP/3 (QUIC)

Enable HTTP/3 in your `Caddyfile`:

```caddyfile
{
    servers {
        protocol {
            quic
        }
    }
}
```

## Docker Integration

Caddy is a first-class citizen in containerized environments.

### Serve Static Files from a Docker Container

```dockerfile
FROM caddy:latest
COPY . /usr/share/caddy
```

Run with:

```bash
docker build -t my-site .
docker run -d -p 80:80 -p 443:443 -e CADDY_INGRESS_NETWORKS=caddy my-site
```

### Use as a Reverse Proxy in Docker Compose

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

**Caddyfile**:

```caddyfile
mydomain.com {
    reverse_proxy app:8080
}
```

Caddy automatically discovers the `app` container via Docker networking.

### Graceful Reloads in Docker

```bash
# After changing the Caddyfile, reload without downtime
docker exec -w /etc/caddy <container_name> caddy reload
```

## Lifecycle Management

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

## Conclusion

Caddy simplifies web serving by automating HTTPS, providing a clean configuration model, and integrating seamlessly with modern stacks. Whether you’re deploying a static site, a microservices backend, or a full API gateway, Caddy gives you security, performance, and ease of use — all in a single binary. With strong Docker support and a vibrant plugin ecosystem, it’s an excellent choice for developers and operations teams alike.