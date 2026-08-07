---
title: "Tauri: Schlanke plattformübergreifende Apps mit Rust und Web-Frontends bauen"
description: "Ein umfassender Entwicklerleitfaden für Tauri, das auf Rust basierende Framework zum Erstellen sicherer, minimaler Desktop- und Mobilanwendungen mit Webtechnologien."
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

# Tauri: Schlanke plattformübergreifende Apps mit Rust und Web-Frontends bauen

## Überblick

**Tauri** ist ein Open-Source-Toolkit zum Erstellen von Desktop- und Mobilanwendungen mit Web-Frontend-Technologien (HTML, CSS, JavaScript/TypeScript) mit einem **Rust-Backend**. Anders als Electron, das eine vollständige Chromium-Engine mitliefert (~150+ MB), nutzt Tauri die **native Webview des Betriebssystems** — WebView2 unter Windows, WebKit unter macOS und WebKitGTK unter Linux. Das führt zu deutlich kleineren Binaries (oft unter 10 MB) und erheblich geringerem Speicherverbrauch.

Tauri 2.0, veröffentlicht im Oktober 2024, fügt offizielle **iOS- und Android-Unterstützung** hinzu und macht das Framework zu einer echten plattformübergreifenden Lösung. Der Kern ist mit Rust gebaut, und die CLI kann über npm, Cargo oder als eigenständiges Binary verwendet werden.

## Warum Tauri?

Die Hauptmotivation für Tauri sind die Bloat und die Angriffsfläche von Electron. Tauri wurde als Antwort auf drei zentrale Problemfelder entwickelt:

| Aspekt | Electron | Tauri |
|---------|----------|-------|
| **Paketgröße** | 150–250 MB pro Installer | 3–15 MB pro Installer |
| **Speicherverbrauch** | 300–500 MB Basislast | 50–150 MB Basislast |
| **Sicherheit** | Vollständige Chromium-Exposition; Remote-Code möglich | Capability-basierte Berechtigungen; standardmäßig kein Remote-Code |
| **Backend** | Node.js (oder Python über Bindings) | Rust (native Geschwindigkeit, speichersicher) |
| **Frontend** | Beliebiges Web-Framework | Beliebiges Web-Framework |

Tauri ist die richtige Wahl, wenn:
- Sie eine App möchten, die sich nativ anfühlt und sofort startet.
- Ihnen Sicherheit wichtig ist und Sie strikt kontrollieren möchten, worauf Ihr Frontend zugreifen kann.
- Sie bereit sind, Rust für die Backend-Logik zu schreiben (oder zu lernen).
- Sie eine Codebasis für Windows, macOS, Linux, iOS und Android benötigen.

## Architektur

Tauris Architektur ist ein Hybrid aus Web-Frontend und Rust-Kern, die über eine sichere IPC-Brücke kommunizieren:

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

**Wichtige architektonische Punkte:**

- **Keine Node.js-Runtime** ist in der finalen App enthalten. Das Frontend besteht aus statischen Assets, die in das Binary kompiliert werden.
- **IPC** zwischen JS und Rust nutzt ein Message-Passing-Protokoll; das Frontend *kann* ohne explizite Berechtigungen nicht direkt auf beliebige System-APIs zugreifen.
- **Capabilities** definieren zur Buildzeit, worauf Ihr Frontend zugreifen kann (Dateisystempfade, HTTP-Hosts, Plugin-Scopes).

## Geschichte & Release-Zeitplan

- **2018** — Daniel Thompson-Yvetot erstellt den ersten Proof-of-Concept.
- **19. Juni 2022** — Stabile Version **Tauri 1.0**.
- **2023** — Die Tauri Foundation tritt der Linux Foundation bei.
- **Oktober 2024** — **Tauri 2.0** fügt iOS-/Android-Unterstützung, ein neues Plugin-System und eine einheitliche Architektur hinzu.

## Installation

### Voraussetzungen

| Plattform | Anforderungen |
|----------|--------------|
| **Windows** | WebView2-Runtime (unter Windows 11 vorinstalliert), Rust, MSVC-Build-Tools |
| **macOS** | Xcode-Befehlszeilentools, Rust |
| **Linux** | `libwebkit2gtk-4.1-dev`, `build-essential`, `libssl-dev`, `libayatana-appindicator3-dev`, `librsvg2-dev`, Rust |

Linux (Debian/Ubuntu) als Einzeiler:

```bash
sudo apt update
sudo apt install libwebkit2gtk-4.1-dev build-essential curl wget file libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev
```

Rust über [rustup](https://rustup.rs/) installieren:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Ein neues Projekt erstellen

Verwenden Sie das offizielle Scaffolding-Werkzeug (funktioniert mit npm, pnpm, yarn, bun, cargo):

```bash
npm create tauri-app@latest
```

Sie werden aufgefordert:
1. Projektname
2. Frontend-Framework (React, Vue, Svelte, Solid, Angular, Vanilla)
3. UI-Sprache (TypeScript / JavaScript)
4. Paketmanager

Dann:

```bash
cd my-app
npm install
npm run tauri dev
```

Dies startet einen Dev-Server für das Hot-Reloading Ihres Frontends und kompiliert das Rust-Binary. Der erste Build dauert ein paar Minuten; spätere Builds sind schnell.

### CLI-Alternativen

```bash
# Globale npm-CLI
npm install -g @tauri-apps/cli

# Oder über Cargo
cargo install tauri-cli
cargo tauri dev
```

## Projektstruktur

Ein generiertes Tauri-Projekt sieht so aus:

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

Die Hauptkonfigurationsdatei steuert alles von der App-Kennung bis zu den Build-Einstellungen:

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

## Kernkonzepte

### 1. Commands (Rust ⇄ JS-IPC)

Commands sind Rust-Funktionen, die dem Frontend zur Verfügung gestellt werden. Definieren Sie sie mit `#[tauri::command]` und registrieren Sie sie im Builder.

**Rust-Seite** (`src-tauri/src/lib.rs`):

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

**JavaScript-Seite** (unter Verwendung des Pakets `@tauri-apps/api`):

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

**Hinweis zur Benennung von Parametern:** Tauri konvertiert Rust-snake_case-Argumente in camelCase in JS. Ein Rust-Parameter mit dem Namen `user_name` wird als `{ userName: "..." }` aufgerufen. Um den exakten Namen beizubehalten, verwenden Sie `rename_all = "snake_case"` in der Command-Definition:

```rust
#[tauri::command(rename_all = "snake_case")]
fn my_command(user_name: &str) {}
```

### 2. Rust-Backend-State

Teilen Sie State über mehrere Commands hinweg mit `manage()`:

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

### 3. Capabilities & Berechtigungen

Seit Tauri 2.0 wird der gesamte IPC-Zugriff durch ein **Capability-System** kontrolliert. Eine Capability-Datei definiert, welche Fenster/Webviews auf welche Commands, Plugins und Scopes zugreifen können.

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

**Wichtig:** Ohne eine Capability, die eine Berechtigung gewährt, schlägt der Aufruf dieses Commands zur Laufzeit mit einem Fehler wegen verweigerter Berechtigung (permission-denied) fehl. Dies ist eine bewusste Designentscheidung, um die Angriffsfläche zu minimieren.

### 4. Events (Frontend ⇄ Backend Pub/Sub)

Tauri bietet ein bidirektionales Event-System.

**Von Rust zu JS:**

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

**Von JS zu Rust:**

```rust
use tauri::Listener;

app.listen("ui-event", |event| {
    println!("Received from UI: {:?}", event.payload());
});
```

### 5. Plugin-System

Tauris Plugin-Architektur ist eines seiner stärksten Features. Offizielle Plugins decken häufige Anforderungen ab:

| Plugin | Zweck |
|--------|-------|
| `tauri-plugin-sql` | SQLite/MySQL/PostgreSQL über Rust `sqlx` |
| `tauri-plugin-http` | HTTP-Client mit benutzerdefinierten Headern & Streaming |
| `tauri-plugin-shell` | Prozesse starten und Kindprozesse verwalten |
| `tauri-plugin-dialog` | Native Öffnen/Speichern-Dialoge und Meldungsfenster |
| `tauri-plugin-fs` | Dateisystemzugriff mit eingeschränkten Berechtigungen |
| `tauri-plugin-notification` | Native Desktop-/Mobile-Benachrichtigungen |
| `tauri-plugin-clipboard-manager` | Zwischenablage lesen/schreiben |
| `tauri-plugin-store` | Persistenter Schlüssel-Wert-Speicher (JSON) |
| `tauri-plugin-autostart` | App beim OS-Login starten |
| `tauri-plugin-updater` | Signierte automatische Updates |

**Beispiel: SQL-Plugin hinzufügen**

```bash
npm install @tauri-apps/plugin-sql
cargo add tauri-plugin-sql --features sqlite
```

In Rust registrieren:

```rust
use tauri_plugin_sql::{Builder as SqlBuilder};

tauri::Builder::default()
    .plugin(
        SqlBuilder::default()
            .add_migrations("sqlite:data.db", vec![/* migrations */])
            .build(),
    )
```

Im Frontend verwenden:

```javascript
import Database from "@tauri-apps/plugin-sql";

const db = await Database.load("sqlite:data.db");
const users = await db.select("SELECT * FROM users WHERE id = $1", [42]);
await db.execute("INSERT INTO users (name) VALUES ($1)", ["Alice"]);
```

Fügen Sie die passenden Berechtigungen zu Ihrer Capability-Datei hinzu:

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

System Tray:

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

### 7. Dateisystem & Pfade

Verwenden Sie den eingeschränkten Dateisystemzugriff über das Plugin:

```javascript
import { readTextFile, writeTextFile, mkdir } from "@tauri-apps/plugin-fs";
import { appDataDir, join } from "@tauri-apps/api/path";

const dir = await appDataDir();
const filePath = await join(dir, "settings.json");

await mkdir(dir, { recursive: true });
await writeTextFile(filePath, JSON.stringify({ theme: "dark" }));
const content = await readTextFile(filePath);
```

Diese Aufrufe erfordern `fs:allow-read-text-file`, `fs:allow-write-text-file` sowie entsprechende Scope-Einträge in Ihrer Capability-Datei.

## Produktions-Builds erstellen

```bash
npm run tauri build
```

Dies führt `beforeBuildCommand` aus, kompiliert das Rust-Binary im Release-Modus und generiert native Installer:

- **Windows**: `.msi` (WiX) und `.exe` (NSIS)
- **macOS**: `.dmg` und `.app`-Bundle
- **Linux**: `.deb`, `.rpm` und AppImage
- **Mobile**: `apk`/`aab` für Android, `ipa` für iOS (erfordert Xcode + Signierung)

Bestimmte Formate erzeugen:

```bash
npm run tauri build -- --bundles msi
npm run tauri build -- --bundles appimage
```

### Codesignierung & Notarisierung

- **macOS**: Setzen Sie `appleDeveloperTeamId` in `tauri.conf.json` und führen Sie den Build mit `--sign` aus.
- **Windows**: Stellen Sie ein `.pfx`-Zertifikat über Umgebungsvariablen bereit (`TAURI_SIGNING_PRIVATE_KEY`).
- **Linux**: Für die meisten Distributionen nicht erforderlich.

## Mobile Entwicklung (Tauri 2.0+)

Tauri 2.0 unterstützt offiziell iOS und Android. Voraussetzungen:

- **Android**: Android Studio, Android SDK/NDK, Java JDK 17
- **iOS**: macOS mit Xcode 15+, CocoaPods

Mobile Plattformen zu Ihrem Projekt hinzufügen:

```bash
npm run tauri android init
npm run tauri ios init
```

Auf einem Gerät/Emulator ausführen:

```bash
npm run tauri android dev
npm run tauri ios dev
```

Hinweise für mobile Entwicklung:

- Verwenden Sie `tauri::mobile_entry_point` in `lib.rs` (das Scaffold enthält es bereits).
- Rust-Commands funktionieren auf Mobilgeräten identisch; die Webview ist auf iOS die `WKWebView` und auf Android die Android-WebView.
- Das Plugin-Ökosystem enthält mobile-spezifische Plugins (z. B. `tauri-plugin-nfc`, `tauri-plugin-barcode-scanner`, `tauri-plugin-geolocation`).
- Die Mobile-Unterstützung wird kontinuierlich verbessert; testen Sie früh und häufig auf echten Geräten.

## Best Practices

1. **Halten Sie Commands klein und nach Möglichkeit synchron** — Async-Commands mit aufwändigen Berechnungen sollten `tokio`-Tasks verwenden, um den IPC-Thread nicht zu blockieren.
2. **Nutzen Sie das Capability-System von Anfang an** — Selbst für Prototypen sollten Sie explizite Berechtigungen definieren. Es wird später deutlich schwerer, dies nachzurüsten.
3. **Setzen Sie eine strikte CSP** in `tauri.conf.json`:

   ```json
   "security": {
     "csp": "default-src 'self'; connect-src ipc: http://ipc.localhost; img-src 'self' data:; style-src 'self' 'unsafe-inline'"
   }
   ```

4. **Entfernen Sie API-Schlüssel aus dem Frontend** — Alles in JS ist einsehbar. Legen Sie Geheimnisse in Rust ab.
5. **Nutzen Sie Rust für leistungskritische Pfade** — Sortieren, Parsen, Krypto, Dateiverarbeitung sind in Rust dramatisch schneller.
6. **Bevorzugen Sie `tauri-plugin-store` für Einstellungen**, anstatt Datei-I/O selbst zu implementieren.
7. **Behandeln Sie Webview-Unterschiede** — Testen Sie auf allen Ziel-Betriebssystemen. Alte WebKitGTK-Versionen unter Linux und ältere WebView2-Versionen unter Windows können sich mit modernem CSS unterschiedlich verhalten.

## Häufige Stolperfallen & Fehlerbehebung

| Problem | Ursache | Lösung |
|---------|---------|--------|
| **Leeres Fenster unter Linux** | Fehlende `webkit2gtk`-Entwicklungspakete | `sudo apt install libwebkit2gtk-4.1-dev` |
| **Berechtigung verweigert** zur Laufzeit | Command/Plugin nicht in Capabilities deklariert | Fügen Sie die Berechtigungskennung zu `capabilities/*.json` hinzu |
| **`cargo build` schlägt mit Linker-Fehlern fehl** | Fehlende MSVC/Windows-SDK- oder `build-essential`-Tools unter Linux | Installieren Sie die Build-Tools der Plattform |
| **Webview zeigt alten Inhalt** | Zwischengespeicherte Dev-Assets | Hard Refresh oder Dev-Server neu starten; ggf. `rm -rf target` |
| **Binary ist immer noch groß** | Debug-Build; kein `strip` verwendet | Mit `npm run tauri build` (Release) bauen und `strip` in `Cargo.toml` aktivieren |
| **Mobile-Build langsam/fehlgeschlagen** | NDK-Versionskonflikt | Verwenden Sie die von Tauri empfohlene NDK-Version; Gradle synchronisieren |
| **JS `invoke` gibt `undefined` zurück** | Command-Name stimmt nicht oder snake_case/camelCase-Verwechslung | Prüfen Sie den Command-Namen und verwenden Sie camelCase in JS (`myCommand` ↔ `my_command`) |

## Ökosystem & Ressourcen

- **Offizielle Dokumentation**: https://v2.tauri.app
- **GitHub**: https://github.com/tauri-apps/tauri
- **Plugin-Verzeichnis**: https://v2.tauri.app/plugin/
- **Awesome Tauri**: https://github.com/tauri-apps/awesome-tauri
- **Discord-Community**: Aktiv, hilfreich und offiziell

## Fazit

Tauri ist die überzeugendste moderne Alternative zu Electron: Es erzeugt deutlich kleinere Binaries, verbraucht weniger Speicher, setzt ein strenges Sicherheitsmodell durch und deckt — mit Tauri 2.x — Desktop **und** Mobile aus einer einzigen Codebasis ab. Der Preis dafür sind eine echte Lernkurve in Rust und die grundsätzliche Inkonsistenz der System-Webviews auf verschiedenen Plattformen.

Für Teams, die mit Web-Frontends bereits vertraut sind und native Leistung, kleine Distributionsgröße und eine Security-First-Architektur wünschen, ist Tauri eine produktionsreife Wahl, die die Zuverlässigkeit von Rust mit der Flexibilität der Web-Plattform verbindet.