---
title: esbuild — Un bundler de JavaScript y TypeScript extremadamente rápido
description: Una guía completa de esbuild, el bundler y minificador impulsado por Go que acelera dramáticamente las compilaciones de JavaScript y TypeScript, desde los fundamentos de la CLI hasta el desarrollo de plugins.
created: 2026-06-21
tags:
  - bundler
  - build-tool
  - javascript
  - typescript
  - minifier
  - performance
status: draft
---

# esbuild — Un bundler de JavaScript y TypeScript extremadamente rápido

## ¿Qué es esbuild?

esbuild es un **bundler y minificador moderno de código abierto** para JavaScript, CSS, TypeScript y JSX. Escrito en Go en lugar de JavaScript, aprovecha el paralelismo agresivo, la gestión eficiente de memoria y el código nativo para lograr **mejoras de velocidad de 10 a 100×** sobre herramientas tradicionales como Webpack, Rollup o Parcel.

Creado por **Evan Wallace** (cofundador de Figma) y lanzado por primera vez en enero de 2020, esbuild se ha convertido en la columna vertebral de frameworks y herramientas importantes gracias a su simplicidad y rendimiento vertiginoso.

---

## ¿Por qué elegir esbuild?

| Característica  | Beneficio                                                                |
|-----------------|--------------------------------------------------------------------------|
| **Velocidad**       | Los bundles se pueden construir en milisegundos, incluso para bases de código grandes. |
| **Configuración cero** | Funciona de inmediato – no necesita archivo de configuración.           |
| **Herramienta única** | Maneja bundling, minificación, transpilación, source maps y más.       |
| **Código moderno** | Soporta ESM, CommonJS y la mezcla de ambos.                             |

esbuild es ideal para:
- **Desarrollo de alto rendimiento** donde los tiempos de espera importan.
- **Herramientas para frameworks** – usado por Vite, Remix, Astro, SvelteKit y otros.
- **Publicación de librerías** – resolución rápida y sincrónica para paquetes Node.js.
- **Prototipado rápido** – empaqueta un archivo TypeScript con un solo comando CLI.

---

## Instalación

```bash
# Instalar localmente como dependencia de desarrollo
npm install --save-dev esbuild

# o usando yarn / pnpm
yarn add -D esbuild
pnpm add -D esbuild
```

Esto instala automáticamente el binario específico para la plataforma. También puedes descargar un binario estático desde la página de [lanzamientos en GitHub](https://github.com/evanw/esbuild/releases).

> **Nota**: esbuild requiere Node.js 12+. Agrupa **sin** necesidad de Babel, `tsc` o Terser – todo está incorporado.

---

## Inicio rápido

### 1. Conceptos básicos de CLI

```bash
# Agrupar un solo archivo JavaScript
npx esbuild src/app.js --bundle --outfile=dist/out.js

# Agrupar TypeScript con JSX, minificar, generar source maps
npx esbuild src/app.tsx --bundle --minify --sourcemap --outdir=dist --platform=browser --target=es2020

# Modo observador para desarrollo
npx esbuild src/app.ts --bundle --outfile=dist/app.js --watch
```

### 2. API de Node.js

```javascript
// build.mjs (ESM) o build.js (CommonJS)
import * as esbuild from 'esbuild'

async function build() {
  await esbuild.build({
    entryPoints: ['src/app.tsx'],
    bundle: true,
    outfile: 'dist/bundle.js',
    loader: { '.ts': 'tsx' },                 // tratar .ts como TSX
    define: { 'process.env.NODE_ENV': '"production"' },
    plugins: [myPlugin],                       // opcional
  })
  console.log('Build succeeded!')
}

build().catch(() => process.exit(1))
```

### 3. API de transformación (transpilación rápida)

```javascript
import { transformSync } from 'esbuild'

const code = `const x: number = 1; console.log(x)`
const result = transformSync(code, { loader: 'ts', target: 'es2020' })
console.log(result.code)
// Output: const x = 1; console.log(x);
```

---

## Características clave con ejemplos

### Bundling (CommonJS y ESM)

esbuild resuelve automáticamente tanto las sentencias `require()` como `import`. Puede mezclar sistemas de módulos en un mismo bundle.

```bash
# Agrupar un archivo que importa paquetes ESM y CJS
npx esbuild src/main.js --bundle --outfile=out.js --format=esm
```

### Minificación

El minificador incorporado suele ser **10× más rápido** que Terser y produce una salida idéntica o más pequeña.

```bash
npx esbuild src/app.ts --bundle --minify --outfile=dist/app.min.js
```

### Tree Shaking

Las exportaciones no utilizadas se eliminan automáticamente cuando se usa `--bundle`. Marca explícitamente los módulos sin efectos secundarios con `"sideEffects": false` en `package.json`.

### Transpilación de TypeScript y JSX

esbuild elimina los tipos y transforma JSX, **pero no realiza verificación de tipos** (usa `tsc --noEmit` para eso). JSX se puede personalizar mediante las opciones `jsxFactory` y `jsxFragment`.

```bash
npx esbuild src/component.tsx --bundle --jsx=automatic --outfile=out.js
```

### Bundling de CSS

esbuild puede agrupar CSS, resolver sentencias `@import` y minificar.

```bash
npx esbuild src/styles.css --bundle --minify --outfile=dist/styles.min.css
```

### Source Maps

La generación rápida de source maps está integrada. Usa `--sourcemap` para mapas externos o `--sourcemap=inline` para incrustados.

### Modo Watch

El flag `--watch` desencadena una reconstrucción cada vez que los archivos fuente cambian. Las compilaciones incrementales son extremadamente rápidas.

```bash
npx esbuild src/app.ts --bundle --watch --outfile=dist/app.js
```

### Plugins

La API de plugins permite interceptar eventos de carga, transformación y resolución. Aquí hay un plugin simple que registra los tamaños de archivo:

```javascript
import * as esbuild from 'esbuild'

let sizePlugin = {
  name: 'size',
  setup(build) {
    build.onEnd(result => {
      for (const file of Object.values(result.metafile.outputs)) {
        console.log(`${file.path}: ${file.bytes} bytes`)
      }
    })
  },
}

await esbuild.build({
  entryPoints: ['src/app.ts'],
  bundle: true,
  outfile: 'dist/out.js',
  metafile: true,
  plugins: [sizePlugin],
})
```

Los plugins también pueden manejar módulos virtuales, loaders personalizados y transformaciones avanzadas.

---

## Casos de uso y ecosistema

esbuild no es solo una herramienta independiente – impulsa el núcleo de muchos frameworks modernos:

- **Vite** – usa esbuild para el pre‑bundling de dependencias y transformaciones en desarrollo.
- **Remix**, **Astro**, **SvelteKit** – aprovechan esbuild como parte de su pipeline de compilación.
- **tsup** – un bundler simple y rápido construido sobre esbuild para librerías Node.js.
- **tsx** – una CLI que ejecuta archivos TypeScript directamente usando la transformación de esbuild.

> **Consejo de integración**: Si usas Vite, puedes personalizar las opciones de esbuild mediante la configuración `optimizeDeps.esbuildOptions`.

---

## Comparación de rendimiento

En pruebas comparativas (agrupando un proyecto típico de React + TypeScript):

| Herramienta | Tiempo (s) | Velocidad relativa |
|-------------|------------|--------------------|
| esbuild     | 0.11       | 1× (base)          |
| Parcel 2    | 0.71       | ~6× más lento      |
| Rollup      | 0.99       | ~9× más lento      |
| Webpack 5   | 1.53       | ~14× más lento     |

*Las cifras son aproximadas basadas en benchmarks de la comunidad. Los resultados reales varían según el proyecto.*

---

## Opciones de configuración

### Flags útiles de la CLI

| Flag               | Descripción                                            |
|--------------------|--------------------------------------------------------|
| `--bundle`         | Agrupar todas las dependencias en la salida.           |
| `--outfile`        | Archivo de salida único.                               |
| `--outdir`         | Directorio de salida (usar con múltiples puntos de entrada). |
| `--minify`         | Minificar la salida (espacios en blanco, sintaxis, identificadores). |
| `--sourcemap`      | Generar source maps.                                   |
| `--target`         | Entorno destino (ej., `es2020`, `chrome80`).           |
| `--platform`       | `browser` o `node` (afecta la resolución).             |
| `--format`         | Formato de salida: `iife`, `cjs`, `esm`.               |
| `--watch`          | Observar cambios y reconstruir.                        |
| `--loader`         | Mapear extensión de archivo a un loader (ej., `.png:file`). |
| `--define`         | Reemplazar identificadores globales con constantes.    |
| `--external`       | Excluir paquetes del agrupamiento.                     |

### Opciones comunes de la API

```javascript
esbuild.build({
  entryPoints: ['src/index.ts'],
  outfile: 'dist/bundle.js',
  bundle: true,
  format: 'esm',
  target: 'esnext',
  sourcemap: true,
  minify: true,
  loader: {
    '.svg': 'dataurl',
    '.png': 'file',
  },
  define: {
    'process.env.API_URL': '"https://api.example.com"',
  },
  external: ['react', 'react-dom'],
})
```

---

## Advertencias y limitaciones

- **No hay verificación de tipos TypeScript** – esbuild transpila solo la sintaxis. Usa `tsc --noEmit` en un paso separado para la seguridad de tipos.
- **Sin acceso al AST** – el sistema de plugins no expone un AST concreto para transformaciones personalizadas.
- **Funcionalidades CSS limitadas** – no soporta PostCSS ni Sass (usa plugins o pre‑procesadores).
- **Code splitting** – solo compatible con formato de salida ESM.
- **Resolución estricta** – algunos casos límite con exports condicionales pueden diferir de otros bundlers.

---

## Lecturas adicionales

- [Documentación oficial de esbuild](https://esbuild.github.io/)
- [Repositorio de GitHub](https://github.com/evanw/esbuild)
- [Referencia de la API de Plugins](https://esbuild.github.io/plugins/)
- [¿Por qué esbuild es tan rápido? (Blog de Evan Wallace)](https://esbuild.github.io/faq/#why-is-esbuild-fast)
- [Benchmarks vs. Webpack, Rollup, Parcel](https://esbuild.github.io/faq/#benchmark-details)

---

*Generado el 2026-06-21*