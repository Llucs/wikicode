---
title: Grafana : la plateforme d'observabilité ouverte
description: Visualisation, monitoring et alerting unifiés pour les métriques, logs et traces.
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

# Grafana : la plateforme d'observabilité ouverte

## Qu'est-ce que Grafana ?

Grafana est la principale plateforme open-source d'analytique et de visualisation interactive pour l'observabilité. Elle se connecte à n'importe quelle source de données — des bases de données de séries temporelles (Prometheus, InfluxDB, Graphite) aux backends de logs (Loki, Elasticsearch), en passant par les systèmes de traçage (Tempo, Jaeger), les bases SQL (PostgreSQL, MySQL) et les API cloud (AWS CloudWatch, Azure Monitor). Elle offre un « panneau de verre » unique pour interroger, visualiser, définir des alertes et comprendre vos métriques, logs et traces.

Parce que Grafana est construit sur des standards ouverts, vous évitez l'enfermement propriétaire. Vous pouvez mélanger des données de dizaines de sources dans le même tableau de bord, et la même plateforme fonctionne aussi bien pour la surveillance d'infrastructure, la gestion des performances applicatives, l'analytique métier ou la télémétrie IoT.

---

## Pourquoi utiliser Grafana ?

- **Unified observability** – regroupez métriques, logs, traces et données métier en un seul endroit.
- **Rich visualization** – des dizaines de types de panneaux (time series, stat, table, heatmap, geomap, candlestick, logs, traces, etc.).
- **Dynamic dashboards** – utilisez des variables de template pour rendre les tableaux de bord réutilisables et interactifs.
- **Unified alerting** – gérez toutes les règles d'alertes à travers les sources de données depuis une interface unique.
- **Explore mode** – dépannage ad‑hoc sans enregistrer un tableau de bord.
- **Extensible** – marketplace de plugins pour sources de données, panneaux et applications.
- **GitOps‑ready** – provisionnez les tableaux de bord, sources de données et règles d'alertes avec des fichiers de configuration.
- **Security & governance** – organisations, équipes, RBAC fin, OAuth et clés API.
- **Self‑hosted or cloud** – faites-le tourner vous-même ou utilisez Grafana Cloud (offre gratuite généreuse).

---

## Installation

### 1. Binary / Package

Téléchargez le fichier `.rpm`, `.deb` ou l'archive autonome depuis la [page de téléchargement](https://grafana.com/grafana/download) et installez-le :

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

Exécutez l'image Docker officielle (port par défaut 3000). Montez des volumes pour les données persistantes :

```bash
docker run -d \
  -p 3000:3000 \
  --name=grafana \
  -v grafana-storage:/var/lib/grafana \
  grafana/grafana:latest
```

### 3. Kubernetes (Helm)

Ajoutez le dépôt Helm de Grafana et déployez :

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install my-grafana grafana/grafana \
  --namespace monitoring --create-namespace \
  --set persistence.enabled=true \
  --set adminPassword='admin'
```

### 4. Grafana Cloud

Créez un compte gratuit sur [grafana.com](https://grafana.com) – l'offre gratuite inclut 10 000 séries, une rétention de 14 jours et l'accès à la plateforme complète.

---

## Utilisation de base

Après avoir démarré Grafana, ouvrez `http://localhost:3000` et connectez-vous avec les identifiants par défaut (`admin` / `admin`). Il vous sera demandé de définir un nouveau mot de passe.

### Étape 1 : Ajouter une source de données

1. Accédez à **Configuration → Data Sources**.
2. Cliquez sur **Add data source**.
3. Sélectionnez un type (par ex., Prometheus).
4. Saisissez l'URL (par ex., `http://prometheus:9090`) et cliquez sur **Save & test**.

### Étape 2 : Créer un tableau de bord

1. Cliquez sur l'icône **+** dans la barre latérale → **New Dashboard**.
2. Cliquez sur **Add a new panel**.
3. Dans l'éditeur de requêtes, écrivez une requête pour votre source de données (par ex., une expression PromQL).
4. Choisissez un type de visualisation (Time series, Stat, Gauge, Table, etc.).
5. Personnalisez les axes, les unités, les couleurs, les seuils et les légendes.
6. Cliquez sur **Apply** pour ajouter le panneau au tableau de bord.
7. Enregistrez le tableau de bord avec un nom descriptif.

### Étape 3 : Interroger les données avec Explore

Pour une investigation ad‑hoc, utilisez la vue **Explore** (icône de boussole dans la barre latérale). Elle fournit un éditeur de requêtes en mode bac à sable sans avoir besoin d'enregistrer ou de construire un tableau de bord.

```promql
# Example PromQL queries to run in Explore
rate(node_cpu_seconds_total[5m])
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
count by (job) (up == 0)
```

### Étape 4 : Définir des alertes

Dans l'éditeur de panneaux, allez dans l'onglet **Alert** :

1. Cliquez sur **Create alert rule from this panel**.
2. Définissez une condition (par ex., `MAX() OF query (A) IS ABOVE 90`).
3. Définissez le comportement d'évaluation (par ex., évaluer toutes les 1m, période d'attente 5m).
4. Ajoutez un **contact point** (Slack, PagerDuty, Email, webhook, etc.).
5. Enregistrez la règle.

Les alertes sont gérées centralement sous **Alerting → Alert rules**, avec la prise en charge des silences, des plages de muting et des politiques de notification.

---

## Fonctionnalités clés avec exemples de commandes

### 1. Tableaux de bord dynamiques et variables de template

Les variables vous permettent de rendre les tableaux de bord interactifs. Par exemple, une variable `$job` peut être utilisée dans une requête PromQL :

```promql
rate(http_requests_total{job=~"$job"}[5m])
```

Définissez les variables dans **Dashboard settings → Variables** – elles peuvent être de type Query, Custom, Interval, Data source, etc.

### 2. Provisioning (GitOps)

Automatisez les sources de données et les tableaux de bord avec des fichiers YAML placés dans le répertoire de provisioning de Grafana (`/etc/grafana/provisioning/`).

**Exemple de provision de source de données** (`datasources.yaml`) :

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://localhost:9090
    isDefault: true
```

**Exemple de provision de tableau de bord** (`dashboards.yaml`) :

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

Placez les fichiers JSON des tableaux de bord dans le chemin spécifié, et Grafana les synchronisera automatiquement.

### 3. API & CLI

Grafana expose une API REST complète pour l'automatisation.

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

Utilisez `grafana-cli` pour gérer les plugins :

```bash
# Install a panel plugin
grafana-cli plugins install grafana-piechart-panel

# List installed plugins
grafana-cli plugins ls
```

### 4. Explore Mode (dépannage avancé)

Explore vous permet d'exécuter des requêtes sur les métriques, logs et traces côte à côte. Par exemple, passez d'une métrique de haute latence à la trace ou l'entrée de log correspondante.

### 5. Unified alerting

Toutes les règles d'alertes, que ce soit pour Prometheus, Loki ou une base de données SQL, sont gérées à un même endroit. Exemple de définition de règle via l'API :

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

### 6. Écosystème de plugins

Étendez Grafana avec des plugins communautaires et officiels. Parcourez le catalogue des [plugins Grafana](https://grafana.com/grafana/plugins/). Installez via l'UI (Configuration → Plugins) ou CLI.

### 7. Sécurité et authentification

Grafana prend en charge plusieurs méthodes d'authentification : OAuth (GitHub, Google, GitLab, Okta), SAML, LDAP et Auth Proxy. Le RBAC peut être configuré via l'UI ou le provisioning.

Exemple d'extrait de configuration (`grafana.ini`) :

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

Grafana est le standard open‑source de facto pour l'observabilité, permettant aux équipes d'unifier, visualiser et alerter sur les données de n'importe quelle source. Que vous l'exécutiez en auto‑hébergement pour un petit cluster, que vous le déployiez dans Kubernetes à grande échelle, ou que vous utilisiez l'offre cloud, Grafana offre la flexibilité et la profondeur nécessaires pour maintenir vos systèmes en bonne santé. Sa communauté solide, son développement actif et son vaste écosystème de plugins en font un outil indispensable dans la boîte à outils moderne des DevOps et SRE.

---

> **Ressources complémentaires**
>
> - Documentation officielle : [https://grafana.com/docs/](https://grafana.com/docs/)
> - Forums communautaires : [https://community.grafana.com/](https://community.grafana.com/)
> - Grafana Play (démo en direct) : [https://play.grafana.org/](https://play.grafana.org/)
> - Blog de Grafana Labs : [https://grafana.com/blog/](https://grafana.com/blog/)