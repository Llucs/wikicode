---
title: Jest
description: Un framework de test JavaScript agréable développé par Facebook qui est un outil largement utilisé pour les tests unitaires.
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

## Qu'est-ce que Jest ?

Jest est un framework de test JavaScript sans configuration développé par Meta (anciennement Facebook). Il est conçu pour être simple et rapide, offrant tout ce dont vous avez besoin prêt à l'emploi pour les tests unitaires, les tests d'intégration et les tests de snapshot.

## Pourquoi Jest ?

- **Zéro configuration** – Aucun besoin de configuration supplémentaire ou de fichiers de configuration pour la plupart des projets JavaScript.
- **Exécution parallèle rapide** – Les tests s'exécutent dans des workers isolés, ce qui rend l'exécution rapide.
- **Mocking intégré** – Moquez facilement des fonctions et des modules grâce à `jest.fn()` et `jest.mock()`.
- **Couverture de code** – Rapport de couverture intégré utilisant Istanbul.
- **Tests de snapshot** – Capturez la sortie rendue pour détecter les modifications non intentionnelles.
- **Bibliothèque d'assertions riche** – Un large ensemble de matchers pour des assertions claires et expressives.
- **Fonctionne avec les bibliothèques populaires** – Intégration transparente avec React, Vue, Angular, TypeScript et Node.

## Installation

```bash
npm install --save-dev jest
```

Ajoutez un script de test à votre `package.json` :

```json
"scripts": {
  "test": "jest"
}
```

Pour le support TypeScript, installez des packages supplémentaires :

```bash
npm install --save-dev ts-jest @types/jest
```

et configurez Jest pour utiliser `ts-jest`.

## Utilisation de base

Créez une fonction simple à tester :

```js
// sum.js
function sum(a, b) {
  return a + b;
}
module.exports = sum;
```

Écrivez le fichier de test correspondant :

```js
// sum.test.js
const sum = require('./sum');

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

Exécutez les tests :

```bash
npm test
```

ou

```bash
npx jest
```

## Fonctionnalités clés

### Zéro configuration

Jest recherche automatiquement les fichiers de test correspondant à `*.test.js`, `*.spec.js`, ou les fichiers dans les répertoires `__tests__`. Il utilise des valeurs par défaut sensées qui fonctionnent pour la plupart des projets.

### Mocking

**Fonction mocking :**

```js
const myMock = jest.fn();
myMock.mockReturnValue('hello');
console.log(myMock()); // 'hello'
```

**Module mocking :**

```js
jest.mock('./api');
const api = require('./api');
// Le module est automatiquement remplacé par un mock qui retourne undefined
```

### Snapshot Testing

Utile pour les composants UI. Capturez la sortie rendue et comparez-la avec des snapshots stockés.

```js
import renderer from 'react-test-renderer';
import MyComponent from './MyComponent';

test('renders correctly', () => {
  const tree = renderer.create(<MyComponent />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

Exécutez avec `--updateSnapshot` (ou `-u`) pour mettre à jour les snapshots en échec.

### Couverture de code

Générez un rapport de couverture en ajoutant le flag `--coverage` :

```bash
jest --coverage
```

Cela produit un dossier `coverage/` détaillé avec un rapport HTML.

### Mode Watch

Réexécutez automatiquement les tests lors de modifications de fichiers.

```bash
jest --watchAll   # pour tous les fichiers de test
jest --watch      # seulement les tests liés aux fichiers modifiés (nécessite Git)
```

### Assertions riches (Matchers)

Les matchers courants incluent :

- `toBe` – égalité stricte (`===`)
- `toEqual` – égalité profonde
- `toContain` – vérifie qu'un élément est dans un tableau/itérable
- `toThrow` – vérifie qu'une fonction lève une exception
- `toBeTruthy` / `toBeFalsy`
- `toBeNull`, `toBeDefined`, `toBeUndefined`
- `.resolves` et `.rejects` – pour les promesses

**Exemples :**

```js
expect(2 + 2).toBe(4);
expect({ a: 1 }).toEqual({ a: 1 });
expect([1, 2, 3]).toContain(2);
expect(() => { throw Error('fail'); }).toThrow('fail');
```

### Tests asynchrones

Testez du code asynchrone avec `async/await` :

```js
test('async data', async () => {
  const data = await fetchData();
  expect(data).toBe('peanut butter');
});
```

Ou en utilisant les matchers `.resolves` / `.rejects` :

```js
test('async resolves', () => {
  return expect(fetchData()).resolves.toBe('peanut butter');
});
```

### Configuration et nettoyage

Utilisez les hooks de cycle de vie pour exécuter du code avant/après les tests :

```js
beforeAll(() => {
  // s'exécute une fois avant tous les tests
});

afterAll(() => {
  // s'exécute une fois après tous les tests
});

beforeEach(() => {
  // s'exécute avant chaque test
});

afterEach(() => {
  // s'exécute après chaque test
});
```

## Options CLI

| Option                | Description                                                              |
|-----------------------|--------------------------------------------------------------------------|
| `--coverage`          | Génère et affiche un rapport de couverture.                              |
| `--watch`             | Surveille les fichiers pour détecter les modifications et réexécute les tests concernés. |
| `--watchAll`          | Surveille tous les fichiers et réexécute tous les tests en cas de modification. |
| `--verbose`           | Affiche les résultats individuels des tests en détail.                   |
| `--updateSnapshot` (ou `-u`) | Met à jour tous les fichiers de snapshot.                          |
| `--testNamePattern`   | Exécute les tests dont les noms correspondent à un motif regex.          |
| `--runInBand`         | Exécute les tests en série (utile pour le débogage).                     |
| `--silent`            | Supprime la sortie console des tests.                                    |
| `--clearCache`        | Vide le cache de Jest.                                                   |

## Configuration

Jest peut être configuré via un fichier `jest.config.js` ou la clé `jest` dans `package.json`.

**Exemple de `jest.config.js` :**

```js
module.exports = {
  testEnvironment: 'node',   // 'jsdom' pour un environnement type navigateur
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

Alternativement, ajoutez la configuration dans `package.json` :

```json
"jest": {
  "testEnvironment": "node",
  "roots": ["src"]
}
```

## Avancé : Tests avec React/DOM

Avec `@testing-library/react` :

```js
import { render, screen } from '@testing-library/react';
import MyComponent from './MyComponent';

test('renders the component', () => {
  render(<MyComponent />);
  expect(screen.getByText('Hello')).toBeInTheDocument();
});
```

## Conclusion

Jest est le standard de facto pour tester les applications JavaScript. Son installation sans configuration, son mocking robuste, ses capacités de snapshot et son exécution parallèle rapide en font un outil essentiel pour tout développeur JavaScript. Que vous testiez des fonctions simples ou des composants React complexes, Jest offre une expérience de test agréable et puissante.

---

*Ce document est un brouillon et sera mis à jour au fur et à mesure de l'évolution de Jest.*