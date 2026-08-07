---
title: "Tauri: Creación de aplicaciones multiplataforma ligeras con Rust y frontends web"
description: "Una guía integral para desarrolladores sobre Tauri, el framework basado en Rust para crear aplicaciones de escritorio y móviles seguras y de tamaño mínimo utilizando tecnologías web."
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

# Tauri: Creación de aplicaciones multiplataforma ligeras con Rust y frontends web

## Resumen

**Tauri** es un kit de herramientas de código abierto para crear aplicaciones de escritorio y móviles utilizando tecnologías web frontend (HTML, CSS, JavaScript/TypeScript) con un **backend en Rust**. A diferencia de Electron, que incluye un motor Chromium completo (~150+ MB), Tauri aprovecha el **webview nativo del sistema operativo** — WebView2 en Windows, WebKit en macOS y WebKitGTK en Linux. Esto se traduce en binarios drásticamente más pequeños (a menudo menos de 10 MB) y un consumo de memoria significativamente menor.

Tauri 2.0, lanzado en octubre de 2024, añade soporte oficial para **iOS y Android**, convirtiéndolo en un framework genuinamente multiplataforma. El núcleo está construido con Rust, y la CLI puede utilizarse mediante npm, Cargo o un binario independiente.

## ¿Por qué Tauri?

La motivación principal de Tauri es el tamaño y la superficie de seguridad de Electron. Tauri se diseñó como respuesta a tres puntos débiles clave:

| Preocupación | Electron | Tauri |
|---------|----------|-------|
| **Tamaño del paquete** | 150–250 MB por instalador | 3–15 MB por instalador |
| **Uso de memoria** | 300–500 MB base | 50–150 MB base |
| **Seguridad** | Exposición completa de Chromium; código remoto posible | Permisos basados en capacidades; sin código remoto por defecto |
| **Backend** | Node.js (o Python mediante bindings) | Rust (velocidad nativa, seguro en memoria) |
| **Frontend** | Cualquier framework web | Cualquier framework web |

Tauri es la elección correcta cuando:
- Quieres una aplicación que se sienta nativa y se lance al instante.
- Te importa la seguridad y quieres un control estricto sobre lo que tu frontend puede acceder.
- Te sientes cómodo escribiendo (o aprendiendo) Rust para la lógica del backend.
- Necesitas una única base de código dirigida a Windows, macOS, Linux, iOS y Android.

## Arquitectura

La arquitectura de Tauri es un híbrido de un frontend web y un núcleo Rust, comunicándose a través de un puente IPC seguro:

```
┌─────────────────────────────────────────────────────┐
│                  Frontend (WebView)                 │
│  React / Vue / Svelte / Solid / Vanilla JS / etc.  │
│             HTML · CSS · JavaScript                 │
└─────────────────────────┬───────────────────────────┘
                          │  IPC (basado en postMessage)
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

**Puntos arquitectónicos clave:**

- **No se incluye ningún runtime de Node.js** en la aplicación final. El frontend consiste en activos estáticos compilados dentro del binario.
- **La IPC** entre JS y Rust utiliza un protocolo de paso de mensajes; el frontend *no puede* llamar directamente a APIs arbitrarias del sistema sin permisos explícitos.
- **Las capacidades** definen qué puede acceder tu frontend (rutas del sistema de archivos, hosts HTTP, alcances de plugins) en tiempo de compilación.

## Historia y cronología de versiones

- **2018** — Daniel Thompson-Yvetot crea la prueba de concepto inicial.
- **19 de junio de 2022** — Lanzamiento estable de **Tauri 1.0**.
- **2023** — La Fundación Tauri se une a la Linux Foundation.
- **Octubre de 2024** — **Tauri 2.0** añade soporte para iOS/Android, un nuevo sistema de plugins y una arquitectura unificada.

## Instalación

### Requisitos previos

| Plataforma | Requisitos |
|----------|--------------|
| **Windows** | Runtime WebView2 (preinstalado en Windows 11), Rust, herramientas de compilación MSVC |
| **macOS** | Xcode Command Line Tools, Rust |
| **Linux** | `libwebkit2gtk-4.1-dev`, `build-essential`, `libssl-dev`, `libayatana-appindicator3-dev`, `librsvg2-dev`, Rust |

Comando único para Linux (Debian/Ubuntu):

```bash
sudo apt update
sudo apt install libwebkit2gtk-4.1-dev build-essential curl wget file libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev
```

Instala Rust mediante [rustup](https://rustup.rs/):

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Crear un nuevo proyecto

Utiliza la herramienta oficial de scaffolding (funciona con npm, pnpm, yarn, bun, cargo):

```bash
npm create tauri-app@latest
```

Se te pedirá:
1. Nombre del proyecto
2. Framework frontend (React, Vue, Svelte, Solid, Angular, Vanilla)
3. Lenguaje de la interfaz (TypeScript / JavaScript)
4. Gestor de paquetes

Después:

```bash
cd my-app
npm install
npm run tauri dev
```

Esto lanza un servidor de desarrollo para recargar tu frontend en caliente y compila el binario de Rust. La primera compilación tarda un par de minutos; las compilaciones posteriores son rápidas.

### Alternativas de CLI

```bash
# CLI global de npm
npm install -g @tauri-apps/cli

# O mediante Cargo
cargo install tauri-cli
cargo tauri dev
```

## Estructura del proyecto

Un proyecto Tauri creado con scaffolding tiene este aspecto:

```
my-app/
├── src/                      # Código fuente del frontend (React, Vue, etc.)
│   ├── main.ts
│   └── App.tsx
├── public/                   # Activos estáticos
├── src-tauri/                # Backend en Rust
│   ├── Cargo.toml
│   ├── tauri.conf.json       # Configuración principal
│   ├── build.rs
│   ├── capabilities/
│   │   └── default.json      # Permisos para tu aplicación
│   ├── icons/
│   ├── src/
│   │   ├── main.rs           # Punto de entrada (Windows/Linux/macOS)
│   │   └── lib.rs            # Código compartido + punto de entrada móvil
└── package.json
```

### `tauri.conf.json`

El archivo de configuración principal controla todo, desde el identificador de la aplicación hasta los ajustes de compilación:

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

## Conceptos fundamentales

### 1. Comandos (IPC Rust ⇄ JS)

Los comandos son funciones de Rust expuestas al frontend. Se definen con `#[tauri::command]` y se registran en el builder.

**Lado Rust** (`src-tauri/src/lib.rs`):

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

**Lado JavaScript** (usando el paquete `@tauri-apps/api`):

```javascript
import { invoke } from "@tauri-apps/api/core";

// Invocación simple
const msg = await invoke("greet", { name: "World" });
console.log(msg); // "Hello, World!"

// Con manejo de errores
try {
  const data = await invoke("read_config", { path: "/etc/example.conf" });
} catch (err) {
  console.error("Failed to read:", err);
}
```

**Nota sobre los nombres de parámetros:** Tauri convierte los argumentos en snake_case de Rust a camelCase en JS. Un parámetro Rust llamado `user_name` se invoca como `{ userName: "..." }`. Para mantener el nombre exacto, usa `rename_all = "snake_case"` en el comando:

```rust
#[tauri::command(rename_all = "snake_case")]
fn my_command(user_name: &str) {}
```

### 2. Estado del backend en Rust

Comparte estado entre comandos usando `manage()`:

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

### 3. Capacidades y permisos

Desde Tauri 2.0, todo el acceso IPC está controlado por un **sistema de capacidades**. Un archivo de capacidad define qué ventanas/webviews pueden acceder a qué comandos, plugins y alcances.

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

**Importante:** Sin una capacidad que conceda un permiso, invocar ese comando fallará con un error de permiso denegado en tiempo de ejecución. Esta es una decisión de diseño deliberada para minimizar la superficie de ataque.

### 4. Eventos (Publicación/suscripción Frontend ⇄ Backend)

Tauri proporciona un sistema de eventos bidireccional.

**De Rust a JS:**

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

// Más tarde, para dejar de escuchar:
unlisten();
```

**De JS a Rust:**

```rust
use tauri::Listener;

app.listen("ui-event", |event| {
    println!("Received from UI: {:?}", event.payload());
});
```

### 5. Sistema de plugins

La arquitectura de plugins de Tauri es una de sus características más sólidas. Los plugins oficiales cubren necesidades comunes:

| Plugin | Propósito |
|--------|---------|
| `tauri-plugin-sql` | SQLite/MySQL/PostgreSQL mediante `sqlx` de Rust |
| `tauri-plugin-http` | Cliente HTTP con cabeceras personalizadas y streaming |
| `tauri-plugin-shell` | Ejecutar procesos y gestionar procesos hijos |
| `tauri-plugin-dialog` | Diálogos nativos de abrir/guardar archivos y cuadros de mensaje |
| `tauri-plugin-fs` | Acceso al sistema de archivos con permisos de alcance |
| `tauri-plugin-notification` | Notificaciones nativas de escritorio/móvil |
| `tauri-plugin-clipboard-manager` | Leer/escribir el portapapeles |
| `tauri-plugin-store` | Almacenamiento persistente clave-valor (JSON) |
| `tauri-plugin-autostart` | Iniciar la aplicación al iniciar sesión en el SO |
| `tauri-plugin-updater` | Actualizaciones automáticas firmadas |

**Ejemplo: añadir el plugin SQL**

```bash
npm install @tauri-apps/plugin-sql
cargo add tauri-plugin-sql --features sqlite
```

Regístrate en Rust:

```rust
use tauri_plugin_sql::{Builder as SqlBuilder};

tauri::Builder::default()
    .plugin(
        SqlBuilder::default()
            .add_migrations("sqlite:data.db", vec![/* migrations */])
            .build(),
    )
```

Úsalo en el frontend:

```javascript
import Database from "@tauri-apps/plugin-sql";

const db = await Database.load("sqlite:data.db");
const users = await db.select("SELECT * FROM users WHERE id = $1", [42]);
await db.execute("INSERT INTO users (name) VALUES ($1)", ["Alice"]);
```

Añade los permisos correspondientes a tu archivo de capacidades:

```json
"permissions": ["sql:default", "sql:allow-select", "sql:allow-execute"]
```

### 6. Múltiples ventanas y bandeja del sistema

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

Bandeja del sistema:

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

### 7. Sistema de archivos y rutas

Usa el acceso al sistema de archivos con alcance a través del plugin:

```javascript
import { readTextFile, writeTextFile, mkdir } from "@tauri-apps/plugin-fs";
import { appDataDir, join } from "@tauri-apps/api/path";

const dir = await appDataDir();
const filePath = await join(dir, "settings.json");

await mkdir(dir, { recursive: true });
await writeTextFile(filePath, JSON.stringify({ theme: "dark" }));
const content = await readTextFile(filePath);
```

Estas llamadas requieren `fs:allow-read-text-file`, `fs:allow-write-text-file` y las entradas de alcance apropiadas en tu archivo de capacidades.

## Compilación de aplicaciones de producción

```bash
npm run tauri build
```

Esto ejecuta `beforeBuildCommand`, compila el binario de Rust en modo release y genera instaladores nativos:

- **Windows**: `.msi` (WiX) y `.exe` (NSIS)
- **macOS**: `.dmg` y paquete `.app`
- **Linux**: `.deb`, `.rpm` y AppImage
- **Móvil**: `apk`/`aab` para Android, `ipa` para iOS (requiere Xcode + firma)

Para apuntar a formatos específicos:

```bash
npm run tauri build -- --bundles msi
npm run tauri build -- --bundles appimage
```

### Firma de código y notarización

- **macOS**: Establece `appleDeveloperTeamId` en `tauri.conf.json` y ejecuta con `--sign`.
- **Windows**: Proporciona un certificado `.pfx` mediante variables de entorno (`TAURI_SIGNING_PRIVATE_KEY`).
- **Linux**: No es necesario para la mayoría de las distribuciones.

## Desarrollo móvil (Tauri 2.0+)

Tauri 2.0 es compatible oficialmente con iOS y Android. Requisitos previos:

- **Android**: Android Studio, Android SDK/NDK, Java JDK 17
- **iOS**: macOS con Xcode 15+, CocoaPods

Añade plataformas móviles a tu proyecto:

```bash
npm run tauri android init
npm run tauri ios init
```

Ejecuta en un dispositivo/emulador:

```bash
npm run tauri android dev
npm run tauri ios dev
```

Notas específicas para móvil:

- Usa `tauri::mobile_entry_point` en `lib.rs` (el scaffolding lo incluye).
- Los comandos de Rust funcionan de manera idéntica en móvil; el webview es `WKWebView` en iOS y el WebView de Android.
- El ecosistema de plugins incluye plugins específicos para móvil (p. ej., `tauri-plugin-nfc`, `tauri-plugin-barcode-scanner`, `tauri-plugin-geolocation`).
- El soporte móvil madura continuamente; prueba con frecuencia y en dispositivos físicos.

## Mejores prácticas

1. **Mantén los comandos pequeños y síncronos cuando sea posible** — Los comandos asíncronos con cómputo pesado deberían usar tareas `tokio` para evitar bloquear el hilo IPC.
2. **Usa el sistema de capacidades desde el primer día** — Incluso para prototipos, define permisos explícitos. Es mucho más difícil adaptarlo después.
3. **Establece una CSP estricta** en `tauri.conf.json`:

   ```json
   "security": {
     "csp": "default-src 'self'; connect-src ipc: http://ipc.localhost; img-src 'self' data:; style-src 'self' 'unsafe-inline'"
   }
   ```

4. **Mantén las claves API fuera del frontend** — Cualquier cosa en JS es inspeccionable. Pon los secretos en Rust.
5. **Aprovecha Rust para rutas críticas de rendimiento** — Ordenar, analizar, criptografía, procesamiento de archivos son dramáticamente más rápidos en Rust.
6. **Prefiere `tauri-plugin-store` para ajustes** en lugar de implementar I/O de archivos manualmente.
7. **Maneja las diferencias de webview** — Prueba en todos los SO objetivo. Las versiones antiguas de WebKitGTK en Linux y las versiones antiguas de WebView2 en Windows pueden comportarse de manera diferente con CSS moderno.

## Errores comunes y solución de problemas

| Problema | Causa | Solución |
|---------|-------|-----|
| **Ventana en blanco en Linux** | Faltan paquetes de desarrollo `webkit2gtk` | `sudo apt install libwebkit2gtk-4.1-dev` |
| **Permiso denegado** en tiempo de ejecución | Comando/plugin no declarado en las capacidades | Añade el identificador de permiso a `capabilities/*.json` |
| **`cargo build` falla con errores del enlazador** | Faltan MSVC/Windows SDK o `build-essential` en Linux | Instala las herramientas de compilación de la plataforma |
| **El webview muestra contenido antiguo** | Activos de desarrollo en caché | Recarga forzada o reinicia el servidor de desarrollo; `rm -rf target` si es necesario |
| **El binario sigue siendo grande** | Compilación debug; no se usa `strip` | Compila con `npm run tauri build` (release) y habilita `strip` en `Cargo.toml` |
| **Compilación móvil lenta/falla** | Incompatibilidad de versión del NDK | Usa la versión de NDK recomendada por Tauri; sincroniza Gradle |
| **`invoke` de JS devuelve `undefined`** | El nombre del comando no coincide o confusión entre snake_case/camelCase | Confirma el nombre del comando y usa camelCase en JS (`myCommand` ↔ `my_command`) |

## Ecosistema y recursos

- **Documentación oficial**: https://v2.tauri.app
- **GitHub**: https://github.com/tauri-apps/tauri
- **Registro de plugins**: https://v2.tauri.app/plugin/
- **Awesome Tauri**: https://github.com/tauri-apps/awesome-tauri
- **Comunidad Discord**: Activa, servicial y oficial

## Conclusión

Tauri representa la alternativa moderna más convincente a Electron: produce binarios drásticamente más pequeños, usa menos memoria, impone un modelo de seguridad estricto y — con Tauri 2.x — abarca escritorio **y** móvil desde una única base de código. La contrapartida es una curva de aprendizaje real en Rust y la inconsistencia inherente de los webviews del sistema entre plataformas.

Para equipos que ya se sienten cómodos con frontends web y que quieren rendimiento nativo, tamaño de distribución pequeño y una arquitectura que prioriza la seguridad, Tauri es una opción lista para producción que combina la fiabilidad de Rust con la flexibilidad de la plataforma web.