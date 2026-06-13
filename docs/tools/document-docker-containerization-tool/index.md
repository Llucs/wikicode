---
title: Docker - Containerization Tool
description: Docker is a platform for developing, packaging, and deploying applications in containers.
created: 2026-06-13
tags:
  - containerization
  - development
  - deployment
status: draft
---

## What is Docker?

Docker is a platform that allows developers to package their application along with all its dependencies into a standardized unit called a container. Containers enable applications to be deployed quickly and consistently across different environments, such as development, testing, staging, and production.

## Why Use Docker?

1. **Portability**: Docker containers are lightweight and portable, making it easy to deploy applications in any environment.
2. **Isolation**: Each container runs in its own isolated environment, ensuring that the application is not affected by other running processes.
3. **Consistency**: Containers ensure a consistent development environment across different stages of an application's lifecycle.

## Installation

Docker can be installed on various operating systems including Windows, macOS, and Linux. The installation process varies based on the OS:

### For Ubuntu (Linux):
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

### For Windows:
1. Download the Docker Desktop from the official website.
2. Follow the installation instructions provided by the installer.

### For macOS:
```sh
# Download and run the Docker Quickstart Terminal
curl -fsSL https://download.docker.com/mac/stable/Docker.dmg | sudo hdiutil attach -mountpoint /Volumes/docker -noverify -nobrowse /dev/rdiski
cd /Volumes/docker/Docker.app/Contents/Resources/etc/docker.conf.d/
sudo curl -L https://github.com/moby/buildkit/releases/download/v0.14.2/bazelisk_v1.37.2_Linux_x86_64.tar.gz | sudo tar -C . -xzvf -
```

## Basic Usage

### Pulling an Image
```sh
# Pull the official Nginx image from Docker Hub
docker pull nginx
```

### Running a Container
```sh
# Run a container using the pulled Nginx image
docker run -d --name my-nginx nginx
```

### Listing Containers
```sh
# List all running containers
docker ps

# List all stopped containers
docker ps -a
```

## Key Features

1. **Images**: Docker images are the building blocks of a container, containing everything needed to run an application.
2. **Volumes**: Persistent storage for data within a container.
3. **Networking**: Allows containers to communicate with each other and with services outside their network.
4. **Swarm Mode**: Enables clustering and orchestration of multiple Docker hosts.

## Conclusion

Docker simplifies the process of building, shipping, and running applications by providing an isolated environment for your code. This makes it easier to manage dependencies and ensure consistent environments across different stages of development and deployment.