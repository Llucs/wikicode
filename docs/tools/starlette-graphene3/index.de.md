---
title: Starlette-Graphene3: Ein mächtiger Rahmenwerk für GraphQL APIs
description: Ein Bibliothek, die für die Arbeit mit GraphQL empfohlen wird, das sich amclosest an die Designrichtlinien von FastAPI ausrichtet und sich auf Typangaben konzentriert.
created: 2026-07-01
tags:
  - Starlette
  - Graphene3
  - GraphQL
  - Python
  - Webentwicklung
status: Entwurf
---

# Starlette-Graphene3: Ein mächtiger Rahmenwerk für GraphQL APIs

Starlette-Graphene3 ist ein Projekt, das Starlette und Graphene3 integriert, um eine optimierte Entwicklungsumgebung für das Erstellen von GraphQL APIs zu schaffen. Die Integration bietet eine glatte Benutzererfahrung, indem sie die besten Funktionen beider Bibliotheken kombiniert und ein einfaches, aber mächtiges Rahmenwerk für die Webentwicklung anbietet.

## Was ist Starlette-Graphene3?

Starlette-Graphene3 ist die Kombination von Starlette und Graphene3, zwei populären Python-Frameworks/Bibliotheken für die Erstellung von Webanwendungen. Starlette ist ein leichter, high-performance Python Webframework, während Graphene3 eine GraphQL-Bibliothek für Python ist, die es Entwicklern ermöglicht, GraphQL APIs zu definieren und zu konsumieren. Gemeinsam bieten sie ein mächtiges und flexibles Werkzeugset für die Erstellung robuster Webanwendungen, insbesondere solcher, die GraphQL APIs erfordern.

## Kernfunktionen

1. **Starlette**: Bietet ein robustes und minimalistisches Framework für die Erstellung von APIs und Anwendungen. Es basiert auf ASGI (Asynchronous Server Gateway Interface) und ist mit synchronen und asynchronen Code kompatibel.
2. **Graphene3**: Erlaubt die Definition und Konsumtion von GraphQL APIs in einer Python-Anwendung. Es unterstützt sowohl synchronen als auch asynchronen Abfragen und Mutationen.

## Geschichte

- **Starlette**: Veröffentlicht im Jahr 2018, wurde Starlette von Daniel Sher entwickelt und ist ein leichtes, high-performance Python Webframework.
- **Graphene3**: Ursprünglich Teil des Graphene-Projekts, wurde Graphene3 2019 als eigenständige Bibliothek veröffentlicht. Es wurde entwickelt, um eine mächtigere und flexiblere GraphQL-Implementierung für Python zu bieten.

## Nutzungsfälle

- **API-Entwicklung**: Das Erstellen robuster, skalierbarer und performanter APIs.
- **GraphQL APIs**: Das Erstellen von GraphQL-Endpunkten für Datensuch- und Mutationen.
- **Webanwendungen**: Das Erstellen vollwertiger Webanwendungen mit einem GraphQL-Backend.
- **Microservices**: Das Erstellen von Microservices, die GraphQL APIs zum Austausch ausweisen.

## Installation

Um Starlette-Graphene3 zu installieren, können Sie pip verwenden:

```bash
pip install starlette graphene3
```

## Grundlegende Nutzung

1. **GraphQL-Schema definieren**: Definieren Sie die Typen und Abfragen in Ihrem Schema.

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

2. **Integrieren mit Starlette**: Stellen Sie eine Starlette-Anwendung zusammen und fügen Sie die Graphene3-Integration hinzu.

```python
# app.py
from starlette.applications import Starlette
from starlette.graphql import GraphQLApp
from schema import schema

app = Starlette()
app.add_route('/graphql', GraphQLApp(schema=schema))
```

3. **Die Anwendung starten**: Führen Sie die Starlette-Anwendung aus, um den Server zu starten.

```bash
uvicorn app:app --reload
```

4. **API abfragen**: Verwenden Sie einen GraphQL-Client (z.B. GraphiQL oder GraphQL Playground), um mit der API zu interagieren.

## Beispiel

Hier ist ein vollständigeres Beispiel:

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

### Die Anwendung starten

Um die Anwendung auszuführen, führen Sie den folgenden Befehl aus:

```bash
uvicorn app:app --reload
```

Dies wird die Anwendung auf `http://0.0.0.0:8000/` starten.

## Zusammenfassung

Starlette-Graphene3 bietet ein robustes und flexibles Lösungsmittel für das Erstellen von GraphQL APIs und Webanwendungen. Indem sie die Stärken beider Starlette und Graphene3 kombinieren, können Entwickler hochperformante, skalierbare Anwendungen erstellen. Unabhängig davon, ob Sie ein Microservice oder eine vollwertige Webanwendung erstellen, bietet dieses Kombinationsprodukt ein mächtiges Rahmenwerk für die Entwicklung.