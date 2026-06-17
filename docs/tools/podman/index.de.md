---
title: Podman - Daemonloses Container-Management
description: Ein umfassender Leitfaden für Podman, die daemonlose Container-Engine zur Verwaltung von Containern, Pods und Images.
created: 2026-06-15
tags:
  - containers
  - podman
  - docker-alternative
  - devops
  - linux
status: draft
ecosystem: containers
---

# Podman - Daemonloses Container-Management

Podman ist eine quelloffene, daemonlose Container-Engine, die von Red Hat entwickelt wird. Sie bietet eine vollständig kompatible Befehlszeilenschnittstelle zu Docker und bietet einzigartige Funktionen wie native Pod-Unterstützung, rootless Betrieb und nahtlose systemd-Integration. Podman hält sich an die OCI (Open Container Initiative)-Standards und ist eine Schlüsselkomponente der Red Hat Container-Toolchain neben Buildah und Skopeo.

## Was ist Podman?

Podman (kurz für **Pod Manager**) ist ein Werkzeug zur Verwaltung von OCI-Containern, Images, Volumes und Pods. Im Gegensatz zu Docker verlässt sich Podman **nicht** auf einen zentralen Hintergrund-Daemon (`dockerd`). Stattdessen laufen Container als direkte Kindprozesse des Podman-Befehls, was die Verwaltung mit standardmäßigen Linux-Prozesswerkzeugen und systemd erleichtert.

## Warum Podman?

- **Daemonlose Architektur** – Kein permanenter Daemon bedeutet geringere Ressourcennutzung, einfachere Fehlersuche und einfachere Integration mit Init-Systemen.
- **Standardmäßig rootless** – Podman kann Container ohne Root-Rechte mithilfe von Benutzer-Namespaces ausführen, was die Angriffsfläche drastisch reduziert.
- **Pod-Unterstützung** – Die integrierte Unterstützung für Pods (Gruppen von Containern, die Namespaces teilen) spiegelt Kubernetes-Konzepte wider und ermöglicht die lokale Entwicklung von Pod-Manifesten.
- **Docker-Kompatibilität** – Befehle wie `podman run`, `podman build` und `podman ps` bilden direkt Docker-Äquivalente ab; ein Alias `alias docker=podman` funktioniert nahtlos für die meisten Arbeitsabläufe.
- **Systemd-Integration** – Erzeugen Sie systemd-Unit-Dateien für jeden Container, die automatischen Start, Neustart bei Fehlern und Integration mit moderner Linux-Diensteverwaltung ermöglichen.
- **Open Source & Community** – Eigentum von Red Hat und Teil des CNCF-Ökosystems mit einer starken Community und Unternehmensunterstützung.

## Installation

Podman ist auf allen wichtigen Betriebssystemen verfügbar. Der einfachste Einstieg hängt von Ihrer Plattform ab.

### Linux

**Fedora / RHEL / CentOS**
```bash
sudo dnf install podman
```

**Debian / Ubuntu**
```bash
sudo apt-get update && sudo apt-get install podman
```

**Arch Linux**
```bash
sudo pacman -S podman
```

### macOS

Verwendung von [Homebrew](https://brew.sh/):
```bash
brew install podman
podman machine init       # Create a Linux VM
podman machine start      # Start the VM
```

### Windows

Verwendung von [Winget](https://learn.microsoft.com/en-us/windows/package-manager/):
```bash
winget install RedHat.Podman
```
Oder laden Sie das Installationsprogramm von der [Podman releases page](https://github.com/containers/podman/releases) herunter.

Nach der Installation führen Sie `podman machine init` und `podman machine start` aus, um die verwaltete VM einzurichten (erforderlich auf macOS und Windows).

## Hauptfunktionen

### Daemonlose und rootless Container

Podman macht einen zentralen Daemon überflüssig. Jeder Aufruf von `podman run` oder `podman exec` startet den Containerprozess direkt unter der UID des aufrufenden Benutzers. Der rootless-Modus ist die Standardeinstellung; der Podman-Benutzer-Namespace bildet den unprivilegierten Host-Benutzer auf root im Container ab. Die Sicherheit wird durch SELinux- und seccomp-Richtlinien weiter verbessert.

### Pods (Natives Kubernetes-ähnliches Gruppieren)

Ein Pod ist eine Sammlung von Containern, die denselben Netzwerk-Namespace, dieselbe IP-Adresse und denselben Portbereich teilen. Pods erleichtern die Modellierung von Multi-Container-Anwendungen, die gemeinsam bereitgestellt werden sollen.

```bash
# Create a pod with an exposed port
podman pod create --name mypod -p 8080:80

# Run an nginx container inside the pod
podman run --pod mypod -d --name web nginx:alpine

# Run a helper container (e.g., sidecar) in the same pod
podman run --pod mypod -d --name logger busybox tail -f /dev/null

# List pods
podman pod ps
```

### Systemd-Integration

Container können als native systemd-Dienste verwaltet werden, was automatischen Neustart beim Hochfahren oder bei Fehlern gewährleistet.

```bash
# Run a container in the background
podman run -d --name myapp my-image

# Generate systemd unit files
podman generate systemd --new --files --name myapp

# Copy the generated file to the systemd directory and enable it
sudo cp container-myapp.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now container-myapp.service
```

### Docker-Kompatibilität & `podman-compose`

Podman akzeptiert die meisten Docker-Befehle direkt. Für Docker-Compose-Dateien können Sie `podman compose` verwenden (erfordert `podman-compose` oder das separat installierte Docker-Compose-Plugin).

```yaml
# Example docker-compose.yml works with podman-compose
version: '3'
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
```

Ausführen mit:
```bash
podman-compose up -d
```

### Images mit Buildah erstellen

Obwohl `podman build` verfügbar ist, bietet das spezielle Buildah-Tool eine feinere Kontrolle über das Image-Building, einschließlich der Möglichkeit, Images ohne eine Container-Laufzeitumgebung zu erstellen.

```bash
podman build -t my-app .
```

## Grundlegende Verwendung

Die folgenden Befehle spiegeln die Syntax von Docker wider und sind sowohl für Podman- als auch für Docker-Umgebungen sicher zu erlernen.

```bash
# Pull an image
podman pull docker.io/library/alpine:latest

# List images
podman images

# Run a container in the foreground, interactive shell
podman run -it --rm alpine /bin/sh

# Run a detached web server
podman run -d --name web -p 8080:80 nginx:alpine

# List running containers
podman ps

# List all containers (including stopped)
podman ps -a

# Execute a command inside a running container
podman exec -it web /bin/sh

# View logs
podman logs web

# Stop and remove a container
podman stop web && podman rm web

# Remove all unused images
podman image prune -a
```

## Migration von Docker

Für diejenigen, die derzeit Docker verwenden, ist der Übergang einfach:

- **Alias für die Befehlszeile**: `alias docker=podman` (zu Ihrem Shell-Profil hinzufügen).
- **Docker Compose**: Installieren Sie `podman-compose` oder verwenden Sie das Docker-Compose-Plugin mit Podmans Socket-Aktivierung (`podman system service`).
- **Volumes und Netzwerke**: Podman unterstützt Docker-ähnliche Volumes und CNI/Netavark-Netzwerke.
- **Dockerfiles**: `podman build` funktioniert mit jedem standardmäßigen Dockerfile.

> ⚠️ *Hinweis*: Einige Docker-spezifische Funktionen (wie Swarm-Modus und Docker-Kontexte) sind in Podman nicht implementiert. Für Swarm ziehen Sie Alternativen wie Nomad oder Kubernetes in Betracht.

## Zusätzliche Ressourcen

- [Offizielle Podman-Dokumentation](https://docs.podman.io/)
- [Podman GitHub-Repository](https://github.com/containers/podman)
- [Red Hat Container-Tools](https://www.redhat.com/en/topics/containers)
- [Rootless Container mit Podman](https://rootlesscontaine.rs/getting-started/podman/)
- [Podman vs Docker: Ein umfassender Vergleich](https://developers.redhat.com/articles/2023/08/29/why-podman-replaces-docker)

---

Podman ist eine moderne, sichere und flexible Container-Engine, die sich sowohl in Entwicklungs- als auch in Produktionsworkflows gut einfügt. Seine daemonlose Architektur und tiefe Integration mit systemd machen es zu einer ausgezeichneten Wahl für Linux-zentrierte Umgebungen, während seine Docker-kompatible API eine sanfte Lernkurve für bestehende Benutzer gewährleistet. Ob Sie einen einzelnen Container auf einem Laptop ausführen oder eine Flotte von Pods in einer CI-Pipeline orchestrieren, Podman bietet die benötigten Werkzeuge ohne den Overhead eines zentralen Daemon.