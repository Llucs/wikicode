---
title: JWT キー注入防止
description: データベースまたはシステムコマンドからキーを取得する前に `kid` パラメータを-sanitize- して、潜在的な SQL Injection または Command Injection 攻撃から保護します。
created: 2026-07-07
tags:
  - jwt
  - セキュリティ
  - 注入
status: 草稿
---

# JWT キー注入防止

## JWT キー注入とは何か

JWT (JSON Web Token) キー注入は、攻撃者が JSON Web Token (JWT) を注入または変更してシステムに不正アクセスを行うセキュリティ脆弱性です。システムが JWT の署名の有効性や整合性を適切に検証していない場合、攻撃者はトークンのペイロードや署名を変更することができます。

## キー機能

1. **署名検証**: JWT の署名が有効で変更されていないことを確認します。
2. **ペイロード整合性**: JWT のペイロード内容が変更されていないことを確認します。
3. **期限チェック**: JWT が期限切れになっていないことを確認します。
4. **取り消しリスト**: JWT が取り消されているかどうかを確認します。

## 歴史

JWT の概念は、2010年に JSON Web Token センタードが導入されたときに使用されてきました。しかし、特定のキー注入脆弱性の特定の問題は、JWT が認証および認可のためにより多く利用されるにつれて最近の年間に注目を集めました。OWASP（オープンウェブアプリケーションセキュリティプロジェクト）ガイドラインで指摘された主要な脆弱性は、JWT のセキュリティを確保する必要性に焦点を当てました。

## 使用例

1. **認証と認可**: JWT は、ウェブおよびモバイルアプリケーションでユーザー認証と認可に広く利用されています。
2. **ステートレスセッション**: JWT は、ステートレス API でセッション状態を管理するために利用されることが多くあります。
3. **単一サインオン (SSO)**: JWT は、ユーザーが一度認証され、複数のシステムで検証されるようにすることで、SSO を促進します。

## インストール

JWT の検証は、JWT をサポートするライブラリやフレームワークによって行われます。たとえば、Node.js アプリケーションでは、`jsonwebtoken` サンプルライブラリを使用してトークンを作成および検証することができます。以下は基本的なインストール手順です:

1. **Node.js**:
   ```bash
   npm install jsonwebtoken
   ```
2. **Python**:
   ```bash
   pip install PyJWT
   ```

## 基本的な使用法

Node.js で `jsonwebtoken` を使用して JWT の基本的な例を以下に示します:

1. **JWT の生成**:
   ```javascript
   const jwt = require('jsonwebtoken');

   const secret = 'your-secret-key';
   const payload = { userId: 123, role: 'admin' };

   const token = jwt.sign(payload, secret);
   console.log(token);
   ```

2. **JWT の検証**:
   ```javascript
   jwt.verify(token, secret, (err, decoded) => {
     if (err) {
       console.error('Token verification failed:', err);
     } else {
       console.log('Decoded:', decoded);
     }
   });
   ```

## キー注入の防止

1. **セキュアな秘密管理**: JWT の秘密キーを安全に管理し、クライアントサイドコードで公開しないでください。
2. **トークンの期限**: JWT の期限を適切に設定して、攻撃の窓口を最小限に抑えます。
3. **取り消しメカニズム**: 取り消されたトークンが存在する場合にメカニズムを実装します。
4. **署名検証**: サーバサイドで常にトークンの署名を検証します。
5. **ペイロードの白リスト化**: JWT のペイロードに許可されたClaimsのみを許可します。

### 取り消しリストの例

取り消しリストを保持するデータベースを設定し、トークン検証時にこのリストに対してチェックします:

1. **データベースの設定**:
   ```sql
   CREATE TABLE revoked_tokens (
     token VARCHAR(255) PRIMARY KEY
   );
   ```

2. **取り消しリストに対するチェック**:
   ```javascript
   const isTokenRevoked = (token) => {
     const tokenExists = revokedTokens.some((revokedToken) => revokedToken === token);
     return tokenExists;
   };

   jwt.verify(token, secret, (err, decoded) => {
     if (err || isTokenRevoked(token)) {
       console.error('Token verification failed:', err);
     } else {
       console.log('Decoded:', decoded);
     }
   });
   ```

これらの戦略を実装することで、アプリケーションでの JWT キー注入脆弱性のリスクを大幅に削減することができます。