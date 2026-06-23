---
title: OAuth 2.1 mit PKCE: Implementierungsleitfaden
description: Eine sichere Authentifizierungsmethode, die OAuth 2.1 mit Proof Key for Code Exchange kombiniert, um Angriffe durch Abfangen von Autorisierungscodes zu verhindern.
created: 2026-06-23
tags:
  - oauth2.1
  - pkce
  - authentication
  - security
  - authorization-code-flow
status: draft
---

# OAuth 2.1 mit PKCE: Implementierungsleitfaden

## Übersicht

OAuth 2.1 ist eine sicherheitsorientierte Konsolidierung des OAuth 2.0-Frameworks (RFC 6749) und seiner zahlreichen Ergänzungen. Es vereinfacht die Kernspezifikation und verschärft gleichzeitig die Sicherheit, indem bisher empfohlene Praktiken **obligatorisch** werden. **Proof Key for Code Exchange (PKCE)**, ursprünglich definiert in RFC 7636 für mobile und native Apps, ist jetzt ein erforderlicher Bestandteil des Authorization Code Flows für **alle** Clients in OAuth 2.1.

Dieser Leitfaden behandelt die Begründung, Implementierungsschritte, wichtigsten Funktionen und Migrationsstrategien für die Einführung von OAuth 2.1 mit PKCE in modernen Anwendungen.

---

## Geschichte & Entwicklung

| Jahr | Ereignis | Auswirkung |
|------|----------|------------|
| 2012 | OAuth 2.0 (RFC 6749) | Einführung mehrerer Grant-Typen, darunter Implicit- und Password-Grants, die sich später als unsicher erwiesen. |
| 2015 | PKCE (RFC 7636) | Entwickelt, um Angriffe durch Abfangen von Autorisierungscodes zu verhindern, hauptsächlich für öffentliche Clients. |
| 2020 | OAuth Security BCP (RFC 9700) | Offizielle Abkündigung von Implicit- und Password-Grants; PKCE für alle öffentlichen Clients im Authorization Code Flow vorgeschrieben. |
| 2023+ | OAuth 2.1 | Konsolidiert die BCP-Empfehlungen in einer einzigen Kernspezifikation, macht PKCE für **alle** Clients obligatorisch und entfernt unsichere Grants vollständig. |

---

## Warum OAuth 2.1 + PKCE wichtig ist

OAuth 2.1 eliminiert ganze Kategorien von Angriffen durch Design statt durch Konfiguration:

- **Autorisierungscode-Abfangen (Authorization Code Interception)** – PKCE stellt sicher, dass die Partei, die den Autorisierungscode austauscht, dieselbe ist, die ihn angefordert hat, selbst wenn der Code abgefangen wird.
- **Mix-Up-Angriffe** – Strikter Abgleich der Redirect-URIs verhindert, dass Angreifer ihre eigenen Weiterleitungen unterschieben.
- **CSRF auf den Code** – Der `code_verifier` fungiert als sicheres Nonce, das nicht erraten werden kann.
- **Entfernung unsicherer Abläufe** – Implicit Grant und Resource Owner Password Grant werden entfernt, wodurch gängige Angriffsvektoren geschlossen werden.

**Produktionsumgebungen** wie MCP-Server (z. B. Azure Container Apps) erfordern jetzt OAuth 2.1 + PKCE als Standard-Authentifizierungsmethode.

---

## Hauptmerkmale von OAuth 2.1

### 1. Obligatorisches PKCE

Der Authorization Code Flow **muss** eine `code_challenge` und einen `code_verifier` enthalten. Auch vertrauliche Clients (confidential clients) mit einem `client_secret` profitieren von einer mehrstufigen Sicherheit (defense-in-depth).

### 2. Entfernung von Implicit- und Password-Grants

Nur noch die Authorization Code-, Client Credentials- und Refresh Token-Grants bleiben erhalten. Alle anderen Grants sind veraltet.

### 3. Strenge Redirect-URI-Validierung

Redirect-URIs müssen mittels exaktem Zeichenfolgenvergleich (exact string matching) geprüft werden. Platzhalter oder Mustererkennung sind nicht erlaubt.

### 4. Rotation von Refresh-Tokens

Refresh-Tokens sollten einmal verwendet werden. Bei erneuter Verwendung eines Refresh-Tokens wird es automatisch widerrufen, was auf eine Kompromittierung hinweist.

### 5. Sender-gebundene Zugriffstokens (Sender-Constrained Access Tokens)

Tokens sollten über mTLS (Mutual TLS) oder DPoP (Demonstration of Proof-of-Possession) an den Client gebunden werden, um einfache Inhaber-Tokens (bearer tokens) nach Möglichkeit zu ersetzen.

---

## Implementierungsablauf (Schritt für Schritt)

### 1. Client-Vorbereitung: PKCE-Parameter generieren

Der Client muss einen kryptographisch zufälligen `code_verifier` generieren und dessen SHA-256-Hash als `code_challenge` berechnen.

**Beispiel mit Node.js (erfordert Node 15+)**

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

**Ausgabe (maskiert):**
```json
{
  "codeVerifier": "fdb8...d2a9",
  "codeChallenge": "EbZ6...7Qxw"
}
```

### 2. Autorisierungsanfrage

Leiten Sie den Benutzer mit den folgenden Parametern zum `/authorize`-Endpunkt des Autorisierungsservers weiter:

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

- `code_challenge_method` **muss** `S256` sein. Die Methode `plain` ist nicht zulässig.

### 3. Autorisierungscode empfangen

Nach der Benutzerauthentifizierung und -einwilligung leitet der Autorisierungsserver zur `redirect_uri` mit einem `?code=AUTHORIZATION_CODE` weiter.

```
GET /callback?code=AUTHORIZATION_CODE&state=OPAQUE_STATE_VALUE
```

Validieren Sie den `state`-Parameter, um CSRF-Angriffe zu verhindern.

### 4. Tokenanfrage (Backchannel)

Der Client sendet eine POST-Anfrage an den `/token`-Endpunkt mit dem `code_verifier`.

**Beispiel mit `oauth4webapi` (empfohlen für OAuth 2.1)**

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

**Curl-Darstellung:**

```bash
curl -X POST https://authorization-server.com/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=AUTHORIZATION_CODE" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "redirect_uri=https://yourapp.com/callback" \
  -d "code_verifier=fdb8...d2a9"
```

### 5. Server-Validierung

Der Token-Endpunkt führt folgende Prüfung durch:

```
HASH(code_verifier) == code_challenge
```

Stimmt der Hash überein, ist der Code gültig. Andernfalls schlägt die Anfrage fehl.

### 6. Tokenantwort

Eine erfolgreiche Antwort enthält `access_token`, `refresh_token` (falls `offline_access` angefordert wurde) und optional `id_token`.

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

## Bibliotheksunterstützung

### Serverseitig (Autorisierungsserver)

| Bibliothek / Plattform | OAuth 2.1-Unterstützung |
|------------------------|--------------------------|
| Keycloak               | Ja (PKCE standardmäßig obligatorisch) |
| Entra ID (Azure AD)    | Ja (Authorization Code mit PKCE) |
| Auth0                  | Ja (erfordert Konfiguration) |
| Okta                   | Ja |
| Curity                 | Ja |
| Spring Security 6+     | Ja (`oauth2Client` mit PKCE) |

### Clientseitig (Anwendung)

| Sprache   | Bibliothek | Anmerkungen |
|-----------|------------|-------------|
| Node.js   | [`oauth4webapi`](https://github.com/panva/oauth4webapi) | Autorenspezifisch, OAuth 2.1 bereit |
| Python    | [`Authlib`](https://authlib.org/) | Unterstützt PKCE und OAuth 2.1-Muster |
| Java      | Spring Security 6+ | Integrierter `NimbusJwtDecoder` mit PKCE |
| Mobil     | AppAuth (Android/iOS) | Native PKCE-Unterstützung |
| Web SPA   | BFF-Muster oder Web Workers | Kein direktes PKCE im Browser, Backend-for-Frontend verwenden |

---

## Migration von OAuth 2.0

### Checkliste

1. **Ersetzen Sie den Implicit Grant** durch Authorization Code + PKCE.
2. **Ersetzen Sie den Password Grant** durch Authorization Code + PKCE oder Client Credentials (für Maschine-zu-Maschine).
3. **Erzwingen Sie PKCE** für jeden Authorization Code-Austausch.
4. **Aktivieren Sie die Rotation von Refresh-Tokens** (einmalige Verwendung).
5. **Aktualisieren Sie den Redirect-URI-Vergleich** auf exakten Zeichenfolgenvergleich.
6. **Wechseln Sie zur S256-Methode**, falls zuvor `plain` verwendet wurde.

### Beispiel: Migration eines Legacy-Authorization-Code-Flows

**Vorher (OAuth 2.0 – optionales PKCE)**

```
Schritt 1: client_id + redirect_uri → Code erhalten
Schritt 2: code + client_secret → Token erhalten
```

**Nachher (OAuth 2.1 – obligatorisches PKCE)**

```
Schritt 1: client_id + redirect_uri + code_challenge (S256) → Code erhalten
Schritt 2: code + code_verifier → Token erhalten
```

---

## Praxisbeispiel: MCP-Server auf Azure Container Apps

Die Model Context Protocol (MCP)-Spezifikation (Stand 2026-03-15) erfordert OAuth 2.1 + PKCE für die Autorisierung bei der Interaktion mit Agentenservern. Hier ist eine vereinfachte Einrichtung:

1. **PRM (Protected Resource Metadata) definieren** – `.well-known/oauth-authorization-server` bereitstellen
2. **Dynamische Client-Registrierung** (RFC 7591) für Clients implementieren.
3. **Scope-Design** – granulare Scopes pro Ressource definieren (z. B. `files:read`, `compute:execute`).
4. **Token-Validierung** – jede API-Anfrage muss die Signatur und den gebundenen Schlüssel des Zugriffstokens überprüfen.

Beispiel für eine AZ CLI-Konfiguration (Konzept):

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

Der Client (z. B. die VSCode Azure MCP-Erweiterung) führt dann den PKCE-Fluss durch, bevor er MCP-Tools aufruft.

---

## Sicherheitsempfehlungen

- **Verwenden Sie einen State-Parameter** – Binden Sie die Autorisierungsanfrage an die Benutzersitzung.
- **Speichern Sie den code_verifier sicher** – In der Backend-Sitzung oder einem sicheren clientseitigen Speicher (nicht in der URL).
- **Validieren Sie jedes Token** – Überprüfen Sie Signatur, Aussteller, Zielgruppe und Ablauf.
- **Rotieren Sie Refresh-Tokens** – Jede Aktualisierung erzeugt ein neues Token und macht das vorherige ungültig.
- **Implementieren Sie DPoP** – Fügen Sie den `cnf`-Anspruch zu Zugriffstokens hinzu, um die Senderbindung zu unterstützen.
- **Protokollieren Sie die Wiederverwendung von Tokens** – Erkennen Sie potenziellen Tokendiebstahl.

---

## Fehlerbehebung bei häufigen Problemen

| Problem | Wahrscheinliche Ursache | Lösung |
|---------|-------------------------|--------|
| `invalid_grant` beim Tokenaustausch | `code_verifier` stimmt nicht mit `code_challenge` überein | Hashen Sie den Verifier exakt wie bei der Erstellung (gleicher Algorithmus, gleiche Zeichenkodierung) |
| `redirect_uri_mismatch` | URL-Vergleich nicht exakt | Stellen Sie sicher, dass die `redirect_uri` exakt übereinstimmt, einschließlich abschließender Schrägstriche |
| Autorisierungscode abgelaufen | Zeitüberschreitung > 10 Minuten | Wiederholen Sie den gesamten Ablauf |
| Refresh-Token nach Rotation abgelehnt | Token-Wiederverwendung erkannt | Der Client muss alte Refresh-Tokens verwerfen; implementieren Sie die Einmal-Rotation korrekt |

---

## Referenzen

- [OAuth 2.1 Entwurfsspezifikation](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)
- [PKCE RFC 7636](https://datatracker.ietf.org/doc/html/rfc7636)
- [OAuth Security BCP (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [oauth4webapi – Offizielle Implementierung](https://github.com/panva/oauth4webapi)
- [Authlib – OAuth 2.1 für Python](https://authlib.org/)
- [Spring Security 6 OAuth 2.1 Client](https://docs.spring.io/spring-security/reference/servlet/oauth2/client/index.html)

---

## Fazit

Die Einführung von OAuth 2.1 mit PKCE ist nicht nur eine Compliance-Anforderung – es ist eine grundlegende Verbesserung der Sicherheitslage. Durch die obligatorische Verwendung von PKCE, die Entfernung schwacher Abläufe und die Durchsetzung strenger Validierung stellt OAuth 2.1 sicher, dass moderne Anwendungen gegen die häufigsten Autorisierungsangriffe widerstandsfähig sind. Ob Sie nun einen neuen MCP-Server erstellen, alte mobile Apps migrieren oder eine Single-Page-Anwendung härten – diese Spezifikation bietet einen klaren und sicheren Weg nach vorne.