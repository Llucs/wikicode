---
title: Demonstrating Proof of Possession (DPoP) — RFC 9449 による送信者制約型 OAuth トークン
description: OAuth 2.0 のアクセストークンとリフレッシュトークンをクライアントが保持する鍵ペアに結び付け、トークンのリプレイや盗用を防ぐ RFC 9449 の仕組み DPoP の開発者向けガイドです。
created: 2026-08-07
tags:
  - oauth2
  - security
  - rfc-9449
  - dpop
  - identity
status: draft
---

# Demonstrating Proof of Possession (DPoP)

## DPoP とは

**Demonstrating Proof of Possession（DPoP）** は、**RFC 9449** で定義されたアプリケーション層の OAuth 2.0 拡張です。アクセストークンとリフレッシュトークンを、クライアントが生成して保持する公開/秘密鍵ペアに結び付けることで、*送信者制約型*にします。

素の `Authorization: Bearer <token>` を送信する代わりに、DPoP 対応クライアントは、トークン発行時に使用された秘密鍵をまだ保持していることをリソースサーバーに証明します。すべてのリクエストは、`DPoP` HTTP ヘッダーに短時間有効な署名付きプルーフ JWT を保持します。そのプルーフは、使用中の正確な HTTP メソッド、URL、アクセストークンに暗号学的に結び付けられています。

アクセストークンはもはや「ベアラー」ではないため、それを持っている人なら誰でも使えるということはなく、盗まれたトークンは対応する秘密鍵がなければ無価値です。

## なぜ重要か

通常の OAuth 2.0 ベアラートークンには根本的な問題があります。トークンの保持自体が唯一の認可証明であることです。サーバーログ、リファラーヘッダー、ブラウザ拡張機能で漏洩したトークン、またはモバイルアプリの侵害後に傍受されたトークンは、攻撃者によってリプレイされる可能性があります。

DPoP は脅威モデルを変えることでこの問題に対処します:

- 盗まれたアクセストークンは、攻撃者がクライアントの秘密鍵も盗まない限りリプレイできません。
- アクセストークンは認可サーバーで特定の鍵にバインドされます。
- リソースサーバーはすべての API 呼び出しで暗号学的プルーフを検証します。
- リフレッシュトークンも送信者制約型にでき、「リフレッシュトークン盗難」のギャップを埋めます。

DPoP は、Open Banking / FAPI 準拠 API、eHealth プラットフォーム、エンタープライズ ID システムなどの高セキュリティ環境で、しばしば必須または推奨されます。

## DPoP の仕組み

### 1. クライアントが鍵ペアを生成する

クライアントは、非対称鍵ペア（通常は EC P-256（ES256））を生成します。秘密鍵はクライアントが保持します。公開鍵は JSON Web Key（JWK）として表現され、すべての DPoP プルーフのヘッダー内に含まれます。

認可サーバーは、トークンの `cnf` クレームに **JWK SHA-256 サムプリント**（`jkt`）を格納することで、アクセストークンをこの公開鍵にバインドします:

```text
jkt = base64url(SHA-256("<canonical JSON of public JWK>"))
```

### 2. クライアントが DPoP プルーフ JWT を構築する

DPoP プルーフは、次の JOSE ヘッダーパラメータを持つ JWT です:

| Header | 値 |
|---|---|
| `typ` | `dpop+jwt` |
| `alg` | 署名アルゴリズム（例: `ES256`） |
| `jwk` | クライアントの公開鍵 |

および、次のクレーム:

| Claim | 意味 |
|---|---|
| `iat` | プルーフ作成時刻 |
| `jti` | プルーフの一意な識別子（リプレイ防止） |
| `htm` | リクエストの HTTP メソッド（例: `GET`） |
| `htu` | 対象 HTTP URI（クエリ文字列を含む） |
| `ath` | Base64url(SHA-256(access_token)) — リソースサーバーを呼び出すときのみ指定 |
| `nonce` | サーバー発行の nonce（任意） |

### 3. トークン要求と API 要求

DPoP が使用される状況は 2 つあります:

**トークン要求** — クライアントは、認可サーバーのトークンエンドポイントへのリクエストで、`DPoP` ヘッダーに DPoP プルーフを送信します。

```http
POST /token HTTP/1.1
Host: auth.example.com
Content-Type: application/x-www-form-urlencoded
DPoP: <dpop-proof-jwt>

grant_type=authorization_code
&code=...
```

認可サーバーはプルーフを検証し、発行したトークンをプルーフの JWK サムプリントにバインドし、トークン応答で `token_type: "DPoP"` を返します。

**リソース要求** — クライアントは `DPoP` 認可スキームでトークンを使用し、`ath` を含む*新しい* DPoP プルーフを添付します。

```http
GET /reports HTTP/1.1
Host: api.example.com
Authorization: DPoP <access-token>
DPoP: <dpop-proof-jwt-with-ath>
```

### 4. リクエストフロー図

```text
Client                          Authorization Server                  Resource Server
  |                                     |                                     |
  | POST /token                         |                                     |
  | DPoP: proof(htm=POST, htu=/token)   |                                     |
  |------------------------------------>|                                     |
  |                                     | verify proof signature              |
  |                                     | bind token -> cnf.jkt = JKT(JWK)    |
  | access_token, token_type=DPoP       |                                     |
  |<------------------------------------|                                     |
  |                                     |                                     |
  | GET /reports                        |                                     |
  | Authorization: DPoP <token>         |                                     |
  | DPoP: proof(htm=GET, htu=/reports,  |                                     |
  |             ath=SHA256(token))      |                                     |
  |---------------------------------------------------------------------->    |
  |                                     |                                     | verify:
  |                                     |                                     |  - proof signature
  |                                     |                                     |  - JWK thumbprint == token cnf.jkt
  |                                     |                                     |  - htm/htu match actual request
  |                                     |                                     |  - jti not seen before
  |                                     |                                     |  - iat is fresh
  |                                 200 OK                                     |
  |<----------------------------------------------------------------------    |
```

### 5. サーバー側の検証チェックリスト

準拠したリソースサーバーは次のことを行う必要があります:

1. `Authorization` スキームが `Bearer` ではなく `DPoP` であることを確認する。
2. `DPoP` プルーフ JWT を解析する。
3. `jwk` ヘッダー内の公開鍵を使用してプルーフの署名を検証する。
4. サポートされていないアルゴリズム（例: `none`）を拒否する。
5. プルーフの `jwk` の JWK サムプリントがトークンの `cnf.jkt` と一致することを確認する。
6. `htm` が実際の HTTP メソッドであることを検証する。
7. `htu` が実際の完全なリクエスト URL（スキーム、ホスト、該当する場合はポート、パス、クエリ）であることを検証する。
8. アクセストークンが提示されている場合は、`ath` がその正確なトークン文字列の SHA-256 ハッシュと等しいことを検証する。
9. `iat` が許容される新しい範囲内（通常 60〜300 秒）であることを検証する。
10. 使用済み `jti` 値の短命なキャッシュを保持し、重複を拒否する。
11. nonce を必須とする設定の場合は、プルーフに現在のサーバー発行 nonce が含まれていることを検証する。

### 6. Nonce チャレンジ

多くの認可サーバーとリソースサーバーは、プルーフにサーバー生成の `nonce` を含めることを要求します。これにより、盗まれたプルーフが長期間リプレイされるのを防ぎます。

クライアントが期待される nonce を省略した場合、サーバーはエラーと `DPoP-Nonce` ヘッダーで応答します:

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json
DPoP-Nonce: R5H6rE8sW

{
  "error": "use_dpop_nonce"
}
```

クライアントは**新しい**プルーフを作成し、nonce を含めて再試行する必要があります。古いプルーフを再利用してはなりません。

## 実際の例 — Python クライアント

次の例では、`cryptography`、`PyJWT`、`requests` を使用してプロトコルを低レベルで示します。本番環境では、自作の暗号処理ではなく、メンテナンスされた OAuth/DCoP ライブラリを優先してください。

前提条件:

```bash
pip install cryptography pyjwt requests
```

```python
import base64
import hashlib
import time
import uuid
from typing import Optional

import jwt
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec


def b64url(data: bytes) -> str:
    """Base64url encode without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def public_jwk(private_key: ec.EllipticCurvePrivateKey) -> dict:
    """Convert an EC P-256 public key to a JWK dictionary."""
    numbers = private_key.public_key().public_numbers()
    return {
        "kty": "EC",
        "crv": "P-256",
        "x": b64url(numbers.x.to_bytes(32, "big")),
        "y": b64url(numbers.y.to_bytes(32, "big")),
    }


def dpop_proof(
    private_key: ec.EllipticCurvePrivateKey,
    method: str,
    uri: str,
    access_token: Optional[str] = None,
    nonce: Optional[str] = None,
) -> str:
    """Create a DPoP proof JWT for the given HTTP request."""
    header = {
        "typ": "dpop+jwt",
        "alg": "ES256",
        "jwk": public_jwk(private_key),
    }

    payload = {
        "iat": int(time.time()),
        "jti": uuid.uuid4().hex,
        "htm": method.upper(),
        "htu": uri,
    }

    if access_token is not None:
        token_hash = hashlib.sha256(access_token.encode("utf-8")).digest()
        payload["ath"] = b64url(token_hash)

    if nonce is not None:
        payload["nonce"] = nonce

    return jwt.encode(payload, private_key, algorithm="ES256", headers=header)


def fetch_access_token(
    token_url: str,
    client_id: str,
    client_secret: Optional[str],
    private_key: ec.EllipticCurvePrivateKey,
) -> str:
    """Exchange credentials for an access token using DPoP."""
    data = {"grant_type": "client_credentials"}
    auth = None

    if client_secret:
        auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    else:
        data["client_id"] = client_id

    proof = dpop_proof(private_key, "POST", token_url)
    headers = {"DPoP": proof}

    resp = requests.post(token_url, data=data, headers=headers, auth=auth)

    if resp.status_code == 400 and resp.json().get("error") == "use_dpop_nonce":
        nonce = resp.headers.get("DPoP-Nonce")
        proof = dpop_proof(private_key, "POST", token_url, nonce=nonce)
        resp = requests.post(
            token_url,
            data=data,
            headers={"DPoP": proof},
            auth=auth,
        )

    resp.raise_for_status()
    return resp.json()["access_token"]


def fetch_resource(
    resource_url: str,
    access_token: str,
    private_key: ec.EllipticCurvePrivateKey,
) -> requests.Response:
    """Call a resource server with a DPoP-bound access token."""
    proof = dpop_proof(
        private_key,
        "GET",
        resource_url,
        access_token=access_token,
    )
    headers = {
        "Authorization": f"DPoP {access_token}",
        "DPoP": proof,
    }

    resp = requests.get(resource_url, headers=headers)

    if resp.status_code == 401 and "DPoP-Nonce" in resp.headers:
        nonce = resp.headers["DPoP-Nonce"]
        proof = dpop_proof(
            private_key,
            "GET",
            resource_url,
            access_token=access_token,
            nonce=nonce,
        )
        headers = {
            "Authorization": f"DPoP {access_token}",
            "DPoP": proof,
        }
        resp = requests.get(resource_url, headers=headers)

    return resp
```

使用例:

```python
client_private_key = ec.generate_private_key(ec.SECP256R1())

token = fetch_access_token(
    token_url="https://auth.example.com/token",
    client_id="my-public-client",
    client_secret=None,  # public client
    private_key=client_private_key,
)

response = fetch_resource(
    resource_url="https://api.example.com/reports",
    access_token=token,
    private_key=client_private_key,
)

print(response.status_code)
```

この例の重要な点:

- プルーフごとに新しい `jti` が生成されます。
- トークン要求のプルーフには `ath` が含まれません。
- リソース要求のプルーフは、正確なアクセストークン文字列をハッシュ化します。
- クライアントはセッションの間、秘密鍵を保持します。

## サーバー側の検証スケッチ

上記のプルーフを検証するリソースサーバーは、`jwk` ヘッダーから公開鍵を再構築し、JWT を検証する必要があります:

```python
def verify_dpop_proof(
    proof: str,
    method: str,
    uri: str,
    access_token: Optional[str] = None,
) -> dict:
    header = jwt.get_unverified_header(proof)

    if header.get("typ") != "dpop+jwt":
        raise ValueError("Invalid DPoP typ header")

    jwk = header.get("jwk")
    if jwk is None or jwk.get("kty") != "EC" or jwk.get("crv") != "P-256":
        raise ValueError("Unsupported DPoP key")

    x = int.from_bytes(base64.urlsafe_b64decode(jwk["x"] + "=="), "big")
    y = int.from_bytes(base64.urlsafe_b64decode(jwk["y"] + "=="), "big")

    public_key = ec.EllipticCurvePublicNumbers(x, y, ec.SECP256R1()).public_key()
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    claims = jwt.decode(proof, pem, algorithms=["ES256"])

    if claims["htm"] != method.upper():
        raise ValueError("DPoP proof method mismatch")
    if claims["htu"] != uri:
        raise ValueError("DPoP proof URI mismatch")
    if access_token is not None:
        expected_ath = b64url(hashlib.sha256(access_token.encode()).digest())
        if claims.get("ath") != expected_ath:
            raise ValueError("DPoP proof ath mismatch")

    # Additional checks in real code:
    # - Reject duplicate / stale jti
    # - Check iat freshness
    # - Validate nonce against server-issued nonce cache
    # - Verify the proof's JWK thumbprint matches the token's cnf.jkt

    return claims
```

最後の項目、つまりプルーフの JWK をトークンにバインドされた `cnf` と照合することは、DPoP の核心です。不透明なアクセストークンの場合、リソースサーバーはトークンイントロスペクションを通じて `cnf` を取得する必要があります。JWT アクセストークンの場合、`cnf` は通常トークンのクレームに直接含まれます。

## トレードオフと代替手段

### DPoP とベアラートークンの比較

| 観点 | ベアラートークン | DPoP |
|---|---|---|
| バインド | なし | クライアントが保持する公開鍵 |
| 盗まれたトークンのリプレイ | 容易 | 秘密鍵なしでは現実的でない |
| クライアントの複雑さ | 非常に低い | 中: 鍵生成、署名、nonce 処理 |
| サーバーの負荷 | 最小限 | リクエストごとの署名検証 |
| 標準 | RFC 6750 | RFC 9449 |

ベアラートークンは、低リスクの内部 API に適しています。DPoP は、トークンが漏洩した場合の影響が大きい場合に正当化されます。

### DPoP と相互 TLS (mTLS) の比較

| 観点 | mTLS (RFC 8705) | DPoP |
|---|---|---|
| バインド層 | トランスポート層 | アプリケーション層 |
| クライアント証明書の管理 | 大変（PKI、プロビジョニング） | 鍵ペアで導入が容易 |
| ブラウザ / SPA での動作 | 難しい | WebCrypto で動作 |
| モバイルアプリでの動作 | 困難 | 可能 |
| FAPI 準拠 | よく使われる | 使用が増えている |

DPoP は、mTLS 証明書インフラよりも、Web およびモバイルのパブリッククライアントへの導入が一般的に容易です。mTLS は、証明書管理がすでに一般的であるサーバー間統合において、引き続き有力な選択肢です。

### DPoP の制限

- **秘密鍵の盗難は致命的です。** DPoP はトークンの盗難を防ぎますが、鍵の盗難は防ぎません。秘密鍵が漏洩すると、攻撃者は正規クライアントと同じ能力を持ちます。
- **リクエストごとの署名コスト。** すべての API リクエストで署名が必要になり、すべてのリソースサーバーリクエストで検証が必要になります。
- **Nonce のラウンドトリップ。** サーバーが nonce を必須とする場合、nonce ローテーション後の最初のリクエストで追加のラウンドトリップが 1 回発生します。
- **鍵管理の負担。** クライアントは鍵を安全に作成、保存、ローテーションする必要があります。鍵を失うと再認証が必要になります。
- **エンドツーエンドのサポートが必要。** 認可サーバーとすべてのリソースサーバーの両方が DPoP を理解し、`cnf` のバインドを尊重する必要があります。
- **PKCE の代替ではありません。** DPoP は認可コードの傍受を防ぎません。パブリッククライアントには PKCE を使用してください。

## ベストプラクティス

1. **DPoP は PKCE と併用してください。** これらは異なる脅威に対処します。PKCE は認可コード交換を保護し、DPoP はその結果得られるトークンを保護します。
2. **P-256 / ES256 を使用してください。** 広くサポートされており、高速で安全です。すべての関係者がサポートしている場合を除き、特殊なアルゴリズムは避けてください。
3. **ユーザーセッションごとに新しい鍵ペアを生成してください。** アプリケーションのすべてのユーザー間で秘密鍵を共有しないでください。
4. **秘密鍵を安全に保管してください。** OS キーチェーン、Android Keystore、iOS Secure Enclave、TPM、またはエクスポート不可能な WebCrypto キーを使用してください。
5. **リフレッシュトークンもバインドしてください。** リフレッシュトークンから新しいアクセストークンを要求する際に DPoP プルーフを送信してください。認可サーバーが送信者制約型リフレッシュトークンをサポートしている場合は、それを利用してください。
6. **フェイルクローズにしてください。** DPoP リクエスト後にサーバーが `token_type: "Bearer"` を返した場合は、透過的にフォールバックするのではなく、設定ミスとして扱ってください。
7. **DPoP プルーフをログに記録しないでください。** 有効なプルーフは時間制限付きですが、サーバーの `jti` キャッシュが短く、攻撃者がすぐに取得した場合にはリプレイされる可能性があります。
8. **監査済みライブラリを使用してください**。生のプロトコルを実装するのではなく、本番環境では監査済みライブラリを使用してください。多くの OAuth SDK が DPoP サポートを提供しています:
   - **Python** — Authlib
   - **JavaScript** — oauth4webapi
   - **Java** — Nimbus OAuth 2.0 SDK / JOSE+JWT
   - **.NET** — IdentityModel
9. **常に HTTPS を使用してください。** DPoP は TLS の代替ではなく、リクエストがクライアントを離れた後のベアラートークン不正使用に対する追加の防御策です。

## 参考資料

- [RFC 9449 — OAuth 2.0 Demonstrating Proof of Possession (DPoP)](https://www.rfc-editor.org/rfc/rfc9449)
- [RFC 6749 — The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749)
- [RFC 7638 — JSON Web Key (JWK) Thumbprint](https://www.rfc-editor.org/rfc/rfc7638)
- [RFC 8705 — OAuth 2.0 Mutual TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705)
- [RFC 7636 — Proof Key for Code Exchange (PKCE)](https://www.rfc-editor.org/rfc/rfc7636)

## まとめ

DPoP は、OAuth トークンをベアラー資格情報から送信者制約型の資格情報へと変えます。クライアントはリクエストごとに秘密鍵の所持を証明し、リソースサーバーは、発行時にトークンにバインドされた鍵に対してそのプルーフを検証します。これは、特にパブリッククライアント、モバイルアプリ、シングルページアプリケーションにおいて、トークン盗難による被害を大幅に軽減する実用的なアプリケーション層の仕組みです。

DPoP の導入には、鍵の管理、nonce、リプレイキャッシュ、リクエストごとの検証といった現実的な複雑さが伴います。しかし、機密データを扱う API にとっては、そのコストに見合うセキュリティ向上が得られることが多いです。