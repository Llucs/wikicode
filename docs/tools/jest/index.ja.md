---
title: Jest
description: Facebookが開発した、ユニットテストに広く使用されている楽しいJavaScriptテストフレームワーク
created: 2026-06-15
tags:
  - javascript
  - testing
  - jest
  - unit-testing
  - meta
status: draft
ecosystem: javascript
---

# Jest

## Jestとは

Jestは、Meta（旧Facebook）が開発したゼロコンフィグレーションのJavaScriptテストフレームワークです。シンプルで高速になるように設計されており、ユニットテスト、統合テスト、スナップショットテストに必要なものをすべてすぐに提供します。

## Jestを選ぶ理由

- **ゼロコンフィグレーション** – ほとんどのJavaScriptプロジェクトで追加のセットアップや設定ファイルは不要です。
- **高速な並列実行** – テストは分離されたワーカーで実行され、高速に動作します。
- **組み込みのモック** – `jest.fn()` や `jest.mock()` を使って関数やモジュールを簡単にモックできます。
- **コードカバレッジ** – Istanbulを使用したカバレッジレポートが組み込まれています。
- **スナップショットテスト** – レンダリングされた出力をキャプチャして、意図しない変更を検出します。
- **豊富なアサーションライブラリ** – 明確で表現力豊かなアサーションのための幅広いマッチャーを提供します。
- **人気ライブラリとの連携** – React、Vue、Angular、TypeScript、Nodeとのシームレスな統合が可能です。

## インストール

```bash
npm install --save-dev jest
```

テストスクリプトを `package.json` に追加します：

```json
"scripts": {
  "test": "jest"
}
```

TypeScriptをサポートするには、追加のパッケージをインストールします：

```bash
npm install --save-dev ts-jest @types/jest
```

そしてJestが `ts-jest` を使用するように設定します。

## 基本的な使い方

テストする簡単な関数を作成します：

```js
// sum.js
function sum(a, b) {
  return a + b;
}
module.exports = sum;
```

対応するテストファイルを記述します：

```js
// sum.test.js
const sum = require('./sum');

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

テストを実行します：

```bash
npm test
```

または

```bash
npx jest
```

## 主な機能

### ゼロコンフィグレーション

Jestは、`*.test.js`、`*.spec.js`、または `__tests__` ディレクトリ内のファイルに一致するテストファイルを自動的に検索します。ほとんどのプロジェクトで動作する適切なデフォルト設定を使用します。

### モック

**関数のモック:**

```js
const myMock = jest.fn();
myMock.mockReturnValue('hello');
console.log(myMock()); // 'hello'
```

**モジュールのモック:**

```js
jest.mock('./api');
const api = require('./api');
// モジュールは自動的にundefinedを返すモックに置き換えられます
```

### スナップショットテスト

UIコンポーネントに便利です。レンダリングされた出力をキャプチャし、保存されたスナップショットと比較します。

```js
import renderer from 'react-test-renderer';
import MyComponent from './MyComponent';

test('renders correctly', () => {
  const tree = renderer.create(<MyComponent />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

失敗したスナップショットを更新するには `--updateSnapshot`（または `-u`）を付けて実行します。

### コードカバレッジ

`--coverage` フラグを追加してカバレッジレポートを生成します：

```bash
jest --coverage
```

これにより、HTMLレポートを含む詳細な `coverage/` ディレクトリが生成されます。

### ウォッチモード

ファイルが変更されると自動的にテストを再実行します。

```bash
jest --watchAll   # すべてのテストファイルに対して
jest --watch      # 変更されたファイルに関連するテストのみ（Gitが必要）
```

### 豊富なアサーション（マッチャー）

一般的なマッチャーには次のものがあります：

- `toBe` – 厳密な等価性（`===`）
- `toEqual` – 深い等価性
- `toContain` – 配列/イテラブルにアイテムが含まれているかを確認
- `toThrow` – 関数が例外をスローするかを確認
- `toBeTruthy` / `toBeFalsy`
- `toBeNull`、`toBeDefined`、`toBeUndefined`
- `.resolves` および `.rejects` – プロミス用

**例:**

```js
expect(2 + 2).toBe(4);
expect({ a: 1 }).toEqual({ a: 1 });
expect([1, 2, 3]).toContain(2);
expect(() => { throw Error('fail'); }).toThrow('fail');
```

### 非同期テスト

`async/await` を使って非同期コードをテストします：

```js
test('async data', async () => {
  const data = await fetchData();
  expect(data).toBe('peanut butter');
});
```

または `.resolves` / `.rejects` マッチャーを使用します：

```js
test('async resolves', () => {
  return expect(fetchData()).resolves.toBe('peanut butter');
});
```

### セットアップとティアダウン

ライフサイクルフックを使用して、テストの前後にコードを実行します：

```js
beforeAll(() => {
  // すべてのテストの前に1回実行
});

afterAll(() => {
  // すべてのテストの後に1回実行
});

beforeEach(() => {
  // 各テストの前に実行
});

afterEach(() => {
  // 各テストの後に実行
});
```

## CLIオプション

| オプション              | 説明                                                      |
|-------------------------|-----------------------------------------------------------|
| `--coverage`            | カバレッジレポートを生成して出力します。                  |
| `--watch`               | ファイルの変更を監視し、関連するテストを再実行します。    |
| `--watchAll`            | すべてのファイルを監視し、変更時にすべてのテストを再実行します。 |
| `--verbose`             | 個々のテスト結果を詳細に表示します。                      |
| `--updateSnapshot` (または `-u`) | すべてのスナップショットファイルを更新します。        |
| `--testNamePattern`     | 正規表現パターンに一致する名前のテストを実行します。      |
| `--runInBand`           | テストを直列に実行します（デバッグに便利です）。          |
| `--silent`              | テストからのコンソール出力を抑制します。                  |
| `--clearCache`          | Jestのキャッシュをクリアします。                           |

## 設定

Jestは `jest.config.js` ファイルまたは `package.json` の `jest` キーを介して設定できます。

**例 `jest.config.js`:**

```js
module.exports = {
  testEnvironment: 'node',   // 'jsdom' はブラウザ風環境
  roots: ['src'],
  testMatch: [
    '**/__tests__/**/*.js',
    '**/?(*.)+(spec|test).js'
  ],
  moduleNameMapper: {
    '\\.(css|less)$': '<rootDir>/__mocks__/styleMock.js'
  }
};
```

または、設定を `package.json` に追加します：

```json
"jest": {
  "testEnvironment": "node",
  "roots": ["src"]
}
```

## 発展: React/DOMのテスト

`@testing-library/react` を使用する：

```js
import { render, screen } from '@testing-library/react';
import MyComponent from './MyComponent';

test('renders the component', () => {
  render(<MyComponent />);
  expect(screen.getByText('Hello')).toBeInTheDocument();
});
```

## 結論

JestはJavaScriptアプリケーションのテストにおける事実上の標準です。ゼロコンフィグのセットアップ、堅牢なモック、スナップショット機能、高速な並列実行により、JavaScript開発者にとって不可欠なツールとなっています。単純な関数のテストから複雑なReactコンポーネントのテストまで、Jestは楽しく強力なテスト体験を提供します。

---

*このドキュメントはドラフトであり、Jestの進化に伴い更新されます。*