---
title: Next.js项目包体与性能分析
description: 使用 `@next/bundle-analyzer`、Lighthouse、CI/CD检查及运行时性能分析工具，全面分析与优化Next.js应用性能的指南。
created: 2026-06-22
tags:
  - nextjs
  - performance
  - bundler
  - optimization
  - profiling
status: draft
---

# Next.js 项目分析：包体、性能与优化

## 什么是Next.js项目分析？

Next.js是一个用于构建全栈Web应用程序的React框架，支持服务端渲染（SSR）、静态站点生成（SSG）和增量静态再生（ISR）。分析Next.js项目涉及评估生成的JavaScript包体的构成与大小、运行时性能指标（Web Vitals）、渲染策略效率以及数据获取模式。

有效的分析帮助开发者识别过大的依赖、减少JavaScript执行时间、优化缓存策略，并在代码进入生产环境前防止性能退化。

## 为什么分析Next.js项目？

- **识别过大的依赖：** 直观地显示哪些包增大了包体（例如，在发现 `moment.js` 占某个路由的30%后，将其替换为 `date-fns`）。
- **防止包体退化：** 自动化CI/CD分析可捕获由拉取请求引入的意外膨胀。
- **优化 Core Web Vitals：** Lighthouse和CrUX（Chrome用户体验报告）揭示Largest Contentful Paint（LCP）、Total Blocking Time（TBT）和Cumulative Layout Shift（CLS）中的瓶颈。
- **优化渲染策略：** 根据数据依赖和包体大小，确定路由应静态生成（SSG）、服务端渲染（SSR）还是按需再生（ISR）。

## 前提条件

- Node.js 20.x 或更高版本
- 一个 Next.js 项目（App Router 或 Pages Router）
- Git（用于CI/CD分析）
- 基本熟悉 `npm` / `yarn` / `pnpm`

---

## 1. 使用 `@next/bundle-analyzer` 进行包体大小分析

`@next/bundle-analyzer` 是官方插件，它将 `webpack-bundle-analyzer` 集成到 Next.js 构建流程中。它生成交互式树图，可视化客户端和服务端包体的构成。

### 安装

```bash
npm install --save-dev @next/bundle-analyzer
```

### 配置

使用该插件包装 `next.config`，通过环境变量条件性地启用分析。

```javascript
// next.config.mjs
import withBundleAnalyzer from '@next/bundle-analyzer';

const config = withBundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
})({});

export default config;
```

### 用法

使用 `ANALYZE` 标志运行构建：

```bash
ANALYZE=true npm run build
```

构建完成后，打开 `.next/analyze/` 目录中生成的静态HTML文件。每个路由都会生成一个树图，显示：

- **Stat size** – 模块在磁盘上的原始大小
- **Parsed size** – 经过 Babel/SWC 转换后的大小
- **Gzip size** – 压缩后的大小

### 主要特性

- **客户端和服务端包体：** 每个渲染目标都有单独的视图。
- **下钻功能：** 点击任何矩形可将模块展开为其组成的导入。
- **Turbopack 支持：** 在 Next.js 15.3+ 中，该插件也可与 Turbopack 绑定器一起使用（使用 `next build --turbo` 启用）。
- **筛选：** 快速分离第三方依赖与应用代码。

```bash
# Example: find the size impact of a specific library
# Open the treemap, use the search field to find 'lodash' or 'chart.js'
```

### 解读输出

寻找最大的矩形。常见的优化目标包括：

- **大型实用库**（`lodash`、`moment`）—— 优先选择可摇树优化的替代方案。
- **重量级图表组件** —— 通过 `next/dynamic` 进行动态导入。
- **跨 chunk 的重复模块** —— 配置 Webpack 去重或迁移到共享模块。

---

## 2. CI/CD 包体退化检查

**Next.js Bundle Analysis** GitHub Action 会自动比较 PR 分支与基础分支的包体大小，并发布可读的评论。

### 设置

创建 `.github/workflows/bundle-analysis.yml`：

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

### 主要特性

- **按路由比较：** 显示每个编译路由的大小增量。
- **历史图表：** 跟踪包体大小随时间的变化。
- **性能预算：** 为每个路由配置最大大小阈值；如果超出预算，该操作可使CI检查失败。

### 使用性能预算

在仓库根目录添加 `bundle-budgets.json` 文件：

```json
{
  "budget": 250000,
  "mode": "maxSize"
}
```

如果任何路由超过 250 KB（gzip），该操作将使 PR 失败。

---

## 3. 使用 Lighthouse 和 CrUX 进行运行时审计

### 生成 Lighthouse 报告

在本地构建并启动生产服务器：

```bash
npm run build && npm run start
```

运行 Lighthouse CLI 或使用 Chrome DevTools 的 Lighthouse 标签页对 `http://localhost:3000` 进行测试。

```bash
npx lighthouse http://localhost:3000 --view --preset=desktop
```

### Next.js 的关键指标

| 指标              | Next.js 特有影响                                        |
|---------------------|----------------------------------------------------------------|
| **Total Blocking Time (TBT)** | 高 TBT 表示过多 JavaScript 阻塞了主线程。通过代码分割和缩小包体来降低。 |
| **Largest Contentful Paint (LCP)** | 通常由主图像主导。确认 `next/image` 使用了明确的 `width`/`height`。 |
| **Cumulative Layout Shift (CLS)** | 通常由广告、嵌入内容或没有尺寸的动态注入内容引起。使用 `next/font` 消除字体引起的 CLS。 |
| **First Input Delay (FID)** | 与初始加载的 JavaScript 量直接相关。较小的包体 = 更好的 FID。 |

### 使用 PageSpeed Insights / CrUX

Lighthouse 提供的是**实验室环境**，而 PageSpeed Insights 通过 Chrome 用户体验报告（CrUX）使用真实用户的**现场数据**。将两者结合，可识别合成测试与实际用户体验之间的差异。

- **实验室问题 ≠ 现场问题：** 如果大多数用户拥有快速设备，实验室的慢速结果可能不匹配真实世界性能。
- **现场问题 ≠ 实验室问题：** 现场高 FID 但实验室低 TBT 表明需要在测试中更好地进行用户画像分析。

---

## 4. 服务端组件与 RSC 负载分析

在 App Router 中， `app/` 目录下的组件默认是**服务端组件**。分析 React Server Components (RSC) 负载对性能至关重要。

### 检查 RSC 负载大小

1. 打开 Chrome DevTools → **Network** 标签页。
2. 按 `__RSC` 过滤请求。
3. 点击导航请求以检查 JSON 响应。

大的 RSC 负载通常表示：

- 将完整数据库记录从服务端传递到客户端。
- Map、Set 或循环对象的低效序列化。

### 检测客户端组件“泄漏”

客户端组件（`'use client'`）会将其所有依赖拉入客户端包体。

```typescript
// app/page.tsx — Server Component (default)
import ClientHeavyChart from './ClientHeavyChart';

export default function Page() {
  return <ClientHeavyChart />;
}
```

使用 **Next.js VSCode Extension** 可查看将组件标记为 `"server"` 或 `"client"` 的内联提示。这有助于确保只有交互式组件才携带客户端运行时。

### 使用 `next/dynamic` 进行优化

使用动态导入包装大型客户端组件以实现懒加载：

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

通过重新运行包体分析器并查找标记为 `HeavyChart` 的 chunk 来验证效果——它现在应该异步加载。

---

## 5. 内置优化审计

Next.js 提供了基于文件的约定，便于审计和微调。

### `next/image`

运行构建并查找与图像相关的警告。每个 `<Image>` 组件应具有：

```typescript
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // only for above-the-fold images
/>
```

- 缺少 `width`/`height` 会导致 CLS。
- 缺少 `priority` 会延迟主图像的 LCP。

### `next/font`

**不良做法：** 从外部 CDN 加载字体（Google Fonts 请求会阻塞渲染）。

**良好做法：** 使用 `next/font` 自动自托管字体文件，消除外部网络请求。

```typescript
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'] });
// => font file is cached and served from your own domain
```

通过从 CSS 文件中移除 Google Fonts 的 `@import` 来进行审计。

### `next/script` 策略

| 策略             | 使用场景                             |
|----------------------|--------------------------------------|
| `afterInteractive`   | 分析工具（默认）                  |
| `beforeInteractive`  | Polyfills、Cookie 横幅            |
| `lazyOnload`         | 聊天小部件、非关键嵌入    |
| `worker` (实验性) | 昂贵的初始化器            |

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

### 读取构建输出

```bash
Route (app)                              Size     First Load JS
┌ ○ /                                    5.8 kB          86.4 kB
├ ○ /_not-found                          875 B           81.5 kB
└ λ /api/hello                           0 B             81.5 kB
```

- **○** – 静态（SSG）
- **λ** – 动态（SSR / ISR）
- **Size** – 该特定路由的包体大小
- **First Load JS** – 该页面初始加载所需的总 JavaScript 量

高 **Size** 但低 **First Load JS** 意味着该路由在代码分割方面优化良好。高 **First Load JS** 表示需要分析共享框架或布局。

---

## 6. VS Code 扩展

官方 **Next.js VS Code Extension** 提供关于组件边界和路由结构的实时反馈。

- **组件边界：** 编辑器在每个组件旁显示标签，指示它是**服务端**还是**客户端**组件。
- **路由结构：** 侧边栏中的“Next.js: Routes”视图列出所有应用路由、其渲染策略和动态参数。
- **内联大小提示** (2.0+ 版本)：悬停在导入上可查看其估计的包体大小。

```bash
# Install from the command line
code --install-extension ms-vscode.vscode-nextjs
```

---

## 总结速查表

| 工具 / 技术               | 目的                                      | 关键命令 / 配置                              |
|--------------------------------|----------------------------------------------|---------------------------------------------------|
| `@next/bundle-analyzer`        | 可视化包体构成                 | `ANALYZE=true npm run build`                      |
| Lighthouse CLI                 | 实验室运行时指标                          | `npx lighthouse http://localhost:3000`            |
| PageSpeed Insights             | 真实世界 CrUX 数据                         | https://pagespeed.web.dev                         |
| Next.js Bundle Analysis Action | CI/CD 回归检测                   | `.github/workflows/bundle-analysis.yml`           |
| RSC Network Analysis           | 服务端组件负载大小                | DevTools → Network → filter `__RSC`               |
| VS Code Extension              | 编辑器内包体与组件边界提示   | `code --install-extension ...`                    |
| `next build` 输出            | 路由级别大小与渲染策略审计  | `npm run build`                                   |

### 附加命令

```bash
# Scaffold a new project with App Router
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir

# Production build with detailed output
npm run build

# Custom bundle analysis with stats.json (advanced)
npx next build --profile
```

## 延伸阅读

- [官方 @next/bundle-analyzer npm 页面](https://www.npmjs.com/package/@next/bundle-analyzer)
- [Next.js Web Vitals 文档](https://nextjs.org/docs/app/building-your-application/optimizing/web-vitals)
- [Next.js Bundle Analysis GitHub Action](https://github.com/marketplace/actions/nextjs-bundle-analysis)
- [Lighthouse 性能评分](https://developer.chrome.com/docs/lighthouse/performance/)