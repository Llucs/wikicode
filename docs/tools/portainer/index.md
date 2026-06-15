---
title: Portainer
description: A self-hosted container and orchestration management tool that centralizes governance, RBAC/SSO, and operational control across multiple environments.
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
---

# Portainer

## Overview

Portainer is the industry standard, open-source "single pane of glass" for managing containerized environments. Designed by Neil Cresswell and forked from DockerUI in 2017, Portainer aims to eliminate the steep learning curve and operational overhead of Docker, Docker Swarm, Kubernetes, Azure ACI, and Hashicorp Nomad. It runs as a lightweight container itself (or via a Helm chart) and exposes a powerful web UI backed by a fully featured REST API.

Portainer is licensed under AGPLv3 for the Community Edition (CE), with a commercial Business Edition (BE) that adds enterprise features like FIPS compliance, granular RBAC, and dedicated support.

## Why Portainer?

- **Unified Control Plane:** Manage every container engine in your fleet from a single web interface instead of context switching between CLIs.
- **Reduced Complexity:** Non-specialist teams can deploy and manage applications without learning intricate `kubectl` or `docker-compose` commands.
- **GitOps Ready:** Stacks can be linked directly to Git repositories. Any push to the repo triggers an automatic redeployment.
- **Edge Compute:** Securely manage thousands of devices behind NAT or firewalls using Edge Agents.
- **Lightweight & Non-Intrusive:** Portainer does not replace your existing orchestrator; it sits beside it, reading the Docker/Kubernetes API via a socket or a dedicated Agent container.

## Architecture

Portainer uses a standard server-agent model:

1.  **Portainer Server (portainer/portainer-ce):** The main application. It serves the Web UI and REST API. This is the node you point your browser to.
2.  **Portainer Agent (portainer/agent):** A lightweight sidecar container deployed on every Docker host or Kubernetes node you wish to manage remotely. The Agent communicates with the local Docker socket and exposes a secured API on port 9001.
3.  **Edge Agent:** A variant of the standard agent designed for remote locations. It initiates an *outbound* tunnel to the Portainer Server, allowing management through strict firewalls without opening inbound ports.

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

### Docker Standalone (Quick Start)

This is the most common method for managing a local or small number of Docker hosts.

```bash
# Create a persistent volume for Portainer data
docker volume create portainer_data

# Run the Portainer Server container
docker run -d -p 8000:8000 -p 9443:9443 --name portainer \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v portainer_data:/data \
    portainer/portainer-ce:lts
```

- `-p 9443:9443`: Web UI and API (HTTPS).
- `-p 8000:8000`: (Optional) TCP tunnel for Edge Agent connections.
- `-v /var/run/docker.sock`: Allows Portainer to manage the host it runs on.
- `:lts`: The Long Term Support tag. **Always use `:lts` in production.**

### Docker Swarm

Deploy Portainer as a global service across your Swarm cluster.

```bash
curl -L https://downloads.portainer.io/ce2-19/portainer-agent-stack.yml -o portainer-agent-stack.yml

docker stack deploy -c portainer-agent-stack.yml portainer
```

### Kubernetes (Helm)

Deploy Portainer into your Kubernetes cluster using the official Helm chart.

```bash
helm repo add portainer https://portainer.github.io/k8s/
helm repo update

helm upgrade --install portainer portainer/portainer \
    --namespace portainer --create-namespace \
    --set service.type=LoadBalancer \
    --set service.httpPort=9000 \
    --set service.httpsPort=9443
```

### Air-Gapped Installation

For environments with no internet access, pre-pull the images.

```bash
# On a machine with internet access
docker pull portainer/portainer-ce:lts
docker pull portainer/agent:lts

# Tag and push to your internal registry
docker tag portainer/portainer-ce:lts <internal-registry>/portainer-ce:lts
docker tag portainer/agent:lts <internal-registry>/agent:lts
docker push <internal-registry>/portainer-ce:lts
docker push <internal-registry>/agent:lts
```

## Initial Setup

1.  Open a browser to `https://<SERVER_IP>:9443`.
2.  Create a strong password for the `admin` user.
3.  The Quick Setup wizard will appear. Select **Docker** and choose **Socket** to connect to the local Docker daemon.
4.  Click **Connect**. You are now on the **Home** page—this is your environment selector.

## Key Features & Command Examples

### 1. Multi-Environment Management

Connect remote Docker hosts by deploying the Portainer Agent.

**On the remote host (target):**
```bash
docker run -d -p 9001:9001 --name portainer_agent \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /var/lib/docker/volumes:/var/lib/docker/volumes \
    portainer/agent:lts
```

**On the Portainer Server UI:**
Navigate to **Environments** > **Add Environment** > **Docker Agent**.
Enter the remote host IP and port (9001). Click **Connect**.

### 2. App Templates (One-Click Deploy)

Portainer includes a catalog of predefined applications (Nginx, MySQL, WordPress, etc.).

**Workflow:**
1. Sidebar > **App Templates**.
2. Click a template (e.g., **Nginx**).
3. Customize name, ports, environment variables.
4. Click **Deploy the stack**.

### 3. Stacks & GitOps

Deploy complex applications using Docker Compose or Kubernetes manifest files. Stacks can be linked to a Git repository for GitOps workflows.

**Manual Compose Deployment:**
Paste this into **Stacks** > **Add Stack** > **Web Editor**:
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

**GitOps Setup:**
1. **Stacks** > **Add Stack** > **Repository**.
2. Enter the Git repo URL and path to the Compose file.
3. Enable **Automatic Updates**.
4. Click **Deploy the stack**. Any `git push` triggers a redeploy.

### 4. Kubernetes Management

Portainer abstracts `kubectl` complexity. You can create Namespaces, Deployments, Services, and Ingresses via a form or YAML.

**Example:** Deploying a simple nginx workload.
1. **Environments** > Select your **Kubernetes cluster**.
2. **Kubernetes** > **Workloads** > **Add Workload**.
3. Fill in the form (Name: `nginx`, Image: `nginx:alpine`, Port: `80`).
4. Click **Deploy**.

### 5. Registries

Centrally manage credentials for Docker Hub, GitLab, Quay, Amazon ECR, and Google Container Registry.

1. **Registries** > **Add Registry**.
2. Choose your provider (e.g., **Docker Hub**).
3. Enter your credentials (username/access token).

### 6. Edge Compute

Manage remote devices (IoT, retail, field sites) behind NAT/firewalls. The server generates an `EDGE_ID` and `EDGE_KEY`.

**On the Edge device:**
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

### 7. REST API

Portainer has a rich REST API. Generate an API key in **Settings** > **Security**.

```bash
# List all environments
curl -X GET 'https://<SERVER_IP>:9443/api/endpoints' \
    -H 'X-API-Key: ptr_xxxxxxxxxxxx' | jq .

# Deploy a stack
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

## Editions Compared

| Feature | Community Edition (CE) | Business Edition (BE) |
|---|---|---|
| License | AGPLv3 | Commercial |
| Multi-Environment | Unlimited | Unlimited |
| GitOps | Yes | Yes |
| Edge Compute | Limited | Full (Edge Groups, Stacks, Jobs) |
| RBAC / SSO | Basic | Advanced (AD/LDAP/OAuth, Team Roles, Resource Controls) |
| Registry Management | Manual | Centralized with governance |
| Support | Community | Commercial (24/7/365) |
| FIPS Compliance | No | Yes |

## Best Practices

1.  **Use `:lts` releases.** Do not use the `:latest` tag in production; it corresponds to bleeding-edge builds.
2.  **Dedicate the Server node.** Do not run dozens of workloads on the Portainer Server container. Use it strictly as a management point.
3.  **Backup `portainer_data` regularly.** Run this to back up the volume:
    ```bash
    docker run --rm -v portainer_data:/data -v $(pwd):/backup alpine tar cvf /backup/portainer_backup.tar /data
    ```
4.  **Secure with proper TLS.** Replace the self-signed certificate in Production.
    ```bash
    docker run -d -p 9443:9443 --name portainer \
        -v /path/to/fullchain.pem:/certs/portainer.crt \
        -v /path/to/privkey.pem:/certs/portainer.key \
        -v portainer_data:/data \
        portainer/portainer-ce:lts
    ```

## Troubleshooting

### Agent connection failures
- Ensure port `9001` is open on the target machine.
- Verify the Portainer Agent container is running.
- If using a firewall, ensure the Server can initiate outbound connections to the Agent.

### Forgotten Admin Password
A helper container generates a hash you can set securely.
```bash
docker run --rm -v portainer_data:/data portainer/helper-reset-password
```

### Portainer won’t start
Check the logs:
```bash
docker logs portainer
```
Common issues include corrupt volume data, mismatched Portainer versions, or host Docker daemon permission errors.

## References

- **Official Website:** [https://www.portainer.io/](https://www.portainer.io/)
- **GitHub:** [https://github.com/portainer/portainer](https://github.com/portainer/portainer)
- **Official Docs:** [https://docs.portainer.io/](https://docs.portainer.io/)
- **Docker Hub:** [portainer/portainer-ce](https://hub.docker.com/r/portainer/portainer-ce)
- **Slack Community:** [Portainer Slack](https://portainer.io/slack)