---
title: cURL — データ転送ツール
description: cURLは、ネットワークプロトコルを使用してデータを転送するためのコマンドラインツールです。
created: 2026-06-14
tags:
  - tool
  - cli
  - networking
status: draft
ecosystem: networking
---

# cURL — データ転送ツール

## 概要

cURL（Client URL）は、URLを使ってデータを転送するためのコマンドラインツールおよびライブラリです。HTTP、HTTPS、FTP、SFTP、SCP、LDAPなど、数十のプロトコルをサポートしています。

## インストール

```bash
# Ubuntu/Debian
sudo apt-get install curl

# macOS (pre-installed, or via Homebrew)
brew install curl

# Windows (via Chocolatey)
choco install curl
```

## 基本的な使い方

### GETリクエスト

```bash
curl https://api.github.com/users/octocat
```

### JSONでのPOST

```bash
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com"}'
```

### レスポンスをファイルに保存

```bash
curl -o output.json https://api.example.com/data
```

### リダイレクトを追跡

```bash
curl -L https://bit.ly/example
```

### カスタムヘッダー

```bash
curl -H "Authorization: Bearer token123" https://api.example.com/protected
```

## 主要なフラグ

| フラグ | 説明 |
|--------|------|
| `-X` | HTTPメソッド（GET、POST、PUT、DELETE） |
| `-H` | カスタムヘッダー |
| `-d` | リクエストボディデータ |
| `-o` | 出力をファイルに書き込む |
| `-L` | リダイレクトを追跡する |
| `-v` | 詳細モード |
| `-s` | サイレントモード（進行状況を非表示） |
| `-k` | 不安全なSSLを許可 |
| `-u` | Basic認証（ユーザー:パスワード） |

## ベストプラクティス

- スクリプト内で `-sS` を使用し、進行状況を非表示にしつつエラーを表示する
- ネットワーク障害時に自動リトライするために `--retry 3` を使用する
- トークンをURLに渡さず、代わりに `Authorization` ヘッダーを使用する