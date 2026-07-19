---
title: OAuth 2.1 における PKCE および Token Binding
description: ウェブおよびモバイルアプリケーションで強化されたセキュリティを実現するための OAuth 2.1 と PKCE および Token Binding の実装ガイドです。
created: 2026-07-19
tags:
  - OAuth
  - PKCE
  - Token Binding
  - Security
  - Authentication
status: draft
---

# OAuth 2.1 における PKCE および Token Binding

OAuth 2.1 は OAuth 2.0 プロトコルの最新バージョンであり、ウェブおよびモバイルアプリケーションにおける認証と認証に広く使用されています。OAuth 2.1 は、PKCE（Proof Key for Code Exchange）と Token Binding の統合を含むいくつかの改善と新しい機能を導入し、セキュリティと使いやすさを向上させます。

## OAuth 2.1 の主要機能

1. **セキュリティの改善**: OAuth 2.1 は、一般的な脆弱性を対策し、新しいセキュリティ措置を実装することで、セキュリティを向上させています。
2. **PKCE（Proof Key for Code Exchange）**: この機能は、公共クライアント（モバイルアプリケーションや単ページアプリケーションなど）がクライアントシークレットを安全に保存できない場合、認証コードの傍受を防ぐために重要です。
3. **Token Binding**: この機能は、トークンが特定のクライアントやデバイスにバインドされることを確保し、トークンの利用を強化します。
4. **動的クライアント登録**: OAuth 2.1 では、認証プロセス中にクライアントが動的に登録できるため、柔軟性と適応性が向上します。
5. **改善された同意メカニズム**: もっと簡単にリソースへのアクセスと認証を管理できる改良された同意フローが提供されています。

## 歴史

- **OAuth 2.0**: OAuth 2.0 の最初のバージョンは 2012 年にリリースされ、その後ウェブ上の認証の標準となりました。
- **OAuth 2.1**: OAuth 2.1 は 2022 年に公式にリリースされ、進化するセキュリティ脅威とユーザーのニーズに対応するための新しいセキュリティ措置や改善が取り入れられています。

## 使用例

1. **ウェブアプリケーション**: セキュアなユーザー認証と認証が必要なウェブアプリケーションに最適です。
2. **モバイルアプリケーション**: 公共クライアントと機密クライアント双方をサポートするため、モバイルアプリケーションに適しています。
3. **API統合**: OAuth 2.1 は、異なるシステム間でAPIを安全かつ効率的に統合するのに役立ちます。
4. **IoT デバイス**: Token Binding フィーチャーは、IoT デバイス上のトークンのセキュリティに特に有用です。

## インストール

OAuth 2.1 は OAuth 2.0 プロトコルの一部として統合されることが多いので、別個のインストールは必要ありません。ただし、アプリケーションに OAuth 2.1 フEATURES である PKCE と Token Binding の対応を追加する必要があります。

1. **OAuth プロバイダーとの登録**: 自身の選択した OAuth プロバイダーからクレデンシャル（クライアント ID とクライアントシークレット）を取得します。
2. **アプリケーションの構成**: OAuth 2.1 の対応を含むアプリケーションを構成します。
3. **PKCE の実装**: 公共クライアントでは、コード挑戦とコード検証の生成と確認を実装します。
4. **Token Binding の実装**: デバイスまたはクライアントにトークンをバインドして、その misuse を防止します。

## 基本的な使用方法

1. **ユーザー認証**:
   - ユーザーを OAuth プロバイダーの認証エンドポイントにリダイレクトします。
   - プロバイダーはユーザーの同意を求めます。
   - その後、プロバイダーは認証コードを生成します。

2. **クライアント認証**:
   - クライアントは、トークンエンドポイントにトークン要求を送信して、認証コードとクライアントクレデンシャル（必要に応じて）と PKCE のためのコード検証を交換します。

3. **Token Binding**:
   - Token Binding の場合は、トークン要求で特定のトークンバインドコンテキストを指定します。
   - プロバイダーは、このコンテキストでトークンをバインドし、そのトークンがその特定のコンテキストのみで使用されることを確認します。

4. **リソースへのアクセス**:
   - クライアントは、ユーザーの名義で API 要求を実行します。
   - トークンは、プロバイダーによって指定されたリクエストヘッダーまたはURLパラメータに含めます。

## 例

以下は、PKCE をウェブアプリケーションで実装する簡略化された例です：

1. **クライアントアプリケーション**:
   ```csharp
   string clientID = "your-client-id";
   string clientSecret = "your-client-secret";
   string redirectURI = "https://your-app.com/callback";
   string authorizationEndpoint = "https://oauth-provider.com/authorize";
   string tokenEndpoint = "https://oauth-provider.com/token";

   // コード検証を生成
   string codeVerifier = GenerateRandomCodeVerifier();
   string codeVerifierBase64Url = Base64UrlEncode(codeVerifier);

   // 暗号ハッシュ関数を使用してコード挑戦を生成
   string codeChallenge = GenerateCodeChallenge(codeVerifierBase64Url);

   // コード挑戦を含む認証URLにユーザーをリダイレクトします
   string authorizationUrl = $"{authorizationEndpoint}?response_type=code&client_id={clientID}&redirect_uri={redirectURI}&scope=profile%20email&code_challenge={codeChallenge}&code_challenge_method=S256";
   Redirect(authorizationUrl);
   ```

2. **認証サーバー**:
   - ユーザーの同意後、認証コードを生成します。
   - 認証コードとステートパラメータと共にユーザーにリダイレクトします。

3. **クライアントアプリケーション**:
   ```csharp
   string authorizationCode = GetAuthorizationCodeFromResponse();
   string redirectURI = "https://your-app.com/callback";
   string codeVerifierBase64Url = Base64UrlEncode(codeVerifier);

   // 認証コードを交換してアクセストークンを得ます
   string tokenRequestUrl = $"{tokenEndpoint}?grant_type=authorization_code&client_id={clientID}&redirect_uri={redirectURI}&code={authorizationCode}&code_verifier={codeVerifierBase64Url}";

   var httpClient = new HttpClient();
   var response = await httpClient.PostAsync(tokenRequestUrl, null);
   var responseContent = await response.Content.ReadAsStringAsync();

   // レスポンスからアクセストークンを抽出します
   var tokenResponse = JsonConvert.DeserializeObject<TokenResponse>(responseContent);
   string accessToken = tokenResponse.AccessToken;
   ```

この例は OAuth 2.1 と PKCE の基本的な使用方法を示しています。具体的な実装詳細は、OAuth プロバイダーと使用されているプログラミング言語によって異なります。

## 結論

OAuth 2.1 と PKCE、Token Binding は、各種アプリケーションで認証と認証を実装するのに強化されたセキュリティと柔軟性を提供します。ガイドラインとベストプラクティスを遵守することで、開発者はアプリケーションを安全で最新の規準に準拠させることができます。