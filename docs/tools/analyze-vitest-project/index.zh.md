---
title: Vitest: 由Vite驱动的下一代测试框架
description: 一个快速、原生于Vite的测试框架，无缝支持TypeScript和ESM，专为现代JavaScript/TypeScript应用设计。
created: 2026-06-23
tags:
  - testing
  - unit-testing
  - vite
  - typescript
  - jest-alternative
status: draft
---

# Vitest: 由Vite驱动的下一代测试框架

## 概述

Vitest 是一个基于 Vite 构建的下一代单元测试框架。由 Anthony Fu 和 Vite 核心团队创建，于 2021 年 12 月发布，旨在解决 Vite 开发服务器与像 Jest 这样的传统测试运行器之间的摩擦。通过利用 Vite 的转换管道、热模块替换（HMR）和插件系统，Vitest 提供了显著更快且更一致的开发体验，特别是对于已经在使用 Vite 的项目。

### 为什么选择 Vitest？

- **原生 ESM 支持：** 与 Jest 不同，Jest 需要复杂的转换来处理 ES 模块，而 Vitest 原生处理 ESM，因为它使用 Vite 基于 rollup 的管道。
- **测试的 HMR：** 仅当代码更改时受影响的部分重新运行，使得反馈循环几乎即时。
- **Jest API 兼容性：** 使用相同的 `describe`、`it`、`expect` API，用 `vi` 替代 `jest` 进行模拟（mocking）和监视（spies）。迁移非常简单。
- **一流的 TypeScript 支持：** TypeScript 通过 esbuild 即时编译，无需额外配置。
- **组件测试：** 内置对 Vue、React、Svelte 和 Lit 的支持，并提供 jsdom、happy-dom 和 Playwright 等环境。
- **内置覆盖率：** 开箱即支持 v8 和 istanbul 覆盖率提供者。
- **Vitest UI：** 一个丰富的图形化仪表盘，用于可视化测试和模块依赖项。

## 安装

将 Vitest 添加为开发依赖：

```bash
npm install -D vitest
```

使用 yarn 或 pnpm：

```bash
yarn add -D vitest
pnpm add -D vitest
```

然后，在 `package.json` 中添加一个测试脚本：

```json
{
  "scripts": {
    "test": "vitest"
  }
}
```

> **注意：** 运行 `vitest run` 进行单次运行（无监听模式）。默认模式为监听模式，在文件更改时重新运行测试。

## 编写测试

Vitest 使用与 Jest 相同的全局 API。从 `vitest` 导入 `test`、`expect`、`describe` 等，或在配置中启用 `globals`。

### 基本示例

```javascript
// sum.test.js
import { expect, test } from 'vitest';
import { sum } from './sum';

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

### 使用 `describe` 和 `it`

```typescript
import { describe, it, expect } from 'vitest';

describe('Array', () => {
  it('should be empty initially', () => {
    const arr: number[] = [];
    expect(arr).toHaveLength(0);
  });
});
```

### 使用 `vi` 进行模拟

```typescript
import { vi, test, expect } from 'vitest';

const mockFn = vi.fn();
mockFn('hello');
expect(mockFn).toHaveBeenCalledWith('hello');

// 模拟一个模块
vi.mock('../api', () => ({
  fetchData: vi.fn(() => Promise.resolve({ data: 'mocked' })),
}));
```

## 配置

Vitest 可以在项目的 `vite.config.ts` 文件（推荐）或单独的 `vitest.config.ts` 中配置。配置位于 `test` 属性下。

```typescript
/// <reference types="vitest/config" />
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true, // use test/expect without importing
    environment: 'jsdom', // or 'happy-dom', 'node', 'edge-runtime'
    setupFiles: './src/setup.ts',
    include: ['src/**/*.{test,spec}.{js,ts}'],
    coverage: {
      provider: 'v8', // or 'istanbul'
      reporter: ['text', 'json', 'html'],
    },
  },
});
```

如果使用独立的 `vitest.config.ts`，格式相同，但必须导出 Vite 配置（Vitest 扩展了 Vite）。

## 主要特性

### 1. 测试的热模块替换（HMR）

Vitest 会监听源文件和测试文件。当发生更改时，仅受影响的相关测试会重新运行，提供近乎即时的反馈。

```bash
vitest
```

按下 `r` 重新运行所有测试，`f` 仅重新运行失败的测试，`q` 退出。

### 2. 原生 ESM 支持

由于 Vitest 使用 Vite 的管道，ES 模块可自然工作。无需 Babel 插件或特殊转换。

### 3. Jest API 兼容性

| Jest | Vitest |
|------|--------|
| `jest.fn()` | `vi.fn()` |
| `jest.mock()` | `vi.mock()` |
| `jest.spyOn()` | `vi.spyOn()` |
| `jest.useFakeTimers()` | `vi.useFakeTimers()` |

所有生命周期钩子（`beforeEach`、`afterEach`、`beforeAll`、`afterAll`）的工作方式相同。

### 4. 一流的 TypeScript 支持

无需 `ts-jest` 或单独的 Babel 配置。直接编写 TypeScript 测试，Vitest 会通过 esbuild 处理编译。

```typescript
interface User { name: string }
function greet(user: User) { return `Hello, ${user.name}`; }

it('greets user', () => {
  expect(greet({ name: 'Alice' })).toBe('Hello, Alice');
});
```

### 5. 组件测试

Vitest 与 `@testing-library/vue`、`@testing-library/react` 和 `@vue/test-utils` 等组件测试库无缝协作。使用 `environment` 选项来模拟浏览器环境。

```typescript
// Example with @vue/test-utils
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

### 6. 代码覆盖率

通过 v8（默认）或 istanbul 内置覆盖率支持。

```bash
vitest run --coverage
```

Or via configuration:

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

一个可选的、丰富的 Web 界面，用于浏览测试结果。

```bash
vitest --ui
```

UI 提供了一个仪表盘，包含测试状态、计时、文件树和模块依赖图。

### 8. 工作区模式（Monorepo 支持）

Vitest 可以使用 `vitest.workspace.ts` 文件在 Monorepo 的多个项目或包中运行测试。配置可以内联或引用文件/glob 模式。

```typescript
// vitest.workspace.ts
import { defineWorkspace } from 'vitest/config';

export default defineWorkspace([
  'packages/*',
  {
    // 特定项目的内联配置
    test: {
      name: 'my-package',
      root: './packages/my-package',
      environment: 'node',
    },
  },
]);
```

每个项目可以有自己的配置，但通过单个命令运行。

### 9. 并行执行

测试通过工作线程（默认）或子进程（设置 `pool: 'forks'`）并行运行。

```typescript
test: {
  pool: 'forks', // or 'threads' (default)
  poolOptions: {
    forks: {
      singleFork: true,
    },
  },
}
```

## 命令示例

| 命令 | 描述 |
|---------|-------------|
| `vitest` | 以监听模式运行测试（默认） |
| `vitest run` | 运行测试一次（无监听） |
| `vitest run --reporter verbose` | 详细输出 |
| `vitest --coverage` | 运行测试并生成覆盖率报告 |
| `vitest --ui` | 启动 Vitest UI |
| `vitest --config vitest.ci.ts` | 使用自定义配置文件 |
| `vitest --project projectName` | 运行工作区中特定项目的测试 |
| `vitest test/specific.test.ts` | 运行特定的测试文件 |
| `npx vitest --run --reporter json` | 输出 JSON 结果（CI 友好） |

## 从 Jest 迁移

从 Jest 迁移到 Vitest 通常涉及：

1. 将测试文件中的 `jest` 替换为 `vi`（spy、mock、fn）。
2. 将导入从 `@jest/globals` 更新为 `vitest`（或使用 `globals: true`）。
3. 将 Jest 配置移动到 `vite.config.ts` 或 `vitest.config.ts` 的 `test` 键下。
4. 调整模块模拟：使用 `vi.mock` 替代 `jest.mock`。
5. 调整定时器：使用 `vi.useFakeTimers()`。

官方 Vitest 文档中提供了专门的迁移指南。

## 使用场景

- **单元测试：** 函数、工具函数和业务逻辑。
- **组件测试：** Vue、React、Svelte、Solid 和 Lit 组件。
- **集成测试：** API 端点、组合模块，配合模拟环境。
- **库 / CLI 开发：** 快速的 CI 运行，并拥有出色的 TypeScript 支持。
- **Monorepo 测试：** 工作区模式提供了跨包的统一测试。

## 为什么选择 Vitest 而非 Jest？

- **ESM 支持：** 无需实验性模块或复杂转换。
- **速度：** 由于 Vite 的优化打包和 esbuild 编译，冷启动更快。
- **HMR：** 即时重跑，实现高效的 TDD 工作流。
- **更简单的配置：** 复用 Vite 配置；无需 Jest 专属的转换器。
- **并行执行：** 工作线程优于 Jest 的默认方式。
- **与现代技术栈对齐：** 专为基于 Vite 的项目设计（Vue、Svelte、React 等）。

对于大型项目和 Monorepo，与 Jest 相比，Vitest 可以将测试执行时间缩短 2-10 倍。

## 附加资源

- [官方文档](https://vitest.dev/)
- [GitHub 仓库](https://github.com/vitest-dev/vitest)
- [从 Jest 迁移指南](https://vitest.dev/guide/migration.html#migrating-from-jest)
- [Vitest UI 演示](https://vitest.dev/guide/ui.html)