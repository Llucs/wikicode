---
title: Jenkins CI/CD 自動化サーバー
description: ソフトウェアプロジェクトの継続的インテグレーションと継続的デリバリーのための自動化サーバーです。
created: 2026-06-15
tags:
  - jenkins
  - ci
  - cd
  - devops
  - automation
  - java
status: draft
ecosystem: ci-cd
---

# Jenkins CI/CD Automation Server

## 概要

Jenkinsは、Javaで書かれたオープンソースの自動化サーバーです。ソフトウェアのビルド、テスト、デプロイを自動化し、継続的インテグレーション（CI）と継続的デリバリー（CD）を可能にします。元々はHudsonプロジェクトからフォークされましたが、現在ではパイプラインオーケストレーションの業界標準となっています。

## なぜJenkinsなのか？

- **拡張性:** 1,800以上のプラグインにより、事実上すべてのDevOpsツール（Git、Docker、Kubernetes、AWS、Azure、Slackなど）と統合できます。
- **柔軟性:** シンプルなフリースタイルジョブから、コードとして定義された複雑なマルチステージパイプラインまでサポートします。
- **分散ビルド:** マスター/エージェントアーキテクチャにより、多くのマシンにワークロードを分散できます。
- **オープンソースで成熟:** 無料（MITライセンス）で、大規模なコミュニティと豊富なドキュメントがあります。
- **リッチなエコシステム:** SCM、ビルドツール、テストレポート、アーティファクト管理、デプロイ、通知のためのプラグインがあります。

## インストール

JenkinsにはJava 8、11、または17（LTS推奨）が必要です。複数のインストール方法があります。

### WARファイル

```bash
java -jar jenkins.war
```
Jenkinsがスタンドアロンでポート8080で実行されます。クイックテストに最適です。

### ネイティブパッケージ

**Debian/Ubuntu:**

```bash
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins
```

**Red Hat/CentOS:**

```bash
sudo wget -O /etc/yum.repos.d/jenkins.repo \
  https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
sudo yum install jenkins
```

### Docker

```bash
docker run -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

### Kubernetes（Helm Chart）

```bash
helm repo add jenkins https://charts.jenkins.io
helm repo update
helm install jenkins jenkins/jenkins --namespace jenkins --create-namespace
```

インストール後、`http://localhost:8080` でJenkinsにアクセスし、ログまたはファイル（`/var/lib/jenkins/secrets/initialAdminPassword`）から初期管理者パスワードを取得します。

## 基本的な使い方

### 1. ジョブを作成する

- **フリースタイルプロジェクト:** 数ステップで簡単なタスクを実行。
- **パイプライン:** `Jenkinsfile`にビルドライフサイクルを定義。

### 2. ソースコードを構成する

- 認証情報（ユーザー名/パスワードまたはSSHキー）を使用してGitリポジトリに接続します。

### 3. トリガーを設定する

- **SCMポーリング:** `* * * * *`（毎分）
- **Webhook:** プッシュ時にGitHub/GitLabから。
- **Cron**: 例: `H 2 * * 1-5`（平日午前2時）

### 4. ビルドステップを追加する

- シェル/バッチコマンドの実行。
- Maven/Gradleのゴールの実行。
- Dockerイメージのビルド。
- 他のビルドツールの呼び出し。

### 5. ビルド後のアクション

- アーティファクトのアーカイブ（例: JAR、レポート）。
- テスト結果の公開（JUnit、HTMLレポート）。
- サーバーへのデプロイ。
- 通知の送信（Slack、メール）。

## 主な機能と例

### パイプラインasコード（Pipeline as Code）

ソースリポジトリ内の宣言的な`Jenkinsfile`:

```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                sh 'mvn clean compile'
            }
        }
        stage('Test') {
            steps {
                sh 'mvn test'
            }
            post {
                always {
                    junit 'target/surefire-reports/*.xml'
                }
            }
        }
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh 'mvn deploy'
            }
        }
    }
    post {
        failure {
            slackSend channel: '#ops', message: "Build failed."
        }
    }
}
```

このパイプラインはコミットのたびに自動的に実行され、コードのコンパイル、テストの実行、テスト結果のアーカイブ、そして`main`ブランチからのデプロイを行います。

### マルチブランチパイプライン

リポジトリ内の各ブランチおよびプルリクエストに対して自動的にパイプラインを作成します。

```groovy
// Jenkins UI: 新規アイテム → マルチブランチパイプライン → Gitソースを追加
// ブランチ内のJenkinsfileが実行を制御します。
```

### エージェントによる分散ビルド

Jenkinsはエージェントにラベル（例: "linux"、"docker"、"high-mem"）を付け、ジョブを割り当てることができます。

```groovy
pipeline {
    agent { label 'linux && docker' }
    stages {
        stage('Test') {
            steps {
                sh 'docker build -t myapp .'
            }
        }
    }
}
```

### 共有ライブラリ（Shared Libraries）

リポジトリ間で再利用可能なパイプラインコード。共有ライブラリのGitリポジトリで定義します。

**vars/buildApp.groovy:**

```groovy
def call(String project) {
    sh "mvn -f ${project}/pom.xml clean package"
}
```

その後、任意の`Jenkinsfile`で:

```groovy
library identifier: 'my-lib@master', retriever: modernSCM(...)
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                buildApp('my-service')
            }
        }
    }
}
```

### Kubernetesとの統合

Kubernetesプラグインを使用して、ビルドエージェントを動的に起動します。

```groovy
pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: maven
    image: maven:3.8.4-openjdk-11
    command: ['cat']
    tty: true
"""
        }
    }
    stages {
        stage('Build') {
            steps {
                container('maven') {
                    sh 'mvn clean install'
                }
            }
        }
    }
}
```

### REST API

Jenkinsは自動化のための包括的なREST APIを提供します。ジョブをトリガーするcurlの例:

```bash
curl -X POST http://jenkins-url/job/my-job/build \
  --user username:api-token
```

ジョブ一覧の取得:

```bash
curl http://jenkins-url/api/json
```

### Blue Ocean UI

パイプラインのためのモダンでビジュアルなインターフェース（Blue Oceanプラグインが必要）。ビルド、ログ、パイプラインステージのグラフィカルなビューを提供します。

## Configuration as Code (JCasC)

`configuration-as-code`プラグインを使用して、Jenkinsの構成をYAMLで宣言的に管理します。

**jenkins.yaml:**

```yaml
jenkins:
  systemMessage: "Managed by JCasC"
  numExecutors: 2
  globalNodeProperties:
  - envVars:
      env:
      - key: VARIABLE1
        value: "value1"
security:
  globalMatrixAuthorizationStrategy:
    grantedPermissions:
      - "Overall/Administer:admin"
      - "Job/Build:developer"
jobs:
  - script: >
      multibranchPipelineJob('my-pipeline') {
        branchSources {
          git {
            remote('https://github.com/org/repo.git')
            credentialsId('github-creds')
          }
        }
      }
```

起動時に適用するか、`reload-configuration-as-code`エンドポイントを介して適用します。

## プラグイン

主要なプラグインカテゴリ:

- **SCM:** Git、GitHub、GitLab、Bitbucket、Subversion
- **ビルド:** Maven、Gradle、Ant、NodeJS、Docker Pipeline
- **テスト:** JUnit、HTML Publisher、Allure、Cucumber Reports
- **デプロイ:** Kubernetes、AWS CodeDeploy、Ansible、SSH
- **通知:** Slack、Email Extension、PagerDuty
- **ユーティリティ:** Credentials Binding、Pipeline Utility Steps、Job DSL

## ベストプラクティス

- **パイプラインasコードを使用する** – `Jenkinsfile`をプロジェクトと共にSCMに保存します。
- **共有ライブラリを使用する** – パイプラインロジックの重複を避けます。
- **エージェントをステートレスに保つ** – DockerまたはKubernetesエージェントを使用します。
- **認証情報を安全に管理する** – 平文ではなくCredentialsプラグインを使用します。
- **JENKINS_HOMEをバックアップする** – ジョブ構成とプラグインデータを定期的にバックアップします。
- **同時実行を制限する** – リソースに敏感なジョブには`properties([disableConcurrentBuilds()])`を使用します。
- **Blue Oceanを使用する** – パイプラインの視覚化を向上させます。
- **Prometheusで監視する** – Prometheus Metricsプラグインを使用します。

## トラブルシューティング

- **ログを確認する:** `tail -f /var/log/jenkins/jenkins.log`
- **構成を再読み込みする:** 「Jenkinsの管理」→「設定をディスクから再読み込み」
- **ビルドキューをクリアする:** ビルドキュー項目をクリック→「キャンセル」
- **Groovyスクリプトを実行する:** 「Jenkinsの管理」→「スクリプトコンソール」で診断。
- **ヒープサイズを増やす:** 起動時に`JAVA_OPTS="-Xmx2048m -Xms1024m"`を設定します。

## 関連リンク

- [Jenkins公式ドキュメント](https://www.jenkins.io/doc/)
- [プラグインインデックス](https://plugins.jenkins.io/)
- [パイプラインシンタックスジェネレーター](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [JCasCドキュメント](https://www.jenkins.io/projects/jcasc/)

---

*このページは開発チーム向けのWikiCodeドキュメントの一部として作成されました。*