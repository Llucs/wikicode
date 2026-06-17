---
title: Team Win Recovery Project (TWRP)
description: TWRP is an open-source custom recovery for Android that enables flashing custom ROMs, full-device backups (NANDroid), and system modifications through a touchscreen interface.
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

TWRP (Team Win Recovery Project) is an **open-source custom recovery image** for Android-based devices. It replaces the stock recovery partition to provide a feature-rich, touchscreen-driven environment for installing third‑party firmware, creating complete system backups, and performing advanced system management tasks — all without needing to boot into Android.

## Why TWRP?

Stock Android recovery is limited to factory resets and OTA updates. TWRP opens up the device for:

- **Custom ROM installation** (LineageOS, Pixel Experience, etc.)
- **Full system backups and restores** (NANDroid) — essential before risky modifications.
- **Rooting** (flashing Magisk or SuperSU).
- **Partition management** (wiping, formatting, resizing).
- **Encryption handling** (decrypting userdata under certain conditions).
- **ADB sideloading and MTP** for transferring files or flashing without storage.

TWRP is the de facto standard for Android enthusiasts and developers; it has replaced earlier recoveries like ClockworkMod (CWM) thanks to its intuitive interface and active community support.

## Key Features

- **Touch GUI** – Full touch support with on‑screen keyboard, file manager, and terminal emulator.
- **NANDroid Backup** – Clones entire partitions (Boot, System, Data, EFS/IMEI) to `/sdcard/TWRP/BACKUPS/`.
- **ZIP Flashing** – Installs custom firmware packages (ROMs, kernels, mods, GApps, Magisk).
- **Advanced Wipe** – Wipe individual partitions, “Format Data” to remove encryption.
- **File Manager** – Browse and modify files on the device’s filesystem.
- **ADB Sideload** – Flash ZIP files from a computer via USB.
- **MTP Support** – Access device storage as a removable drive in recovery.
- **Encryption Support** – Can decrypt userdata with PIN/password/pattern (older encryptions; FBE on modern devices is often unsupported).
- **Theming** – Customizable UI via `.twres` themes.
- **Screenshot** – Capture screen while in recovery.

## History

Created by *Dees_Troy* around 2011, TWRP quickly became the most popular custom recovery due to its proprietary touchscreen interface. It evolved through a Holo theme to a Material Design interface (version 3.0+). Today it is maintained by a core team and supports hundreds of officially listed devices at [twrp.me](https://twrp.me).

## Installation

> **Prerequisites:**
> - Unlocked bootloader (required for most devices).
> - ADB & Fastboot tools installed on your PC.
> - Correct TWRP image for your exact device model (check codename at twrp.me).

### General Fastboot Method (most devices)

1. **Reboot to bootloader:**
   ```bash
   adb reboot bootloader
   ```
2. **Flash the recovery image:**
   ```bash
   fastboot flash recovery twrp-<version>.img
   ```
3. **Boot into recovery immediately** (before system boots, which may overwrite TWRP):
   ```bash
   fastboot reboot recovery
   # or use hardware key combination (Vol Up + Power, etc.)
   ```

### Slot‑based Devices (A/B partitions – e.g., Pixels, OnePlus)

Because the system can auto‑replace the recovery partition on next boot, use a temporary boot method:

1. **Boot the TWRP image temporarily:**
   ```bash
   fastboot boot twrp-<version>.img
   ```
2. **Inside TWRP, go to** *Advanced → Install Recovery Ramdisk*.
   - This flashes TWRP to the inactive slot and prevents it from being overwritten.

### Samsung Devices (via Odin)

1. Download the `.tar` TWRP file (usually named `twrp-<version>-<device>.tar`).
2. Open Odin, place the file in the **AP** slot.
3. Uncheck **Auto-Reboot** in Odin options.
4. Flash, then immediately reboot into recovery using key combo (Vol Up + Home + Power) to prevent stock recovery restoration.

### From a Rooted Device (using Official TWRP App)

1. Install the **Official TWRP App** from the Play Store or twrp.me.
2. Grant root permissions.
3. Select your device and flash the latest image.

### From Terminal (rooted)

```bash
su
dd if=/sdcard/twrp.img of=/dev/block/bootdevice/by-name/recovery
```

Replace the path with your recovery partition location (vary by device – find with `parted` or `ls /dev/block/platform/...`).

## Basic Usage Workflow

### Enter Recovery
- Use the hardware key combination (varies by manufacturer, often **Volume Down + Power**).
- Or from Android (if rooted/bootloader unlocked): `adb reboot recovery`.

### Wiping Partitions

- **Factory Reset** (wipe data/cache) – required before installing a new ROM.
  - *Wipe → Swipe to Factory Reset*
- **Format Data** – removes encryption and wipes internal storage.
  - *Wipe → Format Data → type “yes”*.
- **Advanced Wipe** – select individual partitions to wipe.

### Installing a ZIP (ROM, GApps, Magisk, etc.)

1. Tap **Install**.
2. Navigate to the `.zip` file (usually on `/sdcard` or external SD).
3. Tap the file; optionally tap **Add more Zips** to queue multiple files.
4. **Swipe to Confirm Flash**.
5. *(Optional)* Reboot system.

> Example command for sideload:
> ```bash
> adb sideload custom_rom.zip
> ```

### Backing Up (NANDroid)

1. Tap **Backup**.
2. Select partitions:
   - **Boot**, **System**, **Data** (minimum for a full system restore).
   - **EFS** (stores IMEI – critical for some devices).
3. Swipe to begin backup.
4. Backup is stored in `/sdcard/TWRP/BACKUPS/<device_serial>/`.

### Restoring a Backup

1. Tap **Restore**.
2. Select a backup from the list.
3. Tick the partitions you want to restore.
4. Swipe to confirm.

### File Manager & Terminal

- **File Manager**: *Advanced → File Manager* – navigate, delete, rename, copy files.
- **Terminal**: *Advanced → Terminal* – run commands as root.

## Example Commands (Fastboot & ADB)

```bash
# Reboot to bootloader from Android
adb reboot bootloader

# Flash recovery
fastboot flash recovery twrp-3.7.1_12-0-beryllium.img

# Boot into recovery without flashing
fastboot boot twrp-3.7.1_12-0-beryllium.img

# Sideload a file from PC
adb sideload LineageOS-21.0-20260617-UNOFFICIAL-beryllium.zip

# Push a file to the device in MTP mode
adb push magisk.zip /sdcard/
```

## Critical Warnings

- **Device‑specific images** – Flashing a TWRP image for a different model can **hard brick** your device. Always verify the codename (e.g., `beryllium` for Pocophone F1).
- **A/B slot confusion** – On devices with seamless updates, TWRP must be installed to both slots. If one slot lacks TWRP, the device may revert to stock recovery.
- **Encryption issues** – Modern Android uses **File‑Based Encryption (FBE)**. TWRP often cannot decrypt userdata. Users frequently must **Format Data** (wipes internal storage) when switching ROMs or if TWRP cannot mount `/data`.
- **OTAs with custom recovery** – Stock OTA updates usually fail with TWRP. You must either:
  - Flash the OTA ZIP manually via TWRP.
  - Or revert to stock recovery before applying OTA.
- **Play Integrity / Banking apps** – An unlocked bootloader (required for TWRP) breaks many security checks. Rooting with Magisk can hide this, but adds complexity and is not always successful.
- **Backup before modifying** – Always create a NANDroid backup before flashing any new ROM or risky mod. A full backup can rescue a soft brick in minutes.

## Troubleshooting

| Problem | Solution |
|--------|----------|
| TWRP doesn’t stick after reboot | Use `fastboot boot` then “Install Recovery Ramdisk” (A/B devices). Another option: reflash and immediately boot into recovery. |
| Cannot mount `/data` | Likely encrypted. Go to *Wipe → Format Data* and type “yes”. **This erases all internal storage.** |
| Device stays at boot logo after flash | Try wiping Dalvik/ART Cache and Cache. If still fails, restore a previous backup. |
| ADB Sideload stuck at “sending” | Ensure you have the latest ADB drivers. Try a different USB cable/port. |
| TWRP not booting (black screen) | The image may be corrupted or incorrect. Re-download from the official site. |

## Additional Resources

- **Official site & downloads:** [https://twrp.me](https://twrp.me)
- **Source code:** [https://github.com/TeamWin/Team-Win-Recovery-Project](https://github.com/TeamWin/Team-Win-Recovery-Project)
- **XDA Forums:** Search for your device’s specific forum thread for TWRP builds and support.
- **Compiling TWRP from source:** [https://github.com/TeamWin/Team-Win-Recovery-Project/blob/android-12.1/README.md](https://github.com/TeamWin/Team-Win-Recovery-Project/blob/android-12.1/README.md)

TWRP is a powerful tool for any Android developer or enthusiast. Use it wisely, and always keep a backup handy.