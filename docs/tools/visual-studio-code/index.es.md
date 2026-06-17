---
title: Visual Studio Code
description: Un editor de código fuente ligero pero potente desarrollado por Microsoft que sirve como herramienta de desarrollo integrada.
created: 2026-06-14
tags:
  - editor
  - development
  - microsoft
  - open-source
status: draft
ecosystem: editors
---

# Visual Studio Code

## ¿Qué es VS Code?

Visual Studio Code (comúnmente conocido como VS Code) es un editor de código fuente gratuito y de código abierto desarrollado por Microsoft. Construido sobre el framework Electron, se ejecuta en Windows, macOS y Linux. VS Code combina la velocidad y simplicidad de un editor ligero con las capacidades avanzadas de un entorno de desarrollo integrado (IDE) a través de una rica arquitectura de extensiones.

## ¿Por qué VS Code?

- **Rendimiento**: Se inicia rápidamente y se mantiene receptivo incluso con proyectos grandes.
- **Extensibilidad**: Miles de extensiones añaden lenguajes, temas, depuradores y herramientas de flujo de trabajo.
- **Multiplataforma**: Misma experiencia en todos los sistemas operativos principales.
- **Herramientas integradas**: Control de Git, terminal, depuración – todo dentro del editor.
- **Edición inteligente**: IntelliSense proporciona finalizaciones contextuales, información de parámetros y documentación.
- **Soporte integrado para flujos de trabajo modernos**: Docker, desarrollo remoto, cuadernos Jupyter y más.

## Instalación

### Descarga del instalador
La forma más sencilla es descargar el instalador desde el [sitio web oficial](https://code.visualstudio.com).

| Plataforma | Tipo de instalador |
|----------|----------------|
| Windows  | `.exe` (usuario o sistema) |
| macOS    | `.dmg` (arrastrar a Aplicaciones) |
| Linux    | `.deb` (Debian/Ubuntu) o `.rpm` (Fedora/RHEL) |

### Gestores de paquetes

**macOS (Homebrew)**
```bash
brew install --cask visual-studio-code
```

**Linux (Snap)**
```bash
snap install code --classic
```

**Windows (winget)**
```bash
winget install Microsoft.VisualStudioCode
```

### Modo portátil
Cree una carpeta `data` en el mismo directorio que el ejecutable de VS Code. El editor almacenará toda la configuración, extensiones y datos de usuario dentro de esa carpeta, haciéndolo completamente portátil.

### Compilación Insiders
Para acceso temprano a funciones y compilaciones diarias, instale [VS Code Insiders](https://code.visualstudio.com/insiders). Se puede instalar en paralelo con la versión estable.

## Uso básico

### Abrir un proyecto
Lance VS Code y use **Archivo → Abrir carpeta** (o `Ctrl+K Ctrl+O` / `Cmd+K Cmd+O`) para abrir su directorio de proyecto.

### Paleta de comandos
La paleta de comandos da acceso a todas las acciones en VS Code.

```text
Ctrl+Shift+P   (Windows/Linux)
Cmd+Shift+P    (macOS)
```

Comandos comunes: `>Format Document`, `>Preferences: Open Settings`, `>Extensions: Install Extensions`.

### Edición de archivos
- El resaltado de sintaxis es automático según la extensión del archivo.
- **Multicursor**: `Alt+Click` (Windows/Linux) o `Option+Click` (macOS) para agregar cursores.
- **Emparejamiento de corchetes**: Mueva el cursor dentro de los corchetes y el par coincidente se resaltará.
- **IntelliSense**: Se activa manualmente con `Ctrl+Space`.

### Control de versiones
Abra la vista de Control de código fuente (`Ctrl+Shift+G` en Windows/Linux, `Cmd+Shift+G` en macOS) para ver cambios, preparar archivos, confirmar y realizar push/pull. Use la terminal integrada para operaciones más complejas.

### Terminal integrada
Lance la terminal con `` Ctrl+` `` (acento grave). La terminal usa su shell del sistema (PowerShell, bash, zsh, etc.) de forma predeterminada.

### Extensiones
Abra la vista de Extensiones con `Ctrl+Shift+X`. Busque cualquier extensión (por ejemplo, “Python”, “Prettier”, “Docker”) e instálela con un clic.

### Depuración
Establezca puntos de interrupción haciendo clic en el margen (área de números de línea) o presionando `F9`. Presione `F5` para iniciar la depuración con la configuración activa actualmente. Cree un archivo `launch.json` para configurar los ajustes de depuración de su proyecto.

## Funciones clave con ejemplos de comandos

### IntelliSense
VS Code proporciona finalizaciones inteligentes basadas en servicios de lenguaje, tipos de variables y definiciones de funciones.

```javascript
// Example: Typing "console." then using Ctrl+Space shows methods like log, warn, error
console.log("Hello, VS Code!");
```

**Activar IntelliSense manualmente**: `Ctrl+Space` (Windows/Linux) o `Cmd+Space` (macOS).

**Sugerencias de parámetros**: Al llamar a una función, VS Code muestra los parámetros esperados.

### Depuración integrada
Soporte completo de depuración con configuraciones de lanzamiento.

**launch.json example for Node.js:**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "node",
            "request": "launch",
            "name": "Launch Program",
            "skipFiles": ["<node_internals>/**"],
            "program": "${workspaceFolder}/app.js"
        }
    ]
}
```

**Comandos clave de depuración:**
| Acción | Teclas |
|--------|------|
| Iniciar/Continuar | `F5` |
| Paso por encima | `F10` |
| Paso a paso por instrucciones | `F11` |
| Salir de la función | `Shift+F11` |
| Alternar punto de interrupción | `F9` |

### Git integrado
Control de código fuente visual con preparación, confirmación, ramificación y más.

**Equivalentes en la paleta de comandos:**
- `>Git: Commit` – confirmar cambios preparados.
- `>Git: Create Branch` – crear una nueva rama.
- `>Git: Clone` – clonar un repositorio remoto.
- `>Git: Pull` / `Git: Push` – sincronizar cambios.

### Marketplace de extensiones
Instale extensiones para agregar lenguajes, linters, temas, fragmentos y depuradores.

**Ejemplo: Instalar la extensión de Python**
1. Abra la vista de Extensiones (`Ctrl+Shift+X`).
2. Busque “Python” (de Microsoft).
3. Haga clic en **Instalar**.

**Extensiones populares:**
- Python
- Prettier
- ESLint
- Docker
- Live Server
- GitLens
- Jupyter

### Terminal integrada
Ejecute comandos del shell sin salir de VS Code.

```bash
# Example: inside the integrated terminal
npm install && npm start
```

Abra/cierre la terminal con `` Ctrl+` ``. Se pueden crear múltiples terminales (por ejemplo, una para compilación, otra para git).

### Desarrollo remoto
Conéctese a entornos remotos como:
- **WSL** (Subsistema de Windows para Linux)
- **SSH** máquinas remotas
- **Dev Containers** (Docker)
- **GitHub Codespaces**

**Ejemplos en la paleta de comandos:**
- `>Remote‑SSH: Connect to Host…`
- `>Dev Containers: Reopen in Container`

No es necesario salir del editor: todo su entorno de desarrollo se accede localmente.

## Consejos adicionales

### Sincronización de configuración
Inicie sesión con una cuenta de Microsoft o GitHub y sus ajustes, combinaciones de teclas y extensiones se sincronizarán entre máquinas.

**Paleta de comandos**: `>Turn on Settings Sync…`

### Fragmentos
Cree fragmentos de código personalizados para patrones repetitivos.

**Archivo → Preferencias → Configurar fragmentos de usuario** → elija un idioma.

```json
// Example JavaScript snippet (in javascript.json)
{
    "Arrow Function": {
        "prefix": "arr",
        "body": ["const ${1:name} = (${2:params}) => {", "\t${3:body}", "};"],
        "description": "Create an arrow function"
    }
}
```

### Edición multicursor
- `Alt+Click` – agregar cursor.
- `Ctrl+Alt+Up/Down` – insertar cursor arriba/abajo.
- `Ctrl+D` – seleccionar la siguiente ocurrencia de la selección actual.

### Modo Zen
Concéntrese en el código sin distracciones: `Ctrl+K Z` (Windows/Linux) o `Cmd+K Z` (macOS). Alterne con `Esc Esc`.

## Conclusión

Visual Studio Code es un editor versátil que equilibra velocidad, potencia y personalización. Al dominar sus funciones principales (IntelliSense, depuración, integración de Git, la terminal y el ecosistema de extensiones), puede optimizar su flujo de trabajo de desarrollo en cualquier lenguaje o plataforma.

Para una exploración más profunda, consulte la [documentación oficial de VS Code](https://code.visualstudio.com/docs).