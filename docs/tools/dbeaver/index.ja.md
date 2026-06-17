---
title: DBeaver - ユニバーサルデータベース管理ツール
description: 開発者、データベース管理者、データアナリスト向けの無料でオープンソース、クロスプラットフォームのデータベース管理ツールおよびSQLクライアント。
created: 2026-06-17
tags:
  - database
  - sql
  - management
  - tools
  - open-source
status: draft
---

# DBeaver - ユニバーサルデータベース管理ツール

## 概要

DBeaverは、**無料でオープンソース、クロスプラットフォーム**のデータベース管理ツールおよびSQLクライアントです。JDBCまたはODBCドライバをサポートするあらゆるデータベースと対話するためのリッチなグラフィカルインターフェースを提供し、開発者、データベース管理者、データアナリストにとってユニバーサルなツールとなっています。

- **ライセンス**: Community Edition (CE) は **Apache 2.0** のもとで公開されています。商用のPro/Enterprise/Teamエディションも利用可能です。
- **プラットフォーム**: Windows、macOS、Linux（ポータブルアプリケーションとしても利用可能）。
- **アーキテクチャ**: Eclipse Rich Client Platform (RCP) 上にJavaを使用して構築されています。
- **歴史**: 2010年に、Apache DerbyやOracleに関与していたデータベース専門家のSerge Rielauによって開始されました。このプロジェクトは急速に広く採用され、DBeaver Corp.の設立につながりました。

DBeaverは以下のような用途に最適です:
- **アプリケーション開発** – SQLクエリの作成、デバッグ、最適化。
- **データベース管理** – スキーマ、ユーザー、セッション、インデックスの管理。
- **データ分析** – 分析クエリの実行と、さまざまな形式への結果のエクスポート。
- **データエンジニアリング** – 重いスクリプトを使わずに異なるデータベース間でデータを転送。
- **教育** – 直感的なGUIを通じてSQLとリレーショナルデータベースの概念を学ぶ。

## 主な機能

| 機能 | 説明 |
|---------|-------------|
| **幅広いデータベースサポート** | 100以上のデータベースに標準で接続可能。MySQL/MariaDB、PostgreSQL、Oracle、SQL Server、SQLite、DB2、Snowflake、Redshift、ClickHouseなど多数を含みます。 |
| **高度なSQLエディタ** | シンタックスハイライト、コード補完、複数の結果タブによるクエリ実行、実行計画の可視化（グラフィカル）、SQLフォーマット、パラメータ化クエリ。 |
| **データブラウザ/スプレッドシート** | 強力なインライン編集、高度なフィルタリング、ソート、グリッドインターフェースでのBLOB/CLOBデータの直接処理。 |
| **ER図** | リバースエンジニアリングによるエンティティ関係図（ER図）の自動生成（スキーマまたはテーブルを右クリック）。 |
| **スキーマ管理** | テーブル、ビュー、インデックス、プロシージャ、関数を参照、作成、編集するためのオブジェクトブラウザ。 |
| **データ転送** | データベース間およびファイル形式（CSV、JSON、XML、Excel、SQL、Markdown、HTML）での一括エクスポート/インポート。 |
| **管理ツール** | セッションマネージャー、タスクスケジューラ（Pro）、ユーザー/ロール管理、統合SSH/SSL/プロキシトンネリング。 |
| **拡張性** | プラグインアーキテクチャ。追加のドライバー、バージョン管理（Git）、図のカスタマイズ用のプラグインが利用可能。 |
| **クロスプラットフォーム** | Windows、macOS、Linuxで動作します。 |

## インストール

DBeaverは複数のチャネルから入手できます。環境に合った方法を選択してください。

### 公式インストーラー（全プラットフォーム）

お使いのOS用のインストーラーを[dbeaver.io](https://dbeaver.io)（Community Edition）または[dbeaver.com](https://dbeaver.com)（Enterprise）からダウンロードしてください。

### パッケージマネージャー

**macOS (Homebrew)**
```bash
brew install --cask dbeaver-community
```

**Linux (Snap)**
```bash
sudo snap install dbeaver-ce
```

**Linux (APT / YUM – Official Debian/RPM repos)**
```bash
# Debian/Ubuntu
wget -O - https://dbeaver.io/debs/dbeaver.gpg.key | sudo apt-key add -
echo "deb https://dbeaver.io/debs/dbeaver-ce /" | sudo tee /etc/apt/sources.list.d/dbeaver.list
sudo apt update && sudo apt install dbeaver-ce

# RHEL/CentOS/Fedora
sudo rpm --import https://dbeaver.io/rpms/dbeaver.gpg.key
sudo yum install dbeaver-ce
```

**Windows (winget / Chocolatey)**
```powershell
# winget (Windows 10 / 11)
winget install DBeaver.DBeaverCE

# Chocolatey
choco install dbeaver
```

**Windows ポータブル版**

公式ウェブサイトからポータブル実行ファイルが入手可能で、インストールせずにUSBドライブから実行するのに最適です。

## はじめに – 基本的な使い方

### 1. データベース接続の作成

1. DBeaverを起動します。
2. ツールバーの **新しいデータベース接続** ボタン（プラグアイコン）をクリックします。
3. データベースの種類（例：**PostgreSQL**）を選択します。
4. 接続詳細を入力します：
   - ホスト、ポート、データベース名、ユーザー名、パスワード。
5. **テスト接続** をクリックします。必要なJDBCドライバがまだキャッシュされていない場合、DBeaverが自動的にダウンロードを促します。
6. **完了** をクリックします。接続が **データベースナビゲーター** パネルに表示されます。

![接続ウィザードの例](https://dbeaver.com/docs/images/connection-wizard.png) <!-- Placeholder URL; actual docs provide screenshots -->

### 2. データの参照とクエリ

- **データベースナビゲーター** で接続を展開して、スキーマ、テーブル、ビューなどを表示します。
- テーブルを右クリックして **データを表示** を選択し、データグリッドを開きます。
- カスタムSQLを作成するには、`Ctrl + ]`（Windows/Linux）または `Cmd + ]`（macOS）を押して新しい **SQLエディタ** を開きます。

**Example SQL query:**
```sql
-- Select users with their latest order
SELECT u.id, u.name, o.order_date
FROM users u
JOIN (
    SELECT user_id, MAX(order_date) AS order_date
    FROM orders
    GROUP BY user_id
) o ON u.id = o.user_id
ORDER BY o.order_date DESC;
```

- `Ctrl + Enter`（Windows/Linux）または `Cmd + Enter`（macOS）でクエリを実行します。
- 結果はエディタの下の結果グリッドに表示されます。

### 3. データの編集とエクスポート

- 結果グリッドのセル値を直接クリックして編集します（テーブルに対する **編集** 権限が必要です）。
- 結果グリッドを右クリックし、**データをエクスポート** を選択します。
- 希望の形式（CSV、Excel、JSON、SQL INSERT、XML、Markdown など）を選択し、オプションを設定します。

## 高度な使い方

### エンティティ関係図（ER図）

DBeaverは、スキーマまたは特定のテーブルのER図を生成できます。

1. データベースナビゲーターでスキーマを右クリックします。
2. **図を表示**（または **ER図** タブを開く）を選択します。
3. 図にはテーブル、列、リレーションシップ、インデックスが表示されます。
4. 要素を再配置したり、図を画像としてエクスポートしたり、印刷したりできます。

### データ転送/移行

**データ転送** ウィザードを使用して、データベース間でデータをコピーしたり、データをファイルに抽出したりします。

1. テーブルまたはスキーマを右クリックします。
2. **データ > データ転送** を選択します。
3. ソース（例：テーブル）とターゲット（別のデータベース接続またはファイル）を選択します。
4. 列マッピングと変換ルールを設定します。
5. 転送を実行します。

### 実行計画（EXPLAIN）

SQLチューニングのためにクエリ実行計画を可視化します。

1. SQLエディタでクエリを記述します。
2. **実行計画の表示** ボタンをクリックします（または右クリック → **実行計画の表示**）。
3. DBeaverはコストの詳細とインデックス使用状況を含むグラフィカルな計画を表示します。

### 比較ツール（Pro/Enterprise）

**構造比較** および **データ比較** ツールを使用すると、2つのデータベースまたは環境間でスキーマやデータの差分を確認できます。

- 商用エディションで利用可能です。

## 設定とカスタマイズ

### 接続設定

- **ドライバープロパティ**: 接続エディタからJDBCドライバの属性（タイムアウト、SSLモード、チャンクサイズなど）を変更します。
- **SSHトンネル**: リモートデータベースへの安全なアクセスためにSSHトンネリングを設定します（接続設定の **SSH** タブ）。
- **SSL**: **SSL** タブからSSLを有効にし、証明書をインポートします。

### グローバル設定

- `Window → Preferences` (Windows/Linux) または `DBeaver → Preferences` (macOS)。
- **外観**: ライト/ダークテーマの切り替え、フォントサイズの調整。
- **エディタ**: SQLフォーマットスタイル、自動補完動作、実行オプションの設定。
- **接続**: デフォルトのトランザクション分離レベル、自動コミット、アイドルタイムアウトの設定。

### ドライバー管理

- **ドライバーマネージャー**: `Database → Driver Manager`。カスタムJDBCドライバーの表示、編集、追加。
- データベースに初めて接続するときに、不足しているドライバーをDBeaverのドライバーリポジトリから直接ダウンロードします。

## 自動化とスクリプト

### DBeaver CLI（Pro/Enterprise のみ）

DBeaver Pro/Enterpriseには、GUIなしでSQLスクリプトの実行、データのエクスポート、タスクの実行を行うためのコマンドラインツール（`dbeaver-cli`）が含まれています。

```bash
# Connect and run a script against a PostgreSQL instance
dbeaver-cli -driver postgresql -url jdbc:postgresql://localhost:5432/mydb \
            -user myuser -password mypass -script query.sql
```

### タスクスケジューラー（Pro/Enterprise のみ）

内蔵スケジューラー（cronライクなインターフェース）を使用して、定期的なエクスポート、データ転送、SQLスクリプトをスケジュールします。

## 統合

- **バージョン管理**: Git統合プラグイン（Communityで利用可能）。SQLスクリプトをコミットしたり、コミット済みバージョンと比較できます。
- **Docker**: CLIエディションを使用して、CI/CDパイプライン用にDBeaverをコンテナ内で直接実行することが可能です。
- **クラウドデータベース**: Snowflake、Amazon Redshift、Google BigQuery、Azure SQLなど用の事前設定済みドライバー。
- **SSH/SSL**: 安全な接続とプロキシ認証のための内蔵サポート。

## 互換性とパフォーマンス

| 項目 | 詳細 |
|--------|---------|
| **対応オペレーティングシステム** | Windows 10+, macOS 10.15+, Linux (x64, amd64, aarch64) |
| **Java要件** | JDK 11 以降（インストーラーにバンドル） |
| **データベースサポート** | 100以上のデータベース（リレーショナル、NoSQL系、クラウドを含む）をJDBC/ODBC経由でサポート |
| **パフォーマンスのヒント** | - 大規模なクエリにはインデックスを使用します。<br>- 設定でアイドル接続を閉じます。<br>- 一括操作には **「バッチ更新を使用」** を有効にします。<br>- 非常に大きなデータセットの場合は、チャンクでエクスポートするか、専用の移行ツールを使用します。 |

## トラブルシューティングとFAQ

### よくある問題

1. **“Driver not found” / “Cannot connect”**
   - DBeaverはドライバのダウンロードを促します。自動ダウンロードが失敗した場合は、`Database → Driver Manager` に移動し、データベースを選択して **ダウンロード/更新** をクリックします。
   - インターネットにアクセスできることを確認するか、JARファイルを手動でドライバライブラリに配置します。

2. **接続がハングする、またはタイムアウトする**
   - ネットワーク接続とファイアウォールルールを確認します。
   - SSH/SSL設定を確認します。設定ミスのあるトンネルは接続をブロックする可能性があります。
   - ドライバプロパティで接続タイムアウトを増やします。

3. **SQLエディタのパフォーマンスが遅い**
   - 自動メタデータ読み込みを無効にする：`Preferences → Database → Navigator → Disable lazy metadata reading`。
   - エディタツールバーで結果セットの制限を減らします。

4. **BLOB/CLOBを編集できない**
   - DBeaverは小さなオブジェクトのインライン編集をサポートしています。大きなオブジェクトの場合は、**値の表示/編集** ダイアログ（セルを右クリック → **値の表示**）を使用します。

### よくある質問（FAQ）

**Q: DBeaverは完全に無料ですか？**
**A: Community Editionは無料でオープンソース（Apache 2.0）です。Pro、Enterprise、Teamエディションは商用であり、NoSQLサポート、AIアシスタンス、CLIなどの機能が追加されています。**

**Q: 本番データベースにDBeaverを使用できますか？**
**A: はい、Community Editionは開発およびDBAタスクに対応した本番環境準備済みです。ミッションクリティカルな環境では、追加のサポートと監査機能を備えたEnterpriseエディションを検討してください。**

**Q: DBeaverはMongoDBやその他のNoSQLデータベースで動作しますか？**
**A: Community Editionは基本的なMongoDBサポートを備えています。完全なNoSQLおよびクラウドDBサポート（MongoDB、Cassandra、DynamoDBを含む）はEnterpriseエディションで利用可能です。**

**Q: DBeaverを完全にアンインストールするにはどうすればよいですか？**
**A: システムのパッケージマネージャー（例：`brew uninstall --cask dbeaver-community`、`snap remove dbeaver-ce`）またはOSのアンインストーラーを使用します。ユーザー設定はmacOS/Linuxの場合は`~/.dbeaver`、Windowsの場合は`%APPDATA%\DBeaver`に保存されます。これらのディレクトリを削除してすべての設定を消去します。**

## 結論

DBeaverは、開発者のワークフローにシームレスに適合する、強力で柔軟性が高く、ユーザーフレンドリーなデータベースツールです。そのオープンソースコア、広範なデータベースサポート、豊富な機能セットは、データを扱うすべての人にとって必需品です。

詳細については、公式ドキュメント（[dbeaver.com/docs](https://dbeaver.com/docs/)）を参照するか、[GitHub](https://github.com/dbeaver/dbeaver)でコミュニティに貢献してください。