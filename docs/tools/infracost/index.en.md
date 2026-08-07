---
title: Infracost – Real-Time Cloud Cost Estimation for Infrastructure as Code
description: A practical guide to Infracost, an open-source CLI that estimates cloud costs from Terraform, CloudFormation, and CDK before deployment.
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

Infracost is an open-source, developer-first tool that brings **real-time cloud cost estimates** directly into the infrastructure-as-code (IaC) workflow. Point it at a Terraform, Terragrunt, CloudFormation, or AWS CDK project, and it produces a detailed monthly cost breakdown — before a single resource is deployed.

This page covers what Infracost is, why teams adopt it, how to install and use it, and the key features that make it a standard companion to Terraform and other IaC toolchains.

---

## What is Infracost?

Infracost is a command-line tool (and companion SaaS dashboard) that parses IaC definitions and plans, looks up live pricing data from AWS, Azure, and Google Cloud, and reports exactly what the resources will cost per month. It works on both **static code** and **Terraform plan files**, which means it can show the cost impact of a proposed change before it is applied.

The project launched in 2020 and quickly became the de facto cost-estimation layer for Terraform workflows. The core CLI is free and open source, while the optional Infracost Cloud dashboard adds team-wide visibility, budgets, and historical trend analysis.

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

## Why Infracost?

Traditional cloud cost management is *reactive*: a bill arrives at the end of the month and teams scramble to figure out what happened. Infracost promotes **shift-left FinOps** — catching expensive infrastructure decisions at the moment they are made:

- **During code review** — PR comments show the cost diff (`+$50.12`) so reviewers can reject over-budget changes.
- **In the editor** — VS Code and JetBrains extensions show inline costs as you type HCL.
- **In CI/CD** — pipelines can fail on cost regressions, missing tags, or budget violations before deployment.
- **In the terminal** — a quick `breakdown` command answers "what does this module cost?" without a calculator or spreadsheet.

Because Infracost reads the same code and plan artifacts engineers already produce, there is no extra instrumentation and no drift from what is actually deployed.

---

## Supported platforms

| IaC tool       | Clouds          | Notes                                     |
|----------------|-----------------|-------------------------------------------|
| Terraform HCL  | AWS, Azure, GCP | Full resource coverage and usage profiles |
| Terragrunt     | AWS, Azure, GCP | Detect Terragrunt projects automatically  |
| Terraform plan | AWS, Azure, GCP | `terraform show -json` output             |
| CloudFormation | AWS             | Template and stack set support            |
| AWS CDK        | AWS             | Via synthesized CloudFormation templates   |

Unsupported resources are reported as "skipped" with a message and a link to the resource coverage docs, so the output never silently lies about cost.

---

## Installation

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

### Verify the installation

```bash
infracost --version
infracost --help
```

---

## Authentication

Infracost requires an API key because it queries live cloud pricing APIs. Register a free account at [infracost.io/dashboard](https://www.infracost.io), then log in from the CLI:

```bash
infracost auth login
```

Alternatively, export the API key directly for CI environments:

```bash
export INFRACOST_API_KEY=my-api-key
```

For users who cannot send pricing data to the hosted Infracost API, the CLI supports a self-hosted pricing source (`INFRACOST_PRICING_API_ENDPOINT`) for air-gapped environments.

---

## Basic usage

### 1. Cost breakdown of a Terraform directory

```bash
infracost breakdown --path . --format table
```

This evaluates the HCL in the current directory and prints a resource-by-resource monthly cost table. Supported formats include `table`, `json`, `html`, `markdown`, `sarif`, and `github-comment`.

### 2. Cost breakdown of a Terraform plan

The most accurate picture comes from the plan, since it includes context like `count`, `for_each`, and conditional logic:

```bash
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
infracost breakdown --terraform-plan-json plan.json --show-skipped
```

The `--show-skipped` flag lists resources that Infracost could not price so you can assess coverage.

### 3. Diff mode

Diff mode shows the **cost change** between two states — typically the current deployed state and the proposed change:

```bash
infracost diff --path plan.json
```

Example output fragment:

```
Project: my-project

+ aws_instance.api_server
  +$75.00

- aws_instance.legacy_server
  -$58.49

Monthly cost change: +$16.51
```

### 4. Generate a pull-request comment

After saving a breakdown to a JSON file, convert it into a PR comment format that CI can paste into GitHub, GitLab, or Bitbucket:

```bash
infracost breakdown --path . --format json > infracost.json
infracost output --path infracost.json --format github-comment
```

---

## Key features

### Inline editor integration

The [Infracost VS Code extension](https://marketplace.visualstudio.com/items?itemName=Infracost.infracost) shows inline cost estimates next to each resource in Terraform files, plus a sidebar with the full resource breakdown. It also surfaces FinOps policy issues (missing tags, cost regressions) directly in the editor. JetBrains IDEs are supported through a similar extension.

### CI/CD integrations

Infracost ships native integrations for GitHub Actions, GitLab CI, Bitbucket Pipelines, and Azure DevOps. A minimal GitHub Actions workflow looks like:

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

The PR comment includes the total projected cost, the diff per resource, and any policy failures.

### Usage profiles for realistic estimates

Default estimates assume resources run 730 hours per month at full utilization. Many resources (EC2, Lambda, RDS, Kubernetes) support customer-specific usage files so estimates reflect reality:

```bash
infracost breakdown --path . --usage-file usage.yml
```

Generate a starter usage file from a project with:

```bash
infracost breakdown --path . --sync-usage-file
```

A usage file looks like:

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

### Policy as code (OPA / Rego)

Budget enforcement and tagging rules are expressed as OPA policies. Define policies in a `.infracost` policy directory, then run:

```bash
infracost policy --path infracost.json --policy-path policy/
```

A simple policy that blocks any change with a monthly cost above a threshold:

```rego
package infracost

deny[msg] {
  cost := input.projects[_].diff.totalMonthlyCost
  cost > 1000
  msg := sprintf("Monthly cost $%.2f exceeds $1000 budget", [cost])
}
```

Policies integrate with the same PR-comment flow, so CI can block merges on both cost and compliance failures.

### Savings detection

Beyond pricing, Infracost flags right-sizing opportunities, unused resources, and misconfigured instance types. These appear in the breakdown output as "savings" items with an estimated monthly reduction, and are also exposed in JSON output for FinOps dashboards.

### Infracost Cloud

The optional SaaS dashboard adds:

- Historical cost trends per project and environment
- Budgets with alerts and threshold policies
- Team-level analytics and spend attribution
- A central policy library managed by platform teams

The API key used by the CLI authenticates to the same account, so local and cloud data stay in sync. A free tier is available for small teams.

### Multi-format output for reporting

```bash
# JSON for programmatic consumption / FinOps pipelines
infracost breakdown --path . --format json > cost.json

# HTML report for stakeholders
infracost breakdown --path . --format html > report.html

# SARIF for GitHub code scanning
infracost breakdown --path . --format sarif > infracost.sarif
```

---

## Example: full shift-left workflow

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

The developer sees a `+$400.00 / month` line item *before* running `terraform apply`, and can downgrade the instance type or switch to a spot instance.

---

## Configuration file

Project-level defaults can be stored in `infracost.yml`:

```yaml
version: 0.1
projects:
  - path: .
    name: my-project
    usage_file: usage.yml
    terraform_plan_flags:
      - -var-file=prod.tfvars
```

This keeps CI commands short and consistent across environments.

---

## Limitations

- **List pricing, not contracts**: estimates reflect on-demand list prices. Custom negotiated discounts, EDP pricing, and committed-use discounts must be accounted for separately or via custom price overrides.
- **Requires pricing API access**: the CLI queries the Infracost pricing API, although a self-hosted endpoint exists for air-gapped use.
- **Coverage is broad but not universal**: unsupported resources are skipped and reported, and new cloud offerings can take time to appear.
- **Not a full billing platform**: Infracost estimates infrastructure cost; it does not replace the cloud provider's billing dashboard for actual invoices, taxes, or credits.

---

## References

- Official site: <https://www.infracost.io>
- GitHub repository: <https://github.com/infracost/infracost>
- Resource coverage docs: <https://www.infracost.io/docs/supported_resources/overview/>
- VS Code extension: <https://marketplace.visualstudio.com/items?itemName=Infracost.infracost>
- Community Slack: linked from the Infracost website