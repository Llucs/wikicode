---
title: Grafana: The Open Observability Platform
description: Unified visualization, monitoring, and alerting for metrics, logs, and traces.
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

# Grafana: The Open Observability Platform

## What Is Grafana?

Grafana is the leading open-source analytics and interactive visualization platform for observability. It connects to any data source — from time‑series databases (Prometheus, InfluxDB, Graphite) to logging backends (Loki, Elasticsearch), tracing systems (Tempo, Jaeger), SQL stores (PostgreSQL, MySQL), and cloud APIs (AWS CloudWatch, Azure Monitor). It provides a single “pane of glass” to query, visualize, set alerts on, and understand your metrics, logs, and traces.

Because Grafana is built on open standards, you avoid vendor lock‑in. You can mix data from dozens of sources in the same dashboard, and the same platform works equally well for infrastructure monitoring, application performance management, business analytics, or IoT telemetry.

---

## Why Use Grafana?

- **Unified observability** – bring metrics, logs, traces, and business data together in one place.
- **Rich visualization** – dozens of panel types (time series, stat, table, heatmap, geomap, candlestick, logs, traces, and more).
- **Dynamic dashboards** – use template variables to make dashboards reusable and interactive.
- **Unified alerting** – manage all alert rules across data sources from a single interface.
- **Explore mode** – ad‑hoc troubleshooting without saving a dashboard.
- **Extensible** – plugin marketplace for data sources, panels, and apps.
- **GitOps‑ready** – provision dashboards, data sources, and alert rules with configuration files.
- **Security & governance** – organizations, teams, fine‑grained RBAC, OAuth, and API keys.
- **Self‑hosted or cloud** – run it yourself or use Grafana Cloud (generous free tier).

---

## Installation

### 1. Binary / Package

Download the `.rpm`, `.deb`, or standalone tarball from the [downloads page](https://grafana.com/grafana/download) and install it:

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

Run the official Docker image (default port 3000). Mount volumes for persistent data:

```bash
docker run -d \
  -p 3000:3000 \
  --name=grafana \
  -v grafana-storage:/var/lib/grafana \
  grafana/grafana:latest
```

### 3. Kubernetes (Helm)

Add the Grafana Helm repository and deploy:

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install my-grafana grafana/grafana \
  --namespace monitoring --create-namespace \
  --set persistence.enabled=true \
  --set adminPassword='admin'
```

### 4. Grafana Cloud

Create a free account at [grafana.com](https://grafana.com) – the free tier includes 10,000 series, 14‑day retention, and access to the full platform.

---

## Basic Usage

After starting Grafana, open `http://localhost:3000` and log in with the default credentials (`admin` / `admin`). You will be asked to set a new password.

### Step 1: Add a Data Source

1. Navigate to **Configuration → Data Sources**.
2. Click **Add data source**.
3. Select a type (e.g., Prometheus).
4. Enter the URL (e.g., `http://prometheus:9090`) and click **Save & test**.

### Step 2: Build a Dashboard

1. Click the **+** icon in the sidebar → **New Dashboard**.
2. Click **Add a new panel**.
3. In the query editor, write a query for your data source (e.g., a PromQL expression).
4. Choose a visualization type (Time series, Stat, Gauge, Table, etc.).
5. Customise axes, units, colors, thresholds, and legends.
6. Click **Apply** to add the panel to the dashboard.
7. Save the dashboard with a descriptive name.

### Step 3: Query Data with Explore

For ad‑hoc investigation, use the **Explore** view (sidebar compass icon). It provides a sandboxed query editor without the need to save or build a dashboard.

```promql
# Example PromQL queries to run in Explore
rate(node_cpu_seconds_total[5m])
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
count by (job) (up == 0)
```

### Step 4: Set Alerts

In the panel editor, go to the **Alert** tab:

1. Click **Create alert rule from this panel**.
2. Define a condition (e.g., `MAX() OF query (A) IS ABOVE 90`).
3. Set evaluation behaviour (e.g., evaluate every 1m, pending period 5m).
4. Add a **contact point** (Slack, PagerDuty, Email, webhook, etc.).
5. Save the rule.

Alerts are managed centrally under **Alerting → Alert rules**, with support for silences, mute timings, and notification policies.

---

## Key Features with Command Examples

### 1. Dynamic Dashboards & Template Variables

Variables allow you to make dashboards interactive. For example, a variable `$job` can be used in a PromQL query:

```promql
rate(http_requests_total{job=~"$job"}[5m])
```

Define variables in **Dashboard settings → Variables** – they can be of type Query, Custom, Interval, Data source, etc.

### 2. Provisioning (GitOps)

Automate data sources and dashboards with YAML files placed in Grafana’s provisioning directory (`/etc/grafana/provisioning/`).

**Datasource provision example** (`datasources.yaml`):

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://localhost:9090
    isDefault: true
```

**Dashboard provision example** (`dashboards.yaml`):

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

Place dashboard JSON files in the specified path, and Grafana will sync them automatically.

### 3. API & CLI

Grafana exposes a comprehensive REST API for automation.

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

Use `grafana-cli` to manage plugins:

```bash
# Install a panel plugin
grafana-cli plugins install grafana-piechart-panel

# List installed plugins
grafana-cli plugins ls
```

### 4. Explore Mode (Deep Troubleshooting)

Explore allows you to run queries across metrics, logs, and traces side‑by‑side. For example, jump from a high‑latency metric to the related trace or log entry.

### 5. Unified Alerting

All alert rules, whether for Prometheus, Loki, or a SQL database, are managed in one place. Example rule definition via API:

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

### 6. Plugin Ecosystem

Extend Grafana with community and official plugins. Browse the [Grafana Plugins](https://grafana.com/grafana/plugins/) catalog. Install via UI (Configuration → Plugins) or CLI.

### 7. Security & Authentication

Grafana supports multiple authentication methods: OAuth (GitHub, Google, GitLab, Okta), SAML, LDAP, and Auth Proxy. RBAC can be configured via the UI or provisioning.

Example configuration snippet (`grafana.ini`):

```ini
[auth.github]
enabled = true
allow_sign_up = true
client_id = YOUR_GITHUB_CLIENT_ID
client_secret = YOUR_GITHUB_CLIENT_SECRET
scopes = user:email,read:org
```

---

## Conclusion

Grafana is the de‑facto open‑source standard for observability, empowering teams to unify, visualise, and alert on data from any source. Whether you run it self‑hosted for a small cluster, deploy it in Kubernetes at scale, or use the cloud offering, Grafana provides the flexibility and depth needed to keep your systems healthy. Its strong community, active development, and extensive plugin ecosystem make it an indispensable tool in the modern DevOps and SRE toolkit.

---

> **Further Resources**
>
> - Official documentation: [https://grafana.com/docs/](https://grafana.com/docs/)
> - Community forums: [https://community.grafana.com/](https://community.grafana.com/)
> - Grafana Play (live demo): [https://play.grafana.org/](https://play.grafana.org/)
> - Grafana Labs blog: [https://grafana.com/blog/](https://grafana.com/blog/)