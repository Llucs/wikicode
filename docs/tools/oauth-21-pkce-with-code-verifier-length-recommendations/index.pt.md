---
title: Recomendações de Tamanho para Verificador de Código com OAuth 2.1 PKCE
description: Guia para implementar OAuth 2.1 PKCE com recomendações sobre o tamanho do verificador de código para melhorar a segurança.
created: 2026-07-12
tags:
  - OAuth
  - PKCE
  - Segurança
status: rascunho
---

# Recomendações de Tamanho para Verificador de Código com OAuth 2.1 PKCE

## O que é PKCE?

PKCE (Proof Key for Code Exchange) é uma métrica de segurança usada no OAuth 2.0 para prevenir ataques que possam obter o código de autorização. Adiciona uma camada adicional de segurança exigindo uma chave única e não reutilizável (o verificador de código) a ser trocada entre o cliente e o servidor de autorização.

## Características Chave do OAuth 2.1 PKCE

- **Verificador de Código**: Uma string aleatória usada como segredo entre o cliente e o servidor de autorização.
- **Desafio de Código**: Um hash do verificador de código, usado para prevenir a captura de rede.
- **Nonce**: Um valor único incluído na solicitação de autorização para garantir que o código seja usado apenas uma vez.

## Histórico do PKCE

O PKCE foi introduzido como uma métrica opcional no OAuth 2.0 para melhorar a segurança. No entanto, tornou-se parte obrigatória da especificação OAuth 2.1 para garantir um nível mais alto de segurança, especialmente para clientes públicos.

## Casos de Uso do PKCE

- **Clientes Públicos**: Clientes que não podem armazenar segredos de forma segura, como aplicativos web e aplicativos móveis.
- **Fluxo Híbrido**: Apropriado para cenários onde o cliente precisa trocar o código de autorização pelo token de acesso.
- **Fluxo de Código de Autorização**: Melhora a segurança em cenários onde o cliente redireciona o usuário para um servidor de autorização.

## Recomendações de Tamanho para Verificador de Código

O tamanho do verificador de código é um aspecto crítico da segurança do PKCE. O verificador de código deve ser longo o suficiente para resistir a ataques de força bruta, mas curto o suficiente para ser gerenciável em implementações de cliente.

### Tamanhos Recomendados

- **Tamanho Mínimo**: 43 caracteres
- **Tamanho Recomendado**: 128 caracteres ou mais

O verificador de código mais longo é mais seguro contra ataques de força bruta. O tamanho mínimo de 43 caracteres é recomendado pela especificação OAuth 2.1 para fornecer um nível razoável de segurança. No entanto, o uso de um verificador de código mais longo, como 128 caracteres, proporciona uma margem de segurança significativamente maior.

## Instalação e Uso Básico

### Passo 1: Gerar o Verificador de Código

```python
import random
import string

def gerar_verificador_de_codigo(comprimento=128):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=comprimento))
```

### Passo 2: Gerar o Desafio de Código

```python
import hashlib
import base64

def gerar_desafio_de_codigo(verificador_de_codigo):
    desafio_de_codigo = hashlib.sha256(verificador_de_codigo.encode()).digest()
    return base64.urlsafe_b64encode(desafio_de_codigo).rstrip(b'=').decode()
```

### Passo 3: Incluir PKCE no Fluxo OAuth 2.0

1. **Solicitação de Autorização**:
   - Inclua o `code_challenge` e `code_challenge_method` na solicitação de autorização.
   - Exemplo:
     ```http
     GET /authorize?response_type=code&client_id=seu_id_do_cliente&redirect_uri=https%3A%2F%2Fseuapp.com%2Fcallback&code_challenge=sua_desafio_de_codigo&code_challenge_method=S256&state=algum_valor_do_estado&nonce=algum_valor_do_nonce
     ```

2. **Solicitação de Token**:
   - Inclua o `verificador_de_codigo` na solicitação de token.
   - Exemplo:
     ```http
     POST /token HTTP/1.1
     Host: seu_servidor_de_autorizacao.com
     Content-Type: application/x-www-form-urlencoded

     grant_type=authorization_code&code=seu_codigo_de_autorizacao&redirect_uri=https%3A%2F%2Fseuapp.com%2Fcallback&code_verifier=seu_verificador_de_codigo
     ```

## Conclusão

Usar PKCE com um verificador de código suficientemente longo (pelo menos 128 caracteres) é crucial para melhorar a segurança dos fluxos OAuth 2.0, especialmente em cenários de clientes públicos. Seguindo as recomendações, os desenvolvedores podem garantir um nível mais alto de segurança para suas aplicações.