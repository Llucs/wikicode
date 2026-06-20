---
title: Lazy Loading
description: A comprehensive guide to lazy loading – a performance optimization technique that defers loading of non‑critical resources until they are needed.
created: 2026-06-20
tags:
  - performance
  - optimization
  - javascript
  - web-development
  - code-splitting
status: draft
---

# Lazy Loading

**Lazy loading** is a design pattern and optimization strategy that delays the loading, initialization, or rendering of a resource until it is actually needed. In web development, this typically means deferring the fetching of images, iframes, scripts, or JavaScript bundles until they enter the user’s viewport or are triggered by an interaction. By reducing the amount of work done during the initial page load, lazy loading significantly improves start‑up time, lowers bandwidth consumption, and reduces memory footprint.

---

## Why Use Lazy Loading?

| Benefit | Description |
|---------|-------------|
| **Faster initial page load** | Only critical above‑the‑fold resources are loaded first. |
| **Reduced bandwidth** | Non‑visible resources are not downloaded until the user scrolls to them. |
| **Lower memory usage** | Unused elements (e.g., off‑screen images) are not held in memory. |
| **Better Core Web Vitals** | Proper lazy loading can improve Largest Contentful Paint (LCP) by avoiding competing requests. |
| **Improved user experience** | Pages become interactive sooner, and scrolling is smoother when off‑screen content loads progressively. |

---

## Core Techniques & Approaches

### 1. Native Lazy Loading (HTML `loading` attribute)

Since Chrome 76 (2019) and with full browser support from 2023, the `loading` attribute can be applied to `<img>` and `<iframe>` elements without any JavaScript.

```html
<img src="photo.jpg" loading="lazy" alt="Description" width="800" height="600">
<iframe src="widget.html" loading="lazy"></iframe>
```

**Best practice:** Always provide explicit `width` and `height` attributes (or CSS `aspect‑ratio`) to prevent Cumulative Layout Shift (CLS).

### 2. Intersection Observer API

A powerful browser API that efficiently detects when an element becomes visible. It replaces manual scroll‑event listeners and is the foundation of most modern lazy‑loading libraries.

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

### 3. Code Splitting & Dynamic `import()`

For JavaScript applications, lazy loading means splitting the bundle into smaller chunks that are loaded on demand. Modern bundlers (Webpack, Rollup, Vite) support this natively.

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

**How it works:** The module `./HeavyComponent` is a separate file that is fetched only when `<HeavyComponent>` is rendered. `React.lazy` automatically handles the loading state with `Suspense`.

### 4. Lazy Loading in Backend / ORMs

Lazy loading is not only a frontend concept. ORMs such as Hibernate (Java), SQLAlchemy (Python), and Entity Framework (.NET) allow you to defer loading of related objects until they are accessed.

```python
# SQLAlchemy example — lazy='select' (default)
user = session.query(User).get(1)
# The 'addresses' relationship is loaded only when accessed:
print(user.addresses)  # A separate SQL query is executed
```

**Caution:** Improper use (e.g., accessing a lazy relation inside a loop) can lead to the N+1 query problem. In such cases, use eager loading (`joinedload`, `subqueryload`) or batch loading.

### 5. Virtual Scrolling / Windowing

For huge lists (infinite scroll feeds, data tables), render only the visible rows. Libraries like `react‑window`, `react‑virtualized`, and `@tanstack/react‑virtual` implement this pattern.

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

## Installation & Setup

| Approach | Installation | Notes |
|----------|--------------|-------|
| **Native HTML** | None | Feature detection: `'loading' in HTMLImageElement.prototype` |
| **Intersection Observer** | None (native browser API) | Polyfill available for very old browsers |
| **Lazysizes (classic library)** | `npm install lazysizes@5` | Use the `lazyload` CSS class with `data‑src` |
| **Lozad.js** | `npm install lozad` | Lightweight (1KB) with Intersection Observer |
| **React/Vue/Angular** | Built‑in (`React.lazy`, Vue Async Components, Angular `loadChildren`) | No extra dependencies |
| **Database ORMs** | Part of the ORM | See your ORM’s documentation |

---

## Best Practices & Key Features

- **Always specify dimensions** for lazy‑loaded media to reserve space and avoid layout shifts.
- **Lazy load only non‑critical content** – hero images, above‑the‑fold elements, and the initial route component should be loaded eagerly.
- **Use native `loading="lazy"` when possible** – it’s zero‑cost, well‑supported, and accessible to search engines.
- **Combine with responsive images** – use `srcset` and `sizes` to load the correct image size for the viewport.
- **Implement fallbacks** – for browsers that do not support native lazy loading, use an Intersection Observer fallback (libraries like lazysizes handle this automatically).
- **Measure impact** – use Lighthouse, Chrome DevTools Network panel, and Core Web Vitals reports to verify that lazy loading actually improves performance (it can backfire for near‑viewport images).

---

## Caveats & Pitfalls

| Issue | Explanation | Solution |
|-------|-------------|----------|
| **SEO concerns** | Crawlers may not wait for JavaScript to load images. | Native `loading="lazy"` is respected by major search engines. For JS‑based solutions, consider server‑side rendering or `<noscript>` tags. |
| **Cumulative Layout Shift (CLS)** | If dimensions are not set, the page layout jumps when the image loads. | Always set `width` and `height` or use CSS `aspect‑ratio`. |
| **N+1 queries** | Lazy loading in ORMs can generate a separate query for each relation access. | Use eager loading (`joinedload`, `selectinload`, `include`) when you know you’ll need related data. |
| **Delayed interaction** | Lazy loading heavy libraries on click can cause a noticeable delay. | Preload the chunk with `<link rel="preload">` or use a small placeholder while fetching. |
| **Scroll thrashing** | Manually listening to scroll events (without debouncing) is expensive. | Use Intersection Observer instead – it’s decoupled from the scroll cycle. |

---

## Further Reading

- [MDN Web Docs: Lazy loading](https://developer.mozilla.org/en-US/docs/Web/Performance/Lazy_loading)
- [web.dev: Lazy loading images and video](https://web.dev/articles/lazy-loading-images)
- [MDN: Intersection Observer API](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)
- [React.lazy and Suspense](https://react.dev/reference/react/lazy)
- [Core Web Vitals & Lazy Loading](https://web.dev/articles/lcp-lazy-loading)