---
title: esbuild — An Extremely Fast JavaScript & TypeScript Bundler
description: A comprehensive guide to esbuild, the Go‑powered bundler and minifier that dramatically accelerates JavaScript and TypeScript builds, from CLI basics to plugin development.
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

# esbuild — An Extremely Fast JavaScript & TypeScript Bundler

## What is esbuild?

esbuild is a **modern, open‑source bundler and minifier** for JavaScript, CSS, TypeScript, and JSX. Written in Go instead of JavaScript, it leverages aggressive parallelism, efficient memory management, and native code to achieve **10–100× speed improvements** over traditional tools like Webpack, Rollup, or Parcel.

Created by **Evan Wallace** (co‑founder of Figma) and first released in January 2020, esbuild has become the backbone of major frameworks and tools thanks to its simplicity and blistering performance.

---

## Why Choose esbuild?

| Feature         | Benefit                                                                 |
|-----------------|-------------------------------------------------------------------------|
| **Speed**       | Bundles can be built in milliseconds, even for large codebases.        |
| **Zero Config** | Works out of the box – no config file needed.                          |
| **Single Tool** | Handles bundling, minification, transpilation, source maps, and more. |
| **Modern Code** | Supports ESM, CommonJS, and mixing of both.                           |
| **Extensible**  | Plugin system (JavaScript and Go) for custom loaders and transforms.  |

esbuild is ideal for:
- **High‑performance development** where wait times matter.
- **Framework tooling** – used by Vite, Remix, Astro, SvelteKit, and others.
- **Library publishing** – fast, synchronous resolution for Node.js packages.
- **Quick prototyping** – bundle a TypeScript file with one CLI command.

---

## Installation

```bash
# Install locally as a dev dependency
npm install --save-dev esbuild

# or using yarn / pnpm
yarn add -D esbuild
pnpm add -D esbuild
```

This installs the platform‑specific binary automatically. You can also download a static binary from the [GitHub releases](https://github.com/evanw/esbuild/releases) page.

> **Note**: esbuild requires Node.js 12+. It bundles **without** needing Babel, `tsc`, or Terser – everything is built‑in.

---

## Quick Start

### 1. CLI Basics

```bash
# Bundle a single JavaScript file
npx esbuild src/app.js --bundle --outfile=dist/out.js

# Bundle TypeScript with JSX, minify, generate source maps
npx esbuild src/app.tsx --bundle --minify --sourcemap --outdir=dist --platform=browser --target=es2020

# Watch mode for development
npx esbuild src/app.ts --bundle --outfile=dist/app.js --watch
```

### 2. Node.js API

```javascript
// build.mjs (ESM) or build.js (CommonJS)
import * as esbuild from 'esbuild'

async function build() {
  await esbuild.build({
    entryPoints: ['src/app.tsx'],
    bundle: true,
    outfile: 'dist/bundle.js',
    loader: { '.ts': 'tsx' },                 // treat .ts as TSX
    define: { 'process.env.NODE_ENV': '"production"' },
    plugins: [myPlugin],                       // optional
  })
  console.log('Build succeeded!')
}

build().catch(() => process.exit(1))
```

### 3. Transform API (quick transpilation)

```javascript
import { transformSync } from 'esbuild'

const code = `const x: number = 1; console.log(x)`
const result = transformSync(code, { loader: 'ts', target: 'es2020' })
console.log(result.code)
// Output: const x = 1; console.log(x);
```

---

## Key Features with Examples

### Bundling (CommonJS + ESM)

esbuild automatically resolves both `require()` and `import` statements. It can mix module systems in the same bundle.

```bash
# Bundle a file that imports both ESM and CJS packages
npx esbuild src/main.js --bundle --outfile=out.js --format=esm
```

### Minification

The built‑in minifier is often **10× faster** than Terser and produces identical or smaller output.

```bash
npx esbuild src/app.ts --bundle --minify --outfile=dist/app.min.js
```

### Tree Shaking

Unused exports are automatically removed when `--bundle` is used. Explicitly mark side‑effect‑free modules with `"sideEffects": false` in `package.json`.

### TypeScript and JSX Transpilation

esbuild strips types and transforms JSX, **but does not perform type checking** (use `tsc --noEmit` for that). JSX can be customized via the `jsxFactory` and `jsxFragment` options.

```bash
npx esbuild src/component.tsx --bundle --jsx=automatic --outfile=out.js
```

### CSS Bundling

esbuild can bundle CSS, resolve `@import` statements, and minify.

```bash
npx esbuild src/styles.css --bundle --minify --outfile=dist/styles.min.css
```

### Source Maps

Fast source map generation is built in. Use `--sourcemap` for external maps or `--sourcemap=inline` for inline.

### Watch Mode

The `--watch` flag triggers a rebuild whenever source files change. Incremental builds are extremely fast.

```bash
npx esbuild src/app.ts --bundle --watch --outfile=dist/app.js
```

### Plugins

The plugin API allows intercepting load, transform, and resolve events. Here’s a simple plugin that logs file sizes:

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

Plugins can also handle virtual modules, custom loaders, and advanced transformations.

---

## Use Cases & Ecosystem

esbuild is not just a standalone tool – it powers the core of many modern frameworks:

- **Vite** – uses esbuild for dependency pre‑bundling and development transforms.
- **Remix**, **Astro**, **SvelteKit** – leverage esbuild as part of their build pipeline.
- **tsup** – a simple, fast bundler built on top of esbuild for Node.js libraries.
- **tsx** – a CLI that runs TypeScript files directly using esbuild’s transform.

> **Integration Tip**: If you use Vite, you can customize esbuild options via the `optimizeDeps.esbuildOptions` configuration.

---

## Performance Comparison

In benchmark tests (bundling a typical React + TypeScript project):

| Tool       | Time (s) | Relative Speed |
|------------|----------|----------------|
| esbuild    | 0.11     | 1× (baseline)  |
| Parcel 2   | 0.71     | ~6× slower     |
| Rollup     | 0.99     | ~9× slower     |
| Webpack 5  | 1.53     | ~14× slower    |

*Figures are approximately based on community benchmarks. Actual results vary by project.*

---

## Configuration Options

### Useful CLI Flags

| Flag               | Description                                      |
|--------------------|--------------------------------------------------|
| `--bundle`         | Bundle all dependencies into the output.         |
| `--outfile`        | Single output file.                              |
| `--outdir`         | Output directory (use with multiple entry points).|
| `--minify`         | Minify output (whitespace, syntax, identifiers). |
| `--sourcemap`      | Generate source maps.                            |
| `--target`         | Target environment (e.g., `es2020`, `chrome80`). |
| `--platform`       | `browser` or `node` (affects resolution).        |
| `--format`         | Output format: `iife`, `cjs`, `esm`.             |
| `--watch`          | Watch for changes and rebuild.                   |
| `--loader`         | Map file extension to a loader (e.g., `.png:file`)|
| `--define`         | Replace global identifiers with constants.       |
| `--external`       | Exclude packages from bundling.                  |

### Common API Options

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

## Caveats & Limitations

- **No TypeScript type checking** – esbuild transpiles syntax only. Use `tsc --noEmit` in a separate step for type safety.
- **No AST access** – the plugin system does not expose a concrete AST for custom transforms.
- **Limited CSS features** – does not support PostCSS or Sass (use plugins or pre‑processors).
- **Code splitting** – supported only for ESM output format.
- **Strict resolution** – some edge cases with conditional exports may differ from other bundlers.

---

## Further Reading

- [Official esbuild Documentation](https://esbuild.github.io/)
- [GitHub Repository](https://github.com/evanw/esbuild)
- [Plugin API Reference](https://esbuild.github.io/plugins/)
- [Why esbuild is so fast? (Blog post by Evan Wallace)](https://esbuild.github.io/faq/#why-is-esbuild-fast)
- [Benchmarks vs. Webpack, Rollup, Parcel](https://esbuild.github.io/faq/#benchmark-details)

---

*Generated on 2026-06-21*