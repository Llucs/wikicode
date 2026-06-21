---
title: esbuild — Un bundler JavaScript & TypeScript extrêmement rapide
description: Un guide complet sur esbuild, le bundler et minifier propulsé par Go qui accélère considérablement les builds JavaScript et TypeScript, des bases de la CLI au développement de plugins.
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

# esbuild — Un bundler JavaScript & TypeScript extrêmement rapide

## Qu'est-ce qu'esbuild ?

esbuild est un **bundler et minifier moderne, open-source** pour JavaScript, CSS, TypeScript et JSX. Écrit en Go au lieu de JavaScript, il exploite un parallélisme agressif, une gestion mémoire efficace et du code natif pour obtenir des **améliorations de vitesse de 10 à 100 fois** par rapport aux outils traditionnels comme Webpack, Rollup ou Parcel.

Créé par **Evan Wallace** (co‑fondateur de Figma) et publié pour la première fois en janvier 2020, esbuild est devenu le pilier de nombreux frameworks et outils grâce à sa simplicité et à ses performances fulgurantes.

---

## Pourquoi choisir esbuild ?

| Fonctionnalité  | Avantage                                                                 |
|-----------------|--------------------------------------------------------------------------|
| **Vitesse**     | Les bundles peuvent être construits en quelques millisecondes, même pour de grandes bases de code. |
| **Zéro configuration** | Fonctionne prêt à l'emploi – aucun fichier de configuration nécessaire. |
| **Outil unique** | Gère le bundling, la minification, la transpilation, les source maps, et plus encore. |
| **Code moderne** | Prend en charge ESM, CommonJS et le mélange des deux.                  |
| **Extensible**  | Système de plugins (JavaScript et Go) pour des loaders et transformations personnalisés. |

esbuild est idéal pour :
- **Développement haute performance** où les temps d'attente comptent.
- **Outillage de framework** – utilisé par Vite, Remix, Astro, SvelteKit, et d'autres.
- **Publication de bibliothèques** – résolution rapide et synchrone pour les paquets Node.js.
- **Prototypage rapide** – bundle d'un fichier TypeScript avec une seule commande CLI.

---

## Installation

```bash
# Install locally as a dev dependency
npm install --save-dev esbuild

# or using yarn / pnpm
yarn add -D esbuild
pnpm add -D esbuild
```

Ceci installe automatiquement le binaire spécifique à la plateforme. Vous pouvez également télécharger un binaire statique depuis la page des [GitHub releases](https://github.com/evanw/esbuild/releases).

> **Remarque** : esbuild nécessite Node.js 12+. Il bundle **sans** avoir besoin de Babel, `tsc` ou Terser – tout est intégré.

---

## Démarrage rapide

### 1. Bases de la CLI

```bash
# Bundle a single JavaScript file
npx esbuild src/app.js --bundle --outfile=dist/out.js

# Bundle TypeScript with JSX, minify, generate source maps
npx esbuild src/app.tsx --bundle --minify --sourcemap --outdir=dist --platform=browser --target=es2020

# Watch mode for development
npx esbuild src/app.ts --bundle --outfile=dist/app.js --watch
```

### 2. API Node.js

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

### 3. API Transform (transpilation rapide)

```javascript
import { transformSync } from 'esbuild'

const code = `const x: number = 1; console.log(x)`
const result = transformSync(code, { loader: 'ts', target: 'es2020' })
console.log(result.code)
// Output: const x = 1; console.log(x);
```

---

## Fonctionnalités clés avec exemples

### Bundling (CommonJS + ESM)

esbuild résout automatiquement les instructions `require()` et `import`. Il peut mélanger les systèmes de modules dans le même bundle.

```bash
# Bundle a file that imports both ESM and CJS packages
npx esbuild src/main.js --bundle --outfile=out.js --format=esm
```

### Minification

Le minifier intégré est souvent **10× plus rapide** que Terser et produit une sortie identique ou plus petite.

```bash
npx esbuild src/app.ts --bundle --minify --outfile=dist/app.min.js
```

### Tree Shaking

Les exports inutilisés sont automatiquement supprimés lorsque `--bundle` est utilisé. Marquez explicitement les modules sans effet de bord avec `"sideEffects": false` dans `package.json`.

### Transpilation TypeScript et JSX

esbuild supprime les types et transforme JSX, **mais n'effectue pas la vérification de types** (utilisez `tsc --noEmit` pour cela). JSX peut être personnalisé via les options `jsxFactory` et `jsxFragment`.

```bash
npx esbuild src/component.tsx --bundle --jsx=automatic --outfile=out.js
```

### Bundling CSS

esbuild peut bundler du CSS, résoudre les instructions `@import` et minifier.

```bash
npx esbuild src/styles.css --bundle --minify --outfile=dist/styles.min.css
```

### Source Maps

La génération rapide de source maps est intégrée. Utilisez `--sourcemap` pour des maps externes ou `--sourcemap=inline` pour en ligne.

### Mode Watch

Le flag `--watch` déclenche une reconstruction dès que les fichiers source changent. Les builds incrémentiels sont extrêmement rapides.

```bash
npx esbuild src/app.ts --bundle --watch --outfile=dist/app.js
```

### Plugins

L'API de plugin permet d'intercepter les événements de chargement, transformation et résolution. Voici un plugin simple qui enregistre les tailles de fichiers :

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

Les plugins peuvent également gérer des modules virtuels, des loaders personnalisés et des transformations avancées.

---

## Cas d'utilisation et écosystème

esbuild n'est pas seulement un outil autonome – il alimente le cœur de nombreux frameworks modernes :

- **Vite** – utilise esbuild pour le pré‑bundling des dépendances et les transformations en développement.
- **Remix**, **Astro**, **SvelteKit** – exploitent esbuild dans leur pipeline de build.
- **tsup** – un bundler simple et rapide construit au-dessus d'esbuild pour les bibliothèques Node.js.
- **tsx** – une CLI qui exécute directement des fichiers TypeScript en utilisant la transformation d'esbuild.

> **Astuce d'intégration** : Si vous utilisez Vite, vous pouvez personnaliser les options d'esbuild via la configuration `optimizeDeps.esbuildOptions`.

---

## Comparaison des performances

Dans des tests de benchmark (bundling d'un projet typique React + TypeScript) :

| Outil      | Temps (s) | Vitesse relative |
|------------|-----------|------------------|
| esbuild    | 0.11      | 1× (référence)   |
| Parcel 2   | 0.71      | ~6× plus lent    |
| Rollup     | 0.99      | ~9× plus lent    |
| Webpack 5  | 1.53      | ~14× plus lent   |

*Les chiffres sont approximativement basés sur des benchmarks de la communauté. Les résultats réels varient selon le projet.*

---

## Options de configuration

### Flags CLI utiles

| Flag               | Description                                                             |
|--------------------|-------------------------------------------------------------------------|
| `--bundle`         | Inclure toutes les dépendances dans le bundle.                          |
| `--outfile`        | Fichier de sortie unique.                                               |
| `--outdir`         | Répertoire de sortie (à utiliser avec plusieurs points d'entrée).       |
| `--minify`         | Minifier la sortie (espaces, syntaxe, identifiants).                    |
| `--sourcemap`      | Générer des source maps.                                                |
| `--target`         | Environnement cible (p. ex. `es2020`, `chrome80`).                      |
| `--platform`       | `browser` ou `node` (affecte la résolution).                            |
| `--format`         | Format de sortie : `iife`, `cjs`, `esm`.                                |
| `--watch`          | Surveiller les modifications et reconstruire.                           |
| `--loader`         | Mapper une extension de fichier à un loader (p. ex. `.png:file`).       |
| `--define`         | Remplacer les identifiants globaux par des constantes.                  |
| `--external`       | Exclure des paquets du bundling.                                        |

### Options API courantes

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

## Mises en garde et limitations

- **Pas de vérification de types TypeScript** – esbuild transpile uniquement la syntaxe. Utilisez `tsc --noEmit` dans une étape séparée pour la sécurité des types.
- **Pas d'accès à l'AST** – le système de plugins n'expose pas un AST concret pour les transformations personnalisées.
- **Fonctionnalités CSS limitées** – ne supporte pas PostCSS ou Sass (utilisez des plugins ou pré‑processeurs).
- **Code splitting** – supporté uniquement pour le format de sortie ESM.
- **Résolution stricte** – certains cas particuliers avec des exports conditionnels peuvent différer d'autres bundlers.

---

## Pour aller plus loin

- [Documentation officielle d'esbuild](https://esbuild.github.io/)
- [Dépôt GitHub](https://github.com/evanw/esbuild)
- [Référence API Plugin](https://esbuild.github.io/plugins/)
- [Pourquoi esbuild est-il si rapide ? (Article de blog par Evan Wallace)](https://esbuild.github.io/faq/#why-is-esbuild-fast)
- [Benchmarks vs Webpack, Rollup, Parcel](https://esbuild.github.io/faq/#benchmark-details)

---

*Généré le 2026-06-21*