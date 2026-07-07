---
title: Verhindern von JWT-Schlüsselinjektionen
description: Schützen Sie sich vor möglichen SQL-Injektion- oder Command-Injektion-Angriffen, indem Sie den `kid`-Parameter vor der Verwendung zur Abrufung des Verschlüsselungsschlüssels von einer Datenbank oder einem Systembefehl sauber verarbeiten.
created: 2026-07-07
tags:
  - jwt
  - Sicherheit
  - Injektion
status:草稿
---

# Verhindern von JWT-Schlüsselinjektionen

## Was ist eine JWT-Schlüsselinjektion?

Eine JWT-Schlüsselinjektion ist ein Sicherheitsvulnerabilität, bei der ein Angreifer einen JSON Web Token (JWT) injizieren oder verändern kann, um unberechtigten Zugriff auf ein System zu erhalten. Dies kann passieren, wenn ein System das JWT falsch validiert oder seine Integrität nicht überprüft, was den Angreifer dazu bringt, das Payload oder die Signatur des Tokens zu modifizieren.

## Hauptfunktionen

1. **Signaturverifikation**: Sichern Sie sich, dass die Signatur des JWTs gültig und unverändert ist.
2. **Payload-Integrität**: Verifizieren Sie, dass das Payload-Content im JWT nicht verändert wurde.
3. **Ablaufzeitprüfung**: Sichern Sie sich, dass das JWT nicht abgelaufen ist.
4. **Abolungskontrolle**: Prüfen Sie, ob das JWT abgebolgt wurde.

## Geschichte

Der Konzept von JWTs wurde seit der Einführung des JSON Web Token Standards im Jahr 2010 verwendet. Allerdings hat sich die spezifische Frage der Schlüsselinjektion-Sicherheitslücken in den letzten Jahren verstärkt, da mehr Anwendungen JWTs für die Authentifizierung und Autorisierung verwenden. Bekannte Schwachstellen, wie diejenigen, die im OWASP (Open Web Application Security Project) Leitfaden aufgezeigt wurden, haben die Aufmerksamkeit auf die Sicherheit von JWTs erhöht.

## Nutzungsfallbeispiele

1. **Authentifizierung und Autorisierung**: JWTs werden in web- und mobile Anwendungen weit verbreitete Authentifizierung und Autorisierung verwendet.
2. **Staatlose Sitzungen**: JWTs werden oft in stateless APIs verwendet, um die Sitzungszustände zu verwalten.
3. **Single Sign-On (SSO)**: JWTs können für SSO verwendet werden, indem ein Benutzer einmal angemeldet wird und dann über mehrere Systeme verifiziert wird.

## Installation

Die JWT-Validierung wird normalerweise durch eine Bibliothek oder einen Framework verarbeitet, die JWTs unterstützt. Zum Beispiel in einer Node.js-Anwendung können Sie die Bibliothek `jsonwebtoken` für die Erstellung und Überprüfung von Tokens verwenden. Hier ist ein grundlegendes Installationsprozedur:

1. **Node.js**:
   ```bash
   npm install jsonwebtoken
   ```
2. **Python**:
   ```bash
   pip install PyJWT
   ```

## Grundlegende Nutzung

Hier ist ein grundlegender Beispiel für JWT-Überprüfung in Node.js mit `jsonwebtoken`:

1. **Erstellen eines JWTs**:
   ```javascript
   const jwt = require('jsonwebtoken');

   const secret = 'your-secret-key';
   const payload = { userId: 123, role: 'admin' };

   const token = jwt.sign(payload, secret);
   console.log(token);
   ```

2. **Überprüfen eines JWTs**:
   ```javascript
   jwt.verify(token, secret, (err, decoded) => {
     if (err) {
       console.error('Token-Überprüfung fehlgeschlagen:', err);
     } else {
       console.log('Dezodiert:', decoded);
     }
   });
   ```

## Verhindern von Schlüsselinjektionen

1. **Sichere Schlüsselverwaltung**: Halten Sie den JWT-Schlüssel sicher und zeigen Sie ihn nicht im clientseitigen Code an.
2. **Tokenablaufzeit**: Legen Sie eine vernünftige Ablaufzeit für JWTs fest, um die Angriffsmöglichkeit zu minimieren.
3. **Abolungskontrollmechanismus**: Implementieren Sie ein Mechanismus zur Abolung von Tokens, die kompromittiert wurden.
4. **Signaturverifikation**: Verifizieren Sie die Token-Signatur immer auf dem Serverseiten.
5. **Payload-Whitelisting**: Erlassen Sie nur verwhiteliste Ansprüche im JWT-Payload.

### Beispiel für eine Abolungskontrolle

Sie können eine Liste von abgebolgten Tokens in einer Datenbank verwalten und diese Liste während der Tokenüberprüfung abfragen:

1. **Datenbank-Erstellung**:
   ```sql
   CREATE TABLE revoked_tokens (
     token VARCHAR(255) PRIMARY KEY
   );
   ```

2. **Prüfen auf abgebolgte Token**:
   ```javascript
   const isTokenRevoked = (token) => {
     const tokenExists = revokedTokens.some((revokedToken) => revokedToken === token);
     return tokenExists;
   };

   jwt.verify(token, secret, (err, decoded) => {
     if (err || isTokenRevoked(token)) {
       console.error('Token-Überprüfung fehlgeschlagen:', err);
     } else {
       console.log('Dezodiert:', decoded);
     }
   });
   ```

Indem Sie diese Strategien implementieren, können Sie die Risiken von JWT-Schlüsselinjektionen in Ihren Anwendungen erheblich reduzieren.