---
title: API-Versionierungsstrategien
description: Wesentliche Techniken und Best Practices für die Verwaltung von Änderungen an einer API im Laufe der Zeit, ohne bestehende Clients zu beeinträchtigen, einschließlich URI-basierter, Header-basierter, Query-Parameter-basierter und Schema-basierter Ansätze.
created: 2026-06-24
tags:
  - api-design
  - rest
  - versioning
  - architecture
  - backend
status: draft
---

# API-Versionierungsstrategien

API-Versionierung ist die Praxis der Verwaltung von Änderungen an einem öffentlichen oder internen API-Vertrag, damit Anbieter die Schnittstelle weiterentwickeln können, ohne bestehende Clients zu stören. Sie ermöglicht, dass mehrere Repräsentationen derselben Ressource parallel laufen, und balanciert Innovation mit Stabilität aus. Die Wahl der richtigen Strategie – und ihre konsequente Umsetzung – ist eine der wichtigsten Entscheidungen im API-Design.

Dieser Leitfaden behandelt die gängigsten Versionierungstechniken, ihre Vor- und Nachteile, reale Anwendungsfälle und praktische Implementierungsbeispiele für führende Frameworks. Sie erfahren auch, wie Sie Deprecation und Sunset mit geeigneten Lebenszyklus-Headern handhaben.

---

## Warum Versionierung wichtig ist

Ohne Versionierung ist jede Änderung an einer API riskant:

- Das Hinzufügen eines erforderlichen Feldes kann Clients brechen, die alte Payloads senden.
- Das Entfernen eines Endpunkts kann Produktionsausfälle verursachen.
- Das Ändern des Formats eines Antwortfelds (z. B. von String zu Integer) zwingt alle Clients, gleichzeitig zu aktualisieren.

Eine Versionierungsstrategie bietet einen **Vertrag**: Clients in Version `v1` erhalten eine stabile Schnittstelle, während der Anbieter Breaking Changes in `v2` einführen kann. Auf diese Weise können Teams schnell liefern und gleichzeitig das Vertrauen der Clients wahren.

### Historischer Hintergrund

- **Frühe REST-APIs (Mitte der 2000er):** Flickr, Twitter und andere begannen aus Gründen der Klarheit, URIs mit `/v1/` zu versehen. SOAP basierte auf strengen WSDL-Schemata.
- **Roy Fieldings Dissertation** plädierte für Hypermedia (HATEOAS) als den „natürlichen“ Versionierungsmechanismus – bei dem Links Clients durch Zustände führen. Die Komplexität machte jedoch die URI-Versionierung zum De-facto-Standard.
- **GraphQL (2015)** förderte einen „versionslosen“ Ansatz, indem Felddeprecation anstelle von Breaking Changes verwendet wurde.
- **gRPC** verwendet Protobuf-Pakete und Schema-Registries für die Vertragsentwicklung.
- **Die OpenAPI-Spezifikation** dokumentiert jetzt mehrere Versionen in einer einzigen Spezifikationsdatei, was das Erstellen und Vergleichen von Versionen erleichtert.

---

## Wichtige Strategien

Alle Strategien bewegen sich auf einem Spektrum von expliziten Versionskennungen (einfach für Clients) bis hin zu impliziten Verträgen (sauber für Anbieter). Wählen Sie basierend auf der Reife Ihres Ökosystems und Ihrer Toleranz für Breaking Changes.

### 1. URI-/Pfad-Versionierung

Die Version wird direkt im URL-Pfad eingebettet, was der gebräuchlichste und einfachste Ansatz ist.

```
GET /v1/users
GET /v2/users
```

**Vorteile**
- Einfach zu implementieren und zu routen.
- Hoch auffindbar – Clients sehen die Version sofort.
- Hervorragendes Caching: Verschiedene Versionen können unabhängig voneinander gecacht werden.
- Einfach auf API-Gateways und CDNs bereitzustellen.

**Nachteile**
- Verstößt gegen REST-Semantik: Eine URI sollte eine Ressource identifizieren, keine Version (laut Fielding).
- Fördert das Forken von Servercode, wenn nicht mit Schichten entworfen.
- Kann nicht nach Repräsentation versionieren (z. B. eine andere Version für dieselbe Ressource basierend auf dem `Accept`-Header).

**Implementierungsbeispiel (Express.js)**

```javascript
// v1 router
const v1Router = require('./routes/v1');
app.use('/v1', v1Router);

// v2 router
const v2Router = require('./routes/v2');
app.use('/v2', v2Router);
```

**Implementierungsbeispiel (ASP.NET Core)**

```csharp
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/[controller]")]
public class UsersController : ControllerBase
{
    [HttpGet]
    public IActionResult Get() => Ok("Users from v1");
}
```

### 2. Query-Parameter-Versionierung

Ein Query-Parameter gibt die Version an.

```
GET /users?version=1
GET /users?version=2
```

**Vorteile**
- Einfach hinzuzufügen, ohne Routen zu ändern.
- Das URL-Muster bleibt über Versionen hinweg konsistent.

**Nachteile**
- Verunreinigt die Query-Semantik – `version` ist kein Filter oder Suchbegriff.
- Erschwert Caching, da der Parameter den Cache-Key ändert.
- Clients vergessen leicht, ihn anzugeben, was zu unbeabsichtigtem Fallback auf eine falsche Version führt.

**Implementierungsbeispiel (Express.js)**

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

### 3. Header-Versionierung

Versionsinformationen werden in HTTP-Headern übertragen. Zwei gängige Ansätze:

| Ansatz                           | Header-Beispiel                                   |
|----------------------------------|---------------------------------------------------|
| Benutzerdefinierter Header       | `X-API-Version: 1`                                |
| Accept-Header (anbieterspezifischer MIME-Typ) | `Accept: application/vnd.myapi.v1+json` |

**Vorteile**
- Am RESTfulsten – die URL identifiziert die Ressource, der Header die Repräsentation.
- Saubere URIs, die sich nie ändern.
- Fein granulare Kontrolle: Sie können nach Medientyp versionieren (z. B. `v1` JSON, `v2` XML).

**Nachteile**
- Schlechte Auffindbarkeit – ohne Header-Anpassung schwer im Browser oder mit curl zu testen.
- Erhöht die Komplexität auf der Serverseite für das Routing basierend auf Headern.
- Caching kann knifflig sein, es sei denn, `Vary`-Header werden korrekt gesetzt.

**Implementierungsbeispiel (ASP.NET Core mit Accept-Header)**

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

**Implementierungsbeispiel (Spring Boot)**

```java
@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v1+json")
public class UserControllerV1 { ... }

@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v2+json")
public class UserControllerV2 { ... }
```

### 4. Code-/Schema-Versionierung (Keine explizite Version)

Wird oft als „versionslos“ oder „vertragszuerst“ bezeichnet. Anstatt eine Versionskennung offenzulegen, behält der API-Anbieter die Abwärtskompatibilität bei, indem er nur Felder oder Endpunkte hinzufügt. Breaking Changes werden über Schema-Registries (z. B. Protobuf, Avro) oder durch Einführung eines neuen Endpunkts/Vorgangs kommuniziert.

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

**Vorteile**
- Keine Notwendigkeit, mehrere Routing-Pfade zu pflegen.
- Fördert kontinuierliche Abwärtskompatibilität.
- Gut für interne Mikrodienste und ereignisgesteuerte Systeme.

**Nachteile**
- Kann absichtliche Breaking Changes nicht ohne Versionsindikator kommunizieren.
- Wird zu einem Wartungsaufwand, wenn die Abwärtskompatibilität versehentlich gebrochen wird.

**Geeignet für:**
- Interne Mikrodienste, bei denen Clients und Anbieter in derselben Organisation sind.
- GraphQL-Schemata mit der `@deprecated`-Direktive.
- Ereignisgesteuerte Systeme mit Schema-Registries (Confluent Schema Registry, AWS Glue).

---

## Anwendungsfälle nach Branche

| Anwendungsfall | Bevorzugte Strategie | Begründung |
|----------------|----------------------|------------|
| **Öffentliche APIs (Stripe, Twilio)** | URI-Versionierung | Clients benötigen explizite, stabile Verträge; Caching ist einfach. |
| **Mobile Backends (Facebook, Twitter)** | Header-Versionierung (benutzerdefiniert) | Die App sendet die Version, mit der sie kompiliert wurde; die URL ändert sich nie, was den Druck von App-Store-Updates vermeidet. |
| **Interne Mikrodienste** | Versionslos / Protobuf | Schema-Registries erzwingen Kompatibilität; keine Notwendigkeit, mehrere Endpunktversionen zu pflegen. |
| **Ereignisgesteuerte Systeme** | Schema Registry (Avro/Protobuf) | Datenverträge entwickeln sich unabhängig; Clients validieren anhand der Schema-ID. |

---

## Installation und Einrichtung

Versionierung ist ein Entwurfsmuster, erfordert jedoch Werkzeuge, um Routing, Validierung und Dokumentation durchzusetzen. Nachfolgend finden Sie Installationsschritte für gängige Umgebungen.

### ASP.NET Core

Fügen Sie das NuGet-Paket `Microsoft.AspNetCore.Mvc.Versioning` hinzu und konfigurieren Sie:

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

Keine Bibliothek erforderlich. Erstellen Sie Router pro Version und binden Sie sie ein:

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

Spring Boot unterstützt nativ Header-Versionierung und URI-Versionierung über `@RequestMapping`. Für die Accept-Header-Versionierung können Sie separate Controller mit unterschiedlichen `produces`-Attributen definieren.

```java
// POM dependency: spring-boot-starter-web (includes Spring MVC)
// For media type versioning, controllers produce different vendor MIME types:
@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v1+json")
public class UserControllerV1 { ... }
```

### API-Gateways (Kong, AWS API Gateway)

Konfigurieren Sie Routing-Regeln vorgelagert zu Ihrem Anwendungscode:

- **Kong:** Definieren Sie Dienste und Routen mit spezifischen Pfaden (`/v1/`, `/v2/`). Sie können auch das Pfadpräfix entfernen, bevor Sie an das Backend weiterleiten.
- **AWS API Gateway:** Erstellen Sie Stufen oder Ressourcen mit Pfadparametern wie `{proxy+}` und Versionierung im Pfad. Oder verwenden Sie einen `version`-Header und routen Sie mit einem Zuordnungstemplate.

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

## Bewährte Methoden

### 1. Seien Sie konsistent
Wählen Sie eine Strategie pro API-Oberfläche. Das Mischen von URI- und Header-Versionierung über Endpunkte hinweg führt zu Verwirrung.

### 2. Versionieren Sie den Vertrag, nicht die Implementierung
Ihre OpenAPI-Spezifikation (oder Äquivalent) sollte die Quelle der Wahrheit sein. Änderungen am Vertrag erfordern eine neue Version, nicht Änderungen am internen Code.

### 3. Bevorzugen Sie Abwärtskompatibilität (aber fürchten Sie keine Breaking Changes)
Fügen Sie nach Möglichkeit neue Felder hinzu, anstatt vorhandene zu entfernen oder umzubenennen. Verwenden Sie `@deprecated`-Marker in Ihrer Spezifikation. Allerdings sind Breaking Changes manchmal notwendig – Versionierung ist das Sicherheitsnetz.

### 4. Verwenden Sie explizite Lebenszyklus-Header
Wenn eine Version veraltet ist, geben Sie diese von RFC inspirierten Header zurück:

- `Deprecation: Sat, 01 Jan 2025 00:00:00 GMT` – gibt an, dass die Version veraltet ist.
- `Sunset: Wed, 01 Jul 2026 00:00:00 GMT` – gibt an, wann die Version entfernt wird.
- `Link: </v2/users>; rel="successor-version"` – zeigt auf die Ersatzversion.

**Beispiel für einen Satz von Antwort-Headern:**

```http
HTTP/1.1 200 OK
Content-Type: application/json
Deprecation: true
Sunset: Wed, 01 Jul 2026 00:00:00 GMT
Link: </v2/users>; rel="successor-version"
```

### 5. Behandeln Sie Ihren API-Vertrag mit semantischer Versionierung
Verwenden Sie die Semantik von `MAJOR.MINOR.PATCH`:

- **Major:** Breaking Changes → neue Version (z. B. `/v2/`).
- **Minor:** additive, abwärtskompatible Änderungen (z. B. neue Felder im Body, neue Endpunkte).
- **Patch:** Fehlerbehebungen oder nicht-funktionale Verbesserungen.

### 6. Dokumentieren Sie alles
Nehmen Sie die Versionierungsstrategie in das `info.version`-Feld Ihrer OpenAPI-Spezifikation auf und stellen Sie Migrationsleitfäden zwischen Versionen bereit.

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

### 7. Automatisieren Sie die Sunset-Erzwingung
Verwenden Sie API-Gateways oder Middleware, um Aufrufe an veraltete Versionen nach einem Stichtag abzulehnen. Geben Sie `410 Gone` mit einem Link zur neuesten Version zurück.

---

## Lebenszyklus der Deprecation

Eine vollständig verwaltete versionierte API durchläuft diese Phasen:

1. **Aktiv** – Version ist die Standardeinstellung oder explizit aufrufbar.
2. **Deprecated (veraltet)** – Version funktioniert noch, gibt aber `Deprecation`-Header zurück. Clients sollten in der Dokumentation ein Banner sehen.
3. **Sunset (Auslauf)** – Version wird an einem bestimmten Datum entfernt. Gibt sowohl `Deprecation`- als auch `Sunset`-Header zurück.
4. **Entfernt** – Endpunkt gibt `410 Gone` zurück (nicht `404`). Das `Sunset`-Datum ist überschritten.

**Middleware-Beispiel (Express.js) für automatische Deprecation-Header:**

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

## Fazit

API-Versionierung ist eine strategische Entscheidung, die jeden Client Ihrer API betrifft. Es gibt keine Universallösung; die richtige Wahl hängt von Ihrer Client-Basis, Ihrem Ökosystem und Ihrer Risikotoleranz ab.

| Strategie | Wann wählen |
|-----------|-------------|
| **URI / Pfad** | Öffentliche APIs, bei denen Auffindbarkeit und Caching oberste Priorität haben. |
| **Query-Parameter** | Einfache Anwendungsfälle mit internen Clients, bei denen Flexibilität benötigt wird. |
| **Header (Accept / Benutzerdefiniert)** | Mobile Apps, langlebige Clients oder wenn Sie saubere URIs wünschen. |
| **Versionslos / Schema** | Interne Dienste, ereignisgesteuerte Architekturen oder GraphQL. |

Unabhängig von der Strategie sollten Sie in klare Dokumentation, Lebenszyklus-Header und schrittweise Deprecation investieren. Eine gut versionierte API schafft Vertrauen und ermöglicht es Ihrer Plattform, sich weiterzuentwickeln, ohne das Ökosystem zu zerstören, das von ihr abhängt.

> **Weiterführende Literatur**
> - [REST API Versioning by Microsoft](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design#versioning)
> - [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
> - [RFC 8594: Sunset Header](https://tools.ietf.org/html/rfc8594)
> - [API Design Patterns – Chapter on Versioning](https://www.manning.com/books/api-design-patterns)