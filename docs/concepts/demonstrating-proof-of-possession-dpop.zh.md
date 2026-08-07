---
title: 展示持有证明（DPoP）——使用 RFC 9449 对 OAuth 令牌进行发送方约束
description: 面向开发者的 DPoP 指南，RFC 9449 机制将 OAuth 2.0 访问令牌和刷新令牌绑定到客户端持有的密钥对，以防止令牌重放和窃取。
created: 2026-08-07
tags:
  - oauth2
  - security
  - rfc-9449
  - dpop
  - identity
status: draft
---

# 展示持有证明（DPoP）

## 什么是 DPoP？

**展示持有证明（DPoP）** 是 **RFC 9449** 中定义的一种应用层 OAuth 2.0 扩展。它通过将访问令牌和刷新令牌绑定到客户端生成并持有的公钥/私钥对，对它们进行*发送方约束*。

DPoP 客户端不会发送裸的 `Authorization: Bearer <token>`，而是向资源服务器证明它仍然持有令牌签发时使用的私钥。每个请求都会在 `DPoP` HTTP 头中携带一个短期有效的、已签名的证明 JWT。该证明以密码学方式绑定到所使用的确切 HTTP 方法、URL 和访问令牌。

由于访问令牌不再具有“Bearer”属性——任何持有者都可以使用它——被盗的令牌在没有匹配私钥的情况下毫无用处。

## 为何重要

普通 OAuth 2.0 Bearer 令牌有一个根本性问题：持有令牌是授权的唯一证明。泄露在服务器日志、referrer 头、浏览器扩展程序中的令牌，或在移动应用被攻破后被截获的令牌，都可能被攻击者重放。

DPoP 通过改变威胁模型来解决此问题：

- 被盗的访问令牌无法被重放，除非攻击者同时窃取了客户端的私钥。
- 访问令牌在授权服务器上被绑定到特定密钥。
- 资源服务器在每次 API 调用时验证密码学证明。
- 刷新令牌也可以进行发送方约束，从而堵住“刷新令牌窃取”的漏洞。

在开放银行 / 符合 FAPI 的 API、电子健康平台和企业身份系统等高安全生态系统中，DPoP 通常是被要求或推荐的。

## DPoP 的工作原理

### 1. 客户端生成密钥对

客户端创建非对称密钥对——通常是 EC P-256（ES256）。私钥由客户端保存。公钥以 JSON Web Key（JWK）形式表示，并包含在每个 DPoP 证明的头部中。

授权服务器通过将 **JWK SHA-256 指纹**（`jkt`）存储在令牌的 `cnf` 声明中，将访问令牌绑定到此公钥：

```text
jkt = base64url(SHA-256("<canonical JSON of public JWK>"))
```

### 2. 客户端构建 DPoP 证明 JWT

DPoP 证明是一个 JWT，具有以下 JOSE 头参数：

| 头参数 | 值 |
|---|---|
| `typ` | `dpop+jwt` |
| `alg` | 签名算法，例如 `ES256` |
| `jwk` | 客户端的公钥 |

以及以下声明：

| 声明 | 含义 |
|---|---|
| `iat` | 证明创建时间 |
| `jti` | 唯一证明标识符（防止重放） |
| `htm` | 请求的 HTTP 方法，例如 `GET` |
| `htu` | 目标 HTTP URI，包括查询字符串 |
| `ath` | `Base64url(SHA-256(access_token))` — 仅在调用资源服务器时存在 |
| `nonce` | 可选的服务器签发 nonce |

### 3. 令牌请求与 API 请求

DPoP 用于两种场景：

**令牌请求** — 客户端在向授权服务器的令牌端点发起请求时，在 `DPoP` 头中发送其 DPoP 证明。

```http
POST /token HTTP/1.1
Host: auth.example.com
Content-Type: application/x-www-form-urlencoded
DPoP: <dpop-proof-jwt>

grant_type=authorization_code
&code=...
```

授权服务器验证证明，将签发的令牌绑定到证明的 JWK 指纹，并在令牌响应中返回 `token_type: "DPoP"`。

**资源请求** — 客户端使用 `DPoP` 授权方案和令牌，并附带包含 `ath` 的*全新* DPoP 证明。

```http
GET /reports HTTP/1.1
Host: api.example.com
Authorization: DPoP <access-token>
DPoP: <dpop-proof-jwt-with-ath>
```

### 4. 请求流程图

```text
Client                          Authorization Server                  Resource Server
  |                                     |                                     |
  | POST /token                         |                                     |
  | DPoP: proof(htm=POST, htu=/token)   |                                     |
  |------------------------------------>|                                     |
  |                                     | verify proof signature              |
  |                                     | bind token -> cnf.jkt = JKT(JWK)    |
  | access_token, token_type=DPoP       |                                     |
  |<------------------------------------|                                     |
  |                                     |                                     |
  | GET /reports                        |                                     |
  | Authorization: DPoP <token>         |                                     |
  | DPoP: proof(htm=GET, htu=/reports,  |                                     |
  |             ath=SHA256(token))      |                                     |
  |---------------------------------------------------------------------->    |
  |                                     |                                     | verify:
  |                                     |                                     |  - proof signature
  |                                     |                                     |  - JWK thumbprint == token cnf.jkt
  |                                     |                                     |  - htm/htu match actual request
  |                                     |                                     |  - jti not seen before
  |                                     |                                     |  - iat is fresh
  |                                 200 OK                                     |
  |<----------------------------------------------------------------------    |
```

### 5. 服务端验证清单

合规的资源服务器应当：

1. 检查 `Authorization` 头的认证方案是 `DPoP`，而不是 `Bearer`。
2. 解析 `DPoP` 证明 JWT。
3. 使用 `jwk` 头中的公钥验证证明签名。
4. 拒绝不支持的算法（例如 `none`）。
5. 确认证明的 `jwk` 的 JWK 指纹与令牌的 `cnf.jkt` 匹配。
6. 验证 `htm` 是实际的 HTTP 方法。
7. 验证 `htu` 是实际完整的请求 URL（协议、主机、端口（如适用）、路径、查询字符串）。
8. 如果提供了访问令牌，验证 `ath` 等于该确切令牌字符串的 SHA-256 哈希。
9. 验证 `iat` 在可接受的时效窗口内（通常为 60–300 秒）。
10. 维护已使用 `jti` 值的短期缓存，并拒绝重复值。
11. 如果配置为要求 nonce，验证证明包含当前服务器签发的 nonce。

### 6. Nonce 挑战

许多授权服务器和资源服务器要求证明中包含服务器生成的 `nonce`。这可以防止被盗的证明在长时间内被重放。

如果客户端省略了预期的 nonce，服务器将返回错误和 `DPoP-Nonce` 头：

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json
DPoP-Nonce: R5H6rE8sW

{
  "error": "use_dpop_nonce"
}
```

客户端必须创建**新的**证明，包含该 nonce，然后重试。绝不能重用旧证明。

## 实际示例 — Python 客户端

以下示例使用 `cryptography`、`PyJWT` 和 `requests` 在底层演示该协议。在生产环境中，应优先使用受维护的 OAuth/DCoP 库，而不是手写加密代码。

先决条件：

```bash
pip install cryptography pyjwt requests
```

```python
import base64
import hashlib
import time
import uuid
from typing import Optional

import jwt
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec


def b64url(data: bytes) -> str:
    """Base64url encode without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def public_jwk(private_key: ec.EllipticCurvePrivateKey) -> dict:
    """Convert an EC P-256 public key to a JWK dictionary."""
    numbers = private_key.public_key().public_numbers()
    return {
        "kty": "EC",
        "crv": "P-256",
        "x": b64url(numbers.x.to_bytes(32, "big")),
        "y": b64url(numbers.y.to_bytes(32, "big")),
    }


def dpop_proof(
    private_key: ec.EllipticCurvePrivateKey,
    method: str,
    uri: str,
    access_token: Optional[str] = None,
    nonce: Optional[str] = None,
) -> str:
    """Create a DPoP proof JWT for the given HTTP request."""
    header = {
        "typ": "dpop+jwt",
        "alg": "ES256",
        "jwk": public_jwk(private_key),
    }

    payload = {
        "iat": int(time.time()),
        "jti": uuid.uuid4().hex,
        "htm": method.upper(),
        "htu": uri,
    }

    if access_token is not None:
        token_hash = hashlib.sha256(access_token.encode("utf-8")).digest()
        payload["ath"] = b64url(token_hash)

    if nonce is not None:
        payload["nonce"] = nonce

    return jwt.encode(payload, private_key, algorithm="ES256", headers=header)


def fetch_access_token(
    token_url: str,
    client_id: str,
    client_secret: Optional[str],
    private_key: ec.EllipticCurvePrivateKey,
) -> str:
    """Exchange credentials for an access token using DPoP."""
    data = {"grant_type": "client_credentials"}
    auth = None

    if client_secret:
        auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    else:
        data["client_id"] = client_id

    proof = dpop_proof(private_key, "POST", token_url)
    headers = {"DPoP": proof}

    resp = requests.post(token_url, data=data, headers=headers, auth=auth)

    if resp.status_code == 400 and resp.json().get("error") == "use_dpop_nonce":
        nonce = resp.headers.get("DPoP-Nonce")
        proof = dpop_proof(private_key, "POST", token_url, nonce=nonce)
        resp = requests.post(
            token_url,
            data=data,
            headers={"DPoP": proof},
            auth=auth,
        )

    resp.raise_for_status()
    return resp.json()["access_token"]


def fetch_resource(
    resource_url: str,
    access_token: str,
    private_key: ec.EllipticCurvePrivateKey,
) -> requests.Response:
    """Call a resource server with a DPoP-bound access token."""
    proof = dpop_proof(
        private_key,
        "GET",
        resource_url,
        access_token=access_token,
    )
    headers = {
        "Authorization": f"DPoP {access_token}",
        "DPoP": proof,
    }

    resp = requests.get(resource_url, headers=headers)

    if resp.status_code == 401 and "DPoP-Nonce" in resp.headers:
        nonce = resp.headers["DPoP-Nonce"]
        proof = dpop_proof(
            private_key,
            "GET",
            resource_url,
            access_token=access_token,
            nonce=nonce,
        )
        headers = {
            "Authorization": f"DPoP {access_token}",
            "DPoP": proof,
        }
        resp = requests.get(resource_url, headers=headers)

    return resp
```

用法：

```python
client_private_key = ec.generate_private_key(ec.SECP256R1())

token = fetch_access_token(
    token_url="https://auth.example.com/token",
    client_id="my-public-client",
    client_secret=None,  # public client
    private_key=client_private_key,
)

response = fetch_resource(
    resource_url="https://api.example.com/reports",
    access_token=token,
    private_key=client_private_key,
)

print(response.status_code)
```

此示例中的要点：

- 每个证明都会生成新的 `jti`。
- 令牌请求证明不包含 `ath`。
- 资源请求证明会对确切的访问令牌字符串进行哈希。
- 客户端在会话期间持有私钥。

## 服务端验证示例

资源服务器验证上述证明时，需要从 `jwk` 头重建公钥，然后验证 JWT：

```python
def verify_dpop_proof(
    proof: str,
    method: str,
    uri: str,
    access_token: Optional[str] = None,
) -> dict:
    header = jwt.get_unverified_header(proof)

    if header.get("typ") != "dpop+jwt":
        raise ValueError("Invalid DPoP typ header")

    jwk = header.get("jwk")
    if jwk is None or jwk.get("kty") != "EC" or jwk.get("crv") != "P-256":
        raise ValueError("Unsupported DPoP key")

    x = int.from_bytes(base64.urlsafe_b64decode(jwk["x"] + "=="), "big")
    y = int.from_bytes(base64.urlsafe_b64decode(jwk["y"] + "=="), "big")

    public_key = ec.EllipticCurvePublicNumbers(x, y, ec.SECP256R1()).public_key()
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    claims = jwt.decode(proof, pem, algorithms=["ES256"])

    if claims["htm"] != method.upper():
        raise ValueError("DPoP proof method mismatch")
    if claims["htu"] != uri:
        raise ValueError("DPoP proof URI mismatch")
    if access_token is not None:
        expected_ath = b64url(hashlib.sha256(access_token.encode()).digest())
        if claims.get("ath") != expected_ath:
            raise ValueError("DPoP proof ath mismatch")

    # Additional checks in real code:
    # - Reject duplicate / stale jti
    # - Check iat freshness
    # - Validate nonce against server-issued nonce cache
    # - Verify the proof's JWK thumbprint matches the token's cnf.jkt

    return claims
```

最后一项——将证明 JWK 与令牌绑定的 `cnf` 进行匹配——是 DPoP 的核心。对于不透明访问令牌，资源服务器必须通过令牌内省获取 `cnf`。对于 JWT 访问令牌，`cnf` 通常直接包含在令牌的声明中。

## 权衡与替代方案

### DPoP 与 Bearer 令牌

| 方面 | Bearer 令牌 | DPoP |
|---|---|---|
| 绑定 | 无 | 客户端持有的公钥 |
| 重放被盗令牌 | 容易 | 没有私钥则不可行 |
| 客户端复杂性 | 非常低 | 中等：密钥生成、签名、nonce 处理 |
| 服务器开销 | 最小 | 每个请求进行签名验证 |
| 标准 | RFC 6750 | RFC 9449 |

Bearer 令牌适合低风险的内部 API。当令牌泄露会造成高影响时，DPoP 是合理的选择。

### DPoP 与双向 TLS（mTLS）

| 方面 | mTLS（RFC 8705） | DPoP |
|---|---|---|
| 绑定层 | 传输层 | 应用层 |
| 客户端证书管理 | 繁重（PKI、配置） | 密钥对，更易于部署 |
| 在浏览器 / SPA 中可用 | 困难 | 可与 WebCrypto 配合 |
| 在移动应用中使用 | 困难 | 可以 |
| FAPI 合规性 | 常用 | 越来越常用 |

与 mTLS 证书基础设施相比，DPoP 通常更易于为 Web 和移动公共客户端部署。在证书管理已经很常见的服务器到服务器集成中，mTLS 仍然是强有力的选择。

### DPoP 的局限性

- **私钥窃取是致命的。** DPoP 防护的是令牌窃取，而不是密钥窃取。私钥泄露会使攻击者获得与合法客户端相同的权限。
- **每个请求的签名开销。** 每个 API 请求都需要签名，每个资源服务器请求都需要验证。
- **Nonce 往返。** 如果服务器要求 nonce，则在 nonce 轮换后的第一个请求会多产生一次往返。
- **密钥管理负担。** 客户端必须安全地创建、存储和轮换密钥。丢失密钥意味着需要重新认证。
- **需要端到端支持。** 授权服务器和所有资源服务器都必须理解 DPoP 并遵守 `cnf` 绑定。
- **不能替代 PKCE。** DPoP 无法防止授权码被拦截。公共客户端请使用 PKCE。

## 最佳实践

1. **将 DPoP 与 PKCE 结合使用。** 它们应对不同的威胁。PKCE 保护授权码交换；DPoP 保护产生的令牌。
2. **使用 P-256 / ES256。** 它被广泛支持、快速且安全。除非所有相关方都支持，否则避免使用冷门算法。
3. **为每个用户会话生成新的密钥对。** 不要在应用程序的所有用户之间共享私钥。
4. **安全地存储私钥。** 使用操作系统钥匙串、Android Keystore、iOS Secure Enclave、TPM 或不可导出的 WebCrypto 密钥。
5. **同时绑定刷新令牌。** 使用刷新令牌请求新的访问令牌时，发送 DPoP 证明。如果授权服务器支持发送方约束的刷新令牌，请启用。
6. **故障时关闭（Fail closed）。** 如果服务器在 DPoP 请求后返回 `token_type: "Bearer"`，应将其视为配置错误，而不是自动回退。
7. **绝不要记录 DPoP 证明。** 有效的证明虽然有时效，但如果服务器的 `jti` 缓存很短且攻击者能迅速捕获，它仍然可能被重放。
8. **在生产环境中使用经过审计的库**，而不是自己实现原始协议。许多 OAuth SDK 都提供 DPoP 支持：
   - **Python** — Authlib
   - **JavaScript** — oauth4webapi
   - **Java** — Nimbus OAuth 2.0 SDK / JOSE+JWT
   - **.NET** — IdentityModel
9. **始终使用 HTTPS。** DPoP 不能替代 TLS；它是在请求离开客户端后防止 Bearer 令牌被滥用的额外防御。

## 参考资料

- [RFC 9449 — OAuth 2.0 Demonstrating Proof of Possession (DPoP)](https://www.rfc-editor.org/rfc/rfc9449)
- [RFC 6749 — The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749)
- [RFC 7638 — JSON Web Key (JWK) Thumbprint](https://www.rfc-editor.org/rfc/rfc7638)
- [RFC 8705 — OAuth 2.0 Mutual TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705)
- [RFC 7636 — Proof Key for Code Exchange (PKCE)](https://www.rfc-editor.org/rfc/rfc7636)

## 总结

DPoP 将 OAuth 令牌从 Bearer 凭据转变为发送方约束的凭据。客户端在每个请求中证明自己持有私钥，资源服务器则根据令牌签发时绑定的密钥来验证该证明。它是一种实用的应用层机制，能显著降低令牌窃取造成的损害，尤其适用于公共客户端、移动应用和单页应用。

采用 DPoP 会增加实际的复杂性——密钥处理、nonce、重放缓存和逐请求验证——但对于传输敏感数据的 API 而言，安全性的提升通常值得付出这些成本。