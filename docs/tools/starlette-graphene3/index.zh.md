---
title: Starlette-Graphene3：强大的GraphQL API框架
description: 一个推荐用于处理GraphQL的库，设计上最接近FastAPI的设计，专注于类型注解。
created: 2026-07-01
tags:
  - Starlette
  - Graphene3
  - GraphQL
  - Python
  - Web开发
status: 草稿
---

# Starlette-Graphene3：强大的GraphQL API框架

Starlette-Graphene3 是一个项目，将 Starlette 和 Graphene3 整合在一起，以便为构建 GraphQL API 创建一个简洁高效的开发环境。该集成提供了无缝体验，结合了两个库的最佳功能，为 Web 开发提供了一个简单且强大的框架。

## Starlette-Graphene3是什么？

Starlette-Graphene3 是 Starlette 和 Graphene3 的结合体，这两个是用于构建 Web 应用的流行 Python 框架/库。Starlette 是一个基于 ASGI（异步服务器网关接口）的轻量级高性能 Python Web 框架，而 Graphene3 是一个用于定义和消费 GraphQL API 的 Python GraphQL 库。两者结合提供了强大的工具集，特别适用于需要 GraphQL API 的稳健 Web 应用程序。

## 关键特性

1. **Starlette**：提供了一个用于构建 API 和应用的稳健且简约的框架。它基于 ASGI，并且兼容同步和异步代码。
2. **Graphene3**：允许在 Python 应用中定义和消费 GraphQL API。它支持同步和异步查询和变更。

## 历史

- **Starlette**：于2018年发布，由Daniel Sher创建，是一个基于ASGI的轻量级高性能 Python Web 框架。
- **Graphene3**：最初是 Graphene 项目的一部分，Graphene3 于2019年作为独立库正式发布。它旨在为 Python 提供更灵活和强大的 GraphQL 实现。

## 使用场景

- **API 开发**：构建稳健、可扩展和高性能的API。
- **GraphQL API**：为数据获取和变更创建 GraphQL 端点。
- **Web 应用程序**：开发具有GraphQL后端的完整Web应用程序。
- **微服务**：创建暴露 GraphQL API 进行通信的微服务。

## 安装

要安装 Starlette-Graphene3，可以使用 pip：

```bash
pip install starlette graphene3
```

## 基本用法

1. **定义 GraphQL 架构**：在架构中定义类型和查询。

```python
# schema.py
import graphene
from graphene.relay import Node

class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return 'Hello world!'

schema = graphene.Schema(query=Query)
```

2. **与 Starlette 整合**：设置一个 Starlette 应用程序并添加 Graphene3 整合。

```python
# app.py
from starlette.applications import Starlette
from starlette.graphql import GraphQLApp
from schema import schema

app = Starlette()
app.add_route('/graphql', GraphQLApp(schema=schema))
```

3. **运行应用程序**：运行 Starlette 应用程序以启动服务器。

```bash
uvicorn app:app --reload
```

4. **查询 API**：使用 GraphQL 客户端（例如 GraphiQL 或 GraphQL Playground）与 API 交互。

## 示例

这里是一个更完整的示例：

```python
# schema.py
import graphene
from graphene.relay import Node

class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return 'Hello world!'

schema = graphene.Schema(query=Query)

# app.py
from starlette.applications import Starlette
from starlette.graphql import GraphQLApp
from starlette.routing import Route, Mount
from schema import schema

app = Starlette(
    routes=[
        Route('/graphql', GraphQLApp(schema=schema)),
    ],
    on_startup=[lambda: print("Application started!")]
)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
```

### 运行应用程序

要运行应用程序，请执行以下命令：

```bash
uvicorn app:app --reload
```

这将在 `http://0.0.0.0:8000/` 启动应用程序。

## 结论

Starlette-Graphene3 为构建 GraphQL API 和 Web 应用程序提供了稳健且灵活的解决方案。通过利用 Starlette 和 Graphene3 的优势，开发人员可以创建高性能、可扩展的应用程序。无论是构建微服务还是完整的 Web 应用程序，这种组合都提供了强大的开发框架。