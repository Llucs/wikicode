---
title: HAProxy
description: HAProxy est un équilibreur de charge TCP/HTTP open-source et un proxy inverse haute performance qui offre une fiabilité, des performances et un contrôle extrêmes pour les systèmes distribués modernes.
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

HAProxy (High Availability Proxy) est le standard de facto open-source d'équilibreur de charge et de serveur proxy TCP et HTTP. Écrit en C par Willy Tarreau, il est spécialement conçu pour distribuer le trafic entre les serveurs backend avec des performances et une fiabilité extrêmes, ainsi qu'une empreinte mémoire minimale. HAProxy alimente de nombreux sites web et services parmi les plus fréquentés d'Internet, notamment GitHub, Reddit, Twitter/X et Docker Hub.

## Qu'est-ce que HAProxy ?

HAProxy est un proxy inverse gratuit, très rapide et fiable qui offre une haute disponibilité, un équilibrage de charge et un proxy pour les applications TCP et HTTP. Il fonctionne sous Linux, macOS et FreeBSD. Son utilisation la plus courante est d'améliorer les performances et la fiabilité d'un environnement serveur en répartissant la charge de travail entre plusieurs serveurs (par exemple, web, application, base de données). Au-delà de l'équilibrage de charge de base, HAProxy fournit une gestion avancée du trafic, la terminaison SSL/TLS, la commutation de contenu, les vérifications de santé, la persistance de session, une observabilité approfondie et des fonctionnalités de sécurité telles que la limitation de débit et le durcissement des protocoles.

## Pourquoi HAProxy ?

Dans une infrastructure moderne, les services doivent gérer des millions de connexions simultanées sans aucun temps d'arrêt. Les serveurs web polyvalents comme Nginx ou Apache peuvent agir comme équilibreurs de charge, mais HAProxy est **spécialement conçu** pour ce rôle. Il excelle dans :

- **Performance :** Peut gérer des millions de connexions simultanées sur du matériel modeste grâce à une architecture événementielle, mono-thread (ou multi-thread).
- **Fiabilité :** Construit avec des vérifications de santé agressives ; les conditions impossibles ou les boucles infinies entraînent un crash immédiat avec un dump, empêchant la corruption silencieuse des données.
- **Ensemble de fonctionnalités :** Terminaison SSL native, HTTP/2, gRPC, QUIC/HTTP/3, ACL avancées, stick‑tables, métriques Prometheus et rechargements sans couture.
- **Sécurité :** Protège les backends contre les attaques slow‑loris, les DDoS et les exploits au niveau du protocole.

## Installation

### Depuis les dépôts officiels

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

### Utilisation avec Docker

```bash
docker run --name my-haproxy \
  -v /path/to/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro \
  -p 80:80 \
  -p 443:443 \
  haproxy:lts
```

### Compilation depuis les sources (pour fonctionnalités personnalisées)

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

## Configuration de base

La configuration d'HAProxy est écrite dans un fichier texte unique, généralement situé à `/etc/haproxy/haproxy.cfg`. Le fichier est composé de sections logiques :

| Section     | Description                                                  |
|-------------|--------------------------------------------------------------|
| `global`    | Paramètres à l'échelle du processus (utilisateur, groupe, connexions max, socket de statistiques). |
| `defaults`  | Paramètres partagés pour tous les frontends/backends (mode, timeouts, options de journalisation). |
| `frontend`  | Points d'entrée du trafic : définir les liaisons IP/port, les ACL et les backends par défaut. |
| `backend`   | Pools de serveurs vers lesquels transférer le trafic. Définit l'algorithme d'équilibrage de charge, les vérifications de santé et la persistance. |
| `listen`    | Wrapper pratique qui combine frontend et backend pour les configurations simples. |

### Exemple : équilibreur de charge HTTP simple

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

### Exemple : équilibreur de charge TCP (par exemple, MySQL)

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

### Activation de la page de statistiques

```cfg
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 10s
    # optionally restrict access
    stats auth admin:password
```

## Fonctionnalités clés avec exemples de commandes

### 1. Algorithmes d'équilibrage de charge

HAProxy prend en charge des dizaines d'algorithmes d'équilibrage. Parmi les plus courants :

| Algorithme    | Description                                             |
|---------------|---------------------------------------------------------|
| `roundrobin`  | Distribue les requêtes séquentiellement entre les serveurs. |
| `leastconn`   | Envoie les requêtes au serveur avec le moins de connexions. |
| `source`      | Hache l'adresse IP source, garantissant qu'un client atteint le même serveur (utile pour la persistance). |
| `uri`         | Hache l'URI de la requête, utile pour les configurations de cache. |
| `hdr(name)`   | Hache la valeur d'un en-tête (par exemple, `X-Session-ID`). |

Exemple de configuration :

```cfg
backend webservers
    balance hdr(host)
    server web1 192.168.1.10:80 check
    server web2 192.168.1.11:80 check
```

### 2. Vérifications de santé

Les vérifications de santé actives sont configurées avec le mot-clé `check` sur chaque ligne de serveur. Vous pouvez les affiner :

```cfg
server web1 192.168.1.10:80 check inter 2s fall 3 rise 2
# inter    – check interval
# fall     – number of failures before marking server down
# rise     – number of successes before marking server up
```

Vous pouvez également effectuer des vérifications de niveau 7 (`option httpchk`) pour les backends HTTP :

```cfg
backend webservers
    option httpchk HEAD /health HTTP/1.1\r\nHost:\ localhost
    server web1 192.168.1.10:80 check
```

### 3. Déchargement SSL/TLS

Terminez le HTTPS au niveau de l'équilibreur de charge et transmettez du HTTP simple aux backends :

```cfg
frontend https-in
    bind *:443 ssl crt /etc/ssl/certs/example.pem
    default_backend webservers

backend webservers
    server web1 192.168.1.10:80 check
```

Vous pouvez également ré‑chiffrer vers les backends (pont SSL) ou vérifier les certificats clients.

### 4. Commutation de contenu avec ACL

Utilisez les ACL pour router le trafic en fonction des en-têtes, des chemins d'URL, du SNI TLS, etc.

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

### 5. Persistance de session (Stickiness)

Assurez-vous que les requêtes d'un utilisateur aillent toujours au même serveur backend :

```cfg
backend webservers
    balance roundrobin
    cookie SERVERID insert indirect nocache
    server web1 192.168.1.10:80 check cookie w1
    server web2 192.168.1.11:80 check cookie w2
```

Alternativement, utilisez la persistance `stick‑table` basée sur l'IP ou un en-tête.

### 6. Rechargement sans interruption

Appliquez les changements de configuration sans interrompre les connexions :

```bash
haproxy -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid -sf $(cat /run/haproxy.pid)
```

Ou via systemd :

```bash
systemctl reload haproxy
```

## Fonctionnalités avancées

### Limitation de débit

```cfg
frontend http-in
    bind *:80

    # Allow 10 requests per second per IP, burst to 20
    stick-table type ip size 1m expire 10s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 20 }
    default_backend webservers
```

### HTTP/2 et gRPC

HAProxy prend en charge HTTP/2 et peut proxifier gRPC sans aucune configuration spéciale au-delà de l'activation de `alpn` :

```cfg
frontend https-in
    bind *:443 ssl crt /etc/ssl/certs/example.pem alpn h2,http/1.1
    default_backend grpc_servers

backend grpc_servers
    server grpc1 10.0.0.1:50051 check
```

### QUIC / HTTP/3

Les versions récentes (≥2.5) incluent un support expérimental de QUIC pour HTTP/3 basé sur UDP :

```cfg
frontend quic-in
    bind quic4@:443 ssl crt /etc/ssl/certs/example.pem
    default_backend webservers
```

### Observabilité

- **Page de statistiques :** point de terminaison HTML/JSON intégré (voir exemple précédent).
- **Métriques Prometheus :** utilisez l'option `stats prometheus` :

```cfg
frontend stats
    bind *:8405
    stats enable
    stats uri /metrics
    stats prometheus
```

- **Journalisation brute :** HAProxy génère des journaux détaillés (vers syslog ou un fichier journal séparé) qui peuvent être analysés par des outils comme `tail`, `grep`, ou envoyés vers ELK/Loki.

## Gestion en ligne de commande

HAProxy fournit une API d'exécution riche via un socket Unix ou un socket TCP. L'utilitaire `socat` est couramment utilisé pour envoyer des commandes :

```bash
echo "show info" | socat stdio unix-connect:/run/haproxy.sock
echo "show stat" | socat stdio unix-connect:/run/haproxy.sock
echo "enable server webservers/web1" | socat stdio unix-connect:/run/haproxy.sock
```

L'API d'exécution prend également en charge l'ajout/la suppression dynamique de serveurs, ce qui est crucial pour les environnements conteneurisés.

## Considérations de sécurité

- **Exécution en tant que non‑root :** HAProxy abandonne les privilèges après avoir lié les ports. Les directives `user` et `group` dans `global` sont obligatoires.
- **Activer chroot :** Définissez `chroot /var/lib/haproxy` pour isoler le processus du système de fichiers.
- **Restreindre les statistiques :** Utilisez l'authentification, les ACL ou liez les statistiques sur une interface privée.
- **Régler les timeouts :** Empêche les clients lents d'épuiser les pools de connexions.
- **Activer la protection contre les inondations SYN :** Utilisez les options `tcp-smart-connect` et `tcp-smart-accept`.

## Conclusion

HAProxy est un composant mature et éprouvé qui constitue l'épine dorsale de nombreux systèmes critiques à fort trafic. Son accent mis sur l'équilibrage de charge et le proxying offre des performances, une stabilité et un contrôle granulaire inégalés. Que vous gériez un petit blog ou un SaaS mondial, HAProxy est un outil essentiel dans la boîte à outils de tout ingénieur infrastructure.

Pour en savoir plus, consultez la [documentation officielle d'HAProxy](https://www.haproxy.org/documentation/) ou le [site HAProxy Technologies](https://www.haproxy.com/).