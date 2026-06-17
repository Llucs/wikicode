---
title: Docker - コンテナ化ツール
description: Dockerは、アプリケーションをコンテナ内で開発、パッケージ化、デプロイするためのプラットフォームです。
created: 2026-06-13
tags:
  - containerization
  - development
  - deployment
status: draft
ecosystem: containers
---

## Dockerとは？

Dockerは、開発者がアプリケーションとそのすべての依存関係を、コンテナと呼ばれる標準化されたユニットにパッケージ化できるプラットフォームです。コンテナにより、開発、テスト、ステージング、本番などの異なる環境にアプリケーションを迅速かつ一貫してデプロイできます。

## Dockerを使う理由

1. **ポータビリティ**: Dockerコンテナは軽量で可搬性があり、アプリケーションをあらゆる環境にデプロイしやすくなります。
2. **分離**: 各コンテナは独自の分離された環境で実行され、他の実行中のプロセスの影響を受けないようにします。
3. **一貫性**: コンテナはアプリケーションのライフサイクルのさまざまな段階で一貫した開発環境を保証します。

## インストール

Dockerは、Windows、macOS、Linuxを含むさまざまなオペレーティングシステムにインストールできます。インストールプロセスはOSによって異なります。

### Ubuntu (Linux)の場合:
```sh
# Update package lists
sudo apt-get update

# Install Docker Engine
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

### Windowsの場合:
1. 公式サイトからDocker Desktopをダウンロードします。
2. インストーラが提供するインストール手順に従います。

### macOSの場合:
```sh
# Download and run the Docker Quickstart Terminal
curl -fsSL https://download.docker.com/mac/stable/Docker.dmg | sudo hdiutil attach -mountpoint /Volumes/docker -noverify -nobrowse /dev/rdiski
cd /Volumes/docker/Docker.app/Contents/Resources/etc/docker.conf.d/
sudo curl -L https://github.com/moby/buildkit/releases/download/v0.14.2/bazelisk_v1.37.2_Linux_x86_64.tar.gz | sudo tar -C . -xzvf -
```

## 基本的な使い方

### イメージのプル
```sh
# Pull the official Nginx image from Docker Hub
docker pull nginx
```

### コンテナの実行
```sh
# Run a container using the pulled Nginx image
docker run -d --name my-nginx nginx
```

### コンテナの一覧表示
```sh
# List all running containers
docker ps

# List all stopped containers
docker ps -a
```

## 主要機能

1. **イメージ**: Dockerイメージはコンテナの構成要素であり、アプリケーションの実行に必要なすべてを含んでいます。
2. **ボリューム**: コンテナ内のデータの永続ストレージ。
3. **ネットワーキング**: コンテナが相互に通信し、コンテナの外部のサービスとも通信できるようにします。
4. **Swarmモード**: 複数のDockerホストのクラスタリングとオーケストレーションを可能にします。

## まとめ

Dockerは、コードに隔離された環境を提供することで、アプリケーションの構築、配布、実行のプロセスを簡素化します。これにより、依存関係の管理が容易になり、開発とデプロイのさまざまな段階で一貫した環境を保証できます。