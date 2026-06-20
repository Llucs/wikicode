---
title: 懒加载
description: 懒加载的全面指南——一种性能优化技术，将非关键资源的加载推迟到需要时。
created: 2026-06-20
tags:
  - performance
  - optimization
  - javascript
  - web-development
  - code-splitting
status: draft
---

# 懒加载

**懒加载**是一种设计模式和优化策略，它延迟资源的加载、初始化或渲染，直到实际需要时才进行。在Web开发中，这通常意味着推迟获取图像、iframe、脚本或JavaScript包，直到它们进入用户的视口或由交互触发。通过减少初始页面加载期间完成的工作量，懒加载显著缩短了启动时间，降低了带宽消耗，并减少了内存占用。

---

## 为什么使用懒加载？

| 优势 | 描述 |
|------|------|
| **更快的初始页面加载** | 仅优先加载首屏的关键资源。 |
| **减少带宽消耗** | 在用户滚动到非可见资源之前，不会下载它们。 |
| **降低内存使用** | 未使用的元素（例如屏幕外的图像）不会保留在内存中。 |
| **更好的核心网页指标** | 正确的懒加载可以通过避免竞争请求来改善最大内容绘制（LCP）。 |
| **改善用户体验** | 页面变得更快可用，并且当屏幕外内容逐步加载时，滚动更流畅。 |

---

## 核心技术与方法

### 1. 原生懒加载（HTML `loading` 属性）

自Chrome 76（2019年）起，并从2023年开始获得全面浏览器支持，`loading`属性可以应用于`<img>`和`<iframe>`元素，无需任何JavaScript。

```html
<img src="photo.jpg" loading="lazy" alt="Description" width="800" height="600">
<iframe src="widget.html" loading="lazy"></iframe>
```

**最佳实践：** 始终提供显式的`width`和`height`属性（或CSS `aspect‑ratio`）以防止累积布局偏移（CLS）。

### 2. Intersection Observer API

一个强大的浏览器API，可以有效检测元素何时可见。它取代了手动滚动事件监听器，是大多数现代懒加载库的基础。

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

### 3. 代码分割与动态 `import()`

对于JavaScript应用程序，懒加载意味着将包分割成较小的块，按需加载。现代打包器（Webpack、Rollup、Vite）原生支持此功能。

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

**工作原理：** 模块`./HeavyComponent`是一个单独的文件，仅在渲染`<HeavyComponent>`时获取。`React.lazy`自动与`Suspense`配合处理加载状态。

### 4. 后端/ORM中的懒加载

懒加载不仅仅是前端概念。ORM（如Hibernate (Java)、SQLAlchemy (Python)、Entity Framework (.NET)）允许你将相关对象的加载推迟到访问时。

```python
# SQLAlchemy example — lazy='select' (default)
user = session.query(User).get(1)
# The 'addresses' relationship is loaded only when accessed:
print(user.addresses)  # A separate SQL query is executed
```

**注意事项：** 不当使用（例如在循环中访问懒加载关系）可能导致N+1查询问题。在这种情况下，请使用急加载（`joinedload`、`subqueryload`）或批量加载。

### 5. 虚拟滚动/窗口化

对于大型列表（无限滚动信息流、数据表），仅渲染可见行。像 `react‑window`、`react‑virtualized`、`@tanstack/react‑virtual` 这样的库实现了这种模式。

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

## 安装与设置

| 方法 | 安装 | 说明 |
|------|------|------|
| **原生HTML** | 无 | 特征检测：`'loading' in HTMLImageElement.prototype` |
| **Intersection Observer** | 无（原生浏览器API） | 适用于非常旧的浏览器的Polyfill |
| **Lazysizes（经典库）** | `npm install lazysizes@5` | 使用带有 `data‑src` 的 `lazyload` CSS类 |
| **Lozad.js** | `npm install lozad` | 轻量级（1KB），使用Intersection Observer |
| **React/Vue/Angular** | 内置（`React.lazy`、Vue异步组件、Angular `loadChildren`） | 无需额外依赖 |
| **数据库ORM** | 属于ORM的一部分 | 请参阅您的ORM文档 |

---

## 最佳实践与关键特性

- **始终为懒加载媒体指定尺寸**，以预留空间并避免布局偏移。
- **仅对非关键内容使用懒加载**——英雄图像、首屏元素和初始路由组件应进行急加载。
- **尽可能使用原生 `loading="lazy"`**——零成本、支持良好且对搜索引擎可访问。
- **结合响应式图像**——使用 `srcset` 和 `sizes` 加载适合视口的正确图像尺寸。
- **实现回退**——对于不支持原生懒加载的浏览器，使用Intersection Observer回退（像lazysizes这样的库可以自动处理）。
- **衡量影响**——使用Lighthouse、Chrome DevTools网络面板和Core Web Vitals报告，验证懒加载是否真正提高了性能（对于接近视口的图像，可能会适得其反）。

---

## 注意事项与陷阱

| 问题 | 解释 | 解决方案 |
|------|------|----------|
| **SEO问题** | 爬虫可能不会等待JavaScript加载图像。 | 原生 `loading="lazy"` 被主要搜索引擎尊重。对于基于JS的解决方案，考虑服务端渲染或 `<noscript>` 标签。 |
| **累积布局偏移（CLS）** | 如果未设置尺寸，页面布局会在图像加载时跳动。 | 始终设置 `width` 和 `height` 或使用CSS `aspect‑ratio`。 |
| **N+1查询** | ORM中的懒加载可能为每次关系访问生成单独的查询。 | 当你知道需要关联数据时，使用急加载（`joinedload`、`selectinload`、`include`）。 |
| **延迟交互** | 点击时懒加载重型库可能导致明显延迟。 | 使用 `<link rel="preload">` 预加载块，或在获取时使用小型占位符。 |
| **滚动抖动** | 手动监听滚动事件（无防抖）代价高昂。 | 改用Intersection Observer——它与滚动循环解耦。 |

---

## 延伸阅读

- [MDN Web文档：懒加载](https://developer.mozilla.org/en-US/docs/Web/Performance/Lazy_loading)
- [web.dev：图像和视频的懒加载](https://web.dev/articles/lazy-loading-images)
- [MDN：Intersection Observer API](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)
- [React.lazy 和 Suspense](https://react.dev/reference/react/lazy)
- [核心网页指标与懒加载](https://web.dev/articles/lcp-lazy-loading)