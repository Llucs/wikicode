---
title: Strawberry GraphQL - Uma Biblioteca Python GraphQL Code-First
description: Strawberry é uma biblioteca Python GraphQL moderna e code-first que utiliza type hints para construir APIs seguras e escaláveis.
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

**Strawberry** é uma biblioteca Python code-first para construir APIs GraphQL. Ela utiliza type hints do Python para definir o schema, tornando-o intuitivo e type-safe. Com suporte nativo a `async`, integrações profundas com frameworks populares e um rico ecossistema de extensões, o Strawberry é a escolha moderna para serviços GraphQL de nível de produção.

## Por que Strawberry?

- **Abordagem code-first** — Seu schema é gerado a partir de classes Python, eliminando a necessidade de arquivos separados de Schema Definition Language (SDL).
- **Type-safety** — Integração total com static type checkers (mypy, pyright) detecta erros precocemente.
- **Async nativo** — Suporte integrado para resolvers, dataloaders e subscriptions assíncronos.
- **Integrações com frameworks** — Conecte-se a Django, FastAPI, Flask, Starlette, Sanic ou qualquer aplicação ASGI/WSGI.
- **Comunidade ativa e extensões** — Suporte oficial para federação, consultas persistentes, upload de arquivos e mais.

## Instalação

Instale o pacote principal:

```bash
pip install "strawberry-graphql"
```

Adicione extras para integrações com frameworks:

```bash
pip install "strawberry-graphql[django]"
pip install "strawberry-graphql[fastapi]"
pip install "strawberry-graphql[flask]"
pip install "strawberry-graphql[starlette]"
pip install "strawberry-graphql[sanic]"
pip install "strawberry-graphql[all]"  # todas as integrações
```

## Início Rápido

Defina um schema simples com uma consulta:

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

Execute o schema com um servidor ASGI (ex.: Uvicorn):

```python
from strawberry.asgi import GraphQL

app = GraphQL(schema)
```

```bash
uvicorn myapp:app
```

Abra `http://localhost:8000` no seu navegador ou use GraphiQL em `/graphql`.

## Principais Funcionalidades

### Definição de Schema Code-First

Defina tipos, inputs e scalars GraphQL usando classes Python e type hints. Nenhuma linguagem de definição de schema (SDL) necessária.

```python
@strawberry.input
class BookInput:
    title: str
    author: str

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, book: BookInput) -> Book:
        # lógica de armazenamento
        return Book(title=book.title, author=book.author)
```

### Resolvers Assíncronos e Síncronos

Os resolvers podem ser síncronos ou assíncronos; o Strawberry lida com ambos de forma transparente.

```python
@strawberry.type
class Query:
    @strawberry.field
    async def async_info(self) -> str:
        await asyncio.sleep(1)
        return "Resolvido assincronamente"
```

### Subscriptions

Dados em tempo real com generators assíncronos.

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

### Integração com Frameworks

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

### Extensões

Estenda o schema com validação, consultas persistentes ou lógica personalizada.

```python
class LoggingExtension(strawberry.extensions.SchemaExtension):
    def on_operation(self):
        print(f"Operation: {self.execution_context.operation_name}")
        yield
```

Registre extensões ao criar o schema:

```python
schema = strawberry.Schema(query=Query, extensions=[LoggingExtension])
```

### DataLoaders

Agrupamento e cache eficientes para consultas ao banco de dados.

```python
from strawberry.dataloader import DataLoader

async def load_users(keys: list[int]) -> list[User]:
    return [await db.get_user_by_id(key) for key in keys]

loader = DataLoader(load_users)

async def resolve_user(self, id: int) -> User:
    return await loader.load(id)
```

### Federação

Construa um gateway GraphQL federado.

```python
@strawberry.federation.type(keys=["id"])
class FederatedBook:
    id: strawberry.ID
    title: str

schema = strawberry.federation.Schema(query=Query, enable_federation_2=True)
```

## Uso Avançado

### Scalars Personalizados

```python
import uuid
import strawberry

@strawberry.scalar(name="UUID", serialize=lambda v: str(v), parse_value=lambda v: uuid.UUID(v))
class UUIDScalar:
    pass
```

### Diretivas

```python
@strawberry.directive(name="skip", locations=[GraphQLDirective.Location.FIELD])
def skip(value, if_: bool):
    if if_:
        return None
    return value
```

### Upload de Arquivos

Usando o scalar `Upload`:

```python
from strawberry.file_uploads import Upload

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def upload_file(self, file: Upload) -> bool:
        content = await file.read()
        # processar conteúdo
        return True
```

## Por que Strawberry em vez de Alternativas?

| Recurso | Strawberry | Graphene | Ariadne |
|---------|------------|----------|---------|
| Code-first | ✅ | ❌ (SDK-first) | ❌ (SDL-first) |
| Type-checker friendly | ✅ | ❌ | ❌ |
| Async nativo | ✅ | ❌ | ✅ |
| Suporte a Federation 2 | ✅ | ❌ | ❌ |
| Subscriptions | ✅ | ✅ | ✅ |
| Desenvolvimento ativo | ✅ | Stale | ✅ |

## Conclusão

O Strawberry GraphQL traz o poder do GraphQL para Python de forma idiomática e type-safe. Seja você construindo uma API pública, um microsserviço ou um gateway federado, a filosofia code-first do Strawberry reduz o código repetitivo e melhora a experiência do desenvolvedor. Seu ecossistema robusto e design moderno o tornam uma das principais escolhas para GraphQL em Python em 2026.

## Recursos Adicionais

- [Documentação Oficial](https://strawberry.rocks/)
- [Repositório no GitHub](https://github.com/strawberry-graphql/strawberry)
- [Pacote no PyPI](https://pypi.org/project/strawberry-graphql/)
- [Junte-se ao Discord](https://discord.gg/strawberry-graphql)