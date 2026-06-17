---
title: Auditoria de Navegação para WikiCode
description: Análise e propostas de melhoria para a navegação do site WikiCode.
created: 2026-06-14
tags:
  - meta
  - guide
status: draft
---

# Auditoria de Navegação

## Estrutura Atual

A navegação principal é definida em `mkdocs.yml` e atualmente inclui:

- Início
- Pesquisar
- Primeiros passos
- Trilhas de aprendizado
- Guias
- Referência (Glossário, Arquitetura, Registro de Alterações)
- Tópicos
- Ferramentas
- Tags
- Blog
- Projetos
- Snippets
- Relatórios

## Melhorias Propostas

1. **Agrupar seções meta** sob um único item de menu "Sobre" ou "WikiCode" (Relatórios, Registro de Alterações, Arquitetura)
2. **Mover Tags para dentro de Tópicos** já que são conceitos relacionados
3. **Adicionar indicadores visuais** para conteúdo atualizado recentemente
4. **Garantir breadcrumbs** ativos em todos os níveis de navegação

## Implementação

Todas as alterações devem ser feitas no bloco `nav:` no arquivo `mkdocs.yml`.