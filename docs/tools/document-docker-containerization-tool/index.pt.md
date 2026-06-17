---
title: Docker - Ferramenta de Containerização
description: Docker é uma plataforma para desenvolver, empacotar e implantar aplicações em contêineres.
created: 2026-06-13
tags:
  - containerization
  - development
  - deployment
status: draft
ecosystem: containers
---

## O que é Docker?

Docker é uma plataforma que permite aos desenvolvedores empacotar suas aplicações junto com todas as suas dependências em uma unidade padronizada chamada contêiner. Os contêineres permitem que as aplicações sejam implantadas de forma rápida e consistente em diferentes ambientes, como desenvolvimento, teste, homologação e produção.

## Por que usar Docker?

1. **Portabilidade**: Os contêineres Docker são leves e portáteis, facilitando a implantação de aplicações em qualquer ambiente.
2. **Isolamento**: Cada contêiner é executado em seu próprio ambiente isolado, garantindo que a aplicação não seja afetada por outros processos em execução.
3. **Consistência**: Os contêineres garantem um ambiente de desenvolvimento consistente em diferentes estágios do ciclo de vida de uma aplicação.

## Instalação

O Docker pode ser instalado em vários sistemas operacionais, incluindo Windows, macOS e Linux. O processo de instalação varia de acordo com o SO:

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
1. Baixe o Docker Desktop do site oficial.
2. Siga as instruções de instalação fornecidas pelo instalador.

### Para macOS:
```sh
# Download and run the Docker Quickstart Terminal
curl -fsSL https://download.docker.com/mac/stable/Docker.dmg | sudo hdiutil attach -mountpoint /Volumes/docker -noverify -nobrowse /dev/rdiski
cd /Volumes/docker/Docker.app/Contents/Resources/etc/docker.conf.d/
sudo curl -L https://github.com/moby/buildkit/releases/download/v0.14.2/bazelisk_v1.37.2_Linux_x86_64.tar.gz | sudo tar -C . -xzvf -
```

## Uso Básico

### Baixando uma Imagem
```sh
# Pull the official Nginx image from Docker Hub
docker pull nginx
```

### Executando um Contêiner
```sh
# Run a container using the pulled Nginx image
docker run -d --name my-nginx nginx
```

### Listando Contêineres
```sh
# List all running containers
docker ps

# List all stopped containers
docker ps -a
```

## Recursos Principais

1. **Imagens**: As imagens Docker são os blocos de construção de um contêiner, contendo tudo o que é necessário para executar uma aplicação.
2. **Volumes**: Armazenamento persistente para dados dentro de um contêiner.
3. **Networking**: Permite que os contêineres se comuniquem entre si e com serviços fora de sua rede.
4. **Swarm Mode**: Permite o agrupamento e orquestração de múltiplos hosts Docker.

## Conclusão

O Docker simplifica o processo de construir, enviar e executar aplicações, fornecendo um ambiente isolado para o seu código. Isso facilita o gerenciamento de dependências e garante ambientes consistentes em diferentes estágios de desenvolvimento e implantação.