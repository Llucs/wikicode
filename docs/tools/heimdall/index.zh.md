---
title: Heimdall - 三星固件刷写工具
description: 用于在三星移动设备上刷写固件（ROMs）的跨平台开源工具套件。
created: 2026-06-15
tags:
  - samsung
  - firmware
  - flashing
  - odin
  - android
  - open-source
status: draft
ecosystem: android
---

# Heimdall

## 什么是 Heimdall？

Heimdall 是一个跨平台的开源工具套件，用于将固件（官方 ROM、自定义 ROM、引导加载程序和恢复映像）刷写到三星 Android 设备上。它通过 USB 直接使用三星专有的 Odin 协议进行操作，为仅支持 Windows 的 Odin 工具提供了一个免费且适用于 Linux/macOS 的替代方案。该项目由 Benjamin Dobell 在 GitHub 上维护，自 2010 年代初以来一直在 Android 修改社区中广泛使用。

## 为什么使用 Heimdall？

- **跨平台** – 无需模拟即可在 Windows、Linux 和 macOS 上原生运行。
- **开源** – 完全可审计且由社区驱动。
- **绕过 Odin 限制** – 在 Odin 不可用或需要在非 Windows 系统上刷写时非常有用。
- **可脚本化** – 命令行界面支持自动化并集成到自定义工具链中。
- **分区级刷写** – 可单独刷写分区映像（例如 `BOOT`、`SYSTEM`、`RECOVERY`）以进行针对性修改。

## 安装

### Windows
从 [GitHub 发布页面](https://github.com/Benjamin-Dobell/Heimdall/releases) 下载最新安装程序。运行 `.exe` 并按照图形安装程序操作。

### Linux
可通过多种包管理器获取：
```bash
# Debian/Ubuntu
sudo apt install heimdall-flash

# Fedora
sudo dnf install heimdall

# Arch Linux
sudo pacman -S heimdall
```
或者使用 `cmake` 从源代码构建。

### macOS
通过 Homebrew 安装：
```bash
brew install heimdall
```
或者从发布页面下载 macOS 二进制文件。

## 使用方法

### 前提条件
1. 在三星设备上启用**开发者选项**和**USB 调试**。
2. 将设备启动至**下载模式**（通常：关机 → 按住音量下 + Home + 电源，然后按音量上确认）。
3. 通过 USB 将设备连接到计算机。

### 检测
验证设备是否被识别：
```bash
heimdall detect
```
如果成功，输出将显示设备型号和连接状态。

### 基本刷写
刷写分区映像：
```bash
heimdall flash --RECOVERY twrp-3.6.0-i9300.img
```
一次刷写多个分区：
```bash
heimdall flash --BOOT boot.img --SYSTEM system.img --VENDOR vendor.img
```

### 使用 PIT 文件
当需要完整固件恢复或分区表未知时，提供从设备或固件包中提取的 `.pit` 文件：
```bash
heimdall flash --pit /path/to/device.pit --SLT --no-reboot
```
`--SLT` 标志会刷写 PIT 中定义的所有分区，而 `--no-reboot` 会在完成后保持设备处于下载模式。

### 关闭连接
刷写完成后，关闭 USB 接口：
```bash
heimdall close-pc-screen
```

## 主要特性

- **跨平台**：Windows、Linux、macOS（原生二进制文件）。
- **开源**：基于 BSD 许可的代码库，社区活跃维护。
- **Odin 协议支持**：直接实现三星的低级刷写协议。
- **设备检测**：可靠的 USB 枚举和握手验证。
- **分区级刷写**：可单独刷写分区（boot、recovery、system 等）。
- **基于 PIT 的刷写**：使用分区信息表进行完整固件恢复。
- **内置 USB 驱动**：Windows 安装程序包含必要驱动；Linux/macOS 使用 libusb。
- **脚本支持**：CLI 标志适用于自动化流水线和 CI/CD 环境。

## 示例

### 检测已连接的设备
```bash
$ heimdall detect
Device detected: GT-I9300 (galaxys3)
```

### 刷写自定义恢复（TWRP）
```bash
heimdall flash --RECOVERY twrp-3.6.0_9-i9300.img --no-reboot
```

### 使用 PIT 文件刷写完整官方固件
```bash
heimdall flash --pit AP_I9300_4.3.pit --SLT --no-reboot
```

### 仅刷写 boot 分区
```bash
heimdall flash --BOOT boot.img
```

## 注意事项

- Heimdall 区别于 **Heimdall 应用程序面板**（linuxserver/Heimdall，一个基于 Web 的应用启动器）和 **Heimdall** 网络安全框架。
- 始终使用适合设备型号的固件，以避免变砖。
- 在 Windows 上确保 USB 驱动已安装 – 安装程序已包含它们。在 Linux 上，可能需要添加 udev 规则以便无需 root 即可访问设备。