---
title: UnoCSS：ゼロコンフィグ、ジャストインタイムCSSフレームワーク
description: UnoCSSについての詳細なガイド。これはゼロコンフィグ、ジャストインタイム（JIT）CSSフレームワークで、スタイルを実行時に生成します。インストール、使用法、および主要な機能について学びます。
created: 2026-07-08
tags:
  - UnoCSS
  - CSS-in-JS
  - JIT
  - Tailwind
  - 性能
status: 草稿
---

# UnoCSS：ゼロコンフィグ、ジャストインタイムCSSフレームワーク

UnoCSSは、ゼロコンフィグ、ジャストインタイム（JIT）CSSフレームワークで、スタイルを実行時に生成します。主にTypeScriptで書かれています。従来のCSS-in-JSライブラリはスタイルを事前に処理してバンドルしますが、UnoCSSはコードで使用されるクラスに基づいて実行時にスタイルをコンパイルします。このアプローチにより、必要なスタイルのみが適用されるため、バンドルサイズが小さくなり、性能が向上します。

## 主な機能
1. **ジャストインタイムコンパイル**: UnoCSSはスタイルを実行時に生成し、プロジェクトで実際には使用されるクラスのみが最終出力に含まれることを確保します。
2. **小さなサイズ**: UnoCSSは非常に軽量で、プロジェクトの性能に最小限の影響を与える小さなフットプリントを持っています。
3. **ツリークショーニングフレンドリー**: 生成されたスタイルはツリークショーニングされ、ビルドプロセスで使用されていないスタイルは削除されるため、最終バンドルが最適化されます。
4. **カスタマイズ**: UnoCSSはオプションとプラグインを通じて広範なカスタマイズが可能です、これによりさまざまな使用ケースに対応できます。
5. **バンドルなし**: マニフェストCSSインジャスライブラリとは異なり、UnoCSSはスタイルをバンドルしません。これにより、初期ロード時間が短くなり、性能が向上します。

## インストール

UnoCSSはnpmまたはyarn経由でインストールできます。npmを使用してインストールする方法は以下の通りです：

```bash
npm install unocss
```

また、Viteを使用している場合、次の通りインストールすることも可能です：

```bash
npm install unocss@next
```

## 基本的な使用法

### 1. 設定ファイルを作成する

UnoCSSは設定ファイルを使用して動作をカスタマイズします。基本的な設定は次の通りです：

```javascript
// unocss.config.js
export default {
  theme: {},
  shortcuts: {},
  rules: [],
};
```

### 2. UnoCSSをビルドツールに追加する

ビルドツールによっては、UnoCSSを追加する必要があるため、Viteの場合、`vite.config.js`ファイルに追加します：

```javascript
import { defineConfig } from 'vite';
import unocss from 'unocss';
import { presetUno } from 'unocss';

export default defineConfig({
  plugins: [
    unocss({
      preset: presetUno(),
    }),
  ],
});
```

### 3. UnoCSSを使用するコンポーネント

現在のコードで使用されるクラスに基づいて UnoCSS スタイルが生成されるため、コンポーネントで UnoCSS クラスを使用できます。たとえば、Vueコンポーネントでは：

```vue
<template>
  <div class="text-red-500 font-bold">Hello UnoCSS!</div>
</template>

<script setup>
// 追加の設定は必要ありません
</script>

<style scoped>
/* スタイルは通常のように入力できます */
</style>
```

### 4. スタイルの生成

UnoCSSはクラスを使用するたびにスタイルを生成します。追加のCSSやSCSSを書く必要はありません。

## キー機能とコマンド例

### 1. カスタマイズ

設定ファイルを通じて UnoCSS をカスタマイズします：

```javascript
// unocss.config.js
export default {
  theme: {
    colors: {
      primary: '#007bff',
    },
  },
  shortcuts: {
    'btn-primary': 'text-white bg-primary p-2 rounded',
  },
  rules: [
    ['hover:bg-red-500', ':hover'],
  ],
};
```

### 2. インスペクター

UnoCSS インスペクターは、開発用のデバッグツールで、ソースコード内のユーテリティクラスの位置を意識した分析を提供します。これはunocssと@unocss/viteに含まれています。Viteのデベロップサーバーで`localhost:5173/__unocss`を訪問することでインスペクターを使用できます。インスペクターは生成されたCSSルールと各ファイルに適用されたクラスを inspect できます。また、現在の設定に基づいてユーテリティをテストするための REPL を提供します。

### 3. タリークショーニング

ツリークショーニングを確保するために、ビルドツールを適切に設定します。Viteの場合、次の設定を使用します：

```javascript
import unocss from 'unocss';

export default defineConfig({
  plugins: [
    unocss({
      preset: presetUno(),
      treeShake: true,
    }),
  ],
});
```

### 4. プリセット

プリセットUnoは、一般的に使用されるルールとショートカットの前設定です。次のようになります：

```javascript
import { presetUno } from 'unocss';

export default defineConfig({
  plugins: [
    unocss({
      preset: presetUno(),
    }),
  ],
});
```

## 結論

UnoCSSは現代のWebアプリケーションでCSSを最適化する強力なツールです。ジャストインタイムコンパイル、軽量化、柔軟性により、パフォーマンスを最適化するプロジェクトに最適です。大規模なWebアプリケーション、コンポーネントライブラリ、静的サイトを扱っている場合でも、UnoCSSはバンドルサイズを小さくし、パフォーマンスを向上させます。

---