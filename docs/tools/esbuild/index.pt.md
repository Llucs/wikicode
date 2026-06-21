---
title: esbuild — Um Empacotador Extremamente Rápido para JavaScript e TypeScript
description: Um guia completo sobre o esbuild, o bundler e minifier desenvolvido em Go que acelera drasticamente as compilações de JavaScript e TypeScript, desde os fundamentos da CLI até o desenvolvimento de plugins.
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

# esbuild — Um Empacotador Extremamente Rápido para JavaScript e TypeScript

## O que é o esbuild?

esbuild é um **bundler e minifier moderno, open‑source** para JavaScript, CSS, TypeScript e JSX. Escrito em Go em vez de JavaScript, ele utiliza paralelismo agressivo, gerenciamento eficiente de memória e código nativo para alcançar **melhorias de velocidade de 10–100×** em relação a ferramentas tradicionais como Webpack, Rollup ou Parcel.

Criado por **Evan Wallace** (co‑fundador do Figma) e lançado pela primeira vez em janeiro de 2020, o esbuild se tornou a base de grandes frameworks e ferramentas graças à sua simplicidade e desempenho impressionante.

---

## Por que escolher o esbuild?

| Feature         | Benefit                                                                 |
|-----------------|-------------------------------------------------------------------------|
| **Speed**       | Bundles podem ser construídos em milissegundos, mesmo para grandes bases de código. |
| **Zero Config** | Funciona imediatamente – nenhum arquivo de configuração necessário.     |
| **Single Tool** | Lida com bundling, minification, transpilation, source maps e muito mais. |
| **Modern Code** | Suporta ESM, CommonJS e a mistura de ambos.                           |
| **Extensible**  | Sistema de plugins (JavaScript e Go) para loaders e transforms personalizados. |

esbuild é ideal para:
- **Desenvolvimento de alto desempenho** onde os tempos de espera são importantes.
- **Ferramentas de framework** – usado por Vite, Remix, Astro, SvelteKit e outros.
- **Publicação de bibliotecas** – resolução rápida e síncrona para pacotes Node.js.
- **Prototipagem rápida** – empacote um arquivo TypeScript com um único comando CLI.

---

## Instalação

```bash
# Install locally as a dev dependency
npm install --save-dev esbuild

# or using yarn / pnpm
yarn add -D esbuild
pnpm add -D esbuild
```

Isso instala o binário específico da plataforma automaticamente. Você também pode baixar um binário estático da página de [lançamentos do GitHub](https://github.com/evanw/esbuild/releases).

> **Nota**: o esbuild requer Node.js 12+. Ele faz o bundle **sem** precisar de Babel, `tsc` ou Terser – tudo já está incluído.

---

## Quick Start

### 1. CLI Básico

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

### 3. API Transform (transpilação rápida)

```javascript
import { transformSync } from 'esbuild'

const code = `const x: number = 1; console.log(x)`
const result = transformSync(code, { loader: 'ts', target: 'es2020' })
console.log(result.code)
// Output: const x = 1; console.log(x);
```

---

## Principais Funcionalidades com Exemplos

### Bundling (CommonJS + ESM)

esbuild resolve automaticamente ambas as declarações `require()` e `import`. Ele pode misturar sistemas de módulos no mesmo bundle.

```bash
# Bundle a file that imports both ESM and CJS packages
npx esbuild src/main.js --bundle --outfile=out.js --format=esm
```

### Minification

O minifier integrado é frequentemente **10× mais rápido** que o Terser e produz saída idêntica ou menor.

```bash
npx esbuild src/app.ts --bundle --minify --outfile=dist/app.min.js
```

### Tree Shaking

Exportações não utilizadas são automaticamente removidas quando `--bundle` é usado. Marque explicitamente módulos sem efeitos colaterais com `"sideEffects": false` no `package.json`.

### Transpilação de TypeScript e JSX

esbuild remove os tipos e transforma JSX, **mas não realiza verificação de tipos** (use `tsc --noEmit` para isso). O JSX pode ser personalizado através das opções `jsxFactory` e `jsxFragment`.

```bash
npx esbuild src/component.tsx --bundle --jsx=automatic --outfile=out.js
```

### Bundling de CSS

esbuild pode fazer bundle de CSS, resolver declarações `@import` e minificar.

```bash
npx esbuild src/styles.css --bundle --minify --outfile=dist/styles.min.css
```

### Source Maps

A geração rápida de source maps já está incluída. Use `--sourcemap` para mapas externos ou `--sourcemap=inline` para inline.

### Watch Mode

A flag `--watch` aciona uma reconstrução sempre que os arquivos de origem mudam. As compilações incrementais são extremamente rápidas.

```bash
npx esbuild src/app.ts --bundle --watch --outfile=dist/app.js
```

### Plugins

A API de plugins permite interceptar eventos de load, transform e resolve. Aqui está um plugin simples que registra os tamanhos dos arquivos:

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

Plugins também podem lidar com módulos virtuais, loaders personalizados e transformações avançadas.

---

## Casos de Uso & Ecossistema

esbuild não é apenas uma ferramenta autônoma – ele alimenta o núcleo de muitos frameworks modernos:

- **Vite** – usa esbuild para pré‑bundling de dependências e transforms no desenvolvimento.
- **Remix**, **Astro**, **SvelteKit** – utilizam esbuild como parte de seu pipeline de build.
- **tsup** – um bundler simples e rápido construído sobre o esbuild para bibliotecas Node.js.
- **tsx** – uma CLI que executa arquivos TypeScript diretamente usando o transform do esbuild.

> **Dica de Integração**: Se você usa Vite, pode personalizar as opções do esbuild através da configuração `optimizeDeps.esbuildOptions`.

---

## Comparação de Performance

Em testes de benchmark (fazendo bundle de um projeto típico React + TypeScript):

| Ferramenta | Tempo (s) | Velocidade Relativa |
|------------|-----------|--------------------|
| esbuild    | 0.11      | 1× (referência)    |
| Parcel 2   | 0.71      | ~6× mais lento     |
| Rollup     | 0.99      | ~9× mais lento     |
| Webpack 5  | 1.53      | ~14× mais lento    |

*Os números são aproximados e baseados em benchmarks da comunidade. Os resultados reais variam de acordo com o projeto.*

---

## Opções de Configuração

### Flags CLI Úteis

| Flag               | Description                                      |
|--------------------|--------------------------------------------------|
| `--bundle`         | Faz bundle de todas as dependências na saída.    |
| `--outfile`        | Arquivo de saída único.                          |
| `--outdir`         | Diretório de saída (use com vários entry points).|
| `--minify`         | Minifica a saída (espaços em branco, sintaxe, identificadores). |
| `--sourcemap`      | Gera source maps.                                |
| `--target`         | Ambiente alvo (ex.: `es2020`, `chrome80`).       |
| `--platform`       | `browser` ou `node` (afeta a resolução).         |
| `--format`         | Formato de saída: `iife`, `cjs`, `esm`.          |
| `--watch`          | Observa mudanças e reconstrói.                   |
| `--loader`         | Mapeia extensão de arquivo para um loader (ex.: `.png:file`). |
| `--define`         | Substitui identificadores globais por constantes. |
| `--external`       | Exclui pacotes do bundling.                      |

### Opções Comuns da API

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

## Ressalvas & Limitações

- **Nenhuma verificação de tipos do TypeScript** – o esbuild transpila apenas a sintaxe. Use `tsc --noEmit` em uma etapa separada para segurança de tipos.
- **Sem acesso à AST** – o sistema de plugins não expõe uma AST concreta para transforms personalizados.
- **Funcionalidades de CSS limitadas** – não suporta PostCSS ou Sass (use plugins ou pré‑processadores).
- **Divisão de código** – suportada apenas para formato de saída ESM.
- **Resolução estrita** – alguns casos extremos com exportações condicionais podem diferir de outros bundlers.

---

## Leitura Adicional

- [Documentação Oficial do esbuild](https://esbuild.github.io/)
- [Repositório no GitHub](https://github.com/evanw/esbuild)
- [Referência da API de Plugins](https://esbuild.github.io/plugins/)
- [Por que o esbuild é tão rápido? (Post do blog por Evan Wallace)](https://esbuild.github.io/faq/#why-is-esbuild-fast)
- [Benchmarks vs. Webpack, Rollup, Parcel](https://esbuild.github.io/faq/#benchmark-details)

---

*Gerado em 2026-06-21*