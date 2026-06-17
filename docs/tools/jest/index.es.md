---
title: Jest
description: Un encantador framework de pruebas para JavaScript desarrollado por Facebook que es una herramienta ampliamente utilizada para pruebas unitarias.
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

## ¿Qué es Jest?

Jest es un framework de pruebas para JavaScript de configuración cero desarrollado por Meta (anteriormente Facebook). Está diseñado para ser simple y rápido, proporcionando todo lo que necesitas listo para usar para pruebas unitarias, de integración y de instantáneas.

## ¿Por qué Jest?

- **Cero configuración** – No es necesario configuración adicional ni archivos de configuración para la mayoría de proyectos JavaScript.
- **Ejecución paralela rápida** – Las pruebas se ejecutan en workers aislados, lo que acelera la ejecución.
- **Simulación integrada** – Simula fácilmente funciones y módulos usando `jest.fn()` y `jest.mock()`.
- **Cobertura de código** – Informe de cobertura integrado mediante Istanbul.
- **Pruebas de instantáneas** – Captura la salida renderizada para detectar cambios no deseados.
- **Biblioteca de aserciones completa** – Un amplio conjunto de comparadores para aserciones claras y expresivas.
- **Funciona con bibliotecas populares** – Integración perfecta con React, Vue, Angular, TypeScript y Node.

## Instalación

```bash
npm install --save-dev jest
```

Añade un script de prueba a tu `package.json`:

```json
"scripts": {
  "test": "jest"
}
```

Para soporte de TypeScript, instala paquetes adicionales:

```bash
npm install --save-dev ts-jest @types/jest
```

y configura Jest para usar `ts-jest`.

## Uso básico

Crea una función simple para probar:

```js
// sum.js
function sum(a, b) {
  return a + b;
}
module.exports = sum;
```

Escribe el archivo de prueba correspondiente:

```js
// sum.test.js
const sum = require('./sum');

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

Ejecuta las pruebas:

```bash
npm test
```

o

```bash
npx jest
```

## Características principales

### Configuración cero

Jest busca automáticamente archivos de prueba que coincidan con `*.test.js`, `*.spec.js` o archivos dentro de directorios `__tests__`. Utiliza valores predeterminados sensatos que funcionan para la mayoría de proyectos.

### Simulación (Mocking)

**Simulación de funciones:**

```js
const myMock = jest.fn();
myMock.mockReturnValue('hello');
console.log(myMock()); // 'hello'
```

**Simulación de módulos:**

```js
jest.mock('./api');
const api = require('./api');
// The module is automatically replaced with a mock that returns undefined
```

### Pruebas de instantáneas

Útil para componentes de UI. Captura la salida renderizada y compárala con instantáneas almacenadas.

```js
import renderer from 'react-test-renderer';
import MyComponent from './MyComponent';

test('renders correctly', () => {
  const tree = renderer.create(<MyComponent />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

Ejecuta con `--updateSnapshot` (o `-u`) para actualizar las instantáneas que fallan.

### Cobertura de código

Genera un informe de cobertura añadiendo la bandera `--coverage`:

```bash
jest --coverage
```

Esto produce un directorio `coverage/` detallado con un informe HTML.

### Modo de observación (Watch)

Vuelve a ejecutar las pruebas automáticamente cuando los archivos cambien.

```bash
jest --watchAll   # for all test files
jest --watch      # only tests related to changed files (requires Git)
```

### Aserciones completas (Matchers)

Los comparadores comunes incluyen:

- `toBe` – igualdad estricta (`===`)
- `toEqual` – igualdad profunda
- `toContain` – verificar si un array/iterable contiene un elemento
- `toThrow` – verificar que una función lanza una excepción
- `toBeTruthy` / `toBeFalsy`
- `toBeNull`, `toBeDefined`, `toBeUndefined`
- `.resolves` y `.rejects` – para promesas

**Ejemplos:**

```js
expect(2 + 2).toBe(4);
expect({ a: 1 }).toEqual({ a: 1 });
expect([1, 2, 3]).toContain(2);
expect(() => { throw Error('fail'); }).toThrow('fail');
```

### Pruebas asíncronas

Prueba código asíncrono con `async/await`:

```js
test('async data', async () => {
  const data = await fetchData();
  expect(data).toBe('peanut butter');
});
```

O usando los comparadores `.resolves` / `.rejects`:

```js
test('async resolves', () => {
  return expect(fetchData()).resolves.toBe('peanut butter');
});
```

### Configuración y limpieza

Utiliza hooks del ciclo de vida para ejecutar código antes/después de las pruebas:

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

## Opciones de CLI

| Opción                | Descripción                                              |
|-----------------------|----------------------------------------------------------|
| `--coverage`          | Genera y muestra el informe de cobertura.                |
| `--watch`             | Observa los archivos para cambios y vuelve a ejecutar pruebas relacionadas. |
| `--watchAll`          | Observa todos los archivos y vuelve a ejecutar todas las pruebas al cambiar. |
| `--verbose`           | Muestra los resultados individuales de las pruebas en detalle. |
| `--updateSnapshot` (o `-u`) | Actualiza todos los archivos de instantáneas.         |
| `--testNamePattern`   | Ejecuta pruebas con nombres que coincidan con un patrón regex. |
| `--runInBand`         | Ejecuta las pruebas en serie (útil para depuración).      |
| `--silent`            | Suprime la salida de consola de las pruebas.             |
| `--clearCache`        | Limpia la caché de Jest.                                 |

## Configuración

Jest se puede configurar mediante un archivo `jest.config.js` o la clave `jest` en `package.json`.

**Ejemplo de `jest.config.js`:**

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

Alternativamente, añade la configuración a `package.json`:

```json
"jest": {
  "testEnvironment": "node",
  "roots": ["src"]
}
```

## Avanzado: Pruebas con React/DOM

Usando `@testing-library/react`:

```js
import { render, screen } from '@testing-library/react';
import MyComponent from './MyComponent';

test('renders the component', () => {
  render(<MyComponent />);
  expect(screen.getByText('Hello')).toBeInTheDocument();
});
```

## Conclusión

Jest es el estándar de facto para probar aplicaciones JavaScript. Su configuración cero, robusta simulación, capacidades de instantáneas y rápida ejecución paralela lo convierten en una herramienta esencial para cualquier desarrollador de JavaScript. Ya sea que estés probando funciones simples o componentes complejos de React, Jest proporciona una experiencia de prueba encantadora y potente.

---

*Este documento es un borrador y se actualizará a medida que Jest evolucione.*