---
title: "O Testing Trophy: Priorizando Testes de Integração em Aplicações Web Modernas"
description: "Um guia prático para o modelo de troféu de testes de Kent C. Dodds — uma estratégia que coloca os testes de integração no centro e usa análise estática, testes unitários e testes E2E como camadas de apoio."
created: 2026-08-08
tags:
  - testing
  - frontend
  - integration-testing
  - react
  - quality
status: draft
---

# O Testing Trophy: Priorizando Testes de Integração em Aplicações Web Modernas

## O que é

O **Testing Trophy** é uma metáfora de estratégia de testes criada por Kent C. Dodds (2017) para aplicações web modernas em JavaScript/TypeScript. Enquanto a **Pirâmide de Testes** clássica coloca *muitos testes unitários* na base e *poucos testes de ponta a ponta* no topo, o troféu inverte o investimento central: a maior fatia de testes é a camada de **testes de integração**, apoiada por:

- **Análise estática** (lint, formatação e verificação de tipos) como base;
- **Testes unitários** como uma camada pequena, mas útil;
- **Testes E2E** como um pequeno número de jornadas lentas e de alto valor no topo.

No modelo do troféu, o sinal mais confiável de que um aplicativo funciona vem de exercitá-lo por meio da sua fiação real voltada para o usuário — componentes montados juntos, formulários reais, consultas reais ao DOM e chamadas `fetch` reais contra uma fronteira de rede simulada — em vez de funções isoladas com mocks em todos os módulos.

## Por que isso importa

A orientação da pirâmide de "escrever muitos testes unitários" funciona bem para lógica pura, mas quebra para aplicações centradas em UI. Quando uma base de código frontend é coberta principalmente por testes unitários que aplicam mock em todos os módulos vizinhos:

- Os testes passam a validar **detalhes de implementação**, não comportamento.
- Uma refatoração que mantém a UX inalterada pode quebrar dezenas de testes.
- Erros reais de fiação (nome de `prop` errado, `aria-label` ausente, payload de API incorreto) passam despercebidos porque cada parte é testada isoladamente.

Os testes de integração — fatias renderizadas do aplicativo que exercem interações realistas — capturam essas lacunas de conexão. O troféu os torna cidadãos de primeira classe, dando a você **muito mais por rápidação investido**.

## O modelo em uma imagem

```
                   ┌────────────┐
                   │    E2E    │  ← critical paths, slow, few
                   └────────────┘

              ┌─────────────────────┐
              │  Integration tests  │  ← the trophy body: biggest
              │                     │    slice of your effort
              └─────────────────────┘

              ┌─────────────────────┐
              │     Unit tests      │  ← complex logic, illustrated
              └─────────────────────┘

             ┌─────────────────────────┐
             │    Static + type check  │  ← ESLint, TypeScript,
             └─────────────────────────┘  Prettier; nearly free
```

O conhecido princípio norteador da Testing Library se encaixa neste modelo:

> Quanto mais seus testes se assemelharem ao modo como o software é usado, mais confiança eles podem fornecer.

## Detalhamento por camada

| Camada | Ferramentas | Custo para escrever | Ganho de confiança por teste | Quando usar |
| --- | --- | --- | --- | --- |
| **Análise estática** (base) | ESLint, TypeScript, Prettier | Quase zero | Captura erros de digitação, erros de tipo e contratos de API inválidos antes que um teste seja executado | em todos os lugares; é a sua rede de segurança |
| **Testes unitários** (haste) | Jest, Vitest | Baixo | Alto para lógica isolada; baixo para fiação do aplicativo | funções puras com lógica de ramificação |
| **Testes de integração** (corpo do troféu) | Vitest/Jest + Testing Library, MSW | Médio | **Mais alto para fiação de um aplicativo** | componentes, fluxos e interação de API |
| **Testes E2E** (ponta) | Playwright, Cypress | Alto, lento, às vezes flaky | Alto, porém duplicado com os testes de integração | jornadas de negócio críticas (login, checkout) |

### 1. Análise estática — a base

As ferramentas de análise estática protegem todo o sistema com o menor custo: sem setup de DOM, sem minutos de CI e com feedback imediato. Isso inclui:

- **Linters**, que previnem erros comuns e garantem consistência de estilo;
- **Type checkers**, que validam o formato de cada contrato de função e componente;
- **Formatadores**, que mantêm o diff limpo.

### 2. Testes unitários — a haste

Os testes unitários têm um trabalho real: verificar lógica pura e complexa que é difícil de ser exercitada pela UI. Exemplo: formatação de datas, cálculo de impostos, construção de URL. O ganho total é alto somente quando cada teste foca o *contrato daquela função*, mockando no máximo o necessário para suas entradas diretas.

### 3. Testes de integração — o corpo do troféu

Um teste de integração típico renderiza uma **fatia real do aplicativo** — uma página ou componente — e a conduz por eventos voltados ao usuário (digitar, clicar, enviar) enquanto o DOM real é montado em um ambiente sem navegador (`jsdom`, `happy-dom`). Fronteiras assíncronas reais, como HTTP, são interceptadas na **borda** usando ferramentas como o MSW (Mock Service Worker).

### 4. Testes E2E — a ponta

Algumas jornadas em Playwright/Cypress que fazem o aplicativo inteiro rodar em um navegador real. Use-as para caminhos que você percorreria manualmente em produção: cadastro, checkout, onboarding. Trate-os como uma auditoria, não como uma suíte de regressão — eles são lentos e frágeis demais para cobrir todos os casos de borda.

## Um exemplo completo: um fluxo de login

Vamos ver como cada camada funciona em um aplicativo React + TypeScript + Vite realista.

### Configuração do projeto

```bash
# create the app
npm create vite@latest trophy-demo -- --template react-ts
cd trophy-demo

# install everything we need per nested
npm i -D typescript @types/react @types/react-dom \
  eslint vitest jsdom \
  @testing-library/react @testing-library/user-event @testing-library/jest-dom \
  msw @playwright/test

# install browser binaries once
npx playwright install
```

Adicione os scripts:

```json
{
  "name": "trophy-demo",
  "scripts": {
    "dev": "vite",
    "typecheck": "tsc --noEmit",
    "lint": "eslint .",
    "test": "vitest run",
    "test:e2e": "playwright test"
  }
}
```

### Camada estática: tipos + lint

```json
{
  "compilerOptions": {
    "strict": true,
    "jsx": "react-jsx"
  }
}
```

A camada estática no CI:

```bash
npm run typecheck && npm run lint
```

### O componente que vamos testar

Execute o teste contra o mesmo componente que o usuário segue. Observe que a **fronteira de rede** é a única que interage com algo do ambiente.

```tsx
// src/components/LoginForm.tsx
import { useState, type FormEvent } from "react";

export function LoginForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      setName(username);
    }
  }

  if (name) {
    return <p>Welcome, {name}</p>;
  }

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="username">Username</label>
      <input
        id="username"
        value={username}
        onChange={(event) => setUsername(event.target.value)}
      />

      <label htmlFor="password">Password</label>
      <input
        id="password"
        type="password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
      />

      <button type="submit">Sign in</button>
    </form>
  );
}
```

### Camada unitária: um auxiliar puro

```ts
// src/lib/formatPrice.test.ts
import { describe, expect, it } from "vitest";
import { formatPrice } from "./formatPrice";

describe("formatPrice", () => {
  it("formats cents into a local currency string", () => {
    expect(formatPrice(1999)).toBe("$19.99");
  });

  it("handles zero", () => {
    expect(formatPrice(0)).toBe("$0.00");
  });

  it("rounds to the nearest cent", () => {
    expect(formatPrice(1005)).toBe("$10.05");
  });
});
```

### Camada de integração: o corpo do troféu

Configure o Vitest com um DOM tipo navegador e double matchers na Testing Library:

```ts
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./test/setup.ts"],
  },
});
```

```ts
// test/setup.ts
import "@testing-library/jest-dom/vitest";
import { afterAll, afterEach, beforeAll } from "vitest";

import { server } from "./server";

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

```ts
// test/server.ts
// MSW: enables integration tests to stub at the HTTP edge since
// the component is still using the real `fetch` API.
import { setupServer } from "msw/node";

export const server = setupServer();
```

Agora o fluxo da forma como o usuário digitar:

```tsx
// src/components/LoginForm.test.tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { server } from "../../test/server";
import { LoginForm } from "./LoginForm";

describe("LoginForm", () => {
  it("accepts credentials and welcome the user", async () => {
    server.use(
      http.post("/api/login", () =>
        HttpResponse.json({ token: "test-token" })
      )
    );

    const user = userEvent.setup();
    render(<LoginForm />);

    await user.type(screen.getByLabelText(/username/i), "alice");
    await user.type(screen.getByLabelText(/password/i), "s3cret");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    expect(await screen.findByText(/welcome, alice/i)).toBeInTheDocument();
  });
});
```

Perceba o que o teste de integração **não faz**:

- Ele não faz mock de `LoginForm` nem dos seus submódulos internos.
- Ele não inspeciona o estado interno do React nem a chamada `fetch`.
- Ele atua na fronteira da API — o mesmo lugar onde o servidor real responderia — usando do MSW.

Isso significa que o teste quebra se o payload da `fetch`, o tratamento da resposta, o texto do `label`, o tipo do botão ou a renderização de sucesso quebrarem. Essa é exatamente a confiança que o troféu centraliza.

### Camada E2E: a ponta do troféu

Use o Playwright para uma ou duas das jornadas “pilgrimage”.

```ts
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  webServer: {
    command: "npm run dev",
    url: "http://localhost:5173",
    reuseExistingServer: !process.env.CI,
  },
  use: {
    baseURL: "http://localhost:5173",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
});
```

```ts
// e2e/login.spec.ts
import { expect, test } from "@playwright/test";

test("a returning customer can sign in", async ({ page }) => {
  await page.goto("/login");

  await page.getByLabel("Username").fill("alice");
  await page.getByLabel("Password").fill("s3cret");
  await page.getByRole("button", { name: "Sign in" }).click();

  await expect(page.getByText(/welcome, alice/i)).toBeVisible();
});
```

O teste E2E é quase a mesma sequência que o teste de integração —, o que é correto. O E2E existe para validar que o build de produção/staging sobe, que as rotas funcionam, que a API responde e que não há regressões de infraestrutura. Por isso, um ou dois desses por recurso crítico é enough.

## Estratégia de mock: faça mock na fronteira, nunca para dentro

A linha entre um teste de integração útil e um teste inútil é *“onde”* o mockão acontece.

| O que você está tentado a mockar | Recomendação do troféu |
| --- | --- |
| Um serviço global ou chamada de API (`fetch` — a rede) | ✅ Use na fronteira do **MSW** / `server.use` |
| O SDK de pagamento de terceiros, dentro de um wrapper fino | ✅ Faça stub através da interface pública |
| Um provider de contexto ou sistema de alertas do mesmo app | ✅ Renderize com o provider, se o usuário experiente isso |
| Um componente filho dentro da página | ❌ Isso destrói a verificação de conexão |
| `useState`/estado interno do React | ❌ Teste o resultado renderizado |

Por quê? No momento em que você “mocka” um componente interno, você perde a capacidade de capturar o bug real de interação que o troféu existe para encontrar.

## Trade-offs

### Quando o troféu vence

- **Interfaces pesadas em UI:** o valor está em conectar componentes e serviços.
- **Equipes com pouco tempo:** testes de integração cobrem fluxos que a suíte E2E⁄lenta não alcança.
- **Projetos que adotam a Testing Library com React/Vue/Svelte:** as libs de consulta são projetadas para fluxos de integração.

### Quando o formato do troféu não é um bom ajuste

- **Bibliotecas puras e ferramentas CLI** — uma quantidade forte de testes unitários ainda é o melhor investimento. Não há DOM, não há fluxo de páginas.
- **Backends fortes/negócio com algoritmos complex references** — testes unitários em serviços puros superam uma bateria pesada de testes web integrados.
- **Codebases hobby/experimental** com um backend de teste frágil — o ambiente E2E continua ficando *flaky*. Integração ainda é útil, mas seja conservador.
- **Grandes aplicativos legados com árvore de componentes emaranhada** — você pode precisar começar aos testes de unidade. Em vez de matrix completa, comece com algumas “fatias”.

### Tabela: Pirâmide vs. Troféu vs. Favo

| Estratégia | Ênfase | Exemplo típico | Caso de maior eficiência |
| --- | --- | --- | --- |
| **Pirâmide de Testes (Cohn)** | Centenas de testes unitários; poucos E2E | Suites clássicas de backend | Backend com regras puras e CI rápido |
| **Testing Trophy (Dodds)** | A integração no centro; base estática; alguns E2E | UI frontend Vue/React | Aplicações focadas em frontend e componentes |
| **Testing Honeycomb** | O meio e o topo pesados (integração + E2E) | Serviços distribuídos com muitos contratos | Interação complexa entre serviços |

O troféu não é a resposta “sempre certa” — ele é o padrão de maior ganho por custo para *UI web*.

## Boas práticas

1. **Torne a análise estática a fundação.** `tsc --noEmit`, `eslint .` e Prettier voçe no CI antes dos testes lentos. Faça o fluxo corre ficar vivo: a tipagem captura metade dos bugs antes do primeiro teste rodar.
2. **Escreva testes de integração por padrão.** Para cadastro de usuário, carrinho, dashboard: faça um teste-inchado de unidade** com consultas de usuário. Use MSW para rede.
3. **Consulte como uma pessoa real precisaria.** Use `getByLabelText`, `getByRole`, `getByPlaceholderText`, `findByText`; não `data-testid` ou classe CSS. Aliás: `getByRole('button', { name: 'Sign in' })`.
4. **Espere o real.** Use `findBy*` / `waitFor` quando houver assincronia. Evite `setTimeout` artificial.
5. **Mocke só na fronteira.** A rede, o relógio, o `localStorage` do navegador. Nunca simule a fonteira interna do componente que você está test.
6. **E2E é auditoria, não é regressão.** Mantenha a lista de E2E curta — login, checkout, início. Suíte E2E de 200 testes tem custo de execução e instabilidade alto demais.
7. **Teste unitário é para matemática complexa.** Gaste testes de unidade onde o de baixa está: datas, moedas, sorting, permissões. Ela muta entrada pura → saída.
8. **Se uma refatoração quebrar 40 testes unitários mas o visual continuar igual, é um sinal** de que os teste conhecem mais os detalhes de implementação do que o comportamento. Refatorar os teste para as consultas de role.
9. **Importante no CI:** um `npm run test` deve rodar toda a camada de integração no merge request; o E2E pode ser um job obrigatório à parte, ou entrar depois do unit/lint.

## Resumo

O troféu de testes recolme o mental de “verificar cada função” para “*ver option usando o caminho do usuário*.” Sua insight central é em forma como terra:

> **Confiança é uma medida de quanto perto o teste está do uso real do usuário, não de quantas vezes unidades dividem o aplicativo em cantos mockados.**

- Análise estática de segurança — ela é de graça.
- Testes unitários no suporte — onde a lógica é complexa.
- Testes de integração como o corpo — sua principal garantia.
- E2E no topo — “selo” de uma jornada crítica.

O troféu não remove as pirâmides; ele simplesmente redireciona o esforço dos testes unitários de falsa confiança para prestar atenção real à superfície que o usuário toca: a integração.

## Referências

- Kent C. Dodds — [The Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy)
- Testing Library — [Princípios norteadores](https://testing-library.com/docs/)
- MSW — [Mock Service Worker](https://mswjs.io/docs/)
- Playwright — [Docs](https://playwright.dev/docs/intro)