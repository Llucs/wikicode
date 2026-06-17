---
title: Zustand — Minimalistisches State-Management für React
description: Ein umfassender Leitfaden zu Zustand, einer leichten, Hook-basierten State-Management-Bibliothek für React und Vanilla JavaScript, einschließlich Installation, Kernkonzepte, Middleware und fortgeschrittener Muster.
created: 2026-06-15
tags:
  - analysis
  - state-management
  - react
  - javascript
  - library-study
status: draft
---

# Zustand — Minimalistisches State-Management für React

## Übersicht

**Zustand** (Deutsch für „Zustand“) ist eine leichte, schnelle und skalierbare State-Management-Bibliothek für React und Vanilla JavaScript. Entwickelt von Paul Henschel und dem Poimandres-Kollektiv (derselben Gruppe hinter React Three Fiber, Jotai und React Spring), bietet Zustand eine winzige API (~1 KB gzipped) mit keinem Boilerplate, keinen Wrapper-Providern und einem hook-zentrierten Konsummodell.

Im Gegensatz zu Redux oder MobX erzwingt Zustand keine Architekturmuster, Aktionstypen, Reducer oder Dispatcher. Stattdessen behandelt es den Zustand als ein einfaches Objekt, das über einfache Funktionen gelesen und verändert werden kann – und das alles unter Nutzung von React 18s `useSyncExternalStore` für sicheres gleichzeitiges Rendern.

## Warum Zustand?

- **Provider-los** – Komponenten abonnieren direkt den Store; kein `<Provider>`-Verschachteln.
- **Selektor-basiert** – Komponenten rendern nur neu, wenn sich ihr ausgewählter Ausschnitt ändert (standardmäßig mit striktem `===`).
- **Kleines Bundle** – ~1 KB gzipped, geeignet für leistungskritische Apps.
- **Framework-agnostischer Kern** – Der Store kann außerhalb von React verwendet werden (z. B. in Next.js SSR, Node.js-Skripten oder Web Workern).
- **Reichhaltige Middleware** – Offizielle Plugins für Persistenz (`persist`), Immer-artige mutable Updates (`immer`), Redux DevTools (`devtools`) und selektor-basierte Abonnements (`subscribeWithSelector`).

## Installation

```bash
npm install zustand
# or
yarn add zustand
```

Zustand is fully tree‑shakable and written in TypeScript; types are included out of the box.

## Grundlegende Verwendung

### Erstellen eines Stores

`create` akzeptiert eine Funktion, die `set`, `get` und `storeAPI` als Argumente erhält. Die Funktion gibt ein Objekt zurück, das den Zustand und alle Aktionen enthält.

```javascript
import { create } from 'zustand';

const useBearStore = create((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
  decrease: (by) => set((state) => ({ bears: state.bears - by })),
  reset: () => set({ bears: 0 }),
}));
```

### Verwenden des Stores in einer Komponente

Rufen Sie den Store-Hook mit einem **Selektor** auf, der das benötigte Stück Zustand zurückgibt. Die Komponente wird nur neu gerendert, wenn sich der ausgewählte Wert ändert.

```jsx
function BearCounter() {
  const bears = useBearStore((state) => state.bears);
  const increase = useBearStore((state) => state.increase);

  return (
    <div>
      <h1>{bears} bears</h1>
      <button onClick={() => increase(1)}>Add a bear</button>
    </div>
  );
}
```

### Zugreifen und Abonnieren außerhalb von React

Der Store kann in einfachem JavaScript ohne jede React-Abhängigkeit verwendet werden:

```javascript
// Read current state (without subscribing)
const current = useBearStore.getState();
console.log(current.bears); // 0

// Subscribe to changes
const unsub = useBearStore.subscribe((state) => {
  console.log('State changed:', state.bears);
});

// Trigger an action from outside React
useBearStore.getState().increase(2);

// Unsubscribe when needed
unsub();
```

## Schlüsselfunktionen

### 1. Provider-lose Architektur

Zustand-Stores sind eigenständige Objekte. Es gibt keinen `<BearProvider>`-Wrapper, was bedeutet: kein Verschachteln von Providern, keine versehentlichen Neu-Renderings ganzer Teilbäume und ein einfacheres mentales Modell. Der Store wird einfach importiert und in jeder Komponente verwendet.

### 2. Selektor-basierte Abonnements (Standardmäßig leistungsstark)

Die Selektorfunktion erhält den gesamten Zustand und gibt nur die Werte zurück, die die Komponente benötigt. Zustand verfolgt intern Selektoren und löst nur dann Neu-Renderings aus, wenn sich der zurückgegebene Wert ändert (Referenzgleichheit). Für tiefe Vergleiche können Sie eine benutzerdefinierte Gleichheitsfunktion als zweites Argument an den Hook übergeben.

```javascript
const userName = useUserStore(
  (state) => state.user.name,
  (oldName, newName) => oldName === newName  // deep equal
);
```

Wenn kein Selektor angegeben wird, abonniert die Komponente den **gesamten** Store – dies sollte bei großen Stores vermieden werden.

### 3. Minimaler Boilerplate

Ein kompletter Store wird in einem einzigen `create`-Aufruf erstellt. Aktionen sind einfach Funktionen, die `set` aufrufen, und können verschachtelt, asynchron oder unabhängig exportiert werden.

```javascript
const useAuthStore = create((set, get) => ({
  user: null,
  login: async (credentials) => {
    const user = await api.login(credentials);
    set({ user });
  },
  logout: () => set({ user: null }),
  hasRole: (role) => get().user?.role === role,  // synchronous getter
}));
```

### 4. Middleware-System

Zustand bietet offizielle Middleware, die den Store-Ersteller umschließen, um Fähigkeiten hinzuzufügen.

#### Persist-Middleware

Synchronisiert automatisch den Zustand mit einem Storage-Backend (localStorage, AsyncStorage, IndexedDB usw.).

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
      name: 'app-settings', // storage key
      storage: localStorage, // default is localStorage; can be AsyncStorage
    }
  )
);
```

#### Immer-Middleware

Schreiben Sie Zustandsaktualisierungen auf mutable Weise mit Immer-Entwürfen.

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

#### DevTools-Middleware

Integrieren Sie die Redux DevTools-Browsererweiterung zum Debuggen.

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
    { name: 'TodoStore' } // optional store name in DevTools
  )
);
```

#### subscribeWithSelector-Middleware

Ermöglicht feingranulare Abonnements mit Selektoren, ähnlich der Hook-API, aber außerhalb von React.

```javascript
import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';

const useCounterStore = create(
  subscribeWithSelector(() => ({
    count: 0,
    increment: () => set((state) => ({ count: state.count + 1 })),
  }))
);

// Subscribe to a selector (only fires when count changes)
const unsub = useCounterStore.subscribe(
  (state) => state.count,
  (newCount) => console.log('Count is now', newCount)
);
```

### 5. Vanilla JavaScript (Nicht-React) Verwendung

Die Kernlogik des Zustandsmanagements von Zustand ist vollständig unabhängig von React. Sie können Stores ohne jede React-Abhängigkeit erstellen, was in Node-Skripten, Web Workern oder jeder Nicht-React-Umgebung nützlich ist.

```javascript
import { createStore } from 'zustand/vanilla';

const counterStore = createStore((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}));

// Subscribe using store.subscribe
counterStore.subscribe(console.log);
counterStore.getState().increment(); // logs { count: 1 }
```

Um den Vanilla-Store in React zu integrieren, können Sie ihn mit `useStore` umschließen:

```javascript
import { useStore } from 'zustand';
import { createStore } from 'zustand/vanilla';
import { persist } from 'zustand/middleware'; // middleware also works with vanilla

const vanillaStore = createStore(persist(/* ... */));

function MyComponent() {
  const count = useStore(vanillaStore, (s) => s.count);
  const inc = useStore(vanillaStore, (s) => s.increment);
  // ...
}
```

### 6. Mehrere Stores (Slices-Pattern)

Zustand fördert die Zusammensetzung unabhängiger Stores anstelle eines einzigen monolithischen Stores. Sie können auch mehrere Slices mit dem **Slices-Pattern** in einem Store kombinieren oder einfach `create` mehrmals aufrufen.

#### Separate Stores

```javascript
// store/authStore.js
export const useAuthStore = create(/* ... */);

// store/cartStore.js
export const useCartStore = create(/* ... */);

// Component
import { useAuthStore } from './store/authStore';
import { useCartStore } from './store/cartStore';
```

#### Slices-Pattern (einzelner Store aus mehreren Slices)

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

### 7. Integration mit anderen Bibliotheken

- **React Query / SWR** – Zustand sollte **nicht** das Caching von Server-Zustand ersetzen. Verwenden Sie dedizierte Bibliotheken für API-Daten und Zustand für UI / clientseitigen Zustand.
- **Next.js** – Zustand-Stores können innerhalb von Client-Komponenten erstellt und verwendet werden. Für Server-Komponenten verwenden Sie `createStore` aus `zustand/vanilla` und übergeben Daten als Props.
- **React Native** – Funktioniert sofort. Verwenden Sie die `persist`-Middleware mit `AsyncStorage` über `@react-native-async-storage/async-storage`.

## Vergleich mit anderen Lösungen

| Merkmal | Zustand | Redux Toolkit | React Context |
|---------|---------|---------------|---------------|
| **Boilerplate** | Minimal (ein create-Aufruf) | Mittel (Slice, Actions, Reducer, configureStore) | Gering (Provider + Context) |
| **Provider erforderlich** | Nein | Ja (Provider-Wrapper) | Ja (Context.Provider) |
| **Bundlegröße** | ~1 KB gzipped | ~12 KB gzipped | 0 (eingebaut) |
| **Neu-Rendering-Kontrolle** | Selektor-basiert (strikte Gleichheit) | Selektor-basiert (reselect) | Keine eingebaute Memoisierung; Komponenten rendern bei jeder Context-Wertänderung neu |
| **Middleware-Ökosystem** | Eingebaut: persist, immer, devtools, subscribeWithSelector | Umfangreich (Sagas, Thunks usw.) | Nicht zutreffend |
| **Verwendung außerhalb von React** | Ja (Vanilla Store) | Nein | Nein |
| **TypeScript-Freundlichkeit** | Sehr gut (inferierte Typen) | Gut (Slice-orientiert) | Gut (generische Typen) |

## Best Practices

1. **Halten Sie Stores klein und fokussiert** – Erstellen Sie separate Stores für verschiedene Domänen (Auth, Warenkorb, UI) anstelle eines riesigen Stores.
2. **Verwenden Sie überall Selektoren** – Übergeben Sie immer einen Selektor an den Hook; vermeiden Sie das Abonnieren des gesamten Stores.
3. **Bevorzugen Sie Setter gegenüber direkter Mutation** – Auch bei Verwendung der Immer-Middleware, behalten Sie die Logik in `set` bei, um die Nachvollziehbarkeit zu erhalten.
4. **Nutzen Sie Middleware** – Verwenden Sie `persist` für Zustand, der Seitenneuladungen überstehen muss, `devtools` während der Entwicklung und `immer` für komplexe verschachtelte Updates.
5. **Mischen Sie nicht Server- und Client-Zustand** – Lassen Sie React Query API-Daten verwalten; verwenden Sie Zustand nur für UI/Gerätezustand und clientseitige Caches.
6. **Testen Sie mit Vanilla-APIs** – Der Store kann ohne React-Rendering getestet werden, einfach durch Aufruf von `getState` und `setState`.

## Häufige Fallstricke

- **Weglassen des Selektors** – Führt dazu, dass die Komponente bei jeder Zustandsänderung neu rendert, was die Leistungsvorteile der Bibliothek zunichte macht.
- **Direktes Mutieren des Zustands** – Verwenden Sie immer `set` oder eine kontrollierte Mutationsfunktion; direkte Zuweisung zu `store.state` löst keine Abonnements aus.
- **Verwendung desselben Stores für Server- und Client-Zustand** – Führt zu veralteten Daten und unnötiger Komplexität; verwenden Sie dedizierte Werkzeuge zum Datenabruf.
- **Vergessen, das Abonnement zu kündigen** – Die Vanilla-`subscribe`-Methode gibt eine Kündigungsfunktion zurück; rufen Sie diese auf, wenn das Abonnement nicht mehr benötigt wird, um Speicherlecks zu vermeiden.

## Fazit

Zustand ist zur bevorzugten State-Management-Lösung für moderne React-Anwendungen geworden, aufgrund seiner Einfachheit, geringen Größe und hervorragenden Leistung. Es schafft eine seltene Balance: Es ist einfach genug für einen Prototypen, aber leistungsstark genug für Produktionsanwendungen. Sein provider-loses Design und hook-basierte Nutzung passen perfekt zu den Concurrent Features von React 18, und sein Vanilla-Kern macht es in jedem JavaScript-Kontext verwendbar.

Egal, ob Sie von Redux migrieren, React Context ersetzen oder ein neues Projekt von Grund auf aufbauen, Zustand bietet eine saubere, effiziente und angenehme Entwicklererfahrung.

---

*Für weitere Informationen besuchen Sie das [offizielle Repository](https://github.com/pmndrs/zustand) oder die [Dokumentationsseite](https://docs.pmnd.rs/zustand).*