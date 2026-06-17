---
title: SonarQube
description: CI/CDパイプラインと統合してコードレビューを自動化し、脆弱性を検出するコード品質およびセキュリティ分析ツールです。
created: 2026-06-16
tags:
  - code-quality
  - security
  - static-analysis
  - ci-cd
  - sonarqube
status: draft
---

# SonarQube

## SonarQubeとは

SonarQubeは、SonarSourceによるオープンソースプラットフォームで、コード品質とセキュリティを継続的に検査します。ソースコードに対して静的アプリケーションセキュリティテスト（SAST）を実行し、30以上のプログラミング言語（Java、C#、JavaScript、TypeScript、Python、Goなど）にわたって、**バグ**、**脆弱性**、**コードスメル**、**重複**を検出します。SonarQubeは開発ワークフローにおける中央品質ハブとして機能し、カスタマイズ可能なポリシー（品質ゲート）を適用して問題のあるコードのリリースを防止します。

## SonarQubeを使う理由

- **早期に問題を発見** – CI/CDパイプラインに統合して、すべてのコミットとプルリクエストを自動的にレビューします。
- **品質基準の適用** – ビルドが成功する前に必ず通過しなければならない品質ゲート（例：新しいバグがない、カバレッジしきい値）を定義します。
- **技術的負債の削減** – 既存の問題を修正するために必要な労力を定量化し、時間の経過とともに改善状況を追跡します。
- **セキュリティの向上** – OWASP Top 10やCWEの脆弱性を特定し、手動レビューが必要なセキュリティホットスポットをフラグ付けします。
- **コードレビューの自動化** – フォーマット、ヌルポインタ、リソースリークなどの単純な問題の検出を人間のレビューアから解放し、アーキテクチャとロジックに集中できるようにします。

## 主な機能

### Static Code Analysis
SonarQubeは、信頼性、セキュリティ、保守性の問題についてソースコードをスキャンします。高度なデータフロー解析と制御フロー解析を実行して、以下を検出します：
- 潜在的なヌルポインタ参照外し
- リソースリーク
- SQLインジェクションおよびクロスサイトスクリプティング（XSS）の欠陥
- ハードコードされた認証情報

### Quality Gates
品質ゲートは、プロジェクトが合格するために満たさなければならないメトリクス（例：`New Coverage < 80%`、`New Bugs > 0`）に関するブール条件のセットです。SonarQubeにはデフォルトのゲートが用意されており、チームのポリシーに合わせてカスタムゲートを作成できます。

### Security Hotspots
SonarQubeは手動のセキュリティレビューが必要なコードを強調表示します。これらのホットスポットは自動的に脆弱性として確認されるわけではありませんが、攻撃者が悪意のある入力を注入する可能性がある領域です。開発者はこれらをレビューし、「安全」または「レビューが必要」としてマークできます。

### Technical Debt Measurement
SonarQubeは問題を**技術的負債**メトリクスに変換し、日数またはコスト（例：USD）で表現します。これにより、チームはリファクタリングの予算を立て、優先順位を付けることができます。

### Branch and Pull Request Analysis
SonarQubeはフィーチャーブランチとプルリクエストを分析でき、新しいコードにのみ品質ゲートを適用できます。これは、コードベース全体ではなく差分に焦点を当てる**Clean as You Code**ワークフローに自然に適合します。

### DevOps Integrations
SonarQubeは以下とネイティブに統合します：
- **GitHub、GitLab、Bitbucket** – プルリクエストのデコレーション、インラインコメント。
- **Jenkins、Azure DevOps、Travis CI、CircleCI** – ビルドパイプラインの統合。
- **Maven、Gradle、.NET、SonarScanner CLI** – スキャンの呼び出し。

### SonarLint IDE Extension
SonarLint（VS Code、IntelliJ、Eclipse、Visual Studio用）はSonarQubeサーバーに接続し、同じルールをローカルに適用して、入力時にリアルタイムのフィードバックを提供します。

---

## インストール

SonarQubeには**Java 17以上**と専用のデータベース（本番環境ではPostgreSQL推奨）が必要です。スタンドアロンのWebアプリケーションとして実行されます。

### Docker（評価用クイックスタート）

```bash
docker run -d --name sonarqube \
  -p 9000:9000 \
  -e SONAR_JDBC_URL=jdbc:postgresql://host:port/sonarqube \
  -e SONAR_JDBC_USERNAME=sonar \
  -e SONAR_JDBC_PASSWORD=sonar \
  sonarqube:community
```

> **注:** Community Editionには、ブランチ分析やプルリクエストデコレーションなどの高度な機能は含まれていません。これらが必要な場合は、Developer Edition以上を検討してください。

### 手動インストール（Linux / macOS）

1. 最新バージョンを[SonarSource Download](https://www.sonarsource.com/products/sonarqube/downloads/)からダウンロードします。
2. アーカイブを展開します。
3. データベース接続を `conf/sonar.properties` で設定します：
   ```properties
   sonar.jdbc.url=jdbc:postgresql://localhost/sonarqube
   sonar.jdbc.username=sonar
   sonar.jdbc.password=sonar
   ```
4. サーバーを起動します：
   ```bash
   # Linux/macOS
   bin/linux-x86-64/sonar.sh start
   # Windows
   bin/windows-x86-64/StartSonar.bat
   ```
5. Web UIに `http://localhost:9000` でアクセスします。デフォルトの認証情報: `admin` / `admin`。

---

## 基本的な使い方

### 1. プロジェクトの設定

SonarQubeにログインし、**新しいプロジェクトを作成**をクリックして、キーを指定し、品質プロファイルと品質ゲートを選択します。次に、**プロジェクトトークン**（例：`sqa_xxxx`）を生成します。このトークンはスキャナーを認証します。

### 2. スキャンの実行

#### Mavenを使用

```bash
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=my-project \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqa_xxxx
```

#### Gradleを使用

```groovy
// build.gradle
plugins {
    id "org.sonarqube" version "4.4.1.3373"
}

sonar {
    properties {
        property "sonar.projectKey", "my-project"
        property "sonar.host.url", "http://localhost:9000"
        property "sonar.token", "sqa_xxxx"
    }
}
```

```bash
./gradlew sonarqube
```

#### SonarScanner CLIを使用

SonarScannerをインストールし（SonarSourceからダウンロード）、次に実行します：

```bash
sonar-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=sqa_xxxx
```

### 3. 結果の確認

スキャンが完了すると、SonarQubeダッシュボードには以下が表示されます：
- **品質ゲートステータス** – 合格または不合格。
- **問題** – 重大度（ブロッカー、クリティカル、メジャー、マイナー、情報）とタイプ（バグ、脆弱性、コードスメル）でグループ化。
- **セキュリティホットスポット** – 手動レビューが必要なコード領域。
- **カバレッジ** – JaCoCoやdotCoverなどのツールを使用している場合、カバレッジレポートをインポートします。
- **重複** – 重複したブロックが強調表示されます。

---

## CI/CDとの統合

### GitHub Actions

```yaml
name: SonarQube Scan
on: [push]
jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@v1.9.0
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    environment {
        SONAR_HOST_URL = 'http://sonarqube:9000'
        SONAR_AUTH_TOKEN = credentials('sonarqube-token')
    }
    stages {
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube Server') {
                    sh 'mvn clean verify sonar:sonar'
                }
            }
        }
    }
}
```

### GitLab CI/CD

```yaml
variables:
  SONAR_USER_HOME: "${CI_PROJECT_DIR}/.sonar"
  GIT_DEPTH: "0"

sonarqube-check:
  image: maven:3.8.6-openjdk-17
  script:
    - mvn clean verify sonar:sonar
      -Dsonar.projectKey=$CI_PROJECT_ID
      -Dsonar.host.url=$SONAR_HOST_URL
      -Dsonar.token=$SONAR_TOKEN
      -Dsonar.branch.name=$CI_COMMIT_REF_NAME
```

---

## Clean as You Code メソッド

SonarQubeは**Clean as You Code**アプローチを推奨しています。既存のすべての問題を修正しようとするのではなく、今日書くコードで新しい問題を発生させないことに集中します。これは以下の点に反映されています：

- **新しいコードに焦点** – メトリクスと品質ゲートは新規/変更されたコードを対象とします。
- **プルリクエストデコレーション** – 問題はPRの差分に直接報告されます（GitHub、GitLab、Bitbucket）。
- **SonarLint** – 開発者はコミット前にIDEで問題を検出します。

これにより摩擦が軽減され、品質向上が持続可能になります。

---

## 結論

SonarQubeは、静的解析と品質ガバナンスのための成熟した広く採用されているツールです。開発パイプラインに統合することで、コードレビューを自動化し、セキュリティ基準を適用し、技術的負債を管理し、最終的により信頼性が高く安全なソフトウェアを提供できます。

高度な機能（ブランチ分析、ポートフォリオ管理、言語固有のカバレッジ）については、SonarQube Serverの**Developer**、**Enterprise**、または**Data Center**エディションへのアップグレード、またはクラウドホスト型の**SonarQube Cloud**（旧SonarCloud）の使用を検討してください。