---
title: Analyzing Next.js Project Bundles and Performance
description: A complete guide to analyzing and optimizing Next.js application performance using `@next/bundle-analyzer`, Lighthouse, CI/CD checks, and runtime profiling tools.
created: 2026-06-22
tags:
  - nextjs
  - performance
  - bundler
  - optimization
  - profiling
status: draft
---

# Next.js Project Analysis: Bundles, Performance, and Optimization

## What Is Next.js Project Analysis?

Next.js is a React framework for building full-stack web applications with server-side rendering (SSR), static site generation (SSG), and incremental static regeneration (ISR). Analyzing a Next.js project involves evaluating the composition and size of generated JavaScript bundles, runtime performance metrics (Web Vitals), rendering strategy efficiency, and data-fetching patterns.

Effective analysis helps developers identify oversized dependencies, reduce JavaScript execution time, optimize caching strategies, and prevent performance regression before code reaches production.

## Why Analyze a Next.js Project?

- **Identify oversized dependencies:** Visually expose which packages inflate bundle sizes (e.g., replacing `moment.js` with `date-fns` after discovering it represents 30% of a route).
- **Prevent bundle regression:** Automated CI/CD analysis catches accidental bloat introduced by pull requests.
- **Optimize Core Web Vitals:** Lighthouse and CrUX (Chrome User Experience Report) reveal bottlenecks in Largest Contentful Paint (LCP), Total Blocking Time (TBT), and Cumulative Layout Shift (CLS).
- **Refine rendering strategies:** Determine whether a route should be statically generated (SSG), server-rendered (SSR), or regenerated on demand (ISR) based on data dependencies and bundle sizes.

## Prerequisites

- Node.js 20.x or later
- A Next.js project (App Router or Pages Router)
- Git (for CI/CD analysis)
- Basic familiarity with `npm` / `yarn` / `pnpm`

---

## 1. Bundle Size Analysis with `@next/bundle-analyzer`

`@next/bundle-analyzer` is the official plugin that integrates `webpack-bundle-analyzer` into the Next.js build pipeline. It generates interactive treemaps that visualize the composition of your client and server bundles.

### Installation

```bash
npm install --save-dev @next/bundle-analyzer
```

### Configuration

Wrap your `next.config` with the plugin, conditionally enabling analysis via an environment variable.

```javascript
// next.config.mjs
import withBundleAnalyzer from '@next/bundle-analyzer';

const config = withBundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
})({});

export default config;
```

### Usage

Run the build with the `ANALYZE` flag:

```bash
ANALYZE=true npm run build
```

After the build finishes, open the static HTML files generated in the `.next/analyze/` directory. Each route produces a treemap showing:

- **Stat size** – raw module size on disk
- **Parsed size** – size after Babel / SWC transformation
- **Gzip size** – size after compression

### Key Features

- **Client & Server bundles:** Separate views for each rendering target.
- **Drill-down:** Click any rectangle to explode the module into its constituent imports.
- **Turbopack support:** In Next.js 15.3+, the plugin also works with the Turbopack bundler (use `next build --turbo` to enable).
- **Filtering:** Quickly isolate third-party dependencies vs. application code.

```bash
# Example: find the size impact of a specific library
# Open the treemap, use the search field to find 'lodash' or 'chart.js'
```

### Interpreting the Output

Look for the largest rectangles. Common optimization targets include:

- **Large utility libraries** (`lodash`, `moment`) – prefer tree-shakeable alternatives.
- **Heavy charting components** – dynamic import via `next/dynamic`.
- **Duplicate modules across chunks** – configure Webpack deduplication or migrate to a shared module.

---

## 2. CI/CD Bundle Regression Checks

The **Next.js Bundle Analysis** GitHub Action automatically compares bundle sizes from the PR branch against the base branch and posts a human-readable comment.

### Setup

Create `.github/workflows/bundle-analysis.yml`:

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

### Key Features

- **Per-route comparison:** Shows size deltas for every compiled route.
- **Historical charts:** Tracks bundle size over time.
- **Performance budgets:** Configure a maximum size threshold per route; the action can fail the CI check if a budget is exceeded.

### Using Performance Budgets

Add a `bundle-budgets.json` file to the root of your repository:

```json
{
  "budget": 250000,
  "mode": "maxSize"
}
```

The action will fail the PR if any route exceeds 250 KB (gzip).

---

## 3. Runtime Auditing with Lighthouse & CrUX

### Generating a Lighthouse Report

Build and start your production server locally:

```bash
npm run build && npm run start
```

Run Lighthouse CLI or use the Chrome DevTools Lighthouse tab against `http://localhost:3000`.

```bash
npx lighthouse http://localhost:3000 --view --preset=desktop
```

### Key Metrics for Next.js

| Metric              | Next.js Specific Impact                                        |
|---------------------|----------------------------------------------------------------|
| **Total Blocking Time (TBT)** | High TBT indicates too much JavaScript blocking the main thread. Lower by code-splitting and shrinking bundles. |
| **Largest Contentful Paint (LCP)** | Often dominated by hero images. Verify `next/image` with explicit `width`/`height`. |
| **Cumulative Layout Shift (CLS)** | Usually caused by ads, embeds, or dynamically injected content without dimensions. Use `next/font` to eliminate font-related CLS. |
| **First Input Delay (FID)** | Directly correlated to the amount of JavaScript on the initial load. Smaller bundles = better FID. |

### Using PageSpeed Insights / CrUX

While Lighthouse provides a **lab environment**, PageSpeed Insights uses **field data** from real users via the Chrome User Experience Report (CrUX). Combine both to identify discrepancies between synthetic tests and actual user experiences.

- **Lab issue ≠ Field issue:** A slow lab result might not match real-world performance if most users have fast devices.
- **Field issue ≠ Lab issue:** High FID in the field but low TBT in the lab suggests a need for better user-profiling in tests.

---

## 4. Server Component & RSC Payload Analysis

With the App Router, components in `app/` are **Server Components by default**. Analyzing the React Server Components (RSC) payload is critical for performance.

### Checking RSC Payload Size

1. Open Chrome DevTools → **Network** tab.
2. Filter requests by `__RSC`.
3. Click a navigation request to inspect the JSON response.

Large RSC payloads often indicate:

- Passing full database records from server to client.
- Inefficient serialization of Map, Set, or circular objects.

### Detecting Client Component "Leaks"

A Client Component (`'use client'`) pulls all its dependencies into the client bundle.

```typescript
// app/page.tsx — Server Component (default)
import ClientHeavyChart from './ClientHeavyChart';

export default function Page() {
  return <ClientHeavyChart />;
}
```

Use **Next.js VSCode Extension** to see inlay hints marking a component as `"server"` or `"client"`. This helps ensure only interactive components carry a client runtime.

### Optimizing with `next/dynamic`

Wrap large client components with dynamic imports to lazy-load them:

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

Verify the effect by re-running the bundle analyzer and looking for the chunk labeled `HeavyChart`—it should now load asynchronously.

---

## 5. Built-in Optimization Audit

Next.js provides file-based conventions that are easy to audit and fine-tune.

### `next/image`

Run a build and look for image-related warnings. Every `<Image>` component should have:

```typescript
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // only for above-the-fold images
/>
```

- Missing `width`/`height` causes CLS.
- Missing `priority` delays LCP for hero images.

### `next/font`

**Bad:** Loading fonts from an external CDN (Google Fonts request blocks rendering).

**Good:** Using `next/font` automatically self-hosts the font file, eliminating the external network request.

```typescript
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'] });
// => font file is cached and served from your own domain
```

Audit by removing `@import` of Google Fonts from CSS files.

### `next/script` Strategy

| Strategy             | Use Case                             |
|----------------------|--------------------------------------|
| `afterInteractive`   | Analytics (default)                  |
| `beforeInteractive`  | Polyfills, cookie banners            |
| `lazyOnload`         | Chat widgets, non-critical embeds    |
| `worker` (experimental) | Expensive initializers            |

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

### Reading the Build Output

```bash
Route (app)                              Size     First Load JS
┌ ○ /                                    5.8 kB          86.4 kB
├ ○ /_not-found                          875 B           81.5 kB
└ λ /api/hello                           0 B             81.5 kB
```

- **○** – Static (SSG)
- **λ** – Dynamic (SSR / ISR)
- **Size** – The bundle size for that specific route
- **First Load JS** – The total JavaScript required for the initial load of that page

A high **Size** but low **First Load JS** means the route is well-optimized for code splitting. A high **First Load JS** indicates the shared framework or layout needs analysis.

---

## 6. VS Code Extension

The official **Next.js VS Code Extension** provides real-time feedback on component boundaries and route structure.

- **Component boundaries:** The editor displays a label next to each component indicating whether it is a **server** or **client** component.
- **Route structure:** The “Next.js: Routes” view in the sidebar lists all your app routes, their rendering strategy, and dynamic params.
- **Inline size hints** (version 2.0+): Hover over an import to see its estimated bundle size.

```bash
# Install from the command line
code --install-extension ms-vscode.vscode-nextjs
```

---

## Summary Cheatsheet

| Tool / Technique               | Purpose                                      | Key Command / Config                              |
|--------------------------------|----------------------------------------------|---------------------------------------------------|
| `@next/bundle-analyzer`        | Visualize bundle composition                 | `ANALYZE=true npm run build`                      |
| Lighthouse CLI                 | Lab runtime metrics                          | `npx lighthouse http://localhost:3000`            |
| PageSpeed Insights             | Real-world CrUX data                         | https://pagespeed.web.dev                         |
| Next.js Bundle Analysis Action | CI/CD regression detection                   | `.github/workflows/bundle-analysis.yml`           |
| RSC Network Analysis           | Server component payload size                | DevTools → Network → filter `__RSC`               |
| VS Code Extension              | In-editor bundle & component boundary hints   | `code --install-extension ...`                    |
| `next build` output            | Route-level size & rendering strategy audit  | `npm run build`                                   |

### Additional Commands

```bash
# Scaffold a new project with App Router
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir

# Production build with detailed output
npm run build

# Custom bundle analysis with stats.json (advanced)
npx next build --profile
```

## Further Reading

- [Official @next/bundle-analyzer npm page](https://www.npmjs.com/package/@next/bundle-analyzer)
- [Next.js Web Vitals Documentation](https://nextjs.org/docs/app/building-your-application/optimizing/web-vitals)
- [Next.js Bundle Analysis GitHub Action](https://github.com/marketplace/actions/nextjs-bundle-analysis)
- [Lighthouse Performance Scoring](https://developer.chrome.com/docs/lighthouse/performance/)