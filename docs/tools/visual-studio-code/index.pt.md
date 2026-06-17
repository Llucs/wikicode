---
title: Visual Studio Code
description: Um editor de código fonte leve, mas poderoso, desenvolvido pela Microsoft, que funciona como uma ferramenta de desenvolvimento integrada.
created: 2026-06-14
tags:
  - editor
  - development
  - microsoft
  - open-source
status: draft
ecosystem: editors
---

# Visual Studio Code

## O que é o VS Code?

Visual Studio Code (comumente chamado de VS Code) é um editor de código fonte gratuito e de código aberto desenvolvido pela Microsoft. Construído sobre o framework Electron, ele é executado no Windows, macOS e Linux. O VS Code combina a velocidade e simplicidade de um editor leve com as capacidades avançadas de um ambiente de desenvolvimento integrado (IDE) através de uma rica arquitetura de extensões.

## Por que VS Code?

- **Desempenho**: Inicia rapidamente e permanece responsivo mesmo com projetos grandes.
- **Extensibilidade**: Milhares de extensões adicionam linguagens, temas, depuradores e ferramentas de fluxo de trabalho.
- **Multiplataforma**: Mesma experiência em todos os principais sistemas operacionais.
- **Ferramentas Integradas**: Controle Git, terminal, depuração – tudo dentro do editor.
- **Edição Inteligente**: O IntelliSense fornece conclusões sensíveis ao contexto, informações de parâmetros e documentação.
- **Suporte Integrado para Fluxos de Trabalho Modernos**: Docker, desenvolvimento remoto, Jupyter notebooks e mais.

## Instalação

### Baixar o Instalador

A maneira mais fácil é baixar o instalador do [site oficial](https://code.visualstudio.com).

| Plataforma | Tipo de Instalador |
|------------|-------------------|
| Windows    | `.exe` (usuário ou sistema) |
| macOS      | `.dmg` (arraste para Applications) |
| Linux      | `.deb` (Debian/Ubuntu) ou `.rpm` (Fedora/RHEL) |

### Gerenciadores de Pacotes

**macOS (Homebrew)**
```bash
brew install --cask visual-studio-code
```

**Linux (Snap)**
```bash
snap install code --classic
```

**Windows (winget)**
```bash
winget install Microsoft.VisualStudioCode
```

### Modo Portátil

Crie uma pasta `data` no mesmo diretório do executável do VS Code. O editor armazenará toda a configuração, extensões e dados do usuário nessa pasta, tornando-o totalmente portátil.

### Versão Insiders

Para acesso antecipado a funcionalidades e versões diárias, instale o [VS Code Insiders](https://code.visualstudio.com/insiders). Ele pode ser instalado lado a lado com a versão estável.

## Uso Básico

### Abrir um Projeto

Inicie o VS Code e use **Arquivo → Abrir Pasta** (ou `Ctrl+K Ctrl+O` / `Cmd+K Cmd+O`) para abrir o diretório do seu projeto.

### Paleta de Comandos

A paleta de comandos dá acesso a todas as ações no VS Code.

```text
Ctrl+Shift+P   (Windows/Linux)
Cmd+Shift+P    (macOS)
```

Comandos comuns: `>Format Document`, `>Preferences: Open Settings`, `>Extensions: Install Extensions`.

### Editar Arquivos

- O realce de sintaxe é automático com base na extensão do arquivo.
- **Multicursor**: `Alt+Click` (Windows/Linux) ou `Option+Click` (macOS) para adicionar cursores.
- **Correspondência de Colchetes**: Mova o cursor para dentro de colchetes e o par correspondente é destacado.
- **IntelliSense**: Acione manualmente com `Ctrl+Space`.

### Controle de Versão

Abra a exibição de Controle de Código Fonte (`Ctrl+Shift+G` no Windows/Linux, `Cmd+Shift+G` no macOS) para ver alterações, preparar arquivos, fazer commit e push/pull. Use o terminal integrado para operações mais complexas.

### Terminal Integrado

Inicie o terminal com `` Ctrl+` `` (crase). O terminal usa o shell do seu sistema (PowerShell, bash, zsh, etc.) por padrão.

### Extensões

Abra a exibição de Extensões com `Ctrl+Shift+X`. Pesquise qualquer extensão (ex.: “Python”, “Prettier”, “Docker”) e instale com um clique.

### Depuração

Defina pontos de interrupção clicando na margem (área do número da linha) ou pressionando `F9`. Pressione `F5` para iniciar a depuração com a configuração ativa. Crie um arquivo `launch.json` para configurar as definições de depuração para o seu projeto.

## Principais Recursos com Exemplos de Comandos

### IntelliSense

O VS Code fornece conclusões inteligentes baseadas em serviços de linguagem, tipos de variáveis e definições de funções.

```javascript
// Example: Typing "console." then using Ctrl+Space shows methods like log, warn, error
console.log("Hello, VS Code!");
```

**Acionar IntelliSense manualmente**: `Ctrl+Space` (Windows/Linux) ou `Cmd+Space` (macOS).

**Dicas de Parâmetros**: Ao chamar uma função, o VS Code mostra os parâmetros esperados.

### Depuração Integrada

Suporte completo à depuração com configurações de inicialização.

**Exemplo de launch.json para Node.js:**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "node",
            "request": "launch",
            "name": "Launch Program",
            "skipFiles": ["<node_internals>/**"],
            "program": "${workspaceFolder}/app.js"
        }
    ]
}
```

**Principais comandos de depuração:**
| Ação | Teclas |
|------|--------|
| Iniciar/Continuar | `F5` |
| Pular por cima | `F10` |
| Entrar | `F11` |
| Sair | `Shift+F11` |
| Alternar Ponto de Interrupção | `F9` |

### Git Integrado

Controle de versão visual com preparação (staging), confirmação (committing), ramificação (branching) e mais.

**Equivalente na Paleta de Comandos:**
- `>Git: Commit` – comita as alterações preparadas.
- `>Git: Create Branch` – cria uma nova ramificação.
- `>Git: Clone` – clona um repositório remoto.
- `>Git: Pull` / `Git: Push` – sincroniza alterações.

### Mercado de Extensões

Instale extensões para adicionar linguagens, linters, temas, snippets e depuradores.

**Exemplo: Instalar a extensão Python**
1. Abra a exibição de Extensões (`Ctrl+Shift+X`).
2. Pesquise por “Python” (da Microsoft).
3. Clique em **Instalar**.

**Extensões populares:**
- Python
- Prettier – Formatador de código
- ESLint
- Docker
- Live Server
- GitLens
- Jupyter

### Terminal Integrado

Execute comandos do shell sem sair do VS Code.

```bash
npm install && npm start
```

Abra/fecha o terminal com `` Ctrl+` ``. Vários terminais podem ser criados (ex.: um para build, um para git).

### Desenvolvimento Remoto

Conecte-se a ambientes remotos como:
- **WSL** (Subsistema Windows para Linux)
- Máquinas remotas **SSH**
- **Contêineres de Desenvolvimento** (Docker)
- **GitHub Codespaces**

**Exemplos na Paleta de Comandos:**
- `>Remote‑SSH: Connect to Host…`
- `>Dev Containers: Reopen in Container`

Não é necessário sair do editor—todo o seu ambiente de desenvolvimento é acessado localmente.

## Dicas Adicionais

### Sincronização de Configurações

Faça login com uma conta Microsoft ou GitHub e suas configurações, atalhos de teclado e extensões serão sincronizados entre máquinas.

**Paleta de Comandos**: `>Turn on Settings Sync…`

### Snippets

Crie snippets de código personalizados para padrões repetitivos.

**Arquivo → Preferências → Configurar Snippets de Usuário** → escolha uma linguagem.

```json
// Example JavaScript snippet (in javascript.json)
{
    "Arrow Function": {
        "prefix": "arr",
        "body": ["const ${1:name} = (${2:params}) => {", "\t${3:body}", "};"],
        "description": "Create an arrow function"
    }
}
```

### Edição com Multicursor

- `Alt+Click` – adicionar cursor.
- `Ctrl+Alt+Up/Down` – inserir cursor acima/abaixo.
- `Ctrl+D` – selecionar próxima ocorrência da seleção atual.

### Modo Zen

Foque no código sem distrações: `Ctrl+K Z` (Windows/Linux) ou `Cmd+K Z` (macOS). Alterne com `Esc Esc`.

## Conclusão

O Visual Studio Code é um editor versátil que equilibra velocidade, potência e personalização. Ao dominar seus recursos principais—IntelliSense, depuração, integração Git, terminal e ecossistema de extensões—você pode otimizar seu fluxo de trabalho de desenvolvimento em qualquer linguagem ou plataforma.

Para uma exploração mais aprofundada, consulte a [documentação oficial do VS Code](https://code.visualstudio.com/docs).