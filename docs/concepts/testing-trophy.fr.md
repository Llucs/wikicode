---
title: "Le Trophée des tests : prioriser les tests d’intégration dans les applications web modernes"
description: "Un guide pratique du modèle du trophée de test de Kent C. Dodds — une stratégie qui place les tests d’intégration au centre et utilise l’analyse statique, les tests unitaires et les tests E2E comme couches de support."
created: 2026-08-08
tags:
  - testing
  - frontend
  - integration-testing
  - react
  - quality
status: draft
---

# Le Trophée des tests : prioriser les tests d’intégration dans les applications web modernes

## Ce que c’est

Le **Trophée des tests** est un modèle de stratégie de test créé par Kent C. Dodds (2017) pour les applications web modernes en JavaScript/TypeScript. Là où la **pyramide de test** classique place *de nombreux tests unitaires* à la base et *peu de tests de bout en bout* au sommet, le trophée inverse l’investissement central : la plus grande partie dédiée aux tests est la couche **test d’intégration**, soutenue par :

- **L’analyse statique** (linting, formatage, vérification de types) comme base ;
- **Les tests unitaires** comme une couche petite mais utile ;
- **Les tests de bout en bout** comme un petit nombre de parcours lents et à forte valeur, au sommet.

Dans le modèle du trophée, le signal le plus fiable qu’une application fonctionne provient de son passage à travers le câblage réel orienté utilisateur — des composants montés ensemble, de vrais formulaires, de vraies requêtes DOM, de vrais appels `fetch` vers une frontière réseau simulée — plutôt que de fonctions isolées dont des modules entiers ont été mockés.

## Pourquoi c’est important

Le conseil de la pyramide « écrivez de nombreux tests unitaires » fonctionne bien pour la logique pure, mais s’effondre pour les applications centrées sur l’interface. Quand un code frontend est couvert principalement par des tests unitaires qui mockent chaque module avoisinant :

- Les tests commencent à vérifier les **détails d’implémentation**, pas le comportement.
- Une refactorisation qui préserve l’expérience utilisateur peut casser des dizaines de tests.
- De vraies erreurs de câblage (mauvaise prop, `aria-label` manquant, charge utile API incorrecte) filent entre les mailles parce que chaque unité est testée isolément.

Les tests d’intégration — des tranches d’application rendues qui ex exercent des interactions réalistes — rattrapent ces manques de câblage. Le trophée en fait des citoyens de première classe, ce qui vous donne **plus de confiance pour chaque dollar de test**.

## Le modèle en une image

```
                   ┌────────────┐
                   │    E2E    │  ← critical paths, slow, few
                   └────────────┘

              ┌─────────────────────┐
              │  Integration tests  │  ← the trophy body: biggest
              │                     │    slice of your effort
              └─────────────────────┘

              ┌─────────────────────┐
              │     Unit tests      │  ← complex logic, illustrated
              └─────────────────────┘

             ┌─────────────────────────┐
             │    Static + type check  │  ← ESLint, TypeScript,
             └─────────────────────────┘  Prettier; nearly free
```

}\ Le principe directeur bien connu de Testing Library appartient à ce modèle :

> Plus vos tests ressemblent à la manière dont votre logiciel est utilisé, plus ils peuvent vous donner confiance.

## Décomposition par couche

| Couche | Outils | Coût d’écriture | Confiance gagnée par test | À utiliser quand |
| --- | --- | --- | --- | --- |
| **Analyse statique** (base) | ESLint, TypeScript, Prettier | Quasi nul | Détecte les coquilles, les erreurs de types, les mauvais contrats d’API avant qu’un test s’exécute | partout ; c’est votre filet de sécurité |
| **Tests unitaires** (tige) | Jest, Vitest | Faible | Élevée pour la logique isolée ; faible pour le câblage applicatif | fonctions pures avec de la logique conditionnelle |
| **Tests d’intégration** (corps du trophée) | Vitest/Jest + Testing Library, MSW | Moyen | **La plus élevée pour le câblage applicatif** | les composants, les flux, les interactions API |
| **Tests E2E** (pointe) | Playwright, Cypress | Élevé, lent, parfois instable | Élevée mais redondante avec les tests d’intégration | parcours métier critiques (connexion, commande) |

### 1. Analyse statique — la base

Les outils statiques protègent l’ensemble du système au coût le plus bas : pas de configuration DOM, pas de minutes CI, un retour immédiat. Cela comprend :

- des **linters** qui attrapent les erreurs fréquentes et la cohérence de style ;
- des **vérificateurs de types** qui valident la forme de chaque fonction et de chaque contrat de composant ;
- des **formateurs** pour garder des diffs propres.

### 2. Tests unitaires — la tige

Les tests unitaires ont une vraie mission : valider la logique pure et délicate qui est trop difficile à exercer via une interface. Exemple : le formatage de dates, les calculs de taxe, un constructeur d’URL. La valeur est n’est élevée que lorsque chaque test se concentre sur *le contrat de cette fonction*, en mockant au plus ses entrées directes.

### 3. Tests d’intégration — le corps du trophée

Un test d’intégration générique rend une **vraie tranche de l’application** — une page ou un composant — et la pilote avec des événements visibles par l’utilisateur (écriture, clic, soumission) pendant que le vrai DOM est montable dans un environnement sans navigateur (jsdom, happy-dom). Les frontières asynchrones réelles comme HTTP sont bouchées à la **limite** avec des outils comme MSW (Mock Service Worker).

### 4. Tests E2E — la pointe

Quelques parcours Playwright/Cypress font tourner toute l’application dans un vrai navigateur. Usez-les pour les parcours que vous feriez vous-même en production : inscription, paiement, onboarding. Traitez-les comme un audit, pas comme une boîte à outils de régression : ils sont trop lents et trop fragiles pour couvrir chaque cas limite.

## Un exemple complet : un flux de connexion

Voyons à ressembler ce que chaque couche donne dans une app React + TypeScript + Vite réaliste.

### Configuration du projet

```bash
# create the app
npm create vite@latest trophy-demo -- --template react-ts
cd trophy-demo

# install everything we need per layer
npm i -D typescript @types/react @types/react-dom \
  eslint vitest jsdom \
  @testing-library/react @testing-library/user-event @testing-library/jest-dom \
  msw @playwright/test

# install browser binaries once
npx playwright install
```

Ajoutez les scripts :

```json
{
  "name": "trophy-demo",
  "scripts": {
    "dev": "vite",
    "typecheck": "tsc --noEmit",
    "lint": "eslint .",
    "test": "vitest run",
    "test:e2e": "playwright test"
  }
}
```

### Couche statique : types + lint

```json
{
  "compilerOptions": {
    "strict": true,
    "jsx": "react-jsx"
  }
}
```

La couche statique dans le CI :

```bash
npm run typecheck && npm run lint
```

### Le composant que nous allons tester

Exécutez le test contre le même composant que celui que l’utilisateur utilise. La note que la **frontière réseau** est la seule chose qui touche l’environnement.

```tsx
// src/components/LoginForm.tsx
import { useState, type FormEvent } from "react";

export function LoginForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      setName(username);
    }
  }

  if (name) {
    return <p>Welcome, {name}</p>;
  }

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="username">Username</label>
      <input
        id="username"
        value={username}
        onChange={(event) => setUsername(event.target.value)}
      />

      <label htmlFor="password">Password</label>
      <input
        id="password"
        type="password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
      />

      <button type="submit">Sign in</button>
    </form>
  );
}
```

### Couche unitaire : un helper pur

```ts
// src/lib/formatPrice.test.ts
import { describe, expect, it } from "vitest";
import { formatPrice } from "./formatPrice";

describe("formatPrice", () => {
  it("formats cents into a local currency string", () => {
    expect(formatPrice(1999)).toBe("$19.99");
  });

  it("handles zero", () => {
    expect(formatPrice(0)).toBe("$0.00");
  });

  it("rounds to the nearest cent", () => {
    expect(formatPrice(1005)).toBe("$10.05");
  });
});
```

### Couche d’intégration — le corps du trophée

Configurez Vitest avec un DOM de type navigateur et les matchers de Testing Library :

```ts
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./test/setup.ts"],
  },
});
```

```ts
// test/setup.ts
import "@testing-library/jest-dom/vitest";
import { afterAll, afterEach, beforeAll } from "vitest";

import { server } from "./server";

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

```ts
// test/server.ts
// MSW: enables integration tests to stub at the HTTP edge since
// the component is still using the real `fetch` API.
import { setupServer } from "msw/node";

export const server = setupServer();
```

Maintenant, le flux de connexion comme utilisateur le pourrait taper :

```tsx
// src/components/LoginForm.test.tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { server } from "../../test/server";
import { LoginForm } from "./LoginForm";

describe("LoginForm", () => {
  it("accepts credentials and welcome the user", async () => {
    server.use(
      http.post("/api/login", () =>
        HttpResponse.json({ token: "test-token" })
      )
    );

    const user = userEvent.setup();
    render(<LoginForm />);

    await user.type(screen.getByLabelText(/username/i), "alice");
    await user.type(screen.getByLabelText(/password/i), "s3cret");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    expect(await screen.findByText(/welcome, alice/i)).toBeInTheDocument();
  });
});
```

Remarquons ce que le test d’intégration **ne fait pas** :

- Il ne mocke pas `LoginForm` ni ses sous-modules internes.
- Il n’inspecte pas l’état React ni l’appel `fetch`.
- Il simule à la frontière de l’API — là où le vrai serveur répondrait — avec MSW.

Cela signifie que le test se brise si la charge utile du `fetch`, la gestion des réponses, le texte des labels, le type de bouton ou une seule extension de succès se cassent. C’est exactement la confiance que leème trophée place au centre.

### Couche E2E : la pointe du trophée

Utilisez Playwright pour un ou deux parcours « salutaires » dans la interface.

```ts
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  webServer: {
    command: "npm run dev",
    url: "http://localhost:5173",
    reuseExistingServer: !process.env.CI,
  },
  use: {
    baseURL: "http://localhost:5173",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
});
```

```ts
// e2e/login.spec.ts
import { expect, test } from "@playwright/test";

test("a returning customer can sign in", async ({ page }) => {
  await page.goto("/login");

  await page.getByLabel("Username").fill("alice");
  await page.getByLabel("Password").fill("s3cret");
  await page.getByRole("button", { name: "Sign in" }).click();

  await expect(page.getByText(/welcome, alice/i)).toBeVisible();
});
```

Le test E2E est à peu près la même séquence que le test d’intégration — et c’est normal. Le E2E existe pour vérifier que la version production / engagement se lance, que le routing fonctionne, que l’API répond et qu’aucune bonne infrastructure n’a été introduite. C’est pourquoi un ou deux de ces parcours par fonctionnalité critique suffisent.

## Stratégie de mock : mock à la limite, jamais vers l’intérieur

La ligne entre un test d’intégration utile et un test perd leur temps : *où* le mock se produit.

| Ce que vous êtes tenté de mocker | Recommandation du trophée |
| --- | --- |
| L’appel de service global ou API (`fetch` – le réseau) | ✅ Utilisez la frontière **MSW** / `server.use` |
| Le SDK de paiement tiers à travers un wrapper fin | ✅ Stub à travers l’interface publique |
| Un fournisseur de contexte or un système d’alerte dans la même application | ❌ Rendez-le via le provider si l’utilisateur en dépend réellement |
| Un composant enfant dans la page | ❌ Car cela annule la vérification du câblage |
| `useState` / état interne React | ❌ Testez le résultat rendu |

Pourquoi simuler un utilisateur ? D dès que vous mockez une composant interne, vous perdez la capacité de détecter le vrai bug d’utilisateur final que le trophée essaie de résoudre.

## Compromis

### Quand le trophée gagne

- **Frontend très centré sur l’interface** : le monde vaut dans l’intégration des composants et des services.
- **Équipes avec un temps limité** : les tests d’intégration couvrent des workflows que la suite E2E lente ne peut pas prendre en charge.
- **Projets qui adoptent React / Vue / Svelte Testing Library** : leurs requêtes sont conçues pour les flux d’intégration.

### Quand la forme du trophée n’est pas adaptée

- **Bibliothèques pures et outils CLI** — Une pile de tests unitaires reste le meilleur investissement. Pas de DOM, pas de flux de page.
- **Logique forte côté backend / algorithmes métier** — les tests unitaires sur des services purs dépassent une grosse batterie de tests web d’intégration.
- **codebase de hobby / expérimental avec un backend de test cassé** — les tests E2E vont continuer de flaké. L’intégration reste utile, mais avec modération.
- **Grandes applications héritées avec un arbre de composition enchevêtré** — il faut peut-être laisser les tests unitaires atomiques faire entrer. Commencez par quelques scénarios « tranches » plutôt qu’une matrice complète.

### Tableau : pyramide contre trophée contre nid d’abeille

| Stratégie | L’importance | Exemple typique | Le plus fort quand |
| --- | --- | --- | --- |
| **Pyramide de test (Cohn)** | Des centaines de tests unitaires ; quelques E2E | Les séries backend classiques | Backend avec des règles pures et CI rapide |
| **Trophée de test (Dodds)** | Les tests d’intégration au centre ; une base statique ; quelques E2E | Front-end web React / Vue | App centrées interface, basées composants |
| **Honeycomb de test** | Le centre et le haut lourds (intégration + E2E) | Services distribués avec de nombreux contrats | Interactions complexes entre des services |

Le trophée n’est pas la réponse « juste à tout » — c’est le point de coût le plus efficace par défaut pour une *interface web* //props.

## Meilleures pratiques

1. **Faites de l’analyse statique la fondation.** Exécutez `tsc --noEmit`, `eslint .` et Prettier dans le CI avant les tests lents. Adaptez le flux pour qu’il soit chaleurs : les types attrapent déjà la moitié des bugs avant même qu’un test s’exécute.
2. **Privilégiez les tests d’intégration par défaut.** Pour une inscription pour, le contenu d’un panier , le rendu d’un tableau de bord : un test de session avec des requêtes centrées utilisateur. Utilisez MSW pour la couche réseau.
3. **Interrogez comme un utilisateur.** Utilisez `getByLabelText`, `getByRole`, `getByPlaceholderText`, `findByText`, et jamais des `data-testid` du DOM ou des sélecteurs de classe CSS. Ayez : `getByRole('button', { name: 'Sign in' })`.
4. **Attendez la realité.** Utilisez `findBy*` / `waitFor` dès qu’un état est asynchrone. Évitez tout `setTimeout` artificiel dans les tests.
5. **Mock aux limites.** Le réseau, l’horloge, le `localStorage` du navigateur. Ne mockez jamais le composant qui est bloqué par une dépendance interne.
6. **E2E comme audit, pas comme régression.** Gardez la liste E2E réduite — identification, paiement, onboarding. Une suite E2E avec 200 tests a des coûts de vitesse et de constant instabilité presque garantis.
7. **Tests unitaires sur les mathématiques délicates.** Gâtez vos tests unitaires où la logique est : parsing de dates, devises, contrats, tris, permissions. Ça reste pur d’entrée → sortie.
8. **Si le style du refactor casse 40 tests unitaires mais qu’aucun visuel ne change, c’est un signal** que les tests attendent connaissance de l’implémentation plus que du comportement. Refonte des tests vers les rôles « user view ».
9. **Important en CI** : un seul `npm run test` devrait exécuter toute la couche d’intégration dans la MR; les E2E peuvent être une tâche obligatoire séparée, ou après lint/unité.

## Résumé

Le trophée de test fait passer le modèle mental de « vérifier chaque fonction » à **« vérifier l’application à travers le chemin de l’utilisateur »** . Son idée centrale est ceci :

> La confiance est un produit de la proximité du test avec l’utilisation réelle de l’application, et non pas un produit du nombre de fois où vous découpez l’application en une foule de tests unitaires mockés.

En bas, l’analyse statique — des rails gratuits.
- La philosophie des tests unitaires — une petite[p...] vs complex logic.
- **Tests d’intégration dans le corps** — le réseau principal d’assurance.
- **E2E sur le haut** — l’étalon d’un parcours critique.

Le trophée ne retire pas la pyramide ; il déplace l’effort depuis les tests unitaires de fausse confiance pour les appliquer à la surface qu’un utilisateur touche réellement : l’intégration.

## Références

- Kent C. Dodds — [The Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy)
- Testing Library — [The guiding principles](https://testing-library.com/docs/)
- MSW — [Mock Service Worker](https://mswjs.io/docs/)
- Playwright — [Docs](https://playwright.dev/docs/intro)