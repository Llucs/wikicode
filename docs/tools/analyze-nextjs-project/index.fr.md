---
title: Analyse des bundles et des performances de projets Next.js
description: Un guide complet pour analyser et optimiser les performances des applications Next.js en utilisant `@next/bundle-analyzer`, Lighthouse, les vérifications CI/CD et les outils de profilage runtime.
created: 2026-06-22
tags:
  - nextjs
  - performance
  - bundler
  - optimization
  - profiling
status: draft
---

# Analyse de projets Next.js : Bundles, performances et optimisation

## Qu'est-ce que l'analyse de projet Next.js ?

Next.js est un framework React pour construire des applications web full-stack avec le rendu côté serveur (SSR), la génération de sites statiques (SSG) et la régénération statique incrémentielle (ISR). Analyser un projet Next.js implique d'évaluer la composition et la taille des bundles JavaScript générés, les métriques de performance runtime (Web Vitals), l'efficacité des stratégies de rendu et les schémas de récupération de données.

Une analyse efficace aide les développeurs à identifier les dépendances surdimensionnées, réduire le temps d'exécution JavaScript, optimiser les stratégies de mise en cache et prévenir la régression de performance avant que le code n'atteigne la production.

## Pourquoi analyser un projet Next.js ?

- **Identifier les dépendances surdimensionnées :** Exposer visuellement les packages qui gonflent les tailles de bundle (par exemple, remplacer `moment.js` par `date-fns` après avoir découvert qu'il représente 30% d'une route).
- **Prévenir la régression de bundle :** L'analyse automatisée CI/CD détecte le gonflement accidentel introduit par les pull requests.
- **Optimiser les Core Web Vitals :** Lighthouse et CrUX (Chrome User Experience Report) révèlent les goulots d'étranglement dans le Largest Contentful Paint (LCP), le Total Blocking Time (TBT) et le Cumulative Layout Shift (CLS).
- **Affiner les stratégies de rendu :** Déterminer si une route doit être générée statiquement (SSG), rendue côté serveur (SSR) ou régénérée à la demande (ISR) en fonction des dépendances de données et des tailles de bundle.

## Prérequis

- Node.js 20.x ou ultérieur
- Un projet Next.js (App Router ou Pages Router)
- Git (pour l'analyse CI/CD)
- Connaissance de base de `npm` / `yarn` / `pnpm`

---

## 1. Analyse de la taille des bundles avec `@next/bundle-analyzer`

`@next/bundle-analyzer` est le plugin officiel qui intègre `webpack-bundle-analyzer` dans le pipeline de build Next.js. Il génère des treemaps interactifs qui visualisent la composition de vos bundles client et serveur.

### Installation

```bash
npm install --save-dev @next/bundle-analyzer
```

### Configuration

Enveloppez votre `next.config` avec le plugin, en activant conditionnellement l'analyse via une variable d'environnement.

```javascript
// next.config.mjs
import withBundleAnalyzer from '@next/bundle-analyzer';

const config = withBundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
})({});

export default config;
```

### Utilisation

Lancez le build avec le flag `ANALYZE` :

```bash
ANALYZE=true npm run build
```

Une fois le build terminé, ouvrez les fichiers HTML statiques générés dans le répertoire `.next/analyze/`. Chaque route produit un treemap montrant :

- **Stat size** – taille brute du module sur le disque
- **Parsed size** – taille après transformation Babel / SWC
- **Gzip size** – taille après compression

### Fonctionnalités clés

- **Bundles client et serveur :** Vues séparées pour chaque cible de rendu.
- **Exploration :** Cliquez sur un rectangle pour décomposer le module en ses imports constitutifs.
- **Support Turbopack :** Dans Next.js 15.3+, le plugin fonctionne également avec le bundler Turbopack (utilisez `next build --turbo` pour l'activer).
- **Filtrage :** Isolez rapidement les dépendances tierces du code applicatif.

```bash
# Exemple : trouver l'impact d'une bibliothèque spécifique
# Ouvrez le treemap, utilisez le champ de recherche pour trouver 'lodash' ou 'chart.js'
```

### Interprétation des résultats

Recherchez les plus grands rectangles. Les cibles d'optimisation courantes incluent :

- **Bibliothèques utilitaires volumineuses** (`lodash`, `moment`) – préférez des alternatives élagables (tree-shakeable).
- **Composants de graphiques lourds** – import dynamique via `next/dynamic`.
- **Modules dupliqués entre les chunks** – configurez la déduplication Webpack ou migrez vers un module partagé.

---

## 2. Vérifications de régression de bundle CI/CD

L'action GitHub **Next.js Bundle Analysis** compare automatiquement les tailles de bundle de la branche PR avec la branche de base et publie un commentaire lisible.

### Configuration

Créez `.github/workflows/bundle-analysis.yml` :

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

### Fonctionnalités clés

- **Comparaison par route :** Affiche les écarts de taille pour chaque route compilée.
- **Graphiques historiques :** Suit la taille du bundle au fil du temps.
- **Budgets de performance :** Configurez un seuil de taille maximum par route ; l'action peut faire échouer la vérification CI si un budget est dépassé.

### Utilisation des budgets de performance

Ajoutez un fichier `bundle-budgets.json` à la racine de votre dépôt :

```json
{
  "budget": 250000,
  "mode": "maxSize"
}
```

L'action fera échouer la PR si une route dépasse 250 Ko (gzip).

---

## 3. Audit runtime avec Lighthouse et CrUX

### Génération d'un rapport Lighthouse

Construisez et démarrez votre serveur de production localement :

```bash
npm run build && npm run start
```

Exécutez Lighthouse CLI ou utilisez l'onglet Lighthouse des Chrome DevTools sur `http://localhost:3000`.

```bash
npx lighthouse http://localhost:3000 --view --preset=desktop
```

### Métriques clés pour Next.js

| Métrique              | Impact spécifique Next.js                                        |
|-----------------------|------------------------------------------------------------------|
| **Total Blocking Time (TBT)** | Un TBT élevé indique trop de JavaScript bloquant le thread principal. Réduisez-le en divisant le code et en réduisant les bundles. |
| **Largest Contentful Paint (LCP)** | Souvent dominé par les images hero. Vérifiez `next/image` avec des `width`/`height` explicites. |
| **Cumulative Layout Shift (CLS)** | Généralement causé par des publicités, des contenus embarqués ou du contenu injecté dynamiquement sans dimensions. Utilisez `next/font` pour éliminer le CLS lié aux polices. |
| **First Input Delay (FID)** | Directement corrélé à la quantité de JavaScript lors du chargement initial. Des bundles plus petits = un meilleur FID. |

### Utilisation de PageSpeed Insights / CrUX

Alors que Lighthouse fournit un **environnement de laboratoire**, PageSpeed Insights utilise des **données de terrain** d'utilisateurs réels via le Chrome User Experience Report (CrUX). Combinez les deux pour identifier les écarts entre les tests synthétiques et les expériences utilisateur réelles.

- **Problème de laboratoire ≠ Problème de terrain :** Un résultat de laboratoire lent peut ne pas correspondre aux performances réelles si la plupart des utilisateurs ont des appareils rapides.
- **Problème de terrain ≠ Problème de laboratoire :** Un FID élevé sur le terrain mais un TBT faible en laboratoire suggère un besoin de meilleur profilage utilisateur dans les tests.

---

## 4. Analyse des composants serveur et des payloads RSC

Avec l'App Router, les composants dans `app/` sont des **composants serveur par défaut**. L'analyse du payload des React Server Components (RSC) est critique pour les performances.

### Vérification de la taille du payload RSC

1. Ouvrez Chrome DevTools → onglet **Network**.
2. Filtrez les requêtes par `__RSC`.
3. Cliquez sur une requête de navigation pour inspecter la réponse JSON.

Les gros payloads RSC indiquent souvent :

- Le passage d'enregistrements complets de la base de données du serveur au client.
- Une sérialisation inefficace des objets Map, Set ou circulaires.

### Détection des « fuites » de composants client

Un composant client (`'use client'`) attire toutes ses dépendances dans le bundle client.

```typescript
// app/page.tsx — Server Component (default)
import ClientHeavyChart from './ClientHeavyChart';

export default function Page() {
  return <ClientHeavyChart />;
}
```

Utilisez l'**extension Next.js VSCode** pour voir des indices (inlay hints) marquant un composant comme `"server"` ou `"client"`. Cela aide à garantir que seuls les composants interactifs portent un runtime client.

### Optimisation avec `next/dynamic`

Enveloppez les grands composants clients avec des imports dynamiques pour les charger paresseusement (lazy-load) :

```typescript
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <p>Chargement du graphique…</p>,
  ssr: false, // ignorer le rendu serveur
});

export default function Dashboard() {
  return (
    <div>
      <h1>Tableau de bord</h1>
      <HeavyChart />
    </div>
  );
}
```

Vérifiez l'effet en réexécutant l'analyseur de bundle et en recherchant le chunk étiqueté `HeavyChart`—il devrait maintenant se charger de manière asynchrone.

---

## 5. Audit d'optimisation intégré

Next.js fournit des conventions basées sur les fichiers qui sont faciles à auditer et à ajuster.

### `next/image`

Exécutez un build et recherchez les avertissements liés aux images. Chaque composant `<Image>` doit avoir :

```typescript
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // seulement pour les images au-dessus de la ligne de flottaison
/>
```

- L'absence de `width`/`height` provoque du CLS.
- L'absence de `priority` retarde le LCP pour les images hero.

### `next/font`

**Mauvais :** Charger les polices depuis un CDN externe (la requête Google Fonts bloque le rendu).

**Bon :** Utiliser `next/font` auto-héberge automatiquement le fichier de police, éliminant la requête réseau externe.

```typescript
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'] });
// => le fichier de police est mis en cache et servi depuis votre propre domaine
```

Auditez en supprimant `@import` des Google Fonts des fichiers CSS.

### `next/script` Strategy

| Stratégie             | Cas d'utilisation                             |
|----------------------|-----------------------------------------------|
| `afterInteractive`   | Analytics (par défaut)                        |
| `beforeInteractive`  | Polyfills, bannières de cookies               |
| `lazyOnload`         | Widgets de chat, contenus embarqués non critiques |
| `worker` (expérimental) | Initialisateurs coûteux                     |

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

### Lecture de la sortie du build

```bash
Route (app)                              Size     First Load JS
┌ ○ /                                    5.8 kB          86.4 kB
├ ○ /_not-found                          875 B           81.5 kB
└ λ /api/hello                           0 B             81.5 kB
```

- **○** – Statique (SSG)
- **λ** – Dynamique (SSR / ISR)
- **Size** – La taille du bundle pour cette route spécifique
- **First Load JS** – Le total JavaScript requis pour le chargement initial de cette page

Un **Size** élevé mais un **First Load JS** faible signifie que la route est bien optimisée pour le code splitting. Un **First Load JS** élevé indique que le framework partagé ou le layout nécessite une analyse.

---

## 6. Extension VS Code

L'extension officielle **Next.js VS Code** fournit un retour en temps réel sur les limites des composants et la structure des routes.

- **Limites des composants :** L'éditeur affiche une étiquette à côté de chaque composant indiquant s'il s'agit d'un composant **serveur** ou **client**.
- **Structure des routes :** La vue « Next.js: Routes » dans la barre latérale liste toutes les routes de votre application, leur stratégie de rendu et leurs paramètres dynamiques.
- **Indices de taille en ligne (version 2.0+) :** Survolez un import pour voir sa taille de bundle estimée.

```bash
# Installation depuis la ligne de commande
code --install-extension ms-vscode.vscode-nextjs
```

---

## Aide-mémoire récapitulatif

| Outil / Technique               | Objectif                                      | Commande / Configuration clé                          |
|--------------------------------|-----------------------------------------------|-------------------------------------------------------|
| `@next/bundle-analyzer`        | Visualiser la composition du bundle           | `ANALYZE=true npm run build`                          |
| Lighthouse CLI                 | Métriques runtime en laboratoire              | `npx lighthouse http://localhost:3000`                |
| PageSpeed Insights             | Données CrUX du monde réel                    | https://pagespeed.web.dev                             |
| Next.js Bundle Analysis Action | Détection de régression CI/CD                 | `.github/workflows/bundle-analysis.yml`               |
| RSC Network Analysis           | Taille du payload des composants serveur      | DevTools → Network → filter `__RSC`                   |
| Extension VS Code              | Indices de bundle et de limites de composants  | `code --install-extension ...`                        |
| Sortie `next build`            | Audit de taille et de stratégie de rendu      | `npm run build`                                       |

### Commandes supplémentaires

```bash
# Créez un nouveau projet avec l'App Router
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir

# Build de production avec sortie détaillée
npm run build

# Analyse de bundle personnalisée avec stats.json (avancé)
npx next build --profile
```

## Lectures complémentaires

- [Page npm officielle de @next/bundle-analyzer](https://www.npmjs.com/package/@next/bundle-analyzer)
- [Documentation des Web Vitals Next.js](https://nextjs.org/docs/app/building-your-application/optimizing/web-vitals)
- [Action GitHub d'analyse de bundle Next.js](https://github.com/marketplace/actions/nextjs-bundle-analysis)
- [Score de performance Lighthouse](https://developer.chrome.com/docs/lighthouse/performance/)