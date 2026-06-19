---
title: "Termux: Terminalemulator und Linux-Umgebung für Android"
description: "Ein umfassender Leitfaden für Termux, den leistungsstarken Open-Source-Terminalemulator und die Linux-Umgebung für Android-Geräte, der Installation, Paketverwaltung, fortgeschrittene Nutzung und Entwickler-Workflows abdeckt."
created: 2026-06-19
tags:
  - android
  - terminal
  - linux
  - development
  - tools
status: draft
---

# Termux: Terminalemulator und Linux-Umgebung für Android

## Was ist Termux?

Termux ist ein **Open-Source-Terminalemulator und eine Linux-Umgebung** für Android. Es arbeitet vollständig im Userspace, benötigt **keinen Root-Zugriff** und bietet ein umfangreiches, von Debian/Ubuntu abgeleitetes Paket-Repository. Mit Termux können Sie eine vollständige Linux-Kommandozeilenerfahrung auf Ihrem Android-Gerät nutzen – installieren Sie Compiler, Interpreter, Texteditoren, Netzwerktools und mehr. Es nutzt die Linux-Systemaufrufe des Android-Kernels, um eine nahezu native Umgebung zu schaffen.

### Warum Termux verwenden?

- **Tragbare Entwicklungsumgebung** – Python-Skripte schreiben und ausführen, C-Programme kompilieren, Git-Repositorys verwalten oder eine REPL direkt auf Ihrem Telefon nutzen.
- **Serveradministration unterwegs** – Per SSH zu entfernten Servern verbinden, Netzwerkdiagnose durchführen (ping, traceroute, nmap) und Dateien mit rsync synchronisieren.
- **Lernen & Bildung** – Linux-Befehle, Shell-Scripting und Netzwerkkonzepte üben, ohne einen vollständigen PC zu benötigen.
- **Automatisierung & Integration** – Mit Android-Automatisierungs-Apps (Tasker) kombinieren oder Termux:API verwenden, um mit der Telefonhardware (Kamera, Sensoren, Zwischenablage) zu interagieren.
- **Vollständige Linux-Distributionen** – Installieren Sie Ubuntu, Debian, Arch oder Fedora in einer Termux-Umgebung mit proot-distro für nahezu jede Linux-Aufgabe.

---

## Hauptfunktionen

| Feature | Beschreibung |
|---------|-------------|
| **Terminalemulator** | Voll ausgestattet mit berührungsfreundlichen Gestensteuerungen, zusätzliche Funktionstasten (Tab, Strg, Alt, Esc) erreichbar durch Wischen nach links von der Zahlenreihe. |
| **Paketmanager** | `pkg` (und das zugrunde liegende `apt`) mit Tausenden von Paketen aus dem Termux-Repository. |
| **Multi-Session-Verwaltung** | Ziehen Sie eine Schublade heraus, um separate Terminalsitzungen zu verwalten, die jeweils unabhängig angemeldet sind. |
| **SSH-Client & -Server** | Mit `ssh` zu entfernten Servern verbinden oder einen Server (`sshd`) starten, um von einem Computer auf Ihr Gerät zuzugreifen. |
| **Proot-Distro-Unterstützung** | Führen Sie vollständige Linux-Distributionen (Ubuntu, Debian, Arch, Fedora) mit `proot-distro` aus. |
| **API-Integration** | Die begleitende App *Termux:API* gibt Skripten Zugriff auf Android-Sensoren, Zwischenablage, TTS, Kamera, Benachrichtigungen und mehr. |
| **Speicherzugriff** | Mounten Sie den freigegebenen Android-Speicher (intern/SD) über `termux-setup-storage`. |

---

## Installation

### 1. Termux beziehen

> **Wichtig**: Die **Google Play Store Version ist veraltet** (auf API 28 beschränkt). Installieren Sie immer aus **F-Droid**, um aktuelle Pakete und vollständige Kompatibilität mit modernem Android (10+) zu erhalten.

- **F-Droid-Client**: Suchen Sie in der F-Droid-App nach "Termux" oder laden Sie die APK direkt von [F-Droid](https://f-droid.org/packages/com.termux/) herunter.
- **Direkter APK-Download**: [F-Droid APK](https://f-droid.org/repo/com.termux_*.apk) (immer die neueste Version).

### 2. Begleit-Apps (optional, aber empfohlen)

| App | Zweck |
|-----|-------|
| [Termux:API](https://f-droid.org/packages/com.termux.api/) | Zugriff auf Android-Hardware (Sensoren, Kamera, Zwischenablage usw.) aus Skripten. |
| [Termux:Float](https://f-droid.org/packages/com.termux.float/) | Termux in einem schwebenden Fenster (Overlay) ausführen. |
| [Termux:Styling](https://f-droid.org/packages/com.termux.styling/) | Farbschemata und powerline-fähige Schriftarten für das Terminal. |
| [Termux:Tasker](https://f-droid.org/packages/com.termux.tasker/) | Termux-Programme aus Tasker und kompatiblen Automatisierungs-Apps aufrufen. |
| [Termux:Widget](https://f-droid.org/packages/com.termux.widget/) | Kleine Skriptchen vom Startbildschirm starten. |

### 3. Ersteinrichtung

Nach dem ersten Start von Termux:

```bash
# Update the package repository and upgrade all packages
pkg update && pkg upgrade

# Grant storage access (needed to see your shared folders)
termux-setup-storage
```

Jetzt haben Sie eine vollständig aktualisierte Termux-Umgebung. Der geteilte Android-Speicher ist unter `~/storage/shared` eingebunden.

---

## Paketverwaltung

Termux verwendet den **`pkg`**-Befehl als Wrapper um **`apt`**. Alle Befehle sind Debian/Ubuntu-Benutzern vertraut.

### Häufige Paketoperationen

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

### Verfügbare Pakete (Auswahl)

| Kategorie | Pakete |
|-----------|--------|
| **Sprachen** | python, python3, nodejs, ruby, php, lua, golang, rust |
| **Compiler/Werkzeuge** | clang, make, gdb, cmake, gcc (via proot distro) |
| **Editoren** | vim, emacs, nano, neovim |
| **Netzwerk** | openssh, nmap, traceroute, netcat, rclone |
| **Datenbanken** | mariadb, sqlite, postgresql (requires proot) |
| **Dienstprogramme** | git, curl, wget, rsync, htop, jq, ripgrep, fd |

> **Hinweis**: Da Termux eine Userspace-Umgebung ist, erfordern einige systemnahe Pakete (z. B. `systemd`, `glibc`-Abhängigkeiten) eine vollständige Linux-Distribution über `proot-distro`.

---

## Fortgeschrittene Nutzung

### 1. SSH: Client und Server

**Client** – Wie auf dem Desktop mit entfernten Maschinen verbinden:

```bash
pkg install openssh
ssh user@hostname
```

**Server** – Machen Sie Ihr Android-Gerät per SSH erreichbar (Standardport 8022):

```bash
sshd
# or start it in the foreground with -d
sshd -d
```

Von einem anderen Computer verbinden:

```sh
ssh user@phone-ip -p 8022
```

> Beim ersten Ausführen von `sshd` generiert Termux Hostschlüssel und Sie können ein Passwort für den Termux-Benutzer festlegen (Standardbenutzer ist `u0_aXYZ`). Verwenden Sie `passwd`, um es zu ändern.

### 2. Vollständige Linux-Distributionen mit `proot-distro` ausführen

Proot ermöglicht es, eine standardmäßige Linux-Distribution in Termux ohne Root-Rechte auszuführen. Das Paket `proot-distro` vereinfacht dies.

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

Jetzt haben Sie eine vollständige Ubuntu-Umgebung (einschließlich `systemd`-ähnlicher Dienstmanager über `proot`, auch wenn nicht alle Funktionen perfekt funktionieren). Sie können Pakete wie `gcc`, `postgresql` oder `firefox` (GUI benötigt X-Server) darin installieren.

### 3. Verwendung der Termux:API-Begleitapp

Mit installiertem `Termux:API` können Sie Android-Funktionen von der Kommandozeile aus steuern.

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

### 4. Automatisierung mit Tasker

Termux:Tasker ermöglicht es Ihnen, Termux-Skripte als Tasker-Aktionen auszuführen.

1. Installieren Sie **Termux:Tasker** aus F-Droid.
2. Fügen Sie in Tasker eine Aktion vom Typ `System -> Send Intent` hinzu.
3. Aktion: `com.termux.tasker.RUN_COMMAND`
4. Zusätzliche Schlüssel/Wert-Paare: `command` = Ihr Skript oder Befehl (z. B. `termux-battery-status`).

Sie können auch Skripte in `~/.termux/tasker/` ablegen und sie beim Namen aufrufen.

### 5. Sitzungsverwaltung & UI-Tricks

- **Zusätzliche Tasten**: Wischen Sie von der Zahlenreihe (oben auf der Tastatur) nach links, um eine Reihe mit Tab, Strg, Alt, Esc, einem Funktionstasten-Umschalter und einem Pfeil nach oben (zum Scrollen) anzuzeigen. Sie können diese in `~/.termux/termux.properties` anpassen.
- **Mehrere Sitzungen**: Tippen Sie auf das Drawer-Symbol (drei horizontale Linien) auf der linken Seite des Bildschirms, um Terminalsitzungen aufzulisten, zu wechseln oder neue zu erstellen.
- **Textauswahl**: Langes Drücken im Terminalbereich, um den Auswahlmodus zu aktivieren; Kopieren/Einfügen funktioniert über das Menü.

---

## Anwendungsfälle

- **Mobiles Programmieren** – Python-Skripte, Node.js-Apps oder C-Programme mit vim und gcc schreiben und testen. Verwenden Sie git zur Versionskontrolle.
- **Server-Operationen** – Per SSH zu Produktionsservern verbinden, `tcpdump`- oder `nmap`-Scans durchführen, Logs überwachen und Dateien mit `rsync` übertragen.
- **Datenanalyse** – Installieren Sie Python mit pandas, numpy, scipy und Jupyter (via `pkg install jupyter`) für Datenverarbeitung unterwegs.
- **Linux lernen** – Experimentieren Sie mit dem Dateisystem, Shell-Scripting und Netzwerken ohne einen separaten PC.
- **Taschenrechner** – Verwenden Sie Python als interaktiven Taschenrechner: `python -c 'print(2**100)'` oder starten Sie eine REPL.

---

## Fehlerbehebung & Tipps

- **Paketinstallation schlägt fehl mit "404 Not Found"** – Paketquellen sind möglicherweise veraltet. Führen Sie zuerst `pkg update && pkg upgrade` aus. Wenn das Problem weiterhin besteht, überprüfen Sie, ob Sie die F-Droid-Version (nicht Google Play) verwenden.
- **Speicherzugriff verweigert** – Führen Sie `termux-setup-storage` aus und erteilen Sie die Berechtigung, wenn Sie dazu aufgefordert werden. Wenn dies unter Android 11+ fehlschlägt, stellen Sie sicher, dass Termux die Berechtigung "Dateien und Medien" in den Systemeinstellungen aktiviert hat.
- **Probleme mit libc/glibc-Abhängigkeiten** – Einige Pakete erwarten glibc, aber Termux verwendet bionic (Androids libc). Verwenden Sie eine proot-distro (Ubuntu, Debian) für diese Pakete.
- **So deaktivieren Sie die Vollbild-Tastatur unter Android 10+** – Fügen Sie diese Zeile zu `~/.termux/termux.properties` hinzu: `fullscreen=false` Dann laden Sie mit `termux-reload-settings` neu.
- **Zwischenablagen-Integration mit dem Terminal** – Verwenden Sie `termux-clipboard-get` und `termux-clipboard-set` aus `termux-api`, um mit der Systemzwischenablage zu interagieren.

---

## Community & Ressourcen

- **Offizielle Website**: [termux.com](https://termux.com) (leitet zu GitHub weiter)
- **GitHub-Repository**: [termux/termux-app](https://github.com/termux/termux-app) (Haupt-App)
- **Paket-Repository**: [termux/termux-packages](https://github.com/termux/termux-packages)
- **Wiki**: [Termux Wiki](https://wiki.termux.com)
- **F-Droid**: [F-Droid Termux](https://f-droid.org/packages/com.termux/)
- **Reddit**: [r/termux](https://reddit.com/r/termux)

---

Termux verwandelt Ihr Android-Gerät in eine leistungsstarke, tragbare Linux-Workstation. Mit seinem umfangreichen Paket-Repository, SSH-Funktionen und Kompatibilität mit standardmäßigen Linux-Workflows ist es ein unverzichtbares Werkzeug für Entwickler, Systemadministratoren und alle, die die Kommandozeile gerne in der Tasche haben.