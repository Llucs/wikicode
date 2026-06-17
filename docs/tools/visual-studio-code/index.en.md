---
title: Visual Studio Code
description: A lightweight yet powerful source code editor developed by Microsoft that serves as an integrated development tool.
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

## What is VS Code?

Visual Studio Code (commonly referred to as VS Code) is a free, open‑source source code editor developed by Microsoft. Built on the Electron framework, it runs on Windows, macOS, and Linux. VS Code combines the speed and simplicity of a lightweight editor with the advanced capabilities of an integrated development environment (IDE) through a rich extension architecture.

## Why VS Code?

- **Performance**: Starts quickly and stays responsive even with large projects.
- **Extensibility**: Thousands of extensions add languages, themes, debuggers, and workflow tools.
- **Cross‑platform**: Same experience on all major operating systems.
- **Integrated tooling**: Git control, terminal, debugging – all within the editor.
- **Intelligent editing**: IntelliSense provides context‑aware completions, parameter info, and documentation.
- **Built‑in support for modern workflows**: Docker, remote development, Jupyter notebooks, and more.

## Installation

### Download Installer
The easiest way is to download the installer from the [official website](https://code.visualstudio.com).

| Platform | Installer type |
|----------|----------------|
| Windows  | `.exe` (user or system) |
| macOS    | `.dmg` (drag to Applications) |
| Linux    | `.deb` (Debian/Ubuntu) or `.rpm` (Fedora/RHEL) |

### Package Managers

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

### Portable Mode
Create a `data` folder in the same directory as the VS Code executable. The editor will store all configuration, extensions, and user data inside that folder, making it fully portable.

### Insiders Build
For early access to features and daily builds, install [VS Code Insiders](https://code.visualstudio.com/insiders). It can be installed side‑by‑side with the stable release.

## Basic Usage

### Open a Project
Launch VS Code and use **File → Open Folder** (or `Ctrl+K Ctrl+O` / `Cmd+K Cmd+O`) to open your project directory.

### Command Palette
The command palette gives access to every action in VS Code.

```text
Ctrl+Shift+P   (Windows/Linux)
Cmd+Shift+P    (macOS)
```

Common commands: `>Format Document`, `>Preferences: Open Settings`, `>Extensions: Install Extensions`.

### Editing Files
- Syntax highlighting is automatic based on file extension.
- **Multi‑cursor**: `Alt+Click` (Windows/Linux) or `Option+Click` (macOS) to add cursors.
- **Bracket matching**: Move cursor inside brackets and the matching pair is highlighted.
- **IntelliSense**: Trigger manually with `Ctrl+Space`.

### Version Control
Open the Source Control view (`Ctrl+Shift+G` on Windows/Linux, `Cmd+Shift+G` on macOS) to see changes, stage files, commit, and push/pull. Use the built‑in terminal for more complex operations.

### Integrated Terminal
Launch the terminal with `` Ctrl+` `` (backtick). The terminal uses your system shell (PowerShell, bash, zsh, etc.) by default.

### Extensions
Open the Extensions view with `Ctrl+Shift+X`. Search for any extension (e.g., “Python”, “Prettier”, “Docker”) and install with one click.

### Debugging
Set breakpoints by clicking the gutter (line number area) or pressing `F9`. Press `F5` to start debugging with the currently active configuration. Create a `launch.json` file to configure debug settings for your project.

## Key Features with Command Examples

### IntelliSense
VS Code provides smart completions based on language services, variable types, and function definitions.

```javascript
// Example: Typing "console." then using Ctrl+Space shows methods like log, warn, error
console.log("Hello, VS Code!");
```

**Trigger IntelliSense manually**: `Ctrl+Space` (Windows/Linux) or `Cmd+Space` (macOS).

**Parameter hints**: When calling a function, VS Code shows the expected parameters.

### Integrated Debugging
Full debugging support with launch configurations.

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

**Key debugging commands:**
| Action | Keys |
|--------|------|
| Start/Continue | `F5` |
| Step Over | `F10` |
| Step Into | `F11` |
| Step Out | `Shift+F11` |
| Toggle Breakpoint | `F9` |

### Built‑in Git
Visual source control with staging, committing, branching, and more.

**Command Palette equivalents:**
- `>Git: Commit` – commit staged changes.
- `>Git: Create Branch` – create a new branch.
- `>Git: Clone` – clone a remote repository.
- `>Git: Pull` / `Git: Push` – synchronise changes.

### Extensions Marketplace
Install extensions to add languages, linters, themes, snippets, and debuggers.

**Example: Install the Python extension**
1. Open Extensions view (`Ctrl+Shift+X`).
2. Search for “Python” (by Microsoft).
3. Click **Install**.

**Popular extensions:**
- Python
- Prettier – Code formatter
- ESLint
- Docker
- Live Server
- GitLens
- Jupyter

### Integrated Terminal
Run shell commands without leaving VS Code.

```bash
# Example: inside the integrated terminal
npm install && npm start
```

Open/close the terminal with `` Ctrl+` ``. Multiple terminals can be created (e.g., one for build, one for git).

### Remote Development
Connect to remote environments such as:
- **WSL** (Windows Subsystem for Linux)
- **SSH** remote machines
- **Dev Containers** (Docker)
- **GitHub Codespaces**

**Command Palette examples:**
- `>Remote‑SSH: Connect to Host…`
- `>Dev Containers: Reopen in Container`

No need to leave the editor—your entire development environment is accessed locally.

## Additional Tips

### Settings Sync
Sign in with a Microsoft or GitHub account and your settings, keybindings, and extensions sync across machines.

**Command Palette**: `>Turn on Settings Sync…`

### Snippets
Create custom code snippets for repetitive patterns.

**File → Preferences → Configure User Snippets** → choose a language.

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

### Multi‑cursor Editing
- `Alt+Click` – add cursor.
- `Ctrl+Alt+Up/Down` – insert cursor above/below.
- `Ctrl+D` – select next occurrence of the current selection.

### Zen Mode
Focus on code without distractions: `Ctrl+K Z` (Windows/Linux) or `Cmd+K Z` (macOS). Toggle with `Esc Esc`.

## Conclusion

Visual Studio Code is a versatile editor that balances speed, power, and customisation. By mastering its core features—IntelliSense, debugging, Git integration, the terminal, and the extensions ecosystem—you can streamline your development workflow across any language or platform.

For deeper exploration, refer to the [official VS Code documentation](https://code.visualstudio.com/docs).