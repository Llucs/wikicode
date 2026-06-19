---
title: "Termux: Android向けターミナルエミュレータおよびLinux環境"
description: "Termuxの包括的なガイド。TermuxはAndroid端末向けの強力なオープンソースのターミナルエミュレータおよびLinux環境であり、インストール、パッケージ管理、高度な使用法、開発者ワークフローをカバーしています。"
created: 2026-06-19
tags:
  - android
  - terminal
  - linux
  - development
  - tools
status: draft
---

# Termux: Android向けターミナルエミュレータおよびLinux環境

## Termuxとは？

Termuxは、Android用の**オープンソースのターミナルエミュレータ兼Linux環境**です。完全にユーザースペースで動作し、**ルートアクセスは不要**で、Debian/Ubuntu由来の豊富なパッケージリポジトリを提供します。Termuxを使えば、Android端末で本格的なLinuxコマンドラインエクスペリエンスを実行できます。コンパイラ、インタープリタ、テキストエディタ、ネットワーキングツールなどをインストールできます。AndroidカーネルのLinuxシステムコールを活用し、ネイティブに近い環境を作り出します。

### Termuxを使う理由

- **ポータブル開発環境** – Pythonスクリプトの作成・実行、Cプログラムのコンパイル、Gitリポジトリの管理、または電話上で直接REPLを使用できます。
- **外出先でのサーバー管理** – SSHでリモートサーバーに接続、ネットワーク診断（ping、traceroute、nmap）、rsyncでのファイル同期。
- **学習と教育** – フルPCを必要とせずにLinuxコマンド、シェルスクリプティング、ネットワーク概念を練習。
- **自動化と連携** – Android自動化アプリ（Tasker）と組み合わせるか、Termux:APIを使用して電話のハードウェア（カメラ、センサー、クリップボード）とやり取り。
- **完全なLinuxディストリビューション** – proot-distroを使用してTermux環境内にUbuntu、Debian、Arch、Fedoraをインストールし、ほぼすべてのLinuxタスクを実行可能。

---

## 主な機能

| 機能 | 説明 |
|---------|-------------|
| **ターミナルエミュレータ** | タッチフレンドリーなジェスチャーコントロール、数字行を左にスワイプしてアクセスできる追加ファンクションキー（Tab、Ctrl、Alt、Esc）を備えたフル機能。 |
| **パッケージマネージャー** | Termuxリポジトリからの何千ものパッケージを提供する`pkg`（とその下の`apt`）。 |
| **マルチセッション管理** | ドロワーをスライドして、個別にログインした独立したターミナルセッションを管理。 |
| **SSHクライアントとサーバー** | `ssh`でリモートサーバーに接続、またはサーバー（`sshd`）を起動してコンピュータからデバイスにアクセス。 |
| **Proot Distroサポート** | `proot-distro`を使用して完全なLinuxディストリビューション（Ubuntu、Debian、Arch、Fedora）を実行。 |
| **API連携** | コンパニオンアプリ*Termux:API*がスクリプトにAndroidセンサー、クリップボード、TTS、カメラ、通知などへのアクセスを提供。 |
| **ストレージアクセス** | `termux-setup-storage`を使用して共有Androidストレージ（内部/SD）をマウント。 |

---

## インストール

### 1. Termuxを入手する

> **重要**: **Google Playストア版は非推奨**です（API 28で停止）。最新のパッケージと最新のAndroid（10+）との完全な互換性を得るには、常に**F-Droid**からインストールしてください。

- **F-Droidクライアント**: F-Droidアプリで「Termux」を検索するか、[F-Droid](https://f-droid.org/packages/com.termux/) からAPKを直接ダウンロード。
- **直接APK**: [F-Droid APK](https://f-droid.org/repo/com.termux_*.apk)（常に最新版）。

### 2. コンパニオンアプリ（オプションだが推奨）

| アプリ | 目的 |
|-----|---------|
| [Termux:API](https://f-droid.org/packages/com.termux.api/) | スクリプトからAndroidハードウェア（センサー、カメラ、クリップボードなど）にアクセス。 |
| [Termux:Float](https://f-droid.org/packages/com.termux.float/) | フローティングウィンドウ（オーバーレイ）でTermuxを実行。 |
| [Termux:Styling](https://f-droid.org/packages/com.termux.styling/) | ターミナル用のカラースキームとpowerline対応フォント。 |
| [Termux:Tasker](https://f-droid.org/packages/com.termux.tasker/) | Taskerおよび互換性のある自動化アプリからTermuxの実行ファイルを呼び出す。 |
| [Termux:Widget](https://f-droid.org/packages/com.termux.widget/) | ホーム画面から小さなスクリプトレットを起動。 |

### 3. 初期設定

Termuxを初めて起動した後:

```bash
# Update the package repository and upgrade all packages
pkg update && pkg upgrade

# Grant storage access (needed to see your shared folders)
termux-setup-storage
```

これで、完全に更新されたTermux環境が整いました。共有Androidストレージは `~/storage/shared` にマウントされています。

---

## パッケージ管理

Termuxは**`pkg`**コマンドを**`apt`**のラッパーとして使用します。すべてのコマンドはDebian/Ubuntuユーザーにはおなじみのものです。

### よく使うパッケージ操作

```bash
# Search for a package
pkg search python

# Install packages
pkg install python git vim openssh curl wget

# Remove a package
pkg remove python2

# List installed packages
pkg list-installed

# Upgrade all packages
pkg upgrade
```

### 利用可能なパッケージ（抜粋）

| カテゴリ | パッケージ |
|----------|----------|
| **言語** | python, python3, nodejs, ruby, php, lua, golang, rust |
| **コンパイラ/ツール** | clang, make, gdb, cmake, gcc（proot distro経由） |
| **エディタ** | vim, emacs, nano, neovim |
| **ネットワーキング** | openssh, nmap, traceroute, netcat, rclone |
| **データベース** | mariadb, sqlite, postgresql（prootが必要） |
| **ユーティリティ** | git, curl, wget, rsync, htop, jq, ripgrep, fd |

> **注記**: Termuxはユーザースペース環境であるため、一部のシステムレベルパッケージ（例：`systemd`、`glibc`依存）は`proot-distro`を介した完全なLinuxディストリビューションが必要です。

---

## 高度な使用方法

### 1. SSH: クライアントとサーバー

**クライアント** – デスクトップと同じようにリモートマシンに接続:

```bash
pkg install openssh
ssh user@hostname
```

**サーバー** – Android端末をSSHアクセス可能にする（デフォルトポート8022）:

```bash
sshd
# or start it in the foreground with -d
sshd -d
```

> `sshd`を初めて実行すると、Termuxはホストキーを生成し、termuxユーザーのパスワードを設定できます（デフォルトユーザーは`u0_aXYZ`）。変更するには`passwd`を使用します。

### 2. `proot-distro`を使用した完全なLinuxディストリビューションの実行

Prootを使用すると、Termux内でルートなしで標準的なLinuxディストリビューションを実行できます。`proot-distro`パッケージはこれを簡単にします。

```bash
pkg install proot-distro

# List available distributions
proot-distro list

# Install Ubuntu (example)
proot-distro install ubuntu

# Login to the installed distribution
proot-distro login ubuntu

# Within the Ubuntu environment, you can use apt normally.
```

これで完全なUbuntu環境が手に入ります（`proot`を介した`systemd`ライクなサービス管理も含まれますが、すべての機能が完全に動作するわけではありません）。その中で`gcc`、`postgresql`、あるいは`firefox`（GUIにはXサーバーが必要）のようなパッケージをインストールできます。

### 3. Termux:APIコンパニオンの使用

`Termux:API`をインストールすると、コマンドラインからAndroidの機能を制御できます。

```bash
pkg install termux-api

# Get battery status
termux-battery-status

# Take a photo
termux-camera-photo output.jpg

# Get clipboard content
termux-clipboard-get

# Show a notification
termux-notification --title "Hello" --content "World"

# Check sensors
termux-sensor -s "Accelerometer" -n 5
```

### 4. Taskerを使った自動化

Termux:Taskerを使用すると、TermuxスクリプトをTaskerアクションとして実行できます。

1. F-Droidから**Termux:Tasker**をインストールします。
2. Taskerで、`System -> Send Intent`タイプのアクションを追加します。
3. アクション: `com.termux.tasker.RUN_COMMAND`
4. 追加のキー/値ペア: `command` = スクリプトまたはコマンド（例：`termux-battery-status`）。

スクリプトを`~/.termux/tasker/`に配置し、名前で呼び出すこともできます。

### 5. セッション管理とUIのコツ

- **追加キー**: 数字行（キーボード上部）を左にスワイプすると、Tab、Ctrl、Alt、Esc、ファンクションキートグル、上矢印（上にスクロール）の行が表示されます。これらは`~/.termux/termux.properties`でカスタマイズできます。
- **マルチセッション**: 画面左側のドロワーアイコン（三本線）をタップして、新しいターミナルセッションを一覧表示、切り替え、作成します。
- **テキスト選択**: ターミナル領域を長押しして選択モードに入ります。コピー/ペーストはオーバーフローメニューで行います。

---

## 使用例

- **モバイルコーディング** – vimとgccでPythonスクリプト、Node.jsアプリ、Cプログラムを作成・テスト。gitでバージョン管理。
- **サーバー運用** – 本番サーバーにSSHで接続、`tcpdump`や`nmap`スキャンの実行、ログの監視、`rsync`でのファイル転送。
- **データ分析** – pandas、numpy、scipy、Jupyter（`pkg install jupyter`経由）を備えたPythonをインストールして、外出先でデータ処理。
- **Linux学習** – 別のPCなしでファイルシステム、シェルスクリプティング、ネットワーキングを試す。
- **ポケット計算機** – Pythonを対話型計算機として使用：`python -c 'print(2**100)'` またはREPLを起動。

---

## トラブルシューティングとヒント

### パッケージインストールが「404 Not Found」で失敗する
リポジトリが古い可能性があります。まず`pkg update && pkg upgrade`を実行してください。問題が解決しない場合は、F-Droid版を使用していることを確認してください（Google Play版ではありません）。

### ストレージアクセスが拒否される
`termux-setup-storage` を実行し、プロンプトが表示されたら権限を許可します。Android 11以降で失敗する場合は、システム設定でTermuxに「ファイルとメディア」の権限が有効になっていることを確認してください。

### libc/glibc依存関係の問題
一部のパッケージはglibcを期待しますが、Termuxはbionic（Androidのlibc）を使用します。そのようなパッケージにはproot-distro（Ubuntu、Debian）を使用してください。

### Android 10以降でフルスクリーンキーボードを無効にする方法
`~/.termux/termux.properties` に次の行を追加します:
```
fullscreen=false
```
その後、`termux-reload-settings`で再読み込みします。

### ターミナルとのクリップボード連携
`termux-api` の `termux-clipboard-get` と `termux-clipboard-set` を使用して、システムクリップボードとやり取りします。

---

## コミュニティとリソース

- **公式サイト**: [termux.com](https://termux.com)（GitHubにリダイレクト）
- **GitHubリポジトリ**: [termux/termux-app](https://github.com/termux/termux-app)（メインアプリ）
- **パッケージリポジトリ**: [termux/termux-packages](https://github.com/termux/termux-packages)
- **Wiki**: [Termux Wiki](https://wiki.termux.com)
- **F-Droid**: [F-Droid Termux](https://f-droid.org/packages/com.termux/)
- **Reddit**: [r/termux](https://reddit.com/r/termux)

---

TermuxはあなたのAndroid端末を強力でポータブルなLinuxワークステーションに変えます。その豊富なパッケージリポジトリ、SSH機能、標準的なLinuxワークフローとの互換性により、開発者、システム管理者、コマンドラインをポケットに入れておきたいすべての人にとって不可欠なツールです。