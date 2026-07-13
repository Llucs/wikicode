---
title: OAuth 2.1とPKCEの最善の実践
description: OAuth 2.1の実装を保護コード交換（PKCE）を使用してOAuth 2.0認証フレームワークのセキュリティを強化するための詳細なガイドラインを提供します。認証コード注入攻撃を防止するためにPKCEを使用します。
created: 2026-07-13
tags:
  - OAuth
  - PKCE
  - セキュリティ
  - API
status: 草稿
---

# OAuth 2.1とPKCEの最善の実践

OAuth 2.1とProof Key for Code Exchange (PKCE)は、OAuth 2.0認証フレームワークのセキュリティを向上させるプロトコル拡張です。PKCEは、クライアントシークレットを厳重に保持する方法がない（例：モバイルアプリや単一ページアプリケーション）パブリッククライアントにおける認証コードの interceptions のリスクを軽減するために設計されています。

## 主な機能

1. **コード確認/挑戦**: クライアントがPKCE認証コードを作成するために使用されるランダム生成文字列。コード確認はネットワーク上に送信されず、秘密に保持されます。
2. **コード挑戦**: クライアントのコード確認をハッシュ化したものです。この挑戦は認証サーバーに送信されます。
3. **認証コード授与フロー**: フローは大まかに同じですが、PKCEの追加があります。

## 歴史

OAuth 2.1とPKCEは、クライアント認証のセキュリティ懸念を解決するためにOAuth 2.0の拡張として導入されました。RFC 7636で最初に提案され、その後OAuth 2.1仕様に組み込まれました。

## 使用例

- **パブリッククライアント**: モバイルアプリ、シングルページアプリケーションなど、クライアントシークレットを安全に保管できないクライアント。
- **APIセキュリティ**: ウェブおよびモバイルアプリケーションのAPIアクセスと認証のセキュリティを強化します。
- **ウェブアプリケーション**: OAuthを使用して認証を実装するウェブアプリケーションのセキュリティを改善します。

## インストール

OAuth 2.1とPKCEはプロトコル拡張ですが、それを実装するには通常以下の手順が必要です：

1. **クライアントサイドの実装**:
   - コード確認とコード挑戦を生成します。
   - 認証要求にコード挑戦を使用します。
   - 認証応答を処理し、認証コードをアクセストークンに交換します。

2. **サーバサイドの実装**:
   - サーバーはコード挑戦をコード確認と照合し、認証応答を処理し、認証コードをアクセストークンに交換します。

### 基本的な使用法

1. **クライアント認証**:
   - クライアントがコード確認とコード挑戦を生成します。
   - 認証要求にコード挑戦を含めます。

2. **認証応答**:
   - ユーザーがアクセスを許可するか拒否します。
   - 認証サーバーは認証コードを応答します。

3. **トークン要求**:
   - クライアントはコード確認を使用して認証コードをアクセストークンに交換します。

4. **検証**:
   - 認証サーバーはコード挑戦とコード確認を使用してクライアントの正統性を確認します。

## 最善の実践

1. **強力なコード確認の使用**:
   - 暗号化安全擬似乱数生成器（CSPRNG）を使用してコード確認を生成します。
   - 時間攻撃を防ぐためにコード確認は43文字以上長くすることを確認します。

2. **コード挑戦の方法**:
   - `S256`メソッドを使用してコード確認をハッシュ化します。このメソッドは時間攻撃に耐えます。

3. **クライアント認証**:
   - クライアントタイプに応じて適切なクライアント認証方法を使用します（例：`client_secret_basic`は信頼できるクライアント、`none`はパブリッククライアント）。

4. **トランスポートセキュリティ**:
   - すべての通信をHTTPSで保護して、コード挑戦とその他の機密情報の安全を確保します。

5. **セッション管理**:
   - 認証コードが再利用されないよう適切なセッション管理を実装します。

6. **定期的な監査と更新**:
   - 最新のセキュリティ実践と基準を追跡するために定期的に実装をレビューし、更新します。

7. **レートリミting**:
   - セキュリティの脆弱性を防ぐためにレートリミtingを実装します。

8. **ログとモニタリング**:
   - 認証要求と応答をログとモニタリングし、異常活動を速やかに検知し対応します。

これらの最善の実践に従うことで、PKCEを用いたOAuth 2.1の実装の安全性を向上させ、機密情報が保護され、アプリケーションが常に安全に保たれることが可能です。

## 例：Pythonの実装

以下は、`requests`ライブラリを使用してPKCEをPythonで実装する基本的な例です：

```python
import requests
import string
import random
import hashlib

# コード確認の生成
def generate_code_verifier(length=43):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# コード挑戦の生成
def generate_code_challenge(verifier):
    sha256 = hashlib.sha256()
    sha256.update(verifier.encode('utf-8'))
    return sha256.hexdigest()[:43]

# クライアント認証の例
def authenticate_client(authorization_url, client_id, redirect_uri, code_verifier):
    # コード挑戦の生成
    code_challenge = generate_code_challenge(code_verifier)

    # 認証要求
    auth_params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge
    }

    response = requests.get(authorization_url, params=auth_params)
    if response.status_code != 200:
        raise Exception("クライアント認証に失敗しました")

    # ユーザーとの交互を処理し、認証コードを取得

    # タイム要求
    token_params = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri,
        'code_verifier': code_verifier
    }

    token_response = requests.post(token_url, data=token_params, auth=(client_id, 'client_secret'))
    if token_response.status_code != 200:
        raise Exception("アクセストークンを取得できませんでした")

    return token_response.json()

# 使用例
client_id = 'your_client_id'
redirect_uri = 'http://your-redirect-uri'
authorization_url = 'https://your-authorization-server'
code_verifier = generate_code_verifier()
code_challenge = generate_code_challenge(code_verifier)
access_token = authenticate_client(authorization_url, client_id, redirect_uri, code_verifier)
print("アクセストークン:", access_token['access_token'])
```

この例では、コード確認と挑戦を生成し、認証要求を実行し、認証コードをアクセストークンに交換する方法を示しています。

## 結論

OAuth 2.1とPKCEは、OAuth 2.0の実装における重要なセキュリティ強化手段です。このガイドラインに示された最善の実践に従うことで、OAuthをベースとするアプリケーションの安全性を大幅に向上させることができます。