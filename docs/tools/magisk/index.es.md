---
title: Magisk - Root sin modificación del sistema y gestor de módulos para Android
description: Magisk es una popular herramienta de rooteo para Android que proporciona acceso root sin modificar el sistema y soporte para módulos para modificaciones del sistema.
created: 2026-06-19
tags:
  - android
  - root
  - systemless
  - magisk
  - tool
status: draft
---

# Magisk – Root sin modificación del sistema y gestor de módulos para Android

## ¿Qué es Magisk?

Magisk es un conjunto de software de código abierto creado por **John Wu (topjohnwu)** que permite el **rooteo sin modificación del sistema** y la personalización profunda de dispositivos Android. A diferencia de los métodos de rooteo tradicionales que modifican la partición inmutable `/system`, Magisk funciona parcheando la imagen de arranque del dispositivo (o la partición `init_boot` en dispositivos más nuevos) para crear un sistema de archivos superpuesto en el momento del arranque. Esto permite que el acceso root, scripts de arranque, parches de políticas SELinux y módulos se carguen **sin alterar permanentemente los archivos del sistema**.

Publicado originalmente en 2016, Magisk rápidamente se convirtió en la solución estándar de rooteo para Android, reemplazando herramientas más antiguas como SuperSU. Continúa siendo mantenido activamente y se utiliza ampliamente tanto para rooteo básico como para modificaciones avanzadas del dispositivo.

---

## ¿Por qué usar Magisk?

| Beneficio | Descripción |
|-----------|-------------|
| **Modificaciones sin alterar el sistema** | Las actualizaciones OTA se conservan porque `/system` permanece intacto. |
| **MagiskSU** | Gestión de permisos root puramente de código abierto (conceder, preguntar, denegar). |
| **Sistema de módulos** | Instala ajustes (modificaciones de audio, librerías de cámara, bloqueo de anuncios, fuentes) sin necesidad de reparticionar. |
| **Zygisk** | Inyección de código en el proceso de cada aplicación a través de Zygote: reemplaza a MagiskHide. |
| **DenyList** | Oculta root, módulos y bootloader desbloqueado de aplicaciones específicas (banca, streaming). |
| **MagiskBoot** | Potente herramienta para desempaquetar, modificar y reempaquetar imágenes de arranque de Android. |
| **Comunidad activa** | Miles de módulos y documentación extensa disponible. |

Magisk es esencial para usuarios que necesitan acceso root para herramientas de respaldo avanzadas, automatización (Tasker), ajustes personalizados del sistema, o para reactivar funciones en aplicaciones que bloquean dispositivos rooteados.

---

## Guía de instalación

### Requisitos previos

- **Bootloader desbloqueado** (específico del dispositivo, a menudo requiere desbloqueo OEM).
- **ADB y Fastboot funcionales** en tu computadora.
- **Imagen de fábrica del dispositivo** o `boot.img` de serie (y posiblemente `init_boot.img`).
- **Respaldar** todos los datos importantes.

### Paso 1 – Extraer la imagen de arranque

Obtén la imagen de fábrica para tu dispositivo (por ejemplo, desde la página de imágenes de fábrica de Google) y extrae la imagen de arranque.

```bash
# Example for a Pixel device
unzip [device]_[build].zip
cd [device]_[build]
unzip image-[device]-[build].zip
# boot.img is now in the current directory
```

Para dispositivos con Android 13+ (por ejemplo, la serie Pixel 6), la partición de arranque es `init_boot.img` en lugar de `boot.img`.

### Paso 2 – Parchear la imagen con la aplicación Magisk

1. Instala el último APK de Magisk en tu dispositivo.
2. Abre la aplicación Magisk, toca **Instalar** → **Seleccionar y parchear un archivo**.
3. Elige el `boot.img` extraído (o `init_boot.img`).
4. La aplicación parcheará la imagen y guardará un nuevo archivo llamado `magisk_patched-XXXXX.img` (generalmente en `Download/`).

### Paso 3 – Flashear la imagen parcheada

Transfiere la imagen parcheada a tu computadora, luego inicia tu dispositivo en modo fastboot.

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

### Paso 4 – Verificar la instalación

Después de reiniciar, abre la aplicación Magisk. La pantalla **Inicio** debería mostrar la versión de Magisk instalada y “Instalado” junto al estado de Magisk.

---

## Uso básico

### Interfaz de la aplicación Magisk

- **Pestaña Superusuario** (icono de escudo): Muestra todas las aplicaciones que han solicitado permisos root. Toca una entrada para cambiar su estado de permiso (Conceder / Preguntar / Denegar).
- **Pestaña Módulos** (icono de pieza de rompecabezas): Muestra los módulos instalados. Toca el botón **+** para instalar un nuevo módulo desde un archivo `.zip` almacenado en tu dispositivo. Usa el interruptor para habilitar/deshabilitar un módulo (la mayoría requiere reinicio).
- **Pestaña Configuración** (icono de engranaje):
  - **Zygisk**: Habilitar o deshabilitar Zygisk (requiere reinicio).
  - **DenyList**: Configurar qué aplicaciones Magisk debe ocultar (requiere Zygisk y reinicio).
  - **Canal de actualización**: Elegir Stable, Beta o Canary para actualizaciones de la aplicación y Magisk.
  - **Respuesta automática**: Establecer el comportamiento predeterminado de los permisos root.

### Gestión de módulos

Los módulos se instalan como archivos ZIP estándar. Pueden contener scripts simples, archivos binarios o directorios completos de superposición del sistema.

```bash
# Typical module ZIP structure (inside /data/adb/modules/<module_id>/)
module.prop          # Metadata (id, name, version, author)
system/              # Files to overlay on /system
post-fs-data.sh      # Script run early in boot
service.sh           # Script run later in boot
```

Para instalar un módulo manualmente:

1. Descarga el archivo `.zip` del módulo a tu dispositivo.
2. Abre la aplicación Magisk → pestaña Módulos → **Instalar desde almacenamiento**.
3. Selecciona el archivo, confirma y luego **Reinicia** cuando se te solicite.

### Desinstalar Magisk

La aplicación Magisk proporciona una forma directa de eliminar root por completo:

1. Abre la aplicación Magisk.
2. Toca **Desinstalar Magisk** en la parte inferior de la pantalla Inicio.
3. Confirma: la aplicación restaurará la imagen de arranque original sin parchear y reiniciará.

---

## Características principales

### MagiskSU

Un reemplazo completo de `su` que es completamente de código abierto. Implementa un modelo de permisos con opciones de Conceder / Preguntar / Denegar y registra todos los accesos root. MagiskSU es compatible con todas las aplicaciones existentes que requieren root.

### Módulos de Magisk

Un formato estandarizado para distribuir modificaciones del sistema sin tocar la partición del sistema. Los módulos se cargan al arrancar utilizando el sistema de archivos superpuesto de Magisk. Existen miles de módulos en foros como XDA y el repositorio de Magisk.

### Zygisk

Zygisk es la implementación de Magisk de inyección de código en el proceso Zygote. Permite modificaciones en tiempo de ejecución dentro del proceso de cualquier aplicación. Zygisk reemplaza la funcionalidad anterior de MagiskHide.

### DenyList

Cuando Zygisk está habilitado, puedes configurar una **DenyList** de aplicaciones donde Magisk oculta su presencia (root, módulos, bootloader desbloqueado). Esta es la forma moderna de eludir las comprobaciones de integridad utilizadas por aplicaciones bancarias, de pago y streaming.

### MagiskBoot

MagiskBoot es una herramienta de bajo nivel para trabajar con imágenes de arranque. Puede desempaquetar, modificar y reempaquetarlas sin necesidad de un entorno Android completo. A menudo se usa directamente en una computadora para crear imágenes parcheadas sin la aplicación.

---

## Ejemplos de comandos

### Flashear imagen de arranque parcheada (fastboot)

```bash
fastboot flash boot magisk_patched-27000.img
fastboot reboot
```

### Flashear init_boot para dispositivos más nuevos

```bash
fastboot flash init_boot magisk_patched-27000.img
fastboot reboot
```

### Usar MagiskBoot para desempaquetar una imagen de arranque

```bash
magiskboot unpack boot.img
# This creates: kernel, kernel_dtb, ramdisk.cpio, header, etc.
```

### Reempaquetar una imagen de arranque modificada con MagiskBoot

```bash
magiskboot repack boot.img
# Creates new-boot.img with your modifications.
```

### Verificar el encabezado de la imagen de arranque

```bash
magiskboot info boot.img
```

### Parchear una imagen de arranque con Magisk (línea de comandos)

Si tienes el ejecutable de Magisk en tu computadora, puedes parchear directamente:

```bash
magiskboot boot.img
# Creates patched_boot.img in the current directory.
```

### Ocultar Magisk de una aplicación (DenyList)

Abre la aplicación Magisk → Configuración → **Configurar DenyList** → agrega la aplicación objetivo (por ejemplo, `com.google.android.gms` para Google Play Services). Después de reiniciar, Magisk será invisible para esa aplicación.

---

## Consejos y consideraciones

- **Actualizaciones OTA** – Siguen siendo compatibles porque Magisk solo modifica la partición de arranque. Sin embargo, después de una OTA debes **volver a flashear Magisk** en la nueva imagen de arranque.
- **SafetyNet / Play Integrity** – Si bien Magisk en sí mismo no proporciona omisión de integridad, herramientas como los módulos Zygisk-Assistant o Shamiko pueden ayudar a ocultar root de las comprobaciones de atestación de Google.
- **Conflictos entre módulos** – Algunos módulos pueden interferir entre sí; desactívalos uno por uno para aislar problemas.
- **Respaldos** – Siempre mantén una copia de la imagen de arranque original de serie. Si algo sale mal, puedes restaurarla mediante fastboot.
- **Magisk Canary** – El canal de vanguardia a veces incluye funciones inestables. Úsalo solo para pruebas.

---

## Referencias

- [Repositorio de Magisk en GitHub](https://github.com/topjohnwu/Magisk)
- [Documentación oficial de Magisk (guías para desarrolladores)](https://topjohnwu.github.io/Magisk/)
- [Repositorio de módulos de Magisk (no oficial)](https://www.androidacy.com/modules-repository/)
- [XDA Developers – Discusión y soporte de Magisk](https://forum.xda-developers.com/f/magisk.5903/)

---

*Este documento es parte de la wiki de desarrolladores. Los comentarios y mejoras son bienvenidos.*