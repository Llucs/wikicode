---
title: Infracost – 基础设施即代码的实时云成本估算
description: 一份实用指南，介绍 Infracost，一个开源命令行工具，可在部署前估算 Terraform、CloudFormation 和 CDK 的云成本。
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

Infracost 是一个开源、开发者优先的工具，它将**实时云成本估算**直接带入基础设施即代码（IaC）工作流程。将其指向 Terraform、Terragrunt、CloudFormation 或 AWS CDK 项目，它就会在部署任何资源之前，生成一份详细的月度成本明细。

本页涵盖 Infracost 是什么、团队为何采用它、如何安装和使用它，以及使其成为 Terraform 和其他 IaC 工具链标准伴侣的关键功能。

---

## 什么是 Infracost？

Infracost 是一个命令行工具（以及配套的 SaaS 仪表板），它解析 IaC 定义和计划，查询 AWS、Azure 和 Google Cloud 的实时定价数据，并准确报告这些资源每月将花费多少。它同时作用于**静态代码**和 **Terraform 计划文件**，这意味着它可以在变更应用之前显示其成本影响。

该项目于 2020 年启动，并迅速成为 Terraform 工作流的事实上的成本估算层。核心 CLI 是免费开源的，而可选的 Infracost Cloud 仪表板则增加了团队级可见性、预算和历史趋势分析。

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

## 为什么选择 Infracost？

传统的云成本管理是*反应式*的：账单在月底到达，团队手忙脚乱地弄清楚发生了什么。Infracost 提倡**左移 FinOps**——在做出昂贵的基础设施决策时立即发现它们：

- **在代码审查期间**——PR 评论显示成本差异（`+$50.12`），让审查者可以拒绝超出预算的变更。
- **在编辑器中**——VS Code 和 JetBrains 扩展在你输入 HCL 时显示内联成本。
- **在 CI/CD 中**——流水线可以在部署前因成本回归、缺失标签或预算违规而失败。
- **在终端中**——一条快速的 `breakdown` 命令就能回答“这个模块要花多少钱？”，无需计算器或电子表格。

由于 Infracost 读取的是工程师已经产出的相同代码和计划工件，因此无需额外的探针，也不会与实际部署的内容产生漂移。

---

## 支持的平台

| IaC 工具       | 云供应商       | 说明                                        |
|----------------|----------------|---------------------------------------------|
| Terraform HCL  | AWS, Azure, GCP | 完整的资源覆盖和使用配置文件                |
| Terragrunt     | AWS, Azure, GCP | 自动检测 Terragrunt 项目                    |
| Terraform plan | AWS, Azure, GCP | `terraform show -json` 输出                 |
| CloudFormation | AWS             | 支持模板和堆栈集                            |
| AWS CDK        | AWS             | 通过合成的 CloudFormation 模板              |

不支持的资源会显示为“skipped”，并附带一条消息和指向资源覆盖文档的链接，因此输出绝不会默默地掩盖成本。

---

## 安装

### Homebrew（macOS / Linux）

```bash
brew install infracost
```

### Shell 脚本（Linux / macOS）

```bash
curl -fsSL https://raw.githubusercontent.com/infracost/infracost/master/scripts/install.sh | sh
```

### Windows（Scoop）

```powershell
scoop bucket add infracost https://github.com/infracost/infracost
scoop install infracost
```

### Docker

```bash
docker pull infracost/infracost
```

### 验证安装

```bash
infracost --version
infracost --help
```

---

## 认证

Infracost 需要一个 API 密钥，因为它会查询实时的云定价 API。在 [infracost.io/dashboard](https://www.infracost.io) 注册一个免费账户，然后从 CLI 登录：

```bash
infracost auth login
```

或者，对于 CI 环境，可以直接导出 API 密钥：

```bash
export INFRACOST_API_KEY=my-api-key
```

对于无法将定价数据发送到托管 Infracost API 的用户，CLI 支持自托管定价源（`INFRACOST_PRICING_API_ENDPOINT`），适用于隔离环境。

---

## 基本用法

### 1. Terraform 目录的成本分解

```bash
infracost breakdown --path . --format table
```

这会评估当前目录中的 HCL，并打印一个按资源划分的月度成本表。支持的格式包括 `table`、`json`、`html`、`markdown`、`sarif` 和 `github-comment`。

### 2. Terraform 计划的成本分解

最准确的视图来自计划，因为它包含了 `count`、`for_each` 和条件逻辑等上下文：

```bash
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
infracost breakdown --terraform-plan-json plan.json --show-skipped
```

`--show-skipped` 标志会列出 Infracost 无法定价的资源，以便你评估覆盖率。

### 3. Diff 模式

Diff 模式显示两个状态之间的**成本变化**——通常是当前已部署状态和提议变更之间：

```bash
infracost diff --path plan.json
```

示例输出片段：

```
Project: my-project

+ aws_instance.api_server
  +$75.00

- aws_instance.legacy_server
  -$58.49

Monthly cost change: +$16.51
```

### 4. 生成拉取请求评论

将 breakdown 保存为 JSON 文件后，可将其转换为 PR 评论格式，CI 可以将其粘贴到 GitHub、GitLab 或 Bitbucket 中：

```bash
infracost breakdown --path . --format json > infracost.json
infracost output --path infracost.json --format github-comment
```

---

## 关键功能

### 编辑器内联集成

[Infracost VS Code 扩展](https://marketplace.visualstudio.com/items?itemName=Infracost.infracost) 会在 Terraform 文件中每个资源旁边显示内联成本估算，并附带一个侧边栏显示完整的资源明细。它还将 FinOps 策略问题（缺失标签、成本回归）直接呈现在编辑器中。JetBrains IDE 通过类似扩展获得支持。

### CI/CD 集成

Infracost 为 GitHub Actions、GitLab CI、Bitbucket Pipelines 和 Azure DevOps 提供了原生集成。一个最小的 GitHub Actions 工作流看起来像这样：

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

PR 评论包含总预计成本、每个资源的差异以及任何策略失败信息。

### 使用配置文件实现贴近现实的估算

默认估算假设资源每月运行 730 小时，且完全利用。许多资源（EC2、Lambda、RDS、Kubernetes）支持使用特定于客户的使用文件，使估算更贴近实际：

```bash
infracost breakdown --path . --usage-file usage.yml
```

从项目生成一个初始使用文件：

```bash
infracost breakdown --path . --sync-usage-file
```

使用文件看起来像：

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

### 策略即代码（OPA / Rego）

预算强制和标签规则通过 OPA 策略表达。在一个 `.infracost` 策略目录中定义策略，然后运行：

```bash
infracost policy --path infracost.json --policy-path policy/
```

一个简单的策略，阻止任何月度成本超过阈值的变更：

```rego
package infracost

deny[msg] {
  cost := input.projects[_].diff.totalMonthlyCost
  cost > 1000
  msg := sprintf("Monthly cost $%.2f exceeds $1000 budget", [cost])
}
```

策略与同一条 PR 评论流程集成，因此 CI 可以在成本和合规性失败时阻止合并。

### 节省检测

除了定价之外，Infracost 还会标记出优化机会、未使用的资源和配置错误的实例类型。这些会作为“节省”项出现在 breakdown 输出中，并带有每月预计节省金额，同时也会在 JSON 输出中暴露给 FinOps 仪表板。

### Infracost Cloud

可选的 SaaS 仪表板增加了：

- 每个项目和环境的成本历史趋势
- 带有警报和阈值策略的预算
- 团队级分析和成本归属
- 由平台团队管理的中央策略库

CLI 使用的 API 密钥会认证到同一个账户，因此本地和云端数据保持同步。小团队可使用免费层级。

### 用于报告的多格式输出

```bash
# JSON 用于程序化消费 / FinOps 流水线
infracost breakdown --path . --format json > cost.json

# HTML 报告给干系人
infracost breakdown --path . --format html > report.html

# SARIF 用于 GitHub code scanning
infracost breakdown --path . --format sarif > infracost.sarif
```

---

## 示例：完整的左移工作流

```bash
# 1. 编写 Terraform
cat > main.tf <<'EOF'
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "m5.2xlarge"  # likely over-provisioned
  tags = {
    Name = "web"
  }
}
EOF

# 2. 立即检查成本
infracost breakdown --path .

# 3. 生成计划并与当前状态对比
terraform init
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
infracost diff --path plan.json
```

开发人员在运行 `terraform apply` **之前**就会看到 `+$400.00 / month` 的成本项，然后可以降级实例类型或改用 spot 实例。

---

## 配置文件

项目级默认值可以存储在 `infracost.yml` 中：

```yaml
version: 0.1
projects:
  - path: .
    name: my-project
    usage_file: usage.yml
    terraform_plan_flags:
      - -var-file=prod.tfvars
```

这使 CI 命令在不同环境中保持简短和一致。

---

## 局限性

- **列表价格，而非合同价格**：估算反映的是按需列表价格。自定义协商折扣、EDP 定价和承诺使用折扣必须单独核算，或通过自定义价格覆盖处理。
- **需要定价 API 访问**：CLI 会查询 Infracost 定价 API，不过存在用于隔离环境的自托管端点。
- **覆盖率广泛但并非无所不包**：不支持的资源会被跳过并报告，新的云服务可能需要时间才会被纳入。
- **不是完整的账单平台**：Infracost 估算的是基础设施成本；它不会取代云供应商的账单仪表板来出具实际发票、税费或抵扣额。

---

## 参考

- 官方网站：<https://www.infracost.io>
- GitHub 仓库：<https://github.com/infracost/infracost>
- 资源覆盖文档：<https://www.infracost.io/docs/supported_resources/overview/>
- VS Code 扩展：<https://marketplace.visualstudio.com/items?itemName=Infracost.infracost>
- 社区 Slack：可从 Infracost 网站链接进入。