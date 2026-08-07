---
title: "backon：Python 重试库"
description: "backon 是一个现代 Python 库，用于通过可配置的退避策略自动重试失败的操作，源自 Backoff 的分支。"
created: 2026-08-07
tags:
  - python
  - retry
  - backoff
  - resilience
status: draft
---

# back-on

`back-on`（pip：`backon`）是一个简化在代码中添加重试逻辑的 Python 库。它是著名的 [`backoff`](https://github.com/litaceans/backoff) 库的一个分支，经过重新设计，提供了更具表现力、可链式调用的 API，并支持现代 Python（3.8+）。使用 `back-on`，你可以轻松处理网络调用、数据库操作、文件 I/O 或任何不稳定函数中的瞬时故障，只需使用简洁的装饰器或上下文管理器语法。

## 为什么使用 back-on？

- **人体工程学** – 无需编写显式循环或条件检查；一个装饰器即可用最少的代码注入重试行为。
- **可配置策略** – 固定延迟、指数增长、完整抖动或去相关抖动，以避免惊群效应。
- **异步支持** – 原生集成 `asyncio`，允许在异步代码中重试而不会阻塞事件循环。
- **通知钩子** – 在每次重试尝试和放弃时记录日志或输出指标。
- **零依赖** – 开箱即用；无需外部包。

## 安装

通过 pip 安装：

```bash
pip install backon
```

根据你的项目风格，你也可以将其添加到 `pyproject.toml` 或 `requirements.txt` 中。

## 基本用法

`back-on` 的核心是 `@backon.on_exception` 装饰器。它捕获指定的异常，等待计算出的延迟，然后重试被装饰的函数，直到成功或达到最大重试时间。

```python
import backon
import requests

@backon.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_tries=8,
    max_time=30
)
def fetch_data(url):
    """Fetch a URL, retrying on any request error."""
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()
```

在上面的示例中，该函数最多会被调用 8 次，两次尝试之间的延迟使用指数退避计算（从 0.1 秒开始，每次翻倍）。所有尝试的总耗时不会超过 30 秒。

## 主要特性

### 1. 多种退避策略

`back-on` 提供了一组内置的退避生成器：

| 策略                | 描述                                                                 |
|---------------------|----------------------------------------------------------------------|
| `expo`              | 指数退避：`base * 2^n`，其中 `n` 是重试次数。                       |
| `fib`               | 基于斐波那契的延迟（延迟按前两项之和增长）。                         |
| `full_jitter`       | 在 0 到当前指数退避值之间的随机延迟。                                |
| `equal_jitter`      | 将退避值拆分为随机部分和固定部分。                                   |
| `constant`          | 重试之间的固定延迟。                                                 |
| `decorrelated_jitter` | 去相关抖动退避，减少争用但又不完全随机。                           |

导入时使用 `'expo'`、`'fib'` 等常量：

```python
from backon import expo, fib, full_jitter
```

### 2. 在成功或异常时重试

默认情况下，`on_exception` 在函数**抛出**匹配的异常时重试。你也可以使用 `on_predicate` 在函数返回特定值或对象时重试：

```python
import backon

@backon.on_predicate(
    wait_gen=expo,
    predicate=lambda x: x is None,
    max_tries=5
)
def maybe_none():
    # ... may return None, which we treat as failure
    return None if random.random() < 0.7 else "OK"
```

### 3. 异步支持

`back-on` 可以透明地配合 `asyncio` 使用：

```python
import asyncio
import backon

@backon.on_exception(
    wait_gen=full_jitter,
    exception=TimeoutError,
    max_tries=3
)
async def flaky_async():
    # ... an async operation that sometimes times out
    await asyncio.sleep(0.1)
    class TimeoutError(Exception): pass
    raise TimeoutError()

async def main():
    await flaky_async()
```

不需要单独的装饰器；库会自动检测 `async` 函数并在底层使用 `asyncio.sleep`。

### 4. 失败通知

要监控重试，你可以传入 `on_success`、`on_retry` 和 `on_giveup` 回调：

```python
import logging
import backon

logging.basicConfig(level=logging.INFO)

@backon.on_exception(
    wait_gen=backon.expo,
    max_tries=5,
    on_retry=lambda exc, wait, tries: logging.warning(
        "Attempt %d failed with %s. Retrying in %.2f s", tries, exc, wait
    ),
    on_giveup=lambda exc, tries: logging.error("Giving up after %d", tries)
)
def service_call():
    # ...
    pass
```

`on_retry` 接收异常实例、等待时间（秒）和尝试次数。`on_giveup` 在达到最大重试次数时被调用。

### 5. 自定义等待生成器

你可以通过传入生成器来提供自己的退避序列，该生成器以秒为单位产生延迟：

```python
def custom_delays():
    for d in [0.1, 0.2, 0.5, 1.0, 2.0]:
        yield d
```

然后通过将 `wait_gen=custom_delays` 与内置的 `backoff.on_exception` 搭配使用。注意，生成器必须是无限的，因为装饰器会按需请求值。

## 使用示例

### 带指数退避的 HTTP 客户端

```python
import requests
import backon

@backon.on_exception(
    backoff.expo,
    requests.exceptions.ConnectionError,
    max_tries=5,
    base=1,      # Start at 1 second
    factor=2.0   # Double each retry
)
def download(url: str) -> bytes:
    r = requests.get(url, timeout=3)
    r.raise_for_status()
    return r.content
```

### 数据库连接

```python
import sqlite3
import backon

@backon.on_exception(
    wait_gen=backon.expo,
    exception=sqlite3.OperationalError,
    max_time=30
)
def get_connection(path: str) -> sqlite3.Connection:
    con = sqlite3.connect(path)
    # Sometimes "database is locked" occurs
    return con
```

如果省略 `exception`，`sleep_on` 会隐式捕获所有异常——请小心使用并配合异常处理。

## 高级：异步生成器支持（Python 3.8+）

`back-on` 也适用于异步生成器函数：

```python
import backon
import asyncio

@backon.on_exception(
    backon.expo,
    RuntimeError,
    max_tries=5
)
async def async_gen():
    for i in range(10):
        yield i
```

生成器将在每次 `__anext__` 调用中应用重试逻辑；如果迭代器抛出异常，则恢复生成器。当生成器可能在流中途失败时，这非常有用。

## 与类型提示的集成

不需要特殊的类型提示；异常名称中的拼写错误会在运行时被捕获。该库是完全类型化的，因此你的编辑器可以提供建议。

## 与 `backoff` 的对比

| 特性 | `backoff`（原始） | `back-on` |
|------------------------------------------------|:--------------------:|:---------------------------:|
| 装饰器语法 | 需要 `@backoff.on_exception` | 相同，但提供可链式调用的方法 |
| `on_success` 钩子 | ❌ | ✅ |
| 异步支持 | ✅ 但有单独的装饰器 | ✅ 统一装饰器 |
| 灵活的等待表 | ✅ | ✅ 它仍然保留全部功能 |
| 类型提示 | 部分 | 全面 |
| 项目活跃度 | 维护中 | 积极开发 |

## 结论

`back-on` 是 `backoff` 的即插即用替代品，在保持简洁性的同时增加了现代人体工程学特性。如果你正在寻找一种可靠的方式，让你的 Python 脚本对瞬时调用失败更具弹性，不妨试试 `back-on`。

```bash
pip install backon
```

祝你编写弹性代码愉快！