---
title: OAuth 2.1 con PKCE: Guía de implementación
description: Un método de autenticación seguro que combina OAuth 2.1 con Proof Key for Code Exchange para proteger contra ataques de interceptación del código de autorización.
created: 2026-06-23
tags:
  - oauth2.1
  - pkce
  - authentication
  - security
  - authorization-code-flow
status: draft
---

# OAuth 2.1 con PKCE: Guía de implementación

## Descripción general

OAuth 2.1 es una consolidación centrada en la seguridad del marco OAuth 2.0 (RFC 6749) y sus numerosas modificaciones. Simplifica la especificación base al tiempo que endurece la seguridad al hacer que las prácticas previamente recomendadas sean **obligatorias**. **Proof Key for Code Exchange (PKCE)**, definido originalmente en RFC 7636 para aplicaciones móviles y nativas, es ahora un componente requerido del flujo Authorization Code para **todos** los clientes en OAuth 2.1.

Esta guía cubre la justificación, los pasos de implementación, las características clave y las estrategias de migración para adoptar OAuth 2.1 con PKCE en aplicaciones modernas.

---

## Historia y evolución

| Año | Evento | Impacto |
|------|-------|--------|
| 2012 | OAuth 2.0 (RFC 6749) | Introdujo múltiples tipos de concesión, incluidos los flujos Implicit y Password, que luego resultaron inseguros. |
| 2015 | PKCE (RFC 7636) | Creado para prevenir ataques de interceptación del código de autorización, principalmente para clientes públicos. |
| 2020 | OAuth Security BCP (RFC 9700) | Deprecó oficialmente los flujos Implicit y Password; exigió PKCE para todos los clientes públicos que usan el flujo Authorization Code. |
| 2023+ | OAuth 2.1 | Consolida las recomendaciones del BCP en una especificación central única, haciendo obligatorio el PKCE para **todos** los clientes y eliminando por completo los flujos inseguros. |

---

## Por qué es importante OAuth 2.1 + PKCE

OAuth 2.1 elimina categorías enteras de ataques por diseño, no por configuración:

- **Interceptación del código de autorización** – PKCE asegura que la parte que intercambia el código de autorización sea la misma que lo solicitó, incluso si el código es interceptado.
- **Ataques de confusión (Mix-Up)** – La coincidencia estricta de URI de redirección evita que los atacantes sustituyan sus propias redirecciones.
- **CSRF en el código** – El `code_verifier` actúa como un nonce seguro que no se puede adivinar.
- **Eliminación de flujos inseguros** – El flujo Implícito y el flujo de Contraseña se eliminan, cerrando vectores de ataque comunes.

Los despliegues en producción, como los servidores MCP (por ejemplo, Azure Container Apps), ahora requieren OAuth 2.1 + PKCE como método de autenticación estándar.

---

## Características clave de OAuth 2.1

### 1. PKCE obligatorio

El flujo Authorization Code **debe** incluir un `code_challenge` y un `code_verifier`. Incluso los clientes confidenciales con un `client_secret` se benefician de la defensa en profundidad.

### 2. Eliminación de los flujos Implicit y Password

Solo permanecen los flujos Authorization Code, Client Credentials y Refresh Token. Todos los demás flujos están deprecados.

### 3. Validación estricta de URI de redirección

Las URI de redirección deben compararse mediante coincidencia exacta de cadenas. No se permiten comodines ni coincidencia de patrones.

### 4. Rotación del Refresh Token

Los refresh tokens deben ser de un solo uso. Si un refresh token se reutiliza, se revoca automáticamente, lo que señala un compromiso.

### 5. Sender-Constrained Access Tokens

Los tokens deben estar vinculados al cliente mediante mTLS (Mutual TLS) o DPoP (Demonstration of Proof-of-Possession), reemplazando los tokens bearer simples cuando sea posible.

---

## Flujo de implementación (paso a paso)

### 1. Preparación del cliente: Generar parámetros PKCE

El cliente debe generar un `code_verifier` criptográficamente aleatorio y calcular su hash SHA-256 como `code_challenge`.

**Ejemplo usando Node.js (requiere Node 15+)**

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

**Salida (enmascarada):**
```json
{
  "codeVerifier": "fdb8...d2a9",
  "codeChallenge": "EbZ6...7Qxw"
}
```

### 2. Solicitud de autorización

Redirija al usuario al punto final `/authorize` del servidor de autorización con los siguientes parámetros:

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

- `code_challenge_method` **debe** ser `S256`. El método `plain` no está permitido.

### 3. Recibir código de autorización

Después de la autenticación y el consentimiento del usuario, el servidor de autorización redirige a la `redirect_uri` con un `?code=AUTHORIZATION_CODE`.

```
GET /callback?code=AUTHORIZATION_CODE&state=OPAQUE_STATE_VALUE
```

Valide el parámetro `state` para prevenir ataques CSRF.

### 4. Solicitud de token (Backchannel)

El cliente envía una solicitud POST al punto final `/token` con el `code_verifier`.

**Ejemplo usando `oauth4webapi` (recomendado para OAuth 2.1)**

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

**Representación con curl:**

```bash
curl -X POST https://authorization-server.com/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=AUTHORIZATION_CODE" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "redirect_uri=https://yourapp.com/callback" \
  -d "code_verifier=fdb8...d2a9"
```

### 5. Validación del servidor

El punto final del token realiza:

```
HASH(code_verifier) == code_challenge
```

Si el hash coincide, el código es válido. De lo contrario, la solicitud falla.

### 6. Respuesta del token

Una respuesta exitosa incluye `access_token`, `refresh_token` (si se solicita `offline_access`) y opcionalmente `id_token`.

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

## Soporte de bibliotecas

### Lado del servidor (servidor de autorización)

| Biblioteca / Plataforma | Soporte OAuth 2.1 |
|-------------------|-------------------|
| Keycloak          | Sí (PKCE obligatorio por defecto) |
| Entra ID (Azure AD) | Sí (Authorization Code con PKCE) |
| Auth0             | Sí (requiere configuración) |
| Okta              | Sí |
| Curity            | Sí |
| Spring Security 6+ | Sí (`oauth2Client` con PKCE) |

### Lado del cliente (aplicación)

| Lenguaje | Biblioteca | Notas |
|----------|---------|-------|
| Node.js  | [`oauth4webapi`](https://github.com/panva/oauth4webapi) | Del autor, listo para OAuth 2.1 |
| Python   | [`Authlib`](https://authlib.org/) | Soporta patrones de PKCE y OAuth 2.1 |
| Java     | Spring Security 6+ | `NimbusJwtDecoder` incorporado con PKCE |
| Mobile   | AppAuth (Android/iOS) | Soporte nativo de PKCE |
| Web SPA  | Patrón BFF o Web Workers | Sin PKCE directa en el navegador, usar Backend-for-Frontend |

---

## Migración desde OAuth 2.0

### Lista de verificación

1. **Reemplazar el flujo Implicit** por Authorization Code + PKCE.
2. **Reemplazar el flujo Password** por Authorization Code + PKCE o Client Credentials (para máquina a máquina).
3. **Exigir PKCE** en cada intercambio de Authorization Code.
4. **Habilitar la rotación del Refresh Token** (tokens de un solo uso).
5. **Actualizar la comparación de URI de redirección** a coincidencia exacta de cadenas.
6. **Cambiar al método de desafío S256** si se usaba `plain` anteriormente.

### Ejemplo: Migración de un flujo Authorization Code heredado

**Antes (OAuth 2.0 – PKCE opcional)**

```
step 1: client_id + redirect_uri → get code
step 2: code + client_secret → get token
```

**Después (OAuth 2.1 – PKCE obligatorio)**

```
step 1: client_id + redirect_uri + code_challenge (S256) → get code
step 2: code + code_verifier → get token
```

---

## Ejemplo del mundo real: Servidor MCP en Azure Container Apps

La especificación del Model Context Protocol (MCP) (a partir del 2026-03-15) requiere OAuth 2.1 + PKCE para la autorización al interactuar con servidores de agentes. Aquí hay una configuración resumida:

1. **Definir PRM (Metadatos del Recurso Protegido)** – exponer `.well-known/oauth-authorization-server`
2. **Implementar registro dinámico de clientes** (RFC 7591) para clientes.
3. **Diseño de ámbitos** – definir ámbitos granulares por recurso (por ejemplo, `files:read`, `compute:execute`).
4. **Validación de tokens** – cada solicitud de API debe verificar la firma del token de acceso y la clave vinculada.

Ejemplo de configuración con AZ CLI (concepto):

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

El cliente (por ejemplo, la extensión VSCode Azure MCP) realiza entonces el flujo PKCE antes de invocar las herramientas MCP.

---

## Mejores prácticas de seguridad

- **Usar un parámetro state** – Vincular la solicitud de autorización a la sesión del usuario.
- **Almacenar code_verifier de forma segura** – En la sesión del backend o en un almacenamiento seguro del lado del cliente (no en la URL).
- **Validar cada token** – Verificar firma, emisor, audiencia y caducidad.
- **Rotar refresh tokens** – Cada actualización genera un nuevo token e invalida el anterior.
- **Implementar DPoP** – Agregar la notificación `cnf` a los tokens de acceso para soporte de restricción del emisor.
- **Registrar la reutilización de tokens** – Detectar posible robo de tokens.

---

## Solución de problemas comunes

| Problema | Causa probable | Solución |
|---------|--------------|----------|
| `invalid_grant` durante el intercambio de tokens | `code_verifier` no coincide con `code_challenge` | Volver a aplicar hash al verifier exactamente como durante la creación (mismo algoritmo, misma codificación de caracteres) |
| `redirect_uri_mismatch` | La comparación de URL no es exacta | Asegurarse de que `redirect_uri` coincida exactamente, incluidas las barras diagonales finales |
| El código de autorización expiró | Tiempo de espera > 10 minutos | Reintentar el flujo completo |
| El refresh token es rechazado después de la rotación | Se detectó una reproducción de token | El cliente debe descartar los refresh tokens antiguos; implementar la rotación de un solo uso correctamente |

---

## Referencias

- [OAuth 2.1 Draft Specification](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)
- [PKCE RFC 7636](https://datatracker.ietf.org/doc/html/rfc7636)
- [OAuth Security BCP (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [oauth4webapi – Official Implementation](https://github.com/panva/oauth4webapi)
- [Authlib – OAuth 2.1 for Python](https://authlib.org/)
- [Spring Security 6 OAuth 2.1 Client](https://docs.spring.io/spring-security/reference/servlet/oauth2/client/index.html)

---

## Conclusión

Adoptar OAuth 2.1 con PKCE no es solo un requisito de cumplimiento, sino una mejora fundamental en la postura de seguridad. Al hacer obligatorio PKCE, eliminar flujos débiles y aplicar validación estricta, OAuth 2.1 asegura que las aplicaciones modernas sean resistentes contra los ataques de autorización más comunes. Ya sea que esté construyendo un nuevo servidor MCP, migrando aplicaciones móviles heredadas o reforzando una aplicación de una sola página, esta especificación proporciona un camino claro y seguro hacia adelante.