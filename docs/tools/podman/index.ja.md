---
title: Podman - デーモンレスコンテナ管理
description: Podman（デーモンレスコンテナエンジン）の包括的なガイド。コンテナ、ポッド、イメージの管理について説明します。
created: 2026-06-15
tags:
  - containers
  - podman
  - docker-alternative
  - devops
  - linux
status: draft
ecosystem: containers
---

# Podman - デーモンレスコンテナ管理

Podmanは、Red Hatが開発したオープンソースのデーモンレスコンテナエンジンです。完全なDocker互換性のあるコマンドラインインターフェースを提供し、ネイティブなポッドサポート、ルートレス動作、systemdとのシームレスな統合などのユニークな機能を備えています。PodmanはOCI（Open Container Initiative）標準に準拠しており、BuildahやSkopeoと並んでRed Hatのコンテナツールチェーンの主要コンポーネントです。

## Podmanとは？

Podman（**Pod Manager**の略）は、OCIコンテナ、イメージ、ボリューム、ポッドを管理するためのツールです。Dockerとは異なり、Podmanは中央のバックグラウンドデーモン（`dockerd`）に依存**しません**。その代わり、コンテナはPodmanコマンドの直接の子プロセスとして実行されるため、標準的なLinuxプロセスツールやsystemdで管理が容易になります。

## Podmanを選ぶ理由

- **デーモンレスアーキテクチャ** – 永続的なデーモンがないため、リソース使用量が少なく、トラブルシューティングが簡単で、initシステムとの統合が容易です。
- **デフォルトでルートレス** – ユーザ名前空間を使用してルート権限なしでコンテナを実行でき、攻撃対象領域を大幅に削減します。
- **ポッドサポート** – 名前空間を共有するコンテナグループ（ポッド）の組み込みサポートにより、Kubernetesのコンセプトを反映し、ポッドマニフェストのローカル開発が可能です。
- **Docker互換性** – `podman run`、`podman build`、`podman ps`などのコマンドはDockerの相当コマンドに直接マッピングされ、エイリアス`alias docker=podman`を設定することでほとんどのワークフローでシームレスに動作します。
- **Systemd統合** – 任意のコンテナのsystemdユニットファイルを生成し、自動起動、障害時の再起動、最新のLinuxサービス管理との統合を実現します。
- **オープンソース＆コミュニティ** – Red Hatが所有し、CNCFエコシステムの一部であり、強力なコミュニティとエンタープライズサポートを備えています。

## インストール

Podmanは主要なオペレーティングシステムで利用可能です。開始する最も簡単な方法はプラットフォームによって異なります。

### Linux

**Fedora / RHEL / CentOS**
```bash
sudo dnf install podman
```

**Debian / Ubuntu**
```bash
sudo apt-get update && sudo apt-get install podman
```

**Arch Linux**
```bash
sudo pacman -S podman
```

### macOS

[Homebrew](https://brew.sh/)を使用：
```bash
brew install podman
podman machine init       # Create a Linux VM
podman machine start      # Start the VM
```

### Windows

[Winget](https://learn.microsoft.com/en-us/windows/package-manager/)を使用：
```bash
winget install RedHat.Podman
```
または、[Podmanリリースページ](https://github.com/containers/podman/releases)からインストーラをダウンロードしてください。

インストール後、`podman machine init`と`podman machine start`を実行して管理対象VMをセットアップしてください（macOSとWindowsで必要）。

## 主な機能

### デーモンレス＆ルートレスコンテナ

Podmanは中央デーモンの必要性を排除します。`podman run`や`podman exec`の呼び出しごとに、呼び出し元ユーザーのUIDの下で直接コンテナプロセスをフォークします。ルートレスモードがデフォルトであり、Podmanのユーザー名前空間は、非特権ホストユーザーをコンテナ内のrootにマッピングします。SELinuxやseccompポリシーによってセキュリティがさらに強化されています。

### ポッド（ネイティブなKubernetesスタイルのグループ化）

ポッドは、同じネットワーク名前空間、IPアドレス、ポートスペースを共有するコンテナの集合です。ポッドを使用すると、一緒にデプロイされるマルチコンテナアプリケーションを簡単にモデル化できます。

```bash
# Create a pod with an exposed port
podman pod create --name mypod -p 8080:80

# Run an nginx container inside the pod
podman run --pod mypod -d --name web nginx:alpine

# Run a helper container (e.g., sidecar) in the same pod
podman run --pod mypod -d --name logger busybox tail -f /dev/null

# List pods
podman pod ps
```

### Systemd統合

コンテナはネイティブのsystemdサービスとして管理でき、起動時や障害時の自動再起動が保証されます。

```bash
# Run a container in the background
podman run -d --name myapp my-image

# Generate systemd unit files
podman generate systemd --new --files --name myapp

# Copy the generated file to the systemd directory and enable it
sudo cp container-myapp.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now container-myapp.service
```

### Docker互換性と`podman-compose`

PodmanはほとんどのDockerコマンドを直接受け入れます。Docker Composeファイルには、`podman compose`を使用できます（`podman-compose`またはDocker Composeプラグインが個別にインストールされている必要があります）。

```yaml
# Example docker-compose.yml works with podman-compose
version: '3'
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
```

実行方法：
```bash
podman-compose up -d
```

### Buildahを使用したイメージビルド

`podman build`も利用できますが、専用のBuildahツールは、コンテナランタイムなしでイメージを作成する機能など、イメージビルドをより細かく制御できます。

```bash
podman build -t my-app .
```

## 基本的な使い方

以下のコマンドはDockerの構文を反映しており、Podman環境とDocker環境の両方で安全に学習できます。

```bash
# Pull an image
podman pull docker.io/library/alpine:latest

# List images
podman images

# Run a container in the foreground, interactive shell
podman run -it --rm alpine /bin/sh

# Run a detached web server
podman run -d --name web -p 8080:80 nginx:alpine

# List running containers
podman ps

# List all containers (including stopped)
podman ps -a

# Execute a command inside a running container
podman exec -it web /bin/sh

# View logs
podman logs web

# Stop and remove a container
podman stop web && podman rm web

# Remove all unused images
podman image prune -a
```

## Dockerからの移行

現在Dockerを使用している場合、移行は簡単です：

- **CLIのエイリアス**: `alias docker=podman`（シェルプロファイルに追加）。
- **Docker Compose**: `podman-compose`をインストールするか、Podmanのソケットアクティベーション（`podman system service`）を使用してDocker Composeプラグインを利用します。
- **ボリュームとネットワーク**: PodmanはDockerスタイルのボリュームとCNI/Netavarkネットワークをサポートしています。
- **Dockerfile**: `podman build`は任意の標準Dockerfileで動作します。

> ⚠️ *注意*: SwarmモードやDocker Contextsなど、Docker固有の一部機能はPodmanでは実装されていません。Swarmの場合は、NomadやKubernetesなどの代替手段を検討してください。

## 参考情報

- [Podman公式ドキュメント](https://docs.podman.io/)
- [Podman GitHubリポジトリ](https://github.com/containers/podman)
- [Red Hatコンテナツール](https://www.redhat.com/en/topics/containers)
- [Podmanによるルートレスコンテナ](https://rootlesscontaine.rs/getting-started/podman/)
- [Podman vs Docker: 包括的な比較](https://developers.redhat.com/articles/2023/08/29/why-podman-replaces-docker)

---

Podmanは、開発ワークフローと本番ワークフローの両方に適した、現代的で安全かつ柔軟なコンテナエンジンです。デーモンレスアーキテクチャとsystemdとの深い統合により、Linux中心の環境に最適な選択肢となります。さらに、Docker互換のAPIにより、既存ユーザーは容易に学習できます。ラップトップで単一のコンテナを実行する場合でも、CIパイプラインでポッドのフリートをオーケストレーションする場合でも、Podmanは中央デーモンのオーバーヘッドなしに必要なツールを提供します。