---
title: Heimdall - Herramienta de Flasheo de Firmware Samsung
description: Suite de herramientas de código abierto y multiplataforma para flashear firmware (ROMs) en dispositivos móviles Samsung.
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

## ¿Qué es Heimdall?

Heimdall es una suite de herramientas multiplataforma y de código abierto diseñada para flashear firmware (ROMs de stock, ROMs personalizadas, bootloaders e imágenes de recuperación) en dispositivos Samsung Android. Opera directamente a través de USB utilizando el protocolo propietario Odin de Samsung, proporcionando una alternativa gratuita y amigable con Linux/macOS a la herramienta Odin solo para Windows. El proyecto se mantiene en GitHub por Benjamin Dobell y ha sido ampliamente utilizado en la comunidad de modding de Android desde principios de la década de 2010.

## ¿Por qué usar Heimdall?

- **Multiplataforma** – Se ejecuta de forma nativa en Windows, Linux y macOS sin emulación.
- **Código abierto** – Totalmente auditable e impulsado por la comunidad.
- **Omite restricciones de Odin** – Útil cuando Odin no está disponible o al flashear en sistemas que no son Windows.
- **Programable** – La interfaz de línea de comandos permite la automatización y la integración en herramientas personalizadas.
- **Flasheo a nivel de partición** – Flashea imágenes de particiones individuales (por ejemplo, `BOOT`, `SYSTEM`, `RECOVERY`) para modificaciones específicas.

## Instalación

### Windows
Descarga el instalador más reciente desde la [página de lanzamientos de GitHub](https://github.com/Benjamin-Dobell/Heimdall/releases). Ejecuta el archivo `.exe` y sigue el instalador gráfico.

### Linux
Disponible a través de muchos gestores de paquetes:
```bash
# Debian/Ubuntu
sudo apt install heimdall-flash

# Fedora
sudo dnf install heimdall

# Arch Linux
sudo pacman -S heimdall
```
Alternativamente, compila desde el código fuente usando `cmake`.

### macOS
Instala a través de Homebrew:
```bash
brew install heimdall
```
O descarga el binario de macOS desde la página de lanzamientos.

## Uso

### Prerrequisitos
1. Habilita **Opciones de desarrollador** y **Depuración USB** en el dispositivo Samsung.
2. Inicia el dispositivo en **Modo Descarga** (generalmente: Apagar → mantener presionado Volumen Bajo + Inicio + Encendido, luego presionar Volumen Arriba para confirmar).
3. Conecta el dispositivo a la computadora mediante USB.

### Detección
Verifica que el dispositivo sea reconocido:
```bash
heimdall detect
```
Si tiene éxito, la salida mostrará el modelo del dispositivo y el estado de la conexión.

### Flasheo básico
Flashea una imagen de partición:
```bash
heimdall flash --RECOVERY twrp-3.6.0-i9300.img
```
Flashea múltiples particiones a la vez:
```bash
heimdall flash --BOOT boot.img --SYSTEM system.img --VENDOR vendor.img
```

### Uso de un archivo PIT
Para una restauración completa del firmware o cuando se desconoce la tabla de particiones, proporciona un archivo `.pit` extraído del dispositivo o del paquete de firmware:
```bash
heimdall flash --pit /path/to/device.pit --SLT --no-reboot
```
La opción `--SLT` flashea todas las particiones definidas en el PIT, mientras que `--no-reboot` mantiene el dispositivo en modo descarga después de completar.

### Cerrar conexión
Después de flashear, cierra la interfaz USB:
```bash
heimdall close-pc-screen
```

## Características principales

- **Multiplataforma**: Windows, Linux, macOS (binarios nativos).
- **Código abierto**: Código base bajo licencia BSD con mantenimiento activo de la comunidad.
- **Soporte del protocolo Odin**: Implementación directa del protocolo de flasheo de bajo nivel de Samsung.
- **Detección de dispositivos**: Enumeración USB confiable y verificación de handshake.
- **Flasheo a nivel de partición**: Flashea particiones individuales (boot, recovery, system, etc.).
- **Flasheo basado en PIT**: Usa tablas de información de particiones para una restauración completa del firmware.
- **Controladores USB integrados**: Los instaladores de Windows incluyen los controladores necesarios; se usa libusb en Linux/macOS.
- **Soporte de scripting**: Opciones de CLI adecuadas para pipelines automatizados y entornos CI/CD.

## Ejemplos

### Detectar un dispositivo conectado
```bash
$ heimdall detect
Device detected: GT-I9300 (galaxys3)
```

### Flashear una recuperación personalizada (TWRP)
```bash
heimdall flash --RECOVERY twrp-3.6.0_9-i9300.img --no-reboot
```

### Flashear un firmware de stock completo usando un archivo PIT
```bash
heimdall flash --pit AP_I9300_4.3.pit --SLT --no-reboot
```

### Flashear solo la partición de boot
```bash
heimdall flash --BOOT boot.img
```

## Notas

- Heimdall es distinto de **Heimdall Application Dashboard** (linuxserver/Heimdall, un lanzador de aplicaciones basado en web) y del framework de ciberseguridad **Heimdall**.
- Siempre usa el firmware correcto para tu modelo de dispositivo para evitar bricking.
- Asegúrate de que los controladores USB estén instalados en Windows – el instalador los incluye. En Linux, es posible que sea necesario agregar reglas udev para que el dispositivo sea accesible sin ser root.