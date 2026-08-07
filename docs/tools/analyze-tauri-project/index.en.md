---
title: "Tauri: Building Lightweight Cross-Platform Apps with Rust and Web Frontends"
description: "A comprehensive developer guide to Tauri, the Rust-based framework for building secure, minimal-size desktop and mobile applications using web technologies."
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

# Tauri: Building Lightweight Cross-Platform Apps with Rust and Web Frontends

## Overview

**Tauri** is an open-source toolkit for building desktop and mobile applications using web frontend technologies (HTML, CSS, JavaScript/TypeScript) with a **Rust backend**. Unlike Electron, which bundles a full Chromium engine (~150+ MB), Tauri leverages the **operating system's native webview** — WebView2 on Windows, WebKit on macOS, and WebKitGTK on Linux. This results in dramatically smaller binaries (often under 10 MB) and significantly lower memory consumption.

Tauri 2.0, released in October 2024, adds official **iOS and Android support**, making it a genuinely cross-platform framework. The core is built with Rust, and the CLI can be driven via npm, Cargo, or a standalone binary.

## Why Tauri?

The primary motivation for Tauri is the bloat and security surface of Electron. Tauri was designed as a response to three key pain points:

| Concern | Electron | Tauri |
|---------|----------|-------|
| **Bundle size** | 150–250 MB per installer | 3–15 MB per installer |
| **Memory usage** | 300–500 MB baseline | 50–150 MB baseline |
| **Security** | Full Chromium exposure; remote code possible | Capability-based permissions; no remote code by default |
| **Backend** | Node.js (or Python via bindings) | Rust (native speed, memory-safe) |
| **Frontend** | Any web framework | Any web framework |

Tauri is the right choice when:
- You want an app that feels native and launches instantly.
- You care about security and want strict control over what your frontend can access.
- You're comfortable writing (or learning) Rust for backend logic.
- You need one codebase targeting Windows, macOS, Linux, iOS, and Android.

## Architecture

Tauri's architecture is a hybrid of a web frontend and a Rust core, communicating over a secure IPC bridge:

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

**Key architectural points:**

- **No Node.js runtime** is bundled in the final app. The frontend consists of static assets compiled into the binary.
- **IPC** between JS and Rust uses a message-passing protocol; the frontend *cannot* directly call arbitrary system APIs without explicit permissions.
- **Capabilities** define what your frontend can access (filesystem paths, HTTP hosts, plugin scopes) at build time.

## History & Release Timeline

- **2018** — Daniel Thompson-Yvetot creates the initial proof-of-concept.
- **June 19, 2022** — **Tauri 1.0** stable release.
- **2023** — Tauri Foundation joins the Linux Foundation.
- **October 2024** — **Tauri 2.0** adds iOS/Android support, a new plugin system, and unified architecture.

## Installation

### Prerequisites

| Platform | Requirements |
|----------|--------------|
| **Windows** | WebView2 runtime (preinstalled on Windows 11), Rust, MSVC build tools |
| **macOS** | Xcode Command Line Tools, Rust |
| **Linux** | `libwebkit2gtk-4.1-dev`, `build-essential`, `libssl-dev`, `libayatana-appindicator3-dev`, `librsvg2-dev`, Rust |

Linux (Debian/Ubuntu) one-liner:

```bash
sudo apt update
sudo apt install libwebkit2gtk-4.1-dev build-essential curl wget file libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev
```

Install Rust via [rustup](https://rustup.rs/):

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Scaffold a New Project

Use the official scaffolding tool (works with npm, pnpm, yarn, bun, cargo):

```bash
npm create tauri-app@latest
```

You'll be prompted for:
1. Project name
2. Frontend framework (React, Vue, Svelte, Solid, Angular, Vanilla)
3. UI language (TypeScript / JavaScript)
4. Package manager

Then:

```bash
cd my-app
npm install
npm run tauri dev
```

This launches a dev server for hot-reloading your frontend and compiles the Rust binary. The first build takes a couple of minutes; subsequent builds are fast.

### CLI Alternatives

```bash
# Global npm CLI
npm install -g @tauri-apps/cli

# Or via Cargo
cargo install tauri-cli
cargo tauri dev
```

## Project Structure

A scaffolded Tauri project looks like this:

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

The main configuration file controls everything from the app identifier to build settings:

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

## Core Concepts

### 1. Commands (Rust ⇄ JS IPC)

Commands are Rust functions exposed to the frontend. Define them with `#[tauri::command]` and register them in the builder.

**Rust side** (`src-tauri/src/lib.rs`):

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

**JavaScript side** (using the `@tauri-apps/api` package):

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

**Parameter naming note:** Tauri converts Rust snake_case arguments to camelCase in JS. A Rust param named `user_name` is called as `{ userName: "..." }`. To keep the exact name, use `rename_all = "snake_case"` on the command:

```rust
#[tauri::command(rename_all = "snake_case")]
fn my_command(user_name: &str) {}
```

### 2. Rust Backend State

Share state across commands using `manage()`:

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

### 3. Capabilities & Permissions

Since Tauri 2.0, all IPC access is gated by a **capability system**. A capability file defines which windows/webviews can access which commands, plugins, and scopes.

`src-tauri/capabilities/default.json`:

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

**Important:** Without a capability granting a permission, invoking that command will fail with a permission-denied error at runtime. This is a deliberate design decision to minimize the attack surface.

### 4. Events (Frontend ⇄ Backend Pub/Sub)

Tauri provides a bidirectional event system.

**From Rust to JS:**

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

**From JS to Rust:**

```rust
use tauri::Listener;

app.listen("ui-event", |event| {
    println!("Received from UI: {:?}", event.payload());
});
```

### 5. Plugin System

Tauri's plugin architecture is one of its strongest features. Official plugins cover common needs:

| Plugin | Purpose |
|--------|---------|
| `tauri-plugin-sql` | SQLite/MySQL/PostgreSQL via Rust `sqlx` |
| `tauri-plugin-http` | HTTP client with custom headers & streaming |
| `tauri-plugin-shell` | Spawn processes and manage child processes |
| `tauri-plugin-dialog` | Native open/save file dialogs and message boxes |
| `tauri-plugin-fs` | Filesystem access with scoped permissions |
| `tauri-plugin-notification` | Native desktop/mobile notifications |
| `tauri-plugin-clipboard-manager` | Read/write clipboard |
| `tauri-plugin-store` | Persistent key-value storage (JSON) |
| `tauri-plugin-autostart` | Launch the app at OS login |
| `tauri-plugin-updater` | Signed automatic updates |

**Example: adding SQL plugin**

```bash
npm install @tauri-apps/plugin-sql
cargo add tauri-plugin-sql --features sqlite
```

Register in Rust:

```rust
use tauri_plugin_sql::{Builder as SqlBuilder};

tauri::Builder::default()
    .plugin(
        SqlBuilder::default()
            .add_migrations("sqlite:data.db", vec![/* migrations */])
            .build(),
    )
```

Use in the frontend:

```javascript
import Database from "@tauri-apps/plugin-sql";

const db = await Database.load("sqlite:data.db");
const users = await db.select("SELECT * FROM users WHERE id = $1", [42]);
await db.execute("INSERT INTO users (name) VALUES ($1)", ["Alice"]);
```

Add matching permissions to your capability file:

```json
"permissions": ["sql:default", "sql:allow-select", "sql:allow-execute"]
```

### 6. Multi-Window & System Tray

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

System tray:

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

### 7. File System & Paths

Use scoped filesystem access through the plugin:

```javascript
import { readTextFile, writeTextFile, mkdir } from "@tauri-apps/plugin-fs";
import { appDataDir, join } from "@tauri-apps/api/path";

const dir = await appDataDir();
const filePath = await join(dir, "settings.json");

await mkdir(dir, { recursive: true });
await writeTextFile(filePath, JSON.stringify({ theme: "dark" }));
const content = await readTextFile(filePath);
```

These calls require `fs:allow-read-text-file`, `fs:allow-write-text-file`, and appropriate scope entries in your capabilities file.

## Building Production Apps

```bash
npm run tauri build
```

This runs `beforeBuildCommand`, compiles the Rust binary in release mode, and generates native installers:

- **Windows**: `.msi` (WiX) and `.exe` (NSIS)
- **macOS**: `.dmg` and `.app` bundle
- **Linux**: `.deb`, `.rpm`, and AppImage
- **Mobile**: `apk`/`aab` for Android, `ipa` for iOS (requires Xcode + signing)

Targeting specific formats:

```bash
npm run tauri build -- --bundles msi
npm run tauri build -- --bundles appimage
```

### Code Signing & Notarization

- **macOS**: Set `appleDeveloperTeamId` in `tauri.conf.json` and run with `--sign`.
- **Windows**: Provide a `.pfx` certificate via environment variables (`TAURI_SIGNING_PRIVATE_KEY`).
- **Linux**: Not required for most distributions.

## Mobile Development (Tauri 2.0+)

Tauri 2.0 officially supports iOS and Android. Prerequisites:

- **Android**: Android Studio, Android SDK/NDK, Java JDK 17
- **iOS**: macOS with Xcode 15+, CocoaPods

Add mobile platforms to your project:

```bash
npm run tauri android init
npm run tauri ios init
```

Run on a device/emulator:

```bash
npm run tauri android dev
npm run tauri ios dev
```

Mobile-specific notes:

- Use `tauri::mobile_entry_point` in `lib.rs` (the scaffold includes it).
- Rust commands work identically on mobile; the webview is `WKWebView` on iOS and Android's WebView.
- The plugin ecosystem includes mobile-specific plugins (e.g., `tauri-plugin-nfc`, `tauri-plugin-barcode-scanner`, `tauri-plugin-geolocation`).
- Mobile support matures continuously; test early and often on physical devices.

## Best Practices

1. **Keep commands small and synchronous where possible** — Async commands with heavy computation should use `tokio` tasks to avoid blocking the IPC thread.
2. **Use the capability system from day one** — Even for prototypes, define explicit permissions. It becomes much harder to retrofit later.
3. **Set a strict CSP** in `tauri.conf.json`:

   ```json
   "security": {
     "csp": "default-src 'self'; connect-src ipc: http://ipc.localhost; img-src 'self' data:; style-src 'self' 'unsafe-inline'"
   }
   ```

4. **Scrub API keys from the frontend** — Anything in JS is inspectable. Put secrets in Rust.
5. **Leverage Rust for performance-critical paths** — Sorting, parsing, crypto, file processing are all dramatically faster in Rust.
6. **Prefer `tauri-plugin-store` for settings** rather than hand-rolling file I/O.
7. **Handle webview differences** — Test on all target OSes. Old WebKitGTK versions on Linux and older WebView2 versions on Windows can behave differently with modern CSS.

## Common Pitfalls & Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| **Blank window on Linux** | Missing `webkit2gtk` dev packages | `sudo apt install libwebkit2gtk-4.1-dev` |
| **Permission denied** at runtime | Command/plugin not declared in capabilities | Add the permission identifier to `capabilities/*.json` |
| **`cargo build` fails with linker errors** | Missing MSVC/Windows SDK or `build-essential` on Linux | Install platform build tools |
| **Webview shows old content** | Cached dev assets | Hard refresh or restart dev server; `rm -rf target` if needed |
| **Binary still large** | Debug build; not using `strip` | Build with `npm run tauri build` (release) and enable `strip` in `Cargo.toml` |
| **Mobile build slow/fail** | NDK version mismatch | Use the NDK version recommended by Tauri; sync Gradle |
| **JS `invoke` returns `undefined`** | Command name mismatch or snake_case/camelCase confusion | Confirm command name and use camelCase in JS (`myCommand` ↔ `my_command`) |

## Ecosystem & Resources

- **Official docs**: https://v2.tauri.app
- **GitHub**: https://github.com/tauri-apps/tauri
- **Plugins registry**: https://v2.tauri.app/plugin/
- **Awesome Tauri**: https://github.com/tauri-apps/awesome-tauri
- **Discord community**: Active, helpful, and official

## Conclusion

Tauri represents the most compelling modern alternative to Electron: it produces dramatically smaller binaries, uses less memory, enforces a strict security model, and — with Tauri 2.x — spans desktop **and** mobile from a single codebase. The trade-off is a real learning curve in Rust and the inherent inconsistency of system webviews across platforms.

For teams already comfortable with web frontends who want native performance, small distribution size, and a security-first architecture, Tauri is a production-ready choice that pairs Rust's reliability with the flexibility of the web platform.