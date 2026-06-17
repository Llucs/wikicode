---
title: FastAPI
description: Um framework web moderno e rápido para construir APIs com Python, baseado nas type hints padrão do Python.
created: 2026-06-15
tags:
  - analysis
  - python
  - api
  - web-framework
  - framework-study
status: draft
---

## Visão Geral

FastAPI é um framework web moderno e de alto desempenho para construir APIs com Python 3.7+. Criado por Sebastián Ramírez (tiangolo), ele utiliza as type hints padrão do Python para lidar automaticamente com validação de requisições, serialização e documentação da API. Construído sobre Starlette (ASGI) e Pydantic, seu desempenho é comparável ao Node.js e Go, tornando-o um dos frameworks Python mais rápidos disponíveis.

## Por que FastAPI?

- **Alto Desempenho**: Extremamente rápido devido ao ASGI e Pydantic.
- **Documentação Automática**: OpenAPI (Swagger UI & ReDoc) gerada diretamente das type annotations.
- **Validação de Dados**: Corpos de requisição, parâmetros de consulta e respostas validados perfeitamente usando Pydantic.
- **Injeção de Dependências**: Sistema de DI integrado para código modular limpo (sessões de banco de dados, autenticação, etc.).
- **Suporte a Async e WebSocket**: Suporte completo para async/await e conexões WebSocket.
- **Segurança**: OAuth2 integrado, tokens JWT, Autenticação Básica HTTP e chaves de API com esquema OpenAPI.
- **Suporte a Editores**: Autocompletar e feedback de erros inline incomparáveis em IDEs modernos.

## Instalação

FastAPI requer um servidor ASGI como Uvicorn. Use `pip` para instalar ambos:

```bash
pip install fastapi
pip install "uvicorn[standard]"
```

Os extras `[standard]` incluem otimizações de desempenho. Alternativamente, instale tudo com um comando:

```bash
pip install "fastapi[standard]"
```

## Início Rápido

Crie um arquivo `main.py`:

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

Execute o servidor com Uvicorn:

```bash
uvicorn main:app --reload
```

Abra [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) no seu navegador para ver a documentação interativa do Swagger gerada automaticamente.

## Principais Funcionalidades

### 1. Documentação Automática

FastAPI gera documentação interativa da API (Swagger UI e ReDoc) automaticamente a partir das suas type annotations. Nenhuma configuração extra é necessária.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

O endpoint `/docs` dá acesso ao Swagger UI; `/redoc` fornece o ReDoc.

### 2. Validação de Dados com Pydantic

Defina modelos de requisição usando classes Python com type hints. FastAPI valida, analisa e serializa dados automaticamente.

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

Dados inválidos retornam um erro 422 com mensagens de validação detalhadas.

### 3. Injeção de Dependências

O sistema de injeção de dependências do FastAPI ajuda a gerenciar lógica compartilhada (por exemplo, conexões de banco de dados, autenticação) de forma limpa.

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

As dependências podem ser reutilizadas e aninhadas, melhorando a modularidade e a testabilidade.

### 4. Suporte a Async e WebSocket

Utilize `async/await` para cenários de alta concorrência, ou use WebSockets para comunicação em tempo real.

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

### 5. Segurança

FastAPI inclui ferramentas para OAuth2, JWT, HTTP Basic e chaves de API — tudo integrado ao esquema OpenAPI.

```python
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
def read_current_user(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

O esquema de segurança aparece automaticamente na documentação gerada, permitindo que os usuários se autentiquem através do Swagger UI.

---

FastAPI representa uma mudança de paradigma no desenvolvimento web em Python. Ao centralizar o framework em torno das type hints padrão do Python, ele reduz drasticamente o boilerplate, elimina a desconexão entre código e documentação e proporciona uma experiência de desenvolvimento excepcionalmente suave. Esteja você construindo microsserviços RESTful, endpoints de modelos de ML ou aplicações em tempo real, FastAPI é uma escolha forte e pronta para produção.