---
title: La pyramide des tests : Une stratégie pour une automatisation de tests équilibrée
description: Un modèle de test structuré qui guide les équipes pour construire une suite de tests rapide et fiable en investissant massivement dans les tests unitaires, modérément dans les tests d'intégration, et parcimonieusement dans les tests de bout en bout.
created: 2026-06-23
tags:
  - testing
  - test-automation
  - software-quality
  - strategy
  - ci-cd
status: draft
---

# La pyramide des tests : Une stratégie pour une automatisation de tests équilibrée

## Qu'est-ce que c'est ?

La pyramide des tests est un modèle mental fondamental pour structurer les tests automatisés. Popularisée par **Mike Cohn** dans son livre *Succeeding with Agile* de 2009, elle décrit visuellement les proportions idéales des différents types de tests dans un projet logiciel. La pyramide se compose de trois couches principales :

- **Base (Tests unitaires)** – des tests rapides et isolés de fonctions ou de classes individuelles.
- **Milieu (Tests d'intégration/Service)** – des tests qui vérifient les interactions entre composants (base de données, API, services externes).
- **Sommet (Tests de bout en bout)** – des tests lents et fragiles qui couvrent des flux utilisateur complets depuis l'interface utilisateur jusqu'à la base de données.

La largeur de chaque couche représente le **nombre recommandé de tests** – vous devriez avoir beaucoup plus de tests unitaires que de tests d'intégration, et bien plus de tests d'intégration que de tests E2E.

## Pourquoi l'utiliser ?

La pyramide résout l'anti-modèle courant connu sous le nom de **« Cône de glace »** : les équipes passent la plupart de leur temps à écrire et maintenir des tests d'interface utilisateur lents et fragiles, tout en négligeant les tests unitaires rapides. Cela conduit à :

- Cycles de rétroaction longs (des heures au lieu de secondes).
- Suites de tests fragiles qui cassent à chaque changement d'interface.
- Faible confiance malgré un nombre élevé de tests.
- Vitesse de publication plus lente.

Adopter la pyramide des tests vous donne :

- **Retour rapide** – les tests unitaires s'exécutent en millisecondes.
- **Confiance accrue** – les bogues sont détectés au niveau le moins coûteux.
- **Suites maintenables** – moins de tests E2E signifie moins de pannes.
- **Décalage à gauche** – tester la logique tôt dans le cycle de développement.

## Comment « l'installer » (Configuration dans votre projet)

La pyramide des tests est une stratégie, pas un package. Mais vous pouvez « l'installer » en configurant votre projet pour prendre en charge l'exécution des tests par couche.

### 1. Organisez vos fichiers de test

Séparez les tests dans des dossiers ou utilisez des conventions de nommage :

```
src/
├── __tests__/          # unit tests
│   ├── unit/
│   └── ...
├── __integration__/    # integration tests
└── __e2e__/            # end-to-end tests
```

### 2. Configurez votre exécuteur de test pour exécuter les couches séparément

**JavaScript/TypeScript (Jest) – `jest.config.js`**

```javascript
module.exports = {
  projects: [
    {
      displayName: 'unit',
      testMatch: ['**/__tests__/**/*.test.js'],
      testPathIgnorePatterns: ['/node_modules/']
    },
    {
      displayName: 'integration',
      testMatch: ['**/__integration__/**/*.int.js'],
    },
    {
      displayName: 'e2e',
      testMatch: ['**/__e2e__/**/*.e2e.js'],
    }
  ]
};
```

**Python (pytest) – utilisez des marqueurs**

```python
# pytest.ini
[pytest]
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
```

Fichiers de test :

```python
# test_user_service.py
import pytest

@pytest.mark.unit
def test_user_full_name():
    user = User(first_name="Jane", last_name="Doe")
    assert user.full_name == "Jane Doe"
```

Exécutez avec :

```bash
pytest -m unit
pytest -m integration
pytest -m e2e
```

**Java (JUnit 5) – utilisez des Tags**

```java
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

@Tag("unit")
class UserServiceTest {
    @Test
    void shouldBuildFullName() {
        User user = new User("Jane", "Doe");
        assertEquals("Jane Doe", user.fullName());
    }
}
```

Exécutez avec :

```bash
mvn test -Dgroups=unit
mvn test -Dgroups=integration
mvn test -Dgroups=e2e
```

### 3. Ajoutez des scripts NPM (ou équivalent) pour exécuter les couches facilement

```json
{
  "scripts": {
    "test:unit": "jest --selectProjects unit",
    "test:integration": "jest --selectProjects integration",
    "test:e2e": "jest --selectProjects e2e",
    "test": "npm run test:unit && npm run test:integration"
  }
}
```

### 4. Intégrez dans le CI/CD (par exemple, GitHub Actions)

```yaml
jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run test:unit

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run test:integration

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run test:e2e
```

## Principales fonctionnalités (Les couches en pratique)

### Base : Tests unitaires (environ 70% de la suite)

- **Portée :** une seule fonction, méthode ou classe.
- **Vitesse :** <1 ms par test.
- **Isolation :** pas d'E/S – utilisez des mocks/stubs.
- **Exemples :** validations, calculs, fonctions utilitaires.

```javascript
// unit test example (Jest)
test('adds 1 + 2 equals 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

### Milieu : Tests d'intégration/Service (environ 20% de la suite)

- **Portée :** interaction entre deux ou plusieurs composants (requêtes DB, points d'API, système de fichiers).
- **Vitesse :** dizaines à centaines de millisecondes.
- **Isolation :** utilisez une infrastructure réelle via TestContainers, des bases de données embarquées ou des serveurs légers.

```javascript
// integration test example (supertest + Jest)
const request = require('supertest');
const app = require('../app');

test('GET /api/users returns 200', async () => {
  const response = await request(app).get('/api/users');
  expect(response.statusCode).toBe(200);
});
```

```python
# integration test example (pytest + FastAPI)
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_users():
    response = client.get("/api/users")
    assert response.status_code == 200
```

### Sommet : Tests de bout en bout (environ 10% de la suite)

- **Portée :** système complet via l'interface utilisateur (navigateur, application mobile).
- **Vitesse :** secondes à minutes par test.
- **Fragilité :** très sensible aux changements d'interface.
- **À utiliser uniquement pour :** les flux métier critiques (chemins heureux).

```javascript
// E2E test example (Playwright)
const { test, expect } = require('@playwright/test');

test('user can complete checkout', async ({ page }) => {
  await page.goto('/shop');
  await page.click('text=Add to Cart');
  await page.goto('/checkout');
  await page.fill('#email', 'test@example.com');
  await page.click('text=Place Order');
  await expect(page.locator('.confirmation')).toBeVisible();
});
```

## Pièges courants et principes

### 1. Anti-modèle du cône de glace

Évitez les suites où 80% des tests sont des E2E. Si vous voyez cela, réécrivez agressivement les tests E2E critiques en tests d'intégration ou unitaires en extrayant la logique métier de l'interface utilisateur.

### 2. Décalage à gauche

Lorsqu'un test E2E échoue, écrivez d'abord un test unitaire ou d'intégration qui reproduit le bogue. Souvent, vous pouvez ensuite supprimer ou simplifier le test E2E, rendant l'ensemble de la suite plus rapide.

### 3. Gardez les tests indépendants

Chaque test doit pouvoir s'exécuter de manière isolée et dans n'importe quel ordre. Un état mutable partagé conduit à des tests instables.

### 4. Utilisez un mock approprié au niveau unitaire

Pour les tests unitaires, simulez les dépendances externes. Pour les tests d'intégration, utilisez des instances réelles (TestContainers, bases de données en mémoire) mais ne simulez pas le composant que vous testez.

## Conclusion

La pyramide des tests reste l'un des concepts les plus importants dans les tests logiciels modernes. Elle donne aux équipes un modèle clair et exploitable pour construire une suite de tests rapide, fiable et maintenable. En investissant massivement dans les tests unitaires, en ajoutant des tests d'intégration là où les composants se connectent, et en utilisant les tests E2E uniquement pour les parcours critiques, vous pouvez atteindre à la fois une confiance élevée et un retour rapide.

Commencez par auditer votre suite de tests actuelle : mesurez le temps et le nombre par couche. Ensuite, utilisez les exemples de configuration ci-dessus pour séparer les tests, adoptez la pensée du décalage à gauche, et regardez votre vélocité de publication s'améliorer.