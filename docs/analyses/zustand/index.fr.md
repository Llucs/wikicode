---
title: Zustand — Gestion d'état minimaliste pour React
description: Un guide complet sur Zustand, une bibliothèque de gestion d'état légère et basée sur les hooks pour React et JavaScript vanilla, incluant l'installation, les concepts de base, les middlewares et les schémas avancés.
created: 2026-06-15
tags:
  - analysis
  - state-management
  - react
  - javascript
  - library-study
status: draft
---

# Zustand — Gestion d'état minimaliste pour React

## Aperçu

**Zustand** (qui signifie « état » en allemand) est une bibliothèque de gestion d'état légère, rapide et évolutive pour React et JavaScript vanilla. Créée par Paul Henschel et le collectif Poimandres (le même groupe à l'origine de React Three Fiber, Jotai et React Spring), Zustand offre une API minuscule (~1 Ko gzippé) sans code rébarbatif, sans fournisseur d'encapsulation et avec un modèle de consommation centré sur les hooks.

Contrairement à Redux ou MobX, Zustand n'impose pas de patrons architecturaux, de types d'actions, de réducteurs ou de répartiteurs. Au lieu de cela, il traite l'état comme un objet simple qui peut être lu et modifié via des fonctions simples, tout en tirant parti de `useSyncExternalStore` de React 18 pour un rendu concurrent sans danger.

## Pourquoi Zustand ?

- **Sans Provider** – Les composants s'abonnent directement au store ; pas d'imbrication de `<Provider>`.
- **Basé sur des sélecteurs** – Les composants se re‑rendent uniquement lorsque la partie choisie change (en utilisant une égalité stricte `===` par défaut).
- **Faible empreinte** – ~1 Ko gzippé, ce qui le rend adapté aux applications critiques en termes de performances.
- **Noyau agnostique au framework** – Le store peut être utilisé en dehors de React (par exemple, dans SSR Next.js, scripts Node.js, ou Web Workers).
- **Middlewares riches** – Plugins officiels pour la persistance (`persist`), les modifications mutables de type Immer (`immer`), les DevTools Redux (`devtools`) et les abonnements basés sur les sélecteurs (`subscribeWithSelector`).

## Installation

```bash
npm install zustand
# or
yarn add zustand
```

Zustand est entièrement tree‑shakable et écrit en TypeScript ; les types sont inclus prêts à l'emploi.

## Utilisation de base

### Créer un store

`create` accepte une fonction qui prend `set`, `get` et `storeAPI` comme arguments. La fonction retourne un objet contenant l'état et toutes les actions.

```javascript
import { create } from 'zustand';

const useBearStore = create((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
  decrease: (by) => set((state) => ({ bears: state.bears - by })),
  reset: () => set({ bears: 0 }),
}));
```

### Utiliser le store dans un composant

Appelez le hook du store avec un **sélecteur** qui retourne la partie d'état dont vous avez besoin. Le composant ne se re‑rendra que lorsque la valeur sélectionnée change.

```jsx
function BearCounter() {
  const bears = useBearStore((state) => state.bears);
  const increase = useBearStore((state) => state.increase);

  return (
    <div>
      <h1>{bears} bears</h1>
      <button onClick={() => increase(1)}>Ajouter un ours</button>
    </div>
  );
}
```

### Accéder et s'abonner en dehors de React

Le store peut être utilisé en JavaScript pur sans aucune dépendance à React :

```javascript
// Lire l'état actuel (sans s'abonner)
const current = useBearStore.getState();
console.log(current.bears); // 0

// S'abonner aux changements
const unsub = useBearStore.subscribe((state) => {
  console.log('L\'état a changé :', state.bears);
});

// Déclencher une action depuis l'extérieur de React
useBearStore.getState().increase(2);

// Se désabonner lorsque nécessaire
unsub();
```

## Fonctionnalités clés

### 1. Architecture sans Provider

Les stores Zustand sont des objets autonomes. Il n'y a pas de `<BearProvider>` à encapsuler, ce qui signifie pas d'imbrication de Provider, pas de re‑rendus accidentels de sous‑arbres entiers et un modèle mental plus simple. Le store est simplement importé et utilisé dans n'importe quel composant.

### 2. Abonnements basés sur des sélecteurs (performances par défaut)

La fonction sélecteur reçoit l'état complet et retourne uniquement les valeurs dont le composant a besoin. Zustand suit internement les sélecteurs et ne déclenche de re‑rendu que lorsque la valeur retournée change (égalité de référence). Pour des comparaisons profondes, vous pouvez passer une fonction d'égalité personnalisée en tant que second argument au hook.

```javascript
const userName = useUserStore(
  (state) => state.user.name,
  (oldName, newName) => oldName === newName  // égalité profonde
);
```

Si aucun sélecteur n'est donné, le composant s'abonne à l'**intégralité** du store—à éviter pour les stores volumineux.

### 3. Code rébarbatif minimal

Un store complet est créé en un seul appel `create`. Les actions sont simplement des fonctions qui appellent `set`, et peuvent être imbriquées, asynchrones ou exportées indépendamment.

```javascript
const useAuthStore = create((set, get) => ({
  user: null,
  login: async (credentials) => {
    const user = await api.login(credentials);
    set({ user });
  },
  logout: () => set({ user: null }),
  hasRole: (role) => get().user?.role === role,  // getter synchrone
}));
```

### 4. Système de middlewares

Zustand fournit des middlewares officiels qui enveloppent le créateur du store pour ajouter des fonctionnalités.

#### Middleware Persist

Synchronise automatiquement l'état avec un backend de stockage (localStorage, AsyncStorage, IndexedDB, etc.).

```javascript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const useSettingsStore = create(
  persist(
    (set) => ({
      theme: 'light',
      setTheme: (theme) => set({ theme }),
    }),
    {
      name: 'app-settings', // clé de stockage
      storage: localStorage, // par défaut localStorage ; peut être AsyncStorage
    }
  )
);
```

#### Middleware Immer

Écrivez les mises à jour d'état de manière mutable en utilisant les brouillons Immer.

```javascript
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

const useCartStore = create(
  immer((set) => ({
    items: [],
    addItem: (item) =>
      set((draft) => {
        draft.items.push(item);
      }),
    removeItem: (id) =>
      set((draft) => {
        draft.items = draft.items.filter((i) => i.id !== id);
      }),
  }))
);
```

#### Middleware DevTools

Intégrez l'extension de navigateur Redux DevTools pour le débogage.

```javascript
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

const useTodoStore = create(
  devtools(
    (set) => ({
      todos: [],
      addTodo: (text) =>
        set((state) => ({ todos: [...state.todos, { text, done: false }] })),
    }),
    { name: 'TodoStore' } // nom optionnel du store dans DevTools
  )
);
```

#### Middleware subscribeWithSelector

Permet des abonnements fins avec des sélecteurs, similaire à l'API des hooks, mais en dehors de React.

```javascript
import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';

const useCounterStore = create(
  subscribeWithSelector(() => ({
    count: 0,
    increment: () => set((state) => ({ count: state.count + 1 })),
  }))
);

// S'abonner à un sélecteur (ne se déclenche que lorsque count change)
const unsub = useCounterStore.subscribe(
  (state) => state.count,
  (newCount) => console.log('Le compteur est maintenant à', newCount)
);
```

### 5. Utilisation en JavaScript vanilla (non‑React)

La logique centrale de gestion d'état de Zustand est complètement indépendante de React. Vous pouvez créer des stores sans dépendance à React, ce qui est utile dans des scripts Node, des Web Workers ou tout environnement non‑React.

```javascript
import { createStore } from 'zustand/vanilla';

const counterStore = createStore((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}));

// S'abonner avec store.subscribe
counterStore.subscribe(console.log);
counterStore.getState().increment(); // log { count: 1 }
```

Pour intégrer le store vanilla dans React, vous pouvez l'envelopper avec `useStore` :

```javascript
import { useStore } from 'zustand';
import { createStore } from 'zustand/vanilla';
import { persist } from 'zustand/middleware'; // les middlewares fonctionnent aussi avec vanilla

const vanillaStore = createStore(persist(/* ... */));

function MyComponent() {
  const count = useStore(vanillaStore, (s) => s.count);
  const inc = useStore(vanillaStore, (s) => s.increment);
  // ...
}
```

### 6. Stores multiples (modèle des slices)

Zustand encourage la composition de stores indépendants plutôt qu'un store monolithique unique. Vous pouvez également combiner plusieurs slices en un seul store en utilisant le **modèle des slices** ou simplement en appelant `create` plusieurs fois.

#### Stores séparés

```javascript
// store/authStore.js
export const useAuthStore = create(/* ... */);

// store/cartStore.js
export const useCartStore = create(/* ... */);

// Composant
import { useAuthStore } from './store/authStore';
import { useCartStore } from './store/cartStore';
```

#### Modèle des slices (un seul store à partir de plusieurs slices)

```javascript
import { create } from 'zustand';

const createAuthSlice = (set) => ({
  user: null,
  setUser: (user) => set({ user }),
});

const createCartSlice = (set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
});

const useStore = create((...a) => ({
  ...createAuthSlice(...a),
  ...createCartSlice(...a),
}));
```

### 7. Intégration avec d'autres bibliothèques

- **React Query / SWR** – Zustand ne doit **pas** remplacer la mise en cache d'état serveur. Utilisez des bibliothèques dédiées pour les données d'API et Zustand pour l'état UI / côté client.
- **Next.js** – Les stores Zustand peuvent être créés et consommés dans des composants client. Pour les composants serveur, utilisez `createStore` de `zustand/vanilla` et transmettez les données via les props.
- **React Native** – Fonctionne prêt à l'emploi. Utilisez le middleware `persist` avec `AsyncStorage` via `@react-native-async-storage/async-storage`.

## Comparaison avec d'autres solutions

| Fonctionnalité | Zustand | Redux Toolkit | React Context |
|---------|---------|---------------|---------------|
| **Code rébarbatif** | Minimal (un seul appel create) | Moyen (slice, actions, reducer, configureStore) | Faible (Provider + context) |
| **Provider requis** | Non | Oui (wrapper Provider) | Oui (Context.Provider) |
| **Taille du bundle** | ~1 Ko gzippé | ~12 Ko gzippé | 0 (intégré) |
| **Contrôle des re‑rendus** | Basé sur les sélecteurs (égalité stricte) | Basé sur les sélecteurs (reselect) | Pas de mémoïsation intégrée ; les composants se re‑rendent à chaque changement de valeur du contexte |
| **Écosystème de middlewares** | Intégré : persist, immer, devtools, subscribeWithSelector | Étendu (sagas, thunks, etc.) | N/A |
| **Utilisation hors de React** | Oui (store vanilla) | Non | Non |
| **Compatibilité TypeScript** | Très bonne (types inférés) | Bonne (orienté slice) | Bonne (types génériques) |

## Meilleures pratiques

1. **Gardez les stores petits et ciblés** – Créez des stores séparés pour différents domaines (auth, panier, UI) au lieu d'un store géant unique.
2. **Utilisez des sélecteurs partout** – Passez toujours un sélecteur au hook ; évitez de vous abonner à l'intégralité du store.
3. **Préférez les setters à la mutation directe** – Même en utilisant le middleware Immer, conservez la logique dans `set` pour maintenir la traçabilité.
4. **Tirez parti des middlewares** – Utilisez `persist` pour l'état qui doit survivre aux rechargements de page, `devtools` pendant le développement et `immer` pour les mises à jour imbriquées complexes.
5. **Ne mélangez pas état serveur et état client** – Laissez React Query gérer les données d'API ; utilisez Zustand uniquement pour l'état UI/périphérique et les caches côté client.
6. **Testez avec les API vanilla** – Le store peut être testé sans aucun rendu React, simplement en appelant `getState` et `setState`.

## Pièges courants

- **Omettre le sélecteur** – Provoque le re‑rendu du composant à chaque changement d'état, annulant les avantages en termes de performances de la bibliothèque.
- **Muter l'état directement** – Utilisez toujours `set` ou une fonction de mutation contrôlée ; une assignation directe à `store.state` ne déclenchera pas d'abonnement.
- **Utiliser le même store pour l'état serveur et client** – Conduit à des données obsolètes et à une complexité inutile ; utilisez des outils dédiés pour la récupération de données.
- **Oublier de se désabonner** – La méthode vanilla `subscribe` retourne une fonction de désabonnement ; appelez-la lorsque l'abonnement n'est plus nécessaire pour éviter les fuites mémoire.

## Conclusion

Zustand est devenu une solution de gestion d'état incontournable pour les applications React modernes en raison de sa simplicité, de sa faible empreinte et de ses excellentes performances. Il atteint un équilibre rare : il est assez simple pour un prototype mais assez puissant pour des applications à l'échelle de la production. Sa conception sans Provider et sa consommation basée sur les hooks s'alignent parfaitement avec les fonctionnalités concurrentes de React 18, et son noyau vanilla le rend utilisable dans n'importe quel contexte JavaScript.

Que vous migriez depuis Redux, remplaciez React Context ou construisiez un nouveau projet à partir de zéro, Zustand offre une expérience de développement propre, efficace et agréable.

---

*Pour plus d'informations, visitez le [dépôt officiel](https://github.com/pmndrs/zustand) ou le [site de documentation](https://docs.pmnd.rs/zustand).*