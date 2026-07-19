---
title: TypeScriptを使用した実世界のREST APIプロジェクトの作成
description: TypeScript、Express.js、MongoDBを使用して堅牢なREST APIを構築する全面的なガイド。
created: 2026-07-19
tags:
  - TypeScript
  - Express.js
  - MongoDB
  - REST API
  - 認証
  - Docker
status: 草稿
---

# TypeScriptを使用した実世界のREST APIプロジェクトの作成

このガイドでは、TypeScript、Express.js、MongoDBを使用して堅牢なREST APIを構築するプロセスを詳しく説明します。詳細なドキュメンテーション、ベストプラクティス、実世界の例を通じて、生産環境向けのAPIソリューションの実装を理解し実装する方法を説明します。

## キー機能

1. **TypeScript**: 間違いの発見とコードの品質向上のために静的な型付け。
2. **Express.js**: 人気のあるNode.js Webアプリケーションフレームワーク。
3. **MongoDB**: ノーサーバードキュメントデータベース。
4. **JWT認証**: JSON Web Tokens (JWT) を使用したセキュアなルート。
5. **Mongoose**: MongoDB用のオブジェクトデータモデリング (ODM) ライブラリ。
6. **テスト**: JestとSupertestを使用したユニットテストと統合テスト。
7. **Swaggerドキュメンテーション**: インターネット上のリファレンスのために自動生成されたAPIドキュメンテーション。

## インストール

1. **リポジトリをクローン**:
   ```sh
   git clone https://github.com/username/repo.git
   cd repo
   ```

2. **依存関係をインストール**:
   ```sh
   npm install
   ```

3. **MongoDBを設定**:
   - インストールされていない場合、MongoDBをインストールします。
   - MongoDBサーバーを開始します。
   - `.env`ファイルで接続文字列を設定します。

4. **環境変数を設定**:
   - `.env`ファイルに必要な環境変数、例えばデータベース接続文字列、JWTシークレットなど、を更新します。

5. **サーバーを実行**:
   ```sh
   npm start
   ```

## 基本的な使用方法

### APIエンドポイント

1. **ユーザー管理**:
   - **ユーザー作成**: POST `/api/users`
   - **ユーザー取得**: GET `/api/users/:id`
   - **ユーザー更新**: PATCH `/api/users/:id`
   - **ユーザー削除**: DELETE `/api/users/:id`

2. **製品管理**:
   - **製品作成**: POST `/api/products`
   - **製品取得**: GET `/api/products/:id`
   - **製品更新**: PATCH `/api/products/:id`
   - **製品削除**: DELETE `/api/products/:id`

3. **注文管理**:
   - **注文作成**: POST `/api/orders`
   - **注文取得**: GET `/api/orders/:id`
   - **注文更新**: PATCH `/api/orders/:id`
   - **注文削除**: DELETE `/api/orders/:id`

4. **認証**:
   - **JWTトークンの生成**: POST `/api/auth/login`
   - **保護されたルートへのアクセス**: `Authorization`ヘッダーにJWTトークンを使用

### テスト

1. **ユニットテスト**:
   - Jestを使用してユニットテストを行います。
   - テストを実行します:
     ```sh
     npm test
     ```

2. **統合テスト**:
   - Supertestを使用して統合テストを行います。
   - テストを実行します:
     ```sh
     npm test
     ```

### Swaggerドキュメンテーション

1. **Swagger UIのアクセス**:
   - ブラウザで`http://localhost:3000/docs`に移動します。
   - インターネット上のAPIドキュメンテーションを使用してAPIを理解し操作します。

### 認証

1. **JWTトークンの生成**:
   - `curl`を使用して`/api/auth/login`にPOSTリクエストを送信し、ユーザー資格情報を含めます。
   - 例：
     ```sh
     curl -X POST http://localhost:3000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "password": "password"}'
     ```

2. **保護されたルートへのJWTトークンの含め方**:
   - `Authorization`ヘッダーにJWTトークンを使用します。
   - 例：
     ```sh
     curl -X GET http://localhost:3000/api/users/1 \
     -H "Authorization: Bearer <JWT_TOKEN>"
     ```

### データ管理

1. **Mongooseスキーマの定義**:
   - Mongooseを使用してモデルのスキーマを定義します。
   - ユーザーの例スキーマ：
     ```typescript
     import { Schema, model } from 'mongoose';

     const UserSchema = new Schema({
       name: String,
       email: { type: String, unique: true },
       password: String
     });

     export const User = model('User', UserSchema);
     ```

2. **CRUD操作の実行**:
   - Mongooseメソッドを使用してCRUD操作を行います。
   - ユーザーを作成する例：
     ```typescript
     import { Request, Response } from 'express';
     import User from '../models/User';

     const createUser = async (req: Request, res: Response) => {
       const { name, email, password } = req.body;
       const user = new User({ name, email, password });
       await user.save();
       res.status(201).json(user);
     };
     ```

## 結論

詳細なガイドに従って、提供されたコードベースを使用してAPIを拡張しカスタマイズすることで、特定のプロジェクト要件を満たすことができます。この全面的なプロジェクトは、TypeScript、Express.js、MongoDBを使用した現代のウェブ開発の実践を学ぶための卓越な学習ツールとしても役立ちます。

コーディングを楽しんでください！