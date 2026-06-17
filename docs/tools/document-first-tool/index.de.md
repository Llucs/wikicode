---
title: cURL — Datenübertragungstool
description: cURL ist ein Befehlszeilenwerkzeug zur Datenübertragung mit Netzwerkprotokollen.
created: 2026-06-14
tags:
  - tool
  - cli
  - networking
status: draft
ecosystem: networking
---

# cURL — Datenübertragungstool

## Was es ist

cURL (Client URL) ist ein Befehlszeilenwerkzeug und eine Bibliothek zur Datenübertragung mit URLs. Es unterstützt Dutzende von Protokollen, darunter HTTP, HTTPS, FTP, SFTP, SCP, LDAP und viele mehr.

## Installation

```bash
# Ubuntu/Debian
sudo apt-get install curl

# macOS (pre-installed, or via Homebrew)
brew install curl

# Windows (via Chocolatey)
choco install curl
```

## Grundlegende Verwendung

### GET-Anfrage

```bash
curl https://api.github.com/users/octocat
```

### POST mit JSON

```bash
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com"}'
```

### Antwort in Datei speichern

```bash
curl -o output.json https://api.example.com/data
```

### Weiterleitungen folgen

```bash
curl -L https://bit.ly/example
```

### Benutzerdefinierte Header

```bash
curl -H "Authorization: Bearer token123" https://api.example.com/protected
```

## Wichtige Flags

| Flag | Beschreibung |
|------|--------------|
| `-X` | HTTP-Methode (GET, POST, PUT, DELETE) |
| `-H` | Benutzerdefinierter Header |
| `-d` | Anfragedaten |
| `-o` | Ausgabe in Datei schreiben |
| `-L` | Weiterleitungen folgen |
| `-v` | Ausführlicher Modus |
| `-s` | Stiller Modus (keine Fortschrittsanzeige) |
| `-k` | Unsicheres SSL erlauben |
| `-u` | Basis-Authentifizierung (Benutzer:Passwort) |

## Best Practices

- Verwenden Sie `-sS` in Skripten, um die Fortschrittsanzeige zu unterdrücken, aber Fehler sichtbar zu lassen.
- Verwenden Sie `--retry 3` für automatische Wiederholungen bei Netzwerkfehlern.
- Übergeben Sie niemals Tokens in URLs; verwenden Sie stattdessen den `Authorization`-Header.