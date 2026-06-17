---
title: SpeedCool Magisk Module
description: Android 向けの Magisk モジュールで、システム設定を最適化してパフォーマンスを向上させ、RAM 使用量を削減し、熱管理を改善します。
created: 2026-06-15
tags:
  - android
  - magisk-module
  - performance-tuning
  - thermal-management
  - root
status: draft
ecosystem: android
---

# SpeedCool Magisk モジュール

**SpeedCool** は [Llucs](https://github.com/Llucs/SpeedCool-Magisk-Module) によって作成されたオープンソースの軽量 Magisk モジュールです。起動時にカーネルおよびシステムレベルの包括的な調整を自動的に適用し、root化された Android デバイスのパフォーマンスを向上させ、RAM 使用量を削減し、熱管理を改善します。

標準的なブロートウェアクリーナーとは異なり、SpeedCool は基礎となるシステム設定を変更して、ラグや過熱の根本原因を排除します。

---

## 機能

SpeedCool はいくつかの主要なシステム領域を対象としています。

- **CPU ガバナーと周波数スケーリング:** 要求の厳しいアプリケーション（ゲーム、エミュレーターなど）のウェイクアップレイテンシを削減します。
- **Low Memory Killer (LMK):** バックグラウンドキャッシュプロセスから積極的にメモリを回収しながら、現在アクティブなアプリをメモリに保持することを優先します。
- **サーマルエンジン:** 熱スロットルポイントを変更し、発熱と持続的なパフォーマンスのバランスを取ります。
- **I/O スケジューラ:** ストレージスケジューラを低レイテンシバリアントに切り替え、アプリの読み込みをより機敏にします。
- **ネットワークスタック:** モバイルネットワークでのスループット向上のために TCP 輻輳制御を最適化します。
- **GPU レンダリング:** 強制 GPU レンダリングを有効にし、GPU ガバナーを最適化します。

---

## 使用する理由

- **よりスムーズなゲーム体験:** CPU/GPU ガバナーの調整とサーマルスロットル制御の改善により、フレームレートがより安定します。
- **より高速なマルチタスク:** LMK 値の最適化により、アプリの再読み込み頻度が低下します。
- **より低温での動作:** スマートなサーマルプロファイルにより、高負荷使用時に SoC が危険な温度に達するのを防ぎます。
- **オールインワン最適化:** 複数の競合するパフォーマンスモジュールを置き換えます。
- **軽量:** モジュールのサイズは通常 1 MB 未満で、オーバーヘッドは無視できます。

---

## インストール

### 前提条件

- ブートローダーのロックが解除され、root アクセス権がある Android デバイス。
- **Magisk** (v20.0+) がインストールされていること。
- カスタムリカバリ（TWRP）がフォールバックとして推奨されます。

### 手順

1. [GitHub リリースページ](https://github.com/Llucs/SpeedCool-Magisk-Module/releases) から最新の `SpeedCool-Magisk-Module.zip` を **ダウンロード** します。
2. **Magisk Manager** アプリを開きます。
3. **モジュール** タブに移動します。
4. **ストレージからインストール** をタップします。
5. ダウンロードした `.zip` ファイルを選択します。
6. スワイプしてインストールを確定します。
7. プロンプトが表示されたらデバイスを **再起動** します。

> **ヒント:** ブートループが発生した場合は、セーフモードで起動し（起動時に音量上ボタンを押し続ける）、モジュールを無効にするか、リカバリから `/data/adb/modules/SpeedCool/` を削除して手動で削除してください。

---

## 使用方法と確認

SpeedCool は完全にバックグラウンドで動作するように設計されています。ユーザーインターフェースは必要ありません。ターミナルコマンドを使用して動作を確認できます。

### アクティブステータスの確認

モジュールディレクトリをリスト表示して、インストールされていることを確認します。

```bash
su -c "ls -la /data/adb/modules/SpeedCool/"
```

正常にマウントされている場合、ディレクトリにはモジュールファイル (`system.prop`, `service.sh`, `module.prop`) が含まれています。

### 適用されたシステムプロパティの確認

```bash
su -c "getprop | grep speed"
```

モジュールによって注入されたプロパティ（例: `ro.sys.speedcool.version`）を探します。

---

## コマンド例を含む主な機能

### 1. CPU ガバナーの調整
このモジュールは、すべての CPU コアに低レイテンシガバナー（通常は `performance`、`interactive`、または調整された `schedutil`）を強制します。

```bash
# 現在のガバナーを確認
su -c "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
```

*期待される出力:* `performance` または `schedutil`

### 2. RAM の最適化 (LMK)
Low Memory Killer のしきい値が変更され、フォアグラウンドアプリの応答性を維持しながら、重要性の低いバックグラウンドプロセスを積極的に強制終了します。

```bash
# LMK 値を確認 (adj, minfree)
su -c "cat /sys/module/lowmemorykiller/parameters/minfree"
su -c "cat /sys/module/lowmemorykiller/parameters/adj"
```

### 3. I/O スケジューラの最適化
ブロックレイヤスケジューラが、インタラクティブパフォーマンス向けに最適化されたバリアント（例: `bfq` または `fiops`）に切り替わります。

```bash
# メインストレージブロックデバイスのアクティブなスケジューラを確認
su -c "cat /sys/block/mmcblk0/queue/scheduler"
```

*期待される出力:* `[bfq]` または `[fiops]`

### 4. ネットワーク調整
TCP 輻輳制御が、モバイルネットワークに適したアルゴリズム（例: `westwood` または `bbr`）に切り替わります。

```bash
# アクティブな TCP 輻輳制御アルゴリズムを確認
su -c "cat /proc/sys/net/ipv4/tcp_congestion_control"
```

*期待される出力:* `westwood`

### 5. モジュールログの表示
モジュールスクリプトでデバッグが有効になっている場合、システムログをフィルタリングできます。

```bash
su -c "logcat -d | grep SpeedCool"
```

### 6. モジュールプロファイルの読み取り (設定可能な場合)
一部のバージョンでは、`service.sh` を編集してプロファイルを選択できます。ファイル内の利用可能なコメントを確認します。

```bash
su -c "head -50 /data/adb/modules/SpeedCool/service.sh"
```

---

## トラブルシューティング

| 症状 | 考えられる原因 | 解決策 |
|---|---|---|
| **ブートループ** | 競合するモジュールまたは互換性のないデバイス。 | 起動時に音量上ボタンを押し続けてモジュールを無効にするか、TWRP ファイルマネージャーで `/data/adb/modules/SpeedCool` ディレクトリを削除します。 |
| **パフォーマンスの変化なし** | 競合するモジュール (LKT、FDE.AI、NFS)。 | SpeedCool を使用する前に、他のすべてのパフォーマンスモジュールを削除します。 |
| **デバイスが高温のまま** | サーマルリミットが強すぎる。 | モジュール内のサーマルエンジン設定を確認するか、別のプロファイルを試してください。 |
| **アプリがクラッシュする** | LMK 値が過度に積極的。 | `service.sh` の `minfree` 値を手動で調整します。 |

---

## 削除

1. **Magisk Manager** を開きます。
2. **モジュール** タブに移動します。
3. SpeedCool の横にある **削除** (ゴミ箱) アイコンをタップします。
4. **再起動** をタップします。

**コマンドラインによる削除:**

```bash
su -c "rm -rf /data/adb/modules/SpeedCool/"
reboot
```

---

## 参考情報

- **GitHub リポジトリ:** [Llucs/SpeedCool-Magisk-Module](https://github.com/Llucs/SpeedCool-Magisk-Module)
- **Magisk 公式ドキュメント:** [topjohnwu.github.io/Magisk/](https://topjohnwu.github.io/Magisk/)
- **XDA Developers:** コミュニティサポートのディスカッションについては、*SpeedCool* または *Llucs* を検索してください。

> **免責事項:** システムパラメータの変更には固有のリスクが伴います。パフォーマンスモジュールをインストールする前に、必ず完全な Nandroid バックアップを作成してください。開発者は、デバイスに生じたいかなる損傷についても責任を負いません。