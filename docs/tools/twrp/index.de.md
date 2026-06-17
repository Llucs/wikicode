---
title: Team Win Recovery Project (TWRP)
description: TWRP ist eine quelloffene benutzerdefinierte Wiederherstellung für Android, die das Flashen benutzerdefinierter ROMs, vollständige Geräte-Backups (NANDroid) und Systemmodifikationen über eine Touchscreen-Schnittstelle ermöglicht.
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

TWRP (Team Win Recovery Project) ist ein **quelloffenes benutzerdefiniertes Wiederherstellungsabbild** für Android-basierte Geräte. Es ersetzt die Standard-Wiederherstellungspartition, um eine funktionsreiche, touchscreen-gesteuerte Umgebung für die Installation von Drittanbieter-Firmware, das Erstellen vollständiger System-Backups und die Durchführung fortgeschrittener Systemverwaltungsaufgaben zu bieten – alles ohne in Android booten zu müssen.

## Warum TWRP?

Die Standard-Android-Wiederherstellung ist auf Zurücksetzen auf Werkseinstellungen und OTA-Updates beschränkt. TWRP eröffnet dem Gerät folgende Möglichkeiten:

- **Installation benutzerdefinierter ROMs** (LineageOS, Pixel Experience, etc.)
- **Vollständige System-Backups und -Wiederherstellungen** (NANDroid) – essentiell vor riskanten Modifikationen.
- **Rooten** (Flashen von Magisk oder SuperSU).
- **Partitionsverwaltung** (Löschen, Formatieren, Größe ändern).
- **Handhabung von Verschlüsselung** (Entschlüsseln von Benutzerdaten unter bestimmten Bedingungen).
- **ADB-Sideloading und MTP** zum Übertragen von Dateien oder Flashen ohne Speicher.

TWRP ist der De-facto-Standard für Android-Enthusiasten und -Entwickler; es hat frühere Wiederherstellungen wie ClockworkMod (CWM) aufgrund seiner intuitiven Oberfläche und aktiven Community-Unterstützung ersetzt.

## Hauptfunktionen

- **Touch-GUI** – Vollständige Touch-Unterstützung mit Bildschirmtastatur, Dateimanager und Terminalemulator.
- **NANDroid-Backup** – Klont ganze Partitionen (Boot, System, Data, EFS/IMEI) nach `/sdcard/TWRP/BACKUPS/`.
- **ZIP-Flashen** – Installiert benutzerdefinierte Firmware-Pakete (ROMs, Kernel, Mods, GApps, Magisk).
- **Erweitertes Löschen** – Einzelne Partitionen löschen, „Daten formatieren“, um Verschlüsselung zu entfernen.
- **Dateimanager** – Dateien auf dem Dateisystem des Geräts durchsuchen und ändern.
- **ADB-Sideload** – ZIP-Dateien von einem Computer über USB flashen.
- **MTP-Unterstützung** – Zugriff auf Gerätespeicher als Wechseldatenträger im Wiederherstellungsmodus.
- **Verschlüsselungsunterstützung** – Kann Benutzerdaten mit PIN/Passwort/Muster entschlüsseln (ältere Verschlüsselungen; FBE auf modernen Geräten wird oft nicht unterstützt).
- **Theming** – Anpassbare Benutzeroberfläche über `.twres`-Themes.
- **Screenshot** – Bildschirm im Wiederherstellungsmodus aufnehmen.

## Geschichte

Erstellt von *Dees_Troy* um 2011, wurde TWRP aufgrund seiner proprietären Touchscreen-Oberfläche schnell zur beliebtesten benutzerdefinierten Wiederherstellung. Es entwickelte sich von einem Holo-Design zu einer Material-Design-Oberfläche (Version 3.0+). Heute wird es von einem Kernteam gewartet und unterstützt Hunderte offiziell gelisteter Geräte auf [twrp.me](https://twrp.me).

## Installation

> **Voraussetzungen:**
> - Entsperrter Bootloader (für die meisten Geräte erforderlich).
> - ADB- und Fastboot-Tools auf Ihrem PC installiert.
> - Korrektes TWRP-Abbild für Ihr genaues Gerätemodell (Codenamen auf twrp.me überprüfen).

### Allgemeine Fastboot-Methode (die meisten Geräte)

1. **Neu starten in den Bootloader:**
   ```bash
   adb reboot bootloader
   ```
2. **Wiederherstellungsabbild flashen:**
   ```bash
   fastboot flash recovery twrp-<version>.img
   ```
3. **Sofort in die Wiederherstellung booten** (bevor das System startet, das TWRP überschreiben könnte):
   ```bash
   fastboot reboot recovery
   # oder Tastenkombination verwenden (Lautstärke hoch + Ein/Aus, usw.)
   ```

### Geräte mit Slots (A/B-Partitionen – z. B. Pixel, OnePlus)

Da das System die Wiederherstellungspartition beim nächsten Start automatisch ersetzen kann, verwenden Sie eine temporäre Boot-Methode:

1. **TWRP-Abbild temporär booten:**
   ```bash
   fastboot boot twrp-<version>.img
   ```
2. **Gehen Sie in TWRP zu** *Erweitert → Wiederherstellungs-Ramdisk installieren*.
   - Dadurch wird TWRP in den inaktiven Slot geflasht und verhindert, dass es überschrieben wird.

### Samsung-Geräte (über Odin)

1. Laden Sie die `.tar`-TWRP-Datei herunter (normalerweise benannt `twrp-<version>-<device>.tar`).
2. Öffnen Sie Odin, legen Sie die Datei in den **AP**-Slot.
3. Deaktivieren Sie **Auto-Neustart** in den Odin-Optionen.
4. Flashen und dann sofort mit der Tastenkombination (Lautstärke hoch + Home + Ein/Aus) in die Wiederherstellung booten, um die Wiederherstellung der Standard-Wiederherstellung zu verhindern.

### Von einem gerooteten Gerät (mit der offiziellen TWRP-App)

1. Installieren Sie die **offizielle TWRP-App** aus dem Play Store oder von twrp.me.
2. Root-Berechtigungen erteilen.
3. Wählen Sie Ihr Gerät aus und flashen Sie das neueste Abbild.

### Vom Terminal (gerootet)

```bash
su
dd if=/sdcard/twrp.img of=/dev/block/bootdevice/by-name/recovery
```

Ersetzen Sie den Pfad durch den Speicherort Ihrer Wiederherstellungspartition (variiert je nach Gerät – finden Sie mit `parted` oder `ls /dev/block/platform/...`).

## Grundlegender Arbeitsablauf

### Wiederherstellung starten

- Verwenden Sie die Tastenkombination (variiert je nach Hersteller, oft **Lautstärke leiser + Ein/Aus**).
- Oder von Android aus (wenn gerootet/Bootloader entsperrt): `adb reboot recovery`.

### Löschen von Partitionen

- **Factory Reset** (Daten/Cache löschen) – erforderlich vor der Installation eines neuen ROMs.
  - *Löschen → Wischen, um auf Werkseinstellungen zurückzusetzen*
- **Daten formatieren** – entfernt Verschlüsselung und löscht den internen Speicher.
  - *Löschen → Daten formatieren → „yes“ eingeben*
- **Erweitertes Löschen** – einzelne Partitionen zum Löschen auswählen.

### Installieren eines Zips (ROM, GApps, Magisk, etc.)

1. Tippen Sie auf **Installieren**.
2. Navigieren Sie zur `.zip`-Datei (normalerweise auf `/sdcard` oder externer SD).
3. Tippen Sie auf die Datei; tippen Sie optional auf **Weitere Zips hinzufügen**, um mehrere Dateien in die Warteschlange zu stellen.
4. **Wischen, um das Flashen zu bestätigen**.
5. *(Optional)* System neu starten.

> Beispielbefehl für Sideload:
> ```bash
> adb sideload custom_rom.zip
> ```

### Sichern (NANDroid)

1. Tippen Sie auf **Sichern**.
2. Wählen Sie Partitionen aus:
   - **Boot**, **System**, **Daten** (Minimum für eine vollständige Systemwiederherstellung).
   - **EFS** (speichert IMEI – entscheidend für einige Geräte).
3. Wischen, um die Sicherung zu starten.
4. Die Sicherung wird in `/sdcard/TWRP/BACKUPS/<device_serial>/` gespeichert.

### Wiederherstellen eines Backups

1. Tippen Sie auf **Wiederherstellen**.
2. Wählen Sie ein Backup aus der Liste aus.
3. Markieren Sie die Partitionen, die Sie wiederherstellen möchten.
4. Wischen, um zu bestätigen.

### Dateimanager & Terminal

- **Dateimanager**: *Erweitert → Dateimanager* – Dateien navigieren, löschen, umbenennen, kopieren.
- **Terminal**: *Erweitert → Terminal* – Befehle als root ausführen.

## Beispielbefehle (Fastboot & ADB)

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

## Wichtige Warnungen

- **Gerätespezifische Abbilder** – Das Flashen eines TWRP-Abbilds für ein anderes Modell kann Ihr Gerät **zerstören** (Hard Brick). Überprüfen Sie immer den Codenamen (z. B. `beryllium` für Pocophone F1).
- **A/B-Slot-Verwirrung** – Bei Geräten mit nahtlosen Updates muss TWRP in beiden Slots installiert sein. Wenn einem Slot TWRP fehlt, kann das Gerät zur Standard-Wiederherstellung zurückkehren.
- **Verschlüsselungsprobleme** – Modernes Android verwendet **dateibasierte Verschlüsselung (FBE)**. TWRP kann Benutzerdaten oft nicht entschlüsseln. Benutzer müssen häufig **Daten formatieren** (löscht den internen Speicher) beim Wechsel von ROMs oder wenn TWRP `/data` nicht einbinden kann.
- **OTAs mit benutzerdefinierter Wiederherstellung** – Standard-OTA-Updates schlagen mit TWRP in der Regel fehl. Sie müssen entweder:
  - Das OTA-ZIP manuell über TWRP flashen.
  - Oder vor dem Anwenden des OTA zur Standard-Wiederherstellung zurückkehren.
- **Play Integrity / Banking-Apps** – Ein entsperrter Bootloader (für TWRP erforderlich) deaktiviert viele Sicherheitsprüfungen. Rooten mit Magisk kann dies verbergen, erhöht aber die Komplexität und ist nicht immer erfolgreich.
- **Sicherung vor Änderungen** – Erstellen Sie immer ein NANDroid-Backup, bevor Sie ein neues ROM oder riskantes Mod flashen. Ein vollständiges Backup kann einen Soft Brick in Minuten beheben.

## Fehlerbehebung

| Problem | Lösung |
|--------|----------|
| TWRP bleibt nach einem Neustart nicht erhalten | Verwenden Sie `fastboot boot` und dann „Wiederherstellungs-Ramdisk installieren“ (A/B-Geräte). Alternative: Neu flashen und sofort in die Wiederherstellung booten. |
| `/data` kann nicht eingebunden werden | Wahrscheinlich verschlüsselt. Gehen Sie zu *Löschen → Daten formatieren* und geben Sie „yes“ ein. **Dies löscht den gesamten internen Speicher.** |
| Gerät bleibt nach dem Flashen beim Bootlogo hängen | Versuchen Sie, Dalvik/ART-Cache und Cache zu löschen. Wenn es weiterhin fehlschlägt, stellen Sie ein vorheriges Backup wieder her. |
| ADB Sideload bleibt bei „senden“ hängen | Stellen Sie sicher, dass Sie die neuesten ADB-Treiber haben. Versuchen Sie ein anderes USB-Kabel/einen anderen Anschluss. |
| TWRP startet nicht (schwarzer Bildschirm) | Das Abbild könnte beschädigt oder falsch sein. Laden Sie es von der offiziellen Seite erneut herunter. |

## Zusätzliche Ressourcen

- **Offizielle Seite & Downloads:** [https://twrp.me](https://twrp.me)
- **Quellcode:** [https://github.com/TeamWin/Team-Win-Recovery-Project](https://github.com/TeamWin/Team-Win-Recovery-Project)
- **XDA-Foren:** Suchen Sie nach dem spezifischen Forenthread für Ihr Gerät für TWRP-Builds und Support.
- **TWRP aus dem Quellcode kompilieren:** [https://github.com/TeamWin/Team-Win-Recovery-Project/blob/android-12.1/README.md](https://github.com/TeamWin/Team-Win-Recovery-Project/blob/android-12.1/README.md)

TWRP ist ein leistungsstarkes Werkzeug für jeden Android-Entwickler oder -Enthusiasten. Verwenden Sie es mit Bedacht und halten Sie immer ein Backup bereit.