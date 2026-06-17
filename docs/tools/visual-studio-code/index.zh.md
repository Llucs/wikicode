---
title: Visual Studio Code
description: 一款由微软开发的轻量级但功能强大的源代码编辑器，可作为集成开发工具使用。
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

## 什么是 VS Code？

Visual Studio Code（通常简称为 VS Code）是一款由微软开发的免费、开源的源代码编辑器。它基于 Electron 框架构建，可在 Windows、macOS 和 Linux 上运行。VS Code 通过丰富的扩展架构，将轻量级编辑器的速度与简洁性同集成开发环境（IDE）的高级功能相结合。

## 为什么选择 VS Code？

- **性能**：启动迅速，即使在大型项目中也能保持响应流畅。
- **可扩展性**：数千种扩展可添加语言、主题、调试器和工作流工具。
- **跨平台**：在所有主流操作系统上提供一致体验。
- **集成工具**：Git 控制、终端、调试——全部集成在编辑器中。
- **智能编辑**：IntelliSense 提供上下文感知的自动补全、参数信息和文档。
- **内置支持现代工作流**：Docker、远程开发、Jupyter notebook 等。

## 安装

### 下载安装程序

最简单的方法是从[官方网站](https://code.visualstudio.com)下载安装程序。

| 平台 | 安装程序类型 |
|----------|----------------|
| Windows  | `.exe`（用户或系统） |
| macOS    | `.dmg`（拖入应用程序文件夹） |
| Linux    | `.deb`（Debian/Ubuntu）或 `.rpm`（Fedora/RHEL） |

### 包管理器

**macOS（Homebrew）**
```bash
brew install --cask visual-studio-code
```

**Linux（Snap）**
```bash
snap install code --classic
```

**Windows（winget）**
```bash
winget install Microsoft.VisualStudioCode
```

### 便携模式

在 VS Code 可执行文件所在目录中创建一个 `data` 文件夹。编辑器将把所有配置、扩展和用户数据存储在该文件夹中，从而实现完全便携。

### Insiders 内部版本

要提前体验功能和每日构建版本，请安装 [VS Code Insiders](https://code.visualstudio.com/insiders)。它可以与稳定版并行安装。

## 基本使用

### 打开项目

启动 VS Code，使用 **文件 → 打开文件夹**（或 `Ctrl+K Ctrl+O` / `Cmd+K Cmd+O`）来打开项目目录。

### 命令面板

命令面板可以访问 VS Code 中的所有操作。

```text
Ctrl+Shift+P   (Windows/Linux)
Cmd+Shift+P    (macOS)
```

常用命令：`>Format Document`、`>Preferences: Open Settings`、`>Extensions: Install Extensions`。

### 编辑文件

- 语法高亮根据文件扩展名自动启用。
- **多光标**：`Alt+Click`（Windows/Linux）或 `Option+Click`（macOS）添加光标。
- **括号匹配**：将光标移到括号内，匹配的括号对会高亮显示。
- **IntelliSense**：使用 `Ctrl+Space` 手动触发。

### 版本控制

打开源代码管理视图（Windows/Linux 上使用 `Ctrl+Shift+G`，macOS 上使用 `Cmd+Shift+G`）以查看更改、暂存文件、提交以及推送/拉取。使用内置终端执行更复杂的操作。

### 集成终端

使用 `` Ctrl+` ``（反引号）启动终端。终端默认使用系统 Shell（PowerShell、bash、zsh 等）。

### 扩展

使用 `Ctrl+Shift+X` 打开扩展视图。搜索所需扩展（例如 "Python"、"Prettier"、"Docker"）并一键安装。

### 调试

通过单击装订线（行号区域）或按 `F9` 设置断点。按 `F5` 使用当前活动配置开始调试。创建 `launch.json` 文件为项目配置调试设置。

## 主要功能及命令示例

### IntelliSense

VS Code 根据语言服务、变量类型和函数定义提供智能补全。

```javascript
// Example: Typing "console." then using Ctrl+Space shows methods like log, warn, error
console.log("Hello, VS Code!");
```

**手动触发 IntelliSense**：`Ctrl+Space`（Windows/Linux）或 `Cmd+Space`（macOS）。

**参数提示**：调用函数时，VS Code 会显示期望的参数。

### 集成调试

完整的调试支持，包含启动配置。

**Node.js 的 launch.json 示例：**

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

**主要调试命令：**

| 操作 | 按键 |
|--------|------|
| 开始/继续 | `F5` |
| 单步跳过 | `F10` |
| 单步进入 | `F11` |
| 单步跳出 | `Shift+F11` |
| 切换断点 | `F9` |

### 内置 Git

可视化的源代码管理，支持暂存、提交、分支等操作。

**命令面板对应操作：**

- `>Git: Commit` — 提交暂存的更改。
- `>Git: Create Branch` — 创建新分支。
- `>Git: Clone` — 克隆远程仓库。
- `>Git: Pull` / `Git: Push` — 同步更改。

### 扩展市场

安装扩展以添加语言、代码检查工具、主题、代码片段和调试器等。

**示例：安装 Python 扩展**

1. 打开扩展视图（`Ctrl+Shift+X`）。
2. 搜索 "Python"（由 Microsoft 提供）。
3. 点击 **安装**。

**常用扩展：**

- Python
- Prettier – Code formatter
- ESLint
- Docker
- Live Server
- GitLens
- Jupyter

### 集成终端

无需离开 VS Code 即可运行 Shell 命令。

```bash
# Example: inside the integrated terminal
npm install && npm start
```

使用 `` Ctrl+` `` 打开/关闭终端。可以创建多个终端（例如一个用于构建，一个用于 Git）。

### 远程开发

连接到远程环境，例如：

- WSL（适用于 Linux 的 Windows 子系统）
- SSH 远程机器
- Dev Containers（Docker）
- GitHub Codespaces

**命令面板示例：**

- `>Remote‑SSH: Connect to Host…`
- `>Dev Containers: Reopen in Container`

无需离开编辑器——整个开发环境都可本地访问。

## 附加提示

### 设置同步

使用 Microsoft 或 GitHub 账户登录，即可在机器间同步设置、键绑定和扩展。

**命令面板**：`>Turn on Settings Sync…`

### 代码片段

为重复模式创建自定义代码片段。

**文件 → 首选项 → 配置用户代码片段** → 选择一种语言。

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

### 多光标编辑

- `Alt+Click` — 添加光标。
- `Ctrl+Alt+Up/Down` — 在上方/下方插入光标。
- `Ctrl+D` — 选择当前选择的下一个匹配项。

### 禅宗模式

排除干扰，专注代码：`Ctrl+K Z`（Windows/Linux）或 `Cmd+K Z`（macOS）。按 `Esc Esc` 切换。

## 总结

Visual Studio Code 是一个兼具速度、强大功能和可定制性的多功能编辑器。通过掌握其核心功能——IntelliSense、调试、Git 集成、终端以及扩展生态系统，您可以简化任何语言或平台上的开发工作流。

如需深入了解，请参阅[官方 VS Code 文档](https://code.visualstudio.com/docs)。