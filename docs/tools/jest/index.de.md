---
title: Jest
description: Ein erfreuliches JavaScript-Testframework, das von Facebook entwickelt wurde und ein weit verbreitetes Werkzeug für Unit-Testing ist.
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

## Was ist Jest?

Jest ist ein JavaScript-Testframework ohne Konfiguration, das von Meta (ehemals Facebook) entwickelt wurde. Es ist darauf ausgelegt, einfach und schnell zu sein, und bietet alles, was Sie für Unit-Tests, Integrationstests und Snapshot-Tests benötigen, sofort einsatzbereit.

## Warum Jest?

- **Keine Konfiguration** – Für die meisten JavaScript-Projekte sind keine zusätzlichen Setup- oder Konfigurationsdateien erforderlich.
- **Schnelle parallele Ausführung** – Tests laufen in isolierten Workern, was die Ausführung beschleunigt.
- **Integrierte Mocking-Funktionen** – Einfaches Mocken von Funktionen und Modulen mit `jest.fn()` und `jest.mock()`.
- **Codeabdeckung** – Integrierte Coverage-Berichterstellung mit Istanbul.
- **Snapshot-Tests** – Erfassen gerenderter Ausgaben, um unbeabsichtigte Änderungen zu erkennen.
- **Umfangreiche Assertion-Bibliothek** – Eine breite Palette von Matchern für klare und ausdrucksstarke Assertions.
- **Funktioniert mit beliebten Bibliotheken** – Nahtlose Integration mit React, Vue, Angular, TypeScript und Node.

## Installation

```bash
npm install --save-dev jest
```

Fügen Sie ein Test-Skript zu Ihrer `package.json` hinzu:

```json
"scripts": {
  "test": "jest"
}
```

Für TypeScript-Unterstützung installieren Sie zusätzliche Pakete:

```bash
npm install --save-dev ts-jest @types/jest
```

und konfigurieren Sie Jest so, dass es `ts-jest` verwendet.

## Grundlegende Verwendung

Erstellen Sie eine einfache Funktion, die getestet werden soll:

```js
// sum.js
function sum(a, b) {
  return a + b;
}
module.exports = sum;
```

Schreiben Sie die dazugehörige Testdatei:

```js
// sum.test.js
const sum = require('./sum');

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

Führen Sie die Tests aus:

```bash
npm test
```

oder

```bash
npx jest
```

## Wichtige Funktionen

### Keine Konfiguration

Jest sucht automatisch nach Testdateien, die auf `*.test.js`, `*.spec.js` oder in `__tests__`-Verzeichnissen liegen. Es verwendet sinnvolle Standardeinstellungen, die für die meisten Projekte funktionieren.

### Mocking

**Function-Mocking:**

```js
const myMock = jest.fn();
myMock.mockReturnValue('hello');
console.log(myMock()); // 'hello'
```

**Modul-Mocking:**

```js
jest.mock('./api');
const api = require('./api');
// Das Modul wird automatisch durch einen Mock ersetzt, der undefined zurückgibt
```

### Snapshot-Tests

Nützlich für UI-Komponenten. Erfasst die gerenderte Ausgabe und vergleicht sie mit gespeicherten Snapshots.

```js
import renderer from 'react-test-renderer';
import MyComponent from './MyComponent';

test('renders correctly', () => {
  const tree = renderer.create(<MyComponent />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

Führen Sie mit `--updateSnapshot` (oder `-u`) aus, um fehlschlagende Snapshots zu aktualisieren.

### Codeabdeckung

Generieren Sie einen Coverage-Bericht, indem Sie das Flag `--coverage` hinzufügen:

```bash
jest --coverage
```

Dies erzeugt ein detailliertes `coverage/`-Verzeichnis mit einem HTML-Bericht.

### Watch-Modus

Führen Sie Tests automatisch neu aus, wenn sich Dateien ändern.

```bash
jest --watchAll   # für alle Testdateien
jest --watch      # nur Tests, die sich auf geänderte Dateien beziehen (erfordert Git)
```

### Umfangreiche Assertions (Matcher)

Häufige Matcher sind:

- `toBe` – strikte Gleichheit (`===`)
- `toEqual` – tiefe Gleichheit
- `toContain` – prüft Array/Iterable auf ein Element
- `toThrow` – prüft, ob eine Funktion einen Fehler wirft
- `toBeTruthy` / `toBeFalsy`
- `toBeNull`, `toBeDefined`, `toBeUndefined`
- `.resolves` und `.rejects` – für Promises

**Beispiele:**

```js
expect(2 + 2).toBe(4);
expect({ a: 1 }).toEqual({ a: 1 });
expect([1, 2, 3]).toContain(2);
expect(() => { throw Error('fail'); }).toThrow('fail');
```

### Asynchrone Tests

Testen Sie asynchronen Code mit `async/await`:

```js
test('async data', async () => {
  const data = await fetchData();
  expect(data).toBe('peanut butter');
});
```

Oder mit den `.resolves` / `.rejects`-Matchern:

```js
test('async resolves', () => {
  return expect(fetchData()).resolves.toBe('peanut butter');
});
```

### Setup und Teardown

Verwenden Sie Lifecycle-Hooks, um Code vor/nach Tests auszuführen:

```js
beforeAll(() => {
  // wird einmal vor allen Tests ausgeführt
});

afterAll(() => {
  // wird einmal nach allen Tests ausgeführt
});

beforeEach(() => {
  // wird vor jedem Test ausgeführt
});

afterEach(() => {
  // wird nach jedem Test ausgeführt
});
```

## CLI-Optionen

| Option                | Beschreibung                                              |
|-----------------------|----------------------------------------------------------|
| `--coverage`          | Generieren und Ausgeben des Coverage-Berichts.            |
| `--watch`             | Überwacht Dateien auf Änderungen und führt zugehörige Tests erneut aus. |
| `--watchAll`          | Überwacht alle Dateien und führt bei Änderungen alle Tests erneut aus. |
| `--verbose`           | Zeigt einzelne Testergebnisse detailliert an.             |
| `--updateSnapshot` (oder `-u`) | Aktualisiert alle Snapshot-Dateien.                |
| `--testNamePattern`   | Führt Tests mit Namen aus, die einem Regex-Muster entsprechen. |
| `--runInBand`         | Führt Tests nacheinander aus (nützlich zum Debuggen).     |
| `--silent`            | Unterdrückt Konsolenausgaben von Tests.                   |
| `--clearCache`        | Leert den Jest-Cache.                                     |

## Konfiguration

Jest kann über eine `jest.config.js`-Datei oder den `jest`-Schlüssel in der `package.json` konfiguriert werden.

**Beispiel `jest.config.js`:**

```js
module.exports = {
  testEnvironment: 'node',   // 'jsdom' für eine browserähnliche Umgebung
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

Alternativ kann die Konfiguration in `package.json` ergänzt werden:

```json
"jest": {
  "testEnvironment": "node",
  "roots": ["src"]
}
```

## Fortgeschritten: Testen mit React/DOM

Verwendung von `@testing-library/react`:

```js
import { render, screen } from '@testing-library/react';
import MyComponent from './MyComponent';

test('renders the component', () => {
  render(<MyComponent />);
  expect(screen.getByText('Hello')).toBeInTheDocument();
});
```

## Fazit

Jest ist der De-facto-Standard zum Testen von JavaScript-Anwendungen. Die Einrichtung ohne Konfiguration, robuste Mocking-Funktionen, Snapshot-Fähigkeiten und die schnelle parallele Ausführung machen es zu einem unverzichtbaren Werkzeug für jeden JavaScript-Entwickler. Ob Sie einfache Funktionen oder komplexe React-Komponenten testen, Jest bietet eine erfreuliche und leistungsstarke Testumgebung.

---

*Dieses Dokument ist ein Entwurf und wird aktualisiert, sobald sich Jest weiterentwickelt.*