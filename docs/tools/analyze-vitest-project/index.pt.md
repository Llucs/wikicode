---
title: "Vitest: Framework de Testes de Próxima Geração com o Poder do Vite"
description: "Um framework de testes rápido e nativo do Vite, com suporte contínuo a TypeScript e ESM, projetado para aplicações modernas em JavaScript/TypeScript."
created: 2026-06-23
tags:
  - testing
  - unit-testing
  - vite
  - typescript
  - jest-alternative
status: draft
---

# Vitest: Framework de Testes de Próxima Geração com o Poder do Vite

## Visão Geral

O Vitest é um framework de testes unitários de próxima geração construído sobre o Vite. Criado por Anthony Fu e pela equipe principal do Vite, foi lançado em dezembro de 2021 para resolver o atrito entre o servidor de desenvolvimento do Vite e os executores de teste tradicionais como o Jest. Aproveitando o pipeline de transformação, a substituição de módulo a quente (Hot Module Replacement - HMR) e o sistema de plugins do Vite, o Vitest oferece uma experiência de desenvolvimento significativamente mais rápida e consistente, especialmente para projetos que já utilizam o Vite.

### Por que Vitest?

- **Suporte Nativo a ESM:** Ao contrário do Jest, que requer transformações complexas para ES Modules, o Vitest lida com ESM de forma nativa por usar o pipeline baseado em rollup do Vite.
- **HMR para Testes:** Apenas os testes afetados são reexecutados quando o código muda, tornando o ciclo de feedback quase instantâneo.
- **Compatibilidade com a API do Jest:** Utiliza a mesma API `describe`, `it`, `expect`, com `vi` substituindo `jest` para mocks e espiões. A migração é direta.
- **TypeScript de Primeira Classe:** TypeScript é transpilado instantaneamente via esbuild sem configuração adicional.
- **Testes de Componentes:** Suporte nativo para Vue, React, Svelte e Lit com ambientes como jsdom, happy-dom e Playwright.
- **Cobertura de Código Integrada:** Suporta provedores de cobertura v8 e istanbul prontos para uso.
- **Interface UI do Vitest:** Um painel gráfico rico para visualizar testes e dependências de módulos.

## Instalação

Adicione o Vitest como dependência de desenvolvimento:

```bash
npm install -D vitest
```

Com yarn ou pnpm:

```bash
yarn add -D vitest
pnpm add -D vitest
```

Em seguida, adicione um script de teste ao `package.json`:

```json
{
  "scripts": {
    "test": "vitest"
  }
}
```

> **Nota:** Execute `vitest run` para uma execução única (sem modo watch). O modo padrão é watch, que reexecuta os testes em caso de alterações.

## Escrevendo Testes

O Vitest utiliza a mesma API global do Jest. Importe `test`, `expect`, `describe`, etc., do `vitest` ou habilite `globals` na configuração.

### Exemplo Básico

```javascript
// sum.test.js
import { expect, test } from 'vitest';
import { sum } from './sum';

test('adiciona 1 + 2 e resulta em 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

### Usando `describe` e `it`

```typescript
import { describe, it, expect } from 'vitest';

describe('Array', () => {
  it('deve estar vazio inicialmente', () => {
    const arr: number[] = [];
    expect(arr).toHaveLength(0);
  });
});
```

### Mocks com `vi`

```typescript
import { vi, test, expect } from 'vitest';

const mockFn = vi.fn();
mockFn('hello');
expect(mockFn).toHaveBeenCalledWith('hello');

// Mock de um módulo
vi.mock('../api', () => ({
  fetchData: vi.fn(() => Promise.resolve({ data: 'mocado' })),
}));
```

## Configuração

O Vitest pode ser configurado no arquivo `vite.config.ts` do seu projeto (preferencial) ou em um `vitest.config.ts` separado. A configuração é colocada sob a propriedade `test`.

```typescript
/// <reference types="vitest/config" />
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true, // usar test/expect sem importação
    environment: 'jsdom', // ou 'happy-dom', 'node', 'edge-runtime'
    setupFiles: './src/setup.ts',
    include: ['src/**/*.{test,spec}.{js,ts}'],
    coverage: {
      provider: 'v8', // ou 'istanbul'
      reporter: ['text', 'json', 'html'],
    },
  },
});
```

Se for usar um `vitest.config.ts` independente, o formato é idêntico, mas deve exportar uma configuração do Vite (o Vitest estende o Vite).

## Principais Recursos

### 1. Substituição de Módulo a Quente (HMR) para Testes

O Vitest monitora os arquivos de origem e de teste. Quando alterações são feitas, apenas os testes afetados são reexecutados, fornecendo feedback quase instantâneo.

```bash
vitest
```

Pressione `r` para reexecutar todos os testes, `f` para reexecutar apenas os testes com falha, `q` para sair.

### 2. Suporte Nativo a ESM

Como o Vitest utiliza o pipeline do Vite, os ES Modules funcionam naturalmente. Não são necessários plugins Babel ou transformações especiais.

### 3. Compatibilidade com a API do Jest

| Jest | Vitest |
|------|--------|
| `jest.fn()` | `vi.fn()` |
| `jest.mock()` | `vi.mock()` |
| `jest.spyOn()` | `vi.spyOn()` |
| `jest.useFakeTimers()` | `vi.useFakeTimers()` |

Todos os hooks de ciclo de vida (`beforeEach`, `afterEach`, `beforeAll`, `afterAll`) funcionam de forma idêntica.

### 4. TypeScript de Primeira Classe

Não é necessário usar `ts-jest` ou configuração separada do Babel. Escreva testes TypeScript diretamente e o Vitest lida com a transpilação via esbuild.

```typescript
interface User { name: string }
function greet(user: User) { return `Hello, ${user.name}`; }

it('saúda o usuário', () => {
  expect(greet({ name: 'Alice' })).toBe('Hello, Alice');
});
```

### 5. Testes de Componentes

O Vitest funciona perfeitamente com bibliotecas de teste de componentes como `@testing-library/vue`, `@testing-library/react` e `@vue/test-utils`. Use a opção `environment` para simular um ambiente de navegador.

```typescript
// Exemplo com @vue/test-utils
import { mount } from '@vue/test-utils';
import MyComponent from './MyComponent.vue';
import { describe, it, expect } from 'vitest';

describe('MyComponent', () => {
  it('renderiza', () => {
    const wrapper = mount(MyComponent);
    expect(wrapper.text()).toContain('Hello Vitest');
  });
});
```

### 6. Cobertura de Código

Suporte integrado a cobertura via v8 (padrão) ou istanbul.

```bash
vitest run --coverage
```

Ou via configuração:

```typescript
test: {
  coverage: {
    provider: 'v8',
    all: true,
    include: ['src/**/*.ts'],
    exclude: ['src/test/', '**/*.spec.ts'],
  }
}
```

### 7. Interface UI do Vitest

Uma interface web opcional e rica para explorar os resultados dos testes.

```bash
vitest --ui
```

A UI fornece um painel com status dos testes, tempos, árvore de arquivos e um grafo de dependências de módulos.

### 8. Modo Workspace (Suporte a Monorepo)

O Vitest pode executar testes em vários projetos ou pacotes em um monorepo usando um arquivo `vitest.workspace.ts`. As configurações podem ser embutidas ou referenciar arquivos/glob patterns.

```typescript
// vitest.workspace.ts
import { defineWorkspace } from 'vitest/config';

export default defineWorkspace([
  'packages/*',
  {
    // Configuração embutida para um projeto específico
    test: {
      name: 'my-package',
      root: './packages/my-package',
      environment: 'node',
    },
  },
]);
```

Cada projeto pode ter sua própria configuração, mas ser executado a partir de um único comando.

### 9. Execução Paralela

Os testes são executados em paralelo via worker threads (padrão) ou processos filhos (definindo `pool: 'forks'`).

```typescript
test: {
  pool: 'forks', // ou 'threads' (padrão)
  poolOptions: {
    forks: {
      singleFork: true,
    },
  },
}
```

## Exemplos de Comandos

| Comando | Descrição |
|---------|-----------|
| `vitest` | Executa testes no modo watch (padrão) |
| `vitest run` | Executa testes uma vez (sem watch) |
| `vitest run --reporter verbose` | Saída detalhada |
| `vitest --coverage` | Executa testes com relatório de cobertura |
| `vitest --ui` | Inicia a interface UI do Vitest |
| `vitest --config vitest.ci.ts` | Usa um arquivo de configuração personalizado |
| `vitest --project projectName` | Executa testes para um projeto específico no workspace |
| `vitest test/specific.test.ts` | Executa um arquivo de teste específico |
| `npx vitest --run --reporter json` | Gera resultados em JSON (amigável para CI) |

## Migração a partir do Jest

Migrar do Jest para o Vitest geralmente envolve:

1. Substituir `jest` por `vi` nos arquivos de teste (spy, mock, fn).
2. Atualizar importações de `@jest/globals` para `vitest` (ou usar `globals: true`).
3. Mover a configuração do Jest para `vite.config.ts` ou `vitest.config.ts` sob a chave `test`.
4. Adaptar mocks de módulos: `vi.mock` em vez de `jest.mock`.
5. Ajustar temporizadores: `vi.useFakeTimers()`.

Um guia de migração dedicado está disponível na documentação oficial do Vitest.

## Casos de Uso

- **Testes Unitários:** Funções, utilitários e lógica de negócio.
- **Testes de Componentes:** Componentes Vue, React, Svelte, Solid e Lit.
- **Testes de Integração:** Endpoints de API, módulos combinados, com ambientes simulados.
- **Desenvolvimento de Bibliotecas / CLI:** Execuções rápidas em CI com excelente suporte a TypeScript.
- **Testes em Monorepos:** O modo workspace fornece testes unificados entre pacotes.

## Por que Vitest em vez de Jest?

- **Suporte a ESM:** Sem módulos experimentais ou transformações complexas necessárias.
- **Velocidade:** Inicializações mais rápidas devido à otimização de empacotamento do Vite e transpilação com esbuild.
- **HMR:** Reexecuções instantâneas para um fluxo de trabalho TDD eficiente.
- **Configuração mais simples:** Reutiliza a configuração do Vite; sem transformadores específicos do Jest.
- **Execução paralela:** Worker threads superam o padrão do Jest.
- **Alinhamento com stack moderno:** Projetado para projetos baseados em Vite (Vue, Svelte, React, etc.).

Para projetos grandes e monorepos, o Vitest pode reduzir o tempo de execução dos testes em 2 a 10 vezes em comparação com o Jest.

## Recursos Adicionais

- [Documentação Oficial](https://vitest.dev/)
- [Repositório no GitHub](https://github.com/vitest-dev/vitest)
- [Guia de Migração do Jest](https://vitest.dev/guide/migration.html#migrating-from-jest)
- [Demonstração da UI do Vitest](https://vitest.dev/guide/ui.html)