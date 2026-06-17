---
title: 'Grafana: A Plataforma Aberta de Observabilidade'
description: Visualização, monitoramento e alerta unificados para métricas, logs e traces.
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

# Grafana: A Plataforma Aberta de Observabilidade

## O que é o Grafana?

O Grafana é a principal plataforma open‑source de análise e visualização interativa para observabilidade. Ele conecta‑se a qualquer fonte de dados — desde bancos de dados de séries temporais (Prometheus, InfluxDB, Graphite) até backends de registro (Loki, Elasticsearch), sistemas de rastreamento (Tempo, Jaeger), armazenamentos SQL (PostgreSQL, MySQL) e APIs de nuvem (AWS CloudWatch, Azure Monitor). Ele fornece um único “ponto de visualização” para consultar, visualizar, definir alertas e entender suas métricas, logs e traces.

Por ser construído sobre padrões abertos, você evita a dependência de fornecedor. Você pode misturar dados de dezenas de fontes no mesmo dashboard, e a mesma plataforma funciona igualmente bem para monitoramento de infraestrutura, gerenciamento de desempenho de aplicações, análises de negócios ou telemetria IoT.

---

## Por que usar o Grafana?

- **Observabilidade unificada** – reúna métricas, logs, traces e dados de negócios em um único lugar.
- **Visualização rica** – dezenas de tipos de painéis (time series, stat, table, heatmap, geomap, candlestick, logs, traces e mais).
- **Dashboards dinâmicos** – use variáveis de modelo para tornar os dashboards reutilizáveis e interativos.
- **Alertas unificados** – gerencie todas as regras de alerta entre fontes de dados a partir de uma única interface.
- **Modo Explore** – solução de problemas ad‑hoc sem salvar um dashboard.
- **Extensível** – marketplace de plugins para fontes de dados, painéis e aplicativos.
- **Pronto para GitOps** – provisione dashboards, fontes de dados e regras de alerta com arquivos de configuração.
- **Segurança & governança** – organizações, equipes, RBAC granular, OAuth e chaves de API.
- **Auto‑hospedado ou cloud** – execute você mesmo ou use o Grafana Cloud (generoso nível gratuito).

---

## Instalação

### 1. Binário / Pacote

Baixe o `.rpm`, `.deb` ou tarball autônomo da [página de downloads](https://grafana.com/grafana/download) e instale:

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

Execute a imagem oficial do Docker (porta padrão 3000). Monte volumes para dados persistentes:

```bash
docker run -d \
  -p 3000:3000 \
  --name=grafana \
  -v grafana-storage:/var/lib/grafana \
  grafana/grafana:latest
```

### 3. Kubernetes (Helm)

Adicione o repositório Helm do Grafana e implante:

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install my-grafana grafana/grafana \
  --namespace monitoring --create-namespace \
  --set persistence.enabled=true \
  --set adminPassword='admin'
```

### 4. Grafana Cloud

Crie uma conta gratuita em [grafana.com](https://grafana.com) – o nível gratuito inclui 10.000 séries, retenção de 14 dias e acesso a toda a plataforma.

---

## Uso Básico

Após iniciar o Grafana, abra `http://localhost:3000` e faça login com as credenciais padrão (`admin` / `admin`). Será solicitado que você defina uma nova senha.

### Passo 1: Adicionar uma Fonte de Dados

1. Navegue até **Configuração → Fontes de Dados**.
2. Clique em **Adicionar fonte de dados**.
3. Selecione um tipo (ex.: Prometheus).
4. Insira a URL (ex.: `http://prometheus:9090`) e clique em **Salvar e testar**.

### Passo 2: Criar um Dashboard

1. Clique no ícone **+** na barra lateral → **Novo Dashboard**.
2. Clique em **Adicionar um novo painel**.
3. No editor de consultas, escreva uma consulta para sua fonte de dados (ex.: uma expressão PromQL).
4. Escolha um tipo de visualização (Time series, Stat, Gauge, Table, etc.).
5. Personalize eixos, unidades, cores, limites e legendas.
6. Clique em **Aplicar** para adicionar o painel ao dashboard.
7. Salve o dashboard com um nome descritivo.

### Passo 3: Consultar Dados com o Explore

Para investigação ad‑hoc, use a visualização **Explore** (ícone de bússola na barra lateral). Ela fornece um editor de consultas isolado sem a necessidade de salvar ou criar um dashboard.

```promql
# Exemplo de consultas PromQL para executar no Explore
rate(node_cpu_seconds_total[5m])
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
count by (job) (up == 0)
```

### Passo 4: Definir Alertas

No editor de painéis, vá para a guia **Alerta**:

1. Clique em **Criar regra de alerta a partir deste painel**.
2. Defina uma condição (ex.: `MAX() OF query (A) IS ABOVE 90`).
3. Defina o comportamento de avaliação (ex.: avaliar a cada 1m, período pendente de 5m).
4. Adicione um **ponto de contato** (Slack, PagerDuty, Email, webhook, etc.).
5. Salve a regra.

Os alertas são gerenciados centralmente em **Alertas → Regras de alerta**, com suporte para silêncios, períodos de silêncio e políticas de notificação.

---

## Principais Recursos com Exemplos de Comandos

### 1. Dashboards Dinâmicos e Variáveis de Modelo

As variáveis permitem tornar os dashboards interativos. Por exemplo, uma variável `$job` pode ser usada em uma consulta PromQL:

```promql
rate(http_requests_total{job=~"$job"}[5m])
```

Defina variáveis em **Configurações do dashboard → Variáveis** – elas podem ser do tipo Query, Custom, Interval, Data source, etc.

### 2. Provisionamento (GitOps)

Automatize fontes de dados e dashboards com arquivos YAML colocados no diretório de provisionamento do Grafana (`/etc/grafana/provisioning/`).

**Exemplo de provisionamento de fonte de dados** (`datasources.yaml`):

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://localhost:9090
    isDefault: true
```

**Exemplo de provisionamento de dashboard** (`dashboards.yaml`):

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

Coloque os arquivos JSON dos dashboards no caminho especificado, e o Grafana os sincronizará automaticamente.

### 3. API & CLI

O Grafana expõe uma API REST abrangente para automação.

```bash
# Listar dashboards
curl -s -u admin:admin http://localhost:3000/api/search?type=dash-db | jq .

# Criar uma fonte de dados
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

Use `grafana-cli` para gerenciar plugins:

```bash
# Instalar um plugin de painel
grafana-cli plugins install grafana-piechart-panel

# Listar plugins instalados
grafana-cli plugins ls
```

### 4. Modo Explore (Solução Avançada de Problemas)

O Explore permite executar consultas em métricas, logs e traces lado a lado. Por exemplo, saltar de uma métrica de alta latência para o trace ou entrada de log relacionada.

### 5. Alertas Unificados

Todas as regras de alerta, seja para Prometheus, Loki ou um banco de dados SQL, são gerenciadas em um só lugar. Exemplo de definição de regra via API:

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

### 6. Ecossistema de Plugins

Estenda o Grafana com plugins da comunidade e oficiais. Navegue pelo catálogo de [plugins do Grafana](https://grafana.com/grafana/plugins/). Instale via interface (Configuração → Plugins) ou CLI.

### 7. Segurança e Autenticação

O Grafana suporta vários métodos de autenticação: OAuth (GitHub, Google, GitLab, Okta), SAML, LDAP e Auth Proxy. O RBAC pode ser configurado via interface ou provisionamento.

Exemplo de trecho de configuração (`grafana.ini`):

```ini
[auth.github]
enabled = true
allow_sign_up = true
client_id = YOUR_GITHUB_CLIENT_ID
client_secret = YOUR_GITHUB_CLIENT_SECRET
scopes = user:email,read:org
```

---

## Conclusão

O Grafana é o padrão open‑source de facto para observabilidade, capacitando equipes a unificar, visualizar e alertar sobre dados de qualquer fonte. Seja executando‑o auto‑hospedado para um pequeno cluster, implantando‑o no Kubernetes em escala ou usando a oferta em nuvem, o Grafana fornece a flexibilidade e profundidade necessárias para manter seus sistemas saudáveis. Sua comunidade forte, desenvolvimento ativo e ecossistema extenso de plugins o tornam uma ferramenta indispensável no kit moderno de DevOps e SRE.

> **Recursos Adicionais**
>
> - Documentação oficial: [https://grafana.com/docs/](https://grafana.com/docs/)
> - Fóruns da comunidade: [https://community.grafana.com/](https://community.grafana.com/)
> - Grafana Play (demo ao vivo): [https://play.grafana.org/](https://play.grafana.org/)
> - Blog do Grafana Labs: [https://grafana.com/blog/](https://grafana.com/blog/)