---
title: Heimdall - Samsung Firmware-Flashtool
description: Plattformübergreifende Open-Source-Tool-Suite zum Flashen von Firmware (ROMs) auf Samsung-Mobilgeräte.
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

## Was ist Heimdall?

Heimdall ist eine plattformübergreifende Open-Source-Tool-Suite, die entwickelt wurde, um Firmware (Stock-ROMs, Custom-ROMs, Bootloader und Recovery-Images) auf Samsung-Android-Geräte zu flashen. Es arbeitet direkt über USB mit Samsungs proprietärem Odin-Protokoll und bietet eine kostenlose, Linux/macOS-freundliche Alternative zu dem nur unter Windows verfügbaren Odin-Tool. Das Projekt wird auf GitHub von Benjamin Dobell betreut und wird seit den frühen 2010er Jahren in der Android-Modding-Community häufig eingesetzt.

## Warum Heimdall verwenden?

- **Plattformübergreifend** – Läuft nativ auf Windows, Linux und macOS ohne Emulation.
- **Open Source** – Vollständig überprüfbar und gemeinschaftsorientiert.
- **Umgeht Odin-Einschränkungen** – Nützlich, wenn Odin nicht verfügbar ist oder beim Flashen auf Nicht-Windows-Systemen.
- **Skriptbar** – Die Befehlszeilenschnittstelle ermöglicht Automatisierung und Integration in benutzerdefinierte Toolchains.
- **Partitionsebene-Flashen** – Flashen einzelner Partitions-Images (z. B. `BOOT`, `SYSTEM`, `RECOVERY`) für gezielte Änderungen.

## Installation

### Windows
Laden Sie das neueste Installationsprogramm von der [GitHub-Releases-Seite](https://github.com/Benjamin-Dobell/Heimdall/releases) herunter. Führen Sie die `.exe`-Datei aus und folgen Sie dem grafischen Installer.

### Linux
Verfügbar über viele Paketmanager:
```bash
# Debian/Ubuntu
sudo apt install heimdall-flash

# Fedora
sudo dnf install heimdall

# Arch Linux
sudo pacman -S heimdall
```
Alternativ aus dem Quellcode mit `cmake` erstellen.

### macOS
Installation über Homebrew:
```bash
brew install heimdall
```
Oder laden Sie das macOS-Binary von der Releases-Seite herunter.

## Verwendung

### Voraussetzungen
1. Aktivieren Sie die **Entwickleroptionen** und das **USB-Debugging** auf dem Samsung-Gerät.
2. Starten Sie das Gerät im **Download-Modus** (typischerweise: Ausschalten → Lautstärke leiser + Home + Power gedrückt halten, dann Lautstärke lauter drücken, um zu bestätigen).
3. Verbinden Sie das Gerät über USB mit dem Computer.

### Erkennung
Überprüfen Sie, ob das Gerät erkannt wird:
```bash
heimdall detect
```
Bei Erfolg zeigt die Ausgabe das Gerätemodell und den Verbindungsstatus an.

### Grundlegendes Flashen
Ein Partitions-Image flashen:
```bash
heimdall flash --RECOVERY twrp-3.6.0-i9300.img
```
Mehrere Partitionen gleichzeitig flashen:
```bash
heimdall flash --BOOT boot.img --SYSTEM system.img --VENDOR vendor.img
```

### Verwendung einer PIT-Datei
Für die vollständige Firmware-Wiederherstellung oder wenn die Partitionstabelle unbekannt ist, geben Sie eine `.pit`-Datei an, die vom Gerät oder aus dem Firmware-Paket extrahiert wurde:
```bash
heimdall flash --pit /path/to/device.pit --SLT --no-reboot
```
Das Flag `--SLT` flasht alle in der PIT definierten Partitionen, während `--no-reboot` das Gerät nach Abschluss im Download-Modus hält.

### Verbindung schließen
Nach dem Flashen schließen Sie die USB-Schnittstelle:
```bash
heimdall close-pc-screen
```

## Hauptfunktionen

- **Plattformübergreifend**: Windows, Linux, macOS (native Binärdateien).
- **Open Source**: BSD-lizenzierter Code mit aktiver Community-Wartung.
- **Odin-Protokollunterstützung**: Direkte Implementierung von Samsungs Low-Level-Flasher-Protokoll.
- **Geräteerkennung**: Zuverlässige USB-Aufzählung und Handshake-Überprüfung.
- **Partitionsebene-Flashen**: Flashen einzelner Partitionen (Boot, Recovery, System usw.).
- **PIT-basiertes Flashen**: Verwendung von Partitionstabellen zur vollständigen Firmware-Wiederherstellung.
- **Integrierte USB-Treiber**: Windows-Installer enthalten erforderliche Treiber; libusb wird auf Linux/macOS verwendet.
- **Skriptunterstützung**: CLI-Flags geeignet für automatisierte Pipelines und CI/CD-Umgebungen.

## Beispiele

### Ein verbundenes Gerät erkennen
```bash
$ heimdall detect
Device detected: GT-I9300 (galaxys3)
```

### Benutzerdefinierte Recovery (TWRP) flashen
```bash
heimdall flash --RECOVERY twrp-3.6.0_9-i9300.img --no-reboot
```

### Vollständige Stock-Firmware mit einer PIT-Datei flashen
```bash
heimdall flash --pit AP_I9300_4.3.pit --SLT --no-reboot
```

### Nur die Boot-Partition flashen
```bash
heimdall flash --BOOT boot.img
```

## Hinweise

- Heimdall unterscheidet sich vom **Heimdall Application Dashboard** (linuxserver/Heimdall, ein webbasierter App-Launcher) und dem **Heimdall**-Cybersicherheits-Framework.
- Verwenden Sie immer die richtige Firmware für Ihr Gerätemodell, um Bricking zu vermeiden.
- Stellen Sie sicher, dass USB-Treiber unter Windows installiert sind – der Installer enthält diese. Unter Linux müssen möglicherweise udev-Regeln hinzugefügt werden, damit das Gerät ohne Root-Zugriff erreichbar ist.