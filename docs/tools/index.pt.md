---
title: Ferramentas
description: Ferramentas de desenvolvimento documentadas no WikiCode.
created: 2026-06-03
tags:
  - meta
  - tools
status: stable
---

# Ferramentas

Ferramentas de desenvolvimento documentadas no WikiCode. Cada ferramenta tem sua própria pasta
em `docs/tools/<slug>/` com um resumo `index.md`.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Criado: 2026-06-03</span>
<span class="wikicode-meta-updated">Última atualização: auto (git)</span>
</div>

## Por ecossistema

As ferramentas são classificadas por ecossistema. Veja o índice de tags para a lista completa.

| Ecossistema | Ferramentas |
|-----------|-------|
| Container | Docker, Podman, Portainer |
| CI/CD     | Jenkins, ArgoCD |
| API       | Postman, cURL |
| JavaScript| npm, Jest |
| Editor    | Visual Studio Code |
| CLI       | fzf |
| Android   | SpeedCool |
| Monitoring| Grafana, Heimdall |
| VCS       | Git |

## Como as ferramentas são adicionadas

Tanto o agente de IA quanto os contribuidores humanos seguem a mesma receita:

1. Pesquise a ferramenta usando pesquisa na web (Wikipedia + DuckDuckGo).
2. Escreva um resumo em `docs/tools/<slug>/index.md`.
3. Adicione frontmatter com `title`, `description`, `created`, `tags`,
   e `ecosystem`.
4. Execute `mkdocs build --clean` para validar.

## Ferramentas atuais

<!--awesome-pages:hide-->
<!--awesome-pages:reveal-->

## Convenções

- Uma pasta por ferramenta. Nome da pasta: minúsculo, hifenizado.
- `index.md` é o resumo público.
- O frontmatter deve incluir `title`, `description`, `created`,
  `tags`, `ecosystem` e `status`.
- Uma página de ferramenta deve incluir: um parágrafo "o que é",
  instalação, uso básico e principais recursos com exemplos.