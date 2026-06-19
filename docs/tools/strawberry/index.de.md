---
title: Strawberry GraphQL - Eine Code-First Python GraphQL Bibliothek
description: Strawberry ist eine moderne, code-first Python GraphQL Bibliothek, die Type Hints nutzt, um typsichere, skalierbare APIs zu erstellen.
created: 2026-06-19
tags:
  - graphql
  - python
  - api
  - type-safety
  - strawberry
status: draft
---

# Strawberry GraphQL

**Strawberry** ist eine code-first Python Bibliothek zum Erstellen von GraphQL APIs. Sie nutzt Python Type Hints, um das Schema zu definieren, was es intuitiv und typsicher macht. Mit nativer `async`-Unterstützung, tiefen Integrationen in beliebte Frameworks und einem umfangreichen Ökosystem von Erweiterungen ist Strawberry die moderne Wahl für GraphQL-Dienste auf Produktionsniveau.

## Warum Strawberry?

- **Code-first Ansatz** — Ihr Schema wird aus Python-Klassen generiert, sodass keine separaten Schema Definition Language (SDL) Dateien benötigt werden.
- **Typsicherheit** — Vollständige Integration mit statischen Typprüfern (mypy, pyright) fängt Fehler frühzeitig ab.
- **Async-nativ** — Eingebaute Unterstützung für asynchrone Resolver, DataLoader und Subscriptions.
- **Framework-Integrationen** — Einbindung in Django, FastAPI, Flask, Starlette, Sanic oder jede ASGI/WSGI-Anwendung.
- **Aktive Community & Erweiterungen** — Offizielle Unterstützung für Federation, persisted queries, Datei-Uploads und mehr.

## Installation

Installieren Sie das Kernpaket:

```bash
pip install "strawberry-graphql"
```

Erweiterungen für Framework-Integrationen hinzufügen:

```bash
pip install "strawberry-graphql[django]"
pip install "strawberry-graphql[fastapi]"
pip install "strawberry-graphql[flask]"
pip install "strawberry-graphql[starlette]"
pip install "strawberry-graphql[all]"  # all integrations
```

## Schnellstart

Definieren Sie ein einfaches Schema mit einer Query:

```python
import strawberry

@strawberry.type
class Book:
    title: str
    author: str

@strawberry.type
class Query:
    @strawberry.field
    def books(self) -> list[Book]:
        return [
            Book(title="The Great Gatsby", author="F. Scott Fitzgerald"),
            Book(title="1984", author="George Orwell"),
        ]

schema = strawberry.Schema(query=Query)
```

Führen Sie das Schema mit einem ASGI-Server aus (z.B. Uvicorn):

```python
from strawberry.asgi import GraphQL

app = GraphQL(schema)
```

```bash
uvicorn myapp:app
```

Öffnen Sie `http://localhost:8000` in Ihrem Browser oder verwenden Sie GraphiQL unter `/graphql`.

## Hauptmerkmale

### Code-First Schema Definition

Definieren Sie GraphQL-Typen, Inputs und Skalare mit Python-Klassen und Type Hints. Keine Schema Definition Language (SDL) erforderlich.

```python
@strawberry.input
class BookInput:
    title: str
    author: str

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, book: BookInput) -> Book:
        # store logic
        return Book(title=book.title, author=book.author)
```

### Async & Sync Resolver

Resolver können entweder synchron oder asynchron sein; Strawberry behandelt beide transparent.

```python
@strawberry.type
class Query:
    @strawberry.field
    async def async_info(self) -> str:
        await asyncio.sleep(1)
        return "Resolved asynchronously"
```

### Subscriptions

Echtzeitdaten mit asynchronen Generatoren.

```python
import asyncio
@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, target: int = 5) -> int:
        for i in range(target):
            yield i
            await asyncio.sleep(0.5)
```

### Framework-Integration

#### FastAPI

```python
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

app = FastAPI()
schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
```

#### Django

```python
# urls.py
from django.urls import path
from strawberry.django.views import GraphQLView

urlpatterns = [
    path("graphql", GraphQLView.as_view(schema=schema)),
]
```

### Erweiterungen

Erweitern Sie das Schema mit Validierung, persisted queries oder benutzerdefinierter Logik.

```python
class LoggingExtension(strawberry.extensions.SchemaExtension):
    def on_operation(self):
        print(f"Operation: {self.execution_context.operation_name}")
        yield
```

Erweiterungen beim Erstellen des Schemas registrieren:

```python
schema = strawberry.Schema(query=Query, extensions=[LoggingExtension])
```

### DataLoader

Effizientes Batching und Caching für Datenbankabfragen.

```python
from strawberry.dataloader import DataLoader

async def load_users(keys: list[int]) -> list[User]:
    return [await db.get_user_by_id(key) for key in keys]

loader = DataLoader(load_users)

async def resolve_user(self, id: int) -> User:
    return await loader.load(id)
```

### Federation

Erstellen Sie ein föderiertes GraphQL-Gateway.

```python
@strawberry.federation.type(keys=["id"])
class FederatedBook:
    id: strawberry.ID
    title: str

schema = strawberry.federation.Schema(query=Query, enable_federation_2=True)
```

## Fortgeschrittene Nutzung

### Benutzerdefinierte Skalare

```python
import uuid
import strawberry

@strawberry.scalar(name="UUID", serialize=lambda v: str(v), parse_value=lambda v: uuid.UUID(v))
class UUIDScalar:
    pass
```

### Direktiven

```python
@strawberry.directive(name="skip", locations=[GraphQLDirective.Location.FIELD])
def skip(value, if_: bool):
    if if_:
        return None
    return value
```

### Datei-Uploads

Verwendung des `Upload`-Skalars:

```python
from strawberry.file_uploads import Upload

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def upload_file(self, file: Upload) -> bool:
        content = await file.read()
        # process content
        return True
```

## Warum Strawberry gegenüber Alternativen?

| Merkmal | Strawberry | Graphene | Ariadne |
|---------|------------|----------|---------|
| Code-first | ✅ | ❌ (SDK-first) | ❌ (SDL-first) |
| Type-checker friendly | ✅ | ❌ | ❌ |
| Async native | ✅ | ❌ | ✅ |
| Federation 2 support | ✅ | ❌ | ❌ |
| Subscriptions | ✅ | ✅ | ✅ |
| Aktive Entwicklung | ✅ | Veraltet | ✅ |

## Fazit

Strawberry GraphQL bringt die Leistungsfähigkeit von GraphQL auf idiomatische, typsichere Weise nach Python. Ob Sie eine öffentliche API, einen Microservice oder ein föderiertes Gateway entwickeln, Strawberrys Code-First-Philosophie reduziert Boilerplate und verbessert die Entwicklererfahrung. Sein robustes Ökosystem und modernes Design machen es zu einer der besten Wahlmöglichkeiten für Python GraphQL im Jahr 2026.

## Zusätzliche Ressourcen

- [Offizielle Dokumentation](https://strawberry.rocks/)
- [GitHub-Repository](https://github.com/strawberry-graphql/strawberry)
- [PyPI-Paket](https://pypi.org/project/strawberry-graphql/)
- [Discord beitreten](https://discord.gg/strawberry-graphql)