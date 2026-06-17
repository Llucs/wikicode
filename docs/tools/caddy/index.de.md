---
title: Caddy: Der ultimative Webserver mit automatischem HTTPS
description: Ein unternehmensreifer Open-Source-Webserver mit automatischem HTTPS, Reverse Proxy und Docker-Unterstützung, geschrieben in Go.
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

Caddy ist ein leistungsstarker, unternehmensreifer Open-Source-Webserver und Reverse Proxy, geschrieben in Go. Er ist darauf ausgelegt, einfach zu bedienen zu sein, und bietet gleichzeitig robuste Sicherheit, automatische TLS-Zertifikatsverwaltung und eine moderne Konfigurations-API. Caddy wird von der Caddy Foundation betrieben und ist sowohl in Entwicklungs- als auch in Produktionsumgebungen weit verbreitet.

## Hauptmerkmale

- **Automatisches HTTPS**: Caddy erhält und erneuert automatisch TLS-Zertifikate von Let’s Encrypt oder ZeroSSL für jede konfigurierte Domäne. OCSP-Stapling, HTTP/2 und HTTP/3 (QUIC) werden von Haus aus verwaltet.
- **Einfache Konfiguration**: Verwenden Sie entweder eine benutzerfreundliche `Caddyfile` oder eine leistungsstarke JSON-API für dynamische Konfiguration. Die `Caddyfile` ist ein Adapter, der in JSON übersetzt wird und Ihnen Einfachheit und Flexibilität bietet.
- **Reverse Proxy & Lastausgleich**: Vollständiger Layer-7-Reverse-Proxy mit aktiven/passiven Health Checks, Wiederholungsversuchen, Circuit Breaker und mehreren Lastausgleichsrichtlinien (Zufall, wenigste Verbindungen, IP-Hash, Header-Affinität).
- **Sicherheit von Haus aus**: Geschrieben in der speichersicheren Sprache Go, wodurch Pufferüberlauf-Schwachstellen vermieden werden. TLS-Standards sind streng sicher, und Caddy hört nur bei Bedarf auf privilegierten Ports.
- **Modulare Architektur**: Der Kern ist minimal; Funktionen werden über Module erweitert. Erstellen Sie mit `xcaddy` benutzerdefinierte Binaries, die nur die benötigten Funktionen enthalten.
- **Container-nativ**: Einzelnes Binary, saubere Shutdowns, Graceful Reloads – ideal für Docker und Kubernetes.

## Warum Caddy verwenden?

Caddy beseitigt den Aufwand manueller HTTPS-Einrichtung. Es stellt automatisch Zertifikate bereit und erneuert sie, sodass Sie sich nie um ablaufende TLS kümmern müssen. Die Konfiguration ist intuitiv und eignet sich perfekt als Frontend für Microservices, statische Seiten, APIs und SPAs. Die JSON-API ermöglicht eine nahtlose Integration in Automatisierungstools, während die `Caddyfile` eine benutzerfreundliche Alternative bietet. Einmal schreiben, überall sicher ausliefern.

## Installation

Caddy bietet mehrere Installationsmethoden:

### Ein vorgefertigtes Binary herunterladen

```bash
# Linux / macOS / Windows Binary
curl -fsSL https://caddyserver.com/download/linux/amd64 -o caddy
chmod +x caddy
sudo mv caddy /usr/local/bin/
```

*Oder herunterladen von [caddyserver.com/download](https://caddyserver.com/download)*

### Paketmanager

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

### Benutzerdefiniertes Build mit `xcaddy`

```bash
# Caddy mit einem bestimmten Plugin erstellen
xcaddy build --with github.com/caddyserver/transform-encoder

# Mit einer benutzerdefinierten Version erstellen
xcaddy build v2.8.0 --with github.com/caddyserver/format-encoder
```

`xcaddy` kompiliert ein einzelnes Binary mit nur den gewünschten Modulen.

## Grundlegende Nutzung

### Statischer Dateiserver

```bash
# Aktuelles Verzeichnis auf Port 80 mit automatischem HTTPS ausliefern
caddy file-server
```

### Schneller Reverse Proxy

```bash
# Verkehr von yourdomain.com an ein lokales Backend weiterleiten
caddy reverse-proxy --from yourdomain.com --to localhost:8080
```

### Caddyfile-Konfiguration

Erstellen Sie eine `Caddyfile` im Stammverzeichnis Ihres Projekts:

```caddyfile
example.com {
    root * /var/www/example
    file_server
}
```

Dann ausführen:

```bash
caddy run
```

Caddy wird automatisch ein TLS-Zertifikat für `example.com` besorgen und die statischen Dateien ausliefern.

### JSON-Konfiguration

Caddys natives Konfigurationsformat ist JSON. Sie können es über die Admin-API anwenden:

```bash
caddy run

# In einem anderen Terminal die Konfiguration per POST senden
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

Die JSON-API ist die maßgebliche Quelle; die `Caddyfile` ist lediglich ein Adapter.

## Detaillierte Hauptmerkmale

### Automatisches HTTPS

```caddyfile
mydomain.com {
    tls you@email.com   # Optionale E-Mail für Let's Encrypt-Benachrichtigungen
}
```

Caddy kümmert sich automatisch um Zertifikatsausstellung, -erneuerung und HTTP-zu-HTTPS-Weiterleitungen. Es unterstützt Wildcard-Zertifikate, benutzerdefinierte ACME-Endpunkte (z. B. ZeroSSL) und On-Demand-TLS.

### Reverse Proxy mit Lastausgleich

```caddyfile
api.example.com {
    reverse_proxy api1:8080 api2:8080 api3:8080 {
        lb_policy least_conn
        health_uri /health
        health_interval 10s
    }
}
```

Richtlinien: `random`, `least_conn`, `ip_hash`, `uri_hash`, `header`, `first`, `round_robin`.

### Vorlagen & dynamische Seiten

Caddy kann Vorlagen für dynamische Inhalte ohne separates Backend ausführen:

```caddyfile
example.com {
    templates
    root * /var/www/example
}
```

### Authentifizierung

Modulare Authentifizierung (z. B. JWT, Basic Auth) kann über Plugins hinzugefügt werden:

```caddyfile
example.com {
    basic_auth {
        admin $2a$14$hash...
    }
}
```

### HTTP/3 (QUIC)

Aktivieren Sie HTTP/3 in Ihrer `Caddyfile`:

```caddyfile
{
    servers {
        protocol {
            quic
        }
    }
}
```

## Docker-Integration

Caddy ist in containerisierten Umgebungen erstklassig integriert.

### Statische Dateien aus einem Docker-Container ausliefern

```dockerfile
FROM caddy:latest
COPY . /usr/share/caddy
```

Ausführen mit:

```bash
docker build -t my-site .
docker run -d -p 80:80 -p 443:443 -e CADDY_INGRESS_NETWORKS=caddy my-site
```

### Als Reverse Proxy in Docker Compose verwenden

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

Caddy erkennt den Container `app` automatisch über das Docker-Netzwerk.

### Graceful Reloads in Docker

```bash
# Nach Änderungen an der Caddyfile ohne Ausfallzeit neu laden
docker exec -w /etc/caddy <container_name> caddy reload
```

## Lebenszyklusverwaltung

```bash
# Im Vordergrund ausführen
caddy run

# Als Hintergrunddienst ausführen
caddy start

# Dienst beenden
caddy stop

# Konfiguration gracefull neu laden (Linux)
caddy reload

# Eine Caddyfile validieren
caddy validate
```

## Fazit

Caddy vereinfacht das Web-Serving durch Automatisierung von HTTPS, ein sauberes Konfigurationsmodell und nahtlose Integration in moderne Stacks. Ob Sie eine statische Website, ein Microservices-Backend oder ein vollständiges API-Gateway bereitstellen – Caddy bietet Sicherheit, Leistung und Benutzerfreundlichkeit in einem einzigen Binary. Mit starker Docker-Unterstützung und einem lebendigen Plugin-Ökosystem ist es eine ausgezeichnete Wahl für Entwickler und Betriebsteams gleichermaßen.