---
title: UnoCSS : Un Framework CSS Zero-Config, Just-In-Time
description: Un guide détaillé sur UnoCSS, un framework CSS zero-config, Just-In-Time (JIT) qui génère des styles en temps réel. Apprenez l'installation, l'utilisation et les fonctionnalités clés.
created: 2026-07-08
tags:
  - UnoCSS
  - CSS-in-JS
  - JIT
  - Tailwind
  - Performance
status: brouillon
---

# UnoCSS : Un Framework CSS Zero-Config, Just-In-Time

UnoCSS est un framework CSS zero-config, Just-In-Time (JIT) qui génère des styles en temps réel, principalement écrit en TypeScript. Contrairement aux bibliothèques CSS-in-JS traditionnelles qui pré-traitent et paclent les styles, UnoCSS compile les styles au moment de l'exécution en fonction des classes utilisées dans votre code. Cette approche assure que seules les styles nécessaires sont appliquées, ce qui réduit les tailles des paquets et améliore la performance.

## Fonctionnalités Clés
1. **Compilation Just-In-Time :** UnoCSS compile les styles en temps réel, en s'assurant que seules les classes réellement utilisées dans votre projet sont incluses dans la sortie finale.
2. **Taille Minimale :** UnoCSS est conçu pour être extrêmement léger, avec un empreinte minimale qui réduit l'impact sur la performance de votre projet.
3. **Ami de Tree-Shaking :** Les styles générés peuvent être tree-shaken, ce qui signifie que les styles non utilisés sont supprimés lors du processus de construction, optimisant ainsi le paquet final.
4. **Personnalisable :** UnoCSS permet une personnalisation extensive via des options et des plugins, ce qui le rend flexible pour diverses utilisations.
5. **Aucun Paclage :** Contrairement à de nombreuses bibliothèques CSS-in-JS, UnoCSS ne paclle pas les styles, ce qui peut réduire le temps de chargement initial et améliorer la performance.

## Installation

UnoCSS peut être installé via npm ou yarn. Voici comment l'installer avec npm :

```bash
npm install unocss
```

Alternativement, si vous utilisez un framework comme Vite, vous pouvez l'installer directement :

```bash
npm install unocss@next
```

## Utilisation de Base

### 1. Création d'un Fichier de Configuration

UnoCSS utilise un fichier de configuration pour personnaliser son comportement. Voici un exemple de configuration de base :

```javascript
// unocss.config.js
export default {
  theme: {},
  shortcuts: {},
  rules: [],
};
```

### 2. Intégration de UnoCSS à Votre Outil de Construction

Selon votre outil de construction, vous devez intégrer UnoCSS. Par exemple, avec Vite, vous pouvez l'ajouter au `vite.config.js` :

```javascript
import { defineConfig } from 'vite';
import unocss from 'unocss';
import { presetUno } from 'unocss';

export default defineConfig({
  plugins: [
    unocss({
      preset: presetUno(),
    }),
  ],
});
```

### 3. Utilisation de UnoCSS dans Vos Composants

Vous pouvez maintenant utiliser les classes UnoCSS dans vos composants. Par exemple, dans un composant Vue :

```vue
<template>
  <div class="text-red-500 font-bold">Hello UnoCSS!</div>
</template>

<script setup>
// Aucune configuration supplémentaire nécessaire
</script>

<style scoped>
/* Les styles peuvent être liés comme d'habitude */
</style>
```

### 4. Génération de Styles

UnoCSS génère automatiquement des styles en fonction des classes utilisées. Vous n'avez pas besoin d'écrire de CSS ou de SCSS supplémentaires.

## Fonctionnalités Clés avec des Exemples de Commandes

### 1. Personnalisation

Personnalisez UnoCSS via le fichier de configuration :

```javascript
// unocss.config.js
export default {
  theme: {
    colors: {
      primary: '#007bff',
    },
  },
  shortcuts: {
    'btn-primary': 'text-white bg-primary p-2 rounded',
  },
  rules: [
    ['hover:bg-red-500', ':hover'],
  ],
};
```

### 2. Inspector

L'Inspector UnoCSS est un outil de débogage de développement qui fournit une analyse positionnée des classes utilitaires dans le code source. Il est fourni avec unocss et @unocss/vite. Vous pouvez utiliser l'inspecteur en visitant `localhost:5173/__unocss` dans votre serveur de développement Vite pour voir l'inspecteur. L'inspecteur vous permet d'examiner les règles CSS générées et les classes appliquées pour chaque fichier. Il fournit également un REPL pour tester vos utilitaires basés sur votre configuration actuelle.

### 3. Tree-Shaking

Pour assurer le Tree-Shaking, vous pouvez configurer votre outil de construction pour tree-shaker les sorties UnoCSS. Pour Vite, vous pouvez utiliser la configuration suivante :

```javascript
import unocss from 'unocss';

export default defineConfig({
  plugins: [
    unocss({
      preset: presetUno(),
      treeShake: true,
    }),
  ],
});
```

### 4. Pré-configuration

La Pré-configuration UnoCSS est un ensemble pré-configuré de règles et de raccourcis couramment utilisés. Voici comment l'utiliser :

```javascript
import { presetUno } from 'unocss';

export default defineConfig({
  plugins: [
    unocss({
      preset: presetUno(),
    }),
  ],
});
```

## Conclusion

UnoCSS est un outil puissant pour optimiser le CSS dans les applications web modernes. Sa compilation Just-In-Time, sa nature légère et sa flexibilité en font un excellent choix pour les projets à haute performance. Que vous travailliez sur une application web à grande échelle, une bibliothèque de composants ou un site statique, UnoCSS peut vous aider à obtenir des tailles de paquet plus petites et des performances améliorées.

---