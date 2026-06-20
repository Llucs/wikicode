---
title: Lazy Loading
description: Ein umfassender Leitfaden zu Lazy Loading – eine Technik zur Leistungsoptimierung, die das Laden von nicht‑kritischen Ressourcen verzögert, bis sie benötigt werden.
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

**Lazy loading** ist ein Entwurfsmuster und eine Optimierungsstrategie, die das Laden, Initialisieren oder Rendern einer Ressource verzögert, bis sie tatsächlich benötigt wird. In der Webentwicklung bedeutet dies typischerweise, dass das Abrufen von Bildern, Iframes, Skripten oder JavaScript-Bundles aufgeschoben wird, bis sie in den Viewport des Benutzers gelangen oder durch eine Interaktion ausgelöst werden. Indem die Menge der Arbeit während des anfänglichen Seitenladens reduziert wird, verbessert Lazy Loading die Startzeit erheblich, senkt den Bandbreitenverbrauch und reduziert den Speicherbedarf.

---

## Warum Lazy Loading verwenden?

| Vorteil | Beschreibung |
|---------|--------------|
| **Schnelleres anfängliches Laden der Seite** | Nur kritische Ressourcen oberhalb der Falz werden zuerst geladen. |
| **Reduzierte Bandbreite** | Nicht sichtbare Ressourcen werden erst heruntergeladen, wenn der Benutzer zu ihnen scrollt. |
| **Geringerer Speicherverbrauch** | Nicht verwendete Elemente (z. B. Bilder außerhalb des Bildschirms) werden nicht im Speicher gehalten. |
| **Bessere Core Web Vitals** | Richtiges Lazy Loading kann den Largest Contentful Paint (LCP) verbessern, indem konkurrierende Anfragen vermieden werden. |
| **Verbesserte Benutzererfahrung** | Seiten werden schneller interaktiv, und das Scrollen ist flüssiger, wenn Inhalte außerhalb des Bildschirms progressiv geladen werden. |

---

## Kerntechniken und Ansätze

### 1. Nativer Lazy Loading (HTML `loading`-Attribut)

Seit Chrome 76 (2019) und mit vollständiger Browserunterstützung ab 2023 kann das `loading`-Attribut auf `<img>`- und `<iframe>`-Elemente angewendet werden, ohne JavaScript.

```html
<img src="photo.jpg" loading="lazy" alt="Description" width="800" height="600">
<iframe src="widget.html" loading="lazy"></iframe>
```

**Bewährte Vorgehensweise:** Geben Sie immer explizite `width`- und `height`-Attribute (oder CSS `aspect‑ratio`) an, um Cumulative Layout Shift (CLS) zu verhindern.

### 2. Intersection Observer API

Eine leistungsstarke Browser-API, die effizient erkennt, wann ein Element sichtbar wird. Sie ersetzt manuelle Scroll-Ereignis-Listener und ist die Grundlage der meisten modernen Lazy-Loading-Bibliotheken.

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

Für JavaScript-Anwendungen bedeutet Lazy Loading, das Bundle in kleinere Chunks aufzuteilen, die bei Bedarf geladen werden. Moderne Bundler (Webpack, Rollup, Vite) unterstützen dies nativ.

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

**So funktioniert es:** Das Modul `./HeavyComponent` ist eine separate Datei, die erst abgerufen wird, wenn `<HeavyComponent>` gerendert wird. `React.lazy` verwaltet den Ladezustand automatisch mit `Suspense`.

### 4. Lazy Loading in Backend / ORMs

Lazy Loading ist nicht nur ein Frontend-Konzept. ORMs wie Hibernate (Java), SQLAlchemy (Python) und Entity Framework (.NET) ermöglichen es, das Laden von verwandten Objekten zu verzögern, bis sie abgerufen werden.

```python
# SQLAlchemy example — lazy='select' (default)
user = session.query(User).get(1)
# The 'addresses' relationship is loaded only when accessed:
print(user.addresses)  # A separate SQL query is executed
```

**Vorsicht:** Unsachgemäße Verwendung (z. B. Zugriff auf eine verzögerte Relation innerhalb einer Schleife) kann zum N+1-Abfrageproblem führen. Verwenden Sie in solchen Fällen Eager Loading (`joinedload`, `subqueryload`) oder Batch Loading.

### 5. Virtual Scrolling / Windowing

Für große Listen (Endlos-Scroll-Feeds, Datentabellen) rendern Sie nur die sichtbaren Zeilen. Bibliotheken wie `react-window`, `react-virtualized` und `@tanstack/react-virtual` implementieren dieses Muster.

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

## Installation und Einrichtung

| Ansatz | Installation | Anmerkungen |
|--------|--------------|-------------|
| **Native HTML** | Keine | Funktionserkennung: `'loading' in HTMLImageElement.prototype` |
| **Intersection Observer** | Keine (native Browser-API) | Polyfill für sehr alte Browser verfügbar |
| **Lazysizes (classic library)** | `npm install lazysizes@5` | Verwenden Sie die CSS-Klasse `lazyload` mit `data-src` |
| **Lozad.js** | `npm install lozad` | Leichtgewichtig (1 KB) mit Intersection Observer |
| **React/Vue/Angular** | Eingebaut (`React.lazy`, Vue Async Components, Angular `loadChildren`) | Keine zusätzlichen Abhängigkeiten |
| **Database ORMs** | Teil des ORMs | Siehe Dokumentation Ihres ORMs |

---

## Bewährte Vorgehensweisen und wichtige Funktionen

- **Geben Sie immer Dimensionen** für lazy-geladene Medien an, um Platz zu reservieren und Layoutverschiebungen zu vermeiden.
- **Laden Sie nur nicht-kritische Inhalte lazy** – Hero-Bilder, Elemente oberhalb der Falz und die initiale Routenkomponente sollten eager geladen werden.
- **Verwenden Sie nach Möglichkeit natives `loading="lazy"`** – es ist kostenlos, gut unterstützt und für Suchmaschinen zugänglich.
- **Kombinieren Sie es mit responsiven Bildern** – verwenden Sie `srcset` und `sizes`, um die richtige Bildgröße für den Viewport zu laden.
- **Implementieren Sie Fallbacks** – für Browser, die natives Lazy Loading nicht unterstützen, verwenden Sie einen Intersection Observer-Fallback (Bibliotheken wie Lazysizes erledigen dies automatisch).
- **Messen Sie die Auswirkungen** – verwenden Sie Lighthouse, das Chrome DevTools Network-Panel und Core Web Vitals-Berichte, um zu überprüfen, ob Lazy Loading die Leistung tatsächlich verbessert (es kann bei Bildern in der Nähe des Viewports nach hinten losgehen).

---

## Vorbehalte und Fallstricke

| Problem | Erklärung | Lösung |
|---------|-----------|--------|
| **SEO-Bedenken** | Crawler warten möglicherweise nicht darauf, dass JavaScript Bilder lädt. | Natives `loading="lazy"` wird von großen Suchmaschinen respektiert. Für JS-basierte Lösungen erwägen Sie serverseitiges Rendering oder `<noscript>`-Tags. |
| **Cumulative Layout Shift (CLS)** | Wenn keine Abmessungen festgelegt sind, springt das Seitenlayout, wenn das Bild geladen wird. | Setzen Sie immer `width` und `height` oder verwenden Sie CSS `aspect-ratio`. |
| **N+1-Abfragen** | Lazy Loading in ORMs kann eine separate Abfrage für jeden Relationszugriff erzeugen. | Verwenden Sie Eager Loading (`joinedload`, `selectinload`, `include`), wenn Sie wissen, dass Sie verwandte Daten benötigen. |
| **Verzögerte Interaktion** | Das Lazy Laden schwerer Bibliotheken bei Klick kann eine spürbare Verzögerung verursachen. | Laden Sie den Chunk mit `<link rel="preload">` vor oder verwenden Sie einen kleinen Platzhalter während des Abrufens. |
| **Scroll-Trashing** | Manuelles Lauschen auf Scroll-Ereignisse (ohne Entprellung) ist teuer. | Verwenden Sie stattdessen Intersection Observer – es ist vom Scroll-Zyklus entkoppelt. |

---

## Weiterführende Literatur

- [MDN Web Docs: Lazy Loading](https://developer.mozilla.org/en-US/docs/Web/Performance/Lazy_loading)
- [web.dev: Lazy Loading von Bildern und Videos](https://web.dev/articles/lazy-loading-images)
- [MDN: Intersection Observer API](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)
- [React.lazy und Suspense](https://react.dev/reference/react/lazy)
- [Core Web Vitals & Lazy Loading](https://web.dev/articles/lcp-lazy-loading)