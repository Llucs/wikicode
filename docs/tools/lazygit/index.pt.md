---
title: Lazygit – A Interface de Terminal para Git que Aumenta Sua Produtividade
description: Um guia completo do lazygit, uma interface de usuário Git baseada em terminal que simplifica operações complexas do Git como staging, rebasing e conflict resolution através de uma interface intuitiva e orientada por teclado.
created: 2026-06-20
tags:
  - git
  - tui
  - productivity
  - terminal
status: draft
---

# Lazygit – A Interface de Terminal para Git que Aumenta Sua Produtividade

**Lazygit** é uma Interface de Usuário de Terminal (TUI) multiplataforma e orientada por teclado para o Git. Criado por Jesse Duffield em 2018 e escrito em Go, ele encapsula as operações mais complexas—e muitas vezes propensas a erros—do Git em um layout intuitivo baseado em painéis que vive inteiramente dentro do seu terminal.

> "Pare de memorizar comandos Git. Comece a usar Git intuitivamente."

---

## Por que Lazygit?

A interface de linha de comando do Git é poderosa, mas notoriamente implacável. Interactive rebasing, staging hunks, resolving conflicts e managing branches exigem sequências precisas de comandos. O Lazygit resolve isso ao:

- **Visualizando Seu Repositório** – Veja branches, tags, o grafo de commits, a árvore de trabalho e a stash de relance.
- **Acelerando o Trabalho Diário** – Stage, commit, push e pull sem digitar um único comando `git`.
- **Reduzindo Erros** – Interactive rebasing, cherry-picking e conflict resolution tornam-se orientados por menu e desfazíveis.
- **Reduzindo a Curva de Aprendizado** – Novos membros da equipe podem realizar operações avançadas do Git imediatamente, liberando-os de memorizar sintaxe arcana.
- **Funcionando Multiplataforma** – Executa em Linux, macOS e Windows com a mesma interface e keybindings.

---

## Instalação

O Lazygit está disponível através da maioria dos gerenciadores de pacotes. Escolha sua plataforma:

```bash
# macOS (Homebrew)
brew install lazygit

# Ubuntu / Debian
sudo add-apt-repository ppa:lazygit-team/release
sudo apt update
sudo apt install lazygit

# Arch Linux
pacman -S lazygit

# Windows
winget install lazygit
# or
scoop install lazygit

# Go (requires Go 1.16+)
go install github.com/jesseduffield/lazygit@latest

# Binary downloads (all platforms)
# https://github.com/jesseduffield/lazygit/releases
```

---

## Uso Básico

Navegue até qualquer repositório Git e inicie:

```bash
cd my-project
lazygit
```

O Lazygit abre com um layout de painéis divididos. A coluna esquerda mostra (de cima para baixo) os painéis **Status**, **Files**, **Branches**, **Commits** e **Stash**. O lado direito exibe o diff ou log do item selecionado.

### Navegação entre Painéis

| Tecla | Ação |
|-------|------|
| `←` / `→` | Mover entre painéis |
| `Tab` | Avançar pelos painéis |
| `Shift + Tab` | Retroceder pelos painéis |
| `j` / `k` | Mover para cima/baixo dentro de um painel |
| `J` / `K` | Rolar o painel de diff principal |
| `?` | Mostrar/esconder ajuda completa de atalhos |

### Início Rápido (Fluxo de Trabalho Diário)

1. **Iniciar** – Execute `lazygit` dentro de um repositório.
2. **Stage um arquivo** – Pressione `Space` em um arquivo no painel Files.
3. **Stage de um hunk específico** – Pressione `Enter` para ver o diff, depois `Space` em hunks individuais.
4. **Commit** – Pressione `c`, digite uma mensagem e pressione `Enter`.
5. **Push** – Pressione `P` (maiúsculo) para fazer push.
6. **Pull** – Pressione `p` (minúsculo) para fazer pull.
7. **Sair** – Pressione `q` para sair.

---

## Principais Funcionalidades (com Exemplos de Comandos)

### 🎯 Interactive Staging (Melhor que `git add -p`)

Veja o diff de um arquivo e então faça stage/unstage de linhas ou hunks individualmente visualmente. Chega de contar posições do cursor.

```bash
# Inside the Files panel:
# Enter  → open the file diff
# Space  → stage the selected hunk
# a      → stage all changes
# Enter on a specific hunk → stage individual lines
```

### 🔁 Interactive Rebase (A Funcionalidade Matadora)

Reordene, squash, fixup, edite ou remova commits com teclas únicas.

```bash
# Switch to the Commits panel (press 4):
# i       → start interactive rebase
# s       → squash commit into previous
# f       → fixup (squash, discard message)
# d       → drop commit entirely
# e       → edit commit (pause rebase)
# r       → reword commit message
# Ctrl+j  → move commit down in order
# Ctrl+k  → move commit up in order
```

Após marcar, pressione `Enter` para confirmar. O Lazygit executa o rebase e mostra o progresso. Se ocorrerem conflitos, ele salta para o painel de resolução de conflitos.

### ↩️ Undo / Redo (Rede de Segurança)

O Lazygit rastreia seu próprio histórico interno de ações. Cometeu um erro durante um rebase ou acidentalmente removeu um commit? Desfaça.

```bash
# z  → undo last action
# Z (Shift+z)  → redo
```

### 🌳 Branch Management

Troque, faça merge, rebase, renomeie e exclua branches sem sair da UI.

```bash
# Press 3 to enter the Branches panel:
# Space    → checkout selected branch
# n        → create a new branch (optionally from current HEAD)
# m        → merge selected branch into current
# r        → rebase current branch onto selected
# R        → rename branch
# d        → delete branch (with confirmation)
# Ctrl+r   → update remote branch references
```

### 🍒 Cherry-Pick Commits

Copie commits de uma branch para outra sem `git log` ou caça ao hash de commit.

```bash
# In the Commits panel:
# c        → start cherry-pick mode
# Space    → toggle selection of a commit
# Shift+c  → complete cherry-pick
```

### 🧩 Stash Management

Nomeie stashes, aplique-os, remova-os e até crie branches a partir de stashes.

```bash
# Press 5 to enter the Stash panel:
# g        → toggle stash view
# s        → stash staged changes
# Shift+s  → stash all changes (including untracked files)
# Space    → apply selected stash
# d        → drop stash
# n        → name a new stash
# b        → create branch from stash
```

### ⚔️ Conflict Resolution

Quando um rebase ou merge produz conflitos, o Lazygit mostra um diff de três vias com marcadores de conflito inline. Resolva-os visualmente.

```bash
# Conflict panel will open automatically:
# Ctrl+o → open file in external merge tool
# Space  → stage resolved file
# Enter  → edit file manually
# /      → search for remaining conflict markers
```

### 🌳 Worktree Support

O Lazygit tem suporte de primeira classe para worktrees do Git, permitindo adicionar, remover e alternar entre eles.

```bash
# In the Branches panel (or dedicated Worktrees panel):
# w        → open worktree management
# a        → add a new worktree
# d        → remove a worktree
# Space    → switch to a worktree
```

### 🧹 Custom Commands

Estenda o Lazygit com seus próprios comandos shell ou scripts que aparecem na UI.

```bash
# In ~/.config/lazygit/config.yml:
customCommands:
  - key: "C"
    command: "git cz"
    description: "Commit with Commitizen"
    context: "files"
    loadingText: "Opening commitizen..."
```

---

## Dicas Profissionais

1. **Atalhos de teclado adjacentes ao Vim** – `j/k` para navegar, `J/K` para rolar diffs, `/` para pesquisar dentro dos painéis.
2. **Filtrar arquivos** – Digite `/` no painel Files para filtrar por nome de arquivo.
3. **Diff contra um commit específico** – No painel Commits, pressione `d` em um commit para ver o que mudou naquele commit.
4. **Alternar visibilidade do diff** – Pressione `Ctrl+d` para percorrer os modos de exibição de diff.
5. **Use com sua configuração Git existente** – O Lazygit respeita seus aliases, difftool e configurações de merge tool.

---

## Configuração

O Lazygit é altamente configurável. Um arquivo de configuração completo está em:

- **Linux/macOS:** `~/.config/lazygit/config.yml`
- **Windows:** `%APPDATA%\lazygit\config.yml`

Gere um modelo com:

```bash
lazygit --print-config
```

Configurações comuns incluem substituições de keybindings, cores de tema, comandos personalizados e layout da UI.

---

## Quando Usar Lazygit

| Cenário | Por que o Lazygit Brilha |
|---------|--------------------------|
| Interactive rebasing | Seleção visual de commits e reordenação; desfazer disponível |
| Staging partial changes | Seleção linha por linha de hunks com diff instantâneo |
| Onboarding new devs | Sem necessidade de memorizar comandos Git complexos |
| Code review prep | Crie séries de commits limpas e lógicas em minutos |
| Conflict resolution | Visualizador de diff de três vias com ação inline |
| Repository overview | Veja branches, tags, remotes, stash e o grafo de commits de uma só vez |

---

## Recursos

- **GitHub:** [jesseduffield/lazygit](https://github.com/jesseduffield/lazygit)
- **Documentação:** [Lazygit Wiki](https://github.com/jesseduffield/lazygit/wiki)
- **Referência de Configuração:** [lazygit Configuration](https://github.com/jesseduffield/lazygit/blob/master/docs/Config.md)
- **Ecossistema "lazy" do autor:** Lazygit, Lazydocker, Lazynpm – todos seguindo a mesma filosofia TUI.

---

O Lazygit não substitui o Git; ele o torna acessível, visual e rápido. Seja você um usuário experiente de Git ou um desenvolvedor que só quer voltar a escrever código, o Lazygit vai economizar horas toda semana. Experimente por um dia—você nunca mais vai querer voltar ao simples `git rebase -i` novamente.