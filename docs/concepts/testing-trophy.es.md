---
title: "El Trofeo de Testing: Priorizando las Pruebas de Integración en Aplicaciones Web Modernas"
description: "Una guía práctica del modelo del Trofeo de Testing de Kent C. Dodds, una estrategia que sitúa las pruebas de integración en el centro y utiliza el análisis estático, las pruebas unitarias y las pruebas E2E como capas de apoyo."
created: 2026-08-08
tags:
  - testing
  - frontend
  - integration-testing
  - react
  - quality
status: draft
---

# El Trofeo de Testing: Priorizando las Pruebas de Integración en Aplicaciones Web Modernas

## Qué es

El **Trofeo de Testing** es una metáfora de estrategia de pruebas creada por Kent C. Dodds (2017) para aplicaciones web modernas en JavaScript/TypeScript. Mientras que la clásica **Pirámide de Testing** pone *muchas pruebas unitarias* en la base y *pocas pruebas de extremo a extremo* en la cima, el trofeo invierte la inversión central: la mayor parte de las pruebas es la capa de **pruebas de integración**, apoyada por:

- **Análisis estático** (linting, formato, verificación de tipos) como base;
- **Pruebas unitarias** como una capa pequeña pero útil;
- **Pruebas de extremo a extremo (E2E)** como un pequeño número de recorridos lentos y de alto valor en la parte superior.

En el modelo del trofeo, la señal más fiable de que una aplicación funciona proviene de ejercitarla a través de su cableado real orientado al usuario: componentes montados juntos, formularios reales, consultas reales al DOM y llamadas reales a `fetch` contra un límite de red simulado, en lugar de depender de funciones aisladas con módulos enteros simulados.

## Por qué es importante

El consejo de la pirámide de "escribir muchas pruebas unitarias" funciona bien para lógica pura, pero se desmorona en aplicaciones centradas en la interfaz. Cuando una base de código frontend está cubierta principalmente por pruebas unitarias que simulan todos los módulos cercanos:

- Las pruebas empiezan a verificar **detalles de implementación**, no comportamiento.
- Una refactorización que mantiene la UX igual puede romper decenas de pruebas.
- Errores reales de conexión (un nombre de prop mal, una `aria-label` faltante, un payload incorrecto en la API) se escapan porque cada unidad se prueba de forma aislada.

Las pruebas de integración — porciones renderizadas de la aplicación que ejercitan interacciones realistas — capturan esas brechas de cableado. El trofeo las convierte en ciudadanas de primera clase, dándote **más confianza por cada esfuerzo invertido en pruebas**.

## El modelo en un esquema

```
                   ┌────────────┐
                   │    E2E    │  ← rutas críticas, lentas, pocas
                   └────────────┘

              ┌─────────────────────┐
              │  Integration tests  │  ← el cuerpo del trofeo: la mayor
              │                     │    parte de tu esfuerzo
              └─────────────────────┘

              ┌─────────────────────┐
              │     Unit tests      │  ← lógica compleja, ilustrada
              └─────────────────────┘

             ┌─────────────────────────┐
             │    Static + type check  │  ← ESLint, TypeScript,
             └─────────────────────────┘  Prettier; casi gratis
```

El conocido principio de Testing Library pertenece a este modelo:

> Cuanto más se parezcan tus pruebas a la forma en que se usa el software, más confianza pueden darte.

## Desglose capa por capa

| Capa | Herramientas | Coste de escritura | Confianza ganada por prueba | Cuándo usarla |
| --- | --- | --- | --- | --- |
| **Análisis estático** (base) | ESLint, TypeScript, Prettier | Casi nulo | Captura erratas, errores de tipos y contratos de API incorrectos antes de que se ejecute una prueba | Siembre; es tu red de seguridad |
| **Pruebas unitarias** (tallo) | Jest, Vitest | Bajo | Alta para lógica aislada/profunda; baja para cableado de la app | Funciones puras con lógica ramificada |
| **Pruebas de integración** (cuerpo del trofeo) | Vitest/Jest + Testing Library, MSW | Medio | **La más alta para el cableado de la app** | Componentes, flujos, interacción con API |
| **Pruebas E2E** (punta) | Playwright, Cypress | Alto, lento, a veces inestable | Alta, pero duplicada con las pruebas de integración | Analogías críticas de negocio (inicio de sesión, pago) |

### 1. Análisis estático: la base

¡Las herramientas estáticas protegen todo el sistema con el menor coste: no requieren configuración de DOM, no consumen minutos de CI y ofrecen retroalimentación inmediata. Estos incluyen:

- **Linters** que detectan errores comunes y mantienen la consistencia del estilo;
- **Verificadores de tipos** que validan la forma de cada contrato de función y componente;
- **Formateadores** que mantienen la visualización limpia.

### 2. Pruebas unitarias: el tallo

Las pruebas unitarias tienen un trabajo real: verificar lógica pura y complicada que es demasiado difícil de ejercitar a través de una interfaz. Por ejemplo: el formato de fechas, el cálculo de impuestos o el constructor de URLs. La ganancia solo es dulce cuando cada prueba se centra en el *contrato de esa función*, simulando en todo caso sus entradas directas.

### 3. Pruebas de integración: el cuerpo del trofeo

Una prueba de integración genérica renderiza una **parte real de la aplicación** —una página o un componente— y la maneja mediante eventos orientados al usuario (escribir, hacer clic, enviar) mientras el DOM real se monta en un entorno sin navegador (jsdom, happy-dom). Límites asíncronos reales como HTTP se protegen en el **borde** mediante herramientas como MSW (Mock Service Worker).

### 4. Pruebas E2E: la punta

Pocos flujos con Playwright/Cypress que recorren toda la aplicación en un navegador real. Úsalos para los flujos que podrías recorrer manualmente en producción: registro de logro, pago, onboarding. El panorama es un auditoría, no un kit de regresión: son demasiado lentas y frágiles para cada caso particular.

## Un ejemplo completo funcional: un flujo de inicio de sesión

Veamos cómo se ve cada capa en una aplicación real de React + TypeScript + Vite.

### Configuración del proyecto

```bash
# crea la aplicación
npm create vite@latest trophy-demo -- --template react-ts
cd trophy-demo

# instala todo lo que necesitamos por capa
npm i -D typescript @types/react @types/react-dom \
  eslint vitest jsdom \
  @testing-library/react @testing-library/user-event @testing-library/jest-dom \
  msw @playwright/test

# instala los binarios del navegador una vez
npx playwright install
```

Añade los scripts:

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

### Capa estática: tipos + lint

```json
{
  "compilerOptions": {
    "strict": true,
    "jsx": "react-jsx"
  }
}
```

La capa estática en CI:

```bash
npm run typecheck && npm run lint
```

### El componente que vamos a probar

Ejecuta la prueba contra el mismo componente que ves al usuario. Observa que el **límite de red** es lo único que toca el entorno.

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

### Capa unitaria: un helper puro

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

### Capa de integración: el cuerpo del trofeo

Configura Vitest con un DOM similar a un navegador, más matchers de Testing Library:

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
// MSW : permite que las pruebas de integración simulen en el límite HTTP,
// como el componente todavía usa la API real de `fetch`.
import { setupServer } from "msw/node";

export const server = setupServer();
```

Ahora el flujo de inicio de sesión tal y como lo escribiría un usuario:

```tsx
// src/components/LoginForm.test.tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { server } from "../../test/server";
import { LoginForm } from "./LoginForm";

describe("LoginForm", () => {
  it("accepts credentials and welcomes the user", async () => {
    server.use(
      http.post("/api/login", () =>
        HttpResponse.json({ token: "test-token" })
      )
    );

    const user = userEvent.setup();
    render(<LoginForm />);

    await user.type(screen.getByLabelText(/ username /i), "alice");
    await user.type(screen.getByLabelText(/ password /i), "s3cret");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    expect(await screen.findByText(/welcome, alice/i)).toBeInTheDocument();
  });
});
```

Observa que esta prueba de integración **no** hace:

- No simula `LoginForm` ni sus submódulos internos.
- No inspecciona el estado de React ni la llamada a `fetch`.
- Simula en el límite de la API — el mismo sitio donde respondería en la oficina comercial real — con MSW.

Por lo tanto, la prueba se rompe si cambia el payload de `fetch`, el seguimiento de la respuesta, el texto de la etiqueta, el tipo de botón o el renderizado de éxito. Esa es exactamente la confianza que el trofeo y conocen en el centro.

### Capa E2E: la punta del trofeo

Usa Playwright para uno o dos "peregrinajes" críticos.

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

La prueba E2E es básicamente la misma secuencia que la prueba de integración, lo cual es correcto. E2E existe para verificar que la aplicación en producción/escenario arranca, el enrutamiento funciona, la API responde y no hay regresión del regresión de infraestructura. Por lo tanto, una o dos de estas por cada funcionalidad crítica es suficiente.

## Estrategia de simulación: simula en el límite, nunca hacia adentro

La línea entre una prueba de integración y verdaderamente útil y una pérdida de tiempo está en *dónde se simula*.

| Dónde intentas simular | Unidad recomendada |
| --- | --- |
| El servicio global o la llamada a la API (`fetch` — el borde de red) | ✅ Simular en el núcleo **MSW** / `server.use` |
| El SDK de pagos de terceras partes detrás de una envoltura fina | ✅ Simular a través de su interfaz pública |
| Un proveedor de contexto o sistema de alertas dentro de la misma total. | ❌ Coloca el tras el proveedor si el usuario lo consume |
| Un componente hijo dentro de la página | ❌ Derrotarlo destruye la verificación del cableado |
| `useState` / estado React | ❌ Pruebas de resultado, no que haga incluida |

¿Por qué no simular hacia adentro? En el momento en que simulas un componente interno, pierdes la capacidad de detectar el error real del usuario final que el trofeo existe para encontrar.

## Compensaciones

### Cuándo el trofeo gana

- **Frontends con mucho peso en UI**: el valor está en enchufar componentes y servicios entre sí.
- **Equipos con tiempo limitado**: las pruebas de integración cubren flujos de trabajo que la suite E2E lenta no puede.
- **Proyectos que adoptan React/Vue/Svelte Testing Library**: sus consultas están diseñadas para flujos de integración.

### Cuándo la forma del trofeo no encaja bien

- **Librerías puras y herramientas CLI**: un puede de pruebas unitarias sigue siendo la mejor inversión. No hay DOM, contra flujo de página.
- **Algoritmos de backend/negocio fuertes**: las pruebas unitarias sobre servicios servicios valen más que una batería de integración a nivel web.
- **Proyectos de hobby/experimental con backend roto**: E2E estodará dando fallos intermitentes. La integración aún es útil, pero sé conservador.
- **Grandes apps heredadas con un árbol de componentes enredado**: puede que necesites pruebas unitarias más aisladas para avanzar. Empieza por algunas "porciones" antes que la matriz completa..

### Tabla: pirámide vs. trofeo vs. panal

| Estrategia | Énfasis | Ejemplo típico | Cuándo es más fuerte |
| --- | --- | --- | --- |
| **Pirámide de Testing (Cohn)** | Muchas unitarias unidades; pocas E2E | Suites clásicas de backend | Backend con reglas puras y CI rápido |
| **Trofeo de Testing (Dodds)** | Las pruebas de integración en el centro; base estática; pocas E2E | Frontends de React / Vue | Apps centradas en frontend, basadas en componentes |
| **Panal de Testing (Honeycomb)** | Centradas y partenas pesadas (integración + E2E) | Servicios distribuidos con varios contratos | Interacción compleja entre servicios |

El trofeo no es la respuesta "correcta": es la opción por defecto más rentable para *aplicaciones de UI web*.

## Buenas prácticas

1. **Convierte el análisis estático en la base.** `tsc --noEmit`, `eslint .` y Prettier se ejecutan en CI antes de las pruebas lentas. Los tipos detectan muchos errores antes de que la prueba ejecuta.
2. **Escribe pruebas de integración por defecto.** Para los registros, los filtros de tarjeta, el renderizado de las funcionalidades: una prueba corta con consultas que usa el usuario. Usa MSW para red.
3. **Consulta como lo usar un usuario.** Usa `getByLabelText`, `getByRole`, `getByPlaceholderText`, `findByText`, no `data-testid` o selectores de clase CSS. Es decir, `getByRole('button', { name: 'Sign in' })`.
4. **Mira la realidad espera async.** Usa `findBy*` / `waitFor` cuando haya async. Sin `setTimeout` artificiales en las pruebas.
5. **Simula solo en los límites.** El borde de red, el reloj, el acceso del navegador. No simulando, no simulas nunca el componente que estás probando ni sus dependencias internas.
6. **E2E como auditoría, no como regresión.** El mantra corta E2E — login, pago, onboarding—. Son 200 pruebas E2EE suite E2E con un coste enorme en tiempo y situación.
7. **Pruebas unitarias para la lógica desafiante.** Invierte las pruebas unitarias donde está la lógica (fechas, moneda, ordenación, permisos) con entradas puras a la salida.
8. **Si una refactorización rompe 40 pruebas unitarias pero el comportamiento visual no cambia, es una señal** de que las pruebas saben más de los detalles que del comportamiento. Refactoriza las pruebas hacia consultas de rol.
9. **Importante en CI:** un solo `npm run test` debería que en un mismo Merge Request ejecutar toda la capa de integración; E2E puede funcionar como un trabajo obligatorio separado, o al final después de que pasan unit/lint.

## Resumen

El trofeo de testing remodela el modelo mental de "verificar cada función" a "*verificar la app a través del camino del usuario*". Su idea central es esta:

> **La confianza es una función de cuán cerca esté la prueba del presupuesto real, no de cuántas veces se divierte el en grimos simulados.**

- Análisis estático en base — barreras gratuitas.
- Pruebas unitarias en el tallo — donde está la complejidad.
- Pruebas de integración como cuerpo — tu producto principal.
- E2E en la parte — "la punta" del recorrido crítico.

El trofeo no destruye el de la pirámide; redirige el esfuerzo desde las pruebas unitarias que dan falsa confianza y pone la atención real en la superficie que toca el usuario: la integración.

## Referencia adicional

- Kent C. Dodds — [The Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy)
- Testing Library — [The Guiding Principles](https://testing-library.com/docs/)
- MSW — [Mock Service Worker](https://mswjs.io/docs/)
- Playwright — [Docs](https://playwright.dev/docs/intro)