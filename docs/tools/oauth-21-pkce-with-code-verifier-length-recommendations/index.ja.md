---
title: OAuth 2.1 PKCE とコード検証子の長さ推奨事項
description: OAuth 2.1 PKCE の実装ガイドと、セキュリティ向上のためにコード検証子の長さ推奨事項についての説明
created: 2026-07-12
tags:
  - OAuth
  - PKCE
  - Security
status: draft
---

# OAuth 2.1 PKCE とコード検証子の長さ推奨事項

## PKCE とは？

PKCE（Code Exchange 用の証明キー）は、OAuth 2.0 で攻撃者が認証コードを取得できないようにするセキュリティメカニズムです。クライアントと認証サーバー間で一回限りかつ非再使用の秘密（コード検証子）を交換することによって、追加のセキュリティ層を追加します。

## OAuth 2.1 PKCE の主要機能

- **コード検証子**: クライアントと認証サーバー間の秘密として使用されるランダムな文字列。
- **コード挑戦**: ネットワーク嗅探防止のためにコード検証子のハッシュ。
- **ノンス**: 認証リクエストに含まれる一意の値で、コードが一度しか使用されないようにします。

## PKCE の歴史

PKCE は OAuth 2.0 でオプションのメカニズムとして導入され、セキュリティを向上するために使用されました。しかし、OAuth 2.1 標準では必須の部分となり、特にパブリッククライアントでより高いレベルのセキュリティを確保するためです。

## PKCE の使用例

- **パブリッククライアント**: セCRET を安全に保存できないクライアント、例えばウェブアプリケーションやモバイルアプリケーション。
- **ハイブリッドフロー**: アクセストークンの交換が必要な場面に適しています。
- **認証コードフロー**: 認証サーバーへのリダイレクトが必要なシナリオでセキュリティを向上させます。

## コード検証子の長さ推奨事項

コード検証子の長さは PKCE のセキュリティにとって重要な要素です。コード検証子は、強力なブリーチフォース攻撃から保護されるよう十分な長さを持つべきですが、クライアント実装で扱いやすい長さであることも必要です。

### 推奨長さ

- **最小長さ**: 43 文字
- **推奨長さ**: 128 文字以上

コード検証子が長いほど、ブリーチフォース攻撃に対してより強力な防御が可能です。OAuth 2.1 標準では、43 文字以上の最小長さを推奨しており、これにより相当のセキュリティが確保できます。ただし、128 文字以上の長いコード検証子を使用することで、大幅なセキュリティ余裕も確保できます。

## インストールと基本的な使用法

### 手順 1: コード検証子を生成する

```python
import random
import string

def generate_code_verifier(length=128):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
```

### 手順 2: コード挑戦を生成する

```python
import hashlib
import base64

def generate_code_challenge(code_verifier):
    code_challenge = hashlib.sha256(code_verifier.encode()).digest()
    return base64.urlsafe_b64encode(code_challenge).rstrip(b'=').decode()
```

### 手順 3: OAuth 2.0 フローに PKCE を含める

1. **認証リクエスト**:
   - 認証リクエストに `code_challenge` と `code_challenge_method` を含めます。
   - 例:
     ```http
     GET /authorize?response_type=code&client_id=your_client_id&redirect_uri=https%3A%2F%2Fyourapp.com%2Fcallback&code_challenge=your_code_challenge&code_challenge_method=S256&state=some_state_value&nonce=some_nonce_value
     ```

2. **トークンリクエスト**:
   - トークンリクエストに `code_verifier` を含めます。
   - 例:
     ```http
     POST /token HTTP/1.1
     Host: your_authorization_server.com
     Content-Type: application/x-www-form-urlencoded

     grant_type=authorization_code&code=your_authorization_code&redirect_uri=https%3A%2F%2Fyourapp.com%2Fcallback&code_verifier=your_code_verifier
     ```

## 結論

PKCE と十分な長さのコード検証子（少なくとも 128 文字）を使用することは、特にパブリッククライアントシナリオで OAuth 2.0 フローのセキュリティを向上するために重要です。推奨の実践に従うことで、開発者はアプリケーションのより高いレベルのセキュリティを確保できます。