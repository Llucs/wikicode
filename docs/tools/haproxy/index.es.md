---
title: HAProxy
description: HAProxy es un balanceador de carga TCP/HTTP y proxy inverso de alto rendimiento y código abierto que ofrece fiabilidad, rendimiento y control extremos para sistemas distribuidos modernos.
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

HAProxy (High Availability Proxy) es el balanceador de carga y servidor proxy TCP y HTTP de código abierto estándar de facto. Escrito en C por Willy Tarreau, está diseñado específicamente para distribuir tráfico entre servidores backend con rendimiento, fiabilidad extremos y una huella de memoria mínima. HAProxy impulsa muchos de los sitios web y servicios más concurridos de Internet, incluyendo GitHub, Reddit, Twitter/X y Docker Hub.

## ¿Qué es HAProxy?

HAProxy es un proxy inverso gratuito, muy rápido y confiable que ofrece alta disponibilidad, balanceo de carga y proxy para aplicaciones TCP y HTTP. Se ejecuta en Linux, macOS y FreeBSD. Su uso más común es mejorar el rendimiento y la fiabilidad de un entorno de servidor distribuyendo la carga de trabajo entre múltiples servidores (por ejemplo, web, aplicación, base de datos). Más allá del balanceo de carga básico, HAProxy proporciona gestión avanzada de tráfico, terminación SSL/TLS, conmutación de contenido, comprobaciones de salud, persistencia de sesiones, observabilidad profunda y funciones de seguridad como limitación de velocidad y endurecimiento de protocolos.

## ¿Por qué HAProxy?

En la infraestructura moderna, los servicios deben manejar millones de conexiones concurrentes con cero tiempo de inactividad. Los servidores web de propósito general como Nginx o Apache pueden actuar como balanceadores de carga, pero HAProxy está **diseñado específicamente** para este rol. Se destaca en:

- **Rendimiento:** Puede manejar millones de conexiones concurrentes en hardware modesto gracias a una arquitectura basada en eventos, de un solo hilo (o multi-hilo).
- **Fiabilidad:** Construido con comprobaciones de integridad agresivas; condiciones imposibles o bucles infinitos resultan en un bloqueo inmediato con un volcado, evitando la corrupción silenciosa de datos.
- **Conjunto de características:** Terminación SSL nativa, HTTP/2, gRPC, QUIC/HTTP/3, ACLs avanzadas, tablas de persistencia, métricas de Prometheus y recargas sin interrupciones.
- **Seguridad:** Protege los servidores backend de ataques slow-loris, DDoS y exploits a nivel de protocolo.

## Instalación

HAProxy está disponible en la mayoría de los repositorios de paquetes, se puede ejecutar a través de Docker y se puede compilar desde el código fuente para compilaciones personalizadas.

### Desde Repositorios Oficiales

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

### Usando Docker

```bash
docker run --name my-haproxy \
  -v /path/to/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro \
  -p 80:80 \
  -p 443:443 \
  haproxy:lts
```

### Compilando desde el Código Fuente (para características personalizadas)

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

## Configuración Básica

La configuración de HAProxy se escribe en un solo archivo de texto, típicamente ubicado en `/etc/haproxy/haproxy.cfg`. El archivo se compone de secciones lógicas:

| Section     | Purpose                                                  |
|-------------|----------------------------------------------------------|
| `global`    | Configuraciones a nivel de proceso (usuario, grupo, conexiones máximas, socket de estadísticas). |
| `defaults`  | Parámetros compartidos para todos los frontends/backends (modo, tiempos de espera, opciones de registro). |
| `frontend`  | Puntos de entrada de tráfico: definen enlaces de IP/puerto, ACLs y backends predeterminados. |
| `backend`   | Grupos de servidores a los que se reenvía el tráfico. Define algoritmo de balanceo de carga, comprobaciones de salud y persistencia. |
| `listen`    | Envoltorio de conveniencia que combina frontend y backend para configuraciones simples. |

### Ejemplo: Balanceador de Carga HTTP Simple

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

### Ejemplo: Balanceador de Carga TCP (p. ej., MySQL)

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

### Habilitando la Página de Estadísticas

```cfg
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 10s
    # optionally restrict access
    stats auth admin:password
```

## Características Clave con Ejemplos de Comandos

### 1. Algoritmos de Balanceo de Carga

HAProxy soporta docenas de algoritmos de balanceo. Algunos de los más comunes:

| Algoritmo          | Descripción                                             |
|--------------------|---------------------------------------------------------|
| `roundrobin`       | Distribuye las solicitudes secuencialmente entre los servidores. |
| `leastconn`        | Envía solicitudes al servidor con menos conexiones.   |
| `source`           | Aplica un hash a la IP de origen, asegurando que un cliente llegue al mismo servidor (útil para persistencia). |
| `uri`              | Aplica un hash a la URI de la solicitud, útil para configuraciones de caché. |
| `hdr(name)`        | Aplica un hash al valor de un encabezado (p. ej., `X-Session-ID`). |

Ejemplo de configuración:

```cfg
backend webservers
    balance hdr(host)
    server web1 192.168.1.10:80 check
    server web2 192.168.1.11:80 check
```

### 2. Comprobaciones de Salud

Las comprobaciones de salud activas se configuran con la palabra clave `check` en cada línea de servidor. Puede ajustarlas:

```cfg
server web1 192.168.1.10:80 check inter 2s fall 3 rise 2
# inter    – check interval
# fall     – number of failures before marking server down
# rise     – number of successes before marking server up
```

También puede realizar comprobaciones de capa 7 (`option httpchk`) para backends HTTP:

```cfg
backend webservers
    option httpchk HEAD /health HTTP/1.1\r\nHost:\ localhost
    server web1 192.168.1.10:80 check
```

### 3. Descarga SSL/TLS

Termine HTTPS en el balanceador de carga y reenvíe HTTP simple a los backends:

```cfg
frontend https-in
    bind *:443 ssl crt /etc/ssl/certs/example.pem
    default_backend webservers

backend webservers
    server web1 192.168.1.10:80 check
```

También puede volver a cifrar hacia los backends (puente SSL) o verificar certificados de cliente.

### 4. Conmutación de Contenido con ACLs

Utilice ACLs para enrutar el tráfico basado en encabezados, rutas URL, TLS SNI, etc.

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

### 5. Persistencia de Sesión (Stickiness)

Asegúrese de que las solicitudes de un usuario siempre vayan al mismo servidor backend:

```cfg
backend webservers
    balance roundrobin
    cookie SERVERID insert indirect nocache
    server web1 192.168.1.10:80 check cookie w1
    server web2 192.168.1.11:80 check cookie w2
```

Alternativamente, use persistencia `stick‑table` basada en IP o un encabezado.

### 6. Recargas sin Tiempo de Inactividad

Aplique cambios de configuración sin interrumpir conexiones:

```bash
haproxy -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid -sf $(cat /run/haproxy.pid)
```

O mediante systemd:

```bash
systemctl reload haproxy
```

## Funciones Avanzadas

### Limitación de Velocidad

```cfg
frontend http-in
    bind *:80

    # Allow 10 requests per second per IP, burst to 20
    stick-table type ip size 1m expire 10s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 20 }
    default_backend webservers
```

### HTTP/2 y gRPC

HAProxy soporta HTTP/2 y puede actuar como proxy de gRPC sin ninguna configuración especial más allá de habilitar `alpn`:

```cfg
frontend https-in
    bind *:443 ssl crt /etc/ssl/certs/example.pem alpn h2,http/1.1
    default_backend grpc_servers

backend grpc_servers
    server grpc1 10.0.0.1:50051 check
```

### QUIC / HTTP/3

Las versiones recientes (≥2.5) incluyen soporte experimental de QUIC para HTTP/3 basado en UDP:

```cfg
frontend quic-in
    bind quic4@:443 ssl crt /etc/ssl/certs/example.pem
    default_backend webservers
```

### Observabilidad

- **Página de estadísticas:** endpoint HTML/JSON integrado (ver ejemplo anterior).
- **Métricas de Prometheus:** use la opción `stats prometheus`:

```cfg
frontend stats
    bind *:8405
    stats enable
    stats uri /metrics
    stats prometheus
```

- **Registro sin procesar:** HAProxy genera registros detallados (a syslog o un archivo de registro separado) que pueden ser analizados por herramientas como `tail`, `grep`, o enviados a ELK/Loki.

## Gestión de Línea de Comandos

HAProxy proporciona una API de ejecución enriquecida a través de un socket Unix o socket TCP. La utilidad `socat` se usa comúnmente para enviar comandos:

```bash
echo "show info" | socat stdio unix-connect:/run/haproxy.sock
echo "show stat" | socat stdio unix-connect:/run/haproxy.sock
echo "enable server webservers/web1" | socat stdio unix-connect:/run/haproxy.sock
```

La API de ejecución también soporta la adición/eliminación dinámica de servidores, lo cual es crucial para entornos de contenedores.

## Consideraciones de Seguridad

- **Ejecutar como no root:** HAProxy abandona los privilegios después de enlazar los puertos. Las directivas `user` y `group` en `global` son obligatorias.
- **Habilitar chroot:** Establezca `chroot /var/lib/haproxy` para aislar el proceso del sistema de archivos.
- **Restringir estadísticas:** Use autenticación, ACLs, o enlace las estadísticas en una interfaz privada.
- **Ajustar tiempos de espera:** Evita que clientes lentos agoten los grupos de conexiones.
- **Habilitar protección contra SYN flood:** Use las opciones `tcp-smart-connect` y `tcp-smart-accept`.

## Conclusión

HAProxy es un componente maduro y probado en batalla que forma la columna vertebral de muchos sistemas críticos de alto tráfico. Su enfoque láser en el balanceo de carga y el proxy proporciona rendimiento, estabilidad y control granular sin igual. Ya sea que esté ejecutando un pequeño blog o un SaaS global, HAProxy es una herramienta esencial en el kit de cualquier ingeniero de infraestructura.

Para más información, consulte la [documentación oficial de HAProxy](https://www.haproxy.org/documentation/) o el [sitio de HAProxy Technologies](https://www.haproxy.com/).