---
title: "backon: Python-Wiederholungsbibliothek"
description: "backon ist eine moderne Python-Bibliothek zum automatischen Wiederholen fehlgeschlagener Operationen mit konfigurierbaren Backoff-Strategien, abgeleitet von Backoff."
created: 2026-08-07
tags:
  - python
  - retry
  - backoff
  - resilience
status: draft
---

# back-on

`back-on` (pip: `backon`) ist eine Python-Bibliothek, die das Hinzufügen von Wiederholungslogik zu Ihrem Code vereinfacht. Es ist ein Fork der bekannten [`backoff`](https://github.com/litaceans/backoff)-Bibliothek, neu entwickelt mit einer ausdrucksstärkeren, verkettenbaren API und Unterstützung für modernes Python (3.8+). Mit `back-on` können Sie problemlos vorübergehende Fehler bei Netzwerkaufrufen, Datenbankoperationen, Datei-E/A oder jeder fehleranfälligen Funktion behandeln – mit einer sauberen Decorator- oder Kontextmanager-Syntax.

## Warum back-on verwenden?

- **Ergonomie** – Keine expliziten Schleifen oder Konditionsprüfungen nötig; ein Decorator injiziert Wiederholungsverhalten mit minimalem Umfang.
- **Konfigurierbare Strategien** – Feste Verzögerungen, exponentielles Wachstum, voll– oder dekorrelierter Jitter zur Vermeidung von Thundering Herds.
- **Async-Support** – Native Integration mit `asyncio` ermöglicht Wiederholungen in asynchronem Code ohne Blockieren des Event-Loops.
- **Benachrichtigungs-Hooks** – Protokollieren oder Metriken bei jedem Wiederholungsversuch und beim Aufgeben ausgeben.
- **Zero Dependencies** – Funktioniert ohne zusätzliche externe Pakete.

## Installation

Installieren Sie per pip:

```bash
pip install backon
```

Je nach Projektstil können Sie es auch zu einer `pyproject.toml` oder `requirements.txt` hinzufügen.

## Grundlegende Verwendung

Der Kern von `back-on` ist der `@backon.on_exception`-Decorator. Er fängt bestimmte Ausnahmen ab, wartet die berechnete Verzögerung und wiederholt den dekorierten Funktionsaufruf, bis Erfolg oder die maximale Wiederholungszeit erreicht ist.

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

Im obigen Beispiel wird die Funktion bis zu 8 Mal aufgerufen, wobei die Verzögerung zwischen Versuchen nach exponentieller Backoff berechnet wird (Start bei 0.1 s und Verdoppelung). Gesamtzeit über alle Versuche wird 30 Sekunden nicht überschreiten.

## Schlüsselfunktionen

### 1. Mehrere Backoff-Strategien

`back-on` bietet eine Suite integrierter Backoff-Generatoren:

| Strategie            | Beschreibung                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `expo`              | Exponentieller Backoff: `base * 2^n`, wobei `n` die Anzahl der Wiederholungen ist. |
| `fib`               | Fibonacci-basierte Verzögerungen (Verzögerung wächst um die Summe der beiden vorherigen). |
| `full_jitter`       | Zufällige Verzögerung zwischen 0 und dem aktuellen exponentiellen Backoff-Wert. |
| `equal_jitter`      | Teilt den Backoff-Wert in einen zufälligen und einen festen Bestandteil. |
| `constant`          | Feste Verzögerung zwischen Wiederholungen. |
| `decorrelated_jitter` | Jitter mit verminderter Konkurrenz, ohne vollständige Zufälligkeit. |

Verwenden Sie die Konstanten `'expo'`, `'fib'` usw. beim Import:

```python
from backon import expo, fib, full_jitter
```

### 2. Wiederholung bei Erfolg oder Ausnahme

Standardmäßig wiederholt `on_exception`, wenn die Funktion eine passende Ausnahme **auslöst**. Sie können auch wiederholen, wenn die Funktion einen speziellen Wert oder ein Objekt zurückgibt, mit `on_predicate`:

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

### 3. Async-Support

`back-on` funktioniert transparent mit `asyncio`:

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
    await asyncio.console.warn("...")
    class TimeoutError(Exception): pass
    raise TimeoutError()

async def main():
    await flaky_async()
```

Es sind keine separaten Dekoratoren nötig; die Bibliothek erkennt `async`-Funktionen und verwendet intern `asyncio.sleep`.

### 4. Benachrichtigung bei Fehlern

Zur Überwachung von Wiederholungen können Sie Callbacks `on_success`, `on_retry` und `on_giveup` übergeben:

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

`on_retry` erhält die Ausnahme-Instanz, die Wartezeit (in Sekunden) und die Anzahl der Versuche. `on_giveup` wird aufgerufen, wenn die maximale Wiederholungsanzahl erreicht.

### 5. Benutzerdefinierte Wait-Generatoren

Sie können eine eigene Backoff-Sequenz liefern, indem Sie einen Generator übergeben, der Verzögerungen in Sekunden ausgibt:

```python
def custom_delays():
    for d in [0.1, 0.2, 0.5, 1.0, 2.0]:
        yield d
```

Dann verwenden Sie ihn mit `backoff.on_exception`, indem Sie `wait_gen=custom_delays` setzen. Beachten Sie, dass der Generator unendlich sein muss, da der Decorator bei Bedarf Werte anfordert.

## Anwendungsbeispiele

### HTTP-Client mit exponentiellem Backoff

```python
import requests
import backon

@backon.on_exception(
    backoff.expo,
    requests.exceptions.ConnectionError,
    max_tries=5,
    base=1,      # Start bei 1 Sekunde
    factor=2.0   # Verdopplung bei jedem Versuch
)
def download(url: str) -> bytes:
    r = requests.get(url, timeout=3)
    r.raise_for_status()
    return r.content
```

### Datenbankverbindung

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

`sleep_on` fängt implizit alle Ausnahmen, wenn `exception` weggelassen wird – verwenden Sie dies sorgfältig mit entsprechendem Exception-Handling.

## Fortgeschritten: Asynchroner Generator-Support (Python 3.8+)

`back-on` funktioniert auch mit asynchronen Generator-Funktionen:

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

Der Generator wird mit Wiederholungslogik für jeden `__anext__`-Aufruf iteriert; wenn der Iterator auslöst, wird der Generator wieder fortgesetzt. Das ist nützlich, wenn ein Generator mitten im Stream fehlschlagen könnte.

## Integration mit Typ-Hints

Es sind keine speziellen Typ-Hints erforderlich; Tippfehler bei Ausnahmen werden zur Laufzeit erkannt. Die Bibliothek ist vollständig type-hinted, sodass Ihr Editor Vorschläge anbieten kann.

## Vergleich mit `backoff`

| Feature | `backoff` (Original) | `back-on` |
|------------------------------------------------|:--------------------:|:---------------------------:|
| Decorator-Syntax | Braucht `@backoff.on_exception` | Gleich, aber verkettbare Methoden möglich |
| `on_success`-Hook | ❌ | ✅ |
| Async-Unterstützung | ✅ aber separater Decorator | ✅ einheitlicher Decorator |
| Flexible Wait-Tabelle | ✅ | ✅ | 
| Typ-Hints | Teilweise | Umfassend |
| Projektaktivität | Wartung | Aktiv weiterentwickelt |

## Fazit

`back-on` ist ein Drop-in-Ersatz für `backoff`, der moderne Ergonomie hinzufügt und dabei einfach bleibt. Wenn Sie eine zuverlässige Möglichkeit suchen, Ihre Python-Skripte gegen vorübergehende Ruftfälle widerstandsfähig zu machen, probieren Sie `back-on` aus.

```bash
pip install backon
```

Viel glück beim resilienten Programmieren!