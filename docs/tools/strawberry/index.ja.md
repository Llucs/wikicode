---
title: Strawberry GraphQL - コードファーストなPython GraphQLライブラリ
description: Strawberryは、型ヒントを活用して型安全でスケーラブルなAPIを構築する、モダンでコードファーストなPython GraphQLライブラリです。
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

**Strawberry**は、GraphQL APIを構築するためのコードファーストなPythonライブラリです。Pythonの型ヒントを使用してスキーマを定義するため、直感的で型安全です。ネイティブの`async`サポート、人気フレームワークとの深い統合、豊富な拡張エコシステムを備え、Strawberryは本番環境向けGraphQLサービスのモダンな選択肢です。

## なぜStrawberryなのか？

- **コードファーストアプローチ** — スキーマはPythonクラスから生成されるため、別途スキーマ定義言語（SDL）ファイルが不要です。
- **型安全性** — 静的型チェッカー（mypy、pyright）との完全な統合により、早期にエラーを発見します。
- **非同期ネイティブ** — 非同期リゾルバ、データローダー、サブスクリプションに対する組み込みサポート。
- **フレームワーク統合** — Django、FastAPI、Flask、Starlette、Sanic、または任意のASGI/WSGIアプリケーションにプラグイン可能。
- **活発なコミュニティと拡張機能** — フェデレーション、永続化クエリ、ファイルアップロードなどの公式サポート。

## インストール

コアパッケージをインストール：

```bash
pip install "strawberry-graphql"
```

フレームワーク統合用のエクストラを追加：

```bash
pip install "strawberry-graphql[django]"
pip install "strawberry-graphql[fastapi]"
pip install "strawberry-graphql[flask]"
pip install "strawberry-graphql[starlette]"
pip install "strawberry-graphql[all]"  # すべての統合
```

## クイックスタート

シンプルなクエリスキーマを定義：

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

ASGIサーバー（例：Uvicorn）でスキーマを実行：

```python
from strawberry.asgi import GraphQL

app = GraphQL(schema)
```

```bash
uvicorn myapp:app
```

ブラウザで `http://localhost:8000` を開くか、`/graphql` でGraphiQLを使用します。

## 主な機能

### コードファーストなスキーマ定義

Pythonクラスと型ヒントを使用してGraphQLタイプ、入力、スカラーを定義します。スキーマ定義言語（SDL）は不要です。

```python
@strawberry.input
class BookInput:
    title: str
    author: str

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, book: BookInput) -> Book:
        # 保存処理
        return Book(title=book.title, author=book.author)
```

### 非同期・同期リゾルバ

リゾルバは同期または非同期のどちらでも可能で、Strawberryが透過的に処理します。

```python
@strawberry.type
class Query:
    @strawberry.field
    async def async_info(self) -> str:
        await asyncio.sleep(1)
        return "非同期で解決"
```

### サブスクリプション

非同期ジェネレータによるリアルタイムデータ。

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

### フレームワーク統合

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

### 拡張機能

バリデーション、永続化クエリ、カスタムロジックでスキーマを拡張します。

```python
class LoggingExtension(strawberry.extensions.SchemaExtension):
    def on_operation(self):
        print(f"Operation: {self.execution_context.operation_name}")
        yield
```

スキーマ作成時に拡張機能を登録：

```python
schema = strawberry.Schema(query=Query, extensions=[LoggingExtension])
```

### データローダー

データベースクエリの効率的なバッチ処理とキャッシング。

```python
from strawberry.dataloader import DataLoader

async def load_users(keys: list[int]) -> list[User]:
    return [await db.get_user_by_id(key) for key in keys]

loader = DataLoader(load_users)

async def resolve_user(self, id: int) -> User:
    return await loader.load(id)
```

### フェデレーション

フェデレーションGraphQLゲートウェイを構築します。

```python
@strawberry.federation.type(keys=["id"])
class FederatedBook:
    id: strawberry.ID
    title: str

schema = strawberry.federation.Schema(query=Query, enable_federation_2=True)
```

## 高度な使い方

### カスタムスカラー

```python
import uuid
import strawberry

@strawberry.scalar(name="UUID", serialize=lambda v: str(v), parse_value=lambda v: uuid.UUID(v))
class UUIDScalar:
    pass
```

### ディレクティブ

```python
@strawberry.directive(name="skip", locations=[GraphQLDirective.Location.FIELD])
def skip(value, if_: bool):
    if if_:
        return None
    return value
```

### ファイルアップロード

`Upload`スカラーを使用：

```python
from strawberry.file_uploads import Upload

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def upload_file(self, file: Upload) -> bool:
        content = await file.read()
        # コンテンツを処理
        return True
```

## なぜStrawberryが代替案より優れているのか？

| 機能 | Strawberry | Graphene | Ariadne |
|------|------------|----------|---------|
| コードファースト | ✅ | ❌ | ❌ |
| 型チェッカー対応 | ✅ | ❌ | ❌ |
| 非同期ネイティブ | ✅ | ❌ | ✅ |
| Federation 2 サポート | ✅ | ❌ | ❌ |
| サブスクリプション | ✅ | ✅ | ✅ |
| 活発な開発 | ✅ | 停滞中 | ✅ |

## 結論

Strawberry GraphQLは、GraphQLの力をPythonに慣用的かつ型安全な方法で提供します。公開API、マイクロサービス、フェデレーションゲートウェイのいずれを構築する場合でも、Strawberryのコードファーストの哲学によりボイラープレートが削減され、開発者体験が向上します。その堅牢なエコシステムとモダンなデザインにより、Strawberryは2026年のPython GraphQLのトップチョイスの1つです。

## 参考資料

- [公式ドキュメント](https://strawberry.rocks/)
- [GitHub リポジトリ](https://github.com/strawberry-graphql/strawberry)
- [PyPI パッケージ](https://pypi.org/project/strawberry-graphql/)
- [Discord に参加](https://discord.gg/strawberry-graphql)