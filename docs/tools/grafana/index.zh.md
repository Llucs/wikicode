---
title: Grafana: 开放的可观测性平台
description: 统一的指标、日志和追踪可视化、监控与告警。
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

# Grafana: 开放的可观测性平台

## 什么是 Grafana？

Grafana 是领先的开源分析和交互式可视化平台，用于可观测性。它连接到任何数据源——从时序数据库（Prometheus、InfluxDB、Graphite）到日志后端（Loki、Elasticsearch）、链路追踪系统（Tempo、Jaeger）、SQL 存储（PostgreSQL、MySQL）以及云 API（AWS CloudWatch、Azure Monitor）。它提供了一个单一的“统一视图”来查询、可视化、设置告警并理解您的指标、日志和追踪。

由于 Grafana 建立在开放标准之上，您可以避免供应商锁定。您可以混合来自数十个源的数据到同一个仪表盘中，并且同一个平台同样适用于基础设施监控、应用性能管理、业务分析或 IoT 遥测。

---

## 为什么使用 Grafana？

- **统一的可观测性** – 将指标、日志、追踪和业务数据汇集到一个地方。
- **丰富的可视化** – 数十种面板类型（时序、统计、表格、热力图、地理地图、K 线图、日志、追踪等）。
- **动态仪表盘** – 使用模板变量使仪表盘可复用且交互式。
- **统一告警** – 从单一界面管理所有数据源的告警规则。
- **探索模式** – 无需保存仪表盘即可进行临时故障排查。
- **可扩展** – 提供数据源、面板和应用的插件市场。
- **支持 GitOps** – 通过配置文件预配仪表盘、数据源和告警规则。
- **安全与治理** – 组织、团队、细粒度 RBAC、OAuth 和 API 密钥。
- **自托管或云** – 自行运行或使用 Grafana Cloud（慷慨的免费层）。

---

## 安装

### 1. 二进制/包

从[下载页面](https://grafana.com/grafana/download)下载 `.rpm`、`.deb` 或独立压缩包并安装：

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

运行官方 Docker 镜像（默认端口 3000）。挂载卷以持久化数据：

```bash
docker run -d \
  -p 3000:3000 \
  --name=grafana \
  -v grafana-storage:/var/lib/grafana \
  grafana/grafana:latest
```

### 3. Kubernetes（Helm）

添加 Grafana Helm 仓库并部署：

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install my-grafana grafana/grafana \
  --namespace monitoring --create-namespace \
  --set persistence.enabled=true \
  --set adminPassword='admin'
```

### 4. Grafana Cloud

在 [grafana.com](https://grafana.com) 创建一个免费账户 – 免费层包括 10,000 个序列、14 天保留期以及对完整平台的访问权限。

---

## 基本使用

启动 Grafana 后，打开 `http://localhost:3000`，使用默认凭据（`admin` / `admin`）登录。系统会要求您设置新密码。

### 步骤 1：添加数据源

1. 导航到 **配置 → 数据源**。
2. 点击 **添加数据源**。
3. 选择一个类型（例如 Prometheus）。
4. 输入 URL（例如 `http://prometheus:9090`）并点击 **保存并测试**。

### 步骤 2：构建仪表盘

1. 点击侧边栏中的 **+** 图标 → **新建仪表盘**。
2. 点击 **添加新面板**。
3. 在查询编辑器中，为您的数据源编写一个查询（例如 PromQL 表达式）。
4. 选择一种可视化类型（时序、统计、仪表盘、表格等）。
5. 自定义坐标轴、单位、颜色、阈值和图例。
6. 点击 **应用** 将面板添加到仪表盘。
7. 使用描述性名称保存仪表盘。

### 步骤 3：使用探索功能查询数据

对于临时调查，使用 **探索** 视图（侧边栏指南针图标）。它提供了一个沙盒查询编辑器，无需保存或构建仪表盘。

```promql
# Example PromQL queries to run in Explore
rate(node_cpu_seconds_total[5m])
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
count by (job) (up == 0)
```

### 步骤 4：设置告警

在面板编辑器中，转到 **告警** 选项卡：

1. 点击 **从此面板创建告警规则**。
2. 定义一个条件（例如 `MAX() OF query (A) IS ABOVE 90`）。
3. 设置评估行为（例如每 1 分钟评估一次，等待期 5 分钟）。
4. 添加一个 **联系人**（Slack、PagerDuty、电子邮件、Webhook 等）。
5. 保存规则。

告警在 **告警 → 告警规则** 下集中管理，支持静音、静默时间和通知策略。

---

## 关键功能及命令示例

### 1. 动态仪表盘与模板变量

变量允许您使仪表盘具有交互性。例如，变量 `$job` 可用于 PromQL 查询：

```promql
rate(http_requests_total{job=~"$job"}[5m])
```

在 **仪表盘设置 → 变量** 中定义变量 – 它们可以是查询、自定义、间隔、数据源等类型。

### 2. 预配（GitOps）

使用放置在 Grafana 预配目录（`/etc/grafana/provisioning/`）中的 YAML 文件自动化数据源和仪表盘。

**数据源预配示例** (`datasources.yaml`)：

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://localhost:9090
    isDefault: true
```

**仪表盘预配示例** (`dashboards.yaml`)：

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

将仪表盘 JSON 文件放置在指定路径，Grafana 将自动同步它们。

### 3. API 与 CLI

Grafana 公开了全面的 REST API，用于自动化。

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

使用 `grafana-cli` 管理插件：

```bash
# Install a panel plugin
grafana-cli plugins install grafana-piechart-panel

# List installed plugins
grafana-cli plugins ls
```

### 4. 探索模式（深度故障排查）

探索允许您并排运行跨指标、日志和追踪的查询。例如，从高延迟指标跳转到相关的追踪或日志条目。

### 5. 统一告警

所有告警规则，无论是针对 Prometheus、Loki 还是 SQL 数据库，都在一个地方管理。通过 API 定义规则的示例：

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

### 6. 插件生态系统

使用社区和官方插件扩展 Grafana。浏览 [Grafana 插件](https://grafana.com/grafana/plugins/) 目录。通过 UI（配置 → 插件）或 CLI 安装。

### 7. 安全与认证

Grafana 支持多种认证方法：OAuth（GitHub、Google、GitLab、Okta）、SAML、LDAP 和 Auth Proxy。RBAC 可以通过 UI 或预配配置。

示例配置片段 (`grafana.ini`)：

```ini
[auth.github]
enabled = true
allow_sign_up = true
client_id = YOUR_GITHUB_CLIENT_ID
client_secret = YOUR_GITHUB_CLIENT_SECRET
scopes = user:email,read:org
```

---

## 结论

Grafana 是可观测性领域事实上的开源标准，赋能团队统一、可视化和告警来自任何源的数据。无论您是自托管一个小型集群，在 Kubernetes 中大规模部署，还是使用云服务，Grafana 都提供了保持系统健康所需的灵活性和深度。其强大的社区、活跃的开发以及广泛的插件生态系统使其成为现代 DevOps 和 SRE 工具包中不可或缺的工具。

---

> **更多资源**
>
> - 官方文档：[https://grafana.com/docs/](https://grafana.com/docs/)
> - 社区论坛：[https://community.grafana.com/](https://community.grafana.com/)
> - Grafana Play（在线演示）：[https://play.grafana.org/](https://play.grafana.org/)
> - Grafana Labs 博客：[https://grafana.com/blog/](https://grafana.com/blog/)