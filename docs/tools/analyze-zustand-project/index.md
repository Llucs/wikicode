---
title: Zustand — Minimalistic State Management for React
description: A comprehensive guide to Zustand, a lightweight, hook-based state management library for React and vanilla JavaScript, including installation, core concepts, middleware, and advanced patterns.
created: 2026-06-15
tags:
  - state-management
  - react
  - javascript
  - hooks
  - zustand
  - pmndrs
status: draft
---

# Zustand — Minimalistic State Management for React

## Overview

**Zustand** (German for “state”) is a lightweight, fast, and scalable state management library for React and vanilla JavaScript. Created by Paul Henschel and the Poimandres collective (the same group behind React Three Fiber, Jotai, and React Spring), Zustand offers a tiny API ( ~1 KB gzipped) with zero boilerplate, no wrapper providers, and a hook-centric consumption model.

Unlike Redux or MobX, Zustand does not impose architectural patterns, action types, reducers, or dispatchers. Instead, it treats state as a plain object that can be read and mutated via simple functions—all while leveraging React 18’s `useSyncExternalStore` for safe concurrent rendering.

## Why Zustand?

- **Provider‑less** – Components subscribe directly to the store; no `<Provider>` nesting.
- **Selector‑based** – Components re‑render only when their chosen slice changes (using strict `===` by default).
- **Small bundle** – ~1 KB gzipped, making it suitable for performance‑critical apps.
- **Framework‑agnostic core** – The store can be used outside React (e.g., in Next.js SSR, Node.js scripts, or Web Workers).
- **Rich middleware** – Official plugins for persistence (`persist`), Immer‑style mutable updates (`immer`), Redux DevTools (`devtools`), and selector‑based subscriptions (`subscribeWithSelector`).

## Installation

```bash
npm install zustand
# or
yarn add zustand
```

Zustand is fully tree‑shakable and written in TypeScript; types are included out of the box.

## Basic Usage

### Creating a Store

`create` accepts a function that takes `set`, `get`, and `storeAPI` as arguments. The function returns an object containing the state and any actions.

```javascript
import { create } from 'zustand';

const useBearStore = create((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
  decrease: (by) => set((state) => ({ bears: state.bears - by })),
  reset: () => set({ bears: 0 }),
}));
```

### Using the Store in a Component

Call the store hook with a **selector** that returns the piece of state you need. The component will only re‑render when the selected value changes.

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

### Accessing & Subscribing Outside React

The store can be used in plain JavaScript without any React dependency:

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

## Key Features

### 1. Provider‑less Architecture

Zustand stores are standalone objects. There is no `<BearProvider>` wrapper, which means no provider nesting, no accidental re‑renders of entire subtrees, and a simpler mental model. The store is simply imported and used in any component.

### 2. Selector‑Based Subscriptions (Performance by Default)

The selector function receives the entire state and returns only the values the component needs. Zustand internally tracks selectors and only triggers re‑renders when the returned value changes (reference equality). For deep comparisons, you can pass a custom equality function as a second argument to the hook.

```javascript
const userName = useUserStore(
  (state) => state.user.name,
  (oldName, newName) => oldName === newName  // deep equal
);
```

If no selector is given, the component subscribes to the **entire** store—best avoided for large stores.

### 3. Minimal Boilerplate

A complete store is created in a single `create` call. Actions are simply functions that call `set`, and can be nested, async, or exported independently.

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

### 4. Middleware System

Zustand provides official middleware that wrap the store creator to add capabilities.

#### Persist Middleware

Automatically syncs state to a storage backend (localStorage, AsyncStorage, IndexedDB, etc.).

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

#### Immer Middleware

Write state updates in a mutable fashion using Immer drafts.

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

#### DevTools Middleware

Integrate with the Redux DevTools browser extension for debugging.

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

#### subscribeWithSelector Middleware

Enables fine‑grained subscriptions with selectors, similar to the hook API, but outside React.

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

### 5. Vanilla JavaScript (Non‑React) Usage

Zustand’s core state management logic is completely independent of React. You can create stores without any React dependency, which is useful in Node scripts, Web Workers, or any non‑React environment.

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

To integrate the vanilla store into React, you can wrap it with `useStore`:

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

### 6. Multiple Stores (Slices Pattern)

Zustand encourages composing independent stores rather than a single monolithic store. You can also combine multiple slices into one store using the **slices pattern** or simply by calling `create` multiple times.

#### Separate stores

```javascript
// store/authStore.js
export const useAuthStore = create(/* ... */);

// store/cartStore.js
export const useCartStore = create(/* ... */);

// Component
import { useAuthStore } from './store/authStore';
import { useCartStore } from './store/cartStore';
```

#### Slices pattern (single store from multiple slices)

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

### 7. Integration with Other Libraries

- **React Query / SWR** – Zustand should **not** replace server‑state caching. Use dedicated libraries for API data and Zustand for UI / client‑side state.
- **Next.js** – Zustand stores can be created and consumed inside client components. For server components, use `createStore` from `zustand/vanilla` and pass data as props.
- **React Native** – Works out of the box. Use `persist` middleware with `AsyncStorage` via `@react-native-async-storage/async-storage`.

## Comparison with Other Solutions

| Feature | Zustand | Redux Toolkit | React Context |
|---------|---------|---------------|---------------|
| **Boilerplate** | Minimal (one create call) | Medium (slice, actions, reducer, configureStore) | Low (Provider + context) |
| **Provider required** | No | Yes (Provider wrapper) | Yes (Context.Provider) |
| **Bundle size** | ~1 KB gzipped | ~12 KB gzipped | 0 (built‑in) |
| **Re‑render control** | Selector‑based (strict equality) | Selector‑based (reselect) | No built‑in memoization; components re‑render on every context value change |
| **Middleware ecosystem** | Built‑in: persist, immer, devtools, subscribeWithSelector | Extensive (sagas, thunks, etc.) | N/A |
| **Use outside React** | Yes (vanilla store) | No | No |
| **TypeScript friendliness** | Very good (inferred types) | Good (slice‑oriented) | Good (generic types) |

## Best Practices

1. **Keep stores small and focused** – Create separate stores for different domains (auth, cart, UI) instead of one giant store.
2. **Use selectors everywhere** – Always pass a selector to the hook; avoid subscribing to the entire store.
3. **Prefer setters over direct mutation** – Even when using Immer middleware, keep the logic in `set` to maintain traceability.
4. **Leverage middleware** – Use `persist` for state that needs to survive page reloads, `devtools` during development, and `immer` for complex nested updates.
5. **Don’t mix server and client state** – Let React Query handle API data; use Zustand only for UI/device state and client‑side caches.
6. **Test with vanilla APIs** – The store can be tested without any React rendering, simply by calling `getState` and `setState`.

## Common Pitfalls

- **Omitting the selector** – Causes the component to re‑render on every state change, defeating the library’s performance benefits.
- **Mutating state directly** – Always use `set` or a controlled mutation function; direct assignment to `store.state` will not trigger subscriptions.
- **Using the same store for server and client state** – Leads to stale data and unnecessary complexity; use dedicated tools for data fetching.
- **Forgetting to unsubscribe** – The vanilla `subscribe` method returns an unsubscribe function; call it when the subscription is no longer needed to avoid memory leaks.

## Conclusion

Zustand has become a go‑to state management solution for modern React applications because of its simplicity, small footprint, and excellent performance. It strikes a rare balance: it is easy enough for a prototype but powerful enough for production‑scale applications. Its provider‑less design and hook‑based consumption align perfectly with React 18’s concurrent features, and its vanilla core makes it usable in any JavaScript context.

Whether you are migrating from Redux, replacing React Context, or building a new project from scratch, Zustand provides a clean, efficient, and delightful developer experience.

---

*For more information, visit the [official repository](https://github.com/pmndrs/zustand) or the [documentation site](https://docs.pmnd.rs/zustand).*