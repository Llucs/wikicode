---
title: Team Win Recovery Project (TWRP)
description: TWRP 是一个用于 Android 的开源自定义恢复系统，支持通过触摸屏界面刷写自定义 ROM、进行全设备备份（NANDroid）以及执行系统修改。
created: 2026-06-17
tags:
  - android
  - recovery
  - custom-rom
  - backup
  - twrp
status: draft
---

# Team Win Recovery Project (TWRP)

TWRP（Team Win Recovery Project）是一个适用于 Android 设备的**开源自定义恢复映像**。它替代了原厂恢复分区，提供了一个功能丰富、触摸屏驱动的环境，用于安装第三方固件、创建完整的系统备份以及执行高级系统管理任务——所有这些都无需启动进入 Android。

## 为什么选择 TWRP？

原厂 Android 恢复系统仅限于恢复出厂设置和 OTA 更新。TWRP 为设备解锁了更多功能：

- **自定义 ROM 安装**（如 LineageOS、Pixel Experience 等）
- **完整的系统备份与恢复**（NANDroid）——在进行危险修改前必不可少。
- **Root 设备**（刷写 Magisk 或 SuperSU）。
- **分区管理**（擦除、格式化、调整大小）。
- **加密处理**（在特定条件下解密 userdata）。
- **ADB sideload 与 MTP**，用于传输文件或在没有存储空间的情况下刷机。

TWRP 是 Android 爱好者和开发者的事实标准，凭借其直观的界面和活跃的社区支持，已取代了 ClockworkMod (CWM) 等早期恢复系统。

## 主要特性

- **触控图形界面** – 支持全触摸，带有屏幕键盘、文件管理器和终端模拟器。
- **NANDroid 备份** – 克隆整个分区（Boot、System、Data、EFS/IMEI）到 `/sdcard/TWRP/BACKUPS/`。
- **ZIP 刷写** – 安装自定义固件包（ROM、内核、模块、GApps、Magisk）。
- **高级擦除** – 擦除单个分区，“Format Data”可移除加密。
- **文件管理器** – 浏览和修改设备文件系统上的文件。
- **ADB Sideload** – 通过 USB 从电脑刷写 ZIP 文件。
- **MTP 支持** – 在恢复模式下将设备存储作为可移动驱动器访问。
- **加密支持** – 可使用 PIN/密码/图案解密 userdata（较旧的加密方式；现代设备的 FBE 通常不支持）。
- **主题支持** – 通过 `.twres` 主题可自定义 UI。
- **截屏** – 在恢复模式下捕获屏幕。

## 历史

由 *Dees_Troy* 于 2011 年左右创建，TWRP 凭借其专有的触摸屏界面迅速成为最流行的自定义恢复系统。它经历了从 Holo 主题到 Material Design 界面（3.0+ 版本）的演变。如今由核心团队维护，并在 [twrp.me](https://twrp.me) 上支持数百种官方列出的设备。

## 安装

> **前提条件：**
> - 已解锁的引导加载程序（大多数设备需要）。
> - 电脑上已安装 ADB 和 Fastboot 工具。
> - 适用于您确切设备型号的正确 TWRP 映像（在 twrp.me 上查看代号）。

### 通用 Fastboot 方法（大多数设备）

1. **重启到 bootloader：**
   ```bash
   adb reboot bootloader
   ```
2. **刷写恢复映像：**
   ```bash
   fastboot flash recovery twrp-<version>.img
   ```
3. **立即启动到恢复模式**（在系统启动之前，否则可能覆盖 TWRP）：
   ```bash
   fastboot reboot recovery
   # 或使用硬件按键组合（音量下 + 电源等）
   ```

### 基于槽位的设备（A/B 分区 – 例如 Pixel、OnePlus）

由于系统可能在下次启动时自动替换恢复分区，请使用临时启动方法：

1. **临时启动 TWRP 映像：**
   ```bash
   fastboot boot twrp-<version>.img
   ```
2. **在 TWRP 中，进入** *高级 → Install Recovery Ramdisk*。
   - 这会将 TWRP 刷写到非活动槽位，并防止被覆盖。

### 三星设备（通过 Odin）

1. 下载 `.tar` 格式的 TWRP 文件（通常名为 `twrp-<version>-<device>.tar`）。
2. 打开 Odin，将文件放入 **AP** 槽位。
3. 在 Odin 选项中取消勾选 **Auto-Reboot**。
4. 刷写，然后立即使用按键组合（音量上 + Home + 电源）重启到恢复模式，以防止原厂恢复被恢复。

### 从已 Root 的设备（使用官方 TWRP 应用）

1. 从 Play 商店或 twrp.me 安装 **Official TWRP App**。
2. 授予 root 权限。
3. 选择您的设备并刷写最新映像。

### 从终端（已 Root）

```bash
su
dd if=/sdcard/twrp.img of=/dev/block/bootdevice/by-name/recovery
```

将路径替换为您的恢复分区位置（因设备而异 – 可使用 `parted` 或 `ls /dev/block/platform/...` 查找）。

## 基本使用流程

### 进入恢复模式
- 使用硬件按键组合（因制造商而异，通常为 **音量下 + 电源**）。
- 或从 Android（如果已 root/引导加载程序已解锁）：`adb reboot recovery`。

### 擦除分区

- **恢复出厂设置**（擦除 data/cache）——安装新 ROM 前必须执行。
  - *Wipe → Swipe to Factory Reset*
- **Format Data** – 移除加密并擦除内部存储。
  - *Wipe → Format Data → 输入“yes”*。
- **Advanced Wipe** – 选择要擦除的单个分区。

### 安装 ZIP（ROM、GApps、Magisk 等）

1. 点击 **Install**。
2. 导航到 `.zip` 文件（通常在 `/sdcard` 或外部 SD 卡上）。
3. 点击该文件；可选点击 **Add more Zips** 以排队多个文件。
4. **滑动确认刷写**。
5. *（可选）* 重启系统。

>  sideload 命令示例：
> ```bash
> adb sideload custom_rom.zip
> ```

### 备份（NANDroid）

1. 点击 **Backup**。
2. 选择分区：
   - **Boot**、**System**、**Data**（完整系统恢复的最低要求）。
   - **EFS**（存储 IMEI – 某些设备的关键分区）。
3. 滑动开始备份。
4. 备份存储在 `/sdcard/TWRP/BACKUPS/<device_serial>/`。

### 恢复备份

1. 点击 **Restore**。
2. 从列表中选择一个备份。
3. 勾选要恢复的分区。
4. 滑动确认。

### 文件管理器与终端

- **文件管理器**：*Advanced → File Manager* – 导航、删除、重命名、复制文件。
- **终端**：*Advanced → Terminal* – 以 root 身份运行命令。

## 示例命令（Fastboot 和 ADB）

```bash
# 从 Android 重启到 bootloader
adb reboot bootloader

# 刷写恢复映像
fastboot flash recovery twrp-3.7.1_12-0-beryllium.img

# 不刷写直接启动到恢复模式
fastboot boot twrp-3.7.1_12-0-beryllium.img

# 从电脑 sideload 文件
adb sideload LineageOS-21.0-20260617-UNOFFICIAL-beryllium.zip

# 在 MTP 模式下推送文件到设备
adb push magisk.zip /sdcard/
```

## 重要警告

- **设备专属映像** – 刷写不同型号的 TWRP 映像可能导致**硬砖**。务必验证代号（例如 Pocophone F1 的 `beryllium`）。
- **A/B 槽位混淆** – 在具有无缝更新的设备上，TWRP 必须安装到两个槽位。如果某个槽位缺少 TWRP，设备可能会恢复到原厂恢复。
- **加密问题** – 现代 Android 使用**基于文件的加密 (FBE)**。TWRP 通常无法解密 userdata。切换 ROM 或 TWRP 无法挂载 `/data` 时，用户通常需要 **Format Data**（会擦除内部存储）。
- **使用自定义恢复时的 OTA 更新** – 原厂 OTA 更新通常在使用 TWRP 时会失败。您必须：
  - 通过 TWRP 手动刷写 OTA ZIP。
  - 或者应用 OTA 前恢复到原厂恢复。
- **Play Integrity / 银行应用** – 解锁的引导加载程序（TWRP 所需）会破坏许多安全检测。使用 Magisk 获取 root 可以隐藏这一点，但会增加复杂性，且并非总是成功。
- **修改前备份** – 在刷写任何新 ROM 或危险 mod 之前，务必创建 NANDroid 备份。完整备份可以在几分钟内修复软砖。

## 故障排除

| 问题 | 解决方案 |
|--------|----------|
| TWRP 重启后丢失 | 使用 `fastboot boot` 然后执行“Install Recovery Ramdisk”（A/B 设备）。另一种方法：重新刷写并立即启动到恢复模式。 |
| 无法挂载 `/data` | 可能已加密。进入 *Wipe → Format Data* 并输入“yes”。**这会擦除所有内部存储。** |
| 刷写后设备停留在启动徽标 | 尝试擦除 Dalvik/ART 缓存和 Cache。如果仍然失败，恢复之前的备份。 |
| ADB Sideload 卡在“sending” | 确保拥有最新的 ADB 驱动程序。尝试更换 USB 线缆/端口。 |
| TWRP 无法启动（黑屏） | 映像可能损坏或不正确。从官方站点重新下载。 |

## 其他资源

- **官方网站和下载：** [https://twrp.me](https://twrp.me)
- **源代码：** [https://github.com/TeamWin/Team-Win-Recovery-Project](https://github.com/TeamWin/Team-Win-Recovery-Project)
- **XDA 论坛：** 搜索您设备的具体论坛帖子以获取 TWRP 版本和支持。
- **从源码编译 TWRP：** [https://github.com/TeamWin/Team-Win-Recovery-Project/blob/android-12.1/README.md](https://github.com/TeamWin/Team-Win-Recovery-Project/blob/android-12.1/README.md)

TWRP 是任何 Android 开发者或爱好者的强大工具。明智地使用它，并始终保留下备份。