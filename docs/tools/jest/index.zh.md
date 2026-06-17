---
title: Jest
description: 一个由 Facebook 开发的令人愉悦的 JavaScript 测试框架，是广泛使用的单元测试工具。
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

## 什么是 Jest？

Jest 是一个 Meta（原 Facebook）开发的零配置 JavaScript 测试框架。它被设计得简单而快速，开箱即用地提供单元测试、集成测试和快照测试所需的一切。

## 为什么选择 Jest？

- **零配置** – 大多数 JavaScript 项目无需额外设置或配置文件。
- **快速并行执行** – 测试在隔离的工作线程中运行，执行速度快。
- **内置模拟** – 使用 `jest.fn()` 和 `jest.mock()` 轻松模拟函数和模块。
- **代码覆盖率** – 使用 Istanbul 内置覆盖率报告。
- **快照测试** – 捕获渲染输出以检测意外更改。
- **丰富的断言库** – 广泛的匹配器用于清晰且富有表现力的断言。
- **与流行库协作** – 与 React、Vue、Angular、TypeScript 和 Node 无缝集成。

## 安装

```bash
npm install --save-dev jest
```

在 `package.json` 中添加测试脚本：

```json
"scripts": {
  "test": "jest"
}
```

对于 TypeScript 支持，安装额外包：

```bash
npm install --save-dev ts-jest @types/jest
```

并配置 Jest 使用 `ts-jest`。

## 基本用法

创建一个简单的函数用于测试：

```js
// sum.js
function sum(a, b) {
  return a + b;
}
module.exports = sum;
```

编写对应的测试文件：

```js
// sum.test.js
const sum = require('./sum');

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

运行测试：

```bash
npm test
```

或

```bash
npx jest
```

## 关键特性

### 零配置

Jest 自动查找匹配 `*.test.js`、`*.spec.js` 或 `__tests__` 目录内的测试文件。它使用适用于大多数项目的合理默认设置。

### 模拟

**函数模拟：**

```js
const myMock = jest.fn();
myMock.mockReturnValue('hello');
console.log(myMock()); // 'hello'
```

**模块模拟：**

```js
jest.mock('./api');
const api = require('./api');
// 该模块自动被替换为一个返回 undefined 的模拟
```

### 快照测试

适用于 UI 组件。捕获渲染输出并与存储的快照进行比较。

```js
import renderer from 'react-test-renderer';
import MyComponent from './MyComponent';

test('renders correctly', () => {
  const tree = renderer.create(<MyComponent />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

使用 `--updateSnapshot`（或 `-u`）运行以更新失败快照。

### 代码覆盖率

通过添加 `--coverage` 标志生成覆盖率报告：

```bash
jest --coverage
```

这将生成一个包含 HTML 报告的详细 `coverage/` 目录。

### 监听模式

文件更改时自动重新运行测试。

```bash
jest --watchAll   # 针对所有测试文件
jest --watch      # 仅针对与更改文件相关的测试（需要 Git）
```

### 丰富的断言（匹配器）

常用的匹配器包括：

- `toBe` – 严格相等（`===`）
- `toEqual` – 深度相等
- `toContain` – 检查数组/可迭代对象是否包含某元素
- `toThrow` – 检查函数是否抛出异常
- `toBeTruthy` / `toBeFalsy`
- `toBeNull`、`toBeDefined`、`toBeUndefined`
- `.resolves` 和 `.rejects` – 用于 Promise

**示例：**

```js
expect(2 + 2).toBe(4);
expect({ a: 1 }).toEqual({ a: 1 });
expect([1, 2, 3]).toContain(2);
expect(() => { throw Error('fail'); }).toThrow('fail');
```

### 异步测试

使用 `async/await` 测试异步代码：

```js
test('async data', async () => {
  const data = await fetchData();
  expect(data).toBe('peanut butter');
});
```

或使用 `.resolves` / `.rejects` 匹配器：

```js
test('async resolves', () => {
  return expect(fetchData()).resolves.toBe('peanut butter');
});
```

### 设置与清理

使用生命周期钩子在测试前后运行代码：

```js
beforeAll(() => {
  // 在所有测试之前运行一次
});

afterAll(() => {
  // 在所有测试之后运行一次
});

beforeEach(() => {
  // 在每个测试之前运行
});

afterEach(() => {
  // 在每个测试之后运行
});
```

## CLI 选项

| 选项                | 描述                                              |
|-----------------------|----------------------------------------------------------|
| `--coverage`          | 生成并输出覆盖率报告。                     |
| `--watch`             | 监听文件更改并重新运行相关测试。        |
| `--watchAll`          | 监听所有文件并在更改时重新运行所有测试。         |
| `--verbose`           | 详细显示每个测试结果。               |
| `--updateSnapshot` (或 `-u`) | 更新所有快照文件。                         |
| `--testNamePattern`   | 运行名称匹配指定正则表达式的测试。           |
| `--runInBand`         | 串行运行测试（适用于调试）。               |
| `--silent`            | 抑制测试中的控制台输出。                      |
| `--clearCache`        | 清除 Jest 缓存。                                    |

## 配置

Jest 可以通过 `jest.config.js` 文件或 `package.json` 中的 `jest` 键进行配置。

**示例 `jest.config.js`：**

```js
module.exports = {
  testEnvironment: 'node',   // 'jsdom' 用于浏览器环境
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

或者，将配置添加到 `package.json`：

```json
"jest": {
  "testEnvironment": "node",
  "roots": ["src"]
}
```

## 进阶：使用 React/DOM 进行测试

结合 `@testing-library/react`：

```js
import { render, screen } from '@testing-library/react';
import MyComponent from './MyComponent';

test('renders the component', () => {
  render(<MyComponent />);
  expect(screen.getByText('Hello')).toBeInTheDocument();
});
```

## 结论

Jest 是 JavaScript 应用程序测试的事实标准。它的零配置设置、强大的模拟、快照功能以及快速并行执行使其成为任何 JavaScript 开发者的必备工具。无论您是在测试简单的函数还是复杂的 React 组件，Jest 都能提供令人愉悦且强大的测试体验。

---

*本文档为草稿，将随着 Jest 的更新而更新。*