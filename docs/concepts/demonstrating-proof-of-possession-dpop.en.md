---
title: Demonstrating Proof of Possession (DPoP) — Sender-Constraining OAuth Tokens with RFC 9449
description: A developer guide to DPoP, the RFC 9449 mechanism that binds OAuth 2.0 access and refresh tokens to a client-held key pair to prevent token replay and theft.
created: 2026-08-07
tags:
  - oauth2
  - security
  - rfc-9449
  - dpop
  - identity
status: draft
---

# Demonstrating Proof of Possession (DPoP)

## What is DPoP?

**Demonstrating Proof of Possession (DPoP)** is an application-layer OAuth 2.0 extension defined in **RFC 9449**. It *sender-constrains* access tokens and refresh tokens by binding them to a public/private key pair generated and held by the client.

Instead of sending a bare `Authorization: Bearer <token>`, a DPoP-enabled client proves to the resource server that it still holds the private key that was used when the token was issued. Every request carries a short-lived, signed proof JWT in a `DPoP` HTTP header. That proof is cryptographically bound to the exact HTTP method, URL, and access token being used.

Because the access token is no longer “bearer” — anyone who has it can use it — a stolen token is useless without the matching private key.

## Why it matters

Ordinary OAuth 2.0 bearer tokens have a fundamental problem: possession of the token is the only proof of authorization. A token leaked in a server log, referrer header, browser extension, or intercepted after a mobile app is compromised can be replayed by an attacker.

DPoP addresses this by changing the threat model:

- A stolen access token cannot be replayed unless the attacker also steals the client’s private key.
- The access token is bound to a specific key at the authorization server.
- The resource server verifies a cryptographic proof on every API call.
- Refresh tokens can also be sender-constrained, closing the “refresh token theft” gap.

DPoP is often required or recommended in high-security ecosystems such as Open Banking / FAPI-compliant APIs, eHealth platforms, and enterprise identity systems.

## How DPoP works

### 1. The client generates a key pair

The client creates an asymmetric key pair — typically EC P-256 (ES256). The private key stays with the client. The public key is represented as a JSON Web Key (JWK) and included inside the header of every DPoP proof.

The authorization server binds the access token to this public key by storing its **JWK SHA-256 thumbprint** (`jkt`) in the token’s `cnf` claim:

```text
jkt = base64url(SHA-256("<canonical JSON of public JWK>"))
```

### 2. The client builds a DPoP proof JWT

A DPoP proof is a JWT with these JOSE header parameters:

| Header | Value |
|---|---|
| `typ` | `dpop+jwt` |
| `alg` | The signing algorithm, e.g. `ES256` |
| `jwk` | The client’s public key |

And these claims:

| Claim | Meaning |
|---|---|
| `iat` | Time of proof creation |
| `jti` | Unique proof identifier (replay prevention) |
| `htm` | HTTP method of the request, e.g. `GET` |
| `htu` | Target HTTP URI, including query string |
| `ath` | Base64url(SHA-256(access_token)) — present only when calling a resource server |
| `nonce` | Optional server-issued nonce |

### 3. Token requests and API requests

There are two situations where DPoP is used:

**Token request** — The client sends its DPoP proof in a `DPoP` header on the request to the authorization server’s token endpoint.

```http
POST /token HTTP/1.1
Host: auth.example.com
Content-Type: application/x-www-form-urlencoded
DPoP: <dpop-proof-jwt>

grant_type=authorization_code
&code=...
```

The authorization server verifies the proof, binds the issued token to the proof’s JWK thumbprint, and returns `token_type: "DPoP"` in the token response.

**Resource request** — The client uses the token with the `DPoP` authorization scheme and includes a *fresh* DPoP proof containing `ath`.

```http
GET /reports HTTP/1.1
Host: api.example.com
Authorization: DPoP <access-token>
DPoP: <dpop-proof-jwt-with-ath>
```

### 4. Request flow diagram

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

### 5. Server-side verification checklist

A compliant resource server should:

1. Check that the `Authorization` scheme is `DPoP`, not `Bearer`.
2. Parse the `DPoP` proof JWT.
3. Verify the proof signature using the public key in the `jwk` header.
4. Reject unsupported algorithms (e.g., `none`).
5. Confirm the JWK thumbprint of the proof’s `jwk` matches the token’s `cnf.jkt`.
6. Verify `htm` is the actual HTTP method.
7. Verify `htu` is the actual full request URL (scheme, host, port if applicable, path, query).
8. If an access token is presented, verify `ath` equals the SHA-256 hash of that exact token string.
9. Validate `iat` is within an acceptable freshness window (commonly 60–300 seconds).
10. Keep a short-lived cache of used `jti` values and reject duplicates.
11. If configured to require nonces, validate the proof includes a current server-issued nonce.

### 6. Nonce challenges

Many authorization servers and resource servers require a proof to contain a server-generated `nonce`. This prevents a stolen proof from being replayed for a long period.

If the client omits an expected nonce, the server responds with an error and a `DPoP-Nonce` header:

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json
DPoP-Nonce: R5H6rE8sW

{
  "error": "use_dpop_nonce"
}
```

The client must create a **new** proof, include the nonce, and retry. It must not reuse the old proof.

## Real example — Python client

The following example uses `cryptography`, `PyJWT`, and `requests` to demonstrate the protocol at a low level. In production, prefer a maintained OAuth/DCoP library over hand-rolled crypto.

Prerequisites:

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

Usage:

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

Important details in this example:

- A new `jti` is generated for every proof.
- The token request proof has no `ath`.
- The resource request proof hashes the exact access token string.
- The client keeps the private key for the lifetime of the session.

## Server-side verification sketch

A resource server verifying the proof above needs to reconstruct the public key from the `jwk` header and then validate the JWT:

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

That last item — matching the proof JWK to the token’s bound `cnf` — is the heart of DPoP. For opaque access tokens, the resource server must obtain `cnf` through token introspection. For JWT access tokens, `cnf` is often included directly in the token’s claims.

## Trade-offs and alternatives

### DPoP vs. bearer tokens

| Aspect | Bearer token | DPoP |
|---|---|---|
| Binding | None | Public key held by client |
| Replay of stolen token | Easy | Impractical without private key |
| Client complexity | Very low | Medium: key generation, signing, nonce handling |
| Server overhead | Minimal | Signature verification per request |
| Standard | RFC 6750 | RFC 9449 |

Bearer tokens make sense for low-risk, internal APIs. DPoP is justified when a leaked token would have a high impact.

### DPoP vs. mutual TLS (mTLS)

| Aspect | mTLS (RFC 8705) | DPoP |
|---|---|---|
| Binding layer | Transport layer | Application layer |
| Client certificate management | Heavy (PKI, provisioning) | Key pair, easier to deploy |
| Works in browsers / SPAs | Difficult | Works with WebCrypto |
| Works in mobile apps | Hard | Yes |
| FAPI compliance | Often used | Increasingly used |

DPoP is generally easier to deploy for web and mobile public clients than mTLS certificate infrastructure. mTLS remains a strong option for server-to-server integrations where certificate management is already normal.

### Limitations of DPoP

- **Private key theft is fatal.** DPoP protects against token theft, not key theft. A compromised private key gives the attacker the same power as the legitimate client.
- **Per-request signing cost.** Every API request requires a signature and every resource server request requires verification.
- **Nonce round trips.** If a server requires nonces, the first request after a nonce rotation incurs one extra round trip.
- **Key management burden.** Clients must securely create, store, and rotate keys. Losing the key means re-authentication.
- **Requires end-to-end support.** Both the authorization server and every resource server must understand DPoP and honor `cnf` binding.
- **Not a replacement for PKCE.** DPoP does not prevent authorization code interception. Use PKCE for public clients.

## Best practices

1. **Use DPoP together with PKCE.** They address different threats. PKCE protects the authorization code exchange; DPoP protects the resulting tokens.
2. **Use P-256 / ES256.** It is widely supported, fast, and secure. Avoid exotic algorithms unless every party supports them.
3. **Generate a new key pair per user session.** Do not share a private key across all users of an application.
4. **Store the private key securely.** Use the OS keychain, Android Keystore, iOS Secure Enclave, TPM, or a non-exportable WebCrypto key.
5. **Bind refresh tokens too.** Send a DPoP proof when requesting a new access token from a refresh token. If the authorization server supports sender-constrained refresh tokens, use it.
6. **Fail closed.** If the server returns `token_type: "Bearer"` after a DPoP request, treat it as a misconfiguration rather than transparently falling back.
7. **Never log DPoP proofs.** A valid proof is time-limited but still potentially replayable if the server’s `jti` cache is short and the attacker captures it quickly.
8. **Use an audited library** in production rather than implementing the raw protocol. Many OAuth SDKs provide DPoP support:
   - **Python** — Authlib
   - **JavaScript** — oauth4webapi
   - **Java** — Nimbus OAuth 2.0 SDK / JOSE+JWT
   - **.NET** — IdentityModel
9. **Always use HTTPS.** DPoP is not a replacement for TLS; it is an additional defense against bearer-token misuse after a request has left the client.

## References

- [RFC 9449 — OAuth 2.0 Demonstrating Proof of Possession (DPoP)](https://www.rfc-editor.org/rfc/rfc9449)
- [RFC 6749 — The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749)
- [RFC 7638 — JSON Web Key (JWK) Thumbprint](https://www.rfc-editor.org/rfc/rfc7638)
- [RFC 8705 — OAuth 2.0 Mutual TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705)
- [RFC 7636 — Proof Key for Code Exchange (PKCE)](https://www.rfc-editor.org/rfc/rfc7636)

## Summary

DPoP transforms OAuth tokens from bearer credentials into sender-constrained credentials. The client proves possession of a private key on every request, and the resource server verifies that proof against the key bound to the token at issuance. It is a practical, application-layer mechanism that significantly reduces the damage of token theft, especially for public clients, mobile apps, and single-page applications.

Adopting DPoP adds real complexity — key handling, nonces, replay caches, and per-request verification — but for APIs that carry sensitive data, the security improvement is often worth the cost.