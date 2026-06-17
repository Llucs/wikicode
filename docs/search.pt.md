---
title: Pesquisar na wiki
description: Como pesquisar no WikiCode.
created: 2026-06-03
tags:
  - meta
  - reference
status: stable
---

# Pesquisar na wiki

O WikiCode é totalmente pesquisável. O índice de pesquisa é construído no momento do deploy e executado inteiramente no navegador, portanto as consultas são instantâneas e nenhum dado sai da sua máquina.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Criado: 2026-06-03</span>
<span class="wikicode-meta-updated">Última atualização: auto (git)</span>
</div>

## Como pesquisar

<div class="grid cards" markdown>

- :material-magnify: __Barra de pesquisa__

    Clique no ícone da lupa no canto superior direito de qualquer página
    (ou pressione ++slash++ no teclado) para abrir o modal de pesquisa.

- :material-keyboard: __Atalho de teclado__

    - ++slash++ — focar na barra de pesquisa.
    - ++esc++ — fechar o modal de pesquisa.
    - ++arrow-up++ / ++arrow-down++ — navegar pelos resultados.
    - ++enter++ — abrir o resultado destacado.

- :material-format-letter-case: __Dicas__

    - A pesquisa é **baseada em substrings**. Digitar `mkdocs` corresponde a qualquer
      página que contenha "mkdocs".
    - A pesquisa é **insensível a maiúsculas/minúsculas** por padrão.
    - Frases entre aspas correspondem a substrings exatas: `"open hands"`.
    - Várias palavras correspondem a páginas que contenham todas elas.

</div>

## O que é indexado

O índice de pesquisa cobre todas as páginas Markdown renderizadas no site:

- Artigos, guias e páginas de referência em `docs/`.
- Resumos de projetos em `projects/`.
- Descrições de trechos em `snippets/`.
- Páginas de ferramentas em `docs/tools/`.
- Postagens do blog em `blog/`.
- O texto dos blocos de código (para que você possa pesquisar um nome de função
  ou uma flag de CLI).

O índice é regenerado a cada push para `main`, portanto está sempre sincronizado com o conteúdo publicado.

## Por que client-side

- **Privacidade.** Nenhuma consulta é enviada para um serviço remoto.
- **Velocidade.** Os resultados aparecem enquanto você digita.
- **Custo.** Não há nada para hospedar além do site estático.
- **Offline.** Uma vez que o site carregue, o índice está no
  cache do navegador e continua funcionando sem rede.

## Adicionando um atalho de pesquisa personalizado

Se você quiser um link direto que abra o modal de pesquisa pré-preenchido, anexe `?q=<query>` à URL do site após a pesquisa ter sido focada uma vez. O comportamento exato depende da versão do tema Material; a maneira recomendada é usar o atalho de teclado (++slash++) e digitar a consulta.