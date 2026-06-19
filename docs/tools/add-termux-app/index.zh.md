---
title: "Termux：适用于Android的终端模拟器和Linux环境"
description: "关于Termux的全面指南，这是一款适用于Android设备的强大开源终端模拟器和Linux环境，涵盖安装、软件包管理、高级用法和开发者工作流程。"
created: 2026-06-19
tags:
  - android
  - terminal
  - linux
  - development
  - tools
status: draft
---

# Termux：适用于Android的终端模拟器和Linux环境

## 什么是Termux？

Termux 是一款适用于 Android 的 **开源终端模拟器和 Linux 环境**。它完全在用户空间中运行，**无需 root 权限**，并提供了一个丰富的、基于 Debian/Ubuntu 的软件包仓库。使用 Termux，你可以在 Android 设备上体验完整的 Linux 命令行——安装编译器、解释器、文本编辑器、网络工具等等。它利用 Android 内核的 Linux 系统调用来创建接近原生的环境。

### 为什么使用 Termux？

- **便携开发环境** – 在手机上直接编写和运行 Python 脚本、编译 C 程序、管理 Git 仓库或使用 REPL。
- **移动服务器管理** – SSH 远程登录服务器，检查网络诊断（ping、traceroute、nmap），并使用 rsync 同步文件。
- **学习与教育** – 无需完整 PC 即可练习 Linux 命令、shell 脚本和网络概念。
- **自动化与集成** – 结合 Android 自动化应用（Tasker）或使用 Termux:API 与手机硬件（摄像头、传感器、剪贴板）交互。
- **完整的 Linux 发行版** – 使用 proot-distro 在 Termux 环境中安装 Ubuntu、Debian、Arch 或 Fedora，以执行几乎任何 Linux 任务。

---

## 主要特性

| 特性 | 描述 |
|---------|-------------|
| **终端模拟器** | 功能齐全，支持触摸友好的手势控制，从数字行向左滑动可显示额外的功能键（Tab、Ctrl、Alt、Esc）。 |
| **软件包管理器** | `pkg`（底层使用 `apt`）提供 Termux 仓库中的数千个软件包。 |
| **多会话管理** | 滑动抽屉管理多个独立的终端会话，每个会话独立登录。 |
| **SSH 客户端与服务器** | 使用 `ssh` 连接到远程服务器，或启动服务器（`sshd`）以从电脑访问设备。 |
| **Proot 发行版支持** | 使用 `proot-distro` 运行完整的 Linux 发行版（Ubuntu、Debian、Arch、Fedora）。 |
| **API 集成** | 配套的 *Termux:API* 应用让脚本可以访问 Android 传感器的、剪贴板、TTS、摄像头、通知等。 |
| **存储访问** | 通过 `termux-setup-storage` 挂载共享的 Android 存储（内部存储/SD 卡）。 |

---

## 安装

### 1. 获取 Termux

> **重要提示**：**Google Play Store 版本已废弃**（停留在 API 28）。请始终从 **F-Droid** 安装，以获得最新软件包和对现代 Android（10+）的完全兼容。

- **F-Droid 客户端**：在 F-Droid 应用中搜索 "Termux"，或直接从 [F-Droid](https://f-droid.org/packages/com.termux/) 下载 APK。
- **直接 APK**：[F-Droid APK](https://f-droid.org/repo/com.termux_*.apk)（始终为最新版本）。

### 2. 配套应用（可选但推荐）

| 应用 | 用途 |
|-----|---------|
| [Termux:API](https://f-droid.org/packages/com.termux.api/) | 从脚本访问 Android 硬件（传感器、摄像头、剪贴板等）。 |
| [Termux:Float](https://f-droid.org/packages/com.termux.float/) | 在浮动窗口中运行 Termux（悬浮窗）。 |
| [Termux:Styling](https://f-droid.org/packages/com.termux.styling/) | 终端的配色方案和适配 Powerline 的字体。 |
| [Termux:Tasker](https://f-droid.org/packages/com.termux.tasker/) | 从 Tasker 及兼容的自动化应用中调用 Termux 可执行文件。 |
| [Termux:Widget](https://f-droid.org/packages/com.termux.widget/) | 从主屏幕启动小型脚本。 |

### 3. 初始设置

首次启动 Termux 后：

```bash
# Update the package repository and upgrade all packages
pkg update && pkg upgrade

# Grant storage access (needed to see your shared folders)
termux-setup-storage
```

现在你有了一个完全更新的 Termux 环境。共享的 Android 存储挂载在 `~/storage/shared`。

---

## 软件包管理

Termux 使用 **`pkg`** 命令作为 **`apt`** 的封装。所有命令对于 Debian/Ubuntu 用户来说都很熟悉。

### 常见的软件包操作

```bash
# Search for a package
pkg search python

# Install packages
pkg install python git vim openssh curl wget

# Remove a package
pkg remove python2

# List installed packages
pkg list-installed

# Upgrade all packages
pkg upgrade
```

### 可用软件包（示例）

| 类别 | 软件包 |
|----------|----------|
| **编程语言** | python, python3, nodejs, ruby, php, lua, golang, rust |
| **编译器/工具** | clang, make, gdb, cmake, gcc (via proot distro) |
| **编辑器** | vim, emacs, nano, neovim |
| **网络工具** | openssh, nmap, traceroute, netcat, rclone |
| **数据库** | mariadb, sqlite, postgresql (requires proot) |
| **实用工具** | git, curl, wget, rsync, htop, jq, ripgrep, fd |

> **注意**：由于 Termux 是用户空间环境，某些系统级软件包（例如 `systemd`、`glibc` 依赖）需要通过 `proot-distro` 使用完整的 Linux 发行版。

---

## 高级用法

### 1. SSH：客户端与服务器

**客户端** – 像在桌面上一样连接到远程机器：

```bash
pkg install openssh
ssh user@hostname
```

**服务器** – 让你的 Android 设备支持 SSH 访问（默认端口 8022）：

```bash
sshd
# or start it in the foreground with -d
sshd -d
```

从另一台机器连接：

```sh
ssh user@phone-ip -p 8022
```

> 第一次运行 `sshd` 时，Termux 会生成主机密钥，你可以为 termux 用户设置密码（默认用户为 `u0_aXYZ`）。使用 `passwd` 更改密码。

### 2. 使用 `proot-distro` 运行完整的 Linux 发行版

Proot 允许你在 Termux 内运行标准 Linux 发行版而无需 root 权限。`proot-distro` 软件包简化了此过程。

```bash
pkg install proot-distro

# List available distributions
proot-distro list

# Install Ubuntu (example)
proot-distro install ubuntu

# Login to the installed distribution
proot-distro login ubuntu

# Within the Ubuntu environment, you can use apt normally.
```

现在你拥有一个完整的 Ubuntu 环境（包括通过 `proot` 实现的类似 `systemd` 的服务管理器，尽管并非所有功能都完美运行）。你可以在其中安装 `gcc`、`postgresql` 或 `firefox` 等软件包（GUI 需要 X 服务器）。

### 3. 使用 Termux:API 配套应用

安装 `Termux:API` 后，你可以从命令行控制 Android 功能。

```bash
pkg install termux-api

# Get battery status
termux-battery-status

# Take a photo
termux-camera-photo output.jpg

# Get clipboard content
termux-clipboard-get

# Show a notification
termux-notification --title "Hello" --content "World"

# Check sensors
termux-sensor -s "Accelerometer" -n 5
```

### 4. 使用 Tasker 实现自动化

Termux:Tasker 允许你将 Termux 脚本作为 Tasker 动作运行。

1. 从 F-Droid 安装 **Termux:Tasker**。
2. 在 Tasker 中添加一个类型为 `System -> Send Intent` 的动作。
3. 动作：`com.termux.tasker.RUN_COMMAND`
4. 额外的键/值对：`command` = 你的脚本或命令（例如 `termux-battery-status`）。

你也可以将脚本放在 `~/.termux/tasker/` 中，并通过名称调用它们。

### 5. 会话管理与界面技巧

- **额外功能键**：从数字行（键盘顶部）向左滑动，可显示一行包含 Tab、Ctrl、Alt、Esc、功能键切换和向上箭头（用于向上滚动）的按键。你可以在 `~/.termux/termux.properties` 中自定义这些按键。
- **多会话**：点击屏幕左侧的抽屉图标（三条横线）可以列出、切换或创建新的终端会话。
- **文本选择**：在终端区域长按进入选择模式；复制/粘贴可通过溢出菜单操作。

---

## 使用场景

- **移动编程** – 使用 vim 和 gcc 编写和测试 Python 脚本、Node.js 应用或 C 程序。使用 git 进行版本控制。
- **服务器运维** – SSH 到生产服务器，运行 `tcpdump` 或 `nmap` 扫描，监控日志，并使用 `rsync` 传输文件。
- **数据分析** – 安装包含 pandas、numpy、scipy 和 Jupyter 的 Python（通过 `pkg install jupyter`），随时随地进行数据处理。
- **学习 Linux** – 无需单独 PC，即可尝试文件系统、shell 脚本和网络操作。
- **口袋计算器** – 使用 Python 作为交互式计算器：`python -c 'print(2**100)'` 或启动 REPL。

---

## 故障排除与提示

### 软件包安装失败，提示"404 Not Found"
软件源可能已过时。首先运行 `pkg update && pkg upgrade`。如果问题仍然存在，请检查你使用的是 F-Droid 版本（而非 Google Play 版本）。

### 存储访问被拒绝
运行 `termux-setup-storage` 并在提示时授予权限。如果在 Android 11+ 上失败，请在系统设置中确保 Termux 已启用"文件和媒体"权限。

### libc/glibc 依赖问题
某些软件包需要 glibc，但 Termux 使用 bionic（Android 的 libc）。对于这些软件包，请使用 proot-distro（Ubuntu、Debian）。

### 如何在 Android 10+ 上禁用全屏键盘
将以下行添加到 `~/.termux/termux.properties`：

```
fullscreen=false
```

然后使用 `termux-reload-settings` 重新加载。

### 终端中的剪贴板集成
使用 `termux-api` 中的 `termux-clipboard-get` 和 `termux-clipboard-set` 与系统剪贴板交互。

---

## 社区与资源

- **官方站点**：[termux.com](https://termux.com)（重定向至 GitHub）
- **GitHub 仓库**：[termux/termux-app](https://github.com/termux/termux-app)（主应用）
- **软件包仓库**：[termux/termux-packages](https://github.com/termux/termux-packages)
- **Wiki**：[Termux Wiki](https://wiki.termux.com)
- **F-Droid**：[F-Droid Termux](https://f-droid.org/packages/com.termux/)
- **Reddit**：[r/termux](https://reddit.com/r/termux)

---

Termux 将你的 Android 设备变成一个强大、便携的 Linux 工作站。凭借其广泛的软件包仓库、SSH 功能以及对标准 Linux 工作流程的兼容性，它成为开发者、系统管理员以及任何喜欢随身携带命令行的人不可或缺的工具。