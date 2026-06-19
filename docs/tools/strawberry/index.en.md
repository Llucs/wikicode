---
title: Strawberry GraphQL - A Code-First Python GraphQL Library
description: Strawberry is a modern, code-first Python GraphQL library that leverages type hints to build type-safe, scalable APIs.
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

**Strawberry** is a code-first Python library for building GraphQL APIs. It uses Python type hints to define the schema, making it intuitive and type-safe. With native `async` support, deep integrations with popular frameworks, and a rich extension ecosystem, Strawberry is the modern choice for production-grade GraphQL services.

## Why Strawberry?

- **Code-first approach** — Your schema is generated from Python classes, eliminating the need for separate Schema Definition Language (SDL) files.
- **Type-safety** — Full integration with static type checkers (mypy, pyright) catches errors early.
- **Async-native** — Built-in support for asynchronous resolvers, dataloaders, and subscriptions.
- **Framework integrations** — Plug into Django, FastAPI, Flask, Starlette, Sanic, or any ASGI/WSGI application.
- **Active community & extensions** — Official support for federation, persisted queries, file uploads, and more.

## Installation

Install the core package:

```bash
pip install "strawberry-graphql"
```

Add extras for framework integrations:

```bash
pip install "strawberry-graphql[django]"
pip install "strawberry-graphql[fastapi]"
pip install "strawberry-graphql[flask]"
pip install "strawberry-graphql[starlette]"
pip install "strawberry-graphql[all]"  # all integrations
```

## Quick Start

Define a simple schema with a query:

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

Run the schema with an ASGI server (e.g., Uvicorn):

```python
from strawberry.asgi import GraphQL

app = GraphQL(schema)
```

```bash
uvicorn myapp:app
```

Open `http://localhost:8000` in your browser or use GraphiQL at `/graphql`.

## Key Features

### Code-First Schema Definition

Define GraphQL types, inputs, and scalars using Python classes and type hints. No Schema Definition Language (SDL) needed.

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

### Async & Sync Resolvers

Resolvers can be either sync or async; Strawberry handles both transparently.

```python
@strawberry.type
class Query:
    @strawberry.field
    async def async_info(self) -> str:
        await asyncio.sleep(1)
        return "Resolved asynchronously"
```

### Subscriptions

Real-time data with async generators.

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

### Framework Integration

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

### Extensions

Extend the schema with validation, persisted queries, or custom logic.

```python
class LoggingExtension(strawberry.extensions.SchemaExtension):
    def on_operation(self):
        print(f"Operation: {self.execution_context.operation_name}")
        yield
```

Register extensions when creating the schema:

```python
schema = strawberry.Schema(query=Query, extensions=[LoggingExtension])
```

### DataLoaders

Efficient batching and caching for database queries.

```python
from strawberry.dataloader import DataLoader

async def load_users(keys: list[int]) -> list[User]:
    return [await db.get_user_by_id(key) for key in keys]

loader = DataLoader(load_users)

async def resolve_user(self, id: int) -> User:
    return await loader.load(id)
```

### Federation

Build a federated GraphQL gateway.

```python
@strawberry.federation.type(keys=["id"])
class FederatedBook:
    id: strawberry.ID
    title: str

schema = strawberry.federation.Schema(query=Query, enable_federation_2=True)
```

## Advanced Usage

### Custom Scalars

```python
import uuid
import strawberry

@strawberry.scalar(name="UUID", serialize=lambda v: str(v), parse_value=lambda v: uuid.UUID(v))
class UUIDScalar:
    pass
```

### Directives

```python
@strawberry.directive(name="skip", locations=[GraphQLDirective.Location.FIELD])
def skip(value, if_: bool):
    if if_:
        return None
    return value
```

### File Uploads

Using the `Upload` scalar:

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

## Why Strawberry Over Alternatives?

| Feature | Strawberry | Graphene | Ariadne |
|---------|------------|----------|---------|
| Code-first | ✅ | ❌ (SDK-first) | ❌ (SDL-first) |
| Type-checker friendly | ✅ | ❌ | ❌ |
| Async native | ✅ | ❌ | ✅ |
| Federation 2 support | ✅ | ❌ | ❌ |
| Subscriptions | ✅ | ✅ | ✅ |
| Active development | ✅ | Stale | ✅ |

## Conclusion

Strawberry GraphQL brings the power of GraphQL to Python in an idiomatic, type-safe manner. Whether you are building a public API, microservice, or federated gateway, Strawberry’s code-first philosophy reduces boilerplate and improves developer experience. Its robust ecosystem and modern design make it one of the top choices for Python GraphQL in 2026.

## Additional Resources

- [Official Documentation](https://strawberry.rocks/)
- [GitHub Repository](https://github.com/strawberry-graphql/strawberry)
- [PyPI Package](https://pypi.org/project/strawberry-graphql/)
- [Join the Discord](https://discord.gg/strawberry-graphql)