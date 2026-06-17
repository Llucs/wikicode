---
title: Portainer
description: Una herramienta de gestión de contenedores y orquestación autoalojada que centraliza la gobernanza, RBAC/SSO y el control operativo en múltiples entornos.
created: 2026-06-15
tags:
  - docker
  - kubernetes
  - container-management
  - devops
  - open-source
  - orchestration
  - self-hosted
  - portainer-ce
status: draft
ecosystem: containers
---

# Portainer

## Visión general

Portainer es el estándar de la industria, un "panel único" de código abierto para gestionar entornos contenerizados. Diseñado por Neil Cresswell y bifurcado de DockerUI en 2017, Portainer tiene como objetivo eliminar la pronunciada curva de aprendizaje y la sobrecarga operativa de Docker, Docker Swarm, Kubernetes, Azure ACI y HashiCorp Nomad. Se ejecuta como un contenedor ligero en sí mismo (o mediante un Helm chart) y expone una potente interfaz web respaldada por una API REST con todas las funciones.

Portainer se publica bajo la licencia AGPLv3 para la Community Edition (CE), con una Business Edition (BE) comercial que añade características empresariales como cumplimiento FIPS, RBAC granular y soporte dedicado.

## ¿Por qué Portainer?

- **Plano de control unificado:** Gestiona todos los motores de contenedores de tu flota desde una única interfaz web, evitando tener que cambiar entre diferentes CLIs.
- **Complejidad reducida:** Equipos no especializados pueden desplegar y gestionar aplicaciones sin necesidad de aprender intrincados comandos `kubectl` o `docker-compose`.
- **Preparado para GitOps:** Los stacks se pueden vincular directamente a repositorios Git. Cualquier push al repositorio desencadena un redespliegue automático.
- **Edge Compute:** Gestiona de forma segura miles de dispositivos detrás de NAT o cortafuegos mediante Edge Agents.
- **Ligero y no intrusivo:** Portainer no reemplaza tu orquestador existente; se sitúa a su lado, leyendo la API de Docker/Kubernetes a través de un socket o un contenedor Agent dedicado.

## Arquitectura

Portainer utiliza un modelo estándar servidor-agente:

1.  **Portainer Server (portainer/portainer-ce):** La aplicación principal. Sirve la interfaz web y la API REST. Este es el nodo al que apuntas con tu navegador.
2.  **Portainer Agent (portainer/agent):** Un contenedor sidecar ligero desplegado en cada host Docker o nodo Kubernetes que desees gestionar de forma remota. El Agent se comunica con el socket local de Docker y expone una API segura en el puerto 9001.
3.  **Edge Agent:** Una variante del agente estándar diseñada para ubicaciones remotas. Inicia un túnel *saliente* hacia el Portainer Server, permitiendo la gestión a través de cortafuegos estrictos sin necesidad de abrir puertos entrantes.

```text
[Navegador Admin] <--> [Portainer Server :9443]
                         |
            +------------+-------------+
            |            |             |
    [Docker Agent 1] [Docker Agent 2] [K8s Cluster (Helm)]
            |            |
    [Docker Daemon] [Docker Daemon]
```

## Instalación

### Docker Standalone (Inicio rápido)

Este es el método más común para gestionar un host Docker local o un número reducido de ellos.

```bash
# Crear un volumen persistente para los datos de Portainer
docker volume create portainer_data

# Ejecutar el contenedor Portainer Server
docker run -d -p 8000:8000 -p 9443:9443 --name portainer \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v portainer_data:/data \
    portainer/portainer-ce:lts
```

- `-p 9443:9443`: Interfaz web y API (HTTPS).
- `-p 8000:8000`: (Opcional) Túnel TCP para conexiones de Edge Agent.
- `-v /var/run/docker.sock`: Permite que Portainer gestione el host en el que se ejecuta.
- `:lts`: La etiqueta de Long Term Support. **Usa siempre `:lts` en producción.**

### Docker Swarm

Despliega Portainer como un servicio global en tu clúster Swarm.

```bash
curl -L https://downloads.portainer.io/ce2-19/portainer-agent-stack.yml -o portainer-agent-stack.yml

docker stack deploy -c portainer-agent-stack.yml portainer
```

### Kubernetes (Helm)

Despliega Portainer en tu clúster Kubernetes usando el Helm chart oficial.

```bash
helm repo add portainer https://portainer.github.io/k8s/
helm repo update

helm upgrade --install portainer portainer/portainer \
    --namespace portainer --create-namespace \
    --set service.type=LoadBalancer \
    --set service.httpPort=9000 \
    --set service.httpsPort=9443
```

### Instalación en entorno aislado (Air-Gapped)

Para entornos sin acceso a Internet, descarga previamente las imágenes.

```bash
# En una máquina con acceso a Internet
docker pull portainer/portainer-ce:lts
docker pull portainer/agent:lts

# Etiqueta y sube a tu registro interno
docker tag portainer/portainer-ce:lts <internal-registry>/portainer-ce:lts
docker tag portainer/agent:lts <internal-registry>/agent:lts
docker push <internal-registry>/portainer-ce:lts
docker push <internal-registry>/agent:lts
```

## Configuración inicial

1.  Abre un navegador en `https://<IP_DEL_SERVIDOR>:9443`.
2.  Crea una contraseña segura para el usuario `admin`.
3.  Aparecerá el asistente de configuración rápida. Selecciona **Docker** y elige **Socket** para conectarte al daemon Docker local.
4.  Haz clic en **Conectar**. Ahora estás en la página **Inicio**—este es tu selector de entornos.

## Características principales y ejemplos de comandos

### 1. Gestión multi-entorno

Conecta hosts Docker remotos desplegando el Portainer Agent.

**En el host remoto (destino):**
```bash
docker run -d -p 9001:9001 --name portainer_agent \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /var/lib/docker/volumes:/var/lib/docker/volumes \
    portainer/agent:lts
```

**En la interfaz de Portainer Server:**
Navega a **Entornos** > **Añadir entorno** > **Docker Agent**.
Introduce la IP y el puerto del host remoto (9001). Haz clic en **Conectar**.

### 2. Plantillas de aplicaciones (Despliegue en un clic)

Portainer incluye un catálogo de aplicaciones predefinidas (Nginx, MySQL, WordPress, etc.).

**Flujo de trabajo:**
1. Barra lateral > **Plantillas de aplicaciones**.
2. Haz clic en una plantilla (ej., **Nginx**).
3. Personaliza nombre, puertos, variables de entorno.
4. Haz clic en **Desplegar el stack**.

### 3. Stacks y GitOps

Despliega aplicaciones complejas utilizando archivos Docker Compose o manifiestos de Kubernetes. Los stacks se pueden vincular a un repositorio Git para flujos de trabajo GitOps.

**Despliegue manual con Compose:**
Pega esto en **Stacks** > **Añadir stack** > **Editor web**:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
  db:
    image: postgres:13
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: example
volumes:
  pgdata:
```

**Configuración GitOps:**
1. **Stacks** > **Añadir stack** > **Repositorio**.
2. Introduce la URL del repositorio Git y la ruta al archivo Compose.
3. Activa **Actualizaciones automáticas**.
4. Haz clic en **Desplegar el stack**. Cualquier `git push` desencadena un redespliegue.

### 4. Gestión de Kubernetes

Portainer abstrae la complejidad de `kubectl`. Puedes crear Namespaces, Deployments, Services e Ingresses mediante un formulario o YAML.

**Ejemplo:** Desplegar una carga de trabajo simple con nginx.
1. **Entornos** > Selecciona tu **clúster Kubernetes**.
2. **Kubernetes** > **Cargas de trabajo** > **Añadir carga de trabajo**.
3. Rellena el formulario (Nombre: `nginx`, Imagen: `nginx:alpine`, Puerto: `80`).
4. Haz clic en **Desplegar**.

### 5. Registros

Gestiona centralizadamente las credenciales para Docker Hub, GitLab, Quay, Amazon ECR y Google Container Registry.

1. **Registros** > **Añadir registro**.
2. Elige tu proveedor (ej., **Docker Hub**).
3. Introduce tus credenciales (usuario/token de acceso).

### 6. Edge Compute

Gestiona dispositivos remotos (IoT, retail, ubicaciones de campo) detrás de NAT/cortafuegos. El servidor genera un `EDGE_ID` y un `EDGE_KEY`.

**En el dispositivo Edge:**
```bash
docker run -d \
  -e EDGE=1 \
  -e EDGE_ID=<EDGE_ID> \
  -e EDGE_KEY=<EDGE_KEY> \
  -e CAP_HOST_MANAGEMENT=1 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name portainer_edge_agent \
  portainer/agent:lts
```

### 7. API REST

Portainer tiene una API REST muy completa. Genera una clave de API en **Ajustes** > **Seguridad**.

```bash
# Listar todos los entornos
curl -X GET 'https://<IP_DEL_SERVIDOR>:9443/api/endpoints' \
    -H 'X-API-Key: ptr_xxxxxxxxxxxx' | jq .

# Desplegar un stack
curl -X POST 'https://<IP_DEL_SERVIDOR>:9443/api/stacks' \
    -H 'X-API-Key: ptr_xxxxxxxxxxxx' \
    -H 'Content-Type: application/json' \
    -d '{
      "Name": "my-api-stack",
      "StackFileContent": "version: \"3.8\"\nservices:\n  web:\n    image: nginx:alpine",
      "SwarmID": "",
      "EndpointID": 1
    }'
```

## Comparación de ediciones

| Característica | Community Edition (CE) | Business Edition (BE) |
|---|---|---|
| Licencia | AGPLv3 | Comercial |
| Multi-entorno | Ilimitado | Ilimitado |
| GitOps | Sí | Sí |
| Edge Compute | Limitado | Completo (Edge Groups, Stacks, Jobs) |
| RBAC / SSO | Básico | Avanzado (AD/LDAP/OAuth, Roles de equipo, Controles de recursos) |
| Gestión de registros | Manual | Centralizada con gobernanza |
| Soporte | Comunidad | Comercial (24/7/365) |
| Cumplimiento FIPS | No | Sí |

## Mejores prácticas

1.  **Usa versiones `:lts`.** No uses la etiqueta `:latest` en producción; corresponde a builds en desarrollo (bleeding-edge).
2.  **Dedica el nodo Server.** No ejecutes decenas de cargas de trabajo en el contenedor Portainer Server. Úsalo estrictamente como punto de gestión.
3.  **Realiza copias de seguridad de `portainer_data` regularmente.** Ejecuta esto para respaldar el volumen:
    ```bash
    docker run --rm -v portainer_data:/data -v $(pwd):/backup alpine tar cvf /backup/portainer_backup.tar /data
    ```
4.  **Asegura con TLS adecuado.** Reemplaza el certificado autofirmado en Producción.
    ```bash
    docker run -d -p 9443:9443 --name portainer \
        -v /path/to/fullchain.pem:/certs/portainer.crt \
        -v /path/to/privkey.pem:/certs/portainer.key \
        -v portainer_data:/data \
        portainer/portainer-ce:lts
    ```

## Solución de problemas

### Fallos de conexión del Agent
- Asegúrate de que el puerto `9001` esté abierto en la máquina de destino.
- Verifica que el contenedor Portainer Agent se esté ejecutando.
- Si usas un cortafuegos, asegúrate de que el Server pueda iniciar conexiones salientes hacia el Agent.

### Contraseña de administrador olvidada
Un contenedor auxiliar genera un hash que puedes establecer de forma segura.
```bash
docker run --rm -v portainer_data:/data portainer/helper-reset-password
```

### Portainer no se inicia
Revisa los logs:
```bash
docker logs portainer
```
Los problemas comunes incluyen datos de volumen corruptos, versiones de Portainer no coincidentes o errores de permisos del daemon Docker del host.

## Referencias

- **Sitio web oficial:** [https://www.portainer.io/](https://www.portainer.io/)
- **GitHub:** [https://github.com/portainer/portainer](https://github.com/portainer/portainer)
- **Documentación oficial:** [https://docs.portainer.io/](https://docs.portainer.io/)
- **Docker Hub:** [portainer/portainer-ce](https://hub.docker.com/r/portainer/portainer-ce)
- **Comunidad Slack:** [Portainer Slack](https://portainer.io/slack)