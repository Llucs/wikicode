---
title: Vitest: Test-Framework der nächsten Generation, unterstützt von Vite
description: Ein schnelles, Vite-natives Test-Framework mit nahtloser Unterstützung für TypeScript und ESM, entwickelt für moderne JavaScript/TypeScript-Anwendungen.
created: 2026-06-23
tags:
  - testing
  - unit-testing
  - vite
  - typescript
  - jest-alternative
status: draft
---

# Vitest: Test-Framework der nächsten Generation, unterstützt von Vite

## Überblick

Vitest ist ein Unit-Testing-Framework der nächsten Generation, das auf Vite aufbaut. Erstellt von Anthony Fu und dem Vite-Kernteam, wurde es im Dezember 2021 veröffentlicht, um die Reibung zwischen Vites Entwicklungsserver und traditionellen Test-Runnern wie Jest zu adressieren. Durch die Nutzung von Vites Transformationspipeline, Hot Module Replacement (HMR) und Plugin-System liefert Vitest eine deutlich schnellere und konsistentere Entwicklererfahrung, insbesondere für Projekte, die bereits Vite verwenden.

### Warum Vitest?

- **Native ESM-Unterstützung:** Im Gegensatz zu Jest, das komplexe Transformationen für ES-Module erfordert, unterstützt Vitest ESM nativ, da es die auf Rollup basierende Pipeline von Vite nutzt.
- **HMR für Tests:** Nur betroffene Tests werden bei Codeänderungen erneut ausgeführt, was die Rückkopplungsschleife nahezu augenblicklich macht.
- **Jest-API-Kompatibilität:** Verwendet dieselbe `describe`-, `it`- und `expect`-API, wobei `vi` `jest` für Mocking und Spione ersetzt. Die Migration ist unkompliziert.
- **First-Class-TypeScript:** TypeScript wird ohne zusätzliche Konfiguration über esbuild sofort transpiliert.
- **Komponententests:** Eingebaute Unterstützung für Vue, React, Svelte und Lit mit Umgebungen wie jsdom, happy-dom und Playwright.
- **Eingebaute Codeabdeckung:** Unterstützt standardmäßig v8- und Istanbul-Abdeckungsanbieter.
- **Vitest UI:** Ein umfangreiches grafisches Dashboard zur Visualisierung von Tests und Modulabhängigkeiten.

## Installation

Vitest als Entwicklungsabhängigkeit hinzufügen:

```bash
npm install -D vitest
```

Mit yarn oder pnpm:

```bash
yarn add -D vitest
pnpm add -D vitest
```

Dann fügen Sie ein Test-Skript zur `package.json` hinzu:

```json
{
  "scripts": {
    "test": "vitest"
  }
}
```

> **Hinweis:** Führen Sie `vitest run` für einen einmaligen Durchlauf aus (ohne Watch-Modus). Der Standardmodus ist Watch, der Tests bei Änderungen erneut ausführt.

## Tests schreiben

Vitest verwendet dieselbe globale API wie Jest. Importieren Sie `test`, `expect`, `describe` usw. aus `vitest` oder aktivieren Sie `globals` in der Konfiguration.

### Einfaches Beispiel

```javascript
// sum.test.js
import { expect, test } from 'vitest';
import { sum } from './sum';

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

### Verwendung von `describe` und `it`

```typescript
import { describe, it, expect } from 'vitest';

describe('Array', () => {
  it('should be empty initially', () => {
    const arr: number[] = [];
    expect(arr).toHaveLength(0);
  });
});
```

### Mocking mit `vi`

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

## Konfiguration

Vitest kann in der `vite.config.ts`-Datei Ihres Projekts (bevorzugt) oder in einer separaten `vitest.config.ts` konfiguriert werden. Die Konfiguration erfolgt unter der Eigenschaft `test`.

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

Wenn Sie eine eigenständige `vitest.config.ts` verwenden, ist das Format identisch, muss aber eine Vite-Konfiguration exportieren (Vitest erweitert Vite).

## Hauptfunktionen

### 1. Hot Module Replacement (HMR) für Tests

Vitest überwacht Quell- und Testdateien. Wenn Änderungen vorgenommen werden, werden nur die betroffenen Tests erneut ausgeführt, was ein nahezu sofortiges Feedback bietet.

```bash
vitest
```

Drücken Sie `r`, um alle Tests erneut auszuführen, `f`, um nur fehlgeschlagene Tests erneut auszuführen, `q`, um zu beenden.

### 2. Native ESM-Unterstützung

Da Vitest die Pipeline von Vite verwendet, funktionieren ES-Module auf natürliche Weise. Es sind keine Babel-Plugins oder speziellen Transformationen erforderlich.

### 3. Jest-API-Kompatibilität

| Jest | Vitest |
|------|--------|
| `jest.fn()` | `vi.fn()` |
| `jest.mock()` | `vi.mock()` |
| `jest.spyOn()` | `vi.spyOn()` |
| `jest.useFakeTimers()` | `vi.useFakeTimers()` |

Alle Lebenszyklus-Hooks (`beforeEach`, `afterEach`, `beforeAll`, `afterAll`) funktionieren identisch.

### 4. First-Class-TypeScript

Kein Bedarf für `ts-jest` oder eine separate Babel-Konfiguration. Schreiben Sie TypeScript-Tests direkt und Vitest übernimmt die Transpilierung über esbuild.

```typescript
interface User { name: string }
function greet(user: User) { return `Hello, ${user.name}`; }

it('greets user', () => {
  expect(greet({ name: 'Alice' })).toBe('Hello, Alice');
});
```

### 5. Komponententests

Vitest arbeitet nahtlos mit Komponententestbibliotheken wie `@testing-library/vue`, `@testing-library/react` und `@vue/test-utils` zusammen. Verwenden Sie die Option `environment`, um eine Browserumgebung zu simulieren.

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

### 6. Codeabdeckung

Eingebaute Abdeckungsunterstützung über v8 (Standard) oder Istanbul.

```bash
vitest run --coverage
```

Oder über Konfiguration:

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

Eine optionale, umfangreiche Weboberfläche zur Erkundung von Testergebnissen.

```bash
vitest --ui
```

Die UI bietet ein Dashboard mit Teststatus, Zeiten, Dateibaum und einem Modulabhängigkeitsdiagramm.

### 8. Workspace-Modus (Monorepo-Unterstützung)

Vitest kann Tests über mehrere Projekte oder Pakete in einem Monorepo hinweg ausführen, indem eine `vitest.workspace.ts`-Datei verwendet wird. Konfigurationen können inline erfolgen oder Dateien/Glob-Muster referenzieren.

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

Jedes Projekt kann seine eigene Konfiguration haben, wird aber von einem einzigen Befehl aus ausgeführt.

### 9. Parallele Ausführung

Tests werden parallel über Worker-Threads (Standard) oder Kindprozesse ausgeführt (setzen Sie `pool: 'forks'`).

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

## Befehlsbeispiele

| Befehl | Beschreibung |
|---------|-------------|
| `vitest` | Tests im Watch-Modus ausführen (Standard) |
| `vitest run` | Tests einmalig ausführen (kein Watch) |
| `vitest run --reporter verbose` | Ausführliche Ausgabe |
| `vitest --coverage` | Tests mit Coverage-Bericht ausführen |
| `vitest --ui` | Vitest UI starten |
| `vitest --config vitest.ci.ts` | Eine benutzerdefinierte Konfigurationsdatei verwenden |
| `vitest --project projectName` | Tests für ein bestimmtes Projekt im Workspace ausführen |
| `vitest test/specific.test.ts` | Eine bestimmte Testdatei ausführen |
| `npx vitest --run --reporter json` | JSON-Ergebnisse ausgeben (CI-freundlich) |

## Migration von Jest

Die Migration von Jest zu Vitest umfasst typischerweise:

1. Ersetzen Sie `jest` durch `vi` in Testdateien (spy, mock, fn).
2. Aktualisieren Sie Importe von `@jest/globals` auf `vitest` (oder verwenden Sie `globals: true`).
3. Verschieben Sie die Jest-Konfiguration in `vite.config.ts` oder `vitest.config.ts` unter den Schlüssel `test`.
4. Passen Sie Modul-Mocks an: `vi.mock` statt `jest.mock`.
5. Passen Sie Timer an: `vi.useFakeTimers()`.

Eine spezielle Migrationsanleitung ist in der offiziellen Vitest-Dokumentation verfügbar.

## Anwendungsfälle

- **Unit-Testing:** Funktionen, Hilfsprogramme und Geschäftslogik.
- **Komponententests:** Vue-, React-, Svelte-, Solid- und Lit-Komponenten.
- **Integrationstests:** API-Endpunkte, kombinierte Module, mit simulierten Umgebungen.
- **Bibliotheks-/CLI-Entwicklung:** Schnelle CI-Läufe mit hervorragender TypeScript-Unterstützung.
- **Monorepo-Tests:** Der Workspace-Modus bietet einheitliche Tests über Pakete hinweg.

## Warum Vitest statt Jest?

- **ESM-Unterstützung:** Keine experimentellen Module oder komplexen Transformationen erforderlich.
- **Geschwindigkeit:** Schnellere Kaltstarts dank optimiertem Bundling von Vite und esbuild-Transpilierung.
- **HMR:** Sofortige Neuausführungen für einen effizienten TDD-Workflow.
- **Einfachere Konfiguration:** Verwendet die Vite-Konfiguration wieder; keine Jest-spezifischen Transformatoren.
- **Parallele Ausführung:** Worker-Threads übertreffen den Standard von Jest.
- **Ausrichtung auf moderne Stacks:** Entwickelt für Vite-basierte Projekte (Vue, Svelte, React, etc.).

Bei großen Projekten und Monorepos kann Vitest die Testausführungszeit im Vergleich zu Jest um das 2- bis 10-fache verkürzen.

## Zusätzliche Ressourcen

- [Offizielle Dokumentation](https://vitest.dev/)
- [GitHub-Repository](https://github.com/vitest-dev/vitest)
- [Migrationsanleitung von Jest](https://vitest.dev/guide/migration.html#migrating-from-jest)
- [Vitest UI Demo](https://vitest.dev/guide/ui.html)