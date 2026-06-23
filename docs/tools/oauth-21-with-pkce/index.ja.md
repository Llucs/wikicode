---
title: OAuth 2.1とPKCE: 実装ガイド
description: OAuth 2.1とProof Key for Code Exchangeを組み合わせた安全な認証方式で、認可コードインターセプト攻撃から保護します。
created: 2026-06-23
tags:
  - oauth2.1
  - pkce
  - authentication
  - security
  - authorization-code-flow
status: draft
---

# OAuth 2.1とPKCE: 実装ガイド

## 概要

OAuth 2.1は、OAuth 2.0フレームワーク（RFC 6749）とその多数の修正をセキュリティに焦点を当てて統合したものです。以前は推奨されていたプラクティスを**必須**とすることで、コア仕様を簡素化しながらセキュリティを強化します。**Proof Key for Code Exchange（PKCE）**は、もともとモバイルアプリやネイティブアプリ向けにRFC 7636で定義されていましたが、現在はOAuth 2.1において**すべての**クライアントのAuthorization Codeフローに必須のコンポーネントとなっています。

このガイドでは、最新のアプリケーションでOAuth 2.1とPKCEを採用するための根拠、実装手順、主要機能、移行戦略について説明します。

---

## 歴史と進化

| 年 | イベント | 影響 |
|------|-------|--------|
| 2012 | OAuth 2.0（RFC 6749） | 複数のgrant type（Implicit GrantやPassword Grantなど）を導入したが、後に安全ではないことが判明。 |
| 2015 | PKCE（RFC 7636） | 主にpublic clients向けに、認可コードインターセプト攻撃を防ぐために作成された。 |
| 2020 | OAuth Security BCP（RFC 9700） | Implicit GrantとPassword Grantを公式に非推奨にし、Authorization Code flowを使用するすべてのpublic clientsにPKCEを必須化。 |
| 2023+ | OAuth 2.1 | BCPの推奨事項を単一のコア仕様に統合し、**すべての**クライアントにPKCEを必須とし、安全でないgrantを完全に削除。 |

---

## OAuth 2.1 + PKCEが重要な理由

OAuth 2.1は、設定ではなく設計によって攻撃のカテゴリ全体を排除します。

- **Authorization Code Interception** – PKCEにより、認可コードを交換するパーティーが、そのコードを要求したパーティーと同じであることを保証します（コードがインターセプトされた場合でも）。
- **Mix-Up Attacks** – 厳格なリダイレクトURIの一致により、攻撃者が自身のリダイレクトを挿入することを防ぎます。
- **CSRF on the Code** – `code_verifier`は推測不可能な安全なnonceとして機能します。
- **Removal of Insecure Flows** – Implicit GrantとResource Owner Password Grantが削除され、一般的な攻撃経路が閉じられます。

**本番環境**（例：Azure Container Apps上のMCPサーバー）では、現在OAuth 2.1 + PKCEが標準の認証方法として必要です。

---

## OAuth 2.1の主な特徴

### 1. PKCEの必須化

Authorization Codeフローには、`code_challenge`と`code_verifier`を**含める必要があります**。`client_secret`を持つ機密クライアントでさえ、多層防御の恩恵を受けます。

### 2. Implicit GrantとPassword Grantの削除

Authorization Code、Client Credentials、およびRefresh Tokenグラントのみが残ります。他のすべてのグラントは非推奨です。

### 3. 厳格なリダイレクトURIの検証

リダイレクトURIは、完全な文字列一致で比較する必要があります。ワイルドカードやパターンマッチングは許可されません。

### 4. リフレッシュトークンのローテーション

リフレッシュトークンは単回使用とすべきです。リフレッシュトークンが再利用された場合、自動的に失効され、侵害のシグナルとなります。

### 5. Sender-Constrained Access Tokens

トークンは、mTLS（Mutual TLS）またはDPoP（Proof-of-Possessionの実証）を介してクライアントにバインドする必要があります。可能な場合は単純なbearerトークンを置き換えます。

---

## 実装フロー（ステップバイステップ）

### 1. クライアントの準備: PKCEパラメータの生成

クライアントは、暗号学的にランダムな`code_verifier`を生成し、そのSHA-256ハッシュを`code_challenge`として計算する必要があります。

**Node.jsを使用した例（Node 15以上が必要）**

```javascript
import crypto from 'crypto';

// Generate a secure random code_verifier (43-128 characters)
const codeVerifier = crypto.randomBytes(32)
  .toString('base64url')
  .slice(0, 128);

// Compute S256 code_challenge
const codeChallenge = crypto
  .createHash('sha256')
  .update(codeVerifier)
  .digest('base64url');

console.log({ codeVerifier, codeChallenge });
```

**出力（マスク済み）:**
```json
{
  "codeVerifier": "fdb8...d2a9",
  "codeChallenge": "EbZ6...7Qxw"
}
```

### 2. 認可リクエスト

ユーザーを認可サーバーの`/authorize`エンドポイントに以下のパラメータとともにリダイレクトします。

```
GET /authorize?
  response_type=code
  &client_id=YOUR_CLIENT_ID
  &redirect_uri=https://yourapp.com/callback
  &scope=openid%20profile%20email
  &code_challenge=EbZ6...7Qxw
  &code_challenge_method=S256
  &state=OPAQUE_STATE_VALUE
```

- `code_challenge_method`は**`S256`でなければなりません**。`plain`メソッドは許可されていません。

### 3. 認可コードの受信

ユーザー認証と同意の後、認可サーバーは`?code=AUTHORIZATION_CODE`を含めて`redirect_uri`にリダイレクトします。

```
GET /callback?code=AUTHORIZATION_CODE&state=OPAQUE_STATE_VALUE
```

`state`パラメータを検証してCSRF攻撃を防ぎます。

### 4. トークンリクエスト（バックチャネル）

クライアントは、`code_verifier`を含めて`/token`エンドポイントにPOSTリクエストを送信します。

**`oauth4webapi`を使用した例（OAuth 2.1推奨）**

```javascript
import * as oauth from 'oauth4webapi';

const issuer = new URL('https://authorization-server.com');
const clientId = 'YOUR_CLIENT_ID';
const clientSecret = undefined; // public client

const as = await oauth.discoveryRequest(issuer);
const { authorization_server } = oauth.processDiscoveryResponse(as, {});

const client = {
  client_id: clientId,
  token_endpoint_auth_method: 'none',
};

const authCode = 'AUTHORIZATION_CODE';
const codeVerifier = 'fdb8...d2a9'; // from step 1

const response = await oauth.authorizationCodeGrantRequest(
  authorization_server,
  client,
  authCode,
  issuer + '/redirect_uri',
  codeVerifier,
);

const tokens = await oauth.processAuthorizationCodeResponse(
  authorization_server,
  client,
  response,
  { expectedNonce: 'NONCE_FROM_ID_TOKEN' },
);
```

**Curl表現:**

```bash
curl -X POST https://authorization-server.com/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=AUTHORIZATION_CODE" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "redirect_uri=https://yourapp.com/callback" \
  -d "code_verifier=fdb8...d2a9"
```

### 5. サーバー側の検証

トークンエンドポイントは以下を実行します。

```
HASH(code_verifier) == code_challenge
```

ハッシュが一致すればコードは有効です。一致しない場合、リクエストは失敗します。

### 6. トークンレスポンス

成功したレスポンスには、`access_token`、`refresh_token`（`offline_access`が要求された場合）、およびオプションで`id_token`が含まれます。

```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "DPoP",
  "expires_in": 3600,
  "refresh_token": "dGhpcyBp...",
  "scope": "openid profile email"
}
```

---

## ライブラリサポート

### サーバーサイド（認可サーバー）

| ライブラリ / プラットフォーム | OAuth 2.1のサポート |
|-------------------|-------------------|
| Keycloak          | はい（デフォルトでPKCE必須） |
| Entra ID (Azure AD) | はい（Authorization Code + PKCE） |
| Auth0             | はい（設定が必要） |
| Okta              | はい |
| Curity            | はい |
| Spring Security 6+ | はい（`oauth2Client` with PKCE） |

### クライアントサイド（アプリケーション）

| 言語 | ライブラリ | 備考 |
|----------|---------|-------|
| Node.js  | [`oauth4webapi`](https://github.com/panva/oauth4webapi) | 作者独自、OAuth 2.1対応 |
| Python   | [`Authlib`](https://authlib.org/) | PKCEおよびOAuth 2.1パターンをサポート |
| Java     | Spring Security 6+ | PKCE対応の組み込み`NimbusJwtDecoder` |
| Mobile   | AppAuth (Android/iOS) | ネイティブPKCEサポート |
| Web SPA  | BFFパターンまたはWeb Workers | ブラウザで直接PKCEは不可、Backend-for-Frontendを使用 |

---

## OAuth 2.0からの移行

### チェックリスト

1. **Implicit Grantを** Authorization Code + PKCEに置き換える。
2. **Password Grantを** Authorization Code + PKCEまたはClient Credentials（マシン間通信用）に置き換える。
3. すべてのAuthorization Code交換に**PKCEを強制する**。
4. **Refresh Tokenのローテーションを有効にする**（単回使用トークン）。
5. **リダイレクトURIの比較を**完全一致に更新する。
6. 以前に`plain`を使用していた場合は、チャレンジメソッドを**S256に切り替える**。

### 例: 従来のAuthorization Codeフローの移行

**Before (OAuth 2.0 – optional PKCE)**

```
step 1: client_id + redirect_uri → get code
step 2: code + client_secret → get token
```

**After (OAuth 2.1 – mandatory PKCE)**

```
step 1: client_id + redirect_uri + code_challenge (S256) → get code
step 2: code + code_verifier → get token
```

---

## 実例: Azure Container Apps上のMCPサーバー

Model Context Protocol（MCP）仕様（2026年3月15日時点）では、エージェントサーバーと対話する際の認可にOAuth 2.1 + PKCEを要求しています。以下は簡潔なセットアップです。

1. **PRM（Protected Resource Metadata）を定義** – `.well-known/oauth-authorization-server`を公開
2. クライアント向けに**動的クライアント登録（RFC 7591）を実装**
3. **スコープ設計** – リソースごとに詳細なスコープを定義（例：`files:read`、`compute:execute`）
4. **トークン検証** – すべてのAPIリクエストでアクセストークンの署名とバインドされたキーを検証する必要があります

Azure CLI設定例（概念）:

```bash
az containerapp create \
  --name mcp-server \
  --environment MyEnv \
  --image myregistry.azurecr.io/mcp:v1 \
  --secrets oauth-jwks-secret="$(cat jwks.json)" \
  --env-vars OAUTH_AUTHORIZATION_URL="https://login.contoso.com/authorize" \
             OAUTH_TOKEN_URL="https://login.contoso.com/token" \
             OAUTH_CLIENT_ID="mcp-server" \
  --ingress 'external'
```

クライアント（例：VSCode Azure MCP拡張機能）は、MCPツールを呼び出す前にPKCEフローを実行します。

---

## セキュリティのベストプラクティス

- **stateパラメータを使用する** – 認可リクエストをユーザーセッションにバインドします。
- **code_verifierを安全に保存する** – バックエンドセッションまたは安全なクライアントサイドストア（URLには保存しない）。
- **すべてのトークンを検証する** – 署名、発行者、対象者、有効期限を確認します。
- **リフレッシュトークンをローテーションする** – リフレッシュごとに新しいトークンを発行し、前のトークンを無効化します。
- **DPoPを実装する** – アクセストークンに`cnf`クレームを追加して、sender-constrainedをサポートします。
- **トークンの再利用をログに記録する** – 潜在的なトークンの盗難を検出します。

---

## よくある問題のトラブルシューティング

| 問題 | 考えられる原因 | 解決策 |
|---------|--------------|--------|
| トークン交換中に`invalid_grant` | `code_verifier`が`code_challenge`と一致しない | 作成時とまったく同じ方法でベリファイアを再ハッシュ（同じアルゴリズム、同じ文字エンコーディング） |
| `redirect_uri_mismatch` | URLの比較が完全一致でない | `redirect_uri`が末尾のスラッシュも含めて完全に一致することを確認 |
| 認可コードの期限切れ | タイムアウト超過（10分以上） | フロー全体を再試行 |
| ローテーション後のリフレッシュトークン拒否 | トークンリプレイが検出 | クライアントは古いリフレッシュトークンを破棄し、単回使用のローテーションを正しく実装する |

---

## 参考文献

- [OAuth 2.1 Draft Specification](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)
- [PKCE RFC 7636](https://datatracker.ietf.org/doc/html/rfc7636)
- [OAuth Security BCP (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [oauth4webapi – Official Implementation](https://github.com/panva/oauth4webapi)
- [Authlib – OAuth 2.1 for Python](https://authlib.org/)
- [Spring Security 6 OAuth 2.1 Client](https://docs.spring.io/spring-security/reference/servlet/oauth2/client/index.html)

---

## 結論

OAuth 2.1とPKCEの採用は、単なるコンプライアンス要件ではなく、セキュリティ体制の根本的な改善です。PKCEを必須とし、脆弱なフローを削除し、厳格な検証を実施することで、OAuth 2.1は最新のアプリケーションが最も一般的な認可攻撃に対して耐性を持つことを保証します。新しいMCPサーバーを構築する場合、レガシーモバイルアプリを移行する場合、またはシングルページアプリケーションを強化する場合でも、この仕様は明確で安全な道筋を提供します。