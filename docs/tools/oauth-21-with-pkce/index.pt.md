---
title: OAuth 2.1 com PKCE: Guia de Implementação
description: Um método de autenticação seguro que combina OAuth 2.1 com Proof Key for Code Exchange para proteger contra ataques de interceptação de código de autorização.
created: 2026-06-23
tags:
  - oauth2.1
  - pkce
  - authentication
  - security
  - authorization-code-flow
status: draft
---

# OAuth 2.1 com PKCE: Guia de Implementação

## Visão Geral

O OAuth 2.1 é uma consolidação focada em segurança do framework OAuth 2.0 (RFC 6749) e suas inúmeras emendas. Ele simplifica a especificação principal enquanto endurece a segurança tornando práticas anteriormente recomendadas **obrigatórias**. **Proof Key for Code Exchange (PKCE)**, originalmente definida na RFC 7636 para aplicativos móveis e nativos, é agora um componente obrigatório do fluxo de Código de Autorização para **todos** os clientes no OAuth 2.1.

Este guia aborda a lógica, etapas de implementação, principais recursos e estratégias de migração para adotar o OAuth 2.1 com PKCE em aplicações modernas.

---

## História & Evolução

| Ano | Evento | Impacto |
|-----|--------|---------|
| 2012 | OAuth 2.0 (RFC 6749) | Introduziu vários tipos de concessão, incluindo os grants Implícito e de Senha, que posteriormente se mostraram inseguros. |
| 2015 | PKCE (RFC 7636) | Criado para prevenir ataques de interceptação de código de autorização, principalmente para clientes públicos. |
| 2020 | OAuth Security BCP (RFC 9700) | Depreciou oficialmente os grants Implícito e de Senha; tornou o PKCE obrigatório para todos os clientes públicos que usam o fluxo de Código de Autorização. |
| 2023+ | OAuth 2.1 | Consolida as recomendações do BCP em uma única especificação principal, tornando o PKCE obrigatório para **todos** os clientes e removendo completamente os grants inseguros. |

---

## Por que o OAuth 2.1 + PKCE é Importante

O OAuth 2.1 elimina categorias inteiras de ataques por design, em vez de por configuração:

- **Interceptação de Código de Autorização** – O PKCE garante que a parte que troca o código de autorização seja a mesma que o solicitou, mesmo que o código seja interceptado.
- **Ataques de Mix-Up** – A correspondência estrita de URI de redirecionamento impede que atacantes substituam seus próprios redirecionamentos.
- **CSRF no Código** – O `code_verifier` atua como um nonce seguro que não pode ser adivinhado.
- **Remoção de Fluxos Inseguros** – O Grant Implícito e o Grant de Senha do Proprietário do Recurso são removidos, fechando vetores de ataque comuns.

**Implantações de produção** como servidores MCP (ex: Azure Container Apps) agora exigem OAuth 2.1 + PKCE como método de autenticação padrão.

---

## Principais Recursos do OAuth 2.1

### 1. PKCE Obrigatório

O fluxo de Código de Autorização **deve** incluir um `code_challenge` e `code_verifier`. Mesmo clientes confidenciais com um `client_secret` se beneficiam da defesa em profundidade.

### 2. Remoção dos Grants Implícito e de Senha

Apenas os grants de Código de Autorização, Credenciais de Cliente e Token de Atualização permanecem. Todos os outros grants estão obsoletos.

### 3. Validação Estrita de URI de Redirecionamento

As URIs de redirecionamento devem ser comparadas usando correspondência exata de strings. Nenhum curinga ou correspondência de padrão é permitido.

### 4. Rotação do Token de Atualização

Os tokens de atualização devem ser de uso único. Se um token de atualização for reutilizado, ele é automaticamente revogado, sinalizando comprometimento.

### 5. Tokens de Acesso Restritos ao Remetente

Os tokens devem ser vinculados ao cliente via mTLS (Mutual TLS) ou DPoP (Demonstration of Proof-of-Possession), substituindo tokens de portador simples quando possível.

---

## Fluxo de Implementação (Passo a Passo)

### 1. Preparação do Cliente: Gerar Parâmetros PKCE

O cliente deve gerar um `code_verifier` criptograficamente aleatório e calcular seu hash SHA-256 como o `code_challenge`.

**Exemplo usando Node.js (requer Node 15+)**

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

**Saída (oculta):**
```json
{
  "codeVerifier": "fdb8...d2a9",
  "codeChallenge": "EbZ6...7Qxw"
}
```

### 2. Solicitação de Autorização

Redirecione o usuário para o endpoint `/authorize` do servidor de autorização com os seguintes parâmetros:

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

- `code_challenge_method` **deve** ser `S256`. O método `plain` não é permitido.

### 3. Receber Código de Autorização

Após a autenticação e consentimento do usuário, o servidor de autorização redireciona para o `redirect_uri` com um `?code=AUTHORIZATION_CODE`.

```
GET /callback?code=AUTHORIZATION_CODE&state=OPAQUE_STATE_VALUE
```

Valide o parâmetro `state` para prevenir ataques CSRF.

### 4. Solicitação de Token (Backchannel)

O cliente envia uma requisição POST para o endpoint `/token` com o `code_verifier`.

**Exemplo usando `oauth4webapi` (recomendado para OAuth 2.1)**

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

**Representação com curl:**

```bash
curl -X POST https://authorization-server.com/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=AUTHORIZATION_CODE" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "redirect_uri=https://yourapp.com/callback" \
  -d "code_verifier=fdb8...d2a9"
```

### 5. Validação do Servidor

O endpoint de token realiza:

```
HASH(code_verifier) == code_challenge
```

Se o hash coincidir, o código é válido. Caso contrário, a requisição falha.

### 6. Resposta do Token

Uma resposta bem-sucedida inclui `access_token`, `refresh_token` (se `offline_access` for solicitado) e opcionalmente `id_token`.

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

## Suporte a Bibliotecas

### Lado do Servidor (Servidor de Autorização)

| Biblioteca / Plataforma | Suporte ao OAuth 2.1 |
|-------------------------|----------------------|
| Keycloak                | Sim (PKCE obrigatório por padrão) |
| Entra ID (Azure AD)     | Sim (Código de Autorização com PKCE) |
| Auth0                   | Sim (requer configuração) |
| Okta                    | Sim |
| Curity                  | Sim |
| Spring Security 6+      | Sim (`oauth2Client` com PKCE) |

### Lado do Cliente (Aplicação)

| Linguagem   | Biblioteca                                           | Notas                                                           |
|-------------|------------------------------------------------------|-----------------------------------------------------------------|
| Node.js     | [`oauth4webapi`](https://github.com/panva/oauth4webapi) | Específica do autor, pronta para OAuth 2.1                      |
| Python      | [`Authlib`](https://authlib.org/)                    | Suporta PKCE e padrões OAuth 2.1                                |
| Java        | Spring Security 6+                                   | `NimbusJwtDecoder` embutido com PKCE                            |
| Mobile      | AppAuth (Android/iOS)                                | Suporte nativo a PKCE                                           |
| Web SPA     | Padrão BFF ou Web Workers                            | Sem PKCE direto no navegador, use Backend-for-Frontend          |

---

## Migração do OAuth 2.0

### Lista de Verificação

1. **Substitua o Grant Implícito** por Código de Autorização + PKCE.
2. **Substitua o Grant de Senha** por Código de Autorização + PKCE ou Credenciais de Cliente (para máquina a máquina).
3. **Imponha o PKCE** em cada troca de Código de Autorização.
4. **Ative a Rotação do Token de Atualização** (tokens de uso único).
5. **Atualize a comparação de URI de Redirecionamento** para correspondência exata de strings.
6. **Mude para S256** como método de desafio se anteriormente usava `plain`.

### Exemplo: Migrando um Fluxo de Código de Autorização Legado

**Antes (OAuth 2.0 – PKCE opcional)**

```
step 1: client_id + redirect_uri → get code
step 2: code + client_secret → get token
```

**Depois (OAuth 2.1 – PKCE obrigatório)**

```
step 1: client_id + redirect_uri + code_challenge (S256) → get code
step 2: code + code_verifier → get token
```

---

## Exemplo do Mundo Real: Servidor MCP no Azure Container Apps

A especificação do Model Context Protocol (MCP) (a partir de 2026-03-15) exige OAuth 2.1 + PKCE para autorização ao interagir com servidores de agente. Aqui está uma configuração resumida:

1. **Defina PRM (Metadados de Recurso Protegido)** – exponha `.well-known/oauth-authorization-server`
2. **Implemente o Registro Dinâmico de Cliente** (RFC 7591) para clientes.
3. **Design de Escopos** – defina escopos granulares por recurso (ex: `files:read`, `compute:execute`).
4. **Validação de Token** – toda requisição de API deve verificar a assinatura do token de acesso e a chave vinculada.

Exemplo de configuração AZ CLI (conceito):

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

O cliente (ex: extensão VSCode Azure MCP) então executa o fluxo PKCE antes de invocar ferramentas MCP.

---

## Melhores Práticas de Segurança

- **Use um Parâmetro State** – Vincule a solicitação de autorização à sessão do usuário.
- **Armazene o `code_verifier` de forma segura** – Na sessão do backend ou em um armazenamento seguro do lado do cliente (não na URL).
- **Valide cada token** – Verifique assinatura, emissor, audiência e expiração.
- **Rotacione tokens de atualização** – Cada atualização gera um novo token e invalida o anterior.
- **Implemente DPoP** – Adicione a claim `cnf` aos tokens de acesso para suporte a restrição ao remetente.
- **Registre reutilização de token** – Detecte possível roubo de token.

---

## Solução de Problemas Comuns

| Problema                                          | Causa Provável                                | Solução                                                                                       |
|---------------------------------------------------|-----------------------------------------------|-----------------------------------------------------------------------------------------------|
| `invalid_grant` durante a troca de token          | `code_verifier` não corresponde a `code_challenge` | Refaça o hash do verifier exatamente como durante a criação (mesmo algoritmo, mesma codificação de caracteres) |
| `redirect_uri_mismatch`                           | Comparação de URL não exata                    | Certifique-se de que `redirect_uri` corresponda exatamente, incluindo barras no final         |
| Código de autorização expirado                    | Timeout > 10 minutos                           | Repita o fluxo completo                                                                       |
| Token de atualização rejeitado após rotação        | Reutilização de token detectada                | O cliente deve descartar tokens de atualização antigos; implemente a rotação de uso único corretamente |

---

## Referências

- [Especificação Preliminar do OAuth 2.1](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)
- [PKCE RFC 7636](https://datatracker.ietf.org/doc/html/rfc7636)
- [OAuth Security BCP (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [oauth4webapi – Implementação Oficial](https://github.com/panva/oauth4webapi)
- [Authlib – OAuth 2.1 para Python](https://authlib.org/)
- [Spring Security 6 OAuth 2.1 Client](https://docs.spring.io/spring-security/reference/servlet/oauth2/client/index.html)

---

## Conclusão

Adotar o OAuth 2.1 com PKCE não é apenas um requisito de conformidade — é uma melhoria fundamental na postura de segurança. Ao tornar o PKCE obrigatório, remover fluxos fracos e impor validação estrita, o OAuth 2.1 garante que as aplicações modernas sejam resilientes contra os ataques de autorização mais comuns. Seja construindo um novo servidor MCP, migrando aplicativos móveis legados ou endurecendo uma aplicação de página única, esta especificação fornece um caminho claro e seguro.