---
title: Caddy: El servidor web definitivo con HTTPS automático
description: Un servidor web de código abierto listo para empresas con HTTPS automático, proxy inverso y soporte para Docker, escrito en Go.
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

Caddy es un servidor web y proxy inverso potente, listo para empresas, de código abierto, escrito en Go. Está diseñado para ser simple de usar mientras proporciona seguridad robusta, gestión automática de certificados TLS y una API de configuración moderna. Caddy es mantenido por la Caddy Foundation y ampliamente adoptado tanto para entornos de desarrollo como de producción.

## Características clave

- **HTTPS Automático**: Caddy obtiene y renueva automáticamente certificados TLS de Let’s Encrypt o ZeroSSL para cada dominio configurado. Gestiona OCSP stapling, HTTP/2 y HTTP/3 (QUIC) de forma nativa.
- **Configuración Simple**: Utilice un amigable `Caddyfile` o una potente API JSON para configuración dinámica. El `Caddyfile` es un adaptador que traduce a JSON, brindándole simplicidad y flexibilidad.
- **Proxy Inverso y Balanceo de Carga**: Proxy inverso completo de Capa 7 con comprobaciones de salud activas/pasivas, reintentos, interruptores de circuito y múltiples políticas de balanceo de carga (aleatorio, menos conexiones, hash de IP, afinidad de cabecera).
- **Seguridad por Defecto**: Escrito en Go con seguridad de memoria, eliminando vulnerabilidades de desbordamiento de búfer. Los valores predeterminados de TLS son estrictamente seguros y Caddy solo escucha en puertos privilegiados cuando es necesario.
- **Arquitectura Modular**: El núcleo es mínimo; la funcionalidad se extiende mediante módulos. Construya binarios personalizados con `xcaddy` para incluir solo las funciones que necesite.
- **Nativo para Contenedores**: Binario único, apagados limpios, recargas suaves – ideal para Docker y Kubernetes.

## ¿Por qué usar Caddy?

Caddy elimina el dolor de la configuración manual de HTTPS. Aprovisiona y renueva certificados automáticamente, por lo que nunca tendrá que preocuparse por la caducidad de TLS. Su configuración es intuitiva, y sirve como un front-end perfecto para microservicios, sitios estáticos, APIs y SPAs. La API JSON permite una integración perfecta con herramientas de automatización, mientras que el `Caddyfile` ofrece una alternativa amigable para humanos. Escriba una vez, sirva de forma segura en todas partes.

## Instalación

Caddy ofrece múltiples métodos de instalación:

### Descargar un binario precompilado

```bash
# Linux / macOS / Windows binary
curl -fsSL https://caddyserver.com/download/linux/amd64 -o caddy
chmod +x caddy
sudo mv caddy /usr/local/bin/
```

*O descargue desde [caddyserver.com/download](https://caddyserver.com/download)*

### Gestores de paquetes

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

### Compilación personalizada con `xcaddy`

```bash
# Build Caddy with a specific plugin
xcaddy build --with github.com/caddyserver/transform-encoder

# Build with a custom version
xcaddy build v2.8.0 --with github.com/caddyserver/format-encoder
```

`xcaddy` compila un único binario con solo los módulos que desee.

## Uso básico

### Servidor de archivos estático

```bash
# Serve the current directory on port 80 with automatic HTTPS
caddy file-server
```

### Proxy inverso rápido

```bash
# Proxy traffic from yourdomain.com to a local backend
caddy reverse-proxy --from yourdomain.com --to localhost:8080
```

### Configuración con Caddyfile

Cree un `Caddyfile` en la raíz de su proyecto:

```caddyfile
example.com {
    root * /var/www/example
    file_server
}
```

Luego ejecute:

```bash
caddy run
```

Caddy obtendrá automáticamente un certificado TLS para `example.com` y servirá los archivos estáticos.

### Configuración JSON

El formato de configuración nativo de Caddy es JSON. Puede aplicarlo a través de la API de administración:

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

La API JSON es la fuente de verdad; el `Caddyfile` es solo un adaptador.

## Características clave en profundidad

### HTTPS automático

```caddyfile
mydomain.com {
    tls you@email.com   # Optional email for Let's Encrypt notices
}
```

Caddy maneja la emisión, renovación y redirección de HTTP a HTTPS automáticamente. Soporta certificados comodín, endpoints ACME personalizados (por ejemplo, ZeroSSL) y TLS bajo demanda.

### Proxy inverso con balanceo de carga

```caddyfile
api.example.com {
    reverse_proxy api1:8080 api2:8080 api3:8080 {
        lb_policy least_conn
        health_uri /health
        health_interval 10s
    }
}
```

Políticas: `random`, `least_conn`, `ip_hash`, `uri_hash`, `header`, `first`, `round_robin`.

### Plantillas y sitios dinámicos

Caddy puede ejecutar plantillas para contenido dinámico sin un backend separado:

```caddyfile
example.com {
    templates
    root * /var/www/example
}
```

### Autenticación

Se puede añadir autenticación modular (por ejemplo, JWT, autenticación básica) mediante plugins:

```caddyfile
example.com {
    basic_auth {
        admin $2a$14$hash...
    }
}
```

### HTTP/3 (QUIC)

Habilite HTTP/3 en su `Caddyfile`:

```caddyfile
{
    servers {
        protocol {
            quic
        }
    }
}
```

## Integración con Docker

Caddy es un ciudadano de primera clase en entornos contenerizados.

### Servir archivos estáticos desde un contenedor Docker

```dockerfile
FROM caddy:latest
COPY . /usr/share/caddy
```

Ejecute con:

```bash
docker build -t my-site .
docker run -d -p 80:80 -p 443:443 -e CADDY_INGRESS_NETWORKS=caddy my-site
```

### Usar como proxy inverso en Docker Compose

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

Caddy descubre automáticamente el contenedor `app` a través de la red Docker.

### Recargas suaves en Docker

```bash
# After changing the Caddyfile, reload without downtime
docker exec -w /etc/caddy <container_name> caddy reload
```

## Gestión del ciclo de vida

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

## Conclusión

Caddy simplifica el servicio web automatizando HTTPS, proporcionando un modelo de configuración limpio e integrándose perfectamente con las pilas modernas. Ya sea que esté implementando un sitio estático, un backend de microservicios o una puerta de enlace API completa, Caddy le brinda seguridad, rendimiento y facilidad de uso, todo en un solo binario. Con un sólido soporte para Docker y un ecosistema vibrante de complementos, es una excelente opción tanto para desarrolladores como para equipos de operaciones.