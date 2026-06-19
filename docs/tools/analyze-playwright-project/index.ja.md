---
title: Playwrightプロジェクト分析: 構造、設定、ベストプラクティス
description: TypeScriptを使用した効率的なend-to-endテストのためのPlaywrightプロジェクトのセットアップ、整理、および分析に関する包括的なガイド。
created: 2026-06-19
tags:
  - playwright
  - testing
  - typescript
  - project-structure
  - automation
status: draft
---

# Playwrightプロジェクト分析: 構造、設定、ベストプラクティス

## 概要

Playwrightは、Microsoftが開発したクロスブラウザ自動化ライブラリであり、最新のWebアプリケーションのend-to-endテストのために設計されています。Chromium、Firefox、WebKit向けの統一APIを提供し、複数の言語をサポートしています。このガイドでは、PlaywrightをTypeScriptで使用し、プロジェクトのアーキテクチャを分析して、スケーラビリティ、保守性、信頼性を確保することに焦点を当てています。

適切に構造化されたPlaywrightプロジェクトは、単にテストを書くだけではありません。コードの整理、異なるブラウザやデバイス向けのプロジェクト設定、**auto‑waiting**と**web‑first assertions**の活用、そして**Trace Viewer**や**HTML Reporter**などのツールを使用して実行を分析することが含まれます。新しく始める場合でも、既存のスイートをレビューする場合でも、これらのパターンを理解することが重要です。

---

## なぜPlaywrightプロジェクトを分析するのか？

- **一貫性** – すべてのチームメンバーが同じパターンに従うことを保証します。
- **フレーキネスの低減** – auto‑waitingにより多くのタイミング問題が解消されますが、リトライとプロジェクトの適切な設定は依然として重要です。
- **保守性** – 明確な関心の分離（page objects、fixtures、utilities）により、テストの更新が容易になります。
- **パフォーマンス** – プロジェクトレベルの依存関係とシャーディングにより、CIの実行時間が短縮されます。
- **デバッグ** – Trace ViewerとHTMLレポートは豊富な診断情報を提供します。それらを有効にして分析する方法を知ることが重要です。

---

## Playwrightプロジェクトのセットアップ

```bash
# Create a new Node.js project and initialize Playwright with TypeScript
npm init playwright@latest
```

TypeScriptを選択し、必要に応じてGitHub Actionsワークフローを追加します。これにより、次のデフォルトのファイル構造が作成されます。

```
my-project/
├── playwright.config.ts
├── package.json
├── tests/
│   └── example.spec.ts
├── page-objects/         # (common convention)
├── fixtures/             # (custom fixtures)
└── utils/                # (helper functions)
```

---

## プロジェクト構造のベストプラクティス

目標は、**テストロジック**、**ページ操作**、**設定**を分離することです。一般的なパターン：

```tree
src/
├── tests/
│   ├── login.spec.ts
│   ├── checkout.spec.ts
│   └── profile.spec.ts
├── pages/
│   ├── login.page.ts
│   ├── checkout.page.ts
│   └── profile.page.ts
├── fixtures/
│   └── custom-fixtures.ts
├── utils/
│   ├── helpers.ts
│   └── data-generator.ts
└── playwright.config.ts
```

### Page Object Model (POM)

ページ操作をクラスにカプセル化します：

```typescript
// pages/login.page.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;

  constructor(public readonly page: Page) {
    this.usernameInput = page.getByLabel('Username');
    this.passwordInput = page.getByLabel('Password');
    this.loginButton = page.getByRole('button', { name: 'Sign in' });
  }

  async login(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
    await this.page.waitForURL('/dashboard');
  }
}
```

### Custom Fixtures

**fixtures**を使用して、テスト間で状態とpage objectsを共有します：

```typescript
// fixtures/custom-fixtures.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/login.page';

type MyFixtures = {
  loginPage: LoginPage;
};

export const test = base.extend<MyFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },
});

export { expect } from '@playwright/test';
```

その後、スペックファイルで`./fixtures/custom-fixtures.ts`から`test`を使用します。

---

## 設定の分析

`playwright.config.ts`ファイルはプロジェクトの動作を定義します。分析および最適化すべき主要なセクション：

### 基本設定

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  retries: process.env.CI ? 2 : 0,
  fullyParallel: true,
  reporter: [['html', { outputFolder: 'playwright-report' }]],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 12'] },
    },
  ],
});
```

### プロジェクトの依存関係

あるプロジェクトを別のプロジェクトに依存させることができます（例：すべてのテストの前にセットアップテストを実行する）：

```typescript
projects: [
  { name: 'setup', testMatch: /setup\.global\.ts/ },
  {
    name: 'chromium',
    dependencies: ['setup'],
    use: { ...devices['Desktop Chrome'] },
  },
]
```

### 環境固有の設定

環境変数や個別の設定ファイルを使用して、異なる環境ごとに設定を上書きします。

---

## テストの実行と結果の分析

```bash
# Run all projects
npx playwright test

# Run a specific project
npx playwright test --project=chromium

# Run tests with GUI mode
npx playwright test --ui

# Show HTML report after run
npx playwright show-report
```

### HTMLレポートの解釈

- **合格/不合格ステータス** テストとプロジェクトごと。
- **タイムラインとリトライ** – 赤いハイライトはフレーキーなテストを示します。
- **添付ファイル** – スクリーンショット、トレース、動画。

![HTMLレポートのサンプル](https://playwright.dev/img/playwright-report.png)

### Trace Viewerの使用

設定でトレースを有効にします：

```typescript
use: {
  trace: 'on-first-retry',  // or 'on', 'retain-on-failure'
}
```

その後、レポートから、またはCLIを介してトレースファイルを開きます：

```bash
npx playwright show-trace test-results/trace-*.zip
```

Trace Viewerは次を表示します：
- 各アクションでのDOMスナップショット
- ネットワークリクエスト
- コンソールログ
- パフォーマンスデータ

---

## 分析のための高度なテクニック

### ネットワークのインターセプトとモッキング

テストは外部APIに依存するべきではありません。**route**を使用してネットワークリクエストをスタブ化または変更します：

```typescript
await page.route('**/api/data', route => {
  route.fulfill({ status: 200, body: fakeData });
});
```

### ビジュアルリグレッションテスト

Playwrightのスクリーンショット比較アサーションはUIのリグレッションを検出できます：

```typescript
await expect(page).toHaveScreenshot('homepage.png');
```

UIを意図的に変更した場合、`--update-snapshots`を指定して実行し、ベースライン画像を更新します。

### CI統合

CIでは、**シャーディング**を使用して実行時間を短縮します：

```yaml
# GitHub Actions example
- name: Run tests (shard 1/4)
  run: npx playwright test --shard=1/4
```

また、**レポータープラグイン**も検討してください。例えば、AI生成の障害分析でHTMLレポートに注釈を付けるツール（研究で言及されている「Playwright Test Report Analyzer」など）があります。

---

## よくある落とし穴とその修正方法

| 問題 | 原因 | 解決策 |
|-------|-------|----------|
| フレーキーテスト | 待機不足; 要素の準備ができていない | auto‑waitingに依存; 手動の`waitForTimeout`を避ける |
| テストスイートが遅い | リソース分離なしの過剰な並列テスト | ワーカー数を制限; 共有状態にテストフィクスチャを使用 |
| 失敗理由が不明確 | 失敗時にトレースやスクリーンショットがない | `trace: 'retain-on-failure'`を設定; `afterEach`でスクリーンショットを追加 |
| 保守が難しい | page objectsがファイルに分散 | 一貫したPOM構造を採用; フィクスチャを使用 |

---

## 結論

Playwrightプロジェクトを分析するとは、その**構造**、**設定**、および**ツール**を調査して、信頼性が高く、高速で、保守が容易であることを確認することを意味します。ここで説明したパターン（page objects、カスタムfixtures、プロジェクトレベルの並列処理、トレース表示、ネットワークモッキング）に従うことで、単純なテストスイートを堅牢なQA基盤に変えることができます。

Playwrightの組み込み機能は多くの従来の課題を処理します。あなたの役割はそれらを効果的に調整することです。

---

## 参考文献

- [Playwright Documentation](https://playwright.dev/docs/intro)
- [Playwright Project Configuration](https://playwright.dev/docs/test-projects)
- [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer)
- [Playwright HTML Reporter](https://playwright.dev/docs/test-reporters#html-reporter)