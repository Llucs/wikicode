---
title: Vitest: Next-Generation Testing Framework Powered by Vite
description: A fast, Vite-native testing framework with seamless TypeScript and ESM support, designed for modern JavaScript/TypeScript applications.
created: 2026-06-23
tags:
  - testing
  - unit-testing
  - vite
  - typescript
  - jest-alternative
status: draft
---

# Vitest: Next-Generation Testing Framework Powered by Vite

## Overview

Vitest is a next-generation unit testing framework built on top of Vite. Created by Anthony Fu and the Vite core team, it was released in December 2021 to address the friction between Vite's development server and traditional test runners like Jest. By leveraging Vite's transformation pipeline, Hot Module Replacement (HMR), and plugin system, Vitest delivers a significantly faster and more consistent developer experience, especially for projects already using Vite.

### Why Vitest?

- **Native ESM Support:** Unlike Jest, which requires complex transforms for ES Modules, Vitest handles ESM natively because it uses Vite's rollup-based pipeline.
- **HMR for Tests:** Only affected tests re-run when code changes, making the feedback loop nearly instant.
- **Jest API Compatibility:** Uses the same `describe`, `it`, `expect` API, with `vi` replacing `jest` for mocking and spies. Migration is straightforward.
- **First-Class TypeScript:** TypeScript is transpiled instantly via esbuild without additional configuration.
- **Component Testing:** Built-in support for Vue, React, Svelte, and Lit with environments like jsdom, happy-dom, and Playwright.
- **Built-in Coverage:** Supports v8 and istanbul coverage providers out of the box.
- **Vitest UI:** A rich graphical dashboard for visualizing tests and module dependencies.

## Installation

Add Vitest as a dev dependency:

```bash
npm install -D vitest
```

With yarn or pnpm:

```bash
yarn add -D vitest
pnpm add -D vitest
```

Then, add a test script to `package.json`:

```json
{
  "scripts": {
    "test": "vitest"
  }
}
```

> **Note:** Run `vitest run` for a single run (no watch mode). The default mode is watch, which re-runs tests on changes.

## Writing Tests

Vitest uses the same global API as Jest. Import `test`, `expect`, `describe`, etc. from `vitest` or enable `globals` in configuration.

### Basic Example

```javascript
// sum.test.js
import { expect, test } from 'vitest';
import { sum } from './sum';

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

### Using `describe` and `it`

```typescript
import { describe, it, expect } from 'vitest';

describe('Array', () => {
  it('should be empty initially', () => {
    const arr: number[] = [];
    expect(arr).toHaveLength(0);
  });
});
```

### Mocking with `vi`

```typescript
import { vi, test, expect } from 'vitest';

const mockFn = vi.fn();
mockFn('hello');
expect(mockFn).toHaveBeenCalledWith('hello');

// Mock a module
vi.mock('../api', () => ({
  fetchData: vi.fn(() => Promise.resolve({ data: 'mocked' })),
}));
```

## Configuration

Vitest can be configured in your project's `vite.config.ts` file (preferred) or in a separate `vitest.config.ts`. Configuration is placed under the `test` property.

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

If using a standalone `vitest.config.ts`, the format is identical but must export a Vite config (Vitest extends Vite).

## Key Features

### 1. Hot Module Replacement (HMR) for Tests

Vitest watches source and test files. When changes are made, only the affected tests re-run, providing near-instant feedback.

```bash
vitest
```

Press `r` to re-run all tests, `f` to rerun only failed tests, `q` to quit.

### 2. Native ESM Support

Since Vitest uses Vite's pipeline, ES Modules work naturally. No Babel plugins or special transforms required.

### 3. Jest API Compatibility

| Jest | Vitest |
|------|--------|
| `jest.fn()` | `vi.fn()` |
| `jest.mock()` | `vi.mock()` |
| `jest.spyOn()` | `vi.spyOn()` |
| `jest.useFakeTimers()` | `vi.useFakeTimers()` |

All lifecycle hooks (`beforeEach`, `afterEach`, `beforeAll`, `afterAll`) work identically.

### 4. First-Class TypeScript

No need for `ts-jest` or separate Babel config. Write TypeScript tests directly and Vitest handles transpilation via esbuild.

```typescript
interface User { name: string }
function greet(user: User) { return `Hello, ${user.name}`; }

it('greets user', () => {
  expect(greet({ name: 'Alice' })).toBe('Hello, Alice');
});
```

### 5. Component Testing

Vitest works seamlessly with component testing libraries like `@testing-library/vue`, `@testing-library/react`, and `@vue/test-utils`. Use the `environment` option to simulate a browser environment.

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

### 6. Code Coverage

Built-in coverage support via v8 (default) or istanbul.

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

An optional, rich web interface for exploring test results.

```bash
vitest --ui
```

The UI provides a dashboard with test status, timings, file tree, and a module dependency graph.

### 8. Workspace Mode (Monorepo Support)

Vitest can run tests across multiple projects or packages in a monorepo using a `vitest.workspace.ts` file. Configurations can be inlined or reference files/glob patterns.

```typescript
// vitest.workspace.ts
import { defineWorkspace } from 'vitest/config';

export default defineWorkspace([
  'packages/*',
  {
    // Inline config for a specific project
    test: {
      name: 'my-package',
      root: './packages/my-package',
      environment: 'node',
    },
  },
]);
```

Each project can have its own configuration, yet run from a single command.

### 9. Parallel Execution

Tests run in parallel via worker threads (default) or child processes (set `pool: 'forks'`).

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

## Command Examples

| Command | Description |
|---------|-------------|
| `vitest` | Run tests in watch mode (default) |
| `vitest run` | Run tests once (no watch) |
| `vitest run --reporter verbose` | Verbose output |
| `vitest --coverage` | Run tests with coverage report |
| `vitest --ui` | Launch Vitest UI |
| `vitest --config vitest.ci.ts` | Use a custom config file |
| `vitest --project projectName` | Run tests for a specific project in workspace |
| `vitest test/specific.test.ts` | Run a specific test file |
| `npx vitest --run --reporter json` | Output JSON results (CI-friendly) |

## Migration from Jest

Migrating from Jest to Vitest typically involves:

1. Replace `jest` with `vi` in test files (spy, mock, fn).
2. Update imports from `@jest/globals` to `vitest` (or use `globals: true`).
3. Move Jest configuration to `vite.config.ts` or `vitest.config.ts` under the `test` key.
4. Adapt module mocks: `vi.mock` instead of `jest.mock`.
5. Adjust timers: `vi.useFakeTimers()`.

A dedicated migration guide is available in the official Vitest documentation.

## Use Cases

- **Unit Testing:** Functions, utilities, and business logic.
- **Component Testing:** Vue, React, Svelte, Solid, and Lit components.
- **Integration Testing:** API endpoints, combined modules, with simulated environments.
- **Library / CLI Development:** Fast CI runs with excellent TypeScript support.
- **Monorepo Testing:** Workspace mode provides unified testing across packages.

## Why Vitest Over Jest?

- **ESM support:** No experimental modules or complex transforms needed.
- **Speed:** Faster cold starts due to Vite's optimized bundling and esbuild transpilation.
- **HMR:** Instant re-runs for an efficient TDD workflow.
- **Simpler configuration:** Reuses Vite config; no Jest-specific transformers.
- **Parallel execution:** Worker threads outperform Jest's default.
- **Modern stack alignment:** Designed for Vite-based projects (Vue, Svelte, React, etc.).

For large projects and monorepos, Vitest can cut test execution time by 2–10x compared to Jest.

## Additional Resources

- [Official Documentation](https://vitest.dev/)
- [GitHub Repository](https://github.com/vitest-dev/vitest)
- [Migration Guide from Jest](https://vitest.dev/guide/migration.html#migrating-from-jest)
- [Vitest UI Demo](https://vitest.dev/guide/ui.html)