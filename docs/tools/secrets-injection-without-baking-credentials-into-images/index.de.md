---
title: Secrets Injection ohne die Verwendung von Credentials in Docker-Bildern
description: Ein Verfahren zur sicheren Verwaltung und Einspeisung von Geheimnissen in Container-Bilder ohne die direkte Einbetonung von Anmeldedaten, um eine bessere Sicherheit und Compliance in Bereitstellungspipeline zu gewährleisten.
created: 2026-07-04
tags:
  - DevOps
  - Docker
  - Kubernetes
  - Sicherheit
  - Geheimnisdienstverwaltung
status: draft
---

# Secrets Injection ohne die Verwendung von Credentials in Docker-Bildern

Secrets Injection bezieht sich auf den Prozess der sicheren Verwaltung und Einspeisung von vertraulicher Daten in kontainerte Anwendungen am Laufzeitzeitalter. Dies wird erreicht, indem Anmeldeinformationen oder Geheimnisse nicht direkt in das Docker-Bild eingebettet werden, sondern stattdessen während des Laufzeitzeitalters oder der Bereitstellungsphase bereitgestellt werden.

## Kernfunktionen

1. **Laufzeit-Sicherheit**: Anmeldeinformationen werden nie in das Bild eingebettet, was das Risiko einer Erkennung während der Bildscannung oder einer Verluste durch Schwachstellen verringert.
2. **Flexibilität**: Ermöglicht die einfache Aktualisierung von Geheimnissen, ohne dass das Bild neu aufgebaut und erneut bereitgestellt werden muss.
3. **Skalierbarkeit**: Fördert die sichere Verwaltung von Geheimnissen in einem Mehrcontainer- und Mikrodienstumfeld.
4. **Compliance**: Hilft Organisationen, an regulatory Standards und besten Praktiken für datensicherheit und Compliance zu halten.

## Einsatzfälle

1. **Datenbank-Anmeldeinformationen**: sichere Verwaltung von Datenbank-Benutzernamen und Passwörtern.
2. **API-Schlüssel**: sichere Speicherung und Einspeisung von API-Schlüsseln für verschiedene Dienste.
3. **Konfigurationsverwaltung**: Einspeisung von Konfigurationsereignissen, die nicht Teil des Anwendungscodebases sind.
4. **Verschlüsselungsschlüssel**: Verwaltung von Verschlüsselungsschlüsseln für die Schutz von Daten im Ruhezustand oder im Transportschutz.

## Installation

Die Installationsprozedur variiert je nach dem spezifischen Tool oder der Lösung, die für Geheimnisdienstverwaltung verwendet wird. Hier sind allgemeine Schritte für einige häufige Lösungen:

### Kubernetes Geheimnisse

1. **Voraussetzungen**: Kubernetes-Cluster.
2. **Installation**: Keine explizite Installation erforderlich; Kubernetes-Geheimnisse sind eine integrierte Funktion.
3. **Schritte**:
   1. Erstellen eines Geheimnisses mit `kubectl` oder einem Kubernetes-Dashboard.
   2. Verweisen auf das Geheimnis in deinem Deployment-YAML oder Kubernetes-Manifest.
   3. Mount das Geheimnis als Volume oder verwende es als Umgebungsvariable in deinen Pods.

```yaml
# Beispiel-YAML für das Verweisen auf ein Geheimnis
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app-image
        env:
          - name: MY_SECRET_KEY
            valueFrom:
              secretKeyRef:
                name: my-secret
                key: my-key
```

### Docker Geheimnisse

1. **Voraussetzungen**: Docker Swarm.
2. **Installation**: Keine explizite Installation erforderlich; Docker Swarm unterstützt Geheimnisse standardmäßig.
3. **Schritte**:
   1. Erstellen eines Docker-Geheimnisses mit dem Befehl `docker swarm secret create`.
   2. Verweisen auf das Geheimnis in deiner Dienstdefinition.

```bash
# Erstellen eines Docker-Geheimnisses
docker swarm secret create my-secret my-value

# Verweisen auf das Geheimnis in einer Dienstdefinition
services:
  my-service:
    secrets:
      - my-secret
    command: ["--my-key=$(MY_SECRET_KEY)"]
```

### HashiCorp Vault

1. **Voraussetzungen**: HashiCorp Vault-Server.
2. **Installation**: Herunterladen und Installieren von HashiCorp Vault auf deinem Server oder Nutzung eines verwalteten Dienstes.
3. **Schritte**:
   1. Initialisieren und Entschlüsseln des Vaults.
   2. Erstellen und Speichern von Geheimnissen in Vault.
   3. Verwenden der Vault-API zur Rückgewinnung von Geheimnissen am Laufzeitzeitalter.

```bash
# Initialisieren und Entschlüsseln des Vault
vault operator init
vault unseal <entschlüsselung-schlüssel>

# Erstellen und Speichern eines Geheimnisses
vault kv put secret/my-secret key=my-value

# Rückgewinnung des Geheimnisses über die Vault-API
vault read secret/my-secret
```

## Basisverwendung

### Erstellen eines Geheimnisses

1. **Kubernetes**: `kubectl create secret generic my-secret --from-literal=my-key=my-value`
2. **Docker Swarm**: `docker swarm secret create my-secret my-value`
3. **HashiCorp Vault**: `vault kv put secret/my-secret key=my-value`

### Verweisen auf das Geheimnis

1. **Kubernetes**:
   ```yaml
   spec:
     containers:
     - name: my-app
       image: my-app-image
       env:
         - name: MY_SECRET_KEY
           valueFrom:
             secretKeyRef:
               name: my-secret
               key: my-key
   ```

2. **Docker Swarm**:
   ```yaml
   services:
     my-service:
       secrets:
         - my-secret
       command: ["--my-key=$(MY_SECRET_KEY)"]
   ```

3. **HashiCorp Vault**:
   - Geheimnisse können über die Vault-API oder mit dem Befehl `vault read` zurückgewonnen werden.

Indem Organisationen Secrets Injection-Praktiken einlegen, können sie den Sicherheitsposten ihrer kontainerten Anwendungen signifikant verbessern und sicherstellen, dass vertrauliche Daten während des gesamten Entwicklungslaufzyklus und -bereitstellungspipelines geschützt und verwaltbar bleiben.