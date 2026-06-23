---
title: Vitest: Marco de pruebas de próxima generación impulsado por Vite
description: Un marco de pruebas rápido y nativo de Vite con soporte perfecto para TypeScript y ESM, diseñado para aplicaciones modernas de JavaScript/TypeScript.
created: 2026-06-23
tags:
  - testing
  - unit-testing
  - vite
  - typescript
  - jest-alternative
status: draft
---

# Vitest: Marco de pruebas de próxima generación impulsado por Vite

## Descripción general

Vitest es un marco de pruebas unitarias de próxima generación construido sobre Vite. Creado por Anthony Fu y el equipo central de Vite, fue lanzado en diciembre de 2021 para resolver la fricción entre el servidor de desarrollo de Vite y los ejecutores de pruebas tradicionales como Jest. Al aprovechar el pipeline de transformación de Vite, la sustitución de módulos en caliente (HMR) y el sistema de plugins, Vitest ofrece una experiencia de desarrollo significativamente más rápida y consistente, especialmente para proyectos que ya usan Vite.

### ¿Por qué Vitest?

- **Soporte nativo para ESM:** A diferencia de Jest, que requiere transformaciones complejas para los módulos ES, Vitest maneja ESM de forma nativa porque utiliza el pipeline basado en Rollup de Vite.
- **HMR para pruebas:** Solo las pruebas afectadas se vuelven a ejecutar cuando el código cambia, lo que hace que el ciclo de retroalimentación sea casi instantáneo.
- **Compatibilidad con la API de Jest:** Utiliza la misma API `describe`, `it`, `expect`, con `vi` reemplazando a `jest` para mocks y spies. La migración es sencilla.
- **TypeScript de primera clase:** TypeScript se transpila al instante mediante esbuild sin configuración adicional.
- **Pruebas de componentes:** Soporte integrado para Vue, React, Svelte y Lit con entornos como jsdom, happy-dom y Playwright.
- **Cobertura integrada:** Soporta los proveedores de cobertura v8 e istanbul de forma predeterminada.
- **Vitest UI:** Un dashboard gráfico enriquecido para visualizar pruebas y dependencias de módulos.

## Instalación

Agregue Vitest como dependencia de desarrollo:

```bash
npm install -D vitest
```

Con yarn o pnpm:

```bash
yarn add -D vitest
pnpm add -D vitest
```

Luego, agregue un script de prueba en `package.json`:

```json
{
  "scripts": {
    "test": "vitest"
  }
}
```

> **Nota:** Ejecute `vitest run` para una ejecución única (sin modo watch). El modo predeterminado es watch, que vuelve a ejecutar las pruebas cuando hay cambios.

## Escribir pruebas

Vitest utiliza la misma API global que Jest. Importe `test`, `expect`, `describe`, etc. desde `vitest` o habilite `globals` en la configuración.

### Ejemplo básico

```javascript
// sum.test.js
import { expect, test } from 'vitest';
import { sum } from './sum';

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

### Usando `describe` e `it`

```typescript
import { describe, it, expect } from 'vitest';

describe('Array', () => {
  it('should be empty initially', () => {
    const arr: number[] = [];
    expect(arr).toHaveLength(0);
  });
});
```

### Mocks con `vi`

```typescript
import { vi, test, expect } from 'vitest';

const mockFn = vi.fn();
mockFn('hello');
expect(mockFn).toHaveBeenCalledWith('hello');

// Mock de un módulo
vi.mock('../api', () => ({
  fetchData: vi.fn(() => Promise.resolve({ data: 'mocked' })),
}));
```

## Configuración

Vitest se puede configurar en el archivo `vite.config.ts` de su proyecto (preferido) o en un archivo separado `vitest.config.ts`. La configuración se coloca bajo la propiedad `test`.

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

Si se usa un archivo `vitest.config.ts` independiente, el formato es idéntico pero debe exportar una configuración de Vite (Vitest extiende Vite).

## Características clave

### 1. Sustitución de módulos en caliente (HMR) para pruebas

Vitest observa los archivos fuente y de prueba. Cuando se realizan cambios, solo las pruebas afectadas se vuelven a ejecutar, proporcionando una retroalimentación casi instantánea.

```bash
vitest
```

Presione `r` para volver a ejecutar todas las pruebas, `f` para volver a ejecutar solo las pruebas fallidas, `q` para salir.

### 2. Soporte nativo para ESM

Dado que Vitest utiliza el pipeline de Vite, los módulos ES funcionan de forma natural. No se requieren plugins de Babel ni transformaciones especiales.

### 3. Compatibilidad con la API de Jest

| Jest | Vitest |
|------|--------|
| `jest.fn()` | `vi.fn()` |
| `jest.mock()` | `vi.mock()` |
| `jest.spyOn()` | `vi.spyOn()` |
| `jest.useFakeTimers()` | `vi.useFakeTimers()` |

Todos los hooks del ciclo de vida (`beforeEach`, `afterEach`, `beforeAll`, `afterAll`) funcionan de manera idéntica.

### 4. TypeScript de primera clase

No es necesario `ts-jest` ni una configuración separada de Babel. Escriba pruebas en TypeScript directamente y Vitest maneja la transpilación mediante esbuild.

```typescript
interface User { name: string }
function greet(user: User) { return `Hello, ${user.name}`; }

it('greets user', () => {
  expect(greet({ name: 'Alice' })).toBe('Hello, Alice');
});
```

### 5. Pruebas de componentes

Vitest funciona perfectamente con bibliotecas de pruebas de componentes como `@testing-library/vue`, `@testing-library/react` y `@vue/test-utils`. Use la opción `environment` para simular un entorno de navegador.

```typescript
// Ejemplo con @vue/test-utils
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

### 6. Cobertura de código

Soporte de cobertura integrado a través de v8 (predeterminado) o istanbul.

```bash
vitest run --coverage
```

O a través de la configuración:

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

Una interfaz web opcional y enriquecida para explorar los resultados de las pruebas.

```bash
vitest --ui
```

La UI proporciona un dashboard con el estado de las pruebas, tiempos, árbol de archivos y un gráfico de dependencias de módulos.

### 8. Modo Workspace (soporte para monorepos)

Vitest puede ejecutar pruebas en múltiples proyectos o paquetes en un monorepo usando un archivo `vitest.workspace.ts`. Las configuraciones se pueden incluir en línea o hacer referencia a archivos/patrones glob.

```typescript
// vitest.workspace.ts
import { defineWorkspace } from 'vitest/config';

export default defineWorkspace([
  'packages/*',
  {
    // Configuración en línea para un proyecto específico
    test: {
      name: 'my-package',
      root: './packages/my-package',
      environment: 'node',
    },
  },
]);
```

Cada proyecto puede tener su propia configuración, pero ejecutarse desde un solo comando.

### 9. Ejecución en paralelo

Las pruebas se ejecutan en paralelo a través de hilos de trabajo (worker threads, predeterminado) o procesos hijos (estableciendo `pool: 'forks'`).

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

## Ejemplos de comandos

| Comando | Descripción |
|---------|-------------|
| `vitest` | Ejecuta pruebas en modo watch (predeterminado) |
| `vitest run` | Ejecuta pruebas una vez (sin watch) |
| `vitest run --reporter verbose` | Salida detallada |
| `vitest --coverage` | Ejecuta pruebas con informe de cobertura |
| `vitest --ui` | Inicia la IU de Vitest |
| `vitest --config vitest.ci.ts` | Usa un archivo de configuración personalizado |
| `vitest --project projectName` | Ejecuta pruebas para un proyecto específico en el workspace |
| `vitest test/specific.test.ts` | Ejecuta un archivo de prueba específico |
| `npx vitest --run --reporter json` | Salida en JSON (amigable para CI) |

## Migración desde Jest

La migración de Jest a Vitest generalmente implica:

1. Reemplazar `jest` por `vi` en los archivos de prueba (spy, mock, fn).
2. Actualizar las importaciones de `@jest/globals` a `vitest` (o usar `globals: true`).
3. Mover la configuración de Jest a `vite.config.ts` o `vitest.config.ts` bajo la clave `test`.
4. Adaptar los mocks de módulos: `vi.mock` en lugar de `jest.mock`.
5. Ajustar los temporizadores: `vi.useFakeTimers()`.

Hay una guía de migración dedicada disponible en la documentación oficial de Vitest.

## Casos de uso

- **Pruebas unitarias:** Funciones, utilidades y lógica de negocio.
- **Pruebas de componentes:** Componentes Vue, React, Svelte, Solid y Lit.
- **Pruebas de integración:** Endpoints de API, módulos combinados, con entornos simulados.
- **Desarrollo de librerías/CLI:** Ejecuciones rápidas en CI con excelente soporte para TypeScript.
- **Pruebas en monorepo:** El modo workspace proporciona pruebas unificadas entre paquetes.

## ¿Por qué Vitest en lugar de Jest?

- **Soporte para ESM:** No se necesitan módulos experimentales ni transformaciones complejas.
- **Velocidad:** Arranques en frío más rápidos gracias al empaquetado optimizado de Vite y la transpilación con esbuild.
- **HMR:** Reejecuciones instantáneas para un flujo de trabajo TDD eficiente.
- **Configuración más simple:** Reutiliza la configuración de Vite; sin transformadores específicos de Jest.
- **Ejecución en paralelo:** Los hilos de trabajo (worker threads) superan al predeterminado de Jest.
- **Alineación con el stack moderno:** Diseñado para proyectos basados en Vite (Vue, Svelte, React, etc.).

Para proyectos grandes y monorepos, Vitest puede reducir el tiempo de ejecución de las pruebas de 2 a 10 veces en comparación con Jest.

## Recursos adicionales

- [Documentación oficial](https://vitest.dev/)
- [Repositorio de GitHub](https://github.com/vitest-dev/vitest)
- [Guía de migración desde Jest](https://vitest.dev/guide/migration.html#migrating-from-jest)
- [Demo de Vitest UI](https://vitest.dev/guide/ui.html)