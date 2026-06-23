---
title: 测试金字塔：平衡测试自动化的策略
description: 一种结构化的测试模型，指导团队通过大力投资单元测试、适度投资集成测试和谨慎投资端到端测试，来构建快速可靠的测试套件。
created: 2026-06-23
tags:
  - testing
  - test-automation
  - software-quality
  - strategy
  - ci-cd
status: draft
---

# 测试金字塔：平衡测试自动化的策略

## 它是什么

测试金字塔是构建自动化测试的基础思维模型。由 **Mike Cohn** 在其 2009 年著作《*敏捷成功之道*》中推广，它直观地描述了软件项目中不同测试类型的理想比例。该金字塔包含三个主要层级：

- **底层（单元测试）** – 针对单个函数或方法或类进行快速、隔离的测试。
- **中间层（集成/服务测试）** – 验证组件之间交互的测试（数据库、API、外部服务）。
- **顶层（端到端测试）** – 缓慢、脆弱的测试，涵盖从 UI 到数据库的完整用户工作流。

每一层的宽度代表了**推荐的测试数量**——单元测试的数量应远多于集成测试，而集成测试的数量又应远多于 E2E 测试。

## 为什么要用它？

该金字塔解决了常见的反模式 **“冰淇淋蛋筒”**：团队将大部分时间花在编写和维护缓慢、脆弱的 UI 测试上，而忽略了快速的单元测试。这会导致：

- 反馈周期长（数小时而非数秒）。
- 测试套件脆弱，每次 UI 变更都会中断。
- 尽管测试数量多，但信心不足。
- 发布速度变慢。

采用测试金字塔能为你带来：

- **快速反馈** – 单元测试在毫秒级运行。
- **更高的信心** – 在最便宜的层级捕获错误。
- **可维护的套件** – 较少的 E2E 测试意味着更少的中断。
- **左移** – 在开发周期早期测试逻辑。

## 如何“安装”它（在你的项目中设置）

测试金字塔是一种策略，而非一个包。但你可以通过配置项目来支持按层级运行测试，从而“安装”它。

### 1. 组织你的测试文件

将测试分离到文件夹中或使用命名约定：

```
src/
├── __tests__/          # unit tests
│   ├── unit/
│   └── ...
├── __integration__/    # integration tests
└── __e2e__/            # end-to-end tests
```

### 2. 配置你的测试运行器以分别运行各层级

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

**Python (pytest) – 使用标记**

```python
# pytest.ini
[pytest]
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
```

测试文件：

```python
# test_user_service.py
import pytest

@pytest.mark.unit
def test_user_full_name():
    user = User(first_name="Jane", last_name="Doe")
    assert user.full_name == "Jane Doe"
```

运行方式：

```bash
pytest -m unit
pytest -m integration
pytest -m e2e
```

**Java (JUnit 5) – 使用标签**

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

运行方式：

```bash
mvn test -Dgroups=unit
mvn test -Dgroups=integration
mvn test -Dgroups=e2e
```

### 3. 添加 NPM 脚本（或等效方式）以便便捷地运行各层级

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

### 4. 集成到 CI/CD 中（例如 GitHub Actions）

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

## 关键特性（实践中的层级）

### 底层：单元测试（约占套件的 70%）

- **范围：** 单个函数、方法或类。
- **速度：** 每个测试 <1 毫秒。
- **隔离性：** 无 I/O – 使用模拟/桩。
- **示例：** 验证、计算、工具函数。

```javascript
// unit test example (Jest)
test('adds 1 + 2 equals 3', () => {
  expect(sum(1, 2)).toBe(3);
});
```

### 中间层：集成/服务测试（约占套件的 20%）

- **范围：** 两个或多个组件之间的交互（数据库查询、API 端点、文件系统）。
- **速度：** 几十到几百毫秒。
- **隔离性：** 通过 TestContainers、嵌入式数据库或轻量级服务器使用真实基础设施。

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

### 顶层：端到端测试（约占套件的 10%）

- **范围：** 通过 UI（浏览器、移动应用）的完整系统。
- **速度：** 每个测试几秒到几分钟。
- **脆弱性：** 对 UI 变更高度敏感。
- **仅用于：** 关键业务流（快乐路径）。

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

## 常见陷阱与原则

### 1. 冰淇淋蛋筒反模式

避免套件中 80% 的测试是 E2E 测试。如果出现这种情况，通过从 UI 中提取业务逻辑，积极地将关键 E2E 测试重写为集成测试或单元测试。

### 2. 左移

当 E2E 测试失败时，首先编写一个能够重现该错误的单元测试或集成测试。通常，之后你可以移除或简化该 E2E 测试，从而使整个套件更快。

### 3. 保持测试独立性

每个测试应能够隔离运行且以任意顺序执行。共享的可变状态会导致测试不稳定。

### 4. 在单元测试中使用适当的模拟

对于单元测试，模拟外部依赖。对于集成测试，使用真实实例（TestContainers、内存数据库），但不要模拟被测试的组件。

## 结论

测试金字塔仍然是现代软件测试中最重要的概念之一。它为团队提供了一个清晰、可操作的模型，用于构建快速、可靠且可维护的测试套件。通过大力投资单元测试，在组件连接处添加集成测试，并仅在关键路径上使用 E2E 测试，你可以同时获得高信心和快速反馈。

首先审计你当前的测试套件：测量每个层级的时间和数量。然后使用上面的配置示例来分离测试，采用左移思维，并观察你的发布速度提升。