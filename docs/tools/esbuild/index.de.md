---
title: esbuild — Ein extrem schneller JavaScript- & TypeScript-Bundler
description: Ein umfassender Leitfaden zu esbuild, dem Go‑basierten Bundler und Minifier, der JavaScript- und TypeScript-Builds dramatisch beschleunigt – von den CLI-Grundlagen bis zur Plugin-Entwicklung.
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

# esbuild — Ein extrem schneller JavaScript- & TypeScript-Bundler

## Was ist esbuild?

esbuild ist ein **moderner, quelloffener Bundler und Minifier** für JavaScript, CSS, TypeScript und JSX. Statt in JavaScript wurde es in Go geschrieben und nutzt aggressive Parallelisierung, effizientes Speichermanagement und nativen Code, um **10–100-fache Geschwindigkeitsverbesserungen** gegenüber traditionellen Tools wie Webpack, Rollup oder Parcel zu erzielen.

Entwickelt von **Evan Wallace** (Mitbegründer von Figma) und erstmals im Januar 2020 veröffentlicht, ist esbuild dank seiner Einfachheit und seiner atemberaubenden Leistung zum Rückgrat wichtiger Frameworks und Tools geworden.

---

## Warum esbuild wählen?

| Funktion         | Nutzen                                                                 |
|------------------|------------------------------------------------------------------------|
| **Geschwindigkeit** | Bundles können in Millisekunden erstellt werden, selbst für große Codebasen. |
| **Keine Konfiguration** | Funktioniert sofort – keine Konfigurationsdatei erforderlich.            |
| **Einzelnes Tool** | Übernimmt Bundling, Minifizierung, Transpilierung, Source Maps und mehr. |
| **Moderner Code** | Unterstützt ESM, CommonJS und die Kombination beider.                   |
| **Erweiterbar**   | Plugin-System (JavaScript und Go) für benutzerdefinierte Loader und Transforms. |

esbuild ist ideal für:
- **Hochleistungsentwicklung**, bei der Wartezeiten eine Rolle spielen.
- **Framework-Tooling** – wird von Vite, Remix, Astro, SvelteKit und anderen verwendet.
- **Bibliotheksveröffentlichung** – schnelle, synchrone Auflösung für Node.js-Pakete.
- **Schnelles Prototyping** – Bündeln Sie eine TypeScript-Datei mit einem einzigen CLI-Befehl.

---

## Installation

```bash
# Install locally as a dev dependency
npm install --save-dev esbuild

# or using yarn / pnpm
yarn add -D esbuild
pnpm add -D esbuild
```

Dies installiert automatisch das plattformspezifische Binary. Sie können auch ein statisches Binary von der [GitHub-Releases](https://github.com/evanw/esbuild/releases)-Seite herunterladen.

> **Hinweis**: esbuild benötigt Node.js 12+. Es bündelt **ohne** Babel, `tsc` oder Terser – alles ist integriert.

---

## Quick Start

### 1. CLI-Grundlagen

```bash
# Bundle a single JavaScript file
npx esbuild src/app.js --bundle --outfile=dist/out.js

# Bundle TypeScript with JSX, minify, generate source maps
npx esbuild src/app.tsx --bundle --minify --sourcemap --outdir=dist --platform=browser --target=es2020

# Watch mode for development
npx esbuild src/app.ts --bundle --outfile=dist/app.js --watch
```

### 2. Node.js-API

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

### 3. Transform-API (schnelle Transpilierung)

```javascript
import { transformSync } from 'esbuild'

const code = `const x: number = 1; console.log(x)`
const result = transformSync(code, { loader: 'ts', target: 'es2020' })
console.log(result.code)
// Output: const x = 1; console.log(x);
```

---

## Schlüsselfunktionen mit Beispielen

### Bundling (CommonJS + ESM)

esbuild löst sowohl `require()`- als auch `import`-Anweisungen automatisch auf. Es kann Modulsysteme im selben Bundle mischen.

```bash
# Bundle a file that imports both ESM and CJS packages
npx esbuild src/main.js --bundle --outfile=out.js --format=esm
```

### Minifizierung

Der integrierte Minifier ist oft **10× schneller** als Terser und erzeugt identische oder kleinere Ausgaben.

```bash
npx esbuild src/app.ts --bundle --minify --outfile=dist/app.min.js
```

### Tree Shaking

Nicht verwendete Exporte werden automatisch entfernt, wenn `--bundle` verwendet wird. Markieren Sie Module ohne Nebenwirkungen explizit mit `"sideEffects": false` in der `package.json`.

```bash
# Tree shaking is automatic when bundling
npx esbuild src/index.ts --bundle --outfile=out.js
```

### TypeScript- und JSX-Transpilierung

esbuild entfernt Typen und wandelt JSX um, **führt jedoch keine Typprüfung durch** (verwenden Sie dafür `tsc --noEmit`). JSX kann über die Optionen `jsxFactory` und `jsxFragment` angepasst werden.

```bash
npx esbuild src/component.tsx --bundle --jsx=automatic --outfile=out.js
```

### CSS-Bundling

esbuild kann CSS bündeln, `@import`-Anweisungen auflösen und minifizieren.

```bash
npx esbuild src/styles.css --bundle --minify --outfile=dist/styles.min.css
```

### Source Maps

Die schnelle Erstellung von Source Maps ist integriert. Verwenden Sie `--sourcemap` für externe Maps oder `--sourcemap=inline` für inline.

```bash
npx esbuild src/app.ts --bundle --sourcemap --outfile=dist/app.js
```

### Watch-Modus

Das Flag `--watch` löst einen Neubuild aus, sobald sich Quelldateien ändern. Inkrementelle Builds sind extrem schnell.

```bash
npx esbuild src/app.ts --bundle --watch --outfile=dist/app.js
```

### Plugins

Die Plugin-API ermöglicht das Abfangen von Lade-, Transform- und Auflösungsereignissen. Hier ist ein einfaches Plugin, das Dateigrößen protokolliert:

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

Plugins können auch virtuelle Module, benutzerdefinierte Loader und erweiterte Transformationen verarbeiten.

---

## Anwendungsfälle und Ökosystem

esbuild ist nicht nur ein eigenständiges Tool – es treibt den Kern vieler moderner Frameworks an:

- **Vite** – verwendet esbuild für das Pre-Bundling von Abhängigkeiten und Entwicklungstransformationen.
- **Remix**, **Astro**, **SvelteKit** – nutzen esbuild als Teil ihrer Build-Pipeline.
- **tsup** – ein einfacher, schneller Bundler auf Basis von esbuild für Node.js-Bibliotheken.
- **tsx** – eine CLI, die TypeScript-Dateien direkt mit esbuilds Transform-API ausführt.

> **Integrationstipp**: Wenn Sie Vite verwenden, können Sie esbuild-Optionen über die `optimizeDeps.esbuildOptions`-Konfiguration anpassen.

---

## Leistungsvergleich

In Benchmarktests (Bündelung eines typischen React- + TypeScript-Projekts):

| Tool       | Zeit (s) | Relative Geschwindigkeit |
|------------|----------|--------------------------|
| esbuild    | 0.11     | 1× (Basislinie)          |
| Parcel 2   | 0.71     | ~6× langsamer            |
| Rollup     | 0.99     | ~9× langsamer            |
| Webpack 5  | 1.53     | ~14× langsamer           |

*Die Zahlen basieren ungefähr auf Community-Benchmarks. Die tatsächlichen Ergebnisse variieren je nach Projekt.*

---

## Konfigurationsoptionen

### Nützliche CLI-Flags

| Flag               | Beschreibung                                         |
|--------------------|------------------------------------------------------|
| `--bundle`         | Alle Abhängigkeiten in die Ausgabe bündeln.          |
| `--outfile`        | Einzelne Ausgabedatei.                               |
| `--outdir`         | Ausgabeverzeichnis (bei mehreren Einstiegspunkten verwenden). |
| `--minify`         | Ausgabe minifizieren (Leerzeichen, Syntax, Bezeichner). |
| `--sourcemap`      | Source Maps generieren.                              |
| `--target`         | Zielumgebung (z. B. `es2020`, `chrome80`).          |
| `--platform`       | `browser` oder `node` (beeinflusst die Auflösung).   |
| `--format`         | Ausgabeformat: `iife`, `cjs`, `esm`.                |
| `--watch`          | Auf Änderungen überwachen und neu bauen.             |
| `--loader`         | Dateiendung einem Loader zuordnen (z. B. `.png:file`) |
| `--define`         | Globale Bezeichner durch Konstanten ersetzen.        |
| `--external`       | Pakete vom Bundling ausschließen.                    |

### Häufige API-Optionen

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

## Vorbehalte und Einschränkungen

- **Keine TypeScript-Typprüfung** – esbuild transpiliert nur die Syntax. Verwenden Sie für die Typsicherheit `tsc --noEmit` in einem separaten Schritt.
- **Kein AST-Zugriff** – das Plugin-System stellt keinen konkreten AST für benutzerdefinierte Transformationen bereit.
- **Eingeschränkte CSS-Funktionen** – unterstützt kein PostCSS oder Sass (verwenden Sie Plugins oder Präprozessoren).
- **Code-Splitting** – wird nur für das ESM-Ausgabeformat unterstützt.
- **Strenge Auflösung** – einige Randfälle mit bedingten Exporten können von anderen Bundlern abweichen.

---

## Weiterführende Literatur

- [Offizielle esbuild-Dokumentation](https://esbuild.github.io/)
- [GitHub-Repository](https://github.com/evanw/esbuild)
- [Plugin-API-Referenz](https://esbuild.github.io/plugins/)
- [Warum ist esbuild so schnell? (Blogbeitrag von Evan Wallace)](https://esbuild.github.io/faq/#why-is-esbuild-fast)
- [Benchmarks im Vergleich zu Webpack, Rollup, Parcel](https://esbuild.github.io/faq/#benchmark-details)

---

*Generiert am 2026-06-21*