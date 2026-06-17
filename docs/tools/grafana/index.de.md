---
title: "Grafana: Die offene Observability-Plattform"
description: "Einheitliche Visualisierung, Überwachung und Alarmierung für Metriken, Logs und Traces."
created: 2026-06-15
tags:
  - observability
  - monitoring
  - visualization
  - dashboards
  - open-source
status: draft
ecosystem: observability
---

# Grafana: Die offene Observability-Plattform

## Was ist Grafana?

Grafana ist die führende Open-Source-Plattform für Analytik und interaktive Visualisierung im Bereich Observability. Sie verbindet sich mit beliebigen Datenquellen – von Zeitreihen-Datenbanken (Prometheus, InfluxDB, Graphite) über Logging-Backends (Loki, Elasticsearch), Tracing-Systeme (Tempo, Jaeger), SQL-Datenbanken (PostgreSQL, MySQL) bis hin zu Cloud-APIs (AWS CloudWatch, Azure Monitor). Sie bietet eine einzige Oberfläche („Single Pane of Glass“), um Metriken, Logs und Traces abzufragen, zu visualisieren, zu alarmieren und zu verstehen.

Da Grafana auf offenen Standards basiert, vermeiden Sie eine Herstellerbindung (Vendor Lock-in). Sie können Daten aus Dutzenden von Quellen im selben Dashboard mischen, und die gleiche Plattform eignet sich gleichermaßen für Infrastrukturüberwachung, Anwendungsleistungsmanagement, Geschäftsanalysen oder IoT-Telemetrie.

---

## Warum Grafana?

- **Einheitliche Observability** – bringen Sie Metriken, Logs, Traces und Geschäftsdaten an einem Ort zusammen.
- **Umfangreiche Visualisierungen** – Dutzende von Panel-Typen (Zeitreihen, Statistik, Tabelle, Heatmap, Geomap, Candlestick, Logs, Traces und mehr).
- **Dynamische Dashboards** – nutzen Sie Vorlagenvariablen, um Dashboards wiederverwendbar und interaktiv zu gestalten.
- **Einheitliche Alarmierung** – verwalten Sie alle Alarmregeln über Datenquellen hinweg über eine einzige Oberfläche.
- **Explore-Modus** – Ad-hoc-Fehlerbehebung ohne Speichern eines Dashboards.
- **Erweiterbar** – Plugin-Marktplatz für Datenquellen, Panels und Apps.
- **GitOps-bereit** – provisionieren Sie Dashboards, Datenquellen und Alarmregeln mit Konfigurationsdateien.
- **Sicherheit und Governance** – Organisationen, Teams, fein granulierte RBAC, OAuth und API-Schlüssel.
- **Selbst gehostet oder Cloud** – betreiben Sie es selbst oder nutzen Sie Grafana Cloud (großzügiges kostenloses Kontingent).

---

## Installation

### 1. Binary / Paket

Laden Sie das `.rpm`, `.deb` oder den eigenständigen Tarball von der [Download-Seite](https://grafana.com/grafana/download) herunter und installieren Sie es:

```bash
# Debian / Ubuntu
sudo apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana_11.0.0_amd64.deb
sudo dpkg -i grafana_11.0.0_amd64.deb
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

```bash
# RHEL / CentOS / Fedora
sudo yum install -y https://dl.grafana.com/oss/release/grafana-11.0.0-1.x86_64.rpm
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

### 2. Docker

Führen Sie das offizielle Docker-Image aus (Standard-Port 3000). Binden Sie Volumes für persistente Daten ein:

```bash
docker run -d \
  -p 3000:3000 \
  --name=grafana \
  -v grafana-storage:/var/lib/grafana \
  grafana/grafana:latest
```

### 3. Kubernetes (Helm)

Fügen Sie das Grafana Helm-Repository hinzu und stellen Sie es bereit:

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install my-grafana grafana/grafana \
  --namespace monitoring --create-namespace \
  --set persistence.enabled=true \
  --set adminPassword='admin'
```

### 4. Grafana Cloud

Erstellen Sie ein kostenloses Konto auf [grafana.com](https://grafana.com) – das kostenlose Kontingent umfasst 10.000 Zeitreihen, 14 Tage Aufbewahrungsdauer und Zugriff auf die gesamte Plattform.

---

## Grundlegende Nutzung

Nach dem Start von Grafana öffnen Sie `http://localhost:3000` und melden Sie sich mit den Standard-Zugangsdaten (`admin` / `admin`) an. Sie werden aufgefordert, ein neues Passwort festzulegen.

### Schritt 1: Datenquelle hinzufügen

1. Navigieren Sie zu **Konfiguration → Datenquellen**.
2. Klicken Sie auf **Datenquelle hinzufügen**.
3. Wählen Sie einen Typ (z. B. Prometheus).
4. Geben Sie die URL ein (z. B. `http://prometheus:9090`) und klicken Sie auf **Speichern & testen**.

### Schritt 2: Ein Dashboard erstellen

1. Klicken Sie auf das **+**-Symbol in der Seitenleiste → **Neues Dashboard**.
2. Klicken Sie auf **Neues Panel hinzufügen**.
3. Schreiben Sie im Abfrageeditor eine Abfrage für Ihre Datenquelle (z. B. einen PromQL-Ausdruck).
4. Wählen Sie einen Visualisierungstyp (Zeitreihe, Statistik, Anzeige, Tabelle usw.).
5. Passen Sie Achsen, Einheiten, Farben, Schwellenwerte und Legenden an.
6. Klicken Sie auf **Übernehmen**, um das Panel zum Dashboard hinzuzufügen.
7. Speichern Sie das Dashboard mit einem aussagekräftigen Namen.

### Schritt 3: Daten mit Explore abfragen

Für Ad-hoc-Untersuchungen verwenden Sie die **Explore**-Ansicht (Seitenleisten-Kompass-Symbol). Sie bietet einen abgeschotteten Abfrageeditor, ohne dass ein Dashboard gespeichert oder erstellt werden muss.

```promql
# Example PromQL queries to run in Explore
rate(node_cpu_seconds_total[5m])
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
count by (job) (up == 0)
```

### Schritt 4: Alarme einrichten

Gehen Sie im Panel-Editor zum **Alert**-Tab:

1. Klicken Sie auf **Alarmregel aus diesem Panel erstellen**.
2. Definieren Sie eine Bedingung (z. B. `MAX() OF query (A) IS ABOVE 90`).
3. Legen Sie das Auswertungsverhalten fest (z. B. alle 1m auswerten, Wartezeit 5m).
4. Fügen Sie einen **Kontaktpunkt** hinzu (Slack, PagerDuty, E-Mail, Webhook usw.).
5. Speichern Sie die Regel.

Alarme werden zentral unter **Alerting → Alarmregeln** verwaltet, mit Unterstützung für Stummschaltungen, Stummschaltungszeitpläne und Benachrichtigungsrichtlinien.

---

## Hauptfunktionen mit Befehlsbeispielen

### 1. Dynamische Dashboards & Vorlagenvariablen

Variablen ermöglichen es Ihnen, Dashboards interaktiv zu gestalten. Beispielsweise kann eine Variable `$job` in einer PromQL-Abfrage verwendet werden:

```promql
rate(http_requests_total{job=~"$job"}[5m])
```

Definieren Sie Variablen unter **Dashboard-Einstellungen → Variablen** – sie können vom Typ Abfrage, Benutzerdefiniert, Intervall, Datenquelle usw. sein.

### 2. Provisionierung (GitOps)

Automatisieren Sie Datenquellen und Dashboards mit YAML-Dateien, die im Provisionierungsverzeichnis von Grafana abgelegt werden (`/etc/grafana/provisioning/`).

**Beispiel für die Provisionierung einer Datenquelle** (`datasources.yaml`):

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://localhost:9090
    isDefault: true
```

**Beispiel für die Provisionierung eines Dashboards** (`dashboards.yaml`):

```yaml
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: 'Provisioned Dashboards'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: false
    options:
      path: /var/lib/grafana/dashboards
```

Legen Sie die Dashboard-JSON-Dateien im angegebenen Pfad ab, und Grafana synchronisiert sie automatisch.

### 3. API & CLI

Grafana bietet eine umfassende REST-API zur Automatisierung.

```bash
# List dashboards
curl -s -u admin:admin http://localhost:3000/api/search?type=dash-db | jq .

# Create a data source
curl -s -X POST -u admin:admin \
  -H "Content-Type: application/json" \
  -d '{
        "name":"MyPrometheus",
        "type":"prometheus",
        "url":"http://prometheus:9090",
        "access":"proxy"
      }' \
  http://localhost:3000/api/datasources
```

Verwenden Sie `grafana-cli` zur Verwaltung von Plugins:

```bash
# Install a panel plugin
grafana-cli plugins install grafana-piechart-panel

# List installed plugins
grafana-cli plugins ls
```

### 4. Explore-Modus (Tiefgehende Fehlersuche)

Mit Explore können Sie Abfragen über Metriken, Logs und Traces hinweg nebeneinander ausführen. So können Sie beispielsweise von einer Metrik mit hoher Latenz zu dem zugehörigen Trace oder Logeintrag springen.

### 5. Einheitliche Alarmierung

Alle Alarmregeln, ob für Prometheus, Loki oder eine SQL-Datenbank, werden an einem Ort verwaltet. Beispiel einer Regeldefinition über die API:

```json
{
  "title": "High CPU alert",
  "condition": "A",
  "data": [
    {
      "refId": "A",
      "relativeTimeRange": { "from": 600, "to": 0 },
      "datasourceUid": "P010D9A9C2F1E4B8C",
      "model": {
        "expr": "avg(node_load1) > 2",
        "intervalMs": 1000,
        "maxDataPoints": 100,
        "refId": "A"
      }
    }
  ]
}
```

### 6. Plugin-Ökosystem

Erweitern Sie Grafana mit Community- und offiziellen Plugins. Durchsuchen Sie den [Grafana Plugins](https://grafana.com/grafana/plugins/)-Katalog. Installation über die UI (Konfiguration → Plugins) oder die CLI.

### 7. Sicherheit & Authentifizierung

Grafana unterstützt mehrere Authentifizierungsmethoden: OAuth (GitHub, Google, GitLab, Okta), SAML, LDAP und Auth Proxy. RBAC kann über die UI oder Provisionierung konfiguriert werden.

Beispiel eines Konfigurationsausschnitts (`grafana.ini`):

```ini
[auth.github]
enabled = true
allow_sign_up = true
client_id = YOUR_GITHUB_CLIENT_ID
client_secret = YOUR_GITHUB_CLIENT_SECRET
scopes = user:email,read:org
```

---

## Fazit

Grafana ist der De-facto-Open-Source-Standard für Observability und befähigt Teams, Daten aus beliebigen Quellen zu vereinheitlichen, zu visualisieren und zu alarmieren. Ob Sie es selbst für einen kleinen Cluster hosten, in Kubernetes skalieren oder das Cloud-Angebot nutzen, Grafana bietet die Flexibilität und Tiefe, die erforderlich ist, um Ihre Systeme gesund zu halten. Seine starke Community, aktive Entwicklung und das umfangreiche Plugin-Ökosystem machen es zu einem unverzichtbaren Werkzeug im modernen DevOps- und SRE-Toolkit.

---

> **Weitere Ressourcen**
>
> - Offizielle Dokumentation: [https://grafana.com/docs/](https://grafana.com/docs/)
> - Community-Foren: [https://community.grafana.com/](https://community.grafana.com/)
> - Grafana Play (Live-Demo): [https://play.grafana.org/](https://play.grafana.org/)
> - Grafana Labs Blog: [https://grafana.com/blog/](https://grafana.com/blog/)