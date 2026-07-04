---
title: TanStack Query: Uma Guia Completo
description: TanStack Query é uma biblioteca de gerenciamento de estado para gerenciar a extração de dados do servidor, cache e sincronização principalmente em aplicativos JavaScript e React.
created: 2026-07-04
tags:
  - ferramentas-desenvolvedor
  - gerenciamento-de-estado
  - react
  - extração-de-dados
status: rascunho
---

# TanStack Query: Uma Guia Completo

TanStack Query é uma biblioteca completa desenvolvida pelo TanStack (antigo TSP Frameworks) para gerenciar a extração de dados, cache e sincronização de estado em aplicativos React. Está projetada para simplificar o processo de trabalhar com APIs e gerenciar dados de forma amigável e eficiente.

## Recursos Principais

1. **Segurança de Tipo**: Fornece segurança de tipo através do TypeScript, garantindo que sua lógica de extração de dados seja tipada.
2. **Cache e Gerenciamento de Estado**: Automaticamente armazena respostas da API, reduzindo a necessidade de lógica de cache manual.
3. **Suporte ao Suspense**: Integra-se de forma harmônica com o novo API Suspense do React, permitindo experiências de carregamento de dados suaves.
4. **Gerenciamento de Erros**: Tratamento de erros e lógica de reenvio integradas ajudam a gerenciar e recuperar de erros de API.
5. **Atualizações Dinâmicas de Dados**: Atualizações em tempo real de dados usando websockets ou poling.
6. **Hooks Personalizáveis**: Conjunto extenso de hooks personalizáveis para vários casos de uso, como `useQuery`, `useMutation`, `useInfiniteQuery`, e mais.
7. **Suporte à Hidratação**: Funciona bem com renderização do servidor (SSR) e hidratação do cliente.
8. **Pólicias Configuráveis**: Políticas de extração de dados personalizáveis, como `stale-while-revalidate`.

## Histórico

O TanStack Query foi desenvolvido como parte da suite de ferramentas TSP Frameworks, que inicialmente foi criada para fornecer uma suite de ferramentas para gerenciar o estado e os dados em aplicativos React. O projeto foi posteriormente renomeado para TanStack e evoluiu para uma biblioteca completa para gerenciar a extração de dados e o gerenciamento de estado.

## Casos de Uso

1. **Extração de Dados de APIs**: Extração de dados de APIs REST, APIs GraphQL ou qualquer outra fonte de dados.
2. **Dados em Tempo Real**: Gerenciando atualizações em tempo real usando websockets ou poling.
3. **Paginação e Rolamento Infinito**: Gerenciando paginação e rolamento infinito usando o hook `useInfiniteQuery`.
4. **Gerenciamento de Formulários**: Tratando submissões e validações de formulários com `useMutation`.
5. **Hidratação e Renderização do Servidor**: Garantindo transições suaves entre a renderização do servidor e a hidratação do cliente.
6. **Cache e Otimização**: Melhorando o desempenho ao cachear respostas de API.

## Instalação

Para instalar o TanStack Query, você pode usar o npm ou o yarn:

```bash
npm install @tanstack/react-query
# ou
yarn add @tanstack/react-query
```

## Uso Básico

Aqui está um exemplo simples de como usar o TanStack Query para extração de dados de uma API:

1. **Configuração do Cliente de Consulta**:

   ```javascript
   import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

   const queryClient = new QueryClient();

   function App() {
     return (
       <QueryClientProvider client={queryClient}>
         {/* Seus componentes de aplicação */}
       </QueryClientProvider>
     );
   }
   ```

2. **Extração de Dados**:

   ```javascript
   import { useQuery } from '@tanstack/react-query';
   import { fetchUsers } from './api'; // Sua função de extração de API

   function UsersList() {
     const { data, isLoading, error } = useQuery({
       queryKey: ['users'],
       queryFn: fetchUsers,
     });

     if (isLoading) return <div>Carregando...</div>;
     if (error) return <div>Erro: {error.message}</div>;

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

## Resumo

O TanStack Query é uma biblioteca poderosa e flexível para gerenciar a extração de dados e o gerenciamento de estado em aplicativos React. Suas características robustas, como segurança de tipo, cache e atualizações em tempo real, o tornam uma adição valiosa a qualquer projeto React. A biblioteca é bem documentada e altamente extensível, sendo adequada para uma ampla gama de casos de uso, desde extração de dados simples a aplicações em tempo real complexas.