---
title: SpeedCool Magisk-Modul
description: Ein Magisk-Modul für Android, das Systemeinstellungen optimiert, um die Leistung zu steigern, den RAM-Verbrauch zu senken und das Wärmemanagement zu verbessern.
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

# SpeedCool Magisk-Modul

**SpeedCool** ist ein leichtes Open-Source-Magisk-Modul, erstellt von [Llucs](https://github.com/Llucs/SpeedCool-Magisk-Module). Es wendet automatisch eine umfassende Reihe von Kernel- und Systemoptimierungen beim Start an, um die Leistung zu steigern, den RAM-Verbrauch zu reduzieren und das Wärmemanagement auf jedem gerooteten Android-Gerät zu verbessern.

Im Gegensatz zu einem standardmäßigen Bloatware-Reiniger ändert SpeedCool die zugrunde liegende Systemkonfiguration, um die Grundursachen von Verzögerungen und Überhitzung zu beseitigen.

---

## Was es bewirkt

SpeedCool zielt auf mehrere wichtige Systembereiche ab:

- **CPU-Governor & Frequenzskalierung:** Reduziert die Aufwachverzögerung für anspruchsvolle Anwendungen (z.B. Spiele, Emulatoren).
- **Low Memory Killer (LMK):** Priorisiert das Halten der aktuell aktiven App im Speicher, während aggressiv Speicher von Hintergrund-Cache-Prozessen zurückgewonnen wird.
- **Thermal Engine:** Ändert thermische Drosselungspunkte, um eine dauerhafte Leistung gegen Wärmeentwicklung auszugleichen.
- **I/O-Scheduler:** Wechselt den Speicher-Scheduler zu einer Variante mit geringer Latenz für schnellere App-Ladezeiten.
- **Netzwerk-Stack:** Optimiert die TCP-Überlastungskontrolle für besseren Durchsatz in mobilen Netzwerken.
- **GPU-Rendering:** Aktiviert erzwungenes GPU-Rendering und optimiert den GPU-Governor.

---

## Warum verwenden?

- **Ruhigeres Spielen:** Bildraten sind stabiler aufgrund besserer CPU/GPU-Governor-Abstimmung und thermischer Drosselungskontrolle.
- **Schnelleres Multitasking:** Apps laden seltener neu dank optimierter LMK-Werte.
- **Kühlere Betriebstemperatur:** Intelligente thermische Profile verhindern, dass der SoC bei starker Nutzung kritische Temperaturen erreicht.
- **All-in-One-Optimierer:** Ersetzt die Notwendigkeit mehrerer widersprüchlicher Leistungsmodule.
- **Leichtgewichtig:** Das Modul ist typischerweise unter 1 MB groß und hat einen vernachlässigbaren Overhead.

---

## Installation

### Voraussetzungen

- Android-Gerät mit entsperrtem Bootloader und Root-Zugriff.
- **Magisk** (v20.0+) installiert.
- Benutzerdefinierte Wiederherstellung (TWRP) als Fallback empfohlen.

### Schritte

1. **Laden** Sie die neueste `SpeedCool-Magisk-Module.zip` von der [GitHub Releases-Seite](https://github.com/Llucs/SpeedCool-Magisk-Module/releases) herunter.
2. Öffnen Sie die **Magisk Manager**-App.
3. Navigieren Sie zum **Module**-Tab.
4. Tippen Sie auf **Aus Speicher installieren**.
5. Wählen Sie die heruntergeladene `.zip`-Datei aus.
6. Wischen Sie, um die Installation zu bestätigen.
7. **Starten** Sie Ihr Gerät neu, wenn Sie dazu aufgefordert werden.

> **Tipp:** Wenn Sie einen Bootloop erleben, starten Sie in den abgesicherten Modus (halten Sie während des Bootens die Lautstärke-Taste hoch) und deaktivieren Sie das Modul, oder entfernen Sie es manuell über die Wiederherstellung, indem Sie `/data/adb/modules/SpeedCool/` löschen.

---

## Verwendung & Überprüfung

SpeedCool ist so konzipiert, dass es vollständig im Hintergrund arbeitet. Es ist keine Benutzeroberfläche erforderlich. Sie können seinen Betrieb mit Terminalbefehlen überprüfen.

### Überprüfen des aktiven Status

Listen Sie das Modulverzeichnis auf, um zu bestätigen, dass es installiert ist:

```bash
su -c "ls -la /data/adb/modules/SpeedCool/"
```

Bei erfolgreicher Montage enthält das Verzeichnis die Moduldateien (`system.prop`, `service.sh`, `module.prop`).

### Überprüfen angewandter Systemeigenschaften

```bash
su -c "getprop | grep speed"
```

Suchen Sie nach Eigenschaften, die vom Modul injiziert wurden (z.B. `ro.sys.speedcool.version`).

---

## Hauptfunktionen mit Befehlsbeispielen

### 1. CPU-Governor-Abstimmung

Das Modul erzwingt einen Governor mit niedriger Latenz (normalerweise `performance`, `interactive` oder angepasst `schedutil`) auf allen CPU-Kernen.

```bash
# Check the current governor
su -c "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
```
*Erwartete Ausgabe:* `performance` oder `schedutil`

### 2. RAM-Optimierung (LMK)

Die Low Memory Killer-Schwellenwerte werden geändert, um die Vordergrund-App reaktionsschnell zu halten, während weniger nützliche Hintergrundprozesse aggressiv beendet werden.

```bash
# Check LMK values (adj, minfree)
su -c "cat /sys/module/lowmemorykiller/parameters/minfree"
su -c "cat /sys/module/lowmemorykiller/parameters/adj"
```

### 3. I/O-Scheduler-Optimierung

Der Block-Layer-Scheduler wird auf eine für interaktive Leistung optimierte Variante umgestellt (z.B. `bfq` oder `fiops`).

```bash
# Check the active scheduler for the main storage block device
su -c "cat /sys/block/mmcblk0/queue/scheduler"
```
*Erwartete Ausgabe:* `[bfq]` oder `[fiops]`

### 4. Netzwerkoptimierungen

Die TCP-Überlastungskontrolle wird auf einen Algorithmus umgestellt, der besser für mobile Netzwerke geeignet ist (z.B. `westwood` oder `bbr`).

```bash
# Check the active TCP congestion algorithm
su -c "cat /proc/sys/net/ipv4/tcp_congestion_control"
```
*Erwartete Ausgabe:* `westwood`

### 5. Anzeigen von Modulprotokollen

Wenn das Debugging im Modulskript aktiviert ist, können Sie das Systemprotokoll filtern.

```bash
su -c "logcat -d | grep SpeedCool"
```

### 6. Lesen des Modulprofils (falls konfigurierbar)

Einige Versionen erlauben es, ein Profil durch Bearbeiten von `service.sh` auszuwählen. Überprüfen Sie die verfügbaren Kommentare in der Datei:

```bash
su -c "head -50 /data/adb/modules/SpeedCool/service.sh"
```

---

## Fehlerbehebung

| Symptom | Wahrscheinliche Ursache | Lösung |
|---|---|---|
| **Bootloop** | Konfliktmodul oder inkompatibles Gerät. | Halten Sie während des Bootens die Lautstärke-Taste hoch, um das Modul zu deaktivieren, oder entfernen Sie das Verzeichnis `/data/adb/modules/SpeedCool` im TWRP-Dateimanager. |
| **Keine Leistungsänderung** | Konfliktmodule (LKT, FDE.AI, NFS). | Entfernen Sie alle anderen Leistungsmodule, bevor Sie SpeedCool verwenden. |
| **Gerät wird immer noch heiß** | Thermische Grenzen sind zu aggressiv. | Überprüfen Sie die Thermal-Engine-Konfiguration im Modul oder versuchen Sie ein anderes Profil. |
| **Apps stürzen ab** | Zu aggressive LMK-Werte. | Passen Sie die `minfree`-Werte in `service.sh` manuell an. |

---

## Deinstallation

1. Öffnen Sie **Magisk Manager**.
2. Gehen Sie zum **Module**-Tab.
3. Tippen Sie auf das **Entfernen**-Symbol (Papierkorb) neben SpeedCool.
4. Tippen Sie auf **Neustarten**.

**Alternative Befehlszeilen-Deinstallation:**

```bash
su -c "rm -rf /data/adb/modules/SpeedCool/"
reboot
```

---

## Referenzen

- **GitHub Repository:** [Llucs/SpeedCool-Magisk-Module](https://github.com/Llucs/SpeedCool-Magisk-Module)
- **Magisk Official Docs:** [topjohnwu.github.io/Magisk/](https://topjohnwu.github.io/Magisk/)
- **XDA Developers:** Suchen Sie nach *SpeedCool* oder *Llucs* für Community-Support-Diskussionen.

> **Haftungsausschluss:** Das Ändern von Systemparametern birgt ein inhärentes Risiko. Führen Sie immer ein vollständiges Nandroid-Backup durch, bevor Sie Leistungsmodule installieren. Die Autoren übernehmen keine Verantwortung für Schäden, die an Ihrem Gerät entstehen.