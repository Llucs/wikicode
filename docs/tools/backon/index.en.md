---
title: "backon: Python Retry Library"
description: "backon is a modern Python library for automatically retrying failing operations using configurable backoff strategies, forked from Backoff."
created: 2026-08-07
tags:
  - python
  - retry
  - backoff
  - resilience
status: draft
---

# back-on

`back-on` (pip: `backon`) is a Python library that simplifies adding retry logic to your code. It is a fork of the well-known [`backoff`](https://github.com/litaceans/backoff) library, re‑engineered with a more expressive, chainable API and support for modern Python (3.8+). With `back-on`, you can easily handle transient failures in network calls, database operations, file I/O, or any flaky function, using a clean decorator or context‑manager syntax.

## Why Use back-on?

- **Ergonomics** – No need to write explicit loops or condition checks; one decorator injects retry behaviour with minimal code.
- **Configurable strategies** – Fixed delays, exponential growth, full or decorrelated jitter to avoid thundering herds.
- **Async support** – Native integration with `asyncio`, allowing retries in asynchronous code without blocking the event loop.
- **Notification hooks** – Log or emit metrics on each retry attempt and when giving up.
- **Zero dependencies** – Works out of the box; no external packages required.

## Installation

Install via pip:

```bash
pip install backon
```

Depending on your project management style, you can also add it to a `pyproject.toml` or `requirements.txt`.

## Basic Usage

The core of `back-on` is the `@backon.on_exception` decorator. It catches specified exceptions, waits for the calculated delay, and retries the decorated function until it succeeds or the maximum retry time is reached.

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

In the above example, the function will be called up to 8 times, with the delay between attempts calculated using exponential backoff (starting at 0.1 s and doubling each time). The total time spent across all attempts will not exceed 30 seconds.

## Key Features

### 1. Multiple Backoff Strategies

`back-on` provides a suite of built‑in backoff generators:

| Strategy            | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `expo`              | Exponential backoff: `base * 2^n`, where `n` is the retry number.          |
| `fib`               | Fibonacci‑based delays (delay grows by the sum of the previous two).       |
| `full_jitter`       | Random delay between 0 and the current exponential backoff value.          |
| `equal_jitter`      | Splits the backoff value between a random component and a fixed component. |
| `constant`          | Fixed delay between retries.                                                |
| `decorrelated_jitter` | Jitterised backoff that reduces contention without full randomness.       |

Use the `'expo'`, `'fib'`, etc. constants when importing:

```python
from backon import expo, fib, full_jitter
```

### 2. Retrying on Success or Exception

By default, `on_exception` retries when the function **raises** a matching exception. You can also retry when the function returns a special value or object, using `on_predicate`:

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

### 3. Async Support

`back-on` works transparently with `asyncio`:

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

There is no need for separate decorators; the library detects `async` functions and uses `asyncio.sleep` under the hood.

### 4. Notification on Failure

To monitor retries, you can pass `on_success`, `on_retry`, and `on_giveup` callbacks:

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

`on_retry` receives the exception instance, the wait time (in seconds), and the number of attempts. `on_giveup` is called when the maximum retry count is reached.

### 5. Custom Wait Generators

You can supply your own backoff sequence by passing a generator that yields delays in seconds:

```python
def custom_delays():
    for d in [0.1, 0.2, 0.5, 1.0, 2.0]:
        yield d
```

Then use it with the built‑in `backoff.on_exception` by setting `wait_gen=custom_delays`. Be careful that the generator must be infinite, as the decorator will request values as needed.

## Usage Examples

### HTTP Client with Exponential Backoff

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

### Database Connection

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

`sleep_on` implicitly catches all exceptions if `exception` is omitted – use with careful exception handling.

## Advanced: Asynchronous generator support (Python 3.8+)

`back-on` also works on asynchronous generator functions:

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

The generator will be iterated with retry logic applied to each `__anext__` call; if the iterator raises, the generator is resumed. This is useful when a generator may fail mid‑stream.

## Integration with Type Hints

No special type hints are required; typos in exception names are caught at runtime. The library is fully typed, so your editor can offer suggestions.

## Comparison with `backoff`

| Feature | `backoff` (original) | `back-on` |
|------------------------------------------------|:--------------------:|:---------------------------:|
| Decorator syntax | Needs `@backoff.on_exception` | Same, but chainable methods available |
| `on_success` hook | ❌ | ✅ |
| Async support | ✅ but separate decorator | ✅ unified decorator |
| Flexible wait table | ✅ | ✅ it still has all |
| Type hints | Partial | Comprehensive |
| Project activity | Maintenance | Active development |

## Conclusion

`back-on` is a drop‑in replacement for `backoff` that adds modern ergonomics while keeping its simplicity. If you are looking for a reliable way to make your Python scripts resilient to transient call failures, give `back-on` a try.

```bash
pip install backon
```

Happy resilient coding!