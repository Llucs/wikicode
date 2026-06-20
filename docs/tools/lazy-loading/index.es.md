---
title: Carga diferida
description: Una guía completa sobre la carga diferida – una técnica de optimización del rendimiento que pospone la carga de recursos no críticos hasta que son necesarios.
created: 2026-06-20
tags:
  - performance
  - optimization
  - javascript
  - web-development
  - code-splitting
status: draft
---

# Carga diferida

La **carga diferida** es un patrón de diseño y una estrategia de optimización que retrasa la carga, inicialización o renderización de un recurso hasta que realmente se necesita. En el desarrollo web, esto suele significar diferir la obtención de imágenes, iframes, scripts o paquetes de JavaScript hasta que entran en el viewport del usuario o se activan mediante una interacción. Al reducir la cantidad de trabajo realizado durante la carga inicial de la página, la carga diferida mejora significativamente el tiempo de inicio, reduce el consumo de ancho de banda y disminuye la huella de memoria.

---

## ¿Por qué usar la carga diferida?

| Beneficio | Descripción |
|-----------|-------------|
| **Carga inicial más rápida** | Solo los recursos críticos del área visible se cargan primero. |
| **Reducción del ancho de banda** | Los recursos no visibles no se descargan hasta que el usuario se desplaza hasta ellos. |
| **Menor uso de memoria** | Los elementos no utilizados (por ejemplo, imágenes fuera de pantalla) no se mantienen en memoria. |
| **Mejores métricas Core Web Vitals** | Una carga diferida adecuada puede mejorar el Largest Contentful Paint (LCP) al evitar peticiones en conflicto. |
| **Mejora de la experiencia de usuario** | Las páginas se vuelven interactivas más rápido y el desplazamiento es más fluido cuando el contenido fuera de pantalla se carga progresivamente. |

---

## Técnicas y enfoques principales

### 1. Carga diferida nativa (atributo HTML `loading`)

Desde Chrome 76 (2019) y con soporte completo en navegadores a partir de 2023, el atributo `loading` se puede aplicar a elementos `<img>` e `<iframe>` sin necesidad de JavaScript.

```html
<img src="photo.jpg" loading="lazy" alt="Descripción" width="800" height="600">
<iframe src="widget.html" loading="lazy"></iframe>
```

**Buena práctica:** Proporcione siempre atributos explícitos `width` y `height` (o `aspect‑ratio` en CSS) para evitar el desplazamiento acumulativo del diseño (CLS).

### 2. API Intersection Observer

Una potente API del navegador que detecta de manera eficiente cuándo un elemento se vuelve visible. Reemplaza los listeners manuales de eventos de desplazamiento y es la base de la mayoría de las bibliotecas modernas de carga diferida.

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;         // intercambia el marcador de posición por la URL real
      img.removeAttribute('data-src');
      observer.unobserve(img);
    }
  });
});

document.querySelectorAll('img[data-src]').forEach(img => observer.observe(img));
```

### 3. División de código e importación dinámica `import()`

Para aplicaciones JavaScript, la carga diferida consiste en dividir el paquete en fragmentos más pequeños que se cargan bajo demanda. Los empaquetadores modernos (Webpack, Rollup, Vite) soportan esto de forma nativa.

```javascript
// Ejemplo en React
import React, { Suspense } from 'react';

const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

function MyApp() {
  return (
    <Suspense fallback={<div>Cargando…</div>}>
      <HeavyComponent />
    </Suspense>
  );
}
```

**Cómo funciona:** El módulo `./HeavyComponent` es un archivo separado que se obtiene solo cuando se renderiza `<HeavyComponent>`. `React.lazy` maneja automáticamente el estado de carga con `Suspense`.

### 4. Carga diferida en el backend / ORMs

La carga diferida no es solo un concepto del frontend. ORMs como Hibernate (Java), SQLAlchemy (Python) y Entity Framework (.NET) permiten diferir la carga de objetos relacionados hasta que se accede a ellos.

```python
# Ejemplo con SQLAlchemy — lazy='select' (valor por defecto)
user = session.query(User).get(1)
# La relación 'addresses' se carga solo cuando se accede a ella:
print(user.addresses)  # Se ejecuta una consulta SQL separada
```

**Precaución:** Un uso inadecuado (por ejemplo, acceder a una relación diferida dentro de un bucle) puede provocar el problema de consultas N+1. En tales casos, utilice carga ansiosa (`joinedload`, `subqueryload`) o carga por lotes.

### 5. Desplazamiento virtual / Windowing

Para listas enormes (feeds de desplazamiento infinito, tablas de datos), renderice solo las filas visibles. Bibliotecas como `react‑window`, `react‑virtualized` y `@tanstack/react‑virtual` implementan este patrón.

```jsx
import { FixedSizeList as List } from 'react-window';

const Row = ({ index, style }) => <div style={style}>Fila {index}</div>;

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

## Instalación y configuración

| Enfoque | Instalación | Notas |
|---------|-------------|-------|
| **HTML nativo** | Ninguna | Detección de funcionalidad: `'loading' in HTMLImageElement.prototype` |
| **Intersection Observer** | Ninguna (API nativa del navegador) | Polyfill disponible para navegadores muy antiguos |
| **Lazysizes (biblioteca clásica)** | `npm install lazysizes@5` | Use la clase CSS `lazyload` con `data‑src` |
| **Lozad.js** | `npm install lozad` | Ligero (1KB) con Intersection Observer |
| **React/Vue/Angular** | Incorporado (`React.lazy`, Componentes asíncronos de Vue, `loadChildren` de Angular) | Sin dependencias adicionales |
| **ORMs de bases de datos** | Parte del ORM | Consulte la documentación de su ORM |

---

## Buenas prácticas y características clave

- **Especifique siempre las dimensiones** de los medios cargados de forma diferida para reservar espacio y evitar cambios de diseño.
- **Cargue de forma diferida solo el contenido no crítico** – las imágenes hero, los elementos del área visible y el componente de la ruta inicial deben cargarse de forma ansiosa.
- **Utilice `loading="lazy"` nativo cuando sea posible** – no tiene coste, está bien soportado y es accesible para los motores de búsqueda.
- **Combínelo con imágenes responsivas** – use `srcset` y `sizes` para cargar el tamaño de imagen correcto para el viewport.
- **Implemente alternativas (fallbacks)** – para navegadores que no soportan la carga diferida nativa, use un fallback basado en Intersection Observer (bibliotecas como lazysizes lo manejan automáticamente).
- **Mida el impacto** – use Lighthouse, el panel Network de Chrome DevTools y los informes de Core Web Vitals para verificar que la carga diferida realmente mejora el rendimiento (puede resultar contraproducente para imágenes cercanas al viewport).

---

## Advertencias y dificultades

| Problema | Explicación | Solución |
|----------|-------------|----------|
| **Preocupaciones SEO** | Los rastreadores pueden no esperar a que JavaScript cargue las imágenes. | La carga diferida nativa `loading="lazy"` es respetada por los principales motores de búsqueda. Para soluciones basadas en JS, considere el renderizado del lado del servidor o etiquetas `<noscript>`. |
| **Desplazamiento acumulativo del diseño (CLS)** | Si no se establecen las dimensiones, el diseño de la página salta cuando se carga la imagen. | Establezca siempre `width` y `height` o use `aspect‑ratio` en CSS. |
| **Consultas N+1** | La carga diferida en ORMs puede generar una consulta separada por cada acceso a una relación. | Use carga ansiosa (`joinedload`, `selectinload`, `include`) cuando sepa que necesitará los datos relacionados. |
| **Interacción retrasada** | Cargar bibliotecas pesadas de forma diferida al hacer clic puede causar un retraso notable. | Precargue el fragmento con `<link rel="preload">` o use un marcador de posición pequeño mientras se obtiene. |
| **Thrashing de desplazamiento** | Escuchar eventos de desplazamiento manualmente (sin debouncing) es costoso. | Use Intersection Observer en su lugar – está desacoplado del ciclo de desplazamiento. |

---

## Lecturas adicionales

- [MDN Web Docs: Lazy loading](https://developer.mozilla.org/en-US/docs/Web/Performance/Lazy_loading)
- [web.dev: Lazy loading images and video](https://web.dev/articles/lazy-loading-images)
- [MDN: Intersection Observer API](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)
- [React.lazy and Suspense](https://react.dev/reference/react/lazy)
- [Core Web Vitals & Lazy Loading](https://web.dev/articles/lcp-lazy-loading)