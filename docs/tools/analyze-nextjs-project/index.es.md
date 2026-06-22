---
title: Análisis de Paquetes y Rendimiento de Proyectos Next.js
description: Guía completa para analizar y optimizar el rendimiento de aplicaciones Next.js utilizando `@next/bundle-analyzer`, Lighthouse, verificaciones CI/CD y herramientas de perfilado en tiempo de ejecución.
created: 2026-06-22
tags:
  - nextjs
  - performance
  - bundler
  - optimization
  - profiling
status: draft
---

# Análisis de Proyectos Next.js: Paquetes, Rendimiento y Optimización

## ¿Qué es el Análisis de Proyectos Next.js?

Next.js es un framework de React para construir aplicaciones web full-stack con renderizado del lado del servidor (SSR), generación de sitios estáticos (SSG) y regeneración estática incremental (ISR). Analizar un proyecto Next.js implica evaluar la composición y el tamaño de los paquetes de JavaScript generados, las métricas de rendimiento en tiempo de ejecución (Web Vitals), la eficiencia de la estrategia de renderizado y los patrones de obtención de datos.

Un análisis efectivo ayuda a los desarrolladores a identificar dependencias sobredimensionadas, reducir el tiempo de ejecución de JavaScript, optimizar las estrategias de caché y prevenir la regresión del rendimiento antes de que el código llegue a producción.

## ¿Por qué analizar un proyecto Next.js?

- **Identificar dependencias sobredimensionadas:** Exponer visualmente qué paquetes inflan los tamaños de los paquetes (por ejemplo, reemplazar `moment.js` por `date-fns` después de descubrir que representa el 30% de una ruta).
- **Prevenir la regresión de paquetes:** El análisis automatizado de CI/CD detecta el aumento accidental introducido por los pull requests.
- **Optimizar Core Web Vitals:** Lighthouse y CrUX revelan cuellos de botella en Largest Contentful Paint (LCP), Total Blocking Time (TBT) y Cumulative Layout Shift (CLS).
- **Refinar estrategias de renderizado:** Determinar si una ruta debe generarse estáticamente (SSG), renderizarse en el servidor (SSR) o regenerarse bajo demanda (ISR) según las dependencias de datos y los tamaños de los paquetes.

## Prerrequisitos

- Node.js 20.x o posterior
- Un proyecto Next.js (App Router o Pages Router)
- Git (para análisis CI/CD)
- Familiaridad básica con `npm` / `yarn` / `pnpm`

---

## 1. Análisis del Tamaño de Paquetes con `@next/bundle-analyzer`

`@next/bundle-analyzer` es el plugin oficial que integra `webpack-bundle-analyzer` en el pipeline de construcción de Next.js. Genera mapas de árbol interactivos que visualizan la composición de tus paquetes de cliente y servidor.

### Instalación

```bash
npm install --save-dev @next/bundle-analyzer
```

### Configuración

Envuelve tu `next.config` con el plugin, habilitando condicionalmente el análisis mediante una variable de entorno.

```javascript
// next.config.mjs
import withBundleAnalyzer from '@next/bundle-analyzer';

const config = withBundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
})({});

export default config;
```

### Uso

Ejecuta la construcción con la bandera `ANALYZE`:

```bash
ANALYZE=true npm run build
```

Una vez finalizada la construcción, abre los archivos HTML estáticos generados en el directorio `.next/analyze/`. Cada ruta produce un mapa de árbol que muestra:

- **Tamaño estático** – tamaño del módulo sin procesar en disco
- **Tamaño analizado** – tamaño después de la transformación con Babel / SWC
- **Tamaño gzip** – tamaño después de la compresión

### Características clave

- **Paquetes de cliente y servidor:** Vistas separadas para cada objetivo de renderizado.
- **Desglose interactivo:** Haz clic en cualquier rectángulo para expandir el módulo en sus importaciones constituyentes.
- **Soporte para Turbopack:** En Next.js 15.3+, el plugin también funciona con el empaquetador Turbopack (usa `next build --turbo` para habilitarlo).
- **Filtrado:** Aísla rápidamente las dependencias de terceros vs. el código de la aplicación.

```bash
# Ejemplo: encuentra el impacto de tamaño de una librería específica
# Abre el mapa de árbol, usa el campo de búsqueda para encontrar 'lodash' o 'chart.js'
```

### Interpretar la salida

Busca los rectángulos más grandes. Los objetivos comunes de optimización incluyen:

- **Librerías de utilidades grandes** (`lodash`, `moment`) – prefiere alternativas tree-shakeable.
- **Componentes de gráficos pesados** – importación dinámica mediante `next/dynamic`.
- **Módulos duplicados entre fragmentos** – configura la deduplicación de Webpack o migra a un módulo compartido.

---

## 2. Verificaciones de Regresión de Paquetes en CI/CD

La **GitHub Action Next.js Bundle Analysis** compara automáticamente los tamaños de los paquetes de la rama del PR con la rama base y publica un comentario legible por humanos.

### Configuración

Crea `.github/workflows/bundle-analysis.yml`:

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

### Características clave

- **Comparación por ruta:** Muestra deltas de tamaño para cada ruta compilada.
- **Gráficos históricos:** Realiza seguimiento del tamaño de los paquetes a lo largo del tiempo.
- **Presupuestos de rendimiento:** Configura un umbral de tamaño máximo por ruta; la acción puede fallar la verificación CI si se excede un presupuesto.

### Uso de presupuestos de rendimiento

Agrega un archivo `bundle-budgets.json` a la raíz de tu repositorio:

```json
{
  "budget": 250000,
  "mode": "maxSize"
}
```

La acción fallará el PR si alguna ruta excede los 250 KB (gzip).

---

## 3. Auditoría en Tiempo de Ejecución con Lighthouse y CrUX

### Generar un informe de Lighthouse

Construye e inicia tu servidor de producción localmente:

```bash
npm run build && npm run start
```

Ejecuta Lighthouse CLI o usa la pestaña Lighthouse de Chrome DevTools en `http://localhost:3000`.

```bash
npx lighthouse http://localhost:3000 --view --preset=desktop
```

### Métricas clave para Next.js

| Métrica              | Impacto específico en Next.js                                        |
|----------------------|----------------------------------------------------------------------|
| **Total Blocking Time (TBT)** | Un TBT alto indica demasiado JavaScript bloqueando el hilo principal. Reduce mediante code-splitting y reducción de paquetes. |
| **Largest Contentful Paint (LCP)** | A menudo dominado por imágenes hero. Verifica `next/image` con `width`/`height` explícitos. |
| **Cumulative Layout Shift (CLS)** | Generalmente causado por anuncios, embebidos o contenido inyectado dinámicamente sin dimensiones. Usa `next/font` para eliminar el CLS relacionado con fuentes. |
| **First Input Delay (FID)** | Correlacionado directamente con la cantidad de JavaScript en la carga inicial. Paquetes más pequeños = mejor FID. |

### Uso de PageSpeed Insights / CrUX

Mientras que Lighthouse proporciona un **entorno de laboratorio**, PageSpeed Insights utiliza **datos de campo** de usuarios reales a través del Chrome User Experience Report (CrUX). Combina ambos para identificar discrepancias entre las pruebas sintéticas y las experiencias reales de los usuarios.

- **Problema de laboratorio ≠ Problema de campo:** Un resultado lento en laboratorio puede no coincidir con el rendimiento real si la mayoría de los usuarios tienen dispositivos rápidos.
- **Problema de campo ≠ Problema de laboratorio:** Un FID alto en campo pero TBT bajo en laboratorio sugiere la necesidad de un mejor perfilado del usuario en las pruebas.

---

## 4. Análisis de Componentes de Servidor y Carga RSC

Con el App Router, los componentes en `app/` son **Server Components por defecto**. Analizar la carga de los React Server Components (RSC) es crítico para el rendimiento.

### Verificar el tamaño de la carga RSC

1. Abre Chrome DevTools → pestaña **Network**.
2. Filtra las solicitudes por `__RSC`.
3. Haz clic en una solicitud de navegación para inspeccionar la respuesta JSON.

Las cargas RSC grandes a menudo indican:

- Paso de registros completos de la base de datos del servidor al cliente.
- Serialización ineficiente de Map, Set u objetos circulares.

### Detectar "fugas" de Componentes Cliente

Un Client Component (`'use client'`) arrastra todas sus dependencias al paquete del cliente.

```typescript
// app/page.tsx — Server Component (por defecto)
import ClientHeavyChart from './ClientHeavyChart';

export default function Page() {
  return <ClientHeavyChart />;
}
```

Usa la **Extensión de VSCode para Next.js** para ver sugerencias en línea que marcan un componente como `"server"` o `"client"`. Esto ayuda a garantizar que solo los componentes interactivos lleven un runtime de cliente.

### Optimizar con `next/dynamic`

Envuelve los componentes cliente grandes con importaciones dinámicas para cargarlos de forma diferida:

```typescript
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <p>Cargando gráfico…</p>,
  ssr: false, // omitir renderizado del servidor
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

Verifica el efecto volviendo a ejecutar el analizador de paquetes y buscando el fragmento etiquetado como `HeavyChart`: ahora debería cargarse asincrónicamente.

---

## 5. Auditoría de Optimización Integrada

Next.js proporciona convenciones basadas en archivos que son fáciles de auditar y ajustar.

### `next/image`

Ejecuta una compilación y busca advertencias relacionadas con imágenes. Cada componente `<Image>` debería tener:

```typescript
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // solo para imágenes visibles sin desplazamiento
/>
```

- La falta de `width`/`height` causa CLS.
- La falta de `priority` retrasa el LCP de las imágenes hero.

### `next/font`

**Mal:** Cargar fuentes desde un CDN externo (la solicitud de Google Fonts bloquea el renderizado).

**Bien:** Usar `next/font` aloja automáticamente el archivo de fuente, eliminando la solicitud de red externa.

```typescript
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'] });
// => el archivo de fuente se almacena en caché y se sirve desde tu propio dominio
```

Audita eliminando `@import` de Google Fonts de los archivos CSS.

### Estrategia `next/script`

| Estrategia             | Caso de uso                             |
|------------------------|-----------------------------------------|
| `afterInteractive`     | Analíticas (por defecto)                |
| `beforeInteractive`    | Polyfills, banners de cookies           |
| `lazyOnload`           | Widgets de chat, embebidos no críticos  |
| `worker` (experimental) | Inicializadores costosos               |

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

### Leer la salida de la compilación

```bash
Route (app)                              Size     First Load JS
┌ ○ /                                    5.8 kB          86.4 kB
├ ○ /_not-found                          875 B           81.5 kB
└ λ /api/hello                           0 B             81.5 kB
```

- **○** – Estático (SSG)
- **λ** – Dinámico (SSR / ISR)
- **Size** – El tamaño del paquete para esa ruta específica
- **First Load JS** – El JavaScript total requerido para la carga inicial de esa página

Un **Size** alto pero **First Load JS** bajo significa que la ruta está bien optimizada para code splitting. Un **First Load JS** alto indica que el framework compartido o el layout necesitan análisis.

---

## 6. Extensión de VS Code

La **Extensión oficial de VS Code para Next.js** proporciona retroalimentación en tiempo real sobre los límites de los componentes y la estructura de las rutas.

- **Límites de componentes:** El editor muestra una etiqueta junto a cada componente indicando si es un componente **server** o **client**.
- **Estructura de rutas:** La vista “Next.js: Routes” en la barra lateral enumera todas tus rutas de la aplicación, su estrategia de renderizado y parámetros dinámicos.
- **Sugerencias de tamaño en línea (versión 2.0+):** Pasa el cursor sobre una importación para ver su tamaño estimado del paquete.

```bash
# Instalar desde la línea de comandos
code --install-extension ms-vscode.vscode-nextjs
```

---

## Resumen Cheatsheet

| Herramienta / Técnica               | Propósito                                      | Comando / Configuración Clave                    |
|--------------------------------------|------------------------------------------------|--------------------------------------------------|
| `@next/bundle-analyzer`             | Visualizar la composición del paquete          | `ANALYZE=true npm run build`                     |
| Lighthouse CLI                       | Métricas de laboratorio en tiempo de ejecución | `npx lighthouse http://localhost:3000`           |
| PageSpeed Insights                   | Datos CrUX del mundo real                      | https://pagespeed.web.dev                        |
| Next.js Bundle Analysis Action       | Detección de regresión en CI/CD                | `.github/workflows/bundle-analysis.yml`          |
| RSC Network Analysis                 | Tamaño de la carga de componentes servidor     | DevTools → Network → filtrar `__RSC`             |
| Extensión de VS Code                 | Sugerencias de paquetes y límites de componentes en el editor | `code --install-extension ...` |
| `next build` output                  | Auditoría de tamaño a nivel de ruta y estrategia de renderizado | `npm run build`                 |

### Comandos adicionales

```bash
# Crear un nuevo proyecto con App Router
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir

# Compilación de producción con salida detallada
npm run build

# Análisis de paquetes personalizado con stats.json (avanzado)
npx next build --profile
```

## Lecturas adicionales

- [Página oficial de @next/bundle-analyzer en npm](https://www.npmjs.com/package/@next/bundle-analyzer)
- [Documentación de Web Vitals de Next.js](https://nextjs.org/docs/app/building-your-application/optimizing/web-vitals)
- [GitHub Action Next.js Bundle Analysis](https://github.com/marketplace/actions/nextjs-bundle-analysis)
- [Puntuación de rendimiento de Lighthouse](https://developer.chrome.com/docs/lighthouse/performance/)