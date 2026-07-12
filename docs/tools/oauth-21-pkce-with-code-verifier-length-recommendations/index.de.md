---
title: OAuth 2.1 PKCE mit Anmeldecodeverifier-Länge-Richtlinien
description: Leitfaden zur Implementierung von OAuth 2.1 PKCE mit Empfehlungen zur Anmeldecodeverifier-Länge zum Erhöhen der Sicherheit.
created: 2026-07-12
tags:
  - OAuth
  - PKCE
  - Sicherheit
status: Entwurf
---

# OAuth 2.1 PKCE mit Anmeldecodeverifier-Länge-Richtlinien

## Was ist PKCE?

PKCE (Proof Key for Code Exchange) ist eine Sicherheitsmechanismus in OAuth 2.0, um Angreifer daran zu hindern, den Autorisierungscode zu erhalten. Es fügt eine zusätzliche Sicherheitslayer hinzu, indem es ein eindeutiges, nicht wiederverwendbares Schlüssel (der Anmeldecodeverifier) zwischen dem Client und dem Autorisierungsserver austauscht.

## Schlüsselmerkmale von OAuth 2.1 PKCE

- **Anmeldecodeverifier**: Zufälliger String, der zwischen dem Client und dem Autorisierungsserver als Geheimnis verwendet wird.
- **Anmeldecodechallenge**: Hash des Anmeldecodeverifiers, um Netzwerk-sniffting zu verhindern.
- **Nonce**: Eindeutiger Wert, der im Autorisierungsanfrage eingeschlossen wird, um sicherzustellen, dass der Code nur einmal verwendet wird.

## Geschichte von PKCE

PKCE wurde als optionaler Mechanismus in OAuth 2.0 eingeführt, um die Sicherheit zu erhöhen. Allerdings ist es Teil der OAuth 2.1-Spezifikation und wird als Pflichtelement eingeführt, um eine höhere Sicherheitsstufe zu gewährleisten, insbesondere für öffentliche Clients.

## Einsatzfälle für PKCE

- **Öffentliche Clients**: Clients, die sichere Speicherung von Geheimnissen nicht ermöglichen, wie Webanwendungen und mobilere Apps.
- **Hybride Fluss**: Eignet sich für Szenarien, in denen der Client den Autorisierungscode für einen Zugriffstoken austauschen muss.
- **Autorisierungscode-Fluss**: Erhöht die Sicherheit in Szenarien, in denen der Client den Nutzer an einen Autorisierungs-Server umleitet.

## Anmeldecodeverifier-Länge-Richtlinien

Die Länge des Anmeldecodeverifiers ist ein kritischer Aspekt der PKCE-Sicherheit. Der Anmeldecodeverifier sollte so lang sein, dass er Wiederholungsangriffe widerstandsfähig ist, aber so kurz, dass er im Client umsetzbar ist.

### Empfohlene Längen

- **Minimale Länge**: 43 Zeichen
- **Empfohlene Länge**: 128 Zeichen oder mehr

Je länger der Anmeldecodeverifier, desto sicherer ist er gegen Wiederholungsangriffe. Die minimale Länge von 43 Zeichen wird vom OAuth 2.1-Spezifikationen empfohlen, um eine vernünftige Sicherheitsstufe zu gewährleisten. Allerdings bietet der Einsatz eines längeren Anmeldecodeverifiers, wie 128 Zeichen, eine viel höhere Sicherheitsmarge.

## Installation und Basisverwendung

### Schritt 1: Generieren des Anmeldecodeverifiers

```python
import random
import string

def generate_code_verifier(length=128):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
```

### Schritt 2: Generieren des Anmeldecodechallenges

```python
import hashlib
import base64

def generate_code_challenge(code_verifier):
    code_challenge = hashlib.sha256(code_verifier.encode()).digest()
    return base64.urlsafe_b64encode(code_challenge).rstrip(b'=').decode()
```

### Schritt 3: PKCE in OAuth 2.0-Fluss integrieren

1. **Autorisierungsanfrage**:
   - Füge `code_challenge` und `code_challenge_method` zur Autorisierungsanfrage hinzu.
   - Beispiel:
     ```http
     GET /authorize?response_type=code&client_id=your_client_id&redirect_uri=https%3A%2F%2Fyourapp.com%2Fcallback&code_challenge=your_code_challenge&code_challenge_method=S256&state=some_state_value&nonce=some_nonce_value
     ```

2. **Zugriffstokenanfrage**:
   - Füge `code_verifier` zur Zugriffstokenanfrage hinzu.
   - Beispiel:
     ```http
     POST /token HTTP/1.1
     Host: your_authorization_server.com
     Content-Type: application/x-www-form-urlencoded

     grant_type=authorization_code&code=your_authorization_code&redirect_uri=https%3A%2F%2Fyourapp.com%2Fcallback&code_verifier=your_code_verifier
     ```

## Zusammenfassung

Die Nutzung von PKCE mit einer ausreichend langen Anmeldecodeverifier (mindestens 128 Zeichen) ist entscheidend für die Erhöhung der Sicherheit von OAuth 2.0-Flüssen, insbesondere in Szenarien mit öffentlichen Clients. Durch die Einhaltung der empfohlenen Praktiken können Entwickler eine höhere Sicherheitsstufe für ihre Anwendungen gewährleisten.