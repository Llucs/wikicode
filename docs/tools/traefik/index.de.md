---
title: Traefik – Dynamischer Reverse Proxy und Load Balancer für Cloud-Native Umgebungen
description: Traefik ist ein cloud-nativer HTTP-Reverse-Proxy und Ingress-Controller, der automatisch Dienste erkennt und das Routing in Docker, Kubernetes und anderen Infrastruktur-Backends konfiguriert.
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

## Was ist Traefik?

[Traefik](https://traefik.io/traefik/) (ausgesprochen "Traffic") ist ein **Open-Source-HTTP-Reverse-Proxy und Load Balancer**, der für moderne, containerisierte und cloud-native Architekturen entwickelt wurde. Es ist in Go geschrieben und fungiert als einzelner Einstiegspunkt für Ihr Anwendungsnetzwerk, indem es HTTP-, HTTPS-, TCP-, UDP- und gRPC-Traffic dynamisch an die entsprechenden Backend-Dienste weiterleitet.

Das herausragendste Merkmal von Traefik ist die **automatische Serviceerkennung**: Anstatt eine manuell gepflegte Konfigurationsdatei (wie eine `nginx.conf`) zu benötigen, hört Traefik auf die Orchestrierungsebene (Docker, Kubernetes, Nomad, Consul, etc.) und **konfiguriert sich selbst**, sobald Dienste gestartet, gestoppt oder skaliert werden. Dies ermöglicht Topologieänderungen ohne Ausfallzeiten und ohne Proxy-Neuladevorgänge oder Neustarts.

Traefik ist ein **ausgereiftes Projekt der Cloud Native Computing Foundation (CNCF)** (seit 2022) und bildet den Kern der Traefik-Hub-Plattform, die es um API-Management-, API-Gateway- und AI-Gateway-Funktionen erweitert. Die aktuelle Hauptversion **Traefik v3** (veröffentlicht 2024) führte native HTTP/3-Unterstützung, Gateway-API-Integration für Kubernetes und ein erweitertes Plugin-System ein.

## Warum Traefik verwenden?

| Herausforderung | Traefiks Antwort |
|-----------|------------------|
| Manuelle Proxy-Konfiguration in dynamischen Umgebungen | **Auto-Discovery** – Dienste werden über Labels oder CRDs registriert; keine manuellen Konfigurationsaktualisierungen erforderlich. |
| Aufwand für SSL/TLS-Zertifikatsverwaltung | **Automatisches TLS** – integrierter ACME-Client (Let’s Encrypt, ZeroSSL) mit Unterstützung für HTTP- oder DNS-Challenges. |
| Notwendigkeit eines einheitlichen Einstiegspunkts über Docker und Kubernetes hinweg | **Multi-Provider-Unterstützung** – kann Dienste von Docker, Swarm, Kubernetes, Consul usw. gleichzeitig aggregieren. |
| Komplexe Routinglogik (Canary-Releases, A/B-Tests, Ratenbegrenzung) | **Middleware-Pipeline** – zusammensetzbare Kette von Ratenbegrenzern, Authentifizierung, Header-Manipulation und mehr. |
| Beobachtbarkeit und Fehlersuche | **Umfangreiche Metriken** (Prometheus, Datadog), **Tracing** (OpenTelemetry, Jaeger) und **strukturierte Zugriffsprotokolle**. |
| Entwicklererfahrung | **Live-Dashboard** – Web-UI zur Visualisierung von Routern, Diensten und Middlewares; plus Hot-Reload ohne Neustarts. |

## Installation

Traefik ist leichtgewichtig und wird als einzelne Binärdatei ausgeführt. Die gebräuchlichsten Methoden sind der Container-Einsatz und das Helm-Chart für Kubernetes.

### Docker (single-node)

```bash
docker run -d -p 80:80 -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name traefik \
  traefik:v3.0
```

Der obige Befehl mountet den Docker-Socket, damit Traefik Container erkennen kann. Port 80 ist der HTTP-Entrypoint, Port 8080 dient dem Dashboard.

### Kubernetes (Helm chart)

```bash
helm repo add traefik https://traefik.github.io/charts
helm upgrade --install traefik traefik/traefik \
  --namespace traefik --create-namespace
```

Das Chart deployt Traefik als Ingress-Controller mit sinnvollen Standardeinstellungen, inklusive Service-Load-Balancer, RBAC und optionalen Metriken.

### Binary (Linux)

```bash
# Download the latest release (check for actual version)
wget https://github.com/traefik/traefik/releases/download/v3.0.0/traefik_v3.0.0_linux_amd64.tar.gz
tar -xzf traefik_v3.0.0_linux_amd64.tar.gz
./traefik --configFile=traefik.yml
```

## Hauptfunktionen

### 1. Automatische Serviceerkennung

Traefik integriert sich mit einer Vielzahl von **Providern**:

- Docker / Docker Swarm
- Kubernetes (Ingress, IngressRoute CRD, Gateway API)
- Consul, Consul Connect
- etcd, ZooKeeper
- Nomad
- Rancher, Amazon ECS, Marathon, etc.

Routen werden dynamisch aus Labels (Docker) oder benutzerdefinierten Ressourcen (Kubernetes) generiert – keine statische Konfiguration erforderlich.

### 2. Dynamische Konfiguration mit Middleware-Pipeline

Traefik v2/v3 erzwingt eine klare Trennung zwischen **statischer Konfiguration** (Entrypoints, Provider, Logging) und **dynamischer Konfiguration** (Router, Middlewares, Dienste). Middlewares sind steckbare Kettenkomponenten, die Anfragen/Antworten modifizieren:

- **Authentifizierung**: BasicAuth, DigestAuth, ForwardAuth
- **Sicherheit**: IPAllow/Deny, RedirectScheme, RedirectRegex, Header-Anpassung
- **Verkehrssteuerung**: RateLimit, InFlightReq, CircuitBreaker, Retry
- **Protokollhandhabung**: AddPrefix, StripPrefix, ReplacePath
- **Transformation**: Buffering, ErrorPage, Compress

Beispiel einer Middleware-Definition (dynamisch):

```yaml
http:
  middlewares:
    rate-limit:
      rateLimit:
        average: 100
        burst: 200
```

### 3. Automatisches TLS mit ACME

Traefik enthält einen integrierten ACME-Client, der die Bereitstellung und Erneuerung von Zertifikaten automatisiert:

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

Nach der Konfiguration können Router den Resolver referenzieren:

```yaml
# Dynamic config (file or label)
http:
  routers:
    api:
      rule: Host(`api.example.com`)
      tls:
        certResolver: letsencrypt
```

Traefik wird automatisch Zertifikate abrufen und erneuern, ohne manuelles Eingreifen.

### 4. Natives HTTP/3 (QUIC)

Traefik v3 unterstützt HTTP/3 von Haus aus. Aktivieren Sie es an einem Entrypoint:

```yaml
entryPoints:
  websecure:
    address: ":443"
    http3: {}
```

Clients, die HTTP/3 unterstützen (z. B. moderne Browser), handeln automatisch das schnellere QUIC-Protokoll aus.

### 5. Beobachtbarkeit

| Funktion | Integration |
|---------|-------------|
| Metriken | Prometheus, Datadog, StatsD, InfluxDB, OpenTelemetry |
| Tracing | OpenTelemetry, Jaeger, Zipkin, Instana |
| Zugriffsprotokolle | Strukturiertes JSON oder Common Log Format |
| Gesundheitschecks | TCP, HTTP mit benutzerdefinierten Intervallen und Bedingungen |

### 6. Dashboard

Traefik bietet ein Web-Dashboard, das alle Router, Dienste, Middlewares und Entrypoints in Echtzeit anzeigt. Aktivieren Sie es in der statischen Konfiguration:

```yaml
api:
  dashboard: true
  debug: true
```

Dann rufen Sie `http://<traefik-ip>:8080/dashboard/` auf.

### 7. Traffic-Splitting und Canary-Deployments

Gewichteter Round-Robin zwischen Diensten:

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

### 8. Plugin-System

Traefik v3 unterstützt benutzerdefinierte Plugins, die in Go geschrieben sind (über einen Plugin-Katalog), um Middlewares, Provider oder sogar benutzerdefinierte Logik zu erweitern. Plugins werden über eine Plugin-Registrierung verteilt und können beim Start geladen werden.

## Anwendungsbeispiele

### Docker Quickstart (with whoami Service)

Erstellen Sie eine statische Konfigurationsdatei `traefik.yml`:

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

Traefik ausführen:

```bash
docker run -d -p 80:80 -p 8080:8080 \
  -v $(pwd)/traefik.yml:/etc/traefik/traefik.yml \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name traefik \
  traefik:v3.0
```

Starten Sie einen Backend-Dienst mit Labels:

```bash
docker run -d --name whoami \
  -l "traefik.enable=true" \
  -l "traefik.http.routers.whoami.rule=Host(\`whoami.localhost\`)" \
  -l "traefik.http.routers.whoami.entrypoints=web" \
  traefik/whoami
```

Testen Sie das Routing:

```bash
curl -H "Host: whoami.localhost" http://localhost
```

Sie erhalten die whoami-Antwort, was beweist, dass das dynamische Routing funktioniert hat. **Kein Proxy-Neuladen erforderlich.**

### Kubernetes IngressRoute (CRD)

Traefiks benutzerdefinierte Ressource `IngressRoute` bietet eine umfangreichere Konfiguration als das standardmäßige Kubernetes-Ingress.

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

Die `IngressRoute` wird automatisch vom Kubernetes-Provider von Traefik erkannt und sofort aktiv.

## Architektur: Statische vs. Dynamische Konfiguration

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

Diese Trennung stellt sicher, dass die gemeinsamen Infrastruktureinstellungen (Entrypoints, Provider) stabil bleiben, während sich das Routing nahtlos ändern kann, wenn Dienste skaliert werden.

## Wann Traefik verwenden (vs. Alternativen)

| Anwendungsfall | Warum Traefik glänzt |
|----------|-------------------|
| **Docker-Compose-Entwicklung** | Null Konfiguration – einfach Labels hinzufügen, keine `nginx.conf` nötig. |
| **Kubernetes mit komplexem Routing** | `IngressRoute`-CRDs ermöglichen Middleware-Verkettung, Traffic-Splitting und benutzerdefiniertes TLS ohne Verrenkungen. |
| **Homelab / Self-Hosting** | Automatisches TLS mit Wildcard-Zertifikaten über Let’s Encrypt; einfache Benutzeroberfläche. |
| **Service-Mesh-Edge-Proxy** | Fungiert als Ingress-Gateway für ein Service Mesh (z. B. Linkerd, Consul Connect). |
| **Multi-Cluster / Hybrid Cloud** | Kann Dienste von verschiedenen Providern (Docker + K8s + Consul) unter einem einzigen Edge aggregieren. |

## Fazit

Traefik hat sich von einem Nischen-Docker-Proxy zu einem ausgereiften, von der CNCF graduierten Ingress-Controller und Edge-Router entwickelt. Sein Markenzeichen ist die **automatische, Echtzeit-Serviceerkennung**, die manuelle Proxy-Konfiguration überflüssig macht – eine perfekte Lösung für dynamische, containerbasierte Bereitstellungen. Mit Unterstützung für HTTP/3, ein leistungsstarkes Middleware-System, automatisches TLS und umfassende Beobachtbarkeit ist Traefik die erste Wahl für Entwickler und Betreiber, die einen robusten, einfach zu bedienenden Reverse Proxy suchen, der sich an ihre Infrastruktur anpasst, und nicht umgekehrt.

---

### Ressourcen

- [Offizielle Dokumentation](https://doc.traefik.io/traefik/)
- [GitHub-Repository](https://github.com/traefik/traefik)
- [Traefik Hub (verwaltetes API-Management-Add-on)](https://traefik.io/traefik-hub/)
- [Playground / Demo](https://play.traefik.io/)