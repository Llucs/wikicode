---
title: "The Testing Trophy: Prioritizing Integration Tests in Modern Web Apps"
description: "A practitioner's guide to Kent C. Dodds' testing trophy model — a strategy that puts integration tests at the center and uses static analysis, unit tests, and E2E tests as supporting layers."
created: 2026-08-08
tags:
  - testing
  - frontend
  - integration-testing
  - react
  - quality
status: draft
---

# The Testing Trophy: Prioritizing Integration Tests in Modern Web Apps

## What it is

The **Testing Trophy** is a testing strategy metaphor created by Kent C. Dodds (2017) for modern JavaScript/TypeScript web applications. Where the classic **Testing Pyramid** puts *many unit tests* at the base and *few end-to-end tests* at the top, the trophy inverts the core investment: the largest testing slice is the **integration test** layer, supported by:

- **Static analysis** (linting, formatting, type-checking) as the base;
- **Unit tests** as a small but useful layer;
- **End-to-end tests** as a small number of slow, high-value journeys at the top.

In the trophy model, the most reliable signal that an app works comes from exercising it through its real user-facing wiring — components mounted together, real forms, real DOM queries, real fetch calls against a stubbed network boundary — rather than from isolated functions with entire modules mocked away.

## Why it matters

The pyramid's advice to "write many unit tests" works well for pure logic but breaks down for UI-centric applications. When a frontend codebase is covered mostly by unit tests that mock every nearby module:

- Tests begin to assert **implementation details**, not behavior.
- A refactor that keeps UX the same can break dozens of tests.
- Real wiring errors (wrong prop name, missing `aria-label`, wrong API payload) slip through because each unit is tested in isolation.

Integration tests — rendered app slices exercising realistic interactions — catch those wiring gaps. The trophy makes them the first-class citizen, giving you **more confidence per test dollar**.

## The model in one picture

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

The well-known Testing Library guiding principle belongs to this model:

> The more your tests resemble the way your software is used, the more confidence they can give you.

## Layer-by-layer breakdown

| Layer | Tools | Cost to write | Confidence gain per test | Use it when |
| --- | --- | --- | --- | --- |
| **Static analysis** (base) | ESLint, TypeScript, Prettier | Nearly zero | Catches typos, type errors, bad API contracts before a test runs | everywhere; it is your safety net |
| **Unit tests** (stem) | Jest, Vitest | Low | High for isolated logic; low for app wiring | pure functions with branching logic |
| **Integration tests** (trophy body) | Vitest/Jest + Testing Library, MSW | Medium | **Highest for app wiring** | components, flows, API interaction |
| **E2E tests** (tip) | Playwright, Cypress | High, slow, sometimes flaky | High but duplicated with integration tests | critical business journeys (login, checkout) |

### 1. Static analysis — the base

Static tools guard the whole system with the lowest cost: no DOM setup, no CI minutes, immediate feedback. This includes:

- **Linters** trading common mistakes and style consistency;
- **Type checkers** validating the shape of every function and component contract;
- **Formatters** to keep the diff clean.

### 2. Unit tests — the stem

Unit tests have a real job: verify tricky, pure logic that is too hard to exercise through a UI. Example: date formatting, tax calculation, URL builder. The whole gain is high only when each test focuses on *that function's contract*, mocking at most its direct inputs.

### 3. Integration tests — the trophy body

A generic integration test renders a **real slice of the app** — a page or component — and drives it through user-facing events (typing, clicking, submitting) while the actual DOM is mountable in a no-browser environment (jsdom, happy-dom). Real async boundaries like HTTP are stubbed at the **edge** using tools like MSW (Mock Service Worker).

### 4. E2E tests — the tip

A few Playwright/Cypress journeys that run the whole app through a real browser. Use these for journeys you could manually walk through in production: sign-up, checkout, onboarding. Treat them as an audit, not as a regression toolkit — they are too slow and brittle for every edge case.

## A complete working example: a login flow

Let's see what each layer looks like in a realistic React + TypeScript + Vite app.

### Project setup

```bash
# create the app
npm create vite@latest trophy-demo -- --template react-ts
cd trophy-demo

# install everything we need per layer
npm i -D typescript @types/react @types/react-dom \
  eslint vitest jsdom \
  @testing-library/react @testing-library/user-event @testing-library/jest-dom \
  msw @playwright/test

# install browser binaries once
npx playwright install
```

Add scripts:

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

### Static layer: types + lint

```json
{
  "compilerOptions": {
    "strict": true,
    "jsx": "react-jsx"
  }
}
```

The static layer in CI:

```bash
npm run typecheck && npm run lint
```

### The component we will test

Run the test against the same component the user uses. Note the **network boundary** is the only thing that touches the environment.

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

### Unit layer: a pure helper

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

### Integration layer: the trophy body

Setup Vitest with a browser-like DOM and the Testing Library matchers:

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

Now the login flow as a user would type it:

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

Notice what the integration test **does not do**:

- It doesn't mock `LoginForm` or its internal submodules.
- It doesn't inspect React state or the fetch call.
- It stubs at the API boundary — the same place the real server would respond — with MSW.

This means the test breaks if the `fetch` payload, the response handling, the label text, the button type, or the success rendering all break. That's exactly the confidence the trophy centers around.

### E2E layer: the trophy tip

Use Playwright for the one or two “pilgrimage” journeys.

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

The E2E test is roughly the same sequence as the integration test — which is correct. E2E exists as a verification that the production / staging build boots, routing works, the API responds, and no infrastructure regression. Therefore, one or two of these per critical feature is enough.

## Mocking strategy: mock at the boundary, never inward

The line between a useful integration test and a waste test is *where* the mocking happens.

| What you are tempted to mock | Trophy recommendation |
| --- | --- |
| Global service or API call (`fetch` — the network) | ✅ Use in the **MSW** / `server.use` boundary |
| The third-party payment SDK at a thin wrapper | ✅ Stub through the public interface |
| A context provider or alert system in the same app | ❌ Render it through the provider if your user experiences it |
| A child component inside the page | ❌ It defeats the wire-up verification |
| `useState`/React internal state | ❌ Test the rendered result |

Why fake user answer? The moment you mock an internal component away, you've lost the ability to catch the actual end-user bug the trophy is there to find.

## Trade-offs

### When the trophy wins

- **UI-heavy frontends:** the value is in wiring components and services together.
- **Teams with limited time:** integration tests cover workflows the slow E2E suite can't.
- **Projects adopting React/Vue/Svelte testing Library:** the library's querying is built for integration flows.

### When the trophy shape is not a good fit

- **Pure libraries and CLI tools** — a heap of unit tests is still the best investment. No DOM, no page flow.
- **Strong backend/business algorithms** — unit tests on pure services outperform a battery-level web integration battery.
- **Hobby/experimental codebase** with a broken test backend — E2E will keep flaking. Integration is still useful, but be conservative.
- **Large legacy apps with a tangled component tree** — you may need to look at the atomic tests get in. Start with a few "slices" rather than full matrix.

### Table: pyramid vs. trophy vs. honeycomb

| Strategy | Emphasis | Typical example | Strongest when |
| --- | --- | --- | --- |
| **Testing Pyramid (Cohn)** | Hundreds of unit tests; few E2E | Classic backend suites | Backend with pure rules and fast CI |
| **Testing Trophy (Dodds)** | Integration tests in the middle; static base; few E2E | React / Vue web front-UI | Frontend-focus, component-based apps |
| **Testing Honeycomb** | The middle and top heavy (integration + E2E) | Distributed services with many contracts | Complex interaction between services |

The trophy is not the “always right” answer — it is the most cost-efficient default for *web UI* //props.

## Best practices

1. **Make static analysis the foundation.** `tsc --noEmit`, `eslint .`, and Prettier run in CI before slow tests. Make the workflow warm: types catch half the bugs before a test runs.
2. **Default write integration tests.** For registration, selection of a cart, dashboard render: short session test with user-facing queries. Use MSW for network.
3. **Query like a user.** Use `getByLabelText`, `getByRole`, `getByPlaceholderText`, `findByText`, not DOM `data-testid` or CSS class selectors. Also: `getByRole('button', { name: 'Sign in' })`.
4. **Wait for reality.** Use `findBy*` / `waitFor` when a state has async. Avoid artificial `setTimeout` in tests.
5. **Mock at boundaries only.** The network, the clock, the browser localStorage. Never mock the component you are testing at an internal dependency.
6. **E2E as audit, not regression.** Keep the E2E list short — login, checkout, onboarding. A 200-test E2E suite has virtually guaranteed speed and flake costs too high.
7. **Unit tests on the tricky math.** Spend unit tests where the logic is (date parsing, currency, sorting, permissions), it mutates pure input → output.
8. **If a refactor breaks 40 unit tests but the visual behavior is unchanged, that's a signal** the tests know more implementation details than behavior. Refactor the tests toward the role queries.
9. **Importants in CI:** a single `npm run test` should run the whole integration layer in the MR; E2E can be a required separate job, or after the unit/lint pass. 

## Summary

The testing trophy reshapes the mental model from “verify every function” to “*verify the app through the user’s path*.” Its central insight is land:

> **Confidence is a product of how near the test is to the actual usage, not how many times the unit split the app into mocked corners.**

- Static analysis at the bottom — free guardrails.
- Unit tests in the stem — where logic is complex.
- Integration tests as the body — your main assurance.
- E2E at the top — “hallmark” of a critical journey.

The trophy doesn't remove pyramids; it redirects the effort away from fake-confidence unit tests and pays real attention to the surface a user touches: the integration.

## Further references

- Kent C. Dodds — [The Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy)
- Testing Library — [The guiding principles](https://testing-library.com/docs/)
- MSW — [Mock Service Worker](https://mswjs.io/docs/)
- Playwright — [Docs](https://playwright.dev/docs/intro)