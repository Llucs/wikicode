---
title: FastAPI
description: Pythonの標準型ヒントに基づく、API構築のためのモダンで高速なWebフレームワーク。
created: 2026-06-15
tags:
  - analysis
  - python
  - api
  - web-framework
  - framework-study
status: draft
---

## 概要

FastAPIは、Python 3.7+でAPIを構築するためのモダンで高性能なWebフレームワークです。Sebastián Ramírez（tiangolo）によって作成され、Pythonの標準型ヒントを活用して、リクエストの検証、シリアル化、APIドキュメントを自動的に処理します。Starlette（ASGI）とPydanticを基盤としており、そのパフォーマンスはNode.jsやGoと同等で、利用可能な最も高速なPythonフレームワークの一つです。

## FastAPIが選ばれる理由

- **高性能**: ASGIとPydanticによる驚異的な高速性。
- **自動ドキュメント生成**: 型アノテーションから直接生成されるOpenAPI（Swagger UI & ReDoc）。
- **データ検証**: Pydanticを使用したリクエストボディ、クエリパラメータ、レスポンスのシームレスな検証。
- **依存性注入**: クリーンでモジュール化されたコードのためのビルトインDIシステム（データベースセッション、認証など）。
- **非同期＆WebSocketサポート**: async/awaitとWebSocket接続の完全サポート。
- **セキュリティ**: OAuth2、JWTトークン、HTTP基本認証、APIキーの統合とOpenAPIスキーマ対応。
- **エディタサポート**: 最新のIDEでの比類のない自動補完とインラインエラーフィードバック。

## インストール

FastAPIはUvicornなどのASGIサーバーが必要です。`pip`を使用して両方をインストールします：

```bash
pip install fastapi
pip install "uvicorn[standard]"
```

`[standard]` エクストラにはパフォーマンス最適化が含まれています。または、次の1つのコマンドですべてをインストールできます：

```bash
pip install "fastapi[standard]"
```

## クイックスタート

`main.py`ファイルを作成します：

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}
```

Uvicornでサーバーを実行：

```bash
uvicorn main:app --reload
```

ブラウザで[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)を開くと、自動生成されたインタラクティブなSwaggerドキュメントが表示されます。

## 主要機能

### 1. 自動ドキュメント生成

FastAPIは、型アノテーションからインタラクティブなAPIドキュメント（Swagger UIとReDoc）を自動生成します。追加の設定は不要です。

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

`/docs`エンドポイントでSwagger UIにアクセスでき、`/redoc`でReDocが利用できます。

### 2. Pydanticによるデータ検証

型ヒント付きのPythonクラスを使用してリクエストモデルを定義します。FastAPIはデータの検証、解析、シリアル化を自動的に行います。

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    full_name: str = None

@app.post("/users/")
def create_user(user: User):
    return user
```

無効なデータには、詳細な検証メッセージとともに422エラーが返されます。

### 3. 依存性注入

FastAPIの依存性注入システムは、共有ロジック（例：データベース接続、認証）をクリーンに管理するのに役立ちます。

```python
from fastapi import Depends, FastAPI

app = FastAPI()

def get_db():
    db = SomeDatabaseConnection()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
def read_items(db: SomeType = Depends(get_db)):
    return db.query_all()
```

依存関係は再利用およびネストが可能で、モジュール性とテスト容易性が向上します。

### 4. 非同期＆WebSocketサポート

高同時実行シナリオには`async/await`を活用し、リアルタイム通信にはWebSocketを使用します。

```python
@app.get("/async-items/")
async def read_async_items():
    data = await fetch_data()
    return data

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo: {data}")
```

### 5. セキュリティ

FastAPIには、OAuth2、JWT、HTTP基本認証、APIキーのツールが含まれており、すべてOpenAPIスキーマに統合されています。

```python
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
def read_current_user(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

セキュリティスキーマは生成されたドキュメントに自動的に表示され、ユーザーはSwagger UIを介して認証できます。

---

FastAPIはPythonのWeb開発におけるパラダイムシフトを象徴しています。フレームワークを標準Python型ヒント中心に据えることで、定型コードを大幅に削減し、コードとドキュメントの乖離をなくし、非常にスムーズな開発者体験を提供します。RESTfulマイクロサービス、MLモデルエンドポイント、リアルタイムアプリケーションのいずれを構築する場合でも、FastAPIは強力で本番環境に適した選択肢です。