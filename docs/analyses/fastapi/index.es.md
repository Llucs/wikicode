---
title: FastAPI
description: Un framework web moderno y rápido para construir APIs con Python, basado en las anotaciones de tipo estándar de Python.
created: 2026-06-15
tags:
  - analysis
  - python
  - api
  - web-framework
  - framework-study
status: draft
---

## Resumen

FastAPI es un framework web moderno y de alto rendimiento para construir APIs con Python 3.7+. Creado por Sebastián Ramírez (tiangolo), aprovecha las anotaciones de tipo estándar de Python para manejar automáticamente la validación de solicitudes, serialización y documentación de APIs. Construido sobre Starlette (ASGI) y Pydantic, su rendimiento es comparable al de Node.js y Go, lo que lo convierte en uno de los frameworks Python más rápidos disponibles.

## ¿Por qué FastAPI?

- **Alto Rendimiento**: Muy rápido gracias a ASGI y Pydantic.
- **Documentación Automática**: OpenAPI (Swagger UI y ReDoc) generada directamente desde las anotaciones de tipo.
- **Validación de Datos**: Cuerpos de solicitud, parámetros de consulta y respuestas validados sin problemas usando Pydantic.
- **Inyección de Dependencias**: Sistema de DI incorporado para código modular limpio (sesiones de base de datos, autenticación, etc.).
- **Soporte Asíncrono y WebSocket**: Soporte completo para async/await y conexiones WebSocket.
- **Seguridad**: OAuth2 integrado, tokens JWT, HTTP Basic Auth y API keys con esquema OpenAPI.
- **Soporte de Editor**: Autocompletado inigualable y retroalimentación de errores en línea en IDEs modernos.

## Instalación

FastAPI requiere un servidor ASGI como Uvicorn. Usa `pip` para instalar ambos:

```bash
pip install fastapi
pip install "uvicorn[standard]"
```

Los extras `[standard]` incluyen optimizaciones de rendimiento. Alternativamente, instala todo con un solo comando:

```bash
pip install "fastapi[standard]"
```

## Inicio Rápido

Crea un archivo `main.py`:

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

Ejecuta el servidor con Uvicorn:

```bash
uvicorn main:app --reload
```

Abre [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) en tu navegador para ver la documentación interactiva de Swagger generada automáticamente.

## Características Clave

### 1. Documentación Automática

FastAPI genera documentación interactiva de la API (Swagger UI y ReDoc) automáticamente a partir de tus anotaciones de tipo. No se requiere configuración adicional.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

El endpoint `/docs` da acceso a Swagger UI; `/redoc` proporciona ReDoc.

### 2. Validación de Datos con Pydantic

Define modelos de solicitud usando clases de Python con anotaciones de tipo. FastAPI valida, analiza y serializa datos automáticamente.

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

Los datos no válidos devuelven un error 422 con mensajes de validación detallados.

### 3. Inyección de Dependencias

El sistema de inyección de dependencias de FastAPI ayuda a gestionar la lógica compartida (por ejemplo, conexiones a bases de datos, autenticación) de manera limpia.

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

Las dependencias se pueden reutilizar y anidar, mejorando la modularidad y la facilidad de prueba.

### 4. Soporte Asíncrono y WebSocket

Aprovecha `async/await` para escenarios de alta concurrencia, o usa WebSockets para comunicación en tiempo real.

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

### 5. Seguridad

FastAPI incluye herramientas para OAuth2, JWT, HTTP Basic y API keys, todo integrado en el esquema OpenAPI.

```python
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
def read_current_user(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

El esquema de seguridad aparece automáticamente en la documentación generada, permitiendo a los usuarios autenticarse a través de la interfaz de Swagger UI.

---

FastAPI representa un cambio de paradigma en el desarrollo web con Python. Al centrar el framework en las anotaciones de tipo estándar de Python, reduce drásticamente el código repetitivo, elimina la desconexión entre el código y la documentación, y proporciona una experiencia de desarrollo excepcionalmente fluida. Ya sea que estés construyendo microservicios RESTful, endpoints de modelos de ML o aplicaciones en tiempo real, FastAPI es una opción sólida y lista para producción.