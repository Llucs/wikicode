---
title: Práticas Recomendadas para OAuth 2.1 com PKCE
description: Diretrizes detalhadas para o aprimoramento da segurança das implementações OAuth 2.1 usando Proof Key for Code Exchange (PKCE) para prevenir ataques de injeção de código de autorização.
created: 2026-07-13
tags:
  - OAuth
  - PKCE
  - Segurança
  - API
status: rascunho
---

# Práticas Recomendadas para OAuth 2.1 com PKCE

OAuth 2.1 com Proof Key for Code Exchange (PKCE) é uma extensão de protocolo que aumenta a segurança do esquema de autorização OAuth 2.0. O PKCE foi projetado especificamente para mitigar o risco de interceptação de código de autorização, que pode ocorrer em clientes públicos (por exemplo, aplicativos móveis ou aplicativos web única página) que não têm maneiras seguras de manter segredos de cliente confidenciais.

## Recursos-chave

1. **Verificador de Código/Desafio**: Uma string gerada aleatoriamente usada pelo cliente para gerar o desafio PKCE. O verificador de código é mantido confidencial e não é enviado pela rede.
2. **Desafio de Código**: Um hash do verificador de código, que é enviado ao servidor de autorização.
3. **Fluxo de Aprovação com Código de Autorização**: O fluxo permanece o mesmo, mas com a adição do PKCE.

## Histórico

OAuth 2.1 com PKCE foi introduzido como uma extensão do OAuth 2.0 para abordar preocupações de segurança em autenticação de clientes. Foi proposto inicialmente no RFC 7636 e posteriormente incorporado na especificação do OAuth 2.1.

## Casos de Uso

- **Clientes Públicos**: Aplicativos móveis, aplicativos web única página e qualquer cliente que não possa armazenar segredos de cliente de forma segura.
- **Segurança de API**: Aumentar a segurança do acesso e autenticação de APIs para aplicativos web e móveis.
- **Aplicativos Web**: Melhorar a segurança de aplicativos web que usam OAuth para autenticação.

## Instalação

Enquanto OAuth 2.1 com PKCE é uma extensão de protocolo, a implementação geralmente envolve os seguintes passos:

1. **Implementação do Lado do Cliente**:
   - Gerar um verificador de código e um desafio de código.
   - Usar o desafio de código na solicitação de autorização.
   - Gerenciar a resposta de autorização e trocar o código de autorização por um token de acesso.

2. **Implementação do Lado do Servidor**:
   - Validar o desafio de código contra o verificador de código.
   - Gerenciar a resposta de autorização e trocar o código de autorização por um token de acesso.

### Uso Básico

1. **Autenticação do Cliente**:
   - O cliente gera um verificador de código e um desafio de código.
   - O desafio de código é incluído na solicitação de autorização.

2. **Resposta de Autorização**:
   - O usuário concede ou nega acesso.
   - O servidor de autorização responde com um código de autorização.

3. **Solicitação de Token**:
   - O cliente troca o código de autorização por um token de acesso usando o verificador de código.

4. **Validação**:
   - O servidor de autorização verifica o desafio de código e o verificador de código para garantir a autenticidade do cliente.

## Práticas Recomendadas

1. **Usar Verificadores de Código Fortes**:
   - Gerar verificadores de código usando um gerador de número pseudo-aleatório seguro (CSPRNG).
   - Garantir que o verificador de código tenha pelo menos 43 caracteres para mitigar ataques de tempo.

2. **Métodos de Desafio de Código**:
   - Usar o método `S256` para hash do verificador de código. Este método é projetado para ser resistente a ataques de tempo.

3. **Autenticação do Cliente**:
   - Usar métodos de autenticação de cliente apropriados para o tipo de cliente (por exemplo, `client_secret_basic` para clientes confidenciais, `none` para clientes públicos).

4. **Segurança do Transporte**:
   - Garantir que todas as comunicações ocorram por HTTPS para proteger o desafio de código e outras informações sensíveis.

5. **Gerenciamento de Sessão**:
   - Implementar o gerenciamento de sessão para garantir que o código de autorização não seja reutilizado.

6. **Auditorias e Atualizações Regulares**:
   - Regularmente revisar e atualizar a implementação para manter-se atualizado com as práticas e padrões de segurança mais recentes.

7. **Limites de Taxa**:
   - Implementar limites de taxa para prevenir abusos e ataques por força bruta.

8. **Log e Monitoramento**:
   - Logar e monitorar solicitações e respostas de autorização para detectar e responder a atividades suspeitas de forma prompta.

Adotando essas práticas recomendadas, você pode aumentar a segurança da sua implementação OAuth 2.1 com PKCE, garantindo que as informações sensíveis estejam protegidas e que sua aplicação permaneça segura.

## Exemplo: Implementação em Python

Aqui está um exemplo básico de implementação do PKCE em Python usando a biblioteca `requests`:

```python
import requests
import string
import random
import hashlib

# Gerar um verificador de código
def generate_code_verifier(length=43):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(length))

# Gerar um desafio de código
def generate_code_challenge(verifier):
    sha256 = hashlib.sha256()
    sha256.update(verifier.encode('utf-8'))
    return sha256.hexdigest()[:43]

# Exemplo de autenticação de cliente
def authenticate_client(authorization_url, client_id, redirect_uri, code_verifier):
    # Gerar o desafio de código
    code_challenge = generate_code_challenge(code_verifier)

    # Solicitação de autorização
    auth_params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge
    }

    response = requests.get(authorization_url, params=auth_params)
    if response.status_code != 200:
        raise Exception("Falha na autenticação do cliente")

    # Lidar com a interação do usuário e obter o código de autorização

    # Solicitação de token
    token_params = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri,
        'code_verifier': code_verifier
    }

    token_response = requests.post(token_url, data=token_params, auth=(client_id, 'client_secret'))
    if token_response.status_code != 200:
        raise Exception("Falha na obtenção do token de acesso")

    return token_response.json()

# Uso
client_id = 'sua_id_do_cliente'
redirect_uri = 'http://sua-uri-de-redirecionamento'
authorization_url = 'https://sua-servidor-de-autorizacao'
code_verifier = generate_code_verifier()
code_challenge = generate_code_challenge(code_verifier)
access_token = authenticate_client(authorization_url, client_id, redirect_uri, code_verifier)
print("Token de Acesso:", access_token['access_token'])
```

Este exemplo demonstra como gerar um verificador de código e um desafio de código, realizar a solicitação de autorização e trocar o código de autorização por um token de acesso.