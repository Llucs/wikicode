---
title: Docker - Herramienta de Contenerización
description: Docker es una plataforma para desarrollar, empaquetar y desplegar aplicaciones en contenedores.
created: 2026-06-13
tags:
  - containerization
  - development
  - deployment
status: draft
ecosystem: containers
---

## ¿Qué es Docker?

Docker es una plataforma que permite a los desarrolladores empaquetar su aplicación junto con todas sus dependencias en una unidad estandarizada llamada contenedor. Los contenedores permiten que las aplicaciones se desplieguen de manera rápida y consistente en diferentes entornos, como desarrollo, pruebas, staging y producción.

## ¿Por qué usar Docker?

1. **Portabilidad**: Los contenedores de Docker son ligeros y portátiles, lo que facilita el despliegue de aplicaciones en cualquier entorno.
2. **Aislamiento**: Cada contenedor se ejecuta en su propio entorno aislado, asegurando que la aplicación no se vea afectada por otros procesos en ejecución.
3. **Consistencia**: Los contenedores aseguran un entorno de desarrollo consistente a lo largo de las diferentes etapas del ciclo de vida de una aplicación.

## Instalación

Docker se puede instalar en varios sistemas operativos incluyendo Windows, macOS y Linux. El proceso de instalación varía según el OS:

### Para Ubuntu (Linux):
```sh
# Update package lists
sudo apt-get update

# Install Docker Engine
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### Para Windows:
1. Descargue Docker Desktop desde el sitio web oficial.
2. Siga las instrucciones de instalación proporcionadas por el instalador.

### Para macOS:
```sh
# Download and run the Docker Quickstart Terminal
curl -fsSL https://download.docker.com/mac/stable/Docker.dmg | sudo hdiutil attach -mountpoint /Volumes/docker -noverify -nobrowse /dev/rdiski
cd /Volumes/docker/Docker.app/Contents/Resources/etc/docker.conf.d/
sudo curl -L https://github.com/moby/buildkit/releases/download/v0.14.2/bazelisk_v1.37.2_Linux_x86_64.tar.gz | sudo tar -C . -xzvf -
```

## Uso Básico

### Descargar una Imagen
```sh
# Pull the official Nginx image from Docker Hub
docker pull nginx
```

### Ejecutar un Contenedor
```sh
# Run a container using the pulled Nginx image
docker run -d --name my-nginx nginx
```

### Listar Contenedores
```sh
# List all running containers
docker ps

# List all stopped containers
docker ps -a
```

## Características Principales

1. **Imágenes**: Las imágenes de Docker son los bloques de construcción de un contenedor, contienen todo lo necesario para ejecutar una aplicación.
2. **Volúmenes**: Almacenamiento persistente para datos dentro de un contenedor.
3. **Redes**: Permite que los contenedores se comuniquen entre sí y con servicios fuera de su red.
4. **Swarm Mode**: Habilita la agrupación y orquestación de múltiples hosts Docker.

## Conclusión

Docker simplifica el proceso de construir, enviar y ejecutar aplicaciones al proporcionar un entorno aislado para tu código. Esto facilita la gestión de dependencias y asegura entornos consistentes a lo largo de las diferentes etapas de desarrollo y despliegue.