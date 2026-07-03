---
title: Ghostty - Ein schneller und vielfunktionaler Terminal-Emulator
description: Ghostty ist ein schneller, vielfunktionaler und Plattformübergreifender Terminal-Emulator, der platform-native UI und GPU-Acceleration verwendet.
created: 2026-07-03
tags:
  - terminal
  - Emulator
  - Produktivität
  - Befehlszeilen
  - Plattformübergreifend
status: draft
---

# Ghostty - Ein schneller und vielfunktionaler Terminal-Emulator

Ghostty ist ein schneller, vielfunktionaler und Plattformübergreifender Terminal-Emulator, der platform-native UI und GPU-Acceleration verwendet. Er ist so konzipiert, dass er eine hervorragende Ersatzlösung für Ihren aktuellen Terminal-Emulator auf macOS und Linux darstellt. Ghostty wurde vom Co-Gründer von HashiCorp, Mitchell Hashimoto, entwickelt und zielt auf das neue Leistungsstandard in der Zukunft ab.

## Was ist Ghostty?

Ghostty ist kein Tool zum Erstellen von Projekten oder zum Aufbauen von Anwendungen, sondern ein Terminal-Emulator, der eine moderne und effiziente Benutzeroberfläche anbietet. Er bietet ein schnelles und reaktives Benutzererlebnis mit GPU-Acceleration und einer nativen Benutzeroberfläche, was ihn für Entwickler zu einem hervorragenden Wahlkandidaten für eine verbesserte Produktivität in der Terminal-Umgebung macht.

## Kernfunktionen

- **Plattform-nahe UI**: Bietet eine moderne und intuitive Benutzeroberfläche.
- **GPU-Acceleration**: Verbessert die Leistung und Reaktivität.
- **Plattformübergreifende Unterstützung**: Funktioniert ohne Probleme auf macOS, Linux und Windows.
- **Schnell**: Bietet eine Blitzschnelle Leistung, auch bei komplexen Befehlen und großen Dateioperationen.
- **Vielfunktional**: Enthält fortgeschrittene Funktionen wie gestaffelte Terminals, mehrere Paneelen und mehr.

## Geschichte

Ghostty wurde vom Ghost-Team entwickelt, das sich darauf konzentriert, den Prozess der Erstellung von Inhaltshandels-Systemen und Webanwendungen zu vereinfachen. Mitchell Hashimoto, ehemaliger CEO und CTO von HashiCorp, ist der Hauptentwickler von Ghostty und ist bemüht, das Terminal-Emulator-Experience zu verbessern.

## Einsatzbereiche

Ghostty wird hauptsächlich im Terminal-Umfeld für das Interagieren mit Befehlszeilen-Werkzeugen, das Verwalten von Prozessen und das Ausführen von Skripten verwendet. Er ist besonders für Entwickler und Systemadministratoren nützlich, die einen schnellen und effizienten Terminal-Emulator benötigen.

## Installation

Um Ghostty zu installieren, folgen Sie diesen Schritten:

1. **Node.js installieren**: Stellen Sie sicher, dass Node.js auf Ihrem System installiert ist. Ghostty wird mit Node.js erstellt.
2. **Ghostty installieren**: Öffnen Sie den Terminal und führen Sie den folgenden Befehl aus:

   ```sh
   npm install -g ghostty
   ```

   Alternativ können Sie es mit Yarn installieren:

   ```sh
   yarn global add ghostty
   ```

## Grundlegende Verwendung

Sobald es installiert ist, können Sie Ghostty zum Interagieren mit Ihrem Terminal verwenden. Hier sind einige grundlegende Befehle:

1. **Ghostty starten**: Öffnen Sie Ghostty, indem Sie den Befehl ausführen:

   ```sh
   ghostty
   ```

2. **Neues Terminal öffnen**: Öffnen Sie ein neues Terminalfenster innerhalb von Ghostty:

   ```sh
   ghostty new-terminal
   ```

3. **Aktuelles Terminal schließen**: Beenden Sie das aktuelle Terminalfenster:

   ```sh
   ghostty close-terminal
   ```

4. **Zwischen Terminals wechseln**: Verwenden Sie die Tab-Taste, um zwischen offenen Terminals zu wechseln:

   ```sh
   ghostty switch-terminal
   ```

5. **Datei öffnen**: Öffnen Sie eine Datei im Terminal:

   ```sh
   ghostty open-file /pfad/zur/datei.txt
   ```

6. **Befehl im Terminal ausführen**: Führen Sie einen Befehl im Terminal aus:

   ```sh
   ghostty run-command ls -l
   ```

7. **Ghostty beenden**: Verlassen Sie Ghostty, indem Sie `Ctrl + D` drücken oder den Befehl ausführen:

   ```sh
   ghostty exit
   ```

## Schlussfolgerung

Ghostty ist ein mächtiger und effizienter Terminal-Emulator, der eine moderne und reaktive Benutzeroberfläche anbietet. Er ist so konzipiert, dass er die Produktivität im Terminal-Umfeld erhöht und ist eine wertvolle Wahl für Entwickler und Systemadministratoren, die einen schnellen und vielfunktionalen Terminal-Emulator suchen.

Für weitere Informationen und eine Explorierung zusätzlicher Funktionen, besuchen Sie die [offizielle Ghostty-GitHub-Repository](https://github.com/mitchellh/ghostty).