---
title: Zero-Downtime Bereitstellungen
description: Eine umfassende Anleitung zur Umsetzung von zero-downtime Bereitstellungen mit blau/green, Canary und rolling Strategien.
created: 2026-07-24
tags:
  - DevOps
  - Bereitstellung
  - Zero-Downtime
status: draft
---

# Zero-Downtime Bereitstellungen

Zero-Downtime-Bereitstellung ist ein Software-Engineering-Praktikum, das sicherstellt, dass ein Dienst oder eine Anwendung während des Bereitstellungsprozesses für Benutzer verfügbar bleibt. Diese Technik umfasst Strategien, um die Verfügbarkeit des Dienstes während der Bereitstellung von neuen Code oder Konfigurationen zu minimieren oder vollständig auszuschließen. Das Ziel besteht darin, die Dienstverfügbarkeit während Software-Aufräumungen oder Wartungsarbeiten zu beibehalten.

## Schlüsselwerke

1. **Service-Discovery und Load Balancing:** Nutzung von Mechanismen wie DNS, Service Mesh oder Load Balancers zur Umleitung des Verkehrs zu verschiedenen Instanzen.
2. **Blau/Green-Bereitstellung:** Bereitstellung zweier identischer Umgebungen (blau und green), die das Verkehren zwischen ihnen ohne Unterbrechung ermöglicht.
3. **Canary-Releases:** Neue Versionen langsam an eine kleine Teilmenge von Benutzern auszuprobieren, um Probleme vor dem Ausprobieren für den gesamten Benutzerpool zu erkennen.
4. **Rolling Updates:** Neue Versionen langsam an einzelnen Instanzen oder Gruppen von Instanzen zu aktualisieren, um einen einzelnen Punkt von Versagen zu vermeiden.
5. **Microservices-Architektur:** Das Anwendungsgitter in kleinere, unabhängig bereitstellbare Dienste zu zerlegen, um Fehlereinträge in einem Dienst nicht auf andere Auswirkungen zu haben.

## Installation

Die Installation von Zero-Downtime-Bereitstellungstools und -Strategien hängt von der spezifischen Umgebung und den verwendeten Technologien ab. Hier sind einige allgemeine Schritte:

1. **Umfeld-Setup:**
   - Setze einen Loadbalancer oder ein Service Mesh ein, um das Verkehrsverteilungsmanagement zu verwalten.
   - Konfiguriere DNS für Service-Discovery und Fehlereinfall.

2. **Blau/Green-Bereitstellung:**
   - Bereite eine neue Version des Programms in einer neuen Umgebung aus.
   - Nutze den Loadbalancer, um den Verkehr zwischen der alten und der neuen Umgebung umzuleiten.
   - Sobald die neue Umgebung getestet ist, übertrage den Verkehr komplett.

3. **Canary-Releases:**
   - Bereite eine neue Version für eine kleine Teilmenge von Benutzern oder eine bestimmte Region aus.
   - Überwache die Leistung und die Benutzerfeedback.
   - Erhöhe langsam das Prozentsatz der Benutzer oder der Regionen, die die neue Version erhalten.

4. **Rolling Updates:**
   - Aktualisiere einzelne Instanzen oder Gruppen von Instanzen langsam.
   - Überwache für Probleme und führe gegebenenfalls einen Rollback durch.
   - Graduelle Ausweitung der aktualisierteren Instanzen.

5. **Microservices:**
   - Nutze einen Service Mesh oder eine Orchestrierungstool (wie Kubernetes) zur Verwaltung der Bereitstellung einzelner Dienste.
   - Stelle sicher, dass jede Dienst unabhängig skalierbar und aktualisierbar ist.

## Basisnutzung

1. **Planung der Bereitstellung:**
   - Definiere die Strategie (blau/green, Canary, rolling Updates).
   - Planung von möglichen Problemen und Rollback-Strategien.

2. **Bereitstellung der neuen Version:**
   - Teste und verifiziere die neue Version gründlich.
   - Stelle sicher, dass alle Abhängigkeiten richtig konfiguriert sind.

3. **Bereitstellung der neuen Version:**
   - Nutze die gewählte Strategie zur Bereitstellung der neuen Version.
   - Überwache den Bereitstellungsprozess auf Probleme.

4. **Überprüfung und Skalierung:**
   - Überprüfe die neue Version auf Stabilität und Leistung.
   - Graduelle Skalierung der neuen Version und Rückmeldung der alten Version.

5. **Dokumentation und Erlernen:**
   - Dokumentiere den Bereitstellungsprozess und gelernte Erfahrungen.
   - Verbessere die Bereitstellungsstrategie auf der Grundlage von Erfahrungen.

### Beispiel: Blau/Green-Bereitstellung mit Kubernetes

#### Voraussetzungen
- Kubernetes-Umfeld mit `kubectl` installiert und konfiguriert.
- Zwei identische Bereitstellungen: `blau` und `green`.

#### Schritt 1: Definition der Bereitstellungsmanifeste

Erstelle zwei Bereitstellungsmanifeste, jeweils für eine Umgebung.

**Blauer Bereich:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-blau
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: blau
  template:
    metadata:
      labels:
        app: my-app
        version: blau
    spec:
      containers:
      - name: my-app
        image: my-app:blau
        ports:
        - containerPort: 80
```

**Greener Bereich:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-gruen
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: gruen
  template:
    metadata:
      labels:
        app: my-app
        version: gruen
    spec:
      containers:
      - name: my-app
        image: my-app:gruen
        ports:
        - containerPort: 80
```

#### Schritt 2: Bereitstellung des Blauen Bereichs

```bash
kubectl apply -f blau-bereitstellung.yaml
```

#### Schritt 3: Erstellen eines Service für die Verkehrsverteilung

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: my-app
```

Anwenden des Service-Manifests:

```bash
kubectl apply -f service.yaml
```

#### Schritt 4: Umleitung des Verkehrs zum Grünen Umfeld

Aktualisiere den Service, um den Verkehr zum grünen Umfeld umzuleiten:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: my-app
    version: gruen
```

Anwenden des aktualisierten Service-Manifests:

```bash
kubectl apply -f service.yaml
```

#### Schritt 5: Überprüfung der Bereitstellung

Überprüfe die Pods und den Servicestatus:

```bash
kubectl get pods
kubectl get services
```

Sobald die Überprüfung bestanden hat, kannst du den Verkehr zurück zum blauen Umfeld umleiten, falls erforderlich.

### Beispiel: Canary-Releases

#### Voraussetzungen
- Kubernetes-Umfeld mit `kubectl` installiert und konfiguriert.
- Zwei Bereitstellungen: `stabil` und `canary`.

#### Schritt 1: Definition der Bereitstellungsmanifeste

Erstelle zwei Bereitstellungsmanifeste, jeweils für eine Umgebung.

**Stabile Bereitstellung:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-stabil
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: stabil
  template:
    metadata:
      labels:
        app: my-app
        version: stabil
    spec:
      containers:
      - name: my-app
        image: my-app:stabil
        ports:
        - containerPort: 80
```

**Canary-Bereitstellung:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-canary
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: canary
  template:
    metadata:
      labels:
        app: my-app
        version: canary
    spec:
      containers:
      - name: my-app
        image: my-app:canary
        ports:
        - containerPort: 80
```

#### Schritt 2: Bereitstellung der stabilen Umgebung

```bash
kubectl apply -f stabil-bereitstellung.yaml
```

#### Schritt 3: Erstellen eines Service für die Verkehrsverteilung

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: my-app
```

Anwenden des Service-Manifests:

```bash
kubectl apply -f service.yaml
```

#### Schritt 4: Bereitstellung des Canary-Umfelds

```bash
kubectl apply -f canary-bereitstellung.yaml
```

#### Schritt 5: Umleitung des Verkehrs zum Canary-Umfeld

Aktualisiere den Service, um den Verkehr zum Canary-Umfeld umzuleiten:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: my-app
    version: canary
```

Anwenden des aktualisierten Service-Manifests:

```bash
kubectl apply -f service.yaml
```

#### Schritt 6: Überprüfung der Bereitstellung

Überprüfe die Pods und den Servicestatus:

```bash
kubectl get pods
kubectl get services
```

Sobald die Überprüfung bestanden hat, kannst du die Canary-Umgebung langsam erhöhen:

```bash
kubectl patch service my-app-service -p '{"spec":{"selector":{"app":"my-app","version":"canary"}}}'
```

Überwache die Canary-Umgebung auf Probleme und erhöhe langsam die Canary-Umgebung bis zu 100%.

### Schluss

Zero-Downtime-Bereitstellungen sind für die Wahrung der Zuverlässigkeit und Verfügbarkeit von verteilteren Systemen essentiell. Durch die Einsetzung effektiver Strategien, Implementierungs-Techniken und der Nutzung der richtigen Tools können Organisationen eine glatte Aktualisierung ohne Unterbrechung der Benutzererfahrungen erreichen. Dieses Handbuch bietet eine umfassende Übersicht über blau/green, Canary und rolling-Updates, sowie praktische Beispiele mit Kubernetes.

---