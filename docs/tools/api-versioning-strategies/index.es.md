---
title: Estrategias de versionado de API
description: Técnicas esenciales y mejores prácticas para gestionar cambios en una API a lo largo del tiempo sin romper clientes existentes, incluyendo enfoques basados en URI, cabeceras, parámetros de consulta y esquemas.
created: 2026-06-24
tags:
  - api-design
  - rest
  - versioning
  - architecture
  - backend
status: draft
---

# Estrategias de versionado de API

El versionado de API es la práctica de gestionar cambios en un contrato de API público o interno para que los proveedores puedan evolucionar la interfaz sin interrumpir a los consumidores existentes. Permite que múltiples representaciones del mismo recurso se ejecuten en paralelo, equilibrando innovación con estabilidad. Elegir la estrategia correcta —e implementarla de manera consistente— es una de las decisiones más importantes en el diseño de APIs.

Esta guía cubre las técnicas de versionado más comunes, sus ventajas y desventajas, casos de uso del mundo real y ejemplos prácticos de implementación para frameworks líderes. También aprenderá a manejar la obsolescencia y el retiro con cabeceras de ciclo de vida adecuadas.

---

## Por qué importa la versión

Sin versionado, cada cambio en una API es riesgoso:

- Añadir un campo obligatorio puede romper clientes que envían payloads antiguos.
- Eliminar un endpoint puede causar interrupciones en producción.
- Cambiar el formato de un campo de respuesta (ej., de string a integer) obliga a todos los consumidores a actualizarse simultáneamente.

Una estrategia de versionado proporciona un **contrato**: los clientes en la versión `v1` tienen garantizada una interfaz estable, mientras que el proveedor puede introducir cambios disruptivos en `v2`. Esto permite a los equipos enviar cambios rápidamente manteniendo la confianza de los consumidores.

### Contexto histórico

- **Primeras APIs REST (mediados de los 2000):** Flickr, Twitter y otros comenzaron a prefijar las URIs con `/v1/` por claridad. SOAP dependía de esquemas WSDL estrictos.
- **La disertación de Roy Fielding** abogaba por la hipermedia (HATEOAS) como el mecanismo de versionado "natural", donde los enlaces guían a los clientes a través de estados. Sin embargo, la complejidad hizo que el versionado por URI se convirtiera en el estándar de facto.
- **GraphQL (2015)** promovió un enfoque "sin versiones" usando la obsolescencia de campos en lugar de cambios disruptivos.
- **gRPC** utiliza paquetes Protobuf y registros de esquemas para la evolución del contrato.
- **La especificación OpenAPI** ahora documenta múltiples versiones en un solo archivo de especificación, facilitando la autoría y comparación de versiones.

---

## Principales estrategias

Todas las estrategias se sitúan en un espectro desde **identificadores de versión explícitos** (fáciles para los consumidores) hasta **contratos implícitos** (limpios para los proveedores). Elija según la madurez de su ecosistema y la tolerancia a cambios disruptivos.

### 1. Versionado por URI / Ruta

La versión se incrusta directamente en la ruta URL, siendo el enfoque más común y directo.

```
GET /v1/users
GET /v2/users
```

**Ventajas**
- Simple de implementar y enrutar.
- Altamente descubrible: los consumidores ven la versión inmediatamente.
- Excelente almacenamiento en caché: diferentes versiones pueden almacenarse en caché de forma independiente.
- Fácil de implementar en puertas de enlace de API y CDNs.

**Desventajas**
- Viola la semántica REST: una URI debería identificar un recurso, no una versión (según Fielding).
- Fomenta la bifurcación del código del servidor si no está diseñado con capas.
- No permite versionar por representación (ej., una versión diferente para el mismo recurso basada en la cabecera `Accept`).

**Ejemplo de implementación (Express.js)**

```javascript
// Router v1
const v1Router = require('./routes/v1');
app.use('/v1', v1Router);

// Router v2
const v2Router = require('./routes/v2');
app.use('/v2', v2Router);
```

**Ejemplo de implementación (ASP.NET Core)**

```csharp
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/[controller]")]
public class UsersController : ControllerBase
{
    [HttpGet]
    public IActionResult Get() => Ok("Users from v1");
}
```

### 2. Versionado por parámetro de consulta

Un parámetro de consulta especifica la versión.

```
GET /users?version=1
GET /users?version=2
```

**Ventajas**
- Simple de añadir sin cambiar rutas.
- El patrón de URL se mantiene consistente entre versiones.

**Desventajas**
- Contamina la semántica de la consulta: `version` no es un filtro ni un término de búsqueda.
- Complica el almacenamiento en caché porque el parámetro cambia la clave de caché.
- Es fácil que los clientes olviden incluir el parámetro, lo que lleva a una versión de respaldo no deseada.

**Ejemplo de implementación (Express.js)**

```javascript
app.get('/users', (req, res) => {
  const version = req.query.version || 1;
  switch(version) {
    case '1': return handleV1(req, res);
    case '2': return handleV2(req, res);
    default:  return res.status(400).json({ error: 'Versión no válida' });
  }
});
```

### 3. Versionado por cabecera

La información de la versión se transporta en cabeceras HTTP. Dos enfoques comunes:

| Enfoque               | Ejemplo de cabecera                               |
|-----------------------|---------------------------------------------------|
| Cabecera personalizada | `X-API-Version: 1`                               |
| Cabecera Accept (tipo MIME de proveedor) | `Accept: application/vnd.myapi.v1+json` |

**Ventajas**
- Más RESTful: la URL identifica el recurso, la cabecera identifica la representación.
- URIs limpias que nunca cambian.
- Control fino: se puede versionar por tipo de medio (ej., `v1` JSON, `v2` XML).

**Desventajas**
- Poca descubribilidad: difícil de probar en un navegador o con curl sin modificar la cabecera.
- Simula complejidad en el lado del servidor para el enrutamiento basado en cabeceras.
- El almacenamiento en caché puede ser complicado a menos que las cabeceras `Vary` se configuren adecuadamente.

**Ejemplo de implementación (ASP.NET Core con cabecera Accept)**

```csharp
// En Startup.cs
services.AddApiVersioning(options =>
{
    options.ApiVersionReader = new MediaTypeApiVersionReader();
    options.AssumeDefaultVersionWhenUnspecified = true;
});

// Controlador
[ApiVersion("1.0")]
[Route("api/users")]
public class UsersV1Controller : ControllerBase {}
```

**Ejemplo de implementación (Spring Boot)**

```java
@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v1+json")
public class UserControllerV1 { ... }

@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v2+json")
public class UserControllerV2 { ... }
```

### 4. Versionado por código / esquema (sin versión explícita)

A menudo llamado "sin versiones" o "primero el contrato". En lugar de exponer un identificador de versión, el proveedor de la API mantiene compatibilidad hacia atrás añadiendo solo campos o endpoints. Los cambios disruptivos se comunican a través de registros de esquemas (ej., Protobuf, Avro) o introduciendo un nuevo endpoint/operación.

```
// Versionado de paquete Protobuf
package myapi.v1;
message User {
  string name = 1;
}

// Más tarde, en v2:
message User {
  string name = 1;
  string email = 2;
}
```

**Ventajas**
- No es necesario mantener múltiples rutas de enrutamiento.
- Incentiva la compatibilidad hacia atrás continua.
- Bueno para microservicios internos y sistemas basados en eventos.

**Desventajas**
- No puede comunicar cambios disruptivos intencionales sin un indicador de versión.
- Se convierte en una carga de mantenimiento si la compatibilidad hacia atrás se rompe involuntariamente.

**Mejor para:**
- Microservicios internos donde consumidores y proveedores están en la misma organización.
- Esquemas GraphQL usando la directiva `@deprecated`.
- Sistemas basados en eventos con registros de esquemas (Confluent Schema Registry, AWS Glue).

---

## Casos de uso por industria

| Caso de uso | Estrategia preferida | Razón |
|-------------|----------------------|-------|
| **APIs públicas (Stripe, Twilio)** | Versionado por URI | Los clientes necesitan contratos explícitos y estables; el almacenamiento en caché es simple. |
| **Backends móviles (Facebook, Twitter)** | Versionado por cabecera (personalizada) | La aplicación envía la versión con la que fue compilada; la URL nunca cambia, evitando presión de actualización en la tienda de aplicaciones. |
| **Microservicios internos** | Sin versiones / Protobuf | Los registros de esquemas imponen compatibilidad; no es necesario mantener múltiples versiones de endpoint. |
| **Sistemas basados en eventos** | Registro de esquemas (Avro/Protobuf) | Los contratos de datos evolucionan independientemente; los consumidores validan contra el ID del esquema. |

---

## Instalación y configuración

El versionado es un **patrón de diseño**, pero requiere herramientas para imponer el enrutamiento, la validación y la documentación. A continuación se presentan los pasos de instalación para entornos comunes.

### ASP.NET Core

Agregue el paquete NuGet `Microsoft.AspNetCore.Mvc.Versioning` y configure:

```csharp
// Instalación: dotnet add package Microsoft.AspNetCore.Mvc.Versioning
// En Startup.cs:
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

No se requiere librería. Cree routers por versión y móntelos:

```javascript
// Instalación: npm i express (no se necesita librería adicional)
const express = require('express');
const app = express();

const v1Router = require('./routes/v1');
const v2Router = require('./routes/v2');

app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

app.listen(3000);
```

### Spring Boot

Spring Boot soporta de forma nativa el versionado por cabecera y por URI mediante `@RequestMapping`. Para el versionado por cabecera Accept, puede definir controladores separados con diferentes atributos `produces`.

```java
// Dependencia POM: spring-boot-starter-web (incluye Spring MVC)
// Para versionado por tipo de medio, los controladores producen diferentes tipos MIME de proveedor:
@RestController
@RequestMapping(path = "/users", produces = "application/vnd.company.v1+json")
public class UserControllerV1 { ... }
```

### Puertas de enlace de API (Kong, AWS API Gateway)

Configure reglas de enrutamiento aguas arriba de su código de aplicación:

- **Kong:** Defina servicios y rutas con rutas específicas (`/v1/`, `/v2/`). También puede eliminar el prefijo de ruta antes de reenviar al backend.
- **AWS API Gateway:** Cree etapas o recursos con parámetros de ruta como `{proxy+}` y versionado en la ruta. O use una cabecera `version` y enrute con una plantilla de mapeo.

```yaml
# Configuración declarativa de Kong (YAML)
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

## Mejores prácticas

### 1. Sea consistente
Elija una estrategia por superficie de API. Mezclar versionado por URI y por cabecera en diferentes endpoints genera confusión.

### 2. Versiona el contrato, no la implementación
Su especificación OpenAPI (o equivalente) debe ser la fuente de verdad. Los cambios en el contrato requieren una nueva versión, no cambios en el código interno.

### 3. Prefiera la compatibilidad hacia atrás (pero no tema los cambios disruptivos)
Cuando sea posible, añada nuevos campos en lugar de eliminar o renombrar los existentes. Use marcadores `@deprecated` en su especificación. Sin embargo, a veces los cambios disruptivos son necesarios; el versionado es la red de seguridad.

### 4. Use cabeceras de ciclo de vida explícitas
Cuando una versión esté obsoleta, devuelva estas cabeceras inspiradas en RFC:

- `Deprecation: Sat, 01 Jan 2025 00:00:00 GMT` – indica que la versión está obsoleta.
- `Sunset: Wed, 01 Jul 2026 00:00:00 GMT` – indica cuándo se eliminará la versión.
- `Link: </v2/users>; rel="successor-version"` – apunta al reemplazo.

**Ejemplo de conjunto de cabeceras de respuesta:**

```http
HTTP/1.1 200 OK
Content-Type: application/json
Deprecation: true
Sunset: Wed, 01 Jul 2026 00:00:00 GMT
Link: </v2/users>; rel="successor-version"
```

### 5. Trate su contrato de API con versionado semántico
Use la semántica `MAYOR.MENOR.PARCHE`:

- **Mayor:** cambios disruptivos → nueva versión (ej., `/v2/`).
- **Menor:** cambios aditivos y compatibles hacia atrás (ej., nuevos campos en el cuerpo, nuevos endpoints).
- **Parche:** correcciones o mejoras no funcionales.

### 6. Documente todo
Incluya la estrategia de versionado en el campo `info.version` de su especificación OpenAPI y proporcione guías de migración entre versiones.

```yaml
openapi: 3.0.0
info:
  title: Mi API
  version: 2.0.0
  description: |
    ## Versionado
    Esta API utiliza versionado por ruta URI. Todas las solicitudes deben incluir la versión en la ruta URL, por ejemplo, `/v2/users`.
    Consulte la [guía de migración](/docs/migration) para conocer los cambios de v1 a v2.
```

### 7. Automatice la aplicación de la fecha de retiro
Use puertas de enlace de API o middleware para rechazar llamadas a versiones obsoletas después de una fecha límite. Devuelva `410 Gone` con un enlace a la versión más reciente.

---

## Ciclo de vida de obsolescencia

Una API versionada completamente gestionada pasa por estas etapas:

1. **Activa** – la versión es la predeterminada o explícitamente invocable.
2. **Obsoleta** – la versión aún funciona pero devuelve la cabecera `Deprecation`. Los consumidores deberían ver un aviso en la documentación.
3. **Retiro programado** – la versión se eliminará en una fecha específica. Devuelve ambas cabeceras `Deprecation` y `Sunset`.
4. **Eliminada** – el endpoint devuelve `410 Gone` (no `404`). La fecha `Sunset` ha pasado.

**Ejemplo de middleware (Express.js) para cabeceras de obsolescencia automáticas:**

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

## Conclusión

El versionado de API es una decisión estratégica que afecta a todos los consumidores de su API. No existe una estrategia única para todos; la elección correcta depende de su base de consumidores, ecosistema y tolerancia al riesgo.

| Estrategia | Cuándo elegir |
|------------|---------------|
| **URI / Ruta** | APIs públicas, donde la descubribilidad y el almacenamiento en caché son primordiales. |
| **Parámetro de consulta** | Casos de uso simples con consumidores internos donde se necesita flexibilidad. |
| **Cabecera (Accept / Personalizada)** | Aplicaciones móviles, clientes de larga duración, o cuando se desean URIs limpias. |
| **Sin versiones / Esquema** | Servicios internos, arquitecturas basadas en eventos o GraphQL. |

Independientemente de la estrategia, invierta en documentación clara, cabeceras de ciclo de vida y obsolescencia gradual. Una API bien versionada genera confianza y permite que su plataforma evolucione sin romper el ecosistema que depende de ella.

> **Lecturas adicionales**
> - [Versionado de API REST por Microsoft](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design#versioning)
> - [Especificación OpenAPI](https://spec.openapis.org/oas/latest.html)
> - [RFC 8594: Sunset Header](https://tools.ietf.org/html/rfc8594)
> - [Patrones de diseño de API – Capítulo sobre versionado](https://www.manning.com/books/api-design-patterns)