---
title: Infracost – Echtzeit-Cloud-Kostenschätzung für Infrastructure as Code
description: Ein praktischer Leitfaden für Infracost, ein Open-Source-Kommandozeilentool, das Cloud-Kosten aus Terraform, CloudFormation und CDK vor der Bereitstellung schätzt.
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

Infracost ist ein Open-Source-Tool, das sich an Entwickler richtet und **Echtzeit-Cloud-Kostenschätzungen** direkt in den Infrastructure-as-Code-Workflow (IaC) bringt. Richten Sie es auf ein Terraform-, Terragrunt-, CloudFormation- oder AWS-CDK-Projekt, und es erstellt eine detaillierte monatliche Kostenaufstellung – bevor auch nur eine Ressource bereitgestellt wird.

Diese Seite behandelt, was Infracost ist, warum Teams es einsetzen, wie man es installiert und verwendet, sowie die wichtigsten Funktionen, die es zu einem Standardbegleiter für Terraform und andere IaC-Toolchains machen.

---

## Was ist Infracost?

Infracost ist ein Kommandozeilen-Tool (und ein begleitendes SaaS-Dashboard), das IaC-Definitionen und -Pläne analysiert, Live-Preisdaten von AWS, Azure und Google Cloud abruft und genau angibt, was die Ressourcen pro Monat kosten werden. Es funktioniert sowohl mit **statischem Code** als auch mit **Terraform-Plan-Dateien**, sodass es die Kostenauswirkungen einer vorgeschlagenen Änderung anzeigen kann, bevor sie angewendet wird.

Das Projekt startete 2020 und wurde schnell zur De-facto-Kostenschätzungsschicht für Terraform-Workflows. Das Kern-CLI ist kostenlos und Open Source, während das optionale Infracost-Cloud-Dashboard teamweite Transparenz, Budgets und historische Trendanalysen ergänzt.

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

## Warum Infracost?

Traditionelles Cloud-Kostenmanagement ist *reaktiv*: Eine Rechnung trifft am Ende des Monats ein, und Teams versuchen hektisch herauszufinden, was passiert ist. Infracost fördert **Shift-left-FinOps** – teure Infrastrukturentscheidungen werden in dem Moment erkannt, in dem sie getroffen werden:

- **Während des Code-Reviews** – PR-Kommentare zeigen die Kostendifferenz (`+$50.12`), sodass Prüfer über dem Budget liegende Änderungen ablehnen können.
- **Im Editor** – VS-Code- und JetBrains-Erweiterungen zeigen Inline-Kosten, während Sie HCL eingeben.
- **In CI/CD** – Pipelines können vor der Bereitstellung bei Kostenregressionen, fehlenden Tags oder Budgetverletzungen fehlschlagen.
- **Im Terminal** – ein schneller `breakdown`-Befehl beantwortet „Was kostet dieses Modul?“, ohne Taschenrechner oder Tabellenkalkulation.

Da Infracost dieselben Code- und Plan-Artefakte liest, die Entwickler ohnehin erstellen, gibt es keine zusätzliche Instrumentierung und keine Abweichung von dem, was tatsächlich bereitgestellt wird.

---

## Unterstützte Plattformen

| IaC-Tool        | Clouds          | Hinweise                                           |
|-----------------|-----------------|----------------------------------------------------|
| Terraform HCL   | AWS, Azure, GCP | Vollständige Ressourcenabdeckung und Nutzungsprofile |
| Terragrunt      | AWS, Azure, GCP | Erkennt Terragrunt-Projekte automatisch            |
| Terraform plan  | AWS, Azure, GCP | Ausgabe von `terraform show -json`                  |
| CloudFormation  | AWS             | Unterstützung für Vorlagen und Stack-Sets           |
| AWS CDK         | AWS             | Über synthetisierte CloudFormation-Vorlagen         |

Nicht unterstützte Ressourcen werden als „übersprungen“ (skipped) mit einer Meldung und einem Link zur Dokumentation der Ressourcenabdeckung aufgeführt, sodass die Ausgabe nie stillschweigend über Kosten lügt.

---

## Installation

### Homebrew (macOS / Linux)

```bash
brew install infracost
```

### Shell-Skript (Linux / macOS)

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

### Installation überprüfen

```bash
infracost --version
infracost --help
```

---

## Authentifizierung

Infracost benötigt einen API-Schlüssel, da es Live-Cloud-Preis-APIs abfragt. Registrieren Sie ein kostenloses Konto unter [infracost.io/dashboard](https://www.infracost.io) und melden Sie sich dann über die CLI an:

```bash
infracost auth login
```

Alternativ können Sie den API-Schlüssel für CI-Umgebungen direkt exportieren:

```bash
export INFRACOST_API_KEY=my-api-key
```

Für Nutzer, die keine Preisdaten an die gehostete Infracost-API senden können, unterstützt die CLI eine selbst gehostete Preisquelle (`INFRACOST_PRICING_API_ENDPOINT`) für abgeschottete Umgebungen (air-gapped).

---

## Grundlegende Verwendung

### 1. Kostenaufstellung eines Terraform-Verzeichnisses

```bash
infracost breakdown --path . --format table
```

Dies wertet das HCL im aktuellen Verzeichnis aus und gibt eine ressourcenweise monatliche Kostentabelle aus. Unterstützte Formate sind `table`, `json`, `html`, `markdown`, `sarif` und `github-comment`.

### 2. Kostenaufstellung eines Terraform-Plans

Das genaueste Bild liefert der Plan, da er Kontext wie `count`, `for_each` und bedingte Logik enthält:

```bash
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
infracost breakdown --terraform-plan-json plan.json --show-skipped
```

Die `--show-skipped`-Option listet Ressourcen auf, die Infracost nicht bepreisen konnte, sodass Sie die Abdeckung einschätzen können.

### 3. Diff-Modus

Der Diff-Modus zeigt die **Kostenänderung** zwischen zwei Zuständen – typischerweise dem aktuell bereitgestellten Zustand und der vorgeschlagenen Änderung:

```bash
infracost diff --path plan.json
```

Beispielhafter Ausgabeausschnitt:

```
Project: my-project

+ aws_instance.api_server
  +$75.00

- aws_instance.legacy_server
  -$58.49

Monthly cost change: +$16.51
```

### 4. Pull-Request-Kommentar erzeugen

Nachdem Sie eine Kostenaufstellung in einer JSON-Datei gespeichert haben, wandeln Sie sie in ein PR-Kommentarformat um, das CI in GitHub, GitLab oder Bitbucket einfügen kann:

```bash
infracost breakdown --path . --format json > infracost.json
infracost output --path infracost.json --format github-comment
```

---

## Wichtige Funktionen

### Inline-Editor-Integration

Die [Infracost-VS-Code-Erweiterung](https://marketplace.visualstudio.com/items?itemName=Infracost.infracost) zeigt Inline-Kostenschätzungen neben jeder Ressource in Terraform-Dateien sowie eine Seitenleiste mit der vollständigen Ressourcenaufstellung. Sie zeigt außerdem FinOps-Richtlinienprobleme (fehlende Tags, Kostenregressionen) direkt im Editor an. JetBrains-IDEs werden über eine ähnliche Erweiterung unterstützt.

### CI/CD-Integrationen

Infracost bietet native Integrationen für GitHub Actions, GitLab CI, Bitbucket Pipelines und Azure DevOps. Ein minimaler GitHub-Actions-Workflow sieht wie folgt aus:

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

Der PR-Kommentar enthält die gesamten prognostizierten Kosten, die Differenz pro Ressource und etwaige Richtlinienfehler.

### Nutzungsprofile für realistische Schätzungen

Standardmäßige Schätzungen gehen davon aus, dass Ressourcen 730 Stunden pro Monat bei voller Auslastung laufen. Viele Ressourcen (EC2, Lambda, RDS, Kubernetes) unterstützen kundenspezifische Nutzungsdateien, sodass die Schätzungen die Realität abbilden:

```bash
infracost breakdown --path . --usage-file usage.yml
```

Eine Ausgangs-Nutzungsdatei für ein Projekt erzeugen Sie mit:

```bash
infracost breakdown --path . --sync-usage-file
```

Eine Nutzungsdatei sieht wie folgt aus:

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

### Richtlinien als Code (OPA / Rego)

Budgetdurchsetzung und Tagging-Regeln werden als OPA-Richtlinien ausgedrückt. Definieren Sie Richtlinien in einem `.infracost`-Richtlinienverzeichnis und führen Sie dann aus:

```bash
infracost policy --path infracost.json --policy-path policy/
```

Eine einfache Richtlinie, die jede Änderung mit einem monatlichen Kostenwert über einem Schwellenwert blockiert:

```rego
package infracost

deny[msg] {
  cost := input.projects[_].diff.totalMonthlyCost
  cost > 1000
  msg := sprintf("Monthly cost $%.2f exceeds $1000 budget", [cost])
}
```

Richtlinien integrieren sich in denselben PR-Kommentar-Ablauf, sodass CI Merges sowohl bei Kosten- als auch bei Compliance-Fehlern blockieren kann.

### Einsparungserkennung

Über die Bepreisung hinaus kennzeichnet Infracost Right-Sizing-Optionen, ungenutzte Ressourcen und falsch konfigurierte Instanztypen. Diese erscheinen in der Kostenaufstellung als „Einsparungen“ (savings) mit einer geschätzten monatlichen Reduzierung und werden auch in der JSON-Ausgabe für FinOps-Dashboards bereitgestellt.

### Infracost Cloud

Das optionale SaaS-Dashboard ergänzt:

- Historische Kostenentwicklungen pro Projekt und Umgebung
- Budgets mit Warnmeldungen und Schwellenwertrichtlinien
- Analysen auf Teamebene und Kostenattribution
- Eine zentrale Richtlinienbibliothek, die von Plattformteams verwaltet wird

Der von der CLI verwendete API-Schlüssel authentifiziert sich für dasselbe Konto, sodass lokale Daten und Cloud-Daten synchron bleiben. Für kleine Teams ist eine kostenlose Stufe verfügbar.

### Mehrformat-Ausgabe für Berichte

```bash
# JSON for programmatic consumption / FinOps pipelines
infracost breakdown --path . --format json > cost.json

# HTML report for stakeholders
infracost breakdown --path . --format html > report.html

# SARIF for GitHub code scanning
infracost breakdown --path . --format sarif > infracost.sarif
```

---

## Beispiel: vollständiger Shift-left-Workflow

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

Der Entwickler sieht einen `+$400.00 / Monat`-Posten, *bevor* er `terraform apply` ausführt, und kann den Instanztyp herabstufen oder zu einer Spot-Instanz wechseln.

---

## Konfigurationsdatei

Projektweite Standardeinstellungen können in `infracost.yml` gespeichert werden:

```yaml
version: 0.1
projects:
  - path: .
    name: my-project
    usage_file: usage.yml
    terraform_plan_flags:
      - -var-file=prod.tfvars
```

Dadurch bleiben CI-Befehle kurz und über Umgebungen hinweg konsistent.

---

## Einschränkungen

- **Listenpreise, keine Verträge**: Die Schätzungen spiegeln On-Demand-Listenpreise wider. Individuell ausgehandelte Rabatte, EDP-Preise und Rabatte für zugesicherte Nutzung (Committed Use Discounts) müssen separat oder über benutzerdefinierte Preisüberschreibungen berücksichtigt werden.
- **Erfordert Zugriff auf die Preis-API**: Die CLI fragt die Infracost-Preis-API ab, obwohl für abgeschottete Umgebungen (air-gapped) ein selbst gehosteter Endpunkt existiert.
- **Die Abdeckung ist breit, aber nicht vollständig**: Nicht unterstützte Ressourcen werden übersprungen und gemeldet, und neue Cloud-Angebote können Zeit brauchen, bis sie erscheinen.
- **Keine vollständige Abrechnungsplattform**: Infracost schätzt Infrastrukturkosten; es ersetzt nicht das Abrechnungs-Dashboard des Cloud-Anbieters für tatsächliche Rechnungen, Steuern oder Gutschriften.

---

## Referenzen

- Offizielle Website: <https://www.infracost.io>
- GitHub-Repository: <https://github.com/infracost/infracost>
- Dokumentation zur Ressourcenabdeckung: <https://www.infracost.io/docs/supported_resources/overview/>
- VS-Code-Erweiterung: <https://marketplace.visualstudio.com/items?itemName=Infracost.infracost>
- Community-Slack: über die Infracost-Website verlinkt