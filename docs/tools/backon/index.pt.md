---
title: "backon: Biblioteca de Retry para Python"
description: "backon é uma biblioteca Python moderna para tentar automaticamente novamente operações com falha usando estratégias de backoff configuráveis, um fork do Backoff."
created: 2026-08-07
tags:
  - python
  - retry
  - backoff
  - resilience
status: draft
---

# back-on

`back-on` (pip: `backon`) é uma biblioteca Python que simplifica a adição de lógica de retry ao seu código. É um fork da conhecida biblioteca [`backoff`](https://github.com/litaceans/backoff), sendo reformulada com uma API mais expressiva e encadeável e suporte para Python moderno (3.8+). Com `back-on`, você pode facilmente lidar com falhas transitórias em chamadas de rede, operações de banco de dados, I/O de arquivos, ou qualquer função instável, usando uma sintaxe limpa de decorator ou gerenciador de contexto.

## Por que usar back-on?

- **Ergonomia** – Não precisa escrever loops explícitos ou verificações de condição; um decorator injeta o comportamento de retry com código mínimo.
- **Estratégias configuráveis** – Atrasos fixos, crescimento exponencial, jitter completo ou descorrelacionado para evitar "thundering herds".
- **Suporte a async** – Integração nativa com `asyncio`, permitindo retries em código assíncrono sem bloquear o event loop.
- **Hooks de notificação** – Registre em log ou emita métricas em cada tentativa de retry e quando desistir.
- **Zero dependências** – Funciona sem nenhum pacote externo adicional.

## Instalação

Instale via pip:

```bash
pip install backon
```

Dependendo do seu estilo de gerenciamento de projeto, você também pode adicioná-lo a um `pyproject.toml` ou `requirements.txt`.

## Uso Básico

O núcleo do `back-on` é o decorator `@backon.on_exception`. Ele captura exceções específicas, espera o atraso calculado e tenta novamente a função decorada até que ela tenha sucesso ou o tempo máximo de retry seja atingido.

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
    """Busca uma URL, tentando novamente em caso de erro de requisição."""
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()
```

No exemplo acima, a função será chamada até 8 vezes, com o atraso entre tentativas calculado usando backoff exponencial (começando em 0,1 s e dobrando a cada vez). O tempo total gasto em todas as tentativas não ultrapassará 30 segundos.

## Principais Recursos

### 1. Múltiplas Estratégias de Backoff

`back-on` fornece um conjunto de geradores de backoff integrados:

| Estratégia | Descrição                                                                 |
|------------|---------------------------------------------------------------------------|
| `expo`     | Backoff exponencial: `base * 2^n`, onde `n` é o número da tentativa.      |
| `fib`      | Atrasos baseados em Fibonacci (o atraso cresce pela soma dos dois anteriores). |
| `full_jitter` | Atraso aleatório entre 0 e o valor atual do backoff exponencial.    |
| `equal_jitter` | Divide o valor de backoff entre um componente aleatório e um fixo. |
| `constant` | Atraso fixo entre tentativas.                                               |
| `decorrelated_jitter` | Backoff com jitter que reduz contenção sem total aleatoriedade. |

Use as constantes `'expo'`, `'fib'`, etc. ao importar:

```python
from backon import expo, fib, full_jitter
```

### **2. Tentativa novamente em Sucesso ou Exceção**

Por padrão, `on_exception` tenta novamente quando a função **lança** uma exceção correspondente. Você também pode tentar novamente quando a função retorna um valor ou objeto especial, usando `on_predicate`:

```python
import backon

@backon.on_predicate(
    wait_gen=expo,
    predicate=lambda x: x is None,
    max_tries=5
)
def maybe_none():
    # ... pode retornar None, que tratamos como falha
    return None if random.random() < 0.7 else "OK"
```

### **3. Suporte a Async**

`back-on` funciona de forma transparente com `asyncio`:

```python
import asyncio
import backon

@backon.on_exception(
    wait_gen=full_jitter,
    exception=TimeoutError,
    max_tries=3
)
async def flaky_async():
    # ... uma operação assíncrona que às vezes excede o tempo
    await asyncio.sleep(0.1)
    class TimeoutError(Exception): pass
    raise TimeoutError()

async def main():
    await flaky_async()
```

Não é necessário decorators separados; a biblioteca detecta funções `async` e usa `asyncio.sleep` internamente.

### **4. Notificação de Falhas**

Para monitorar as tentativas, você pode passar callbacks `on_success`, `on_retry` e `on_giveup`:

```python
import logging
import backon

logging.basicConfig(level=logging.INFO)

@backon.on_exception(
    wait_gen=backon.expo,
    max_tries=5,
    on_retry=lambda exc, wait, tries: logging.warning(
        "Tentativa %d falhou com %s. Tentaremos novamente em %.2f s", tries, exc, wait
    ),
    on_giveup=lambda exc, tries: logging.error("Desistindo após %d tentativas", tries)
)
def service_call():
    # ...
    pass
```

`on_retry` recebe a instância da exceção, o tempo de espera (em segundos) e o número de tentativas. `on_giveup` é chamado quando o número máximo de tentativas é atingido.

### **5. Geradores de Espera Personalizados**

Você pode fornecer sua própria sequência de backoff passando um gerador que retorna delays em segundos:

```python
def custom_delays():
    for d in [0.1, 0.2, 0.5, 1.0, 2.0]:
        yield d
```

Em seguida, use-o com o `backon.on_exception` definindo `wait_gen=custom_delays`. Lembre-se de que o gerador deve ser infinito, pois o decorator solicitará valores conforme necessário.

## Exemplos de Uso

### Cliente HTTP com Backoff Exponencial

```python
import requests
import backon

@backon.on_exception(
    backoff.expo,
    requests.exceptions.ConnectionError,
    max_tries=5,
    base=1,      # Começa em 1 segundo
    factor=2.0   # Dobra a cada tentativa
)
def download(url: str) -> bytes:
    r = requests.get(url, timeout=3)
    r.raise_for_status()
    return r.content
```

### Conexão de Banco de Dados

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
    # Às vezes ocorre "database is locked"
    return con
```

`sleep_on` implicitamente captura todas as exceções se `exception` for omitido – use com cuidado no tratamento de exceções.

## Avançado: Suporte a geradores assíncronos (Python 3.8+)

O `back-on` também funciona em funções geradoras assíncronas:

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

O gerador será iterado com lógica de retry aplicada a cada chamada `__anext__`; se o iterador lançar, o gerador é retomado. Isso é útil quando um gerador pode falhar no meio do processo.

## Integração com Type Hints

Não são necessários type hints especiais; erros de digitação nos nomes de exceção são capturados em tempo de execução. A biblioteca é totalmente tipada, então seu editor pode sugerir correções.

## Comparação com o `backoff`

| Característica | `backoff` (original) | `back-on` |
|------------------------------------------------|:--------------------:|:---------------------------:|
| Sintaxe de decorator | Precisa `@backoff.on_exception` | Igual, mas com métodos encadeáveis disponíveis |
| Hook `on_success` | ❌ | ✅ |
| Suporte a async | ✅ mas com decorator separado | ✅ decorator unificado |
| Tabela de espera flexível | ✅ | ✅ (ainda possui todas) |
| Type hints | Parcial | Abrangente |
| Atividade do projeto | Manutenção | Desenvolvimento ativo |

## Conclusão

Você é só para substituir o `backoff` e adiciona ergonomia moderna mantendo sua simplicidade. Se você está procurando uma forma confiável de tornar seus scripts Python resilientes a falhas transitórias de chamadas, experimente o `back-on`.

```bash
pip install backon
```

Feliz codificação resiliente!