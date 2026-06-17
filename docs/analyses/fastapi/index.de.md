---
title: FastAPI
description: Ein modernes, schnelles Web-Framework zum Erstellen von APIs mit Python, basierend auf standardmäßigen Python Type Hints.
created: 2026-06-15
tags:
  - analysis
  - python
  - api
  - web-framework
  - framework-study
status: draft
---

## Überblick

FastAPI ist ein modernes, leistungsstarkes Web-Framework zum Erstellen von APIs mit Python 3.7+. Entwickelt von Sebastián Ramírez (tiangolo), nutzt es die standardmäßigen Python Type Hints, um automatisch Anfragevalidierung, Serialisierung und API-Dokumentation zu handhaben. Es basiert auf Starlette (ASGI) und Pydantic und ist in der Leistung mit Node.js und Go vergleichbar, was es zu einem der schnellsten verfügbaren Python-Frameworks macht.

## Warum FastAPI?

- **Hohe Leistung**: Blitzschnell dank ASGI und Pydantic.
- **Automatische Dokumentation**: OpenAPI (Swagger UI & ReDoc) wird direkt aus Type Hints generiert.
- **Datenvalidierung**: Anfragekörper, Abfrageparameter und Antworten werden nahtlos mit Pydantic validiert.
- **Abhängigkeitsinjektion**: Integriertes DI-System für sauberen modularen Code (Datenbank-Sitzungen, Authentifizierung usw.).
- **Async & WebSocket-Unterstützung**: Volle Unterstützung für async/await und WebSocket-Verbindungen.
- **Sicherheit**: Integrierte OAuth2-, JWT-Tokens, HTTP-Basic-Auth und API-Schlüssel mit OpenAPI-Schema.
- **Editor-Unterstützung**: Unübertroffene Autovervollständigung und Inline-Fehlerrückmeldung in modernen IDEs.

## Installation

FastAPI benötigt einen ASGI-Server wie Uvicorn. Verwenden Sie `pip`, um beide zu installieren:

```bash
pip install fastapi
pip install "uvicorn[standard]"
```

Die `[standard]` Extras enthalten Leistungsoptimierungen. Alternativ können Sie alles mit einem Befehl installieren:

```bash
pip install "fastapi[standard]"
```

## Schnellstart

Erstellen Sie eine Datei `main.py`:

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

Starten Sie den Server mit Uvicorn:

```bash
uvicorn main:app --reload
```

Öffnen Sie [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in Ihrem Browser, um die automatisch generierte interaktive Swagger-Dokumentation zu sehen.

## Hauptmerkmale

### 1. Automatische Dokumentation

FastAPI generiert automatisch interaktive API-Dokumente (Swagger UI und ReDoc) aus Ihren Type Hints. Es ist keine zusätzliche Konfiguration erforderlich.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

Der Endpunkt `/docs` bietet Zugriff auf Swagger UI; `/redoc` stellt ReDoc bereit.

### 2. Datenvalidierung mit Pydantic

Definieren Sie Anfragemodelle mit Python-Klassen und Type Hints. FastAPI validiert, parst und serialisiert Daten automatisch.

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

Ungültige Daten geben einen 422-Fehler mit detaillierten Validierungsmeldungen zurück.

### 3. Abhängigkeitsinjektion

Das Abhängigkeitsinjektionssystem von FastAPI hilft, gemeinsame Logik (z. B. Datenbankverbindungen, Authentifizierung) sauber zu verwalten.

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

Abhängigkeiten können wiederverwendet und verschachtelt werden, was die Modularität und Testbarkeit verbessert.

### 4. Async & WebSocket-Unterstützung

Nutzen Sie `async/await` für Szenarien mit hoher Gleichzeitigkeit oder WebSockets für Echtzeitkommunikation.

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

### 5. Sicherheit

FastAPI enthält Werkzeuge für OAuth2, JWT, HTTP Basic und API-Schlüssel – alle in das OpenAPI-Schema integriert.

```python
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
def read_current_user(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

Das Sicherheitsschema erscheint automatisch in der generierten Dokumentation, sodass Benutzer sich über die Swagger UI authentifizieren können.

---

FastAPI stellt einen Paradigmenwechsel in der Python-Webentwicklung dar. Indem es das Framework um standardmäßige Python Type Hints zentriert, reduziert es drastisch den Boilerplate-Code, beseitigt die Trennung zwischen Code und Dokumentation und bietet eine außergewöhnlich reibungslose Entwicklererfahrung. Ob Sie RESTful-Mikrodienste, ML-Modell-Endpunkte oder Echtzeitanwendungen erstellen, FastAPI ist eine starke, produktionsreife Wahl.