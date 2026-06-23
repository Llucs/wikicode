---
title: OAuth 2.1 with PKCE: Implementation Guide
description: A secure authentication method that combines OAuth 2.1 with Proof Key for Code Exchange to protect against authorization code interception attacks.
created: 2026-06-23
tags:
  - oauth2.1
  - pkce
  - authentication
  - security
  - authorization-code-flow
status: draft
---

# OAuth 2.1 with PKCE: Implementation Guide

## Overview

OAuth 2.1 is a security-focused consolidation of the OAuth 2.0 framework (RFC 6749) and its numerous amendments. It simplifies the core specification while hardening security by making previously recommended practices **mandatory**. **Proof Key for Code Exchange (PKCE)**, originally defined in RFC 7636 for mobile and native apps, is now a required component of the Authorization Code flow for **all** clients in OAuth 2.1.

This guide covers the rationale, implementation steps, key features, and migration strategies for adopting OAuth 2.1 with PKCE in modern applications.

---

## History & Evolution

| Year | Event | Impact |
|------|-------|--------|
| 2012 | OAuth 2.0 (RFC 6749) | Introduced multiple grant types including Implicit and Password grants, which later proved insecure. |
| 2015 | PKCE (RFC 7636) | Created to prevent authorization code interception attacks, primarily for public clients. |
| 2020 | OAuth Security BCP (RFC 9700) | Officially deprecated Implicit and Password grants; mandated PKCE for all public clients using the Authorization Code flow. |
| 2023+ | OAuth 2.1 | Consolidates BCP recommendations into a single core specification, making PKCE mandatory for **all** clients and removing insecure grants entirely. |

---

## Why OAuth 2.1 + PKCE Matters

OAuth 2.1 eliminates entire categories of attacks by design rather than by configuration:

- **Authorization Code Interception** – PKCE ensures that the party exchanging the authorization code is the same one that requested it, even if the code is intercepted.
- **Mix-Up Attacks** – Strict redirect URI matching prevents attackers from substituting their own redirects.
- **CSRF on the Code** – The `code_verifier` acts as a secure nonce that cannot be guessed.
- **Removal of Insecure Flows** – Implicit Grant and Resource Owner Password Grant are removed, closing common attack vectors.

**Production deployments** like MCP servers (e.g., Azure Container Apps) now require OAuth 2.1 + PKCE as the standard authentication method.

---

## Key Features of OAuth 2.1

### 1. Mandatory PKCE

The Authorization Code flow **must** include a `code_challenge` and `code_verifier`. Even confidential clients with a `client_secret` benefit from defense-in-depth.

### 2. Removal of Implicit and Password Grants

Only the Authorization Code, Client Credentials, and Refresh Token grants remain. All other grants are deprecated.

### 3. Strict Redirect URI Validation

Redirect URIs must be compared using exact string matching. No wildcards or pattern matching allowed.

### 4. Refresh Token Rotation

Refresh tokens should be single-use. If a refresh token is reused, it is automatically revoked, signaling compromise.

### 5. Sender-Constrained Access Tokens

Tokens should be bound to the client via mTLS (Mutual TLS) or DPoP (Demonstration of Proof-of-Possession), replacing simple bearer tokens where possible.

---

## Implementation Flow (Step by Step)

### 1. Client Preparation: Generate PKCE Parameters

The client must generate a cryptographically random `code_verifier` and compute its SHA-256 hash as the `code_challenge`.

**Example using Node.js (requires Node 15+)**

```javascript
import crypto from 'crypto';

// Generate a secure random code_verifier (43-128 characters)
const codeVerifier = crypto.randomBytes(32)
  .toString('base64url')
  .slice(0, 128);

// Compute S256 code_challenge
const codeChallenge = crypto
  .createHash('sha256')
  .update(codeVerifier)
  .digest('base64url');

console.log({ codeVerifier, codeChallenge });
```

**Output (masked):**
```json
{
  "codeVerifier": "fdb8...d2a9",
  "codeChallenge": "EbZ6...7Qxw"
}
```

### 2. Authorization Request

Redirect the user to the authorization server’s `/authorize` endpoint with the following parameters:

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

- `code_challenge_method` **must** be `S256`. The plain method is not allowed.

### 3. Receive Authorization Code

After user authentication and consent, the authorization server redirects to the `redirect_uri` with a `?code=AUTHORIZATION_CODE`.

```
GET /callback?code=AUTHORIZATION_CODE&state=OPAQUE_STATE_VALUE
```

Validate the `state` parameter to prevent CSRF attacks.

### 4. Token Request (Backchannel)

The client sends a POST request to the `/token` endpoint with the `code_verifier`.

**Example using `oauth4webapi` (recommended for OAuth 2.1)**

```javascript
import * as oauth from 'oauth4webapi';

const issuer = new URL('https://authorization-server.com');
const clientId = 'YOUR_CLIENT_ID';
const clientSecret = undefined; // public client

const as = await oauth.discoveryRequest(issuer);
const { authorization_server } = oauth.processDiscoveryResponse(as, {});

const client = {
  client_id: clientId,
  token_endpoint_auth_method: 'none',
};

const authCode = 'AUTHORIZATION_CODE';
const codeVerifier = 'fdb8...d2a9'; // from step 1

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

**Curl representation:**

```bash
curl -X POST https://authorization-server.com/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=AUTHORIZATION_CODE" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "redirect_uri=https://yourapp.com/callback" \
  -d "code_verifier=fdb8...d2a9"
```

### 5. Server Validation

The token endpoint performs:

```
HASH(code_verifier) == code_challenge
```

If the hash matches, the code is valid. Otherwise, the request fails.

### 6. Token Response

Successful response includes `access_token`, `refresh_token` (if offline_access is requested), and optionally `id_token`.

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

## Library Support

### Server-Side (Authorization Server)

| Library / Platform | OAuth 2.1 Support |
|-------------------|-------------------|
| Keycloak          | Yes (PKCE mandatory by default) |
| Entra ID (Azure AD) | Yes (Authorization Code with PKCE) |
| Auth0             | Yes (requires configuration) |
| Okta              | Yes |
| Curity            | Yes |
| Spring Security 6+ | Yes (`oauth2Client` with PKCE) |

### Client-Side (Application)

| Language | Library | Notes |
|----------|---------|-------|
| Node.js  | [`oauth4webapi`](https://github.com/panva/oauth4webapi) | Author-specific, OAuth 2.1 ready |
| Python   | [`Authlib`](https://authlib.org/) | Supports PKCE and OAuth 2.1 patterns |
| Java     | Spring Security 6+ | Built-in `NimbusJwtDecoder` with PKCE |
| Mobile   | AppAuth (Android/iOS) | Native PKCE support |
| Web SPA  | BFF pattern or Web Workers | No direct PKCE in browser, use Backend-for-Frontend |

---

## Migration from OAuth 2.0

### Checklist

1. **Replace Implicit Grant** with Authorization Code + PKCE.
2. **Replace Password Grant** with Authorization Code + PKCE or Client Credentials (for machine-to-machine).
3. **Enforce PKCE** for every Authorization Code exchange.
4. **Enable Refresh Token Rotation** (single-use tokens).
5. **Update Redirect URI comparison** to exact string matching.
6. **Switch to S256** challenge method if previously using `plain`.

### Example: Migrating a Legacy Authorization Code Flow

**Before (OAuth 2.0 – optional PKCE)**

```
step 1: client_id + redirect_uri → get code
step 2: code + client_secret → get token
```

**After (OAuth 2.1 – mandatory PKCE)**

```
step 1: client_id + redirect_uri + code_challenge (S256) → get code
step 2: code + code_verifier → get token
```

---

## Real-World Example: MCP Server on Azure Container Apps

The Model Context Protocol (MCP) spec (as of 2026-03-15) requires OAuth 2.1 + PKCE for authorization when interacting with agent servers. Here is a condensed setup:

1. **Define PRM (Protected Resource Metadata)** – expose `.well-known/oauth-authorization-server`
2. **Implement Dynamic Client Registration** (RFC 7591) for clients.
3. **Scope Design** – define granular scopes per resource (e.g., `files:read`, `compute:execute`).
4. **Token Validation** – every API request must verify the access token’s signature and bound key.

Example AZ CLI configuration (concept):

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

The client (e.g., VSCode Azure MCP extension) then performs the PKCE flow before invoking MCP tools.

---

## Security Best Practices

- **Use a State Parameter** – Bind the authorization request to the user session.
- **Store code_verifier securely** – In backend session or a secure client-side store (not in URL).
- **Validate every token** – Check signature, issuer, audience, and expiry.
- **Rotate refresh tokens** – Each refresh yields a new token and invalidates the previous one.
- **Implement DPoP** – Add `cnf` claim to access tokens for sender-constrained support.
- **Log token reuse** – Detect potential token theft.

---

## Troubleshooting Common Issues

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| `invalid_grant` during token exchange | `code_verifier` does not match `code_challenge` | Re-hash the verifier exactly as during creation (same algorithm, same character encoding) |
| `redirect_uri_mismatch` | URL comparison not exact | Ensure `redirect_uri` matches exactly, including trailing slashes |
| Authorization code expired | Timeout > 10 minutes | Retry the full flow |
| Refresh token rejected after rotation | Token replay detected | The client must discard old refresh tokens; implement single-use rotation correctly |

---

## References

- [OAuth 2.1 Draft Specification](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)
- [PKCE RFC 7636](https://datatracker.ietf.org/doc/html/rfc7636)
- [OAuth Security BCP (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [oauth4webapi – Official Implementation](https://github.com/panva/oauth4webapi)
- [Authlib – OAuth 2.1 for Python](https://authlib.org/)
- [Spring Security 6 OAuth 2.1 Client](https://docs.spring.io/spring-security/reference/servlet/oauth2/client/index.html)

---

## Conclusion

Adopting OAuth 2.1 with PKCE is not just a compliance requirement—it is a fundamental improvement in security posture. By making PKCE mandatory, removing weak flows, and enforcing strict validation, OAuth 2.1 ensures that modern applications are resilient against the most common authorization attacks. Whether you are building a new MCP server, migrating legacy mobile apps, or hardening a single-page application, this specification provides a clear and secure path forward.