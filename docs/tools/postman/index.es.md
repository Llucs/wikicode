---
title: Postman - Plataforma de Desarrollo y Pruebas de API
description: Una guía completa de Postman, la plataforma API estándar de la industria para diseñar, construir, probar y documentar APIs.
created: 2026-06-15
tags:
  - postman
  - api-testing
  - api-development
  - collaboration
  - newman
status: draft
ecosystem: api
---

# Postman - Plataforma de Desarrollo y Pruebas de API

## ¿Qué es Postman?

Postman es una plataforma API completa que simplifica cada paso del ciclo de vida de las API – desde el diseño y desarrollo hasta las pruebas, documentación y monitoreo. Originalmente comenzó como un simple cliente HTTP, ha evolucionado hasta convertirse en un entorno colaborativo utilizado por millones de desarrolladores e ingenieros de QA en todo el mundo. Postman es compatible con los protocolos REST, GraphQL y SOAP, y proporciona un rico conjunto de herramientas para construir y trabajar con API de manera eficiente.

## ¿Por qué usar Postman?

- **Cliente HTTP Completo:** Envía fácilmente solicitudes de cualquier método, personaliza encabezados, autenticación y contenido del cuerpo.
- **Herramientas de Organización:** Agrupa solicitudes en Colecciones, gestiona variables con Entornos y reutiliza datos en todo un espacio de trabajo.
- **Scripts y Pruebas:** Escribe scripts de prueba en JavaScript para automatizar aserciones, extraer datos entre solicitudes y manejar flujos de trabajo dinámicos.
- **Listo para Automatización:** Usa el Collection Runner para ejecuciones manuales o Newman para ejecución sin interfaz gráfica (CI/CD, pipelines).
- **Colaboración:** Comparte colecciones y entornos mediante espacios de trabajo en la nube con control de versiones y comentarios.
- **Documentación y Simulación (Mocking):** Genera automáticamente documentación de API y servidores mock para simular respuestas de API antes de que el backend esté listo.
- **Monitoreo:** Configura monitores para programar ejecuciones de colecciones y verificar el estado de la API.

## Instalación

### App de Escritorio (Recomendada)

Postman proporciona aplicaciones de escritorio nativas para Windows, macOS y Linux.

- Descarga el instalador adecuado desde [getpostman.com](https://getpostman.com)
- Alternativamente, usa la **versión web** en [go.postman.co](https://go.postman.co) con el Agente de Escritorio para manejar las llamadas API.

### Newman (CLI para CI/CD)

Newman es el ejecutor de colecciones desde la línea de comandos para Postman. Te permite ejecutar y probar una colección de Postman directamente desde la línea de comandos, lo que lo hace ideal para integrar pruebas de API en tu pipeline de desarrollo.

Instalación con npm:

```bash
npm install -g newman
```

O con Yarn:

```bash
yarn global add newman
```

## Uso Básico

1. **Crear una solicitud**  
   Haz clic en el botón **New** y selecciona **HTTP Request** (o usa `Ctrl+N`).

2. **Especificar la solicitud**  
   - Ingresa la URL (ej., `https://jsonplaceholder.typicode.com/posts`)  
   - Selecciona el método HTTP (`GET`, `POST`, `PUT`, etc.)  
   - Agrega cualquier encabezado, parámetro de consulta o cuerpo de solicitud necesario.

3. **Enviar e inspeccionar**  
   Haz clic en **Send**. El panel de respuesta muestra el código de estado, el tiempo de respuesta, los encabezados y el cuerpo.

4. **Guardar en una colección**  
   Haz clic en **Save** y crea una nueva colección o añádelo a una existente.

5. **Añadir una prueba**  
   En la pestaña **Tests**, escribe un script en JavaScript para validar la respuesta. Ejemplo:

   ```javascript
   pm.test("Response status code is 200", function () {
       pm.response.to.have.status(200);
   });
   ```

   Vuelve a ejecutar la solicitud – el resultado de la prueba aparece en la pestaña **Test Results**.

## Características Clave con Ejemplos

### 1. Colecciones

Las colecciones te ayudan a agrupar solicitudes relacionadas y compartirlas con tu equipo. Una colección también puede incluir carpetas y metadatos.

```javascript
// Example of using collection variables in a pre-request script
pm.collectionVariables.set("baseUrl", "https://api.example.com");
```

Ejecuta una colección completa usando Newman:

```bash
newman run MyCollection.json
```

### 2. Entornos

Los entornos contienen pares clave-valor para variables que cambian entre configuraciones (desarrollo, staging, producción).

```json
{
  "base_url": "https://dev-api.example.com",
  "api_key": "abc123"
}
```

Usa `{{base_url}}` en tus URLs de solicitud. Cambia entre entornos para alternar contextos al instante.

### 3. Scripts de Pre-solicitud y Prueba

Los scripts de Postman se escriben en JavaScript y se ejecutan en un entorno aislado (sandbox) con acceso a objetos proporcionados por Postman como `pm`.

**Script de pre-solicitud** (se ejecuta antes de que se envíe la solicitud):

```javascript
// Dynamically set a timestamp parameter
pm.variables.set("timestamp", Date.now());
```

**Script de prueba** (se ejecuta después de recibir la respuesta):

```javascript
pm.test("Response time is less than 2000ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

pm.test("Body contains expected user", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData[0].name).to.eql("Leanne Graham");
});
```

### 4. Collection Runner

Ejecuta una colección completa o una carpeta varias veces con archivos de datos.

- Abre **Runner** desde la parte superior izquierda de Postman.
- Selecciona una colección, elige un entorno, establece iteraciones.
- Puedes proporcionar un archivo de datos CSV o JSON para inyectar datos en cada iteración.

### 5. Newman – Integración en Línea de Comandos

Newman te permite integrar tus pruebas de Postman en pipelines de CI/CD (Jenkins, GitLab CI, GitHub Actions, etc.).

**Ejecutar una colección con un entorno y un archivo de datos:**

```bash
newman run MyCollection.json \
  --environment staging.json \
  --iteration-data test-data.csv \
  --reporters cli,htmlextra
```

El reporter `htmlextra` genera un informe HTML interactivo de la ejecución de la prueba.

**Usar en un script de Node.js:**

```javascript
const newman = require('newman');

newman.run({
    collection: require('./MyCollection.json'),
    environment: require('./staging.json'),
    reporters: 'cli'
}, function (err, summary) {
    if (err) { throw err; }
    console.log('Collection run completed!');
    console.log(summary.run.stats);
});
```

### 6. Generación de Documentación

Postman puede generar automáticamente documentación para cualquier colección. Simplemente abre una colección, haz clic en el menú **...** y elige **View documentation**. La documentación incluye solicitudes de ejemplo, esquemas de solicitud/respuesta y fragmentos de código en varios idiomas.

Publica la documentación en la web mediante el botón **Publish Docs**, o expórtala como HTML.

### 7. Servidores Mock

Simula una API creando un servidor mock desde tu colección. Esto es extremadamente útil para el desarrollo frontend cuando el backend aún no está listo.

- Selecciona una colección, haz clic en **Mock Servers**.
- Postman crea una URL de servidor mock que devuelve las respuestas de ejemplo guardadas.

### 8. Monitores

Los monitores te permiten programar ejecuciones periódicas de una colección en la infraestructura en la nube de Postman. Recibes alertas si alguna prueba falla.

- Ve a **Monitors** → **Create a monitor**.
- Selecciona una colección, establece una frecuencia (ej., cada hora) y opcionalmente define alertas (correo electrónico, Slack, etc.).

## Resumen

Postman es mucho más que un cliente de API – es una plataforma completa que respalda todo el ciclo de vida de las API. Desde la simulación inicial y el diseño colaborativo hasta las pruebas automatizadas mediante Newman y la monitorización en producción, Postman proporciona a los equipos una fuente única de verdad para sus APIs. Su facilidad de uso, combinada con potentes scripts y la integración con CI/CD, lo convierte en una herramienta indispensable para los flujos de trabajo de desarrollo modernos.