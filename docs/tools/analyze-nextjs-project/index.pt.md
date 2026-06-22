---
title: Analisando Bundles e Performance de Projetos Next.js
description: Um guia completo para analisar e otimizar a performance de aplicações Next.js usando `@next/bundle-analyzer`, Lighthouse, verificações CI/CD e ferramentas de perfilamento em tempo de execução.
created: 2026-06-22
tags:
  - nextjs
  - performance
  - bundler
  - optimization
  - profiling
status: draft
---

# Análise de Projetos Next.js: Bundles, Performance e Otimização

## O que é Análise de Projetos Next.js?

Next.js é um framework React para construir aplicações web full-stack com renderização no servidor (SSR), geração de sites estáticos (SSG) e regeneração estática incremental (ISR). Analisar um projeto Next.js envolve avaliar a composição e o tamanho dos bundles JavaScript gerados, métricas de performance em tempo de execução (Web Vitals), eficiência da estratégia de renderização e padrões de busca de dados.

Uma análise eficaz ajuda os desenvolvedores a identificar dependências superdimensionadas, reduzir o tempo de execução do JavaScript, otimizar estratégias de cache e prevenir regressões de performance antes que o código chegue à produção.

## Por que Analisar um Projeto Next.js?

- **Identificar dependências superdimensionadas:** Expor visualmente quais pacotes inflam os tamanhos dos bundles (por exemplo, substituir `moment.js` por `date-fns` após descobrir que ele representa 30% de uma rota).
- **Prevenir regressão de bundle:** A análise automatizada em CI/CD detecta inchaço acidental introduzido por pull requests.
- **Otimizar as Core Web Vitals:** Lighthouse e CrUX (Chrome User Experience Report) revelam gargalos em Largest Contentful Paint (LCP), Total Blocking Time (TBT) e Cumulative Layout Shift (CLS).
- **Refinar estratégias de renderização:** Determinar se uma rota deve ser gerada estaticamente (SSG), renderizada no servidor (SSR) ou regenerada sob demanda (ISR) com base nas dependências de dados e tamanhos dos bundles.

## Pré-requisitos

- Node.js 20.x ou superior
- Um projeto Next.js (App Router ou Pages Router)
- Git (para análise em CI/CD)
- Familiaridade básica com `npm` / `yarn` / `pnpm`

---

## 1. Análise de Tamanho de Bundle com `@next/bundle-analyzer`

`@next/bundle-analyzer` é o plugin oficial que integra o `webpack-bundle-analyzer` no pipeline de build do Next.js. Ele gera mapas interativos (treemaps) que visualizam a composição dos seus bundles do cliente e do servidor.

### Instalação

```bash
npm install --save-dev @next/bundle-analyzer
```

### Configuração

Envolva seu `next.config` com o plugin, habilitando a análise condicionalmente por meio de uma variável de ambiente.

```javascript
// next.config.mjs
import withBundleAnalyzer from '@next/bundle-analyzer';

const config = withBundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
})({});

export default config;
```

### Uso

Execute o build com a flag `ANALYZE`:

```bash
ANALYZE=true npm run build
```

Após o build, abra os arquivos HTML estáticos gerados no diretório `.next/analyze/`. Cada rota produz um treemap mostrando:

- **Stat size** – tamanho bruto do módulo no disco
- **Parsed size** – tamanho após a transformação com Babel / SWC
- **Gzip size** – tamanho após compressão

### Principais Funcionalidades

- **Bundles do cliente e do servidor:** Visualizações separadas para cada destino de renderização.
- **Aprofundamento:** Clique em qualquer retângulo para explodir o módulo em suas importações constituintes.
- **Suporte a Turbopack:** A partir do Next.js 15.3+, o plugin também funciona com o bundler Turbopack (use `next build --turbo` para habilitar).
- **Filtragem:** Isole rapidamente dependências de terceiros vs. código da aplicação.

```bash
# Exemplo: encontre o impacto de tamanho de uma biblioteca específica
# Abra o treemap, use o campo de busca para localizar 'lodash' ou 'chart.js'
```

### Interpretando a Saída

Procure pelos retângulos maiores. Alvos comuns de otimização incluem:

- **Bibliotecas utilitárias grandes** (`lodash`, `moment`) – prefira alternativas que suportem tree-shaking.
- **Componentes de gráficos pesados** – importação dinâmica via `next/dynamic`.
- **Módulos duplicados entre chunks** – configure a deduplicação do Webpack ou migre para um módulo compartilhado.

---

## 2. Verificações de Regressão de Bundle em CI/CD

A **Next.js Bundle Analysis** GitHub Action compara automaticamente os tamanhos dos bundles do branch do PR com o branch base e publica um comentário legível.

### Configuração

Crie `.github/workflows/bundle-analysis.yml`:

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

### Principais Funcionalidades

- **Comparação por rota:** Mostra deltas de tamanho para cada rota compilada.
- **Gráficos históricos:** Acompanha o tamanho do bundle ao longo do tempo.
- **Orçamentos de performance:** Configure um limite máximo de tamanho por rota; a ação pode falhar a verificação de CI se um orçamento for excedido.

### Usando Orçamentos de Performance

Adicione um arquivo `bundle-budgets.json` na raiz do seu repositório:

```json
{
  "budget": 250000,
  "mode": "maxSize"
}
```

A ação falhará o PR se qualquer rota exceder 250 KB (gzip).

---

## 3. Auditoria em Tempo de Execução com Lighthouse e CrUX

### Gerando um Relatório Lighthouse

Compile e inicie seu servidor de produção localmente:

```bash
npm run build && npm run start
```

Execute o Lighthouse CLI ou use a aba Lighthouse do Chrome DevTools em `http://localhost:3000`.

```bash
npx lighthouse http://localhost:3000 --view --preset=desktop
```

### Métricas Chave para Next.js

| Métrica              | Impacto Específico no Next.js                                        |
|----------------------|----------------------------------------------------------------------|
| **Total Blocking Time (TBT)** | TBT alto indica JavaScript excessivo bloqueando a thread principal. Reduza com code-splitting e encolhimento dos bundles. |
| **Largest Contentful Paint (LCP)** | Frequentemente dominado por imagens hero. Verifique `next/image` com `width`/`height` explícitos. |
| **Cumulative Layout Shift (CLS)** | Geralmente causado por anúncios, embeds ou conteúdo injetado dinamicamente sem dimensões. Use `next/font` para eliminar CLS relacionado a fontes. |
| **First Input Delay (FID)** | Diretamente correlacionado à quantidade de JavaScript no carregamento inicial. Bundles menores = melhor FID. |

### Usando PageSpeed Insights / CrUX

Enquanto o Lighthouse fornece um **ambiente de laboratório**, o PageSpeed Insights utiliza **dados de campo** de usuários reais por meio do Chrome User Experience Report (CrUX). Combine ambos para identificar discrepâncias entre testes sintéticos e experiências reais dos usuários.

- **Problema de laboratório ≠ Problema de campo:** Um resultado lento no laboratório pode não corresponder à performance real se a maioria dos usuários tiver dispositivos rápidos.
- **Problema de campo ≠ Problema de laboratório:** FID alto no campo, mas TBT baixo no laboratório sugere a necessidade de melhor perfilamento de usuários nos testes.

---

## 4. Análise de Componentes Servidor e Payload RSC

Com o App Router, componentes em `app/` são **Componentes Servidor por padrão**. Analisar o payload dos React Server Components (RSC) é crítico para performance.

### Verificando o Tamanho do Payload RSC

1. Abra o Chrome DevTools → aba **Network**.
2. Filtre as requisições por `__RSC`.
3. Clique em uma requisição de navegação para inspecionar a resposta JSON.

Payloads RSC grandes frequentemente indicam:

- Passagem de registros completos do banco de dados do servidor para o cliente.
- Serialização ineficiente de Map, Set ou objetos circulares.

### Detectando "Vazamentos" de Componentes Cliente

Um Componente Cliente (`'use client'`) puxa todas as suas dependências para o bundle do cliente.

```typescript
// app/page.tsx — Server Component (default)
import ClientHeavyChart from './ClientHeavyChart';

export default function Page() {
  return <ClientHeavyChart />;
}
```

Use a **Extensão VS Code do Next.js** para ver dicas in-line marcando um componente como `"server"` ou `"client"`. Isso ajuda a garantir que apenas componentes interativos carreguem um runtime do cliente.

### Otimizando com `next/dynamic`

Empacote componentes cliente grandes com importações dinâmicas para carregá-los com lazy load:

```typescript
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <p>Carregando gráfico…</p>,
  ssr: false, // ignorar renderização no servidor
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

Verifique o efeito executando novamente o analisador de bundle e procurando pelo chunk nomeado `HeavyChart`—ele agora deve carregar assincronamente.

---

## 5. Auditoria de Otimização Integrada

O Next.js fornece convenções baseadas em arquivos que são fáceis de auditar e ajustar.

### `next/image`

Execute um build e procure por avisos relacionados a imagens. Cada componente `<Image>` deve ter:

```typescript
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // apenas para imagens acima da dobra
/>
```

- A falta de `width`/`height` causa CLS.
- A falta de `priority` atrasa o LCP para imagens hero.

### `next/font`

**Ruim:** Carregar fontes de um CDN externo (a requisição do Google Fonts bloqueia a renderização).

**Bom:** Usar `next/font` automaticamente hospeda o arquivo de fonte localmente, eliminando a requisição externa de rede.

```typescript
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'] });
// => o arquivo de fonte é armazenado em cache e servido a partir do seu próprio domínio
```

Audite removendo `@import` de Google Fonts dos arquivos CSS.

### `next/script` Strategy

| Estratégia             | Caso de Uso                             |
|------------------------|-----------------------------------------|
| `afterInteractive`     | Analytics (padrão)                      |
| `beforeInteractive`    | Polyfills, banners de cookies           |
| `lazyOnload`           | Widgets de chat, embeds não críticos    |
| `worker` (experimental) | Inicializadores pesados                 |

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

### Lendo a Saída do Build

```bash
Route (app)                              Size     First Load JS
┌ ○ /                                    5.8 kB          86.4 kB
├ ○ /_not-found                          875 B           81.5 kB
└ λ /api/hello                           0 B             81.5 kB
```

- **○** – Static (SSG)
- **λ** – Dynamic (SSR / ISR)
- **Size** – O tamanho do bundle para aquela rota específica
- **First Load JS** – O JavaScript total necessário para o carregamento inicial daquela página

Um **Size** alto mas **First Load JS** baixo significa que a rota está bem otimizada para code splitting. Um **First Load JS** alto indica que o framework compartilhado ou layout precisa de análise.

---

## 6. Extensão VS Code

A extensão oficial **Next.js VS Code** fornece feedback em tempo real sobre limites de componentes e estrutura de rotas.

- **Limites de componentes:** O editor exibe um rótulo ao lado de cada componente indicando se ele é um componente **servidor** ou **cliente**.
- **Estrutura de rotas:** A visualização "Next.js: Routes" na barra lateral lista todas as rotas do seu app, sua estratégia de renderização e parâmetros dinâmicos.
- **Dicas de tamanho inline (versão 2.0+):** Passe o mouse sobre uma importação para ver o tamanho estimado do bundle.

```bash
# Instalar a partir da linha de comando
code --install-extension ms-vscode.vscode-nextjs
```

---

## Resumo (Cheatsheet)

| Ferramenta / Técnica               | Propósito                                      | Comando / Configuração Chave                              |
|------------------------------------|------------------------------------------------|-----------------------------------------------------------|
| `@next/bundle-analyzer`            | Visualizar a composição do bundle              | `ANALYZE=true npm run build`                              |
| Lighthouse CLI                     | Métricas de runtime em laboratório             | `npx lighthouse http://localhost:3000`                    |
| PageSpeed Insights                 | Dados reais do CrUX                            | https://pagespeed.web.dev                                 |
| Next.js Bundle Analysis Action     | Detecção de regressão em CI/CD                 | `.github/workflows/bundle-analysis.yml`                   |
| Análise de Rede RSC                | Tamanho do payload de componentes servidor     | DevTools → Network → filtrar `__RSC`                      |
| Extensão VS Code                   | Dicas de bundle e limites de componentes no editor | `code --install-extension ...`                        |
| Saída do `next build`              | Auditoria de tamanho e estratégia por rota     | `npm run build`                                           |

### Comandos Adicionais

```bash
# Scaffold de um novo projeto com App Router
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir

# Build de produção com saída detalhada
npm run build

# Análise customizada de bundle com stats.json (avançado)
npx next build --profile
```

## Leitura Adicional

- [Página oficial do @next/bundle-analyzer no npm](https://www.npmjs.com/package/@next/bundle-analyzer)
- [Documentação de Web Vitals do Next.js](https://nextjs.org/docs/app/building-your-application/optimizing/web-vitals)
- [Next.js Bundle Analysis GitHub Action](https://github.com/marketplace/actions/nextjs-bundle-analysis)
- [Pontuação de Performance do Lighthouse](https://developer.chrome.com/docs/lighthouse/performance/)