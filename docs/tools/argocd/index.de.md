---
title: ArgoCD – GitOps Continuous Delivery für Kubernetes
description: ArgoCD ist ein deklaratives, GitOps-gesteuertes Continuous-Delivery-Tool, das Kubernetes-Anwendungen mit Git-Repositories als einziger Quelle der Wahrheit synchronisiert.
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

# ArgoCD – GitOps Continuous Delivery für Kubernetes

## Was ist ArgoCD?

ArgoCD ist ein deklaratives, **GitOps**-Continuous-Delivery-(CD-)Tool, das speziell für Kubernetes entwickelt wurde. Es behandelt Git-Repositories als **einzige Quelle der Wahrheit** für Anwendungsdefinitionen und Kubernetes-Manifeste. ArgoCD überwacht ständig den Live-Clusterzustand und gleicht ihn mit dem in Git definierten gewünschten Zustand ab, was vollständig automatisierte, nachvollziehbare und wiederholbare Bereitstellungen ermöglicht.

## Warum ArgoCD?

- **Deklarativ & Versionskontrolliert** – Alle Infrastruktur- und Anwendungskonfigurationen leben in Git. Änderungen erfolgen über Pull Requests, nicht über imperative Befehle.
- **Automatische Selbstheilung** – Das System korrigiert automatisch Konfigurationsabweichungen, indem es manuelle Änderungen rückgängig macht und auf den in Git definierten Zustand zurücksetzt.
- **Prüfpfad** – Jede Bereitstellung wird in der Git-Historie festgehalten und bietet ein unveränderliches Prüfprotokoll.
- **Multi-Cluster-Verwaltung** – Eine einzige ArgoCD-Instanz kann Anwendungen in Hunderten von Kubernetes-Clustern verwalten.
- **Konfigurationsmanagement-Agnostisch** – Funktioniert mit einfachem YAML, Helm, Kustomize, Jsonnet und mehr.

## Installation

ArgoCD kann in wenigen Minuten auf jedem Kubernetes-Cluster installiert werden.

### 1. Namespace erstellen und Manifest anwenden

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. Auf den API-Server zugreifen (Port-Forwarding)

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Jetzt können Sie die Web-UI unter `https://localhost:8080` erreichen.

### 3. Initiales Admin-Passwort abrufen

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

### 4. Mit der CLI anmelden

```bash
argocd login localhost:8080
```

Verwenden Sie den Benutzernamen `admin` und das Passwort aus dem vorherigen Schritt.

## Grundlegende Nutzung

### Ein Git-Repository verbinden

```bash
argocd repo add https://github.com/my-org/my-app.git
```

### Einen Zielcluster registrieren

Falls der Zielcluster nicht derselbe ist, auf dem ArgoCD läuft, registrieren Sie ihn:

```bash
argocd cluster add <kube-context-name>
```

### Eine Anwendung definieren (deklaratives YAML)

Erstellen Sie eine Datei `nginx-app.yaml`:

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

Wenden Sie sie an:

```bash
kubectl apply -f nginx-app.yaml
```

### Eine Anwendung synchronisieren

Manuelle Synchronisation (oder die automatische Synchronisationsrichtlinie übernimmt es):

```bash
argocd app sync nginx-prod
```

Eine Synchronisation kann auch über die Web-UI oder per Webhook von Ihrem Git-Anbieter ausgelöst werden.

## Hauptmerkmale & Befehle

### Automatische Synchronisation & Selbstheilung

- **Auto‑Sync** – ArgoCD kann automatisch eine Synchronisation starten, sobald ein neuer Commit in den verfolgten Branch gepusht wird.
- **Self‑Heal** – Wenn jemand manuell Ressourcen im Cluster ändert, setzt ArgoCD sie auf den in Git definierten Zustand zurück.

Konfiguration im YAML unter `syncPolicy.automated` oder per CLI:

```bash
argocd app set nginx-prod --sync-policy automated --auto-prune --self-heal
```

### Multi-Cluster-Verwaltung

Verwenden Sie eine ArgoCD-Instanz, um in vielen Clustern mit verschiedenen Namespaces Bereitstellungen durchzuführen. Cluster auflisten:

```bash
argocd cluster list
```

### Application Sets (CRD)

Dynamische Generierung von Applications basierend auf Parametern (z. B. für jeden Cluster, für jeden Branch oder aus einer Liste von Generatoren). Beispiel mit einem Git-Generator:

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

### Konfigurationsmanagement-Tools

ArgoCD rendert nativ Manifeste aus:

- **Helm** – Verwenden Sie `helm.parameters` oder `helm.valueFiles`
- **Kustomize** – Zeigen Sie einfach auf das Kustomize-Overlay-Verzeichnis
- **Jsonnet** – Über eine `jsonnet.libsonnet`-Datei

### Sync-Wellen & Hooks

Steuern Sie die Reihenfolge der Ressourcenbereitstellung:

- **Sync-Wellen** – Setzen Sie die Annotation `argocd.argoproj.io/sync-wave` mit einer ganzen Zahl (niedrigere Zahlen werden zuerst bereitgestellt).
- **Sync-Hooks** – Führen Sie Jobs (pre‑sync, sync, post‑sync, etc.) für Datenbankmigrationen oder Validierungen aus.

### Benachrichtigungen & Webhooks

- **Integrierte Benachrichtigungen** – Senden Sie Warnmeldungen an Slack, E‑Mail oder benutzerdefinierte Endpunkte, wenn sich der Synchronisationsstatus ändert.
- **Webhook-Trigger** – Integrieren Sie GitHub/GitLab/Bitbucket für nahezu sofortige Synchronisation bei Push.

### Image Updater (optionale Komponente)

Aktualisiert automatisch den Container-Image-Tag in Git, wenn ein neues Image in eine Registry gepusht wird. Diese Komponente (Argo CD Image Updater) überwacht Ihre Container-Registry und committed den neuen Tag in die Git-Quelle.

## Architektur – Komponenten auf hoher Ebene

- **API-Server** – Stellt die API-, Web-UI- und CLI-Endpunkte bereit; kümmert sich um Authentifizierung, RBAC und Projektverwaltung.
- **Repository-Server** – Cached Git-Repositories und generiert Kubernetes-Manifeste (z. B. rendert Helm-Charts, Kustomize-Overlays).
- **Application Controller** – Überwacht kontinuierlich den Live-Zustand von Anwendungen und vergleicht ihn mit dem gewünschten Zustand vom Repository-Server; löst Synchronisations-, Bereinigungs- und Selbstheilungsvorgänge aus.

## Zusammenfassung

ArgoCD verwandelt Kubernetes-Bereitstellungen in einen vollautomatischen, Git-gesteuerten Workflow. Indem Git zur Quelle der Wahrheit gemacht wird, werden Konfigurationsabweichungen vermieden, ein unveränderlicher Prüfpfad bereitgestellt und eine selbstheilende Infrastruktur ermöglicht. Mit integrierter Unterstützung für Helm, Kustomize, Multi-Cluster-Verwaltung und dynamische Application Sets ist es der De-facto-Standard für GitOps auf Kubernetes.

Für die offizielle Dokumentation besuchen Sie [argoproj.github.io/argo-cd](https://argoproj.github.io/argo-cd/).