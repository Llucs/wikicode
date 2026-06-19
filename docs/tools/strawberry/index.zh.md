---
title: Strawberry GraphQL - 一个代码优先的 Python GraphQL 库
description: Strawberry 是一个现代的、代码优先的 Python GraphQL 库，利用类型提示构建类型安全、可扩展的 API。
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

**Strawberry** 是一个用于构建 GraphQL API 的代码优先的 Python 库。它使用 Python 类型提示来定义 schema，使其直观且类型安全。凭借原生的 `async` 支持、与流行框架的深度集成以及丰富的扩展生态系统，Strawberry 是构建生产级 GraphQL 服务的现代选择。

## 为什么选择 Strawberry？

- **代码优先的方法** — 你的 schema 由 Python 类生成，无需单独的 Schema Definition Language (SDL) 文件。
- **类型安全** — 与静态类型检查器（mypy, pyright）完全集成，尽早捕获错误。
- **原生异步** — 内置对异步解析器、数据加载器和订阅的支持。
- **框架集成** — 可接入 Django、FastAPI、Flask、Starlette、Sanic 或任何 ASGI/WSGI 应用。
- **活跃的社区和扩展** — 官方支持联邦、持久化查询、文件上传等。

## 安装

安装核心包：

```bash
pip install "strawberry-graphql"
```

添加框架集成的额外包：

```bash
pip install "strawberry-graphql[django]"
pip install "strawberry-graphql[fastapi]"
pip install "strawberry-graphql[flask]"
pip install "strawberry-graphql[starlette]"
pip install "strawberry-graphql[all]"  # all integrations
```

## 快速开始

定义一个带有查询的简单 schema：

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

用 ASGI 服务器（例如 Uvicorn）运行 schema：

```python
from strawberry.asgi import GraphQL

app = GraphQL(schema)
```

```bash
uvicorn myapp:app
```

在浏览器中打开 `http://localhost:8000` 或使用 `/graphql` 的 GraphiQL 界面。

## 主要特性

### 代码优先的 Schema 定义

使用 Python 类和类型提示定义 GraphQL 类型、输入和标量。无需 Schema Definition Language (SDL)。

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

### 异步与同步解析器

解析器可以是同步或异步的；Strawberry 透明地处理两者。

```python
@strawberry.type
class Query:
    @strawberry.field
    async def async_info(self) -> str:
        await asyncio.sleep(1)
        return "Resolved asynchronously"
```

### 订阅

使用异步生成器实现实时数据。

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

### 框架集成

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

### 扩展

通过验证、持久化查询或自定义逻辑扩展 schema。

```python
class LoggingExtension(strawberry.extensions.SchemaExtension):
    def on_operation(self):
        print(f"Operation: {self.execution_context.operation_name}")
        yield
```

注册扩展创建 schema 时：

```python
schema = strawberry.Schema(query=Query, extensions=[LoggingExtension])
```

### 数据加载器

高效的数据库查询批处理和缓存。

```python
from strawberry.dataloader import DataLoader

async def load_users(keys: list[int]) -> list[User]:
    return [await db.get_user_by_id(key) for key in keys]

loader = DataLoader(load_users)

async def resolve_user(self, id: int) -> User:
    return await loader.load(id)
```

### 联邦

构建联邦 GraphQL 网关。

```python
@strawberry.federation.type(keys=["id"])
class FederatedBook:
    id: strawberry.ID
    title: str

schema = strawberry.federation.Schema(query=Query, enable_federation_2=True)
```

## 高级用法

### 自定义标量

```python
import uuid
import strawberry

@strawberry.scalar(name="UUID", serialize=lambda v: str(v), parse_value=lambda v: uuid.UUID(v))
class UUIDScalar:
    pass
```

### 指令

```python
@strawberry.directive(name="skip", locations=[GraphQLDirective.Location.FIELD])
def skip(value, if_: bool):
    if if_:
        return None
    return value
```

### 文件上传

使用 `Upload` 标量：

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

## 为什么选择 Strawberry 而非其他替代方案？

| 特性 | Strawberry | Graphene | Ariadne |
|-----|------------|----------|---------|
| 代码优先 | ✅ | ❌ (SDK-first) | ❌ (SDL-first) |
| 类型检查友好 | ✅ | ❌ | ❌ |
| 原生异步 | ✅ | ❌ | ✅ |
| 联邦2支持 | ✅ | ❌ | ❌ |
| 订阅 | ✅ | ✅ | ✅ |
| 积极开发 | ✅ | 停滞 | ✅ |

## 结论

Strawberry GraphQL 以一种地道的、类型安全的方式将 GraphQL 的强大功能带到 Python 中。无论你是在构建公共 API、微服务还是联邦网关，Strawberry 的代码优先理念都能减少样板代码并改善开发者体验。其强大的生态系统和现代设计使其成为 2026 年 Python GraphQL 的顶级选择之一。

## 其他资源

- [官方文档](https://strawberry.rocks/)
- [GitHub 仓库](https://github.com/strawberry-graphql/strawberry)
- [PyPI 包](https://pypi.org/project/strawberry-graphql/)
- [加入 Discord](https://discord.gg/strawberry-graphql)