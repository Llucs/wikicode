---
title: OWASP API 安全 Top 10
description: 涵盖 OWASP API 安全 Top 10（2023）的综合性开发者指南，包括深入探讨、测试策略和 CI/CD 集成。
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

# OWASP API 安全 Top 10

**OWASP API 安全 Top 10** 是由开放 Web 应用程序安全项目（OWASP）发布的行业标准意识文档，于 2023 年更新，反映了现代 REST、GraphQL、gRPC 和 SOAP API 的独特安全风险。与通用的 OWASP Web Top 10（涵盖 XSS、SQLi、CSRF 等）不同，本列表**仅**关注困扰 API 驱动应用程序的架构和逻辑缺陷。

截至 2026 年，API 相关故障仍是数据泄露的主要因素，Twitter、T-Mobile、Optus 等大公司的安全事件均能追溯到此框架中记载的少数可预防错误。

---

## 2023 年 API 安全十大风险

| 排名 | 名称 | 缩写 | 核心问题 |
|------|------|---------|--------------|
| API1 | 对象级授权失效 | BOLA | 未进行适当的 ACL 检查即可访问其他用户的对象 |
| API2 | 身份认证失效 | — | 凭证管理薄弱、令牌泄露、会话固定 |
| API3 | 对象属性级授权失效 | BOPLA | 敏感字段的批量赋值/过度提交 |
| API4 | 资源消耗无限制 | — | 缺少速率限制、分页上限或有效载荷大小限制 |
| API5 | 功能级授权失效 | BFLA | 以普通用户身份调用高权限管理员端点 |
| API6 | 敏感业务流的无限制访问 | — | 机器人利用有效的 API 工作流（票务抢购、数据抓取） |
| API7 | 服务器端请求伪造 | SSRF | API 获取用户控制的 URL，允许探测内部服务 |
| API8 | 安全配置错误 | — | 默认凭据、详细错误、CORS 缺失、系统未修补 |
| API9 | 库存管理不当 | — | 僵尸/弃用 API 版本、遗忘的调试端点、影子 API |
| API10 | 不安全的 API 消费 | — | 盲目信任第三方 API 响应（供应链风险） |

### 2019 版的显著变化

2023 版移除了通用 Web 威胁（XSS、SQLi——现由标准 Top 10 涵盖），并引入了五个全新类别：**BOPLA**、**无限制业务流**、**SSRF**、**不当库存管理**和**不安全消费**。

还正式提出了 **“洗、冲、重复”** 方法论——一个持续循环的发现（Discovery）→ 验证（Validation）→ 修复（Remediation）。

---

## 采用方法论

由于这是一个**框架**（而非软件包），“安装”意味着将相关思维和测试流程整合到你的开发生命周期中。

### 阶段 1：发现与库存 (针对 API9)

映射每个端点、其数据敏感性、认证机制和版本。这是最容易被忽视的步骤。

```bash
# 对常见 API 路径进行简单的发现扫描
for endpoint in /api/v1 /api/v2 /api/v3 /graphql /rest /soap /debug /health /swagger.json /openapi.json; do
  status=$(curl -o /dev/null -s -w "%{http_code}\n" "http://target.com${endpoint}")
  echo "端点 ${endpoint} 返回了 ${status}"
done
```

工具：Postman、Swagger Inspector、Burp Suite、自定义爬虫。

### 阶段 2：自动化扫描

针对你的 API 规范运行动态扫描器。

```bash
# OWASP ZAP API 扫描
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py -t file:///zap/wrk/openapi.yaml -f openapi -r report.html
```

**要自动运行的关键检查：**
- **BOLA：** 在批量请求中替换对象 ID。
- **BFLA：** 尝试以低权限令牌对管理员端点执行 DELETE/PUT 操作。
- **SSRF：** 向 URL 参数注入 `http://169.254.169.254/metadata/instance`。
- **安全配置错误：** 检查 `Access-Control-Allow-Origin: *` 和详细的错误响应。

### 阶段 3：手动深入检查 (渗透测试模式)

将 Top 10 作为检查清单使用。

#### API1：对象级授权失效 (BOLA)

```bash
# 尝试通过更改 URL 中的 ID 来访问其他用户的数据
curl -X GET https://api.example.com/api/v1/users/123 \
  -H "Authorization: Bearer valid_token_for_user_456"
# 如果响应中包含用户 123 的数据，则存在 BOLA 漏洞。
```

#### API3：对象属性级授权失效 (BOPLA)

```bash
# Mass assignment: try to add "role":"admin" or "salary":100000 to a PATCH
curl -X PATCH https://api.example.com/api/v1/user/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"test","role":"admin","salary":999999}'
```

#### API6：无限制业务流

```python
import requests
# Simulate a bot abusing a voting / coupon / checkout flow
url = "https://ticketing.example.com/api/v2/checkout"
payload = {"event_id": 1, "quantity": 1}
session = requests.Session()
session.headers.update({"Authorization": "Bearer valid_token"})

for i in range(100):
    r = session.post(url, json=payload)
    print(f"Attempt {i}: {r.status_code} - {r.text[:100]}")
    # If all 100 succeed without rate limiting, API6 is present.
```

### 阶段 4：CI/CD 集成

将检查嵌入到你的流水线中。一个典型的安全流水线阶段如下所示：

```yaml
# .gitlab-ci.yml (GitLab CI) 或等效的 GitHub Actions
api-security:
  stage: test
  script:
    # 针对 BOPLA 模式的静态分析
    - semgrep --config=auto .
    # 使用 ZAP 进行动态扫描
    - docker run -v $(pwd):/zap/wrk/ zaproxy/zap-stable \
        zap-api-scan.py -t http://staging/api/openapi.json -f openapi
    # 速率限制/业务流滥用测试 (k6)
    - k6 run tests/abuse.js
  only:
    - branches
```

#### 示例：Semgrep 规则 (Django 中的 BOPLA / 批量赋值)

```yaml
rules:
  - id: mass-assignment-django
    patterns:
      - pattern-either:
          - pattern: Model.objects.update(...)  # Unsafe if not filtering fields
          - pattern: serializer.save(...)
    message: >
      Potential Mass Assignment vulnerability (API3 / BOPLA).
      Explicitly define allowed fields using `fields` or `read_only_fields` in the serializer.
    severity: WARNING
    languages:
      - python
```

#### 示例：速率限制中间件 (Go)

```go
import (
    "golang.org/x/time/rate"
    "net/http"
)

var limiter = rate.NewLimiter(rate.Limit(100), 200) // 100 requests/s, burst 200

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

## “洗、冲、重复”方法论

此概念在 2023 版中被重点强调，它指出 API 安全**不是一次性的渗透测试**，而是一个持续循环：

1. **洗：** 发现你的整个 API 表面（包括影子 API）。
2. **冲：** 通过自动化和手动测试验证发现。
3. **重复：** 每当部署新端点或新版本时重新扫描。

这直接应对了 **API9（不当库存管理）**，并确保安全态势随代码库同步演化。

## 与其他标准的关系

- **PCI DSS 4.0：** 要求对持卡人数据环境实施强大的 API 安全控制（包括 BOLA/BFLA 测试）。
- **SOC 2：** Top 10 为可用性和安全标准提供了具体的控制框架。
- **ISO 27001：** 有助于围绕逻辑访问和操作安全构建附录 A 控制。
- **OWASP Web Top 10：** 相互补充；始终检查两个列表。Web Top 10 涵盖注入和密码学，而 API Top 10 涵盖逻辑和业务缺陷。

## 何时不使用 API 安全 Top 10

- 它是一个**意识文档**，不是严格的合规标准。将其视为起点，而非详尽的审计检查清单。
- 它不详细涵盖密码学、日志记录或物理安全（请参考 ASVS 或 MASVS）。
- 它**不能替代**针对你特定架构量身定制的威胁模型。

## 关键要点

| 风险 | 主要缓解措施 | 示例测试 |
|------|--------------------|--------------|
| BOLA | 要求对每个对象访问进行严格的所有权检查。 | 在 GET 请求中替换 ID。 |
| BOPLA | 使用 DTO/ViewModel；永远不要直接将用户对象传递给 ORM。 | 注入 `role` 或 `admin` 字段。 |
| SSRF | 禁止列表私有 IP 范围；允许列表出站目标。 | 获取元数据端点（`169.254.169.254`）。 |
| 业务流 | 对敏感操作进行速率限制 + CAPTCHA 验证。 | 自动化结账 100 次。 |
| 库存管理 | 在 CI 流水线中维护一个活跃的 API 目录。 | 爬取 `v1/`、`swagger.json`、`/debug`。 |

## 参考文献

- OWASP API 安全项目官方：[https://github.com/OWASP/API-Security](https://github.com/OWASP/API-Security)
- OWASP Web Top 10 (2021) ：[https://owasp.org/Top10/](https://owasp.org/Top10/)
- OWASP ZAP API 扫描：[https://www.zaproxy.org/docs/docker/api-scan/](https://www.zaproxy.org/docs/docker/api-scan/)
- 用于 API 安全的 Semgrep 规则：[https://semgrep.dev](https://semgrep.dev)

---

*状态：草稿。最后更新：2026-06-25。*