---
title: 遅延読み込み
description: 遅延読み込みに関する包括的なガイド – 必要になるまで非重要なリソースの読み込みを遅延させるパフォーマンス最適化手法です。
created: 2026-06-20
tags:
  - performance
  - optimization
  - javascript
  - web-development
  - code-splitting
status: draft
---

# 遅延読み込み

**遅延読み込み**は、リソースの読み込み、初期化、レンダリングを実際に必要になるまで遅延させるデザインパターンおよび最適化戦略です。Web開発では通常、画像、iframe、スクリプト、JavaScriptバンドルがユーザーのビューポートに入るか、インタラクションによってトリガーされるまで、それらのフェッチを遅延させることを意味します。初期ページ読み込み時の作業量を減らすことで、遅延読み込みは起動時間を大幅に改善し、帯域幅の消費を減らし、メモリ使用量を削減します。

---

## なぜ遅延読み込みを使うのか？

| メリット | 説明 |
|---------|-------------|
| **初期ページ読み込みの高速化** | 最初にファーストビューの重要なリソースのみが読み込まれます。 |
| **帯域幅の削減** | ユーザーがスクロールするまで、非表示のリソースはダウンロードされません。 |
| **メモリ使用量の低減** | 未使用の要素（例：画面外の画像）はメモリに保持されません。 |
| **Core Web Vitalsの改善** | 適切な遅延読み込みにより、競合するリクエストを回避してLargest Contentful Paint（LCP）を改善できます。 |
| **ユーザー体験の向上** | ページがより早くインタラクティブになり、画面外のコンテンツが段階的に読み込まれるためスクロールがスムーズになります。 |

---

## 主要なテクニックとアプローチ

### 1. ネイティブの遅延読み込み（HTML `loading` 属性）

Chrome 76（2019年）以降、2023年からはすべてのブラウザがサポートしており、`loading` 属性を `<img>` および `<iframe>` 要素に適用することで、JavaScriptを一切使わずに遅延読み込みが可能です。

```html
<img src="photo.jpg" loading="lazy" alt="Description" width="800" height="600">
<iframe src="widget.html" loading="lazy"></iframe>
```

**ベストプラクティス:** Cumulative Layout Shift（CLS）を防ぐために、明示的な `width` と `height` 属性（または CSS `aspect‑ratio`）を常に指定してください。

### 2. Intersection Observer API

要素が可視になったときを効率的に検出する強力なブラウザAPIです。手動のスクロールイベントリスナーを置き換え、最新の遅延読み込みライブラリの基盤となっています。

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;         // swap placeholder with real URL
      img.removeAttribute('data-src');
      observer.unobserve(img);
    }
  });
});

document.querySelectorAll('img[data-src]').forEach(img => observer.observe(img));
```

### 3. コード分割と動的 `import()`

JavaScriptアプリケーションでは、遅延読み込みはバンドルをより小さなチャンクに分割し、必要に応じて読み込むことを意味します。最新のバンドラ（Webpack、Rollup、Vite）はこれをネイティブでサポートしています。

```javascript
// React example
import React, { Suspense } from 'react';

const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

function MyApp() {
  return (
    <Suspense fallback={<div>Loading…</div>}>
      <HeavyComponent />
    </Suspense>
  );
}
```

**動作の仕組み:** `./HeavyComponent` モジュールは `<HeavyComponent>` がレンダリングされたときのみフェッチされる別ファイルです。`React.lazy` は `Suspense` を使用して読み込み状態を自動的に処理します。

### 4. バックエンド / ORM での遅延読み込み

遅延読み込みはフロントエンドの概念だけではありません。Hibernate（Java）、SQLAlchemy（Python）、Entity Framework（.NET）などのORMでは、関連オブジェクトの読み込みをアクセスされるまで遅延させることができます。

```python
# SQLAlchemy example — lazy='select' (default)
user = session.query(User).get(1)
# The 'addresses' relationship is loaded only when accessed:
print(user.addresses)  # A separate SQL query is executed
```

**注意:** 不適切な使用（例：ループ内で遅延リレーションにアクセスする）はN+1クエリ問題を引き起こす可能性があります。そのような場合は、eager loading（`joinedload`、`subqueryload`）またはバッチ読み込みを使用してください。

### 5. バーチャルスクロール / ウィンドウイング

巨大なリスト（無限スクロールフィード、データテーブル）の場合、表示されている行のみをレンダリングします。`react‑window`、`react‑virtualized`、`@tanstack/react‑virtual` などのライブラリがこのパターンを実装しています。

```jsx
import { FixedSizeList as List } from 'react-window';

const Row = ({ index, style }) => <div style={style}>Row {index}</div>;

const Example = () => (
  <List
    height={400}
    itemCount={10000}
    itemSize={35}
    width={300}
  >
    {Row}
  </List>
);
```

---

## インストールとセットアップ

| アプローチ | インストール | 備考 |
|----------|--------------|------|
| **ネイティブHTML** | なし | 機能検出: `'loading' in HTMLImageElement.prototype` |
| **Intersection Observer** | なし（ネイティブブラウザAPI） | 非常に古いブラウザ向けのPolyfillが利用可能 |
| **Lazysizes（クラシックライブラリ）** | `npm install lazysizes@5` | `lazyload` CSSクラスと`data‑src`を使用 |
| **Lozad.js** | `npm install lozad` | 軽量（1KB）でIntersection Observerを使用 |
| **React/Vue/Angular** | 組み込み（`React.lazy`、Vue Async Components、Angular `loadChildren`） | 追加の依存関係なし |
| **データベースORM** | ORMの一部 | 使用しているORMのドキュメントを参照 |

---

## ベストプラクティスと主要機能

- **遅延読み込みするメディアには常に寸法を指定**して、スペースを確保し、レイアウトのずれを防ぎます。
- **非重要なコンテンツのみを遅延読み込み** – ヒーロー画像、ファーストビュー要素、初期ルートコンポーネントは即時読み込みする必要があります。
- **可能な限りネイティブの `loading="lazy"` を使用** – コストがかからず、サポートも充実しており、検索エンジンからもアクセス可能です。
- **レスポンシブ画像と組み合わせる** – `srcset` と `sizes` を使用して、ビューポートに適した画像サイズを読み込みます。
- **フォールバックを実装** – ネイティブの遅延読み込みをサポートしないブラウザには、Intersection Observerのフォールバックを使用します（lazysizesのようなライブラリは自動的に処理します）。
- **影響を測定** – Lighthouse、Chrome DevToolsのネットワークパネル、Core Web Vitalsレポートを使用して、遅延読み込みが実際にパフォーマンスを向上させているか確認します（ビューポート近くの画像では逆効果になる可能性があります）。

---

## 注意点と落とし穴

| 問題 | 説明 | 解決策 |
|-------|-------------|----------|
| **SEOの懸念事項** | クローラーがJavaScriptによる画像の読み込みを待たない可能性があります。 | ネイティブの `loading="lazy"` は主要な検索エンジンで尊重されます。JavaScriptベースのソリューションの場合は、サーバーサイドレンダリングや `<noscript>` タグを検討してください。 |
| **Cumulative Layout Shift（CLS）** | 寸法が設定されていない場合、画像読み込み時にページレイアウトがジャンプします。 | 常に `width` と `height` を設定するか、CSS `aspect‑ratio` を使用します。 |
| **N+1クエリ** | ORMでの遅延読み込みは、リレーションにアクセスするたびに個別のクエリを生成する可能性があります。 | 関連データが必要だとわかっている場合は、eager loading（`joinedload`、`selectinload`、`include`）を使用します。 |
| **操作の遅延** | クリック時に重いライブラリを遅延読み込みすると、顕著な遅延が発生する可能性があります。 | `<link rel="preload">` を使用してチャンクを事前読み込みするか、フェッチ中に小さなプレースホルダーを使用します。 |
| **スクロールスラッシング** | 手動でスクロールイベントを（デバウンスなしで）リッスンするとコストが高くなります。 | 代わりにIntersection Observerを使用してください – スクロールサイクルから切り離されています。 |

---

## 参考資料

- [MDN Web Docs: 遅延読み込み](https://developer.mozilla.org/en-US/docs/Web/Performance/Lazy_loading)
- [web.dev: 画像と動画の遅延読み込み](https://web.dev/articles/lazy-loading-images)
- [MDN: Intersection Observer API](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)
- [React.lazy と Suspense](https://react.dev/reference/react/lazy)
- [Core Web Vitals と遅延読み込み](https://web.dev/articles/lcp-lazy-loading)