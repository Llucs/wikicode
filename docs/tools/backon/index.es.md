---
title: "backon: Biblioteca de Reintentos para Python"
description: "backon es una biblioteca moderna de Python para reintentar automáticamente operaciones fallidas usando estrategias de backoff configurables, bifurcada de Backoff."
created: 2026-08-07
tags:
  - python
  - retry
  - backoff
  - resilience
status: draft
---

# back-on

`back-on` (pip: `backon`) es una biblioteca de Python que simplifica añadir lógica de reintentos a tu código. Es una bifurcación de la conocida biblioteca [`backoff`](https://github.com/litaceans/backoff), rediseñada con una API más expresiva y encadenable, y soporte para Python moderno (3.8+). Con `back-on`, puedes manejar fácilmente fallos transitorios en llamadas de red, operaciones de bases de datos, E/S de archivos o cualquier función inestable, usando una sintaxis limpia de decorador o administrador de contexto.

## ¿Por qué usar back-on?

- **Ergonomía** – No hay necesidad de escribir bucles explícitos ni comprobaciones condicionales; un solo decorador inyecta comportamiento de reintento con el mínimo código.
- **Estrategias configurables** – Retrasos fijos, crecimiento exponencial, jitter completo o descorrelacionado para evitar tormentas de peticiones.
- **Soporte async** – Integración nativa con `asyncio`, lo que permite reintentos en código asíncrono sin bloquear el bucle de eventos.
- **Ganchos de notificación** – Registra o emite métricas en cada intento de reintento y cuando se cede.
- **Cero dependencias** – Funciona de fábrica; no se requieren paquetes externos.

## Instalación

Instala vía pip:

```bash
pip install backon
```

Dependiendo de tu estilo de gestión de proyectos, también puedes añadirlo a un `pyproject.toml` o `requirements.txt`.

## Uso básico

El núcleo de `back-on` es el decorador `@backon.on_exception`. Captura las excepciones especificadas, espera el retraso calculado y reintenta la función decorada hasta que tenga éxito o se alcance el tiempo máximo de reintento.

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

En el ejemplo anterior, la función se llamará hasta 8 veces, con el retraso entre intentos calculado mediante backoff exponencial (comenzando en 0,1 s y duplicándose cada vez). El tiempo total empleado en todos los intentos no superará los 30 segundos.

## Características Clave

### 1. Múltiples Estrategias de Backoff

`back-on` provee un conjunto de generadores de backoff integrados:

| Estrategia            | Descripción                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `expo`                | Backoff exponencial: `base * 2^n`, donde `n` es el número de reintento.      |
| `fib`                 | Retrasos basados en Fibonacci (crece según la suma de los dos anteriores).   |
| `full_jitter`         | Retraso aleatorio entre 0 y el valor de backoff exponencial actual.          |
| `equal_jitter`        | Divide el valor de backoff entre un componente aleatorio y uno fijo.         |
| `constant`            | Retraso fijo entre reintentos.                                               |
| `decorrelated_jitter` | Backoff con jitter que reduce la contención sin completa aleatoriedad.       |

Usa las constantes `'expo'`, `'fib'`, etc. al importar:

```python
from backon import expo, fib, full_jitter
```

### 2. Reintentar por Éxito o Excepción

Por defecto, `on_exception` reintenta cuando la función **lanza** una excepción que coincide. También puedes reintentar cuando la función retorna un valor u objeto especial, usando `on_predicate`:

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

### 3. Soporte Async

`back-on` funciona de manera transparente con `asyncio`:

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

No se necesitan decoradores separados; la biblioteca reacciona ante funciones `async` y usa `asyncio.sleep` por debajo.

### 4. Notificación en Fallos

Para monitorear reintentos, puedes pasar callbacks `on_success`, `on_retry` y `on_giveup`:

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

`on_retry` recibe la instancia de excepción, el tiempo de espera (en segundos) y el número de intentos. `on_giveup` se llama cuando se alcanza el número máximo de reintentos.

### 5. Generadores de Espera Personalizados

Puedes proporcionar tu propia secuencia de backoff pasando un generador que ceda los retrasos en segundos:

```python
def custom_delays():
    for d in [0.1, 0.2, 0.5, 1.0, 2.0]:
        yield d
```

Luego, úsalo con el decorador `backon.on_exception` asignando `wait_gen=custom_delays`. Ten en cuenta que el generador debe ser infinito, ya que el decorador solicitará valores según los necesite.

## Ejemplos de Uso

### Cliente HTTP con Backoff Exponencial

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

### Conexión a Base de Datos

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

`sleep_on` captura implícitamente todas las excepciones si se omite `exception` – úsalo con cuidado en el manejo de excepciones.

## Avanzado: Soport para Generadores Asíncronos (Python 3.8+)

`back-on` también funciona en funciones generadoras asíncronas:

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

El generador será iterado con lógica de reintento aplicada a cada llamada `__anext__`; si el iterador eleva una excepción, el generador se reanuda. Esto es útil cuando un generador puede fallar a mitad de la generación.

## Integración con Type Hints

No se requieren anotaciones de tipo especiales; los errores en los nombres de excepciones se atrapan en tiempo de ejecución. La biblioteca está completamente tipada, por lo que tu editor puede ofrecer sugerencias.

## Comparación con `backoff`

| Característica | `backoff` (original) | `back-on` |
|------------------------------------------------|:--------------------:|:---------------------------:|
| Sintaxis de decorador | Necesita `@backoff.on_exception` | Igual, pero métodos encadenables disponibles |
| Hook `on_success` | ❌ | ✅ |
| Soporte Async | ✅ pero decorador separado | ✅ decorador unificado |
| Tabla de esperas flexible | ✅ | ✅ aún las tiene todas |
| Type hints | Parciales | Completas |
| Actividad del proyecto | Mantenimiento | Desarrollo activo |

## Conclusión

`back-on` es un reemplazo directo para `backoff`` que añade ergonomía moderna manteniendo su simplicidad. Si buscas una forma fiable de hacer tus scripts de Python resilientes a fallos transitorios en las llamadas, prueba `back-on`.

```bash
pip install backon
```

¡Feliz codificación resiliente!