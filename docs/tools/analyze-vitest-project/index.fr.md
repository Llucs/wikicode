---
title: "Vitest : Framework de Test de Nouvelle Génération Propulsé par Vite"
description: "Un framework de test rapide, natif de Vite, avec un support transparent de TypeScript et d'ESM, conçu pour les applications modernes JavaScript/TypeScript."
created: 2026-06-23
tags:
  - testing
  - unit-testing
  - vite
  - typescript
  - jest-alternative
status: draft
---

# Vitest : Framework de Test de Nouvelle Génération Propulsé par Vite

## Aperçu

Vitest est un framework de test unitaire de nouvelle génération construit sur Vite. Créé par Anthony Fu et l'équipe principale de Vite, il a été publié en décembre 2021 pour remédier aux frictions entre le serveur de développement de Vite et les exécuteurs de test traditionnels comme Jest. En exploitant le pipeline de transformation de Vite, le Hot Module Replacement (HMR) et son système de plugins, Vitest offre une expérience développeur significativement plus rapide et plus cohérente, en particulier pour les projets utilisant déjà Vite.

### Pourquoi Vitest ?

- **Support natif ESM :** Contrairement à Jest, qui nécessite des transformations complexes pour les modules ES, Vitest gère les modules ESM nativement car il utilise le pipeline basé sur Rollup de Vite.
- **HMR pour les tests :** Seuls les tests concernés sont réexécutés lorsque le code change, rendant la boucle de rétroaction quasi instantanée.
- **Compatibilité avec l'API Jest :** Utilise la même API `describe`, `it`, `expect`, avec `vi` remplaçant `jest` pour les mocks et les espions. La migration est simple.
- **Support de première classe pour TypeScript :** TypeScript est transpilé instantanément via esbuild sans configuration supplémentaire.
- **Tests de composants :** Support intégré pour Vue, React, Svelte et Lit avec des environnements comme jsdom, happy-dom et Playwright.
- **Couverture de code intégrée :** Prend en charge les fournisseurs de couverture v8 et Istanbul dès l'installation.
- **Interface Vitest UI :** Un tableau de bord graphique riche pour visualiser les tests et les dépendances des modules.

## Installation

Ajoutez Vitest comme dépendance de développement :

```bash
npm install -D vitest
```

Avec yarn ou pnpm :

```bash
yarn add -D vitest
pnpm add -D vitest
```

Ensuite, ajoutez un script de test dans `package.json` :

```json
{
  "scripts": {
    "test": "vitest"
  }
}
```

> **Note :** Exécutez `vitest run` pour une exécution unique (sans mode watch). Le mode par défaut est le mode watch, qui relance les tests en cas de modification.

## Écrire des tests

Vitest utilise la même API globale que Jest. Importez `test`, `expect`, `describe`, etc. depuis `vitest` ou activez `globals` dans la configuration.

### Exemple de base

```javascript
// sum.test.js
import { expect, test } from 'vitest';
import { sum } from './sum';

test('adds 1 + 2 to equal 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

### Utilisation de `describe` et `it`

```typescript
import { describe, it, expect } from 'vitest';

describe('Array', () => {
  it('should be empty initially', () => {
    const arr: number[] = [];
    expect(arr).toHaveLength(0);
  });
});
```

### Mocks avec `vi`

```typescript
import { vi, test, expect } from 'vitest';

const mockFn = vi.fn();
mockFn('hello');
expect(mockFn).toHaveBeenCalledWith('hello');

// Mock d'un module
vi.mock('../api', () => ({
  fetchData: vi.fn(() => Promise.resolve({ data: 'mocked' })),
}));
```

## Configuration

Vitest peut être configuré dans le fichier `vite.config.ts` de votre projet (recommandé) ou dans un fichier `vitest.config.ts` séparé. La configuration est placée sous la propriété `test`.

```typescript
/// <reference types="vitest/config" />
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true, // Utiliser test/expect sans import
    environment: 'jsdom', // ou 'happy-dom', 'node', 'edge-runtime'
    setupFiles: './src/setup.ts',
    include: ['src/**/*.{test,spec}.{js,ts}'],
    coverage: {
      provider: 'v8', // ou 'istanbul'
      reporter: ['text', 'json', 'html'],
    },
  },
});
```

Si vous utilisez un `vitest.config.ts` autonome, le format est identique mais doit exporter une configuration Vite (Vitest étend Vite).

## Fonctionnalités clés

### 1. Hot Module Replacement (HMR) pour les tests

Vitest surveille les fichiers source et de test. Lorsque des modifications sont apportées, seuls les tests concernés sont réexécutés, offrant un retour quasi instantané.

```bash
vitest
```

Appuyez sur `r` pour relancer tous les tests, `f` pour relancer uniquement les tests échoués, `q` pour quitter.

### 2. Support natif ESM

Puisque Vitest utilise le pipeline de Vite, les modules ES fonctionnent naturellement. Aucun plugin Babel ou transformation spéciale n'est nécessaire.

### 3. Compatibilité avec l'API Jest

| Jest | Vitest |
|------|--------|
| `jest.fn()` | `vi.fn()` |
| `jest.mock()` | `vi.mock()` |
| `jest.spyOn()` | `vi.spyOn()` |
| `jest.useFakeTimers()` | `vi.useFakeTimers()` |

Tous les hooks de cycle de vie (`beforeEach`, `afterEach`, `beforeAll`, `afterAll`) fonctionnent identiquement.

### 4. Support de première classe pour TypeScript

Pas besoin de `ts-jest` ni de configuration Babel séparée. Écrivez directement des tests TypeScript et Vitest gère la transpilation via esbuild.

```typescript
interface User { name: string }
function greet(user: User) { return `Hello, ${user.name}`; }

it('greets user', () => {
  expect(greet({ name: 'Alice' })).toBe('Hello, Alice');
});
```

### 5. Tests de composants

Vitest fonctionne parfaitement avec les bibliothèques de test de composants comme `@testing-library/vue`, `@testing-library/react` et `@vue/test-utils`. Utilisez l'option `environment` pour simuler un environnement navigateur.

```typescript
// Exemple avec @vue/test-utils
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

### 6. Couverture de code

Support de couverture intégré via v8 (par défaut) ou Istanbul.

```bash
vitest run --coverage
```

Ou via la configuration :

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

### 7. Interface Vitest UI

Une interface web optionnelle et riche pour explorer les résultats des tests.

```bash
vitest --ui
```

L'interface fournit un tableau de bord avec l'état des tests, les durées, une arborescence de fichiers et un graphique des dépendances entre modules.

### 8. Mode espace de travail (support des monorepos)

Vitest peut exécuter des tests sur plusieurs projets ou packages dans un monorepo à l'aide d'un fichier `vitest.workspace.ts`. Les configurations peuvent être intégrées ou référencer des fichiers/glob patterns.

```typescript
// vitest.workspace.ts
import { defineWorkspace } from 'vitest/config';

export default defineWorkspace([
  'packages/*',
  {
    // Configuration intégrée pour un projet spécifique
    test: {
      name: 'my-package',
      root: './packages/my-package',
      environment: 'node',
    },
  },
]);
```

Chaque projet peut avoir sa propre configuration, tout en étant exécuté à partir d'une seule commande.

### 9. Exécution parallèle

Les tests s'exécutent en parallèle via des threads workers (par défaut) ou des processus enfants (définissez `pool: 'forks'`).

```typescript
test: {
  pool: 'forks', // ou 'threads' (par défaut)
  poolOptions: {
    forks: {
      singleFork: true,
    },
  },
}
```

## Exemples de commandes

| Commande | Description |
|----------|-------------|
| `vitest` | Exécute les tests en mode watch (par défaut) |
| `vitest run` | Exécute les tests une fois (sans mode watch) |
| `vitest run --reporter verbose` | Sortie détaillée |
| `vitest --coverage` | Exécute les tests avec rapport de couverture |
| `vitest --ui` | Lance l'interface Vitest UI |
| `vitest --config vitest.ci.ts` | Utilise un fichier de configuration personnalisé |
| `vitest --project projectName` | Exécute les tests d'un projet spécifique dans l'espace de travail |
| `vitest test/specific.test.ts` | Exécute un fichier de test spécifique |
| `npx vitest --run --reporter json` | Génère les résultats au format JSON (adapté à l'intégration continue) |

## Migration depuis Jest

La migration de Jest vers Vitest implique généralement les étapes suivantes :

1. Remplacez `jest` par `vi` dans les fichiers de test (spy, mock, fn).
2. Mettez à jour les imports de `@jest/globals` vers `vitest` (ou utilisez `globals: true`).
3. Déplacez la configuration Jest vers `vite.config.ts` ou `vitest.config.ts` sous la clé `test`.
4. Adaptez les mocks de modules : utilisez `vi.mock` au lieu de `jest.mock`.
5. Ajustez les timers : utilisez `vi.useFakeTimers()`.

Un guide de migration dédié est disponible dans la documentation officielle de Vitest.

## Cas d'utilisation

- **Tests unitaires :** Fonctions, utilitaires et logique métier.
- **Tests de composants :** Composants Vue, React, Svelte, Solid et Lit.
- **Tests d'intégration :** Points d'API, modules combinés, avec environnements simulés.
- **Développement de bibliothèques / CLI :** Exécutions CI rapides avec un excellent support TypeScript.
- **Tests de monorepo :** Le mode espace de travail offre des tests unifiés dans tous les packages.

## Pourquoi Vitest plutôt que Jest ?

- **Support ESM :** Aucun module expérimental ou transformation complexe nécessaire.
- **Vitesse :** Démarrages à froid plus rapides grâce au bundling optimisé de Vite et à la transpilation avec esbuild.
- **HMR :** Réexécutions instantanées pour un workflow TDD efficace.
- **Configuration simplifiée :** Réutilise la configuration Vite ; pas de transformateurs spécifiques à Jest.
- **Exécution parallèle :** Les threads workers surpassent la configuration par défaut de Jest.
- **Alignement avec la pile moderne :** Conçu pour les projets basés sur Vite (Vue, Svelte, React, etc.).

Pour les grands projets et les monorepos, Vitest peut réduire le temps d'exécution des tests de 2 à 10 fois par rapport à Jest.

## Ressources supplémentaires

- [Documentation officielle](https://vitest.dev/)
- [Dépôt GitHub](https://github.com/vitest-dev/vitest)
- [Guide de migration depuis Jest](https://vitest.dev/guide/migration.html#migrating-from-jest)
- [Démo de l'interface Vitest UI](https://vitest.dev/guide/ui.html)