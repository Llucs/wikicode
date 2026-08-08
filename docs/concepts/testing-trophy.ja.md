---
title: "テストトロフィー: モダンWebアプリにおける統合テストの優先"
description: "Kent C. Dodds氏のテストトロフィーモデルを基にした実践者向けガイド — 統合テストを中心に据え、静的解析・単体テスト・E2Eテストを支援レイヤーとして活用する戦略です。"
created: 2026-08-08
tags:
  - testing
  - frontend
  - integration-testing
  - react
  - quality
status: draft
---

# テストトロフィー: モダンWebアプリにおける統合テストの優先

## とは

**テストトロフィー**は、Kent C. Dodds（2017）がモダンな JavaScript/TypeScript Web アプリケーション向けに提唱したテスト戦略のメタファーです。古典的な**テストピラミッド**が底部に*多数の単体テスト*、上部に*少数のE2Eテスト*を置くのに対し、トロフィーは最も重要な投資先を逆転させます。最大のテストレイヤーは**統合テスト**であり、それを次の層が支えます。

- **静的解析**（Lint、フォーマット、型チェック）を基盤として
- **単体テスト**を小さいが有用なレイヤーとして
- **E2Eテスト**を少数の、遅いが価値の高いジャーニーとして頂点に

トロフィーモデルにおいて、アプリが機能するという最も信頼できるシグナルは、実際のユーザー向けの配線（コンポーネントを組み合わせ、実際のフォーム、実際のDOMクエリ、スタブ化されたネットワーク境界に対する実際の`fetch`呼び出し）を通してテストすることから得られます。モジュール全体をモックした孤立した関数から得られるのではありません。

## なぜ重要か

ピラミッドによる「単体テストを多く書け」というアドバイスは、純粋ロジックには有効ですが、UI中心のアプリでは機能しません。フロントエンドのコードベースが、周囲のモジュールをすべてモックする単体テストで大部分占められると、次のことが起こります。

- テストが**実装詳細**を検証し始め、挙動を検証しなくなる。
- UXを変えないリファクタリングによって、多数のテストが壊れることがある。
- プロップ名の誤り、`aria-label`の欠落、APIペイロードの不備など、実際の配線ミスが、個々のユニットが孤立しているために見逃される。

統合テスト — 実際的なユーザー操作を伴うアプリの断片を描画するテスト — は、そうした配線のギャップを検出します。トロフィーは統合テストを第一級の市民とし、**テスト費用あたりにより高い保証**を得られるようにします。

## モデルをひと目で

```
                   ┌────────────┐
                   │    E2E    │  ← 重要pass, 遅い, 少数
                   └────────────┘

              ┌─────────────────────┐
              │  Integration tests  │  ← トロフィーの胴体: 最も大きな
              │                     │    努力を注ぐ領域
              └─────────────────────┘

              ┌─────────────────────┐
              │     Unit tests      │  ← 複雑なロジック、補助
              └─────────────────────┘

             ┌─────────────────────────┐
             │    Static + type check  │  ← ESLint, TypeScript,
             └─────────────────────────┘  Prettier; ほぼ無料
```

このモデルに合致するテストライブラリの有名な指針があります。

> テストがソフトウェアの使われ方に近ければ近いほど、得られる信頼度は高くなります。

## レイヤーごとの内訳

| レイヤー | ツール例 | 作成コスト | 1テストあたりの信頼性向上 | 使うべきタイミング |
| --- | --- | --- | --- | --- |
| **静的解析**（基盤） | ESLint, TypeScript, Prettier | ほぼゼロ | テスト実行前にタイプミス、型エラー、API契約の不備を検出 | 常に。あなたのセーフティネットです |
| **単体テスト**（幹） | Jest, Vitest | 低 | 孤立したロジックには高い。アプリの配線に対しては低い | 分岐ロジックを持つ純粋関数 |
| **統合テスト**（トロフィーの胴体） | Vitest/Jest + Testing Library, MSW | 中 | **アプリ配線に対して最高** | コンポーネント、フロー、API連携 |
| **E2Eテスト**（頂点） | Playwright, Cypress | 高く、遅く、時々不安定 | 高いが、統合テストと重複する | 重要ビジネスジャーニー（ログイン、チェックアウト） |

### 1. 静的解析 — 基盤

静的ツールは最低コストでシステム全体を一定します。DOMのセットアップは不要、CIの分も惜しみなく、差し迫ったフィードバックが得られます。これには以下が含まれます。

- **Linter** はよくある小さいミス防止とスタイルの一貫性を実現します。
- **型チェッカー** はすべての関数・コンポーネントの契約の形を検証します。
- **フォーマッタ** は差分をクリーンに保ちます。

### 2. 単体テスト — 幹

単体テストには実際の役割があります。UIを操作するだけではテストが難しいトリッキーな純粋ロジックを検証することです。例: 日付フォーマット、税額計算、URL構築。それぞれのテストが*その関数の契約*に焦点を当て、直接の依存関係のみをモックするときに、その効果は高くなります。

### 3. 統合テスト — トロフィーの胴体

典型的な統合テストは、**ページやコンポーネントの実際の一部**を描画し、ユーザーが行う操作（タイピング、クリック、送信）で内容を押します。実際のDOM環境は、ブラウザなしで動くjsdomやhappy-domなどで用意できます。HTTPのような実際の非同期境界は、MSWのようなツールを使って**境界**でスタブにします。

### 4. E2Eテスト — 頂点

少数のPlaywright/Cypressジャーニーを本物のブラウザを通してアプリ全体を動かします。本番で手動で歩くシナリオ（サインアップ、チェックアウト、オンボーディング）に使います。これらは監査として見なすべきであり、リグレッションのテスト一式としては捉えません。遅すぎるうえ、すべてのエッジケースを対象にするには脆すぎます。

## 完全な作動例: ログインフロー

React + TypeScript + Vite の現実的なアプリで、各レイヤーがどのように見えるかを見てみましょう。

### プロジェクトのセットアップ

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

スクリプトを追加します。

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

### 静的層: 型 + Lint

```json
{
  "compilerOptions": {
    "strict": true,
    "jsx": "react-jsx"
  }
}
```

CIでの静的層の実行:

```bash
npm run typecheck && npm run lint
```

### テスト対象のコンポーネント

テストは、ユーザーが使う実際のコンポーネントに対して行います。**ネットワーク境界**だけが環境に触れる唯一のポイントです。

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

### 単体層: 純粋ヘルパー

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

### 結合層: トロフィーの胴体

Vitest をブラウザライクなDOMとTesting Libraryマッチャーで設定します。

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

では、ユーザーが入力するのと同じようにログインフローをテストします。

```tsx
// src/components/LoginForm.test.tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { server } from "../../test/server";
import { LoginForm } from " ./LoginForm";

describe("LoginForm", () => {
  it("accepts credentials and welcomes the user", async () => {
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

この統合テストが**行わない**ことに注目してください。

- `LoginForm` やその内部のサブコンポーネントをモックしていません。
- React の state や fetch の呼び出し内容を検証していません。
- API 境界 — 実際のサーバーが応答する場所 — を MSW でスタブしているだけです。

つまり、fetch のペイロード、レスポンス処理、ラベル文言、ボタンの種類、成功時表示がどこかで壊れた場合に、テストは失敗します。こそがトロフィーが求める信頼なのです。

### E2E層: トロフィーの頂点

Playwright は、1〜2の「代表的な重要なジャーニー」に使います。

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

E2Eテストは統合テストとほぼ同じ手順になります。それは正しいことです。E2Eは、本番・ステージングのビルドが起動し、ルーティングが機能し、APIに接続できて、インフラの回帰がないことを確認するためのものです。したがって、各重要機能に対して1〜2本で十分です。

## モッキング戦略: 境界でモックし、内部はモックしない

有効な統合テストと無駄なテストの分かれ目は、*どこで*モックするかです。

| モックしたくなるもの | トロフィー推奨 |
| --- | --- |
| グローバルサービスや API 呼び出し（`fetch` — ネットワーク） | ✅ **MSW** / `server.use` の境界で使う |
| 薄いラッパーの後ろにある第三者決済SDK | ✅ 公開インターフェースを通してスタブする |
| 同一アプリ内のコンテキストプロバイダやアラート連携 | ❌ ユーザーがそれを体験するなら、プロバイダを通して描画する |
| ページ内部の子コンポーネント | ❌ 配線の検証が台無しになったのです |
| `useState` / React内部状態 | ❌ レンダリング結果をテストする |

内部のものをモックして閉じれば閉じるほど、トロフィーが追い求める実際のエンドユーザーバグ検出の能力を失います。内部ではなく境界でモックすることが重要です。

## トレードオフ

### トロフィーが優れている場合

- **UI中心のフロントエンド:** 価値はコンポーネントとサービスを配線的に結びつけるところにあります。
- **時間が限られたチーム:** 統合テストは、遅いE2Eスイートではカバーできない作業内容を守ります。
- **React/Vue/Svelte Testing Library を採用しているプロジェクト:** このライブラリのクエリは統合フロー用に設計されています。

### トロフィーの形が適合しない場合

- **純粋なライブラリやCLIツール** — 大量の単体テストが最も有効です。DOMもページフローもありません。
- **バックエンドやビジネスアルゴリズム中心のプロジェクト** — 純粋な機能に対する単体テストが、ウェブ全体の結合テスト群よりもはるかに高い成果を挙げます。
- **バックエンドが不安定な、趣味や実験的なコードベース** — 頻繁に失敗するE2Eはおすすめできません。統合テストは依然有用ですが、控えめに。
- **依存関係が複雑に張り巡らされた大規模なレガシーアプリ** — 統合テストをいきなり適用するのは難しいでしょう。「スライス」をいくつか選んで始めるのがよいです。

### 比較: ピラミッド vs トロフィー vs ハニカム

| 戦略 | 重点 | 典型的な例 | 最も有用な場面 |
| --- | --- | --- | --- |
| **テストピラミッド（Cohn）** | 大量の単体テスト、少数のE2E | 古典的なバックエンドスイート | 純粋なロジックと高速CIを備えたバックエンド |
| **テストトロフィー（Dodds）** | 中央に統合テスト、静的解析を基盤、少数のE2E | React / Vue などのWebフロント | コンポーネント中心のUIアプリ |
| **テストハニカム** | 中央〜上層部が厚い（統合 + E2E） | 多数の契約を持つ分散サービス | サービス間の複雑な相互接続 |

トロフィーは「常に正しい」という答えではありません。*Web UI*に対して最もコスト効率の高いデフォルトという意味です。

## ベストプラクティス

1. **静的解析を土台にする。** CIでは遅いテストの前に`tsc --noEmit`、`eslint .`、Prettierを実行します。型チェックがテスト実行前に多くのバグを防ぎます。
2. **統合テストをデフォルトにする。** 登録、カートへの追加、ダッシュボードの表示などを、ユーザー視点のクエリを使った短いセッショップ型テストとして書きます。ネットワークにはMSWを使います。
3. **ユーザーのようにクエリする。** `getByLabelText`, `getByRole`, `getByPlaceholderText`, `findByText` を使います。`data-testid` やCSSクラスによるDOM/UIへの依存は避けます。たとえば `getByRole('button', { name: 'Sign in' })` のようにします。
4. **実際のタイミングに合わせる。** 非同期で変わる状態は `findBy*` / `waitFor` を使します。テスト内で人工的な `setTimeout` を避けます。
5. **境界だけをモックする。** ネットワーク、時計、ブラウザのlocalStorageが対象です。テスト対象コンポーネントの内部依存をモックしてはいけません。
6. **E2Eは監査であり、回帰テストではない。** E2Eリストは短く保つ（ログイン、チェックアウト、オンボーディング）。それ以外をE2Eで大量にすると、速度と不安定さというコストが高くなりすぎます。
7. **複雑な計算は単体テストで。** 日付解析、通貨、並べ替え、権限のような入出力が純粋なロジックこそ単体テストを活用します。
8. **リファクタリングでビジュアルの変化がないのに多数の単体テストが壊れたら、それはテストが実装詳細を意識すぎる証拠。** ロール(役割)ベースのクエリに書き換えましょう。
9. **CIでは:** `npm run test` により統合層を同一MR上で実行し、E2Eは必須の別ジョブにするか、ユニット／Lint成功後に実行します。

## まとめ

テストトロフィーは「すべての機能を検証する」というマインドセットを、「ユーザーの動線を通してアプリを検証する」に変えます。その中心となる洞察は次の通りです。

> **信頼性は、単体テストでモジュールをどれだけ隔離したかではなく、テストがソフトウェアの実際の使われ方にどれだけ近いかによって決まります。**

- 静的解析は土台 — 無料のガードレール。
- 単体テストは幹 — ロジックの複雑な部分を担う。
- 統合テストは胴体 — 主な安心材料。
- E2Eは頂点 — 重要なジャニーの“証印”。

トロフィーはピラミッドを否定するものではありません。しかし、モックだらけの単体テストから得られるはずの低い信頼に汲み取られず、ユーザーが触れる実際の界面 — 統合の部分に注意を向けるように、努力を向け替えます。

## 参考資料

- Kent C. Dodds — [The Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy)
- Testing Library — [The guiding principles](https://testing-library.com/docs/)
- MSW — [Mock Service Worker](https://mswjs.io/docs/)
- Playwright — [Docs](https://playwright.dev/docs/intro)