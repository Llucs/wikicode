---
title: Portainer
description: Ein selbst gehostetes Verwaltungstool für Container und Orchestrierung, das Governance, RBAC/SSO und betriebliche Steuerung über mehrere Umgebungen hinweg zentralisiert.
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

## Übersicht

Portainer ist der Branchenstandard, eine quelloffene „Single Pane of Glass“ für die Verwaltung containerisierter Umgebungen. Entwickelt von Neil Cresswell und 2017 von DockerUI abgespalten, zielt Portainer darauf ab, die steile Lernkurve und den betrieblichen Aufwand von Docker, Docker Swarm, Kubernetes, Azure ACI und Hashicorp Nomad zu beseitigen. Es läuft selbst als leichtgewichtiger Container (oder über ein Helm-Chart) und bietet eine leistungsstarke Weboberfläche, die von einer vollwertigen REST-API unterstützt wird.

Portainer wird unter der AGPLv3 für die Community Edition (CE) lizenziert, mit einer kommerziellen Business Edition (BE), die Unternehmensfunktionen wie FIPS-Konformität, granulare RBAC und dedizierten Support hinzufügt.

## Warum Portainer?

- **Einheitliche Steuerungsebene:** Verwalten Sie jede Container-Engine in Ihrem Bestand über eine einzige Weboberfläche, anstatt zwischen verschiedenen CLIs zu wechseln.
- **Reduzierte Komplexität:** Nicht spezialisierte Teams können Anwendungen bereitstellen und verwalten, ohne komplizierte `kubectl`- oder `docker-compose`-Befehle lernen zu müssen.
- **GitOps-Bereit:** Stacks können direkt mit Git-Repositories verknüpft werden. Jeder Push in das Repository löst eine automatische Neuerstellung aus.
- **Edge Computing:** Verwalten Sie sicher Tausende von Geräten hinter NAT oder Firewalls mit Edge Agents.
- **Leichtgewichtig & nicht intrusiv:** Portainer ersetzt nicht Ihren vorhandenen Orchestrator; es arbeitet neben ihm, indem es die Docker-/Kubernetes-API über einen Socket oder einen dedizierten Agent-Container abfragt.

## Architektur

Portainer verwendet ein Standard-Server-Agent-Modell:

1.  **Portainer Server (portainer/portainer-ce):** Die Hauptanwendung. Sie stellt die Weboberfläche und die REST-API bereit. Dies ist der Knoten, den Sie in Ihrem Browser aufrufen.
2.  **Portainer Agent (portainer/agent):** Ein leichtgewichtiger Sidecar-Container, der auf jedem Docker-Host oder Kubernetes-Knoten bereitgestellt wird, den Sie remote verwalten möchten. Der Agent kommuniziert mit dem lokalen Docker-Socket und stellt eine gesicherte API auf Port 9001 bereit.
3.  **Edge Agent:** Eine Variante des Standard-Agents, die für entfernte Standorte entwickelt wurde. Sie initiiert einen *ausgehenden* Tunnel zum Portainer Server, wodurch die Verwaltung durch strenge Firewalls hindurch möglich ist, ohne eingehende Ports öffnen zu müssen.

```text
[Admin Browser] <--> [Portainer Server :9443]
                         |
            +------------+-------------+
            |            |             |
    [Docker Agent 1] [Docker Agent 2] [K8s Cluster (Helm)]
            |            |
    [Docker Daemon] [Docker Daemon]
```

## Installation

### Docker Standalone (Schnellstart)

Dies ist die gebräuchlichste Methode, um einen lokalen oder eine kleine Anzahl von Docker-Hosts zu verwalten.

```bash
# Erstellen Sie ein persistentes Volume für Portainer-Daten
docker volume create portainer_data

# Starten Sie den Portainer-Server-Container
docker run -d -p 8000:8000 -p 9443:9443 --name portainer \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v portainer_data:/data \
    portainer/portainer-ce:lts
```

- `-p 9443:9443`: Weboberfläche und API (HTTPS).
- `-p 8000:8000`: (Optional) TCP-Tunnel für Edge-Agent-Verbindungen.
- `-v /var/run/docker.sock`: Erlaubt Portainer, den Host zu verwalten, auf dem es läuft.
- `:lts`: Der Long-Term-Support-Tag. **Verwenden Sie in der Produktion immer `:lts`.**

### Docker Swarm

Stellen Sie Portainer als globalen Dienst in Ihrem Swarm-Cluster bereit.

```bash
curl -L https://downloads.portainer.io/ce2-19/portainer-agent-stack.yml -o portainer-agent-stack.yml

docker stack deploy -c portainer-agent-stack.yml portainer
```

### Kubernetes (Helm)

Stellen Sie Portainer mit der offiziellen Helm-Chart in Ihrem Kubernetes-Cluster bereit.

```bash
helm repo add portainer https://portainer.github.io/k8s/
helm repo update

helm upgrade --install portainer portainer/portainer \
    --namespace portainer --create-namespace \
    --set service.type=LoadBalancer \
    --set service.httpPort=9000 \
    --set service.httpsPort=9443
```

### Air-Gapped-Installation

Für Umgebungen ohne Internetzugang ziehen Sie die Images vorab.

```bash
# Auf einem Rechner mit Internetzugang
docker pull portainer/portainer-ce:lts
docker pull portainer/agent:lts

# Taggen und in Ihre interne Registry pushen
docker tag portainer/portainer-ce:lts <internal-registry>/portainer-ce:lts
docker tag portainer/agent:lts <internal-registry>/agent:lts
docker push <internal-registry>/portainer-ce:lts
docker push <internal-registry>/agent:lts
```

## Ersteinrichtung

1.  Öffnen Sie einen Browser mit `https://<SERVER_IP>:9443`.
2.  Erstellen Sie ein sicheres Passwort für den Benutzer `admin`.
3.  Der Schnellstart-Assistent wird angezeigt. Wählen Sie **Docker** und dann **Socket**, um eine Verbindung zum lokalen Docker-Daemon herzustellen.
4.  Klicken Sie auf **Verbinden**. Sie befinden sich nun auf der **Startseite** – dies ist Ihre Umgebungsauswahl.

## Hauptfunktionen & Befehlsbeispiele

### 1. Multi-Umgebungs-Management

Verbinden Sie entfernte Docker-Hosts, indem Sie den Portainer-Agent bereitstellen.

**Auf dem entfernten Host (Ziel):**
```bash
docker run -d -p 9001:9001 --name portainer_agent \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /var/lib/docker/volumes:/var/lib/docker/volumes \
    portainer/agent:lts
```

**In der Portainer-Server-UI:**
Navigieren Sie zu **Umgebungen** > **Umgebung hinzufügen** > **Docker-Agent**.
Geben Sie die IP des entfernten Hosts und den Port (9001) ein. Klicken Sie auf **Verbinden**.

### 2. App-Vorlagen (Ein-Klick-Bereitstellung)

Portainer enthält einen Katalog vordefinierter Anwendungen (Nginx, MySQL, WordPress, etc.).

**Workflow:**
1. Seitenleiste > **App-Vorlagen**.
2. Klicken Sie auf eine Vorlage (z.B. **Nginx**).
3. Passen Sie Name, Ports und Umgebungsvariablen an.
4. Klicken Sie auf **Stack bereitstellen**.

### 3. Stacks & GitOps

Stellen Sie komplexe Anwendungen mit Docker Compose oder Kubernetes-Manifestdateien bereit. Stacks können für GitOps-Workflows mit einem Git-Repository verknüpft werden.

**Manuelles Compose-Deployment:**
Fügen Sie dies unter **Stacks** > **Stack hinzufügen** > **Web-Editor** ein:
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

**GitOps-Einrichtung:**
1. **Stacks** > **Stack hinzufügen** > **Repository**.
2. Geben Sie die Git-Repository-URL und den Pfad zur Compose-Datei ein.
3. Aktivieren Sie **Automatische Updates**.
4. Klicken Sie auf **Stack bereitstellen**. Jeder `git push` löst eine erneute Bereitstellung aus.

### 4. Kubernetes-Management

Portainer abstrahiert die Komplexität von `kubectl`. Sie können Namespaces, Deployments, Services und Ingresses über ein Formular oder YAML erstellen.

**Beispiel:** Bereitstellen einer einfachen Nginx-Workload.
1. **Umgebungen** > Wählen Sie Ihren **Kubernetes-Cluster** aus.
2. **Kubernetes** > **Workloads** > **Workload hinzufügen**.
3. Füllen Sie das Formular aus (Name: `nginx`, Image: `nginx:alpine`, Port: `80`).
4. Klicken Sie auf **Bereitstellen**.

### 5. Registries

Verwalten Sie zentral Anmeldedaten für Docker Hub, GitLab, Quay, Amazon ECR und Google Container Registry.

1. **Registries** > **Registry hinzufügen**.
2. Wählen Sie Ihren Anbieter (z.B. **Docker Hub**).
3. Geben Sie Ihre Anmeldedaten ein (Benutzername/Zugriffstoken).

### 6. Edge Computing

Verwalten Sie entfernte Geräte (IoT, Einzelhandel, Außenstellen) hinter NAT/Firewalls. Der Server generiert eine `EDGE_ID` und einen `EDGE_KEY`.

**Auf dem Edge-Gerät:**
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

### 7. REST-API

Portainer verfügt über eine umfangreiche REST-API. Generieren Sie einen API-Schlüssel unter **Einstellungen** > **Sicherheit**.

```bash
# Alle Umgebungen auflisten
curl -X GET 'https://<SERVER_IP>:9443/api/endpoints' \
    -H 'X-API-Key: ptr_xxxxxxxxxxxx' | jq .

# Einen Stack bereitstellen
curl -X POST 'https://<SERVER_IP>:9443/api/stacks' \
    -H 'X-API-Key: ptr_xxxxxxxxxxxx' \
    -H 'Content-Type: application/json' \
    -d '{
      "Name": "my-api-stack",
      "StackFileContent": "version: \"3.8\"\nservices:\n  web:\n    image: nginx:alpine",
      "SwarmID": "",
      "EndpointID": 1
    }'
```

## Editionsvergleich

| Feature | Community Edition (CE) | Business Edition (BE) |
|---|---|---|
| Lizenz | AGPLv3 | Kommerziell |
| Multi-Umgebungen | Unbegrenzt | Unbegrenzt |
| GitOps | Ja | Ja |
| Edge Computing | Eingeschränkt | Vollständig (Edge-Gruppen, Stacks, Jobs) |
| RBAC / SSO | Basis | Erweitert (AD/LDAP/OAuth, Teamrollen, Ressourcenkontrollen) |
| Registry-Verwaltung | Manuell | Zentral mit Governance |
| Support | Community | Kommerziell (24/7/365) |
| FIPS-Konformität | Nein | Ja |

## Best Practices

1.  **Verwenden Sie `:lts`-Releases.** Verwenden Sie in der Produktion nicht den Tag `:latest`; er entspricht den aktuellsten, möglicherweise instabilen Builds.
2.  **Widmen Sie den Serverknoten vollständig.** Führen Sie nicht Dutzende von Workloads auf dem Portainer-Server-Container aus. Nutzen Sie ihn ausschließlich als Verwaltungspunkt.
3.  **Sichern Sie `portainer_data` regelmäßig.** Führen Sie diesen Befehl aus, um das Volume zu sichern:
    ```bash
    docker run --rm -v portainer_data:/data -v $(pwd):/backup alpine tar cvf /backup/portainer_backup.tar /data
    ```
4.  **Sichern Sie mit geeignetem TLS.** Ersetzen Sie das selbstsignierte Zertifikat in der Produktion.
    ```bash
    docker run -d -p 9443:9443 --name portainer \
        -v /path/to/fullchain.pem:/certs/portainer.crt \
        -v /path/to/privkey.pem:/certs/portainer.key \
        -v portainer_data:/data \
        portainer/portainer-ce:lts
    ```

## Fehlerbehebung

### Agent-Verbindungsfehler
- Stellen Sie sicher, dass Port `9001` auf dem Zielrechner geöffnet ist.
- Überprüfen Sie, ob der Portainer-Agent-Container läuft.
- Wenn eine Firewall verwendet wird, stellen Sie sicher, dass der Server ausgehende Verbindungen zum Agent initiieren kann.

### Vergessenes Admin-Passwort
Ein Hilfscontainer generiert einen Hash, den Sie sicher setzen können.
```bash
docker run --rm -v portainer_data:/data portainer/helper-reset-password
```

### Portainer startet nicht
Überprüfen Sie die Logs:
```bash
docker logs portainer
```
Häufige Probleme sind beschädigte Volumedaten, nicht übereinstimmende Portainer-Versionen oder Berechtigungsfehler des Docker-Daemons auf dem Host.

## Referenzen

- **Offizielle Website:** [https://www.portainer.io/](https://www.portainer.io/)
- **GitHub:** [https://github.com/portainer/portainer](https://github.com/portainer/portainer)
- **Offizielle Dokumentation:** [https://docs.portainer.io/](https://docs.portainer.io/)
- **Docker Hub:** [portainer/portainer-ce](https://hub.docker.com/r/portainer/portainer-ce)
- **Slack-Community:** [Portainer Slack](https://portainer.io/slack)