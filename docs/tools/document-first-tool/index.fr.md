---
title: cURL — Outil de transfert de données
description: cURL est un outil en ligne de commande pour transférer des données via des protocoles réseau.
created: 2026-06-14
tags:
  - tool
  - cli
  - networking
status: draft
ecosystem: networking
---

# cURL — Outil de transfert de données

## Ce que c'est

cURL (Client URL) est un outil en ligne de commande et une bibliothèque pour transférer des données avec des URL. Il prend en charge des dizaines de protocoles, notamment HTTP, HTTPS, FTP, SFTP, SCP, LDAP et bien d'autres.

## Installation

```bash
# Ubuntu/Debian
sudo apt-get install curl

# macOS (pre-installed, or via Homebrew)
brew install curl

# Windows (via Chocolatey)
choco install curl
```

## Utilisation de base

### Requête GET

```bash
curl https://api.github.com/users/octocat
```

### POST avec JSON

```bash
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com"}'
```

### Sauvegarder la réponse dans un fichier

```bash
curl -o output.json https://api.example.com/data
```

### Suivre les redirections

```bash
curl -L https://bit.ly/example
```

### En-têtes personnalisés

```bash
curl -H "Authorization: Bearer token123" https://api.example.com/protected
```

## Options principales

| Flag | Description |
|------|-------------|
| `-X` | Méthode HTTP (GET, POST, PUT, DELETE) |
| `-H` | En-tête personnalisé |
| `-d` | Données du corps de la requête |
| `-o` | Écrire la sortie dans un fichier |
| `-L` | Suivre les redirections |
| `-v` | Mode verbeux |
| `-s` | Mode silencieux (sans progression) |
| `-k` | Autoriser SSL non sécurisé |
| `-u` | Authentification de base (utilisateur:mot de passe) |

## Meilleures pratiques

- Utilisez `-sS` dans les scripts pour supprimer la progression mais garder les erreurs visibles.
- Utilisez `--retry 3` pour des tentatives automatiques en cas d'échecs réseau.
- Ne passez jamais de jetons dans les URL; utilisez plutôt l'en-tête `Authorization`.