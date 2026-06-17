---
title: npm - Gerenciador de Pacotes do Node
description: Um gerenciador de pacotes para Node.js que é uma ferramenta fundamental para gerenciar dependências JavaScript.
created: 2026-06-14
tags:
  - package-manager
  - javascript
  - nodejs
  - cli
  - dependency-management
status: draft
ecosystem: javascript
---

# npm – Gerenciador de Pacotes do Node

npm (Gerenciador de Pacotes do Node) é o gerenciador de pacotes padrão para o runtime Node.js. Ele consiste em dois componentes principais: uma **CLI** (interface de linha de comando) para gerenciar dependências e o **npm Registry**, um enorme banco de dados público de pacotes JavaScript. Tornou-se uma ferramenta essencial no ecossistema JavaScript, permitindo que desenvolvedores compartilhem, reutilizem e gerenciem código de forma eficiente.

## O que é npm?

npm fornece uma maneira de:

- **Instalar e gerenciar dependências** – rastrear pacotes no `package.json` e arquivos de lock.
- **Publicar pacotes** – compartilhar suas próprias bibliotecas com a comunidade ou sua organização.
- **Executar scripts** – automatizar fluxos de trabalho de build, teste e deploy.
- **Gerenciar monorepos** – usar workspaces para lidar com vários pacotes em um único repositório.

## Por que usar npm?

- **Padronização** – npm é fornecido junto com o Node.js, tornando-o a escolha padrão para a maioria dos projetos JavaScript.
- **Ecossistema enorme** – mais de 2 milhões de pacotes no registry, cobrindo praticamente todas as necessidades.
- **Reprodutibilidade** – o arquivo `package-lock.json` garante instalações determinísticas em diferentes ambientes.
- **Segurança** – `npm audit` ajuda a encontrar e corrigir vulnerabilidades na sua árvore de dependências.
- **Conveniência** – `npx` permite executar pacotes sem instalação global, e scripts simplificam tarefas comuns.

## Instalação

npm é instalado automaticamente com Node.js. Para obter a versão LTS mais recente:

1. Baixe o Node.js em [nodejs.org](https://nodejs.org/).
2. Verifique a instalação:

```bash
node -v
npm -v
```

### Instalar via gerenciador de versão (nvm/fnm)

Usar um gerenciador de versão permite alternar entre versões do Node.js e instalar npm para cada uma:

```bash
# Example with nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install --lts
```

Após a instalação, o npm está pronto para uso.

## Uso Básico

### Inicializar um projeto

Crie um novo projeto ou converta uma pasta existente:

```bash
npm init -y
```

Isso gera um arquivo `package.json` com valores padrão. Use `npm init` (sem `-y`) para um prompt interativo.

### Instalar dependências

```bash
# Production dependency
npm install lodash

# Dev-only dependency
npm install --save-dev jest

# Global package (use sparingly; prefer npx)
npm install -g nodemon

# Install all dependencies from package.json
npm install
```

### Instalar versões específicas

```bash
npm install react@18.2.0
npm install "express@>=4.17.0 <5.0.0"
```

### Executar scripts

Scripts são definidos na chave `"scripts"` do `package.json`. Atalhos comuns:

```bash
npm start        # runs the "start" script
npm test         # runs the "test" script
npm run build    # custom script, e.g., "build"
```

### Desinstalar pacotes

```bash
npm uninstall lodash
```

### Atualizar pacotes

```bash
npm update                # update all packages within version ranges
npm install lodash@latest # force a specific version update
```

### Verificar vulnerabilidades

```bash
npm audit
```

Para corrigir automaticamente (quando disponível):

```bash
npm audit fix
```

### Instalação limpa para CI

```bash
npm ci
```

`npm ci` é mais rápido e remove `node_modules` antes de instalar exatamente a partir do `package-lock.json`.

## Principais Recursos

### npx – Executar pacotes sem instalar

`npx` vem com o npm e permite executar binários do registry sem instalações globais:

```bash
npx create-react-app my-app
npx cowsay "Hello, npm!"
```

Se o pacote já estiver instalado localmente, `npx` usará essa versão.

### Workspaces (suporte a monorepos)

Os workspaces do npm permitem gerenciar vários pacotes em um único repositório:

```json
{
  "workspaces": [
    "packages/*"
  ]
}
```

Em seguida, execute comandos em todos os workspaces:

```bash
npm install              # installs dependencies for all workspaces
npm run test --workspaces
```

A vinculação entre pacotes do workspace é tratada automaticamente.

### Ganchos do ciclo de vida de scripts

O npm fornece ganchos pre/post para scripts comuns:

- `prepublish` / `postpublish`
- `preinstall` / `postinstall`
- `prebuild` / `postbuild`

Exemplo:

```json
{
  "scripts": {
    "prebuild": "rimraf dist",
    "build": "webpack --config webpack.prod.js"
  }
}
```

### package-lock.json

Este arquivo fixa a versão exata de cada dependência e suas dependências transitivas. Ele garante que todos que executam `npm install` obtenham a mesma árvore, tornando as builds reproduzíveis.

### Overrides e resoluções

Você pode forçar versões específicas de dependências transitivas no `package.json`:

```json
{
  "overrides": {
    "graceful-fs": "4.2.11"
  }
}
```

Isso é útil quando uma sub-dependência tem uma vulnerabilidade que você precisa corrigir sem esperar pelo lançamento de sua dependência pai.

### npm config

Personalize o comportamento do npm globalmente ou por projeto:

```bash
npm config set init-author-name "Your Name"
npm config get registry
npm config delete <key>
```

Você também pode usar um arquivo `.npmrc` na raiz do projeto.

### Pacotes globais vs. npx

Instalações globais devem ser reservadas para ferramentas que você usa em muitos projetos (por exemplo, `npm`, `yarn`, `node-gyp`). Para comandos pontuais, prefira `npx` para evitar poluir o namespace global e garantir que você sempre use a versão pretendida.

## Conclusão

npm é uma ferramenta poderosa e essencial para qualquer desenvolvedor JavaScript. Desde a instalação simples de dependências até o gerenciamento complexo de monorepos, seu rico conjunto de recursos ajuda a manter projetos organizados, seguros e reproduzíveis. Esteja você construindo uma pequena biblioteca ou uma grande aplicação, dominar o npm melhorará significativamente seu fluxo de trabalho.