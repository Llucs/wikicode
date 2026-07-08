---
title: tRPC - Ein type-sicherer RPC-Bibliothek für React und Node.js
description: tRPC ist ein Framework für die Entwicklung von type-sicheren APIs mit TypeScript. Es unterstützt verschiedene JavaScript-Frameworks und Laufzeiten und bietet eine robuste und pflegeleichte Möglichkeit, APIs zu definieren und zu konsumieren.
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

# tRPC - Ein type-sicherer RPC-Bibliothek für React und Node.js

tRPC, oder TypeScript Router Protocol, ist eine Bibliothek zur Entwicklung robuster und pflegeleichter APIs mit TypeScript. Sie wurde so gestaltet, dass sie ein type-sicher und flexibles Verfahren für die Erstellung von APIs bietet, die sowohl auf der Server- als auch auf der Clientseite verwendet werden können. tRPC ermöglicht das Schreiben von Server- und Client-APIs mit TypeScript und integriert sich perfekt mit React und anderen Frameworks.

## Was ist tRPC?

tRPC ist eine Sammlung von Bibliotheken, die es Entwicklern ermöglicht, APIs in einem type-sicheren Modus zu definieren und zu konsumieren. Sie bietet eine Möglichkeit, Server- und Client-APIs mit TypeScript zu definieren und integriert sich seamlessly mit React und anderen Frameworks. tRPC erlaubt es, API-Operateure mit TypeScript-Typen zu definieren, was sicherstellt, dass der API-Raum korrekt verwendet wird.

## Hauptmerkmale

- **Typsicherheit**: tRPC ermöglicht es, API-Operateure mit TypeScript-Typen zu definieren, was sicherstellt, dass der API-Raum korrekt verwendet wird.
- **Client-Server-Separation**: tRPC kann Typen für Client und Server erzeugen, was einen type-sicheren Raum auf beiden Seiten ermöglicht.
- **Integration mit React Query**: tRPC kann mit React Query verwendet werden, um API-Antworten zu verwalten und zu cacheen.
- **Middleware-Support**: tRPC unterstützt benutzerdefinierte Middleware für serverseitige Operateure.
- **Validation**: tRPC kann mit zod, einem beliebten Validierungsbibliothek für TypeScript, Eingabe- und Ausgabedaten validieren.

## Installation

Um tRPC zu installieren, können Sie npm oder yarn verwenden. Hier ist ein Beispiel für die Installation von tRPC und seinen Abhängigkeiten:

```bash
npm install trpc zod react-query
```

oder

```bash
yarn add trpc zod react-query
```

## Grundlegende Nutzung

### API-Operateure definieren

Sie definieren API-Operateure mit TypeScript-Typen.

```typescript
import { createTRPCRouter, publicProcedure } from './trpc';
import { z } from 'zod';

export const appRouter = createTRPCRouter({
  sayHello: publicProcedure
    .input(z.object({ name: z.string() }))
    .output(z.string())
    .desc('Ein Verfahren, das den Benutzer mit dem Namen begrüßt'),
  getUsers: publicProcedure
    .query(async ({ ctx }) => {
      // Annahme: ctx ist Ihr Datenbankkontext
      const users = await ctx.prisma.user.findMany();
      return users;
    })
});
```

### Serverseitige Nutzung

Sie können tRPC verwenden, um API-Anfragen auf der Serverseite zu verwalten.

```typescript
import { appRouter } from './app';
import { createContext } from 'tRPC';

export const createContextHandler = () => ({
  prisma: prisma, // Ihr Datenbankkontext
});
```

### Clientseitige Nutzung

Sie können tRPC mit React Query verwenden, um Daten abzurufen und zu verwalten.

```typescript
import { useTRPCContext } from '@trpc/react';
import { useQuery } from 'react-query';

const getUsersQuery = useQuery({
  queryKey: ['getUsers'],
  queryFn: () => appRouter.getUsers(),
});

if (getUsersQuery.isError) {
  console.error('Fehler beim Abrufen der Benutzer:', getUsersQuery.error);
} else {
  console.log('Benutzer:', getUsersQuery.data);
}
```

## Zusammenfassung

tRPC ist eine leistungsstarke Bibliothek für die Entwicklung von APIs mit TypeScript, die eine type-sichere und pflegeleichte Möglichkeit zur Definition und Verwendung von APIs bietet. Sie integriert sich gut mit React und anderen Frameworks und ist ein populäres Wahlkriterium in der modernen Web-Entwicklung.