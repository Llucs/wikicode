---
title: tRPC - A Type-safe RPC Library for React and Node.js
description: tRPC is a framework for building end-to-end typesafe APIs with TypeScript. It supports various JavaScript frameworks and runtimes, providing a robust and maintainable way to define and consume APIs.
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

# tRPC - A Type-safe RPC Library for React and Node.js

tRPC, or TypeScript Router Protocol, is a library for building robust and maintainable APIs using TypeScript. It is designed to be a type-safe and flexible way to create APIs that can be used both on the server and client sides, leveraging the power of TypeScript for type safety and the benefits of the React Query ecosystem for client-side data fetching.

## What is tRPC?

tRPC is a set of libraries that enable developers to define and consume APIs in a type-safe manner. It provides a way to write server and client APIs using TypeScript and integrates seamlessly with React and other frameworks. tRPC allows you to define API operations using TypeScript types, ensuring that the API is used correctly.

## Key Features

- **Type Safety**: tRPC allows you to define API operations with TypeScript types, ensuring that the API is used correctly.
- **Client-Server Separation**: tRPC can generate types for both the client and server, allowing for type-safe operations on both sides.
- **Integration with React Query**: tRPC can be used with React Query to manage and cache API responses.
- **Middleware Support**: tRPC supports custom middleware for server-side operations.
- **Validation**: tRPC can validate input and output data using zod, a popular validation library for TypeScript.

## Installation

To install tRPC, you can use npm or yarn. Here is an example of how to install tRPC and its dependencies:

```bash
npm install trpc zod react-query
```

or

```bash
yarn add trpc zod react-query
```

## Basic Usage

### Define API Operations

You define API operations using TypeScript types.

```typescript
import { createTRPCRouter, publicProcedure } from './trpc';
import { z } from 'zod';

export const appRouter = createTRPCRouter({
  sayHello: publicProcedure
    .input(z.object({ name: z.string() }))
    .output(z.string())
    .desc('A procedure that greets the user by name'),
  getUsers: publicProcedure
    .query(async ({ ctx }) => {
      // Assume ctx is your database context
      const users = await ctx.prisma.user.findMany();
      return users;
    })
});
```

### Server Side

You can use tRPC to handle API requests on the server side.

```typescript
import { appRouter } from './app';
import { createContext } from 'tRPC';

export const createContextHandler = () => ({
  prisma: prisma, // Your database context
});
```

### Client Side

You can use tRPC with React Query to fetch and manage data.

```typescript
import { useTRPCContext } from '@trpc/react';
import { useQuery } from 'react-query';

const getUsersQuery = useQuery({
  queryKey: ['getUsers'],
  queryFn: () => appRouter.getUsers(),
});

if (getUsersQuery.isError) {
  console.error('Error fetching users:', getUsersQuery.error);
} else {
  console.log('Users:', getUsersQuery.data);
}
```

## Conclusion

tRPC is a powerful library for building APIs with TypeScript, providing a type-safe and maintainable way to define and consume APIs. It integrates well with React and other frameworks, making it a popular choice in the modern web development ecosystem.

---