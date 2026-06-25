---
title: OWASP API Security Top 10
description: Um wiki abrangente para desenvolvedores que cobre o OWASP API Security Top 10 (2023), incluindo análises aprofundadas, estratégias de teste e integração CI/CD.
created: 2026-06-25
tags:
  - owasp
  - api-security
  - top-10
  - bola
  - bopla
  - secure-coding
  - devsecops
  - bug-bounty
status: draft
---

# OWASP API Security Top 10

O **OWASP API Security Top 10** é um documento de conscientização padrão da indústria publicado pelo Open Web Application Security Project (OWASP), atualizado em 2023 para refletir os riscos de segurança únicos das APIs modernas (REST, GraphQL, gRPC e SOAP). Diferentemente do OWASP Web Top 10 geral (que cobre XSS, SQLi, CSRF, etc.), esta lista foca **exclusivamente** nas falhas arquiteturais e lógicas que afligem aplicações orientadas a APIs.

Em 2026, falhas relacionadas a APIs continuam sendo o principal vetor de violações de dados, com incidentes em grandes empresas (Twitter, T-Mobile, Optus) remontando a um punhado de erros evitáveis documentados neste framework.

---

## Os 10 Principais Riscos de Segurança em APIs (2023)

| Posição | Nome | Acrônimo | Problema Principal |
|---------|------|----------|--------------------|
| API1 | Broken Object Level Authorization | BOLA | Acessar objetos pertencentes a outros usuários sem verificações de ACL adequadas |
| API2 | Broken Authentication | — | Gerenciamento fraco de credenciais, vazamento de tokens, fixação de sessão |
| API3 | Broken Object Property Level Authorization | BOPLA | Atribuição em massa / sobrecarga de campos sensíveis |
| API4 | Unrestricted Resource Consumption | — | Falta de limitação de taxa, limites de paginação ou restrição de tamanho de payload |
| API5 | Broken Function Level Authorization | BFLA | Chamar endpoints administrativos de alto privilégio como um usuário comum |
| API6 | Unrestricted Access to Sensitive Business Flows | — | Bots explorando fluxos de API válidos (scalping, scraping) |
| API7 | Server Side Request Forgery | SSRF | URLs controladas pelo usuário são buscadas pela API, permitindo sondagem de serviços internos |
| API8 | Security Misconfiguration | — | Credenciais padrão, erros verbosos, falta de CORS, sistemas sem patch |
| API9 | Improper Inventory Management | — | Versões de API zumbis/obsoletas, endpoints de debug esquecidos, APIs sombra |
| API10 | Unsafe Consumption of APIs | — | Confiar cegamente em respostas de APIs de terceiros (risco na cadeia de suprimentos) |

### Mudanças Notáveis desde 2019

A edição de 2023 removeu ameaças web genéricas (XSS, SQLi — agora cobertas pelo Top 10 padrão) e introduziu cinco categorias totalmente novas: **BOPLA**, **Fluxos de Negócio Irrestritos**, **SSRF**, **Gerenciamento de Inventário Impróprio** e **Consumo Inseguro de APIs**.

Também formalizou a metodologia **"Lather, Rinse, Repeat"** — um ciclo contínuo de Descoberta → Validação → Remediação.

---

## Metodologia de Adoção

Como isso é um *framework* (não um pacote de software), "instalação" significa integrar a mentalidade e os fluxos de teste no seu ciclo de desenvolvimento.

### Fase 1: Descoberta e Inventário (Aborda API9)

Mapeie cada endpoint, sua sensibilidade de dados, mecanismo de autenticação e versão. Esta é a etapa mais negligenciada.

```bash
# Um scan de descoberta simples para caminhos comuns de API
for endpoint in /api/v1 /api/v2 /api/v3 /graphql /rest /soap /debug /health /swagger.json /openapi.json; do
  status=$(curl -o /dev/null -s -w "%{http_code}\n" "http://target.com${endpoint}")
  echo "Endpoint ${endpoint} retornou ${status}"
done
```

Ferramentas: Postman, Swagger Inspector, Burp Suite, crawlers personalizados.

### Fase 2: Scanners Automatizados

Execute scanners dinâmicos contra sua especificação de API.

```bash
# Escaneamento de API do OWASP ZAP
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py -t file:///zap/wrk/openapi.yaml -f openapi -r report.html
```

**Verificações principais para executar automaticamente:**
- **BOLA:** Troque IDs de objetos em requisições em lote.
- **BFLA:** Tente DELETE/PUT em endpoints administrativos com tokens de baixo privilégio.
- **SSRF:** Injete `http://169.254.169.254/metadata/instance` em parâmetros de URL.
- **Misconfiguration:** Verifique por `Access-Control-Allow-Origin: *` e respostas de erro verbosas.

### Fase 3: Análise Manual Profunda (Modo Pentest)

Use o Top 10 como uma checklist.

#### API1: Broken Object Level Authorization (BOLA)

```bash
# Tentar acessar dados de outro usuário alterando o ID na URL
curl -X GET https://api.example.com/api/v1/users/123 \
  -H "Authorization: Bearer valid_token_for_user_456"
# Se a resposta contiver dados do usuário 123, você tem uma vulnerabilidade BOLA.
```

#### API3: Broken Object Property Level Authorization (BOPLA)

```bash
# Atribuição em massa: tente adicionar "role":"admin" ou "salary":100000 a um PATCH
curl -X PATCH https://api.example.com/api/v1/user/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"test","role":"admin","salary":999999}'
```

#### API6: Unrestricted Business Flows

```python
import requests
# Simular um bot abusando de um fluxo de votação / cupom / checkout
url = "https://ticketing.example.com/api/v2/checkout"
payload = {"event_id": 1, "quantity": 1}
session = requests.Session()
session.headers.update({"Authorization": "Bearer valid_token"})

for i in range(100):
    r = session.post(url, json=payload)
    print(f"Tentativa {i}: {r.status_code} - {r.text[:100]}")
    # Se todas as 100 forem bem-sucedidas sem limitação de taxa, API6 está presente.
```

### Fase 4: Integração CI/CD

Embeba as verificações no seu pipeline. Um estágio típico de pipeline seguro se parece com isso:

```yaml
# .gitlab-ci.yml (GitLab CI) ou GitHub Actions equivalente
api-security:
  stage: test
  script:
    # Análise Estática para padrões BOPLA
    - semgrep --config=auto .
    # Varredura Dinâmica com ZAP
    - docker run -v $(pwd):/zap/wrk/ zaproxy/zap-stable \
        zap-api-scan.py -t http://staging/api/openapi.json -f openapi
    # Teste de Limitação de Taxa / Abuso de Fluxo de Negócio (k6)
    - k6 run tests/abuse.js
  only:
    - branches
```

#### Exemplo: Regra Semgrep para BOPLA (Atribuição em Massa no Django)

```yaml
rules:
  - id: mass-assignment-django
    patterns:
      - pattern-either:
          - pattern: Model.objects.update(...)  # Inseguro se não filtrar campos
          - pattern: serializer.save(...)
    message: >
      Potencial vulnerabilidade de Atribuição em Massa (API3 / BOPLA).
      Defina explicitamente os campos permitidos usando `fields` ou `read_only_fields` no serializer.
    severity: WARNING
    languages:
      - python
```

#### Exemplo: Middleware de Limitação de Taxa (Go)

```go
import (
    "golang.org/x/time/rate"
    "net/http"
)

var limiter = rate.NewLimiter(rate.Limit(100), 200) // 100 requisições/s, burst 200

func rateLimitMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        if !limiter.Allow() {
            http.Error(w, `{"error":"rate_limit_exceeded"}`, http.StatusTooManyRequests)
            return
        }
        next.ServeHTTP(w, r)
    })
}
```

## A Metodologia "Lather, Rinse, Repeat"

Introduzida fortemente na edição de 2023, este conceito enfatiza que a segurança de API **não é um pentest único**, mas um ciclo contínuo:

1. **Lather:** Descubra toda a superfície da sua API (incluindo APIs sombra).
2. **Rinse:** Valide as descobertas através de testes automatizados e manuais.
3. **Repeat:** Reescaneie sempre que um novo endpoint ou versão for implantado.

Isso combate diretamente o **API9 (Gerenciamento de Inventário Impróprio)** e garante que a postura de segurança evolua com o código.

## Relacionamento com Outros Padrões

- **PCI DSS 4.0:** Requer controles robustos de segurança de API (incluindo testes de BOLA/BFLA) para ambientes com dados de portadores de cartão.
- **SOC 2:** O Top 10 fornece um framework de controle concreto para critérios de disponibilidade e segurança.
- **ISO 27001:** Ajuda a estruturar os controles do Anexo A em torno de acesso lógico e segurança operacional.
- **OWASP Web Top 10:** Complementar; sempre verifique ambas as listas. O Web Top 10 cobre injeção e criptografia, enquanto o API Top 10 cobre falhas lógicas e de negócio.

## Quando NÃO Usar o API Security Top 10

- É um **documento de conscientização**, não um padrão de conformidade rigoroso. Trate-o como um ponto de partida, não como uma checklist de auditoria exaustiva.
- Ele não cobre criptografia, logging ou segurança física em detalhes (consulte ASVS ou MASVS para isso).
- **Não** substitui um modelo de ameaças adaptado à sua arquitetura específica.

## Principais Conclusões

| Risco | Mitigação Principal | Exemplo de Teste |
|-------|---------------------|------------------|
| BOLA | Exija verificações estritas de propriedade para cada acesso a objeto. | Trocar IDs em requisições GET. |
| BOPLA | Use DTOs/ViewModels; nunca passe objetos de usuário diretamente para o ORM. | Injetar campos `role` ou `admin`. |
| SSRF | Negue listas de IPs privados; permita listas de destinos de saída. | Buscar endpoints de metadados (`169.254.169.254`). |
| Fluxos de Negócio | Limitação de taxa + CAPTCHA para ações sensíveis. | Automatizar checkout 100 vezes. |
| Inventário | Mantenha um catálogo de API vivo no seu pipeline CI. | Crawler por `v1/`, `swagger.json`, `/debug`. |

## Referências

- Projeto Oficial de Segurança de API do OWASP: [https://github.com/OWASP/API-Security](https://github.com/OWASP/API-Security)
- OWASP Top 10 Web (2021): [https://owasp.org/Top10/](https://owasp.org/Top10/)
- Escaneamento de API do OWASP ZAP: [https://www.zaproxy.org/docs/docker/api-scan/](https://www.zaproxy.org/docs/docker/api-scan/)
- Regras Semgrep para Segurança de API: [https://semgrep.dev](https://semgrep.dev/)

---

*Status: rascunho. Última atualização: 2026-06-25.*