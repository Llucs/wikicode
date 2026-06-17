---
title: fzf - Localizador Fuzzy de Linha de Comando
description: Uma ferramenta de localização fuzzy para linha de comando que aprimora a busca de arquivos e texto no terminal.
created: 2026-06-15
tags:
  - command-line
  - fuzzy-finder
  - fzf
  - productivity
  - terminal
status: draft
ecosystem: cli
---

# fzf – Localizador Fuzzy de Linha de Comando de Propósito Geral

fzf é um **localizador fuzzy** interativo que traz o poder da pesquisa incremental para qualquer lista apresentada na linha de comando. Originalmente escrito em Ruby e posteriormente reescrito em Go por [Junegunn Choi](https://github.com/junegunn), tornou-se uma ferramenta essencial para desenvolvedores, administradores de sistemas e usuários avançados que desejam navegar por arquivos, comandos, processos e muito mais com rapidez instantânea.

Em vez de digitar nomes exatos ou depender apenas do preenchimento por tab, o fzf permite que você digite qualquer substring (ou até mesmo uma sequência fuzzy) e filtra instantaneamente a entrada. Ele funciona com qualquer dado enviado via stdin e retorna o item selecionado no stdout, sendo perfeito para pipelines Unix.

---

## Por que usar o fzf?

- **Velocidade**: Lida com centenas de milhares de entradas em tempo quase real.
- **Correspondência Fuzzy**: Encontre arquivos e comandos sem precisar lembrar nomes exatos.
- **Interatividade**: Filtragem ao vivo com feedback visual imediato.
- **Componibilidade**: Funciona com qualquer comando que produza ou consuma texto.
- **Personalização**: Temas, atalhos de teclado, janelas de visualização e mais.

---

## Instalação

### macOS
```bash
brew install fzf
# Install useful key bindings and fuzzy auto-completion
$(brew --prefix)/opt/fzf/install
```

### Linux (Debian/Ubuntu)
```bash
sudo apt install fzf           # Often outdated – prefer building from source
# Or from the official repository:
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

### Arch Linux
```bash
sudo pacman -S fzf
```

### Windows (WSL / Git Bash / Scoop)
```bash
scoop install fzf
# Or with Chocolatey
choco install fzf
```

### Go (qualquer plataforma)
```bash
go install github.com/junegunn/fzf@latest
```

---

## Uso Básico

### Enviar uma lista via pipe para o fzf
```bash
# Search through all files in the current directory
find . -type f | fzf
```

### Selecionar um arquivo e abri-lo em um editor
```bash
vim "$(find . -type f | fzf)"
```

### Visualizar conteúdo do arquivo
```bash
fzf --preview 'cat {}'       # {} is the path of the current item
```

### Layout reverso (busca na parte inferior)
```bash
fzf --reverse
```

### Seleção múltipla (com Tab)
```bash
fzf --multi
```

### Prompt personalizado
```bash
fzf --prompt="Pick a file> "
```

---

## Principais Recursos

### Modos de Correspondência Fuzzy
fzf oferece suporte a vários modos de correspondência para ajustar sua busca:

- **Fuzzy (padrão)**: `abc` corresponde a `alphabet.txt` – qualquer sequência de substring funciona.
- **Correspondência exata**: prefixo com `'` → `'abc` corresponde apenas a linhas contendo exatamente “abc”.
- **Correspondência de prefixo**: sufixo com `^` → `^abc` corresponde a linhas iniciadas com “abc”.
- **Correspondência de sufixo**: prefixo com `$` → `abc$` corresponde a linhas terminadas com “abc”.
- **Expressão regular**: prefixo `!` para inverter, ou usar integração com `rg`.

### Janela de Visualização
A janela de visualização mostra informações contextuais para o item destacado. Ela pode usar comandos externos como `cat`, `bat`, `head` ou até scripts personalizados:

```bash
fzf --preview 'bat --color=always --style=numbers {}'
```

### Integração com o Shell
O script `install` oficial configura três atalhos de teclado úteis (Bash, Zsh, Fish):

| Atalho | Ação |
|--------|------|
| `Ctrl+R` | Pesquisar histórico de comandos |
| `Ctrl+T` | Pesquisar arquivos/diretórios e colar seus caminhos |
| `Alt+C`  | Ir para um subdiretório (cd fuzzy) |

### Plugin para Vim / Neovim
o fzf fornece um plugin nativo para Vim. A extensão mais popular é [fzf.vim](https://github.com/junegunn/fzf.vim), que adiciona comandos como:

| Comando | Propósito |
|---------|-----------|
| `:Files [path]` | Pesquisar arquivos |
| `:Rg [pattern]` | Pesquisar conteúdo de arquivos (requer ripgrep) |
| `:Buffers` | Alternar entre buffers abertos |
| `:GFiles?` | Pesquisar arquivos não rastreados em um repositório Git |
| `:Commands` | Listar comandos do Vim |
| `:Maps` | Mostrar mapeamentos de teclado |

### Extensibilidade
Como o fzf opera em stdin/stdout, ele se integra perfeitamente a qualquer fluxo de trabalho. Você pode encapsulá-lo em funções do shell ou scripts para criar seus próprios menus interativos.

---

## Casos de Uso Avançados

### Matador de Processos
```bash
ps aux | fzf | awk '{print $2}' | xargs kill -9
```

### Checkout de um Branch do Git
```bash
git branch -a | fzf | tr -d ' *' | xargs git checkout
```

### SSH em Hosts a partir do Config
```bash
cat ~/.ssh/config | grep -i '^host ' | awk '{print $2}' | fzf | xargs ssh
```

### Pesquisar Conteúdo de Arquivos com Visualização
```bash
rg --line-number . | fzf --delimiter : \
    --preview 'bat --color=always --highlight-line {2} {1}'
```

### Alterar Diretório Interativamente (com fd)
```bash
cd "$(fd --type d | fzf)"
```
Ou use o atalho integrado `Alt+C`.

### Pesquisa de Contêineres Docker
```bash
docker ps | fzf | awk '{print $NF}'
```

---

## Dicas e Truques

- **Use a opção `--header`** para mostrar instruções:
  ```bash
  fzf --header "Press Ctrl-R for history, Ctrl-T for files"
  ```
- **Armazene itens selecionados em uma variável** para operações em lote.
- **Adicione uma visualização colorida** usando `bat` ou `highlight` com suporte a ANSI.
- **Combine com `tmux`** para abrir o painel de visualização em uma divisão separada.
- **Personalize o esquema de cores** através da variável de ambiente `FZF_DEFAULT_OPTS`:
  ```bash
  export FZF_DEFAULT_OPTS='--color=bg+:#383838,fg+:#f0f0f0'
  ```

---

## Conclusão

o fzf é uma ferramenta padrão ouro para pesquisa interativa no terminal. Sua correspondência fuzzy, velocidade e componibilidade o tornam indispensável para quem vive na linha de comando. Esteja você navegando por arquivos, procurando processos ou criando fluxos de trabalho personalizados, o fzf transforma tarefas tediosas de busca em uma experiência fluida e quase mágica.

Para documentação completa, visite o [repositório no GitHub](https://github.com/junegunn/fzf).