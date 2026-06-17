---
title: ArgoCD – 面向 Kubernetes 的 GitOps 持续交付工具
description: ArgoCD 是一个声明式的、基于 GitOps 的持续交付工具，它将 Git 仓库作为单一事实来源来同步 Kubernetes 应用。
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

# ArgoCD – 面向 Kubernetes 的 GitOps 持续交付工具

## 什么是 ArgoCD？

ArgoCD 是一个声明式的、**GitOps** 持续交付（CD）工具，专门为 Kubernetes 设计。它将 Git 仓库视为应用定义和 Kubernetes 清单的**单一真实来源**。ArgoCD 持续监控实时集群状态，并将其与 Git 中定义的期望状态进行调和，从而实现完全自动化、可审计且可重复的部署。

## 为什么选择 ArgoCD？

- **声明式与版本控制** – 所有基础设施和应用配置都存放在 Git 中。通过拉取请求进行变更，而非命令式命令。
- **自动化自愈** – 系统自动纠正配置漂移，将所有手动更改恢复为 Git 中定义的状态。
- **审计追踪** – 每次部署都记录在 Git 历史中，提供不可篡改的审计日志。
- **多集群管理** – 单个 ArgoCD 实例可管理跨数百个 Kubernetes 集群的应用。
- **配置管理无关性** – 支持纯 YAML、Helm、Kustomize、Jsonnet 等。

## 安装

ArgoCD 可在几分钟内安装到任何 Kubernetes 集群上。

### 1. 创建命名空间并应用清单

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. 访问 API 服务器（端口转发）

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

现在您可以通过 `https://localhost:8080` 访问 Web UI。

### 3. 获取初始管理员密码

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

### 4. 使用 CLI 登录

```bash
argocd login localhost:8080
```

使用用户名 `admin` 和上一步获取的密码。

## 基本用法

### 连接一个 Git 仓库

```bash
argocd repo add https://github.com/my-org/my-app.git
```

### 注册一个目标集群

如果目标集群不是 ArgoCD 运行所在的集群，请注册它：

```bash
argocd cluster add <kube-context-name>
```

### 定义应用（声明式 YAML）

创建一个文件 `nginx-app.yaml`：

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

应用它：

```bash
kubectl apply -f nginx-app.yaml
```

### 同步一个应用

手动同步（或由自动同步策略处理）：

```bash
argocd app sync nginx-prod
```

也可以从 Web UI 或通过 Git 提供商的 webhook 触发同步。

## 主要功能与命令

### 自动同步与自愈

- **自动同步** – ArgoCD 可以在新提交推送到跟踪分支时自动开始同步。
- **自愈** – 如果有人手动修改了集群中的资源，ArgoCD 会将它们恢复到 Git 中定义的状态。

在 YAML 的 `syncPolicy.automated` 下或通过 CLI 配置：

```bash
argocd app set nginx-prod --sync-policy automated --auto-prune --self-heal
```

### 多集群管理

使用一个 ArgoCD 实例部署到多个具有不同命名空间的集群。列出集群：

```bash
argocd cluster list
```

### Application Sets（CRD）

基于参数动态生成 Applications（例如，针对每个集群、每个分支或来自生成器列表）。使用 Git 生成器的示例：

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

### 配置管理工具

ArgoCD 原生支持从以下方式渲染清单：

- **Helm** – 使用 `helm.parameters` 或 `helm.valueFiles`
- **Kustomize** – 直接指向 Kustomize overlay 目录
- **Jsonnet** – 通过 `jsonnet.libsonnet` 文件

### 同步波与钩子

控制资源部署的顺序：

- **同步波** – 设置注解 `argocd.argoproj.io/sync-wave`，使用整数（数字越小越先部署）。
- **同步钩子** – 运行作业（pre‑sync、sync、post‑sync 等）以执行数据库迁移或验证。

### 通知与 Webhooks

- **内置通知** – 当同步状态变更时，向 Slack、电子邮件或自定义端点发送告警。
- **Webhook 触发** – 与 GitHub/GitLab/Bitbucket 集成，实现推送时的近乎即时同步。

### 镜像更新器（可选组件）

当新镜像推送到镜像仓库时，自动更新 Git 中的容器镜像标签。该组件（Argo CD Image Updater）会监控您的镜像仓库，并将新标签提交到 Git 源。

## 架构 – 高层组件

- **API 服务器** – 暴露 API、Web UI 和 CLI 端点；处理身份验证、RBAC 和项目管理。
- **仓库服务器** – 缓存 Git 仓库并生成 Kubernetes 清单（例如，渲染 Helm charts、Kustomize overlays）。
- **应用控制器** – 持续监控应用的实时状态，并将其与仓库服务器中的期望状态进行比较；触发同步、剪除和自愈操作。

## 总结

ArgoCD 将 Kubernetes 部署转变为完全自动化的、由 Git 驱动的工作流。通过使 Git 成为事实来源，它消除了配置漂移，提供了不可篡改的审计追踪，并实现了自愈基础设施。凭借对 Helm、Kustomize、多集群管理和动态 Application Sets 的内置支持，它已成为 Kubernetes 上 GitOps 的事实标准。

有关官方文档，请访问 [argoproj.github.io/argo-cd](https://argoproj.github.io/argo-cd/)。