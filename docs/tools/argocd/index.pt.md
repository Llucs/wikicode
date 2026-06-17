---
title: ArgoCD – GitOps Entrega Contínua para Kubernetes
description: ArgoCD é uma ferramenta de entrega contínua declarativa, orientada por GitOps, que sincroniza aplicações Kubernetes com repositórios Git como a única fonte de verdade.
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

# ArgoCD – GitOps Entrega Contínua para Kubernetes

## O que é ArgoCD?

ArgoCD é uma ferramenta de entrega contínua (CD) declarativa, **GitOps**, projetada especificamente para Kubernetes. Ela trata os repositórios Git como a **única fonte de verdade** para definições de aplicações e manifests do Kubernetes. O ArgoCD monitora constantemente o estado ativo do cluster e o reconcilia com o estado desejado definido no Git, possibilitando implantações totalmente automatizadas, auditáveis e repetíveis.

## Por que ArgoCD?

- **Declarativa e Controlada por Versão** – Toda infraestrutura e configurações de aplicação vivem no Git. As alterações são feitas via pull requests, não por comandos imperativos.
- **Auto-Cura Automatizada** – O sistema corrige automaticamente o desvio de configuração revertendo qualquer alteração manual para o que está definido no Git.
- **Trilha de Auditoria** – Cada implantação é capturada no histórico do Git, fornecendo um registro de auditoria imutável.
- **Gerenciamento Multi‑Cluster** – Uma única instância do ArgoCD pode gerenciar aplicações em centenas de clusters Kubernetes.
- **Agnóstico em Gerenciamento de Configuração** – Funciona com YAML puro, Helm, Kustomize, Jsonnet e mais.

## Instalação

O ArgoCD pode ser instalado em qualquer cluster Kubernetes em minutos.

### 1. Criar o namespace e aplicar o manifest

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. Acessar o servidor da API (port‑forward)

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Agora você pode acessar a interface web em `https://localhost:8080`.

### 3. Obter a senha inicial do administrador

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

### 4. Fazer login usando a CLI

```bash
argocd login localhost:8080
```

Use o usuário `admin` e a senha do passo anterior.

## Uso Básico

### Conectar um Repositório Git

```bash
argocd repo add https://github.com/my-org/my-app.git
```

### Registrar um Cluster Alvo

Se o alvo não for o mesmo cluster onde o ArgoCD está sendo executado, registre‑o:

```bash
argocd cluster add <kube-context-name>
```

### Definir uma Aplicação (YAML Declarativo)

Crie um arquivo `nginx-app.yaml`:

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

Aplique‑o:

```bash
kubectl apply -f nginx-app.yaml
```

### Sincronizar uma Aplicação

Sincronização manual (ou a política de sincronização automatizada cuidará disso):

```bash
argocd app sync nginx-prod
```

Uma sincronização também pode ser acionada pela interface web ou via webhook do seu provedor Git.

## Principais Funcionalidades e Comandos

### Sincronização Automatizada e Auto‑Cura

- **Auto‑Sync** – O ArgoCD pode iniciar automaticamente uma sincronização sempre que um novo commit é enviado para o branch monitorado.
- **Self‑Heal** – Se alguém modificar manualmente recursos no cluster, o ArgoCD os reverte para o estado definido no Git.

Configure no YAML sob `syncPolicy.automated` ou via CLI:

```bash
argocd app set nginx-prod --sync-policy automated --auto-prune --self-heal
```

### Gerenciamento Multi‑Cluster

Use uma instância do ArgoCD para implantar em vários clusters com diferentes namespaces. Liste os clusters:

```bash
argocd cluster list
```

### Application Sets (CRD)

Geração dinâmica de Aplicações com base em parâmetros (por exemplo, para cada cluster, para cada branch, ou a partir de uma lista de geradores). Exemplo usando um gerador Git:

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

### Ferramentas de Gerenciamento de Configuração

O ArgoCD renderiza nativamente manifests a partir de:

- **Helm** – Use `helm.parameters` ou `helm.valueFiles`
- **Kustomize** – Simplesmente aponte para o diretório de overlay do Kustomize
- **Jsonnet** – Através de um arquivo `jsonnet.libsonnet`

### Waves e Hooks de Sincronização

Controle a ordem da implantação de recursos:

- **Sync Waves** – Defina a anotação `argocd.argoproj.io/sync-wave` com um número inteiro (números menores implantam primeiro).
- **Sync Hooks** – Execute jobs (pre‑sync, sync, post‑sync, etc.) para migrações de banco de dados ou validação.

### Notificações e Webhooks

- **Notificações Integradas** – Envie alertas para Slack, e‑mail ou endpoints personalizados quando o status de sincronização mudar.
- **Gatilhos de Webhook** – Integre com GitHub/GitLab/Bitbucket para sincronização quase instantânea ao fazer push.

### Image Updater (Componente Opcional)

Atualize automaticamente a tag da imagem do contêiner no Git quando uma nova imagem for enviada para um registry. Este componente (Argo CD Image Updater) monitora seu registry de contêiner e faz commit da nova tag na fonte Git.

## Arquitetura – Componentes de Alto Nível

- **API Server** – Expõe a API, a interface web e os endpoints da CLI; lida com autenticação, RBAC e gerenciamento de projetos.
- **Repository Server** – Armazena em cache repositórios Git e gera manifests do Kubernetes (por exemplo, renderiza charts Helm, overlays Kustomize).
- **Application Controller** – Monitora continuamente o estado ativo das aplicações e o compara com o estado desejado do servidor de repositório; dispara operações de sincronização, limpeza e auto‑cura.

## Resumo

O ArgoCD transforma implantações Kubernetes em um fluxo de trabalho totalmente automatizado e orientado por Git. Ao tornar o Git a fonte de verdade, ele elimina o desvio de configuração, fornece uma trilha de auditoria imutável e possibilita uma infraestrutura com auto‑cura. Com suporte nativo a Helm, Kustomize, gerenciamento multi‑cluster e Application Sets dinâmicos, ele é o padrão de facto para GitOps no Kubernetes.

Para documentação oficial, visite [argoproj.github.io/argo-cd](https://argoproj.github.io/argo-cd/).