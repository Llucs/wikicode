---
title: Appwrite: Plataforma de Backend como Servicio Autoalojada
description: BaaS de código abierto que proporciona API para autenticación, bases de datos, almacenamiento, funciones serverless y mensajería – una alternativa a Firebase que controlas.
created: 2026-06-15
tags:
  - analysis
  - backend-as-a-service
  - self-hosted
  - firebase-alternative
  - serverless
  - platform-study
status: draft
---

# Appwrite: Plataforma de Backend como Servicio Autoalojada

Appwrite es una plataforma **Backend como Servicio (BaaS) de código abierto** que proporciona un conjunto completo de API y herramientas de servidor para construir aplicaciones web, móviles y de IA rápidamente. Creada por Eldad Fux en 2019 y respaldada por una gran comunidad (más de 40k estrellas en GitHub), está diseñada como una alternativa autoalojada a Firebase, priorizando la propiedad de los datos, la privacidad y el despliegue flexible.

En lugar de conectar microservicios individualmente, Appwrite proporciona una API unificada para autenticación, bases de datos, almacenamiento, funciones serverless, mensajería y eventos en tiempo real, todo ejecutándose en tu propia infraestructura.

---

## ¿Por qué Appwrite?

- **Propiedad de los datos** – Tú controlas dónde y cómo se almacenan los datos, crucial para cumplimiento de GDPR, HIPAA, o normativas internas.
- **Sin dependencia del proveedor** – Autoalójalo o usa la oferta en la nube; tu código sigue siendo portátil.
- **Amplio conjunto de servicios** – Autenticación (OAuth2, MFA, JWT, URLs mágicas), bases de datos NoSQL, almacenamiento de archivos, funciones serverless, mensajería push/correo electrónico/SMS, suscripciones en tiempo real y más, todo en un solo paquete.
- **API simple y unificada** – Un mismo patrón de SDK en web (JavaScript/TypeScript), Flutter, Android, iOS y código de servidor.
- **Ecosistema activo de código abierto** – Respaldado por una comunidad próspera, SDKs oficiales, CLI y una creciente biblioteca de integraciones (Stripe, Twilio, SendGrid, GPT-4o a través de funciones).
- **Desde prototipado rápido hasta producción** – Usa la consola de administración para configurar sin código, luego integra el SDK para control total.

---

## Características clave con ejemplos de comandos

### Autenticación
Admite correo electrónico/contraseña, teléfono (SMS), OAuth2 (Google, GitHub, Discord, etc.), URL mágica, JWT, sesiones anónimas y autenticación multifactor (MFA).

```javascript
import { Client, Account, ID } from 'appwrite';

// Initialize client
const client = new Client()
    .setEndpoint('https://<HOST>/v1')
    .setProject('<PROJECT_ID>');

const account = new Account(client);

// Register a user
await account.create(ID.unique(), 'user@example.com', 'password123', 'Jane Doe');

// Log in
await account.createEmailPasswordSession('user@example.com', 'password123');

// Get current user
const user = await account.get();
```

### Base de datos (NoSQL)
Almacenamiento basado en documentos con consultas avanzadas, búsqueda de texto completo, oyentes en tiempo real y relaciones.

```javascript
import { Databases, ID } from 'appwrite';

const databases = new Databases(client);

// Create a document
await databases.createDocument(
    '<DATABASE_ID>',
    '<COLLECTION_ID>',
    ID.unique(),
    { title: 'My Post', body: 'Hello, world!', tags: ['appwrite'] }
);

// List documents
const results = await databases.listDocuments(
    '<DATABASE_ID>',
    '<COLLECTION_ID>',
    [Query.equal('tags', ['appwrite'])]
);
```

### Almacenamiento
Carga de archivos con vista previa de imagen integrada, redimensionamiento, recorte y escaneo de malware.

```javascript
import { Storage, ID } from 'appwrite';

const storage = new Storage(client);

// Upload a file
const uploaded = await storage.createFile(
    '<BUCKET_ID>',
    ID.unique(),
    myFile
);
```

### Funciones serverless
Ejecuta código en respuesta a eventos (base de datos, almacenamiento, autenticación, programaciones). Entornos de ejecución compatibles: Node.js, Python, Ruby, PHP, Dart, Deno, Kotlin, Swift, .NET.

```bash
# Create a function via CLI
appwrite functions create \
  --name='sendWelcomeEmail' \
  --runtime='node-18.0' \
  --execute='any' \
  --entrypoint='index.js'

# Deploy code
appwrite functions deploy \
  --functionId='<FUNCTION_ID>' \
  --path='./my-function'
```

```javascript
// Index function code (Node.js)
export default async ({ req, res, log, error }) => {
    log('Function triggered');
    return res.json({ message: 'Hello from Appwrite Functions!' });
};
```

### Mensajería
Notificaciones push (FCM/APNS), correos electrónicos (SMTP, SendGrid, Mailgun) y SMS (Twilio, Vonage, TextMagic). Todo gestionado a través de la consola de administración o la API.

```javascript
import { Messaging } from 'appwrite';

const messaging = new Messaging(client);
await messaging.createEmail(
    '<MESSAGE_ID>',
    '<SUBJECT>',
    '<CONTENT>',
    [userEmail]
);
```

### Tiempo real
Suscríbete a eventos de base de datos, almacenamiento y funciones (basado en WebSocket).

```javascript
import { Client } from 'appwrite';

const client = new Client()
    .setEndpoint('https://<HOST>/v1')
    .setProject('<PROJECT_ID>');

client.subscribe('databases.<DB_ID>.collections.<COLL_ID>.documents', response => {
    console.log('Document changed:', response.payload);
});
```

### API GraphQL
Appwrite expone un endpoint GraphQL completo, adecuado para frameworks front-end que funcionan bien con GraphQL.

```graphql
query {
  usersList(limit: 10) {
    users {
      name
      email
      $id
    }
  }
}
```

### Consola de administración
Una interfaz web completa para gestionar todos los servicios: no se requiere programación para crear bases de datos, colecciones, usuarios, buckets de almacenamiento o disparadores.

---

## Arquitectura

Appwrite utiliza una **arquitectura de microservicios** orquestada con Docker. Cada servicio se ejecuta como un contenedor aislado:

- **MariaDB** – Almacén de metadatos (proyectos, usuarios, etc.)
- **Redis** – Caché y cola de trabajos
- **InfluxDB** – Métricas de uso y análisis
- **Kafka** – Streaming de mensajes y eventos
- **Workers** – Tareas en segundo plano (correos electrónicos, funciones, webhooks, migraciones)

Workers dedicados manejan el trabajo asíncrono, manteniendo la API principal receptiva. Todo el stack se lanza mediante un solo comando de instalación.

---

## Instalación

### Autoalojado (Docker)

La forma más sencilla de poner Appwrite en funcionamiento en tu propio servidor:

```bash
docker run -it --rm \
    --volume /var/run/docker.sock:/var/run/docker.sock \
    --volume "$(pwd)"/appwrite:/storage/config:rw \
    --entrypoint="install" \
    appwrite/appwrite:latest
```

Esto inicia un instalador interactivo que descarga y configura todos los contenedores necesarios. Por defecto, Appwrite se ejecuta en `http://0.0.0.0`.

### Nube (Gestionado)

Regístrate en [cloud.appwrite.io](https://cloud.appwrite.io) – hay un nivel gratuito con límites de uso, perfecto para prototipado.

### Configuración de la consola

Después de la instalación (autoalojada o en la nube), crea un proyecto en la consola, anota el ID del proyecto y el endpoint, y genera una clave API.

---

## Uso básico (SDK de JavaScript)

1. **Inicializar cliente y autenticar**

   ```javascript
   import { Client, Account, ID } from 'appwrite';

   const client = new Client()
       .setEndpoint('https://<HOST>/v1')
       .setProject('<PROJECT_ID>');

   const account = new Account(client);

   // Register & Login
   await account.create(ID.unique(), 'user@test.com', 'password123', 'Jane Doe');
   await account.createEmailPasswordSession('user@test.com', 'password123');
   ```

2. **Crear y consultar documentos**

   ```javascript
   import { Databases, Query } from 'appwrite';

   const databases = new Databases(client);

   // Create
   await databases.createDocument(
       '<DATABASE_ID>',
       '<COLLECTION_ID>',
       ID.unique(),
       { name: 'Task', status: 'backlog' }
   );

   // Query
   const tasks = await databases.listDocuments(
       '<DATABASE_ID>',
       '<COLLECTION_ID>',
       [Query.equal('status', 'backlog'), Query.limit(25)]
   );
   ```

3. **Desplegar una función mediante la CLI**

   ```bash
   appwrite functions create --name='processOrder' --runtime='node-18.0' --execute='any'
   appwrite functions deploy --functionId='<ID>' --path='./functions/process-order'
   ```

4. **Escuchar eventos en tiempo real**

   ```javascript
   client.subscribe('databases.*.collections.*.documents', event => {
       console.log(`${event.events[0]} –`, event.payload);
   });
   ```

---

## Casos de uso

- **Crear MVP y prototipos rápidos** – omite la configuración del backend; concéntrate en la lógica del front-end.
- **Aplicaciones web full-stack** – React, Vue, Next.js, Svelte, Nuxt, Angular.
- **Aplicaciones móviles multiplataforma** – Flutter, Android, iOS (SwiftUI), React Native.
- **Funciones habilitadas para IA** – integra GPT-4o u otros LLM a través de funciones serverless.
- **Herramientas internas** – usa la consola de administración y las actualizaciones en tiempo real para paneles de administración.
- **Aplicaciones compatibles con GDPR/HIPAA** – autoalojadas en tu propio centro de datos.

---

## Comparación con herramientas similares

| Característica                | Appwrite                        | Supabase                          | PocketBase                        |
|-------------------------------|----------------------------------|-----------------------------------|-----------------------------------|
| Modelo de base de datos       | NoSQL (documentos)               | SQL (PostgreSQL)                  | SQLite                            |
| Autoalojado                   | Sí (Docker)                      | Sí (Docker)                       | Sí (binario único)                |
| Funciones serverless          | Sí (Node, Python, Ruby, etc.)    | Sí (funciones PostgreSQL + edge)  | Sí (JavaScript/Go)                |
| Tiempo real                   | WebSocket (DB, Almacen., Eventos)| Replicación PostgreSQL            | WebSocket (DB)                    |
| Autenticación                 | OAuth2, MFA, URL mágica, SMS     | OAuth2, MFA, SSO                  | OAuth2, MFA                       |
| Mensajería                    | Push, correo, SMS                | Correo (via pgmq)                 | –                                 |
| Almacenamiento                | Vista previa, redimensionar, escanear | Sí (compatible S3)           | Sí                                |
| Interfaz de administración    | Consola web completa             | Consola web                       | Interfaz web mínima               |
| SDK de cliente                | Web, Flutter, Android, iOS, CLI  | Web, Flutter, Swift, Kotlin, etc. | Web, Dart, Android, iOS, Go       |

**Elige Appwrite** si necesitas una plataforma NoSQL unificada y definida con mensajería integrada, GraphQL y una consola de administración completa, y si quieres mantener tus datos en tu propio stack de Docker.

---

## Comunidad y ecosistema

- **GitHub** – [github.com/appwrite/appwrite](https://github.com/appwrite/appwrite)
- **Discord** – comunidad activa de desarrolladores
- **Plantillas y proyectos abiertos** – mira [builtwith.appwrite.network](https://builtwith.appwrite.network)
- **Integraciones** – Appwrite MCP para IA, sensores, detección de fraude y más
- **Hackathones** – aparece con frecuencia en Hacktoberfest, desafíos de Dev.to

---

## Conclusión

Appwrite es una plataforma BaaS madura y de código abierto que te brinda el poder de Firebase sin la dependencia. Su capacidad de autoalojamiento, su amplio conjunto de funciones y su comunidad activa la convierten en una excelente opción para todo, desde hackathones hasta entornos empresariales regulados. Ya sea que uses la versión en la nube o la ejecutes tú mismo, Appwrite abstrae la complejidad del backend para que puedas concentrarte en construir tu aplicación.

**Comienza hoy:**

```bash
docker run -it --rm --volume /var/run/docker.sock:/var/run/docker.sock --volume $(pwd)/appwrite:/storage/config:rw --entrypoint="install" appwrite/appwrite:latest
```
O simplemente regístrate en [cloud.appwrite.io](https://cloud.appwrite.io).