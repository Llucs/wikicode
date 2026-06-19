---
title: "Termux: Emulador de Terminal e Ambiente Linux para Android"
description: "Um guia abrangente sobre o Termux, o poderoso emulador de terminal de código aberto e ambiente Linux para dispositivos Android, cobrindo instalação, gerenciamento de pacotes, uso avançado e fluxos de trabalho de desenvolvimento."
created: 2026-06-19
tags:
  - android
  - terminal
  - linux
  - development
  - tools
status: draft
---

# Termux: Emulador de Terminal e Ambiente Linux para Android

## O que é o Termux?

O Termux é um **emulador de terminal de código aberto e ambiente Linux** para Android. Opera inteiramente no espaço do usuário, **sem exigir acesso root**, e fornece um rico repositório de pacotes derivado do Debian/Ubuntu. Com o Termux, você pode executar uma experiência completa de linha de comando Linux no seu dispositivo Android — instalar compiladores, interpretadores, editores de texto, ferramentas de rede e muito mais. Ele aproveita as chamadas de sistema Linux do kernel Android para criar um ambiente quase nativo.

### Por que usar o Termux?

- **Ambiente de Desenvolvimento Portátil** – Escreva e execute scripts Python, compile programas C, gerencie repositórios Git ou use um REPL diretamente no seu telefone.
- **Administração de Servidores em Movimento** – Conecte-se via SSH a servidores remotos, verifique diagnósticos de rede (ping, traceroute, nmap) e sincronize arquivos com rsync.
- **Aprendizado e Educação** – Pratique comandos Linux, shell scripting e conceitos de rede sem precisar de um PC completo.
- **Automação e Integração** – Combine com aplicativos de automação Android (Tasker) ou use o Termux:API para interagir com o hardware do telefone (câmera, sensores, área de transferência).
- **Distribuições Linux Completas** – Instale Ubuntu, Debian, Arch ou Fedora dentro de um ambiente termux usando o proot-distro para quase qualquer tarefa Linux.

---

## Principais Recursos

| Recurso | Descrição |
|---------|-----------|
| **Emulador de Terminal** | Completo, com controles de gestos amigáveis ao toque, teclas de função extras (Tab, Ctrl, Alt, Esc) acessíveis deslizando para a esquerda a partir da linha de números. |
| **Gerenciador de Pacotes** | `pkg` (e o `apt` subjacente) com milhares de pacotes do repositório Termux. |
| **Gerenciamento de Múltiplas Sessões** | Deslize uma gaveta para gerenciar sessões de terminal separadas, cada uma logada independentemente. |
| **Cliente e Servidor SSH** | Conecte-se a servidores remotos com `ssh`, ou inicie um servidor (`sshd`) para acessar seu dispositivo a partir de um computador. |
| **Suporte a Distros Proot** | Execute distribuições Linux completas (Ubuntu, Debian, Arch, Fedora) usando `proot-distro`. |
| **Integração com API** | O aplicativo complementar *Termux:API* dá aos scripts acesso a sensores Android, área de transferência, TTS, câmera, notificações e muito mais. |
| **Acesso ao Armazenamento** | Monte o armazenamento compartilhado do Android (interno/SD) via `termux-setup-storage`. |

---

## Instalação

### 1. Obter o Termux

> **Importante**: A **versão da Google Play Store está obsoleta** (travada na API 28). Instale sempre a partir do **F-Droid** para pacotes atualizados e compatibilidade total com Android moderno (10+).

- **Cliente F-Droid**: Procure por "Termux" no aplicativo F-Droid ou baixe o APK diretamente do [F-Droid](https://f-droid.org/packages/com.termux/).
- **APK Direto**: [F-Droid APK](https://f-droid.org/repo/com.termux_*.apk) (sempre o mais recente).

### 2. Aplicativos Complementares (Opcionais, mas Recomendados)

| Aplicativo | Finalidade |
|------------|-----------|
| [Termux:API](https://f-droid.org/packages/com.termux.api/) | Acesse o hardware Android (sensores, câmera, área de transferência, etc.) a partir de scripts. |
| [Termux:Float](https://f-droid.org/packages/com.termux.float/) | Execute o Termux em uma janela flutuante (overlay). |
| [Termux:Styling](https://f-droid.org/packages/com.termux.styling/) | Esquemas de cores e fontes prontas para powerline para o terminal. |
| [Termux:Tasker](https://f-droid.org/packages/com.termux.tasker/) | Chame executáveis do Termux a partir do Tasker e aplicativos de automação compatíveis. |
| [Termux:Widget](https://f-droid.org/packages/com.termux.widget/) | Inicie pequenos scriptlets a partir da tela inicial. |

### 3. Configuração Inicial

Após iniciar o Termux pela primeira vez:

```bash
# Update the package repository and upgrade all packages
pkg update && pkg upgrade

# Grant storage access (needed to see your shared folders)
termux-setup-storage
```

Agora você tem um ambiente Termux totalmente atualizado. O armazenamento compartilhado do Android é montado em `~/storage/shared`.

---

## Gerenciamento de Pacotes

O Termux usa o comando **`pkg`** como um wrapper ao redor do **`apt`**. Todos os comandos são familiares aos usuários Debian/Ubuntu.

### Operações Comuns de Pacotes

```bash
# Search for a package
pkg search python

# Install packages
pkg install python git vim openssh curl wget

# Remove a package
pkg remove python2

# List installed packages
pkg list-installed

# Upgrade all packages
pkg upgrade
```

### Pacotes Disponíveis (amostragem)

| Categoria | Pacotes |
|-----------|---------|
| **Linguagens** | python, python3, nodejs, ruby, php, lua, golang, rust |
| **Compiladores/Ferramentas** | clang, make, gdb, cmake, gcc (via proot distro) |
| **Editores** | vim, emacs, nano, neovim |
| **Redes** | openssh, nmap, traceroute, netcat, rclone |
| **Bancos de Dados** | mariadb, sqlite, postgresql (requer proot) |
| **Utilitários** | git, curl, wget, rsync, htop, jq, ripgrep, fd |

> **Nota**: Por ser um ambiente de espaço do usuário, alguns pacotes de nível de sistema (por exemplo, dependências `systemd`, `glibc`) exigem uma distribuição Linux completa via `proot-distro`.

---

## Uso Avançado

### 1. SSH: Cliente e Servidor

**Cliente** – Conecte-se a máquinas remotas como no desktop:

```bash
pkg install openssh
ssh user@hostname
```

**Servidor** – Torne seu dispositivo Android acessível via SSH (porta padrão 8022):

```bash
sshd
# or start it in the foreground with -d
sshd -d
```

Conecte-se de outra máquina:

```sh
ssh user@phone-ip -p 8022
```

> Na primeira vez que você executar `sshd`, o Termux gerará chaves de host e você poderá definir uma senha para o usuário termux (o usuário padrão é `u0_aXYZ`). Use `passwd` para alterá-la.

### 2. Executando Distribuições Linux Completas com `proot-distro`

O Proot permite executar uma distribuição Linux padrão dentro do Termux sem root. O pacote `proot-distro` simplifica isso.

```bash
pkg install proot-distro

# List available distributions
proot-distro list

# Install Ubuntu (example)
proot-distro install ubuntu

# Login to the installed distribution
proot-distro login ubuntu

# Within the Ubuntu environment, you can use apt normally.
```

Agora você tem um ambiente Ubuntu completo (incluindo gerenciadores de serviços similares ao `systemd` via `proot`, embora nem todos os recursos funcionem perfeitamente). Você pode instalar pacotes como `gcc`, `postgresql` ou `firefox` (GUI precisa de servidor X) dentro dele.

### 3. Usando o Complemento Termux:API

Com o `Termux:API` instalado, você pode controlar recursos do Android a partir da linha de comando.

```bash
pkg install termux-api

# Get battery status
termux-battery-status

# Take a photo
termux-camera-photo output.jpg

# Get clipboard content
termux-clipboard-get

# Show a notification
termux-notification --title "Hello" --content "World"

# Check sensors
termux-sensor -s "Accelerometer" -n 5
```

### 4. Automação com Tasker

O Termux:Tasker permite executar scripts do Termux como ações do Tasker.

1. Instale o **Termux:Tasker** a partir do F-Droid.
2. No Tasker, adicione uma ação do tipo `System -> Send Intent`.
3. Ação: `com.termux.tasker.RUN_COMMAND`
4. Pares chave/valor extras: `command` = seu script ou comando (ex.: `termux-battery-status`).

Você também pode colocar scripts em `~/.termux/tasker/` e chamá-los pelo nome.

### 5. Gerenciamento de Sessão e Truques de Interface

- **Teclas Extras**: Deslize para a esquerda a partir da linha de números (no topo do teclado) para revelar uma linha com Tab, Ctrl, Alt, Esc, uma alternância de tecla Função e uma seta para cima (para rolar para cima). Você pode personalizá-las em `~/.termux/termux.properties`.
- **Múltiplas Sessões**: Toque no ícone da gaveta (três linhas horizontais) no lado esquerdo da tela para listar, alternar ou criar novas sessões de terminal.
- **Seleção de Texto**: Pressione longamente na área do terminal para entrar no modo de seleção; copiar/colar funciona com o menu de opções.

---

## Casos de Uso

- **Codificação Móvel** – Escreva e teste scripts Python, aplicativos Node.js ou programas C com vim e gcc. Use git para controle de versão.
- **Operações de Servidor** – Conecte-se via SSH a servidores de produção, execute varreduras `tcpdump` ou `nmap`, monitore logs e transfira arquivos com `rsync`.
- **Análise de Dados** – Instale Python com pandas, numpy, scipy e Jupyter (via `pkg install jupyter`) para processamento de dados em qualquer lugar.
- **Aprendendo Linux** – Experimente o sistema de arquivos, shell scripting e redes sem um PC separado.
- **Calculadora de Bolso** – Use Python como calculadora interativa: `python -c 'print(2**100)'` ou inicie um REPL.

---

## Solução de Problemas e Dicas

### A instalação de pacotes falha com "404 Not Found"

Os repositórios podem estar desatualizados. Execute `pkg update && pkg upgrade` primeiro. Se o problema persistir, verifique se você está usando a versão do F-Droid (não do Google Play).

### Acesso ao armazenamento negado

Execute `termux-setup-storage` e conceda a permissão quando solicitado. Se falhar no Android 11+, certifique-se de que o Termux tem a permissão 'Arquivos e mídia' ativada nas configurações do sistema.

### Problemas com dependências libc/glibc

Alguns pacotes esperam glibc, mas o Termux usa bionic (libc do Android). Use um proot-distro (Ubuntu, Debian) para esses pacotes.

### Como desabilitar o teclado em tela cheia no Android 10+

Adicione esta linha ao `~/.termux/termux.properties`:

```
fullscreen=false
```

Em seguida, recarregue com `termux-reload-settings`.

### Integração da área de transferência com o terminal

Use `termux-clipboard-get` e `termux-clipboard-set` do `termux-api` para interagir com a área de transferência do sistema.

---

## Comunidade e Recursos

- **Site Oficial**: [termux.com](https://termux.com) (redireciona para o GitHub)
- **Repositório no GitHub**: [termux/termux-app](https://github.com/termux/termux-app) (aplicativo principal)
- **Repositório de Pacotes**: [termux/termux-packages](https://github.com/termux/termux-packages)
- **Wiki**: [Termux Wiki](https://wiki.termux.com)
- **F-Droid**: [F-Droid Termux](https://f-droid.org/packages/com.termux/)
- **Reddit**: [r/termux](https://reddit.com/r/termux)

---

O Termux transforma seu dispositivo Android em uma estação de trabalho Linux portátil e poderosa. Com seu extenso repositório de pacotes, capacidades SSH e compatibilidade com fluxos de trabalho Linux padrão, é uma ferramenta indispensável para desenvolvedores, administradores de sistemas e qualquer pessoa que goste de manter a linha de comando no bolso.