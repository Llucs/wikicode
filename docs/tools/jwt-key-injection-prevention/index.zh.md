---
title: JWT 密钥注入预防
description: 通过在使用 JWT 从数据库或系统命令中检索加密密钥之前对 `kid` 参数进行净化来防止潜在的 SQL 注入或命令注入攻击。
created: 2026-07-07
tags:
  - jwt
  - 安全
  - 注入
status: 草稿
---

# JWT 密钥注入预防

## 什么是 JWT 密钥注入？

JWT（JSON Web Token）密钥注入是一种安全漏洞，攻击者可以通过注入或篡改 JSON Web Token (JWT) 来获得未经授权的系统访问权限。这可能发生在系统不恰当地验证或验证 JWT 的完整性的情况下，允许攻击者修改令牌的有效载荷或签名。

## 关键功能

1. **签名验证**：确保 JWT 的签名有效且未被篡改。
2. **有效载荷完整性**：验证 JWT 有效载荷内容未被修改。
3. **过期检查**：确保 JWT 未过期。
4. **吊销列表**：检查 JWT 是否已被吊销。

## 历史

JWT 概念自 2010 年 JSON Web Token 标准引入以来一直在使用。然而，具体的关键注入漏洞问题在近年来随着更多应用程序依赖 JWT 进行身份验证和授权而引起了更多关注。 OWASP（开放 Web 应用程序安全项目）准则中指出的漏洞使人们对 JWT 安全性更加关注。

## 使用场景

1. **身份验证和授权**：JWT 在跨 Web 和移动应用程序的身份验证和授权中广泛使用。
2. **无状态会话**：JWT 经常用于无状态 API 来管理会话状态。
3. **单点登录 (SSO)**：JWT 可以通过允许用户一次认证并跨多个系统验证来实现 SSO。

## 安装

JWT 验证通常由支持 JWT 的库或框架处理。例如，在一个 Node.js 应用程序中，你可以使用 `jsonwebtoken` 库生成和验证令牌。以下是基本的安装过程：

1. **Node.js**：
   ```bash
   npm install jsonwebtoken
   ```
2. **Python**：
   ```bash
   pip install PyJWT
   ```

## 基本用法

以下是在 Node.js 中使用 `jsonwebtoken` 进行 JWT 验证的基本示例：

1. **生成 JWT**：
   ```javascript
   const jwt = require('jsonwebtoken');

   const secret = 'your-secret-key';
   const payload = { userId: 123, role: 'admin' };

   const token = jwt.sign(payload, secret);
   console.log(token);
   ```

2. **验证 JWT**：
   ```javascript
   jwt.verify(token, secret, (err, decoded) => {
     if (err) {
       console.error('Token verification failed:', err);
     } else {
       console.log('Decoded:', decoded);
     }
   });
   ```

## 防止密钥注入

1. **安全密钥管理**：保持 JWT 密钥安全，并不要在客户端代码中暴露它。
2. **令牌过期**：为 JWT 设置合理的过期时间，以减小攻击窗口。
3. **吊销机制**：实现一种吊销已 compromized 令牌的机制。
4. **签名验证**：始终在服务器端验证令牌签名。
5. **有效载荷白名单**：仅允许 JWT 有效载荷中的白名单声明。

### 吊销列表示例

你可以在数据库中维护一个吊销令牌列表，并在验证令牌时检查此列表：

1. **数据库设置**：
   ```sql
   CREATE TABLE revoked_tokens (
     token VARCHAR(255) PRIMARY KEY
   );
   ```

2. **检查吊销列表**：
   ```javascript
   const isTokenRevoked = (token) => {
     const tokenExists = revokedTokens.some((revokedToken) => revokedToken === token);
     return tokenExists;
   };

   jwt.verify(token, secret, (err, decoded) => {
     if (err || isTokenRevoked(token)) {
       console.error('Token verification failed:', err);
     } else {
       console.log('Decoded:', decoded);
     }
   });
   ```

通过实施这些策略，你可以在你的应用程序中显著降低 JWT 密钥注入漏洞的风险。