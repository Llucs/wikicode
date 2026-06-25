---
title: Top 10 de Seguridad de API de OWASP
description: Una wiki completa para desarrolladores que cubre el Top 10 de Seguridad de API de OWASP (2023), incluyendo análisis profundos, estrategias de pruebas e integración con CI/CD.
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

# Top 10 de Seguridad de API de OWASP

El **Top 10 de Seguridad de API de OWASP** es un documento de concienciación estándar de la industria publicado por el Open Web Application Security Project (OWASP), actualizado en 2023 para reflejar los riesgos de seguridad únicos de las API modernas REST, GraphQL, gRPC y SOAP. A diferencia del Top 10 Web general de OWASP (que cubre XSS, SQLi, CSRF, etc.), esta lista se centra **exclusivamente** en las fallas arquitectónicas y lógicas que afectan a las aplicaciones impulsadas por API.

A partir de 2026, las fallas relacionadas con API siguen siendo el vector principal de violaciones de datos, con incidentes en grandes empresas (Twitter, T-Mobile, Optus) que se remontan a un puñado de errores evitables documentados en este marco.

---

## Los 10 Principales Riesgos de Seguridad de API (2023)

| Rango | Nombre | Acrónimo | Problema Central |
|------|--------|----------|------------------|
| API1 | Autorización a Nivel de Objeto Rota | BOLA | Acceder a objetos que pertenecen a otros usuarios sin las comprobaciones de ACL adecuadas |
| API2 | Autenticación Rota | — | Gestión débil de credenciales, fuga de tokens, fijación de sesión |
| API3 | Autorización a Nivel de Propiedad de Objeto Rota | BOPLA | Asignación masiva / publicación excesiva de campos sensibles |
| API4 | Consumo Irrestricto de Recursos | — | Falta de limitación de velocidad, límites de paginación o control del tamaño del payload |
| API5 | Autorización a Nivel de Función Rota | BFLA | Llamar a endpoints de administrador con altos privilegios como usuario estándar |
| API6 | Acceso Irrestricto a Flujos de Negocio Sensibles | — | Bots que explotan flujos de trabajo válidos de la API (reventa, scraping) |
| API7 | Server Side Request Forgery | SSRF | URLs controladas por el usuario que son obtenidas por la API permiten sondear servicios internos |
| API8 | Configuración Incorrecta de Seguridad | — | Credenciales por defecto, errores detallados, falta de CORS, sistemas sin parches |
| API9 | Gestión Incorrecta del Inventario | — | Versiones de API zombie/obsoletas, endpoints de depuración olvidados, APIs ocultas |
| API10 | Consumo Inseguro de API | — | Confiar ciegamente en respuestas de API de terceros (riesgo de cadena de suministro) |

### Cambios Notables desde 2019

La edición de 2023 eliminó amenazas web genéricas (XSS, SQLi—ahora cubiertas por el Top 10 estándar) e introdujo cinco categorías completamente nuevas: **BOPLA**, **Flujos de Negocio Irrestrictos**, **SSRF**, **Gestión Incorrecta del Inventario** y **Consumo Inseguro de API**.

También formalizó la metodología **"Enjabonar, Enjuagar, Repetir"** —un ciclo continuo de Descubrimiento → Validación → Remediación.

---

## Metodología de Adopción

Dado que esto es un *framework* (no un paquete de software), la "instalación" significa integrar la mentalidad y los flujos de pruebas en tu ciclo de vida de desarrollo.

### Fase 1: Descubrimiento e Inventario (Aborda API9)

Mapea cada endpoint, su sensibilidad de datos, mecanismo de autenticación y versión. Este es el paso más pasado por alto.

```bash
# A simple discovery scan for common API paths
for endpoint in /api/v1 /api/v2 /api/v3 /graphql /rest /soap /debug /health /swagger.json /openapi.json; do
  status=$(curl -o /dev/null -s -w "%{http_code}\n" "http://target.com${endpoint}")
  echo "Endpoint ${endpoint} returned ${status}"
done
```

Herramientas: Postman, Swagger Inspector, Burp Suite, rastreadores personalizados.

### Fase 2: Escaneo Automatizado

Ejecuta escáneres dinámicos contra tu especificación de API.

```bash
# OWASP ZAP API scanning
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py -t file:///zap/wrk/openapi.yaml -f openapi -r report.html
```

**Verificaciones clave para ejecutar automáticamente:**
- **BOLA:** Intercambia IDs de objetos en solicitudes masivas.
- **BFLA:** Intenta DELETE/PUT en endpoints de administrador con tokens de bajo privilegio.
- **SSRF:** Inyecta `http://169.254.169.254/metadata/instance` en parámetros de URL.
- **Configuración Incorrecta:** Verifica `Access-Control-Allow-Origin: *` y respuestas de error detalladas.

### Fase 3: Inmersión Profunda Manual (Modo Pentest)

Usa el Top 10 como lista de verificación.

#### API1: Autorización a Nivel de Objeto Rota (BOLA)

```bash
# Attempt to access another user's data by changing the ID in the URL
curl -X GET https://api.example.com/api/v1/users/123 \
  -H "Authorization: Bearer valid_token_for_user_456"
# If the response contains data for user 123, you have a BOLA vulnerability.
```

#### API3: Autorización a Nivel de Propiedad de Objeto Rota (BOPLA)

```bash
# Mass assignment: try to add "role":"admin" or "salary":100000 to a PATCH
curl -X PATCH https://api.example.com/api/v1/user/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"test","role":"admin","salary":999999}'
```

#### API6: Flujos de Negocio Irrestrictos

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

### Fase 4: Integración CI/CD

Incorpora las verificaciones en tu pipeline. Una etapa típica de pipeline seguro tiene este aspecto:

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

#### Ejemplo: Regla Semgrep para BOPLA (Mass Assignment en Django)

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

#### Ejemplo: Middleware de Limitación de Velocidad (Go)

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

## La Metodología "Enjabonar, Enjuagar, Repetir"

Introducido fuertemente en la edición de 2023, este concepto enfatiza que la seguridad de API **no es una prueba de penetración única** sino un ciclo continuo:

1. **Enjabonar:** Descubre toda tu superficie de API (incluyendo APIs ocultas).
2. **Enjuagar:** Valida los hallazgos mediante pruebas automatizadas y manuales.
3. **Repetir:** Vuelve a escanear cada vez que se despliega un nuevo endpoint o versión.

Esto combate directamente **API9 (Gestión Incorrecta del Inventario)** y asegura que la postura de seguridad evoluciona con el código.

## Relación con Otros Estándares

- **PCI DSS 4.0:** Requiere controles robustos de seguridad de API (incluyendo pruebas BOLA/BFLA) para entornos de datos de titulares de tarjetas.
- **SOC 2:** El Top 10 proporciona un marco de control concreto para los criterios de disponibilidad y seguridad.
- **ISO 27001:** Ayuda a estructurar los controles del Anexo A en torno al acceso lógico y la seguridad operativa.
- **OWASP Web Top 10:** Complementario; siempre revisa ambas listas. El Top 10 Web cubre inyección y criptografía, mientras que el Top 10 de API cubre fallos lógicos y de negocio.

## Cuándo NO Usar el Top 10 de Seguridad de API

- Es un **documento de concienciación**, no un estándar de cumplimiento estricto. Trátalo como un punto de partida, no como una lista de verificación de auditoría exhaustiva.
- No cubre criptografía, registro o seguridad física en detalle (consulta ASVS o MASVS para eso).
- No es *un* reemplazo para un modelo de amenazas adaptado a tu arquitectura específica.

## Conclusiones Clave

| Riesgo | Mitigación Principal | Prueba de Ejemplo |
|--------|----------------------|-------------------|
| BOLA | Requiere verificaciones estrictas de propiedad para cada acceso a objeto. | Intercambiar IDs en solicitudes GET. |
| BOPLA | Usa DTOs/ViewModels; nunca pases objetos de usuario directamente al ORM. | Inyectar campos `role` o `admin`. |
| SSRF | Lista negra de rangos IP privados; lista blanca de destinos de salida. | Obtener endpoints de metadatos (`169.254.169.254`). |
| Flujos de Negocio | Limitación de velocidad + CAPTCHA para acciones sensibles. | Automatizar el pago 100 veces. |
| Inventario | Mantener un catálogo de API vivo en tu pipeline de CI. | Rastrear `v1/`, `swagger.json`, `/debug`. |

## Referencias

- Official OWASP API Security Project: [https://github.com/OWASP/API-Security](https://github.com/OWASP/API-Security)
- OWASP Top 10 Web (2021): [https://owasp.org/Top10/](https://owasp.org/Top10/)
- OWASP ZAP API Scanning: [https://www.zaproxy.org/docs/docker/api-scan/](https://www.zaproxy.org/docs/docker/api-scan/)
- Semgrep Rules for API Security: [https://semgrep.dev](https://semgrep.dev/)

---

*Estado: borrador. Última actualización: 2026-06-25.*