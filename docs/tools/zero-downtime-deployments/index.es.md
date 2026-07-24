---
title: Despliegues Sin Interrupción
description: Una guía completa para implementar despliegues sin interrupción con estrategias de azul/verde, canarios y actualizaciones escalonadas.
created: 2026-07-24
tags:
  - DevOps
  - Despliegue
  - Sin Interrupción
status: borrador
---

# Despliegues Sin Interrupción

El despliegue sin interrupción es una práctica de ingeniería de software que asegura que un servicio o aplicación esté disponible para los usuarios durante el proceso de implementación. Esta técnica implica estrategias para minimizar o eliminar cualquier interrupción en la disponibilidad del servicio cuando se despliegan nuevas versiones de código o configuraciones. El objetivo es mantener la disponibilidad del servicio incluso durante actualizaciones de software o actividades de mantenimiento.

## Características Clave

1. **Descubrimiento de Servicios y Equilibrado de Carga:** Utiliza mecanismos como DNS, enrutadores de servicios o equilibradores de carga para rutear el tráfico a diferentes instancias.
2. **Despliegue Azul/Verde:** Deploea dos ambientes idénticos (azul y verde), permitiendo el cambio de tráfico entre ellos sin interrupción.
3. **Lanzamientos Canarios:** Introduce gradualmente nuevas versiones a un pequeño subconjunto de usuarios para probar problemas antes de desplegarlas a todo el conjunto de usuarios.
4. **Actualizaciones Escalonadas:** Actualiza gradualmente las instancias individuales o en grupos para asegurar que no haya un solo punto de fallo.
5. **Arquitectura Microservicios:** Rompe la aplicación en servicios más pequeños e independientes para asegurar que los fallos en un servicio no afecten a otros.

## Instalación

La instalación de herramientas y estrategias de despliegue sin interrupción depende del entorno y las tecnologías específicas en uso. Aquí hay algunos pasos generales:

1. **Configuración del Entorno:**
   - Configura un equilibrador de carga o enrutador de servicios para administrar el ruteo de tráfico.
   - Configura DNS para el descubrimiento de servicios y el fallo de la ruta.

2. **Despliegue Azul/Verde:**
   - Deploea una nueva versión del servicio en un nuevo entorno.
   - Usa el equilibrador de carga para rutear el tráfico entre el antiguo y el nuevo entorno.
   - Una vez verificado el nuevo entorno, cambia completamente el tráfico.

3. **Lanzamientos Canarios:**
   - Deploea una nueva versión a un pequeño subconjunto de usuarios o a una región específica.
   - Monitorea el rendimiento y la retroalimentación del usuario.
   - Aumenta gradualmente la porción de usuarios o regiones que reciben la nueva versión.

4. **Actualizaciones Escalonadas:**
   - Actualiza una instancia a la vez o en lotes.
   - Monitorea cualquier problema y realiza un despliegue de retroceso si es necesario.
   - Aumenta gradualmente el número de instancias actualizadas.

5. **Microservicios:**
   - Usa un enrutador de servicios o herramienta de orquestación (como Kubernetes) para gestionar el despliegue de servicios individuales.
   - Asegúrate de que cada servicio pueda ser escalado e actualizado individualmente.

## Uso Básico

1. **Planificación del Despliegue:**
   - Define la estrategia (azul/verde, canarios, actualizaciones escalonadas).
   - Planifica para posibles problemas y prepara estrategias de retroceso.

2. **Preparación del Nuevo Despliegue:**
   - Construye y prueba la nueva versión de manera exhaustiva.
   - Asegúrate de que todas las dependencias estén correctamente configuradas.

3. **Despliegue de la Nueva Versión:**
   - Usa la estrategia elegida para desplegar la nueva versión.
   - Monitorea el proceso de despliegue para cualquier problema.

4. **Verificación y Escalado:**
   - Monitorea la nueva versión para la estabilidad y el rendimiento.
   - Aumenta gradualmente la nueva versión y retira la antigua.

5. **Documentación e Aprendizaje:**
   - Documenta el proceso de despliegue y las lecciones aprendidas.
   - Mejora continuamente la estrategia de despliegue basándose en la experiencia.

### Ejemplo: Despliegue Azul/Verde con Kubernetes

#### Requisitos Previos
- Clúster de Kubernetes con `kubectl` instalado y configurado.
- Dos despliegues idénticos: `azul` y `verde`.

#### Paso 1: Definir los Manifestos de Despliegue

Crea dos manifiestos de despliegue, uno para cada entorno.

**Despliegue Azul:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-azul
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: azul
  template:
    metadata:
      labels:
        app: my-app
        version: azul
    spec:
      containers:
      - name: my-app
        image: my-app:azul
        ports:
        - containerPort: 80
```

**Despliegue Verde:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-verde
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: verde
  template:
    metadata:
      labels:
        app: my-app
        version: verde
    spec:
      containers:
      - name: my-app
        image: my-app:verde
        ports:
        - containerPort: 80
```

#### Paso 2: Despliegue del Entorno Azul

```bash
kubectl apply -f azul-deployment.yaml
```

#### Paso 3: Crear un Servicio para el Equilibrio de Carga

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: my-app
```

Aplica el manifiesto del servicio:

```bash
kubectl apply -f service.yaml
```

#### Paso 4: Cambiar el Tráfico al Entorno Verde

Actualiza el servicio para rutear el tráfico al entorno verde:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: my-app
    version: verde
```

Aplica el manifiesto del servicio actualizado:

```bash
kubectl apply -f service.yaml
```

#### Paso 5: Verificar el Despliegue

Comprueba el estado de los pods y el servicio:

```bash
kubectl get pods
kubectl get services
```

Una vez verificado, puedes cambiar el tráfico de vuelta al entorno azul si es necesario.

### Ejemplo: Lanzamientos Canarios

#### Requisitos Previos
- Clúster de Kubernetes con `kubectl` instalado y configurado.
- Dos despliegues: `stable` y `canario`.

#### Paso 1: Definir los Manifestos de Despliegue

Crea dos manifiestos de despliegue, uno para cada entorno.

**Despliegue Stable:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-stable
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: stable
  template:
    metadata:
      labels:
        app: my-app
        version: stable
    spec:
      containers:
      - name: my-app
        image: my-app:stable
        ports:
        - containerPort: 80
```

**Despliegue Canario:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-canario
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: canario
  template:
    metadata:
      labels:
        app: my-app
        version: canario
    spec:
      containers:
      - name: my-app
        image: my-app:canario
        ports:
        - containerPort: 80
```

#### Paso 2: Despliegue del Entorno Stable

```bash
kubectl apply -f stable-deployment.yaml
```

#### Paso 3: Crear un Servicio para el Equilibrio de Carga

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: my-app
```

Aplica el manifiesto del servicio:

```bash
kubectl apply -f service.yaml
```

#### Paso 4: Despliegue del Entorno Canario

```bash
kubectl apply -f canario-deployment.yaml
```

#### Paso 5: Rutear el Tráfico al Entorno Canario

Actualiza el servicio para rutear el tráfico al entorno canario:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: my-app
    version: canario
```

Aplica el manifiesto del servicio actualizado:

```bash
kubectl apply -f service.yaml
```

#### Paso 6: Verificar el Despliegue

Comprueba el estado de los pods y el servicio:

```bash
kubectl get pods
kubectl get services
```

Una vez verificado, puedes aumentar gradualmente el tráfico canario:

```bash
kubectl patch service my-app-service -p '{"spec":{"selector":{"app":"my-app","version":"canario"}}}'
```

Monitorea el entorno canario para cualquier problema y aumenta gradualmente el tráfico canario hasta el 100%.

### Conclusión

Los despliegues sin interrupción son esenciales para mantener la confiabilidad y la disponibilidad de sistemas distribuidos. Al emplear estrategias efectivas, técnicas de implementación y herramientas adecuadas, las organizaciones pueden lograr actualizaciones sin interrupciones sin interrumpir la experiencia del usuario. Este guía proporciona una visión general completa de las estrategias de despliegue azul/verde, canarios y actualizaciones escalonadas, junto con ejemplos prácticos utilizando Kubernetes.

---