---
title: Magisk - Android向け Systemless Root and Module Manager
description: Magiskは、systemless rootアクセスとsystem modificationのためのmoduleサポートを提供する人気のAndroid rooting toolです。
created: 2026-06-19
tags:
  - android
  - root
  - systemless
  - magisk
  - tool
status: draft
---

# Magisk – Android向け Systemless Root and Module Manager

## Magiskとは？

Magiskは、**John Wu (topjohnwu)** によって作成されたオープンソースソフトウェアスイートで、**systemless rooting** とAndroidデバイスの高度なカスタマイズを可能にします。変更不可能な `/system` パーティションを変更する従来のroot化手法とは異なり、Magiskはデバイスのboot image（新しいデバイスでは `init_boot` パーティション）にパッチを適用し、起動時にオーバーレイファイルシステムを作成します。これにより、システムファイルを恒久的に変更することなく、rootアクセス、起動スクリプト、SELinuxポリシーパッチ、modulesをロードできます。

2016年に最初にリリースされて以来、Magiskはすぐに標準のAndroid root化ソリューションとなり、SuperSUなどの古いツールを置き換えました。現在も積極的にメンテナンスされており、基本的なroot化から高度なデバイス変更まで広く使用されています。

---

## なぜMagiskを使うのか？

| 利点 | 説明 |
|---------|-------------|
| **Systemless modifications** | `/system` は変更されないため、OTAアップデートが維持されます。 |
| **MagiskSU** | 純粋なオープンソースのroot権限管理（許可/確認/拒否）。 |
| **Module system** | 再パーティションなしで、オーディオmod、カメラlib、広告ブロック、フォントなどの調整をインストール。 |
| **Zygisk** | Zygoteを介してすべてのアプリプロセスにコードを注入 – MagiskHideを置き換えます。 |
| **DenyList** | 特定のアプリ（銀行、ストリーミング）からroot、modules、unlocked bootloaderを隠します。 |
| **MagiskBoot** | Android boot imageを展開、変更、再パッケージ化する強力なツール。 |
| **Active community** | 数千ものmodulesと広範なドキュメントが利用可能。 |

Magiskは、高度なバックアップツール、自動化（Tasker）、カスタムシステム調整、あるいはroot化デバイスをブロックするアプリの機能を再び有効にするためにrootアクセスが必要なユーザーにとって不可欠です。

---

## インストールガイド

### 前提条件

- **Unlocked bootloader**（デバイス固有、通常はOEM unlockが必要）。
- **動作するADBとFastboot**。
- **デバイスのfactory image**またはストックの `boot.img`（および必要に応じて `init_boot.img`）。
- **すべての重要なデータをバックアップ**。

### ステップ1 – Boot Imageの抽出

お使いのデバイスのfactory imageを入手し（例：Googleのfactory imagesページ）、boot imageを展開します。

```bash
# Pixelデバイスの例
unzip [device]_[build].zip
cd [device]_[build]
unzip image-[device]-[build].zip
# boot.imgがカレントディレクトリに作成されます
```

Android 13+（例：Pixel 6シリーズ）を搭載したデバイスの場合、rootパーティションは `boot.img` ではなく `init_boot.img` です。

### ステップ2 – Magiskアプリでイメージにパッチを適用

1. デバイスに最新のMagisk APKをインストールします。
2. Magiskアプリを開き、**インストール** → **ファイルを選択してパッチ** をタップします。
3. 抽出した `boot.img`（または `init_boot.img`）を選択します。
4. アプリがイメージにパッチを適用し、`magisk_patched-XXXXX.img` という名前の新しいファイル（通常は `Download/` 内）を保存します。

### ステップ3 – パッチ済みイメージをフラッシュ

パッチ済みイメージをコンピュータに転送し、デバイスをfastbootモードで起動します。

```bash
adb pull /storage/emulated/0/Download/magisk_patched-XXXXX.img .
adb reboot bootloader
# ほとんどのデバイスの場合:
fastboot flash boot magisk_patched-XXXXX.img
# Pixel 6+の場合（init_bootパーティション）:
fastboot flash init_boot magisk_patched-XXXXX.img
# 再起動:
fastboot reboot
```

### ステップ4 – インストールの確認

再起動後、Magiskアプリを開きます。**ホーム**画面にインストールされているMagiskバージョンと、Magiskステータスの横に「Installed」と表示されるはずです。

---

## 基本的な使い方

### Magiskアプリのインターフェース

- **Superuserタブ**（シールドアイコン）: root権限を要求したすべてのアプリの一覧。エントリをタップして権限ステータス（許可/確認/拒否）を変更できます。
- **Modulesタブ**（パズルピースアイコン）: インストール済みのmodulesを表示。**+** ボタンをタップして、デバイスに保存されている `.zip` ファイルから新しいmoduleをインストールします。トグルスイッチでmoduleの有効/無効を切り替えます（ほとんどの場合再起動が必要）。
- **設定タブ**（歯車アイコン）:
  - **Zygisk**: Zygiskの有効/無効を設定（再起動が必要）。
  - **DenyList**: Magiskを隠すアプリを設定（Zygiskと再起動が必要）。
  - **Update Channel**: アプリとMagiskのアップデートチャンネル（Stable、Beta、Canary）を選択。
  - **Automatic Response**: デフォルトのroot権限動作を設定。

### Module管理

Modulesは標準のZIPアーカイブとしてインストールされます。簡単なスクリプト、バイナリファイル、または完全なsystem overlayディレクトリを含めることができます。

```bash
# 典型的なmodule ZIP構造（/data/adb/modules/<module_id>/ 内）
module.prop          # メタデータ（id、name、version、author）
system/              # /systemにオーバーレイするファイル
post-fs-data.sh      # 起動初期に実行されるスクリプト
service.sh           # 起動後半に実行されるスクリプト
```

moduleを手動でインストールするには:

1. module `.zip` をデバイスにダウンロードします。
2. Magiskアプリを開き、Modulesタブ → **ストレージからインストール** をタップします。
3. ファイルを選択し、確認して、プロンプトが表示されたら **再起動** します。

### Magiskのアンインストール

Magiskアプリはrootを完全に削除する直接的な方法を提供します。

1. Magiskアプリを開きます。
2. ホーム画面の下部にある **Magiskをアンインストール** をタップします。
3. 確認 – アプリは元のパッチ未適用のboot imageを復元し、再起動します。

---

## 主な機能

### MagiskSU

完全にオープンソースの `su` の完全な代替品。許可/確認/拒否のオプションを持つパーミッションモデルを実装し、すべてのrootアクセスを記録します。MagiskSUは、rootを必要とするすべての既存アプリと互換性があります。

### Magisk Modules

システムパーティションに触れずにシステム変更を配布するための標準化された形式。ModulesはMagiskオーバーレイファイルシステムを使用して起動時にロードされます。XDAなどのフォーラムやMagiskリポジトリには数千のmodulesが存在します。

### Zygisk

Zygiskは、Zygoteプロセスへのコード注入を実装したMagiskの機能です。任意のアプリプロセス内で実行時の変更を可能にします。Zygiskは古いMagiskHide機能を置き換えます。

### DenyList

Zygiskが有効な場合、Magiskが自身の存在（root、modules、unlocked bootloader）を隠すアプリの **DenyList** を設定できます。これは、銀行、決済、ストリーミングアプリが使用する整合性チェックを回避する最新の方法です。

### MagiskBoot

MagiskBootはboot imageを操作するための低レベルツールです。完全なAndroid環境を必要とせずに、展開、変更、再パッケージ化が可能です。アプリを使わずにパッチ済みイメージを作成するために、コンピュータ上で直接使用されることがよくあります。

---

## コマンド例

### パッチ済みboot imageのフラッシュ（fastboot）

```bash
fastboot flash boot magisk_patched-27000.img
fastboot reboot
```

### 新しいデバイス用のinit_bootのフラッシュ

```bash
fastboot flash init_boot magisk_patched-27000.img
fastboot reboot
```

### MagiskBootを使用したboot imageの展開

```bash
magiskboot unpack boot.img
# これにより、kernel、kernel_dtb、ramdisk.cpio、headerなどが作成されます。
```

### MagiskBootを使用した変更済みboot imageの再パッケージ化

```bash
magiskboot repack boot.img
# 変更が加えられたnew-boot.imgを作成します。
```

### Boot image headerの確認

```bash
magiskboot info boot.img
```

### Magiskによるboot imageへのパッチ適用（コマンドライン）

コンピュータ上にMagisk実行可能ファイルがある場合は、直接パッチを適用できます:

```bash
magiskboot boot.img
# カレントディレクトリにpatched_boot.imgを作成します。
```

### アプリからMagiskを隠す（DenyList）

Magiskアプリを開き、設定 → **DenyListを設定** → 対象アプリを追加（例：Google Play Servicesの `com.google.android.gms`）。再起動後、Magiskはそのアプリから見えなくなります。

---

## ヒントと考慮事項

- **OTAアップデート** – Magiskはbootパーティションのみを変更するため、互換性があります。ただし、OTA後は新しいboot imageに **Magiskを再フラッシュ** する必要があります。
- **SafetyNet / Play Integrity** – Magisk自体は整合性バイパスを提供しませんが、Zygisk-AssistantやShamikoモジュールなどのツールは、Googleのアテステーションチェックからrootを隠すのに役立ちます。
- **Moduleの競合** – 一部のmoduleは互いに干渉する可能性があります。問題を特定するには、1つずつ無効にしてください。
- **バックアップ** – 元のストックboot imageのコピーを常に保管してください。問題が発生した場合、fastboot経由で復元できます。
- **Magisk Canary** – 最先端チャンネルには不安定な機能が含まれることがあります。テスト目的でのみ使用してください。

---

## 参考資料

- [Magisk GitHub リポジトリ](https://github.com/topjohnwu/Magisk)
- [公式 Magisk ドキュメント (開発者ガイド)](https://topjohnwu.github.io/Magisk/)
- [Magisk モジュールリポジトリ (非公式)](https://www.androidacy.com/modules-repository/)
- [XDA Developers – Magisk ディスカッション & サポート](https://forum.xda-developers.com/f/magisk.5903/)

---

*このドキュメントは開発者Wikiの一部です。コメントや改善点があればお寄せください。*