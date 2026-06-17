---
title: Zustand — Gestión de Estado Minimalista para React
description: Una guía completa de Zustand, una biblioteca ligera de gestión de estado basada en hooks para React y JavaScript vanilla, incluyendo instalación, conceptos clave, middleware y patrones avanzados.
created: 2026-06-15
tags:
  - analysis
  - state-management
  - react
  - javascript
  - library-study
status: draft
---

# Zustand — Gestión de Estado Minimalista para React

## Overview

**Zustand** (en alemán, “estado”) es una biblioteca de gestión de estado ligera, rápida y escalable para React y JavaScript vanilla. Creada por Paul Henschel y el colectivo Poimandres (el mismo grupo detrás de React Three Fiber, Jotai y React Spring), Zustand ofrece una API pequeña ( ~1 KB comprimido) con cero código repetitivo, sin proveedores envolventes y un modelo de consumo centrado en hooks.

A diferencia de Redux o MobX, Zustand no impone patrones arquitectónicos, tipos de acción, reductores o despachadores. En su lugar, trata el estado como un objeto simple que puede leerse y modificarse mediante funciones sencillas, todo mientras aprovecha `useSyncExternalStore` de React 18 para un renderizado concurrente seguro.

## ¿Por qué Zustand?

- **Sin proveedor** – Los componentes se suscriben directamente al store; sin anidamiento de `<Provider>`.
- **Basado en selectores** – Los componentes se re-renderizan solo cuando la porción elegida cambia (usando `===` estricto por defecto).
- **Paquete pequeño** – ~1 KB comprimido, lo que lo hace adecuado para aplicaciones críticas en rendimiento.
- **Núcleo independiente del framework** – El store puede usarse fuera de React (por ejemplo, en SSR con Next.js, scripts de Node.js o Web Workers).
- **Middlewares ricos** – Complementos oficiales para persistencia (`persist`), actualizaciones mutables estilo Immer (`immer`), Redux DevTools (`devtools`) y suscripciones basadas en selectores (`subscribeWithSelector`).

## Instalación

```bash
npm install zustand
# or
yarn add zustand
```

Zustand es completamente tree-shakable y está escrito en TypeScript; los tipos se incluyen por defecto.

## Uso Básico

### Creando un Store

`create` acepta una función que recibe `set`, `get` y `storeAPI` como argumentos. La función devuelve un objeto que contiene el estado y cualquier acción.

```javascript
import { create } from 'zustand';

const useBearStore = create((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
  decrease: (by) => set((state) => ({ bears: state.bears - by })),
  reset: () => set({ bears: 0 }),
}));
```

### Usando el Store en un Componente

Llama al hook del store con un **selector** que devuelva la parte del estado que necesitas. El componente solo se re-renderizará cuando el valor seleccionado cambie.

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

### Accediendo y Suscribiéndose Fuera de React

El store puede usarse en JavaScript simple sin ninguna dependencia de React:

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

## Características Clave

### 1. Arquitectura sin Proveedor

Los stores de Zustand son objetos independientes. No hay un envoltorio `<BearProvider>`, lo que significa que no hay anidamiento de proveedores, no hay re-renderizados accidentales de subárboles completos y un modelo mental más simple. El store simplemente se importa y se usa en cualquier componente.

### 2. Suscripciones Basadas en Selectores (Rendimiento por Defecto)

La función selectora recibe el estado completo y devuelve solo los valores que el componente necesita. Zustand rastrea internamente los selectores y solo provoca re-renderizados cuando el valor devuelto cambia (igualdad de referencia). Para comparaciones profundas, puedes pasar una función de igualdad personalizada como segundo argumento al hook.

```javascript
const userName = useUserStore(
  (state) => state.user.name,
  (oldName, newName) => oldName === newName  // deep equal
);
```

Si no se proporciona un selector, el componente se suscribe al **store completo**—mejor evitarlo para stores grandes.

### 3. Código Repetitivo Mínimo

Un store completo se crea en una sola llamada a `create`. Las acciones son simplemente funciones que llaman a `set`, y pueden ser anidadas, asíncronas o exportadas de forma independiente.

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

### 4. Sistema de Middleware

Zustand proporciona middleware oficial que envuelve el creador del store para añadir capacidades.

#### Middleware de Persistencia

Sincroniza automáticamente el estado con un backend de almacenamiento (localStorage, AsyncStorage, IndexedDB, etc.).

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

#### Middleware de Immer

Escribe actualizaciones de estado de manera mutable usando borradores de Immer.

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

#### Middleware de DevTools

Integra con la extensión de navegador Redux DevTools para depuración.

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

#### Middleware de subscribeWithSelector

Permite suscripciones detalladas con selectores, similar a la API del hook, pero fuera de React.

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

### 5. Uso con JavaScript Vanilla (No React)

La lógica central de gestión de estado de Zustand es completamente independiente de React. Puedes crear stores sin ninguna dependencia de React, lo que es útil en scripts de Node, Web Workers o cualquier entorno no React.

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

Para integrar el store vanilla en React, puedes envolverlo con `useStore`:

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

### 6. Múltiples Stores (Patrón de Slices)

Zustand fomenta la composición de stores independientes en lugar de un único store monolítico. También puedes combinar múltiples slices en un solo store usando el **patrón de slices** o simplemente llamando a `create` varias veces.

#### Stores separados

```javascript
// store/authStore.js
export const useAuthStore = create(/* ... */);

// store/cartStore.js
export const useCartStore = create(/* ... */);

// Component
import { useAuthStore } from './store/authStore';
import { useCartStore } from './store/cartStore';
```

#### Patrón de slices (un solo store a partir de múltiples slices)

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

### 7. Integración con Otras Bibliotecas

- **React Query / SWR** – Zustand **no** debe reemplazar el almacenamiento en caché del estado del servidor. Usa bibliotecas dedicadas para datos de API y Zustand para el estado de UI / cliente.
- **Next.js** – Los stores de Zustand pueden crearse y consumirse dentro de componentes cliente. Para componentes servidor, usa `createStore` de `zustand/vanilla` y pasa datos como props.
- **React Native** – Funciona sin configuración adicional. Usa el middleware `persist` con `AsyncStorage` a través de `@react-native-async-storage/async-storage`.

## Comparación con Otras Soluciones

| Característica | Zustand | Redux Toolkit | React Context |
|---------|---------|---------------|---------------|
| **Código repetitivo** | Mínimo (una llamada a create) | Medio (slice, acciones, reducer, configureStore) | Bajo (Provider + context) |
| **Proveedor requerido** | No | Sí (envoltorio Provider) | Sí (Context.Provider) |
| **Tamaño del paquete** | ~1 KB comprimido | ~12 KB comprimido | 0 (incluido) |
| **Control de re-renderizado** | Basado en selectores (igualdad estricta) | Basado en selectores (reselect) | Sin memoización incorporada; los componentes se re-renderizan en cada cambio del valor del contexto |
| **Ecosistema de middleware** | Incorporados: persist, immer, devtools, subscribeWithSelector | Extenso (sagas, thunks, etc.) | N/A |
| **Uso fuera de React** | Sí (store vanilla) | No | No |
| **Compatibilidad con TypeScript** | Muy buena (tipos inferidos) | Buena (orientado a slices) | Buena (tipos genéricos) |

## Mejores Prácticas

1. Mantén los stores pequeños y enfocados – Crea stores separados para diferentes dominios (auth, carrito, UI) en lugar de un solo store gigante.
2. Usa selectores en todas partes – Siempre pasa un selector al hook; evita suscribirte al store completo.
3. Prefiere setters en lugar de mutación directa – Incluso al usar middleware Immer, mantén la lógica en `set` para mantener la trazabilidad.
4. Aprovecha el middleware – Usa `persist` para el estado que debe sobrevivir a recargas de página, `devtools` durante el desarrollo y `immer` para actualizaciones anidadas complejas.
5. No mezcles estado del servidor y del cliente – Deja que React Query maneje los datos de API; usa Zustand solo para estado de UI/dispositivo y cachés del lado del cliente.
6. Prueba con las APIs vanilla – El store puede probarse sin ningún renderizado de React, simplemente llamando a `getState` y `setState`.

## Errores Comunes

- **Omitir el selector** – Hace que el componente se re-renderice en cada cambio de estado, anulando los beneficios de rendimiento de la biblioteca.
- **Mut ar el estado directamente** – Siempre usa `set` o una función de mutación controlada; la asignación directa a `store.state` no activará suscripciones.
- **Usar el mismo store para estado del servidor y del cliente** – Lleva a datos obsoletos y complejidad innecesaria; usa herramientas dedicadas para la obtención de datos.
- **Olvidar cancelar la suscripción** – El método `subscribe` vanilla devuelve una función de cancelación; llámala cuando la suscripción ya no sea necesaria para evitar fugas de memoria.

## Conclusión

Zustand se ha convertido en una solución de gestión de estado de referencia para aplicaciones React modernas debido a su simplicidad, tamaño reducido y excelente rendimiento. Logra un equilibrio poco común: es lo suficientemente fácil para un prototipo, pero lo suficientemente potente para aplicaciones a escala de producción. Su diseño sin proveedor y su consumo basado en hooks se alinean perfectamente con las características concurrentes de React 18, y su núcleo vanilla lo hace utilizable en cualquier contexto de JavaScript.

Ya sea que estés migrando desde Redux, reemplazando React Context o construyendo un nuevo proyecto desde cero, Zustand proporciona una experiencia de desarrollo limpia, eficiente y agradable.

---

*Para más información, visita el [repositorio oficial](https://github.com/pmndrs/zustand) o el [sitio de documentación](https://docs.pmnd.rs/zustand).*