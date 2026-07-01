---
title: Starlette-Graphene3: Un Potente Framework para APIs de GraphQL
description: Una biblioteca recomendada para trabajar con GraphQL, diseñada para ser lo más cercana posible al diseño de FastAPI con un énfasis en anotaciones de tipo.
created: 2026-07-01
tags:
  - Starlette
  - Graphene3
  - GraphQL
  - Python
  - Desarrollo Web
status: borrador
---

# Starlette-Graphene3: Un Potente Framework para APIs de GraphQL

Starlette-Graphene3 es un proyecto que integra Starlette y Graphene3 para crear un entorno de desarrollo simplificado para construir APIs de GraphQL. La integración proporciona una experiencia fluida, combinando las mejores características de ambos bibliotecas para ofrecer un marco simple pero potente para el desarrollo web.

## ¿Qué es Starlette-Graphene3?

Starlette-Graphene3 es una combinación de Starlette y Graphene3, dos bibliotecas populares en Python para construir aplicaciones web. Starlette es un marco de trabajo ligero y de alta rendimiento para Python, mientras que Graphene3 es una biblioteca de GraphQL para Python que permite a los desarrolladores definir y consumir APIs de GraphQL. Juntos, proporcionan una herramienta potente y flexible para construir aplicaciones web robustas, especialmente aquellas que requieren APIs de GraphQL.

## Características Principales

1. **Starlette**: Proporciona un marco de trabajo robusto y minimalista para la construcción de APIs y aplicaciones. Está construido sobre ASGI (Asynchronous Server Gateway Interface) y es compatible con código sincrónico y asíncrono.
2. **Graphene3**: Permite definir y consumir APIs de GraphQL en una aplicación Python. Soporta consultas y mutaciones tanto sincrónicas como asíncronas.

## Historia

- **Starlette**: Lanzada en 2018, Starlette fue creada por Daniel Sher y es un marco de trabajo ligero y de alta rendimiento para Python.
- **Graphene3**: Inicialmente parte del proyecto Graphene, Graphene3 se lanzó oficialmente como una biblioteca independiente en 2019. Fue desarrollado para proporcionar una implementación de GraphQL más flexible y potente para Python.

## Casos de Uso

- **Desarrollo de APIs**: Construcción de APIs robustas, escalables y de alta performance.
- **APIs de GraphQL**: Creación de puntos finales de GraphQL para la recuperación de datos y mutaciones.
- **Aplicaciones Web**: Desarrollo de aplicaciones web completas con un backend de GraphQL.
- **Microservicios**: Creación de microservicios que exponen APIs de GraphQL para la comunicación.

## Instalación

Para instalar Starlette-Graphene3, puedes usar pip:

```bash
pip install starlette graphene3
```

## Uso Básico

1. **Definir Esquema de GraphQL**: Definir los tipos y consultas en tu esquema.

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

2. **Integrar con Starlette**: Configura una aplicación Starlette e intégrala con Graphene3.

```python
# app.py
from starlette.applications import Starlette
from starlette.graphql import GraphQLApp
from schema import schema

app = Starlette()
app.add_route('/graphql', GraphQLApp(schema=schema))
```

3. **Ejecutar la Aplicación**: Ejecuta la aplicación Starlette para iniciar el servidor.

```bash
uvicorn app:app --reload
```

4. **Consultar la API**: Usa un cliente de GraphQL (por ejemplo, GraphiQL o GraphQL Playground) para interactuar con la API.

## Ejemplo

Aquí tienes un ejemplo más completo:

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

### Ejecutar la Aplicación

Para ejecutar la aplicación, ejecuta el siguiente comando:

```bash
uvicorn app:app --reload
```

Este comando iniciará la aplicación en `http://0.0.0.0:8000/`.

## Conclusión

Starlette-Graphene3 proporciona una solución robusta y flexible para la construcción de APIs de GraphQL y aplicaciones web. Al aprovechar las fortalezas de ambos Starlette y Graphene3, los desarrolladores pueden crear aplicaciones de alta performance y escalables. Ya sea que estés construyendo un microservicio o una aplicación web completa, esta combinación ofrece un marco potente para el desarrollo.