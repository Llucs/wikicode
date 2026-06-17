---
title: Team Win Recovery Project (TWRP)
description: TWRP es una recuperación personalizada de código abierto para Android que permite flashear ROMs personalizadas, hacer copias de seguridad completas del dispositivo (NANDroid) y realizar modificaciones del sistema a través de una interfaz táctil.
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

TWRP (Team Win Recovery Project) es una **imagen de recuperación personalizada de código abierto** para dispositivos Android. Reemplaza la partición de recuperación de fábrica para proporcionar un entorno rico en funciones y controlado por pantalla táctil para instalar firmware de terceros, crear copias de seguridad completas del sistema y realizar tareas avanzadas de gestión del sistema, todo sin necesidad de iniciar Android.

## ¿Por qué TWRP?

La recuperación de Android de fábrica se limita a restablecimientos de fábrica y actualizaciones OTA. TWRP abre el dispositivo para:

- **Instalación de ROMs personalizadas** (LineageOS, Pixel Experience, etc.)
- **Copias de seguridad y restauraciones completas del sistema** (NANDroid) — esencial antes de modificaciones arriesgadas.
- **Rooteo** (flasheo de Magisk o SuperSU).
- **Gestión de particiones** (borrado, formateo, redimensionado).
- **Manejo de cifrado** (descifrado de userdata bajo ciertas condiciones).
- **ADB sideloading y MTP** para transferir archivos o flashear sin almacenamiento.

TWRP es el estándar de facto para entusiastas y desarrolladores de Android; ha reemplazado recuperaciones anteriores como ClockworkMod (CWM) gracias a su interfaz intuitiva y al soporte activo de la comunidad.

## Características principales

- **GUI táctil** – Soporte táctil completo con teclado en pantalla, administrador de archivos y emulador de terminal.
- **Copia de seguridad NANDroid** – Clona particiones completas (Boot, System, Data, EFS/IMEI) a `/sdcard/TWRP/BACKUPS/`.
- **Flasheo de ZIP** – Instala paquetes de firmware personalizados (ROMs, kernels, mods, GApps, Magisk).
- **Borrado avanzado** – Borra particiones individuales, “Formatear datos” para eliminar el cifrado.
- **Administrador de archivos** – Navega y modifica archivos en el sistema de archivos del dispositivo.
- **ADB Sideload** – Flashea archivos ZIP desde un ordenador vía USB.
- **Soporte MTP** – Accede al almacenamiento del dispositivo como una unidad extraíble en recuperación.
- **Soporte de cifrado** – Puede descifrar userdata con PIN/contraseña/patrón (cifrados antiguos; FBE en dispositivos modernos a menudo no es compatible).
- **Temas** – Interfaz de usuario personalizable mediante temas `.twres`.
- **Captura de pantalla** – Captura la pantalla mientras está en recuperación.

## Historia

Creado por *Dees_Troy* alrededor de 2011, TWRP rápidamente se convirtió en la recuperación personalizada más popular debido a su interfaz táctil patentada. Evolucionó a través de un tema Holo a una interfaz Material Design (versión 3.0+). Hoy es mantenido por un equipo central y admite cientos de dispositivos listados oficialmente en [twrp.me](https://twrp.me).

## Instalación

> **Requisitos previos:**
> - Bootloader desbloqueado (necesario para la mayoría de los dispositivos).
> - Herramientas ADB y Fastboot instaladas en tu PC.
> - Imagen TWRP correcta para tu modelo exacto de dispositivo (verifica el nombre de código en twrp.me).

### Método Fastboot general (la mayoría de los dispositivos)

1. **Reinicia en bootloader:**
   ```bash
   adb reboot bootloader
   ```
2. **Flashea la imagen de recuperación:**
   ```bash
   fastboot flash recovery twrp-<version>.img
   ```
3. **Inicia en recuperación inmediatamente** (antes de que el sistema arranque, lo que podría sobrescribir TWRP):
   ```bash
   fastboot reboot recovery
   # o usa la combinación de teclas de hardware (Subir Volumen + Encendido, etc.)
   ```

### Dispositivos basados en ranuras (particiones A/B – ej., Pixels, OnePlus)

Debido a que el sistema puede reemplazar automáticamente la partición de recuperación en el próximo arranque, usa un método de arranque temporal:

1. **Inicia la imagen de TWRP temporalmente:**
   ```bash
   fastboot boot twrp-<version>.img
   ```
2. **Dentro de TWRP, ve a** *Advanced → Install Recovery Ramdisk*.
   - Esto flashea TWRP a la ranura inactiva y evita que sea sobrescrito.

### Dispositivos Samsung (mediante Odin)

1. Descarga el archivo TWRP `.tar` (generalmente nombrado `twrp-<version>-<device>.tar`).
2. Abre Odin, coloca el archivo en la ranura **AP**.
3. Desmarca **Auto-Reinicio** en las opciones de Odin.
4. Flashea, luego reinicia inmediatamente en recuperación usando la combinación de teclas (Subir Volumen + Inicio + Encendido) para evitar la restauración de la recuperación de fábrica.

### Desde un dispositivo rooteado (usando la aplicación oficial de TWRP)

1. Instala la **aplicación oficial de TWRP** desde Play Store o twrp.me.
2. Otorga permisos de root.
3. Selecciona tu dispositivo y flashea la última imagen.

### Desde terminal (rooteado)

```bash
su
dd if=/sdcard/twrp.img of=/dev/block/bootdevice/by-name/recovery
```

Reemplaza la ruta con la ubicación de tu partición de recuperación (varía según el dispositivo – encuentra con `parted` o `ls /dev/block/platform/...`).

## Flujo de trabajo de uso básico

### Ingresar a Recuperación

- Usa la combinación de teclas de hardware (varía según el fabricante, a menudo **Bajar Volumen + Encendido**).
- O desde Android (si está rooteado/bootloader desbloqueado): `adb reboot recovery`.

### Borrado de particiones

- **Restablecimiento de fábrica** (borra datos/caché) – requerido antes de instalar una nueva ROM.
  - *Wipe → Swipe to Factory Reset*
- **Formatear Datos** – elimina el cifrado y borra el almacenamiento interno.
  - *Wipe → Format Data → escribe “yes”*.
- **Borrado Avanzado** – selecciona particiones individuales para borrar.

### Instalación de un ZIP (ROM, GApps, Magisk, etc.)

1. Toca **Instalar**.
2. Navega hasta el archivo `.zip` (generalmente en `/sdcard` o SD externa).
3. Toca el archivo; opcionalmente toca **Añadir más Zips** para encolar varios archivos.
4. **Desliza para confirmar el flasheo**.
5. *(Opcional)* Reiniciar sistema.

> Comando de ejemplo para sideload:
> ```bash
> adb sideload custom_rom.zip
> ```

### Realizar copia de seguridad (NANDroid)

1. Toca **Copia de seguridad**.
2. Selecciona particiones:
   - **Boot**, **System**, **Data** (mínimo para una restauración completa del sistema).
   - **EFS** (almacena IMEI – crítico para algunos dispositivos).
3. Desliza para comenzar la copia de seguridad.
4. La copia de seguridad se almacena en `/sdcard/TWRP/BACKUPS/<device_serial>/`.

### Restaurar una copia de seguridad

1. Toca **Restaurar**.
2. Selecciona una copia de seguridad de la lista.
3. Marca las particiones que deseas restaurar.
4. Desliza para confirmar.

### Administrador de archivos y terminal

- **Administrador de archivos**: *Advanced → File Manager* – navega, elimina, renombra, copia archivos.
- **Terminal**: *Advanced → Terminal* – ejecuta comandos como root.

## Comandos de ejemplo (Fastboot y ADB)

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

## Advertencias críticas

- **Imágenes específicas del dispositivo** – Flashear una imagen de TWRP para un modelo diferente puede **hard brick** tu dispositivo. Siempre verifica el nombre de código (ej., `beryllium` para Pocophone F1).
- **Confusión de ranuras A/B** – En dispositivos con actualizaciones fluidas, TWRP debe instalarse en ambas ranuras. Si una ranura carece de TWRP, el dispositivo puede revertir a la recuperación de fábrica.
- **Problemas de cifrado** – Android moderno usa **File‑Based Encryption (FBE)**. TWRP a menudo no puede descifrar userdata. Los usuarios frecuentemente deben **Formatear Datos** (borra el almacenamiento interno) al cambiar de ROM o si TWRP no puede montar `/data`.
- **OTAs con recuperación personalizada** – Las actualizaciones OTA de fábrica generalmente fallan con TWRP. Debes:
  - Flashear el ZIP de OTA manualmente mediante TWRP.
  - O revertir a la recuperación de fábrica antes de aplicar la OTA.
- **Play Integrity / apps bancarias** – Un bootloader desbloqueado (requerido para TWRP) rompe muchas comprobaciones de seguridad. Rootear con Magisk puede ocultar esto, pero añade complejidad y no siempre es exitoso.
- **Copia de seguridad antes de modificar** – Siempre crea una copia de seguridad NANDroid antes de flashear cualquier ROM nueva o mod arriesgado. Una copia de seguridad completa puede rescatar un soft brick en minutos.

## Solución de problemas

| Problema | Solución |
|--------|----------|
| TWRP no persiste después del reinicio | Usa `fastboot boot` luego “Install Recovery Ramdisk” (dispositivos A/B). Otra opción: reflashear e inmediatamente iniciar en recuperación. |
| No se puede montar `/data` | Probablemente cifrado. Ve a *Wipe → Format Data* y escribe “yes”. **Esto borra todo el almacenamiento interno.** |
| El dispositivo se queda en el logo de arranque después del flasheo | Intenta borrar Dalvik/ART Cache y Cache. Si aún falla, restaura una copia de seguridad anterior. |
| ADB Sideload atascado en “enviando” | Asegúrate de tener los últimos controladores ADB. Prueba con un cable/puerto USB diferente. |
| TWRP no arranca (pantalla negra) | La imagen puede estar corrupta o ser incorrecta. Descárgala nuevamente desde el sitio oficial. |

## Recursos adicionales

- **Sitio oficial y descargas:** [https://twrp.me](https://twrp.me)
- **Código fuente:** [https://github.com/TeamWin/Team-Win-Recovery-Project](https://github.com/TeamWin/Team-Win-Recovery-Project)
- **Foros XDA:** Busca el hilo del foro específico de tu dispositivo para compilaciones y soporte de TWRP.
- **Compilar TWRP desde el código fuente:** [https://github.com/TeamWin/Team-Win-Recovery-Project/blob/android-12.1/README.md](https://github.com/TeamWin/Team-Win-Recovery-Project/blob/android-12.1/README.md)

TWRP es una herramienta poderosa para cualquier desarrollador o entusiasta de Android. Úsala con sabiduría y ten siempre una copia de seguridad a mano.