---
title: Docker - Containerisierungstool
description: Docker ist eine Plattform zum Entwickeln, Verpacken und Bereitstellen von Anwendungen in Containern.
created: 2026-06-13
tags:
  - containerization
  - development
  - deployment
status: draft
ecosystem: containers
---

## Was ist Docker?

Docker ist eine Plattform, die es Entwicklern ermöglicht, ihre Anwendung zusammen mit all ihren Abhängigkeiten zu einer standardisierten Einheit, einem sogenannten Container, zu bündeln. Container ermöglichen es, Anwendungen schnell und konsistent über verschiedene Umgebungen wie Entwicklung, Test, Staging und Produktion hinweg bereitzustellen.

## Warum Docker verwenden?

1. **Portabilität**: Docker-Container sind leicht und portabel, was es einfach macht, Anwendungen in jeder Umgebung bereitzustellen.
2. **Isolation**: Jeder Container läuft in seiner eigenen isolierten Umgebung, sodass die Anwendung nicht von anderen laufenden Prozessen beeinflusst wird.
3. **Konsistenz**: Container gewährleisten eine konsistente Entwicklungsumgebung über verschiedene Phasen des Lebenszyklus einer Anwendung.

## Installation

Docker kann auf verschiedenen Betriebssystemen installiert werden, darunter Windows, macOS und Linux. Der Installationsprozess variiert je nach Betriebssystem:

### Für Ubuntu (Linux):
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

### Für Windows:
1. Laden Sie Docker Desktop von der offiziellen Website herunter.
2. Folgen Sie den vom Installationsprogramm bereitgestellten Installationsanweisungen.

### Für macOS:
```sh
# Download and run the Docker Quickstart Terminal
curl -fsSL https://download.docker.com/mac/stable/Docker.dmg | sudo hdiutil attach -mountpoint /Volumes/docker -noverify -nobrowse /dev/rdiski
cd /Volumes/docker/Docker.app/Contents/Resources/etc/docker.conf.d/
sudo curl -L https://github.com/moby/buildkit/releases/download/v0.14.2/bazelisk_v1.37.2_Linux_x86_64.tar.gz | sudo tar -C . -xzvf -
```

## Grundlegende Verwendung

### Ein Image pullen
```sh
# Pull the official Nginx image from Docker Hub
docker pull nginx
```

### Einen Container ausführen
```sh
# Run a container using the pulled Nginx image
docker run -d --name my-nginx nginx
```

### Container auflisten
```sh
# List all running containers
docker ps

# List all stopped containers
docker ps -a
```

## Hauptmerkmale

1. **Images**: Docker-Images sind die Bausteine eines Containers und enthalten alles, was für den Betrieb einer Anwendung benötigt wird.
2. **Volumes**: Permanenter Speicher für Daten innerhalb eines Containers.
3. **Netzwerk**: Ermöglicht die Kommunikation von Containern untereinander und mit Diensten außerhalb ihres Netzwerks.
4. **Swarm-Modus**: Ermöglicht das Clustering und die Orchestrierung mehrerer Docker-Hosts.

## Fazit

Docker vereinfacht den Prozess des Erstellens, Auslieferns und Ausführens von Anwendungen, indem es eine isolierte Umgebung für Ihren Code bereitstellt. Dadurch wird es einfacher, Abhängigkeiten zu verwalten und konsistente Umgebungen über verschiedene Entwicklungs- und Bereitstellungsphasen hinweg sicherzustellen.