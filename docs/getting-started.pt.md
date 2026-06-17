---
title: Primeiros passos
description: Layout do repositório, compilação local e convenções de contribuição.
created: 2026-06-03
---

# Primeiros passos

Tudo o que você precisa para ler, construir e contribuir com o WikiCode.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Criado: 2026-06-03</span>
<span class="wikicode-meta-updated">Última atualização: automático (git)</span>
</div>

## 1. Layout do repositório

```
.
├── README.md            # Visão geral do projeto
├── LICENSE              # Licença MIT
├── AGENT.md             # Contrato de operação para agentes
├── mkdocs.yml           # Configuração do site estático
├── .gitignore
├── .github/
│   └── workflows/
│       ├── pages.yml    # Constrói e faz deploy do site ao fazer push na main
│       └── wikicode-agent.yml# Fluxo de trabalho do agente autônomo
├── docs/                # Conteúdo do site (artigos, guias)
│   ├── assets/css/      # Estilização personalizada
│   ├── index.md
│   └── getting-started.md
├── projects/            # Projetos de desenvolvedor autocontidos
├── snippets/            # Trechos de código reutilizáveis
├── memory/              # Memória de longo prazo do agente
│   ├── mission.md
│   ├── rules.md
│   ├── knowledge.md
│   └── decisions.md
├── tasks/               # Pipeline de trabalho
│   ├── queue.md
│   └── completed.md
└── reports/             # Relatórios de execução com carimbo de data/hora
```

## 2. O loop "a wiki cresce a partir do repositório"

WikiCode é um site **repository-first**. Nada em `site/` (a saída publicada) é editado manualmente.

1. Uma alteração é feita no repositório (um novo artigo, projeto, trecho, relatório, decisão, etc.).
2. A alteração é commitada e enviada para `main`.
3. `.github/workflows/pages.yml` é executado automaticamente no push.
4. MkDocs lê `docs/`, `projects/`, `snippets/` e reconstrói o site completo.
5. GitHub Pages serve a nova compilação.

O agente de IA local (ou qualquer contribuidor) se conecta a este loop escrevendo no repositório. O site então captura a alteração sem intervenção manual.

## 3. Executar o site localmente

Você precisa de Python 3.10+.

```bash
pip install mkdocs mkdocs-material \
            mkdocs-awesome-pages-plugin \
            mkdocs-git-revision-date-localized-plugin
mkdocs serve
```

O site estará disponível em `http://127.0.0.1:8000`. Edições em qualquer arquivo Markdown em `docs/`, `projects/` ou `snippets/` disparam uma recarga instantânea.

## 4. Construir o site estático

```bash
mkdocs build --clean
```

A saída é escrita em `site/`. O CI usa o mesmo comando.

## 5. Adicionar conteúdo

| Você quer adicionar… | Coloque em…                              | Arquivos necessários                  |
| -------------------- | ---------------------------------------- | ------------------------------------- |
| Um artigo            | `docs/<tópico>/<slug>.md` ou `docs/`      | o próprio arquivo `.md`               |
| Um projeto           | `projects/<slug>/`                       | `README.md` + `index.md` + código-fonte |
| Um trecho de código  | `snippets/<slug>/`                       | o arquivo de código + `index.md`      |
| Uma decisão          | `memory/decisions.md`                    | anexe uma nova entrada                |
| Uma tarefa           | `tasks/queue.md`                         | anexe uma nova entrada com caixa de seleção |
| Um relatório         | `reports/YYYY-MM-DD-<slug>.md`           | o arquivo + atualização do índice     |

Seções que não fazem parte de `docs/` (projects, snippets) são capturadas automaticamente pelo plugin `awesome-pages` do MkDocs através de seus arquivos `index.md`.

## 6. Frontmatter

Cada página do site tem pelo menos:

```yaml
---
title: Título da página
description: Breve descrição.
created: AAAA-MM-DD
---
```

A data `created` é definida quando a página é adicionada pela primeira vez. A data de **última atualização** é obtida automaticamente do histórico git do arquivo, portanto está sempre precisa sem edições manuais.

## 7. Trabalhando autonomamente

Agentes devem seguir `AGENT.md`. A versão resumida:

1. Leia `memory/mission.md` e `memory/rules.md`.
2. Escolha a próxima tarefa de `tasks/queue.md`.
3. Faça exatamente uma alteração significativa no repositório.
4. Escreva um relatório em `reports/`.
5. Mova a tarefa para `tasks/completed.md`.
6. Faça commit e push. O site será reconstruído automaticamente.

## 8. Pesquisa

WikiCode é totalmente pesquisável. O índice de pesquisa é construído na hora do deploy e roda inteiramente no navegador.

- Pressione ++slash++ em qualquer página para focar a barra de pesquisa.
- O índice cobre todas as páginas do site, incluindo blocos de código e posts do blog.
- Veja [Pesquisa](search.md) para detalhes completos e dicas.

## 9. Como o agente é acionado

O workflow wikicode-agent suporta **gatilhos automáticos e manuais**:

| Gatilho              | Quando                                               | Caso de uso                                   |
| -------------------- | ---------------------------------------------------- | --------------------------------------------- |
| `schedule`           | Diariamente às 12:00 UTC.                             | Execução padrão de "crescer um pouco todos os dias". |
| `workflow_dispatch`  | Manualmente a partir da aba Actions.                 | Execução sob demanda, útil para desbloqueios. |
| `issue_comment`      | Quando alguém escreve `@agent` em uma issue.          | Transformar uma issue em uma contribuição.    |
| `issues` com label   | Quando uma issue é etiquetada com `agent`.           | Execuções em lote selecionadas pelo operador. |

Apenas **uma** tarefa é executada por execução. A IA usa a API OpenCode para geração de conteúdo — nenhuma chave de API externa é necessária.

## 10. Convenções

- Nomes de arquivos Markdown: minúsculos, com hífen.
- Cada pasta de projeto, trecho e ferramenta expõe um `index.md` para navegação.
- Decisões sobre arquitetura, ferramentas ou fluxo de trabalho são registradas em `memory/decisions.md`.
- Nenhuma credencial, token ou dado privado é jamais commitado.
- O agente de IA local usa `secrets.GITHUB_TOKEN` (integrado) para commit e push. Nenhuma chave de API externa é necessária.