---
title: Guias
description: Guias longos, orientados por tópicos.
created: 2026-06-03
tags:
  - meta
status: stable
---

# Guias

Guias longos agrupados por tópico. Cada guia é um arquivo Markdown real em `docs/guides/` (ou uma subpasta).

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Criado: 2026-06-03</span>
<span class="wikicode-meta-updated">Última atualização: auto (git)</span>
</div>

## Convenções

- Uma pasta ou arquivo `.md` por guia.
- Nome da pasta: minúsculo, com hífen.
- O frontmatter deve incluir `title`, `description`, `created` e `tags`.
- As tags ajudam na vinculação cruzada: prefira reutilizar tags existentes de [Tags](../tags.md) a inventar novas.

## Tags sugeridas

| Tag             | Significado                                               |
| --------------- | --------------------------------------------------------- |
| `meta`          | Páginas sobre o próprio WikiCode.                         |
| `guide`         | Conteúdo de tutoriais.                                    |
| `reference`     | Material de referência (glossários, listas).              |
| `architecture`  | Como o wiki é construído e como funciona.                 |
| `process`       | Fluxo de trabalho, contribuição, governança.              |
| `language-go`   | Conteúdo principalmente sobre Go.                         |
| `language-py`   | Conteúdo principalmente sobre Python.                     |
| `language-cpp`  | Conteúdo principalmente sobre C++.                        |
| `language-rs`   | Conteúdo principalmente sobre Rust.                       |
| `language-js`   | Conteúdo principalmente sobre JavaScript / TypeScript.    |
| `backend`       | Tópicos de engenharia de backend.                         |
| `frontend`      | Tópicos de engenharia de frontend.                        |
| `devops`        | Build, deploy, observabilidade.                           |
| `security`      | Tópicos de segurança.                                     |
| `data`          | Bancos de dados, pipelines, análises.                     |

Adicione tags ao frontmatter assim:

```yaml
---
title: My guide
tags:
  - guide
  - backend
---
```