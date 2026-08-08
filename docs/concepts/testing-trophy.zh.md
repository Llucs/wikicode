---
title: "测试奖杯：在现代 Web 应用中优先进行集成测试"
description: "一份实践指南：Kent C. Dodds 的测试奖杯模型——将集成测试置于中心，并用静态分析、单元测试和端到端测试作为支撑层。"
created: 2026-08-08
tags:
  - testing
  - frontend
  - integration-testing
  - react
  - quality
status: draft
---

# 测试奖杯：在现代 Web 应用中优先进行集成测试

## 它是什么

**测试奖杯**是 Kent C. Dodds（2017 年）为现代 JavaScript/TypeScript Web 应用创建的测试策略隐喻。在经典的**测试金字塔**中，*大量单元测试*位于底座，*少量端到端测试*位于塔尖；而奖杯模型则反转了核心投入：最大的测试部分是**集成测试**层，由以下几层支撑：

- **静态分析**（lint、格式化、类型检查）作为底座；
- **单元测试**作为较小但有用的层级；
- **端到端测试**作为少量缓慢但高价值的用户路径，位于顶部。

在奖杯模型中，应用是否能工作的最可靠信号，来自于通过真实的用户可见线路来使用它——组件被真正安装、真实表单、真实 DOM 查询、在桩掉的网络边界上真实的 API fetch 调用——而不是为了把整个模块都 mock 掉而锁在隔离区里的函数。

## 它为什么重要

金字塔的“写大量单元测试”建议对纯逻辑有效，但对 UI 型应用会失效。当一个前端代码库大部分单元测试都在 mock 相邻模块时：

- 测试会开始断言**通过的细节**，而不是行为；
- 一次不改变用户展示效果的重构，可能破坏数十个测试；
- 真正的装配错误（prop 名写错、缺少 `aria-label`、API payload 错误）逃过了测试，因为每个单元都在隔离状态中测过。

集成测试——渲染应用切片、用真实用户交互去驱动它们——能抓住这些线路空白。奖杯模型把集成测试放回一等公民的位置，让你**在测试上花得越多钱，收回的信心越多**。

## 模型一览

```
                The trophy in one picture:

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

同样，Testing Library 给出的广为人知的指导原则正适合这一模型：

> 测试越接近软件被使用的方式，它们给你的信心就越多。

## 按层分层解析

| 层级 | 工具 | 编写成本 | 每个测试的信心收益 | 该什么时候用 |
| --- | --- | --- | --- |
| **静态分析**（底座） | ESLint, TypeScript, Prettier | 几乎为零 | 在测试运行前发现实验细节、类型错误和糟糕的 API 契约 | 到处用；这是你的安全网 |
| **单元测试**（茎） | Jest, Vitest | 低 | 对纯逻辑高；对应用接线两端 | 复杂的纯函数 / 分支逻辑 |
| **集成测试**（奖杯主体） | Vitest/Jest + Testing Library, MSW | 中等 | **对应用装配线路最高** | 页面、组件、API 交互 |
| **E2E 测试**（顶部凝一人） | Playwright, Cypress | 高、慢、有时不稳定 | 高但是被集成测试覆盖 | 关键业务路径（登录、结算） |

### 1. 静态分析——底座

静态测试工具挡住整个系统，成本数千：不需要 DOM、不跑 CI 分钟、反馈即时。包括：

- **Linter** 预防常见的坑并保证风格：
- **类型检查器**验证函数、组件类型的契约；
- **格式化工具**让 diff 干净整洁。

### 2. 单元测试——茎部

单元测试有它的实际担当：验证困难的纯逻辑，是通过 UI 不容易触达的。例子有：日期格式化、税费计算、URL 构造器。只有每个测试都盯着那个函数的契约、最多只 mock 一些直接输入时，整体收益才最高。

### 3. 集成测试——奖杯的主体

一个典型集成测试渲染**真实的应用切片**（一个页面或组件），并用用户可感知的事件（键入、点击、提交）来驱动它，而且真实 DOM 可以渲染在无浏览器环境（jsdom、happy-dom）里。真正的异步边界（如 HTTP）用诸如 MSW（Mock Service Worker）这类工具在**边缘**处打桩。

### 4. E2E 测试——顶部

用几个 Playwright/Cypress 流程，在真实浏览器里跑完整个应用。这些测试只给了那些你会在生产环境里手工完整走一遍的流程：注册、结账、上手指引。把这些成为审计型测试，而不是回归测试工具——它们太慢、太容易 break 了。

## 一个完整的登录流程例子

我们来看看在一个真实 React + TypeScript + Vite 应用中，每一层看起来长什么样。

### 项目初始化

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

添加 scripts：

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

### 可配置层：类型 + 检查

```json
{
  "compilerOptions": {
    "strict": true,
    "jsx": "react-jsx"
  }
}
```

CI 中的静态层：

```bash
npm run typecheck && npm run lint
```

### 我们测试的组件

使用和真实用户一样的组件运行测试。注意这个**网络边界**才是唯一与时实际操作环境的点。

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

### 单元层：一个纯辅助函数

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

### 集成层：奖杯主体

用 Vitest 准备好类浏览器的 DOM 和 Testing Library 匹配器：

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

现在，像真实用户那样去测试：

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

注意这个集成测试**不会**做什么：

- 它不会 mock `LoginForm` 或它的内部子模块。
- 它不会检查 `fetch` 调用或 React state。
- 它只在 API 边界打桩——这正是真实服务器响应的位置——并且用 MSW。

这表示：如果 fetch 的 payload、后端响应处理、label 文本、button 类型或成功渲染变化，测试就会失败。这正是奖杯模型所关心的下单。

### E2E 层：顶部

用 Playwright 跑一两天“朝圣”流程。

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

E2E 测试和集成测试几乎一模一样——这是对的。E2E 的存在是为了验证：生产/预发布构建可以启动、路由正确、API 有响应、基础设施没有回退。因此，每个关键功能有一条两条就够了。

## Mock 策略：在边缘打桩，不要往内部打桩

集成测试有没有用，它的分界线是“mock 发生在哪个位置”。

| 你想 mock 的东西 | 奖杯模型的建议 |
| --- | --- |
| 全局服务或 API 调用（`fetch` 网络） | ✅ 使用 **MSW** / `server.use` 在边界处打桩 |
| 对第三方支付 SDK 薄封装 | ✅ 直接对公共接口打桩 |
| 同一个应用中的 Provider 或提示系统 | ❌ 用户你会通过它，就真的很干活 |
| 页面内部的某个子组件 | ❌ 这会打坏“装配”正在检查的东西 |
| `useState` / React 内部 state | ❌ 测试渲染结果 |

为什么？：因为你只要把内部组件 mock 掉，实际用户的“装配 bug”将没有被接住的可能——而这个 bug 正是奖杯模型想要找的。

## 取舍

### 奖杯模型赢的场景

- **UI 重的前端**：核心收益在组件与服务的装配中。
- **测试时间有限的团队**：集成测试能覆盖慢速 E2E 没有时间覆盖的路径。
- **用了 React/Vue/Svelte Testing Library 的项目**：它的查询 API 本来就是为集成流程设计规化。

### 奖杯形状不太合适的场景

- **纯函数库 / CLI 工具**：大量单元测试仍然是最好选择。没有 DOM、没有页面 flow。
- **后端想法、业务算法**：用纯服务单元测试，比整个 Web 集成套件更合适。
- **还在实验阶段的代码库**、测试后端不稳定：E2E 会一直 flaky。集成测试仍然有用，但要克制。
- **巨大且组件树缠在一起的遗留应用**：先从“切片”开始，而不要追张做整个矩阵。

### 表格：金字塔 vs. 奖杯 vs. 蜂窝

| 策略 | 重点 | 典型例子 | 什么状态下最有效 |
| --- | --- | --- | --- |
| **测试金字塔（Cohn）** | 单元测试重量级、少量 E2E | 经典后端套件 | 后端强逻辑、CI 快速 |
| **测试奖杯（Dodds）** | 集成测试为主体；静态底座；少量 E2E | 面向 Web UI 的组件化前端 | 组件装配多的前端 |
| **测试蜂巢（Honeycomb）** | 中间和上层都很重（集成+E2E） | 有很多契约的分布式服务 | 服务之间交互复杂 |

奖杯模型不是“永远正确”的方案，它只是对 *Web UI* 默认最划算的选择。

## 最佳实践

1. **底线防在静态分析**：在 CI 里先跑 `tsc --noEmit`、`eslint .` 和 Prettier。测试开始前，类型系统就已经抓掉往四近一半的 bug。
2. **默认写集成测试**：对注册、登录、表单提交、仪表盘组件：输入一个个简短的、面向用户的测试脚本，网络用 MSW。
3. **像用户一样查询**：使用 `getByLabelText`、`getByRole`、`getByPlaceholderText`、`findByText`，不要用 `data-testid` 或 CSS 类选择器。
4. **等待真实结果**：异步结果用 `findBy*` / `waitFor`；不要用 `setTimeout`。
5. **只在边界上打桩**：网络、时钟、浏览器 localStorage。正是部分用户要求你打内部依赖。
6. **E2E 是审计，不是回归**：两三个关键流程——登录、支付、onboarding。200 个 E2E 用例，基本只看告诉你速度和 flaky 的成本。
7. **单元测试只留给“难数学”**：日期、金额、规则、排序、权限——纯粹的输入→输出。
8. **如果重构只破坏了 40 个单元测试而 UI 没变，说明测试生活习惯比行为更多**：把测试改成角色行为查询。
9. **CI 中有个点**：一个 `npm run test` 应该在 MR 里跑完整个集成层；E2E 可作为单独的一条 Required Job，或放在 lint/unit 之后再跑。

## 总结

测试奖杯把心智模型从“**验证每个函数**”转向“**通过用户路径来验证应用**”。它的核心洞察是：

> 信心回报不来自 split 出多少个 mock 掉的角落，而来自测试是否和真实使用方式足够接近。

- 静态分析在最下方——免费的护栏
- 单元测试在茎部——处理复杂逻辑
- 集成测试在主体——你真正能依赖的保证
- E2E 在最上面——关键路径的“你到这里就值得”

奖杯模型不推翻金字塔，它只是把力气从“mock 掉一切的虚假单元测试”里省出来，放到用户真正触摸的那个层——**集成层**。

## 更多参考

- Kent C. Dodds — [The Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy)
- Testing Library — [The guiding principles](https://testing-library.com/docs/)
- MSW — [Mock Service Worker](https://mswjs.io/docs/)
- Playwright — [Docs](https://playwright.dev/docs/intro)