---
title: Team Win Recovery Project (TWRP)
description: TWRPは、Android向けのオープンソースのカスタムリカバリです。カスタムROMのフラッシュ、デバイス全体のバックアップ（NANDroid）、タッチスクリーンインターフェースによるシステム変更を可能にします。
created: 2026-06-17
tags:
  - android
  - recovery
  - custom-rom
  - backup
  - twrp
status: draft
---

# Team Win Recovery Project (TWRP)

TWRP (Team Win Recovery Project) は、Androidベースのデバイス向けの**オープンソースのカスタムリカバリイメージ**です。ストックのリカバリパーティションを置き換え、サードパーティ製ファームウェアのインストール、完全なシステムバックアップの作成、高度なシステム管理タスクを実行するための、豊富な機能を備えたタッチスクリーン駆動の環境を提供します。これらはすべて、Androidを起動せずに行えます。

## なぜTWRPなのか？

ストックのAndroidリカバリは、ファクトリーリセットとOTAアップデートのみに制限されています。TWRPはデバイスを次のように開放します：

- **カスタムROMのインストール** (LineageOS, Pixel Experienceなど)
- **完全なシステムバックアップとリストア** (NANDroid) — リスクのある変更の前には必須です。
- **ルート化** (MagiskまたはSuperSUのフラッシュ)
- **パーティション管理** (ワイプ、フォーマット、リサイズ)
- **暗号化の処理** (特定の条件下でのuserdataの復号)
- **ADBサイドローディングとMTP** ストレージがなくてもファイル転送やフラッシュが可能。

TWRPは、Android愛好家や開発者にとって事実上の標準となっています。直感的なインターフェースと活発なコミュニティサポートにより、ClockworkMod (CWM) などの以前のリカバリを置き換えました。

## 主な機能

- **Touch GUI** – フルタッチサポート、オンスクリーンキーボード、ファイルマネージャー、ターミナルエミュレータを備えています。
- **NANDroid Backup** – パーティション全体（Boot、System、Data、EFS/IMEI）を `/sdcard/TWRP/BACKUPS/` にクローンします。
- **ZIP Flashing** – カスタムファームウェアパッケージ（ROM、カーネル、Mod、GApps、Magisk）をインストールします。
- **Advanced Wipe** – 個別のパーティションのワイプ、「Format Data」による暗号化の解除。
- **File Manager** – デバイスのファイルシステムを参照および変更できます。
- **ADB Sideload** – USB経由でコンピュータからZIPファイルをフラッシュします。
- **MTP Support** – リカバリ内でデバイスストレージをリムーバブルドライブとしてアクセスできます。
- **Encryption Support** – PIN/パスワード/パターンでuserdataを復号できます（古い暗号化方式、最近のデバイスのFBEはサポートされていないことが多い）。
- **Theming** – `.twres` テーマによるカスタマイズ可能なUI。
- **Screenshot** – リカバリ中の画面をキャプチャ。

## 歴史

*Dees_Troy* によって2011年頃に作成され、TWRPは独自のタッチスクリーンインターフェースにより、すぐに最も人気のあるカスタムリカバリになりました。Holoテーマからマテリアルデザインインターフェース（バージョン3.0以降）へと進化しました。現在はコアチームによってメンテナンスされ、[twrp.me](https://twrp.me) で数百の公式サポートデバイスを提供しています。

## インストール

> **前提条件:**
> - ブートローダーのロック解除（ほとんどのデバイスで必要）
> - PCにADBおよびFastbootツールがインストールされていること
> - 使用するデバイスモデルに正確に対応するTWRPイメージ（twrp.meでコードネームを確認）

### 一般的なFastbootメソッド（ほとんどのデバイス）

1. **ブートローダーに再起動:**
   ```bash
   adb reboot bootloader
   ```
2. **リカバリイメージをフラッシュ:**
   ```bash
   fastboot flash recovery twrp-<version>.img
   ```
3. **すぐにリカバリに起動する**（システムが起動する前に、TWRPが上書きされる可能性があります）:
   ```bash
   fastboot reboot recovery
   # or use hardware key combination (Vol Up + Power, etc.)
   ```

### スロットベースのデバイス（A/Bパーティション – 例：Pixel、OnePlus）

システムが次回起動時にリカバリパーティションを自動的に置き換える可能性があるため、一時的なブート方法を使用します：

1. **一時的にTWRPイメージを起動:**
   ```bash
   fastboot boot twrp-<version>.img
   ```
2. **TWRP内で、** *Advanced → Install Recovery Ramdisk* に移動します。
   - これにより、TWRPが非アクティブスロットにフラッシュされ、上書きされるのを防ぎます。

### Samsungデバイス（Odin経由）

1. `.tar` 形式のTWRPファイルをダウンロード（通常は `twrp-<version>-<device>.tar` という名前）。
2. Odinを開き、ファイルを **AP** スロットに配置。
3. Odinオプションの **Auto-Reboot** のチェックを外す。
4. フラッシュし、すぐにキーコンボ（Vol Up + Home + Power）でリカバリに再起動して、ストックリカバリの復元を防ぐ。

### ルート化されたデバイスから（公式TWRPアプリを使用）

1. Playストアまたはtwrp.meから **Official TWRP App** をインストール。
2. ルート権限を付与。
3. デバイスを選択し、最新のイメージをフラッシュ。

### ターミナルから（ルート化済み）

```bash
su
dd if=/sdcard/twrp.img of=/dev/block/bootdevice/by-name/recovery
```

パスは実際のリカバリパーティションの場所に置き換えてください（デバイスによって異なります – `parted` や `ls /dev/block/platform/...` で確認）。

## 基本的な使用手順

### リカバリに入る

- ハードウェアキーの組み合わせを使用（メーカーによって異なりますが、通常は **Volume Down + Power**）。
- またはAndroidから（ルート化/ブートローダーアンロック済みの場合）：`adb reboot recovery`

### パーティションのワイプ

- **Factory Reset**（データ/キャッシュのワイプ） – 新しいROMのインストール前に必要。
  - *Wipe → Swipe to Factory Reset*
- **Format Data** – 暗号化を解除し、内部ストレージをワイプ。
  - *Wipe → Format Data → “yes”と入力*
- **Advanced Wipe** – ワイプする個別のパーティションを選択。

### ZIPのインストール（ROM、GApps、Magiskなど）

1. **Install** をタップ。
2. `.zip` ファイルに移動（通常は `/sdcard` または外部SDカード）。
3. ファイルをタップ。必要に応じて **Add more Zips** をタップして複数のファイルをキューに入れる。
4. **フラッシュを確認するためにスワイプ**。
5. *(オプション)* システムを再起動。

> サイドロードのコマンド例：
> ```bash
> adb sideload custom_rom.zip
> ```

### バックアップ（NANDroid）

1. **Backup** をタップ。
2. パーティションを選択：
   - **Boot**、**System**、**Data**（完全なシステムリストアに最小限）
   - **EFS**（IMEIを保存 – 一部のデバイスで重要）
3. スワイプしてバックアップを開始。
4. バックアップは `/sdcard/TWRP/BACKUPS/<device_serial>/` に保存されます。

### バックアップの復元

1. **Restore** をタップ。
2. リストからバックアップを選択。
3. 復元したいパーティションをチェック。
4. スワイプして確認。

### ファイルマネージャーとターミナル

- **File Manager**: *Advanced → File Manager* – ファイルの移動、削除、名前変更、コピー。
- **Terminal**: *Advanced → Terminal* – ルートとしてコマンドを実行。

## コマンド例（Fastboot & ADB）

```bash
# Reboot to bootloader from Android
adb reboot bootloader

# Flash recovery
fastboot flash recovery twrp-3.7.1_12-0-beryllium.img

# Boot into recovery without flashing
fastboot boot twrp-3.7.1_12-0-beryllium.img

# Sideload a file from PC
adb sideload LineageOS-21.0-20260617-UNOFFICIAL-beryllium.zip

# Push a file to the device in MTP mode
adb push magisk.zip /sdcard/
```

## 重要な注意事項

- **デバイス固有のイメージ** – 異なるモデル用のTWRPイメージをフラッシュすると、デバイスが**文鎮化（ハードブリック）**する可能性があります。必ずコードネームを確認してください（例：Pocophone F1の場合は`beryllium`）。
- **A/Bスロットの混乱** – シームレスアップデート対応デバイスでは、TWRPを両方のスロットにインストールする必要があります。一方のスロットにTWRPがないと、ストックリカバリに戻る可能性があります。
- **暗号化の問題** – 最近のAndroidは**ファイルベース暗号化（FBE）**を使用しています。TWRPはuserdataを復号できないことがよくあります。ROMを切り替える場合やTWRPが`/data`をマウントできない場合、ユーザーは頻繁に**Format Data**（内部ストレージをワイプ）する必要があります。
- **カスタムリカバリでのOTA** – ストックOTAアップデートは通常TWRPでは失敗します。次のいずれかを行う必要があります：
  - TWRP経由で手動でOTA ZIPをフラッシュする。
  - または、OTAを適用する前にストックリカバリに戻す。
- **Play Integrity / 銀行アプリ** – ブートローダーのロック解除（TWRPに必要）は多くのセキュリティチェックを破ります。Magiskによるルート化でこれを隠すことはできますが、複雑さが増し、常に成功するとは限りません。
- **変更前のバックアップ** – 新しいROMやリスクのあるModをフラッシュする前に、必ずNANDroidバックアップを作成してください。完全なバックアップは、ソフトブリックを数分で救出できます。

## トラブルシューティング

| 問題 | 解決方法 |
|--------|----------|
| TWRPが再起動後に残らない | `fastboot boot` を使用し、その後「Install Recovery Ramdisk」を実行（A/Bデバイス）。別のオプション：再フラッシュしてすぐにリカバリに起動。 |
| `/data` をマウントできない | 暗号化されている可能性があります。*Wipe → Format Data* に移動し、“yes” と入力してください。**これにより内部ストレージがすべて消去されます。** |
| フラッシュ後、デバイスが起動ロゴで止まる | Dalvik/ART CacheとCacheのワイプを試してください。それでも失敗する場合は、以前のバックアップを復元してください。 |
| ADB Sideloadが「sending」で停止する | 最新のADBドライバーを確認してください。別のUSBケーブル/ポートを試してみてください。 |
| TWRPが起動しない（ブラックスクリーン） | イメージが破損しているか間違っている可能性があります。公式サイトから再ダウンロードしてください。 |

## 参考資料

- **公式サイトとダウンロード:** [https://twrp.me](https://twrp.me)
- **ソースコード:** [https://github.com/TeamWin/Team-Win-Recovery-Project](https://github.com/TeamWin/Team-Win-Recovery-Project)
- **XDAフォーラム:** お使いのデバイスのTWRPビルドとサポートに関する具体的なフォーラムスレッドを検索してください。
- **ソースからTWRPをコンパイル:** [https://github.com/TeamWin/Team-Win-Recovery-Project/blob/android-12.1/README.md](https://github.com/TeamWin/Team-Win-Recovery-Project/blob/android-12.1/README.md)

TWRPは、Android開発者や愛好家にとって強力なツールです。賢く使用し、常にバックアップを手元に置いてください。