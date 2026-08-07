---
title: "Tauri：使用 Rust 与 Web 前端构建轻量级跨平台应用"
description: "一份面向开发者的 Tauri 综合指南，介绍如何用这一基于 Rust 的框架通过 Web 技术构建安全、体积最小的桌面与移动应用。"
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

# Tauri：使用 Rust 与 Web 前端构建轻量级跨平台应用

## 概述

**Tauri** 是一个开源工具包，用于构建基于 Web 前端技术（HTML、CSS、JavaScript/TypeScript）并搭配 **Rust 后端**的桌面与移动应用。与捆绑完整 Chromium 引擎（约 150+ MB）的 Electron 不同，Tauri 充分利用**操作系统自带的原生 webview**——Windows 上的 WebView2、macOS 上的 WebKit 以及 Linux 上的 WebKitGTK。这使得最终二进制文件体积大幅缩小（通常不到 10 MB），内存消耗也显著降低。

2024 年 10 月发布的 Tauri 2.0 增加了对 **iOS 和 Android 的官方支持**，使其成为真正意义上的跨平台框架。核心基于 Rust 构建，CLI 可以通过 npm、Cargo 或独立二进制文件来驱动。

## 为什么选择 Tauri？

选择 Tauri 的主要动机来自 Electron 的臃肿体积与攻击面。Tauri 正是针对以下三个关键痛点而设计的：

| 关注点 | Electron | Tauri |
|---------|----------|-------|
| **安装包体积** | 每个安装包 150–250 MB | 每个安装包 3–15 MB |
| **内存占用** | 300–500 MB 基础用量 | 50–150 MB 基础用量 |
| **安全性** | 完整 Chromium 暴露面；可执行远程代码 | 基于能力的权限控制；默认不执行远程代码 |
| **后端** | Node.js（或通过绑定使用 Python） | Rust（原生速度，内存安全） |
| **前端** | 任意 Web 框架 | 任意 Web 框架 |

在以下场景中，Tauri 是正确的选择：
- 你希望应用具备原生体验并能瞬时启动。
- 你重视安全性，希望严格控制前端能够访问的内容。
- 你愿意用 Rust 编写（或学习）后端逻辑。
- 你需要一套代码库同时覆盖 Windows、macOS、Linux、iOS 和 Android。

## 架构

Tauri 的架构是 Web 前端与 Rust 核心的混合体，二者通过安全的 IPC 桥接进行通信：

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

**关键架构要点：**

- **不捆绑 Node.js 运行时**。前端由编译进二进制文件的静态资源组成。
- JS 与 Rust 之间的 **IPC** 采用消息传递协议；前端在未获得显式权限的情况下*无法*直接调用任意系统 API。
- **能力（Capabilities）** 在构建时定义了你的前端可以访问的内容（文件系统路径、HTTP 主机、插件作用域）。

## 历史与发布时间线

- **2018 年** — Daniel Thompson-Yvetot 创建了最初的概念验证。
- **2022 年 6 月 19 日** — **Tauri 1.0** 稳定版发布。
- **2023 年** — Tauri 基金会加入 Linux 基金会。
- **2024 年 10 月** — **Tauri 2.0** 增加了 iOS/Android 支持、全新的插件系统与统一架构。

## 安装

### 环境要求

| 平台 | 要求 |
|----------|--------------|
| **Windows** | WebView2 运行时（Windows 11 已预装）、Rust、MSVC 构建工具 |
| **macOS** | Xcode 命令行工具、Rust |
| **Linux** | `libwebkit2gtk-4.1-dev`、`build-essential`、`libssl-dev`、`libayatana-appindicator3-dev`、`librsvg2-dev`、Rust |

Linux（Debian/Ubuntu）一行命令：

```bash
sudo apt update
sudo apt install libwebkit2gtk-4.1-dev build-essential curl wget file libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev
```

通过 [rustup](https://rustup.rs/) 安装 Rust：

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### 创建新项目骨架

使用官方脚手架工具（支持 npm、pnpm、yarn、bun、cargo）：

```bash
npm create tauri-app@latest
```

系统会依次提示你选择：
1. 项目名称
2. 前端框架（React、Vue、Svelte、Solid、Angular、Vanilla）
3. UI 语言（TypeScript / JavaScript）
4. 包管理器

然后执行：

```bash
cd my-app
npm install
npm run tauri dev
```

这会启动一个开发服务器以实现前端热重载，并编译 Rust 二进制文件。首次构建需要几分钟，后续构建会很快。

### CLI 替代方案

```bash
# Global npm CLI
npm install -g @tauri-apps/cli

# Or via Cargo
cargo install tauri-cli
cargo tauri dev
```

## 项目结构

一个脚手架化的 Tauri 项目结构如下：

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

主配置文件控制从应用标识符到构建设置的一切：

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

## 核心概念

### 1. 命令（Rust ⇄ JS IPC）

命令是暴露给前端的 Rust 函数。使用 `#[tauri::command]` 定义它们，并在 builder 中注册。

**Rust 端**（`src-tauri/src/lib.rs`）：

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

**JavaScript 端**（使用 `@tauri-apps/api` 包）：

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

**参数命名说明：** Tauri 会将 Rust 的 snake_case 参数转换为 JS 中的 camelCase。例如 Rust 参数名为 `user_name` 时，在 JS 中应写作 `{ userName: "..." }`。如需保持原名，可在命令上使用 `rename_all = "snake_case"`：

```rust
#[tauri::command(rename_all = "snake_case")]
fn my_command(user_name: &str) {}
```

### 2. Rust 后端状态

使用 `manage()` 在多个命令之间共享状态：

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

### 3. 能力与权限

自 Tauri 2.0 起，所有 IPC 访问都受**能力系统**管控。能力文件定义了哪些窗口/webview 可以访问哪些命令、插件和作用域。

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

**重要提示：** 如果能力文件中未授予相应权限，调用该命令将在运行时以“权限被拒绝”错误失败。这是有意为之的设计决策，旨在将攻击面降至最低。

### 4. 事件（前端 ⇄ 后端 发布/订阅）

Tauri 提供了双向事件系统。

**从 Rust 到 JS：**

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

**从 JS 到 Rust：**

```rust
use tauri::Listener;

app.listen("ui-event", |event| {
    println!("Received from UI: {:?}", event.payload());
});
```

### 5. 插件系统

Tauri 的插件架构是其最强大的特性之一。官方插件覆盖了常见的需求：

| 插件 | 用途 |
|--------|---------|
| `tauri-plugin-sql` | 通过 Rust `sqlx` 操作 SQLite/MySQL/PostgreSQL |
| `tauri-plugin-http` | 支持自定义请求头与流式传输的 HTTP 客户端 |
| `tauri-plugin-shell` | 启动进程并管理子进程 |
| `tauri-plugin-dialog` | 原生打开/保存文件对话框与消息框 |
| `tauri-plugin-fs` | 具备作用域权限的文件系统访问 |
| `tauri-plugin-notification` | 桌面/移动端原生通知 |
| `tauri-plugin-clipboard-manager` | 读写剪贴板 |
| `tauri-plugin-store` | 持久化键值存储（JSON） |
| `tauri-plugin-autostart` | 在操作系统登录时启动应用 |
| `tauri-plugin-updater` | 签名自动更新 |

**示例：添加 SQL 插件**

```bash
npm install @tauri-apps/plugin-sql
cargo add tauri-plugin-sql --features sqlite
```

在 Rust 中注册：

```rust
use tauri_plugin_sql::{Builder as SqlBuilder};

tauri::Builder::default()
    .plugin(
        SqlBuilder::default()
            .add_migrations("sqlite:data.db", vec![/* migrations */])
            .build(),
    )
```

在前端中使用：

```javascript
import Database from "@tauri-apps/plugin-sql";

const db = await Database.load("sqlite:data.db");
const users = await db.select("SELECT * FROM users WHERE id = $1", [42]);
await db.execute("INSERT INTO users (name) VALUES ($1)", ["Alice"]);
```

在能力文件中添加相应的权限：

```json
"permissions": ["sql:default", "sql:allow-select", "sql:allow-execute"]
```

### 6. 多窗口与系统托盘

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

系统托盘：

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

### 7. 文件系统与路径

通过插件使用受作用域约束的文件系统访问：

```javascript
import { readTextFile, writeTextFile, mkdir } from "@tauri-apps/plugin-fs";
import { appDataDir, join } from "@tauri-apps/api/path";

const dir = await appDataDir();
const filePath = await join(dir, "settings.json");

await mkdir(dir, { recursive: true });
await writeTextFile(filePath, JSON.stringify({ theme: "dark" }));
const content = await readTextFile(filePath);
```

这些调用需要在能力文件中声明 `fs:allow-read-text-file`、`fs:allow-write-text-file` 以及相应的作用域条目。

## 构建生产应用

```bash
npm run tauri build
```

这会运行 `beforeBuildCommand`，以发布模式编译 Rust 二进制文件，并生成原生安装包：

- **Windows**：`.msi`（WiX）和 `.exe`（NSIS）
- **macOS**：`.dmg` 和 `.app` 应用包
- **Linux**：`.deb`、`.rpm` 和 AppImage
- **移动端**：Android 的 `apk`/`aab`、iOS 的 `ipa`（需要 Xcode + 签名）

指定特定格式：

```bash
npm run tauri build -- --bundles msi
npm run tauri build -- --bundles appimage
```

### 代码签名与公证

- **macOS**：在 `tauri.conf.json` 中设置 `appleDeveloperTeamId`，并使用 `--sign` 参数运行。
- **Windows**：通过环境变量（`TAURI_SIGNING_PRIVATE_KEY`）提供 `.pfx` 证书。
- **Linux**：大多数发行版不需要签名。

## 移动开发（Tauri 2.0+）

Tauri 2.0 官方支持 iOS 和 Android。前置要求：

- **Android**：Android Studio、Android SDK/NDK、Java JDK 17
- **iOS**：macOS + Xcode 15+、CocoaPods

为项目添加移动平台支持：

```bash
npm run tauri android init
npm run tauri ios init
```

在设备/模拟器上运行：

```bash
npm run tauri android dev
npm run tauri ios dev
```

移动端特别说明：

- 在 `lib.rs` 中使用 `tauri::mobile_entry_point`（脚手架中已包含）。
- Rust 命令在移动端的工作方式完全相同；iOS 上的 webview 是 `WKWebView`，Android 上则是 Android 的 WebView。
- 插件生态包含移动端专用插件（例如 `tauri-plugin-nfc`、`tauri-plugin-barcode-scanner`、`tauri-plugin-geolocation`）。
- 移动端支持仍在持续成熟中；请尽早并经常在真机上测试。

## 最佳实践

1. **尽可能保持命令小而同步** —— 计算量大的异步命令应使用 `tokio` 任务，以避免阻塞 IPC 线程。
2. **从一开始就使用能力系统** —— 即使是原型，也要定义明确的权限。事后补充会困难得多。
3. **在 `tauri.conf.json` 中设置严格的 CSP**：

   ```json
   "security": {
     "csp": "default-src 'self'; connect-src ipc: http://ipc.localhost; img-src 'self' data:; style-src 'self' 'unsafe-inline'"
   }
   ```

4. **从前端中清除 API 密钥** —— JS 中的任何内容都是可被检查的。将机密信息放在 Rust 中。
5. **让 Rust 承担性能关键路径** —— 排序、解析、加密、文件处理在 Rust 中都会快得多。
6. **优先使用 `tauri-plugin-store` 管理设置**，而不是手写文件 I/O。
7. **处理 webview 差异** —— 在目标操作系统上全面测试。Linux 上较旧的 WebKitGTK 版本和 Windows 上较旧的 WebView2 版本对现代 CSS 的表现可能不同。

## 常见陷阱与故障排查

| 问题 | 原因 | 解决方法 |
|---------|-------|-----|
| **Linux 上窗口空白** | 缺少 `webkit2gtk` 开发包 | `sudo apt install libwebkit2gtk-4.1-dev` |
| 运行时提示 **权限被拒绝** | 命令/插件未在能力文件中声明 | 将权限标识符添加到 `capabilities/*.json` |
| **`cargo build` 出现链接器错误** | 缺少 MSVC/Windows SDK（Windows）或 `build-essential`（Linux） | 安装平台构建工具 |
| **Webview 显示旧内容** | 开发资源被缓存 | 硬刷新或重启开发服务器；必要时执行 `rm -rf target` |
| **二进制文件仍然很大** | 调试构建；未使用 `strip` | 使用 `npm run tauri build`（发布模式）构建，并在 `Cargo.toml` 中启用 `strip` |
| **移动端构建缓慢/失败** | NDK 版本不匹配 | 使用 Tauri 推荐的 NDK 版本；同步 Gradle |
| **JS `invoke` 返回 `undefined`** | 命令名称不匹配或 snake_case/camelCase 混淆 | 确认命令名称，并在 JS 中使用 camelCase（`myCommand` ↔ `my_command`） |

## 生态与资源

- **官方文档**：https://v2.tauri.app
- **GitHub**：https://github.com/tauri-apps/tauri
- **插件注册表**：https://v2.tauri.app/plugin/
- **Awesome Tauri**：https://github.com/tauri-apps/awesome-tauri
- **Discord 社区**：活跃、乐于助人且官方认证

## 结语

Tauri 代表了当今最具吸引力的 Electron 替代方案：它能生成体积大幅缩小的二进制文件，占用更少内存，实施严格的安全模型，并且凭借 Tauri 2.x，可在单一代码库上同时覆盖桌面端**和**移动端。付出的代价则是 Rust 真实的学习成本曲线，以及系统 webview 在不同平台上的固有不一致性。

对于已经熟悉 Web 前端、同时又追求原生性能、小巧分发体积以及安全至上架构的团队来说，Tauri 是一个可直接用于生产环境的选择，它将 Rust 的可靠性与 Web 平台的灵活性完美结合。