---
title: Strawberry GraphQL - Une bibliothèque Python GraphQL code-first
description: Strawberry est une bibliothèque Python GraphQL moderne et code-first qui exploite les annotations de type pour construire des API type-safe et évolutives.
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

**Strawberry** est une bibliothèque Python code-first pour construire des API GraphQL. Elle utilise les type hints Python pour définir le schéma, le rendant intuitif et type-safe. Avec le support natif d'`async`, des intégrations poussées avec les frameworks populaires et un riche écosystème d'extensions, Strawberry est le choix moderne pour les services GraphQL de production.

## Pourquoi Strawberry ?

- **Approche code-first** — Votre schéma est généré à partir de classes Python, éliminant le besoin de fichiers SDL séparés.
- **Type-safety** — Intégration complète avec les vérificateurs de type statiques (mypy, pyright) pour détecter les erreurs rapidement.
- **Async-native** — Support intégré pour les résolveurs asynchrones, dataloaders et subscriptions.
- **Intégrations avec les frameworks** — Intégration avec Django, FastAPI, Flask, Starlette, Sanic, ou toute application ASGI/WSGI.
- **Communauté active et extensions** — Support officiel pour la fédération, les requêtes persistées, les téléchargements de fichiers, et plus encore.

## Installation

Installez le paquet principal :

```bash
pip install "strawberry-graphql"
```

Ajoutez des extras pour les intégrations de frameworks :

```bash
pip install "strawberry-graphql[django]"
pip install "strawberry-graphql[fastapi]"
pip install "strawberry-graphql[flask]"
pip install "strawberry-graphql[starlette]"
pip install "strawberry-graphql[sanic]"
pip install "strawberry-graphql[all]"  # all integrations
```

## Démarrage rapide

Définissez un schéma simple avec une requête :

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

Exécutez le schéma avec un serveur ASGI (par exemple, Uvicorn) :

```python
from strawberry.asgi import GraphQL

app = GraphQL(schema)
```

```bash
uvicorn myapp:app
```

Ouvrez `http://localhost:8000` dans votre navigateur ou utilisez GraphiQL à `/graphql`.

## Fonctionnalités clés

### Définition de schéma code-first

Définissez des types, entrées et scalaires GraphQL à l'aide de classes Python et d'annotations de type. Aucun langage de définition de schéma (SDL) nécessaire.

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

### Résolveurs asynchrones et synchrones

Les résolveurs peuvent être synchrones ou asynchrones ; Strawberry gère les deux de manière transparente.

```python
@strawberry.type
class Query:
    @strawberry.field
    async def async_info(self) -> str:
        await asyncio.sleep(1)
        return "Resolved asynchronously"
```

### Subscriptions

Données en temps réel avec des générateurs asynchrones.

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

### Intégration avec les frameworks

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

Étendez le schéma avec de la validation, des requêtes persistées ou une logique personnalisée.

```python
class LoggingExtension(strawberry.extensions.SchemaExtension):
    def on_operation(self):
        print(f"Operation: {self.execution_context.operation_name}")
        yield
```

Enregistrez les extensions lors de la création du schéma :

```python
schema = strawberry.Schema(query=Query, extensions=[LoggingExtension])
```

### DataLoaders

Traitement par lots et mise en cache efficaces pour les requêtes de base de données.

```python
from strawberry.dataloader import DataLoader

async def load_users(keys: list[int]) -> list[User]:
    return [await db.get_user_by_id(key) for key in keys]

loader = DataLoader(load_users)

async def resolve_user(self, id: int) -> User:
    return await loader.load(id)
```

### Federation

Construisez une passerelle GraphQL fédérée.

```python
@strawberry.federation.type(keys=["id"])
class FederatedBook:
    id: strawberry.ID
    title: str

schema = strawberry.federation.Schema(query=Query, enable_federation_2=True)
```

## Utilisation avancée

### Scalaires personnalisés

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

### Téléchargements de fichiers

En utilisant le scalaire `Upload` :

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

## Pourquoi Strawberry par rapport aux alternatives ?

| Fonctionnalité | Strawberry | Graphene | Ariadne |
|---------|------------|----------|---------|
| Code-first | ✅ | ❌ (SDK-first) | ❌ (SDL-first) |
| Type-checker friendly | ✅ | ❌ | ❌ |
| Async native | ✅ | ❌ | ✅ |
| Federation 2 support | ✅ | ❌ | ❌ |
| Subscriptions | ✅ | ✅ | ✅ |
| Active development | ✅ | Stale | ✅ |

## Conclusion

Strawberry GraphQL apporte la puissance de GraphQL à Python de manière idiomatique et type-safe. Que vous construisiez une API publique, un microservice ou une passerelle fédérée, la philosophie code-first de Strawberry réduit le code redondant et améliore l'expérience développeur. Son écosystème robuste et sa conception moderne en font l'un des meilleurs choix pour Python GraphQL en 2026.

## Ressources supplémentaires

- [Documentation officielle](https://strawberry.rocks/)
- [Dépôt GitHub](https://github.com/strawberry-graphql/strawberry)
- [Paquet PyPI](https://pypi.org/project/strawberry-graphql/)
- [Rejoignez le Discord](https://discord.gg/strawberry-graphql)