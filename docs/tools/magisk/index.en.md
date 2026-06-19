---
title: Magisk - Systemless Root and Module Manager for Android
description: Magisk is a popular Android rooting tool that provides systemless root access and module support for system modifications.
created: 2026-06-19
tags:
  - android
  - root
  - systemless
  - magisk
  - tool
status: draft
---

# Magisk – Systemless Root and Module Manager for Android

## What is Magisk?

Magisk is an open-source software suite created by **John Wu (topjohnwu)** that enables **systemless rooting** and deep customization of Android devices. Unlike traditional rooting methods that modify the immutable `/system` partition, Magisk works by patching the device’s boot image (or `init_boot` partition on newer devices) to create an overlay file system at boot time. This allows root access, boot scripts, SELinux policy patches, and modules to load **without permanently altering system files**.

Originally released in 2016, Magisk quickly became the standard Android rooting solution, replacing older tools like SuperSU. It continues to be actively maintained and is widely used for both basic rooting and advanced device modifications.

---

## Why Use Magisk?

| Benefit | Description |
|---------|-------------|
| **Systemless modifications** | OTA updates are preserved because `/system` remains untouched. |
| **MagiskSU** | Pure open-source root permission management (grant, prompt, deny). |
| **Module system** | Install tweaks (audio mods, camera libs, ad-blocking, fonts) without repartitioning. |
| **Zygisk** | Code injection into every app’s process via Zygote – replaces MagiskHide. |
| **DenyList** | Hide root, modules, and unlocked bootloader from specific apps (banking, streaming). |
| **MagiskBoot** | Powerful tool to unpack, modify, and repack Android boot images. |
| **Active community** | Thousands of modules and extensive documentation available. |

Magisk is essential for users who need root access for advanced backup tools, automation (Tasker), custom system tweaks, or to re-enable features in apps that block rooted devices.

---

## Installation Guide

### Prerequisites

- **Unlocked bootloader** (device‑specific, often requires OEM unlock).
- **Working ADB and Fastboot** on your computer.
- **Device factory image** or stock `boot.img` (and possibly `init_boot.img`).
- **Backup** all important data.

### Step 1 – Extract the Boot Image

Obtain the factory image for your device (e.g., from Google’s factory images page) and extract the boot image.

```bash
# Example for a Pixel device
unzip [device]_[build].zip
cd [device]_[build]
unzip image-[device]-[build].zip
# boot.img is now in the current directory
```

For devices running Android 13+ (e.g., Pixel 6 series), the root partition is `init_boot.img` instead of `boot.img`.

### Step 2 – Patch the Image with the Magisk App

1. Install the latest Magisk APK on your device.
2. Open the Magisk app, tap **Install** → **Select and Patch a File**.
3. Choose the extracted `boot.img` (or `init_boot.img`).
4. The app will patch the image and save a new file named `magisk_patched-XXXXX.img` (usually in `Download/`).

### Step 3 – Flash the Patched Image

Transfer the patched image to your computer, then boot your device to fastboot mode.

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

### Step 4 – Verify Installation

After reboot, open the Magisk app. The **Home** screen should display the installed Magisk version and “Installed” next to Magisk status.

---

## Basic Usage

### Magisk App Interface

- **Superuser tab** (shield icon): Lists all apps that have requested root permissions. Tap an entry to change its permission status (Grant / Prompt / Deny).
- **Modules tab** (puzzle piece icon): Shows installed modules. Tap the **+** button to install a new module from a `.zip` file stored on your device. Use the toggle switch to enable/disable a module (most require a reboot).
- **Settings tab** (gear icon):
  - **Zygisk**: Enable or disable Zygisk (requires reboot).
  - **DenyList**: Configure which apps Magisk should hide from (requires Zygisk and a reboot).
  - **Update Channel**: Choose Stable, Beta, or Canary for app and Magisk updates.
  - **Automatic Response**: Set default root permission behavior.

### Module Management

Modules are installed as standard ZIP archives. They can contain simple scripts, binary files, or full system overlay directories.

```bash
# Typical module ZIP structure (inside /data/adb/modules/<module_id>/)
module.prop          # Metadata (id, name, version, author)
system/              # Files to overlay on /system
post-fs-data.sh      # Script run early in boot
service.sh           # Script run later in boot
```

To install a module manually:

1. Download the module `.zip` to your device.
2. Open Magisk app → Modules tab → **Install from storage**.
3. Select the file, confirm, and then **Reboot** when prompted.

### Uninstalling Magisk

The Magisk app provides a direct way to remove root completely:

1. Open Magisk app.
2. Tap **Uninstall Magisk** at the bottom of the Home screen.
3. Confirm – the app will restore the original, unpatched boot image and reboot.

---

## Key Features

### MagiskSU

A complete replacement for `su` that is fully open‑source. It implements a permission model with Grant / Prompt / Deny options and logs all root accesses. MagiskSU is compatible with all existing apps that require root.

### Magisk Modules

A standardized format to distribute system modifications without touching the system partition. Modules are loaded at boot using the Magisk overlay filesystem. Thousands of modules exist on forums like XDA and the Magisk repository.

### Zygisk

Zygisk is Magisk’s implementation of code injection into the Zygote process. It enables run‑time modifications inside any app’s process. Zygisk replaces the older MagiskHide functionality.

### DenyList

When Zygisk is enabled, you can configure a **DenyList** of apps where Magisk hides its presence (root, modules, unlocked bootloader). This is the modern way to bypass integrity checks used by banking, payment, and streaming apps.

### MagiskBoot

MagiskBoot is a low‑level tool for working with boot images. It can unpack, modify, and repack them without needing a full Android environment. It is often used directly on a computer to create patched images without the app.

---

## Command Examples

### Flash patched boot image (fastboot)

```bash
fastboot flash boot magisk_patched-27000.img
fastboot reboot
```

### Flash init_boot for newer devices

```bash
fastboot flash init_boot magisk_patched-27000.img
fastboot reboot
```

### Use MagiskBoot to unpack a boot image

```bash
magiskboot unpack boot.img
# This creates: kernel, kernel_dtb, ramdisk.cpio, header, etc.
```

### Repack a modified boot image with MagiskBoot

```bash
magiskboot repack boot.img
# Creates new-boot.img with your modifications.
```

### Verify boot image header

```bash
magiskboot info boot.img
```

### Patch a boot image with Magisk (command line)

If you have the Magisk executable on your computer, you can patch directly:

```bash
magiskboot boot.img
# Creates patched_boot.img in the current directory.
```

### Hide Magisk from an app (DenyList)

Open Magisk app → Settings → **Configure DenyList** → add the target app (e.g., `com.google.android.gms` for Google Play Services). After a reboot, Magisk will be invisible to that app.

---

## Tips and Considerations

- **OTA updates** remain compatible because Magisk only modifies the boot partition. However, after an OTA you must **re‑flash Magisk** to the new boot image.
- **SafetyNet / Play Integrity** – While Magisk itself does not provide integrity bypass, tools like Zygisk-Assistant or Shamiko modules can help hide root from Google’s attestation checks.
- **Module conflicts** – Some modules may interfere with each other; disable them one by one to isolate issues.
- **Backups** – Always keep a copy of the original stock boot image. If something goes wrong, you can restore it via fastboot.
- **Magisk Canary** – The bleeding‑edge channel sometimes includes unstable features. Use it only for testing.

---

## References

- [Magisk GitHub repository](https://github.com/topjohnwu/Magisk)
- [Official Magisk documentation (developer guides)](https://topjohnwu.github.io/Magisk/)
- [Magisk module repository (unofficial)](https://www.androidacy.com/modules-repository/)
- [XDA Developers – Magisk Discussion & Support](https://forum.xda-developers.com/f/magisk.5903/)

---

*This document is part of the developer wiki. Comments and improvements are welcome.*