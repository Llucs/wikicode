---
title: "Appwrite : Plateforme Backend-as-a-Service auto-hébergée"
description: "BaaS open-source fournissant des APIs pour l'authentification, les bases de données, le stockage, les fonctions serverless et la messagerie – une alternative à Firebase que vous contrôlez."
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

# Appwrite : Plateforme Backend-as-a-Service auto-hébergée

Appwrite est une plateforme **Backend-as-a-Service (BaaS) open-source** qui vous offre un ensemble complet d'API serveur et d'outils pour créer rapidement des applications web, mobiles et IA. Créé par Eldad Fux en 2019 et soutenu par une large communauté (40k+ étoiles GitHub), il est conçu comme une alternative auto-hébergée à Firebase, privilégiant la propriété des données, la confidentialité et un déploiement flexible.

Au lieu de câbler des microservices individuels, Appwrite fournit une API unifiée pour l'authentification, les bases de données, le stockage, les fonctions serverless, la messagerie et les événements en temps réel – le tout fonctionnant sur votre propre infrastructure.

---

## Pourquoi Appwrite ?

- **Propriété des données** – Vous contrôlez où et comment les données sont stockées, essentiel pour la conformité GDPR, HIPAA ou interne.
- **Pas de dépendance envers un fournisseur** – Auto-hébergé ou utilisez l'offre cloud ; votre code reste portable.
- **Ensemble riche de services** – Authentification (OAuth2, MFA, JWT, URLs magiques), bases de données NoSQL, stockage de fichiers, fonctions serverless, messagerie push/e-mail/SMS, abonnements en temps réel, et plus – tout dans un seul boîtier.
- **API simple et unifiée** – Un seul modèle SDK pour le web (JavaScript/TypeScript), Flutter, Android, iOS et le code serveur.
- **Écosystème open-source actif** – Soutenu par une communauté florissante, SDK officiels, CLI et une bibliothèque croissante d'intégrations (Stripe, Twilio, SendGrid, GPT-4o via les fonctions).
- **Du prototypage rapide à la production** – Utilisez la console d'administration pour une configuration sans code, puis intégrez le SDK pour un contrôle total.

---

## Fonctionnalités clés avec exemples de commandes

### Authentification
Prend en charge e-mail/mot de passe, téléphone (SMS), OAuth2 (Google, GitHub, Discord, etc.), URL magique, JWT, sessions anonymes et authentification multifacteur (MFA).

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

### Base de données (NoSQL)
Stockage basé sur des documents avec des requêtes avancées, recherche en texte intégral, écouteurs en temps réel et relations.

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

### Stockage
Téléchargements de fichiers avec prévisualisation d'image intégrée, redimensionnement, recadrage et analyse de logiciels malveillants.

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

### Fonctions serverless
Exécutez du code en réponse à des événements (base de données, stockage, authentification, planifications). Runtimes supportés : Node.js, Python, Ruby, PHP, Dart, Deno, Kotlin, Swift, .NET.

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

### Messagerie
Notifications push (FCM/APNS), e-mails (SMTP, SendGrid, Mailgun) et SMS (Twilio, Vonage, TextMagic). Le tout géré via la console d'administration ou l'API.

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

### Temps réel
Abonnez-vous aux événements de base de données, de stockage et de fonctions (basé sur WebSocket).

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
Appwrite expose un endpoint GraphQL complet – adapté aux frameworks front-end qui fonctionnent bien avec GraphQL.

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

### Console d'administration
Une interface web complète pour gérer tous les services – aucune programmation nécessaire pour créer des bases de données, des collections, des utilisateurs, des buckets de stockage ou des déclencheurs.

---

## Architecture

Appwrite utilise une **architecture microservices** orchestrée avec Docker. Chaque service s'exécute dans un conteneur isolé :

- **MariaDB** – magasin de métadonnées (projets, utilisateurs, etc.)
- **Redis** – cache et file d'attente de tâches
- **InfluxDB** – métriques d'utilisation et analyses
- **Kafka** – streaming de messages et d'événements
- **Workers** – tâches en arrière-plan (e-mails, fonctions, webhooks, migrations)

Des workers dédiés gèrent le travail asynchrone, maintenant l'API principale réactive. L'ensemble de la pile est lancé via une seule commande d'installation.

---

## Installation

### Auto-hébergé (Docker)

La façon la plus simple de faire fonctionner Appwrite sur votre propre serveur :

```bash
docker run -it --rm \
    --volume /var/run/docker.sock:/var/run/docker.sock \
    --volume "$(pwd)"/appwrite:/storage/config:rw \
    --entrypoint="install" \
    appwrite/appwrite:latest
```

### Cloud (géré)

Inscrivez-vous sur [cloud.appwrite.io](https://cloud.appwrite.io) – un niveau gratuit est disponible avec des limites d'utilisation, parfait pour le prototypage.

### Configuration de la console

Après l'installation (auto-hébergée ou cloud), créez un projet dans la console, notez l'ID du projet et l'endpoint, et générez une clé API.

---

## Utilisation de base (SDK JavaScript)

1. **Initialiser le client et s'authentifier**

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

2. **Créer et interroger des documents**

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

3. **Déployer une fonction via CLI**

   ```bash
   appwrite functions create --name='processOrder' --runtime='node-18.0' --execute='any'
   appwrite functions deploy --functionId='<ID>' --path='./functions/process-order'
   ```

4. **Écouter les événements en temps réel**

   ```javascript
   client.subscribe('databases.*.collections.*.documents', event => {
       console.log(`${event.events[0]} –`, event.payload);
   });
   ```

---

## Cas d'utilisation

- **Construire des MVP et des prototypes rapides** – évitez la configuration backend ; concentrez-vous sur la logique front-end.
- **Applications web full-stack** – React, Vue, Next.js, Svelte, Nuxt, Angular.
- **Applications mobiles multiplateformes** – Flutter, Android, iOS (SwiftUI), React Native.
- **Fonctionnalités basées sur l'IA** – intégrez GPT-4o ou d'autres LLM via des fonctions serverless.
- **Outils internes** – utilisez la console d'administration et les mises à jour en temps réel pour les tableaux de bord d'administration.
- **Applications conformes GDPR / HIPAA** – auto-hébergées dans votre propre centre de données.

---

## Comparaison avec des outils similaires

| Fonctionnalité            | Appwrite                        | Supabase                          | PocketBase                        |
|---------------------------|----------------------------------|-----------------------------------|-----------------------------------|
| Modèle de base de données | NoSQL (documents)                | SQL (PostgreSQL)                  | SQLite                            |
| Auto-hébergé              | Oui (Docker)                     | Oui (Docker)                      | Oui (binaire unique)              |
| Fonctions serverless      | Oui (Node, Python, Ruby, etc.)   | Oui (fonctions PostgreSQL + edge) | Oui (JavaScript/Go)               |
| Temps réel                | WebSocket (BD, Stockage, Événements) | Réplication PostgreSQL            | WebSocket (BD)                    |
| Authentification          | OAuth2, MFA, URL magique, SMS    | OAuth2, MFA, SSO                  | OAuth2, MFA                       |
| Messagerie                | Push, e-mail, SMS                | E-mail (via pgmq)                 | –                                 |
| Stockage                  | Prévisualisation d'image, redimensionnement, analyse | Oui (compatible S3)               | Oui                               |
| Interface d'administration | Console web complète            | Console web                       | Interface web minimale            |
| SDK clients               | Web, Flutter, Android, iOS, CLI  | Web, Flutter, Swift, Kotlin, etc. | Web, Dart, Android, iOS, Go       |

**Choisissez Appwrite** si vous avez besoin d'une plateforme NoSQL unifiée et orientée avec messagerie intégrée, GraphQL et une console d'administration riche – et si vous souhaitez conserver vos données sur votre propre pile Docker.

---

## Communauté et écosystème

- **GitHub** – [github.com/appwrite/appwrite](https://github.com/appwrite/appwrite)
- **Discord** – communauté de développeurs active
- **Modèles et projets ouverts** – voir [builtwith.appwrite.network](https://builtwith.appwrite.network)
- **Intégrations** – Appwrite MCP pour l'IA, les capteurs, la détection de fraude, et plus
- **Hackathons** – fréquemment présenté dans Hacktoberfest, défis Dev.to

---

## Conclusion

Appwrite est un BaaS open-source mature qui vous offre la puissance de Firebase sans le verrouillage. Sa capacité d'auto-hébergement, son ensemble riche de fonctionnalités et sa communauté active en font un excellent choix pour tout, des hackathons aux environnements d'entreprise réglementés. Que vous utilisiez la version cloud ou que vous l'exécutiez vous-même, Appwrite abstrait la complexité du backend afin que vous puissiez vous concentrer sur la création de votre application.

**Commencez dès aujourd'hui :**

```bash
docker run -it --rm --volume /var/run/docker.sock:/var/run/docker.sock --volume $(pwd)/appwrite:/storage/config:rw --entrypoint="install" appwrite/appwrite:latest
```

Ou inscrivez-vous simplement sur [cloud.appwrite.io](https://cloud.appwrite.io).