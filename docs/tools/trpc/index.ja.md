---
title: tRPC - ReactとNode.js用の型安全RPCライブラリ
description: tRPCはTypeScriptを使用したエンドツーエンドの型安全なAPIを構築するためのフレームワークです。多种類JavaScriptフレームワークとランタイムをサポートし、タイプ安全で保守性の高いAPIの定義と消費を提供します。
created: 2026-07-08
tags:
  - tRPC
  - TypeScript
  - API
  - React
  - Node.js
  - RPC
status: draft
---

# tRPC - ReactとNode.js用の型安全RPCライブラリ

tRPC, またはTypeScript Router Protocolは、TypeScriptを使用した堅牢で保守性の高いAPIの構築用ライブラリです。Reactやその他のフレームワークとの統合を考慮し、タイプ安全性とReact Queryエコシステムの利点を活用してクライアント側のデータ取得を行う柔軟でタイプ安全なAPIの作成を可能にします。

## tRPCとは？

tRPCは、開発者がタイプ安全な方法でAPIを定義し、消費するためのライブラリのセットです。TypeScriptとReact Queryエコシステムと統合し、サーバーサイドとクライアントサイド双方でタイプ安全な操作を行うことができます。

## キー機能

- **型安全性**: tRPCはAPI操作をTypeScriptのタイプを使用して定義し、APIが正しく使用されるようにします。
- **クライアントとサーバーの分離**: tRPCはクライアントとサーバー両方でタイプ安全な操作を生成できます。
- **React Queryとの統合**: tRPCはReact Queryを使用してAPIレスポンスの管理とキャッシュを行います。
- **ミドルウェアサポート**: tRPCはサーバーサイド操作用のカスタムミドルウェアをサポートします。
- **バリデーション**: tRPCはzodという人気のあるTypeScriptのバリデーションライブラリを使用して、入力と出力データを検証します。

## インストール

tRPCをインストールするには、npmまたはyarnを使用できます。以下の例は、tRPCとその依存関係をインストールする方法です。

```bash
npm install trpc zod react-query
```

or

```bash
yarn add trpc zod react-query
```

## 基本的な使用法

### API操作の定義

API操作はTypeScriptのタイプを使用して定義します。

```typescript
import { createTRPCRouter, publicProcedure } from './trpc';
import { z } from 'zod';

export const appRouter = createTRPCRouter({
  sayHello: publicProcedure
    .input(z.object({ name: z.string() }))
    .output(z.string())
    .desc('名前でユーザーを挨拶する操作'),
  getUsers: publicProcedure
    .query(async ({ ctx }) => {
      // ctxはあなたのデータベースコンテキストであると仮定します
      const users = await ctx.prisma.user.findMany();
      return users;
    })
});
```

### サーバーサイド

tRPCを使用してAPIリクエストをサーバーサイドで処理できます。

```typescript
import { appRouter } from './app';
import { createContext } from 'tRPC';

export const createContextHandler = () => ({
  prisma: prisma, // あなたのデータベースコンテキスト
});
```

### クライアントサイド

tRPCはReact Queryと組み合わせてデータを取得し、管理します。

```typescript
import { useTRPCContext } from '@trpc/react';
import { useQuery } from 'react-query';

const getUsersQuery = useQuery({
  queryKey: ['getUsers'],
  queryFn: () => appRouter.getUsers(),
});

if (getUsersQuery.isError) {
  console.error('ユーザー取得時にエラー:', getUsersQuery.error);
} else {
  console.log('ユーザー:', getUsersQuery.data);
}
```

## 結論

tRPCはTypeScriptを使用したAPIの構築に強力なライブラリであり、タイプ安全で保守性の高いAPIの定義と消費を提供します。Reactや他のフレームワークとの統合が良好で、現代のWeb開発エコシステムで人気の高い選択肢となっています。

---