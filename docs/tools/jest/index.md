---
title: Jest
description: A delightful JavaScript testing framework developed by Facebook that is a widely used tool for unit testing.
created: 2026-06-15
tags:
  - javascript
  - testing
  - jest
  - unit-testing
  - meta
status: draft
---

# Jest

## What is Jest?

Jest is a zero-configuration JavaScript testing framework developed by Meta (formerly Facebook). It is designed to be simple and fast, providing everything you need out of the box for unit testing, integration testing, and snapshot testing.

## Why Jest?

- **Zero configuration** – No need for additional setup or config files for most JavaScript projects.
- **Fast parallel execution** – Tests run in isolated workers, making execution fast.
- **Built-in mocking** – Easily mock functions and modules using `jest.fn()` and `jest.mock()`.
- **Code coverage** – Built-in coverage reporting using Istanbul.
- **Snapshot testing** – Capture rendered output to detect unintended changes.
- **Rich assertion library** – A wide set of matchers for clear and expressive assertions.
- **Works with popular libraries** – Seamless integration with React, Vue, Angular, TypeScript, and Node.

## Installation

```bash
npm install --save-dev jest
```

Add a test script to your `package.json`:

```json
"scripts": {
  "test": "jest"
}
```

For TypeScript support, install additional packages:

```bash
npm install --save-dev ts-jest @types/jest
```

and configure Jest to use `ts-jest`.

## Basic Usage

Create a simple function to test:

```js
// sum.js
function sum(a, b) {
  return a + b;
}
module.exports = sum;
```

Write the corresponding test file:

```js
// sum.test.js
const sum = require('./sum');

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

Run the tests:

```bash
npm test
```

or

```bash
npx jest
```

## Key Features

### Zero Configuration

Jest automatically looks for test files matching `*.test.js`, `*.spec.js`, or files inside `__tests__` directories. It uses sensible defaults that work for most projects.

### Mocking

**Function mocking:**

```js
const myMock = jest.fn();
myMock.mockReturnValue('hello');
console.log(myMock()); // 'hello'
```

**Module mocking:**

```js
jest.mock('./api');
const api = require('./api');
// The module is automatically replaced with a mock that returns undefined
```

### Snapshot Testing

Useful for UI components. Capture the rendered output and compare with stored snapshots.

```js
import renderer from 'react-test-renderer';
import MyComponent from './MyComponent';

test('renders correctly', () => {
  const tree = renderer.create(<MyComponent />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

Run with `--updateSnapshot` (or `-u`) to update failing snapshots.

### Code Coverage

Generate a coverage report by adding the `--coverage` flag:

```bash
jest --coverage
```

This produces a detailed `coverage/` directory with an HTML report.

### Watch Mode

Re-run tests automatically when files change.

```bash
jest --watchAll   # for all test files
jest --watch      # only tests related to changed files (requires Git)
```

### Rich Assertions (Matchers)

Common matchers include:

- `toBe` – strict equality (`===`)
- `toEqual` – deep equality
- `toContain` – check array/iterable for an item
- `toThrow` – check that a function throws
- `toBeTruthy` / `toBeFalsy`
- `toBeNull`, `toBeDefined`, `toBeUndefined`
- `.resolves` and `.rejects` – for promises

**Examples:**

```js
expect(2 + 2).toBe(4);
expect({ a: 1 }).toEqual({ a: 1 });
expect([1, 2, 3]).toContain(2);
expect(() => { throw Error('fail'); }).toThrow('fail');
```

### Async Testing

Test asynchronous code with `async/await`:

```js
test('async data', async () => {
  const data = await fetchData();
  expect(data).toBe('peanut butter');
});
```

Or using the `.resolves` / `.rejects` matchers:

```js
test('async resolves', () => {
  return expect(fetchData()).resolves.toBe('peanut butter');
});
```

### Setup and Teardown

Use lifecycle hooks to run code before/after tests:

```js
beforeAll(() => {
  // runs once before all tests
});

afterAll(() => {
  // runs once after all tests
});

beforeEach(() => {
  // runs before each test
});

afterEach(() => {
  // runs after each test
});
```

## CLI Options

| Option                | Description                                              |
|-----------------------|----------------------------------------------------------|
| `--coverage`          | Generate and output coverage report.                     |
| `--watch`             | Watch files for changes and re-run related tests.        |
| `--watchAll`          | Watch all files and re-run all tests on changes.         |
| `--verbose`           | Display individual test results in detail.               |
| `--updateSnapshot` (or `-u`) | Update all snapshot files.                         |
| `--testNamePattern`   | Run tests with names matching a regex pattern.           |
| `--runInBand`         | Run tests serially (useful for debugging).               |
| `--silent`            | Suppress console output from tests.                      |
| `--clearCache`        | Clear the Jest cache.                                    |

## Configuration

Jest can be configured via a `jest.config.js` file or the `jest` key in `package.json`.

**Example `jest.config.js`:**

```js
module.exports = {
  testEnvironment: 'node',   // 'jsdom' for browser-like environment
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

Alternatively, add the configuration to `package.json`:

```json
"jest": {
  "testEnvironment": "node",
  "roots": ["src"]
}
```

## Advanced: Testing with React/DOM

Using `@testing-library/react`:

```js
import { render, screen } from '@testing-library/react';
import MyComponent from './MyComponent';

test('renders the component', () => {
  render(<MyComponent />);
  expect(screen.getByText('Hello')).toBeInTheDocument();
});
```

## Conclusion

Jest is the de facto standard for testing JavaScript applications. Its zero‑config setup, robust mocking, snapshot capabilities, and fast parallel execution make it an essential tool for any JavaScript developer. Whether you are testing simple functions or complex React components, Jest provides a delightful and powerful testing experience.

---

*This document is a draft and will be updated as Jest evolves.*