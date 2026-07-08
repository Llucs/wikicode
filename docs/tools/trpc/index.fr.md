---
title: tRPC - Une bibliothèque de RPC sûre en type pour React et Node.js
description: tRPC est un framework pour la création d’APIs sûres en type avec TypeScript. Il soutient divers frameworks et moteurs de runtime JavaScript, offrant une manière robuste et maintenable de définir et consommer des APIs.
created: 2026-07-08
tags:
  - tRPC
  - TypeScript
  - API
  - React
  - Node.js
  - RPC
status: brouillon
---

# tRPC - Une bibliothèque de RPC sûre en type pour React et Node.js

tRPC, ou TypeScript Router Protocol, est une bibliothèque pour la création d’APIs robustes et maintenables en utilisant TypeScript. Elle est conçue pour être une manière sûre et flexible de créer des APIs qui peuvent être utilisées à la fois côté serveur et côté client, en tirant parti du pouvoir de TypeScript pour la sûreté en type et des avantages de l’écosystème React Query pour la récupération de données côté client.

## Qu’est-ce que tRPC ?

tRPC est un ensemble de bibliothèques qui permettent aux développeurs de définir et consommer des APIs de manière sûre en type. Il fournit un moyen d’écrire des APIs côté serveur et côté client en utilisant TypeScript et s’intègre facilement avec React et d’autres frameworks. tRPC vous permet de définir des opérations API en utilisant des types TypeScript, garantissant que l’API est utilisée correctement.

## Fonctionnalités clés

- **Sûreté en type** : tRPC vous permet de définir des opérations API avec des types TypeScript, garantissant que l’API est utilisée correctement.
- **Séparation côté client/côté serveur** : tRPC peut générer des types pour le côté client et le côté serveur, permettant des opérations sûres en type de partout.
- **Intégration avec React Query** : tRPC peut être utilisé avec React Query pour gérer et stocker en cache les réponses API.
- **Support des middlewares** : tRPC prend en charge des middlewares personnalisés pour les opérations côté serveur.
- **Validation** : tRPC peut valider les données d’entrée et de sortie en utilisant zod, une bibliothèque de validation populaire pour TypeScript.

## Installation

Pour installer tRPC, vous pouvez utiliser npm ou yarn. Voici un exemple de comment installer tRPC et ses dépendances :

```bash
npm install trpc zod react-query
```

ou

```bash
yarn add trpc zod react-query
```

## Utilisation de base

### Définir des opérations API

Vous définissez des opérations API en utilisant des types TypeScript.

```typescript
import { createTRPCRouter, publicProcedure } from './trpc';
import { z } from 'zod';

export const appRouter = createTRPCRouter({
  sayHello: publicProcedure
    .input(z.object({ name: z.string() }))
    .output(z.string())
    .desc('Une procédure qui salue l’utilisateur par son nom'),
  getUsers: publicProcedure
    .query(async ({ ctx }) => {
      // Supposons que ctx est votre contexte de base de données
      const users = await ctx.prisma.user.findMany();
      return users;
    })
});
```

### Côté serveur

Vous pouvez utiliser tRPC pour gérer les requêtes API côté serveur.

```typescript
import { appRouter } from './app';
import { createContext } from 'tRPC';

export const createContextHandler = () => ({
  prisma: prisma, // Votre contexte de base de données
});
```

### Côté client

Vous pouvez utiliser tRPC avec React Query pour récupérer et gérer les données.

```typescript
import { useTRPCContext } from '@trpc/react';
import { useQuery } from 'react-query';

const getUsersQuery = useQuery({
  queryKey: ['getUsers'],
  queryFn: () => appRouter.getUsers(),
});

if (getUsersQuery.isError) {
  console.error('Erreur lors du chargement des utilisateurs :', getUsersQuery.error);
} else {
  console.log('Utilisateurs :', getUsersQuery.data);
}
```

## Conclusion

tRPC est une bibliothèque puissante pour la création d’APIs avec TypeScript, offrant une manière sûre et maintenante de définir et consommer des APIs. Elle s’intègre bien avec React et d’autres frameworks, en faisant d’elle une option populaire dans l’écosystème de développement web moderne.

---