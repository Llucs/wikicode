---
title: cURL — Ferramenta de Transferência de Dados
description: cURL é uma ferramenta de linha de comando para transferir dados usando protocolos de rede.
created: 2026-06-14
tags:
  - tool
  - cli
  - networking
status: draft
ecosystem: networking
---

# cURL — Ferramenta de Transferência de Dados

## O que é

cURL (Client URL) é uma ferramenta de linha de comando e biblioteca para transferir dados com URLs. Suporta dezenas de protocolos incluindo HTTP, HTTPS, FTP, SFTP, SCP, LDAP e muitos outros.

## Instalação

```bash
# Ubuntu/Debian
sudo apt-get install curl

# macOS (pre-installed, or via Homebrew)
brew install curl

# Windows (via Chocolatey)
choco install curl
```

## Uso básico

### Requisição GET

```bash
curl https://api.github.com/users/octocat
```

### POST com JSON

```bash
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com"}'
```

### Salvar resposta em arquivo

```bash
curl -o output.json https://api.example.com/data
```

### Seguir redirecionamentos

```bash
curl -L https://bit.ly/example
```

### Cabeçalhos personalizados

```bash
curl -H "Authorization: Bearer token123" https://api.example.com/protected
```

## Principais flags

| Flag | Descrição |
|------|-----------|
| `-X` | método HTTP (GET, POST, PUT, DELETE) |
| `-H` | Cabeçalho personalizado |
| `-d` | Dados do corpo da requisição |
| `-o` | Escrever saída em arquivo |
| `-L` | Seguir redirecionamentos |
| `-v` | Modo verboso |
| `-s` | Modo silencioso (sem progresso) |
| `-k` | Permitir SSL inseguro |
| `-u` | Autenticação básica (usuário:senha) |

## Melhores práticas

- Use `-sS` em scripts para suprimir o progresso, mas manter os erros visíveis
- Use `--retry 3` para tentativas automáticas em falhas de rede
- Nunca passe tokens em URLs; use o cabeçalho `Authorization` em vez disso