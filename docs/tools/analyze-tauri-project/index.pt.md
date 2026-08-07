---
title: "Tauri: Construindo Aplicativos Leves Multiplataforma com Rust e Frontends Web"
description: "Um guia de desenvolvimento abrangente para Tauri, o framework baseado em Rust para construir aplicativos para desktop e mobile, seguros e de tamanho mínimo, usando tecnologias web."
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

# Tauri: Construindo Aplicativos Leves Multiplataforma com Rust e Frontends Web

## Visão Geral

**Tauri** é um kit de ferramentas de código aberto para construir aplicativos desktop e mobile usando tecnologias de frontend web (HTML, CSS, JavaScript/TypeScript) com um **backend em Rust**. Diferente do Electron, que empacota um motor Chromium completo (~150+ MB), o Tauri aproveita a **webview nativa do sistema operacional** — WebView2 no Windows, WebKit no macOS e WebKitGTK no Linux. Isso resulta em binários drasticamente menores (frequentemente abaixo de 10 MB) e consumo de memória significativamente menor.

O Tauri 2.0, lançado em outubro de 2024, adiciona suporte oficial a **iOS e Android**, tornando-o um framework genuinamente multiplataforma. O núcleo é construído com Rust, e a CLI pode ser utilizada via npm, Cargo ou um binário independente.

## Por que Tauri?

A principal motivação para o Tauri é o inchaço e a superfície de segurança do Electron. O Tauri foi projetado como resposta a três pontos críticos:

| Característica | Electron | Tauri |
|---------|----------|-------|
| **Tamanho do pacote** | 150–250 MB por instalador | 3–15 MB por instalador |
| **Uso de memória** | 300–500 MB de consumo base | 50–150 MB de consumo base |
| **Segurança** | Exposição total do Chromium; código remoto possível | Permissões baseadas em capacidades; sem código remoto por padrão |
| **Backend** | Node.js (ou Python via bindings) | Rust (velocidade nativa, memory-safe) |
| **Frontend** | Qualquer framework web | Qualquer framework web |

Tauri é a escolha certa quando:
- Você quer um aplicativo que pareça nativo e abra instantaneamente.
- Você se preocupa com segurança e deseja controle rigoroso sobre o que seu frontend pode acessar.
- Você se sente confortável escrevendo (ou aprendendo) Rust para a lógica de backend.
- Você precisa de uma única base de código que atenda Windows, macOS, Linux, iOS e Android.

## Arquitetura

A arquitetura do Tauri é um híbrido entre um frontend web e um núcleo Rust, que se comunicam por uma ponte IPC segura:

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

**Pontos-chave da arquitetura:**

- **Nenhum runtime Node.js** é empacotado no aplicativo final. O frontend consiste em assets estáticos compilados no binário.
- **IPC** entre JS e Rust usa um protocolo de passagem de mensagens; o frontend *não pode* chamar APIs de sistema arbitrárias diretamente sem permissões explícitas.
- **Capacidades** definem o que seu frontend pode acessar (caminhos do sistema de arquivos, hosts HTTP, escopos de plugins) em tempo de build.

## Histórico e Linha do Tempo de Lançamento

- **2018** — Daniel Thompson-Yvetot cria a prova de conceito inicial.
- **19 de junho de 2022** — lançamento estável do **Tauri 1.0**.
- **2023** — A Tauri Foundation junta-se à Linux Foundation.
- **Outubro de 2024** — **Tauri 2.0** adiciona suporte a iOS/Android, um novo sistema de plugins e arquitetura unificada.

## Instalação

### Pré-requisitos

| Plataforma | Requisitos |
|----------|--------------|
| **Windows** | Runtime WebView2 (pré-instalado no Windows 11), Rust, ferramentas de build MSVC |
| **macOS** | Xcode Command Line Tools, Rust |
| **Linux** | `libwebkit2gtk-4.1-dev`, `build-essential`, `libssl-dev`, `libayatana-appindicator3-dev`, `librsvg2-dev`, Rust |

Comando único para Linux (Debian/Ubuntu):

```bash
sudo apt update
sudo apt install libwebkit2gtk-4.1-dev build-essential curl wget file libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev
```

Instale o Rust via [rustup](https://rustup.rs/):

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Crie um Novo Projeto

Use a ferramenta oficial de scaffolding (funciona com npm, pnpm, yarn, bun, cargo):

```bash
npm create tauri-app@latest
```

Serão solicitados:
1. Nome do projeto
2. Framework frontend (React, Vue, Svelte, Solid, Angular, Vanilla)
3. Linguagem de UI (TypeScript / JavaScript)
4. Gerenciador de pacotes

Em seguida:

```bash
cd my-app
npm install
npm run tauri dev
```

Isso inicia um servidor de desenvolvimento para hot-reload do seu frontend e compila o binário Rust. O primeiro build leva alguns minutos; os builds subsequentes são rápidos.

### Alternativas de CLI

```bash
# Global npm CLI
npm install -g @tauri-apps/cli

# Or via Cargo
cargo install tauri-cli
cargo tauri dev
```

## Estrutura do Projeto

Um projeto Tauri gerado tem esta estrutura:

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

O arquivo de configuração principal controla tudo, desde o identificador do aplicativo até as configurações de build:

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

## Conceitos Fundamentais

### 1. Comandos (Rust ⇄ JS IPC)

Comandos são funções Rust expostas ao frontend. Defina-os com `#[tauri::command]` e registre-os no builder.

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

**Lado JavaScript** (usando o pacote `@tauri-apps/api`):

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

**Nota sobre a nomenclatura de parâmetros:** o Tauri converte argumentos snake_case do Rust para camelCase em JS. Um parâmetro Rust chamado `user_name` é usado como `{ userName: "..." }`. Para manter o nome exato, use `rename_all = "snake_case"` no comando:

```rust
#[tauri::command(rename_all = "snake_case")]
fn my_command(user_name: &str) {}
```

### 2. Estado do Backend Rust

Compartilhe estado entre comandos usando `manage()`:

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

### 3. Capacidades e Permissões

Desde o Tauri 2.0, todo acesso IPC é controlado por um **sistema de capacidades**. Um arquivo de capacidade define quais janelas/webviews podem acessar quais comandos, plugins e escopos.

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

**Importante:** sem uma capacidade que conceda permissão, invocar esse comando falhará com um erro de permissão negada em tempo de execução. Essa é uma decisão de design deliberada para minimizar a superfície de ataque.

### 4. Eventos (Frontend ⇄ Backend Pub/Sub)

O Tauri fornece um sistema de eventos bidirecional.

**Do Rust para JS:**

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

**Do JS para Rust:**

```rust
use tauri::Listener;

app.listen("ui-event", |event| {
    println!("Received from UI: {:?}", event.payload());
});
```

### 5. Sistema de Plugins

A arquitetura de plugins do Tauri é um de seus pontos mais fortes. Os plugins oficiais cobrem necessidades comuns:

| Plugin | Finalidade |
|--------|---------|
| `tauri-plugin-sql` | SQLite/MySQL/PostgreSQL via Rust `sqlx` |
| `tauri-plugin-http` | Cliente HTTP com cabeçalhos personalizados e streaming |
| `tauri-plugin-shell` | Iniciar processos e gerenciar processos filhos |
| `tauri-plugin-dialog` | Diálogos nativos de abrir/salvar arquivos e caixas de mensagem |
| `tauri-plugin-fs` | Acesso ao sistema de arquivos com permissões de escopo |
| `tauri-plugin-notification` | Notificações nativas para desktop/mobile |
| `tauri-plugin-clipboard-manager` | Ler/escrever área de transferência |
| `tauri-plugin-store` | Armazenamento persistente chave-valor (JSON) |
| `tauri-plugin-autostart` | Iniciar o aplicativo no login do SO |
| `tauri-plugin-updater` | Atualizações automáticas assinadas |

**Exemplo: adicionando o plugin SQL**

```bash
npm install @tauri-apps/plugin-sql
cargo add tauri-plugin-sql --features sqlite
```

Registre no Rust:

```rust
use tauri_plugin_sql::{Builder as SqlBuilder};

tauri::Builder::default()
    .plugin(
        SqlBuilder::default()
            .add_migrations("sqlite:data.db", vec![/* migrations */])
            .build(),
    )
```

Use no frontend:

```javascript
import Database from "@tauri-apps/plugin-sql";

const db = await Database.load("sqlite:data.db");
const users = await db.select("SELECT * FROM users WHERE id = $1", [42]);
await db.execute("INSERT INTO users (name) VALUES ($1)", ["Alice"]);
```

Adicione as permissões correspondentes ao seu arquivo de capacidades:

```json
"permissions": ["sql:default", "sql:allow-select", "sql:allow-execute"]
```

### 6. Múltiplas Janelas e Bandeja do Sistema

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

Bandeja do sistema:

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

### 7. Sistema de Arquivos e Caminhos

Use o acesso ao sistema de arquivos com escopo por meio do plugin:

```javascript
import { readTextFile, writeTextFile, mkdir } from "@tauri-apps/plugin-fs";
import { appDataDir, join } from "@tauri-apps/api/path";

const dir = await appDataDir();
const filePath = await join(dir, "settings.json");

await mkdir(dir, { recursive: true });
await writeTextFile(filePath, JSON.stringify({ theme: "dark" }));
const content = await readTextFile(filePath);
```

Essas chamadas exigem `fs:allow-read-text-file`, `fs:allow-write-text-file` e entradas de escopo apropriadas no seu arquivo de capacidades.

## Compilando Aplicativos de Produção

```bash
npm run tauri build
```

Isso executa o `beforeBuildCommand`, compila o binário Rust em modo release e gera instaladores nativos:

- **Windows**: `.msi` (WiX) e `.exe` (NSIS)
- **macOS**: `.dmg` e pacote `.app`
- **Linux**: `.deb`, `.rpm` e AppImage
- **Mobile**: `apk`/`aab` para Android, `ipa` para iOS (requer Xcode + assinatura)

Definindo formatos específicos:

```bash
npm run tauri build -- --bundles msi
npm run tauri build -- --bundles appimage
```

### Assinatura de Código e Notarização

- **macOS**: Defina `appleDeveloperTeamId` no `tauri.conf.json` e execute com `--sign`.
- **Windows**: Forneça um certificado `.pfx` por meio de variáveis de ambiente (`TAURI_SIGNING_PRIVATE_KEY`).
- **Linux**: Não é necessário para a maioria das distribuições.

## Desenvolvimento Mobile (Tauri 2.0+)

O Tauri 2.0 suporta oficialmente iOS e Android. Pré-requisitos:

- **Android**: Android Studio, Android SDK/NDK, Java JDK 17
- **iOS**: macOS com Xcode 15+, CocoaPods

Adicione as plataformas mobile ao seu projeto:

```bash
npm run tauri android init
npm run tauri ios init
```

Execute em um dispositivo/emulador:

```bash
npm run tauri android dev
npm run tauri ios dev
```

Observações específicas para mobile:

- Use `tauri::mobile_entry_point` em `lib.rs` (o scaffold já o inclui).
- Os comandos Rust funcionam de forma idêntica no mobile; a webview é `WKWebView` no iOS e a WebView do Android.
- O ecossistema de plugins inclui plugins específicos para mobile (por exemplo, `tauri-plugin-nfc`, `tauri-plugin-barcode-scanner`, `tauri-plugin-geolocation`).
- O suporte a mobile amadurece continuamente; teste cedo e com frequência em dispositivos físicos.

## Boas Práticas

1. **Mantenha os comandos pequenos e síncronos quando possível** — Comandos assíncronos com computação pesada devem usar tarefas `tokio` para evitar bloquear a thread de IPC.
2. **Use o sistema de capacidades desde o início** — Mesmo para protótipos, defina permissões explícitas. Fica muito mais difícil adaptá-lo depois.
3. **Defina um CSP estrito** no `tauri.conf.json`:

   ```json
   "security": {
     "csp": "default-src 'self'; connect-src ipc: http://ipc.localhost; img-src 'self' data:; style-src 'self' 'unsafe-inline'"
   }
   ```

4. **Elimine chaves de API do frontend** — Qualquer coisa em JS é inspecionável. Coloque segredos no Rust.
5. **Use Rust para caminhos críticos de desempenho** — Ordenação, parsing, criptografia e processamento de arquivos são drasticamente mais rápidos em Rust.
6. **Prefira `tauri-plugin-store` para configurações** em vez de implementar E/S de arquivos manualmente.
7. **Lide com diferenças de webview** — Teste em todos os SOs alvo. Versões antigas do WebKitGTK no Linux e versões mais antigas do WebView2 no Windows podem se comportar de maneira diferente com CSS moderno.

## Armadilhas Comuns e Solução de Problemas

| Problema | Causa | Solução |
|---------|-------|-----|
| **Janela em branco no Linux** | Pacotes de desenvolvimento `webkit2gtk` ausentes | `sudo apt install libwebkit2gtk-4.1-dev` |
| **Permissão negada** em tempo de execução | Comando/plugin não declarado nas capacidades | Adicione o identificador de permissão em `capabilities/*.json` |
| **`cargo build` falha com erros de linker** | MSVC/Windows SDK ausente ou `build-essential` no Linux | Instale as ferramentas de build da plataforma |
| **Webview mostra conteúdo antigo** | Assets de desenvolvimento em cache | Atualização forçada ou reinicie o servidor de desenvolvimento; `rm -rf target` se necessário |
| **Binário ainda grande** | Build de debug; sem usar `strip` | Compile com `npm run tauri build` (release) e habilite `strip` no `Cargo.toml` |
| **Build mobile lento/com falha** | Versão do NDK incompatível | Use a versão do NDK recomendada pelo Tauri; sincronize o Gradle |
| **`invoke` JS retorna `undefined`** | Nome do comando incorreto ou confusão entre snake_case/camelCase | Confirme o nome do comando e use camelCase em JS (`myCommand` ↔ `my_command`) |

## Ecossistema e Recursos

- **Documentação oficial**: https://v2.tauri.app
- **GitHub**: https://github.com/tauri-apps/tauri
- **Registro de plugins**: https://v2.tauri.app/plugin/
- **Awesome Tauri**: https://github.com/tauri-apps/awesome-tauri
- **Comunidade no Discord**: Ativa, prestativa e oficial

## Conclusão

O Tauri representa a alternativa moderna mais atraente ao Electron: ele produz binários drasticamente menores, usa menos memória, impõe um modelo de segurança estrito e — com o Tauri 2.x — abrange desktop **e** mobile a partir de uma única base de código. O trade-off é uma curva de aprendizado real em Rust e a inconsistência inerente das webviews do sistema entre plataformas.

Para equipes já familiarizadas com frontends web que desejam desempenho nativo, tamanho de distribuição pequeno e uma arquitetura que prioriza a segurança, o Tauri é uma escolha pronta para produção que une a confiabilidade do Rust à flexibilidade da plataforma web.