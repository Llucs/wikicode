---
title: Ghostty - Um Emulador de Terminal Rápido e de Alto Nível de Recursos
description: O Ghostty é um emulador de terminal rápido, de alto nível de recursos e cross-platform que usa interfaces gráficas nativas e aceleração de GPU. Foi projetado para ser uma substituição ideal para seu emulador de terminal atual em macOS e Linux. O Ghostty foi desenvolvido por Mitchell Hashimoto, um dos cofundadores da HashiCorp, e visa ser a nova referência em desempenho em 2026.
created: 2026-07-03
tags:
  - terminal
  - emulador
  - produtividade
  - linha de comando
  - cross-platform
status: rascunho
---

# Ghostty - Um Emulador de Terminal Rápido e de Alto Nível de Recursos

O Ghostty é um emulador de terminal rápido, de alto nível de recursos e cross-platform que usa interfaces gráficas nativas e aceleração de GPU. Foi projetado para ser a melhor substituição drop-in para seu emulador de terminal atual em macOS e Linux. O Ghostty foi desenvolvido por Mitchell Hashimoto, um dos cofundadores da HashiCorp, e visa ser a nova referência em desempenho em 2026.

## O que é o Ghostty?

O Ghostty não é uma ferramenta para gerar projetos ou estruturar aplicações, mas sim um emulador de terminal que oferece uma interface de usuário moderna e eficiente. Ele oferece uma experiência rápida e responsiva, com aceleração de GPU e interface gráfica nativa, tornando-o uma escolha superior para desenvolvedores que buscam aumentar sua produtividade em um ambiente de terminal.

## Recursos Principais

- **Interface Gráfica Nativa**: Oferece uma interface de usuário moderna e intuitiva.
- **Aceleração de GPU**: Aumenta o desempenho e a responsividade.
- **Suporte Cross-Platform**: Funciona em macOS, Linux e Windows de forma transparente.
- **Rápido**: Oferece desempenho acelerado, mesmo com comandos complexos e operações com arquivos grandes.
- **De Alto Nível de Recursos**: Inclui recursos avançados como terminais em abas, múltiplos painéis e muito mais.

## História

O Ghostty foi criado pela equipe do projeto Ghost, cujo objetivo é simplificar o processo de construção de sistemas de gerenciamento de conteúdo e aplicações web. Mitchell Hashimoto, ex-CEO e CTO da HashiCorp, é o desenvolvedor principal do Ghostty e está dedicado a melhorar a experiência de emulador de terminal.

## Casos de Uso

O Ghostty é usado principalmente em um ambiente de terminal para interagir com ferramentas da linha de comando, gerenciar processos e executar scripts. É particularmente útil para desenvolvedores e administradores de sistemas que precisam de um emulador de terminal rápido e eficiente.

## Instalação

Para instalar o Ghostty, siga estas etapas:

1. **Instalar Node.js**: Certifique-se de ter o Node.js instalado em seu sistema. O Ghostty é construído usando Node.js.
2. **Instalar o Ghostty**: Abra seu terminal e execute o seguinte comando:

   ```sh
   npm install -g ghostty
   ```

   Alternativamente, você pode instalá-lo via Yarn:

   ```sh
   yarn global add ghostty
   ```

## Uso Básico

Uma vez instalado, você pode usar o Ghostty para interagir com seu terminal. Aqui estão alguns comandos básicos:

1. **Iniciar o Ghostty**: Abra o Ghostty executando o comando:

   ```sh
   ghostty
   ```

2. **Abrir um Novo Terminal**: Você pode abrir uma nova janela de terminal dentro do Ghostty:

   ```sh
   ghostty new-terminal
   ```

3. **Fechar o Terminal Atual**: Sair da janela de terminal atual:

   ```sh
   ghostty close-terminal
   ```

4. **Alternar entre Terminals**: Use a tecla de seta para alternar entre as janelas de terminal abertas:

   ```sh
   ghostty switch-terminal
   ```

5. **Abrir um Arquivo**: Abra um arquivo no terminal:

   ```sh
   ghostty open-file /caminho/para/arquivo.txt
   ```

6. **Executar um Comando no Terminal**: Execute um comando no terminal:

   ```sh
   ghostty run-command ls -l
   ```

7. **Fechar o Ghostty**: Sair do Ghostty pressionando `Ctrl + D` ou executando:

   ```sh
   ghostty exit
   ```

## Conclusão

O Ghostty é um emulador de terminal poderoso e eficiente que oferece uma interface de usuário moderna e responsiva. Foi projetado para aumentar sua produtividade em um ambiente de terminal e é uma escolha digna para desenvolvedores e administradores de sistemas que buscam um emulador de terminal rápido e de alto nível de recursos.

Para obter mais informações e explorar recursos adicionais, visite o [repositório GitHub oficial do Ghostty](https://github.com/mitchellh/ghostty).