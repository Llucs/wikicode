---
title: Portainer
description: Uma ferramenta auto-hospedada de gerenciamento de containers e orquestração que centraliza governança, RBAC/SSO e controle operacional em vários ambientes.
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

## Overview

Portainer é o padrão da indústria, um "painel único" open-source para gerenciar ambientes conteinerizados. Projetado por Neil Cresswell e bifurcado do DockerUI em 2017, Portainer visa eliminar a curva de aprendizado íngreme e a sobrecarga operacional do Docker, Docker Swarm, Kubernetes, Azure ACI e Hashicorp Nomad. Ele é executado como um container leve (ou através de um Helm chart) e expõe uma interface web poderosa apoiada por uma API REST completa.

Portainer é licenciado sob AGPLv3 para a Community Edition (CE), com uma Business Edition (BE) comercial que adiciona recursos empresariais como conformidade FIPS, RBAC granular e suporte dedicado.

## Why Portainer?

- **Unified Control Plane:** Gerencie todos os mecanismos de container em sua frota a partir de uma única interface web, em vez de alternar entre CLIs.
- **Reduced Complexity:** Equipes não especialistas podem implantar e gerenciar aplicações sem aprender comandos intrincados de `kubectl` ou `docker-compose`.
- **GitOps Ready:** Stacks podem ser vinculados diretamente a repositórios Git. Qualquer push no repositório aciona uma reimplantação automática.
- **Edge Compute:** Gerencie com segurança milhares de dispositivos atrás de NAT ou firewalls usando Edge Agents.
- **Lightweight & Non-Intrusive:** Portainer não substitui seu orquestrador existente; ele fica ao lado, lendo a API do Docker/Kubernetes através de um socket ou de um container Agent dedicado.

## Architecture

Portainer usa um modelo padrão servidor-agente:

1.  **Portainer Server (portainer/portainer-ce):** A aplicação principal. Ela serve a Web UI e a API REST. Este é o nó para o qual você aponta seu navegador.
2.  **Portainer Agent (portainer/agent):** Um container sidecar leve implantado em cada host Docker ou nó Kubernetes que você deseja gerenciar remotamente. O Agent se comunica com o socket local do Docker e expõe uma API segura na porta 9001.
3.  **Edge Agent:** Uma variante do agent padrão projetada para locais remotos. Ele inicia um túnel *de saída* para o Portainer Server, permitindo o gerenciamento através de firewalls restritivos sem abrir portas de entrada.

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

Este é o método mais comum para gerenciar um host local ou um pequeno número de hosts Docker.

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

- `-p 9443:9443`: Web UI e API (HTTPS).
- `-p 8000:8000`: (Opcional) Túnel TCP para conexões de Edge Agent.
- `-v /var/run/docker.sock`: Permite que o Portainer gerencie o host em que é executado.
- `:lts`: A tag de Long Term Support. **Sempre use `:lts` em produção.**

### Docker Swarm

Implante o Portainer como um serviço global em seu cluster Swarm.

```bash
curl -L https://downloads.portainer.io/ce2-19/portainer-agent-stack.yml -o portainer-agent-stack.yml

docker stack deploy -c portainer-agent-stack.yml portainer
```

### Kubernetes (Helm)

Implante o Portainer em seu cluster Kubernetes usando o Helm chart oficial.

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

Para ambientes sem acesso à internet, baixe as imagens antecipadamente.

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

1.  Abra um navegador em `https://<SERVER_IP>:9443`.
2.  Crie uma senha forte para o usuário `admin`.
3.  O assistente de configuração rápida aparecerá. Selecione **Docker** e escolha **Socket** para conectar ao daemon Docker local.
4.  Clique em **Connect**. Agora você está na página **Home**—este é o seletor de ambiente.

## Key Features & Command Examples

### 1. Multi-Environment Management

Conecte hosts Docker remotos implantando o Portainer Agent.

**On the remote host (target):**
```bash
docker run -d -p 9001:9001 --name portainer_agent \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /var/lib/docker/volumes:/var/lib/docker/volumes \
    portainer/agent:lts
```

**Na interface do Portainer Server:**
Navegue para **Environments** > **Add Environment** > **Docker Agent**.
Insira o IP do host remoto e a porta (9001). Clique em **Connect**.

### 2. App Templates (One-Click Deploy)

Portainer inclui um catálogo de aplicações predefinidas (Nginx, MySQL, WordPress, etc.).

**Fluxo de trabalho:**
1. Barra lateral > **App Templates**.
2. Clique em um template (ex.: **Nginx**).
3. Personalize nome, portas, variáveis de ambiente.
4. Clique em **Deploy the stack**.

### 3. Stacks & GitOps

Implante aplicações complexas usando arquivos Docker Compose ou manifestos Kubernetes. Stacks podem ser vinculados a um repositório Git para fluxos de trabalho GitOps.

**Manual Compose Deployment:**
Cole isso em **Stacks** > **Add Stack** > **Web Editor**:
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

**Configuração GitOps:**
1. **Stacks** > **Add Stack** > **Repository**.
2. Insira a URL do repositório Git e o caminho para o arquivo Compose.
3. Ative **Automatic Updates**.
4. Clique em **Deploy the stack**. Qualquer `git push` aciona uma reimplantação.

### 4. Kubernetes Management

Portainer abstrai a complexidade do `kubectl`. Você pode criar Namespaces, Deployments, Services e Ingresses através de um formulário ou YAML.

**Exemplo:** Implantando uma carga de trabalho nginx simples.
1. **Environments** > Selecione seu **Kubernetes cluster**.
2. **Kubernetes** > **Workloads** > **Add Workload**.
3. Preencha o formulário (Name: `nginx`, Image: `nginx:alpine`, Port: `80`).
4. Clique em **Deploy**.

### 5. Registries

Gerencie centralmente credenciais para Docker Hub, GitLab, Quay, Amazon ECR e Google Container Registry.

1. **Registries** > **Add Registry**.
2. Escolha seu provedor (ex.: **Docker Hub**).
3. Insira suas credenciais (username/access token).

### 6. Edge Compute

Gerencie dispositivos remotos (IoT, varejo, locais de campo) atrás de NAT/firewalls. O servidor gera um `EDGE_ID` e `EDGE_KEY`.

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

Portainer possui uma API REST rica. Gere uma chave de API em **Settings** > **Security**.

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

| Recurso | Community Edition (CE) | Business Edition (BE) |
|---|---|---|
| Licença | AGPLv3 | Comercial |
| Multi-ambiente | Ilimitado | Ilimitado |
| GitOps | Sim | Sim |
| Edge Compute | Limitado | Completo (Edge Groups, Stacks, Jobs) |
| RBAC / SSO | Básico | Avançado (AD/LDAP/OAuth, Team Roles, Resource Controls) |
| Gerenciamento de Registries | Manual | Centralizado com governança |
| Suporte | Comunidade | Comercial (24/7/365) |
| Conformidade FIPS | Não | Sim |

## Best Practices

1.  **Use as versões `:lts`.** Não use a tag `:latest` em produção; ela corresponde a versões de ponta.
2.  **Dedique o nó Server.** Não execute dezenas de cargas de trabalho no container Portainer Server. Use-o estritamente como um ponto de gerenciamento.
3.  **Faça backup do `portainer_data` regularmente.** Execute isso para fazer backup do volume:
    ```bash
    docker run --rm -v portainer_data:/data -v $(pwd):/backup alpine tar cvf /backup/portainer_backup.tar /data
    ```
4.  **Proteja com TLS adequado.** Substitua o certificado autoassinado em Produção.
    ```bash
    docker run -d -p 9443:9443 --name portainer \
        -v /path/to/fullchain.pem:/certs/portainer.crt \
        -v /path/to/privkey.pem:/certs/portainer.key \
        -v portainer_data:/data \
        portainer/portainer-ce:lts
    ```

## Troubleshooting

### Falhas de conexão do Agent
- Certifique-se de que a porta `9001` está aberta na máquina de destino.
- Verifique se o container Portainer Agent está em execução.
- Se estiver usando um firewall, garanta que o Server possa iniciar conexões de saída para o Agent.

### Esqueceu a senha do admin
Um container auxiliar gera um hash que você pode definir de forma segura.
```bash
docker run --rm -v portainer_data:/data portainer/helper-reset-password
```

### Portainer não inicia
Verifique os logs:
```bash
docker logs portainer
```
Problemas comuns incluem dados de volume corrompidos, versões incompatíveis do Portainer ou erros de permissão do daemon Docker do host.

## References

- **Site Oficial:** [https://www.portainer.io/](https://www.portainer.io/)
- **GitHub:** [https://github.com/portainer/portainer](https://github.com/portainer/portainer)
- **Documentação Oficial:** [https://docs.portainer.io/](https://docs.portainer.io/)
- **Docker Hub:** [portainer/portainer-ce](https://hub.docker.com/r/portainer/portainer-ce)
- **Comunidade Slack:** [Portainer Slack](https://portainer.io/slack)