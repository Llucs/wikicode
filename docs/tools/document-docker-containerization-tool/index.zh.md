---
title: Docker - 容器化工具
description: Docker是一个用于在容器中开发、打包和部署应用的平台。
created: 2026-06-13
tags:
  - containerization
  - development
  - deployment
status: draft
ecosystem: containers
---

## 什么是Docker？

Docker是一个平台，允许开发人员将他们的应用以及所有依赖项打包成一个标准化单元，称为容器。容器能够使应用程序快速且一致地部署到不同的环境中，如开发、测试、预发布和生产。

## 为什么使用Docker？

1. **可移植性**：Docker容器轻量级且可移植，使得应用可以轻松部署到任何环境。
2. **隔离性**：每个容器在其自己的隔离环境中运行，确保应用不受其他运行进程的影响。
3. **一致性**：容器确保应用生命周期不同阶段的环境一致。

## 安装

Docker可以安装在各种操作系统上，包括Windows、macOS和Linux。安装过程因操作系统而异：

### 对于Ubuntu（Linux）：
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

### 对于Windows：
1. 从官方网站下载Docker Desktop。
2. 按照安装程序提供的安装说明进行操作。

### 对于macOS：
```sh
# Download and run the Docker Quickstart Terminal
curl -fsSL https://download.docker.com/mac/stable/Docker.dmg | sudo hdiutil attach -mountpoint /Volumes/docker -noverify -nobrowse /dev/rdiski
cd /Volumes/docker/Docker.app/Contents/Resources/etc/docker.conf.d/
sudo curl -L https://github.com/moby/buildkit/releases/download/v0.14.2/bazelisk_v1.37.2_Linux_x86_64.tar.gz | sudo tar -C . -xzvf -
```

## 基本用法

### 拉取镜像
```sh
# Pull the official Nginx image from Docker Hub
docker pull nginx
```

### 运行容器
```sh
# Run a container using the pulled Nginx image
docker run -d --name my-nginx nginx
```

### 列出容器
```sh
# List all running containers
docker ps

# List all stopped containers
docker ps -a
```

## 关键特性

1. **镜像（Images）**：Docker镜像是容器的构建块，包含运行应用程序所需的一切。
2. **卷（Volumes）**：容器内数据的持久化存储。
3. **网络（Networking）**：允许容器之间以及与其网络外部的服务进行通信。
4. **Swarm模式**：支持多台Docker主机的集群和编排。

## 结论

Docker通过为代码提供隔离环境，简化了构建、分发和运行应用的过程。这使得管理依赖和确保在开发与部署的不同阶段有一致的环境变得更加容易。