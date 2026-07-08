---
title: UnoCSS: Um Framework CSS Sem Configuração e Just-In-Time
description: Uma guia detalhado sobre o UnoCSS, um framework CSS sem configuração e Just-In-Time (JIT) que gera estilos em tempo de execução. Aprenda sobre a instalação, utilização e principais características.
created: 2026-07-08
tags:
  - UnoCSS
  - CSS-in-JS
  - JIT
  - Tailwind
  - Performance
status: draft
---

# UnoCSS: Um Framework CSS Sem Configuração e Just-In-Time

O UnoCSS é um framework CSS sem configuração e Just-In-Time (JIT) que gera estilos em tempo de execução, principalmente escrito em TypeScript. Diferentemente das bibliotecas CSS-in-JS que pré-processam e embarcam estilos, o UnoCSS compila estilos em tempo de execução com base nas classes usadas no seu código. Esta abordagem garante que apenas os estilos necessários sejam aplicados, resultando em menores tamanhos de pacote e melhor performance.

## Principais Características
1. **Compilação Just-In-Time:** O UnoCSS compila estilos em tempo de execução, garantindo que apenas as classes realmente usadas no seu projeto estejam incluídas na saída final.
2. **Pequena Tamanho:** O UnoCSS foi projetado para ser extremamente leve, com uma footprint mínima que minimiza o impacto no desempenho do seu projeto.
3. **Amigável para Shake de Árvore:** Os estilos gerados podem ser shakeados, o que significa que estilos não utilizados são removidos durante o processo de construção, otimizando ainda mais o pacote final.
4. **Personalizável:** O UnoCSS permite uma personalização extensa através de opções e plugins, tornando-o flexível para vários casos de uso.
5. **Sem Embaralhamento:** Diferentemente de muitas bibliotecas CSS-in-JS, o UnoCSS não embarca estilos, o que pode reduzir o tempo de carregamento inicial e melhorar o desempenho.

## Instalação

O UnoCSS pode ser instalado via npm ou yarn. Aqui está como você pode instalá-lo usando npm:

```bash
npm install unocss
```

Alternativamente, se você estiver usando um framework como o Vite, você pode instalá-lo diretamente:

```bash
npm install unocss@next
```

## Uso Básico

### 1. Crie um Arquivo de Configuração

O UnoCSS usa um arquivo de configuração para personalizar seu comportamento. Aqui está um exemplo básico:

```javascript
// unocss.config.js
export default {
  theme: {},
  shortcuts: {},
  rules: [],
};
```

### 2. Adicione o UnoCSS ao Seu Ferramental de Construção

Dependendo do seu ferramental de construção, você precisa integrar o UnoCSS. Por exemplo, com o Vite, você pode adicioná-lo ao arquivo `vite.config.js`:

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

### 3. Usando o UnoCSS em Seus Componentes

Você pode agora usar classes do UnoCSS em seus componentes. Por exemplo, em um componente Vue:

```vue
<template>
  <div class="text-red-500 font-bold">Olá, UnoCSS!</div>
</template>

<script setup>
// Não é necessário nenhuma configuração adicional
</script>

<style scoped>
/* Estilos podem ser escopados como usualmente */
</style>
```

### 4. Geração de Estilos

O UnoCSS gera automaticamente estilos com base nas classes usadas. Você não precisa escrever nenhum estilo adicional ou SCSS.

## Principais Características com Exemplos de Comandos

### 1. Personalização

Personalize o UnoCSS através do arquivo de configuração:

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

O Inspector do UnoCSS é uma ferramenta de depuração de desenvolvimento que fornece análise posicionada de classes utilitárias em código-fonte. Ele vem integrado com o unocss e @unocss/vite. Você pode usá-lo visitando `localhost:5173/__unocss` em seu servidor de desenvolvimento Vite para ver o Inspector. O Inspector permite que você inspeccione as regras de CSS geradas e as classes aplicadas para cada arquivo. Também fornece um REPL para testar suas utilidades com base na sua configuração atual.

### 3. Shake de Árvore

Para garantir o shake de árvore, você pode configurar seu ferramental de construção para shakear a saída do UnoCSS. Para o Vite, você pode usar a seguinte configuração:

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

O Preset Uno é um conjunto pré-configurado de regras e shortcuts comumente utilizados. Aqui está como usá-lo:

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

## Conclusão

O UnoCSS é uma ferramenta potente para otimizar CSS em aplicativos web modernos. Sua compilação Just-In-Time, pequena natureza e flexibilidade o tornam uma ótima escolha para projetos de alta performance. Seja você trabalhando em um grande aplicativo web, uma biblioteca de componentes ou um site estático, o UnoCSS pode ajudá-lo a alcançar melhores performance e menores tamanhos de pacote.

---