---
title: Magisk - Android 无系统分区 Root 与模块管理器
description: Magisk 是一款流行的 Android Root 工具，提供无系统分区 Root 权限和模块支持，用于系统修改。
created: 2026-06-19
tags:
  - android
  - root
  - systemless
  - magisk
  - tool
status: draft
---

# Magisk – Android 无系统分区 Root 与模块管理器

## 什么是 Magisk？

Magisk 是由 **John Wu (topjohnwu)** 创建的一个开源软件套件，可实现**无系统分区 Root** 和对 Android 设备的深度定制。与修改不可变 `/system` 分区的传统 Root 方法不同，Magisk 通过修补设备的启动映像（或新设备上的 `init_boot` 分区）在启动时创建一个覆盖文件系统。这使得 Root 访问、启动脚本、SELinux 策略补丁和模块能够加载，**而无需永久修改系统文件**。

Magisk 最初于 2016 年发布，迅速成为 Android Root 的标准解决方案，取代了 SuperSU 等旧工具。它仍在积极维护中，并广泛用于基本的 Root 和高级设备修改。

---

## 为什么使用 Magisk？

| 优势 | 描述 |
|---------|-------------|
| **无系统分区修改** | OTA 更新得以保留，因为 `/system` 保持不变。 |
| **MagiskSU** | 纯开源 Root 权限管理（授予、提示、拒绝）。 |
| **模块系统** | 安装各种调整（音频模块、相机库、广告拦截、字体），无需重新分区。 |
| **Zygisk** | 通过 Zygote 向每个应用的进程注入代码——取代 MagiskHide。 |
| **DenyList** | 向特定应用（银行、流媒体）隐藏 Root、模块和解锁的 bootloader。 |
| **MagiskBoot** | 强大的工具，用于解包、修改和重新打包 Android 启动映像。 |
| **活跃的社区** | 数千个模块和丰富的文档可用。 |

Magisk 对于需要 Root 访问以使用高级备份工具、自动化（Tasker）、自定义系统调整或重新启用阻止 Root 设备中的应用功能来说至关重要。

---

## 安装指南

### 前提条件

- **已解锁的 bootloader**（因设备而异，通常需要 OEM 解锁）。
- **计算机上可用的 ADB 和 Fastboot**。
- **设备厂方镜像**或原厂 `boot.img`（可能还包括 `init_boot.img`）。
- **备份**所有重要数据。

### 第一步 – 提取启动映像

获取你设备的厂方镜像（例如，从 Google 的厂方镜像页面），然后提取启动映像。

```bash
# Example for a Pixel device
unzip [device]_[build].zip
cd [device]_[build]
unzip image-[device]-[build].zip
# boot.img is now in the current directory
```

对于运行 Android 13+ 的设备（例如 Pixel 6 系列），根分区是 `init_boot.img` 而不是 `boot.img`。

### 第二步 – 使用 Magisk 应用修补映像

1. 在你的设备上安装最新的 Magisk APK。
2. 打开 Magisk 应用，点击 **安装** → **选择并修补一个文件**。
3. 选择提取的 `boot.img`（或 `init_boot.img`）。
4. 该应用将修补映像并保存一个名为 `magisk_patched-XXXXX.img` 的新文件（通常在 `Download/` 中）。

### 第三步 – 刷入修补后的映像

将修补后的映像传输到你的计算机，然后将设备启动到 fastboot 模式。

```bash
adb pull /storage/emulated/0/Download/magisk_patched-XXXXX.img .
adb reboot bootloader
# For most devices:
fastboot flash boot magisk_patched-XXXXX.img
# For Pixel 6+ (init_boot partition):
fastboot flash init_boot magisk_patched-XXXXX.img
# Reboot:
fastboot reboot
```

### 第四步 – 验证安装

重启后，打开 Magisk 应用。**首页**应显示已安装的 Magisk 版本，并在 Magisk 状态旁显示“已安装”。

---

## 基本用法

### Magisk 应用界面

- **超级用户标签**（盾牌图标）：列出所有已请求 Root 权限的应用。点击条目可更改其权限状态（授予 / 提示 / 拒绝）。
- **模块标签**（拼图图标）：显示已安装的模块。点击 **+** 按钮可从设备上存储的 `.zip` 文件安装新模块。使用开关启用/禁用模块（大多数需要重启）。
- **设置标签**（齿轮图标）：
  - **Zygisk**：启用或禁用 Zygisk（需要重启）。
  - **DenyList**：配置 Magisk 应对哪些应用隐藏（需要 Zygisk 并重启）。
  - **更新通道**：为应用和 Magisk 更新选择稳定版、Beta 版或 Canary 版。
  - **自动响应**：设置默认 Root 权限行为。

### 模块管理

模块以标准 ZIP 归档文件形式安装。它们可以包含简单的脚本、二进制文件或完整的系统覆盖目录。

```bash
# Typical module ZIP structure (inside /data/adb/modules/<module_id>/)
module.prop          # Metadata (id, name, version, author)
system/              # Files to overlay on /system
post-fs-data.sh      # Script run early in boot
service.sh           # Script run later in boot
```

要手动安装模块：

1. 将模块 `.zip` 下载到你的设备。
2. 打开 Magisk 应用 → 模块标签 → **从存储安装**。
3. 选择文件，确认，然后在提示时**重启**。

### 卸载 Magisk

Magisk 应用提供了直接完全移除 Root 的方法：

1. 打开 Magisk 应用。
2. 点击首页底部的**卸载 Magisk**。
3. 确认 – 应用将恢复原始的未修补启动映像并重启。

---

## 主要特性

### MagiskSU

完全替代 `su` 的工具，完全开源。它实现了带有授予/提示/拒绝选项的权限模型，并记录所有 Root 访问。MagiskSU 与所有需要 Root 的现有应用兼容。

### Magisk 模块

一种标准化的格式，用于分发系统修改而无需触碰系统分区。模块在启动时通过 Magisk 覆盖文件系统加载。在 XDA 等论坛和 Magisk 仓库中存在数千个模块。

### Zygisk

Zygisk 是 Magisk 对 Zygote 进程的代码注入实现。它可以在任何应用的进程内进行运行时修改。Zygisk 取代了旧的 MagiskHide 功能。

### DenyList

当 Zygisk 启用时，你可以配置一个 **DenyList**，包含 Magisk 对其隐藏自身（Root、模块、解锁的 bootloader）的应用。这是绕过银行、支付和流媒体应用使用的完整性检查的现代方法。

### MagiskBoot

MagiskBoot 是一个用于处理启动映像的低级工具。它可以解包、修改和重新打包它们，而无需完整的 Android 环境。它通常直接在计算机上使用，无需应用即可创建修补后的映像。

---

## 命令示例

### Flash 修补后的启动映像（fastboot）

```bash
fastboot flash boot magisk_patched-27000.img
fastboot reboot
```

### 为新设备刷入 init_boot

```bash
fastboot flash init_boot magisk_patched-27000.img
fastboot reboot
```

### 使用 MagiskBoot 解包启动映像

```bash
magiskboot unpack boot.img
# This creates: kernel, kernel_dtb, ramdisk.cpio, header, etc.
```

### 使用 MagiskBoot 重新打包修改后的启动映像

```bash
magiskboot repack boot.img
# Creates new-boot.img with your modifications.
```

### 验证启动映像头部

```bash
magiskboot info boot.img
```

### 使用 Magisk 修补启动映像（命令行）

```bash
magiskboot boot.img
# Creates patched_boot.img in the current directory.
```

### 向应用隐藏 Magisk（DenyList）

打开 Magisk 应用 → 设置 → **配置 DenyList** → 添加目标应用（例如，`com.google.android.gms` 对应 Google Play Services）。重启后，Magisk 将对那个应用不可见。

---

## 提示与注意事项

- **OTA 更新**仍然兼容，因为 Magisk 只修改启动分区。但是，OTA 之后你必须**重新刷入 Magisk** 到新的启动映像。
- **SafetyNet / Play Integrity** – 虽然 Magisk 本身不提供完整性绕过，但像 Zygisk-Assistant 或 Shamiko 模块可以帮助向 Google 的 attestation 检查隐藏 Root。
- **模块冲突** – 某些模块可能相互干扰；逐个禁用它们以隔离问题。
- **备份** – 始终保留原始原厂启动映像的副本。如果出现问题，你可以通过 fastboot 恢复它。
- **Magisk Canary** – 前沿通道有时包含不稳定特性。仅用于测试。

---

## 参考

- [Magisk GitHub 仓库](https://github.com/topjohnwu/Magisk)
- [官方 Magisk 文档（开发者指南）](https://topjohnwu.github.io/Magisk/)
- [Magisk 模块仓库（非官方）](https://www.androidacy.com/modules-repository/)
- [XDA Developers – Magisk 讨论与支持](https://forum.xda-developers.com/f/magisk.5903/)

---

*本文档是开发者 Wiki 的一部分。欢迎评论和改进。*