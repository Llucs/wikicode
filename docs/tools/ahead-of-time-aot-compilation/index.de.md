---
title: Ahead-of-Time (AOT)-Kompilierung
description: Eine Build-Optimierungstechnik, bei der Code vor der Laufzeit kompiliert wird, um die Performance, den sofortigen Start und kleinere Bereitstellungen zu verbessern.
created: 2026-06-21
tags:
  - compilation
  - aot
  - native-image
  - performance
  - graalvm
  - dotnet
  - go
  - rust
status: draft
---

# Ahead-of-Time (AOT)-Kompilierung

## Was ist Ahead-of-Time-Kompilierung?

Ahead-of-Time (AOT)-Kompilierung ist der Prozess, bei dem Quellcode einer höheren Programmiersprache oder eine Zwischendarstellung (wie .NET IL, Java-Bytecode oder LLVM IR) **vor** der Ausführung, typischerweise zur Build-Zeit, in nativen Maschinencode übersetzt wird. Dies steht im Gegensatz zur Just-in-Time (JIT)-Kompilierung, die zur Laufzeit erfolgt.

Sprachen wie C, C++, Go und Rust sind von Natur aus AOT-kompiliert. Moderne verwaltete Sprachen unterstützen AOT ebenfalls durch spezialisierte Toolchains, wie GraalVM Native Image für Java, NativeAOT für .NET und Angular AOT für TypeScript.

## Warum AOT-Kompilierung verwenden?

AOT bietet mehrere wesentliche Vorteile gegenüber JIT- oder interpretierter Ausführung:

- **Sofortiger Start** – Keine Aufwärmphase; nativer Code wird sofort ausgeführt.
- **Deterministische Leistung** – Keine JIT-Pausen während der Ausführung, was die Latenz in den Schwanzzeiten reduziert.
- **Geringerer Speicherverbrauch** – Kein JIT-Compiler oder Laufzeit-Kompilierungsdaten erforderlich.
- **Kleinere Bereitstellungen** – Statisch gelinkte, einzelne ausführbare Dateien führen zu minimalen Container-Images.
- **Cold-Start-Optimierung** – Unverzichtbar für serverlose, Edge- und containerisierte Anwendungen.

## Installation

Die AOT-Toolchain variiert je nach Plattform. Im Folgenden sind gängige Einrichtungen aufgeführt:

### GraalVM Native Image (Java)

1. Laden Sie GraalVM von [graalvm.org](https://graalvm.org) herunter.
2. Setzen Sie `JAVA_HOME` und fügen Sie `bin` zum `PATH` hinzu.
3. Installieren Sie das `native-image`-Tool:
   ```bash
   gu install native-image
   ```

### .NET NativeAOT

Erfordert .NET 7 oder höher (volle Unterstützung ab .NET 8+). Die Workload ist im SDK enthalten.

### Go (standardmäßig AOT)

Keine zusätzliche Installation – der standardmäßige `go`-Compiler führt AOT aus.

### Rust (standardmäßig AOT)

Installation über `rustup` (z.B. `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`).

## Verwendung

### Java mit GraalVM Native Image

```bash
native-image -jar myapp.jar myapp-native
```

Beispielausgabe:
```
================================================================================
GraalVM Native Image: Generating 'myapp-native' (executable)...
================================================================================
```

### .NET NativeAOT

```bash
dotnet publish -c Release -r linux-x64 -p:PublishAot=true
```

Die Ausgabe ist eine eigenständige native ausführbare Datei im Verzeichnis `bin/Release/net8.0/linux-x64/publish/`.

### Go (implizites AOT)

```bash
go build -o myapp main.go
```

Das erzeugte Binary ist in sich geschlossen und läuft sofort ohne Laufzeitumgebung.

### Rust

```bash
cargo build --release
```

Das resultierende Binary in `target/release/` ist AOT-kompiliert und profitiert oft von profilgesteuerter Optimierung (PGO) für eine noch bessere Leistung.

## Hauptmerkmale

### 1. Null Aufwärmzeit

Da der gesamte Code bereits kompiliert ist, starten Anwendungen sofort und erreichen sofort die Spitzenleistung.

*Beispiel (Java):*
```bash
time java -jar myapp.jar      # JIT – may take seconds
time ./myapp-native           # AOT – starts in milliseconds
```

### 2. Deterministische Latenz

Keine GC- und JIT-bedingte Pausen. Entscheidend für Echtzeitsysteme, Handelsplattformen und Hochfrequenzhandel.

### 3. Geringerer Speicherverbrauch

- **GraalVM Native Image** kann die Image-Größe von >200 MB (JVM+App) auf <20 MB reduzieren.
- **.NET NativeAOT** erzeugt Binaries, die nur die notwendigen Laufzeitkomponenten enthalten.

### 4. Eliminierung von Totem Code

AOT-Analyzer entfernen unerreichbaren Code, was zu kleineren ausführbaren Dateien und verbesserter Sicherheit führt.

### 5. Profilgesteuerte Optimierung (PGO)

In Kombination mit AOT können Profildaten, die bei Testläufen gesammelt wurden, zur Build-Zeit verwendet werden, um das Binary weiter zu optimieren.

*Beispiel (Rust):*
```bash
RUSTFLAGS="-Cprofile-generate=/tmp/pgo-data" cargo build --release
# Run training workload
RUSTFLAGS="-Cprofile-use=/tmp/pgo-data" cargo build --release
```

## Einschränkungen

- **Reflection / Dynamisches Laden** – Muss explizit konfiguriert werden (z.B. `reflect-config.json` für Native Image).
- **Build-Zeit** – AOT-Kompilierung ist langsamer als JIT.
- **Spitzenleistung** – Laufzeit-JIT mit Profiling kann bei CPU-intensiven Workloads immer noch besser sein als AOT.
- **Unterstützung** – Nicht alle Bibliotheken und Frameworks sind AOT-kompatibel.

## Fazit

AOT-Kompilierung ist eine grundlegende Technik für moderne cloud-native, serverlose und Edge-Anwendungen. Durch den Verzicht auf etwas Laufzeitflexibilität bietet sie unübertroffene Startgeschwindigkeit, vorhersagbare Leistung und minimale Ressourcennutzung. Tools wie GraalVM Native Image, .NET NativeAOT, Go und Rust machen AOT für den Produktionseinsatz zugänglich und praktikabel.