---
title: Next.js プロジェクトのバンドルとパフォーマンスを分析する
description: `@next/bundle-analyzer`、Lighthouse、CI/CD チェック、ランタイムプロファイリングツールを使用して Next.js アプリケーションのパフォーマンスを分析および最適化するための完全ガイド。
created: 2026-06-22
tags:
  - nextjs
  - performance
  - bundler
  - optimization
  - profiling
status: draft
---

# Next.js プロジェクト分析：バンドル、パフォーマンス、最適化

## Next.js プロジェクト分析とは？

Next.js は、サーバーサイドレンダリング（SSR）、静的サイト生成（SSG）、インクリメンタル静的再生成（ISR）を使用してフルスタック Web アプリケーションを構築するための React フレームワークです。Next.js プロジェクトの分析には、生成された JavaScript バンドルの構成とサイズ、ランタイムパフォーマンスメトリクス（Web Vitals）、レンダリング戦略の効率性、データフェッチパターンの評価が含まれます。

効果的な分析により、開発者は過剰なサイズの依存関係を特定し、JavaScript の実行時間を削減し、キャッシュ戦略を最適化し、コードが本番環境に到達する前にパフォーマンスの低下を防ぐことができます。

## Next.js プロジェクトを分析する理由？

- **過剰なサイズの依存関係の特定：** どのパッケージがバンドルサイズを膨らませているかを視覚的に明らかにします（例：`moment.js` を `date-fns` に置き換えることで、特定のルートの 30% を占めていた場合）。
- **バンドルサイズの後退防止：** 自動化された CI/CD 分析により、プルリクエストで意図せず追加された肥大化を検出します。
- **Core Web Vitals の最適化：** Lighthouse と CrUX（Chrome User Experience Report）が、Largest Contentful Paint（LCP）、Total Blocking Time（TBT）、Cumulative Layout Shift（CLS）のボトルネックを明らかにします。
- **レンダリング戦略の洗練：** データの依存関係とバンドルサイズに基づいて、ルートを静的生成（SSG）、サーバーレンダリング（SSR）、またはオンデマンドで再生成（ISR）するかを決定します。

## 前提条件

- Node.js 20.x 以降
- Next.js プロジェクト（App Router または Pages Router）
- Git（CI/CD 分析用）
- `npm` / `yarn` / `pnpm` の基本的な知識

---

## 1. `@next/bundle-analyzer` によるバンドルサイズ分析

`@next/bundle-analyzer` は、`webpack-bundle-analyzer` を Next.js のビルドパイプラインに統合する公式プラグインです。クライアントバンドルとサーバーバンドルの構成を視覚化するインタラクティブなツリーマップを生成します。

### インストール

```bash
npm install --save-dev @next/bundle-analyzer
```

### 設定

プラグインで `next.config` をラップし、環境変数によって分析を条件付きで有効にします。

```javascript
// next.config.mjs
import withBundleAnalyzer from '@next/bundle-analyzer';

const config = withBundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
})({});

export default config;
```

### 使用方法

`ANALYZE` フラグを指定してビルドを実行します：

```bash
ANALYZE=true npm run build
```

ビルドが完了したら、`.next/analyze/` ディレクトリに生成された静的な HTML ファイルを開きます。各ルートには次の情報を示すツリーマップが生成されます：

- **Stat サイズ** – ディスク上のモジュールの生のサイズ
- **Parsed サイズ** – Babel / SWC 変換後のサイズ
- **Gzip サイズ** – 圧縮後のサイズ

### 主な機能

- **クライアント & サーバーバンドル：** レンダリング対象ごとに個別のビューを表示。
- **ドリルダウン：** 任意の矩形をクリックして、モジュールをその構成インポートに展開。
- **Turbopack 対応：** Next.js 15.3 以上では、プラグインは Turbopack バンドラーでも動作します（有効にするには `next build --turbo` を使用）。
- **フィルタリング：** サードパーティの依存関係とアプリケーションコードを迅速に分離。

```bash
# 例：特定のライブラリのサイズへの影響を確認する
# ツリーマップを開き、検索フィールドを使用して 'lodash' や 'chart.js' を検索
```

### 出力の解釈

最大の矩形を探します。一般的な最適化対象は以下の通りです：

- **大規模なユーティリティライブラリ（`lodash`、`moment`）** – ツリーシェイキング可能な代替手段を優先。
- **重いチャートコンポーネント** – `next/dynamic` による動的インポート。
- **チャンク間の重複モジュール** – Webpack の重複排除を設定するか、共有モジュールに移行。

---

## 2. CI/CD バンドルサイズ後退チェック

**Next.js Bundle Analysis** GitHub Action は、PR ブランチのバンドルサイズをベースブランチと自動的に比較し、人間が読めるコメントを投稿します。

### セットアップ

`.github/workflows/bundle-analysis.yml` を作成します：

```yaml
name: Next.js Bundle Analysis

on:
  pull_request:
    branches: [main]

permissions:
  contents: read
  pull-requests: write

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run build
      - uses: andriech/nextjs-bundle-analysis@main
        with:
          build-output: .next
          save: true
      - uses: marocchino/sticky-pull-request-comment@v2
        with:
          header: next-bundle-analysis
          path: .next/analyze/__bundle_analysis_comment.md
```

### 主な機能

- **ルートごとの比較：** コンパイルされたすべてのルートのサイズ差分を表示。
- **履歴チャート：** バンドルサイズの経時変化を追跡。
- **パフォーマンスバジェット：** ルートごとに最大サイズしきい値を設定。バジェットを超えた場合、アクションは CI チェックを失敗させることができます。

### パフォーマンスバジェットの使用

リポジトリのルートに `bundle-budgets.json` ファイルを追加します：

```json
{
  "budget": 250000,
  "mode": "maxSize"
}
```

アクションは、いずれかのルートが 250 KB（gzip）を超えた場合、PR を失敗させます。

---

## 3. Lighthouse と CrUX によるランタイム監査

### Lighthouse レポートの生成

本番サーバーをローカルでビルドして起動します：

```bash
npm run build && npm run start
```

`http://localhost:3000` に対して、Lighthouse CLI を実行するか、Chrome DevTools の Lighthouse タブを使用します。

```bash
npx lighthouse http://localhost:3000 --view --preset=desktop
```

### Next.js における主要指標

| Metric                          | Next.js での影響                                                              |
|---------------------------------|-------------------------------------------------------------------------------|
| **Total Blocking Time (TBT)**   | TBT が高いと、メインスレッドをブロックする JavaScript が多すぎることを示します。コード分割とバンドル縮小で改善します。 |
| **Largest Contentful Paint (LCP)** | 多くの場合、ヒーロー画像が支配的です。`next/image` で明示的な `width`/`height` を指定してください。 |
| **Cumulative Layout Shift (CLS)** | 通常、広告、埋め込みコンテンツ、またはサイズ指定なしで動的に注入されたコンテンツが原因です。`next/font` を使用してフォント関連の CLS を排除します。 |
| **First Input Delay (FID)**     | 初期ロード時の JavaScript の量に直接相関します。バンドルが小さいほど FID が向上します。 |

### PageSpeed Insights / CrUX の使用

Lighthouse は**ラボ環境**を提供するのに対し、PageSpeed Insights は Chrome User Experience Report（CrUX）を介して実際のユーザーからの**フィールドデータ**を使用します。両方を組み合わせて、合成テストと実際のユーザーエクスペリエンスとの間の不一致を特定します。

- **ラボの問題 ≠ フィールドの問題：** ラボの結果が遅くても、ほとんどのユーザーが高速なデバイスを使用している場合、実際のパフォーマンスと一致しない可能性があります。
- **フィールドの問題 ≠ ラボの問題：** フィールドで FID が高いのにラボで TBT が低い場合、テストでより良いユーザープロファイリングが必要であることを示唆しています。

---

## 4. サーバーコンポーネントと RSC ペイロード分析

App Router では、`app/` 内のコンポーネントはデフォルトで**サーバーコンポーネント**です。React Server Components（RSC）ペイロードの分析はパフォーマンスにとって重要です。

### RSC ペイロードサイズの確認

1. Chrome DevTools を開き → **Network** タブを選択。
2. リクエストを `__RSC` でフィルタリング。
3. ナビゲーションリクエストをクリックして JSON レスポンスを確認。

大きな RSC ペイロードは、多くの場合以下を示します：

- サーバーからクライアントへの完全なデータベースレコードの受け渡し。
- Map、Set、循環オブジェクトの非効率なシリアル化。

### クライアントコンポーネントの「リーク」検出

クライアントコンポーネント（`'use client'`）は、その依存関係すべてをクライアントバンドルに取り込みます。

```typescript
// app/page.tsx — Server Component (default)
import ClientHeavyChart from './ClientHeavyChart';

export default function Page() {
  return <ClientHeavyChart />;
}
```

**Next.js VSCode Extension** を使用すると、コンポーネントに `"server"` または `"client"` と表示されるインラインヒントが表示されます。これにより、インタラクティブなコンポーネントのみがクライアントランタイムを持つことが保証されます。

### `next/dynamic` による最適化

大きなクライアントコンポーネントを動的インポートでラップして遅延ロードします：

```typescript
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <p>Loading chart…</p>,
  ssr: false, // skip server render
});

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <HeavyChart />
    </div>
  );
}
```

効果を確認するには、バンドルアナライザーを再実行し、`HeavyChart` というラベルのチャンクを探します。非同期で読み込まれるはずです。

---

## 5. 組み込みの最適化監査

Next.js は、監査と微調整が容易なファイルベースの規約を提供します。

### `next/image`

ビルドを実行し、画像関連の警告を探します。すべての `<Image>` コンポーネントには以下が必要です：

```typescript
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // only for above-the-fold images
/>
```

- `width`/`height` がないと CLS を引き起こします。
- `priority` がないと、ヒーロー画像の LCP が遅れます。

### `next/font`

**悪い例：** 外部 CDN からのフォント読み込み（Google Fonts のリクエストがレンダリングをブロックする）。

**良い例：** `next/font` を使用すると、フォントファイルが自動的にセルフホスティングされ、外部ネットワークリクエストが排除されます。

```typescript
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'] });
// => font file is cached and served from your own domain
```

CSS ファイルから Google Fonts の `@import` を削除して監査します。

### `next/script` のストラテジー

| Strategy               | ユースケース                     |
|------------------------|----------------------------------|
| `afterInteractive`     | 分析（デフォルト）               |
| `beforeInteractive`    | ポリフィル、クッキーバナー       |
| `lazyOnload`           | チャットウィジェット、重要でない埋め込み |
| `worker` (experimental)| 負荷の高い初期化処理             |

```typescript
import Script from 'next/script';

export default function Page() {
  return (
    <>
      <Script
        src="https://analytics.example.com/script.js"
        strategy="lazyOnload"
      />
    </>
  );
}
```

### ビルド出力の読み方

```bash
Route (app)                              Size     First Load JS
┌ ○ /                                    5.8 kB          86.4 kB
├ ○ /_not-found                          875 B           81.5 kB
└ λ /api/hello                           0 B             81.5 kB
```

- **○** – 静的 (SSG)
- **λ** – 動的 (SSR / ISR)
- **Size** – そのルートのバンドルサイズ
- **First Load JS** – そのページの初期ロードに必要な JavaScript の総量

**Size** が大きくても **First Load JS** が小さい場合、そのルートはコード分割が適切に最適化されています。**First Load JS** が大きい場合は、共有フレームワークまたはレイアウトの分析が必要です。

---

## 6. VS Code 拡張機能

公式の **Next.js VS Code 拡張機能**は、コンポーネントの境界とルート構造に関するリアルタイムのフィードバックを提供します。

- **コンポーネントの境界：** エディタは各コンポーネントの横に、それが**サーバー**コンポーネントか**クライアント**コンポーネントかを示すラベルを表示します。
- **ルート構造：** サイドバーの「Next.js: Routes」ビューに、アプリのすべてのルート、そのレンダリング戦略、動的パラメータが一覧表示されます。
- **インラインサイズヒント（バージョン 2.0 以上）：** インポートにカーソルを合わせると、推定バンドルサイズが表示されます。

```bash
# コマンドラインからインストール
code --install-extension ms-vscode.vscode-nextjs
```

---

## まとめチートシート

| ツール / テクニック             | 目的                                   | キーコマンド / 設定                             |
|--------------------------------|----------------------------------------|-------------------------------------------------|
| `@next/bundle-analyzer`        | バンドル構成の可視化                   | `ANALYZE=true npm run build`                    |
| Lighthouse CLI                 | ラボのランタイムメトリクス             | `npx lighthouse http://localhost:3000`          |
| PageSpeed Insights             | 実際の CrUX データ                     | https://pagespeed.web.dev                       |
| Next.js Bundle Analysis Action | CI/CD 回帰検出                         | `.github/workflows/bundle-analysis.yml`         |
| RSC Network Analysis           | サーバーコンポーネントのペイロードサイズ | DevTools → Network → filter `__RSC`             |
| VS Code Extension              | エディタ内のバンドル・コンポーネント境界ヒント | `code --install-extension ...`             |
| `next build` 出力              | ルートレベルのサイズ・レンダリング戦略監査 | `npm run build`                                 |

### 追加コマンド

```bash
# App Router を使用して新しいプロジェクトをスキャフォールド
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir

# 詳細出力付きでプロダクションビルド
npm run build

# stats.json を使用したカスタムバンドル分析（上級者向け）
npx next build --profile
```

## 参考資料

- [Official @next/bundle-analyzer npm page](https://www.npmjs.com/package/@next/bundle-analyzer)
- [Next.js Web Vitals Documentation](https://nextjs.org/docs/app/building-your-application/optimizing/web-vitals)
- [Next.js Bundle Analysis GitHub Action](https://github.com/marketplace/actions/nextjs-bundle-analysis)
- [Lighthouse Performance Scoring](https://developer.chrome.com/docs/lighthouse/performance/)