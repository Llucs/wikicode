---
title: Demostración de la Prueba de Posesión (DPoP) — Tokens OAuth restringidos al remitente con RFC 9449
description: Una guía para desarrolladores sobre DPoP, el mecanismo de RFC 9449 que vincula los tokens de acceso y de actualización de OAuth 2.0 a un par de claves en poder del cliente para evitar la reproducción y el robo de tokens.
created: 2026-08-07
tags:
  - oauth2
  - security
  - rfc-9449
  - dpop
  - identity
status: draft
---

# Demostración de la Prueba de Posesión (DPoP)

## ¿Qué es DPoP?

**Demonstrating Proof of Possession (DPoP)** es una extensión de OAuth 2.0 a nivel de aplicación definida en **RFC 9449**. *Restringe al remitente* los tokens de acceso y los tokens de actualización al vincularlos a un par de claves pública/privada generado y conservado por el cliente.

En lugar de enviar un simple `Authorization: Bearer <token>`, un cliente compatible con DPoP demuestra al servidor de recursos que todavía posee la clave privada que se utilizó cuando se emitió el token. Cada solicitud incluye un JWT de prueba firmado y de corta duración en una cabecera HTTP `DPoP`. Esa prueba está vinculada criptográficamente al método HTTP, la URL y el token de acceso exactos que se están utilizando.

Dado que el token de acceso ya no es "bearer" — cualquiera que lo tenga puede usarlo — un token robado es inútil sin la clave privada correspondiente.

## Por qué es importante

Los tokens bearer ordinarios de OAuth 2.0 tienen un problema fundamental: la posesión del token es la única prueba de autorización. Un token que se filtra en un registro del servidor, en una cabecera referrer, en una extensión del navegador, o que es interceptado después de que una aplicación móvil se vea comprometida, puede ser reproducido por un atacante.

DPoP aborda este problema cambiando el modelo de amenazas:

- Un token de acceso robado no puede reproducirse a menos que el atacante también robe la clave privada del cliente.
- El token de acceso está vinculado a una clave específica en el servidor de autorización.
- El servidor de recursos verifica una prueba criptográfica en cada llamada a la API.
- Los tokens de actualización también pueden restringirse al remitente, cerrando la brecha del "robo del token de actualización".

DPoP se exige o recomienda a menudo en ecosistemas de alta seguridad, como las API compatibles con Open Banking / FAPI, plataformas de salud electrónica y sistemas de identidad empresarial.

## Cómo funciona DPoP

### 1. El cliente genera un par de claves

El cliente crea un par de claves asimétricas — normalmente EC P-256 (ES256). La clave privada permanece en el cliente. La clave pública se representa como una JSON Web Key (JWK) y se incluye dentro de la cabecera de cada prueba DPoP.

El servidor de autorización vincula el token de acceso a esta clave pública almacenando su **huella digital JWK SHA-256** (`jkt`) en la reclamación `cnf` del token:

```text
jkt = base64url(SHA-256("<canonical JSON of public JWK>"))
```

### 2. El cliente construye un JWT de prueba DPoP

Una prueba DPoP es un JWT con estos parámetros de cabecera JOSE:

| Cabecera | Valor |
|---|---|
| `typ` | `dpop+jwt` |
| `alg` | El algoritmo de firma, p. ej. `ES256` |
| `jwk` | La clave pública del cliente |

Y estas reclamaciones:

| Reclamación | Significado |
|---|---|
| `iat` | Hora de creación de la prueba |
| `jti` | Identificador único de la prueba (prevención de reproducción) |
| `htm` | Método HTTP de la solicitud, p. ej. `GET` |
| `htu` | URI HTTP de destino, incluida la cadena de consulta |
| `ath` | Base64url(SHA-256(access_token)) — presente solo al llamar a un servidor de recursos |
| `nonce` | Nonce opcional emitido por el servidor |

### 3. Solicitudes de token y solicitudes de API

Existen dos situaciones en las que se utiliza DPoP:

**Solicitud de token** — El cliente envía su prueba DPoP en una cabecera `DPoP` en la solicitud al endpoint de token del servidor de autorización.

```http
POST /token HTTP/1.1
Host: auth.example.com
Content-Type: application/x-www-form-urlencoded
DPoP: <dpop-proof-jwt>

grant_type=authorization_code
&code=...
```

El servidor de autorización verifica la prueba, vincula el token emitido a la huella digital JWK de la prueba y devuelve `token_type: "DPoP"` en la respuesta del token.

**Solicitud de recurso** — El cliente utiliza el token con el esquema de autorización `DPoP` e incluye una prueba DPoP *nueva* que contiene `ath`.

```http
GET /reports HTTP/1.1
Host: api.example.com
Authorization: DPoP <access-token>
DPoP: <dpop-proof-jwt-with-ath>
```

### 4. Diagrama de flujo de la solicitud

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

### 5. Lista de verificación en el lado del servidor

Un servidor de recursos compatible debe:

1. Comprobar que el esquema `Authorization` es `DPoP`, no `Bearer`.
2. Analizar el JWT de prueba `DPoP`.
3. Verificar la firma de la prueba utilizando la clave pública en la cabecera `jwk`.
4. Rechazar algoritmos no admitidos (p. ej., `none`).
5. Confirmar que la huella digital JWK de la `jwk` de la prueba coincide con el `cnf.jkt` del token.
6. Verificar que `htm` es el método HTTP real.
7. Verificar que `htu` es la URL completa real de la solicitud (esquema, host, puerto si corresponde, ruta, consulta).
8. Si se presenta un token de acceso, verificar que `ath` es igual al hash SHA-256 de la cadena exacta de ese token.
9. Validar que `iat` se encuentra dentro de una ventana de frescura aceptable (comúnmente 60–300 segundos).
10. Mantener una caché de corta duración de los valores `jti` utilizados y rechazar duplicados.
11. Si está configurado para exigir nonces, validar que la prueba incluye un nonce actual emitido por el servidor.

### 6. Desafíos de nonce

Muchos servidores de autorización y servidores de recursos exigen que una prueba contenga un `nonce` generado por el servidor. Esto evita que una prueba robada se reproduzca durante un largo período.

Si el cliente omite un nonce esperado, el servidor responde con un error y una cabecera `DPoP-Nonce`:

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json
DPoP-Nonce: R5H6rE8sW

{
  "error": "use_dpop_nonce"
}
```

El cliente debe crear una prueba **nueva**, incluir el nonce y reintentarlo. No debe reutilizar la prueba antigua.

## Ejemplo real — Cliente Python

El siguiente ejemplo utiliza `cryptography`, `PyJWT` y `requests` para demostrar el protocolo a bajo nivel. En producción, prefiera una biblioteca OAuth/DCoP mantenida antes que implementar criptografía manualmente.

Requisitos previos:

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

Uso:

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

Detalles importantes de este ejemplo:

- Se genera un nuevo `jti` para cada prueba.
- La prueba de la solicitud de token no tiene `ath`.
- La prueba de la solicitud de recurso aplica un hash a la cadena exacta del token de acceso.
- El cliente conserva la clave privada durante toda la sesión.

## Esquema de verificación en el lado del servidor

Un servidor de recursos que verifica la prueba anterior debe reconstruir la clave pública a partir de la cabecera `jwk` y luego validar el JWT:

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

Ese último punto — hacer coincidir la JWK de la prueba con el `cnf` vinculado al token — es el corazón de DPoP. Para tokens de acceso opacos, el servidor de recursos debe obtener `cnf` mediante la introspección del token. Para tokens de acceso JWT, `cnf` suele incluirse directamente en las reclamaciones del token.

## Ventajas e inconvenientes y alternativas

### DPoP frente a tokens bearer

| Aspecto | Token bearer | DPoP |
|---|---|---|
| Vinculación | Ninguna | Clave pública en poder del cliente |
| Reproducción de token robado | Fácil | Impracticable sin la clave privada |
| Complejidad del cliente | Muy baja | Media: generación de claves, firma, manejo de nonces |
| Sobrecarga del servidor | Mínima | Verificación de firma por solicitud |
| Estándar | RFC 6750 | RFC 9449 |

Los tokens bearer tienen sentido para APIs internas de bajo riesgo. DPoP se justifica cuando un token filtrado tendría un alto impacto.

### DPoP frente a TLS mutuo (mTLS)

| Aspecto | mTLS (RFC 8705) | DPoP |
|---|---|---|
| Capa de vinculación | Capa de transporte | Capa de aplicación |
| Gestión de certificados de cliente | Pesada (PKI, aprovisionamiento) | Par de claves, más fácil de implementar |
| Funciona en navegadores / SPA | Difícil | Funciona con WebCrypto |
| Funciona en aplicaciones móviles | Difícil | Sí |
| Cumplimiento FAPI | Usado a menudo | Cada vez más usado |

DPoP es generalmente más fácil de implementar para clientes públicos web y móviles que la infraestructura de certificados mTLS. mTLS sigue siendo una opción sólida para integraciones servidor a servidor donde la gestión de certificados ya es habitual.

### Limitaciones de DPoP

- **El robo de la clave privada es fatal.** DPoP protege contra el robo de tokens, no contra el robo de claves. Una clave privada comprometida otorga al atacante el mismo poder que al cliente legítimo.
- **Coste de firma por solicitud.** Cada solicitud a la API requiere una firma y cada solicitud al servidor de recursos requiere verificación.
- **Viajes de ida y vuelta de nonces.** Si un servidor exige nonces, la primera solicitud después de una rotación de nonce incurre en un viaje de ida y vuelta adicional.
- **Carga de gestión de claves.** Los clientes deben crear, almacenar y rotar claves de forma segura. Perder la clave implica volver a autenticarse.
- **Requiere soporte de extremo a extremo.** Tanto el servidor de autorización como todos los servidores de recursos deben comprender DPoP y respetar la vinculación `cnf`.
- **No sustituye a PKCE.** DPoP no evita la interceptación del código de autorización. Utilice PKCE para clientes públicos.

## Buenas prácticas

1. **Utilice DPoP junto con PKCE.** Abordan amenazas diferentes. PKCE protege el intercambio del código de autorización; DPoP protege los tokens resultantes.
2. **Utilice P-256 / ES256.** Es ampliamente compatible, rápido y seguro. Evite algoritmos exóticos a menos que todas las partes los admitan.
3. **Genere un nuevo par de claves por sesión de usuario.** No comparta una clave privada entre todos los usuarios de una aplicación.
4. **Almacene la clave privada de forma segura.** Utilice el llavero del sistema, Android Keystore, iOS Secure Enclave, TPM o una clave WebCrypto no exportable.
5. **Vincule también los tokens de actualización.** Envíe una prueba DPoP al solicitar un nuevo token de acceso a partir de un token de actualización. Si el servidor de autorización admite tokens de actualización restringidos al remitente, úselo.
6. **Fallo en modo cerrado.** Si el servidor devuelve `token_type: "Bearer"` después de una solicitud DPoP, trátelo como una configuración incorrecta en lugar de degradar silenciosamente el comportamiento.
7. **No registre nunca las pruebas DPoP.** Una prueba válida tiene un límite de tiempo, pero aún podría reproducirse si la caché `jti` del servidor es corta y el atacante la captura rápidamente.
8. **Utilice una biblioteca auditada** en producción en lugar de implementar el protocolo desde cero. Muchos SDK de OAuth ofrecen soporte DPoP:
   - **Python** — Authlib
   - **JavaScript** — oauth4webapi
   - **Java** — Nimbus OAuth 2.0 SDK / JOSE+JWT
   - **.NET** — IdentityModel
9. **Utilice siempre HTTPS.** DPoP no sustituye a TLS; es una defensa adicional contra el uso indebido del token bearer después de que una solicitud haya salido del cliente.

## Referencias

- [RFC 9449 — OAuth 2.0 Demonstrating Proof of Possession (DPoP)](https://www.rfc-editor.org/rfc/rfc9449)
- [RFC 6749 — The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749)
- [RFC 7638 — JSON Web Key (JWK) Thumbprint](https://www.rfc-editor.org/rfc/rfc7638)
- [RFC 8705 — OAuth 2.0 Mutual TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705)
- [RFC 7636 — Proof Key for Code Exchange (PKCE)](https://www.rfc-editor.org/rfc/rfc7636)

## Resumen

DPoP transforma los tokens OAuth de credenciales de portador a credenciales restringidas al remitente. El cliente demuestra la posesión de una clave privada en cada solicitud, y el servidor de recursos verifica esa prueba contra la clave vinculada al token en el momento de su emisión. Es un mecanismo práctico a nivel de aplicación que reduce significativamente el daño del robo de tokens, especialmente para clientes públicos, aplicaciones móviles y aplicaciones de una sola página.

Adoptar DPoP añade una complejidad real — gestión de claves, nonces, cachés de reproducción y verificación por solicitud — pero para las API que manejan datos sensibles, la mejora de seguridad a menudo merece la pena.