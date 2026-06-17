---
title: ArgoCD – Entrega Continua GitOps para Kubernetes
description: ArgoCD es una herramienta declarativa de entrega continua impulsada por GitOps que sincroniza aplicaciones de Kubernetes con repositorios de Git como la fuente única de verdad.
created: 2026-06-15
tags:
  - gitops
  - kubernetes
  - continuous-delivery
  - argocd
  - devops-tools
status: draft
ecosystem: kubernetes
---

# ArgoCD – Entrega Continua GitOps para Kubernetes

## ¿Qué es ArgoCD?

ArgoCD es una herramienta declarativa de **GitOps** para entrega continua (CD) diseñada específicamente para Kubernetes. Trata los repositorios de Git como la **fuente única de verdad** para las definiciones de aplicaciones y manifiestos de Kubernetes. ArgoCD monitorea constantemente el estado del clúster en vivo y lo reconcilia con el estado deseado definido en Git, permitiendo despliegues totalmente automatizados, auditables y repetibles.

## ¿Por qué ArgoCD?

- **Declarativo y Controlado por Versiones** – Toda la configuración de infraestructura y aplicaciones vive en Git. Los cambios se realizan mediante pull requests, no comandos imperativos.
- **Autocuración Automatizada** – El sistema corrige automáticamente la desviación de configuración revirtiendo cualquier cambio manual a lo definido en Git.
- **Traza de Auditoría** – Cada despliegue queda capturado en el historial de Git, proporcionando un registro de auditoría inmutable.
- **Gestión Multi‑Clúster** – Una sola instancia de ArgoCD puede gestionar aplicaciones en cientos de clústeres de Kubernetes.
- **Agnóstico de Gestión de Configuración** – Funciona con YAML plano, Helm, Kustomize, Jsonnet y más.

## Instalación

ArgoCD puede instalarse en cualquier clúster de Kubernetes en minutos.

### 1. Crear el namespace y aplicar el manifiesto

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. Acceder al servidor API (port‑forward)

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Ahora puedes acceder a la interfaz web en `https://localhost:8080`.

### 3. Obtener la contraseña de administrador inicial

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

### 4. Iniciar sesión usando la CLI

```bash
argocd login localhost:8080
```

Usa el usuario `admin` y la contraseña del paso anterior.

## Uso Básico

### Conectar un Repositorio Git

```bash
argocd repo add https://github.com/my-org/my-app.git
```

### Registrar un Clúster de Destino

Si el destino no es el mismo clúster donde se ejecuta ArgoCD, regístralo:

```bash
argocd cluster add <kube-context-name>
```

### Definir una Aplicación (YAML Declarativo)

Crea un archivo `nginx-app.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: nginx-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/my-org/nginx.git'
    path: production
    targetRevision: HEAD
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

Aplicarlo:

```bash
kubectl apply -f nginx-app.yaml
```

### Sincronizar una Aplicación

Sincronización manual (o la política de sincronización automatizada se encargará):

```bash
argocd app sync nginx-prod
```

Una sincronización también puede activarse desde la interfaz web o mediante webhook desde tu proveedor Git.

## Características Principales y Comandos

### Sincronización Automatizada y Autocuración

- **Auto‑Sync** – ArgoCD puede iniciar automáticamente una sincronización cada vez que se envía un nuevo commit a la rama rastreada.
- **Self‑Heal** – Si alguien modifica manualmente recursos en el clúster, ArgoCD los revierte al estado definido en Git.

Configurar en el YAML bajo `syncPolicy.automated` o mediante CLI:

```bash
argocd app set nginx-prod --sync-policy automated --auto-prune --self-heal
```

### Gestión Multi‑Clúster

Usa una instancia de ArgoCD para desplegar en muchos clústeres con diferentes namespaces. Listar clústeres:

```bash
argocd cluster list
```

### Application Sets (CRD)

Generación dinámica de Aplicaciones basada en parámetros (p. ej., para cada clúster, para cada rama, o desde una lista de generadores). Ejemplo usando un generador Git:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: my-apps
spec:
  generators:
  - git:
      repoURL: 'https://github.com/my-org/deploy-config.git'
      revision: HEAD
      files:
        - path: "clusters/*/config.json"
  template:
    metadata:
      name: '{{ cluster }}-my-app'
    spec:
      project: default
      source:
        repoURL: 'https://github.com/my-org/my-app.git'
        targetRevision: HEAD
        path: '{{ env }}'
      destination:
        server: '{{ server }}'
        namespace: '{{ namespace }}'
```

### Herramientas de Administración de Configuración

ArgoCD renderiza nativamente manifiestos desde:

- **Helm** – Usa `helm.parameters` o `helm.valueFiles`
- **Kustomize** – Simplemente apunta al directorio de overlay de Kustomize
- **Jsonnet** – Mediante un archivo `jsonnet.libsonnet`

### Sync Waves & Hooks

Controla el orden de despliegue de recursos:

- **Sync Waves** – Establece la anotación `argocd.argoproj.io/sync-wave` con un entero (los números más bajos se despliegan primero).
- **Sync Hooks** – Ejecuta jobs (pre‑sync, sync, post‑sync, etc.) para migraciones de base de datos o validación.

### Notificaciones y Webhooks

- **Notificaciones Integradas** – Envía alertas a Slack, correo electrónico o endpoints personalizados cuando cambia el estado de sincronización.
- **Disparadores Webhook** – Integra con GitHub/GitLab/Bitbucket para sincronización casi instantánea al hacer push.

### Image Updater (Componente Opcional)

Actualiza automáticamente la etiqueta de imagen de contenedor en Git cuando se envía una nueva imagen a un registro. Este componente (Argo CD Image Updater) vigila tu registro de contenedores y envía el commit con la nueva etiqueta a la fuente Git.

## Arquitectura – Componentes de Alto Nivel

- **API Server** – Expone la API, la interfaz web y los endpoints CLI; maneja autenticación, RBAC y gestión de proyectos.
- **Repository Server** – Almacena en caché los repositorios Git y genera manifiestos de Kubernetes (por ejemplo, renderiza charts de Helm, overlays de Kustomize).
- **Application Controller** – Monitorea continuamente el estado activo de las aplicaciones y lo compara con el estado deseado del servidor de repositorios; desencadena operaciones de sincronización, poda y autocuración.

## Resumen

ArgoCD convierte los despliegues de Kubernetes en un flujo de trabajo totalmente automatizado e impulsado por Git. Al hacer de Git la fuente de verdad, elimina la desviación de configuración, proporciona un registro de auditoría inmutable y permite una infraestructura autocurable. Con soporte integrado para Helm, Kustomize, gestión multi‑clúster y Application Sets dinámicos, es el estándar de facto para GitOps en Kubernetes.

Para documentación oficial, visita [argoproj.github.io/argo-cd](https://argoproj.github.io/argo-cd/).