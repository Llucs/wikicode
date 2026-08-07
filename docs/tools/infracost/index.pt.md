---
title: Infracost – Estimativa de custos em nuvem em tempo real para Infraestrutura como Código
description: Um guia prático para o Infracost, um CLI de código aberto que estima custos de nuvem a partir de Terraform, CloudFormation e CDK antes da implantação.
created: 2026-08-07
tags:
  - infracost
  - terraform
  - finops
  - cloud-cost
  - infrastructure-as-code
  - devtools
status: draft
---

# Infracost

O Infracost é uma ferramenta de código aberto, pensada para desenvolvedores, que leva **estimativas de custos de nuvem em tempo real** diretamente para o fluxo de trabalho de infraestrutura como código (IaC). Aponte-o para um projeto Terraform, Terragrunt, CloudFormation ou AWS CDK, e ele produz um detalhamento mensal de custos — antes mesmo de qualquer recurso ser implantado.

Esta página aborda o que é o Infracost, por que as equipes o adotam, como instalá-lo e usá-lo, e os principais recursos que o tornam um complemento padrão para o Terraform e outras cadeias de ferramentas IaC.

---

## O que é o Infracost?

O Infracost é uma ferramenta de linha de comando (e um painel SaaS complementar) que analisa definições e planos de IaC, consulta dados de preços em tempo real da AWS, Azure e Google Cloud e informa exatamente quanto os recursos custarão por mês. Ele funciona tanto com **código estático** quanto com **arquivos de plano do Terraform**, o que significa que pode mostrar o impacto no custo de uma alteração proposta antes de ela ser aplicada.

O projeto foi lançado em 2020 e rapidamente se tornou a camada de estimativa de custos de facto para fluxos de trabalho com Terraform. O CLI principal é gratuito e de código aberto, enquanto o painel opcional Infracost Cloud adiciona visibilidade para toda a equipe, orçamentos e análise de tendências históricas.

```
$ infracost breakdown --path .
✔ Extracting only cost-related params from terraform
  Evaluating usage file...
  Calculating cost estimates...

Project: my-project

 Name                                               Monthly Qty  Unit                        Monthly Cost
 ---------------------------------------------------------------------------------------------------------
 aws_instance.web_server
 ├─ Instance usage (Linux/UNIX, on-demand, m5.large)  730          hours                          $100.74
 └─ root_block_device
    └─ General Purpose SSD storage (gp3)               20          GB                              $1.60
 aws_s3_bucket.assets
 └─ Storage (standard)                                 50          GB                              $1.15
 ---------------------------------------------------------------------------------------------------------
 OVERALL TOTAL                                                                                     $103.49
```

---

## Por que o Infracost?

O gerenciamento tradicional de custos de nuvem é *reativo*: a fatura chega no final do mês e as equipes correm para descobrir o que aconteceu. O Infracost promove **FinOps shift-left** — identificando decisões caras de infraestrutura no momento em que são tomadas:

- **Durante a revisão de código** — comentários em PRs mostram a diferença de custo (`+$50.12`) para que revisores possam rejeitar alterações acima do orçamento.
- **No editor** — extensões para VS Code e JetBrains mostram custos inline enquanto você digita HCL.
- **Em CI/CD** — pipelines podem falhar por regressões de custo, tags ausentes ou violações de orçamento antes da implantação.
- **No terminal** — um comando rápido `breakdown` responde "quanto custa este módulo?" sem calculadora ou planilha.

Como o Infracost lê os mesmos artefatos de código e plano que os engenheiros já produzem, não há instrumentação extra nem divergência em relação ao que está realmente implantado.

---

## Plataformas suportadas

| Ferramenta IaC | Nuvens          | Observações                                      |
|----------------|-----------------|--------------------------------------------------|
| Terraform HCL  | AWS, Azure, GCP | Cobertura completa de recursos e perfis de uso   |
| Terragrunt     | AWS, Azure, GCP | Detecta projetos Terragrunt automaticamente      |
| Terraform plan | AWS, Azure, GCP | Saída de `terraform show -json`                  |
| CloudFormation | AWS             | Suporte a modelos e stack sets                   |
| AWS CDK        | AWS             | Via modelos CloudFormation sintetizados           |

Recursos não suportados são relatados como "skipped", com uma mensagem e um link para a documentação de cobertura de recursos, para que a saída nunca apresente informações incorretas sobre custos silenciosamente.

---

## Instalação

### Homebrew (macOS / Linux)

```bash
brew install infracost
```

### Shell script (Linux / macOS)

```bash
curl -fsSL https://raw.githubusercontent.com/infracost/infracost/master/scripts/install.sh | sh
```

### Windows (Scoop)

```powershell
scoop bucket add infracost https://github.com/infracost/infracost
scoop install infracost
```

### Docker

```bash
docker pull infracost/infracost
```

### Verifique a instalação

```bash
infracost --version
infracost --help
```

---

## Autenticação

O Infracost exige uma chave de API porque consulta APIs de preços de nuvem em tempo real. Crie uma conta gratuita em [infracost.io/dashboard](https://www.infracost.io) e faça login pelo CLI:

```bash
infracost auth login
```

Como alternativa, exporte a chave de API diretamente para ambientes de CI:

```bash
export INFRACOST_API_KEY=my-api-key
```

Para usuários que não podem enviar dados de preços para a API hospedada do Infracost, o CLI oferece suporte a uma fonte de preços auto-hospedada (`INFRACOST_PRICING_API_ENDPOINT`) para ambientes isolados (air-gapped).

---

## Uso básico

### 1. Detalhamento de custos de um diretório Terraform

```bash
infracost breakdown --path . --format table
```

Isso avalia o HCL no diretório atual e exibe uma tabela mensal de custos recurso por recurso. Os formatos suportados incluem `table`, `json`, `html`, `markdown`, `sarif` e `github-comment`.

### 2. Detalhamento de custos de um plano do Terraform

A visão mais precisa vem do plano, pois ele inclui contexto como `count`, `for_each` e lógica condicional:

```bash
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
infracost breakdown --terraform-plan-json plan.json --show-skipped
```

A flag `--show-skipped` lista os recursos que o Infracost não conseguiu precificar, para que você possa avaliar a cobertura.

### 3. Modo diff

O modo diff mostra a **mudança de custo** entre dois estados — normalmente o estado atualmente implantado e a alteração proposta:

```bash
infracost diff --path plan.json
```

Exemplo de saída:

```
Project: my-project

+ aws_instance.api_server
  +$75.00

- aws_instance.legacy_server
  -$58.49

Monthly cost change: +$16.51
```

### 4. Gerar um comentário de pull request

Depois de salvar um detalhamento em um arquivo JSON, converta-o em um formato de comentário de PR que a CI pode colar no GitHub, GitLab ou Bitbucket:

```bash
infracost breakdown --path . --format json > infracost.json
infracost output --path infracost.json --format github-comment
```

---

## Principais recursos

### Integração inline com o editor

A [extensão do Infracost para VS Code](https://marketplace.visualstudio.com/items?itemName=Infracost.infracost) mostra estimativas de custo inline ao lado de cada recurso em arquivos Terraform, além de uma barra lateral com o detalhamento completo dos recursos. Ela também exibe problemas de políticas FinOps (tags ausentes, regressões de custo) diretamente no editor. As IDEs JetBrains são suportadas por meio de uma extensão semelhante.

### Integrações com CI/CD

O Infracost oferece integrações nativas para GitHub Actions, GitLab CI, Bitbucket Pipelines e Azure DevOps. Um fluxo de trabalho mínimo do GitHub Actions é assim:

```yaml
name: Infracost
on: [pull_request]

jobs:
  infracost:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Infracost
        uses: infracost/actions/setup@v3
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}

      - name: Generate cost diff
        run: |
          infracost breakdown --path . --format json \
            --compare-to infracost_previous.json > infracost.json
```

O comentário no PR inclui o custo total projetado, a diferença por recurso e quaisquer falhas de política.

### Perfis de uso para estimativas realistas

As estimativas padrão presumem que os recursos operam 730 horas por mês com utilização total. Muitos recursos (EC2, Lambda, RDS, Kubernetes) suportam arquivos de uso específicos do cliente para que as estimativas reflitam a realidade:

```bash
infracost breakdown --path . --usage-file usage.yml
```

Gere um arquivo de uso inicial a partir de um projeto com:

```bash
infracost breakdown --path . --sync-usage-file
```

Um arquivo de uso tem a seguinte aparência:

```yaml
version: 0.1
resource_usage:
  aws_instance.web_server:
    monthly_hours: 438  # ~60% utilization
    operating_system: linux
    instances: 2
  aws_lambda_function.handler:
    monthly_requests: 1000000
    request_duration_ms: 250
```

### Política como código (OPA / Rego)

A aplicação de orçamentos e as regras de marcação (tagging) são expressas como políticas OPA. Defina as políticas em um diretório de políticas `.infracost` e execute:

```bash
infracost policy --path infracost.json --policy-path policy/
```

Uma política simples que bloqueia qualquer alteração com custo mensal acima de um limite:

```rego
package infracost

deny[msg] {
  cost := input.projects[_].diff.totalMonthlyCost
  cost > 1000
  msg := sprintf("Monthly cost $%.2f exceeds $1000 budget", [cost])
}
```

As políticas se integram ao mesmo fluxo de comentários em PRs, de modo que a CI possa bloquear merges tanto por custo quanto por falhas de conformidade.

### Detecção de economia

Além da precificação, o Infracost sinaliza oportunidades de right-sizing, recursos não utilizados e tipos de instância mal configurados. Eles aparecem na saída do detalhamento como itens de "economia" com uma redução mensal estimada e também são expostos na saída JSON para painéis de FinOps.

### Infracost Cloud

O painel SaaS opcional adiciona:

- Tendências históricas de custo por projeto e ambiente
- Orçamentos com alertas e políticas de limite
- Análises em nível de equipe e atribuição de gastos
- Uma biblioteca central de políticas gerenciada pelas equipes de plataforma

A chave de API usada pelo CLI autentica na mesma conta, mantendo os dados locais e na nuvem sincronizados. Um plano gratuito está disponível para equipes pequenas.

### Saída em múltiplos formatos para relatórios

```bash
# JSON for programmatic consumption / FinOps pipelines
infracost breakdown --path . --format json > cost.json

# HTML report for stakeholders
infracost breakdown --path . --format html > report.html

# SARIF for GitHub code scanning
infracost breakdown --path . --format sarif > infracost.sarif
```

---

## Exemplo: fluxo de trabalho shift-left completo

```bash
# 1. Author Terraform
cat > main.tf <<'EOF'
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "m5.2xlarge"  # likely over-provisioned
  tags = {
    Name = "web"
  }
}
EOF

# 2. Check the cost immediately
infracost breakdown --path .

# 3. Generate the plan and compare to current state
terraform init
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
infracost diff --path plan.json
```

O desenvolvedor vê um item de linha `+$400.00 / month` *antes* de executar `terraform apply` e pode fazer downgrade do tipo de instância ou alternar para uma instância spot.

---

## Arquivo de configuração

Os padrões em nível de projeto podem ser armazenados em `infracost.yml`:

```yaml
version: 0.1
projects:
  - path: .
    name: my-project
    usage_file: usage.yml
    terraform_plan_flags:
      - -var-file=prod.tfvars
```

Isso mantém os comandos de CI curtos e consistentes entre ambientes.

---

## Limitações

- **Preço de tabela, não contratos**: as estimativas refletem os preços de tabela sob demanda. Descontos personalizados negociados, preços EDP e descontos por uso comprometido devem ser considerados separadamente ou por meio de substituições de preço personalizadas.
- **Exige acesso à API de preços**: o CLI consulta a API de preços do Infracost; no entanto, existe um endpoint auto-hospedado para uso em ambientes isolados (air-gapped).
- **A cobertura é ampla, mas não universal**: recursos não suportados são ignorados e reportados, e novas ofertas de nuvem podem levar tempo para aparecer.
- **Não é uma plataforma completa de faturamento**: o Infracost estima o custo da infraestrutura; ele não substitui o painel de faturamento do provedor de nuvem para faturas reais, impostos ou créditos.

---

## Referências

- Site oficial: <https://www.infracost.io>
- Repositório no GitHub: <https://github.com/infracost/infracost>
- Documentação de cobertura de recursos: <https://www.infracost.io/docs/supported_resources/overview/>
- Extensão para VS Code: <https://marketplace.visualstudio.com/items?itemName=Infracost.infracost>
- Slack da comunidade: link disponível no site do Infracost