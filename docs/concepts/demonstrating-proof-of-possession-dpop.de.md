---
title: Demonstration des Besitznachweises (DPoP) — Sendergebundene OAuth-Tokens mit RFC 9449
description: Ein Entwicklerleitfaden für DPoP, den RFC-9449-Mechanismus, der OAuth-2.0-Access- und Refresh-Tokens an ein vom Client gehaltenes Schlüsselpaar bindet, um Token-Replay und -Diebstahl zu verhindern.
created: 2026-08-07
tags:
  - oauth2
  - security
  - rfc-9449
  - dpop
  - identity
status: draft
---

# Demonstration des Besitznachweises (DPoP)

## Was ist DPoP?

**Demonstration des Besitznachweises (DPoP)** (englisch *Demonstrating Proof of Possession*) ist eine auf Anwendungsebene angesiedelte OAuth-2.0-Erweiterung, die in **RFC 9449** definiert ist. Sie versieht Access- und Refresh-Tokens mit einer Senderbindung (Sender-Constraining), indem sie diese an ein öffentlich/privates Schlüsselpaar bindet, das vom Client erzeugt und gehalten wird.

Anstatt ein nacktes `Authorization: Bearer <token>` zu senden, weist ein DPoP-fähiger Client dem Ressourcenserver nach, dass er noch immer den privaten Schlüssel besitzt, der bei der Ausstellung des Tokens verwendet wurde. Jede Anfrage enthält ein kurzlebiges, signiertes Proof-JWT in einem `DPoP`-HTTP-Header. Dieser Proof ist kryptografisch an die exakte HTTP-Methode, URL und das verwendete Access-Token gebunden.

Da das Access-Token nicht länger ein „Bearer“-Token ist – jeder, der es besitzt, kann es verwenden –, ist ein gestohlenes Token ohne den zugehörigen privaten Schlüssel nutzlos.

## Warum das wichtig ist

Gewöhnliche OAuth-2.0-Bearer-Tokens haben ein grundlegendes Problem: Der Besitz des Tokens ist der einzige Nachweis der Autorisierung. Ein Token, das in einem Server-Log, im Referrer-Header, in einer Browsererweiterung verloren geht oder nach der Kompromittierung einer mobilen App abgefangen wird, kann von einem Angreifer erneut verwendet werden.

DPoP begegnet diesem Problem, indem es das Bedrohungsmodell ändert:

- Ein gestohlenes Access-Token kann nicht erneut verwendet werden, es sei denn, der Angreifer stiehlt auch den privaten Schlüssel des Clients.
- Das Access-Token ist beim Autorisierungsserver an einen bestimmten Schlüssel gebunden.
- Der Ressourcenserver verifiziert bei jedem API-Aufruf einen kryptografischen Nachweis.
- Auch Refresh-Tokens können sendergebunden werden, wodurch die Lücke bei „Refresh-Token-Diebstahl“ geschlossen wird.

DPoP wird in Hochsicherheits-Ökosystemen wie Open-Banking-/FAPI-konformen APIs, E-Health-Plattformen und Enterprise-Identity-Systemen häufig gefordert oder empfohlen.

## Wie DPoP funktioniert

### 1. Der Client erzeugt ein Schlüsselpaar

Der Client erzeugt ein asymmetrisches Schlüsselpaar – typischerweise EC P-256 (ES256). Der private Schlüssel verbleibt beim Client. Der öffentliche Schlüssel wird als JSON Web Key (JWK) repräsentiert und im Header jedes DPoP-Proofs mitgeführt.

Der Autorisierungsserver bindet das Access-Token an diesen öffentlichen Schlüssel, indem er dessen **JWK-SHA-256-Thumbprint** (`jkt`) im `cnf`-Claim des Tokens speichert:

```text
jkt = base64url(SHA-256("<canonical JSON of public JWK>"))
```

### 2. Der Client erstellt ein DPoP-Proof-JWT

Ein DPoP-Proof ist ein JWT mit folgenden JOSE-Header-Parametern:

| Header | Wert |
|---|---|
| `typ` | `dpop+jwt` |
| `alg` | Der Signaturalgorithmus, z. B. `ES256` |
| `jwk` | Der öffentliche Schlüssel des Clients |

Und diesen Claims:

| Claim | Bedeutung |
|---|---|
| `iat` | Zeitpunkt der Erstellung des Proofs |
| `jti` | Eindeutige Proof-Kennung (Replay-Schutz) |
| `htm` | HTTP-Methode der Anfrage, z. B. `GET` |
| `htu` | Ziel-HTTP-URI, einschließlich Query-String |
| `ath` | Base64url(SHA-256(access_token)) – nur beim Aufruf eines Ressourcenservers vorhanden |
| `nonce` | Optionaler, vom Server ausgestellter Nonce |

### 3. Tokenanfragen und API-Anfragen

Es gibt zwei Situationen, in denen DPoP verwendet wird:

**Tokenanfrage** – Der Client sendet seinen DPoP-Proof im `DPoP`-Header mit der Anfrage an den Token-Endpunkt des Autorisierungsservers.

```http
POST /token HTTP/1.1
Host: auth.example.com
Content-Type: application/x-www-form-urlencoded
DPoP: <dpop-proof-jwt>

grant_type=authorization_code
&code=...
```

Der Autorisierungsserver verifiziert den Proof, bindet das ausgestellte Token an den JWK-Thumbprint des Proofs und gibt in der Token-Antwort `token_type: "DPoP"` zurück.

**Ressourcenanfrage** – Der Client verwendet das Token mit dem Autorisierungsschema `DPoP` und fügt einen *neuen* DPoP-Proof mit `ath` hinzu.

```http
GET /reports HTTP/1.1
Host: api.example.com
Authorization: DPoP <access-token>
DPoP: <dpop-proof-jwt-with-ath>
```

### 4. Ablaufdiagramm

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

### 5. Checkliste für die serverseitige Verifizierung

Ein konformer Ressourcenserver sollte:

1. Prüfen, dass das Autorisierungsschema `DPoP` und nicht `Bearer` ist.
2. Das DPoP-Proof-JWT parsen.
3. Die Proof-Signatur mit dem öffentlichen Schlüssel aus dem `jwk`-Header verifizieren.
4. Nicht unterstützte Algorithmen ablehnen (z. B. `none`).
5. Bestätigen, dass der JWK-Thumbprint des `jwk` des Proofs mit `cnf.jkt` des Tokens übereinstimmt.
6. Prüfen, dass `htm` der tatsächlichen HTTP-Methode entspricht.
7. Prüfen, dass `htu` der tatsächlichen vollständigen Anfrage-URL entspricht (Schema, Host, Port falls zutreffend, Pfad, Query).
8. Falls ein Access-Token vorgelegt wird, prüfen, dass `ath` dem SHA-256-Hash dieser exakten Token-Zeichenkette entspricht.
9. Validieren, dass `iat` innerhalb eines akzeptablen Aktualitätsfensters liegt (üblicherweise 60–300 Sekunden).
10. Einen kurzlebigen Cache verwendeter `jti`-Werte führen und Duplikate ablehnen.
11. Falls die Konfiguration Nonces erfordert, prüfen, dass der Proof einen aktuellen, vom Server ausgestellten Nonce enthält.

### 6. Nonce-Challenges

Viele Autorisierungs- und Ressourcenserver verlangen, dass ein Proof einen vom Server erzeugten `nonce` enthält. Dies verhindert, dass ein gestohlener Proof über einen längeren Zeitraum erneut verwendet werden kann.

Wenn der Client einen erwarteten Nonce weglässt, antwortet der Server mit einem Fehler und einem `DPoP-Nonce`-Header:

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json
DPoP-Nonce: R5H6rE8sW

{
  "error": "use_dpop_nonce"
}
```

Der Client muss einen **neuen** Proof erstellen, den Nonce einfügen und es erneut versuchen. Er darf den alten Proof nicht wiederverwenden.

## Praxisbeispiel – Python-Client

Das folgende Beispiel verwendet `cryptography`, `PyJWT` und `requests`, um das Protokoll auf niedriger Ebene zu demonstrieren. In Produktionsumgebungen sollten Sie eine gewartete OAuth-/DPoP-Bibliothek bevorzugen, anstatt Kryptografie selbst zu implementieren.

Voraussetzungen:

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

Verwendung:

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

Wichtige Details in diesem Beispiel:

- Für jeden Proof wird ein neues `jti` erzeugt.
- Der Proof der Tokenanfrage enthält kein `ath`.
- Der Proof der Ressourcenanfrage hasht die exakte Access-Token-Zeichenkette.
- Der Client bewahrt den privaten Schlüssel für die gesamte Sitzung auf.

## Skizze der serverseitigen Verifizierung

Ein Ressourcenserver, der den obigen Proof verifiziert, muss den öffentlichen Schlüssel aus dem `jwk`-Header rekonstruieren und anschließend das JWT validieren:

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

Der letzte Punkt – die Übereinstimmung des Proof-JWK mit dem gebundenen `cnf` des Tokens – ist das Herzstück von DPoP. Bei opaken Access-Tokens muss der Ressourcenserver `cnf` über die Token-Introspektion ermitteln. Bei JWT-Access-Tokens ist `cnf` häufig direkt in den Claims des Tokens enthalten.

## Abwägungen und Alternativen

### DPoP im Vergleich zu Bearer-Tokens

| Aspekt | Bearer-Token | DPoP |
|---|---|---|
| Bindung | Keine | Öffentlicher Schlüssel, der vom Client gehalten wird |
| Wiederverwendung gestohlener Token | Einfach | Ohne privaten Schlüssel unpraktikabel |
| Client-Komplexität | Sehr gering | Mittel: Schlüsselerzeugung, Signatur, Nonce-Handling |
| Server-Overhead | Minimal | Signaturverifikation pro Anfrage |
| Standard | RFC 6750 | RFC 9449 |

Bearer-Tokens sind für risikoarme, interne APIs sinnvoll. DPoP ist gerechtfertigt, wenn ein geleaktes Token erhebliche Auswirkungen hätte.

### DPoP im Vergleich zu Mutual TLS (mTLS)

| Aspekt | mTLS (RFC 8705) | DPoP |
|---|---|---|
| Bindungsebene | Transportschicht | Anwendungsschicht |
| Client-Zertifikatsverwaltung | Aufwendig (PKI, Provisioning) | Schlüsselpaar, einfacher zu deployen |
| Funktioniert im Browser / in SPAs | Schwierig | Funktioniert mit WebCrypto |
| Funktioniert in mobilen Apps | Schwer | Ja |
| FAPI-Konformität | Häufig verwendet | Zunehmend verwendet |

DPoP ist für Web- und mobile öffentliche Clients in der Regel einfacher zu deployen als eine mTLS-Zertifikatsinfrastruktur. mTLS bleibt eine starke Option für Server-zu-Server-Integrationen, in denen Zertifikatsverwaltung bereits üblich ist.

### Einschränkungen von DPoP

- **Der Diebstahl des privaten Schlüssels ist fatal.** DPoP schützt vor Token-Diebstahl, nicht vor Schlüsseldiebstahl. Ein kompromittierter privater Schlüssel verleiht dem Angreifer dieselben Rechte wie dem legitimen Client.
- **Kosten für die Signatur pro Anfrage.** Jede API-Anfrage erfordert eine Signatur, und jede Ressourcenserver-Anfrage erfordert eine Verifizierung.
- **Nonce-Roundtrips.** Wenn ein Server Nonces verlangt, verursacht die erste Anfrage nach einer Nonce-Rotation einen zusätzlichen Roundtrip.
- **Schlüsselverwaltungsaufwand.** Clients müssen Schlüssel sicher erzeugen, speichern und rotieren. Ein verlorener Schlüssel bedeutet eine erneute Authentifizierung.
- **Erfordert End-to-End-Unterstützung.** Sowohl der Autorisierungsserver als auch jeder Ressourcenserver müssen DPoP verstehen und die `cnf`-Bindung beachten.
- **Kein Ersatz für PKCE.** DPoP verhindert das Abfangen von Autorisierungscodes nicht. Verwenden Sie PKCE für öffentliche Clients.

## Bewährte Vorgehensweisen

1. **Setzen Sie DPoP zusammen mit PKCE ein.** Sie adressieren unterschiedliche Bedrohungen. PKCE schützt den Austausch des Autorisierungscodes; DPoP schützt die resultierenden Token.
2. **Verwenden Sie P-256 / ES256.** Es ist weit verbreitet, schnell und sicher. Vermeiden Sie exotische Algorithmen, sofern nicht alle Parteien sie unterstützen.
3. **Erzeugen Sie ein neues Schlüsselpaar pro Benutzersitzung.** Teilen Sie einen privaten Schlüssel nicht über alle Benutzer einer Anwendung.
4. **Speichern Sie den privaten Schlüssel sicher.** Verwenden Sie den OS-Keychain, Android Keystore, iOS Secure Enclave, TPM oder einen nicht exportierbaren WebCrypto-Schlüssel.
5. **Binden Sie auch Refresh-Tokens.** Senden Sie einen DPoP-Proof, wenn Sie mit einem Refresh-Token ein neues Access-Token anfordern. Wenn der Autorisierungsserver sendergebundene Refresh-Tokens unterstützt, nutzen Sie dies.
6. **Fail closed.** Wenn der Server nach einer DPoP-Anfrage `token_type: "Bearer"` zurückgibt, behandeln Sie dies als Fehlkonfiguration, anstatt stillschweigend auf Bearer zurückzufallen.
7. **Protokollieren Sie niemals DPoP-Proofs.** Ein gültiger Proof ist zeitlich begrenzt, aber unter Umständen dennoch wiederverwendbar, wenn der `jti`-Cache des Servers kurz ist und der Angreifer ihn schnell erfasst.
8. **Verwenden Sie in Produktion eine geprüfte Bibliothek**, anstatt das Protokoll selbst zu implementieren. Viele OAuth-SDKs bieten DPoP-Unterstützung:
   - **Python** – Authlib
   - **JavaScript** – oauth4webapi
   - **Java** – Nimbus OAuth 2.0 SDK / JOSE+JWT
   - **.NET** – IdentityModel
9. **Verwenden Sie immer HTTPS.** DPoP ist kein Ersatz für TLS; es ist eine zusätzliche Verteidigung gegen den Missbrauch von Bearer-Tokens, nachdem eine Anfrage den Client verlassen hat.

## Referenzen

- [RFC 9449 — OAuth 2.0 Demonstrating Proof of Possession (DPoP)](https://www.rfc-editor.org/rfc/rfc9449)
- [RFC 6749 — The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749)
- [RFC 7638 — JSON Web Key (JWK) Thumbprint](https://www.rfc-editor.org/rfc/rfc7638)
- [RFC 8705 — OAuth 2.0 Mutual TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705)
- [RFC 7636 — Proof Key for Code Exchange (PKCE)](https://www.rfc-editor.org/rfc/rfc7636)

## Zusammenfassung

DPoP verwandelt OAuth-Tokens von Bearer-Zugangsdaten in sendergebundene Zugangsdaten. Der Client weist bei jeder Anfrage den Besitz eines privaten Schlüssels nach, und der Ressourcenserver prüft diesen Nachweis gegen den Schlüssel, der dem Token bei der Ausstellung zugeordnet wurde. Es ist ein praktischer Mechanismus auf Anwendungsebene, der den Schaden durch Token-Diebstahl erheblich reduziert – insbesondere für öffentliche Clients, mobile Apps und Single-Page-Anwendungen.

Die Einführung von DPoP erhöht die Komplexität erheblich – Schlüsselverwaltung, Nonces, Replay-Caches und Verifikation pro Anfrage – aber für APIs, die sensible Daten übertragen, ist die Sicherheitsverbesserung den Aufwand oft wert.