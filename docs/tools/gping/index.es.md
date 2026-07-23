---
title: gping - Herramienta de Supervisión de Red
description: gping es una herramienta de línea de comandos para medir la latencia de red con visualización en tiempo real de gráficos.
created: 2026-07-23
tags:
  - red
  - supervisión
  - gping
  - ping
status: borrador
---

# gping - Herramienta de Supervisión de Red

## Overview

**gping** es una herramienta de línea de comandos para medir el tiempo de ida y vuelta (RTT) entre dos nodos de red. A diferencia del comando `ping`, utiliza la función `getaddrinfo` del `glibc` para resolver nombres de host, lo que lo hace más flexible y capaz de manejar diferentes tipos de direcciones de red. gping está diseñado para la supervisión de red, la depuración de problemas y la prueba de rendimiento.

## Características Principales

- **Resolución de DNS**: Utiliza `getaddrinfo` para la resolución de nombres de host, soportando IPv4, IPv6 y otros tipos de direcciones.
- **Soporte para Varios Nodos**: Puede pingear múltiples nodos simultáneamente.
- **Configuración Flexible**: Permite la personalización de parámetros de ping como el timeout, el tamaño del paquete, etc.
- **Información Extensa**: Proporciona información detallada sobre el recorrido de la red y la resolución de DNS.

## Historia

`gping` fue desarrollado como parte del proyecto de la Biblioteca C de GNU (glibc). La primera implementación fue añadida a glibc en la versión 2.15. Desde entonces, se ha mejorado y actualizado continuamente para soportar protocolos de red y características más nuevos.

## Casos de Uso

- **Depuración de Red**: Diagnóstico de problemas de latencia y conectividad de red.
- **Prueba de Rendimiento**: Evaluación del rendimiento de las conexiones de red y los servicios.
- **Scripting e Introducción Automatizada**: Incorporación de pruebas de red en scripts y flujos de trabajo automatizados.

## Instalación

`gping` se incluye típicamente en el paquete glibc, que forma parte del sistema base en muchas distribuciones de Linux. Aquí te mostramos cómo instalarlo:

### Debian/Ubuntu
```sh
sudo apt-get update
sudo apt-get install glibc-doc
```

### Red Hat/CentOS
```sh
sudo yum install glibc-doc
```

### Arch Linux
```sh
sudo pacman -S glibc
```

## Uso Básico

### Ping Básico
Para realizar un ping básico a un nombre de host o dirección IP:
```sh
gping google.com
```

### Especificación de Opciones de Ping
Puedes especificar varias opciones para personalizar el comportamiento de ping:

```sh
gping -c 10 -i 2 google.com
```
- `-c 10`: Enviar 10 solicitudes ICMP.
- `-i 2`: Usar un intervalo de 2 segundos entre las paquetes de ping.

### Pingear Varios Nodos Simultáneamente
Para pingear múltiples nodos simultáneamente:
```sh
gping -c 1 -i 1 google.com example.com
```

### Salida Detallada
Para obtener una salida detallada:
```sh
gping -v google.com
```

## Ejemplo de Uso

Aquí tienes un ejemplo de una sesión:

```sh
gping -v google.com
```

La salida podría ser algo así:
```
PING google.com (93.184.216.34): 56 bytes de datos
64 bytes de 93.184.216.34: secuencia=0 TTL=56 tiempo=24.1 ms
64 bytes de 93.184.216.34: secuencia=1 TTL=56 tiempo=23.5 ms
64 bytes de 93.184.216.34: secuencia=2 TTL=56 tiempo=23.3 ms
64 bytes de 93.184.216.34: secuencia=3 TTL=56 tiempo=23.0 ms
64 bytes de 93.184.216.34: secuencia=4 TTL=56 tiempo=24.4 ms
--- google.com ping statistics ---
5 paquetes transmitidos, 5 paquetes recibidos, 0.0% pérdida de paquetes
Tiempo de ida y vuelta min./prom./max./desviación típica = 23.0/23.7/24.4/0.6 ms
```

En este ejemplo, `gping` pинг `google.com` con éxito y proporciona el tiempo de ida y vuelta promedio y otras estadísticas relevantes.

## Conclusión

`gping` es una herramienta poderosa para el diagnóstico de red y la prueba de rendimiento, ofreciendo una forma flexible y robusta de medir la latencia de red y la resolución de nombres. Su integración con glibc lo convierte en una herramienta valiosa en el conjunto de cualquier administrador de red.