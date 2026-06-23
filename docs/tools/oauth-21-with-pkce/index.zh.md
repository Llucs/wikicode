---
title: OAuth 2.1 与 PKCE：实施指南
description: 一种安全认证方法，结合 OAuth 2.1 与授权码交换证明密钥（PKCE），以防御授权码拦截攻击。
created: 2026-06-23
tags:
  - oauth2.1
  - pkce
  - authentication
  - security
  - authorization-code-flow
status: draft
---

# OAuth 2.1 与 PKCE：实施指南

## 概述

OAuth 2.1 是 OAuth 2.0 框架（RFC 6749）及其大量修订版的安全聚焦整合。它简化了核心规范，同时通过将先前推荐的做法变为**强制**要求来强化安全性。**授权码交换证明密钥（PKCE）** 最初在 RFC 7636 中为移动端和原生应用定义，现在已成为 OAuth 2.1 中**所有**客户端授权码流程的必需组件。

本指南涵盖采用 OAuth 2.1 与 PKCE 在现代应用中的原理、实施步骤、关键特性及迁移策略。

---

## 历史与演进

| 年份 | 事件 | 影响 |
|------|------|------|
| 2012 | OAuth 2.0 (RFC 6749) | 引入多种授权类型，包括隐式授权和密码授权，后证明不安全。 |
| 2015 | PKCE (RFC 7636) | 创建用于防止授权码拦截攻击，主要针对公开客户端。 |
| 2020 | OAuth 安全最佳实践 (RFC 9700) | 正式弃用隐式授权和密码授权；要求所有使用授权码流程的公开客户端强制使用 PKCE。 |
| 2023+ | OAuth 2.1 | 将最佳实践建议整合为单一核心规范，使 PKCE 对**所有**客户端成为强制要求，并完全移除不安全的授权类型。 |

---

## 为什么 OAuth 2.1 + PKCE 重要

OAuth 2.1 通过设计而非配置消除了整类攻击：

- **授权码拦截** – PKCE 确保交换授权码的一方与请求它的一方是同一方，即使授权码被拦截。
- **混合攻击** – 严格的重定向 URI 匹配防止攻击者替换自己的重定向。
- **针对授权码的 CSRF** – `code_verifier` 作为不可猜测的安全随机数。
- **移除不安全流程** – 隐式授权和资源拥有者密码授权被移除，关闭常见攻击向量。

**生产部署**（如 MCP 服务器，例如 Azure Container Apps）现在要求以 OAuth 2.1 + PKCE 作为标准认证方法。

---

## OAuth 2.1 的关键特性

### 1. 强制使用 PKCE

授权码流程**必须**包含 `code_challenge` 和 `code_verifier`。即使具有 `client_secret` 的机密客户端也能从纵深防御中受益。

### 2. 移除隐式授权和密码授权

仅保留授权码、客户端凭证和刷新令牌授权。所有其他授权类型均已弃用。

### 3. 严格的重定向 URI 验证

重定向 URI 必须使用精确字符串匹配进行比较。不允许通配符或模式匹配。

### 4. 刷新令牌轮换

刷新令牌应为一次性使用。如果刷新令牌被重用，则自动撤销，表明存在泄露。

### 5. 发送者约束的访问令牌

令牌应通过 mTLS（双向 TLS）或 DPoP（令牌持有者证明）绑定到客户端，尽可能替代简单的 Bearer 令牌。

---

## 实施流程（逐步）

### 1. 客户端准备：生成 PKCE 参数

客户端必须生成加密随机的 `code_verifier`，并计算其 SHA-256 哈希作为 `code_challenge`。

**使用 Node.js 的示例（需要 Node 15+）**

```javascript
import crypto from 'crypto';

// 生成安全随机的 code_verifier（43-128 字符）
const codeVerifier = crypto.randomBytes(32)
  .toString('base64url')
  .slice(0, 128);

// 计算 S256 code_challenge
const codeChallenge = crypto
  .createHash('sha256')
  .update(codeVerifier)
  .digest('base64url');

console.log({ codeVerifier, codeChallenge });
```

**输出（已脱敏）：**
```json
{
  "codeVerifier": "fdb8...d2a9",
  "codeChallenge": "EbZ6...7Qxw"
}
```

### 2. 授权请求

将用户重定向到授权服务器的 `/authorize` 端点，包含以下参数：

```
GET /authorize?
  response_type=code
  &client_id=YOUR_CLIENT_ID
  &redirect_uri=https://yourapp.com/callback
  &scope=openid%20profile%20email
  &code_challenge=EbZ6...7Qxw
  &code_challenge_method=S256
  &state=OPAQUE_STATE_VALUE
```

- `code_challenge_method` **必须**为 `S256`。不允许使用 plain 方法。

### 3. 接收授权码

用户认证并同意后，授权服务器重定向到 `redirect_uri`，附带 `?code=AUTHORIZATION_CODE`。

```
GET /callback?code=AUTHORIZATION_CODE&state=OPAQUE_STATE_VALUE
```

验证 `state` 参数以防止 CSRF 攻击。

### 4. 令牌请求（后端通道）

客户端向 `/token` 端点发送 POST 请求，包含 `code_verifier`。

**使用 `oauth4webapi` 的示例（推荐用于 OAuth 2.1）**

```javascript
import * as oauth from 'oauth4webapi';

const issuer = new URL('https://authorization-server.com');
const clientId = 'YOUR_CLIENT_ID';
const clientSecret = undefined; // 公开客户端

const as = await oauth.discoveryRequest(issuer);
const { authorization_server } = oauth.processDiscoveryResponse(as, {});

const client = {
  client_id: clientId,
  token_endpoint_auth_method: 'none',
};

const authCode = 'AUTHORIZATION_CODE';
const codeVerifier = 'fdb8...d2a9'; // 来自步骤 1

const response = await oauth.authorizationCodeGrantRequest(
  authorization_server,
  client,
  authCode,
  issuer + '/redirect_uri',
  codeVerifier,
);

const tokens = await oauth.processAuthorizationCodeResponse(
  authorization_server,
  client,
  response,
  { expectedNonce: 'NONCE_FROM_ID_TOKEN' },
);
```

**Curl 表示：**

```bash
curl -X POST https://authorization-server.com/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=AUTHORIZATION_CODE" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "redirect_uri=https://yourapp.com/callback" \
  -d "code_verifier=fdb8...d2a9"
```

### 5. 服务器验证

令牌端点执行：

```
HASH(code_verifier) == code_challenge
```

如果哈希匹配，则授权码有效。否则请求失败。

### 6. 令牌响应

成功响应包含 `access_token`、`refresh_token`（如果请求了 offline_access），以及可选的 `id_token`。

```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "DPoP",
  "expires_in": 3600,
  "refresh_token": "dGhpcyBp...",
  "scope": "openid profile email"
}
```

---

## 库支持

### 服务端（授权服务器）

| 库 / 平台 | OAuth 2.1 支持 |
|-----------|----------------|
| Keycloak  | 是（默认强制 PKCE） |
| Entra ID (Azure AD) | 是（授权码 + PKCE） |
| Auth0     | 是（需要配置） |
| Okta      | 是 |
| Curity    | 是 |
| Spring Security 6+ | 是（`oauth2Client` 支持 PKCE） |

### 客户端（应用程序）

| 语言    | 库 | 说明 |
|---------|-----|------|
| Node.js  | [`oauth4webapi`](https://github.com/panva/oauth4webapi) | 作者专属，已就绪 OAuth 2.1 |
| Python   | [`Authlib`](https://authlib.org/) | 支持 PKCE 和 OAuth 2.1 模式 |
| Java     | Spring Security 6+ | 内置 `NimbusJwtDecoder` 并支持 PKCE |
| 移动端   | AppAuth (Android/iOS) | 原生 PKCE 支持 |
| Web SPA  | BFF 模式或 Web Workers | 浏览器中不直接支持 PKCE，请使用后端为前端模式 |

---

## 从 OAuth 2.0 迁移

### 检查清单

1. **将隐式授权替换**为授权码 + PKCE。
2. **将密码授权替换**为授权码 + PKCE 或客户端凭证（用于机器对机器）。
3. **强制每次授权码交换使用 PKCE**。
4. **启用刷新令牌轮换**（一次性令牌）。
5. **更新重定向 URI 比较**为精确字符串匹配。
6. **切换为 S256** 挑战方法（如果之前使用 plain）。

### 示例：迁移旧版授权码流程

**之前（OAuth 2.0 – 可选 PKCE）**

```
步骤 1: client_id + redirect_uri → 获取 code
步骤 2: code + client_secret → 获取 token
```

**之后（OAuth 2.1 – 强制 PKCE）**

```
步骤 1: client_id + redirect_uri + code_challenge (S256) → 获取 code
步骤 2: code + code_verifier → 获取 token
```

---

## 真实世界示例：Azure Container Apps 上的 MCP 服务器

模型上下文协议（MCP）规范（截至 2026-03-15）要求在与代理服务器交互时使用 OAuth 2.1 + PKCE 进行授权。以下是简化的配置：

1. **定义保护资源元数据（PRM）** – 暴露 `.well-known/oauth-authorization-server`
2. **实现动态客户端注册**（RFC 7591）用于客户端。
3. **作用域设计** – 为每个资源定义细粒度作用域（例如 `files:read`、`compute:execute`）。
4. **令牌验证** – 每个 API 请求必须验证访问令牌的签名和绑定密钥。

Azure CLI 配置示例（概念）：

```bash
az containerapp create \
  --name mcp-server \
  --environment MyEnv \
  --image myregistry.azurecr.io/mcp:v1 \
  --secrets oauth-jwks-secret="$(cat jwks.json)" \
  --env-vars OAUTH_AUTHORIZATION_URL="https://login.contoso.com/authorize" \
             OAUTH_TOKEN_URL="https://login.contoso.com/token" \
             OAUTH_CLIENT_ID="mcp-server" \
  --ingress 'external'
```

然后客户端（例如 VSCode Azure MCP 扩展）在调用 MCP 工具之前执行 PKCE 流程。

---

## 安全最佳实践

- **使用状态参数** – 将授权请求绑定到用户会话。
- **安全存储 code_verifier** – 存放于后端会话或安全的客户端存储（不在 URL 中）。
- **验证每个令牌** – 检查签名、颁发者、受众和过期时间。
- **轮换刷新令牌** – 每次刷新生成新令牌并使上一个失效。
- **实现 DPoP** – 在访问令牌中添加 `cnf` 声明以实现发送者约束支持。
- **记录令牌重用** – 检测潜在的令牌窃取。

---

## 常见问题排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 令牌交换时出现 `invalid_grant` | `code_verifier` 与 `code_challenge` 不匹配 | 重新对验证器进行哈希，与创建时完全相同（相同算法，相同字符编码） |
| `redirect_uri_mismatch` | URL 比较不精确 | 确保 `redirect_uri` 完全匹配，包括尾部斜杠 |
| 授权码过期 | 超时 > 10 分钟 | 重新执行完整流程 |
| 轮换后刷新令牌被拒绝 | 检测到令牌重放 | 客户端必须丢弃旧刷新令牌；正确实现一次性轮换 |

---

## 参考文献

- [OAuth 2.1 草案规范](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)
- [PKCE RFC 7636](https://datatracker.ietf.org/doc/html/rfc7636)
- [OAuth 安全最佳实践 (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [oauth4webapi – 官方实现](https://github.com/panva/oauth4webapi)
- [Authlib – Python 的 OAuth 2.1](https://authlib.org/)
- [Spring Security 6 OAuth 2.1 客户端](https://docs.spring.io/spring-security/reference/servlet/oauth2/client/index.html)

---

## 结论

采用 OAuth 2.1 与 PKCE 不仅仅是合规要求——更是安全态势的根本改进。通过强制使用 PKCE、移除弱流程并强制执行严格验证，OAuth 2.1 确保现代应用能够抵御最常见的授权攻击。无论您是在构建新的 MCP 服务器、迁移旧版移动应用，还是加固单页应用，本规范都提供了一条清晰且安全的路径。