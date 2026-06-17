---
title: Arquitetura
description: Como o WikiCode é construído e como se mantém atualizado.
created: 2026-06-03
tags:
  - reference
  - architecture
  - meta
status: stable
---

# Arquitetura

Como o WikiCode é construído, como se mantém atualizado e como agentes autônomos se encaixam no loop.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Criado em: 2026-06-03</span>
<span class="wikicode-meta-updated">Última atualização: auto (git)</span>
</div>

## Diagrama de alto nível

```
┌──────────────────────────────────────────────────────────────┐
│                       Repository                             │
│                                                              │
│   docs/        projects/    snippets/                        │
│   memory/      tasks/       reports/                         │
│   blog/        scripts/     mkdocs.yml                       │
│                                                              │
└─────────────┬──────────────────────────────┬────────────────┘
              │                              │
              │  push to main                │  Agent run
              │                              │  (manual, schedule,
              │                              │   @agent, label)
              ▼                              ▼
      ┌──────────────────┐         ┌──────────────────────┐
      │  pages.yml       │         │  wikicode-agent.yml  │
      │  ─ mkdocs build  │         │  ─ install deps      │
      │  ─ upload Pages  │         │  ─ read context      │
      │    artifact      │         │  ─ web research*     │
      └────────┬─────────┘         │  ─ generate content  │
               │                  │  ─ validate build    │
               │                  │  ─ commit & push     │
               │                  └──────────┬───────────┘
               │                             │
               ▼                             │
       GitHub Pages                          │
       (public site)                         │
                                             │
       new commit on main  ◄─────────────────┘
```

`*` O agente usa as APIs da Wikipedia e DuckDuckGo para pesquisa na web, não sendo necessárias chaves de API.

## Camadas

### 1. Conteúdo

Markdown simples. A criação não requer ferramentas especiais.

| Caminho | Finalidade |
| ------- | ---------- |
| `docs/` | Artigos, guias, referência, o que você lê no site. |
| `docs/concepts/` | Padrões de arquitetura, princípios de design, conceitos técnicos. |
| `docs/guides/` | Guias longos e orientados a tópicos. |
| `docs/tools/` | Uma pasta por ferramenta de desenvolvedor documentada. |
| `docs/analyses/` | Análise técnica e estudos arquiteturais de plataformas/bibliotecas. |
| `docs/reference/` | Glossário, arquitetura, changelog. |
| `docs/topics/` | Índice de tópicos. |
| `projects/` | Projetos reais e executáveis. Cada um é uma unidade independente. |
| `snippets/` | Trechos de código pequenos, focados e executáveis. |
| `blog/` | Artigos mais longos, anúncios, post-mortems. |
| `memory/` | Contexto de longo prazo para agentes (missão, regras, decisões). |
| `tasks/` | Pipeline de trabalho (fila + concluídos). |
| `reports/` | Relatórios de execução com data, organizados por ano/mês. |

### 2. Geração

- **MkDocs** com o tema **Material** transforma a árvore Markdown em um site estático.
- Plugins:
  - `search` — pesquisa de texto completo no lado do cliente.
  - `awesome-pages` — índices automáticos de seções.
  - `git-revision-date-localized` — data da última atualização a partir do git.
  - `blog` — suporte nativo a blog do Material.
  - `git-committers` — opcional, controlado por variável de ambiente.

### 3. Implantação

- `pages.yml` é executado a cada push para `main`. Ele constrói o site e o implanta no **GitHub Pages** usando as actions oficiais do Pages (`actions/upload-pages-artifact` + `actions/deploy-pages`).
- Pages é configurado com `build_type: workflow` e HTTPS forçado.

### 4. Automação

#### Crescimento diário

`wikicode-agent.yml` é executado em uma **programação duas vezes ao dia** (`0 6,18 * * *`, 06:00 e 18:00 UTC) e em acionamentos manuais. Cada execução é uma alteração única e com escopo definido, para que a wiki cresça um pouco a cada dia.

O loop esperado por execução:

1. O workflow é iniciado. As dependências Python são instaladas.
2. `scripts/agent.py` lê `memory/` para obter contexto. Se a fila de tarefas estiver vazia, ele descobre proativamente novas ferramentas e projetos para documentar. Em seguida, pesquisa o tópico escolhido por meio das APIs da Wikipedia + DuckDuckGo.
3. A API OpenCode gera o conteúdo (Markdown com frontmatter).
4. O agente escreve os arquivos, executa `mkdocs build --clean` para validar, depois faz commit e push.
5. `pages.yml` reconstrói e implanta o site.
6. A execução da próxima execução vê uma wiki um pouco maior e continua.

#### Acionamentos

| Acionamento            | Caso de uso                                        |
| ---------------------- | -------------------------------------------------- |
| `schedule`             | A execução de crescimento padrão (06:00 e 18:00 UTC). |
| `workflow_dispatch`    | Execução manual a partir da aba Actions.            |
| `issue_comment`        | Menção `@agent` em um comentário de issue ou PR.    |
| `issues` com label     | Issues marcadas com o label `agent`.                |

#### Concorrência

`concurrency: wikicode-agent` é definido com `cancel-in-progress: true` para que execuções sobrepostas não gravem duas vezes no repositório.

### 5. Antiduplicação

WikiCode não quer documentar a mesma coisa duas vezes. O mecanismo de desduplicação tem três partes:

1. **Páginas de índice de seção.** Cada seção tem um `index.md` que lista seus conteúdos atuais. O plugin `awesome-pages` descobre automaticamente a lista a partir do sistema de arquivos, então está sempre precisa.
2. **Fallback `git grep`.** O script do agente verifica os índices de seção e a lista de tarefas, depois usa `git grep` para confirmar que um tópico é novo antes de gerar conteúdo.
3. **Registro de conhecimento.** `memory/knowledge.md` lista as principais peças de conteúdo e as regras para adicionar novas.

Se uma duplicata for detectada, o agente deve melhorar a página existente em vez de escrever uma nova (regra 16 em `memory/rules.md`).

### 6. Pesquisa na web

O agente usa as APIs da Wikipedia e DuckDuckGo para coletar informações sobre qualquer tópico que precise documentar. Este é o mecanismo que mantém o conteúdo gerado factual e atualizado:

1. `research_topic()` em `scripts/agent.py` executa tanto uma pesquisa na Wikipedia quanto uma consulta DuckDuckGo Instant Answer para o tópico.
2. A Wikipedia retorna títulos de artigos + extratos introdutórios (texto simples, até 2000 caracteres).
3. DuckDuckGo retorna o resumo e tópicos relacionados.
4. Se ambos retornarem vazios, o agente recorre ao conhecimento de treinamento do LLM.
5. O texto de pesquisa coletado é injetado no prompt de geração de conteúdo para que o LLM escreva a partir de informações do mundo real.

## Taxonomia de conteúdo v2

Todo documento no WikiCode pertence a exatamente uma destas categorias:

| Categoria    | Caminho                 | O que vai lá                                         |
| ------------ | ----------------------- | ---------------------------------------------------- |
| **Conceito** | `docs/concepts/<slug>/` | Padrão de arquitetura, princípio de design ou conceito técnico. |
| **Ferramenta** | `docs/tools/<slug>/` | Documentação de ferramenta de desenvolvedor (instalação, uso, recursos). |
| **Análise**  | `docs/analyses/<slug>/` | Estudo arquitetural de uma plataforma, framework ou biblioteca. |
| **Projeto**  | `projects/<slug>/`      | Projeto open source real e executável com guia de configuração. |
| **Guia**     | `docs/guides/`          | Tutorial ou how-to longo e orientado a tópicos.      |
| **Relatório**| `reports/YYYY/MM/`      | Registro de execução com data, imutável após o commit. |
| **Memória**  | `memory/`               | Contexto do agente: missão, regras, decisões, conhecimento, estado, qualidade. |

A separação é semântica, não cosmética:

- **Conceitos vs Guias** — uma página de conceito explica um padrão, princípio ou técnica (ex.: microsserviços, CQRS, OAuth). Um guia é um passo a passo narrativo que pode abranger vários conceitos ou ferramentas.
- **Ferramentas vs Análises** — uma página de ferramenta ensina *como usar* algo (instalar → configurar → executar). Uma análise estuda *arquitetura e trade-offs* (comparar alternativas, avaliar decisões de design).
- **Guias vs Ferramentas** — um guia é um passo a passo narrativo por várias ferramentas ou conceitos. Uma página de ferramenta é um cartão de referência único.
- **Relatórios como registros** — relatórios são imutáveis após o commit. Eles são organizados por `YYYY/MM/` para evitar inchaço de diretório plano e permitir navegação cronológica.
- **Memória como contrato do agente** — cada arquivo em `memory/` tem uma função distinta (declarada em `memory/knowledge.md`). O agente lê todos eles na inicialização; `state.md` também é escrito após cada execução.

## Contrato de frontmatter

Toda página no site deve ter:

```yaml
---
title: Human-readable title
description: One-sentence summary.
created: YYYY-MM-DD
tags: [tag1, tag2]
status: draft | stable | archived | deprecated
---
```

`title` e `description` são usados na navegação e pesquisa. `created` alimenta o cartão de metadados; `git-revision-date-localized` preenche a data da "última atualização" automaticamente. `tags` permite a navegação baseada em tags. `status` sinaliza a maturidade da página.

## Segredos e segurança

| Segredo              | Propósito                                            | Fonte                 |
| -------------------- | ---------------------------------------------------- | --------------------- |
| `GITHUB_TOKEN`       | Acesso ao repositório dentro dos workflows.          | Integrado.            |

Nenhuma credencial é armazenada no repositório.

## Como evoluir a arquitetura

Qualquer alteração que afete como o site é construído, implantado ou automatizado deve:

1. Ser registrada como uma nova entrada em `memory/decisions.md` com o próximo número disponível.
2. Ser refletida nesta página se alterar o diagrama de alto nível.
3. Manter o contrato de repositório primeiro: nunca editar o site publicado diretamente.