---
title: OAuth 2.1 mit PKCE-Best-Praxis
description: Detaillierte Leitlinien zur Sicherung von OAuth 2.1-Implementierungen mit Proof Key for Code Exchange (PKCE), um Anmeldecode-Injektionsangriffe zu verhindern.
created: 2026-07-13
tags:
  - OAuth
  - PKCE
  - Sicherheit
  - API
status: Entwurf
---

# OAuth 2.1 mit PKCE-Best-Praxis

OAuth 2.1 mit Proof Key for Code Exchange (PKCE) ist ein Protokollextension, die die Sicherheit des OAuth 2.0-Autorisierungsframeworks verbessert. PKCE ist speziell dazu entwickelt, den Risiken von Anmeldecode-Intercepting entgegenzuwirken, was bei offenen Clients (z.B. mobilen Apps oder Single-Page-Apps) auftreten kann, die keine sicheren Methoden zur Verwendung von Client-Secrets haben.

## Hauptmerkmale

1. **Code-Verifier/Challenge**: Zufallsgeneriertes String, das vom Client verwendet wird, um den PKCE-Code-Challenge zu generieren. Der Code-Verifier bleibt geheim und wird nicht über das Netzwerk gesendet.
2. **Code-Challenge**: Hash des Code-Verifiers, der an die Autorisierungsstelle gesendet wird.
3. **Anmeldecode-Ausschließlichkeitsablauf**: Der Prozess bleibt grundsätzlich gleich, enthält aber die Hinzufügung von PKCE.

## Geschichte

OAuth 2.1 mit PKCE wurde als Erweiterung des OAuth 2.0 vorgeschlagen, um Sicherheitsprobleme in der Client-Authentifizierung zu bewältigen. Es wurde zuerst in RFC 7636 vorgeschlagen und später in der OAuth 2.1-Spezifikation integriert.

## Nutzungsfälle

- **Offene Clients**: Mobile Apps, Single-Page-Apps und jede App, die keine sicheren Methoden zur Speicherung von Client-Secrets besitzt.
- **API-Sicherheit**: Verbessern der Sicherheit von API-Zugriff und Authentifizierung für Web- und mobile Apps.
- **Web-Apps**: Verbessern der Sicherheit von Web-Apps, die OAuth für die Authentifizierung verwenden.

## Installation

Während OAuth 2.1 mit PKCE ein Protokollextension ist, um es zu implementieren, umfasst dies typischerweise die folgenden Schritte:

1. **Clientseitige Implementierung**:
   - Erstellen eines Code-Verifiers und eines Code-Challenges.
   - Verwenden des Code-Challenge im Autorisierungsanforderung.
   - Verwalten des Autorisierungsresponses und Austauschen des Anmeldecodes für einen Zugriffstonken.

2. **Serverseitige Implementierung**:
   - Überprüfen des Code-Challenges auf den Code-Verifier.
   - Verwalten des Autorisierungsresponses und Austauschen des Anmeldecodes für einen Zugriffstonken.

### Basis-Nutzung

1. **Client-Autentifizierung**:
   - Der Client generiert einen Code-Verifier und einen Code-Challenge.
   - Der Code-Challenge wird in der Autorisierungsanforderung verwendet.

2. **Autorisierungsantwort**:
   - Der Benutzer gibt Zutritt zu oder ablehnt den Zugriff.
   - Die Autorisierungsstelle antwortet mit einem Anmeldecode.

3. **Zugriffstonkenanforderung**:
   - Der Client tauscht den Anmeldecode gegen einen Zugriffstonken aus, den Code-Verifier verwendet.

4. **Überprüfung**:
   - Die Autorisierungsstelle überprüft den Code-Challenge und den Code-Verifier, um die Authentifiziertheit des Clients zu bestätigen.

## Best-Praxis

1. **Starken Code-Verifiers verwenden**:
   - Verwenden Sie einen kryptografisch sicheren pseudorzufälligen Zahlengenerator (CSPRNG) zum Generieren von Code-Verifiers.
   - Sorgen Sie dafür, dass der Code-Verifier mindestens 43 Zeichen lang ist, um Zeitangriffe zu mindern.

2. **Code-Challenge-Methoden**:
   - Verwenden Sie den `S256`-Methoden für das Hashen des Code-Verifiers. Diese Methode ist gegen Zeitangriffe gestaltet.

3. **Client-Autentifizierung**:
   - Verwenden Sie angemessene Autentifizierungsmethoden für den Client-Typ (z.B. `client_secret_basic` für vertrauliche Clients, `none` für offene Clients).

4. **Transport-Sicherheit**:
   - Stellen Sie sicher, dass alle Kommunikation über HTTPS erfolgt, um den Code-Challenge und andere sensible Informationen zu schützen.

5. **Sitzungsinventarverwaltung**:
   - Implementieren Sie eine angemessene Sitzungsinventarverwaltung, um sicherzustellen, dass der Anmeldecode nicht wiederholt wird.

6. **Reguläre Audits und Aktualisierungen**:
   - Regelmäßig überprüfen und aktualisieren Sie Ihre Implementierung, um sich mit den neuesten Sicherheitspraktiken und Standards zu vertrauten.

7. **Begrenzung der Anfragen (Rate Limiting)**:
   - Implementieren Sie Begrenzungen, um Missbrauch und Bruteforce-Angriffe zu verhindern.

8. **Protokollierung und Überwachung**:
   - Protokollieren und überwachen Sie Autorisierungsanfragen und -antworten, um gegebenenfalls verfahrene Aktivitäten zu erkennen und zu beantworten.

Indem Sie sich an diese Best-Praxis halten, können Sie die Sicherheit Ihrer OAuth 2.1-Implementierung mit PKCE verbessern, was sensibles Information schützt und Ihre Anwendung sich sichert.

## Beispiel: Python-Implementierung

Hier ist ein grundlegendes Beispiel zur Implementierung von PKCE in Python mit der `requests`-Bibliothek:

```python
import requests
import string
import random
import hashlib

# Erstellen eines Code-Verifiers
def generate_code_verifier(length=43):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Erstellen eines Code-Challenges
def generate_code_challenge(verifier):
    sha256 = hashlib.sha256()
    sha256.update(verifier.encode('utf-8'))
    return sha256.hexdigest()[:43]

# Beispiel für Client-Autentifizierung
def authenticate_client(authorization_url, client_id, redirect_uri, code_verifier):
    # Erstellen des Code-Challenge
    code_challenge = generate_code_challenge(code_verifier)

    # Autorisierungsanforderung
    auth_params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge
    }

    response = requests.get(authorization_url, params=auth_params)
    if response.status_code != 200:
        raise Exception("Fehler bei der Client-Autentifizierung")

    # Verwalten des Benutzerinteraktion und Erhalten des Anmeldecodes

    # Zugriffstonkenanforderung
    token_params = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri,
        'code_verifier': code_verifier
    }

    token_response = requests.post(token_url, data=token_params, auth=(client_id, 'client_secret'))
    if token_response.status_code != 200:
        raise Exception("Fehler beim Abrufen des Zugriffstonkens")

    return token_response.json()

# Nutzung
client_id = 'deine_client_id'
redirect_uri = 'http://deine-redirect-uri'
authorization_url = 'https://deine-autorisierungsstelle'
code_verifier = generate_code_verifier()
code_challenge = generate_code_challenge(code_verifier)
access_token = authenticate_client(authorization_url, client_id, redirect_uri, code_verifier)
print("Zugriffstonken:", access_token['access_token'])
```

Dieses Beispiel zeigt, wie Sie einen Code-Verifier und -Challenge erzeugen, eine Autorisierungsanforderung durchführen und den Anmeldecode gegen einen Zugriffstonken austauschen.