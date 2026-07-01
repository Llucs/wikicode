---
title: Starlette-Graphene3: Um Conjunto Potente para APIs GraphQL
description: Uma biblioteca recomendada para trabalhar com GraphQL, projetada para ser a mais próxima do design do FastAPI, com foco em anotações de tipo.
created: 2026-07-01
tags:
  - Starlette
  - Graphene3
  - GraphQL
  - Python
  - Desenvolvimento Web
status: rascunho
---

# Starlette-Graphene3: Um Conjunto Potente para APIs GraphQL

Starlette-Graphene3 é um projeto que integra Starlette e Graphene3 para criar um ambiente de desenvolvimento enxuto para a construção de APIs GraphQL. A integração oferece uma experiência fluida, combinando as melhores características de ambos os bibliotecas para fornecer um framework simples e poderoso para o desenvolvimento web.

## O que é Starlette-Graphene3?

Starlette-Graphene3 é uma combinação de Starlette e Graphene3, duas bibliotecas populares em Python para o desenvolvimento de aplicativos web. Starlette é uma framework de API para Python leve e de alta performance, enquanto Graphene3 é uma biblioteca de GraphQL para Python que permite que os desenvolvedores definam e consumam APIs GraphQL. Juntos, eles oferecem uma ferramenta poderosa e flexível para a construção de aplicativos web robustos, especialmente aqueles que requerem APIs GraphQL.

## Características Principais

1. **Starlette**: Fornece uma framework robusta e minimalista para a construção de APIs e aplicativos. Ele é construído em cima do ASGI (Asynchronous Server Gateway Interface) e é compatível com código síncrono e assíncrono.
2. **Graphene3**: Permite a definição e o consumo de APIs GraphQL em um aplicativo Python. Ele suporta tanto consultas quanto mutações síncronas e assíncronas.

## Histórico

- **Starlette**: Lançado em 2018, Starlette foi criado por Daniel Sher e é uma framework de API leve e de alta performance em Python.
- **Graphene3**: Inicialmente parte do projeto Graphene, Graphene3 foi lançado oficialmente como uma biblioteca independente em 2019. Foi desenvolvido para fornecer uma implementação mais flexível e poderosa de GraphQL para Python.

## Casos de Uso

- **Desenvolvimento de APIs**: Construindo APIs robustas, escaláveis e de alta performance.
- **APIs GraphQL**: Criando endpoints GraphQL para o fetching e a mutação de dados.
- **Aplicativos Web**: Desenvolvendo aplicativos web completos com um backend em GraphQL.
- **Microserviços**: Criando microserviços que expõem APIs GraphQL para comunicação.

## Instalação

Para instalar Starlette-Graphene3, você pode usar o pip:

```bash
pip install starlette graphene3
```

## Uso Básico

1. **Definir o Esquema GraphQL**: Defina os tipos e as consultas em seu esquema.

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

2. **Integrar com Starlette**: Configure uma aplicação Starlette e adicione a integração Graphene3.

```python
# app.py
from starlette.applications import Starlette
from starlette.graphql import GraphQLApp
from schema import schema

app = Starlette()
app.add_route('/graphql', GraphQLApp(schema=schema))
```

3. **Rodar a Aplicação**: Execute a aplicação Starlette para iniciar o servidor.

```bash
uvicorn app:app --reload
```

4. **Consultar a API**: Use um cliente GraphQL (por exemplo, GraphiQL ou GraphQL Playground) para interagir com a API.

## Exemplo

Aqui está um exemplo mais completo:

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

### Rodando a Aplicação

Para rodar a aplicação, execute o seguinte comando:

```bash
uvicorn app:app --reload
```

Isso iniciará a aplicação em `http://0.0.0.0:8000/`.

## Conclusão

Starlette-Graphene3 oferece uma solução robusta e flexível para a construção de APIs GraphQL e aplicativos web. Ao aproveitar as forças de ambas as bibliotecas, os desenvolvedores podem criar aplicações de alto desempenho e escaláveis. Seja você esteja construindo um microserviço ou um aplicativo web completo, esta combinação oferece um framework poderoso para o desenvolvimento.