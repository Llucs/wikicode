---
title: Traefik – Dynamic Reverse Proxy and Load Balancer for Cloud-Native Environments
description: Traefik is a cloud-native HTTP reverse proxy and ingress controller that automatically discovers services and configures routing in Docker, Kubernetes, and other infrastructure backends.
created: 2026-06-16
tags:
  - reverse-proxy
  - load-balancer
  - traefik
  - docker
  - kubernetes
  - cloud-native
status: draft
---

# Traefik – Edge Router, Reverse Proxy & Load Balancer

## What is Traefik?

[Traefik](https://traefik.io/traefik/) (pronounced "traffic") is an **open-source HTTP reverse proxy and load balancer** engineered for modern, containerized, and cloud-native architectures. Written in Go, it acts as the single entry point for your application network, dynamically routing HTTP, HTTPS, TCP, UDP, and gRPC traffic to the appropriate backend services.

Traefik’s most distinctive characteristic is **automatic service discovery**: instead of requiring a manually maintained configuration file (like an `nginx.conf`), Traefik listens to the orchestration layer (Docker, Kubernetes, Nomad, Consul, etc.) and **self-configures** its routing rules as services are started, stopped, or scaled. This allows zero-downtime topology changes without proxy reloads or restarts.

Traefik is a **Cloud Native Computing Foundation (CNCF) graduated project** (since 2022) and is the core of the Traefik Hub platform, which extends it with API management, API gateway, and AI gateway capabilities. The current major version, **Traefik v3** (released 2024), introduced native HTTP/3 support, Gateway API integration for Kubernetes, and an enhanced plugin system.

## Why Use Traefik?

| Challenge | Traefik’s Answer |
|-----------|------------------|
| Manual proxy configuration in dynamic environments | **Auto-discovery** – services are registered via labels or CRDs; no manual config updates. |
| SSL/TLS certificate management overhead | **Automatic TLS** – built-in ACME client (Let’s Encrypt, ZeroSSL) with HTTP or DNS challenge support. |
| Need for a unified entry point across Docker and Kubernetes | **Multi-provider support** – can aggregate services from Docker, Swarm, Kubernetes, Consul, etc. simultaneously. |
| Complex routing logic (canaries, A/B tests, rate limiting) | **Middleware pipeline** – composable chain of rate limiters, authentication, headers manipulation, and more. |
| Observability and debugging | **Rich metrics** (Prometheus, Datadog), **tracing** (OpenTelemetry, Jaeger), and **structured access logs**. |
| Developer experience | **Live Dashboard** – web UI to visualize routers, services, middlewares; plus hot-reloading without restarts. |

## Installation

Traefik is lightweight and runs as a single binary. The most common methods are container deployment and Helm chart for Kubernetes.

### Docker (single-node)

```bash
docker run -d -p 80:80 -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name traefik \
  traefik:v3.0
```

The above command mounts the Docker socket so Traefik can discover containers. Port 80 is the HTTP entry point, port 8080 serves the dashboard.

### Kubernetes (Helm chart)

```bash
helm repo add traefik https://traefik.github.io/charts
helm upgrade --install traefik traefik/traefik \
  --namespace traefik --create-namespace
```

The chart deploys Traefik as an Ingress Controller with sensible defaults, including service load balancer, RBAC, and optional metrics.

### Binary (Linux)

```bash
# Download the latest release (check for actual version)
wget https://github.com/traefik/traefik/releases/download/v3.0.0/traefik_v3.0.0_linux_amd64.tar.gz
tar -xzf traefik_v3.0.0_linux_amd64.tar.gz
./traefik --configFile=traefik.yml
```

## Key Features

### 1. Automatic Service Discovery

Traefik integrates with a wide range of **providers**:

- Docker / Docker Swarm
- Kubernetes (Ingress, IngressRoute CRD, Gateway API)
- Consul, Consul Connect
- etcd, ZooKeeper
- Nomad
- Rancher, Amazon ECS, Marathon, etc.

Routes are dynamically generated from labels (Docker) or custom resources (Kubernetes) – no static configuration required.

### 2. Dynamic Configuration with Middleware Pipeline

Traefik v2/v3 enforces a clear separation between **static configuration** (entry points, providers, logging) and **dynamic configuration** (routers, middlewares, services). Middlewares are pluggable chain components that modify requests/responses:

- **Authentication**: BasicAuth, DigestAuth, ForwardAuth
- **Security**: IPAllow/Deny, RedirectScheme, RedirectRegex, Headers customisation
- **Traffic management**: RateLimit, InFlightReq, CircuitBreaker, Retry
- **Protocol handling**: AddPrefix, StripPrefix, ReplacePath
- **Transformation**: Buffering, ErrorPage, Compress

Example middleware definition (dynamic):

```yaml
http:
  middlewares:
    rate-limit:
      rateLimit:
        average: 100
        burst: 200
```

### 3. Automatic TLS with ACME

Traefik includes a built-in ACME client that automates certificate provisioning and renewal:

```yaml
# Static config (traefik.yml)
certificatesResolvers:
  letsencrypt:
    acme:
      email: admin@example.com
      storage: /acme.json
      httpChallenge:
        entryPoint: web
```

Once configured, routers can reference the resolver:

```yaml
# Dynamic config (file or label)
http:
  routers:
    api:
      rule: Host(`api.example.com`)
      tls:
        certResolver: letsencrypt
```

Traefik will automatically obtain and renew certificates without any manual intervention.

### 4. Native HTTP/3 (QUIC)

Traefik v3 supports HTTP/3 out of the box. Enable it on an entry point:

```yaml
entryPoints:
  websecure:
    address: ":443"
    http3: {}
```

Clients that support HTTP/3 (e.g., modern browsers) will automatically negotiate the faster QUIC protocol.

### 5. Observability

| Feature | Integration |
|---------|-------------|
| Metrics | Prometheus, Datadog, StatsD, InfluxDB, OpenTelemetry |
| Tracing | OpenTelemetry, Jaeger, Zipkin, Instana |
| Access logs | Structured JSON or Common Log Format |
| Health checks | TCP, HTTP with custom intervals and conditions |

### 6. Dashboard

Traefik provides a web dashboard displaying all routers, services, middlewares, and entry points in real time. Enable it in static config:

```yaml
api:
  dashboard: true
  debug: true
```

Then access `http://<traefik-ip>:8080/dashboard/`.

### 7. Traffic Splitting & Canary Deployments

Weighted round-robin between services:

```yaml
http:
  services:
    api-canary:
      weighted:
        services:
          - name: api-v1
            weight: 90
          - name: api-v2
            weight: 10
```

### 8. Plugin System

Traefik v3 supports custom plugins written in Go (via a plugin catalog) for extending middlewares, providers, or even custom logic. Plugins are distributed through a plugin registry and can be loaded at startup.

## Usage Examples

### Docker Quickstart (with whoami Service)

Create a static config file `traefik.yml`:

```yaml
api:
  dashboard: true

entryPoints:
  web:
    address: ":80"

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
```

Run Traefik:

```bash
docker run -d -p 80:80 -p 8080:8080 \
  -v $(pwd)/traefik.yml:/etc/traefik/traefik.yml \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name traefik \
  traefik:v3.0
```

Launch a backend service with labels:

```bash
docker run -d --name whoami \
  -l "traefik.enable=true" \
  -l "traefik.http.routers.whoami.rule=Host(\`whoami.localhost\`)" \
  -l "traefik.http.routers.whoami.entrypoints=web" \
  traefik/whoami
```

Test the routing:

```bash
curl -H "Host: whoami.localhost" http://localhost
```

You will receive the whoami response, proving the dynamic routing worked. **No proxy reload required.**

### Kubernetes IngressRoute (CRD)

Traefik's custom resource `IngressRoute` offers richer configuration than standard Kubernetes Ingress.

```yaml
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: webapp
spec:
  entryPoints:
    - web
  routes:
    - kind: Rule
      match: Host(`webapp.example.com`)
      services:
        - name: webapp-svc
          port: 80
      middlewares:
        - name: auth
---
apiVersion: traefik.containo.us/v1alpha1
kind: Middleware
metadata:
  name: auth
spec:
  basicAuth:
    secret: webauth
```

The `IngressRoute` is automatically picked up by Traefik’s Kubernetes provider and becomes active immediately.

## Architecture: Static vs Dynamic Configuration

```
+-------------------+       +-----------------------+
|   Static Config   |       |   Dynamic Config      |
|  (traefik.yml)    |       |  (labels, CRDs, KV)   |
|                   |       |                       |
| - entryPoints     |       | - routers             |
| - providers       |       | - middlewares         |
| - logging         |       | - services            |
| - metrics         |       | - TLS options         |
| - plugins         |       | - etc.                |
+-------------------+       +-----------------------+
          |                           |
          |  Loaded at startup        |  Continuously watched
          |  (must restart to change) |  (hot-reloaded)
          v                           v
    +---------------------------------------+
    |        Traefik Proxy Engine            |
    |  (watches dynamic provider events)     |
    +---------------------------------------+
```

This separation ensures that common infrastructure settings (entry points, providers) are stable, while routing can change fluidly as services scale.

## When to Use Traefik (vs Alternatives)

| Use Case | Why Traefik Shines |
|----------|-------------------|
| **Docker Compose development** | Zero config – just add labels, no need for an `nginx.conf`. |
| **Kubernetes with complex routing** | `IngressRoute` CRDs allow middleware chaining, traffic splitting, and custom TLS without contortions. |
| **Homelab / self-hosting** | Automatic TLS with wildcard certificates via Let’s Encrypt; simple UI. |
| **Service mesh edge proxy** | Acts as the ingress gateway for a service mesh (e.g., Linkerd, Consul Connect). |
| **Multi-cluster / hybrid cloud** | Can aggregate services from different providers (Docker + K8s + Consul) under a single edge. |

## Conclusion

Traefik has evolved from a niche Docker proxy into a mature, CNCF-graduated ingress controller and edge router. Its hallmark is **automatic, real-time service discovery** that eliminates manual proxy configuration – a perfect fit for dynamic, container-based deployments. With support for HTTP/3, a powerful middleware system, automatic TLS, and deep observability, Traefik is a top choice for developers and operators who want a robust, easy-to-use reverse proxy that adapts to their infrastructure rather than the other way around.

---

### Resources

- [Official documentation](https://doc.traefik.io/traefik/)
- [GitHub repository](https://github.com/traefik/traefik)
- [Traefik Hub (managed API management add-on)](https://traefik.io/traefik-hub/)
- [Playground / Demo](https://play.traefik.io/)