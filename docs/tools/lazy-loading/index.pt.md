---
title: Carregamento Preguiçoso
description: Um guia abrangente sobre carregamento preguiçoso – uma técnica de otimização de desempenho que adia o carregamento de recursos não críticos até que sejam necessários.
created: 2026-06-20
tags:
  - performance
  - optimization
  - javascript
  - web-development
  - code-splitting
status: draft
---

# Carregamento Preguiçoso

**Carregamento preguiçoso** é um padrão de design e estratégia de otimização que atrasa o carregamento, a inicialização ou a renderização de um recurso até que ele seja realmente necessário. No desenvolvimento web, isso normalmente significa adiar a obtenção de imagens, iframes, scripts ou pacotes JavaScript até que eles entrem na janela de visualização do usuário ou sejam acionados por uma interação. Ao reduzir a quantidade de trabalho realizada durante o carregamento inicial da página, o carregamento preguiçoso melhora significativamente o tempo de inicialização, reduz o consumo de largura de banda e diminui a pegada de memória.

---

## Por que usar carregamento preguiçoso?

| Benefício | Descrição |
|-----------|----------|
| **Carregamento inicial mais rápido** | Apenas recursos críticos acima da dobra são carregados primeiro. |
| **Largura de banda reduzida** | Recursos não visíveis não são baixados até que o usuário role até eles. |
| **Menor uso de memória** | Elementos não utilizados (por exemplo, imagens fora da tela) não são mantidos na memória. |
| **Melhores Core Web Vitals** | O carregamento preguiçoso adequado pode melhorar o Largest Contentful Paint (LCP) ao evitar requisições concorrentes. |
| **Experiência do usuário melhorada** | As páginas tornam-se interativas mais cedo e a rolagem é mais suave quando o conteúdo fora da tela carrega progressivamente. |

---

## Técnicas e Abordagens Principais

### 1. Carregamento Preguiçoso Nativo (atributo HTML `loading`)

Desde o Chrome 76 (2019) e com suporte total dos navegadores a partir de 2023, o atributo `loading` pode ser aplicado a elementos `<img>` e `<iframe>` sem qualquer JavaScript.

```html
<img src="photo.jpg" loading="lazy" alt="Description" width="800" height="600">
<iframe src="widget.html" loading="lazy"></iframe>
```

**Melhor prática:** Sempre forneça atributos `width` e `height` explícitos (ou `aspect-ratio` do CSS) para evitar Cumulative Layout Shift (CLS).

### 2. API Intersection Observer

Uma poderosa API do navegador que detecta eficientemente quando um elemento se torna visível. Ela substitui listeners manuais de eventos de rolagem e é a base da maioria das bibliotecas modernas de carregamento preguiçoso.

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

### 3. Code Splitting e `import()` Dinâmico

Para aplicações JavaScript, o carregamento preguiçoso significa dividir o bundle em partes menores que são carregadas sob demanda. Bundlers modernos (Webpack, Rollup, Vite) suportam isso nativamente.

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

**Como funciona:** O módulo `./HeavyComponent` é um arquivo separado que é obtido apenas quando `<HeavyComponent>` é renderizado. O `React.lazy` gerencia automaticamente o estado de carregamento com `Suspense`.

### 4. Carregamento Preguiçoso no Backend / ORMs

O carregamento preguiçoso não é apenas um conceito de frontend. ORMs como Hibernate (Java), SQLAlchemy (Python) e Entity Framework (.NET) permitem adiar o carregamento de objetos relacionados até que sejam acessados.

```python
# SQLAlchemy example — lazy='select' (default)
user = session.query(User).get(1)
# The 'addresses' relationship is loaded only when accessed:
print(user.addresses)  # A separate SQL query is executed
```

**Cuidado:** O uso inadequado (por exemplo, acessar uma relação lazy dentro de um loop) pode levar ao problema de consulta N+1. Nesses casos, use carregamento eager (`joinedload`, `subqueryload`) ou batch loading.

### 5. Rolagem Virtual / Windowing

Para listas enormes (feeds de rolagem infinita, tabelas de dados), renderize apenas as linhas visíveis. Bibliotecas como `react-window`, `react-virtualized` e `@tanstack/react-virtual` implementam esse padrão.

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

## Instalação e Configuração

| Abordagem | Instalação | Notas |
|-----------|------------|-------|
| **HTML Nativo** | Nenhuma | Feature detection: `'loading' in HTMLImageElement.prototype` |
| **Intersection Observer** | Nenhuma (API nativa do navegador) | Polyfill disponível para navegadores muito antigos |
| **Lazysizes (biblioteca clássica)** | `npm install lazysizes@5` | Use a classe CSS `lazyload` com `data-src` |
| **Lozad.js** | `npm install lozad` | Leve (1KB) com Intersection Observer |
| **React/Vue/Angular** | Integrado (`React.lazy`, Vue Async Components, Angular `loadChildren`) | Sem dependências extras |
| **ORMs de Banco de Dados** | Parte do ORM | Consulte a documentação do seu ORM |

---

## Melhores Práticas e Recursos Principais

- **Sempre especifique dimensões** para mídia com carregamento preguiçoso para reservar espaço e evitar mudanças de layout.
- **Carregue preguiçosamente apenas conteúdo não crítico** – imagens hero, elementos acima da dobra e o componente inicial da rota devem ser carregados de forma eager.
- **Use o `loading="lazy"` nativo quando possível** – é de custo zero, bem suportado e acessível aos motores de busca.
- **Combine com imagens responsivas** – use `srcset` e `sizes` para carregar o tamanho de imagem correto para a janela de visualização.
- **Implemente fallbacks** – para navegadores que não suportam carregamento preguiçoso nativo, use um fallback do Intersection Observer (bibliotecas como lazysizes fazem isso automaticamente).
- **Meça o impacto** – use Lighthouse, o painel Network do Chrome DevTools e relatórios do Core Web Vitals para verificar se o carregamento preguiçoso realmente melhora o desempenho (pode ser contraproducente para imagens próximas à janela de visualização).

---

## Advertências e Armadilhas

| Problema | Explicação | Solução |
|----------|------------|---------|
| **Preocupações com SEO** | Os rastreadores podem não esperar o JavaScript carregar as imagens. | O `loading="lazy"` nativo é respeitado pelos principais mecanismos de busca. Para soluções baseadas em JS, considere renderização no servidor ou tags `<noscript>`. |
| **Cumulative Layout Shift (CLS)** | Se as dimensões não forem definidas, o layout da página salta quando a imagem carrega. | Sempre defina `width` e `height` ou use `aspect-ratio` do CSS. |
| **Consultas N+1** | O carregamento preguiçoso em ORMs pode gerar uma consulta separada para cada acesso à relação. | Use carregamento eager (`joinedload`, `selectinload`, `include`) quando souber que precisará dos dados relacionados. |
| **Interação atrasada** | Carregar bibliotecas pesadas preguiçosamente ao clicar pode causar um atraso perceptível. | Pré-carregue o chunk com `<link rel="preload">` ou use um pequeno placeholder durante a busca. |
| **Thrashing de rolagem** | Ouvir manualmente eventos de rolagem (sem debouncing) é caro. | Use Intersection Observer – é desacoplado do ciclo de rolagem. |

---

## Leitura Adicional

- [MDN Web Docs: Carregamento preguiçoso](https://developer.mozilla.org/en-US/docs/Web/Performance/Lazy_loading)
- [web.dev: Carregamento preguiçoso de imagens e vídeo](https://web.dev/articles/lazy-loading-images)
- [MDN: Intersection Observer API](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)
- [React.lazy e Suspense](https://react.dev/reference/react/lazy)
- [Core Web Vitals e Carregamento Preguiçoso](https://web.dev/articles/lcp-lazy-loading)