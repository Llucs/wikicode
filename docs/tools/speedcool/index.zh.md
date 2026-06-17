---
title: SpeedCool Magisk模块
description: 一款用于Android的Magisk模块，通过优化系统设置来提升性能、减少RAM占用并改善热管理。
created: 2026-06-15
tags:
  - android
  - magisk-module
  - performance-tuning
  - thermal-management
  - root
status: draft
ecosystem: android
---

# SpeedCool Magisk模块

**SpeedCool** 是一款开源、轻量级的Magisk模块，由 [Llucs](https://github.com/Llucs/SpeedCool-Magisk-Module) 创建。它会在启动时自动应用一套全面的内核和系统级调整，以提升任何已root的Android设备的性能、减少RAM占用并改进热管理。

与标准的臃肿软件清理器不同，SpeedCool 修改底层系统配置，从根源上消除卡顿和过热问题。

---

## 功能说明

SpeedCool 针对几个关键系统区域：

- **CPU Governor 与频率缩放：** 降低对要求苛刻的应用（例如游戏、模拟器）的唤醒延迟。
- **Low Memory Killer (LMK)：** 优先将当前活跃应用保留在内存中，同时激进地从后台缓存进程回收内存。
- **热引擎：** 修改热节流点，以在持续性能与热量产生之间取得平衡。
- **I/O调度器：** 将存储调度器切换为低延迟变体，以实现更快的应用加载。
- **网络栈：** 优化TCP拥塞控制，以获得更好的移动网络吞吐量。
- **GPU渲染：** 启用强制GPU渲染并优化GPU调控器。

---

## 为什么使用它？

- **更流畅的游戏体验：** 由于更好的CPU/GPU调控器调整和热节流控制，帧率更加稳定。
- **更快的多任务处理：** 得益于优化的LMK值，应用重新加载的频率降低。
- **更凉爽的运行：** 智能热配置文件防止SoC在重度使用期间达到临界温度。
- **一体化优化器：** 替换多个冲突的性能模块。
- **轻量级：** 模块通常小于1MB，且开销极小。

---

## 安装

### 先决条件

- Android设备，已解锁引导加载程序并获取root权限。
- 已安装 **Magisk**（v20.0+）。
- 建议使用自定义恢复（TWRP）作为备用。

### 步骤

1. **下载** 最新版 `SpeedCool-Magisk-Module.zip` 从 [GitHub发布页面](https://github.com/Llucs/SpeedCool-Magisk-Module/releases)。
2. 打开 **Magisk Manager** 应用。
3. 导航至 **模块** 选项卡。
4. 点击 **从存储安装**。
5. 选择下载的 `.zip` 文件。
6. 滑动确认安装。
7. 根据提示 **重启** 设备。

> **提示：** 如果遇到启动循环，请在启动时按住音量上键进入安全模式并禁用该模块，或者通过恢复模式手动删除 `/data/adb/modules/SpeedCool/` 目录来移除它。

---

## 使用与验证

SpeedCool 设计为完全在后台运行，无需用户界面。您可以使用终端命令来验证其运行状态。

### 检查激活状态

列出模块目录以确认安装：

```bash
su -c "ls -la /data/adb/modules/SpeedCool/"
```

如果成功挂载，该目录将包含模块文件（`system.prop`、`service.sh`、`module.prop`）。

### 检查已应用的系统属性

```bash
su -c "getprop | grep speed"
```

查找模块注入的属性（例如 `ro.sys.speedcool.version`）。

---

## 主要功能及命令示例

### 1. CPU 调控器调整
该模块在所有CPU核心上强制使用低延迟调控器（通常为 `performance`、`interactive` 或调整过的 `schedutil`）。

```bash
# 检查当前调控器
su -c "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
```
*预期输出：* `performance` 或 `schedutil`

### 2. RAM优化 (LMK)
Low Memory Killer阈值被修改，以保持前台应用响应迅速，同时积极杀死不太有用的后台进程。

```bash
# 检查LMK值（adj, minfree）
su -c "cat /sys/module/lowmemorykiller/parameters/minfree"
su -c "cat /sys/module/lowmemorykiller/parameters/adj"
```

### 3. I/O调度器优化
块层调度器被切换为针对交互性能优化的变体（例如 `bfq` 或 `fiops`）。

```bash
# 检查主存储块设备的当前调度器
su -c "cat /sys/block/mmcblk0/queue/scheduler"
```
*预期输出：* `[bfq]` 或 `[fiops]`

### 4. 网络调整
TCP拥塞控制被切换为更适合移动网络的算法（例如 `westwood` 或 `bbr`）。

```bash
# 检查当前TCP拥塞算法
su -c "cat /proc/sys/net/ipv4/tcp_congestion_control"
```
*预期输出：* `westwood`

### 5. 查看模块日志
如果模块脚本中启用了调试，您可以过滤系统日志。

```bash
su -c "logcat -d | grep SpeedCool"
```

### 6. 读取模块配置文件（如果可配置）
某些版本允许您通过编辑 `service.sh` 来选择配置。查看文件中的可用注释：

```bash
su -c "head -50 /data/adb/modules/SpeedCool/service.sh"
```

---

## 故障排除

| 症状 | 可能原因 | 解决方案 |
|---|---|---|
| **启动循环** | 模块冲突或设备不兼容。 | 启动时按住音量上键禁用模块，或在TWRP文件管理器中删除 `/data/adb/modules/SpeedCool` 目录。 |
| **性能无变化** | 存在冲突模块（LKT、FDE.AI、NFS）。 | 使用SpeedCool前移除所有其他性能模块。 |
| **设备仍然发热** | 热限制过于激进。 | 检查模块中的thermal-engine配置，或尝试其他配置文件。 |
| **应用崩溃** | LMK值过于激进。 | 在 `service.sh` 中手动调整 `minfree` 值。 |

---

## 移除

1. 打开 **Magisk Manager**。
2. 前往 **模块** 选项卡。
3. 点击 SpeedCool 旁边的 **移除**（垃圾桶）图标。
4. 点击 **重启**。

**替代命令行移除方式：**

```bash
su -c "rm -rf /data/adb/modules/SpeedCool/"
reboot
```

---

## 参考

- **GitHub仓库：** [Llucs/SpeedCool-Magisk-Module](https://github.com/Llucs/SpeedCool-Magisk-Module)
- **Magisk官方文档：** [topjohnwu.github.io/Magisk/](https://topjohnwu.github.io/Magisk/)
- **XDA Developers：** 搜索 *SpeedCool* 或 *Llucs* 以获取社区支持讨论。

> **免责声明：** 修改系统参数存在固有风险。在安装性能模块之前，请始终进行完整的Nandroid备份。作者对设备造成的任何损坏概不负责。