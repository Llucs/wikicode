---
title: Vitest: Viteが支える次世代テストフレームワーク
description: 高速でViteネイティブなテストフレームワーク。シームレスなTypeScriptとESMのサポートを備え、モダンなJavaScript/TypeScriptアプリケーション向けに設計されています。
created: 2026-06-23
tags:
  - testing
  - unit-testing
  - vite
  - typescript
  - jest-alternative
status: draft
---

# Vitest: Viteが支える次世代テストフレームワーク

## 概要

VitestはViteの上に構築された次世代ユニットテストフレームワークです。Anthony FuとViteコアチームによって作成され、2021年12月にリリースされました。Viteの開発サーバーと従来のテストランナー（Jestなど）との間の摩擦に対処するために開発されました。Viteの変換パイプライン、ホットモジュールリプレイスメント（HMR）、プラグインシステムを活用することで、特に既にViteを使用しているプロジェクトにおいて、大幅に高速で一貫性のある開発者体験を提供します。

### なぜVitestなのか？

- **ネイティブESMサポート:** JestではESモジュールに複雑な変換が必要ですが、VitestはViteのrollupベースのパイプラインを使用するため、ネイティブにESMを処理します。
- **テストのHMR:** コードが変更されると影響を受けるテストのみが再実行されるため、フィードバックループがほぼ瞬時に行われます。
- **Jest API互換性:** 同じ`describe`、`it`、`expect`のAPIを使用し、モックやスパイには`jest`の代わりに`vi`を使用します。移行は簡単です。
- **ファーストクラスのTypeScript:** esbuildにより追加設定なしでTypeScriptが即座にトランスパイルされます。
- **コンポーネントテスト:** jsdom、happy-dom、Playwrightなどの環境を使用して、Vue、React、Svelte、Litのテストを組み込みでサポートします。
- **組み込みカバレッジ:** v8およびistanbulカバレッジプロバイダーを標準でサポートします。
- **Vitest UI:** テストとモジュールの依存関係を可視化するリッチなグラフィカルダッシュボードを提供します。

## インストール

Vitestを開発依存関係として追加します。

```bash
npm install -D vitest
```

yarnまたはpnpmを使用する場合:

```bash
yarn add -D vitest
pnpm add -D vitest
```

次に、`package.json`にテストスクリプトを追加します。

```json
{
  "scripts": {
    "test": "vitest"
  }
}
```

> **注記:** 単一実行（ウォッチモードなし）の場合は`vitest run`を実行します。デフォルトモードはウォッチで、変更があるとテストを再実行します。

## テストの作成

VitestはJestと同じグローバルAPIを使用します。`test`、`expect`、`describe`などは`vitest`からインポートするか、設定で`globals`を有効にします。

### 基本例

```javascript
// sum.test.js
import { expect, test } from 'vitest';
import { sum } from './sum';

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

### `describe`と`it`の使用

```typescript
import { describe, it, expect } from 'vitest';

describe('Array', () => {
  it('should be empty initially', () => {
    const arr: number[] = [];
    expect(arr).toHaveLength(0);
  });
});
```

### `vi`を使ったモック

```typescript
import { vi, test, expect } from 'vitest';

const mockFn = vi.fn();
mockFn('hello');
expect(mockFn).toHaveBeenCalledWith('hello');

// モジュールをモック
vi.mock('../api', () => ({
  fetchData: vi.fn(() => Promise.resolve({ data: 'mocked' })),
}));
```

## 設定

Vitestの設定は、プロジェクトの`vite.config.ts`ファイル（推奨）または別の`vitest.config.ts`で行います。設定は`test`プロパティの下に記述します。

```typescript
/// <reference types="vitest/config" />
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true, // インポートなしでtest/expectを使用
    environment: 'jsdom', // または 'happy-dom', 'node', 'edge-runtime'
    setupFiles: './src/setup.ts',
    include: ['src/**/*.{test,spec}.{js,ts}'],
    coverage: {
      provider: 'v8', // または 'istanbul'
      reporter: ['text', 'json', 'html'],
    },
  },
});
```

スタンドアロンの`vitest.config.ts`を使用する場合も形式は同じですが、Vite設定をエクスポートする必要があります（VitestはViteを拡張します）。

## 主な機能

### 1. テストのホットモジュールリプレイスメント（HMR）

Vitestはソースファイルとテストファイルを監視します。変更が加えられると、影響を受けるテストのみが再実行され、ほぼ瞬時にフィードバックが得られます。

```bash
vitest
```

`r`で全テスト再実行、`f`で失敗したテストのみ再実行、`q`で終了します。

### 2. ネイティブESMサポート

VitestはViteのパイプラインを使用するため、ESモジュールが自然に動作します。Babelプラグインや特別な変換は必要ありません。

### 3. Jest API互換性

| Jest | Vitest |
|------|--------|
| `jest.fn()` | `vi.fn()` |
| `jest.mock()` | `vi.mock()` |
| `jest.spyOn()` | `vi.spyOn()` |
| `jest.useFakeTimers()` | `vi.useFakeTimers()` |

すべてのライフサイクルフック（`beforeEach`、`afterEach`、`beforeAll`、`afterAll`）は同じように動作します。

### 4. ファーストクラスのTypeScript

`ts-jest`や別のBabel設定は不要です。TypeScriptテストをそのまま記述し、Vitestがesbuildによるトランスパイルを処理します。

```typescript
interface User { name: string }
function greet(user: User) { return `Hello, ${user.name}`; }

it('greets user', () => {
  expect(greet({ name: 'Alice' })).toBe('Hello, Alice');
});
```

### 5. コンポーネントテスト

Vitestは`@testing-library/vue`、`@testing-library/react`、`@vue/test-utils`などのコンポーネントテストライブラリとシームレスに連携します。`environment`オプションを使用してブラウザ環境をシミュレートします。

```typescript
// @vue/test-utilsを使った例
import { mount } from '@vue/test-utils';
import MyComponent from './MyComponent.vue';
import { describe, it, expect } from 'vitest';

describe('MyComponent', () => {
  it('renders', () => {
    const wrapper = mount(MyComponent);
    expect(wrapper.text()).toContain('Hello Vitest');
  });
});
```

### 6. コードカバレッジ

v8（デフォルト）またはistanbulによる組み込みカバレッジサポート。

```bash
vitest run --coverage
```

または設定で:

```typescript
test: {
  coverage: {
    provider: 'v8',
    all: true,
    include: ['src/**/*.ts'],
    exclude: ['src/test/', '**/*.spec.ts'],
  }
}
```

### 7. Vitest UI

テスト結果を探索するためのオプションのリッチなウェブインターフェース。

```bash
vitest --ui
```

UIはテストステータス、タイミング、ファイルツリー、モジュール依存関係グラフを含むダッシュボードを提供します。

### 8. ワークスペースモード（モノレポサポート）

Vitestは`vitest.workspace.ts`ファイルを使用して、モノレポ内の複数のプロジェクトやパッケージにわたってテストを実行できます。設定はインライン化するか、ファイルやグロブパターンを参照します。

```typescript
// vitest.workspace.ts
import { defineWorkspace } from 'vitest/config';

export default defineWorkspace([
  'packages/*',
  {
    // 特定のプロジェクトのインライン設定
    test: {
      name: 'my-package',
      root: './packages/my-package',
      environment: 'node',
    },
  },
]);
```

各プロジェクトは独自の設定を持つことができ、単一のコマンドから実行できます。

### 9. 並列実行

テストはワーカースレッド（デフォルト）または子プロセス（`pool: 'forks'`）によって並列実行されます。

```typescript
test: {
  pool: 'forks', // または 'threads' (デフォルト)
  poolOptions: {
    forks: {
      singleFork: true,
    },
  },
}
```

## コマンド例

| コマンド | 説明 |
|---------|------|
| `vitest` | ウォッチモードでテストを実行（デフォルト） |
| `vitest run` | テストを1回だけ実行（ウォッチなし） |
| `vitest run --reporter verbose` | 冗長な出力 |
| `vitest --coverage` | カバレッジレポート付きでテストを実行 |
| `vitest --ui` | Vitest UIを起動 |
| `vitest --config vitest.ci.ts` | カスタム設定ファイルを使用 |
| `vitest --project projectName` | ワークスペース内の特定のプロジェクトのテストを実行 |
| `vitest test/specific.test.ts` | 特定のテストファイルを実行 |
| `npx vitest --run --reporter json` | JSON結果を出力（CIに適しています） |

## Jestからの移行

JestからVitestへの移行は通常、以下を含みます。

1. テストファイル内の`jest`を`vi`に置き換える（spy、mock、fn）。
2. `@jest/globals`からのインポートを`vitest`に更新する（または`globals: true`を使用）。
3. Jest設定を`vite.config.ts`または`vitest.config.ts`の`test`キーに移動する。
4. モジュールモックを適応させる: `jest.mock`の代わりに`vi.mock`。
5. タイマーを調整する: `vi.useFakeTimers()`。

専用の移行ガイドが公式Vitestドキュメントで提供されています。

## ユースケース

- **ユニットテスト:** 関数、ユーティリティ、ビジネスロジック。
- **コンポーネントテスト:** Vue、React、Svelte、Solid、Litの各コンポーネント。
- **統合テスト:** APIエンドポイント、組み合わせたモジュール、シミュレート環境。
- **ライブラリ/CLI開発:** 優れたTypeScriptサポートによる高速なCI実行。
- **モノレポテスト:** ワークスペースモードでパッケージ間の統一テストを提供。

## なぜJestではなくVitestなのか？

- **ESMサポート:** 実験的モジュールや複雑な変換は不要。
- **速度:** Viteの最適化されたバンドルとesbuildトランスパイルにより、コールドスタートが高速。
- **HMR:** インスタントな再実行で効率的なTDDワークフロー。
- **よりシンプルな設定:** Vite設定を再利用。Jest固有のトランスフォーマーは不要。
- **並列実行:** ワーカースレッドはJestのデフォルトよりも優れている。
- **モダンスタックとの整合性:** Viteベースのプロジェクト（Vue、Svelte、Reactなど）向けに設計。

大規模プロジェクトやモノレポでは、VitestはJestと比較してテスト実行時間を2〜10倍短縮できます。

## 関連リソース

- [公式ドキュメント](https://vitest.dev/)
- [GitHubリポジトリ](https://github.com/vitest-dev/vitest)
- [Jestからの移行ガイド](https://vitest.dev/guide/migration.html#migrating-from-jest)
- [Vitest UIデモ](https://vitest.dev/guide/ui.html)