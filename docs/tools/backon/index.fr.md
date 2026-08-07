---
title: "backon : bibliothèque de nouvelles tentatives pour Python"
description: "backon est une bibliothèque Python moderne permettant de relancer automatiquement des opérations échouées à l'aide de stratégies de backoff configurables, dérivée de Backoff."
created: 2026-08-07
tags:
  - python
  - retry
  - backoff
  - resilience
status: draft
---

# back-on

`back-on` (pip : `backon`) est une bibliothèque Python qui simplifie l'ajout de logique de nouvelle tentative à votre code. C'est un fork de la célèbre bibliothèque [`backoff`](https://github.com/litaceans/backoff), repensée avec une API plus expressive et chaînable, ainsi qu'une prise en charge du Python moderne (3.8+). Avec `back-on`, vous pouvez facilement gérer les échecs transitoires dans les appels réseau, les opérations de base de données, les entrées/sorties de fichiers, ou toute fonction instable, grâce à une syntaxe propre de décorateur ou de gestionnaire de contexte.

## Pourquoi utiliser back-on ?

- **Ergonomie** – Pas besoin d'écrire des boucles explicites ou de vérifier des conditions ; un seul décorateur injecte le comportement de nouvelle tentative avec un code minimal.
- **Stratégies configurables** – Délais fixes, croissance exponentielle, gigue complète ou décorrélée pour éviter l'effet de troupeau.
- **Support asynchrone** – Intégration native avec `asyncio`, permettant de nouvelles tentatives dans du code asynchrone sans bloquer la boucle d'événements.
- **Capteurs de notification** – Journalisez ou émettez des métriques à chaque tentative et lors de l'abandon.
- **Zéro dépendance** – Fonctionne dès l'installation ; aucun paquet externe requis.

## Installation

Installez via pip :

```bash
pip install backon
```

Selon votre mode de gestion de projet, vous pouvez également l'ajouter à un `pyproject.toml` ou un `requirements.txt`.

## Utilisation de base

Le cœur de `back-on` est le décorateur `@backon.on_exception`. Il capture les exceptions spécifiées, attend le délai calculé, puis relance la fonction décorée jusqu'à ce qu'elle réussisse ou que le temps maximal de tentatives soit atteint.

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

Dans l'exemple ci-dessus, la fonction sera appelée jusqu'à 8 fois, l'intervalle entre chaque tentative étant calculé à l'aide d'un backoff exponentiel (départ à 0,1 s puis doublé à chaque fois). La durée totale cumulée de toutes les tentatives ne dépassera pas 30 secondes.

## Fonctionnalités principales

### 1. Plusieurs stratégies de backoff

`back-on` offre une suite de générateurs de backoff intégrés :

| Stratégie            | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `expo`               | Backoff exponentiel : `base * 2^n`, où `n` est le numéro de tentative.     |
| `fib`                | Délais basés sur la suite de Fibonacci (le délai croît selon la somme des deux précédents). |
| `full_jitter`        | Délai aléatoire entre 0 et la valeur de backoff exponentiel actuelle.      |
| `equal_jitter`       | Divise le backoff entre une composante aléatoire et une composante fixe.   |
| `constant`           | Délai fixe entre les tentatives.                                            |
| `decorrelated_jitter`| Backoff avec gigue décorrélée, réduisant la contention sans aléa total.    |

Utilisez les constantes `'expo'`, `'fib'`, etc. lors de l'import :

```python
from backon import expo, fib, full_jitter
```

### 2. Nouvelle tentative après succès ou exception

Par défaut, `on_exception` réessaie lorsque la fonction **lève** une exception correspondante. Vous pouvez également retenter lorsque la fonction renvoie une valeur ou un objet particulier, en utilisant `on_predicate` :

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

### 3. Support asynchrone

`back-on` fonctionne de manière transparente avec `asyncio` :

```python
import asyncio
import backon

@backon.on_exception(
    wait_gen=full_jitter,
    exception=TimeoutError,
    max_tries=3
)
async def flaky_async():
    # ... a async operation that sometimes times out
    await asyncio.sleep(0.1)
    class TimeoutError(Exception): pass
    raise TimeoutError()

async def main():
    await flaky_async()
```

Pas besoin de décorateurs séparés ; la bibliothèque détecte les fonctions `async` et utilise `asyncio.sleep` sous le capot.

### 4. Notification en cas d'échec

Pour superviser les tentatives, vous pouvez passer des callbacks `on_success`, `on_retry` et `on_giveup` :

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
    on_giveup=lambda exc, tries: logging.error("Eternally failed after %d tries", tries)
)
def service_call():
    # ...
    pass
```

`on_retry` reçoit l'instance de l'exception, le temps d'attente (en secondes) et le nombre de tentatives. `on_giveup` est appelé lorsque le nombre maximal de tentatives est atteint.

### 5. Générateurs de délais personnalisés

Vous pouvez fournir votre propre séquence de backoff en passant un générateur qui produit des intervalles en secondes :

```python
def custom_delays():
    for d in [0.1, 0.2, 0.5, 1.0, 2.0]:
        yield d
```

Utilisez-le ensuite avec le décorateur `backoff.on_exception` (via le paramètre `wait_gen=custom_delays`). Attention : le générateur doit être infini, car le décorateur réclamera des valeurs à la demande.

## Exemples d'utilisation

### Client HTTP avec backoff exponentiel

```python
import requests
import backon

@backon.on_exception(
    backoff.expo,
    requests.exceptions.ConnectionError,
    max_tries=5,
    base=1      # Start at 1 second
    factor=2.0  # Double each attempt
)
def download(url: str) -> bytes:
    r = requests.get(url, timeout=3)
    r.raise_for_status()
    return r.content
```

### Connexion à une base de données

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

`sleep_on` capture implicitement toutes les exceptions si le paramètre `exception` est omis – mais utilisez-le avec une gestion d'exceptions rigoureuse.

## Avancé : support des générateurs asynchrones (Python 3.8+)

`back-on` fonctionne également sur des fonctions génératrices asynchrones :

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

Le générateur sera itéré avec une logique de nouvelle tentative appliquée à chaque appel `__anext__` ; si l'itérateur lève une exception, le générateur est repris sur un nouvel essai. Cela est utile quand un générateur peut échouer en cours de route.

## Intégration avec les indications de type

Aucune indication de type spéciale n'est nécessaire ; les fautes de frappe dans les noms d'exceptions sont détectées à l'exécution. La bibliothèque est entièrement typée, ce qui permet à votre éditeur d'offrir des suggestions.

## Comparaison avec `backoff`

| Fonctionnalité               | `backoff` (original)   | `back-on`                 |
|------------------------------|:----------------------:|:-------------------------:|
| Syntaxe de décorateur        | `@backoff.on_exception`| Modulable, chaînable      |
| Callback `on_success`        | ❌                      | ✅                        |
| Support asynchrone           | ✅ (décorateur séparé) | ✅ (décorateur unifié)    |
| Table de délais flexible (backoff) | ✅                  | ✅                        |
| Indications de type          | Partielles             | Compañines                |
| Activité du projet           | Maintenance            | Développement actif       |

## Conclusion

`back-on` est un remplacement direct de `backoff` qui ajoute une ergonomie moderne tout en conservant sa simplicité. Si vous cherchez un moyen fiable de rendre vos scripts Python résilients face aux échecs de communication transitoires, essayez `back-on`.

```bash
pip install backon
```

Bon développement résilient !