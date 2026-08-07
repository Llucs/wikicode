---
title: Infracost – Estimation des coûts cloud en temps réel pour Infrastructure as Code
description: Un guide pratique d'Infracost, un CLI open-source qui estime les coûts cloud à partir de Terraform, CloudFormation et CDK avant le déploiement.
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

Infracost est un outil open-source, conçu pour les développeurs, qui intègre **l’estimation des coûts cloud en temps réel** directement dans le flux de travail d’infrastructure-as-code (IaC). Pointez-le vers un projet Terraform, Terragrunt, CloudFormation ou AWS CDK, et il produit une ventilation détaillée des coûts mensuels — avant qu’une seule ressource ne soit déployée.

Cette page explique ce qu’est Infracost, pourquoi les équipes l’adoptent, comment l’installer et l’utiliser, ainsi que les fonctionnalités clés qui en font un compagnon standard de Terraform et d’autres chaînes d’outils IaC.

---

## Qu’est-ce qu’Infracost ?

Infracost est un outil en ligne de commande (accompagné d’un tableau de bord SaaS) qui analyse les définitions et les plans IaC, interroge les données de tarification en direct d’AWS, Azure et Google Cloud, et indique exactement ce que les ressources coûteront par mois. Il fonctionne à la fois sur le **code statique** et les **fichiers de plan Terraform**, ce qui signifie qu’il peut montrer l’impact financier d’un changement proposé avant qu’il ne soit appliqué.

Le projet a été lancé en 2020 et est rapidement devenu la couche d’estimation des coûts de facto pour les flux de travail Terraform. Le CLI de base est gratuit et open source, tandis que le tableau de bord facultatif Infracost Cloud ajoute une visibilité à l’échelle de l’équipe, des budgets et une analyse des tendances historiques.

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

## Pourquoi Infracost ?

La gestion traditionnelle des coûts cloud est *réactive* : une facture arrive à la fin du mois et les équipes s’activent pour comprendre ce qui s’est passé. Infracost favorise le **FinOps shift-left** — détecter les décisions d’infrastructure coûteuses au moment où elles sont prises :

- **Pendant la revue de code** — les commentaires de PR affichent la différence de coût (`+$50.12`) afin que les relecteurs puissent rejeter les modifications hors budget.
- **Dans l’éditeur** — les extensions VS Code et JetBrains affichent les coûts en ligne pendant que vous écrivez du HCL.
- **Dans le CI/CD** — les pipelines peuvent échouer en cas de régression de coût, de tags manquants ou de dépassement de budget avant le déploiement.
- **Dans le terminal** — une commande `breakdown` rapide répond à la question « combien coûte ce module ? » sans calculatrice ni feuille de calcul.

Comme Infracost lit les mêmes artefacts de code et de plan que les ingénieurs produisent déjà, il n’y a pas d’instrumentation supplémentaire ni de dérive par rapport à ce qui est réellement déployé.

---

## Plateformes prises en charge

| Outil IaC       | Clouds         | Notes                                            |
|-----------------|----------------|--------------------------------------------------|
| Terraform HCL   | AWS, Azure, GCP| Couverture complète des ressources et profils d’utilisation |
| Terragrunt      | AWS, Azure, GCP| Détecte automatiquement les projets Terragrunt   |
| Terraform plan  | AWS, Azure, GCP| Sortie de `terraform show -json`                 |
| CloudFormation  | AWS            | Prise en charge des modèles et des stack sets    |
| AWS CDK         | AWS            | Via des modèles CloudFormation synthétisés       |

Les ressources non prises en charge sont signalées comme « ignorées » avec un message et un lien vers la documentation de couverture des ressources, afin que la sortie ne mente jamais silencieusement sur le coût.

---

## Installation

### Homebrew (macOS / Linux)

```bash
brew install infracost
```

### Script shell (Linux / macOS)

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

### Vérifier l’installation

```bash
infracost --version
infracost --help
```

---

## Authentification

Infracost nécessite une clé API car il interroge les API de tarification cloud en direct. Créez un compte gratuit sur [infracost.io/dashboard](https://www.infracost.io), puis connectez-vous à partir du CLI :

```bash
infracost auth login
```

Vous pouvez également exporter la clé API directement pour les environnements CI :

```bash
export INFRACOST_API_KEY=my-api-key
```

Pour les utilisateurs qui ne peuvent pas envoyer de données de tarification à l’API Infracost hébergée, le CLI prend en charge une source de tarification auto-hébergée (`INFRACOST_PRICING_API_ENDPOINT`) pour les environnements isolés (air-gapped).

---

## Utilisation de base

### 1. Ventilation des coûts d’un répertoire Terraform

```bash
infracost breakdown --path . --format table
```

Cette commande évalue le HCL dans le répertoire courant et affiche un tableau des coûts mensuels ressource par ressource. Les formats pris en charge incluent `table`, `json`, `html`, `markdown`, `sarif` et `github-comment`.

### 2. Ventilation des coûts d’un plan Terraform

L’image la plus précise provient du plan, car celui-ci inclut le contexte comme `count`, `for_each` et la logique conditionnelle :

```bash
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
infracost breakdown --terraform-plan-json plan.json --show-skipped
```

Le drapeau `--show-skipped` liste les ressources qu’Infracost n’a pas pu tarifer afin que vous puissiez évaluer la couverture.

### 3. Mode diff

Le mode diff affiche la **variation de coût** entre deux états — généralement l’état actuellement déployé et la modification proposée :

```bash
infracost diff --path plan.json
```

Exemple de sortie :

```
Project: my-project

+ aws_instance.api_server
  +$75.00

- aws_instance.legacy_server
  -$58.49

Monthly cost change: +$16.51
```

### 4. Générer un commentaire de pull request

Après avoir enregistré une ventilation dans un fichier JSON, convertissez-la en un format de commentaire de PR que le CI peut coller dans GitHub, GitLab ou Bitbucket :

```bash
infracost breakdown --path . --format json > infracost.json
infracost output --path infracost.json --format github-comment
```

---

## Fonctionnalités clés

### Intégration dans l’éditeur

L’[extension VS Code Infracost](https://marketplace.visualstudio.com/items?itemName=Infracost.infracost) affiche des estimations de coûts en ligne à côté de chaque ressource dans les fichiers Terraform, ainsi qu’une barre latérale avec la ventilation complète des ressources. Elle fait également remonter les problèmes de politique FinOps (tags manquants, régressions de coûts) directement dans l’éditeur. Les IDE JetBrains sont pris en charge via une extension similaire.

### Intégrations CI/CD

Infracost fournit des intégrations natives pour GitHub Actions, GitLab CI, Bitbucket Pipelines et Azure DevOps. Un workflow GitHub Actions minimal ressemble à ceci :

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

Le commentaire de PR inclut le coût total projeté, la différence par ressource et toute défaillance de politique.

### Profils d’utilisation pour des estimations réalistes

Les estimations par défaut supposent que les ressources fonctionnent 730 heures par mois à pleine utilisation. De nombreuses ressources (EC2, Lambda, RDS, Kubernetes) prennent en charge des fichiers d’utilisation spécifiques au client afin que les estimations reflètent la réalité :

```bash
infracost breakdown --path . --usage-file usage.yml
```

Générez un fichier d’utilisation de départ à partir d’un projet avec :

```bash
infracost breakdown --path . --sync-usage-file
```

Un fichier d’utilisation ressemble à :

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

Les règles de respect du budget et de tagging sont exprimées sous forme de politiques OPA. Définissez les politiques dans un répertoire de politiques `.infracost`, puis exécutez :

```bash
infracost policy --path infracost.json --policy-path policy/
```

Une politique simple qui bloque toute modification dont le coût mensuel dépasse un seuil :

```rego
package infracost

deny[msg] {
  cost := input.projects[_].diff.totalMonthlyCost
  cost > 1000
  msg := sprintf("Monthly cost $%.2f exceeds $1000 budget", [cost])
}
```

Les politiques s’intègrent au même flux de commentaires de PR, de sorte que le CI peut bloquer les fusions en cas de défaillance de coût et de conformité.

### Détection des économies

Au-delà de la tarification, Infracost signale les opportunités de right-sizing, les ressources inutilisées et les types d’instances mal configurés. Ils apparaissent dans la sortie de ventilation comme des éléments « économies » avec une réduction mensuelle estimée, et sont également exposés dans la sortie JSON pour les tableaux de bord FinOps.

### Infracost Cloud

Le tableau de bord SaaS facultatif ajoute :

- Des tendances historiques des coûts par projet et par environnement
- Des budgets avec alertes et politiques de seuil
- Des analyses au niveau de l’équipe et l’attribution des dépenses
- Une bibliothèque de politiques centralisée gérée par les équipes de plateforme

La clé API utilisée par le CLI authentifie le même compte, de sorte que les données locales et cloud restent synchronisées. Un niveau gratuit est disponible pour les petites équipes.

### Sortie multi-format pour les rapports

```bash
# JSON for programmatic consumption / FinOps pipelines
infracost breakdown --path . --format json > cost.json

# HTML report for stakeholders
infracost breakdown --path . --format html > report.html

# SARIF for GitHub code scanning
infracost breakdown --path . --format sarif > infracost.sarif
```

---

## Exemple : flux de travail shift-left complet

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

Le développeur voit un poste `+$400.00 / mois` *avant* d’exécuter `terraform apply`, et peut réduire le type d’instance ou passer à une instance spot.

---

## Fichier de configuration

Les paramètres par défaut au niveau du projet peuvent être stockés dans `infracost.yml` :

```yaml
version: 0.1
projects:
  - path: .
    name: my-project
    usage_file: usage.yml
    terraform_plan_flags:
      - -var-file=prod.tfvars
```

Cela maintient les commandes CI courtes et cohérentes entre les environnements.

---

## Limitations

- **Prix catalogue, pas de contrats** : les estimations reflètent les prix catalogue à la demande. Les remises négociées personnalisées, la tarification EDP et les remises pour engagement d’utilisation doivent être comptabilisées séparément ou via des surcharges de prix personnalisées.
- **Nécessite un accès à l’API de tarification** : le CLI interroge l’API de tarification Infracost, bien qu’un point de terminaison auto-hébergé existe pour une utilisation isolée (air-gapped).
- **La couverture est large mais pas universelle** : les ressources non prises en charge sont ignorées et signalées, et les nouvelles offres cloud peuvent mettre du temps à apparaître.
- **Pas une plateforme de facturation complète** : Infracost estime le coût de l’infrastructure ; il ne remplace pas le tableau de bord de facturation du fournisseur cloud pour les factures réelles, les taxes ou les crédits.

---

## Références

- Site officiel : <https://www.infracost.io>
- Dépôt GitHub : <https://github.com/infracost/infracost>
- Documentation sur la couverture des ressources : <https://www.infracost.io/docs/supported_resources/overview/>
- Extension VS Code : <https://marketplace.visualstudio.com/items?itemName=Infracost.infracost>
- Slack communautaire : lien disponible sur le site Web d’Infracost