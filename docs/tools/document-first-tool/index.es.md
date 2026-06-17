---
title: cURL — Herramienta de Transferencia de Datos
description: cURL es una herramienta de línea de comandos para transferir datos utilizando protocolos de red.
created: 2026-06-14
tags:
  - tool
  - cli
  - networking
status: draft
ecosystem: networking
---

# cURL — Herramienta de Transferencia de Datos

## Qué es

cURL (Client URL) es una herramienta y biblioteca de línea de comandos para transferir datos con URLs. Soporta docenas de protocolos incluyendo HTTP, HTTPS, FTP, SFTP, SCP, LDAP y muchos más.

## Instalación

```bash
# Ubuntu/Debian
sudo apt-get install curl

# macOS (pre-installed, or via Homebrew)
brew install curl

# Windows (via Chocolatey)
choco install curl
```

## Uso básico

### Solicitud GET

```bash
curl https://api.github.com/users/octocat
```

### POST con JSON

```bash
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com"}'
```

### Guardar respuesta en archivo

```bash
curl -o output.json https://api.example.com/data
```

### Seguir redirecciones

```bash
curl -L https://bit.ly/example
```

### Encabezados personalizados

```bash
curl -H "Authorization: Bearer token123" https://api.example.com/protected
```

## Banderas clave

| Bandera | Descripción |
|------|-------------|
| `-X` | Método HTTP (GET, POST, PUT, DELETE) |
| `-H` | Encabezado personalizado |
| `-d` | Datos del cuerpo de la solicitud |
| `-o` | Escribir salida en archivo |
| `-L` | Seguir redirecciones |
| `-v` | Modo verboso |
| `-s` | Modo silencioso (sin progreso) |
| `-k` | Permitir SSL inseguro |
| `-u` | Autenticación básica (usuario:contraseña) |

## Mejores prácticas

- Usa `-sS` en scripts para suprimir el progreso pero mantener visibles los errores
- Usa `--retry 3` para reintentos automáticos en fallos de red
- Nunca pases tokens en las URLs; usa el encabezado `Authorization` en su lugar