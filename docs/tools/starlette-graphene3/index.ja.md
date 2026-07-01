---
title: Starlette-Graphene3: GraphQL APIs の強力なフレームワーク
description: GraphQL に取り組む際に推奨されるライブラリで、FastAPI のデザインに最も近いもので、型注釈に重点を置いている。
created: 2026-07-01
tags:
  - Starlette
  - Graphene3
  - GraphQL
  - Python
  - ウェブ開発
status: 草稿
---

# Starlette-Graphene3: GraphQL APIs の強力なフレームワーク

Starlette-Graphene3 は、Starlette と Graphene3 の統合により、GraphQL APIs の構築に最適な streamlined 開発環境を提供するプロジェクトです。統合により、両ライブラリの最高機能を組み合わせた単純ながら強力なウェブ開発フレームワークが提供されます。

## Starlette-Graphene3 とは何か？

Starlette-Graphene3 は、Starlette と Graphene3 の組み合わせです。これらは Python でウェブアプリケーションを構築するために人気のあるフレームワーク/ライブラリです。Starlette は Python 用の軽量で高性能なウェブフレームワークで、Graphene3 は Python でGraphQL APIs を定義および消費できるライブラリです。これらは強力かつ柔軟なツールセットを提供し、特にGraphQL APIs を必要とするアプリケーションに特に適しています。

## キー フEATURES

1. **Starlette**: APIs およびアプリケーションの構築にrobust で minimalistic なフレームワークを提供します。これは ASGI（Asynchronous Server Gateway Interface）に基づいており、同期と非同期コードに両方対応しています。
2. **Graphene3**: Python アプリケーションで GraphQL APIs の定義と消費を可能にします。同期と非同期クエリとミューテーションの両方をサポートしています。

## 歴史

- **Starlette**: 2018 年にリリースされた Starlette は、Daniel Sher によって作成され、Python 用の軽量で高性能なウェブフレームワークです。
- **Graphene3**: Graphene の一部として最初に提供された Graphene3 は、2019 年に独立したライブラリとして正式にリリースされました。Python 用のより柔軟で強力なGraphQL 実装を提供するために作成されました。

## 使用例

- **API 開発**: 堅固でスケーラブルでパフォーマンスの高いAPI を構築します。
- **GraphQL APIs**: データの取得とミューテーション用の GraphQL 端末点を作成します。
- **ウェブアプリケーション**: GraphQL バックエンドを持つ完全なウェブアプリケーションを開発します。
- **マイクロサービス**: GraphQL APIs を通信のために公開するマイクロサービスを作成します。

## インストール

Starlette-Graphene3 をインストールするには、pip を使用します:

```bash
pip install starlette graphene3
```

## 基本的な使用法

1. **GraphQL スキーマ定義**: スキーマ内でタイプとクエリを定義します。

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

2. **Starlette と統合**: Starlette アプリケーションをセットアップし、Graphene3 の統合を行います。

```python
# app.py
from starlette.applications import Starlette
from starlette.graphql import GraphQLApp
from schema import schema

app = Starlette()
app.add_route('/graphql', GraphQLApp(schema=schema))
```

3. **アプリケーションの実行**: Starlette アプリケーションを起動するためのサーバーを開始します。

```bash
uvicorn app:app --reload
```

4. **API とのクエリ**: GraphQL クライアント（例：GraphiQL または GraphQL Playground）を使用して API と相互作用します。

## 例

以下は、より完全な例です：

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

### アプリケーションの実行

アプリケーションを実行するには、以下のコマンドを実行します:

```bash
uvicorn app:app --reload
```

これにより、アプリケーションは `http://0.0.0.0:8000/` で起動します。

## 結論

Starlette-Graphene3 は、GraphQL APIs とウェブアプリケーションの構築に robust で柔軟なソリューションを提供します。Starlette と Graphene3 の長所を組み合わせることにより、開発者は高性能でスケーラブルなアプリケーションを作成できます。マイクロサービスや完全なウェブアプリケーションのいずれかに取り組んでいる場合、この組み合わせは開発のための強力なフレームワークを提供します。