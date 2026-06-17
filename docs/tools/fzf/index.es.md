---
title: fzf - Buscador difuso de línea de comandos
description: Una herramienta de búsqueda difusa de línea de comandos que mejora la búsqueda de archivos y texto en el terminal.
created: 2026-06-15
tags:
  - command-line
  - fuzzy-finder
  - fzf
  - productivity
  - terminal
status: draft
ecosystem: cli
---

# fzf – Buscador difuso de línea de comandos de propósito general

fzf es un **buscador difuso** interactivo que lleva el poder de la búsqueda incremental a cualquier lista presentada en la línea de comandos. Originalmente escrito en Ruby y luego reescrito en Go por [Junegunn Choi](https://github.com/junegunn), se ha convertido en una herramienta esencial para desarrolladores, administradores de sistemas y usuarios avanzados que desean navegar archivos, comandos, procesos y más a una velocidad relámpago.

En lugar de escribir nombres exactos o depender solo de la autocompletación con tabulador, fzf le permite escribir cualquier subcadena (o incluso una secuencia difusa) y filtra instantáneamente la entrada. Funciona con cualquier dato transmitido a través de stdin y devuelve el elemento seleccionado en stdout, lo que lo hace perfecto para tuberías de Unix.

---

## ¿Por qué usar fzf?

- **Velocidad**: Maneja cientos de miles de entradas en tiempo casi real.
- **Coincidencia difusa**: Encuentre archivos y comandos sin recordar nombres exactos.
- **Interactividad**: Filtrado en vivo con retroalimentación visual inmediata.
- **Componibilidad**: Funciona con cualquier comando que produzca o consuma texto.
- **Personalización**: Temas, combinaciones de teclas, ventanas de vista previa y más.

---

## Instalación

### macOS
```bash
brew install fzf
# Install useful key bindings and fuzzy auto-completion
$(brew --prefix)/opt/fzf/install
```

### Linux (Debian/Ubuntu)
```bash
sudo apt install fzf           # Often outdated – prefer building from source
# Or from the official repository:
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

### Arch Linux
```bash
sudo pacman -S fzf
```

### Windows (WSL / Git Bash / Scoop)
```bash
scoop install fzf
# Or with Chocolatey
choco install fzf
```

### Go (cualquier plataforma)
```bash
go install github.com/junegunn/fzf@latest
```

---

## Uso básico

### Enviar una lista a fzf
```bash
# Search through all files in the current directory
find . -type f | fzf
```

### Seleccionar un archivo y abrirlo en un editor
```bash
vim "$(find . -type f | fzf)"
```

### Previsualizar el contenido del archivo
```bash
fzf --preview 'cat {}'       # {} is the path of the current item
```

### Diseño inverso (búsqueda en la parte inferior)
```bash
fzf --reverse
```

### Selección múltiple (con Tab)
```bash
fzf --multi
```

### Aviso personalizado
```bash
fzf --prompt="Pick a file> "
```

---

## Características principales

### Modos de coincidencia difusa
fzf admite varios modos de coincidencia para ajustar su búsqueda:

- **Difuso (predeterminado)**: `abc` coincide con `alphabet.txt` – cualquier secuencia de subcadena funciona.
- **Coincidencia exacta**: prefijo con `'` → `'abc` coincide solo con líneas que contienen exactamente “abc”.
- **Coincidencia de prefijo**: sufijo con `^` → `^abc` coincide con líneas que comienzan con “abc”.
- **Coincidencia de sufijo**: prefijo con `$` → `abc$` coincide con líneas que terminan con “abc”.
- **Expresión regular**: prefijo `!` para invertir, o use la integración con `rg`.

### Ventana de vista previa
La ventana de vista previa muestra información contextual del elemento resaltado. Puede usar comandos externos como `cat`, `bat`, `head` o incluso scripts personalizados:

```bash
fzf --preview 'bat --color=always --style=numbers {}'
```

### Integración con el shell
El script oficial `install` configura tres atajos de teclado útiles (Bash, Zsh, Fish):

| Atajo   | Acción |
|---------|--------|
| `Ctrl+R` | Buscar en el historial de comandos |
| `Ctrl+T` | Buscar archivos/directorios y pegar sus rutas |
| `Alt+C`  | Saltar a un subdirectorio (cd difuso) |

### Plugin para Vim / Neovim
fzf proporciona un plugin nativo para Vim. La extensión más popular es [fzf.vim](https://github.com/junegunn/fzf.vim), que añade comandos como:

| Comando | Propósito |
|---------|-----------|
| `:Files [path]` | Buscar archivos |
| `:Rg [pattern]` | Buscar contenido de archivos (requiere ripgrep) |
| `:Buffers` | Cambiar entre buffers abiertos |
| `:GFiles?` | Buscar archivos no rastreados en un repositorio Git |
| `:Commands` | Listar comandos de Vim |
| `:Maps` | Mostrar asignaciones de teclas |

### Extensibilidad
Debido a que fzf opera sobre stdin/stdout, se integra perfectamente en cualquier flujo de trabajo. Puede envolverlo en funciones de shell o scripts para crear sus propios menús interactivos.

---

## Casos de uso avanzados

### Matar procesos
```bash
ps aux | fzf | awk '{print $2}' | xargs kill -9
```

### Cambiar a una rama de Git
```bash
git branch -a | fzf | tr -d ' *' | xargs git checkout
```

### SSH a hosts desde Config
```bash
cat ~/.ssh/config | grep -i '^host ' | awk '{print $2}' | fzf | xargs ssh
```

### Buscar contenido de archivos con vista previa
```bash
rg --line-number . | fzf --delimiter : \
    --preview 'bat --color=always --highlight-line {2} {1}'
```

### Cambiar directorio interactivamente (con fd)
```bash
cd "$(fd --type d | fzf)"
```
O use el atajo incorporado `Alt+C`.

### Buscar contenedores Docker
```bash
docker ps | fzf | awk '{print $NF}'
```

---

## Consejos y trucos

- **Use la opción `--header`** para mostrar instrucciones:
  ```bash
  fzf --header "Press Ctrl-R for history, Ctrl-T for files"
  ```
- **Almacene los elementos seleccionados en una variable** para operaciones por lotes.
- **Agregue una vista previa en color** usando `bat` o `highlight` con soporte ANSI.
- **Combine con `tmux`** para abrir el panel de vista previa en una división separada.
- **Personalice el esquema de color** a través de la variable de entorno `FZF_DEFAULT_OPTS`:
  ```bash
  export FZF_DEFAULT_OPTS='--color=bg+:#383838,fg+:#f0f0f0'
  ```

---

## Conclusión

fzf es una herramienta de referencia para la búsqueda interactiva en terminal. Su coincidencia difusa, velocidad y componibilidad lo hacen indispensable para cualquiera que viva en la línea de comandos. Ya sea que esté navegando archivos, localizando procesos o creando flujos de trabajo personalizados, fzf convierte las tediosas tareas de búsqueda en una experiencia fluida, casi mágica.

Para obtener la documentación completa, visite el [repositorio de GitHub](https://github.com/junegunn/fzf).