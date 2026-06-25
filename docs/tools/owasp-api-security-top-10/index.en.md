---
title: OWASP API Security Top 10
description: A comprehensive developer wiki covering the OWASP API Security Top Ten (2023), including deep dives, testing strategies, and CI/CD integration.
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

The **OWASP API Security Top 10** is an industry-standard awareness document published by the Open Web Application Security Project (OWASP), updated in 2023 to reflect the unique security risks of modern REST, GraphQL, gRPC, and SOAP APIs. Unlike the general OWASP Web Top 10 (which covers XSS, SQLi, CSRF, etc.), this list focuses **exclusively** on the architectural and logical flaws that plague API-driven applications.

As of 2026, API-related failures remain the leading vector for data breaches, with incidents at major companies (Twitter, T-Mobile, Optus) tracing back to a handful of preventable mistakes documented in this framework.

---

## The Top 10 API Security Risks (2023)

| Rank | Name | Acronym | Core Problem |
|------|------|---------|--------------|
| API1 | Broken Object Level Authorization | BOLA | Accessing objects belonging to other users without proper ACL checks |
| API2 | Broken Authentication | — | Weak credential management, token leakage, session fixation |
| API3 | Broken Object Property Level Authorization | BOPLA | Mass assignment / over-posting of sensitive fields |
| API4 | Unrestricted Resource Consumption | — | Lack of rate limiting, pagination caps, or payload size enforcement |
| API5 | Broken Function Level Authorization | BFLA | Calling high-privilege admin endpoints as a standard user |
| API6 | Unrestricted Access to Sensitive Business Flows | — | Bots exploiting valid API workflows (scalping, scraping) |
| API7 | Server Side Request Forgery | SSRF | User-controlled URLs fetched by the API allow probing of internal services |
| API8 | Security Misconfiguration | — | Default credentials, verbose errors, missing CORS, unpatched systems |
| API9 | Improper Inventory Management | — | Zombie/deprecated API versions, forgotten debug endpoints, shadow APIs |
| API10 | Unsafe Consumption of APIs | — | Blindly trusting third-party API responses (supply chain risk) |

### Notable Changes from 2019

The 2023 edition removed generic web threats (XSS, SQLi—now covered by the standard Top 10) and introduced five entirely new categories: **BOPLA**, **Unrestricted Business Flows**, **SSRF**, **Improper Inventory Management**, and **Unsafe Consumption**.

It also formalised the **"Lather, Rinse, Repeat"** methodology—a continuous cycle of Discovery → Validation → Remediation.

---

## Adoption Methodology

Since this is a *framework* (not a software package), "installation" means integrating the mindset and testing flows into your development lifecycle.

### Phase 1: Discovery & Inventory (Addresses API9)

Map every endpoint, its data sensitivity, authentication mechanism, and version. This is the most overlooked step.

```bash
# A simple discovery scan for common API paths
for endpoint in /api/v1 /api/v2 /api/v3 /graphql /rest /soap /debug /health /swagger.json /openapi.json; do
  status=$(curl -o /dev/null -s -w "%{http_code}\n" "http://target.com${endpoint}")
  echo "Endpoint ${endpoint} returned ${status}"
done
```

Tools: Postman, Swagger Inspector, Burp Suite, custom crawlers.

### Phase 2: Automated Scanning

Run dynamic scanners against your API specification.

```bash
# OWASP ZAP API scanning
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py -t file:///zap/wrk/openapi.yaml -f openapi -r report.html
```

**Key checks to run automatically:**
- **BOLA:** Swap object IDs in bulk requests.
- **BFLA:** Attempt DELETE/PUT on admin endpoints as low-privilege tokens.
- **SSRF:** Inject `http://169.254.169.254/metadata/instance` into URL parameters.
- **Misconfiguration:** Check for `Access-Control-Allow-Origin: *` and verbose error responses.

### Phase 3: Manual Deep Dive (Pentest Mode)

Use the Top 10 as a checklist.

#### API1: Broken Object Level Authorization (BOLA)

```bash
# Attempt to access another user's data by changing the ID in the URL
curl -X GET https://api.example.com/api/v1/users/123 \
  -H "Authorization: Bearer valid_token_for_user_456"
# If the response contains data for user 123, you have a BOLA vulnerability.
```

#### API3: Broken Object Property Level Authorization (BOPLA)

```bash
# Mass assignment: try to add "role":"admin" or "salary":100000 to a PATCH
curl -X PATCH https://api.example.com/api/v1/user/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"test","role":"admin","salary":999999}'
```

#### API6: Unrestricted Business Flows

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

### Phase 4: CI/CD Integration

Embed the checks into your pipeline. A typical secure pipeline stage looks like this:

```yaml
# .gitlab-ci.yml (GitLab CI) or equivalent GitHub Actions
api-security:
  stage: test
  script:
    # Static Analysis for BOPLA patterns
    - semgrep --config=auto .
    # Dynamic Scan with ZAP
    - docker run -v $(pwd):/zap/wrk/ zaproxy/zap-stable \
        zap-api-scan.py -t http://staging/api/openapi.json -f openapi
    # Rate Limit / Business Flow abuse test (k6)
    - k6 run tests/abuse.js
  only:
    - branches
```

#### Example: Semgrep Rule for BOPLA (Mass Assignment in Django)

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

#### Example: Rate Limiting Middleware (Go)

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

## The "Lather, Rinse, Repeat" Methodology

Introduced heavily in the 2023 edition, this concept stresses that API security is **not a one-time pentest** but a continuous cycle:

1. **Lather:** Discover your entire API surface (including shadow APIs).
2. **Rinse:** Validate the findings through automated and manual testing.
3. **Repeat:** Re-scan whenever a new endpoint or version is deployed.

This directly combats **API9 (Improper Inventory Management)** and ensures that security posture evolves with the codebase.

## Relationship to Other Standards

- **PCI DSS 4.0:** Requires robust API security controls (including BOLA/BFLA testing) for cardholder data environments.
- **SOC 2:** The Top 10 provides a concrete control framework for availability and security criteria.
- **ISO 27001:** Helps structure Annex A controls around logical access and operational security.
- **OWASP Web Top 10:** Complementary; always check both lists. The Web Top 10 covers injection and cryptography, while the API Top 10 covers logic and business flaws.

## When NOT to Use the API Security Top 10

- It is an **awareness document**, not a strict compliance standard. Treat it as a starting point, not an exhaustive audit checklist.
- It does not cover cryptography, logging, or physical security in detail (refer to ASVS or MASVS for that).
- It is *not* a replacement for a threat model tailored to your specific architecture.

## Key Takeaways

| Risk | Primary Mitigation | Example Test |
|------|--------------------|--------------|
| BOLA | Require strict ownership checks for every object access. | Swapping IDs in GET requests. |
| BOPLA | Use DTOs/ViewModels; never pass user objects to the ORM directly. | Injecting `role` or `admin` fields. |
| SSRF | Deny-list private IP ranges; allow-list outbound destinations. | Fetching metadata endpoints (`169.254.169.254`). |
| Business Flows | Rate limiting + CAPTCHA for sensitive actions. | Automating checkout 100 times. |
| Inventory | Maintain a living API catalog in your CI pipeline. | Crawling for `v1/`, `swagger.json`, `/debug`. |

## References

- Official OWASP API Security Project: [https://github.com/OWASP/API-Security](https://github.com/OWASP/API-Security)
- OWASP Top 10 Web (2021): [https://owasp.org/Top10/](https://owasp.org/Top10/)
- OWASP ZAP API Scanning: [https://www.zaproxy.org/docs/docker/api-scan/](https://www.zaproxy.org/docs/docker/api-scan/)
- Semgrep Rules for API Security: [https://semgrep.dev](https://semgrep.dev/)

---

*Status: draft. Last updated: 2026-06-25.*