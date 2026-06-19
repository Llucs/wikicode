---
title: "Termux: Emulador de terminal y entorno Linux para Android"
description: "Una guía completa sobre Termux, el potente emulador de terminal de código abierto y entorno Linux para dispositivos Android, que cubre instalación, gestión de paquetes, uso avanzado y flujos de trabajo para desarrolladores."
created: 2026-06-19
tags:
  - android
  - terminal
  - linux
  - development
  - tools
status: draft
---

# Termux: Emulador de terminal y entorno Linux para Android

## ¿Qué es Termux?

Termux es un **emulador de terminal y entorno Linux de código abierto** para Android. Funciona completamente en espacio de usuario, sin requerir **acceso root**, y proporciona un amplio repositorio de paquetes derivado de Debian/Ubuntu. Con Termux, puedes tener una experiencia completa de línea de comandos Linux en tu dispositivo Android: instalar compiladores, intérpretes, editores de texto, herramientas de red y más. Aprovecha las syscalls del kernel de Android para crear un entorno casi nativo.

### ¿Por qué usar Termux?

- **Entorno de desarrollo portátil** – Escribir y ejecutar scripts de Python, compilar programas en C, gestionar repositorios Git o usar un REPL directamente en tu teléfono.
- **Administración de servidores sobre la marcha** – Conectar por SSH a servidores remotos, ejecutar diagnósticos de red (ping, traceroute, nmap) y sincronizar archivos con rsync.
- **Aprendizaje y educación** – Practicar comandos de Linux, shell scripting y conceptos de red sin necesidad de un PC completo.
- **Automatización e integración** – Combinar con aplicaciones de automatización de Android (Tasker) o usar Termux:API para interactuar con el hardware del teléfono (cámara, sensores, portapapeles).
- **Distribuciones Linux completas** – Instalar Ubuntu, Debian, Arch o Fedora dentro del entorno de Termux usando proot-distro para casi cualquier tarea de Linux.

---

## Características clave

| Característica | Descripción |
|---------|-------------|
| **Emulador de terminal** | Completo con gestos táctiles fáciles de usar, teclas de función adicionales (Tab, Ctrl, Alt, Esc) accesibles deslizando el dedo hacia la izquierda desde la fila de números. |
| **Gestor de paquetes** | `pkg` (y el subyacente `apt`) con miles de paquetes del repositorio de Termux. |
| **Gestión de múltiples sesiones** | Desliza un cajón para gestionar sesiones de terminal separadas, cada una con su propio inicio de sesión. |
| **Cliente y servidor SSH** | Conéctate a servidores remotos con `ssh`, o inicia un servidor (`sshd`) para acceder a tu dispositivo desde un ordenador. |
| **Soporte de Proot Distro** | Ejecuta distribuciones Linux completas (Ubuntu, Debian, Arch, Fedora) usando `proot-distro`. |
| **Integración con API** | La aplicación complementaria *Termux:API* da acceso a scripts a los sensores de Android, portapapeles, TTS, cámara, notificaciones y más. |
| **Acceso al almacenamiento** | Monta el almacenamiento compartido de Android (interno/SD) mediante `termux-setup-storage`. |

---

## Instalación

### 1. Obtener Termux

> **Importante**: La **versión de Google Play Store está obsoleta** (estancada en API 28). Instala siempre desde **F-Droid** para obtener paquetes actualizados y compatibilidad total con Android moderno (10+).

- **Cliente F-Droid**: Busca "Termux" en la aplicación F-Droid o descarga el APK directamente desde [F-Droid](https://f-droid.org/packages/com.termux/).
- **APK directo**: [F-Droid APK](https://f-droid.org/repo/com.termux_*.apk) (siempre la versión más reciente).

### 2. Aplicaciones complementarias (opcionales pero recomendadas)

| Aplicación | Propósito |
|-----|---------|
| [Termux:API](https://f-droid.org/packages/com.termux.api/) | Acceder al hardware de Android (sensores, cámara, portapapeles, etc.) desde scripts. |
| [Termux:Float](https://f-droid.org/packages/com.termux.float/) | Ejecutar Termux en una ventana flotante (superposición). |
| [Termux:Styling](https://f-droid.org/packages/com.termux.styling/) | Esquemas de colores y fuentes preparadas para powerline en la terminal. |
| [Termux:Tasker](https://f-droid.org/packages/com.termux.tasker/) | Llamar ejecutables de Termux desde Tasker y aplicaciones de automatización compatibles. |
| [Termux:Widget](https://f-droid.org/packages/com.termux.widget/) | Iniciar pequeños scripts desde la pantalla de inicio. |

### 3. Configuración inicial

Después de iniciar Termux por primera vez:

```bash
# Actualizar el repositorio de paquetes y actualizar todos los paquetes
pkg update && pkg upgrade

# Conceder acceso al almacenamiento (necesario para ver tus carpetas compartidas)
termux-setup-storage
```

Ahora tienes un entorno Termux completamente actualizado. El almacenamiento compartido de Android se monta en `~/storage/shared`.

---

## Gestión de paquetes

Termux usa el comando **`pkg`** como envoltorio de **`apt`**. Todos los comandos son familiares para usuarios de Debian/Ubuntu.

### Operaciones comunes con paquetes

```bash
# Buscar un paquete
pkg search python

# Instalar paquetes
pkg install python git vim openssh curl wget

# Eliminar un paquete
pkg remove python2

# Listar paquetes instalados
pkg list-installed

# Actualizar todos los paquetes
pkg upgrade
```

### Paquetes disponibles (muestra)

| Categoría | Paquetes |
|----------|----------|
| **Lenguajes** | python, python3, nodejs, ruby, php, lua, golang, rust |
| **Compiladores/Herramientas** | clang, make, gdb, cmake, gcc (mediante proot distro) |
| **Editores** | vim, emacs, nano, neovim |
| **Redes** | openssh, nmap, traceroute, netcat, rclone |
| **Bases de datos** | mariadb, sqlite, postgresql (requiere proot) |
| **Utilidades** | git, curl, wget, rsync, htop, jq, ripgrep, fd |

> **Nota**: Debido a que Termux es un entorno de espacio de usuario, algunos paquetes a nivel de sistema (por ejemplo, `systemd`, dependencias de `glibc`) requieren una distribución Linux completa mediante `proot-distro`.

---

## Uso avanzado

### 1. SSH: Cliente y servidor

**Cliente** – Conéctate a máquinas remotas igual que en un escritorio:

```bash
pkg install openssh
ssh usuario@servidor
```

**Servidor** – Haz que tu dispositivo Android sea accesible por SSH (puerto predeterminado 8022):

```bash
sshd
# o inícialo en primer plano con -d
sshd -d
```

Conéctate desde otra máquina:

```sh
ssh usuario@ip-del-teléfono -p 8022
```

> La primera vez que ejecutes `sshd`, Termux generará las claves de host y podrás establecer una contraseña para el usuario de termux (el usuario predeterminado es `u0_aXYZ`). Usa `passwd` para cambiarla.

### 2. Ejecutar distribuciones Linux completas con `proot-distro`

Proot te permite ejecutar una distribución Linux estándar dentro de Termux sin root. El paquete `proot-distro` simplifica esto.

```bash
pkg install proot-distro

# Listar distribuciones disponibles
proot-distro list

# Instalar Ubuntu (ejemplo)
proot-distro install ubuntu

# Iniciar sesión en la distribución instalada
proot-distro login ubuntu

# Dentro del entorno Ubuntu, puedes usar apt normalmente.
```

Ahora tienes un entorno Ubuntu completo (incluyendo administradores de servicios similares a `systemd` mediante `proot`, aunque no todas las funciones funcionan perfectamente). Puedes instalar paquetes como `gcc`, `postgresql` o `firefox` (la interfaz gráfica necesita un servidor X) dentro de él.

### 3. Usar el complemento Termux:API

Con `Termux:API` instalado, puedes controlar funciones de Android desde la línea de comandos.

```bash
pkg install termux-api

# Obtener estado de la batería
termux-battery-status

# Tomar una foto
termux-camera-photo salida.jpg

# Obtener contenido del portapapeles
termux-clipboard-get

# Mostrar una notificación
termux-notification --title "Hola" --content "Mundo"

# Consultar sensores
termux-sensor -s "Acelerómetro" -n 5
```

### 4. Automatización con Tasker

Termux:Tasker te permite ejecutar scripts de Termux como acciones de Tasker.

1. Instala **Termux:Tasker** desde F-Droid.
2. En Tasker, añade una acción de tipo `System -> Send Intent`.
3. Action: `com.termux.tasker.RUN_COMMAND`
4. Extra key/value pairs: `command` = tu script o comando (ej., `termux-battery-status`).

También puedes colocar scripts en `~/.termux/tasker/` y llamarlos por nombre.

### 5. Gestión de sesiones y trucos de interfaz

- **Teclas adicionales**: Desliza hacia la izquierda desde la fila de números (en la parte superior del teclado) para mostrar una fila con Tab, Ctrl, Alt, Esc, un alternador de teclas de función y una flecha hacia arriba (para desplazarse hacia arriba). Puedes personalizarlas en `~/.termux/termux.properties`.
- **Múltiples sesiones**: Toca el icono del cajón (tres líneas horizontales) en el lado izquierdo de la pantalla para listar, cambiar o crear nuevas sesiones de terminal.
- **Selección de texto**: Mantén presionada el área de la terminal para entrar en modo de selección; copiar/pegar funciona con el menú desplegable.

---

## Casos de uso

- **Programación móvil** – Escribir y probar scripts de Python, aplicaciones Node.js o programas en C con vim y gcc. Usa Git para el control de versiones.
- **Operaciones de servidor** – SSH a servidores de producción, ejecutar `tcpdump` o escaneos con `nmap`, monitorear registros y transferir archivos con `rsync`.
- **Análisis de datos** – Instalar Python con pandas, numpy, scipy y Jupyter (mediante `pkg install jupyter`) para procesar datos sobre la marcha.
- **Aprendizaje de Linux** – Experimentar con el sistema de archivos, shell scripting y redes sin un PC separado.
- **Calculadora de bolsillo** – Usar Python como calculadora interactiva: `python -c 'print(2**100)'` o iniciar un REPL.

---

## Solución de problemas y consejos

### La instalación del paquete falla con "404 Not Found"
Los repositorios pueden estar desactualizados. Ejecuta `pkg update && pkg upgrade` primero. Si el problema persiste, verifica que estás usando la versión de F-Droid (no la de Google Play).

### Acceso al almacenamiento denegado
Ejecuta `termux-setup-storage` y concede el permiso cuando se solicite. Si falla en Android 11+, asegúrate de que Termux tenga habilitado el permiso "Archivos y medios" en la configuración del sistema.

### Problemas con dependencias de libc/glibc
Algunos paquetes esperan glibc, pero Termux usa bionic (libc de Android). Usa un proot-distro (Ubuntu, Debian) para esos paquetes.

### Cómo desactivar el teclado de pantalla completa en Android 10+
Agrega esta línea a `~/.termux/termux.properties`:
```
fullscreen=false
```
Luego recarga con `termux-reload-settings`.

### Integración del portapapeles con la terminal
Usa `termux-clipboard-get` y `termux-clipboard-set` de `termux-api` para interactuar con el portapapeles del sistema.

---

## Comunidad y recursos

- **Sitio oficial**: [termux.com](https://termux.com) (redirige a GitHub)
- **Repositorio de GitHub**: [termux/termux-app](https://github.com/termux/termux-app) (aplicación principal)
- **Repositorio de paquetes**: [termux/termux-packages](https://github.com/termux/termux-packages)
- **Wiki**: [Termux Wiki](https://wiki.termux.com)
- **F-Droid**: [F-Droid Termux](https://f-droid.org/packages/com.termux/)
- **Reddit**: [r/termux](https://reddit.com/r/termux)

---

Termux convierte tu dispositivo Android en una potente y portátil estación de trabajo Linux. Con su extenso repositorio de paquetes, capacidades SSH y compatibilidad con flujos de trabajo Linux estándar, es una herramienta indispensable para desarrolladores, administradores de sistemas y cualquier persona que quiera llevar la línea de comandos en el bolsillo.