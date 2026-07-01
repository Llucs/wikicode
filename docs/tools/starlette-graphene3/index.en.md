---
title: Starlette-Graphene3: A Powerful Framework for GraphQL APIs
description: A library recommended for working with GraphQL, designed to be closest to FastAPI's design with a focus on type annotations.
created: 2026-07-01
tags:
  - Starlette
  - Graphene3
  - GraphQL
  - Python
  - Web Development
status: draft
---

# Starlette-Graphene3: A Powerful Framework for GraphQL APIs

Starlette-Graphene3 is a project that integrates Starlette and Graphene3 to create a streamlined development environment for building GraphQL APIs. The integration provides a seamless experience, combining the best features of both libraries to offer a simple yet powerful framework for web development.

## What is Starlette-Graphene3?

Starlette-Graphene3 is a combination of Starlette and Graphene3, two popular Python frameworks/libraries for building web applications. Starlette is a lightweight, high-performance web framework for Python, while Graphene3 is a GraphQL library for Python that allows developers to define and consume GraphQL APIs. Together, they provide a powerful and flexible toolset for building robust web applications, especially those requiring GraphQL APIs.

## Key Features

1. **Starlette**: Provides a robust and minimalistic framework for building APIs and applications. It is built on top of ASGI (Asynchronous Server Gateway Interface) and is compatible with both synchronous and asynchronous code.
2. **Graphene3**: Allows for the definition and consumption of GraphQL APIs in a Python application. It supports both synchronous and asynchronous queries and mutations.

## History

- **Starlette**: Released in 2018, Starlette was created by Daniel Sher and is a lightweight, high-performance web framework for Python.
- **Graphene3**: Initially part of the Graphene project, Graphene3 was officially released as a standalone library in 2019. It was developed to provide a more flexible and powerful GraphQL implementation for Python.

## Use Cases

- **API Development**: Building robust, scalable, and performant APIs.
- **GraphQL APIs**: Creating GraphQL endpoints for data fetching and mutation.
- **Web Applications**: Developing full-fledged web applications with a GraphQL backend.
- **Microservices**: Creating microservices that expose GraphQL APIs for communication.

## Installation

To install Starlette-Graphene3, you can use pip:

```bash
pip install starlette graphene3
```

## Basic Usage

1. **Define GraphQL Schema**: Define the types and queries in your schema.

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

2. **Integrate with Starlette**: Set up a Starlette application and add the Graphene3 integration.

```python
# app.py
from starlette.applications import Starlette
from starlette.graphql import GraphQLApp
from schema import schema

app = Starlette()
app.add_route('/graphql', GraphQLApp(schema=schema))
```

3. **Run the Application**: Run the Starlette application to start the server.

```bash
uvicorn app:app --reload
```

4. **Query the API**: Use a GraphQL client (e.g., GraphiQL or GraphQL Playground) to interact with the API.

## Example

Here is a more complete example:

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

### Running the Application

To run the application, execute the following command:

```bash
uvicorn app:app --reload
```

This will start the application on `http://0.0.0.0:8000/`.

## Conclusion

Starlette-Graphene3 provides a robust and flexible solution for building GraphQL APIs and web applications. By leveraging the strengths of both Starlette and Graphene3, developers can create high-performance, scalable applications. Whether you are building a microservice or a full-fledged web application, this combination offers a powerful framework for development.