---title: esbuild — 超高速なJavaScript & TypeScriptバンドラー
description: esbuild（Goで動作するバンドラー兼ミニファイア）の包括的ガイド。CLIの基本からプラグイン開発まで、JavaScriptとTypeScriptのビルドを劇的に高速化します。
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

# esbuild — 超高速なJavaScript & TypeScriptバンドラー

## esbuildとは？

esbuildはJavaScript、CSS、TypeScript、JSX向けの**モダンでオープンソースなバンドラー兼ミニファイア**です。JavaScriptではなくGoで記述されており、積極的な並列処理、効率的なメモリ管理、ネイティブコードを活用することで、Webpack、Rollup、Parcelなどの従来ツールと比較して**10〜100倍の速度向上**を実現します。

**Evan Wallace**（Figmaの共同創設者）によって作成され、2020年1月に初めてリリースされたesbuildは、そのシンプルさと驚異的なパフォーマンスにより、主要なフレームワークやツールの基盤となっています。

---

## esbuildを選ぶ理由

| 機能 | 利点 |
|-----------------|-------------------------------------------------------------------------|
| **速度** | 大規模コードベースでもミリ秒単位でバンドルを構築可能。 |
| **設定不要** | すぐに使える – 設定ファイルは不要。 |
| **単一ツール** | バンドル、ミニファイ、トランスパイル、ソースマップなどを処理。 |
| **モダンコード** | ESM、CommonJS、両方の混在をサポート。 |
| **拡張性** | プラグインシステム（JavaScriptおよびGo）でカスタムローダーや変換が可能。 |

esbuildは以下のような場面に最適です：

- **高速な開発** – 待ち時間が重要な場合。
- **フレームワークツール** – Vite、Remix、Astro、SvelteKitなどで使用されています。
- **ライブラリ公開** – Node.jsパッケージ向けの高速な同期的解決。
- **迅速なプロトタイピング** – 1つのCLIコマンドでTypeScriptファイルをバンドル。

---

## インストール

```bash
# Install locally as a dev dependency
npm install --save-dev esbuild

# or using yarn / pnpm
yarn add -D esbuild
pnpm add -D esbuild
```

これにより、プラットフォーム固有のバイナリが自動的にインストールされます。[GitHub releases](https://github.com/evanw/esbuild/releases)ページから静的バイナリをダウンロードすることもできます。

> **注記**: esbuildはNode.js 12+が必要です。Babel、`tsc`、Terserを必要と**せずに**バンドルします – すべてが組み込まれています。

---

## クイックスタート

### 1. CLIの基本

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

### 3. Transform API（高速トランスパイル）

```javascript
import { transformSync } from 'esbuild'

const code = `const x: number = 1; console.log(x)`
const result = transformSync(code, { loader: 'ts', target: 'es2020' })
console.log(result.code)
// Output: const x = 1; console.log(x);
```

---

## 主な機能と例

### バンドル（CommonJS + ESM）

esbuildは`require()`と`import`の両方の文を自動的に解決します。同じバンドル内でモジュールシステムを混在させることができます。

```bash
# Bundle a file that imports both ESM and CJS packages
npx esbuild src/main.js --bundle --outfile=out.js --format=esm
```

### ミニファイ

組み込みのミニファイアはTerserよりも**10倍高速**で、同一またはより小さな出力を生成します。

```bash
npx esbuild src/app.ts --bundle --minify --outfile=dist/app.min.js
```

### ツリーシェイキング

`--bundle`を使用すると、未使用のエクスポートが自動的に削除されます。`package.json`で`"sideEffects": false`を使用して副作用のないモジュールを明示的にマークします。

### TypeScriptとJSXのトランスパイル

esbuildは型を除去しJSXを変換しますが、**型チェックは実行しません**（型チェックには`tsc --noEmit`を使用してください）。JSXは`jsxFactory`および`jsxFragment`オプションでカスタマイズできます。

```bash
npx esbuild src/component.tsx --bundle --jsx=automatic --outfile=out.js
```

### CSSのバンドル

esbuildはCSSのバンドル、`@import`文の解決、ミニファイが可能です。

```bash
npx esbuild src/styles.css --bundle --minify --outfile=dist/styles.min.css
```

### ソースマップ

高速なソースマップ生成が組み込まれています。外部マップには`--sourcemap`、インラインには`--sourcemap=inline`を使用します。

### ウォッチモード

`--watch`フラグは、ソースファイルが変更されるたびに再ビルドをトリガーします。インクリメンタルビルドは非常に高速です。

```bash
npx esbuild src/app.ts --bundle --watch --outfile=dist/app.js
```

### プラグイン

プラグインAPIは、ロード、変換、解決イベントをインターセプトできます。以下はファイルサイズをログ出力するシンプルなプラグインです：

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

プラグインは仮想モジュール、カスタムローダー、高度な変換も処理できます。

---

## ユースケースとエコシステム

esbuildは単なる独立したツールではなく、多くのモダンフレームワークの中核を担っています：

- **Vite** – esbuildを依存関係のプリバンドルと開発用変換に使用。
- **Remix**、**Astro**、**SvelteKit** – ビルドパイプラインの一部としてesbuildを活用。
- **tsup** – esbuild上に構築されたNode.jsライブラリ向けのシンプルで高速なバンドラー。
- **tsx** – esbuildの変換機能を使用してTypeScriptファイルを直接実行するCLI。

> **統合のヒント**: Viteを使用している場合、`optimizeDeps.esbuildOptions`設定を介してesbuildオプションをカスタマイズできます。

---

## パフォーマンス比較

ベンチマークテスト（典型的なReact + TypeScriptプロジェクトのバンドル）において：

| ツール       | 時間（秒） | 相対速度 |
|------------|----------|----------------|
| esbuild    | 0.11     | 1× (baseline)  |
| Parcel 2   | 0.71     | ~6× slower     |
| Rollup     | 0.99     | ~9× slower     |
| Webpack 5  | 1.53     | ~14× slower    |

*数値はコミュニティのベンチマークに基づくおおよその値です。実際の結果はプロジェクトによって異なります。*

---

## 設定オプション

### 便利なCLIフラグ

| フラグ               | 説明                                      |
|--------------------|--------------------------------------------------|
| `--bundle`         | すべての依存関係を出力にバンドルします。 |
| `--outfile`        | 単一の出力ファイル。 |
| `--outdir`         | 出力ディレクトリ（複数のエントリポイントで使用）。 |
| `--minify`         | 出力をミニファイ（空白、構文、識別子）。 |
| `--sourcemap`      | ソースマップを生成します。 |
| `--target`         | ターゲット環境（例：`es2020`、`chrome80`）。 |
| `--platform`       | `browser`または`node`（解決に影響）。 |
| `--format`         | 出力形式：`iife`、`cjs`、`esm`。 |
| `--watch`          | ファイルの変更を監視して再ビルドします。 |
| `--loader`         | ファイル拡張子をローダーにマッピング（例：`.png:file`）。 |
| `--define`         | グローバル識別子を定数で置き換えます。 |
| `--external`       | バンドルからパッケージを除外します。 |

### 一般的なAPIオプション

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

## 注意点と制限事項

- **TypeScriptの型チェックなし** – esbuildは構文のみをトランスパイルします。型安全性のために、別途`tsc --noEmit`を使用してください。
- **ASTアクセス不可** – プラグインシステムはカスタム変換のための具体的なASTを公開しません。
- **CSS機能は限定的** – PostCSSやSassはサポートしていません（プラグインやプリプロセッサを使用してください）。
- **コード分割** – ESM出力形式でのみサポートされています。
- **厳格な解決** – 条件付きエクスポートに関する一部のエッジケースは、他のバンドラーと異なる場合があります。

---

## 関連リンク

- [esbuild公式ドキュメント](https://esbuild.github.io/)
- [GitHubリポジトリ](https://github.com/evanw/esbuild)
- [プラグインAPIリファレンス](https://esbuild.github.io/plugins/)
- [なぜesbuildはそんなに速いのか? (Evan Wallaceによるブログ記事)](https://esbuild.github.io/faq/#why-is-esbuild-fast)
- [Webpack、Rollup、Parcelとのベンチマーク比較](https://esbuild.github.io/faq/#benchmark-details)

---

*2026-06-21 生成*