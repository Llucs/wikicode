---
title: FastAPI
description: Un framework web moderne et rapide pour construire des API avec Python, basé sur les annotations de type standard de Python.
created: 2026-06-15
tags:
  - analysis
  - python
  - api
  - web-framework
  - framework-study
status: draft
---

## Vue d'ensemble

FastAPI est un framework web moderne et haute performance pour construire des API avec Python 3.7+. Créé par Sebastián Ramírez (tiangolo), il exploite les annotations de type standard de Python pour gérer automatiquement la validation des requêtes, la sérialisation et la documentation des API. Construit sur Starlette (ASGI) et Pydantic, ses performances sont comparables à celles de Node.js et Go, ce qui en fait l'un des frameworks Python les plus rapides disponibles.

## Pourquoi FastAPI ?

- **Haute Performance** : Extrêmement rapide grâce à ASGI et Pydantic.
- **Documentation Automatique** : OpenAPI (Swagger UI & ReDoc) générée directement à partir des annotations de type.
- **Validation des Données** : Corps de requêtes, paramètres de requête et réponses validés de manière transparente avec Pydantic.
- **Injection de Dépendances** : Système DI intégré pour un code modulaire propre (sessions de base de données, authentification, etc.).
- **Support Async & WebSocket** : Prise en charge complète de async/await et des connexions WebSocket.
- **Sécurité** : OAuth2 intégré, jetons JWT, HTTP Basic Auth et clés API avec schéma OpenAPI.
- **Support Éditeur** : Autocomplétion inégalée et retour d'erreur en ligne dans les IDE modernes.

## Installation

FastAPI nécessite un serveur ASGI tel que Uvicorn. Utilisez `pip` pour installer les deux :

```bash
pip install fastapi
pip install "uvicorn[standard]"
```

Les extras `[standard]` incluent des optimisations de performances. Vous pouvez aussi tout installer avec une seule commande :

```bash
pip install "fastapi[standard]"
```

## Démarrage rapide

Créez un fichier `main.py` :

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

Lancez le serveur avec Uvicorn :

```bash
uvicorn main:app --reload
```

Ouvrez [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) dans votre navigateur pour voir la documentation interactive Swagger générée automatiquement.

## Fonctionnalités clés

### 1. Documentation Automatique

FastAPI génère automatiquement une documentation interactive (Swagger UI et ReDoc) à partir de vos annotations de type. Aucune configuration supplémentaire n'est requise.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

Le point de terminaison `/docs` donne accès à Swagger UI ; `/redoc` fournit ReDoc.

### 2. Validation des Données avec Pydantic

Définissez des modèles de requête à l'aide de classes Python avec annotations de type. FastAPI valide, parse et sérialise automatiquement les données.

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

Des données invalides renvoient une erreur 422 avec des messages de validation détaillés.

### 3. Injection de Dépendances

Le système d'injection de dépendances de FastAPI permet de gérer proprement la logique partagée (ex. connexions à la base de données, authentification).

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

Les dépendances peuvent être réutilisées et imbriquées, améliorant la modularité et la testabilité.

### 4. Support Async & WebSocket

Exploitez `async/await` pour des scénarios à haute concurrence, ou utilisez WebSockets pour la communication en temps réel.

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

### 5. Sécurité

FastAPI inclut des outils pour OAuth2, JWT, HTTP Basic et les clés API — tous intégrés dans le schéma OpenAPI.

```python
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
def read_current_user(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

Le schéma de sécurité apparaît automatiquement dans la documentation générée, permettant aux utilisateurs de s'authentifier via l'interface Swagger.

---

FastAPI représente un changement de paradigme dans le développement web Python. En centrant le framework sur les annotations de type standard de Python, il réduit considérablement le code standard, élimine le décalage entre le code et la documentation, et offre une expérience développeur exceptionnellement fluide. Que vous construisiez des microservices RESTful, des endpoints de modèles ML, ou des applications en temps réel, FastAPI est un choix solide et prêt pour la production.