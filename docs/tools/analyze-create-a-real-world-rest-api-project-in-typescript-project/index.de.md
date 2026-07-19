---
title: Erstellen eines realen REST API-Projekts in TypeScript
description: Ein umfassender Leitfaden zur Erstellung eines robusten REST API-Systems mit TypeScript, Express.js und MongoDB.
created: 2026-07-19
tags:
  - TypeScript
  - Express.js
  - MongoDB
  - REST API
  - Authentifizierung
  - Docker
status:草稿
---

# Erstellen eines realen REST API-Projekts in TypeScript

Dieser Leitfaden führt Sie durch den Prozess der Erstellung eines robusten REST API-Systems unter Verwendung von TypeScript, Express.js und MongoDB. Er enthält detaillierte Dokumentation, Best Practices und real-world-Beispiele, um Ihnen dabei zu helfen, ein production-ready API-System zu implementieren.

## Hauptmerkmale

1. **TypeScript**: Statische Typisierung für bessere Fehlererkennung und bessere Codequalität.
2. **Express.js**: Eine beliebte Node.js Web-Application-Framework.
3. **MongoDB**: Eine NoSQL-Dokumentdatenbank zur Datenspeicherung.
4. **JWT-Authentifizierung**: Verwenden von JSON Web Tokens (JWT) für sichere Routen.
5. **Mongoose**: Ein Object Data Modeling (ODM) Library für MongoDB.
6. **Testing**: Einheitliche und Integrationstests mit Jest und Supertest.
7. **Swagger-Dokumentation**: Automatisch generierte API-Dokumentation zur leichteren Verwendung.

## Installation

1. **Repository klonen**:
   ```sh
   git clone https://github.com/username/repo.git
   cd repo
   ```

2. **Abhängigkeiten installieren**:
   ```sh
   npm install
   ```

3. **MongoDB einrichten**:
   - Installieren Sie MongoDB, wenn es noch nicht installiert ist.
   - Starten Sie den MongoDB-Server.
   - Konfigurieren Sie die Verbindungszeichenfolge im `.env`-File.

4. **Umgebungsvariablen konfigurieren**:
   - Aktualisieren Sie das `.env`-File mit notwendigen Umgebungsvariablen, wie z.B. die Datenbankverbindungszeichenfolge, das JWT-Secret, usw.

5. **Server starten**:
   ```sh
   npm start
   ```

## Grundlegende Nutzung

### API-Endpunkte

1. **Benutzerverwaltung**:
   - **Benutzer erstellen**: POST `/api/users`
   - **Benutzer abrufen**: GET `/api/users/:id`
   - **Benutzer aktualisieren**: PATCH `/api/users/:id`
   - **Benutzer löschen**: DELETE `/api/users/:id`

2. **Produktverwaltung**:
   - **Produkt erstellen**: POST `/api/products`
   - **Produkt abrufen**: GET `/api/products/:id`
   - **Produkt aktualisieren**: PATCH `/api/products/:id`
   - **Produkt löschen**: DELETE `/api/products/:id`

3. **Bestellverwaltung**:
   - **Bestellung erstellen**: POST `/api/orders`
   - **Bestellung abrufen**: GET `/api/orders/:id`
   - **Bestellung aktualisieren**: PATCH `/api/orders/:id`
   - **Bestellung löschen**: DELETE `/api/orders/:id`

4. **Authentifizierung**:
   - **JWT-Token generieren**: POST `/api/auth/login`
   - **Schützte Routen schützen**: Verwenden Sie das JWT-Token im `Authorization`-Header

### Testing

1. **Einheitliche Testing**:
   - Verwenden Sie Jest für die Einheitliche Testing.
   - Führen Sie die Tests mit:
     ```sh
     npm test
     ```

2. **Integration Testing**:
   - Verwenden Sie Supertest für die Integration Testing.
   - Führen Sie die Tests mit:
     ```sh
     npm test
     ```

### Swagger-Dokumentation

1. **Swagger UI aufbauen**:
   - Navigieren Sie zu `http://localhost:3000/docs` in Ihrem Browser.
   - Nutzen Sie die generierte Dokumentation, um das API zu verstehen und mitzuarbeiten.

### Authentifizierung

1. **JWT-Token generieren**:
   - Führen Sie einen POST-Request an `/api/auth/login` mit Benutzerdaten durch.
   - Beispiel mit `curl`:
     ```sh
     curl -X POST http://localhost:3000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password"}'
     ```

2. **JWT in Anfragen verwenden**:
   - Fügen Sie das JWT im `Authorization`-Header zu geschützten Routen hinzu.
   - Beispiel mit `curl`:
     ```sh
     curl -X GET http://localhost:3000/api/users/1 \
     -H "Authorization: Bearer <JWT_TOKEN>"
     ```

### Datenverwaltung

1. **Mongoose Schemata definieren**:
   - Verwenden Sie Mongoose, um Schemata für Modelle zu definieren.
   - Beispiel für ein Benutzerschema:
     ```typescript
     import { Schema, model } from 'mongoose';

     const UserSchema = new Schema({
       name: String,
       email: { type: String, unique: true },
       password: String
     });

     export const User = model('User', UserSchema);
     ```

2. **CRUD-Operationen durchführen**:
   - Verwenden Sie Mongoose-Methoden für CRUD-Operationen.
   - Beispiel zur Erstellung eines Benutzers:
     ```typescript
     import { Request, Response } from 'express';
     import User from '../models/User';

     const createUser = async (req: Request, res: Response) => {
       const { name, email, password } = req.body;
       const user = new User({ name, email, password });
       await user.save();
       res.status(201).json(user);
     };
     ```

## Abschluss

Indem Sie den detaillierten Leitfaden nachvollziehen und den bereitgestellten Codebasen als Ausgangspunkt verwenden, können Sie das API erweitern und an Ihre spezifischen Projektoberlegungen anpassen. Dieses umfassende Projekt bietet nicht nur einen praktischen Beispielsystem, sondern dient auch als ausgezeichnetes Lernmaterial für das Verständnis moderner Web-Entwicklungspraktiken mit TypeScript, Express.js und MongoDB.

Glückwunsch beim Coden!