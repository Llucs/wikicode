---
title: API版本化策略
description: 管理API随时间变化而不破坏现有客户端的基本技术和最佳实践，包括基于URI、基于头部、基于查询参数和基于模式的方法。
created: 2026-06-24
tags:
  - api-design
  - rest
  - versioning
  - architecture
  - backend
status: draft
---

# API版本化策略

API版本化是管理公共或内部API契约变更的实践，使得提供者能够在不干扰现有消费者的情况下演进接口。它允许同一资源的多种表示并行运行，在创新与稳定性之间取得平衡。选择合适的策略——并持续实施——是API设计中最重要的决策之一。

本指南涵盖了最常见的版本化技术、它们的权衡、实际使用案例以及主流框架的实用实现示例。您还将学习如何使用适当的生命周期头部处理弃用和退役。

---

## 为什么版本化很重要

没有版本化，对API的每次更改都存在风险：

- 添加必需字段可能会破坏发送旧负载的客户端。
- 移除端点可能导致生产中断。
- 更改响应字段的格式（例如，string改为integer）会强制所有消费者同时更新。

版本化策略提供了一个**契约**：使用版本`v1`的客户端获得稳定接口的保证，而提供者可以在`v2`中引入破坏性更改。这使得团队能够在保持消费者信任的同时快速交付。

### 历史背景

- **早期REST API（2000年代中期）：** Flickr、Twitter等开始为清晰起见，在URI前加上`/v1/`。SOAP则依赖严格的WSDL模式。
- **Roy Fielding的论文**倡导使用超媒体（HATEOAS）作为“自然”的版本化机制——其中链接引导客户端遍历状态。然而，复杂性使得URI版本化成为事实标准。
- **GraphQL（2015）** 通过使用字段弃用而不是破坏性更改，推广了“无版本”方法。
- **gRPC** 使用Protobuf包和模式注册表来实现契约演进。
- **OpenAPI规范** 现在可以在单个规范文件中记录多个版本，从而更容易编写和比较版本。

---

## 主要策略

所有策略都分布在一个从**显式版本标识符**（对消费者友好）到**隐式契约**（对提供者简洁）的谱系上。根据您生态系统的成熟度和对破坏性更改的容忍度来选择。

### 1. URI / 路径版本化

版本直接嵌入到URL路径中，是最常见和直接的方法。

```
GET /v1/users
GET /v2/users
```

**优点**
- 易于实现和路由。
- 高可发现性——消费者立即可见版本。
- 出色的缓存：不同版本可以独立缓存。
- 易于在API网关和CDN上部署。

**缺点**
- 违反REST语义：根据Fielding的说法，URI应该标识资源，而不是版本。
- 如果未分层设计，会鼓励分支服务器代码。
- 无法按表示进行版本化（例如，根据`Accept`头对同一资源使用不同版本）。

**实现示例（Express.js）**

```javascript
// v1 router
const v1Router = require('./routes/v1');
app.use('/v1', v1Router);

// v2 router
const v2Router = require('./routes/v2');
app.use('/v2', v2Router);
```

**实现示例（ASP.NET Core）**

```csharp
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/[controller]")]
public class UsersController : ControllerBase
{
    [HttpGet]
    public IActionResult Get() => Ok("Users from v1");
}
```

### 2. 查询参数版本化

查询参数指定版本。

```
GET /users?version=1
GET /users?version=2
```

**优点**
- 易于添加，无需更改路由。
- URL模式在不同版本间保持一致。

**缺点**
- 污染查询语义——`version`不是过滤或查询项。
- 使缓存复杂化，因为参数会更改缓存键。
- 客户端容易忘记包含，导致意外的版本回退。

**实现示例（Express.js）**

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

### 3. 头部版本化

版本信息通过HTTP头部携带。两种常见方法：

| 方法               | 头部示例                                   |
|--------------------|--------------------------------------------|
| 自定义头部         | `X-API-Version: 1`                         |
| Accept头部（厂商MIME类型） | `Accept: application/vnd.myapi.v1+json` |

**优点**
- 最符合REST风格——URL标识资源，头部标识表示。
- 干净的URI，从不会更改。
- 细粒度控制：可以按媒体类型版本化（例如，`v1` JSON，`v2` XML）。

**缺点**
- 可发现性差——在不修改头部的情况下，在浏览器或curl中测试困难。
- 服务器端基于头部路由增加了复杂度。
- 除非正确设置`Vary`头，否则缓存可能很棘手。

**实现示例（ASP.NET Core 使用 Accept 头）**

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

**实现示例（Spring Boot）**

```java
@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v1+json")
public class UserControllerV1 { ... }

@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v2+json")
public class UserControllerV2 { ... }
```

### 4. 代码/模式版本化（无显式版本）

常被称为“无版本”或“契约优先”。API提供者不暴露版本标识符，而是仅通过添加字段或端点来保持向后兼容性。破坏性更改通过模式注册表（例如，Protobuf、Avro）或引入新端点/操作来传达。

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

**优点**
- 无需维护多个路由路径。
- 激励持续的向后兼容性。
- 适用于内部微服务和事件驱动系统。

**缺点**
- 没有版本指示符就无法传达有意的破坏性更改。
- 如果无意中破坏了向后兼容性，会变成维护负担。

**最适合：**
- 消费者和提供者位于同一组织的内部微服务。
- 使用`@deprecated`指令的GraphQL模式。
- 使用模式注册表的事件驱动系统（Confluent Schema Registry、AWS Glue）。

---

## 按行业划分的使用案例

| 使用案例 | 首选策略 | 理由 |
|----------|----------|------|
| **公共API（Stripe、Twilio）** | URI版本化 | 客户端需要明确、稳定的契约；缓存简单。 |
| **移动后端（Facebook、Twitter）** | 头部版本化（自定义） | 应用程序发送其编译时所带的版本；URL从未改变，避免了应用商店的更新压力。 |
| **内部微服务** | 无版本 / Protobuf | 模式注册表强制兼容性；无需维护多个端点版本。 |
| **事件驱动系统** | 模式注册表（Avro/Protobuf） | 数据契约独立演进；消费者根据模式ID进行验证。 |

---

## 安装与设置

版本化是一种**设计模式**，但它需要工具来实施路由、验证和文档。以下是常见环境的安装步骤。

### ASP.NET Core

添加`Microsoft.AspNetCore.Mvc.Versioning` NuGet包并进行配置：

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

无需库。为每个版本创建路由器并挂载：

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

Spring Boot原生支持通过`@RequestMapping`进行头部版本化和URI版本化。对于Accept头部版本化，您可以定义具有不同`produces`属性的单独控制器。

```java
// POM dependency: spring-boot-starter-web (includes Spring MVC)
// For media type versioning, controllers produce different vendor MIME types:
@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v1+json")
public class UserControllerV1 { ... }
```

### API网关（Kong、AWS API Gateway）

在应用代码上游配置路由规则：

- **Kong：** 使用特定路径（`/v1/`、`/v2/`）定义服务和路由。你还可以在转发到后端之前剥离路径前缀。
- **AWS API Gateway：** 创建带有路径参数（如`{proxy+}`）的阶段或资源，并在路径中进行版本化。或者使用`version`头部和映射模板进行路由。

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

## 最佳实践

### 1. 保持一致性
每个API表面对选择一个策略。跨端点混合使用URI和头部版本化会导致混乱。

### 2. 对契约进行版本化，而非实现
您的OpenAPI规范（或等效文档）应该是事实来源。契约的更改需要新版本，而不是对内部代码的更改。

### 3. 优先选择向后兼容（但不要害怕破坏性更改）
尽可能添加新字段，而不是删除或重命名现有字段。在规范中使用`@deprecated`标记。然而，破坏性更改有时是必要的——版本化就是安全网。

### 4. 使用显式的生命周期头部
当版本被弃用时，返回这些受RFC启发的头部：

- `Deprecation: Sat, 01 Jan 2025 00:00:00 GMT` – 表示该版本已被弃用。
- `Sunset: Wed, 01 Jul 2026 00:00:00 GMT` – 表示该版本将被移除的时间。
- `Link: </v2/users>; rel="successor-version"` – 指向替代版本。

**示例响应头部集：**

```http
HTTP/1.1 200 OK
Content-Type: application/json
Deprecation: true
Sunset: Wed, 01 Jul 2026 00:00:00 GMT
Link: </v2/users>; rel="successor-version"
```

### 5. 使用语义化版本对待您的API契约
使用`MAJOR.MINOR.PATCH`语义：

- **主版本（Major）：** 破坏性更改 → 新版本（例如，`/v2/`）。
- **次版本（Minor）：** 新增、向后兼容的更改（例如，请求体中的新字段、新端点）。
- **补丁（Patch）：** 修复或非功能性改进。

### 6. 记录一切
在OpenAPI规范的`info.version`字段中包含版本化策略，并提供版本间的迁移指南。

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

### 7. 自动化退役执行
使用API网关或中间件在截止日期后拒绝调用已弃用的版本。返回`410 Gone`并附带最新版本的链接。

---

## 弃用生命周期

一个完全托管的版本化API经历以下阶段：

1. **活跃（Active）** – 版本是默认或明确可调用的。
2. **弃用（Deprecated）** – 版本仍然工作，但返回`Deprecation`头部。消费者应在文档中看到横幅。
3. **退役（Sunset）** – 版本将在特定日期移除。返回`Deprecation`和`Sunset`两个头部。
4. **已移除（Removed）** – 端点返回`410 Gone`（而不是`404`）。`Sunset`日期已过。

**自动弃用头部的中间件示例（Express.js）：**

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

## 结论

API版本化是一项战略决策，影响API的每一个消费者。没有放之四海而皆准的策略；正确的选择取决于您的消费者基础、生态系统和风险承受能力。

| 策略 | 何时选择 |
|------|----------|
| **URI / 路径** | 公共API，其中可发现性和缓存至关重要。 |
| **查询参数** | 内部消费者的简单用例，需要灵活性。 |
| **头部（Accept / 自定义）** | 移动应用、长期存在的客户端，或者当你想要干净的URI时。 |
| **无版本 / 模式** | 内部服务、事件驱动架构或GraphQL。 |

无论采用何种策略，都应投资于清晰的文档、生命周期头部和逐步弃用。一个良好版本化的API能够建立信任，并允许您的平台在不破坏依赖它的生态系统的情况下演进。

> **进一步阅读**
> - [REST API版本化（Microsoft）](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design#versioning)
> - [OpenAPI规范](https://spec.openapis.org/oas/latest.html)
> - [RFC 8594: Sunset Header](https://tools.ietf.org/html/rfc8594)
> - [API设计模式——版本化章节](https://www.manning.com/books/api-design-patterns)