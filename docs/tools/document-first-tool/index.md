---
title: cURL — Data Transfer Tool
description: cURL is a command-line tool for transferring data using network protocols.
created: 2026-06-14
tags:
  - tool
  - cli
  - networking
status: draft
---

# cURL — Data Transfer Tool

## What it is

cURL (Client URL) is a command-line tool and library for transferring data with URLs. It supports dozens of protocols including HTTP, HTTPS, FTP, SFTP, SCP, LDAP and many more.

## Installation

```bash
# Ubuntu/Debian
sudo apt-get install curl

# macOS (pre-installed, or via Homebrew)
brew install curl

# Windows (via Chocolatey)
choco install curl
```

## Basic usage

### GET request

```bash
curl https://api.github.com/users/octocat
```

### POST with JSON

```bash
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com"}'
```

### Save response to file

```bash
curl -o output.json https://api.example.com/data
```

### Follow redirects

```bash
curl -L https://bit.ly/example
```

### Custom headers

```bash
curl -H "Authorization: Bearer token123" https://api.example.com/protected
```

## Key flags

| Flag | Description |
|------|-------------|
| `-X` | HTTP method (GET, POST, PUT, DELETE) |
| `-H` | Custom header |
| `-d` | Request body data |
| `-o` | Write output to file |
| `-L` | Follow redirects |
| `-v` | Verbose mode |
| `-s` | Silent mode (no progress) |
| `-k` | Allow insecure SSL |
| `-u` | Basic auth (user:password) |

## Best practices

- Use `-sS` in scripts to suppress progress but keep errors visible
- Use `--retry 3` for automatic retries on network failures
- Never pass tokens in URLs; use the `Authorization` header instead
