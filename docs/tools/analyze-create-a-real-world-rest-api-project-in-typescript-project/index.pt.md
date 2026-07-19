---
title: Crie um Projeto de API REST do Mundo Real em TypeScript
description: Um guia completo para construir uma API REST robusta usando TypeScript, Express.js e MongoDB.
created: 2026-07-19
tags:
  - TypeScript
  - Express.js
  - MongoDB
  - API REST
  - Autenticação
  - Docker
status: rascunho
---

# Crie um Projeto de API REST do Mundo Real em TypeScript

Este guia o guiará através do processo de construção de uma API REST robusta usando TypeScript, Express.js e MongoDB. Inclui documentação detalhada, melhores práticas e exemplos do mundo real para ajudar você a entender e implementar uma solução de API de produção.

## Características Principais

1. **TypeScript**: Tipagem estática para detecção de erros melhorada e qualidade do código.
2. **Express.js**: Um framework web popular em Node.js.
3. **MongoDB**: Um banco de dados NoSQL de documentos para armazenamento de dados.
4. **JWT Autenticação**: Rotas seguras usando Tokens de Juntura de JSON (JWT).
5. **Mongoose**: Uma biblioteca de modelo de objeto (ODM) para MongoDB.
6. **Testes**: Testes de unidade e integração com Jest e Supertest.
7. **Swagger Documentação**: Documentação de API gerada automaticamente para referência fácil.

## Instalação

1. **Clonar o Repositório**:
   ```sh
   git clone https://github.com/username/repo.git
   cd repo
   ```

2. **Instalar Dependências**:
   ```sh
   npm install
   ```

3. **Configurar MongoDB**:
   - Instale o MongoDB se ainda não estiver instalado.
   - Inicie o servidor do MongoDB.
   - Configure a string de conexão no arquivo `.env`.

4. **Configurar Variáveis de Ambiente**:
   - Atualize o arquivo `.env` com variáveis de ambiente necessárias, como a string de conexão do banco de dados, segredo JWT, etc.

5. **Executar o Servidor**:
   ```sh
   npm start
   ```

## Uso Básico

### Pontos de Extremidade da API

1. **Gerenciamento de Usuários**:
   - **Criar Usuário**: POST `/api/users`
   - **Obter Usuário**: GET `/api/users/:id`
   - **Atualizar Usuário**: PATCH `/api/users/:id`
   - **Excluir Usuário**: DELETE `/api/users/:id`

2. **Gerenciamento de Produtos**:
   - **Criar Produto**: POST `/api/products`
   - **Obter Produto**: GET `/api/products/:id`
   - **Atualizar Produto**: PATCH `/api/products/:id`
   - **Excluir Produto**: DELETE `/api/products/:id`

3. **Gerenciamento de Pedidos**:
   - **Criar Pedido**: POST `/api/orders`
   - **Obter Pedido**: GET `/api/orders/:id`
   - **Atualizar Pedido**: PATCH `/api/orders/:id`
   - **Excluir Pedido**: DELETE `/api/orders/:id`

4. **Autenticação**:
   - **Gerar Token JWT**: POST `/api/auth/login`
   - **Proteger Rotas**: Use o token JWT na cabeca `Authorization`

### Testes

1. **Testes de Unidade**:
   - Use Jest para testes de unidade.
   - Execute os testes com:
     ```sh
     npm test
     ```

2. **Testes de Integração**:
   - Use Supertest para testes de integração.
   - Execute os testes com:
     ```sh
     npm test
     ```

### Documentação Swagger

1. **Acessar Swagger UI**:
   - Navegue para `http://localhost:3000/docs` no seu navegador.
   - Use a documentação gerada para entender e interagir com a API.

### Autenticação

1. **Gerar Token JWT**:
   - Faça uma requisição POST para `/api/auth/login` com credenciais de usuário.
   - Exemplo usando `curl`:
     ```sh
     curl -X POST http://localhost:3000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password"}'
     ```

2. **Incluir JWT nas Requisições**:
   - Use o token JWT na cabeca `Authorization` para rotas protegidas.
   - Exemplo usando `curl`:
     ```sh
     curl -X GET http://localhost:3000/api/users/1 \
     -H "Authorization: Bearer <JWT_TOKEN>"
     ```

### Gerenciamento de Dados

1. **Definir Esquemas do Mongoose**:
   - Use o Mongoose para definir esquemas para modelos.
   - Exemplo de esquema para um Usuário:
     ```typescript
     import { Schema, model } from 'mongoose';

     const UserSchema = new Schema({
       name: String,
       email: { type: String, unique: true },
       password: String
     });

     export const User = model('User', UserSchema);
     ```

2. **Realizar Operações CRUD**:
   - Use métodos do Mongoose para realizar operações CRUD.
   - Exemplo para criar um usuário:
     ```typescript
     import { Request, Response } from 'express';
     import User from '../models/User';

     const createUser = async (req: Request, res: Response) => {
       const { name, email, password } = req.body;
       const user = new User({ name, email, password });
       await user.save();
       res.status(201).json(user);
     };
     ```

## Conclusão

Seguindo o guia detalhado e usando o código-base fornecido como ponto de partida, você pode estender e personalizar a API para atender requisitos específicos do projeto. Este projeto completo não só fornece um exemplo prático, mas também serve como uma ótima ferramenta de aprendizado para entender as melhores práticas modernas de desenvolvimento web com TypeScript, Express.js e MongoDB.

Feliz codificação!