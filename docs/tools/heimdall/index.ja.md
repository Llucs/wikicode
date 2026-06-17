---
title: Heimdall - Samsung ファームウェアフラッシュツール
description: Samsungモバイルデバイスにファームウェア（ROM）をフラッシュするためのクロスプラットフォームオープンソースツールスイート。
created: 2026-06-15
tags:
  - samsung
  - firmware
  - flashing
  - odin
  - android
  - open-source
status: draft
ecosystem: android
---

# Heimdall

## Heimdallとは？

Heimdallは、Samsung Androidデバイスにファームウェア（ストックROM、カスタムROM、ブートローダー、リカバリイメージ）をフラッシュするために設計された、クロスプラットフォームでオープンソースのツールスイートです。Samsung独自のOdinプロトコルをUSB経由で直接操作し、Windows専用のOdinツールに代わる、無料でLinux/macOS対応の代替手段を提供します。このプロジェクトはBenjamin DobellによってGitHub上でメンテナンスされており、2010年代初頭からAndroid moddingコミュニティで広く使用されています。

## Heimdallを使う理由

- **クロスプラットフォーム** – Windows、Linux、macOS上でエミュレーションなしでネイティブに動作します。
- **オープンソース** – 完全に監査可能でコミュニティ主導です。
- **Odinの制限を回避** – Odinが利用できない場合や、Windows以外のシステムでフラッシュする場合に便利です。
- **スクリプト可能** – コマンドラインインターフェースにより、自動化やカスタムツールチェーンへの統合が可能です。
- **パーティションレベルのフラッシュ** – 個々のパーティションイメージ（例: `BOOT`、`SYSTEM`、`RECOVERY`）をフラッシュして、特定の変更を行うことができます。

## インストール

### Windows

最新のインストーラーを[GitHubリリースページ](https://github.com/Benjamin-Dobell/Heimdall/releases)からダウンロードしてください。`.exe`を実行し、グラフィカルインストーラーに従ってください。

### Linux

多くのパッケージマネージャーから利用可能です：
```bash
# Debian/Ubuntu
sudo apt install heimdall-flash

# Fedora
sudo dnf install heimdall

# Arch Linux
sudo pacman -S heimdall
```
あるいは、`cmake`を使用してソースからビルドします。

### macOS

Homebrew経由でインストール：
```bash
brew install heimdall
```
または、リリースページからmacOSバイナリをダウンロードしてください。

## 使い方

### 前提条件

1. Samsungデバイスで**開発者オプション**と**USBデバッグ**を有効にしてください。
2. デバイスを**ダウンロードモード**で起動してください（通常: 電源オフ → 音量Down + Home + Powerを長押し、その後音量Upを押して確認）。
3. USB経由でデバイスをコンピュータに接続してください。

### 検出

デバイスが認識されていることを確認してください：
```bash
heimdall detect
```
成功した場合、出力にデバイスモデルと接続ステータスが表示されます。

### 基本的なフラッシュ

パーティションイメージをフラッシュ：
```bash
heimdall flash --RECOVERY twrp-3.6.0-i9300.img
```
複数のパーティションを一度にフラッシュ：
```bash
heimdall flash --BOOT boot.img --SYSTEM system.img --VENDOR vendor.img
```

### PITファイルの使用

完全なファームウェア復元やパーティションテーブルが不明な場合は、デバイスまたはファームウェアパッケージから抽出した`.pit`ファイルを指定してください：
```bash
heimdall flash --pit /path/to/device.pit --SLT --no-reboot
```
`--SLT`フラグはPITで定義されたすべてのパーティションをフラッシュし、`--no-reboot`は完了後もデバイスをダウンロードモードのままにします。

### 接続を閉じる

フラッシュ後、USBインターフェースを閉じてください：
```bash
heimdall close-pc-screen
```

## 主な機能

- **クロスプラットフォーム**: Windows、Linux、macOS（ネイティブバイナリ）。
- **オープンソース**: BSDライセンスのコードベースで、コミュニティによる活発なメンテナンス。
- **Odinプロトコル対応**: Samsungの低レベルフラッシュプロトコルの直接実装。
- **デバイス検出**: 信頼性の高いUSB列挙とハンドシェイク検証。
- **パーティションレベルのフラッシュ**: 個々のパーティション（boot、recovery、systemなど）をフラッシュ。
- **PITベースのフラッシュ**: パーティション情報テーブルを使用して完全なファームウェア復元。
- **内蔵USBドライバ**: Windowsインストーラーには必要なドライバが含まれています。Linux/macOSではlibusbを使用。
- **スクリプティング対応**: 自動化パイプラインやCI/CD環境に適したCLIフラグ。

## 例

### 接続されたデバイスを検出

```bash
$ heimdall detect
Device detected: GT-I9300 (galaxys3)
```

### カスタムリカバリ（TWRP）をフラッシュ

```bash
heimdall flash --RECOVERY twrp-3.6.0_9-i9300.img --no-reboot
```

### PITファイルを使用してフルストックファームウェアをフラッシュ

```bash
heimdall flash --pit AP_I9300_4.3.pit --SLT --no-reboot
```

### ブートパーティションのみをフラッシュ

```bash
heimdall flash --BOOT boot.img
```

## 注意事項

- Heimdallは、**Heimdall Application Dashboard**（linuxserver/Heimdall、Webベースのアプリランチャー）や **Heimdall** サイバーセキュリティフレームワークとは異なります。
- デバイスモデルに正しいファームウェアを常に使用して、文鎮化を避けてください。
- WindowsではUSBドライバがインストールされていることを確認してください – インストーラーに含まれています。Linuxでは、ルート権限なしでデバイスにアクセスできるようにudevルールを追加する必要がある場合があります。