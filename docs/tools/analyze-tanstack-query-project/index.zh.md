---
title: TanStack Query：全面指南
description: TanStack Query 是一个用于管理和同步 React 应用程序中服务器端数据获取、缓存和状态管理的状态管理库。它主要在 JavaScript 和 React 应用程序中使用。
created: 2026-07-04
tags:
  - developer-tools
  - state-management
  - react
  - data-fetching
status: draft
---

# TanStack Query：全面指南

TanStack Query 是由 TanStack（原 TSP Frameworks）开发的全面库，用于管理和同步 React 应用程序中的数据获取、缓存和状态。它旨在简化与 API 的交互过程，并以用户友好和高效的方式管理数据。

## 关键功能

1. **类型安全性**：通过 TypeScript 提供类型安全性，确保您的数据获取逻辑是强类型的。
2. **缓存和状态管理**：自动缓存 API 响应，减少手动缓存逻辑的需求。
3. **断言支持**：与 React 的新断言 API 整合，实现平滑的数据加载体验。
4. **错误处理**：内置的错误处理和重试逻辑帮助管理和从 API 错误中恢复。
5. **动态数据更新**：使用 WebSockets 或轮询实现数据的实时更新。
6. **自定义钩子**：为各种用例提供广泛的自定义钩子，如 `useQuery`、`useMutation`、`useInfiniteQuery` 等。
7. **水合支持**：与服务器端渲染（SSR）和客户端水合兼容。
8. **可配置策略**：可配置的数据获取策略，如 `stale-while-revalidate`。

## 历史

TanStack Query 是作为 TSP Frameworks 套件的一部分开发的，最初是为了提供一套用于管理和数据状态的工具。该项目后来更名为 TanStack 并演变为一个全面的库，用于管理数据获取和状态管理。

## 用例

1. **API 数据获取**：从 REST API、GraphQL API 或任何其他数据源获取数据。
2. **实时数据**：使用 WebSockets 或长轮询处理实时更新。
3. **分页和无限滚动**：使用 `useInfiniteQuery` 钩子管理分页和无限滚动。
4. **表单管理**：使用 `useMutation` 处理表单提交和验证。
5. **水合和服务器端渲染**：确保在服务器端渲染和客户端水合之间平滑过渡。
6. **缓存和优化**：通过缓存 API 响应来提高性能。

## 安装

要安装 TanStack Query，可以使用 npm 或 yarn：

```bash
npm install @tanstack/react-query
# 或
yarn add @tanstack/react-query
```

## 基本用法

以下是如何使用 TanStack Query 从 API 获取数据的简单示例：

1. **设置查询客户端**：

   ```javascript
   import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

   const queryClient = new QueryClient();

   function App() {
     return (
       <QueryClientProvider client={queryClient}>
         {/* 你的应用程序组件 */}
       </QueryClientProvider>
     );
   }
   ```

2. **获取数据**：

   ```javascript
   import { useQuery } from '@tanstack/react-query';
   import { fetchUsers } from './api'; // 你的 API 获取函数

   function UsersList() {
     const { data, isLoading, error } = useQuery({
       queryKey: ['users'],
       queryFn: fetchUsers,
     });

     if (isLoading) return <div>Loading...</div>;
     if (error) return <div>Error: {error.message}</div>;

     return (
       <ul>
         {data.map((user) => (
           <li key={user.id}>{user.name}</li>
         ))}
       </ul>
     );
   }

   export default UsersList;
   ```

## 总结

TanStack Query 是一个强大的灵活库，用于管理和同步 React 应用程序中的数据获取和状态管理。其强大的功能，如类型安全性、缓存和实时更新，使其成为任何 React 项目的重要组成部分。该库文档齐全且高度可扩展，适用于从简单的数据获取到复杂的实时应用程序的各种用例。