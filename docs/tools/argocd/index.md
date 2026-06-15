---
title: ArgoCD – GitOps Continuous Delivery for Kubernetes
description: ArgoCD is a declarative, GitOps-driven continuous delivery tool that synchronizes Kubernetes applications with Git repositories as the single source of truth.
created: 2026-06-15
tags:
  - gitops
  - kubernetes
  - continuous-delivery
  - argocd
  - devops-tools
status: draft
---

# ArgoCD – GitOps Continuous Delivery for Kubernetes

## What Is ArgoCD?

ArgoCD is a declarative, **GitOps** continuous delivery (CD) tool designed specifically for Kubernetes. It treats Git repositories as the **single source of truth** for application definitions and Kubernetes manifests. ArgoCD constantly monitors the live cluster state and reconciles it with the desired state defined in Git, enabling fully automated, auditable, and repeatable deployments.

## Why ArgoCD?

- **Declarative & Version‑Controlled** – All infrastructure and application configurations live in Git. Changes are made via pull requests, not imperative commands.
- **Automated Self‑Healing** – The system automatically corrects configuration drift by reverting any manual change back to what is defined in Git.
- **Audit Trail** – Every deployment is captured in Git history, providing an immutable audit log.
- **Multi‑Cluster Management** – A single ArgoCD instance can manage applications across hundreds of Kubernetes clusters.
- **Config‑Management Agnostic** – Works with plain YAML, Helm, Kustomize, Jsonnet, and more.

## Installation

ArgoCD can be installed on any Kubernetes cluster in minutes.

### 1. Create the namespace and apply the manifest

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. Access the API server (port‑forward)

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Now you can reach the web UI at `https://localhost:8080`.

### 3. Retrieve the initial admin password

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

### 4. Log in using the CLI

```bash
argocd login localhost:8080
```

Use the username `admin` and the password from the previous step.

## Basic Usage

### Connect a Git Repository

```bash
argocd repo add https://github.com/my-org/my-app.git
```

### Register a Target Cluster

If the target is not the same cluster as the one ArgoCD runs on, register it:

```bash
argocd cluster add <kube-context-name>
```

### Define an Application (Declarative YAML)

Create a file `nginx-app.yaml`:

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

Apply it:

```bash
kubectl apply -f nginx-app.yaml
```

### Synchronise an Application

Manual sync (or the automated sync policy will handle it):

```bash
argocd app sync nginx-prod
```

A sync can also be triggered from the web UI or via webhook from your Git provider.

## Key Features & Commands

### Automated Sync & Self‑Healing

- **Auto‑Sync** – ArgoCD can automatically start a sync whenever a new commit is pushed to the tracked branch.
- **Self‑Heal** – If someone manually modifies resources in the cluster, ArgoCD reverts them back to the state defined in Git.

Configure in the YAML under `syncPolicy.automated` or via CLI:

```bash
argocd app set nginx-prod --sync-policy automated --auto-prune --self-heal
```

### Multi‑Cluster Management

Use one ArgoCD instance to deploy to many clusters with different namespaces. List clusters:

```bash
argocd cluster list
```

### Application Sets (CRD)

Dynamic generation of Applications based on parameters (e.g., for each cluster, for each branch, or from a list of generators). Example using a Git generator:

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

### Config‑Management Tools

ArgoCD natively renders manifests from:

- **Helm** – Use `helm.parameters` or `helm.valueFiles`
- **Kustomize** – Simply point to the Kustomize overlay directory
- **Jsonnet** – Via a `jsonnet.libsonnet` file

### Sync Waves & Hooks

Control the order of resource deployment:

- **Sync Waves** – Set annotation `argocd.argoproj.io/sync-wave` with an integer (lower numbers deploy first).
- **Sync Hooks** – Run jobs (pre‑sync, sync, post‑sync, etc.) for database migrations or validation.

### Notifications & Webhooks

- **Built‑in Notifications** – Send alerts to Slack, email, or custom endpoints when sync status changes.
- **Webhook Triggers** – Integrate with GitHub/GitLab/Bitbucket for near‑instantaneous sync on push.

### Image Updater (Optional Component)

Automatically update the container image tag in Git when a new image is pushed to a registry. This component (Argo CD Image Updater) watches your container registry and commits the new tag to the Git source.

## Architecture – High‑Level Components

- **API Server** – Exposes the API, Web UI, and CLI endpoints; handles authentication, RBAC, and project management.
- **Repository Server** – Caches Git repositories and generates Kubernetes manifests (e.g., renders Helm charts, Kustomize overlays).
- **Application Controller** – Continuously monitors the live state of applications and compares it to the desired state from the repository server; triggers sync, prune, and self‑heal operations.

## Summary

ArgoCD turns Kubernetes deployments into a fully automated, Git‑driven workflow. By making Git the source of truth, it eliminates configuration drift, provides an immutable audit trail, and enables self‑healing infrastructure. With built‑in support for Helm, Kustomize, multi‑cluster management, and dynamic Application Sets, it is the de‑facto standard for GitOps on Kubernetes.

For official documentation, visit [argoproj.github.io/argo-cd](https://argoproj.github.io/argo-cd/).