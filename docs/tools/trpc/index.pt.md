---
title: tRPC - Uma Biblioteca de RPC Segura em Tipos para React e Node.js
description: O tRPC é um framework para construção de APIs end-to-end seguras em tipos com TypeScript. Ele suporta diversos frameworks e runtime JavaScript, fornecendo uma maneira robusta e mantelível de definir e consumir APIs.
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

# tRPC - Uma Biblioteca de RPC Segura em Tipos para React e Node.js

tRPC, ou TypeScript Router Protocol, é uma biblioteca para construção de APIs robustas e manteláveis usando TypeScript. É projetada para ser uma maneira segura e flexível de criar APIs que podem ser usadas tanto no lado do servidor quanto no lado do cliente, aproveitando o poder do TypeScript para segurança em tipos e os benefícios do ecossistema React Query para o gerenciamento de dados na camada do cliente.

## O que é tRPC?

tRPC é um conjunto de bibliotecas que permitem aos desenvolvedores definir e consumir APIs de forma segura em tipos. Ele fornece uma maneira de escrever APIs de servidor e cliente usando TypeScript e integra-se de maneira seletiva com React e outros frameworks. tRPC permite que você defina operações de API usando tipos TypeScript, garantindo que a API seja usada corretamente.

## Recursos Principais

- **Segurança em Tipos**: tRPC permite que você defina operações de API com tipos TypeScript, garantindo que a API seja usada corretamente.
- **Separação Cliente-Servidor**: tRPC pode gerar tipos para cliente e servidor, permitindo operações seguras em ambos os lados.
- **Integração com React Query**: tRPC pode ser usado com React Query para gerenciar e armazenar localmente as respostas de API.
- **Suporte a Middleware**: tRPC suporta middleware personalizados para operações do lado do servidor.
- **Validação**: tRPC pode validar dados de entrada e saída usando o zod, uma biblioteca de validação popular para TypeScript.

## Instalação

Para instalar o tRPC, você pode usar o npm ou o yarn. Aqui está um exemplo de como instalar o tRPC e suas dependências:

```bash
npm install trpc zod react-query
```

ou

```bash
yarn add trpc zod react-query
```

## Uso Básico

### Definir Operações de API

Você define operações de API usando tipos TypeScript.

```typescript
import { createTRPCRouter, publicProcedure } from './trpc';
import { z } from 'zod';

export const appRouter = createTRPCRouter({
  sayHello: publicProcedure
    .input(z.object({ name: z.string() }))
    .output(z.string())
    .desc('Uma operação que cumprimenta o usuário pelo nome'),
  getUsers: publicProcedure
    .query(async ({ ctx }) => {
      // Suponha que ctx é seu contexto de banco de dados
      const users = await ctx.prisma.user.findMany();
      return users;
    })
});
```

### Lado do Servidor

Você pode usar o tRPC para lidar com solicitações de API no lado do servidor.

```typescript
import { appRouter } from './app';
import { createContext } from 'tRPC';

export const createContextHandler = () => ({
  prisma: prisma, // Seu contexto de banco de dados
});
```

### Lado do Cliente

Você pode usar o tRPC com React Query para buscar e gerenciar dados.

```typescript
import { useTRPCContext } from '@trpc/react';
import { useQuery } from 'react-query';

const getUsersQuery = useQuery({
  queryKey: ['getUsers'],
  queryFn: () => appRouter.getUsers(),
});

if (getUsersQuery.isError) {
  console.error('Erro ao buscar usuários:', getUsersQuery.error);
} else {
  console.log('Usuários:', getUsersQuery.data);
}
```

## Conclusão

O tRPC é uma biblioteca poderosa para construção de APIs com TypeScript, fornecendo uma maneira segura e mantelível de definir e consumir APIs. Ele se integra bem com React e outros frameworks, sendo uma escolha popular no ecossistema de desenvolvimento web moderno.

---