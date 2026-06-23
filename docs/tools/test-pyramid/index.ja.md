---
title: テストピラミッド：バランスの取れたテスト自動化のための戦略
description: A structured testing model that guides teams to build a fast, reliable suite by investing heavily in unit tests, moderately in integration tests, and sparingly in end-to-end tests.
created: 2026-06-23
tags:
  - testing
  - test-automation
  - software-quality
  - strategy
  - ci-cd
status: draft
---

# テストピラミッド：バランスの取れたテスト自動化のための戦略

## テストピラミッドとは

テストピラミッドは、自動テストを構造化するための基礎的なメンタルモデルです。**Mike Cohn** が2009年の著書 *Succeeding with Agile* で広めたもので、ソフトウェアプロジェクトにおけるさまざまなテストタイプの理想的な比率を視覚的に示しています。ピラミッドは3つの主要な層で構成されています：

- **ベース層（ユニットテスト）** – 個々の関数やクラスに対する高速で独立したテスト。
- **ミドル層（インテグレーションテスト/サービステスト）** – コンポーネント間の相互作用（データベース、API、外部サービス）を検証するテスト。
- **トップ層（エンドツーエンドテスト）** – UIからデータベースまでカバーする、遅くて壊れやすいテスト。

各層の幅は**推奨されるテスト数**を表しています。ユニットテストはインテグレーションテストよりはるかに多く、インテグレーションテストはE2Eテストよりはるかに多く作成すべきです。

## なぜ使うのか？

テストピラミッドは、**「アイスクリームコーン」** として知られる一般的なアンチパターンを解決します。チームが時間の大半を遅くて壊れやすいUIテストの作成と保守に費やし、高速なユニットテストを軽視している状態です。これにより、以下の問題が発生します：

- フィードバックサイクルの長期化（秒単位ではなく時間単位）。
- UI変更のたびに壊れる脆弱なテストスイート。
- テスト数が多い割に信頼性が低い。
- リリース速度の低下。

テストピラミッドを採用することで、以下のメリットが得られます：

- **迅速なフィードバック** – ユニットテストはミリ秒で実行。
- **高い信頼性** – 最も低コストなレベルでバグを発見。
- **保守しやすいスイート** – E2Eテストが少ないため、破損が少ない。
- **Shift Left** – 開発サイクルの早い段階でテストを行う。

## 導入方法（プロジェクトへの設定）

テストピラミッドは戦略であり、パッケージではありません。しかし、プロジェクトを設定して層ごとにテストを実行できるようにすることで、「導入」することができます。

### 1. テストファイルを整理する

テストファイルをフォルダに分けるか、命名規則を使用します：

```
src/
├── __tests__/          # unit tests
│   ├── unit/
│   └── ...
├── __integration__/    # integration tests
└── __e2e__/            # end-to-end tests
```

### 2. テストランナーを設定して層ごとに実行する

**JavaScript/TypeScript (Jest) – `jest.config.js`**

```javascript
module.exports = {
  projects: [
    {
      displayName: 'unit',
      testMatch: ['**/__tests__/**/*.test.js'],
      testPathIgnorePatterns: ['/node_modules/']
    },
    {
      displayName: 'integration',
      testMatch: ['**/__integration__/**/*.int.js'],
    },
    {
      displayName: 'e2e',
      testMatch: ['**/__e2e__/**/*.e2e.js'],
    }
  ]
};
```

**Python (pytest) – マーカーを使用**

```python
# pytest.ini
[pytest]
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
```

テストファイル：

```python
# test_user_service.py
import pytest

@pytest.mark.unit
def test_user_full_name():
    user = User(first_name="Jane", last_name="Doe")
    assert user.full_name == "Jane Doe"
```

実行方法：

```bash
pytest -m unit
pytest -m integration
pytest -m e2e
```

**Java (JUnit 5) – タグを使用**

```java
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

@Tag("unit")
class UserServiceTest {
    @Test
    void shouldBuildFullName() {
        User user = new User("Jane", "Doe");
        assertEquals("Jane Doe", user.fullName());
    }
}
```

実行方法：

```bash
mvn test -Dgroups=unit
mvn test -Dgroups=integration
mvn test -Dgroups=e2e
```

### 3. NPMスクリプト（または同等のもの）を追加して簡単に層ごとに実行する

```json
{
  "scripts": {
    "test:unit": "jest --selectProjects unit",
    "test:integration": "jest --selectProjects integration",
    "test:e2e": "jest --selectProjects e2e",
    "test": "npm run test:unit && npm run test:integration"
  }
}
```

### 4. CI/CDに統合する（例：GitHub Actions）

```yaml
jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run test:unit

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run test:integration

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run test:e2e
```

## 主な特徴（各層の実践）

### ベース層：ユニットテスト（スイートの約70％）

- **範囲：** 単一の関数、メソッド、クラス。
- **速度：** 1テストあたり1ms未満。
- **独立性：** I/Oなし – モック/スタブを使用。
- **例：** バリデーション、計算、ユーティリティ関数。

```javascript
// unit test example (Jest)
test('adds 1 + 2 equals 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

### ミドル層：インテグレーションテスト/サービステスト（スイートの約20％）

- **範囲：** 2つ以上のコンポーネント間の相互作用（DBクエリ、APIエンドポイント、ファイルシステム）。
- **速度：** 数十～数百ミリ秒。
- **独立性：** TestContainers、組み込みデータベース、軽量サーバーを介して実際のインフラを使用。

```javascript
// integration test example (supertest + Jest)
const request = require('supertest');
const app = require('../app');

test('GET /api/users returns 200', async () => {
  const response = await request(app).get('/api/users');
  expect(response.statusCode).toBe(200);
});
```

```python
# integration test example (pytest + FastAPI)
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_users():
    response = client.get("/api/users")
    assert response.status_code == 200
```

### トップ層：エンドツーエンドテスト（スイートの約10％）

- **範囲：** UIを通じたシステム全体（ブラウザ、モバイルアプリ）。
- **速度：** 1テストあたり数秒～数分。
- **脆弱性：** UI変更に非常に敏感。
- **使用目的：** クリティカルなビジネスフローのみ（ハッピーパス）。

```javascript
// E2E test example (Playwright)
const { test, expect } = require('@playwright/test');

test('user can complete checkout', async ({ page }) => {
  await page.goto('/shop');
  await page.click('text=Add to Cart');
  await page.goto('/checkout');
  await page.fill('#email', 'test@example.com');
  await page.click('text=Place Order');
  await expect(page.locator('.confirmation')).toBeVisible();
});
```
```

## よくある落とし穴と原則

### 1. アイスクリームコーンアンチパターン

テストの80％がE2Eであるスイートは避けてください。このような場合は、UIからビジネスロジックを抽出して、クリティカルなE2Eテストをインテグレーションテストまたはユニットテストに積極的に書き換えてください。

### 2. Shift Left

E2Eテストが失敗したら、まずバグを再現するユニットテストまたはインテグレーションテストを作成します。その後、E2Eテストを削除または簡略化できることが多く、スイート全体が高速になります。

### 3. テストを独立させる

各テストは独立して、どの順序でも実行できる必要があります。共有された可変状態はフレーキーなテストの原因になります。

### 4. ユニットレベルで適切なモックを使用する

ユニットテストでは外部依存関係をモックします。インテグレーションテストでは実際のインスタンス（TestContainers、インメモリDB）を使用しますが、テスト対象のコンポーネントはモックしません。

## 結論

テストピラミッドは、現代のソフトウェアテストにおいて最も重要な概念のひとつであり続けています。これは、高速で信頼性が高く、保守可能なテストスイートを構築するための明確で実践可能なモデルをチームに提供します。ユニットテストに積極的に投資し、コンポーネントが接続する部分にインテグレーションテストを追加し、クリティカルなパスのみにE2Eテストを使用することで、高い信頼性と迅速なフィードバックの両方を実現できます。

まず、現在のテストスイートを監査することから始めてください。各層の時間と数を測定します。次に、上記の設定例を使用してテストを分離し、Shift Left の考え方を採用すれば、リリース速度が向上するのを実感できるでしょう。