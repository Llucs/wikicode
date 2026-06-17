---
title: Grafana: la plataforma abierta de observabilidad
description: Visualización, monitoreo y alertas unificados para métricas, registros y trazas.
created: 2026-06-15
tags:
  - observability
  - monitoring
  - visualization
  - dashboards
  - open-source
status: draft
ecosystem: observability
---

# Grafana: la plataforma abierta de observabilidad

## ¿Qué es Grafana?

Grafana es la plataforma líder de análisis y visualización interactiva de código abierto para la observabilidad. Se conecta a cualquier fuente de datos —desde bases de datos de series temporales (Prometheus, InfluxDB, Graphite) hasta sistemas de registro (Loki, Elasticsearch), sistemas de trazado (Tempo, Jaeger), almacenes SQL (PostgreSQL, MySQL) y APIs en la nube (AWS CloudWatch, Azure Monitor). Proporciona un único “pane of glass” para consultar, visualizar, configurar alertas y comprender tus métricas, registros y trazas.

Debido a que Grafana está construido sobre estándares abiertos, evitas el vendor lock‑in. Puedes mezclar datos de docenas de fuentes en el mismo panel, y la misma plataforma funciona igualmente bien para monitoreo de infraestructura, gestión del rendimiento de aplicaciones, análisis de negocio o telemetría IoT.

---

## ¿Por qué usar Grafana?

- **Observabilidad unificada** – reúne métricas, registros, trazas y datos de negocio en un solo lugar.
- **Visualización enriquecida** – docenas de tipos de paneles (series temporales, estadísticas, tabla, mapa de calor, geomapa, velas, registros, trazas y más).
- **Paneles dinámicos** – usa variables de plantilla para hacer que los paneles sean reutilizables e interactivos.
- **Alertas unificadas** – gestiona todas las reglas de alerta entre fuentes de datos desde una única interfaz.
- **Modo Explore** – solución de problemas ad hoc sin guardar un panel.
- **Extensible** – mercado de complementos para fuentes de datos, paneles y aplicaciones.
- **Preparado para GitOps** – aprovisiona paneles, fuentes de datos y reglas de alerta con archivos de configuración.
- **Seguridad y gobierno** – organizaciones, equipos, RBAC detallado, OAuth y claves API.
- **Autogestionado o en la nube** – ejecútalo tú mismo o usa Grafana Cloud (generoso nivel gratuito).

---

## Instalación

### 1. Binario / Paquete

Descarga el paquete `.rpm`, `.deb` o el tarball independiente desde la [página de descargas](https://grafana.com/grafana/download) e instálalo:

```bash
# Debian / Ubuntu
sudo apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana_11.0.0_amd64.deb
sudo dpkg -i grafana_11.0.0_amd64.deb
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

```bash
# RHEL / CentOS / Fedora
sudo yum install -y https://dl.grafana.com/oss/release/grafana-11.0.0-1.x86_64.rpm
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

### 2. Docker

Ejecuta la imagen oficial de Docker (puerto predeterminado 3000). Monta volúmenes para datos persistentes:

```bash
docker run -d \
  -p 3000:3000 \
  --name=grafana \
  -v grafana-storage:/var/lib/grafana \
  grafana/grafana:latest
```

### 3. Kubernetes (Helm)

Agrega el repositorio de Helm de Grafana e implementa:

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install my-grafana grafana/grafana \
  --namespace monitoring --create-namespace \
  --set persistence.enabled=true \
  --set adminPassword='admin'
```

### 4. Grafana Cloud

Crea una cuenta gratuita en [grafana.com](https://grafana.com): el nivel gratuito incluye 10 000 series, retención de 14 días y acceso a la plataforma completa.

---

## Uso básico

Después de iniciar Grafana, abre `http://localhost:3000` e inicia sesión con las credenciales predeterminadas (`admin` / `admin`). Se te pedirá que establezcas una nueva contraseña.

### Paso 1: Agregar una fuente de datos

1. Ve a **Configuración → Fuentes de datos**.
2. Haz clic en **Agregar fuente de datos**.
3. Selecciona un tipo (por ejemplo, Prometheus).
4. Ingresa la URL (por ejemplo, `http://prometheus:9090`) y haz clic en **Guardar y probar**.

### Paso 2: Construir un panel

1. Haz clic en el icono **+** en la barra lateral → **Nuevo panel**.
2. Haz clic en **Agregar un nuevo panel**.
3. En el editor de consultas, escribe una consulta para tu fuente de datos (por ejemplo, una expresión PromQL).
4. Elige un tipo de visualización (Series temporales, Estadística, Indicador, Tabla, etc.).
5. Personaliza ejes, unidades, colores, umbrales y leyendas.
6. Haz clic en **Aplicar** para agregar el panel al tablero.
7. Guarda el tablero con un nombre descriptivo.

### Paso 3: Consultar datos con Explore

Para investigaciones ad hoc, usa la vista **Explore** (icono de brújula en la barra lateral). Proporciona un editor de consultas aislado sin necesidad de guardar o construir un panel.

```promql
# Ejemplo de consultas PromQL para ejecutar en Explore
rate(node_cpu_seconds_total[5m])
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
count by (job) (up == 0)
```

### Paso 4: Configurar alertas

En el editor de paneles, ve a la pestaña **Alerta**:

1. Haz clic en **Crear regla de alerta desde este panel**.
2. Define una condición (por ejemplo, `MAX() OF query (A) IS ABOVE 90`).
3. Establece el comportamiento de evaluación (por ejemplo, evaluar cada 1 m, período pendiente 5 m).
4. Agrega un **punto de contacto** (Slack, PagerDuty, Correo electrónico, webhook, etc.).
5. Guarda la regla.

Las alertas se gestionan centralmente en **Alertas → Reglas de alerta**, con soporte para silencios, tiempos de silencio y políticas de notificación.

---

## Funciones principales con ejemplos de comandos

### 1. Paneles dinámicos y variables de plantilla

Las variables te permiten hacer que los paneles sean interactivos. Por ejemplo, una variable `$job` se puede usar en una consulta PromQL:

```promql
rate(http_requests_total{job=~"$job"}[5m])
```

Define las variables en **Configuración del panel → Variables**: pueden ser de tipo Consulta, Personalizado, Intervalo, Fuente de datos, etc.

### 2. Aprovisionamiento (GitOps)

Automatiza fuentes de datos y paneles con archivos YAML colocados en el directorio de aprovisionamiento de Grafana (`/etc/grafana/provisioning/`).

**Ejemplo de aprovisionamiento de fuente de datos** (`datasources.yaml`):

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://localhost:9090
    isDefault: true
```

**Ejemplo de aprovisionamiento de panel** (`dashboards.yaml`):

```yaml
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: 'Provisioned Dashboards'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: false
    options:
      path: /var/lib/grafana/dashboards
```

Coloca los archivos JSON del panel en la ruta especificada, y Grafana los sincronizará automáticamente.

### 3. API y CLI

Grafana expone una API REST completa para automatización.

```bash
# Listar paneles
curl -s -u admin:admin http://localhost:3000/api/search?type=dash-db | jq .

# Crear una fuente de datos
curl -s -X POST -u admin:admin \
  -H "Content-Type: application/json" \
  -d '{
        "name":"MyPrometheus",
        "type":"prometheus",
        "url":"http://prometheus:9090",
        "access":"proxy"
      }' \
  http://localhost:3000/api/datasources
```

Usa `grafana-cli` para gestionar complementos:

```bash
# Instalar un complemento de panel
grafana-cli plugins install grafana-piechart-panel

# Listar complementos instalados
grafana-cli plugins ls
```

### 4. Modo Explore (solución de problemas avanzada)

Explore te permite ejecutar consultas entre métricas, registros y trazas una al lado de la otra. Por ejemplo, saltar de una métrica de alta latencia a la traza o entrada de registro relacionada.

### 5. Alertas unificadas

Todas las reglas de alerta, ya sea para Prometheus, Loki o una base de datos SQL, se gestionan en un solo lugar. Ejemplo de definición de regla a través de la API:

```json
{
  "title": "High CPU alert",
  "condition": "A",
  "data": [
    {
      "refId": "A",
      "relativeTimeRange": { "from": 600, "to": 0 },
      "datasourceUid": "P010D9A9C2F1E4B8C",
      "model": {
        "expr": "avg(node_load1) > 2",
        "intervalMs": 1000,
        "maxDataPoints": 100,
        "refId": "A"
      }
    }
  ]
}
```

### 6. Ecosistema de complementos

Extiende Grafana con complementos de la comunidad y oficiales. Navega por el catálogo de [complementos de Grafana](https://grafana.com/grafana/plugins/). Instálalos a través de la interfaz de usuario (Configuración → Complementos) o CLI.

### 7. Seguridad y autenticación

Grafana es compatible con varios métodos de autenticación: OAuth (GitHub, Google, GitLab, Okta), SAML, LDAP y Auth Proxy. RBAC se puede configurar a través de la interfaz de usuario o mediante aprovisionamiento.

Ejemplo de fragmento de configuración (`grafana.ini`):

```ini
[auth.github]
enabled = true
allow_sign_up = true
client_id = YOUR_GITHUB_CLIENT_ID
client_secret = YOUR_GITHUB_CLIENT_SECRET
scopes = user:email,read:org
```

---

## Conclusión

Grafana es el estándar abierto de facto para la observabilidad, que permite a los equipos unificar, visualizar y alertar sobre datos de cualquier fuente. Ya sea que lo ejecutes autogestionado para un pequeño clúster, lo implementes en Kubernetes a escala o uses la oferta en la nube, Grafana proporciona la flexibilidad y profundidad necesarias para mantener tus sistemas saludables. Su fuerte comunidad, desarrollo activo y extenso ecosistema de complementos lo convierten en una herramienta indispensable en el kit de herramientas moderno de DevOps y SRE.

---

> **Recursos adicionales**
>
> - Documentación oficial: [https://grafana.com/docs/](https://grafana.com/docs/)
> - Foros de la comunidad: [https://community.grafana.com/](https://community.grafana.com/)
> - Grafana Play (demo en vivo): [https://play.grafana.org/](https://play.grafana.org/)
> - Blog de Grafana Labs: [https://grafana.com/blog/](https://grafana.com/blog/)