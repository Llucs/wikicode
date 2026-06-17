---
title: Zustand — ミニマルなReact向け状態管理
description: Zustand（ReactおよびバニラJavaScript向けの軽量フックベース状態管理ライブラリ）の包括的ガイド。インストール、基本概念、ミドルウェア、高度なパターンを解説します。
created: 2026-06-15
tags:
  - analysis
  - state-management
  - react
  - javascript
  - library-study
status: draft
---

# Zustand — ミニマルなReact向け状態管理

## 概要

**Zustand**（ドイツ語で「状態」）は、ReactおよびバニラJavaScript向けの軽量で高速かつスケーラブルな状態管理ライブラリです。Paul HenschelとPoimandresコレクティブ（React Three Fiber、Jotai、React Springと同じグループ）によって作られました。Zustandは、ゼロ・ボイラープレート、ラッパープロバイダなし、フック中心の消費モデルを備えた小さなAPI（ ~1 KB gzipped）を提供します。

ReduxやMobXとは異なり、Zustandはアーキテクチャパターン、アクションタイプ、レデューサー、ディスパッチャーを強制しません。代わりに、状態をプレーンなオブジェクトとして扱い、単純な関数で読み取りや変更を行えます。すべてはReact 18の`useSyncExternalStore`を活用して安全な並行レンダリングを実現しています。

## Zustandを選ぶ理由

- **プロバイダ不要** – コンポーネントはストアに直接購読します。`<Provider>`のネストは不要です。
- **セレクタベース** – コンポーネントは選択したスライスが変更されたときのみ再レンダリングされます（デフォルトでは厳密な`===`を使用）。
- **小さなバンドル** – 約1 KB gzippedで、パフォーマンスが重要なアプリに適しています。
- **フレームワーク非依存のコア** – ストアはReactの外部で使用可能です（例：Next.js SSR、Node.jsスクリプト、Web Worker）。
- **リッチなミドルウェア** – 公式プラグイン：永続化（`persist`）、Immerスタイルのミュータブル更新（`immer`）、Redux DevTools（`devtools`）、およびセレクタベースの購読（`subscribeWithSelector`）。

## インストール

```bash
npm install zustand
# or
yarn add zustand
```

Zustandは完全にツリーシェイカブルで、TypeScriptで書かれています。型はそのまま利用可能です。

## 基本的な使い方

### ストアの作成

`create`は`set`、`get`、`storeAPI`を引数に取る関数を受け取ります。関数は状態と任意のアクションを含むオブジェクトを返します。

```javascript
import { create } from 'zustand';

const useBearStore = create((set) => ({
  bears: 0,
  increase: (by) => set((state) => ({ bears: state.bears + by })),
  decrease: (by) => set((state) => ({ bears: state.bears - by })),
  reset: () => set({ bears: 0 }),
}));
```

### コンポーネントでのストアの使用

ストアフックを呼び出し、**セレクタ**で必要な状態の一部を返します。コンポーネントは選択された値が変更されたときのみ再レンダリングされます。

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

### React外でのアクセスと購読

ストアはReactに依存せずにプレーンなJavaScriptで使用できます：

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

## 主な機能

### 1. プロバイダ不要のアーキテクチャ

Zustandストアはスタンドアロンなオブジェクトです。`<BearProvider>`のようなラッパーはなく、プロバイダのネストやサブツリー全体の不必要な再レンダリングがなく、よりシンプルなメンタルモデルで扱えます。ストアは単にインポートして任意のコンポーネントで使用します。

### 2. セレクタベースの購読（デフォルトでパフォーマンス）

セレクタ関数は完全な状態を受け取り、コンポーネントが必要とする値のみを返します。Zustandは内部でセレクタを追跡し、返された値が変更されたときのみ再レンダリングをトリガーします（参照等価性）。深い比較を行うには、フックの第二引数としてカスタム等価関数を渡せます。

```javascript
const userName = useUserStore(
  (state) => state.user.name,
  (oldName, newName) => oldName === newName  // deep equal
);
```

セレクタが指定されない場合、コンポーネントは**ストア全体**に購読します。大規模なストアでは避けるべきです。

### 3. 最小限のボイラープレート

完全なストアは単一の`create`呼び出しで作成されます。アクションは単に`set`を呼び出す関数で、入れ子、非同期、独立したエクスポートが可能です。

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

### 4. ミドルウェアシステム

Zustandは、ストアクリエーターをラップして機能を追加する公式ミドルウェアを提供します。

#### Persist Middleware

状態をストレージバックエンド（localStorage、AsyncStorage、IndexedDBなど）に自動的に同期します。

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

Immerのドラフトを使用して、状態更新をミュータブルなスタイルで記述します。

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

デバッグ用にRedux DevToolsブラウザ拡張と統合します。

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

フックAPIと同様にセレクタを使った細かい購読を可能にしますが、Reactの外部で使用できます。

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

### 5. バニラJavaScript（非React）での使用

Zustandのコア状態管理ロジックは完全にReactから独立しています。React依存なしでストアを作成でき、Nodeスクリプト、Web Worker、その他の非React環境で役立ちます。

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

バニラストアをReactに統合するには、`useStore`でラップします：

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

### 6. 複数ストア（スライスパターン）

Zustandは単一のモノリシックストアではなく、独立したストアを構成することを推奨しています。**スライスパターン**を使用して複数のスライスを1つのストアに結合するか、単に`create`を複数回呼び出すこともできます。

#### 個別のストア

```javascript
// store/authStore.js
export const useAuthStore = create(/* ... */);

// store/cartStore.js
export const useCartStore = create(/* ... */);

// Component
import { useAuthStore } from './store/authStore';
import { useCartStore } from './store/cartStore';
```

#### スライスパターン（複数スライスから単一ストア）

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

### 7. 他のライブラリとの統合

- **React Query / SWR** – Zustandは**サーバー状態のキャッシュを置き換えるべきではありません**。APIデータには専用のライブラリを、UIやクライアント側状態にはZustandを使用してください。
- **Next.js** – Zustandストアはクライアントコンポーネント内で作成および利用できます。サーバーコンポーネントでは、`zustand/vanilla`から`createStore`を使用し、データをプロップとして渡します。
- **React Native** – そのまま動作します。`@react-native-async-storage/async-storage`を介した`AsyncStorage`とともに`persist`ミドルウェアを使用してください。

## 他のソリューションとの比較

| 機能 | Zustand | Redux Toolkit | React Context |
|------|---------|---------------|---------------|
| **ボイラープレート** | 最小限（create呼び出し1回） | 中程度（slice, actions, reducer, configureStore） | 低い（Provider + context） |
| **プロバイダの必要性** | なし | あり（Providerラッパー） | あり（Context.Provider） |
| **バンドルサイズ** | ~1 KB gzipped | ~12 KB gzipped | 0（ビルトイン） |
| **再レンダリング制御** | セレクタベース（厳密等価） | セレクタベース（reselect） | ビルトインのメモ化なし；コンテキスト値が変更されるたびに再レンダリング |
| **ミドルウェアエコシステム** | ビルトイン：persist, immer, devtools, subscribeWithSelector | 豊富（sagas, thunksなど） | N/A |
| **React外部での使用** | あり（バニラストア） | なし | なし |
| **TypeScriptとの親和性** | 非常に良好（型推論） | 良好（スライス指向） | 良好（ジェネリック型） |

## ベストプラクティス

1. **ストアは小さく焦点を絞る** – 1つの巨大なストアではなく、異なるドメイン（認証、カート、UI）ごとに個別のストアを作成します。
2. **セレクタを常に使用** – フックには常にセレクタを渡し、ストア全体に購読するのを避けます。
3. **直接変更よりセッターを優先** – Immerミドルウェア使用時でも、トレーサビリティを維持するためにロジックは`set`に置きます。
4. **ミドルウェアを活用** – ページリロード後も状態を維持したい場合は`persist`、開発中は`devtools`、複雑なネスト更新には`immer`を使用します。
5. **サーバー状態とクライアント状態を混在させない** – APIデータはReact Queryに任せ、ZustandはUI/デバイス状態とクライアント側キャッシュのみに使用します。
6. **バニラAPIでテスト** – ストアは`getState`と`setState`を呼び出すだけで、Reactレンダリングなしでテストできます。

## よくある落とし穴

- **セレクタを省略する** – コンポーネントがすべての状態変更で再レンダリングされ、ライブラリのパフォーマンスメリットが失われます。
- **状態を直接変更する** – 常に`set`または制御されたミューテーション関数を使用してください。`store.state`への直接代入では購読がトリガーされません。
- **サーバー状態とクライアント状態に同じストアを使用する** – 古いデータと不必要な複雑さを招きます。データ取得には専用のツールを使用してください。
- **購読解除を忘れる** – バニラの`subscribe`メソッドは購読解除関数を返します。購読が不要になったらメモリリークを防ぐために呼び出してください。

## 結論

Zustandは、そのシンプルさ、小さなフットプリント、優れたパフォーマンスにより、現代のReactアプリケーションにおける第一選択の状態管理ソリューションとなっています。プロトタイプには十分簡単でありながら、プロダクション規模のアプリケーションにも十分強力という、稀有なバランスを実現しています。プロバイダ不要の設計とフックベースの消費モデルはReact 18の並行機能と完全に調和し、バニラコアはあらゆるJavaScriptコンテキストで使用可能です。

Reduxからの移行、React Contextの置き換え、あるいは新しいプロジェクトの構築のいずれの場合でも、Zustandはクリーンで効率的、そして楽しい開発体験を提供します。

---

*詳細については、[公式リポジトリ](https://github.com/pmndrs/zustand)または[ドキュメントサイト](https://docs.pmnd.rs/zustand)をご覧ください。*