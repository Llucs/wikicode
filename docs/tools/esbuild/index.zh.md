---
title: esbuild — 极速的 JavaScript 与 TypeScript 打包工具
description: 一份关于 esbuild 的全面指南，这个由 Go 驱动的打包工具和压缩工具能极大加速 JavaScript 和 TypeScript 构建，内容涵盖 CLI 基础到插件开发。
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

# esbuild — 极速的 JavaScript 与 TypeScript 打包工具

## 什么是 esbuild？

esbuild 是一个**现代化、开源且支持 JavaScript、CSS、TypeScript 和 JSX 的打包工具和压缩器**。它采用 Go 语言而非 JavaScript 编写，充分利用了激进的并行性、高效的内存管理和原生代码，相较于 Webpack、Rollup 或 Parcel 等传统工具，实现了 **10–100 倍的速度提升**。

由 **Evan Wallace**（Figma 联合创始人）创建，并于 2020 年 1 月首次发布，esbuild 凭借其简洁性和惊人的性能，已成为主要框架和工具的基石。

---

## 为何选择 esbuild？

| 特性         | 优势                                                                 |
|-----------------|-------------------------------------------------------------------------|
| **速度**       | 即使是大型代码库，也能在毫秒级完成打包。        |
| **零配置** | 开箱即用 – 无需配置文件。                          |
| **单一工具** | 处理打包、压缩、转译、源码映射等。 |
| **现代代码** | 支持 ESM、CommonJS 及两者混合。                           |
| **可扩展**  | 插件系统（JavaScript 和 Go）用于自定义加载器和转换器。  |

esbuild 适用于：
- **高性能开发**，等待时间至关重要。
- **框架工具化** – 被 Vite、Remix、Astro、SvelteKit 等使用。
- **库发布** – 为 Node.js 包提供快速的同步解析。
- **快速原型开发** – 通过一条 CLI 命令打包 TypeScript 文件。

---

## 安装

```bash
# Install locally as a dev dependency
npm install --save-dev esbuild

# or using yarn / pnpm
yarn add -D esbuild
pnpm add -D esbuild
```

这会自动安装适用于当前平台的可执行文件。你也可以从 [GitHub 发布页](https://github.com/evanw/esbuild/releases) 下载静态二进制文件。

> **注意**：esbuild 需要 Node.js 12 及以上版本。它在打包**无需** Babel、`tsc` 或 Terser – 所有功能都内置。

---

## 快速入门

### 1. CLI 基础

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

### 3. Transform API（快速转译）

```javascript
import { transformSync } from 'esbuild'

const code = `const x: number = 1; console.log(x)`
const result = transformSync(code, { loader: 'ts', target: 'es2020' })
console.log(result.code)
// Output: const x = 1; console.log(x);
```

---

## 关键特性与示例

### 打包（CommonJS + ESM）

esbuild 会自动解析 `require()` 和 `import` 语句。它可以在同一个包中混合使用模块系统。

```bash
# Bundle a file that imports both ESM and CJS packages
npx esbuild src/main.js --bundle --outfile=out.js --format=esm
```

### 压缩

内置的压缩工具通常比 Terser **快 10 倍**，且输出相同或更小。

```bash
npx esbuild src/app.ts --bundle --minify --outfile=dist/app.min.js
```

### Tree Shaking

使用 `--bundle` 时，未使用的导出会自动移除。在 `package.json` 中将无副作用的模块显式标记为 `"sideEffects": false`。

### TypeScript 与 JSX 转译

esbuild 会移除类型并转换 JSX，**但不执行类型检查**（需使用 `tsc --noEmit`）。可通过 `jsxFactory` 和 `jsxFragment` 选项自定义 JSX。

```bash
npx esbuild src/component.tsx --bundle --jsx=automatic --outfile=out.js
```

### CSS 打包

esbuild 可以打包 CSS、解析 `@import` 语句并进行压缩。

```bash
npx esbuild src/styles.css --bundle --minify --outfile=dist/styles.min.css
```

### Source Maps

内置快速的源代码映射生成。使用 `--sourcemap` 生成外部映射，或使用 `--sourcemap=inline` 生成内联映射。

### 监听模式

`--watch` 标志会在源文件发生变更时触发重新构建。增量构建非常快速。

```bash
npx esbuild src/app.ts --bundle --watch --outfile=dist/app.js
```

### 插件

插件 API 允许拦截加载、转换和解析事件。以下是一个简单插件，用于记录文件大小：

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

插件还可以处理虚拟模块、自定义加载器和高级转换。

---

## 使用场景与生态系统

esbuild 不仅仅是一个独立工具——它为许多现代框架提供了核心动力：

- **Vite** – 使用 esbuild 进行依赖预打包和开发转换。
- **Remix**、**Astro**、**SvelteKit** – 在其构建流程中利用 esbuild。
- **tsup** – 基于 esbuild 构建的简单快速打包工具，适用于 Node.js 库。
- **tsx** – 一个 CLI，可直接使用 esbuild 的转换功能运行 TypeScript 文件。

> **集成提示**：如果你使用 Vite，可以通过 `optimizeDeps.esbuildOptions` 配置自定义 esbuild 选项。

---

## 性能对比

| 工具       | 耗时（秒） | 相对速度           |
|------------|------------|--------------------|
| esbuild    | 0.11       | 1×（基准）         |
| Parcel 2   | 0.71       | 慢约 6 倍          |
| Rollup     | 0.99       | 慢约 9 倍          |
| Webpack 5  | 1.53       | 慢约 14 倍         |

*数据大致基于社区基准测试。实际结果因项目而异。*

---

## 配置选项

### 有用 CLI 标志

| 标志               | 描述                                            |
|--------------------|--------------------------------------------------|
| `--bundle`         | 将所有依赖打包到输出中。         |
| `--outfile`        | 单个输出文件。                              |
| `--outdir`         | 输出目录（与多个入口点一起使用）。|
| `--minify`         | 压缩输出（空白、语法、标识符）。 |
| `--sourcemap`      | 生成源代码映射。                            |
| `--target`         | 目标环境（例如 `es2020`、`chrome80`）。 |
| `--platform`       | `browser` 或 `node`（影响解析方式）。        |
| `--format`         | 输出格式：`iife`、`cjs`、`esm`。             |
| `--watch`          | 监听变更并重新构建。                   |
| `--loader`         | 将文件扩展名映射到加载器（例如 `.png:file`）|
| `--define`         | 用常量替换全局标识符。       |
| `--external`       | 从打包中排除包。                  |

### 常见 API 选项

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

## 注意事项与局限

- **无 TypeScript 类型检查** – esbuild 仅转译语法。需在单独步骤中使用 `tsc --noEmit` 进行类型检查。
- **无 AST 访问** – 插件系统不暴露具体 AST 供自定义转换。
- **CSS 功能有限** – 不支持 PostCSS 或 Sass（使用插件或预处理器）。
- **代码分割** – 仅支持 ESM 输出格式。
- **严格解析** – 某些条件导出的边缘情况可能与其他打包工具不同。

---

## 进一步阅读

- [esbuild 官方文档](https://esbuild.github.io/)
- [GitHub 仓库](https://github.com/evanw/esbuild)
- [插件 API 参考](https://esbuild.github.io/plugins/)
- [esbuild 为何如此之快？（Evan Wallace 的博文）](https://esbuild.github.io/faq/#why-is-esbuild-fast)
- [与 Webpack、Rollup、Parcel 的基准测试对比](https://esbuild.github.io/faq/#benchmark-details)

---

*生成于 2026-06-21*