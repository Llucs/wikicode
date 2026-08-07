title: Infracost – Infrastructure as Code（IaC）のためのリアルタイムクラウドコスト見積もり
description: デプロイ前にTerraform、CloudFormation、CDKからクラウドコストを見積もるオープンソースCLI、Infracostの実践ガイド。
created: 2026-08-07
tags:
  - infracost
  - terraform
  - finops
  - cloud-cost
  - infrastructure-as-code
  - devtools
status: draft

# Infracost

Infracostは、オープンソースで開発者ファーストのツールであり、**リアルタイムのクラウドコスト見積もり**をInfrastructure as Code（IaC）ワークフローに直接もたらします。Terraform、Terragrunt、CloudFormation、AWS CDKプロジェクトを指定すると、リソースが1つもデプロイされる前に、詳細な月間コスト内訳を生成します。

このページでは、Infracostとは何か、なぜチームが採用するのか、インストール方法と使用方法、そしてTerraformやその他のIaCツールチェーンの標準的なコンパニオンとなっている主要機能について説明します。

---

## Infracostとは？

Infracostは、IaC定義とプランを解析し、AWS、Azure、Google Cloudのライブ価格データを参照して、リソースの月間コストを正確に報告するコマンドラインツール（および付属のSaaSダッシュボード）です。**静的コード**と**Terraformプランファイル**の両方で動作するため、提案された変更を適用する前にコストへの影響を表示できます。

このプロジェクトは2020年に開始され、すぐにTerraformワークフローの事実上の標準的なコスト見積もりレイヤーになりました。コアCLIは無料でオープンソースであり、オプションのInfracost Cloudダッシュボードは、チーム全体の可視性、予算、履歴トレンド分析を追加します。

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

## なぜInfracostなのか？

従来のクラウドコスト管理は*事後対応型*です。月末に請求書が届き、チームは何が起きたのかを把握しようと慌てます。Infracostは**shift-left FinOps**を促進します。つまり、高コストなインフラストラクチャの決定が行われた瞬間にそれを検出します。

- **コードレビュー中** — PRコメントにコスト差分（`+$50.12`）が表示されるため、レビュアーは予算超過の変更を却下できます。
- **エディタ内** — VS CodeおよびJetBrains拡張機能が、HCLを入力する際にインラインでコストを表示します。
- **CI/CD内** — パイプラインは、デプロイ前にコスト回帰、タグ欠落、予算違反で失敗させることができます。
- **ターミナル内** — 簡単な`breakdown`コマンドで、電卓やスプレッドシートを使わずに「このモジュールのコストはいくらか？」に答えます。

Infracostは、エンジニアがすでに生成するコードとプラン成果物をそのまま読み取るため、追加の計装は不要で、実際にデプロイされているものからの乖離もありません。

---

## サポートされているプラットフォーム

| IaCツール       | クラウド          | 備考                                     |
|----------------|-----------------|-------------------------------------------|
| Terraform HCL  | AWS、Azure、GCP | 完全なリソースカバレッジと使用プロファイル |
| Terragrunt     | AWS、Azure、GCP | Terragruntプロジェクトを自動検出          |
| Terraform plan | AWS、Azure、GCP | `terraform show -json`出力             |
| CloudFormation | AWS             | テンプレートとスタックセットのサポート            |
| AWS CDK        | AWS             | 合成されたCloudFormationテンプレート経由   |

サポートされていないリソースは「スキップ」としてメッセージとリソースカバレッジドキュメントへのリンク付きで報告されるため、出力がコストについて黙って嘘をつくことはありません。

---

## インストール

### Homebrew（macOS / Linux）

```bash
brew install infracost
```

### シェルスクリプト（Linux / macOS）

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

### インストールの確認

```bash
infracost --version
infracost --help
```

---

## 認証

Infracostは、ライブのクラウド価格APIを照会するため、APIキーが必要です。[infracost.io/dashboard](https://www.infracost.io)で無料アカウントを登録し、CLIからログインします：

```bash
infracost auth login
```

あるいは、CI環境用にAPIキーを直接エクスポートします：

```bash
export INFRACOST_API_KEY=my-api-key
```

ホスト型Infracost APIに価格データを送信できないユーザーのために、CLIはエアギャップ環境向けのセルフホスト型価格ソース（`INFRACOST_PRICING_API_ENDPOINT`）をサポートしています。

---

## 基本的な使用方法

### 1. Terraformディレクトリのコスト内訳

```bash
infracost breakdown --path . --format table
```

これにより、現在のディレクトリ内のHCLが評価され、リソースごとの月間コストテーブルが出力されます。サポートされている形式には、`table`、`json`、`html`、`markdown`、`sarif`、`github-comment`があります。

### 2. Terraformプランのコスト内訳

最も正確な全体像はプランから得られます。なぜなら、`count`、`for_each`、条件ロジックなどのコンテキストが含まれるためです：

```bash
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
infracost breakdown --terraform-plan-json plan.json --show-skipped
```

`--show-skipped`フラグは、Infracostが価格設定できなかったリソースを一覧表示するため、カバレッジを評価できます。

### 3. 差分モード

差分モードは、2つの状態間の**コスト変更**を示します。通常は、現在デプロイされている状態と提案された変更との間です：

```bash
infracost diff --path plan.json
```

出力例の抜粋：

```
Project: my-project

+ aws_instance.api_server
  +$75.00

- aws_instance.legacy_server
  -$58.49

Monthly cost change: +$16.51
```

### 4. プルリクエストコメントの生成

内訳をJSONファイルに保存した後、CIがGitHub、GitLab、Bitbucketに貼り付けられるPRコメント形式に変換します：

```bash
infracost breakdown --path . --format json > infracost.json
infracost output --path infracost.json --format github-comment
```

---

## 主要機能

### インラインエディタ統合

[Infracost VS Code拡張機能](https://marketplace.visualstudio.com/items?itemName=Infracost.infracost)は、Terraformファイルの各リソースの横にインラインのコスト見積もりを表示し、サイドバーに完全なリソース内訳も表示します。また、FinOpsポリシーの問題（タグ欠落、コスト回帰）をエディタ内で直接提示します。JetBrains IDEも同様の拡張機能でサポートされています。

### CI/CD統合

Infracostは、GitHub Actions、GitLab CI、Bitbucket Pipelines、Azure DevOps向けのネイティブ統合を提供しています。最小限のGitHub Actionsワークフローは次のようになります：

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

PRコメントには、予測される総コスト、リソースごとの差分、およびポリシー違反が含まれます。

### 現実的な見積もりのための使用プロファイル

デフォルトの見積もりでは、リソースが月730時間フル稼働すると想定されています。多くのリソース（EC2、Lambda、RDS、Kubernetes）は顧客固有の使用ファイルをサポートしており、見積もりを現実に即したものにできます：

```bash
infracost breakdown --path . --usage-file usage.yml
```

プロジェクトからスターター使用ファイルを生成するには：

```bash
infracost breakdown --path . --sync-usage-file
```

使用ファイルは次のようになります：

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

### Policy as Code（OPA / Rego）

予算の適用とタグ付けルールは、OPAポリシーとして記述されます。`.infracost`ポリシーディレクトリにポリシーを定義し、次のコマンドを実行します：

```bash
infracost policy --path infracost.json --policy-path policy/
```

月間コストがしきい値を超える変更をブロックする単純なポリシー：

```rego
package infracost

deny[msg] {
  cost := input.projects[_].diff.totalMonthlyCost
  cost > 1000
  msg := sprintf("Monthly cost $%.2f exceeds $1000 budget", [cost])
}
```

ポリシーは同じPRコメントフローと統合されるため、CIはコストとコンプライアンスの両方の失敗でマージをブロックできます。

### 節約の検出

価格設定に加えて、Infracostはライトサイジングの機会、未使用リソース、誤設定されたインスタンスタイプをフラグ付けします。これらは内訳出力に「savings」項目として推定月間削減額とともに表示され、FinOpsダッシュボード用のJSON出力にも公開されます。

### Infracost Cloud

オプションのSaaSダッシュボードは次を追加します：

- プロジェクトおよび環境ごとの履歴コストトレンド
- アラートとしきい値ポリシー付きの予算
- チームレベルの分析と支出の帰属
- プラットフォームチームが管理する中央ポリシーライブラリ

CLIが使用するAPIキーは同じアカウントに認証されるため、ローカルデータとクラウドデータの同期が保たれます。小規模チーム向けの無料ティアも利用できます。

### レポート用のマルチフォーマット出力

```bash
# JSON for programmatic consumption / FinOps pipelines
infracost breakdown --path . --format json > cost.json

# HTML report for stakeholders
infracost breakdown --path . --format html > report.html

# SARIF for GitHub code scanning
infracost breakdown --path . --format sarif > infracost.sarif
```

---

## 例：完全なshift-leftワークフロー

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

開発者は、`terraform apply`を実行する*前*に`+$400.00 / 月`の項目を確認し、インスタンスタイプをダウングレードするか、スポットインスタンスに切り替えることができます。

---

## 設定ファイル

プロジェクトレベルのデフォルトは`infracost.yml`に保存できます：

```yaml
version: 0.1
projects:
  - path: .
    name: my-project
    usage_file: usage.yml
    terraform_plan_flags:
      - -var-file=prod.tfvars
```

これにより、CIコマンドを短く保ち、環境間で一貫性を維持できます。

---

## 制限事項

- **リスト価格であり、契約価格ではない**：見積もりはオンデマンドのリスト価格を反映します。カスタム交渉割引、EDP価格、コミット使用割引は、別途またはカスタム価格上書きで考慮する必要があります。
- **価格APIアクセスが必要**：CLIはInfracost価格APIを照会しますが、エアギャップ使用向けのセルフホストエンドポイントも存在します。
- **カバレッジは広いが普遍的ではない**：サポートされていないリソースはスキップされて報告され、新しいクラウドサービスのサポート追加には時間がかかることがあります。
- **完全な請求プラットフォームではない**：Infracostはインフラストラクチャコストを見積もります。実際の請求書、税金、クレジットについては、クラウドプロバイダーの請求ダッシュボードを置き換えるものではありません。

---

## 参考リンク

- 公式サイト：<https://www.infracost.io>
- GitHubリポジトリ：<https://github.com/infracost/infracost>
- リソースカバレッジドキュメント：<https://www.infracost.io/docs/supported_resources/overview/>
- VS Code拡張機能：<https://marketplace.visualstudio.com/items?itemName=Infracost.infracost>
- コミュニティSlack：Infracostウェブサイトからリンクされています