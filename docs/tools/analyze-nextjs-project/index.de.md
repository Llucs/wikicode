---
title: Analyse von Next.js-Projekt-Bundles und Performance
description: Eine vollständige Anleitung zur Analyse und Optimierung der Leistung (Performance) von Next.js-Anwendungen mithilfe von `@next/bundle-analyzer`, Lighthouse, CI/CD-Prüfungen und Laufzeit-Profiling-Tools.
created: 2026-06-22
tags:
  - nextjs
  - performance
  - bundler
  - optimization
  - profiling
status: draft
---

# Next.js-Projektanalyse: Bundles, Performance und Optimierung

## Was ist Next.js-Projektanalyse?

Next.js ist ein React-Framework zum Erstellen von Full-Stack-Webanwendungen mit Server-seitigem Rendering (SSR), statischer Seitengenerierung (SSG) und inkrementeller statischer Regeneration (ISR). Die Analyse eines Next.js-Projekts umfasst die Bewertung der Zusammensetzung und Größe generierter JavaScript-Bundles, Laufzeit-Performance-Metriken (Web Vitals), Effizienz der Rendering-Strategie und Datenabrufmuster.

Eine effektive Analyse hilft Entwicklern, überdimensionierte Abhängigkeiten zu identifizieren, die JavaScript-Ausführungszeit zu reduzieren, Caching-Strategien zu optimieren und Leistungseinbußen (Performance Regression) zu verhindern, bevor Code in die Produktion gelangt.

## Warum ein Next.js-Projekt analysieren?

- **Überdimensionierte Abhängigkeiten identifizieren:** Visuell aufdecken, welche Pakete die Bundle-Größen aufblähen (z.B. Ersetzen von `moment.js` durch `date-fns`, nachdem festgestellt wurde, dass es 30% einer Route ausmacht).
- **Bundle-Regression verhindern:** Automatisierte CI/CD-Analyse erfasst versehentliche Aufblähung durch Pull Requests.
- **Core Web Vitals optimieren:** Lighthouse und CrUX (Chrome User Experience Report) decken Engpässe bei Largest Contentful Paint (LCP), Total Blocking Time (TBT) und Cumulative Layout Shift (CLS) auf.
- **Rendering-Strategien verfeinern:** Bestimmen, ob eine Route statisch generiert (SSG), serverseitig gerendert (SSR) oder bei Bedarf regeneriert (ISR) werden sollte, basierend auf Datenabhängigkeiten und Bundle-Größen.

## Voraussetzungen

- Node.js 20.x oder höher
- Ein Next.js-Projekt (App Router oder Pages Router)
- Git (für CI/CD-Analyse)
- Grundlegende Vertrautheit mit `npm` / `yarn` / `pnpm`

---

## 1. Bundle-Größenanalyse mit `@next/bundle-analyzer`

`@next/bundle-analyzer` ist das offizielle Plugin, das `webpack-bundle-analyzer` in die Next.js-Build-Pipeline integriert. Es generiert interaktive Treemaps, die die Zusammensetzung Ihrer Client- und Server-Bundles visualisieren.

### Installation

```bash
npm install --save-dev @next/bundle-analyzer
```

### Konfiguration

Umwickeln Sie Ihre `next.config` mit dem Plugin und aktivieren Sie die Analyse bedingt über eine Umgebungsvariable.

```javascript
// next.config.mjs
import withBundleAnalyzer from '@next/bundle-analyzer';

const config = withBundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
})({});

export default config;
```

### Verwendung

Führen Sie den Build mit dem `ANALYZE`-Flag aus:

```bash
ANALYZE=true npm run build
```

Nachdem der Build abgeschlossen ist, öffnen Sie die statischen HTML-Dateien im Verzeichnis `.next/analyze/`. Jede Route erzeugt eine Treemap, die Folgendes anzeigt:

- **Stat-Größe** – rohe Modulgröße auf der Festplatte
- **Parsed-Größe** – Größe nach Babel/SWC-Transformation
- **Gzip-Größe** – Größe nach Komprimierung

### Hauptfunktionen

- **Client- und Server-Bundles:** Separate Ansichten für jedes Rendering-Ziel.
- **Drill-down:** Klicken Sie auf ein beliebiges Rechteck, um das Modul in seine Bestandteile zu zerlegen.
- **Turbopack-Unterstützung:** In Next.js 15.3+ funktioniert das Plugin auch mit dem Turbopack-Bundler (verwenden Sie `next build --turbo`, um es zu aktivieren).
- **Filterung:** Isolieren Sie schnell Drittanbieter-Abhängigkeiten vom Anwendungscode.

```bash
# Example: find the size impact of a specific library
# Open the treemap, use the search field to find 'lodash' or 'chart.js'
```

### Interpretieren der Ausgabe

Suchen Sie nach den größten Rechtecken. Häufige Optimierungsziele sind:

- **Große Utility-Bibliotheken** (`lodash`, `moment`) – bevorzugen Sie tree-shakeable Alternativen.
- **Schwere Charting-Komponenten** – dynamischer Import über `next/dynamic`.
- **Doppelte Module über Chunks hinweg** – konfigurieren Sie Webpack-Deduplizierung oder migrieren Sie zu einem gemeinsamen Modul.

---

## 2. CI/CD Bundle-Regressionsprüfungen

Die **Next.js Bundle Analysis** GitHub-Aktion vergleicht automatisch die Bundle-Größen des PR-Branches mit dem Basis-Branch und veröffentlicht einen menschenlesbaren Kommentar.

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

### Hauptfunktionen

- **Pro-Route-Vergleich:** Zeigt Größendeltas für jede kompilierte Route an.
- **Historische Diagramme:** Verfolgt die Bundle-Größe im Zeitverlauf.
- **Performance-Budgets:** Konfigurieren Sie einen maximalen Größenschwellenwert pro Route; die Aktion kann die CI-Prüfung fehlschlagen lassen, wenn ein Budget überschritten wird.

### Verwendung von Performance-Budgets

Fügen Sie eine Datei `bundle-budgets.json` im Stammverzeichnis Ihres Repositorys hinzu:

```json
{
  "budget": 250000,
  "mode": "maxSize"
}
```

Die Aktion wird den PR fehlschlagen lassen, wenn eine Route 250 KB (gzip) überschreitet.

---

## 3. Laufzeit-Auditing mit Lighthouse und CrUX

### Erstellen eines Lighthouse-Berichts

Erstellen und starten Sie Ihren Produktionsserver lokal:

```bash
npm run build && npm run start
```

Führen Sie Lighthouse CLI aus oder verwenden Sie den Chrome DevTools Lighthouse-Tab gegen `http://localhost:3000`.

```bash
npx lighthouse http://localhost:3000 --view --preset=desktop
```

### Wichtige Metriken für Next.js

| Metric              | Next.js-spezifische Auswirkung                                     |
|---------------------|---------------------------------------------------------------------|
| **Total Blocking Time (TBT)** | Hohe TBT weist auf zu viel JavaScript hin, das den Hauptthread blockiert. Reduzieren Sie sie durch Code-Splitting und Verkleinerung der Bundles. |
| **Largest Contentful Paint (LCP)** | Wird oft von Hero-Images dominiert. Überprüfen Sie `next/image` mit expliziten `width`/`height`. |
| **Cumulative Layout Shift (CLS)** | Wird normalerweise durch Anzeigen, Einbettungen oder dynamisch eingefügte Inhalte ohne Abmessungen verursacht. Verwenden Sie `next/font`, um font-bedingtes CLS zu eliminieren. |
| **First Input Delay (FID)** | Steht in direktem Zusammenhang mit der Menge an JavaScript beim initialen Laden. Kleinere Bundles = besseres FID. |

### Verwendung von PageSpeed Insights / CrUX

Während Lighthouse eine **Laborumgebung** bietet, verwendet PageSpeed Insights **Felddaten** von echten Benutzern über den Chrome User Experience Report (CrUX). Kombinieren Sie beide, um Diskrepanzen zwischen synthetischen Tests und tatsächlichen Benutzererfahrungen zu identifizieren.

- **Laborproblem ≠ Feldproblem:** Ein langsames Laborergebnis entspricht möglicherweise nicht der realen Leistung, wenn die meisten Benutzer schnelle Geräte haben.
- **Feldproblem ≠ Laborproblem:** Hohe FID im Feld, aber niedrige TBT im Labor deutet auf einen Bedarf an besserem User-Profiling in Tests hin.

---

## 4. Serverkomponenten- und RSC-Payload-Analyse

Mit dem App Router sind Komponenten in `app/` standardmäßig **Serverkomponenten**. Die Analyse des React Server Components (RSC)-Payloads ist entscheidend für die Leistung.

### Überprüfen der RSC-Payload-Größe

1. Öffnen Sie Chrome DevTools → Tab **Network**.
2. Filtern Sie Anfragen nach `__RSC`.
3. Klicken Sie auf eine Navigationsanfrage, um die JSON-Antwort zu inspizieren.

Große RSC-Payloads deuten oft auf Folgendes hin:

- Übergabe vollständiger Datenbankeinträge vom Server an den Client.
- Ineffiziente Serialisierung von Map, Set oder zirkulären Objekten.

### Erkennen von Client-Komponenten-„Leaks“

Eine Client-Komponente (`'use client'`) zieht alle ihre Abhängigkeiten in das Client-Bundle.

```typescript
// app/page.tsx — Server Component (default)
import ClientHeavyChart from './ClientHeavyChart';

export default function Page() {
  return <ClientHeavyChart />;
}
```

Verwenden Sie die **Next.js VSCode Extension**, um Inline-Hinweise zu sehen, die eine Komponente als `"server"` oder `"client"` markieren. Dies hilft sicherzustellen, dass nur interaktive Komponenten eine Client-Laufzeit haben.

### Optimieren mit `next/dynamic`

Umschließen Sie große Client-Komponenten mit dynamischen Importen, um sie lazy zu laden:

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

Überprüfen Sie den Effekt, indem Sie den Bundle-Analyzer erneut ausführen und nach dem Chunk mit der Bezeichnung `HeavyChart` suchen – er sollte jetzt asynchron geladen werden.

---

## 5. Integriertes Optimierungs-Audit

Next.js bietet dateibasierte Konventionen, die leicht zu überprüfen und zu optimieren sind.

### `next/image`

Führen Sie einen Build aus und achten Sie auf bildbezogene Warnungen. Jede `<Image>`-Komponente sollte Folgendes haben:

```typescript
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // only for above-the-fold images
/>
```

- Fehlende `width`/`height` verursacht CLS.
- Fehlendes `priority` verzögert LCP für Hero-Images.

### `next/font`

**Schlecht:** Schriftarten von einem externen CDN laden (Google Fonts-Anfrage blockiert das Rendering).

**Gut:** Die Verwendung von `next/font` hostet die Schriftartdatei automatisch selbst, wodurch die externe Netzwerkanfrage entfällt.

```typescript
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'] });
// => font file is cached and served from your own domain
```

Überprüfen Sie, ob Sie `@import` von Google Fonts aus CSS-Dateien entfernt haben.

### `next/script`-Strategie

| Strategie               | Anwendungsfall                       |
|-------------------------|--------------------------------------|
| `afterInteractive`      | Analytics (Standard)                 |
| `beforeInteractive`     | Polyfills, Cookie-Banner             |
| `lazyOnload`            | Chat-Widgets, nicht kritische Einbettungen |
| `worker` (experimentell)| Teure Initialisierungen              |

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

### Lesen der Build-Ausgabe

```bash
Route (app)                              Size     First Load JS
┌ ○ /                                    5.8 kB          86.4 kB
├ ○ /_not-found                          875 B           81.5 kB
└ λ /api/hello                           0 B             81.5 kB
```

- **○** – Statisch (SSG)
- **λ** – Dynamisch (SSR / ISR)
- **Size** – Die Bundle-Größe für diese spezifische Route
- **First Load JS** – Das gesamte JavaScript, das für das initiale Laden dieser Seite erforderlich ist

Ein hoher **Size**-Wert, aber niedriger **First Load JS**-Wert bedeutet, dass die Route gut für Code-Splitting optimiert ist. Ein hoher **First Load JS**-Wert deutet darauf hin, dass das gemeinsame Framework oder Layout analysiert werden muss.

---

## 6. VS Code-Erweiterung

Die offizielle **Next.js VS Code Extension** bietet Echtzeit-Feedback zu Komponentengrenzen und Routenstruktur.

- **Komponentengrenzen:** Der Editor zeigt neben jeder Komponente eine Bezeichnung an, die angibt, ob es sich um eine **Server**- oder **Client**-Komponente handelt.
- **Routenstruktur:** Die Ansicht „Next.js: Routes“ in der Seitenleiste listet alle Ihre App-Routen, ihre Rendering-Strategie und dynamischen Parameter auf.
- **Inline-Größenhinweise** (Version 2.0+): Fahren Sie mit der Maus über einen Import, um seine geschätzte Bundle-Größe zu sehen.

```bash
# Install from the command line
code --install-extension ms-vscode.vscode-nextjs
```

---

## Zusammenfassung – Spickzettel

| Tool / Technik                | Zweck                                   | Schlüsselbefehl / Konfiguration                  |
|-------------------------------|-----------------------------------------|---------------------------------------------------|
| `@next/bundle-analyzer`       | Bundle-Zusammensetzung visualisieren    | `ANALYZE=true npm run build`                      |
| Lighthouse CLI                | Labormessungen der Laufzeit             | `npx lighthouse http://localhost:3000`            |
| PageSpeed Insights            | Echte CrUX-Daten                        | https://pagespeed.web.dev                         |
| Next.js Bundle Analysis Action | CI/CD-Regressionserkennung            | `.github/workflows/bundle-analysis.yml`           |
| RSC-Netzwerkanalyse           | Größe des Serverkomponenten-Payloads    | DevTools → Network → filter `__RSC`               |
| VS Code Extension             | In-Editor-Bundle- und Komponentengrenzen-Hinweise | `code --install-extension ...`            |
| `next build` Ausgabe          | Routen-Level-Größen- und Renderingstrategie-Audit | `npm run build`                         |

### Zusätzliche Befehle

```bash
# Scaffold a new project with App Router
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir

# Production build with detailed output
npm run build

# Custom bundle analysis with stats.json (advanced)
npx next build --profile
```

## Weiterführende Literatur

- [Official @next/bundle-analyzer npm page](https://www.npmjs.com/package/@next/bundle-analyzer)
- [Next.js Web Vitals Documentation](https://nextjs.org/docs/app/building-your-application/optimizing/web-vitals)
- [Next.js Bundle Analysis GitHub Action](https://github.com/marketplace/actions/nextjs-bundle-analysis)
- [Lighthouse Performance Scoring](https://developer.chrome.com/docs/lighthouse/performance/)