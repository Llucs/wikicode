---
title: Trivy
description: Trivy é um scanner de segurança de código aberto e tudo-em-um para detectar vulnerabilidades, más configurações, segredos e licenças em contêineres, Kubernetes, repositórios de código e nuvem.
created: 2026-06-17
tags:
  - security
  - devsecops
  - scanning
  - container-security
  - kubernetes
  - opensource
status: draft
---

# Trivy

## O que é o Trivy?

Trivy (pronuncia-se **"tri-vee"**, um trocadilho com "trivial") é um scanner de segurança de código aberto criado pela Aqua Security. Projetado para tornar a varredura de segurança trivial para equipes DevOps, ele detecta vulnerabilidades, más configurações, segredos e problemas de licenciamento em imagens de contêineres, sistemas de arquivos, repositórios Git, clusters Kubernetes e ambientes de nuvem.

**História**  
Trivy foi criado em 2019 por Teppei Fukuda (knqyf263) na Aqua Security como uma CLI leve para vulnerabilidades em imagens de contêineres. Rapidamente se expandiu para cobrir infraestrutura como código (IaC), segredos, Kubernetes e geração de Lista de Materiais de Software (SBOM), tornando-se um padrão unificado em fluxos de trabalho DevSecOps.

## Por que Trivy?

Desenvolvedores e equipes de segurança escolhem Trivy porque ele:

- **Unifica vários scanners** – uma ferramenta para vulnerabilidades, más configurações, segredos, licenças e SBOM.
- **É fácil de instalar** – um único comando ou binário, sem necessidade de configuração de banco de dados.
- **É rápido e preciso** – combina múltiplos bancos de dados de vulnerabilidades (NVD, GHSA, OSV, RedHat, etc.), armazena resultados em cache e verifica o status de exploração (EPSS, CVSS) para minimizar falsos positivos.
- **Integra-se em qualquer lugar** – suporte nativo para CI/CD (GitHub Actions, GitLab CI, Jenkins, CircleCI), registries de contêineres (Harbor, AWS ECR, GCR) e Kubernetes.

## Instalação

Trivy pode ser instalado via gerenciadores de pacotes, Docker, Go ou diretamente dos lançamentos do GitHub.

```bash
# macOS (Homebrew)
brew install trivy

# Debian/Ubuntu (add official repository)
sudo apt-get install trivy

# RHEL/CentOS (add official repository)
sudo yum install trivy

# Docker
docker pull aquasec/trivy

# Go
go install github.com/aquasecurity/trivy/cmd/trivy@latest
```

Para outros sistemas (Windows, binário estático, etc.) consulte o [guia de instalação oficial](https://trivy.dev/latest/getting-started/installation/).

## Uso Básico

Trivy fornece vários subcomandos (`image`, `fs`, `repo`, `config`, `k8s`). Aqui estão os mais comuns:

### Escanear uma imagem de contêiner em busca de vulnerabilidades

```bash
trivy image nginx:alpine
```

### Escanear com filtro de gravidade e saída JSON

```bash
trivy image --severity CRITICAL,HIGH --format json nginx:alpine
```

### Escanear sistema de arquivos local (vulnerabilidades, segredos, configurações incorretas)

```bash
# Padrão: escaneia pacotes do SO e dependências de linguagem
trivy fs .

# Especifique múltiplos scanners
trivy fs --scanners vuln,secret,config .
```

### Escanear um repositório Git remoto

```bash
trivy repo https://github.com/knqyf263/vuln-image
```

### Escanear modelos IaC (Terraform, Dockerfile, Kubernetes YAML, CloudFormation, Helm)

```bash
trivy config ./my-terraform-project/
```

### Escanear um cluster Kubernetes

```bash
trivy k8s cluster     # cluster inteiro
trivy k8s node        # nó específico
trivy k8s deployment  # varredura de deployment
```

### Gerar uma Lista de Materiais de Software (SBOM)

```bash
# Formato CycloneDX
trivy image --format cyclonedx --output alpine.cdx.json alpine:3.15

# Formato SPDX
trivy image --format spdx-json --output alpine.spdx.json alpine:3.15
```

### Escanear por segredos em um repositório

```bash
trivy fs --scanners secret --severity HIGH,CRITICAL .
```

## Principais Recursos

### 1. Varredura de vulnerabilidades
Trivy cobre pacotes do SO (Alpine, Debian, Ubuntu, CentOS, RHEL, etc.) e dependências de aplicativos (npm, pip, bundler, cargo, Maven, módulos Go, NuGet, Composer e mais). Ele atualiza seu banco de dados de vulnerabilidades automaticamente.

```bash
# Escanear uma imagem e mostrar apenas vulnerabilidades corrigíveis
trivy image --ignore-unfixed alpine:3.15
```

### 2. Varredura de Infraestrutura como Código (IaC)
Detecta configurações incorretas em Terraform, Dockerfiles, Kubernetes YAML, CloudFormation e Helm charts usando um conjunto rico de políticas integradas.

```bash
# Escanear um diretório de arquivos Terraform
trivy config --tf-exclude-downloaded-modules ./terraform/
```

### 3. Detecção de segredos
Identifica credenciais hardcoded, chaves de API, tokens e outros segredos usando correspondência de padrões e análise de entropia.

```bash
# Escanear diretório local em busca de segredos com alta confiança
trivy fs --scanners secret --secret-config trivy-secret.yaml .
```

### 4. Geração de SBOM e conformidade de licenças
Exporta uma Lista de Materiais de Software nos formatos CycloneDX ou SPDX e audita licenças de dependências.

```bash
# Gerar SBOM e verificar licenças
trivy image --format cyclonedx --licenses alpine:3.15
```

### 5. Auditoria de segurança Kubernetes
Escaneie todo o seu cluster em busca de imagens vulneráveis, configurações RBAC inseguras e segredos expostos.

```bash
# Varredura completa do cluster
trivy k8s cluster --report summary
```

### 6. Alto desempenho e cache
Trivy armazena em cache as atualizações do banco de dados de vulnerabilidades e a análise de camadas de imagem, tornando varreduras repetidas extremamente rápidas.

```bash
# Limpar cache e escanear de novo
trivy image --clear-cache --no-cache alpine:latest
```

### 7. Múltiplos formatos de saída
Suporta saída em tabela, JSON, SARIF, HTML, CycloneDX, SPDX e mais para integração com outras ferramentas.

```bash
# Saída SARIF (útil para GitHub Code Scanning)
trivy image --format sarif --output results.sarif nginx:alpine
```

## Exemplo de Integração: GitHub Actions

Trivy integra-se nativamente com GitHub Actions. O workflow abaixo escanea cada push em busca de vulnerabilidades críticas e segredos.

```yaml
name: Trivy Scan
on: [push]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Trivy filesystem scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
```

## Recursos

- **Documentação oficial:** <https://trivy.dev>
- **Repositório GitHub:** <https://github.com/aquasecurity/trivy>
- **Notas de versão:** <https://github.com/aquasecurity/trivy/releases>

---

*Trivy torna a varredura de segurança trivial – um binário, sem configuração e uma visão unificada dos riscos da sua cadeia de suprimentos de software.*