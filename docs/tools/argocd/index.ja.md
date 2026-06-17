---
title: ArgoCD – GitOpsによるKubernetes向け継続的デリバリー
description: ArgoCDは、Gitリポジトリを単一の真実の情報源としてKubernetesアプリケーションを同期する、宣言的かつGitOps駆動の継続的デリバリーツールです。
created: 2026-06-15
tags:
  - gitops
  - kubernetes
  - continuous-delivery
  - argocd
  - devops-tools
status: draft
ecosystem: kubernetes
---

# ArgoCD – GitOpsによるKubernetes向け継続的デリバリー

## ArgoCDとは？

ArgoCDは、Kubernetes専用に設計された宣言的かつ**GitOps**な継続的デリバリー（CD）ツールです。アプリケーション定義とKubernetesマニフェストのための**単一の真実の情報源**としてGitリポジトリを扱います。ArgoCDは、実際のクラスターの状態を常に監視し、Gitで定義された望ましい状態と調整することで、完全に自動化された、監査可能で再現性のあるデプロイを実現します。

## ArgoCDの利点

- **宣言的かつバージョン管理** – すべてのインフラストラクチャとアプリケーション構成はGitに保存されます。変更は命令的なコマンドではなく、プルリクエストによって行われます。
- **自動自己修復** – システムは、手動での変更をすべてGitで定義された状態に戻すことで、構成のドリフトを自動的に修正します。
- **監査証跡** – すべてのデプロイがGit履歴に記録され、不変の監査ログを提供します。
- **マルチクラスタ管理** – 単一のArgoCDインスタンスで、数百のKubernetesクラスタにまたがるアプリケーションを管理できます。
- **構成管理に依存しない** – プレーンなYAML、Helm、Kustomize、Jsonnetなどと連携します。

## インストール

ArgoCDは、数分で任意のKubernetesクラスターにインストールできます。

### 1. 名前空間を作成し、マニフェストを適用する

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. APIサーバーにアクセスする（ポートフォワーディング）

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

これで、`https://localhost:8080`でWeb UIにアクセスできます。

### 3. 初期管理者パスワードを取得する

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

### 4. CLIを使用してログインする

```bash
argocd login localhost:8080
```

ユーザー名 `admin` と前の手順で取得したパスワードを使用します。

## 基本的な使い方

### Gitリポジトリを接続する

```bash
argocd repo add https://github.com/my-org/my-app.git
```

### ターゲットクラスターを登録する

ターゲットがArgoCDが実行されているクラスターと同じでない場合は、登録します。

```bash
argocd cluster add <kube-context-name>
```

### アプリケーションを定義する（宣言的YAML）

ファイル `nginx-app.yaml` を作成します。

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: nginx-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/my-org/nginx.git'
    path: production
    targetRevision: HEAD
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

適用します。

```bash
kubectl apply -f nginx-app.yaml
```

### アプリケーションを同期する

手動同期（または自動同期ポリシーが処理します）。

```bash
argocd app sync nginx-prod
```

同期は、Web UIから、またはGitプロバイダーからのWebhookを介してトリガーすることもできます。

## 主要機能とコマンド

### 自動同期と自己修復

- **自動同期** – ArgoCDは、追跡対象ブランチに新しいコミットがプッシュされるたびに、自動的に同期を開始できます。
- **自己修復** – 誰かがクラスター内のリソースを手動で変更した場合、ArgoCDはそれらをGitで定義された状態に戻します。

`syncPolicy.automated` の下でYAMLで設定するか、CLI経由で設定します。

```bash
argocd app set nginx-prod --sync-policy automated --auto-prune --self-heal
```

### マルチクラスタ管理

1つのArgoCDインスタンスを使用して、異なる名前空間を持つ多くのクラスターにデプロイします。クラスターを一覧表示します。

```bash
argocd cluster list
```

### Application Sets（CRD）

パラメータに基づくアプリケーションの動的生成（例：各クラスター、各ブランチ、またはジェネレーターのリストから）。Gitジェネレーターを使用した例。

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: my-apps
spec:
  generators:
  - git:
      repoURL: 'https://github.com/my-org/deploy-config.git'
      revision: HEAD
      files:
        - path: "clusters/*/config.json"
  template:
    metadata:
      name: '{{ cluster }}-my-app'
    spec:
      project: default
      source:
        repoURL: 'https://github.com/my-org/my-app.git'
        targetRevision: HEAD
        path: '{{ env }}'
      destination:
        server: '{{ server }}'
        namespace: '{{ namespace }}'
```

### 構成管理ツール

ArgoCDは、以下のものからマニフェストをネイティブにレンダリングします。

- **Helm** – `helm.parameters` または `helm.valueFiles` を使用
- **Kustomize** – Kustomizeのオーバーレイディレクトリを指定するだけ
- **Jsonnet** – `jsonnet.libsonnet` ファイル経由

### 同期ウェーブとフック

リソースデプロイの順序を制御します。

- **同期ウェーブ** – `argocd.argoproj.io/sync-wave` アノテーションに整数を設定します（小さい数字が先にデプロイされます）。
- **同期フック** – データベースマイグレーションや検証のためにジョブ（pre-sync、sync、post-syncなど）を実行します。

### 通知とWebhook

- **組み込み通知** – 同期ステータスが変更されたときに、Slack、メール、またはカスタムエンドポイントにアラートを送信します。
- **Webhookトリガー** – GitHub/GitLab/Bitbucketと統合して、プッシュ時にほぼ瞬時に同期します。

### イメージアップデーター（オプションコンポーネント）

新しいイメージがレジストリにプッシュされたときに、Git内のコンテナイメージタグを自動的に更新します。このコンポーネント（Argo CD Image Updater）は、コンテナレジストリを監視し、新しいタグをGitソースにコミットします。

## アーキテクチャ – 高レベルコンポーネント

- **APIサーバー** – API、Web UI、CLIエンドポイントを公開します。認証、RBAC、プロジェクト管理を処理します。
- **リポジトリサーバー** – Gitリポジトリをキャッシュし、Kubernetesマニフェストを生成します（例：Helmチャート、Kustomizeオーバーレイのレンダリング）。
- **アプリケーションコントローラー** – アプリケーションの実際の状態を継続的に監視し、リポジトリサーバーからの望ましい状態と比較します。同期、prune、自己修復操作をトリガーします。

## まとめ

ArgoCDは、Kubernetesデプロイを完全に自動化されたGit駆動のワークフローに変えます。Gitを真実の情報源にすることで、構成のドリフトを排除し、不変の監査証跡を提供し、自己修復インフラストラクチャを実現します。Helm、Kustomize、マルチクラスタ管理、動的Application Setsの組み込みサポートにより、Kubernetes上のGitOpsの事実上の標準となっています。

公式ドキュメントについては、[argoproj.github.io/argo-cd](https://argoproj.github.io/argo-cd/) を参照してください。