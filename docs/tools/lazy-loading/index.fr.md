---
title: Chargement différé
description: Un guide complet sur le chargement différé – une technique d'optimisation des performances qui diffère le chargement des ressources non critiques jusqu'à ce qu'elles soient nécessaires.
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

**Lazy loading** est un modèle de conception et une stratégie d'optimisation qui retarde le chargement, l'initialisation ou le rendu d'une ressource jusqu'à ce qu'elle soit réellement nécessaire. Dans le développement web, cela signifie généralement différer le téléchargement d'images, d'iframes, de scripts ou de bundles JavaScript jusqu'à ce qu'ils entrent dans le viewport de l'utilisateur ou soient déclenchés par une interaction. En réduisant la quantité de travail effectué lors du chargement initial de la page, le lazy loading améliore considérablement le temps de démarrage, réduit la consommation de bande passante et diminue l'empreinte mémoire.

---

## Pourquoi utiliser le lazy loading?

| Avantage | Description |
|---------|-------------|
| **Chargement initial plus rapide** | Seules les ressources critiques au-dessus de la ligne de flottaison sont chargées en premier. |
| **Bande passante réduite** | Les ressources non visibles ne sont pas téléchargées tant que l'utilisateur n'a pas fait défiler jusqu'à elles. |
| **Utilisation mémoire réduite** | Les éléments inutilisés (par exemple, les images hors écran) ne sont pas conservés en mémoire. |
| **Meilleurs Core Web Vitals** | Un lazy loading approprié peut améliorer le Largest Contentful Paint (LCP) en évitant les requêtes concurrentes. |
| **Expérience utilisateur améliorée** | Les pages deviennent interactives plus tôt et le défilement est plus fluide lorsque le contenu hors écran se charge progressivement. |

---

## Techniques fondamentales et approches

### 1. Native Lazy Loading (attribut HTML `loading`)

Depuis Chrome 76 (2019) et avec une prise en charge complète des navigateurs à partir de 2023, l'attribut `loading` peut être appliqué aux éléments `<img>` et `<iframe>` sans aucun JavaScript.

```html
<img src="photo.jpg" loading="lazy" alt="Description" width="800" height="600">
<iframe src="widget.html" loading="lazy"></iframe>
```

**Bonnes pratiques :** Fournissez toujours des attributs `width` et `height` explicites (ou un `aspect-ratio` CSS) pour éviter le Cumulative Layout Shift (CLS).

### 2. API Intersection Observer

Une API navigateur puissante qui détecte efficacement quand un élément devient visible. Elle remplace les écouteurs d'événements de défilement manuels et est la base de la plupart des bibliothèques modernes de lazy loading.

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

### 3. Code splitting et import dynamique `import()`

Pour les applications JavaScript, le lazy loading signifie diviser le bundle en morceaux plus petits qui sont chargés à la demande. Les bundlers modernes (Webpack, Rollup, Vite) prennent en charge cela nativement.

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

**Fonctionnement :** Le module `./HeavyComponent` est un fichier séparé qui n'est récupéré que lorsque `<HeavyComponent>` est rendu. `React.lazy` gère automatiquement l'état de chargement avec `Suspense`.

### 4. Lazy loading dans le backend / ORM

Le lazy loading n'est pas seulement un concept frontend. Les ORM tels que Hibernate (Java), SQLAlchemy (Python) et Entity Framework (.NET) permettent de différer le chargement des objets liés jusqu'à ce qu'ils soient accédés.

```python
# SQLAlchemy example — lazy='select' (default)
user = session.query(User).get(1)
# The 'addresses' relationship is loaded only when accessed:
print(user.addresses)  # A separate SQL query is executed
```

**Attention :** Une utilisation inappropriée (par exemple, accéder à une relation lazy dans une boucle) peut conduire au problème de requêtes N+1. Dans ce cas, utilisez le chargement impatient (`joinedload`, `subqueryload`) ou le chargement par lots.

### 5. Défilement virtuel / Windowing

Pour les très grandes listes (flux de défilement infini, tableaux de données), ne rendez que les lignes visibles. Les bibliothèques comme `react-window`, `react-virtualized` et `@tanstack/react-virtual` implémentent ce modèle.

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

## Installation et configuration

| Approche | Installation | Remarques |
|----------|--------------|-------|
| **HTML natif** | Aucune | Détection de fonctionnalité : `'loading' in HTMLImageElement.prototype` |
| **Intersection Observer** | Aucune (API navigateur native) | Polyfill disponible pour les navigateurs très anciens |
| **Lazysizes (bibliothèque classique)** | `npm install lazysizes@5` | Utilisez la classe CSS `lazyload` avec `data-src` |
| **Lozad.js** | `npm install lozad` | Léger (1 Ko) avec Intersection Observer |
| **React/Vue/Angular** | Built‑in (`React.lazy`, Vue Async Components, Angular `loadChildren`) | Aucune dépendance supplémentaire |
| **ORM de bases de données** | Partie intégrante de l'ORM | Consultez la documentation de votre ORM |

---

## Bonnes pratiques et fonctionnalités clés

- **Spécifiez toujours les dimensions** des médias chargés avec lazy loading pour réserver l'espace et éviter les changements de mise en page.
- **Utilisez le lazy loading uniquement pour le contenu non critique** – les images hero, les éléments au-dessus de la ligne de flottaison et le composant de route initial doivent être chargés immédiatement.
- **Utilisez le `loading="lazy"` natif lorsque c'est possible** – il est sans coût, bien supporté et accessible aux moteurs de recherche.
- **Combinez avec des images responsives** – utilisez `srcset` et `sizes` pour charger la taille d'image correcte pour le viewport.
- **Implémentez des solutions de repli** – pour les navigateurs qui ne supportent pas le lazy loading natif, utilisez un repli basé sur Intersection Observer (les bibliothèques comme lazysizes gèrent cela automatiquement).
- **Mesurez l'impact** – utilisez Lighthouse, le panneau Réseau des outils de développement Chrome et les rapports Core Web Vitals pour vérifier que le lazy loading améliore réellement les performances (il peut être contre-productif pour les images proches du viewport).

---

## Mises en garde et écueils

| Problème | Explication | Solution |
|-------|-------------|----------|
| **SEO concerns** | Les robots d'indexation peuvent ne pas attendre que JavaScript charge les images. | Le `loading="lazy"` natif est respecté par les principaux moteurs de recherche. Pour les solutions basées sur JS, envisagez le rendu côté serveur ou des balises `<noscript>`. |
| **Cumulative Layout Shift (CLS)** | Si les dimensions ne sont pas définies, la mise en page saute lorsque l'image se charge. | Définissez toujours `width` et `height` ou utilisez le `aspect-ratio` CSS. |
| **N+1 queries** | Le lazy loading dans les ORM peut générer une requête distincte pour chaque accès à une relation. | Utilisez le chargement impatient (`joinedload`, `selectinload`, `include`) lorsque vous savez que vous aurez besoin des données liées. |
| **Delayed interaction** | Le chargement en lazy de bibliothèques lourdes au clic peut provoquer un délai notable. | Préchargez le morceau avec `<link rel="preload">` ou utilisez un petit placeholder pendant le chargement. |
| **Scroll thrashing** | L'écoute manuelle des événements de défilement (sans débouncing) est coûteuse. | Utilisez plutôt Intersection Observer – il est découplé du cycle de défilement. |

---

## Pour en savoir plus

- [MDN Web Docs: Lazy loading](https://developer.mozilla.org/en-US/docs/Web/Performance/Lazy_loading)
- [web.dev: Lazy loading images and video](https://web.dev/articles/lazy-loading-images)
- [MDN: Intersection Observer API](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)
- [React.lazy and Suspense](https://react.dev/reference/react/lazy)
- [Core Web Vitals & Lazy Loading](https://web.dev/articles/lcp-lazy-loading)