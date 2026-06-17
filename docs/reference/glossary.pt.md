---
title: Glossário
description: Terminologia usada em todo o WikiCode.
created: 2026-06-03
tags:
  - reference
  - meta
status: stable
---

# Glossário

Terminologia canônica usada em todo o WikiCode. As definições são curtas
e referenciam a fonte autoritativa quando útil.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Criado: 2026-06-03</span>
<span class="wikicode-meta-updated">Última atualização: auto (git)</span>
</div>

## Conceitos principais

<dl markdown>
<dt markdown>**WikiCode**</dt>
<dd markdown>O repositório e o site estático que ele produz. "WikiCode"
refere-se a ambos, dependendo do contexto.</dd>

<dt markdown>**Article**</dt>
<dd markdown>Uma página Markdown de formato longo em `docs/`. Os artigos
são destinados a serem lidos por completo.</dd>

<dt markdown>**Project**</dt>
<dd markdown>Um software autocontido e executável em
`projects/`. Cada projeto tem seu próprio `README.md`, `index.md` e
árvore de origem.</dd>

<dt markdown>**Snippet**</dt>
<dd markdown>Uma unidade de código pequena, focada e executável em `snippets/`.
Os snippets são destinados a serem copiados e adaptados.</dd>

<dt markdown>**Report**</dt>
<dd markdown>Um arquivo Markdown com timestamp em `reports/` que
descreve uma única execução. Formato:
`YYYY-MM-DD-<slug>.md`.</dd>

<dt markdown>**Decision**</dt>
<dd markdown>Uma escolha arquitetural ou operacional registrada em
`memory/decisions.md` com um número de quatro dígitos e um status.</dd>

<dt markdown>**Agent**</dt>
<dd markdown>Qualquer processo — humano ou autônomo — que segue
`AGENT.md` ao trabalhar no repositório.</dd>

<dt markdown>**Task**</dt>
<dd markdown>Uma única unidade de trabalho listada em `tasks/queue.md`. Uma
tarefa por execução.</dd>
</dl>

## Termos do fluxo de trabalho

<dl markdown>
<dt markdown>**Push to `main`**</dt>
<dd markdown>Aciona `pages.yml`, que reconstrói e implanta o
site. Toda mudança no site publicado ocorre por meio desse
mecanismo.</dd>

<dt markdown>**Agent run**</dt>
<dd markdown>Uma execução acionada de `.github/workflows/wikicode-agent.yml`,
seja por `workflow_dispatch`, por uma menção `@agent` em uma
issue, ou por uma issue rotulada como `agent`.</dd>

<dt markdown>**Frontmatter**</dt>
<dd markdown>Metadados YAML no topo de um arquivo Markdown, delimitados
por `---`. O WikiCode espera pelo menos `title`, `description` e
`created`.</dd>

<dt markdown>**Tag**</dt>
<dd markdown>Um rótulo declarado no frontmatter que agrupa páginas
relacionadas. O Material renderiza automaticamente páginas de índice por
tag.</dd>
</dl>

## Valores de status

Páginas e projetos podem declarar um `status` em seu frontmatter:

| Status      | Significado                                                     |
| ----------- | --------------------------------------------------------------- |
| `draft`     | Trabalho em andamento; pode ser incompleto ou incorreto.         |
| `stable`    | Revisado e considerado correto. Pode ainda evoluir.              |
| `archived`  | Mantido para referência; não mais mantido.                      |
| `deprecated`| Substituído por algo outro; mantido para contexto histórico.      |

`status: stable` é a expectativa padrão para qualquer conteúdo publicado.