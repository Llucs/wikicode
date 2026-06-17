---
title: Caddy : Le serveur web ultime avec HTTPS automatique
description: Un serveur web open-source prêt pour l'entreprise avec HTTPS automatique, reverse proxy et support Docker, écrit en Go.
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

Caddy est un serveur web puissant, prêt pour l'entreprise, open-source et un proxy inverse écrit en Go. Il est conçu pour être simple d'utilisation tout en offrant une sécurité robuste, une gestion automatique des certificats TLS et une API de configuration moderne. Caddy est maintenu par la Caddy Foundation et largement adopté dans les environnements de développement et de production.

## Fonctionnalités clés

- **Automatic HTTPS** : Caddy obtient et renouvelle automatiquement les certificats TLS de Let's Encrypt ou ZeroSSL pour chaque domaine configuré. Il gère l'OCSP stapling, HTTP/2 et HTTP/3 (QUIC) par défaut.
- **Simple Configuration** : Utilisez soit un `Caddyfile` convivial, soit une API JSON puissante pour une configuration dynamique. Le `Caddyfile` est un adaptateur qui traduit en JSON, vous offrant simplicité et flexibilité.
- **Reverse Proxy & Load Balancing** : Proxy inverse complet de couche 7 avec health checks actifs/passifs, retries, circuit breakers et plusieurs politiques de load balancing (random, least connections, IP hash, header affinity).
- **Security by Default** : Écrit en memory-safe Go, éliminant les vulnérabilités de buffer overflow. Les valeurs par défaut de TLS sont strictement sécurisées et Caddy n'écoute sur les ports privilégiés que lorsque nécessaire.
- **Modular Architecture** : Le noyau est minimal ; les fonctionnalités sont étendues via des modules. Construisez des binaires personnalisés avec `xcaddy` pour n'inclure que les fonctionnalités dont vous avez besoin.
- **Container Native** : Binaire unique, clean shutdowns, graceful reloads – idéal pour Docker et Kubernetes.

## Pourquoi utiliser Caddy ?

Caddy élimine la douleur de la configuration manuelle du HTTPS. Il provisionne et renouvelle automatiquement les certificats, vous n'avez donc jamais à vous soucier de l'expiration des certificats TLS. Sa configuration est intuitive et il sert de parfait intermédiaire pour les microservices, sites statiques, API et SPA. L'API JSON permet une intégration transparente avec les outils d'automatisation, tandis que le `Caddyfile` offre une alternative conviviale. Écrivez une fois, servez de manière sécurisée partout.

## Installation

Caddy propose plusieurs méthodes d'installation :

### Téléchargement d'un binaire pré-compilé

```bash
# Linux / macOS / Windows binary
curl -fsSL https://caddyserver.com/download/linux/amd64 -o caddy
chmod +x caddy
sudo mv caddy /usr/local/bin/
```

*Ou téléchargez depuis [caddyserver.com/download](https://caddyserver.com/download)*

### Gestionnaires de paquets

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

### Construction personnalisée avec `xcaddy`

```bash
# Build Caddy with a specific plugin
xcaddy build --with github.com/caddyserver/transform-encoder

# Build with a custom version
xcaddy build v2.8.0 --with github.com/caddyserver/format-encoder
```

`xcaddy` compile un seul binaire avec uniquement les modules que vous souhaitez.

## Utilisation de base

### Serveur de fichiers statiques

```bash
# Serve the current directory on port 80 with automatic HTTPS
caddy file-server
```

### Proxy inverse rapide

```bash
# Proxy traffic from yourdomain.com to a local backend
caddy reverse-proxy --from yourdomain.com --to localhost:8080
```

### Configuration Caddyfile

Créez un `Caddyfile` à la racine de votre projet :

```caddyfile
example.com {
    root * /var/www/example
    file_server
}
```

Ensuite, exécutez :

```bash
caddy run
```

Caddy obtiendra automatiquement un certificat TLS pour `example.com` et servira les fichiers statiques.

### Configuration JSON

Le format de configuration natif de Caddy est JSON. Vous pouvez l'appliquer via l'API d'administration :

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

L'API JSON est la source de vérité ; le `Caddyfile` n'est qu'un adaptateur.

## Fonctionnalités clés en détail

### Automatic HTTPS

```caddyfile
mydomain.com {
    tls you@email.com   # Optional email for Let's Encrypt notices
}
```

Caddy gère la délivrance, le renouvellement des certificats et les redirections HTTP vers HTTPS automatiquement. Il prend en charge les certificats wildcard, les points de terminaison ACME personnalisés (par exemple ZeroSSL) et le TLS à la demande.

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

Politiques : `random`, `least_conn`, `ip_hash`, `uri_hash`, `header`, `first`, `round_robin`.

### Templating et sites dynamiques

Caddy peut exécuter des templates pour du contenu dynamique sans backend séparé :

```caddyfile
example.com {
    templates
    root * /var/www/example
}
```

### Authentification

L'authentification modulaire (par exemple JWT, basic auth) peut être ajoutée via des plugins :

```caddyfile
example.com {
    basic_auth {
        admin $2a$14$hash...
    }
}
```

### HTTP/3 (QUIC)

Activez HTTP/3 dans votre `Caddyfile` :

```caddyfile
{
    servers {
        protocol {
            quic
        }
    }
}
```

## Intégration Docker

Caddy est un citoyen de première classe dans les environnements conteneurisés.

### Servir des fichiers statiques depuis un conteneur Docker

```dockerfile
FROM caddy:latest
COPY . /usr/share/caddy
```

Exécuter avec :

```bash
docker build -t my-site .
docker run -d -p 80:80 -p 443:443 -e CADDY_INGRESS_NETWORKS=caddy my-site
```

### Utiliser comme proxy inverse dans Docker Compose

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

**Caddyfile** :

```caddyfile
mydomain.com {
    reverse_proxy app:8080
}
```

Caddy découvre automatiquement le conteneur `app` via le réseau Docker.

### Rechargements en douceur dans Docker

```bash
# After changing the Caddyfile, reload without downtime
docker exec -w /etc/caddy <container_name> caddy reload
```

## Gestion du cycle de vie

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

Caddy simplifie le service web en automatisant le HTTPS, en offrant un modèle de configuration propre et en s'intégrant parfaitement aux piles modernes. Que vous déployiez un site statique, un backend de microservices ou une passerelle API complète, Caddy vous offre sécurité, performances et facilité d'utilisation — tout en un seul binaire. Avec un support Docker solide et un écosystème de plugins dynamique, c'est un excellent choix pour les développeurs et les équipes d'exploitation.