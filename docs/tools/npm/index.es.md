---
title: npm – Gestor de Paquetes de Node
description: Un gestor de paquetes para Node.js que es una herramienta fundamental para gestionar dependencias de JavaScript.
created: 2026-06-14
tags:
  - package-manager
  - javascript
  - nodejs
  - cli
  - dependency-management
status: draft
ecosystem: javascript
---

# npm – Gestor de Paquetes de Node

npm (Node Package Manager) es el gestor de paquetes predeterminado para el runtime de JavaScript Node.js. Se compone de dos componentes principales: una **CLI** (interfaz de línea de comandos) para gestionar dependencias y el **npm Registry**, una enorme base de datos pública de paquetes JavaScript. Se ha convertido en una herramienta esencial en el ecosistema JavaScript, permitiendo a los desarrolladores compartir, reutilizar y gestionar código de manera eficiente.

## ¿Qué es npm?

npm proporciona una forma de:

- **Instalar y gestionar dependencias** – hacer seguimiento de paquetes en `package.json` y archivos de bloqueo.
- **Publicar paquetes** – compartir tus propias bibliotecas con la comunidad o tu organización.
- **Ejecutar scripts** – automatizar flujos de trabajo de construcción, prueba e implementación.
- **Gestionar monorepos** – usar workspaces para manejar múltiples paquetes en un solo repositorio.

## ¿Por qué usar npm?

- **Estandarización** – npm viene incluido con Node.js, lo que lo convierte en la opción predeterminada para la mayoría de los proyectos JavaScript.
- **Gran ecosistema** – más de 2 millones de paquetes en el registro, cubriendo prácticamente todas las necesidades.
- **Reproducibilidad** – el archivo `package-lock.json` garantiza instalaciones deterministas en todos los entornos.
- **Seguridad** – `npm audit` te ayuda a encontrar y corregir vulnerabilidades en tu árbol de dependencias.
- **Conveniencia** – `npx` te permite ejecutar paquetes sin instalación global, y los scripts simplifican tareas comunes.

## Instalación

npm se instala automáticamente con Node.js. Para obtener la última versión LTS:

1. Descarga Node.js desde [nodejs.org](https://nodejs.org/).
2. Verifica la instalación:

```bash
node -v
npm -v
```

### Instalar mediante un gestor de versiones (nvm/fnm)

Usar un gestor de versiones te permite cambiar entre versiones de Node.js e instalar npm para cada una:

```bash
# Example with nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install --lts
```

Después de la instalación, npm está listo para usar.

## Uso Básico

### Inicializar un proyecto

Crea un nuevo proyecto o convierte una carpeta existente:

```bash
npm init -y
```

Esto genera un archivo `package.json` con valores predeterminados. Usa `npm init` (sin `-y`) para un asistente interactivo.

### Instalar dependencias

```bash
# Production dependency
npm install lodash

# Dev-only dependency
npm install --save-dev jest

# Global package (use sparingly; prefer npx)
npm install -g nodemon

# Install all dependencies from package.json
npm install
```

### Instalar versiones específicas

```bash
npm install react@18.2.0
npm install "express@>=4.17.0 <5.0.0"
```

### Ejecutar scripts

Los scripts se definen bajo la clave `"scripts"` en `package.json`. Atajos comunes:

```bash
npm start        # runs the "start" script
npm test         # runs the "test" script
npm run build    # custom script, e.g., "build"
```

### Desinstalar paquetes

```bash
npm uninstall lodash
```

### Actualizar paquetes

```bash
npm update                # update all packages within version ranges
npm install lodash@latest # force a specific version update
```

### Verificar vulnerabilidades

```bash
npm audit
```

Para corregir automáticamente (cuando esté disponible):

```bash
npm audit fix
```

### Instalación limpia para CI

```bash
npm ci
```

`npm ci` es más rápido y elimina `node_modules` antes de instalar exactamente desde `package-lock.json`.

## Características Principales

### npx – Ejecutar paquetes sin instalación

`npx` viene con npm y te permite ejecutar binarios del registro sin instalaciones globales:

```bash
npx create-react-app my-app
npx cowsay "Hello, npm!"
```

Si el paquete ya está instalado localmente, `npx` usará esa versión.

### Workspaces (soporte para monorepos)

Los workspaces de npm te permiten gestionar múltiples paquetes en un solo repositorio:

```json
{
  "workspaces": [
    "packages/*"
  ]
}
```

Luego ejecuta comandos en todos los workspaces:

```bash
npm install              # installs dependencies for all workspaces
npm run test --workspaces
```

La vinculación entre paquetes de workspace se maneja automáticamente.

### Hooks del ciclo de vida de scripts

npm proporciona hooks pre/post para scripts comunes:

- `prepublish` / `postpublish`
- `preinstall` / `postinstall`
- `prebuild` / `postbuild`

Ejemplo:

```json
{
  "scripts": {
    "prebuild": "rimraf dist",
    "build": "webpack --config webpack.prod.js"
  }
}
```

### package-lock.json

Este archivo bloquea la versión exacta de cada dependencia y sus dependencias transitivas. Asegura que todos los que ejecuten `npm install` obtengan el mismo árbol, haciendo que las compilaciones sean reproducibles.

### Overrides y resoluciones

Puedes forzar versiones específicas de dependencias transitivas en `package.json`:

```json
{
  "overrides": {
    "graceful-fs": "4.2.11"
  }
}
```

Esto es útil cuando una subdependencia tiene una vulnerabilidad que necesitas parchear sin esperar a que se publique su versión padre.

### npm config

Personaliza el comportamiento de npm de forma global o por proyecto:

```bash
npm config set init-author-name "Your Name"
npm config get registry
npm config delete <key>
```

También puedes usar un archivo `.npmrc` en la raíz del proyecto.

### Paquetes globales vs. npx

Las instalaciones globales deben reservarse para herramientas que usas en muchos proyectos (por ejemplo, `npm`, `yarn`, `node-gyp`). Para comandos puntuales, prefiere `npx` para evitar contaminar el espacio de nombres global y asegurarte de usar siempre la versión deseada.

## Conclusión

npm es una herramienta potente y esencial para cualquier desarrollador de JavaScript. Desde la instalación simple de dependencias hasta la gestión compleja de monorepos, su amplio conjunto de funciones ayuda a mantener los proyectos organizados, seguros y reproducibles. Ya sea que estés construyendo una pequeña biblioteca o una gran aplicación, dominar npm mejorará significativamente tu flujo de trabajo.