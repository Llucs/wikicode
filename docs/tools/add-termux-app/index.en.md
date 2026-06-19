---
title: "Termux: Terminal Emulator and Linux Environment for Android"
description: "A comprehensive guide to Termux, the powerful open-source terminal emulator and Linux environment for Android devices, covering installation, package management, advanced usage, and developer workflows."
created: 2026-06-19
tags:
  - android
  - terminal
  - linux
  - development
  - tools
status: draft
---

# Termux: Terminal Emulator and Linux Environment for Android

## What is Termux?

Termux is an **open-source terminal emulator and Linux environment** for Android. It operates entirely in userspace, requiring **no root access**, and provides a rich, Debian/Ubuntu-derived package repository. With Termux, you can run a full Linux command-line experience on your Android device—install compilers, interpreters, text editors, networking tools, and more. It leverages the Android kernel’s Linux syscalls to create a near-native environment.

### Why Use Termux?

- **Portable Development Environment** – Write and run Python scripts, compile C programs, manage Git repositories, or use a REPL directly on your phone.
- **Server Administration on the Go** – SSH into remote servers, check network diagnostics (ping, traceroute, nmap), and sync files with rsync.
- **Learning & Education** – Practice Linux commands, shell scripting, and network concepts without needing a full PC.
- **Automation & Integration** – Combine with Android automation apps (Tasker) or use Termux:API to interact with phone hardware (camera, sensors, clipboard).
- **Full Linux Distros** – Install Ubuntu, Debian, Arch, or Fedora inside a termux environment using proot-distro for almost any Linux task.

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Terminal Emulator** | Full-featured with touch-friendly gesture controls, extra function keys (Tab, Ctrl, Alt, Esc) accessible by swiping left from the number row. |
| **Package Manager** | `pkg` (and underlying `apt`) with thousands of packages from the Termux repository. |
| **Multi-Session Management** | Slide out a drawer to manage separate terminal sessions, each independently logged in. |
| **SSH Client & Server** | Connect to remote servers with `ssh`, or start a server (`sshd`) to access your device from a computer. |
| **Proot Distro Support** | Run full Linux distributions (Ubuntu, Debian, Arch, Fedora) using `proot-distro`. |
| **API Integration** | The companion *Termux:API* app gives scripts access to Android sensors, clipboard, TTS, camera, notifications, and more. |
| **Storage Access** | Mount shared Android storage (internal/SD) via `termux-setup-storage`. |

---

## Installation

### 1. Get Termux

> **Important**: The **Google Play Store version is deprecated** (stuck at API 28). Always install from **F-Droid** for up-to-date packages and full compatibility with modern Android (10+).

- **F-Droid client**: Search for "Termux" in the F-Droid app or download the APK directly from [F-Droid](https://f-droid.org/packages/com.termux/).
- **Direct APK**: [F-Droid APK](https://f-droid.org/repo/com.termux_*.apk) (always the latest).

### 2. Companion Apps (Optional but Recommended)

| App | Purpose |
|-----|---------|
| [Termux:API](https://f-droid.org/packages/com.termux.api/) | Access Android hardware (sensors, camera, clipboard, etc.) from scripts. |
| [Termux:Float](https://f-droid.org/packages/com.termux.float/) | Run Termux in a floating window (overlay). |
| [Termux:Styling](https://f-droid.org/packages/com.termux.styling/) | Color schemes and powerline-ready fonts for the terminal. |
| [Termux:Tasker](https://f-droid.org/packages/com.termux.tasker/) | Call Termux executables from Tasker and compatible automation apps. |
| [Termux:Widget](https://f-droid.org/packages/com.termux.widget/) | Start small scriptlets from the home screen. |

### 3. Initial Setup

After launching Termux for the first time:

```bash
# Update the package repository and upgrade all packages
pkg update && pkg upgrade

# Grant storage access (needed to see your shared folders)
termux-setup-storage
```

Now you have a fully updated Termux environment. The shared Android storage is mounted at `~/storage/shared`.

---

## Package Management

Termux uses the **`pkg`** command as a wrapper around **`apt`**. All commands are familiar to Debian/Ubuntu users.

### Common Package Operations

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

### Available Packages (sampling)

| Category | Packages |
|----------|----------|
| **Languages** | python, python3, nodejs, ruby, php, lua, golang, rust |
| **Compilers/Tools** | clang, make, gdb, cmake, gcc (via proot distro) |
| **Editors** | vim, emacs, nano, neovim |
| **Networking** | openssh, nmap, traceroute, netcat, rclone |
| **Databases** | mariadb, sqlite, postgresql (requires proot) |
| **Utilities** | git, curl, wget, rsync, htop, jq, ripgrep, fd |

> **Note**: Because Termux is a user-space environment, some system-level packages (e.g., `systemd`, `glibc` dependencies) require a full Linux distro via `proot-distro`.

---

## Advanced Usage

### 1. SSH: Client and Server

**Client** – Connect to remote machines just like on desktop:

```bash
pkg install openssh
ssh user@hostname
```

**Server** – Make your Android device SSH-accessible (default port 8022):

```bash
sshd
# or start it in the foreground with -d
sshd -d
```

Connect from another machine:

```sh
ssh user@phone-ip -p 8022
```

> The first time you run `sshd`, Termux will generate host keys and you can set a password for the termux user (default user is `u0_aXYZ`). Use `passwd` to change it.

### 2. Running Full Linux Distributions with `proot-distro`

Proot lets you run a standard Linux distribution inside Termux without root. The `proot-distro` package simplifies this.

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

Now you have a full Ubuntu environment (including `systemd`-like service managers via `proot`, though not all features work perfectly). You can install packages like `gcc`, `postgresql`, or `firefox` (GUI needs X server) inside it.

### 3. Using the Termux:API Companion

With `Termux:API` installed, you can control Android features from the command line.

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

### 4. Automation with Tasker

Termux:Tasker allows you to run Termux scripts as Tasker actions.

1. Install **Termux:Tasker** from F-Droid.
2. In Tasker, add an action of type `System -> Send Intent`.
3. Action: `com.termux.tasker.RUN_COMMAND`
4. Extra key/value pairs: `command` = your script or command (e.g., `termux-battery-status`).

You can also place scripts in `~/.termux/tasker/` and call them by name.

### 5. Session Management & UI Tricks

- **Extra Keys**: Swipe left from the number row (at the top of the keyboard) to reveal a row with Tab, Ctrl, Alt, Esc, a Function key toggle, and an up arrow (to scroll up). You can customize these in `~/.termux/termux.properties`.
- **Multi-Session**: Tap the drawer icon (three horizontal lines) on the left side of the screen to list, switch, or create new terminal sessions.
- **Text Selection**: Long press in the terminal area to enter selection mode; copy/paste works with the overflow menu.

---

## Use Cases

- **Mobile Coding** – Write and test Python scripts, Node.js apps, or C programs with vim and gcc. Use git for version control.
- **Server Ops** – SSH to production servers, run `tcpdump` or `nmap` scans, monitor logs, and transfer files with `rsync`.
- **Data Analysis** – Install Python with pandas, numpy, scipy, and Jupyter (via `pkg install jupyter`) for on-the-go data crunching.
- **Learning Linux** – Experiment with the file system, shell scripting, and networking without a separate PC.
- **Pocket Calculator** – Use Python as an interactive calculator: `python -c 'print(2**100)'` or launch a REPL.

---

## Troubleshooting & Tips

### Package installation fails with "404 Not Found"
Repositories may be outdated. Run `pkg update && pkg upgrade` first. If the problem persists, check that you’re using the F-Droid version (not Google Play).

### Storage access denied
Run `termux-setup-storage` and grant the permission when prompted. If it fails on Android 11+, ensure Termux has the "Files and media" permission enabled in system settings.

### Problems with libc/glibc dependencies
Some packages expect glibc, but Termux uses bionic (Android’s libc). Use a proot-distro (Ubuntu, Debian) for those packages.

### How to disable full-screen keyboard on Android 10+
Add this line to `~/.termux/termux.properties`:
```
fullscreen=false
```
Then reload with `termux-reload-settings`.

### Clipboard integration with terminal
Use `termux-clipboard-get` and `termux-clipboard-set` from `termux-api` to interact with the system clipboard.

---

## Community & Resources

- **Official Site**: [termux.com](https://termux.com) (redirects to GitHub)
- **GitHub Repo**: [termux/termux-app](https://github.com/termux/termux-app) (main app)
- **Packages Repo**: [termux/termux-packages](https://github.com/termux/termux-packages)
- **Wiki**: [Termux Wiki](https://wiki.termux.com)
- **F-Droid**: [F-Droid Termux](https://f-droid.org/packages/com.termux/)
- **Reddit**: [r/termux](https://reddit.com/r/termux)

---

Termux turns your Android device into a powerful, portable Linux workstation. With its extensive package repository, SSH capabilities, and compatibility with standard Linux workflows, it’s an indispensable tool for developers, system administrators, and anyone who likes to keep the command line in their pocket.