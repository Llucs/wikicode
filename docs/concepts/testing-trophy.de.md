---
title: "Die Testing Trophy: Priorisierung von Integrationstests in modernen Web-Apps"
description: "Ein Praxisleitfaden zu Kent C. Dodds' Testing-Trophy-Modell – eine Strategie, die Integrationstests ins Zentrum rückt und statische Analyse, Unit-Tests und E2E-Tests als unterstützende Ebenen nutzt."
created: 2026-08-08
tags:
  - testing
  - frontend
  - integration-testing
  - react
  - quality
status: draft
---

# Die Testing Trophy: Priorisierung von Integrationstests in modernen Web-Apps

## Was es ist

Die **Testing Trophy** ist eine Teststrategie-Metapher, die Kent C. Dodds 2017 für moderne JavaScript/TypeScript-Web-Anwendungen entwickelt hat. Während die klassische **Testing-Pyramide** *viele Unit-Tests* an der Basis und *wenige End-to-End-Tests* an der Spitze platziert, dreht die Trophy die zentrale Investition um: Die größte Testschicht ist die **Integrationstest**-Ebene, unterstützt durch:

- **Statische Analyse** (Linting, Formatierung, Typprüfung) als Basis;
- **Unit-Tests** als kleine, aber nützliche Schicht;
- **End-to-End-Tests** als wenige, langsame, aber wertvolle Durchläufe an der Spitze.

Im Trophy-Modell entsteht das verlässlichste Signal dafür, dass eine App funktioniert, dadurch, dass man sie über ihre echten, benutzernahen Verbindungen testet – zusammengehörige Komponenten, echte Formulare, echte DOM-Abfragen, echte `fetch`-Aufrufe gegen eine gestubbte Netzwerkgrenze – nicht durch isoliert getestete Funktionen, bei denen ganze Module weggemockt wurden.

## Warum es wichtig ist

Die Empfehlung der Pyramide, „viele Unit-Tests zu schreiben“, funktioniert gut für reine Logik, aber bricht bei UI-zentrierten Anwendungen. Wenn eine Frontend-Codebasis überwiegend mit Unit-Tests abgedeckt ist, die jedes benachbarte Modul mocken:

- Tests prüfen zunehmend **Implementationsdetails** statt Verhalten.
- Ein Refactoring, das exakt dieselbe UX erhält, kann Dutzende Tests brechen.
- Echte Verdrahtungsfehler (falscher Prop-Name, fehlendes `aria-label`, falsche API-Payload) schlüpfen durch, weil jede Einheit in Isolation getestet wird.

Integrationstests – gerenderte App-Ausschnitte, die die realistische Interaktionen durchlaufen – decken genau solche Lücken auf. Die Trophy macht sie zur Erstklässigkeit und gibt dir damit **mehr Vertrauen pro Test-Dollar**.

## Das Modell im Bild

```
                   ┌────────────┐
                   │    E2E    │  ← kritische Pfade, langsam, wenige
                   └────────────┘

              ┌─────────────────────┐
              │  Integrationstests  │  ← Trophähenhauptteil: das größte
              │                     │    Stück deines Aufwands
              └─────────────────────┘

              ┌─────────────────────┐
              │     Unit-Tests      │  ← komplexe Logik, gezielt
              └─────────────────────┘

             ┌─────────────────────────┐
             │  Statik+Typprüfung       │  ← ESLint, TypeScript,
             └─────────────────────────┘  Prettier; beinahe kostenlos
```

Das bekannte Leitprinzip der Testing Library passt genau zu diesem Modell:

> Je mehr deine Tests der Art ähneln, in der deine Software verwendet wird, desto mehr Vertrauen geben sie dir.

## Die Ebenen im Einzelnen

| Ebene | Werkzeuge | Aufwand beim Schreiben | Vertrauensgewinn pro Test | Einsatzzeit |
| --- | --- | --- | --- | --- |
| **Statistische Analyse** (Basis) | ESLint, TypeScript, Prettier | Fast surf Null | Findet Tippfehler, Typfehler, schlechte API-Verträge, bevor der Test läuft | überall; das ist dein Sicherheitsnetz |
| **Unit-Tests** (Stiel) | Jest, Vitest | Gering | Hoch für isolichte Logik; niedrig für App-Verdrahtung | pure Funktionen mit Verzweigungslogik |
| **Integrationstests** (Trophfaventeil) | Vitest/Jest + Testing Library, MSW | Mittel | **Am höchten für die App-Verdrahtung** | Komponenten, Datenströme, API-Interaktion |
| **E2E-Tests** (Spitze) | Playwright, Cypress | Hoch, langsam, manchmal flaky | Hoch, aber mit Integrationstests duplikat | kritische Business-Pfade (Login, Checkout) |

### 1. Statische Analyse – die Basis

Statische Tools schützen das gesamte System zu den geringsten Kosten: kein DOM-Aufbau, keine CI-Minuten, sofortiges Feedback. Dazu gehören:

- **Linter**, die häufig Fehler und Stilabweichungen vermeiden;
- **Typprüfer**, die die Form jedes Funktions- und Komponentenvertrags überprüfen;
- **Formatierer**, die den Diff sauber halten.

### 2. Unit-Tests – der Stiel

Unit-Tests haben eine echte Aufgabe: schwierige, pure Logik prüfen, die ist zu komplex, um sie allein über die UI abzudecken. Beispiel: Datumformatierung, Steuerberechung, URL-Aufbau. Der Gewinn ist nur dann hoch, wenn jeder Test den Vertrag *genau dieser Funktion* prüft und höchstens die direkten Eingaben, Mockt.

### 3. Integrationstests – der Hauptteil der Trophy

Ein typischer Integrationstest rendert einen **echten Teil der App** – eine Seite oder Komponente – und treibt sie über benutzernahe Ereignisse (Jeben, Klicken, Senden), während das echte DOM in einer Browserlaufen-Browserumgebung (jsdom, happy-dom) verfügbar ist. Echte HTTP-Grenzen wie HTTP werden an der **Kante** mit Werkzeugen wie MSW (Mock Service Worker) umgehen.

### 4. E2E-Tests – die Spitze

Einige wenige Playwright/Cypress-Durchläufe, die die gesamte App in einem richtigen Browser ausführen. Nutze sie für die Abläufe, die du manuell durchgehen würdest Anmeldung, Checkout, Onboarding. Behandler sie wie ein Audit, nicht wie ein Werkzeug für den Kompletttest: Sie sind zu langsam und zerbrechlich für jeden Randfall.

## Ein vollständiges Beispiel: Login-Workflow

Schauen wir uns das Vorgehen in einer realistische React- + TypeScript- + Vite-Praxis an.

### Projekt-Setup

``bash
# App erstellen
npm create vite@latest trophy-demo -- --template react-ts
cd trophy-demo

# Abhängige Dinge je Ebene installieren
npm i -D typescript @types/react @types/react-dom \
  eslint vitest jsdom \
  @testing-library/react @testing-library/user-event @testing-library/jest-dom \
  msw @playwright/test

# Browser installieren
npx playwright install
```

Skripte hinzufügen:

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

### Statique Ebene: Typen + Lint

```json
{
  "compilerOptions": {
    "strict": true,
    "jsx": "react-jsx"
  }
}
```

Statische Ebene in CI:

```bash
npm run typecheck && npm run lint
```

### Die Komponente, die wir testen

Führe den Test mit genau der Komponente aus, die auch der Nutzer sieht. Beachte: die **Netzwerkgrenze** ist das einzige, was mit der Umgebung zusammenkommt.

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

### Unit-Ebene: ein reinen Helfer

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

### Integrationsebene: der Trophäenhauptteil

Vitest mit einem DOM und den Testing-Library-Matchern einrichten:

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
// MSW: macht Integrationstests möglich, weil die Stubs an der HTTP-Grenze sind,
// die Komponente nutzt aber noch das echte `fetch`.
import { setupServer } from "msw/node";

export const server = setupServer();
```

Jetzt der Login-Ablauf, wie ihn Benutzer eintippt:

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

Achte darauf, was der Integrationstest **nicht tut**:

- Er mockts colon `LoginForm` oder ihre internen Module.
- Er prüft nicht React-State oder den `fetch`-Aufruf.
- Er spielt die API-Grenze – genau das, was die echte Server es wäre – mit MSW.

Das heißt: Der Test scheitert genau dann, wenn die `fetch`-Payload, die Response-Verarbeitung, das `Label`, der Button-Typ oder die Darstellung des Erfolgs verdrahtet sind – genau das Vertrauen, das die Trophyzentral.

### E2E-Ebene: die Spitze der Trophy

Playwright für die ein oder zwei „Pilger“-Abläufe verwenden.

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

Der E2E-Test ist fast identisch mit dem Integrationstest – das ist richtig. E2E existiert als Bestätigung, dass Production/Staging wirklich startet, Routing funktioniert, die API antwortet und nichts der Infrastruktur funktioniert. Deshalb reicht für kritische Features ein oder zwei Stück.

## Mocking-Strategie: Mock an der Grenze, niemals nach innen

Die Grenze zwischen sinnvollem Integrationstest und wertlosem Test ist *wo* man mockt.

| Was Sie gerne mockt | Trophy-Empfehlung |
| --- | --- |
| Globaler Service oder API-Call (`fetch` – network) | ✅ Nutze MSW / `server.use` an dieser Grenze |
| Third-Party-Zahlungs-SDK in einem an dünnen Wrapper | ✅ Stubbt seine öffentliche Schnittstelle |
| Ein Context-Provider oder Alert-System innerhalb derselben App | ❌ Rendere über den Provider, wenn der User es spürt |
| Eine untergeordnete Komponente auf der Seite | ❌ Dadurch werden Verdrahtungsprüfung wirkungslos |
| `useState`/React-interner Zustand | ❌ Testest das gerenderte Ergebnis |

Warum sollte man nicht die interne Antwort? Sobald du eine Komponente im Inneren wegkoppst, hast du die Fähigkeit verloren, den eigentlichen Endnutzer-Bug zu finden, für den die Trophy da ist.

## Abwägungen

### Wann die Trophy gewinnt

- **UI-dominate Frontends**: Der Wert liegt in Verdrahtung von Komponenten und Services.
- **Teams mit wenig Zeit**: Integrationstests decken Montagen ab, die die langsame E2E-Suite nicht schafft.
- **Projekte, die React/Vue/Svelte Testing-Library verwenden**: Deren Suchmethoden sind für Integrationflows gebaut.

### Wann die Trophy nicht passt

- **Reine Bibliotheken und CLI-Tools** – hier bleibt ein großes Set an Unit-Tests die beste Lösung. Kein DOM, kein Seitenfluss.
- **Backend- oder Geschäftslogik** – Unit-Tests für reine Dienste bieten mehr als ein ausgibiger Web-Integration-Suite.
- **Leegacy mit verworrenem Komponentenbaum** – manchmal braucht es erst kleinere „Slice“-Tests. Starte mit wenigen Scheiben, nicht mit einer vollständigen Matrix.
- **Hobby-/Experimentalbasis** mit µ fragilem Test-Einhof – E2E wir flakes haltig. Integration bleibt trotzdem sinnvoll, aber bewusst.

### Tabelle: Pyramide vs. Trophy vs. Honeycomb

| Strategie | Fokus | Typisches Beispiel | Am stärksten bei |
| --- | --- | --- | --- |
| **Testing-Pyramide (Cohn)** | Hunderte Unit-Tests; wenige E2E | Klassische Backend-Suites | Backend mit reiner Logik und schneller CI |
| **Testing Trophy (Dodds)** | Integrationstests in der Mitte; statische Basis; wenige E2E | React-/Vue-Web-Atom UI | komponentenbasierte Apps |
| **Testing-Honeycomb** | Mittelfeld und Stirn voll (Integration + E2E) | Verteilte Dienste mit vielen Verträgen | komplexe Service-Interaktion |

Die Trophy ist nicht die „immer richtige“ Antwort – sie ist aber der kosteneffizienteste Standard für *Web-UI*-Anwendungen.

## Best Practices

1. **Mache statische Analyse zur Basis.** Lass in CI zuerst `tsc --noEmit`, `eslint .` und Prettier laufen, bevor langsame Tests ablaufen. Nutze das zum Aufwärmen: Typ-Check fängt die Hälfte aller Bugs ab, bevor überhaupt ein Test ausgeführt wird.
2. **Standardmäßig Integrationstests schreiben.** Für Abschluss, Warenkorbauswahl, Dashboard-Rendering: ein test von „Session-Workflow“ mit benutzerzentrierten Queries. Verwende die Netzgrenze bei MSW.
3. **Fragen wie ein Nutzer.** Nutze `getByLabelText`, `getByRole`, `getByPlaceholderText`, `findByText` statt `data-testid` oder CSS-Klassen.
4. **Warte auf real asynchrones Verhalten.**`findBy*`/`waitFor` verwenden, wenn asynchron etwas auftritt. Keine künstlichen `setTimeout` in Tests.
5. **Mock nur an den Grenzen.** Netz, Zeitgeber, Browser local. In Google: Verwende nicht einfach Jest, um die Komponente, die du testest, nach innen zu mocken.
6. **E2E als Audit, nicht als Regressionstool.** Die E2E-Liste kurz halten – Login, ImCheckout, Onboarding. Mehr als riesige E2E-Suite aus Aufwand und Flako neu.
7. **Unit-Tests für knifflige Logik.** Date-Parsing, Währung, Sortierung, Permissions – hier bleibt asserts die jeweilreine Funktion wirksam.
8. **Wenn ein Refactoring 40 Unit-Tests bricht, aber das sichtbare Verhalten identisch bleibt, ist das ein Signal**, dass die Tests mehr Implementation als Verhalten wissen. Refactore die Tests in Richtung Rolle/nutzbare Abfragen.
9. **Für die CI: Eine einzige `npm run test`-Pipeline muss die komplette Integrationsebene im MR laufen. E2E-Tests können separater Pflicht-Job oder danach mit Prettier/Lint/Unit/Pipe laufen.

## Zusammenfassung

Die Testing-Trophy verlagert das Denken von „Jede Funktion in Teilen testen“ zu „*Teste die App über die Benutzerpfade wirklich*“ Ihr zentraler Gedanke an das:

> **Vertrauen entsteht daraus, wie nah der Test an echtes Nutzer zeigt ist – nicht wie viele Male die Unit die App in isolierte Ecken.**

- Statische Analyse als Basis: kostenlose Leitplanken.
- Unit-Tests im Stiel: wo Logik komplex ist.
- Integrationstests das Hauptteil: deine wichtigste Absicherung.
- E2E oben: Markstein eines kritischen Pfads.

Die Trophy entfernt Pyramiden nicht; sie lenkt die Energie von fake-confidence Unit-Tests um die Oberfläche, die der Nutzer wirklich berührt: die Integration.

## Weiterführende Referenzen

- Kent C. Dodds — Die [Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy)
- Testing Library — [Leitprinzipien](https://testing-library.com/docs/)
- MSW — [Mock Service Worker](https://msgsjs.io/docs/)
- Playwright — [Dokumentation](https://playwright.dev/docs/intro)