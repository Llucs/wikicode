---
title: Zustand — 针对 React 的极简状态管理
description: 一份全面的 Zustand 指南，Zustand 是一个轻量级、基于 Hook 的状态管理库，适用于 React 和 vanilla JavaScript，涵盖安装、核心概念、中间件和高级模式。
created: 2026-06-15
tags:
  - analysis
  - state-management
  - react
  - javascript
  - library-study
status: draft
---

# Zustand — 针对 React 的极简状态管理

## 概述

**Zustand**（德语中意为“状态”）是一个轻量级、快速且可扩展的状态管理库，适用于 React 和 vanilla JavaScript。由 Paul Henschel 和 Poimandres 团队（也是 React Three Fiber、Jotai 和 React Spring 的团队）创建，Zustand 提供了极小的 API（gzip 后约 1 KB），零样板代码，无包装 Provider，以及以 Hook 为中心的使用模式。

与 Redux 或 MobX 不同，Zustand 不强加架构模式、Action 类型、Reducer 或 Dispatcher。相反，它将状态视为一个普通对象，可以通过简单的函数进行读取和修改——同时利用 React 18 的 `useSyncExternalStore` 实现安全的并发渲染。

## 为什么选择 Zustand？

- **无 Provider** – 组件直接订阅 store；无需 `<Provider>` 嵌套。
- **基于 Selector** – 组件仅在其选择的切片发生变化时重新渲染（默认使用严格 `===` 比较）。
- **小巧的打包体积** – gzip 后约 1 KB，适用于性能关键的应用程序。
- **框架无关的核心** – store 可以脱离 React 使用（例如在 Next.js SSR、Node.js 脚本或 Web Workers 中）。
- **丰富的中间件** – 官方插件支持持久化（`persist`）、Immer 风格的可变更新（`immer`）、Redux DevTools（`devtools`）以及基于 Selector 的订阅（`subscribeWithSelector`）。

## 安装

```bash
npm install zustand
# or
yarn add zustand
```

Zustand 完全支持 tree‑shaking，并使用 TypeScript 编写；类型开箱即用。

## 基本用法

### 创建 Store

`create` 接受一个函数，该函数接收 `set`、`get` 和 `storeAPI` 作为参数。该函数返回一个包含状态和任意 action 的对象。

```javascript
import { create } from 'zustand';

const useBearStore = create((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
  decrease: (by) => set((state) => ({ bears: state.bears - by })),
  reset: () => set({ bears: 0 }),
}));
```

### 在组件中使用 Store

将 store 的 Hook 与一个 **selector** 一起调用，该 selector 返回你需要的状态片段。组件仅在选择的值发生变化时才会重新渲染。

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

### 在 React 外部访问和订阅

store 可以在纯 JavaScript 中使用，无需任何 React 依赖：

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

## 关键特性

### 1. 无 Provider 架构

Zustand 的 store 是独立的对象。没有 `<BearProvider>` 包装器，这意味着没有 Provider 嵌套，没有整个子树意外重新渲染的问题，并且心智模型更简单。store 只需导入即可在任何组件中使用。

### 2. 基于 Selector 的订阅（默认即高性能）

selector 函数接收整个状态并仅返回组件所需的值。Zustand 在内部跟踪 selector，并且仅在返回值发生变化时触发重新渲染（引用相等性）。对于深度比较，你可以将自定义相等函数作为第二个参数传递给 Hook。

```javascript
const userName = useUserStore(
  (state) => state.user.name,
  (oldName, newName) => oldName === newName  // deep equal
);
```

如果没有提供 selector，组件将订阅**整个** store——对于大型 store 最好避免这样做。

### 3. 极少的样板代码

一个完整的 store 通过一次 `create` 调用即可创建。Action 只是调用 `set` 的函数，可以嵌套、异步或独立导出。

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

### 4. 中间件系统

Zustand 提供了官方的中间件，用于包装 store 创建者以添加功能。

#### Persist 中间件

自动将状态同步到存储后端（localStorage、AsyncStorage、IndexedDB 等）。

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

#### Immer 中间件

使用 Immer draft 以可变方式编写状态更新。

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

#### DevTools 中间件

与 Redux DevTools 浏览器扩展集成以进行调试。

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

#### subscribeWithSelector 中间件

启用基于 selector 的细粒度订阅，类似于 Hook API，但在 React 外部使用。

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

### 5. 在 Vanilla JavaScript（非 React）中使用

Zustand 的核心状态管理逻辑完全独立于 React。你可以在没有任何 React 依赖的情况下创建 store，这在 Node 脚本、Web Workers 或任何非 React 环境中非常有用。

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

要将 vanilla store 集成到 React 中，你可以使用 `useStore` 包裹它：

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

### 6. 多个 Store（Slices 模式）

Zustand 鼓励组合独立的 store，而不是单个庞大的 store。你还可以使用 **slices 模式**或直接多次调用 `create` 将多个 slice 合并到一个 store 中。

#### 独立的 Store

```javascript
// store/authStore.js
export const useAuthStore = create(/* ... */);

// store/cartStore.js
export const useCartStore = create(/* ... */);

// Component
import { useAuthStore } from './store/authStore';
import { useCartStore } from './store/cartStore';
```

#### Slices 模式（从多个 slice 合并为单个 store）

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

### 7. 与其他库的集成

- **React Query / SWR** – Zustand**不应**替换服务端状态缓存。请使用专用库处理 API 数据，使用 Zustand 处理 UI/客户端状态。
- **Next.js** – Zustand store 可以在客户端组件中创建和使用。对于服务端组件，请使用 `zustand/vanilla` 中的 `createStore`，并通过 props 传递数据。
- **React Native** – 开箱即用。通过 `@react-native-async-storage/async-storage` 将 `persist` 中间件与 `AsyncStorage` 结合使用。

## 与其他解决方案的对比

| 特性 | Zustand | Redux Toolkit | React Context |
|---------|---------|---------------|---------------|
| **样板代码** | 极少（一次 create 调用） | 中等（slice, actions, reducer, configureStore） | 低（Provider + context） |
| **需要 Provider** | 否 | 是（Provider 包装器） | 是（Context.Provider） |
| **打包体积** | ~1 KB（gzip 后） | ~12 KB（gzip 后） | 0（内置） |
| **重新渲染控制** | 基于 Selector（严格相等性） | 基于 Selector（reselect） | 无内置记忆化；组件在每次 context 值变化时重新渲染 |
| **中间件生态** | 内置：persist、immer、devtools、subscribeWithSelector | 丰富（sagas、thunks 等） | 不适用 |
| **在 React 外部使用** | 是（vanilla store） | 否 | 否 |
| **TypeScript 友好性** | 非常好（类型推断） | 良好（面向 slice） | 良好（泛型） |

## 最佳实践

1. **保持 store 小而专注** – 为不同的领域（认证、购物车、UI）创建独立的 store，而不是一个巨大的 store。
2. **处处使用 selector** – 始终将 selector 传递给 Hook；避免订阅整个 store。
3. **优先使用 setter 而非直接修改** – 即使使用 Immer 中间件，也将逻辑放在 `set` 中以保持可追溯性。
4. **利用中间件** – 对于需要在页面重新加载后存活的状态使用 `persist`，在开发期间使用 `devtools`，对于复杂的嵌套更新使用 `immer`。
5. **不要混用服务端和客户端状态** – 让 React Query 处理 API 数据；仅将 Zustand 用于 UI/设备状态和客户端缓存。
6. **使用 vanilla API 进行测试** – store 可以在没有任何 React 渲染的情况下进行测试，只需调用 `getState` 和 `setState` 即可。

## 常见陷阱

- **省略 selector** – 导致组件在每个状态变化时重新渲染，失去了库的性能优势。
- **直接修改状态** – 始终使用 `set` 或受控的修改函数；直接赋值给 `store.state` 不会触发订阅。
- **对服务端和客户端状态使用同一个 store** – 导致数据过时和不必要的复杂性；请使用专用工具进行数据获取。
- **忘记取消订阅** – vanilla 的 `subscribe` 方法返回一个取消订阅函数；在不再需要订阅时调用它以避免内存泄漏。

## 结论

Zustand 因其简单性、小巧的体量和出色的性能，已成为现代 React 应用程序的首选状态管理解决方案。它实现了罕见的平衡：对原型开发足够简单，对生产级应用又足够强大。其无 Provider 设计和基于 Hook 的使用模式与 React 18 的并发特性完美契合，而 vanilla 核心使其在任何 JavaScript 环境中都可用。

无论你是从 Redux 迁移、替换 React Context，还是从头开始构建新项目，Zustand 都能提供干净、高效且令人愉悦的开发体验。

---

*更多信息，请访问[官方仓库](https://github.com/pmndrs/zustand)或[文档站点](https://docs.pmnd.rs/zustand)。*