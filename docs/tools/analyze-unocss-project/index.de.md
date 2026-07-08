---
title: UnoCSS: Ein Zero-Config, Just-In-Time CSS-Framework
description: Ein detaillierter Leitfaden zu UnoCSS, einem zero-config, Just-In-Time (JIT) CSS-Framework, das Styles im Laufzeitbetrieb generiert. Erfahren Sie die Installation, die Nutzung und die wichtigsten Funktionen.
created: 2026-07-08
tags:
  - UnoCSS
  - CSS-in-JS
  - JIT
  - Tailwind
  - Leistung
status: draft
---

# UnoCSS: Ein Zero-Config, Just-In-Time CSS-Framework

UnoCSS ist ein zero-config, Just-In-Time (JIT) CSS-Framework, das Styles im Laufzeitbetrieb generiert und wird hauptsächlich in TypeScript geschrieben. Im Gegensatz zu traditionellen CSS-in-JS-Bibliotheken, die Styles vorverarbeiten und bundeln, kompiliert UnoCSS Styles laufzeitabhängig auf der Grundlage der in Ihrem Code verwendeten Klassen. Diese Ansatzgarantiert, dass nur die notwendigen Styles angewendet werden, was zu kleineren Bundle-Größen und verbesserte Leistung führt.

## Wichtige Funktionen
1. **Just-In-Time-Kompilierung:** UnoCSS kompiliert Styles im Laufzeitbetrieb, was bedeutet, dass nur die in Ihrem Projekt tatsächlich verwendeten Klassen in der endgültigen Ausgabe enthalten sind.
2. **Klein formatiert:** UnoCSS ist mit einem kleinen Profil konzipiert, das die Auswirkungen auf die Leistung Ihres Projekts minimiert.
3. **Tree-Shaking-Freundlich:** Die generierten Styles können tree-shaken werden, was bedeutet, dass nicht verwendete Styles während des Build-Prozesses entfernt werden und somit die endgültige Bundle-Größe optimiert wird.
4. **Anpassbar:** UnoCSS erlaubt eine umfangreiche Anpassung durch Optionen und Plugins, was es für verschiedene Anwendungsfälle flexibel macht.
5. **Keine Bundling:** Im Gegensatz zu vielen CSS-in-JS-Bibliotheken kompiliert UnoCSS keine Styles, was die Anfangsladetime und die Leistung reduziert.

## Installation

UnoCSS kann über npm oder yarn installiert werden. Hier ist, wie Sie es mit npm installieren:

```bash
npm install unocss
```

Alternativ, wenn Sie eine Framework wie Vite verwenden, können Sie es direkt installieren:

```bash
npm install unocss@next
```

## Grundlegende Nutzung

### 1. Erstellen eines Konfigurationsdatei

UnoCSS verwendet eine Konfigurationsdatei, um seine Verhaltensweisen anzupassen. Hier ist eine grundlegende Konfiguration:

```javascript
// unocss.config.js
export default {
  theme: {},
  shortcuts: {},
  rules: [],
};
```

### 2. Fügen Sie UnoCSS zu Ihrem Build Tool hinzu

Abhängig von Ihrem Build Tool müssen Sie UnoCSS integrieren. Zum Beispiel in Vite können Sie es im `vite.config.js` Datei hinzufügen:

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

### 3. Verwenden von UnoCSS in Ihren Komponenten

Sie können UnoCSS-Klassen jetzt in Ihren Komponenten verwenden. Zum Beispiel in einem Vue-Komponenten:

```vue
<template>
  <div class="text-red-500 font-bold">Hallo UnoCSS!</div>
</template>

<script setup>
// Keine zusätzliche Konfiguration erforderlich
</script>

<style scoped>
/* Styles können wie üblich abgegrenzt werden */
</style>
```

### 4. Generierung von Styles

UnoCSS generiert Styles automatisch basierend auf den Klassen, die verwendet werden. Sie müssen keine zusätzliche CSS oder SCSS schreiben.

## Wichtige Funktionen mit Befehlssyntax Beispielen

### 1. Anpassung

Anpassen von UnoCSS durch die Konfigurationsdatei:

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

Der UnoCSS Inspector ist ein Entwicklungsdebugging-Tool, das eine positionssensibele Analyse von Nutzungsklassen in Quellcode bereitstellt. Es schippert mit unocss und @unocss/vite. Sie können es durch Besuch von `localhost:5173/__unocss` im Vite Entwicklungs-Server verwenden, um den Inspector zu sehen. Der Inspector ermöglicht es, die generierten CSS-Regeln und die angewandten Klassen für jedes Datei zu inspecten. Er bietet auch einen REPL, um Ihre Utilities basierend auf Ihrer aktuellen Konfiguration zu testen.

### 3. Tree-Shaking

Um Tree-Shaking zu sicherzustellen, können Sie Ihren Build Tool konfigurieren, um das UnoCSS-Output tree-shaking zu ermöglichen. Für Vite können Sie das folgende Konfiguration verwenden:

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

### 4. Vordefiniert

Preset Uno ist eine vordefinierte Kombination von Regeln und Shortcuts, die in der Regel verwendet werden. Hier ist, wie Sie es verwenden:

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

## Zusammenfassung

UnoCSS ist ein mächtiges Tool, um CSS in modernen Webanwendungen zu optimieren. Seine Just-In-Time-Kompilierung, seine leichtgewichtige Natur und seine Flexibilität machen es eine großartige Wahl für Leistungscritical-Projekte. Unabhängig davon, ob Sie an einer großen Anwendung, einem Komponentenlibrary oder einer statischen Seite arbeiten, kann UnoCSS Ihnen helfen, bessere Leistung und kleinere Bundle-Größen zu erreichen.

---