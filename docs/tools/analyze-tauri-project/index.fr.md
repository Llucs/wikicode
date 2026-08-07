---
title: "Tauri : créer des applications multiplateformes légères avec Rust et des frontends web"
description: "Un guide complet pour les développeurs sur Tauri, le framework basé sur Rust pour créer des applications desktop et mobiles sécurisées et de taille minimale à l'aide de technologies web."
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

# Tauri : créer des applications multiplateformes légères avec Rust et des frontends web

## Vue d'ensemble

**Tauri** est un ensemble d'outils open-source pour créer des applications desktop et mobiles à l'aide de technologies frontend web (HTML, CSS, JavaScript/TypeScript) avec un **backend Rust**. Contrairement à Electron, qui embarque un moteur Chromium complet (~150 Mo et plus), Tauri tire parti de la **webview native du système d'exploitation** — WebView2 sur Windows, WebKit sur macOS et WebKitGTK sur Linux. Cela se traduit par des binaires considérablement plus petits (souvent moins de 10 Mo) et une consommation mémoire nettement inférieure.

Tauri 2.0, publié en octobre 2024, ajoute la prise en charge officielle d'**iOS et d'Android**, ce qui en fait un framework véritablement multiplateforme. Le cœur est construit avec Rust, et la CLI peut être pilotée via npm, Cargo ou un binaire autonome.

## Pourquoi Tauri ?

La motivation principale de Tauri est l'encombrement et la surface de sécurité d'Electron. Tauri a été conçu comme une réponse à trois problèmes clés :

| Critère | Electron | Tauri |
|---------|----------|-------|
| **Taille du bundle** | 150–250 Mo par installateur | 3–15 Mo par installateur |
| **Utilisation mémoire** | 300–500 Mo en base | 50–150 Mo en base |
| **Sécurité** | Exposition complète à Chromium ; exécution de code à distance possible | Permissions fondées sur les capacités ; aucune exécution de code à distance par défaut |
| **Backend** | Node.js (ou Python via des bindings) | Rust (vitesse native, sécurité mémoire) |
| **Frontend** | N'importe quel framework web | N'importe quel framework web |

Tauri est le bon choix lorsque :
- Vous voulez une application qui semble native et se lance instantanément.
- Vous tenez à la sécurité et souhaitez un contrôle strict de ce à quoi votre frontend peut accéder.
- Vous êtes à l'aise pour écrire (ou apprendre) Rust pour la logique backend.
- Vous avez besoin d'une base de code unique ciblant Windows, macOS, Linux, iOS et Android.

## Architecture

L'architecture de Tauri est un hybride entre un frontend web et un cœur Rust, communiquant via un pont IPC sécurisé :

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

**Points architecturaux clés :**

- **Aucun runtime Node.js** n'est inclus dans l'application finale. Le frontend se compose d'actifs statiques compilés dans le binaire.
- **L'IPC** entre JS et Rust utilise un protocole de passage de messages ; le frontend *ne peut pas* appeler directement des API système arbitraires sans autorisations explicites.
- Les **capacités** définissent ce à quoi votre frontend peut accéder (chemins du système de fichiers, hôtes HTTP, portées de plugins) à la compilation.

## Historique et chronologie des versions

- **2018** — Daniel Thompson-Yvetot crée la preuve de concept initiale.
- **19 juin 2022** — Sortie stable de **Tauri 1.0**.
- **2023** — La Tauri Foundation rejoint la Linux Foundation.
- **Octobre 2024** — **Tauri 2.0** ajoute la prise en charge d'iOS/Android, un nouveau système de plugins et une architecture unifiée.

## Installation

### Prérequis

| Plateforme | Prérequis |
|----------|--------------|
| **Windows** | Runtime WebView2 (préinstallé sur Windows 11), Rust, outils de build MSVC |
| **macOS** | Xcode Command Line Tools, Rust |
| **Linux** | `libwebkit2gtk-4.1-dev`, `build-essential`, `libssl-dev`, `libayatana-appindicator3-dev`, `librsvg2-dev`, Rust |

Linux (Debian/Ubuntu) en une ligne :

```bash
sudo apt update
sudo apt install libwebkit2gtk-4.1-dev build-essential curl wget file libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev
```

Installez Rust via [rustup](https://rustup.rs/) :

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Créer un nouveau projet

Utilisez l'outil de génération officiel (fonctionne avec npm, pnpm, yarn, bun, cargo) :

```bash
npm create tauri-app@latest
```

Vous serez invité à renseigner :
1. Le nom du projet
2. Le framework frontend (React, Vue, Svelte, Solid, Angular, Vanilla)
3. Le langage d'interface (TypeScript / JavaScript)
4. Le gestionnaire de paquets

Ensuite :

```bash
cd my-app
npm install
npm run tauri dev
```

Cela lance un serveur de développement pour le rechargement à chaud de votre frontend et compile le binaire Rust. La première compilation prend quelques minutes ; les compilations suivantes sont rapides.

### Alternatives à la CLI

```bash
# Global npm CLI
npm install -g @tauri-apps/cli

# Or via Cargo
cargo install tauri-cli
cargo tauri dev
```

## Structure du projet

Un projet Tauri généré ressemble à ceci :

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

Le fichier de configuration principal contrôle tout, de l'identifiant de l'application aux paramètres de compilation :

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

## Concepts fondamentaux

### 1. Commandes (Rust ⇄ JS IPC)

Les commandes sont des fonctions Rust exposées au frontend. Définissez-les avec `#[tauri::command]` et enregistrez-les dans le builder.

**Côté Rust** (`src-tauri/src/lib.rs`) :

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

**Côté JavaScript** (à l'aide du paquet `@tauri-apps/api`) :

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

**Remarque sur le nommage des paramètres :** Tauri convertit les arguments snake_case de Rust en camelCase en JS. Un paramètre Rust nommé `user_name` est appelé sous la forme `{ userName: "..." }`. Pour conserver le nom exact, utilisez `rename_all = "snake_case"` sur la commande :

```rust
#[tauri::command(rename_all = "snake_case")]
fn my_command(user_name: &str) {}
```

### 2. État du backend Rust

Partagez l'état entre les commandes à l'aide de `manage()` :

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

### 3. Capacités et permissions

Depuis Tauri 2.0, tout accès IPC est contrôlé par un **système de capacités**. Un fichier de capacités définit quelles fenêtres/webviews peuvent accéder à quelles commandes, plugins et portées.

`src-tauri/capabilities/default.json` :

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

**Important :** Sans capacité accordant une permission, l'appel de cette commande échouera avec une erreur d'autorisation refusée à l'exécution. C'est un choix de conception délibéré pour minimiser la surface d'attaque.

### 4. Événements (Frontend ⇄ Backend Pub/Sub)

Tauri fournit un système d'événements bidirectionnel.

**De Rust vers JS :**

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

**De JS vers Rust :**

```rust
use tauri::Listener;

app.listen("ui-event", |event| {
    println!("Received from UI: {:?}", event.payload());
});
```

### 5. Système de plugins

L'architecture de plugins de Tauri est l'un de ses atouts les plus forts. Les plugins officiels couvrent les besoins courants :

| Plugin | Objectif |
|--------|---------|
| `tauri-plugin-sql` | SQLite/MySQL/PostgreSQL via Rust `sqlx` |
| `tauri-plugin-http` | Client HTTP avec en-têtes personnalisés et streaming |
| `tauri-plugin-shell` | Lancer des processus et gérer les processus enfants |
| `tauri-plugin-dialog` | Boîtes de dialogue natives d'ouverture/enregistrement de fichiers et boîtes de message |
| `tauri-plugin-fs` | Accès au système de fichiers avec permissions par portée |
| `tauri-plugin-notification` | Notifications natives desktop/mobile |
| `tauri-plugin-clipboard-manager` | Lire/écrire le presse-papiers |
| `tauri-plugin-store` | Stockage persistant clé-valeur (JSON) |
| `tauri-plugin-autostart` | Lancer l'application à la connexion au système |
| `tauri-plugin-updater` | Mises à jour automatiques signées |

**Exemple : ajout du plugin SQL**

```bash
npm install @tauri-apps/plugin-sql
cargo add tauri-plugin-sql --features sqlite
```

Enregistrez-le dans Rust :

```rust
use tauri_plugin_sql::{Builder as SqlBuilder};

tauri::Builder::default()
    .plugin(
        SqlBuilder::default()
            .add_migrations("sqlite:data.db", vec![/* migrations */])
            .build(),
    )
```

Utilisez-le dans le frontend :

```javascript
import Database from "@tauri-apps/plugin-sql";

const db = await Database.load("sqlite:data.db");
const users = await db.select("SELECT * FROM users WHERE id = $1", [42]);
await db.execute("INSERT INTO users (name) VALUES ($1)", ["Alice"]);
```

Ajoutez les permissions correspondantes à votre fichier de capacités :

```json
"permissions": ["sql:default", "sql:allow-select", "sql:allow-execute"]
```

### 6. Fenêtres multiples et zone de notification système

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

Zone de notification système :

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

### 7. Système de fichiers et chemins

Utilisez l'accès au système de fichiers par portée via le plugin :

```javascript
import { readTextFile, writeTextFile, mkdir } from "@tauri-apps/plugin-fs";
import { appDataDir, join } from "@tauri-apps/api/path";

const dir = await appDataDir();
const filePath = await join(dir, "settings.json");

await mkdir(dir, { recursive: true });
await writeTextFile(filePath, JSON.stringify({ theme: "dark" }));
const content = await readTextFile(filePath);
```

Ces appels nécessitent `fs:allow-read-text-file`, `fs:allow-write-text-file` et les entrées de portée appropriées dans votre fichier de capacités.

## Compilation d'applications de production

```bash
npm run tauri build
```

Cela exécute `beforeBuildCommand`, compile le binaire Rust en mode release et génère des installateurs natifs :

- **Windows** : `.msi` (WiX) et `.exe` (NSIS)
- **macOS** : `.dmg` et bundle `.app`
- **Linux** : `.deb`, `.rpm` et AppImage
- **Mobile** : `apk`/`aab` pour Android, `ipa` pour iOS (nécessite Xcode + signature)

Ciblage de formats spécifiques :

```bash
npm run tauri build -- --bundles msi
npm run tauri build -- --bundles appimage
```

### Signature de code et notarisation

- **macOS** : définissez `appleDeveloperTeamId` dans `tauri.conf.json` et exécutez avec `--sign`.
- **Windows** : fournissez un certificat `.pfx` via les variables d'environnement (`TAURI_SIGNING_PRIVATE_KEY`).
- **Linux** : pas requis pour la plupart des distributions.

## Développement mobile (Tauri 2.0+)

Tauri 2.0 prend officiellement en charge iOS et Android. Prérequis :

- **Android** : Android Studio, Android SDK/NDK, Java JDK 17
- **iOS** : macOS avec Xcode 15+, CocoaPods

Ajoutez les plateformes mobiles à votre projet :

```bash
npm run tauri android init
npm run tauri ios init
```

Exécutez sur un appareil/émulateur :

```bash
npm run tauri android dev
npm run tauri ios dev
```

Remarques spécifiques au mobile :

- Utilisez `tauri::mobile_entry_point` dans `lib.rs` (le squelette généré l'inclut).
- Les commandes Rust fonctionnent à l'identique sur mobile ; la webview est `WKWebView` sur iOS et la WebView d'Android.
- L'écosystème de plugins inclut des plugins spécifiques au mobile (par exemple `tauri-plugin-nfc`, `tauri-plugin-barcode-scanner`, `tauri-plugin-geolocation`).
- La prise en charge mobile évolue en permanence ; testez tôt et souvent sur des appareils physiques.

## Bonnes pratiques

1. **Gardez les commandes courtes et synchrones lorsque c'est possible** — Les commandes asynchrones avec des calculs lourds doivent utiliser des tâches `tokio` pour éviter de bloquer le thread IPC.
2. **Utilisez le système de capacités dès le premier jour** — Même pour les prototypes, définissez des permissions explicites. Il devient beaucoup plus difficile de les ajouter après coup.
3. **Définissez une CSP stricte** dans `tauri.conf.json` :

   ```json
   "security": {
     "csp": "default-src 'self'; connect-src ipc: http://ipc.localhost; img-src 'self' data:; style-src 'self' 'unsafe-inline'"
   }
   ```

4. **Supprimez les clés API du frontend** — Tout ce qui est en JS est inspectable. Placez les secrets dans Rust.
5. **Exploitez Rust pour les chemins critiques en performance** — Le tri, l'analyse, la cryptographie et le traitement de fichiers sont tous considérablement plus rapides en Rust.
6. **Préférez `tauri-plugin-store` pour les paramètres** plutôt que d'écrire vous-même les entrées/sorties fichier.
7. **Gérez les différences entre webviews** — Testez sur tous les systèmes d'exploitation cibles. Les anciennes versions de WebKitGTK sous Linux et les versions plus anciennes de WebView2 sous Windows peuvent se comporter différemment avec le CSS moderne.

## Pièges courants et dépannage

| Problème | Cause | Solution |
|---------|-------|-----|
| **Fenêtre vide sous Linux** | Paquets de développement `webkit2gtk` manquants | `sudo apt install libwebkit2gtk-4.1-dev` |
| **Autorisation refusée** à l'exécution | Commande/plugin non déclarés dans les capacités | Ajoutez l'identifiant de permission à `capabilities/*.json` |
| **`cargo build` échoue avec des erreurs de liaison** | MSVC/Windows SDK ou `build-essential` manquants sous Linux | Installez les outils de compilation de la plateforme |
| **La webview affiche d'anciens contenus** | Actifs de développement en cache | Rechargement complet ou redémarrage du serveur de développement ; `rm -rf target` si nécessaire |
| **Binaire encore volumineux** | Compilation debug ; `strip` non utilisé | Compilez avec `npm run tauri build` (release) et activez `strip` dans `Cargo.toml` |
| **Compilation mobile lente/échouée** | Incompatibilité de version du NDK | Utilisez la version du NDK recommandée par Tauri ; synchronisez Gradle |
| **`invoke` en JS renvoie `undefined`** | Nom de commande incorrect ou confusion entre snake_case et camelCase | Vérifiez le nom de la commande et utilisez le camelCase en JS (`myCommand` ↔ `my_command`) |

## Écosystème et ressources

- **Documentation officielle** : https://v2.tauri.app
- **GitHub** : https://github.com/tauri-apps/tauri
- **Registre des plugins** : https://v2.tauri.app/plugin/
- **Awesome Tauri** : https://github.com/tauri-apps/awesome-tauri
- **Communauté Discord** : active, utile et officielle

## Conclusion

Tauri représente l'alternative moderne la plus convaincante à Electron : il produit des binaires considérablement plus petits, utilise moins de mémoire, applique un modèle de sécurité strict et — avec Tauri 2.x — couvre le desktop **et** le mobile à partir d'une base de code unique. La contrepartie est une véritable courbe d'apprentissage en Rust et l'incohérence inhérente des webviews système selon les plateformes.

Pour les équipes déjà à l'aise avec les frontends web qui souhaitent des performances natives, une taille de distribution réduite et une architecture où la sécurité est prioritaire, Tauri est un choix prêt pour la production qui associe la fiabilité de Rust à la flexibilité de la plateforme web.