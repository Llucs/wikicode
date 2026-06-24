---
title: Estratégias de Versionamento de API
description: Técnicas essenciais e melhores práticas para gerenciar mudanças em uma API ao longo do tempo sem quebrar clientes existentes, incluindo abordagens baseadas em URI, header, parâmetro de consulta e schema.
created: 2026-06-24
tags:
  - api-design
  - rest
  - versioning
  - architecture
  - backend
status: draft
---

# Estratégias de Versionamento de API

O versionamento de API é a prática de gerenciar mudanças em um contrato de API público ou interno para que os provedores possam evoluir a interface sem prejudicar os consumidores existentes. Ela permite que múltiplas representações do mesmo recurso sejam executadas em paralelo, equilibrando inovação e estabilidade. Escolher a estratégia correta—e implementá-la de forma consistente—é uma das decisões mais importantes no design de APIs.

Este guia aborda as técnicas de versionamento mais comuns, seus prós e contras, casos de uso reais e exemplos práticos de implementação para frameworks líderes. Você também aprenderá a lidar com depreciação e sunset com cabeçalhos de ciclo de vida adequados.

---

## Por que o Versionamento é Importante

Sem versionamento, cada mudança em uma API é arriscada:

- Adicionar um campo obrigatório pode quebrar clientes que enviam payloads antigos.
- Remover um endpoint pode causar paradas na produção.
- Alterar o formato de um campo de resposta (por exemplo, de string para inteiro) força todos os consumidores a se atualizarem simultaneamente.

Uma estratégia de versionamento fornece um **contrato**: clientes na versão `v1` têm garantia de uma interface estável, enquanto o provedor pode introduzir mudanças que quebram a compatibilidade na `v2`. Isso permite que as equipes entreguem rapidamente, mantendo a confiança dos consumidores.

### Contexto Histórico

- **APIs REST iniciais (meados dos anos 2000):** Flickr, Twitter e outros começaram a prefixar URIs com `/v1/` para clareza. SOAP dependia de esquemas WSDL estritos.
- **A dissertação de Roy Fielding** defendia o hypermedia (HATEOAS) como o mecanismo de versionamento "natural"—onde links guiam os clientes através de estados. No entanto, a complexidade fez com que o versionamento por URI se tornasse o padrão de facto.
- **GraphQL (2015)** promoveu uma abordagem "sem versão" usando depreciação de campos em vez de mudanças que quebram a compatibilidade.
- **gRPC** usa pacotes Protobuf e registries de schema para evolução de contrato.
- **A especificação OpenAPI** agora documenta múltiplas versões em um único arquivo de especificação, facilitando a criação e comparação de versões.

---

## Principais Estratégias

Todas as estratégias se situam em um espectro que vai de **identificadores de versão explícitos** (fáceis para consumidores) a **contratos implícitos** (limpos para provedores). Escolha com base na maturidade do seu ecossistema e na tolerância a mudanças que quebram a compatibilidade.

### 1. Versionamento por URI / Caminho

A versão é incorporada diretamente no caminho da URL, sendo a abordagem mais comum e direta.

```
GET /v1/users
GET /v2/users
```

**Prós**
- Simples de implementar e rotear.
- Altamente detectável—os consumidores veem a versão imediatamente.
- Cache excelente: versões diferentes podem ser armazenadas em cache de forma independente.
- Fácil de implantar em gateways de API e CDNs.

**Contras**
- Viola a semântica REST: uma URI deve identificar um recurso, não uma versão (de acordo com Fielding).
- Incentiva a ramificação do código do servidor se não for projetado com camadas.
- Não é possível versionar por representação (por exemplo, uma versão diferente para o mesmo recurso com base no header `Accept`).

**Exemplo de Implementação (Express.js)**

```javascript
// v1 router
const v1Router = require('./routes/v1');
app.use('/v1', v1Router);

// v2 router
const v2Router = require('./routes/v2');
app.use('/v2', v2Router);
```

**Exemplo de Implementação (ASP.NET Core)**

```csharp
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/[controller]")]
public class UsersController : ControllerBase
{
    [HttpGet]
    public IActionResult Get() => Ok("Users from v1");
}
```

### 2. Versionamento por Parâmetro de Consulta

Um parâmetro de consulta especifica a versão.

```
GET /users?version=1
GET /users?version=2
```

**Prós**
- Simples de adicionar sem alterar rotas.
- O padrão de URL permanece consistente entre as versões.

**Contras**
- Polui a semântica da consulta—`version` não é um filtro ou termo de consulta.
- Complica o cache porque o parâmetro altera a chave do cache.
- Fácil para os clientes esquecerem de incluir, levando a um fallback de versão não intencional.

**Exemplo de Implementação (Express.js)**

```javascript
app.get('/users', (req, res) => {
  const version = req.query.version || 1;
  switch(version) {
    case '1': return handleV1(req, res);
    case '2': return handleV2(req, res);
    default:  return res.status(400).json({ error: 'Invalid version' });
  }
});
```

### 3. Versionamento por Header

As informações da versão são transportadas nos cabeçalhos HTTP. Duas abordagens comuns:

| Abordagem               | Exemplo de Header                                   |
|------------------------|--------------------------------------------------|
| Custom header          | `X-API-Version: 1`                               |
| Accept header (vendor MIME type) | `Accept: application/vnd.myapi.v1+json` |

**Prós**
- Mais RESTful—a URL identifica o recurso, o header identifica a representação.
- URIs limpas que nunca mudam.
- Controle refinado: você pode versionar por tipo de mídia (por exemplo, `v1` JSON, `v2` XML).

**Contras**
- Baixa detectabilidade—difícil de testar em um navegador ou curl sem modificação de header.
- Aumenta a complexidade no lado do servidor devido ao roteamento baseado em headers.
- O cache pode ser complicado a menos que os headers `Vary` sejam configurados corretamente.

**Exemplo de Implementação (ASP.NET Core com Accept Header)**

```csharp
// In Startup.cs
services.AddApiVersioning(options =>
{
    options.ApiVersionReader = new MediaTypeApiVersionReader();
    options.AssumeDefaultVersionWhenUnspecified = true;
});

// Controller
[ApiVersion("1.0")]
[Route("api/users")]
public class UsersV1Controller : ControllerBase {}
```

**Exemplo de Implementação (Spring Boot)**

```java
@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v1+json")
public class UserControllerV1 { ... }

@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v2+json")
public class UserControllerV2 { ... }
```

### 4. Versionamento por Código / Schema (Sem Versão Explícita)

Frequentemente chamada de "sem versão" ou "contrato primeiro". Em vez de expor um identificador de versão, o provedor da API mantém compatibilidade com versões anteriores adicionando apenas campos ou endpoints. Mudanças que quebram a compatibilidade são comunicadas por meio de registries de schema (por exemplo, Protobuf, Avro) ou pela introdução de um novo endpoint/operação.

```
// Protobuf package versioning
package myapi.v1;
message User {
  string name = 1;
}

// Later, in v2:
message User {
  string name = 1;
  string email = 2;
}
```

**Prós**
- Não é necessário manter vários caminhos de roteamento.
- Incentiva a compatibilidade contínua com versões anteriores.
- Bom para microsserviços internos e sistemas orientados a eventos.

**Contras**
- Não é possível comunicar mudanças intencionais que quebram a compatibilidade sem um indicador de versão.
- Torna-se um fardo de manutenção se a compatibilidade com versões anteriores for quebrada não intencionalmente.

**Melhor para:**
- Microsserviços internos onde consumidores e provedores estão na mesma organização.
- Esquemas GraphQL que usam a diretiva `@deprecated`.
- Sistemas orientados a eventos com registries de schema (Confluent Schema Registry, AWS Glue).

---

## Casos de Uso por Indústria

| Caso de Uso | Estratégia Preferida | Justificativa |
|------------|---------------------|---------------|
| **APIs Públicas (Stripe, Twilio)** | Versionamento por URI | Os clientes precisam de contratos explícitos e estáveis; o cache é simples. |
| **Backends para celular (Facebook, Twitter)** | Versionamento por Header (personalizado) | O aplicativo envia a versão com a qual foi compilado; a URL nunca muda, evitando pressão de atualização na loja de aplicativos. |
| **Microsserviços internos** | Sem versão / Protobuf | Registries de schema garantem a compatibilidade; não é necessário manter várias versões de endpoint. |
| **Sistemas orientados a eventos** | Schema Registry (Avro/Protobuf) | Contratos de dados evoluem independentemente; os consumidores validam com base no ID do schema. |

---

## Instalação e Configuração

Versionamento é um **padrão de projeto**, mas requer ferramentas para impor roteamento, validação e documentação. Abaixo estão as etapas de instalação para ambientes comuns.

### ASP.NET Core

Adicione o pacote NuGet `Microsoft.AspNetCore.Mvc.Versioning` e configure:

```csharp
// Installation: dotnet add package Microsoft.AspNetCore.Mvc.Versioning
// In Startup.cs:
public void ConfigureServices(IServiceCollection services)
{
    services.AddControllers();
    services.AddApiVersioning(options =>
    {
        options.DefaultApiVersion = new ApiVersion(1, 0);
        options.AssumeDefaultVersionWhenUnspecified = true;
        options.ReportApiVersions = true;
    });
}
```

### Express.js

Nenhuma biblioteca necessária. Crie roteadores por versão e monte-os:

```javascript
// Installation: npm i express (no extra lib needed)
const express = require('express');
const app = express();

const v1Router = require('./routes/v1');
const v2Router = require('./routes/v2');

app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

app.listen(3000);
```

### Spring Boot

O Spring Boot oferece suporte nativo a versionamento por header e por URI via `@RequestMapping`. Para versionamento pelo header Accept, você pode definir controladores separados com diferentes atributos `produces`.

```java
// POM dependency: spring-boot-starter-web (includes Spring MVC)
// For media type versioning, controllers produce different vendor MIME types:
@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v1+json")
public class UserControllerV1 { ... }
```

### API Gateways (Kong, AWS API Gateway)

Configure regras de roteamento a montante do código da sua aplicação:

- **Kong:** Defina serviços e rotas com caminhos específicos (`/v1/`, `/v2/`). Você também pode remover o prefixo do caminho antes de encaminhar para o backend.
- **AWS API Gateway:** Crie estágios ou recursos com parâmetros de caminho como `{proxy+}` e versionamento no caminho. Ou use um header `version` e roteie com um modelo de mapeamento.

```yaml
# Kong declarative config (YAML)
services:
  - name: users-api
    routes:
      - name: users-v1
        paths:
          - /v1/users
        strip_path: true
        service: users-api-v1-upstream
      - name: users-v2
        paths:
          - /v2/users
        strip_path: true
        service: users-api-v2-upstream
```

---

## Melhores Práticas

### 1. Seja Consistente
Escolha uma estratégia por área de superfície da API. Misturar versionamento por URI e por header entre endpoints leva à confusão.

### 2. Versionar o Contrato, Não a Implementação
Sua especificação OpenAPI (ou equivalente) deve ser a fonte da verdade. Mudanças no contrato exigem uma nova versão, não alterações no código interno.

### 3. Prefira Compatibilidade com Versões Anteriores (Mas Não Tema Mudanças que Quebram)
Quando possível, adicione novos campos em vez de remover ou renomear os existentes. Use marcadores `@deprecated` em sua especificação. No entanto, mudanças que quebram a compatibilidade são às vezes necessárias—o versionamento é a rede de segurança.

### 4. Use Cabeçalhos de Ciclo de Vida Explícitos
Quando uma versão for descontinuada, retorne estes cabeçalhos inspirados em RFC:

- `Deprecation: Sat, 01 Jan 2025 00:00:00 GMT` – indica que a versão está depreciada.
- `Sunset: Wed, 01 Jul 2026 00:00:00 GMT` – indica quando a versão será removida.
- `Link: </v2/users>; rel="successor-version"` – aponta para a substituição.

**Exemplo de conjunto de cabeçalhos de resposta:**

```http
HTTP/1.1 200 OK
Content-Type: application/json
Deprecation: true
Sunset: Wed, 01 Jul 2026 00:00:00 GMT
Link: </v2/users>; rel="successor-version"
```

### 5. Trate Seu Contrato de API com Versionamento Semântico
Use a semântica `MAJOR.MINOR.PATCH`:

- **Major:** mudanças que quebram → nova versão (por exemplo, `/v2/`).
- **Minor:** mudanças aditivas e compatíveis com versões anteriores (por exemplo, novos campos no corpo, novos endpoints).
- **Patch:** correções ou melhorias não funcionais.

### 6. Documente Tudo
Inclua a estratégia de versionamento no campo `info.version` da sua especificação OpenAPI e forneça guias de migração entre versões.

```yaml
openapi: 3.0.0
info:
  title: My API
  version: 2.0.0
  description: |
    ## Versioning
    This API uses URI path versioning. All requests must include the version in the URL path, e.g., `/v2/users`.
    See the [migration guide](/docs/migration) for changes from v1 to v2.
```

### 7. Automatize a Aplicação do Sunset
Use gateways de API ou middleware para rejeitar chamadas a versões depreciadas após uma data limite. Retorne `410 Gone` com um link para a versão mais recente.

---

## Ciclo de Vida da Depreciação

Uma API versionada totalmente gerenciada passa por estes estágios:

1. **Ativa** – a versão é a padrão ou explicitamente chamável.
2. **Depreciada** – a versão ainda funciona, mas retorna o header `Deprecation`. Os consumidores devem ver um banner na documentação.
3. **Sunset** – a versão será removida em uma data específica. Retorna ambos os headers `Deprecation` e `Sunset`.
4. **Removida** – o endpoint retorna `410 Gone` (não `404`). A data de `Sunset` já passou.

**Exemplo de middleware (Express.js) para cabeçalhos de depreciação automáticos:**

```javascript
const deprecatedVersions = {
  v1: { deprecatedAt: new Date('2025-01-01'), sunsetAt: new Date('2026-07-01'), successor: '/v2/users' }
};

app.use((req, res, next) => {
  const match = req.path.match(/^\/v(\d+)/);
  if (match && deprecatedVersions[`v${match[1]}`]) {
    const info = deprecatedVersions[`v${match[1]}`];
    res.set('Deprecation', info.deprecatedAt.toUTCString());
    res.set('Sunset', info.sunsetAt.toUTCString());
    if (info.successor) {
      res.set('Link', `<${info.successor}>; rel="successor-version"`);
    }
  }
  next();
});
```

---

## Conclusão

O versionamento de API é uma decisão estratégica que afeta todos os consumidores da sua API. Não existe uma estratégia única para todos; a escolha correta depende da sua base de consumidores, ecossistema e tolerância a riscos.

| Estratégia | Quando Escolher |
|------------|----------------|
| **URI / Caminho** | APIs públicas, onde a detectabilidade e o caching são primordiais. |
| **Parâmetro de Consulta** | Casos de uso simples com consumidores internos, onde a flexibilidade é necessária. |
| **Header (Accept / Custom)** | Aplicativos móveis, clientes de longa duração ou quando você deseja URIs limpas. |
| **Sem Versão / Schema** | Serviços internos, arquiteturas orientadas a eventos ou GraphQL. |

Independentemente da estratégia, invista em documentação clara, cabeçalhos de ciclo de vida e depreciação gradual. Uma API bem versionada gera confiança e permite que sua plataforma evolua sem quebrar o ecossistema que depende dela.

> **Leitura Adicional**
> - [REST API Versioning da Microsoft](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design#versioning)
> - [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
> - [RFC 8594: Sunset Header](https://tools.ietf.org/html/rfc8594)
> - [Padrões de Design de API – Capítulo sobre Versionamento](https://www.manning.com/books/api-design-patterns)