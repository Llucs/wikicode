---
title: OAuth 2.1 PKCE with Code Verifier Length Recommendations
description: Guide to implementing OAuth 2.1 PKCE with recommendations on code verifier length to enhance security.
created: 2026-07-12
tags:
  - OAuth
  - PKCE
  - Security
status: draft
---

# OAuth 2.1 PKCE with Code Verifier Length Recommendations

## What is PKCE?

PKCE (Proof Key for Code Exchange) is a security mechanism used in OAuth 2.0 to prevent attackers from obtaining the authorization code. It adds an additional layer of security by requiring a unique, non-reusable key (the code verifier) to be exchanged between the client and the authorization server.

## Key Features of OAuth 2.1 PKCE

- **Code Verifier**: A random string used as a secret between the client and the authorization server.
- **Code Challenge**: A hash of the code verifier, used to prevent network sniffing.
- **Nonce**: A unique value included in the authorization request to ensure the code is used only once.

## History of PKCE

PKCE was introduced as an optional mechanism in OAuth 2.0 to enhance security. However, it became a mandatory part of the OAuth 2.1 specification to ensure a higher level of security, especially for public clients.

## Use Cases for PKCE

- **Public Clients**: Clients that cannot securely store secrets, such as web applications and mobile apps.
- **Hybrid Flow**: Suitable for scenarios where the client needs to exchange the authorization code for an access token.
- **Authorization Code Flow**: Enhances security in scenarios where a client redirects the user to an authorization server.

## Code Verifier Length Recommendations

The length of the code verifier is a critical aspect of PKCE security. The code verifier should be long enough to resist brute-force attacks but short enough to be manageable in client implementations.

### Recommended Lengths

- **Minimum Length**: 43 characters
- **Recommended Length**: 128 characters or more

The longer the code verifier, the more secure it is against brute-force attacks. The minimum length of 43 characters is recommended by the OAuth 2.1 specification to provide a reasonable level of security. However, using a longer code verifier, such as 128 characters, provides a significantly higher security margin.

## Installation and Basic Usage

### Step 1: Generate the Code Verifier

```python
import random
import string

def generate_code_verifier(length=128):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
```

### Step 2: Generate the Code Challenge

```python
import hashlib
import base64

def generate_code_challenge(code_verifier):
    code_challenge = hashlib.sha256(code_verifier.encode()).digest()
    return base64.urlsafe_b64encode(code_challenge).rstrip(b'=').decode()
```

### Step 3: Include PKCE in OAuth 2.0 Flow

1. **Authorization Request**:
   - Include the `code_challenge` and `code_challenge_method` in the authorization request.
   - Example:
     ```http
     GET /authorize?response_type=code&client_id=your_client_id&redirect_uri=https%3A%2F%2Fyourapp.com%2Fcallback&code_challenge=your_code_challenge&code_challenge_method=S256&state=some_state_value&nonce=some_nonce_value
     ```

2. **Token Request**:
   - Include the `code_verifier` in the token request.
   - Example:
     ```http
     POST /token HTTP/1.1
     Host: your_authorization_server.com
     Content-Type: application/x-www-form-urlencoded

     grant_type=authorization_code&code=your_authorization_code&redirect_uri=https%3A%2F%2Fyourapp.com%2Fcallback&code_verifier=your_code_verifier
     ```

## Conclusion

Using PKCE with a sufficiently long code verifier (at least 128 characters) is crucial for enhancing the security of OAuth 2.0 flows, especially in public client scenarios. By following the recommended practices, developers can ensure a higher level of security for their applications.