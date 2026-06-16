---
title: Heimdall - Samsung Firmware Flashing Tool
description: Cross-platform open-source tool suite for flashing firmware (ROMs) onto Samsung mobile devices.
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

## What is Heimdall?

Heimdall is a cross-platform, open-source tool suite designed to flash firmware (stock ROMs, custom ROMs, bootloaders, and recovery images) onto Samsung Android devices. It operates directly over USB using Samsung's proprietary Odin protocol, providing a free and Linux/macOS-friendly alternative to the Windows-only Odin tool. The project is maintained on GitHub by Benjamin Dobell and has been widely used in the Android modding community since the early 2010s.

## Why use Heimdall?

- **Cross-platform** – Runs natively on Windows, Linux, and macOS without emulation.
- **Open source** – Fully auditable and community-driven.
- **Bypasses Odin restrictions** – Useful when Odin is unavailable or when flashing on non-Windows systems.
- **Scriptable** – Command-line interface enables automation and integration into custom toolchains.
- **Partition-level flashing** – Flash individual partition images (e.g., `BOOT`, `SYSTEM`, `RECOVERY`) for targeted modifications.

## Installation

### Windows
Download the latest installer from the [GitHub releases page](https://github.com/Benjamin-Dobell/Heimdall/releases). Run the `.exe` and follow the graphical installer.

### Linux
Available via many package managers:
```bash
# Debian/Ubuntu
sudo apt install heimdall-flash

# Fedora
sudo dnf install heimdall

# Arch Linux
sudo pacman -S heimdall
```
Alternatively, build from source using `cmake`.

### macOS
Install via Homebrew:
```bash
brew install heimdall
```
Or download the macOS binary from the releases page.

## Usage

### Prerequisites
1. Enable **Developer Options** and **USB Debugging** on the Samsung device.
2. Boot the device into **Download Mode** (typically: Power Off → hold Volume Down + Home + Power, then press Volume Up to confirm).
3. Connect the device to the computer via USB.

### Detection
Verify the device is recognised:
```bash
heimdall detect
```
If successful, output will display the device model and connection status.

### Basic Flashing
Flash a partition image:
```bash
heimdall flash --RECOVERY twrp-3.6.0-i9300.img
```
Flash multiple partitions at once:
```bash
heimdall flash --BOOT boot.img --SYSTEM system.img --VENDOR vendor.img
```

### Using a PIT file
For full firmware restoration or when partition table is unknown, provide a `.pit` file extracted from the device or firmware package:
```bash
heimdall flash --pit /path/to/device.pit --SLT --no-reboot
```
The `--SLT` flag flashes all partitions defined in the PIT, while `--no-reboot` keeps the device in download mode after completion.

### Close connection
After flashing, close the USB interface:
```bash
heimdall close-pc-screen
```

## Key Features

- **Cross-platform**: Windows, Linux, macOS (native binaries).
- **Open source**: BSD-licensed codebase with active community maintenance.
- **Odin protocol support**: Direct implementation of Samsung's low-level flashing protocol.
- **Device detection**: Reliable USB enumeration and handshake verification.
- **Partition-level flashing**: Flash individual partitions (boot, recovery, system, etc.).
- **PIT-based flashing**: Use partition information tables for complete firmware restoration.
- **Built-in USB drivers**: Windows installers include necessary drivers; libusb used on Linux/macOS.
- **Scripting support**: CLI flags suitable for automated pipelines and CI/CD environments.

## Examples

### Detect a connected device
```bash
$ heimdall detect
Device detected: GT-I9300 (galaxys3)
```

### Flash a custom recovery (TWRP)
```bash
heimdall flash --RECOVERY twrp-3.6.0_9-i9300.img --no-reboot
```

### Flash a full stock firmware using a PIT file
```bash
heimdall flash --pit AP_I9300_4.3.pit --SLT --no-reboot
```

### Flash only the boot partition
```bash
heimdall flash --BOOT boot.img
```

## Notes

- Heimdall is distinct from the **Heimdall Application Dashboard** (linuxserver/Heimdall, a web-based app launcher) and the **Heimdall** cybersecurity framework.
- Always use the correct firmware for your device model to avoid bricking.
- Ensure USB drivers are installed on Windows – the installer includes them. On Linux, udev rules may need to be added for the device to be accessible without root.