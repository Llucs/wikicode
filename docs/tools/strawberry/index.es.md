---
title: Strawberry GraphQL - Una biblioteca GraphQL en Python con enfoque code-first
description: Strawberry es una biblioteca moderna de GraphQL para Python con enfoque code-first que aprovecha las sugerencias de tipo para construir APIs seguras y escalables.
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

**Strawberry** es una biblioteca Python con enfoque code-first para construir APIs GraphQL. Utiliza las sugerencias de tipo de Python para definir el esquema, lo que lo hace intuitivo y seguro en cuanto a tipos. Con soporte nativo para `async`, integraciones profundas con frameworks populares y un rico ecosistema de extensiones, Strawberry es la opción moderna para servicios GraphQL de nivel de producción.

## ¿Por qué Strawberry?

- **Enfoque code-first** — Tu esquema se genera a partir de clases de Python, eliminando la necesidad de archivos separados de Schema Definition Language (SDL).
- **Seguridad de tipos** — Integración completa con verificadores de tipos estáticos (mypy, pyright) que detectan errores temprano.
- **Nativo asíncrono** — Soporte incorporado para resolutores asíncronos, dataloaders y suscripciones.
- **Integraciones con frameworks** — Conéctalo con Django, FastAPI, Flask, Starlette, Sanic o cualquier aplicación ASGI/WSGI.
- **Comunidad activa y extensiones** — Soporte oficial para federación, consultas persistentes, carga de archivos y más.

## Instalación

Instala el paquete principal:

```bash
pip install "strawberry-graphql"
```

Añade extras para integraciones con frameworks:

```bash
pip install "strawberry-graphql[django]"
pip install "strawberry-graphql[fastapi]"
pip install "strawberry-graphql[flask]"
pip install "strawberry-graphql[starlette]"
pip install "strawberry-graphql[all]"  # all integrations
```

## Inicio rápido

Define un esquema simple con una consulta:

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

Ejecuta el esquema con un servidor ASGI (por ejemplo, Uvicorn):

```python
from strawberry.asgi import GraphQL

app = GraphQL(schema)
```

```bash
uvicorn myapp:app
```

Abre `http://localhost:8000` en tu navegador o usa GraphiQL en `/graphql`.

## Características principales

### Definición del esquema code-first

Define tipos, inputs y escalares de GraphQL usando clases de Python y sugerencias de tipo. No se necesita Schema Definition Language (SDL).

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

### Resolutores asíncronos y síncronos

Los resolutores pueden ser síncronos o asíncronos; Strawberry maneja ambos de forma transparente.

```python
@strawberry.type
class Query:
    @strawberry.field
    async def async_info(self) -> str:
        await asyncio.sleep(1)
        return "Resolved asynchronously"
```

### Suscripciones

Datos en tiempo real con generadores asíncronos.

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

### Integración con frameworks

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

### Extensiones

Extiende el esquema con validación, consultas persistentes o lógica personalizada.

```python
class LoggingExtension(strawberry.extensions.SchemaExtension):
    def on_operation(self):
        print(f"Operation: {self.execution_context.operation_name}")
        yield
```

Registra las extensiones al crear el esquema:

```python
schema = strawberry.Schema(query=Query, extensions=[LoggingExtension])
```

### DataLoaders

Agrupación eficiente y caché para consultas a la base de datos.

```python
from strawberry.dataloader import DataLoader

async def load_users(keys: list[int]) -> list[User]:
    return [await db.get_user_by_id(key) for key in keys]

loader = DataLoader(load_users)

async def resolve_user(self, id: int) -> User:
    return await loader.load(id)
```

### Federación

Construye una puerta de enlace GraphQL federada.

```python
@strawberry.federation.type(keys=["id"])
class FederatedBook:
    id: strawberry.ID
    title: str

schema = strawberry.federation.Schema(query=Query, enable_federation_2=True)
```

## Uso avanzado

### Escalares personalizados

```python
import uuid
import strawberry

@strawberry.scalar(name="UUID", serialize=lambda v: str(v), parse_value=lambda v: uuid.UUID(v))
class UUIDScalar:
    pass
```

### Directivas

```python
@strawberry.directive(name="skip", locations=[GraphQLDirective.Location.FIELD])
def skip(value, if_: bool):
    if if_:
        return None
    return value
```

### Carga de archivos

Usando el escalar `Upload`:

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

## ¿Por qué Strawberry sobre las alternativas?

| Característica | Strawberry | Graphene | Ariadne |
|----------------|------------|----------|---------|
| Code-first | ✅ | ❌ (SDK-first) | ❌ (SDL-first) |
| Compatible con verificadores de tipos | ✅ | ❌ | ❌ |
| Nativo asíncrono | ✅ | ❌ | ✅ |
| Soporte para Federation 2 | ✅ | ❌ | ❌ |
| Suscripciones | ✅ | ✅ | ✅ |
| Desarrollo activo | ✅ | Desactualizado | ✅ |

## Conclusión

Strawberry GraphQL trae el poder de GraphQL a Python de una manera idiomática y segura en cuanto a tipos. Ya sea que estés construyendo una API pública, un microservicio o una puerta de enlace federada, la filosofía code-first de Strawberry reduce el código repetitivo y mejora la experiencia del desarrollador. Su ecosistema robusto y su diseño moderno lo convierten en una de las mejores opciones para Python GraphQL en 2026.

## Recursos adicionales

- [Documentación oficial](https://strawberry.rocks/)
- [Repositorio de GitHub](https://github.com/strawberry-graphql/strawberry)
- [Paquete en PyPI](https://pypi.org/project/strawberry-graphql/)
- [Únete al Discord](https://discord.gg/strawberry-graphql)