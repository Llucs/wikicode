---
title: Registro de alterações
description: Mudanças notáveis no WikiCode.
created: 2026-06-03
tags:
  - reference
  - meta
status: stable
---

# Registro de alterações

Mudanças notáveis no WikiCode. Edições menores e do dia a dia são
registradas no histórico do git; apenas mudanças estruturais e
visíveis ao usuário aparecem aqui.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Criado: 2026-06-03</span>
<span class="wikicode-meta-updated">Última atualização: auto (git)</span>
</div>

## 1.0.0 — 2026-06-03 — Inicial

Estrutura inicial orientada à produção.

### Adicionado

- **Geração do site.** MkDocs (tema Material) com pesquisa no lado
  do cliente, índices de seção automáticos e uma camada CSS limpa e
  personalizada.
- **Publicação orientada pelo repositório.** O site é regenerado a
  partir do repositório a cada push para `main` via
  `.github/workflows/pages.yml`. Nada no site publicado é editado
  manualmente.
- **Agente de IA (OpenCode API).** `.github/workflows/wikicode-agent.yml`
  executa o agente autônomo no runner de CI. Geração de conteúdo via
  OpenCode API (`deepseek-v4-flash-free`), pesquisa na web via APIs da
  Wikipedia e DuckDuckGo. Nenhuma chave de API externa necessária.
- **GitHub Pages.** Habilitado com o tipo de build do workflow e
  HTTPS imposto.
- **Seções de conteúdo.**
  - `docs/` para artigos, guias e páginas de referência.
  - `projects/` para projetos autônomos e executáveis.
  - `snippets/` para trechos de código focados.
  - `blog/` para artigos mais longos e anúncios.
  - `memory/` para contexto de agente de longo prazo (missão, regras,
    conhecimento, decisões).
  - `tasks/` para o pipeline de trabalho.
  - `reports/` para relatórios de execução com carimbo de data/hora.
- **Metadados de data.** Cada página exibe um cartão com sua data de
  **criação** (do frontmatter) e data de **última atualização** (do
  histórico do git, via `mkdocs-git-revision-date-localized-plugin`).
- **Sistema de tags.** As páginas podem declarar tags no frontmatter;
  o tema Material renderiza automaticamente páginas de índice por tag.
- **Guias de nível superior.**
  - [Glossário](glossary.md)
  - [Arquitetura](architecture.md)
  - [Registro de alterações](changelog.md)
  - [Caminhos de aprendizado](../learning-paths.md)
- **Arquivos raiz.** `README.md`, `LICENSE`, `AGENT.md`,
  `CONTRIBUTING.md`, `CHANGELOG.md`, `ARCHITECTURE.md`,
  `.gitignore`.
- **Decisões iniciais.** Quatro entradas numeradas em
  `memory/decisions.md` (0001–0004).
- **Tarefas iniciais.** Quatro itens enfileirados em `tasks/queue.md`.

### Notas

- O site está disponível no URL fornecido pelo GitHub Pages assim que
  a primeira execução de `pages.yml` for concluída com sucesso.
- Nenhuma chave de API externa é necessária. O agente usa `GITHUB_TOKEN`
  (integrado) para acesso ao repositório e a OpenCode API para geração
  de conteúdo.