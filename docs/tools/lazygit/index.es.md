---
title: Lazygit – La interfaz de Git en terminal que impulsa tu productividad
description: Una guía completa sobre lazygit, una interfaz de Git basada en terminal que simplifica operaciones complejas de Git como el staging, rebasing y resolución de conflictos mediante una interfaz intuitiva controlada por teclado.
created: 2026-06-20
tags:
  - git
  - tui
  - productivity
  - terminal
status: draft
---

# Lazygit – La interfaz de Git en terminal que impulsa tu productividad

**Lazygit** es una interfaz de usuario de terminal (TUI) multiplataforma y controlada por teclado para Git. Creado por Jesse Duffield en 2018 y escrito en Go, envuelve las operaciones más complejas de Git —y a menudo propensas a errores— en un diseño intuitivo basado en paneles que vive enteramente dentro de tu terminal.

> "Deja de memorizar comandos de Git. Empieza a usar Git de forma intuitiva."

---

## ¿Por qué Lazygit?

La interfaz de línea de comandos de Git es poderosa pero notoriamente implacable. El rebase interactivo, el stage de hunks, la resolución de conflictos y la gestión de ramas requieren secuencias precisas de comandos. Lazygit resuelve esto al:

- **Visualizar tu repositorio** – Ver ramas, etiquetas, el gráfico de commits, el árbol de trabajo y el stash de un vistazo.
- **Acelerar el trabajo diario** – Hacer stage, commit, push y pull sin escribir un solo comando `git`.
- **Reducir errores** – El rebase interactivo, el cherry-pick y la resolución de conflictos se vuelven manejables con menús y deshacer.
- **Reducir la curva de aprendizaje** – Los nuevos miembros del equipo pueden realizar operaciones avanzadas de Git de inmediato, liberándolos de memorizar sintaxis arcana.
- **Funcionar multiplataforma** – Se ejecuta en Linux, macOS y Windows con la misma interfaz y combinaciones de teclas.

---

## Instalación

Lazygit está disponible a través de la mayoría de los gestores de paquetes. Elige tu plataforma:

```bash
# macOS (Homebrew)
brew install lazygit

# Ubuntu / Debian
sudo add-apt-repository ppa:lazygit-team/release
sudo apt update
sudo apt install lazygit

# Arch Linux
pacman -S lazygit

# Windows
winget install lazygit
# or
scoop install lazygit

# Go (requires Go 1.16+)
go install github.com/jesseduffield/lazygit@latest

# Binary downloads (all platforms)
# https://github.com/jesseduffield/lazygit/releases
```

---

## Uso básico

Navega a cualquier repositorio de Git y ejecuta:

```bash
cd my-project
lazygit
```

Lazygit se abre con un diseño de paneles divididos. La columna izquierda muestra (de arriba a abajo) los paneles de **Estado**, **Archivos**, **Ramas**, **Commits** y **Stash**. El lado derecho muestra el diff o el log del elemento seleccionado.

### Navegación entre paneles

| Tecla | Acción |
|-------|--------|
| `←` / `→` | Moverse entre paneles |
| `Tab` | Ciclar paneles hacia adelante |
| `Shift + Tab` | Ciclar paneles hacia atrás |
| `j` / `k` | Moverse arriba/abajo dentro de un panel |
| `J` / `K` | Desplazar el panel de diff principal |
| `?` | Mostrar/ocultar ayuda completa de combinaciones de teclas |

### Inicio rápido (flujo de trabajo diario)

1. **Iniciar** – Ejecutar `lazygit` dentro de un repositorio.
2. **Hacer stage de un archivo** – Presiona `Espacio` en un archivo en el panel de Archivos.
3. **Hacer stage de un hunk específico** – Presiona `Enter` para ver el diff, luego `Espacio` en hunks individuales.
4. **Hacer commit** – Presiona `c`, escribe un mensaje y presiona `Enter`.
5. **Hacer push** – Presiona `P` (mayúscula) para hacer push.
6. **Hacer pull** – Presiona `p` (minúscula) para hacer pull.
7. **Salir** – Presiona `q` para salir.

---

## Características principales (con ejemplos de comandos)

### 🎯 Stage interactivo (Mejor que `git add -p`)

Ve el diff de un archivo, luego haz stage/unstage de líneas o hunks individuales visualmente. No más contar posiciones del cursor.

```bash
# Inside the Files panel:
# Enter  → open the file diff
# Space  → stage the selected hunk
# a      → stage all changes
# Enter on a specific hunk → stage individual lines
```

### 🔁 Rebase interactivo (La característica estrella)

Reordena, squash, fixup, edita o elimina commits con pulsaciones de teclas individuales.

```bash
# Switch to the Commits panel (press 4):
# i       → start interactive rebase
# s       → squash commit into previous
# f       → fixup (squash, discard message)
# d       → drop commit entirely
# e       → edit commit (pause rebase)
# r       → reword commit message
# Ctrl+j  → move commit down in order
# Ctrl+k  → move commit up in order
```

Después de marcar, presiona `Enter` para confirmar. Lazygit ejecuta el rebase y muestra el progreso. Si ocurren conflictos, salta al panel de resolución de conflictos.

### ↩️ Deshacer / Rehacer (Red de seguridad)

Lazygit realiza un seguimiento de su propio historial de acciones internas. ¿Cometiste un error durante un rebase o eliminaste accidentalmente un commit? Deshazlo.

```bash
# z  → undo last action
# Z (Shift+z)  → redo
```

### 🌳 Gestión de ramas

Cambia, fusiona, rebase, renombra y elimina ramas sin salir de la interfaz.

```bash
# Press 3 to enter the Branches panel:
# Space    → checkout selected branch
# n        → create a new branch (optionally from current HEAD)
# m        → merge selected branch into current
# r        → rebase current branch onto selected
# R        → rename branch
# d        → delete branch (with confirmation)
# Ctrl+r   → update remote branch references
```

### 🍒 Cherry-pick de commits

Copia commits de una rama a otra sin `git log` ni búsqueda de hash de commits.

```bash
# In the Commits panel:
# c        → start cherry-pick mode
# Space    → toggle selection of a commit
# Shift+c  → complete cherry-pick
```

### 🧩 Gestión de stash

Nombra stashes, aplícalos, pópalos e incluso crea ramas a partir de stashes.

```bash
# Press 5 to enter the Stash panel:
# g        → toggle stash view
# s        → stash staged changes
# Shift+s  → stash all changes (including untracked files)
# Space    → apply selected stash
# d        → drop stash
# n        → name a new stash
# b        → create branch from stash
```

### ⚔️ Resolución de conflictos

Cuando un rebase o una fusión produce conflictos, Lazygit muestra un diff de tres vías con marcadores de conflicto en línea. Resuélvelos visualmente.

```bash
# Conflict panel will open automatically:
# Ctrl+o → open file in external merge tool
# Space  → stage resolved file
# Enter  → edit file manually
# /      → search for remaining conflict markers
```

### 🌳 Soporte de worktrees

Lazygit tiene soporte de primera clase para worktrees de Git, permitiéndote agregar, eliminar y cambiar entre ellos.

```bash
# In the Branches panel (or dedicated Worktrees panel):
# w        → open worktree management
# a        → add a new worktree
# d        → remove a worktree
# Space    → switch to a worktree
```

### 🧹 Comandos personalizados

Extiende Lazygit con tus propios comandos de shell o scripts que aparecen en la interfaz.

```bash
# In ~/.config/lazygit/config.yml:
customCommands:
  - key: "C"
    command: "git cz"
    description: "Commit with Commitizen"
    context: "files"
    loadingText: "Opening commitizen..."
```

---

## Consejos profesionales

1. **Combinaciones de teclas al estilo Vim** – `j/k` para navegar, `J/K` para desplazar diffs, `/` para buscar dentro de los paneles.
2. **Filtrar archivos** – Escribe `/` en el panel de Archivos para filtrar por nombre de archivo.
3. **Diff contra un commit específico** – En el panel de Commits, presiona `d` en un commit para ver qué cambió en ese commit.
4. **Alternar visibilidad del diff** – Presiona `Ctrl+d` para ciclar entre los modos de visualización del diff.
5. **Usar con tu configuración existente de Git** – Lazygit respeta tus alias, herramientas de diff y merge.

---

## Configuración

Lazygit es altamente configurable. El archivo de configuración completo se encuentra en:

- **Linux/macOS:** `~/.config/lazygit/config.yml`
- **Windows:** `%APPDATA%\lazygit\config.yml`

Genera una plantilla con:

```bash
lazygit --print-config
```

Las configuraciones comunes incluyen anulaciones de combinaciones de teclas, colores de tema, comandos personalizados y diseño de interfaz.

---

## Cuándo recurrir a Lazygit

| Escenario | Por qué Lazygit destaca |
|-----------|------------------------|
| Rebase interactivo | Selección visual de commits y reordenación; disponible deshacer |
| Stage de cambios parciales | Selección de hunks línea por línea con diff instantáneo |
| Incorporación de nuevos desarrolladores | No es necesario memorizar comandos complejos de Git |
| Preparación de revisiones de código | Crear series de commits limpias y lógicas en minutos |
| Resolución de conflictos | Visor de diff de tres vías con acción en línea |
| Vista general del repositorio | Ver ramas, etiquetas, remotos, stash y gráfico de commits de un vistazo |

---

## Recursos

- **GitHub:** [jesseduffield/lazygit](https://github.com/jesseduffield/lazygit)
- **Documentación:** [Lazygit Wiki](https://github.com/jesseduffield/lazygit/wiki)
- **Referencia de configuración:** [Configuración de Lazygit](https://github.com/jesseduffield/lazygit/blob/master/docs/Config.md)
- **Ecosistema "lazy" del autor:** Lazygit, Lazydocker, Lazynpm – todos siguiendo la misma filosofía TUI.

---

Lazygit no reemplaza a Git; lo hace accesible, visual y rápido. Ya seas un usuario experimentado de Git o un desarrollador que solo quiere volver a escribir código, Lazygit te ahorrará horas cada semana. Pruébalo un día—nunca querrás volver a usar `git rebase -i` simple otra vez.