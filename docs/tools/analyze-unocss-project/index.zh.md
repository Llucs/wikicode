---
title: UnoCSS：一个零配置、即时编译的CSS框架
description: 详细了解UnoCSS，这是一个零配置、即时编译(JIT)的CSS框架，能够动态生成样式。学习安装、使用方法和主要功能。
created: 2026-07-08
tags:
  - UnoCSS
  - CSS-in-JS
  - JIT
  - Tailwind
  - 性能
status: 草稿
---

# UnoCSS：一个零配置、即时编译的CSS框架

UnoCSS是一个零配置、即时编译(JIT)的CSS框架，能够动态生成样式，主要用TypeScript编写。与传统的CSS-in-JS库预先处理和打包样式不同，UnoCSS在运行时根据代码中使用的类来编译样式。这种做法确保只应用必要的样式，从而减少打包大小并提高性能。

## 主要功能
1. **即时编译：** UnoCSS动态编译样式，确保只包含项目中实际使用的类。
2. **小巧的体积：** UnoCSS设计得非常轻量级，具有小的脚印，对项目性能的影响最小。
3. **树摇友好：** 生成的样式可以树摇，即在构建过程中移除未使用的样式，进一步优化最终的打包。
4. **可定制：** UnoCSS通过选项和插件进行高度定制，使其适用于各种用例。
5. **不打包样式：** 与许多CSS-in-JS库不同，UnoCSS不打包样式，这可以减少初始加载时间和提高性能。

## 安装

可以通过npm或yarn安装UnoCSS。以下是如何使用npm安装它的方法：

```bash
npm install unocss
```

或者如果你使用的是像Vite这样的框架，可以直接安装：

```bash
npm install unocss@next
```

## 基本使用

### 1. 创建配置文件

UnoCSS使用配置文件来自定义其行为。这里是一个基本的配置：

```javascript
// unocss.config.js
export default {
  theme: {},
  shortcuts: {},
  rules: [],
};
```

### 2. 将UnoCSS集成到构建工具中

根据你的构建工具，需要将UnoCSS集成进去。例如，对于Vite，可以在`vite.config.js`文件中添加：

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

### 3. 在组件中使用UnoCSS

现在可以在组件中使用UnoCSS类。例如，在一个Vue组件中：

```vue
<template>
  <div class="text-red-500 font-bold">Hello UnoCSS!</div>
</template>

<script setup>
// 无需额外设置
</script>

<style scoped>
/* 样式可以按范围限制 */
</style>
```

### 4. 生成样式

UnoCSS会根据使用的类自动生成样式。无需编写任何额外的CSS或SCSS。

## 通过命令示例查看主要功能

### 1. 自定义

通过配置文件自定义UnoCSS：

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

### 2. 诊断器

UnoCSS诊断器是一个开发调试工具，可以在源代码中提供带有位置感知的实用类分析。它随unocss和@unocss/vite一起提供。可以使用它通过访问`localhost:5173/__unocss`在Vite开发服务器中查看诊断器。诊断器允许你检查生成的CSS规则和每个文件中应用的类。它还提供了一个REPL来根据当前配置测试你的实用类。

### 3. 树摇

为了确保树摇，请配置你的构建工具以摇掉UnoCSS的输出。对于Vite，可以使用以下配置：

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

### 4. 预置

Preset Uno是一组常用的规则和快捷键的预配置。这里是如何使用它的方法：

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

## 结论

UnoCSS是一个强大的工具，用于优化现代Web应用程序中的CSS。其即时编译、轻量级以及灵活性使其成为性能关键项目的好选择。无论是大型Web应用、组件库还是静态网站，UnoCSS都可以帮助你实现更好的性能和更小的打包大小。

---