---
title: FastAPI
description: 一个现代的、快速的、基于标准Python类型提示构建API的Web框架。
created: 2026-06-15
tags:
  - analysis
  - python
  - api
  - web-framework
  - framework-study
status: draft
---

## 概述

FastAPI是一个现代的、高性能的Web框架，用于使用Python 3.7+构建API。由Sebastián Ramírez（tiangolo）创建，它利用Python标准类型提示自动处理请求验证、序列化和API文档。它构建在Starlette（ASGI）和Pydantic之上，性能与Node.js和Go相当，使其成为可用的最快Python框架之一。

## 为什么选择FastAPI？

- **高性能**：由于ASGI和Pydantic而具有极快速度。
- **自动文档**：直接从类型注解生成OpenAPI（Swagger UI和ReDoc）。
- **数据验证**：使用Pydantic无缝验证请求体、查询参数和响应。
- **依赖注入**：内置的依赖注入系统，用于简洁模块化代码（数据库会话、身份验证等）。
- **异步与WebSocket支持**：完全支持async/await和WebSocket连接。
- **安全性**：集成了OAuth2、JWT令牌、HTTP基本认证和API密钥，并与OpenAPI模式集成。
- **编辑器支持**：在现代IDE中提供无与伦比的自动补全和内联错误反馈。

## 安装

FastAPI需要一个ASGI服务器，例如Uvicorn。使用`pip`安装两者：

```bash
pip install fastapi
pip install "uvicorn[standard]"
```

`[standard]`扩展包含性能优化。或者，使用一个命令安装所有依赖：

```bash
pip install "fastapi[standard]"
```

## 快速开始

创建一个文件`main.py`：

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

使用Uvicorn运行服务器：

```bash
uvicorn main:app --reload
```

在浏览器中打开[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)即可看到自动生成的交互式Swagger文档。

## 关键特性

### 1. 自动文档

FastAPI会根据你的类型注解自动生成交互式API文档（Swagger UI和ReDoc）。无需额外配置。

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

`/docs`端点提供Swagger UI访问；`/redoc`提供ReDoc。

### 2. 使用Pydantic进行数据验证

使用带有类型注解的Python类定义请求模型。FastAPI会自动验证、解析和序列化数据。

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

无效数据会返回带有详细验证消息的422错误。

### 3. 依赖注入

FastAPI的依赖注入系统有助于干净地管理共享逻辑（例如数据库连接、身份验证）。

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

依赖项可以重用和嵌套，提高了模块性和可测试性。

### 4. 异步与WebSocket支持

利用`async/await`处理高并发场景，或使用WebSockets进行实时通信。

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

### 5. 安全性

FastAPI包含OAuth2、JWT、HTTP基本认证和API密钥等工具——所有这些都已集成到OpenAPI模式中。

```python
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
def read_current_user(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

安全方案会自动出现在生成的文档中，允许用户通过Swagger UI进行身份验证。

---

FastAPI代表了Python Web开发中的一种范式转变。通过围绕标准Python类型提示构建框架，它大幅减少了样板代码，消除了代码与文档之间的脱节，并提供了极其流畅的开发体验。无论你是在构建RESTful微服务、ML模型端点还是实时应用，FastAPI都是一个可靠的生产就绪选择。