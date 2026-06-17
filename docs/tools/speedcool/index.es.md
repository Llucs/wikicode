---
title: Módulo Magisk SpeedCool
description: Un módulo Magisk para Android que optimiza la configuración del sistema para aumentar el rendimiento, reducir el uso de RAM y mejorar la gestión térmica.
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

# Módulo Magisk SpeedCool

**SpeedCool** es un módulo Magisk de código abierto y ligero creado por [Llucs](https://github.com/Llucs/SpeedCool-Magisk-Module). Aplica automáticamente un conjunto completo de ajustes a nivel de kernel y sistema al arrancar para aumentar el rendimiento, reducir el uso de RAM y mejorar la gestión térmica en cualquier dispositivo Android rooteado.

A diferencia de un limpiador de bloatware estándar, SpeedCool modifica la configuración subyacente del sistema para eliminar las causas fundamentales del lag y el sobrecalentamiento.

---

## Qué Hace

SpeedCool se enfoca en varias áreas clave del sistema:

- **CPU Governor & Frequency Scaling:** Reduce la latencia de activación para aplicaciones exigentes (p. ej., juegos, emuladores).
- **Low Memory Killer (LMK):** Prioriza mantener la aplicación activa en la memoria mientras recupera agresivamente la memoria de los procesos de caché en segundo plano.
- **Thermal Engine:** Modifica los puntos de regulación térmica para equilibrar el rendimiento sostenido con la generación de calor.
- **I/O Scheduler:** Cambia el planificador de almacenamiento a una variante de baja latencia para una carga más rápida de aplicaciones.
- **Network Stack:** Optimiza el control de congestión TCP para un mejor rendimiento en redes móviles.
- **GPU Rendering:** Habilita el renderizado forzado por GPU y optimiza el gobernador de la GPU.

---

## Por Qué Usarlo

- **Juegos más fluidos:** Las tasas de fotogramas son más estables gracias a un mejor ajuste del gobernador de CPU/GPU y al control de la regulación térmica.
- **Multitarea más rápida:** Las aplicaciones se recargan con menos frecuencia gracias a los valores LMK optimizados.
- **Funcionamiento más frío:** Los perfiles térmicos inteligentes evitan que el SoC alcance temperaturas críticas durante el uso intensivo.
- **Optimizador todo en uno:** Reemplaza la necesidad de múltiples módulos de rendimiento conflictivos.
- **Ligero:** El módulo suele tener menos de 1 MB y una sobrecarga insignificante.

---

## Instalación

### Requisitos Previos

- Dispositivo Android con cargador de arranque desbloqueado y acceso root.
- **Magisk** (v20.0+) instalado.
- Se recomienda un recovery personalizado (TWRP) como respaldo.

### Pasos

1. **Descarga** el último `SpeedCool-Magisk-Module.zip` desde la [página de versiones de GitHub](https://github.com/Llucs/SpeedCool-Magisk-Module/releases).
2. Abre la aplicación **Magisk Manager**.
3. Navega a la pestaña **Módulos**.
4. Toca **Instalar desde almacenamiento**.
5. Selecciona el archivo `.zip` descargado.
6. Desliza para confirmar la instalación.
7. **Reinicia** tu dispositivo cuando se solicite.

> **Consejo:** Si experimentas un bootloop, arranca en modo seguro (mantén presionado Volumen Arriba durante el arranque) y deshabilita el módulo, o elimínalo manualmente a través del recovery borrando `/data/adb/modules/SpeedCool/`.

---

## Uso y Verificación

SpeedCool está diseñado para funcionar completamente en segundo plano. No se requiere interfaz de usuario. Puedes verificar su funcionamiento usando comandos de terminal.

### Comprobación del Estado Activo

Lista el directorio del módulo para confirmar que está instalado:

```bash
su -c "ls -la /data/adb/modules/SpeedCool/"
```

Si se montó correctamente, el directorio contendrá los archivos del módulo (`system.prop`, `service.sh`, `module.prop`).

### Comprobación de las Propiedades del Sistema Aplicadas

```bash
su -c "getprop | grep speed"
```

Busca propiedades inyectadas por el módulo (p. ej., `ro.sys.speedcool.version`).

---

## Características Principales con Ejemplos de Comandos

### 1. Ajuste del Gobernador de la CPU

El módulo fuerza un gobernador de baja latencia (generalmente `performance`, `interactive` o `schedutil` ajustado) en todos los núcleos de la CPU.

```bash
# Check the current governor
su -c "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
```
*Salida esperada:* `performance` o `schedutil`

### 2. Optimización de RAM (LMK)

Los umbrales del Low Memory Killer se modifican para mantener la aplicación en primer plano receptiva mientras se eliminan agresivamente los procesos de fondo menos útiles.

```bash
# Check LMK values (adj, minfree)
su -c "cat /sys/module/lowmemorykiller/parameters/minfree"
su -c "cat /sys/module/lowmemorykiller/parameters/adj"
```

### 3. Optimización del Planificador de E/S

El planificador de la capa de bloque se cambia a una variante optimizada para el rendimiento interactivo (p. ej., `bfq` o `fiops`).

```bash
# Check the active scheduler for the main storage block device
su -c "cat /sys/block/mmcblk0/queue/scheduler"
```
*Salida esperada:* `[bfq]` o `[fiops]`

### 4. Ajustes de Red

El control de congestión TCP se cambia a un algoritmo más adecuado para redes móviles (p. ej., `westwood` o `bbr`).

```bash
# Check the active TCP congestion algorithm
su -c "cat /proc/sys/net/ipv4/tcp_congestion_control"
```
*Salida esperada:* `westwood`

### 5. Visualización de Registros del Módulo

Si la depuración está habilitada en el script del módulo, puedes filtrar el registro del sistema.

```bash
su -c "logcat -d | grep SpeedCool"
```

### 6. Lectura del Perfil del Módulo (si es configurable)

Algunas versiones te permiten elegir un perfil editando `service.sh`. Revisa los comentarios disponibles dentro del archivo:

```bash
su -c "head -50 /data/adb/modules/SpeedCool/service.sh"
```

---

## Solución de Problemas

| Síntoma | Causa Probable | Solución |
|---|---|---|
| **Bootloop** | Módulo conflictivo o dispositivo incompatible. | Mantén presionado Volumen Arriba durante el arranque para deshabilitar el módulo, o elimina el directorio `/data/adb/modules/SpeedCool` en el administrador de archivos de TWRP. |
| **Sin cambio de rendimiento** | Módulos conflictivos (LKT, FDE.AI, NFS). | Elimina todos los demás módulos de rendimiento antes de usar SpeedCool. |
| **Dispositivo aún caliente** | Los límites térmicos son demasiado agresivos. | Revisa la configuración de thermal-engine en el módulo o prueba un perfil diferente. |
| **Aplicaciones fallando** | Valores LMK demasiado agresivos. | Ajusta manualmente los valores `minfree` en `service.sh`. |

---

## Eliminación

1. Abre **Magisk Manager**.
2. Ve a la pestaña **Módulos**.
3. Toca el icono **Eliminar** (papelera) junto a SpeedCool.
4. Toca **Reiniciar**.

**Eliminación alternativa por línea de comandos:**

```bash
su -c "rm -rf /data/adb/modules/SpeedCool/"
reboot
```

---

## Referencias

- **Repositorio de GitHub:** [Llucs/SpeedCool-Magisk-Module](https://github.com/Llucs/SpeedCool-Magisk-Module)
- **Documentación oficial de Magisk:** [topjohnwu.github.io/Magisk/](https://topjohnwu.github.io/Magisk/)
- **XDA Developers:** Busca *SpeedCool* o *Llucs* para discusiones de soporte de la comunidad.

> **Descargo de responsabilidad:** Modificar los parámetros del sistema conlleva un riesgo inherente. Siempre realiza una copia de seguridad Nandroid completa antes de instalar módulos de rendimiento. Los autores no son responsables de ningún daño causado a tu dispositivo.