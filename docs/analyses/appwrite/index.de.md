---
title: Appwrite: Selbstgehostete Backend-as-a-Service-Plattform
description: Open-Source-BaaS, das APIs für Authentifizierung, Datenbanken, Speicher, serverlose Funktionen und Messaging bereitstellt – eine Firebase-Alternative, die Sie kontrollieren.
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

# Appwrite: Selbstgehostete Backend-as-a-Service-Plattform

Appwrite ist eine **Open-Source-Backend-as-a-Service (BaaS)**-Plattform, die Ihnen einen vollständigen Satz von Server-APIs und Tools bietet, um schnell Web-, Mobil- und KI-Apps zu erstellen. Erstellt von Eldad Fux im Jahr 2019 und jetzt von einer großen Community unterstützt (40k+ GitHub-Sterne), ist es als selbstgehostete Alternative zu Firebase konzipiert, die Datenhoheit, Privatsphäre und flexible Bereitstellung priorisiert.

Anstatt einzelne Microservices zu verdrahten, bietet Appwrite eine einheitliche API für Authentifizierung, Datenbanken, Speicher, serverlose Funktionen, Messaging und Echtzeit-Ereignisse – alles betrieben auf Ihrer eigenen Infrastruktur.

---

## Warum Appwrite?

- **Datenhoheit** – Sie kontrollieren, wo und wie Daten gespeichert werden, entscheidend für GDPR, HIPAA oder interne Compliance.
- **Keine Vendor-Lock-in** – Selbst gehostet oder die Cloud-Angebote nutzbar; Ihr Code bleibt portabel.
- **Umfangreicher Service-Satz** – Auth (OAuth2, MFA, JWT, Magic URLs), NoSQL-Datenbanken, Dateispeicher, serverlose Funktionen, Push-/E-Mail-/SMS-Messaging, Echtzeit-Abonnements und mehr – alles in einer Box.
- **Einfache, einheitliche API** – Ein SDK-Muster für Web (JavaScript/TypeScript), Flutter, Android, iOS und serverseitigen Code.
- **Aktives Open-Source-Ökosystem** – Unterstützt von einer lebendigen Community, offiziellen SDKs, CLI und einer wachsenden Bibliothek von Integrationen (Stripe, Twilio, SendGrid, GPT-4o via Functions).
- **Schnelles Prototyping bis zur Produktion** – Nutzen Sie die Admin Console für No-Code-Setup, dann das SDK für vollständige Kontrolle.

---

## Hauptfunktionen mit Befehlsbeispielen

### Authentifizierung
Unterstützt E-Mail/Passwort, Telefon (SMS), OAuth2 (Google, GitHub, Discord, etc.), Magic URL, JWT, anonyme Sitzungen und Multi-Faktor-Authentifizierung (MFA).

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

### Datenbank (NoSQL)
Dokumentbasierter Speicher mit erweiterten Abfragen, Volltextsuche, Echtzeit-Listenern und Beziehungen.

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

### Speicher
Datei-Uploads mit integrierter Bildvorschau, Größenänderung, Zuschneiden und Malware-Scan.

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

### Serverlose Funktionen
Führen Sie Code als Reaktion auf Ereignisse aus (Datenbank, Speicher, Auth, Zeitpläne). Unterstützte Runtimes: Node.js, Python, Ruby, PHP, Dart, Deno, Kotlin, Swift, .NET.

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

### Messaging
Push-Benachrichtigungen (FCM/APNS), E-Mails (SMTP, SendGrid, Mailgun) und SMS (Twilio, Vonage, TextMagic). Alles über die Admin Console oder API verwaltet.

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

### Echtzeit
Abonnieren Sie Datenbank-, Speicher- und Funktionsereignisse (WebSocket-basiert).

```javascript
import { Client } from 'appwrite';

const client = new Client()
    .setEndpoint('https://<HOST>/v1')
    .setProject('<PROJECT_ID>');

client.subscribe('databases.<DB_ID>.collections.<COLL_ID>.documents', response => {
    console.log('Document changed:', response.payload);
});
```

### GraphQL-API
Appwrite stellt einen vollständigen GraphQL-Endpunkt bereit – geeignet für Frontend-Frameworks, die gut mit GraphQL arbeiten.

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

### Admin Console
Eine vollständige Weboberfläche zur Verwaltung aller Dienste – keine Codierung erforderlich, um Datenbanken, Sammlungen, Benutzer, Speicher-Buckets oder Trigger zu erstellen.

---

## Architektur

Appwrite verwendet eine **Microservices-Architektur**, die mit Docker orchestriert wird. Jeder Dienst läuft als isolierter Container:

- **MariaDB** – Metadatenspeicher (Projekte, Benutzer, etc.)
- **Redis** – Cache und Job-Warteschlange
- **InfluxDB** – Nutzungsmetriken und Analysen
- **Kafka** – Nachrichten- und Ereignis-Streaming
- **Workers** – Hintergrundaufgaben (E-Mails, Funktionen, Webhooks, Migrationen)

Dedizierte Worker erledigen asynchrone Arbeit und halten die Haupt-API reaktionsfähig. Der gesamte Stack wird mit einem einzigen Installationsbefehl gestartet.

---

## Installation

### Selbst gehostet (Docker)

Der einfachste Weg, Appwrite auf Ihrem eigenen Server zum Laufen zu bringen:

```bash
docker run -it --rm \
    --volume /var/run/docker.sock:/var/run/docker.sock \
    --volume "$(pwd)"/appwrite:/storage/config:rw \
    --entrypoint="install" \
    appwrite/appwrite:latest
```

Dies startet einen interaktiven Installer, der alle erforderlichen Container herunterlädt und konfiguriert. Standardmäßig läuft Appwrite auf `http://0.0.0.0`.

### Cloud (Managed)

Melden Sie sich unter [cloud.appwrite.io](https://cloud.appwrite.io) an – ein kostenloser Tarif mit Nutzungslimits ist verfügbar, perfekt für Prototyping.

### Konsolen-Setup

Nach der Installation (selbst gehostet oder Cloud) erstellen Sie ein Projekt in der Konsole, notieren Sie die Projekt-ID und den Endpunkt und generieren Sie einen API-Schlüssel.

---

## Grundlegende Nutzung (JavaScript SDK)

1. **Client initialisieren und authentifizieren**

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

2. **Dokumente erstellen und abfragen**

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

3. **Eine Funktion über die CLI bereitstellen**

   ```bash
   appwrite functions create --name='processOrder' --runtime='node-18.0' --execute='any'
   appwrite functions deploy --functionId='<ID>' --path='./functions/process-order'
   ```

4. **Echtzeit-Ereignisse abhören**

   ```javascript
   client.subscribe('databases.*.collections.*.documents', event => {
       console.log(`${event.events[0]} –`, event.payload);
   });
   ```

---

## Anwendungsfälle

- **MVPs & schnelle Prototypen erstellen** – Backend-Setup überspringen; sich auf die Frontend-Logik konzentrieren.
- **Full-Stack-Web-Apps** – React, Vue, Next.js, Svelte, Nuxt, Angular.
- **Plattformübergreifende Mobile-Apps** – Flutter, Android, iOS (SwiftUI), React Native.
- **KI-gestützte Funktionen** – GPT-4o oder andere LLMs über serverlose Funktionen integrieren.
- **Interne Tools** – Admin Console und Echtzeit-Updates für Admin-Dashboards nutzen.
- **GDPR-/HIPAA-konforme Apps** – Selbst in Ihrem eigenen Rechenzentrum hosten.

---

## Vergleich mit ähnlichen Tools

| Funktion                | Appwrite                        | Supabase                          | PocketBase                        |
|--------------------------|----------------------------------|-----------------------------------|-----------------------------------|
| Datenbankmodell          | NoSQL (Dokumente)                | SQL (PostgreSQL)                  | SQLite                            |
| Selbst gehostet          | Ja (Docker)                     | Ja (Docker)                       | Ja (einzelne Binärdatei)          |
| Serverlose Funktionen    | Ja (Node, Python, Ruby, etc.)   | Ja (PostgreSQL-Funktionen + Edge) | Ja (JavaScript/Go)                |
| Echtzeit                 | WebSocket (DB, Speicher, Events)| PostgreSQL-Replikation            | WebSocket (DB)                    |
| Authentifizierung        | OAuth2, MFA, Magic URL, SMS     | OAuth2, MFA, SSO                  | OAuth2, MFA                       |
| Messaging                | Push, E-Mail, SMS               | E-Mail (via pgmq)                 | –                                 |
| Speicher                 | Bildvorschau, Größenänderung, Scan | Ja (S3-kompatibel)              | Ja                                |
| Admin-UI                 | Voll funktionsfähige Web-Konsole | Web-Konsole                       | Minimale Web-Oberfläche            |
| Client-SDKs              | Web, Flutter, Android, iOS, CLI | Web, Flutter, Swift, Kotlin, etc. | Web, Dart, Android, iOS, Go       |

**Appwrite wählen**, wenn Sie eine einheitliche, meinungsstarke NoSQL-Plattform mit integriertem Messaging, GraphQL und einer umfangreichen Admin-Konsole benötigen und Ihre Daten auf Ihrem eigenen Docker-Stapel behalten möchten.

---

## Community & Ökosystem

- **GitHub** – [github.com/appwrite/appwrite](https://github.com/appwrite/appwrite)
- **Discord** – aktive Entwickler-Community
- **Vorlagen & offene Projekte** – siehe [builtwith.appwrite.network](https://builtwith.appwrite.network)
- **Integrationen** – Appwrite MCP für KI, Sensoren, Betrugserkennung und mehr
- **Hackathons** – häufig in Hacktoberfest, Dev.to Challenges vorgestellt

---

## Fazit

Appwrite ist ein ausgereiftes, quelloffenes BaaS, das Ihnen die Leistung von Firebase ohne Vendor-Lock-in bietet. Die Fähigkeit zum Selbsthosten, der umfangreiche Funktionsumfang und die aktive Community machen es zu einer ausgezeichneten Wahl für alles von Hackathons bis hin zu regulierten Unternehmensumgebungen. Ob Sie die Cloud-Version nutzen oder es selbst betreiben, Appwrite abstrahiert die Backend-Komplexität, damit Sie sich auf die Entwicklung Ihrer App konzentrieren können.

**Heute starten:**

```bash
docker run -it --rm --volume /var/run/docker.sock:/var/run/docker.sock --volume $(pwd)/appwrite:/storage/config:rw --entrypoint="install" appwrite/appwrite:latest
```
Oder melden Sie sich einfach unter [cloud.appwrite.io](https://cloud.appwrite.io) an.