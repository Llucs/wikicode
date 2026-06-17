---
title: Zustand — Gerenciamento de Estado Minimalista para React
description: Um guia abrangente sobre Zustand, uma biblioteca de gerenciamento de estado leve e baseada em hooks para React e JavaScript puro, incluindo instalação, conceitos principais, middleware e padrões avançados.
created: 2026-06-15
tags:
  - analysis
  - state-management
  - react
  - javascript
  - library-study
status: draft
---

# Zustand — Gerenciamento de Estado Minimalista para React

## Visão Geral

**Zustand** (alemão para “estado”) é uma biblioteca de gerenciamento de estado leve, rápida e escalável para React e JavaScript puro. Criado por Paul Henschel e pelo coletivo Poimandres (o mesmo grupo por trás de React Three Fiber, Jotai e React Spring), Zustand oferece uma API minúscula (~1 KB gzipado) com zero boilerplate, sem providers wrapper e um modelo de consumo centrado em hooks.

Ao contrário de Redux ou MobX, Zustand não impõe padrões arquiteturais, tipos de ação, reducers ou dispatchers. Em vez disso, trata o estado como um objeto simples que pode ser lido e modificado através de funções simples — tudo isso enquanto aproveita o `useSyncExternalStore` do React 18 para renderização concorrente segura.

## Por que Zustand?

- **Sem Provider** – Componentes se inscrevem diretamente na store; sem aninhamento de `<Provider>`.
- **Baseado em Selector** – Componentes re-renderizam apenas quando a parte escolhida muda (usando `===` estrito por padrão).
- **Pequeno bundle** – ~1 KB gzipado, tornando-o adequado para aplicações críticas de performance.
- **Núcleo agnóstico de framework** – A store pode ser usada fora do React (ex.: em SSR com Next.js, scripts Node.js ou Web Workers).
- **Middleware rico** – Plugins oficiais para persistência (`persist`), atualizações mutáveis estilo Immer (`immer`), Redux DevTools (`devtools`) e assinaturas baseadas em selector (`subscribeWithSelector`).

## Instalação

```bash
npm install zustand
# or
yarn add zustand
```

Zustand é totalmente tree‑shakable e escrito em TypeScript; os tipos estão incluídos de fábrica.

## Uso Básico

### Criando uma Store

`create` aceita uma função que recebe `set`, `get` e `storeAPI` como argumentos. A função retorna um objeto contendo o estado e quaisquer ações.

```javascript
import { create } from 'zustand';

const useBearStore = create((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
  decrease: (by) => set((state) => ({ bears: state.bears - by })),
  reset: () => set({ bears: 0 }),
}));
```

### Usando a Store em um Componente

Chame o hook da store com um **selector** que retorne a parte do estado que você precisa. O componente só re-renderizará quando o valor selecionado mudar.

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

### Acessando e Assinando Fora do React

A store pode ser usada em JavaScript puro sem qualquer dependência do React:

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

## Principais Características

### 1. Arquitetura Sem Provider

As stores do Zustand são objetos independentes. Não há um wrapper `<BearProvider>`, o que significa sem aninhamento de provider, sem re-renderizações acidentais de subárvores inteiras e um modelo mental mais simples. A store é simplesmente importada e usada em qualquer componente.

### 2. Assinaturas Baseadas em Selector (Performance por Padrão)

A função selector recebe o estado inteiro e retorna apenas os valores que o componente precisa. Zustand rastreia internamente os selectors e só aciona re-renderizações quando o valor retornado muda (igualdade de referência). Para comparações profundas, você pode passar uma função de igualdade personalizada como segundo argumento para o hook.

```javascript
const userName = useUserStore(
  (state) => state.user.name,
  (oldName, newName) => oldName === newName  // deep equal
);
```

Se nenhum selector for fornecido, o componente se inscreve na store **inteira** — é melhor evitar para stores grandes.

### 3. Boilerplate Mínimo

Uma store completa é criada em uma única chamada `create`. Ações são simplesmente funções que chamam `set`, e podem ser aninhadas, assíncronas ou exportadas independentemente.

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

Zustand fornece middleware oficial que envolve o criador da store para adicionar capacidades.

#### Persist Middleware

Sincroniza automaticamente o estado com um backend de armazenamento (localStorage, AsyncStorage, IndexedDB, etc.).

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

Escreva atualizações de estado de forma mutável usando rascunhos do Immer.

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

Integre-se com a extensão do navegador Redux DevTools para depuração.

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

Permite assinaturas granulares com selectors, semelhante à API de hooks, mas fora do React.

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

### 5. Uso com JavaScript Puro (Não‑React)

A lógica central de gerenciamento de estado do Zustand é completamente independente do React. Você pode criar stores sem qualquer dependência do React, o que é útil em scripts Node, Web Workers ou qualquer ambiente não‑React.

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

Para integrar a store vanilla no React, você pode envolvê-la com `useStore`:

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

### 6. Múltiplas Stores (Padrão de Slices)

Zustand incentiva a composição de stores independentes em vez de uma única store monolítica. Você também pode combinar vários slices em uma única store usando o **padrão de slices** ou simplesmente chamando `create` várias vezes.

#### Stores Separadas

```javascript
// store/authStore.js
export const useAuthStore = create(/* ... */);

// store/cartStore.js
export const useCartStore = create(/* ... */);

// Component
import { useAuthStore } from './store/authStore';
import { useCartStore } from './store/cartStore';
```

#### Padrão de Slices (Store Única a Partir de Múltiplos Slices)

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

### 7. Integração com Outras Bibliotecas

- **React Query / SWR** – Zustand **não** deve substituir o cache de estado do servidor. Use bibliotecas dedicadas para dados de API e Zustand para estado de UI / cliente.
- **Next.js** – Stores do Zustand podem ser criadas e consumidas dentro de componentes cliente. Para componentes servidor, use `createStore` de `zustand/vanilla` e passe dados como props.
- **React Native** – Funciona imediatamente. Use o middleware `persist` com `AsyncStorage` através de `@react-native-async-storage/async-storage`.

## Comparação com Outras Soluções

| Característica | Zustand | Redux Toolkit | React Context |
|---------|---------|---------------|---------------|
| **Boilerplate** | Mínimo (uma chamada create) | Médio (slice, actions, reducer, configureStore) | Baixo (Provider + contexto) |
| **Provider necessário** | Não | Sim (wrapper Provider) | Sim (Context.Provider) |
| **Tamanho do bundle** | ~1 KB gzipado | ~12 KB gzipado | 0 (integrado) |
| **Controle de re‑render** | Baseado em selector (igualdade estrita) | Baseado em selector (reselect) | Sem memoização integrada; componentes re-renderizam a cada mudança de valor do contexto |
| **Ecossistema de middleware** | Integrado: persist, immer, devtools, subscribeWithSelector | Extensivo (sagas, thunks, etc.) | N/A |
| **Uso fora do React** | Sim (store vanilla) | Não | Não |
| **Amigabilidade com TypeScript** | Muito bom (tipos inferidos) | Bom (orientado a slices) | Bom (tipos genéricos) |

## Melhores Práticas

1. **Mantenha as stores pequenas e focadas** – Crie stores separadas para diferentes domínios (auth, carrinho, UI) em vez de uma store gigante.
2. **Use selectors em toda parte** – Sempre passe um selector para o hook; evite se inscrever na store inteira.
3. **Prefira setters em vez de mutação direta** – Mesmo ao usar o middleware Immer, mantenha a lógica em `set` para manter a rastreabilidade.
4. **Aproveite o middleware** – Use `persist` para estado que precisa sobreviver a recarregamentos de página, `devtools` durante o desenvolvimento e `immer` para atualizações aninhadas complexas.
5. **Não misture estado de servidor e cliente** – Deixe o React Query lidar com dados de API; use Zustand apenas para estado de UI/dispositivo e caches do lado do cliente.
6. **Teste com APIs vanilla** – A store pode ser testada sem qualquer renderização do React, simplesmente chamando `getState` e `setState`.

## Armadilhas Comuns

- **Omitir o selector** – Faz com que o componente re-renderize a cada mudança de estado, anulando os benefícios de performance da biblioteca.
- **Mutação direta do estado** – Sempre use `set` ou uma função de mutação controlada; a atribuição direta a `store.state` não acionará assinaturas.
- **Usar a mesma store para estado de servidor e cliente** – Leva a dados obsoletos e complexidade desnecessária; use ferramentas dedicadas para busca de dados.
- **Esquecer de cancelar a assinatura** – O método `subscribe` do vanilla retorna uma função de cancelamento; chame-a quando a assinatura não for mais necessária para evitar vazamentos de memória.

## Conclusão

Zustand se tornou uma solução de gerenciamento de estado de referência para aplicações React modernas por sua simplicidade, tamanho reduzido e excelente performance. Ele atinge um equilíbrio raro: é fácil o suficiente para um protótipo, mas poderoso o suficiente para aplicações em escala de produção. Seu design sem provider e consumo baseado em hooks se alinham perfeitamente com os recursos concorrentes do React 18, e seu núcleo vanilla o torna utilizável em qualquer contexto JavaScript.

Se você está migrando do Redux, substituindo o React Context ou construindo um novo projeto do zero, Zustand proporciona uma experiência de desenvolvimento limpa, eficiente e agradável.

---

*Para mais informações, visite o [repositório oficial](https://github.com/pmndrs/zustand) ou o [site de documentação](https://docs.pmnd.rs/zustand).*