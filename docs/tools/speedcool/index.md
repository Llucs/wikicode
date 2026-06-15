---
title: SpeedCool Magisk Module
description: A Magisk module for Android that optimizes system settings to boost performance, reduce RAM usage, and improve thermal management.
created: 2026-06-15
tags:
  - android
  - magisk-module
  - performance-tuning
  - thermal-management
  - root
status: draft
---

# SpeedCool Magisk Module

**SpeedCool** is an open-source, lightweight Magisk module created by [Llucs](https://github.com/Llucs/SpeedCool-Magisk-Module). It automatically applies a comprehensive set of kernel and system-level tweaks at boot to boost performance, reduce RAM usage, and improve thermal management on any rooted Android device.

Unlike a standard bloatware cleaner, SpeedCool modifies the underlying system configuration to eliminate the root causes of lag and overheating.

---

## What It Does

SpeedCool targets several key system areas:

- **CPU Governor & Frequency Scaling:** Reduces wake-up latency for demanding applications (e.g., games, emulators).
- **Low Memory Killer (LMK):** Prioritizes keeping the currently active app in memory while aggressively reclaiming memory from background cache processes.
- **Thermal Engine:** Modifies thermal throttle points to balance sustained performance against heat generation.
- **I/O Scheduler:** Switches the storage scheduler to a low-latency variant for snappier app loading.
- **Network Stack:** Optimizes TCP congestion control for better throughput on mobile networks.
- **GPU Rendering:** Enables forced GPU rendering and optimizes the GPU governor.

---

## Why Use It?

- **Smoother Gaming:** Frame rates are more stable due to better CPU/GPU governor tuning and thermal throttling control.
- **Faster Multitasking:** Apps reload less frequently thanks to optimized LMK values.
- **Cooler Operation:** Smart thermal profiles prevent the SoC from reaching critical temperatures during heavy use.
- **All-in-One Optimizer:** Replaces the need for multiple conflicting performance modules.
- **Lightweight:** The module is typically under 1 MB and has negligible overhead.

---

## Installation

### Prerequisites

- Android device with an unlocked bootloader and root access.
- **Magisk** (v20.0+) installed.
- Custom recovery (TWRP) recommended as a fallback.

### Steps

1. **Download** the latest `SpeedCool-Magisk-Module.zip` from the [GitHub Releases page](https://github.com/Llucs/SpeedCool-Magisk-Module/releases).
2. Open the **Magisk Manager** app.
3. Navigate to the **Modules** tab.
4. Tap **Install from storage**.
5. Select the downloaded `.zip` file.
6. Swipe to confirm the installation.
7. **Reboot** your device when prompted.

> **Tip:** If you experience a bootloop, boot into Safe Mode (hold Volume Up during boot) and disable the module, or remove it manually via recovery by deleting `/data/adb/modules/SpeedCool/`.

---

## Usage & Verification

SpeedCool is designed to work entirely in the background. No user interface is required. You can verify its operation using terminal commands.

### Checking Active Status

List the module directory to confirm it is installed:

```bash
su -c "ls -la /data/adb/modules/SpeedCool/"
```

If successfully mounted, the directory will contain the module files (`system.prop`, `service.sh`, `module.prop`).

### Checking Applied System Properties

```bash
su -c "getprop | grep speed"
```

Look for properties injected by the module (e.g., `ro.sys.speedcool.version`).

---

## Key Features with Command Examples

### 1. CPU Governor Tuning
The module forces a low-latency governor (usually `performance`, `interactive`, or tweaked `schedutil`) on all CPU cores.

```bash
# Check the current governor
su -c "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
```
*Expected output:* `performance` or `schedutil`

### 2. RAM Optimization (LMK)
The Low Memory Killer thresholds are modified to keep the foreground app responsive while aggressively killing off less useful background processes.

```bash
# Check LMK values (adj, minfree)
su -c "cat /sys/module/lowmemorykiller/parameters/minfree"
su -c "cat /sys/module/lowmemorykiller/parameters/adj"
```

### 3. I/O Scheduler Optimization
The block layer scheduler is switched to a variant optimized for interactive performance (e.g., `bfq` or `fiops`).

```bash
# Check the active scheduler for the main storage block device
su -c "cat /sys/block/mmcblk0/queue/scheduler"
```
*Expected output:* `[bfq]` or `[fiops]`

### 4. Network Tweaks
TCP congestion control is switched to an algorithm better suited for mobile networks (e.g., `westwood` or `bbr`).

```bash
# Check the active TCP congestion algorithm
su -c "cat /proc/sys/net/ipv4/tcp_congestion_control"
```
*Expected output:* `westwood`

### 5. Viewing Module Logs
If debugging is enabled in the module script, you can filter the system log.

```bash
su -c "logcat -d | grep SpeedCool"
```

### 6. Reading the Module Profile (if configurable)
Some versions allow you to choose a profile by editing `service.sh`. Check the available comments inside the file:

```bash
su -c "head -50 /data/adb/modules/SpeedCool/service.sh"
```

---

## Troubleshooting

| Symptom | Likely Cause | Solution |
|---|---|---|
| **Bootloop** | Conflicting module or incompatible device. | Hold Volume Up during boot to disable module, or remove the `/data/adb/modules/SpeedCool` directory in TWRP file manager. |
| **No performance change** | Conflicting modules (LKT, FDE.AI, NFS). | Remove all other performance modules before using SpeedCool. |
| **Device still hot** | Thermal limits are too aggressive. | Check thermal-engine config in the module or try a different profile. |
| **Apps crashing** | Overly aggressive LMK values. | Manually adjust the `minfree` values in `service.sh`. |

---

## Removal

1. Open **Magisk Manager**.
2. Go to the **Modules** tab.
3. Tap the **Remove** (trash) icon next to SpeedCool.
4. Tap **Reboot**.

**Alternative command-line removal:**

```bash
su -c "rm -rf /data/adb/modules/SpeedCool/"
reboot
```

---

## References

- **GitHub Repository:** [Llucs/SpeedCool-Magisk-Module](https://github.com/Llucs/SpeedCool-Magisk-Module)
- **Magisk Official Docs:** [topjohnwu.github.io/Magisk/](https://topjohnwu.github.io/Magisk/)
- **XDA Developers:** Search for *SpeedCool* or *Llucs* for community support discussions.

> **Disclaimer:** Modifying system parameters carries inherent risk. Always perform a full Nandroid backup before installing performance modules. The authors are not responsible for any damage caused to your device.