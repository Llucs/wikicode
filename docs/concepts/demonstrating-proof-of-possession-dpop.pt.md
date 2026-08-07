---
title: Demonstrando Prova de Posse (DPoP) — Restringindo Tokens OAuth ao Remetente com RFC 9449
description: Um guia para desenvolvedores sobre DPoP, o mecanismo da RFC 9449 que vincula tokens de acesso e atualização do OAuth 2.0 a um par de chaves mantido pelo cliente para evitar reprodução e roubo de tokens.
created: 2026-08-07
tags:
  - oauth2
  - security
  - rfc-9449
  - dpop
  - identity
status: draft
---

# Demonstrando Prova de Posse (DPoP)

## O que é DPoP?

**Demonstrando Prova de Posse (DPoP)** é uma extensão de OAuth 2.0 em nível de aplicação definida na **RFC 9449**. Ela *restringe ao remetente* tokens de acesso e tokens de atualização, vinculando-os a um par de chaves pública/privada gerado e mantido pelo cliente.

Em vez de enviar um `Authorization: Bearer <token>` simples, um cliente habilitado para DPoP prova ao servidor de recursos que ainda possui a chave privada usada quando o token foi emitido. Cada requisição carrega um JWT de prova assinado e de curta duração em um cabeçalho HTTP `DPoP`. Essa prova é criptograficamente vinculada ao método HTTP exato, à URL e ao token de acesso em uso.

Como o token de acesso não é mais "bearer" — qualquer um que o possua pode usá-lo — um token roubado é inútil sem a chave privada correspondente.

## Por que isso importa

Tokens bearer OAuth 2.0 comuns têm um problema fundamental: a posse do token é a única prova de autorização. Um token vazado em um log de servidor, cabeçalho de referer, extensão de navegador, ou interceptado após um aplicativo móvel ser comprometido pode ser reproduzido por um atacante.

O DPoP resolve isso mudando o modelo de ameaça:

- Um token de acesso roubado não pode ser reproduzido, a menos que o atacante também roube a chave privada do cliente.
- O token de acesso é vinculado a uma chave específica no servidor de autorização.
- O servidor de recursos verifica uma prova criptográfica em cada chamada de API.
- Tokens de atualização também podem ser restritos ao remetente, fechando a lacuna do "roubo de token de atualização".

O DPoP é frequentemente exigido ou recomendado em ecossistemas de alta segurança, como APIs compatíveis com Open Banking / FAPI, plataformas de saúde digital e sistemas de identidade empresarial.

## Como o DPoP funciona

### 1. O cliente gera um par de chaves

O cliente cria um par de chaves assimétricas — normalmente EC P-256 (ES256). A chave privada permanece com o cliente. A chave pública é representada como uma JSON Web Key (JWK) e incluída no cabeçalho de cada prova DPoP.

O servidor de autorização vincula o token de acesso a essa chave pública armazenando sua **impressão digital SHA-256 da JWK** (`jkt`) na declaração `cnf` do token:

```text
jkt = base64url(SHA-256("<canonical JSON of public JWK>"))
```

### 2. O cliente constrói um JWT de prova DPoP

Uma prova DPoP é um JWT com estes parâmetros de cabeçalho JOSE:

| Cabeçalho | Valor |
|---|---|
| `typ` | `dpop+jwt` |
| `alg` | O algoritmo de assinatura, ex.: `ES256` |
| `jwk` | A chave pública do cliente |

E estas declarações:

| Declaração | Significado |
|---|---|
| `iat` | Horário de criação da prova |
| `jti` | Identificador único da prova (prevenção de reprodução) |
| `htm` | Método HTTP da requisição, ex.: `GET` |
| `htu` | URI HTTP de destino, incluindo a string de consulta |
| `ath` | Base64url(SHA-256(access_token)) — presente apenas ao chamar um servidor de recursos |
| `nonce` | Nonce opcional emitido pelo servidor |

### 3. Requisições de token e requisições de API

Há duas situações em que o DPoP é usado:

**Requisição de token** — O cliente envia sua prova DPoP em um cabeçalho `DPoP` na requisição ao endpoint de token do servidor de autorização.

```http
POST /token HTTP/1.1
Host: auth.example.com
Content-Type: application/x-www-form-urlencoded
DPoP: <dpop-proof-jwt>

grant_type=authorization_code
&code=...
```

O servidor de autorização verifica a prova, vincula o token emitido à impressão digital da JWK da prova e retorna `token_type: "DPoP"` na resposta do token.

**Requisição de recurso** — O cliente usa o token com o esquema de autorização `DPoP` e inclui uma prova DPoP *nova* contendo `ath`.

```http
GET /reports HTTP/1.1
Host: api.example.com
Authorization: DPoP <access-token>
DPoP: <dpop-proof-jwt-with-ath>
```

### 4. Diagrama de fluxo da requisição

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

### 5. Checklist de verificação no lado do servidor

Um servidor de recursos em conformidade deve:

1. Verificar se o esquema do `Authorization` é `DPoP`, e não `Bearer`.
2. Analisar o JWT de prova DPoP.
3. Verificar a assinatura da prova usando a chave pública no cabeçalho `jwk`.
4. Rejeitar algoritmos não suportados (ex.: `none`).
5. Confirmar que a impressão digital da JWK da prova (`jwk`) corresponde ao `cnf.jkt` do token.
6. Verificar se `htm` é o método HTTP real.
7. Verificar se `htu` é a URL completa real da requisição (esquema, host, porta se aplicável, caminho, consulta).
8. Se um token de acesso for apresentado, verificar se `ath` é igual ao hash SHA-256 da string exata desse token.
9. Validar se `iat` está dentro de uma janela de atualização aceitável (normalmente de 60 a 300 segundos).
10. Manter um cache de curta duração com os valores `jti` usados e rejeitar duplicatas.
11. Se estiver configurado para exigir nonces, validar se a prova inclui um nonce atual emitido pelo servidor.

### 6. Desafios de nonce

Muitos servidores de autorização e servidores de recursos exigem que uma prova contenha um `nonce` gerado pelo servidor. Isso evita que uma prova roubada seja reproduzida por um longo período.

Se o cliente omitir um nonce esperado, o servidor responde com um erro e um cabeçalho `DPoP-Nonce`:

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json
DPoP-Nonce: R5H6rE8sW

{
  "error": "use_dpop_nonce"
}
```

O cliente deve criar uma prova **nova**, incluir o nonce e tentar novamente. Ele não deve reutilizar a prova antiga.

## Exemplo real — cliente Python

O exemplo a seguir usa `cryptography`, `PyJWT` e `requests` para demonstrar o protocolo em baixo nível. Em produção, prefira uma biblioteca OAuth/DCoP mantida em vez de criptografia feita manualmente.

Pré-requisitos:

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

Detalhes importantes neste exemplo:

- Um novo `jti` é gerado para cada prova.
- A prova da requisição de token não tem `ath`.
- A prova da requisição de recurso aplica hash à string exata do token de acesso.
- O cliente mantém a chave privada durante todo o tempo de vida da sessão.

## Esboço de verificação no lado do servidor

Um servidor de recursos que verifica a prova acima precisa reconstruir a chave pública a partir do cabeçalho `jwk` e então validar o JWT:

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

O último item — corresponder a JWK da prova ao `cnf` vinculado ao token — é o coração do DPoP. Para tokens de acesso opacos, o servidor de recursos deve obter `cnf` por meio de introspecção de token. Para tokens de acesso JWT, `cnf` geralmente é incluído diretamente nas declarações do token.

## Trade-offs e alternativas

### DPoP vs. tokens bearer

| Aspecto | Token bearer | DPoP |
|---|---|---|
| Vinculação | Nenhuma | Chave pública mantida pelo cliente |
| Reprodução de token roubado | Fácil | Inviável sem a chave privada |
| Complexidade do cliente | Muito baixa | Média: geração de chaves, assinatura, tratamento de nonces |
| Sobrecarga do servidor | Mínima | Verificação de assinatura por requisição |
| Padrão | RFC 6750 | RFC 9449 |

Tokens bearer fazem sentido para APIs internas de baixo risco. O DPoP é justificável quando um token vazado teria alto impacto.

### DPoP vs. TLS mútuo (mTLS)

| Aspecto | mTLS (RFC 8705) | DPoP |
|---|---|---|
| Camada de vinculação | Camada de transporte | Camada de aplicação |
| Gerenciamento de certificados do cliente | Pesado (PKI, provisionamento) | Par de chaves, mais fácil de implantar |
| Funciona em navegadores / SPAs | Difícil | Funciona com WebCrypto |
| Funciona em aplicativos móveis | Difícil | Sim |
| Conformidade com FAPI | Frequentemente usado | Cada vez mais usado |

O DPoP é geralmente mais fácil de implantar para clientes públicos web e móveis do que a infraestrutura de certificados mTLS. O mTLS continua sendo uma opção robusta para integrações servidor a servidor em que o gerenciamento de certificados já é comum.

### Limitações do DPoP

- **O roubo da chave privada é fatal.** O DPoP protege contra roubo de token, não contra roubo de chave. Uma chave privada comprometida dá ao atacante o mesmo poder que o cliente legítimo.
- **Custo de assinatura por requisição.** Cada requisição de API exige uma assinatura, e cada requisição ao servidor de recursos exige verificação.
- **Viagens de ida e volta com nonce.** Se um servidor exigir nonces, a primeira requisição após uma rotação de nonce incorre em uma viagem de ida e volta extra.
- **Responsabilidade de gerenciamento de chaves.** Os clientes devem criar, armazenar e rotacionar chaves com segurança. Perder a chave significa reautenticar.
- **Exige suporte de ponta a ponta.** Tanto o servidor de autorização quanto todos os servidores de recursos devem entender DPoP e honrar a vinculação `cnf`.
- **Não substitui o PKCE.** O DPoP não impede a interceptação do código de autorização. Use PKCE para clientes públicos.

## Boas práticas

1. **Use DPoP junto com PKCE.** Eles tratam ameaças diferentes. O PKCE protege a troca do código de autorização; o DPoP protege os tokens resultantes.
2. **Use P-256 / ES256.** É amplamente suportado, rápido e seguro. Evite algoritmos exóticos, a menos que todas as partes os suportem.
3. **Gere um novo par de chaves por sessão de usuário.** Não compartilhe uma chave privada entre todos os usuários de um aplicativo.
4. **Armazene a chave privada com segurança.** Use o chaveiro do sistema operacional, Android Keystore, iOS Secure Enclave, TPM ou uma chave WebCrypto não exportável.
5. **Vincule também os tokens de atualização.** Envie uma prova DPoP ao solicitar um novo token de acesso a partir de um token de atualização. Se o servidor de autorização suportar tokens de atualização restritos ao remetente, use esse recurso.
6. **Falhe de forma fechada.** Se o servidor retornar `token_type: "Bearer"` após uma requisição DPoP, trate isso como uma configuração incorreta em vez de fazer fallback transparente.
7. **Nunca registre provas DPoP em logs.** Uma prova válida tem tempo limitado, mas ainda pode ser reproduzível se o cache de `jti` do servidor for curto e o atacante a capturar rapidamente.
8. **Use uma biblioteca auditada** em produção em vez de implementar o protocolo do zero. Muitos SDKs OAuth oferecem suporte a DPoP:
   - **Python** — Authlib
   - **JavaScript** — oauth4webapi
   - **Java** — Nimbus OAuth 2.0 SDK / JOSE+JWT
   - **.NET** — IdentityModel
9. **Sempre use HTTPS.** O DPoP não substitui o TLS; é uma defesa adicional contra o uso indevido de tokens bearer depois que uma requisição sai do cliente.

## Referências

- [RFC 9449 — OAuth 2.0 Demonstrating Proof of Possession (DPoP)](https://www.rfc-editor.org/rfc/rfc9449)
- [RFC 6749 — The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749)
- [RFC 7638 — JSON Web Key (JWK) Thumbprint](https://www.rfc-editor.org/rfc/rfc7638)
- [RFC 8705 — OAuth 2.0 Mutual TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705)
- [RFC 7636 — Proof Key for Code Exchange (PKCE)](https://www.rfc-editor.org/rfc/rfc7636)

## Resumo

O DPoP transforma tokens OAuth de credenciais bearer em credenciais restritas ao remetente. O cliente prova a posse de uma chave privada em cada requisição, e o servidor de recursos verifica essa prova contra a chave vinculada ao token na emissão. É um mecanismo prático, em nível de aplicação, que reduz significativamente o dano causado por roubo de tokens, especialmente para clientes públicos, aplicativos móveis e aplicações de página única.

Adotar DPoP adiciona complexidade real — gerenciamento de chaves, nonces, caches de reprodução e verificação por requisição —, mas para APIs que transportam dados sensíveis, a melhoria de segurança geralmente vale o custo.