---
title: Jest
description: Um agradável JavaScript testing framework desenvolvido pelo Facebook que é uma ferramenta amplamente utilizada para unit testing.
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

## O que é Jest?

Jest é um zero-configuration JavaScript testing framework desenvolvido pela Meta (anteriormente Facebook). Ele é projetado para ser simples e rápido, fornecendo tudo que você precisa prontamente para unit testing, integration testing e snapshot testing.

## Por que Jest?

- **Zero configuration** – Sem necessidade de configuração adicional ou arquivos de config para a maioria dos projetos JavaScript.
- **Fast parallel execution** – Os testes são executados em workers isolados, tornando a execução rápida.
- **Built-in mocking** – Mock funções e módulos facilmente usando `jest.fn()` e `jest.mock()`.
- **Code coverage** – Relatório de coverage integrado usando Istanbul.
- **Snapshot testing** – Capture a saída renderizada para detectar mudanças não intencionais.
- **Rich assertion library** – Um amplo conjunto de matchers para asserções claras e expressivas.
- **Works with popular libraries** – Integração perfeita com React, Vue, Angular, TypeScript e Node.

## Instalação

```bash
npm install --save-dev jest
```

Adicione um script de teste ao seu `package.json`:

```json
"scripts": {
  "test": "jest"
}
```

Para suporte a TypeScript, instale pacotes adicionais:

```bash
npm install --save-dev ts-jest @types/jest
```

e configure o Jest para usar `ts-jest`.

## Uso Básico

Crie uma função simples para testar:

```js
// sum.js
function sum(a, b) {
  return a + b;
}
module.exports = sum;
```

Escreva o arquivo de teste correspondente:

```js
// sum.test.js
const sum = require('./sum');

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

Execute os testes:

```bash
npm test
```

ou

```bash
npx jest
```

## Principais Recursos

### Zero Configuration

Jest automaticamente procura por arquivos de teste que correspondem a `*.test.js`, `*.spec.js`, ou arquivos dentro de diretórios `__tests__`. Ele usa padrões sensatos que funcionam para a maioria dos projetos.

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

Útil para componentes de UI. Capture a saída renderizada e compare com snapshots armazenados.

```js
import renderer from 'react-test-renderer';
import MyComponent from './MyComponent';

test('renders correctly', () => {
  const tree = renderer.create(<MyComponent />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

Execute com `--updateSnapshot` (ou `-u`) para atualizar snapshots com falha.

### Code Coverage

Gere um relatório de coverage adicionando a flag `--coverage`:

```bash
jest --coverage
```

Isso produz um diretório `coverage/` detalhado com um relatório HTML.

### Watch Mode

Re-executa os testes automaticamente quando arquivos mudam.

```bash
jest --watchAll   # para todos os arquivos de teste
jest --watch      # apenas testes relacionados a arquivos alterados (requer Git)
```

### Rich Assertions (Matchers)

Matchers comuns incluem:

- `toBe` – igualdade estrita (`===`)
- `toEqual` – igualdade profunda
- `toContain` – verifica se um array/iterável contém um item
- `toThrow` – verifica se uma função lança exceção
- `toBeTruthy` / `toBeFalsy`
- `toBeNull`, `toBeDefined`, `toBeUndefined`
- `.resolves` e `.rejects` – para promises

**Exemplos:**

```js
expect(2 + 2).toBe(4);
expect({ a: 1 }).toEqual({ a: 1 });
expect([1, 2, 3]).toContain(2);
expect(() => { throw Error('fail'); }).toThrow('fail');
```

### Async Testing

Teste código assíncrono com `async/await`:

```js
test('async data', async () => {
  const data = await fetchData();
  expect(data).toBe('peanut butter');
});
```

Ou usando os matchers `.resolves` / `.rejects`:

```js
test('async resolves', () => {
  return expect(fetchData()).resolves.toBe('peanut butter');
});
```

### Setup and Teardown

Use lifecycle hooks para executar código antes/depois dos testes:

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

## Opções de CLI

| Option                | Description                                              |
|-----------------------|----------------------------------------------------------|
| `--coverage`          | Gera e exibe relatório de coverage.                     |
| `--watch`             | Observa arquivos quanto a alterações e reexecuta testes relacionados. |
| `--watchAll`          | Observa todos os arquivos e reexecuta todos os testes em alterações. |
| `--verbose`           | Exibe resultados individuais dos testes em detalhes.     |
| `--updateSnapshot` (or `-u`) | Atualiza todos os arquivos de snapshot.                         |
| `--testNamePattern`   | Executa testes com nomes que correspondem a um padrão regex.           |
| `--runInBand`         | Executa testes serialmente (útil para depuração).               |
| `--silent`            | Suprime a saída do console dos testes.                      |
| `--clearCache`        | Limpa o cache do Jest.                                    |

## Configuração

Jest pode ser configurado através de um arquivo `jest.config.js` ou da chave `jest` no `package.json`.

**Exemplo `jest.config.js`:**

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

Alternativamente, adicione a configuração ao `package.json`:

```json
"jest": {
  "testEnvironment": "node",
  "roots": ["src"]
}
```

## Avançado: Testando com React/DOM

Usando `@testing-library/react`:

```js
import { render, screen } from '@testing-library/react';
import MyComponent from './MyComponent';

test('renders the component', () => {
  render(<MyComponent />);
  expect(screen.getByText('Hello')).toBeInTheDocument();
});
```

## Conclusão

Jest é o padrão de facto para testar aplicações JavaScript. Sua configuração zero‑config, mocking robusto, capacidades de snapshot e execução paralela rápida fazem dele uma ferramenta essencial para qualquer desenvolvedor JavaScript. Quer você esteja testando funções simples ou componentes React complexos, Jest oferece uma experiência de teste agradável e poderosa.

---

*Este documento é um rascunho e será atualizado conforme a evolução do Jest.*