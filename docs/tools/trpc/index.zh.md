---
title: tRPC - 一个基于 TypeScript 的 RPC 库
description: tRPC 是一个使用 TypeScript 构建端到端类型安全 API 的框架。它支持各种 JavaScript 框架和运行时，提供了一种强大且可维护的方式来定义和消费 API。
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

# tRPC - 一个基于 TypeScript 的 RPC 库

tRPC，或 TypeScript Router Protocol，是一个使用 TypeScript 构建强大且可维护的 API 的库。它旨在以类型安全和灵活的方式创建 API，这些 API 可在服务器端和客户端使用，并利用 TypeScript 的类型安全功能以及 React Query 生态系统为客户端数据获取带来的好处。

## 什么是 tRPC？

tRPC 是一组库，使开发人员能够以类型安全的方式定义和消费 API。它提供了一种使用 TypeScript 和 React 及其他框架无缝集成的方式来定义和消费 API。tRPC 允许您使用 TypeScript 类型定义 API 操作，确保 API 的正确使用。

## 主要特性

- **类型安全性**：tRPC 允许您使用 TypeScript 类型定义 API 操作，确保 API 的正确使用。
- **客户端-服务器分离**：tRPC 可以为客户端和服务器生成类型，允许在两边进行类型安全的操作。
- **集成 React Query**：tRPC 可以与 React Query 一起使用来管理和缓存 API 响应。
- **中间件支持**：tRPC 支持自定义中间件用于服务器端操作。
- **验证**：tRPC 可以使用 zod 进行输入和输出数据验证，zod 是一个流行的 TypeScript 验证库。

## 安装

要安装 tRPC，可以使用 npm 或 yarn。以下是如何安装 tRPC 及其依赖项的示例：

```bash
npm install trpc zod react-query
```

或者

```bash
yarn add trpc zod react-query
```

## 基本用法

### 定义 API 操作

您使用 TypeScript 类型来定义 API 操作。

```typescript
import { createTRPCRouter, publicProcedure } from './trpc';
import { z } from 'zod';

export const appRouter = createTRPCRouter({
  sayHello: publicProcedure
    .input(z.object({ name: z.string() }))
    .output(z.string())
    .desc('一个通过名字问候用户的程序'),
  getUsers: publicProcedure
    .query(async ({ ctx }) => {
      // 假设 ctx 是您的数据库上下文
      const users = await ctx.prisma.user.findMany();
      return users;
    })
});
```

### 服务器端

您可以使用 tRPC 处理服务器端的 API 请求。

```typescript
import { appRouter } from './app';
import { createContext } from 'tRPC';

export const createContextHandler = () => ({
  prisma: prisma, // 您的数据库上下文
});
```

### 客户端

您可以使用 tRPC 与 React Query 一起获取和管理数据。

```typescript
import { useTRPCContext } from '@trpc/react';
import { useQuery } from 'react-query';

const getUsersQuery = useQuery({
  queryKey: ['getUsers'],
  queryFn: () => appRouter.getUsers(),
});

if (getUsersQuery.isError) {
  console.error('获取用户时出错：', getUsersQuery.error);
} else {
  console.log('用户：', getUsersQuery.data);
}
```

## 结论

tRPC 是一个强大的库，用于使用 TypeScript 构建 API，提供了一种类型安全且可维护的方式来定义和消费 API。它与 React 及其他框架集成良好，在现代 Web 开发生态系统中非常流行。

---