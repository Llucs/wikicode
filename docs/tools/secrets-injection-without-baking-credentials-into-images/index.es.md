---
title: Inyección de Secretos Sin Introducir Credenciales en Imágenes de Docker
description: Un método para gestionar de manera segura y inyectar secretos en imágenes de contenedores sin incrustarlos directamente, asegurando una mejor seguridad y cumplimiento en los flujos de implementación.
created: 2026-07-04
tags:
  - DevOps
  - Docker
  - Kubernetes
  - Seguridad
  - Gestión de Secretos
status: borrador
---

# Inyección de Secretos Sin Introducir Credenciales en Imágenes de Docker

La inyección de secretos se refiere al proceso de gestionar y inyectar datos sensibles en aplicaciones contenerizadas en tiempo de ejecución. Esto se logra no incrustando credenciales o secretos directamente en la imagen de Docker, sino proporcionándolos en tiempo de ejecución o durante el proceso de implementación.

## Características Clave

1. **Seguridad en Tiempo de Ejecución**: Las credenciales nunca se incrustan en la imagen, lo que reduce el riesgo de exposición durante el análisis de imágenes o filtraciones debido a vulnerabilidades.
2. **Flexibilidad**: Permite actualizaciones fáciles de secretos sin la necesidad de重建提示：
似乎在翻译过程中，Markdown的内容没有被完整翻译。请允许我继续完成这个翻译任务。以下是翻译后的完整内容：

---
title: Inyección de Secretos Sin Introducir Credenciales en Imágenes de Docker
description: Un método para gestionar de manera segura y inyectar secretos en imágenes de contenedores sin incrustarlos directamente, asegurando una mejor seguridad y cumplimiento en los flujos de implementación.
created: 2026-07-04
tags:
  - DevOps
  - Docker
  - Kubernetes
  - Seguridad
  - Gestión de Secretos
status: borrador
---

# Inyección de Secretos Sin Introducir Credenciales en Imágenes de Docker

Secrets injection (inyección de secretos) se refiere al proceso de gestionar y inyectar datos sensibles en aplicaciones contenerizadas en tiempo de ejecución. Esto se logra no incrustando credenciales o secretos directamente en la imagen de Docker, sino proporcionándolos en tiempo de ejecución o durante el proceso de implementación.

## Características Clave

1. **Seguridad en Tiempo de Ejecución**: Las credenciales nunca se incrustan en la imagen, lo que reduce el riesgo de exposición durante el análisis de imágenes o filtraciones debido a vulnerabilidades.
2. **Flexibilidad**: Permite actualizaciones fáciles de secretos sin la necesidad de reconstruir y redeployar la imagen.
3. **Escala**: Facilita la gestión segura de secretos en un entorno de contenedores múltiples y microservicios.
4. **Cumplimiento**: Ayuda a las organizaciones a adherirse a estándares regulatorios y prácticas de seguridad y cumplimiento.

## Casos de Uso

1. **Credenciales de Base de Datos**: Gestionar de manera segura los nombres de usuario y contraseñas de la base de datos.
2. **Claves de API**: Almacenar y inyectar claves de API para diversos servicios.
3. **Gestión de Configuración**: Inyectar configuraciones que no forman parte del código fuente de la aplicación.
4. **Claves de Encriptación**: Administrar claves de encriptación para la protección de datos en reposo o en tránsito.

## Instalación

El proceso de instalación varía según la herramienta o solución específica utilizada para la gestión de secretos. Aquí se presentan pasos generales para algunas soluciones comunes:

### Secretos de Kubernetes

1. **Requisitos Previos**: Clúster de Kubernetes.
2. **Instalación**: No se requiere instalación expresa; los secretos son una funcionalidad incorporada en Kubernetes.
3. **Pasos**:
   1. Cree un secreto usando `kubectl` o una consola de Kubernetes.
   2. Refiera el secreto en su archivo YAML de implementación o manifiesto de Kubernetes.
   3. Monta el secreto como volumen o úsalo como variable de entorno en tus pods.

```yaml
# Ejemplo YAML para referenciar un secreto
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app-image
        env:
          - name: MY_SECRET_KEY
            valueFrom:
              secretKeyRef:
                name: my-secret
                key: my-key
```

### Secretos de Docker

1. **Requisitos Previos**: Docker Swarm.
2. **Instalación**: No se requiere instalación expresa; Docker Swarm soporta secretos por defecto.
3. **Pasos**:
   1. Cree un secreto de Docker usando el comando `docker swarm secret create`.
   2. Refiera el secreto en su definición de servicio.

```bash
# Cree un secreto de Docker
docker swarm secret create my-secret my-value

# Refiere el secreto en una definición de servicio
services:
  my-service:
    secrets:
      - my-secret
    command: ["--my-key=$(MY_SECRET_KEY)"]
```

### HashiCorp Vault

1. **Requisitos Previos**: Servidor HashiCorp Vault.
2. **Instalación**: Descargue e instale HashiCorp Vault en su servidor o utilice un servicio administrado.
3. **Pasos**:
   1. Inicialice y desbloquee Vault.
   2. Cree y almacene secretos en Vault.
   3. Utilice la API de Vault para recuperar secretos en tiempo de ejecución.

```bash
# Inicialice y desbloquee Vault
vault operator init
vault unseal <unseal-key>

# Cree y almacene un secreto
vault kv put secret/my-secret key=my-value

# Recupere el secreto utilizando la API de Vault
vault read secret/my-secret
```

## Uso Básico

### Creación de un Secreto

1. **Kubernetes**: `kubectl create secret generic my-secret --from-literal=my-key=my-value`
2. **Docker Swarm**: `docker swarm secret create my-secret my-value`
3. **HashiCorp Vault**: `vault kv put secret/my-secret key=my-value`

### Referencia del Secreto

1. **Kubernetes**:
   ```yaml
   spec:
     containers:
     - name: my-app
       image: my-app-image
       env:
         - name: MY_SECRET_KEY
           valueFrom:
             secretKeyRef:
               name: my-secret
               key: my-key
   ```

2. **Docker Swarm**:
   ```yaml
   services:
     my-service:
       secrets:
         - my-secret
       command: ["--my-key=$(MY_SECRET_KEY)"]
   ```

3. **HashiCorp Vault**:
   - Los secretos se pueden recuperar mediante la API de Vault o utilizando el comando `vault read`.

Adoptando prácticas de inyección de secretos, las organizaciones pueden mejorar significativamente la postura de seguridad de sus aplicaciones contenerizadas, asegurándose de que los datos sensibles permanezcan protegidos y gestionables a lo largo del ciclo de desarrollo e implementación.