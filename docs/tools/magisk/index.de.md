---
title: Magisk – Systemloser Root- und Modulmanager für Android
description: Magisk ist ein beliebtes Android-Rooting-Tool, das systemlosen Root-Zugriff und Modulunterstützung für Systemmodifikationen bietet.
created: 2026-06-19
tags:
  - android
  - root
  - systemless
  - magisk
  - tool
status: draft
---

# Magisk – Systemloser Root- und Modulmanager für Android

## Was ist Magisk?

Magisk ist eine Open-Source-Softwaresuite, die von **John Wu (topjohnwu)** entwickelt wurde und **systemloses Rooten** sowie tiefgehende Anpassungen von Android-Geräten ermöglicht. Im Gegensatz zu traditionellen Rooting-Methoden, die die unveränderliche `/system`-Partition modifizieren, arbeitet Magisk, indem es das Boot-Image (oder die `init_boot`-Partition bei neueren Geräten) patcht, um beim Booten ein Overlay-Dateisystem zu erstellen. Dies erlaubt Root-Zugriff, Boot-Skripte, SELinux-Richtlinien-Patches und Module zu laden, **ohne Systemdateien dauerhaft zu verändern**.

Ursprünglich 2016 veröffentlicht, wurde Magisk schnell zur Standard-Android-Rooting-Lösung und ersetzte ältere Werkzeuge wie SuperSU. Es wird weiterhin aktiv gewartet und sowohl für grundlegendes Rooten als auch für fortgeschrittene Gerätemodifikationen eingesetzt.

---

## Warum Magisk verwenden?

| Nutzen | Beschreibung |
|---------|-------------|
| **Systemlose Änderungen** | OTA-Updates bleiben erhalten, da `/system` unberührt bleibt. |
| **MagiskSU** | Reine Open-Source-Root-Berechtigungsverwaltung (gewähren, nachfragen, verweigern). |
| **Modulsystem** | Installiere Tweaks (Audio-Mods, Kamera-Bibliotheken, Werbeblocker, Schriftarten) ohne Neupartitionierung. |
| **Zygisk** | Code-Injektion in jeden App-Prozess über Zygote – ersetzt MagiskHide. |
| **DenyList** | Root, Module und entsperrten Bootloader vor bestimmten Apps verstecken (Banking, Streaming). |
| **MagiskBoot** | Leistungsstarkes Werkzeug zum Entpacken, Modifizieren und Neuverpacken von Android-Boot-Images. |
| **Aktive Community** | Tausende Module und umfangreiche Dokumentation verfügbar. |

Magisk ist unverzichtbar für Nutzer, die Root-Zugriff für erweiterte Backup-Tools, Automatisierung (Tasker), benutzerdefinierte System-Tweaks oder zur Wiederherstellung von Funktionen in Apps benötigen, die gerootete Geräte blockieren.

---

## Installationsanleitung

### Voraussetzungen

- **Entsperrter Bootloader** (gerätespezifisch, erfordert oft OEM-Entsperrung).
- **Funktionierendes ADB und Fastboot** auf Ihrem Computer.
- **Geräte-Factory-Image** oder das originale `boot.img` (und möglicherweise `init_boot.img`).
- **Sichern** Sie alle wichtigen Daten.

### Schritt 1 – Boot-Image extrahieren

Besorgen Sie sich das Factory-Image für Ihr Gerät (z. B. von der Google Factory Images-Seite) und extrahieren Sie das Boot-Image.

```bash
# Example for a Pixel device
unzip [device]_[build].zip
cd [device]_[build]
unzip image-[device]-[build].zip
# boot.img is now in the current directory
```

Bei Geräten mit Android 13+ (z. B. Pixel 6-Serie) ist die Root-Partition `init_boot.img` anstelle von `boot.img`.

### Schritt 2 – Image mit der Magisk-App patchen

1. Installieren Sie die neueste Magisk APK auf Ihrem Gerät.
2. Öffnen Sie die Magisk-App, tippen Sie auf **Installieren** → **Datei auswählen und patchen**.
3. Wählen Sie das extrahierte `boot.img` (oder `init_boot.img`).
4. Die App wird das Image patchen und eine neue Datei namens `magisk_patched-XXXXX.img` speichern (normalerweise in `Download/`).

### Schritt 3 – Das gepatchte Image flashen

Übertragen Sie das gepatchte Image auf Ihren Computer und starten Sie Ihr Gerät dann im Fastboot-Modus.

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

### Schritt 4 – Installation überprüfen

Nach dem Neustart öffnen Sie die Magisk-App. Der **Startbildschirm** sollte die installierte Magisk-Version und „Installiert“ neben dem Magisk-Status anzeigen.

---

## Grundlegende Verwendung

### Magisk-App-Oberfläche

- **Superuser-Tab** (Schild-Symbol): Listet alle Apps auf, die Root-Berechtigungen angefordert haben. Tippen Sie auf einen Eintrag, um seinen Berechtigungsstatus zu ändern (Gewähren / Nachfragen / Verweigern).
- **Module-Tab** (Puzzleteil-Symbol): Zeigt installierte Module an. Tippen Sie auf die **+**-Taste, um ein neues Modul aus einer auf Ihrem Gerät gespeicherten `.zip`-Datei zu installieren. Verwenden Sie den Schalter, um ein Modul zu aktivieren/deaktivieren (die meisten erfordern einen Neustart).
- **Einstellungen-Tab** (Zahnrad-Symbol):
  - **Zygisk**: Zygisk aktivieren oder deaktivieren (erfordert Neustart).
  - **DenyList**: Konfigurieren, vor welchen Apps Magisk versteckt werden soll (erfordert Zygisk und einen Neustart).
  - **Update-Kanal**: Wählen Sie Stabil, Beta oder Canary für App- und Magisk-Updates.
  - **Automatische Antwort**: Legen Sie das Standardverhalten für Root-Berechtigungen fest.

### Modulverwaltung

Module werden als standardmäßige ZIP-Archive installiert. Sie können einfache Skripte, Binärdateien oder vollständige System-Overlay-Verzeichnisse enthalten.

```bash
# Typical module ZIP structure (inside /data/adb/modules/<module_id>/)
module.prop          # Metadata (id, name, version, author)
system/              # Files to overlay on /system
post-fs-data.sh      # Script run early in boot
service.sh           # Script run later in boot
```

Um ein Modul manuell zu installieren:

1. Laden Sie das Modul-`.zip` auf Ihr Gerät herunter.
2. Öffnen Sie die Magisk-App → Module-Tab → **Aus Speicher installieren**.
3. Wählen Sie die Datei aus, bestätigen Sie und starten Sie dann bei Aufforderung **neu**.

### Magisk deinstallieren

Die Magisk-App bietet eine direkte Möglichkeit, Root vollständig zu entfernen:

1. Öffnen Sie die Magisk-App.
2. Tippen Sie unten im Startbildschirm auf **Magisk deinstallieren**.
3. Bestätigen Sie – die App stellt das originale, ungepatchte Boot-Image wieder her und startet neu.

---

## Hauptfunktionen

### MagiskSU

Ein vollständiger Ersatz für `su`, der vollständig quelloffen ist. Es implementiert ein Berechtigungsmodell mit den Optionen Gewähren / Nachfragen / Verweigern und protokolliert alle Root-Zugriffe. MagiskSU ist mit allen vorhandenen Apps kompatibel, die Root benötigen.

### Magisk-Module

Ein standardisiertes Format zur Verteilung von Systemmodifikationen, ohne die Systempartition zu berühren. Module werden beim Booten über das Magisk-Overlay-Dateisystem geladen. Tausende Module existieren in Foren wie XDA und dem Magisk-Repository.

### Zygisk

Zygisk ist Magisks Implementierung von Code-Injektion in den Zygote-Prozess. Es ermöglicht Laufzeitmodifikationen innerhalb jedes App-Prozesses. Zygisk ersetzt die ältere MagiskHide-Funktionalität.

### DenyList

Wenn Zygisk aktiviert ist, können Sie eine **DenyList** von Apps konfigurieren, vor denen Magisk seine Präsenz verbirgt (Root, Module, entsperrter Bootloader). Dies ist die moderne Methode, um Integritätsprüfungen zu umgehen, die von Banking-, Zahlungs- und Streaming-Apps verwendet werden.

### MagiskBoot

MagiskBoot ist ein Low-Level-Werkzeug für die Arbeit mit Boot-Images. Es kann sie entpacken, modifizieren und neu verpacken, ohne eine vollständige Android-Umgebung zu benötigen. Es wird oft direkt auf einem Computer verwendet, um gepatchte Images ohne die App zu erstellen.

---

## Befehlsbeispiele

### Gepatchtes Boot-Image flashen (fastboot)

```bash
fastboot flash boot magisk_patched-27000.img
fastboot reboot
```

### init_boot für neuere Geräte flashen

```bash
fastboot flash init_boot magisk_patched-27000.img
fastboot reboot
```

### MagiskBoot verwenden, um ein Boot-Image zu entpacken

```bash
magiskboot unpack boot.img
# This creates: kernel, kernel_dtb, ramdisk.cpio, header, etc.
```

### Ein modifiziertes Boot-Image mit MagiskBoot neu verpacken

```bash
magiskboot repack boot.img
# Creates new-boot.img with your modifications.
```

### Boot-Image-Header überprüfen

```bash
magiskboot info boot.img
```

### Ein Boot-Image mit Magisk patchen (Kommandozeile)

```bash
magiskboot boot.img
# Creates patched_boot.img in the current directory.
```

### Magisk vor einer App verstecken (DenyList)

Öffnen Sie die Magisk-App → Einstellungen → **DenyList konfigurieren** → fügen Sie die Ziel-App hinzu (z. B. `com.google.android.gms` für Google Play Dienste). Nach einem Neustart ist Magisk für diese App unsichtbar.

---

## Tipps und Hinweise

- **OTA-Updates** bleiben kompatibel, da Magisk nur die Boot-Partition modifiziert. Nach einem OTA müssen Sie Magisk jedoch **erneut flashen** in das neue Boot-Image.
- **SafetyNet / Play Integrity** – Obwohl Magisk selbst keine Integritätsumgehung bietet, können Tools wie Zygisk-Assistant oder Shamiko-Module helfen, Root vor den Attestierungsprüfungen von Google zu verstecken.
- **Modulkonflikte** – Einige Module können sich gegenseitig beeinträchtigen; deaktivieren Sie sie einzeln, um Probleme zu isolieren.
- **Backups** – Bewahren Sie immer eine Kopie des originalen Stock-Boot-Images auf. Wenn etwas schiefgeht, können Sie es über Fastboot wiederherstellen.
- **Magisk Canary** – Der Canary-Kanal enthält manchmal instabile Funktionen. Verwenden Sie ihn nur zu Testzwecken.

---

## Referenzen

- [Magisk GitHub-Repository](https://github.com/topjohnwu/Magisk)
- [Offizielle Magisk-Dokumentation (Entwicklerleitfäden)](https://topjohnwu.github.io/Magisk/)
- [Magisk-Modul-Repository (inoffiziell)](https://www.androidacy.com/modules-repository/)
- [XDA Developers – Magisk Diskussion & Support](https://forum.xda-developers.com/f/magisk.5903/)

---

*Dieses Dokument ist Teil des Entwicklerwikis. Kommentare und Verbesserungen sind willkommen.*