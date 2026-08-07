--- 
title: "Tauri: RustとWebフロントエンドによる軽量クロスプラットフォームアプリ構築"
description: "Web技術を利用してセキュアで最小サイズのデスクトップ・モバイルアプリケーションを構築するためのRustベースのフレームワーク、Tauriの包括的な開発者ガイド。"
created: 2026-08-07
tags:
  - tauri
  - rust
  - desktop-apps
  - mobile-development
  - webview
  - electron-alternative
status: draft
---

# Tauri: RustとWebフロントエンドによる軽量クロスプラットフォームアプリ構築

## 概要

**Tauri** は、Webフロントエンド技術（HTML、CSS、JavaScript/TypeScript）と **Rustバックエンド** を用いてデスクトップおよびモバイルアプリケーションを構築するためのオープンソースツールキットです。Electron が完全な Chromium エンジン（150 MB以上）を同梱するのとは異なり、Tauri は **OS標準のWebView**（WindowsのWebView2、macOSのWebKit、LinuxのWebKitGTK）を活用します。その結果、バイナリサイズは劇的に小さく（多くの場合10MB未満）、メモリ消費も大幅に削減されます。

Tauri 2.0（2024年10月リリース）は、公式に **iOSおよびAndroidサポート** を追加し、真のクロスプラットフォームフレームワークとなりました。コアはRustで構築されており、CLIはnpm、Cargo、またはスタンドアロンバイナリ経由で利用できます。

## Tauriを選ぶ理由

Tauriを選ぶ主な動機は、Electronの肥大化とセキュリティ面の広さにあります。Tauriは、次の3つの主要な問題点への応答として設計されました。

| 項目 | Electron | Tauri |
|---------|----------|-------|
| **バンドルサイズ** | インストーラあたり150–250 MB | インストーラあたり3–15 MB |
| **メモリ使用量** | ベースライン300–500 MB | ベースライン50–150 MB |
| **セキュリティ** | Chromium全体が露出、リモートコード実行が可能 | ケイパビリティベースの権限、デフォルトでリモートコードなし |
| **バックエンド** | Node.js（またはバインディング経由のPython） | Rust（ネイティブ速度、メモリ安全） |
| **フロントエンド** | 任意のWebフレームワーク | 任意のWebフレームワーク |

Tauriは以下の場合に最適な選択肢です：
- ネイティブに感じられ、即座に起動するアプリが必要な場合。
- セキュリティを重視し、フロントエンドがアクセスできる範囲を厳密に制御したい場合。
- バックエンドロジックをRustで書く（または学ぶ）ことに抵抗がない場合。
- Windows、macOS、Linux、iOS、Androidをターゲットにした単一のコードベースが必要な場合。

## アーキテクチャ

Tauriのアーキテクチャは、WebフロントエンドとRustコアのハイブリッドであり、セキュアなIPCブリッジを介して通信します。

```
┌─────────────────────────────────────────────────────┐
│                  Frontend (WebView)                 │
│  React / Vue / Svelte / Solid / Vanilla JS / etc.  │
│             HTML · CSS · JavaScript                 │
└─────────────────────────┬───────────────────────────┘
                          │  IPC (postMessage-based)
                          ▼
┌─────────────────────────────────────────────────────┐
│                Tauri Core (Rust)                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │  Commands   │  │   Events    │  │  Plugins    │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
│  ┌───────────────────────────────────────────────┐  │
│  │  System APIs (fs, shell, http, dialog, etc.)  │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

**アーキテクチャの主要なポイント：**

- 最終的なアプリには **Node.jsランタイムは同梱されません**。フロントエンドはバイナリにコンパイルされた静的アセットで構成されます。
- **IPC** はJSとRustの間でメッセージパッシングプロトコルを使用します。フロントエンドは明示的な権限なしに任意のシステムAPIを直接呼び出すことは *できません*。
- **ケイパビリティ** は、ビルド時にフロントエンドがアクセスできる内容（ファイルシステムのパス、HTTPホスト、プラグインスコープ）を定義します。

## 歴史とリリース年表

- **2018年** — Daniel Thompson-Yvetotが初期コンセプト実証を作成。
- **2022年6月19日** — **Tauri 1.0** 安定版リリース。
- **2023年** — Tauri FoundationがLinux Foundationに参加。
- **2024年10月** — **Tauri 2.0** がiOS/Androidサポート、新しいプラグインシステム、統合アーキテクチャを追加。

## インストール

### 前提条件

| プラットフォーム | 要件 |
|----------|--------------|
| **Windows** | WebView2ランタイム（Windows 11にはプレインストール済み）、Rust、MSVCビルドツール |
| **macOS** | Xcode Command Line Tools、Rust |
| **Linux** | `libwebkit2gtk-4.1-dev`、`build-essential`、`libssl-dev`、`libayatana-appindicator3-dev`、`librsvg2-dev`、Rust |

Linux（Debian/Ubuntu）で一度にインストール：

```bash
sudo apt update
sudo apt install libwebkit2gtk-4.1-dev build-essential curl wget file libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev
```

[rustup](https://rustup.rs/) を使ってRustをインストール：

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### 新規プロジェクトの雛形作成

公式のスキャフォールディングツールを使用します（npm、pnpm、yarn、bun、cargoに対応）：

```bash
npm create tauri-app@latest
```

次の項目を求められます：
1. プロジェクト名
2. フロントエンドフレームワーク（React、Vue、Svelte、Solid、Angular、Vanilla）
3. UI言語（TypeScript／JavaScript）
4. パッケージマネージャー

次に：

```bash
cd my-app
npm install
npm run tauri dev
```

これにより、フロントエンドをホットリロードする開発サーバーが起動し、Rustバイナリがコンパイルされます。初回ビルドは数分かかりますが、以降のビルドは高速です。

### CLIの代替手段

```bash
# Global npm CLI
npm install -g @tauri-apps/cli

# Or via Cargo
cargo install tauri-cli
cargo tauri dev
```

## プロジェクト構成

Tauriプロジェクトの雛形は次のようになります：

```
my-app/
├── src/                      # Frontend source (React, Vue, etc.)
│   ├── main.ts
│   └── App.tsx
├── public/                   # Static assets
├── src-tauri/                # Rust backend
│   ├── Cargo.toml
│   ├── tauri.conf.json       # Main configuration
│   ├── build.rs
│   ├── capabilities/
│   │   └── default.json      # Permissions for your app
│   ├── icons/
│   ├── src/
│   │   ├── main.rs           # Entry point (Windows/Linux/macOS)
│   │   └── lib.rs            # Shared code + mobile entry point
└── package.json
```

### `tauri.conf.json`

メイン設定ファイルは、アプリ識別子からビルド設定までを制御します：

```json
{
  "$schema": "https://schema.tauri.app/config/2",
  "productName": "my-app",
  "version": "0.1.0",
  "identifier": "com.example.myapp",
  "build": {
    "beforeDevCommand": "npm run dev",
    "devUrl": "http://localhost:1420",
    "beforeBuildCommand": "npm run build",
    "frontendDist": "../dist"
  },
  "app": {
    "windows": [
      {
        "title": "My App",
        "width": 1200,
        "height": 800,
        "resizable": true
      }
    ],
    "security": {
      "csp": "default-src 'self'; style-src 'self' 'unsafe-inline'"
    }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png"
    ]
  }
}
```

## コアコンセプト

### 1. コマンド（Rust ⇄ JS IPC）

コマンドはフロントエンドに公開されるRust関数です。`#[tauri::command]` で定義し、ビルダーに登録します。

**Rust側**（`src-tauri/src/lib.rs`）：

```rust
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

#[tauri::command]
async fn read_config(path: String) -> Result<String, String> {
    std::fs::read_to_string(&path).map_err(|e| e.to_string())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet, read_config])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**JavaScript側**（`@tauri-apps/api` パッケージを使用）：

```javascript
import { invoke } from "@tauri-apps/api/core";

// Simple invocation
const msg = await invoke("greet", { name: "World" });
console.log(msg); // "Hello, World!"

// With error handling
try {
  const data = await invoke("read_config", { path: "/etc/example.conf" });
} catch (err) {
  console.error("Failed to read:", err);
}
```

**パラメータ命名の注意：** TauriはRustのスネークケース引数をJSのキャメルケースに変換します。Rustのパラメータ名 `user_name` は `{ userName: "..." }` として呼び出されます。正確な名前を保持するには、コマンドに `rename_all = "snake_case"` を使用します：

```rust
#[tauri::command(rename_all = "snake_case")]
fn my_command(user_name: &str) {}
```

### 2. Rustバックエンドの状態管理

`manage()` を使用してコマンド間で状態を共有します：

```rust
struct AppState {
    db_connection: Mutex<sqlite::Connection>,
}

#[tauri::command]
fn get_user(state: tauri::State<AppState>, id: u32) -> String {
    let conn = state.db_connection.lock().unwrap();
    // ... query
}

pub fn run() {
    tauri::Builder::default()
        .manage(AppState {
            db_connection: Mutex::new(/* initialize */),
        })
        .invoke_handler(tauri::generate_handler![get_user])
        .run(tauri::generate_context!())
        .expect("error");
}
```

### 3. ケイパビリティと権限

Tauri 2.0以降、すべてのIPCアクセスは **ケイパビリティシステム** によって制御されます。ケイパビリティファイルは、どのウィンドウ／WebViewがどのコマンド、プラグイン、スコープにアクセスできるかを定義します。

`src-tauri/capabilities/default.json`：

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Default capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "core:window:allow-set-title",
    "dialog:allow-open",
    "fs:allow-read-text-file",
    {
      "identifier": "fs:scope",
      "allow": [{ "path": "$HOME/**" }, { "path": "$APPDATA/**" }]
    }
  ]
}
```

**重要：** 権限を許可するケイパビリティがない場合、そのコマンドを呼び出すと実行時に権限拒否エラーで失敗します。これは攻撃対象領域を最小化するための意図的な設計です。

### 4. イベント（フロントエンド ⇄ バックエンド Pub/Sub）

Tauriは双方向イベントシステムを提供します。

**RustからJSへ：**

```rust
use tauri::Emitter;

#[tauri::command]
fn emit_progress(app: tauri::AppHandle) {
    for i in 0..100 {
        app.emit("download-progress", i).unwrap();
        std::thread::sleep(std::time::Duration::from_millis(50));
    }
}
```

```javascript
import { listen } from "@tauri-apps/api/event";

const unlisten = await listen("download-progress", (event) => {
  console.log("Progress:", event.payload);
});

// Later, to stop listening:
unlisten();
```

**JSからRustへ：**

```rust
use tauri::Listener;

app.listen("ui-event", |event| {
    println!("Received from UI: {:?}", event.payload());
});
```

### 5. プラグインシステム

Tauriのプラグインアーキテクチャは最も強力な機能の1つです。公式プラグインが一般的なニーズをカバーしています：

| プラグイン | 目的 |
|--------|---------|
| `tauri-plugin-sql` | Rustの`sqlx`経由でSQLite/MySQL/PostgreSQLを利用 |
| `tauri-plugin-http` | カスタムヘッダーとストリーミングを備えたHTTPクライアント |
| `tauri-plugin-shell` | プロセスの起動と子プロセスの管理 |
| `tauri-plugin-dialog` | ネイティブのファイルを開く／保存ダイアログとメッセージボックス |
| `tauri-plugin-fs` | スコープ付き権限によるファイルシステムアクセス |
| `tauri-plugin-notification` | デスクトップ／モバイル向けネイティブ通知 |
| `tauri-plugin-clipboard-manager` | クリップボードの読み書き |
| `tauri-plugin-store` | 永続的なキーバリューストレージ（JSON） |
| `tauri-plugin-autostart` | OSログイン時にアプリを自動起動 |
| `tauri-plugin-updater` | 署名付き自動アップデート |

**例：SQLプラグインの追加**

```bash
npm install @tauri-apps/plugin-sql
cargo add tauri-plugin-sql --features sqlite
```

Rust側で登録：

```rust
use tauri_plugin_sql::{Builder as SqlBuilder};

tauri::Builder::default()
    .plugin(
        SqlBuilder::default()
            .add_migrations("sqlite:data.db", vec![/* migrations */])
            .build(),
    )
```

フロントエンドで使用：

```javascript
import Database from "@tauri-apps/plugin-sql";

const db = await Database.load("sqlite:data.db");
const users = await db.select("SELECT * FROM users WHERE id = $1", [42]);
await db.execute("INSERT INTO users (name) VALUES ($1)", ["Alice"]);
```

ケイパビリティファイルに対応する権限を追加します：

```json
"permissions": ["sql:default", "sql:allow-select", "sql:allow-execute"]
```

### 6. マルチウィンドウとシステムトレイ

```rust
use tauri::{WebviewUrl, WebviewWindowBuilder};

#[tauri::command]
async fn open_secondary(app: tauri::AppHandle) -> Result<(), String> {
    WebviewWindowBuilder::new(&app, "secondary", WebviewUrl::App("index.html".into()))
        .title("Secondary Window")
        .inner_size(600.0, 400.0)
        .build()
        .map_err(|e| e.to_string())?;
    Ok(())
}
```

システムトレイ：

```rust
use tauri::tray::{TrayIconBuilder, TrayIconEvent};
use tauri::menu::{Menu, MenuItem};

let quit_i = MenuItem::with_id(app, "quit", "Quit", true, None::<&str>)?;
let menu = Menu::with_items(app, &[&quit_i])?;

TrayIconBuilder::new()
    .icon(app.default_window_icon().unwrap().clone())
    .menu(&menu)
    .on_menu_event(|app, event| match event.id.as_ref() {
        "quit" => app.exit(0),
        _ => {}
    })
    .on_tray_icon_event(|tray, event| {
        if let TrayIconEvent::Click { .. } = event {
            let app = tray.app_handle();
            if let Some(window) = app.get_webview_window("main") {
                let _ = window.show();
                let _ = window.set_focus();
            }
        }
    })
    .build(app)?;
```

### 7. ファイルシステムとパス

プラグインを介してスコープ付きのファイルシステムアクセスを使用します：

```javascript
import { readTextFile, writeTextFile, mkdir } from "@tauri-apps/plugin-fs";
import { appDataDir, join } from "@tauri-apps/api/path";

const dir = await appDataDir();
const filePath = await join(dir, "settings.json");

await mkdir(dir, { recursive: true });
await writeTextFile(filePath, JSON.stringify({ theme: "dark" }));
const content = await readTextFile(filePath);
```

これらの呼び出しには、`fs:allow-read-text-file`、`fs:allow-write-text-file`、およびケイパビリティファイル内の適切なスコープエントリが必要です。

## 本番アプリのビルド

```bash
npm run tauri build
```

これにより `beforeBuildCommand` が実行され、リリースモードでRustバイナリがコンパイルされ、ネイティブインストーラが生成されます：

- **Windows**: `.msi`（WiX）と `.exe`（NSIS）
- **macOS**: `.dmg` と `.app` バンドル
- **Linux**: `.deb`、`.rpm`、AppImage
- **モバイル**: Android用 `apk`／`aab`、iOS用 `ipa`（Xcodeと署名が必要）

特定のフォーマットを指定する場合：

```bash
npm run tauri build -- --bundles msi
npm run tauri build -- --bundles appimage
```

### コード署名とノータリゼーション

- **macOS**: `tauri.conf.json` に `appleDeveloperTeamId` を設定し、`--sign` を付けて実行します。
- **Windows**: 環境変数（`TAURI_SIGNING_PRIVATE_KEY`）を介して `.pfx` 証明書を指定します。
- **Linux**: ほとんどのディストリビューションでは不要です。

## モバイル開発（Tauri 2.0+）

Tauri 2.0はiOSとAndroidを公式にサポートしています。前提条件：

- **Android**: Android Studio、Android SDK/NDK、Java JDK 17
- **iOS**: Xcode 15+を搭載したmacOS、CocoaPods

モバイルプラットフォームをプロジェクトに追加：

```bash
npm run tauri android init
npm run tauri ios init
```

デバイス／エミュレータで実行：

```bash
npm run tauri android dev
npm run tauri ios dev
```

モバイル固有の注意点：

- `lib.rs` で `tauri::mobile_entry_point` を使用します（雛形に含まれています）。
- Rustコマンドはモバイルでも同じように動作します。WebViewはiOSでは `WKWebView`、AndroidではAndroidのWebViewです。
- プラグインエコシステムにはモバイル固有のプラグインが含まれます（例：`tauri-plugin-nfc`、`tauri-plugin-barcode-scanner`、`tauri-plugin-geolocation`）。
- モバイルサポートは継続的に成熟しています。実機で早い段階から頻繁にテストしてください。

## ベストプラクティス

1. **コマンドは可能な限り小さく、同期的に保つ** — 重い計算を行う非同期コマンドは、IPCスレッドをブロックしないように `tokio` タスクを使用してください。
2. **初日からケイパビリティシステムを使う** — プロトタイプでも明示的な権限を定義してください。後から追加するのははるかに困難になります。
3. **`tauri.conf.json` で厳格なCSPを設定**：

   ```json
   "security": {
     "csp": "default-src 'self'; connect-src ipc: http://ipc.localhost; img-src 'self' data:; style-src 'self' 'unsafe-inline'"
   }
   ```

4. **フロントエンドからAPIキーを排除する** — JS内のものはすべて検査可能です。シークレットはRust側に置いてください。
5. **パフォーマンスが重要な経路にはRustを活用する** — ソート、パース、暗号、ファイル処理はすべてRustのほうが劇的に高速です。
6. **設定には手書きのファイルI/Oではなく `tauri-plugin-store` を推奨**します。
7. **WebViewの差異に対処する** — すべてのターゲットOSでテストしてください。Linuxの古いWebKitGTKバージョンやWindowsの古いWebView2バージョンは、最新のCSSで異なる動作をすることがあります。

## よくある落とし穴とトラブルシューティング

| 問題 | 原因 | 解決策 |
|---------|-------|-----|
| **Linuxでウィンドウが真っ白** | `webkit2gtk` 開発パッケージの欠落 | `sudo apt install libwebkit2gtk-4.1-dev` |
| **実行時に権限拒否** | コマンド／プラグインがケイパビリティで宣言されていない | `capabilities/*.json` に権限識別子を追加 |
| **`cargo build` がリンカーエラーで失敗** | MSVC／Windows SDK、またはLinuxの`build-essential`が欠落 | プラットフォームのビルドツールをインストール |
| **WebViewに古いコンテンツが表示される** | 開発アセットのキャッシュ | ハードリフレッシュまたは開発サーバーの再起動。必要に応じて `rm -rf target` |
| **バイナリがまだ大きい** | デバッグビルド、`strip` 未使用 | `npm run tauri build`（リリース）でビルドし、`Cargo.toml` で `strip` を有効化 |
| **モバイルビルドが遅い／失敗する** | NDKバージョンの不一致 | Tauri推奨のNDKバージョンを使用し、Gradleを同期 |
| **JSの `invoke` が `undefined` を返す** | コマンド名の不一致、またはスネークケース／キャメルケースの混同 | コマンド名を確認し、JSではキャメルケースを使用（`myCommand` ↔ `my_command`） |

## エコシステムとリソース

- **公式ドキュメント**：https://v2.tauri.app
- **GitHub**：https://github.com/tauri-apps/tauri
- **プラグインレジストリ**：https://v2.tauri.app/plugin/
- **Awesome Tauri**：https://github.com/tauri-apps/awesome-tauri
- **Discordコミュニティ**：活発で、支援的、そして公式です。

## まとめ

Tauriは、Electronに対する最も魅力的な現代の代替手段です。劇的に小さいバイナリを生成し、メモリ消費が少なく、厳格なセキュリティモデルを強制し、さらにTauri 2.xでは単一のコードベースからデスクトップ **および** モバイルをカバーします。その代償として、Rustの真の学習曲線と、プラットフォーム間でのシステムWebViewの本質的な一貫性のなさがあります。

すでにWebフロントエンドに慣れており、ネイティブパフォーマンス、小さな配布サイズ、セキュリティファーストのアーキテクチャを求めるチームにとって、TauriはRustの信頼性とWebプラットフォームの柔軟性を組み合わせた、本番利用可能な選択肢です。