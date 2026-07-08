---
title: UnoCSS: A Zero-Config, Just-In-Time CSS Framework
description: A detailed guide to UnoCSS, a zero-config, Just-In-Time (JIT) CSS framework that generates styles on the fly. Learn installation, usage, and key features.
created: 2026-07-08
tags:
  - UnoCSS
  - CSS-in-JS
  - JIT
  - Tailwind
  - Performance
status: draft
---

# UnoCSS: A Zero-Config, Just-In-Time CSS Framework

UnoCSS is a zero-config, Just-In-Time (JIT) CSS framework that generates styles on the fly, primarily written in TypeScript. Unlike traditional CSS-in-JS libraries that pre-process and bundle styles, UnoCSS compiles styles at runtime based on the classes used in your code. This approach ensures that only the necessary styles are applied, leading to reduced bundle sizes and improved performance.

## Key Features
1. **Just-In-Time Compilation:** UnoCSS compiles styles on the fly, ensuring that only the classes actually used in your project are included in the final output.
2. **Tiny Size:** UnoCSS is designed to be extremely lightweight, with a small footprint that minimizes the impact on your project's performance.
3. **Tree-Shaking Friendly:** The generated styles can be tree-shaken, meaning unused styles are removed during the build process, further optimizing the final bundle.
4. **Customizable:** UnoCSS allows extensive customization through options and plugins, making it flexible for various use cases.
5. **No Bundling:** Unlike many CSS-in-JS libraries, UnoCSS does not bundle styles, which can reduce initial load times and improve performance.

## Installation

UnoCSS can be installed via npm or yarn. Here’s how you can install it using npm:

```bash
npm install unocss
```

Alternatively, if you are using a framework like Vite, you can install it directly:

```bash
npm install unocss@next
```

## Basic Usage

### 1. Create a Configuration File

UnoCSS uses a configuration file to customize its behavior. Here’s a basic configuration:

```javascript
// unocss.config.js
export default {
  theme: {},
  shortcuts: {},
  rules: [],
};
```

### 2. Add UnoCSS to Your Build Tool

Depending on your build tool, you need to integrate UnoCSS. For example, with Vite, you can add it to the `vite.config.js` file:

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

### 3. Using UnoCSS in Your Components

You can now use UnoCSS classes in your components. For example, in a Vue component:

```vue
<template>
  <div class="text-red-500 font-bold">Hello UnoCSS!</div>
</template>

<script setup>
// No additional setup required
</script>

<style scoped>
/* Styles can be scoped as usual */
</style>
```

### 4. Generating Styles

UnoCSS automatically generates styles based on the classes used. You don’t need to write any additional CSS or SCSS.

## Key Features with Command Examples

### 1. Customization

Customize UnoCSS through the configuration file:

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

The UnoCSS Inspector is a development debugging tool that provides position-aware analysis of utility classes in source code. It ships with unocss and @unocss/vite. You can use it by visiting `localhost:5173/__unocss` in your Vite dev server to see the inspector. The inspector allows you to inspect the generated CSS rules and the applied classes for each file. It also provides a REPL to test your utilities based on your current configuration.

### 3. Tree-Shaking

To ensure tree-shaking, you can configure your build tool to tree-shake the UnoCSS output. For Vite, you can use the following configuration:

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

### 4. Preset

Preset Uno is a pre-configured set of rules and shortcuts that are commonly used. Here’s how to use it:

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

UnoCSS is a powerful tool for optimizing CSS in modern web applications. Its Just-In-Time compilation, lightweight nature, and flexibility make it a great choice for performance-critical projects. Whether you are working on a large-scale web application, a component library, or a static site, UnoCSS can help you achieve better performance and smaller bundle sizes.

---