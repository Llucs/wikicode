---
title: Promtail - Un Envíador de Log para Prometheus
description: Promtail es un envíador de log ligero, flexible y altamente configurable diseñado para recoger logs de diversas fuentes y enviarlos a un servidor de Prometheus o a otros sistemas de almacenamiento compatibles.
created: 2026-06-26
tags:
  - logging
  - prometheus
  - grafana
status: draft
---

# Promtail - Un Envíador de Log para Prometheus

Promtail es un envíador de log para Prometheus, desarrollado y mantenido por Grafana Labs. Es una herramienta ligera, flexible y altamente configurable diseñada para recoger logs de diversas fuentes y enviarlos a un servidor de Prometheus o a otros sistemas de almacenamiento compatibles.

## Características Principales

1. **Alta Disponibilidad y Resistencia a Fallos**: Promtail está diseñado para manejar las fallas de manera grácil. Puede reintentar logs fallidos de forma automática y admite la configuración para la reprocessed de logs.
2. **Flexibilidad**: Promtail soporta diversos formatos de logs (JSON, syslog, texto plano) y puede ser configurado para coincidir y extraer información relevante de los logs utilizando expresiones regulares.
3. **Escala**: Promtail está optimizado para el procesamiento de gran volumen de logs y puede manejar grandes cantidades de datos de manera eficiente.
4. **Seguridad**: Soporta TLS para comunicación segura entre Promtail y el servidor de Prometheus.
5. **Configuración**: Las configuraciones se almacenan en un archivo YAML, lo que facilita el manejo y mantenimiento.
6. **Integración**: Promtail puede integrarse fácilmente en infraestructuras de registro existentes y es compatible con una variedad de sistemas de registro.

## Historia

Promtail fue introducido por primera vez en 2018 como parte del proyecto Grafana Labs. Fue desarrollado inicialmente para abordar la necesidad de un envíador de log ligero y eficiente que se pudiera integrar con el sistema de monitoreo Prometheus. A lo largo de los años, Promtail ha evolucionado para convertirse en una herramienta robusta y ampliamente utilizada en el ecosistema de registro y monitoreo.

## Casos de Uso

1. **Logs de Aplicación**: Promtail puede utilizarse para recoger logs de servidores, contenedores y otras fuentes y enviarlos a Prometheus para monitoreo y alertas.
2. **Monitoreo de Seguridad**: Al recoger y analizar datos de logs, Promtail puede utilizarse para detectar infracciones de seguridad, anomalías y otros eventos relacionados con la seguridad.
3. **Soporte Diagnóstico**: Promtail ayuda en la diagnóstico de problemas en sistemas en producción proporcionando logs detallados que pueden ser analizados para depuración.
4. **Cumplimiento**: Promtail puede utilizarse para asegurar que los datos de logs se recopilen y almacenados en cumplimiento con requisitos regulatorios.
5. **Monitoreo**: Promtail integra de manera sin problemas con Prometheus para monitoreo en tiempo real de logs y alertas basadas en datos de logs.

## Instalación

### Requisitos Previos
- Go (para la construcción desde el fuente)
- Docker (para instalaciones en contenedor)

### Construcción desde el Fuente
1. **Clonar el Repositorio**:
   ```sh
   git clone https://github.com/grafana/promtail.git
   cd promtail
   ```

2. **Compilar la Binaria**:
   ```sh
   make build
   ```

3. **Ejecutar Promtail**:
   ```sh
   ./promtail
   ```

### Instalación con Docker
1. **Pullar la Imagen de Docker**:
   ```sh
   docker pull grafana/promtail
   ```

2. **Ejecutar Promtail con Docker**:
   ```sh
   docker run -d --name promtail \
     -v /path/to/config.yml:/promtail/promtail.yml \
     grafana/promtail -config.file=/promtail/promtail.yml
   ```

## Uso Básico

### Configuración de Promtail
Promtail utiliza un archivo YAML para especificar las fuentes de logs, reglas de análisis y destinos de salida. Aquí está un ejemplo de configuración:

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://localhost:9091/log

scrape_configs:
  - job_name: server
    static_configs:
      - targets:
          - localhost
        labels:
          job: server
```

### Ejecutar Promtail
Una vez que la configuración del archivo esté lista, se puede ejecutar Promtail para empezar a recoger logs.

```sh
promtail -config.file=/path/to/config.yml
```

### Monitorear Logs
Promtail envía los logs recolectados al servidor de Prometheus especificado. Se puede usar Prometheus para consultar y visualizar los datos de logs.

## Conclusión

Promtail es una herramienta poderosa para recoger y enviar datos de logs a Prometheus, proporcionando una integración sin problemas para monitoreo y alertas. Su flexibilidad y facilidad de uso lo hacen una adición valiosa a cualquier infraestructura de registro y monitoreo.

---