---
title: WikiCode
description: Uma wiki viva para desenvolvedores — artigos, projetos e trechos de código mantidos ao longo do tempo.
created: 2026-06-03
tags:
  - meta
  - overview
status: stable
---

# WikiCode

Uma wiki de desenvolvimento viva construída e mantida ao longo do tempo. Cada página
que você lê aqui é gerada diretamente do repositório, então o site
é sempre um espelho fiel da fonte da verdade.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Criado: 2026-06-03</span>
<span class="wikicode-meta-updated">Última atualização: auto (git)</span>
</div>

## O que você encontrará

<div class="grid cards" markdown>

- :material-book-open-page-variant-outline: __Artigos e guias__

    Explicações detalhadas de conceitos, padrões e ferramentas. Veja
    [Guias](guides/index.md).

- :material-folder-outline: __Projetos__

    Projetos independentes e executáveis. Veja [Projetos](projects/index.md).

- :material-code-tags: __Trechos de código__

    Pequenos trechos de código focados e prontos para copiar e colar. Veja
    [Trechos de código](snippets/index.md).

- :material-school-outline: __Trilhas de aprendizado__

    Ordens de leitura selecionadas para novos usuários. Veja
    [Trilhas de aprendizado](learning-paths.md).

- :material-tag-multiple-outline: __Tópicos e tags__

    Navegue pelo conteúdo por tópico ou por tag. Veja
    [Tópicos](topics/index.md) e [Tags](tags.md).

- :material-clipboard-text-outline: __Relatórios__

    Relatórios de execução com carimbo de data/hora. Veja [Relatórios](reports/index.md).

- :material-rss: __Blog__

    Anúncios e artigos mais longos. Veja [Blog](blog/index.md).

- :material-bookshelf: __Referência__

    Glossário, arquitetura e changelog. Veja
    [Referência](reference/glossary.md).

</div>

## Como as atualizações fluem

O site **nunca é editado diretamente**. Ele é regenerado a partir do
repositório a cada push para `main`:

```
Autonomous AI agent (OpenCode API) / contributor
        │
        ▼
   commit + push to main
        │
        ▼
   .github/workflows/pages.yml
        │
        ▼
   mkdocs build (from docs/, projects/, snippets/, blog/)
        │
        ▼
   GitHub Pages (public site)
```

Quando o agente de IA local (ou qualquer contribuidor) atualiza um arquivo
Markdown, adiciona uma pasta de projeto, escreve um trecho de código, publica
uma postagem no blog ou move uma tarefa de `queue.md` para `completed.md`, o
próximo push para `main` aciona uma nova compilação e o site publicado reflete
a mudança.

## Por onde começar

- [Começando](getting-started.md) — layout do repositório, compilação local, convenções.
- [Trilhas de aprendizado](learning-paths.md) — ordens de leitura guiadas.
- [Referência](reference/glossary.md) — terminologia e arquitetura.