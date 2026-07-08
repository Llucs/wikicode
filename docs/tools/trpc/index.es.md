---
title: tRPC - Una Biblioteca de RPC Segura en Tipos para React y Node.js
description: tRPC es una frameworks para construir APIs end-to-end seguras en tipos con TypeScript. Soporta varios frameworks de JavaScript y runtime, proporcionando un camino robusto y mantenedor para definir y consumir APIs.
created: 2026-07-08
tags:
  - tRPC
  - TypeScript
  - API
  - React
  - Node.js
  - RPC
status: borrador
---

# tRPC - Una Biblioteca de RPC Segura en Tipos para React y Node.js

tRPC, o TypeScript Router Protocol, es una biblioteca para construir APIs robustas y mantenibles usando TypeScript. Está diseñada para ser una forma segura y flexible de crear APIs que se pueden usar tanto en el lado del servidor como en el cliente, aprovechando la potencia del TypeScript para la seguridad en tipos y los beneficios del ecosistema de React Query para la recuperación de datos en el lado del cliente.

## ¿Qué es tRPC?

tRPC es un conjunto de bibliotecas que permiten a los desarrolladores definir y consumir APIs de manera segura en tipos. Proporciona una manera de escribir APIs en el servidor y en el cliente usando TypeScript e integra de manera sencilla con React y otros frameworks. tRPC te permite definir operaciones de API usando tipos de TypeScript, asegurando que la API se use correctamente.

## Características Clave

- **Seguridad en Tipos**: tRPC te permite definir operaciones de API con tipos de TypeScript, asegurando que la API se use correctamente.
- **Separación Cliente-Servidor**: tRPC puede generar tipos tanto para el cliente como para el servidor, permitiendo operaciones seguras en ambos lados.
- **Integración con React Query**: tRPC puede usarse con React Query para gestionar y cachear las respuestas de la API.
- **Soporte de Middleware**: tRPC tiene soporte para middleware personalizado para operaciones del lado del servidor.
- **Validación**: tRPC puede validar datos de entrada y salida usando zod, una popular biblioteca de validación para TypeScript.

## Instalación

Para instalar tRPC, puedes usar npm o yarn. Aquí tienes un ejemplo de cómo instalar tRPC y sus dependencias:

```bash
npm install trpc zod react-query
```

o

```bash
yarn add trpc zod react-query
```

## Uso Básico

### Definir Operaciones de API

Defines operaciones de API usando tipos de TypeScript.

```typescript
import { createTRPCRouter, publicProcedure } from './trpc';
import { z } from 'zod';

export const appRouter = createTRPCRouter({
  sayHello: publicProcedure
    .input(z.object({ name: z.string() }))
    .output(z.string())
    .desc('Una operación que saluda al usuario por su nombre'),
  getUsers: publicProcedure
    .query(async ({ ctx }) => {
      // Suponiendo que ctx es tu contexto de base de datos
      const users = await ctx.prisma.user.findMany();
      return users;
    })
});
```

### Lado del Servidor

Puedes usar tRPC para manejar solicitudes de API en el lado del servidor.

```typescript
import { appRouter } from './app';
import { createContext } from 'tRPC';

export const createContextHandler = () => ({
  prisma: prisma, // Tu contexto de base de datos
});
```

### Lado del Cliente

Puedes usar tRPC con React Query para recuperar y gestionar datos.

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

## Conclusión

tRPC es una biblioteca potente para construir APIs con TypeScript, proporcionando una forma segura y mantenible de definir y consumir APIs. Se integra bien con React y otros frameworks, siendo una opción popular en el ecosistema de desarrollo web moderno.

---