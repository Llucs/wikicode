---
title: OWASP API Security Top 10
description: Ein umfassendes Entwickler-Wiki, das die OWASP API Security Top Ten (2023) abdeckt, einschließlich tiefergehender Analysen, Teststrategien und CI/CD-Integration.
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

Die **OWASP API Security Top 10** ist ein branchenweit anerkanntes Sensibilisierungsdokument, das vom Open Web Application Security Project (OWASP) veröffentlicht und 2023 aktualisiert wurde, um die einzigartigen Sicherheitsrisiken moderner REST-, GraphQL-, gRPC- und SOAP-APIs widerzuspiegeln. Anders als die allgemeine OWASP Web Top 10 (die XSS, SQLi, CSRF usw. abdeckt) konzentriert sich diese Liste **ausschließlich** auf die Architektur- und Logikfehler, die API-gesteuerte Anwendungen plagen.

Stand 2026 bleiben API-bezogene Fehler der häufigste Vektor für Datenschutzverletzungen, wobei Vorfälle bei großen Unternehmen (Twitter, T-Mobile, Optus) auf eine Handvoll vermeidbarer Fehler zurückgeführt werden, die in diesem Rahmenwerk dokumentiert sind.

---

## Die Top 10 API-Sicherheitsrisiken (2023)

| Rang | Name | Akronym | Kernproblem |
|------|------|---------|--------------|
| API1 | Broken Object Level Authorization | BOLA | Zugriff auf Objekte, die anderen Benutzern gehören, ohne ordnungsgemäße ACL-Prüfungen |
| API2 | Broken Authentication | — | Schwaches Credential-Management, Token-Leckage, Session Fixation |
| API3 | Broken Object Property Level Authorization | BOPLA | Massenzuweisung / Übermittlung sensibler Felder |
| API4 | Unrestricted Resource Consumption | — | Fehlendes Rate Limiting, Paginierungsbegrenzungen oder Durchsetzung der Nutzlastgröße |
| API5 | Broken Function Level Authorization | BFLA | Aufruf von Admin-Endpunkten mit hohen Privilegien als Standardbenutzer |
| API6 | Unrestricted Access to Sensitive Business Flows | — | Bots, die gültige API-Workflows ausnutzen (Scalping, Scraping) |
| API7 | Server Side Request Forgery | SSRF | Vom Benutzer kontrollierte URLs, die von der API abgerufen werden, ermöglichen das Ausspähen interner Dienste |
| API8 | Security Misconfiguration | — | Standard-Anmeldeinformationen, ausführliche Fehler, fehlendes CORS, ungepatchte Systeme |
| API9 | Improper Inventory Management | — | Zombie-/veraltete API-Versionen, vergessene Debug-Endpunkte, Schatten-APIs |
| API10 | Unsafe Consumption of APIs | — | Blindes Vertrauen in Drittanbieter-API-Antworten (Lieferkettenrisiko) |

### Bemerkenswerte Änderungen seit 2019

Die Ausgabe 2023 entfernte generische Web-Bedrohungen (XSS, SQLi – jetzt im Standard Top 10 abgedeckt) und führte fünf völlig neue Kategorien ein: **BOPLA**, **Unrestricted Business Flows**, **SSRF**, **Improper Inventory Management** und **Unsafe Consumption**.

Es formalisierte auch die **"Lather, Rinse, Repeat"**-Methodik – einen kontinuierlichen Kreislauf aus Discovery → Validation → Remediation.

---

## Einführungsmethodik

Da es sich um ein *Framework* (kein Softwarepaket) handelt, bedeutet "Installation" die Integration der Denkweise und der Testabläufe in Ihren Entwicklungslebenszyklus.

### Phase 1: Discovery & Inventory (behandelt API9)

Erfassen Sie jeden Endpunkt, seine Datensensitivität, den Authentifizierungsmechanismus und die Version. Dies ist der am meisten übersehene Schritt.

```bash
# A simple discovery scan for common API paths
for endpoint in /api/v1 /api/v2 /api/v3 /graphql /rest /soap /debug /health /swagger.json /openapi.json; do
  status=$(curl -o /dev/null -s -w "%{http_code}\n" "http://target.com${endpoint}")
  echo "Endpoint ${endpoint} returned ${status}"
done
```

Tools: Postman, Swagger Inspector, Burp Suite, benutzerdefinierte Crawler.

### Phase 2: Automatisiertes Scannen

Führen Sie dynamische Scanner gegen Ihre API-Spezifikation aus.

```bash
# OWASP ZAP API scanning
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py -t file:///zap/wrk/openapi.yaml -f openapi -r report.html
```

**Wichtige automatisch durchzuführende Prüfungen:**
- **BOLA:** Austauschen von Objekt-IDs in Batch-Anfragen.
- **BFLA:** Versuchen Sie DELETE/PUT auf Admin-Endpunkten mit Token mit niedrigen Berechtigungen.
- **SSRF:** Injizieren Sie `http://169.254.169.254/metadata/instance` in URL-Parameter.
- **Fehlkonfiguration:** Überprüfen Sie auf `Access-Control-Allow-Origin: *` und ausführliche Fehlerantworten.

### Phase 3: Manuelles Deep Dive (Pentest-Modus)

Verwenden Sie die Top 10 als Checkliste.

#### API1: Broken Object Level Authorization (BOLA)

```bash
# Attempt to access another user's data by changing the ID in the URL
curl -X GET https://api.example.com/api/v1/users/123 \
  -H "Authorization: Bearer valid_token_for_user_456"
# If the response contains data for user 123, you have a BOLA vulnerability.
```

Wenn die Antwort Daten für Benutzer 123 enthält, liegt eine BOLA-Sicherheitslücke vor.

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

### Phase 4: CI/CD-Integration

Betten Sie die Prüfungen in Ihre Pipeline ein. Eine typische sichere Pipeline-Stufe sieht wie folgt aus:

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

#### Beispiel: Semgrep-Regel für BOPLA (Mass Assignment in Django)

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

#### Beispiel: Rate-Limiting-Middleware (Go)

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

## Die „Lather, Rinse, Repeat“-Methodik

In der Ausgabe 2023 stark hervorgehoben, betont dieses Konzept, dass API-Sicherheit **kein einmaliger Pentest** ist, sondern ein kontinuierlicher Kreislauf:

1. **Lather:** Entdecken Sie Ihre gesamte API-Oberfläche (einschließlich Schatten-APIs).
2. **Rinse:** Validieren Sie die Ergebnisse durch automatisierte und manuelle Tests.
3. **Repeat:** Führen Sie einen erneuten Scan durch, sobald ein neuer Endpunkt oder eine neue Version bereitgestellt wird.

Dies bekämpft direkt **API9 (Improper Inventory Management)** und stellt sicher, dass die Sicherheitslage mit der Codebasis Schritt hält.

## Beziehung zu anderen Standards

- **PCI DSS 4.0:** Erfordert robuste API-Sicherheitskontrollen (einschließlich BOLA/BFLA-Tests) für Umgebungen mit Karteninhaberdaten.
- **SOC 2:** Die Top 10 bietet einen konkreten Kontrollrahmen für Verfügbarkeits- und Sicherheitskriterien.
- **ISO 27001:** Hilft bei der Strukturierung der Anhang-A-Kontrollen für logischen Zugriff und operative Sicherheit.
- **OWASP Web Top 10:** Ergänzend; überprüfen Sie immer beide Listen. Die Web Top 10 deckt Injection und Kryptographie ab, während die API Top 10 Logik- und Geschäftsfehler abdeckt.

## Wann Sie die API Security Top 10 NICHT verwenden sollten

- Es ist ein **Sensibilisierungsdokument**, kein strenger Compliance-Standard. Behandeln Sie es als Ausgangspunkt, nicht als erschöpfende Audit-Checkliste.
- Es deckt Kryptographie, Protokollierung oder physische Sicherheit nicht im Detail ab (siehe dazu ASVS oder MASVS).
- Es ist *kein* Ersatz für ein auf Ihre spezifische Architektur zugeschnittenes Bedrohungsmodell.

## Wichtige Erkenntnisse

| Risiko | Primäre Abhilfe | Beispieltest |
|------|--------------------|--------------|
| BOLA | Strenge Besitzprüfungen für jeden Objektzugriff erforderlich. | Austauschen von IDs in GET-Anfragen. |
| BOPLA | Verwenden Sie DTOs/ViewModels; übergeben Sie Benutzerobjekte niemals direkt an das ORM. | Injizieren von `role`- oder `admin`-Feldern. |
| SSRF | Private IP-Bereiche auf die Blockliste setzen; ausgehende Ziele auf die Whitelist setzen. | Abrufen von Metadaten-Endpunkten (`169.254.169.254`). |
| Business Flows | Rate Limiting + CAPTCHA für sensible Aktionen. | Automatisierung des Checkouts 100 Mal. |
| Inventory | Pflegen Sie einen lebenden API-Katalog in Ihrer CI-Pipeline. | Crawlen nach `v1/`, `swagger.json`, `/debug`. |

## Referenzen

- Official OWASP API Security Project: [https://github.com/OWASP/API-Security](https://github.com/OWASP/API-Security)
- OWASP Top 10 Web (2021): [https://owasp.org/Top10/](https://owasp.org/Top10/)
- OWASP ZAP API Scanning: [https://www.zaproxy.org/docs/docker/api-scan/](https://www.zaproxy.org/docs/docker/api-scan/)
- Semgrep Rules for API Security: [https://semgrep.dev](https://semgrep.dev)

---

*Status: Entwurf. Letzte Aktualisierung: 2026-06-25.*