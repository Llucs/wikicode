---
title: HAProxy
description: HAProxy ist ein leistungsstarker, quelloffener TCP/HTTP-Lastverteiler und Reverse-Proxy, der extreme Zuverlässigkeit, Leistung und Kontrolle für moderne verteilte Systeme bietet.
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

HAProxy (High Availability Proxy) ist der De‑facto‑Standard-Lastverteiler und Proxy‑Server für TCP und HTTP im Open‑Source‑Bereich. Entwickelt in C von Willy Tarreau, ist es speziell für die Verteilung von Traffic auf Backend‑Server mit extremer Leistung, Zuverlässigkeit und einem minimalen Speicherverbrauch konzipiert. HAProxy betreibt viele der am stärksten frequentierten Websites und Dienste im Internet, darunter GitHub, Reddit, Twitter/X und Docker Hub.

## Was ist HAProxy?

HAProxy ist ein kostenloser, sehr schneller und zuverlässiger Reverse‑Proxy, der Hochverfügbarkeit, Lastverteilung und Proxy‑Funktionen für TCP‑ und HTTP‑basierte Anwendungen bietet. Es läuft auf Linux, macOS und FreeBSD. Der häufigste Einsatzzweck ist die Verbesserung der Leistung und Zuverlässigkeit einer Serverumgebung durch die Verteilung der Arbeitslast auf mehrere Server (z. B. Web, Anwendung, Datenbank). Über die grundlegende Lastverteilung hinaus bietet HAProxy erweitertes Traffic‑Management, SSL/TLS‑Terminierung, Content‑Switching, Health Checks, Sitzungspersistenz, tiefgehende Observability und Sicherheitsfunktionen wie Ratenbegrenzung und Protokollhärtung.

## Warum HAProxy?

In modernen Infrastrukturen müssen Dienste Millionen gleichzeitiger Verbindungen mit null Ausfallzeiten bewältigen. Allgemeine Webserver wie Nginx oder Apache können als Lastverteiler fungieren, aber HAProxy ist **speziell für diese Rolle konzipiert**. Es zeichnet sich aus durch:

- **Leistung:** Kann Millionen gleichzeitiger Verbindungen auf bescheidener Hardware bewältigen, dank einer ereignisgesteuerten, ein‑ oder mehrthreadigen Architektur.
- **Zuverlässigkeit:** Mit aggressiven Plausibilitätsprüfungen gebaut; unmögliche Bedingungen oder Endlosschleifen führen zu einem sofortigen Absturz mit einem Dump, wodurch eine stille Datenkorruption verhindert wird.
- **Funktionsumfang:** Native SSL‑Terminierung, HTTP/2, gRPC, QUIC/HTTP/3, erweiterte ACLs, Stick‑Tables, Prometheus‑Metriken und nahtloses Neuladen.
- **Sicherheit:** Schützt Backends vor Slow‑Loris‑Angriffen, DDoS und Protokollexploits.

## Installation

HAProxy ist in den meisten Paketquellen verfügbar, kann per Docker ausgeführt und für individuelle Anpassungen aus dem Quellcode kompiliert werden.

### Aus den offiziellen Paketquellen

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

### Mit Docker

```bash
docker run --name my-haproxy \
  -v /path/to/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro \
  -p 80:80 \
  -p 443:443 \
  haproxy:lts
```

### Kompilieren aus dem Quellcode (für benutzerdefinierte Funktionen)

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

## Grundlegende Konfiguration

Die HAProxy‑Konfiguration wird in eine einzelne Textdatei geschrieben, die sich normalerweise unter `/etc/haproxy/haproxy.cfg` befindet. Die Datei besteht aus logischen Abschnitten:

| Abschnitt    | Zweck                                                  |
|--------------|--------------------------------------------------------|
| `global`     | Prozessweite Einstellungen (Benutzer, Gruppe, maximale Verbindungen, Stats‑Socket). |
| `defaults`   | Gemeinsame Parameter für alle Frontends/Backends (Modus, Timeouts, Logging‑Optionen). |
| `frontend`   | Verkehrseintrittspunkte: Definition von IP/Port‑Bindungen, ACLs und Standard‑Backends. |
| `backend`    | Pools von Servern, an die der Verkehr weitergeleitet wird. Definiert Lastverteilungsalgorithmus, Health Checks und Persistenz. |
| `listen`     | Praktischer Wrapper, der Frontend und Backend für einfache Setups kombiniert. |

### Beispiel: Einfacher HTTP‑Lastverteiler

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

### Beispiel: TCP‑Lastverteiler (z. B. MySQL)

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

### Aktivieren der Statistikseite

```cfg
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 10s
    # optionally restrict access
    stats auth admin:password
```

## Hauptmerkmale mit Befehlsbeispielen

### 1. Lastverteilungsalgorithmen

HAProxy unterstützt Dutzende von Algorithmen. Einige der häufigsten:

| Algorithmus        | Beschreibung                                             |
|--------------------|----------------------------------------------------------|
| `roundrobin`       | Verteilt Anfragen sequenziell auf die Server.            |
| `leastconn`        | Sendet Anfragen an den Server mit den wenigsten Verbindungen. |
| `source`           | Hasht die Quell‑IP, sodass ein Client denselben Server erreicht (nützlich für Persistenz). |
| `uri`              | Hasht die Request‑URI, nützlich für Caching‑Konfigurationen. |
| `hdr(name)`        | Hasht den Wert eines Headers (z. B. `X-Session-ID`).     |

Beispielkonfiguration:

```cfg
backend webservers
    balance hdr(host)
    server web1 192.168.1.10:80 check
    server web2 192.168.1.11:80 check
```

### 2. Health Checks

Aktive Health Checks werden mit dem Schlüsselwort `check` in jeder Serverzeile konfiguriert. Sie können diese feinabstimmen:

```cfg
server web1 192.168.1.10:80 check inter 2s fall 3 rise 2
# inter    – Check-Intervall
# fall     – Anzahl Fehlschläge vor dem Markieren als down
# rise     – Anzahl Erfolge vor dem Markieren als up
```

Sie können auch Layer‑7‑Checks (`option httpchk`) für HTTP‑Backends durchführen:

```cfg
backend webservers
    option httpchk HEAD /health HTTP/1.1\r\nHost:\ localhost
    server web1 192.168.1.10:80 check
```

### 3. SSL/TLS‑Offloading

HTTPS am Loadbalancer terminieren und unverschlüsseltes HTTP an die Backends weiterleiten:

```cfg
frontend https-in
    bind *:443 ssl crt /etc/ssl/certs/example.pem
    default_backend webservers

backend webservers
    server web1 192.168.1.10:80 check
```

Sie können auch eine Neuverschlüsselung zu den Backends (SSL‑Bridging) durchführen oder Clientzertifikate prüfen.

### 4. Content Switching mit ACLs

Verwenden Sie ACLs, um Traffic basierend auf Headern, URL‑Pfaden, TLS‑SNI usw. zu routen.

```cfg
frontend http-in
    bind *:80

    # ACLs definieren
    acl is_api path_beg /api/
    acl is_static path_end .jpg .png .css .js

    # ACLs zur Auswahl des Backends verwenden
    use_backend api_servers if is_api
    use_backend static_servers if is_static
    default_backend webservers
```

### 5. Sitzungspersistenz (Stickiness)

Stellen Sie sicher, dass die Anfragen eines Benutzers immer an denselben Backend‑Server gehen:

```cfg
backend webservers
    balance roundrobin
    cookie SERVERID insert indirect nocache
    server web1 192.168.1.10:80 check cookie w1
    server web2 192.168.1.11:80 check cookie w2
```

Alternativ können Sie `stick‑table`‑Persistenz basierend auf IP oder einem Header verwenden.

### 6. Neuladen ohne Ausfallzeiten

Konfigurationsänderungen anwenden, ohne Verbindungen zu trennen:

```bash
haproxy -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid -sf $(cat /run/haproxy.pid)
```

Oder per systemd:

```bash
systemctl reload haproxy
```

## Erweiterte Funktionen

### Ratenbegrenzung

```cfg
frontend http-in
    bind *:80

    # 10 Anfragen pro Sekunde pro IP erlauben, Spitze 20
    stick-table type ip size 1m expire 10s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 20 }
    default_backend webservers
```

### HTTP/2 und gRPC

HAProxy unterstützt HTTP/2 und kann gRPC ohne besondere Konfiguration proxieren, außer dass `alpn` aktiviert wird:

```cfg
frontend https-in
    bind *:443 ssl crt /etc/ssl/certs/example.pem alpn h2,http/1.1
    default_backend grpc_servers

backend grpc_servers
    server grpc1 10.0.0.1:50051 check
```

### QUIC / HTTP/3

Neuere Versionen (≥2.5) enthalten experimentelle QUIC‑Unterstützung für UDP‑basiertes HTTP/3:

```cfg
frontend quic-in
    bind quic4@:443 ssl crt /etc/ssl/certs/example.pem
    default_backend webservers
```

### Observability

- **Statistikseite:** integrierter HTML/JSON‑Endpunkt (siehe vorheriges Beispiel).
- **Prometheus‑Metriken:** verwenden Sie die Option `stats prometheus`:

```cfg
frontend stats
    bind *:8405
    stats enable
    stats uri /metrics
    stats prometheus
```

- **Roh‑Logging:** HAProxy gibt detaillierte Logs aus (an syslog oder eine separate Logdatei), die mit Tools wie `tail`, `grep` analysiert oder an ELK/Loki gesendet werden können.

## Befehlszeilenverwaltung

HAProxy bietet eine umfangreiche Laufzeit‑API über einen Unix‑Socket oder TCP‑Socket. Das Dienstprogramm `socat` wird häufig verwendet, um Befehle zu senden:

```bash
echo "show info" | socat stdio unix-connect:/run/haproxy.sock
echo "show stat" | socat stdio unix-connect:/run/haproxy.sock
echo "enable server webservers/web1" | socat stdio unix-connect:/run/haproxy.sock
```

Die Laufzeit‑API unterstützt auch das dynamische Hinzufügen/Entfernen von Servern, was für Containerumgebungen entscheidend ist.

## Sicherheitsaspekte

- **Als Nicht‑Root ausführen:** HAProxy gibt Berechtigungen nach dem Binden von Ports ab. Die Direktiven `user` und `group` in `global` sind obligatorisch.
- **Chroot aktivieren:** Setzen Sie `chroot /var/lib/haproxy`, um den Prozess vom Dateisystem zu isolieren.
- **Stats einschränken:** Verwenden Sie Authentifizierung, ACLs oder binden Sie Stats an eine private Schnittstelle.
- **Timeouts anpassen:** Verhindert, dass langsame Clients Verbindungspools erschöpfen.
- **SYN‑Flood‑Schutz aktivieren:** Verwenden Sie die Optionen `tcp-smart-connect` und `tcp-smart-accept`.

## Fazit

HAProxy ist eine ausgereifte, kampferprobte Komponente, die das Rückgrat vieler stark frequentierter, kritischer Systeme bildet. Ihr laserartiger Fokus auf Lastverteilung und Proxying bietet unübertroffene Leistung, Stabilität und granulare Kontrolle. Ob Sie einen kleinen Blog oder eine weltumspannende SaaS betreiben, HAProxy ist ein unverzichtbares Werkzeug im Werkzeugkasten jedes Infrastruktur‑Ingenieurs.

Für weitere Informationen lesen Sie die [offizielle HAProxy‑Dokumentation](https://www.haproxy.org/documentation/) oder besuchen Sie die [HAProxy Technologies‑Website](https://www.haproxy.com/).