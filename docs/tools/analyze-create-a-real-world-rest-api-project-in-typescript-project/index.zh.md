---
title: 使用 TypeScript 创建一个实际项目的 REST API
description: 本综合指南将指导您使用 TypeScript、Express.js 和 MongoDB 构建一个健壮的 REST API。它包括详细的文档、最佳实践和实际示例，帮助您理解和实现一个生产就绪的 API 解决方案。
created: 2026-07-19
tags:
  - TypeScript
  - Express.js
  - MongoDB
  - REST API
  - 认证
  - Docker
status: draft
---

# 使用 TypeScript 创建一个实际项目的 REST API

本指南将带您逐步构建一个使用 TypeScript、Express.js 和 MongoDB 的健壮 REST API。它包括详细的文档、最佳实践和实际示例，帮助您理解和实现一个生产就绪的 API 解决方案。

## 关键功能

1. **TypeScript**: 静态类型检测，以提高错误检测和代码质量。
2. **Express.js**: 一个流行的 Node.js Web 应用程序框架。
3. **MongoDB**: 一个 NoSQL 文档数据库，用于数据存储。
4. **JWT 认证**: 使用 JSON Web Tokens (JWT) 安全地保护路由。
5. **Mongoose**: 一个 MongoDB 的对象数据建模 (ODM) 库。
6. **测试**: 使用 Jest 和 Supertest 进行单元和集成测试。
7. **Swagger 文档**: 生成的 API 文档，方便查阅。

## 安装

1. **克隆仓库**：
   ```sh
   git clone https://github.com/username/repo.git
   cd repo
   ```

2. **安装依赖项**：
   ```sh
   npm install
   ```

3. **设置 MongoDB**：
   - 如果尚未安装，请安装 MongoDB。
   - 启动 MongoDB 服务器。
   - 在 `.env` 文件中配置连接字符串。

4. **配置环境变量**：
   - 在 `.env` 文件中更新必要的环境变量，例如数据库连接字符串、JWT 密钥等。

5. **运行服务器**：
   ```sh
   npm start
   ```

## 基本用法

### API 端点

1. **用户管理**：
   - **创建用户**：POST `/api/users`
   - **获取用户**：GET `/api/users/:id`
   - **更新用户**：PATCH `/api/users/:id`
   - **删除用户**：DELETE `/api/users/:id`

2. **产品管理**：
   - **创建产品**：POST `/api/products`
   - **获取产品**：GET `/api/products/:id`
   - **更新产品**：PATCH `/api/products/:id`
   - **删除产品**：DELETE `/api/products/:id`

3. **订单管理**：
   - **创建订单**：POST `/api/orders`
   - **获取订单**：GET `/api/orders/:id`
   - **更新订单**：PATCH `/api/orders/:id`
   - **删除订单**：DELETE `/api/orders/:id`

4. **认证**：
   - **生成 JWT 令牌**：POST `/api/auth/login`
   - **保护路由**：在 `Authorization` 头中使用 JWT 令牌

### 测试

1. **单元测试**：
   - 使用 Jest 进行单元测试。
   - 运行测试：
     ```sh
     npm test
     ```

2. **集成测试**：
   - 使用 Supertest 进行集成测试。
   - 运行测试：
     ```sh
     npm test
     ```

### Swagger 文档

1. **访问 Swagger UI**：
   - 在浏览器中导航到 `http://localhost:3000/docs`。
   - 使用生成的文档来理解和与 API 交互。

### 认证

1. **生成 JWT 令牌**：
   - 向 `/api/auth/login` 发送 POST 请求并附带用户凭据。
   - 使用 `curl` 为例：
     ```sh
     curl -X POST http://localhost:3000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password"}'
     ```

2. **在请求中包含 JWT 令牌**：
   - 对受保护的路由使用 JWT 令牌在 `Authorization` 头中。
   - 使用 `curl` 为例：
     ```sh
     curl -X GET http://localhost:3000/api/users/1 \
     -H "Authorization: Bearer <JWT_TOKEN>"
     ```

### 数据管理

1. **定义 Mongoose 模型**：
   - 使用 Mongoose 定义模型的模式。
   - 用户模式示例：
     ```typescript
     import { Schema, model } from 'mongoose';

     const UserSchema = new Schema({
       name: String,
       email: { type: String, unique: true },
       password: String
     });

     export const User = model('User', UserSchema);
     ```

2. **执行 CRUD 操作**：
   - 使用 Mongoose 方法执行 CRUD 操作。
   - 创建用户示例：
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

## 结论

通过遵循本详细指南并以提供的代码库作为起点，您可以扩展和定制 API 以满足特定项目需求。这个全面的项目不仅提供了一个实用示例，也是一个学习使用 TypeScript、Express.js 和 MongoDB 现代 Web 开发实践的绝佳工具。

祝您编码愉快！