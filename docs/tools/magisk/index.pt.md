---
title: Magisk - Root Systemless e Gerenciador de Módulos para Android
description: Magisk é uma ferramenta popular de rooting para Android que fornece acesso root systemless e suporte a módulos para modificações do sistema.
created: 2026-06-19
tags:
  - android
  - root
  - systemless
  - magisk
  - tool
status: draft
---

# Magisk – Root Systemless e Gerenciador de Módulos para Android

## O que é Magisk?

Magisk é um conjunto de software de código aberto criado por **John Wu (topjohnwu)** que permite **root systemless** e personalização profunda de dispositivos Android. Ao contrário dos métodos de root tradicionais que modificam a partição imutável `/system`, o Magisk funciona corrigindo a imagem de boot do dispositivo (ou partição `init_boot` em dispositivos mais novos) para criar um sistema de arquivos overlay na inicialização. Isso permite que acesso root, scripts de inicialização, patches de política SELinux e módulos sejam carregados **sem alterar permanentemente arquivos do sistema**.

Lançado originalmente em 2016, o Magisk rapidamente se tornou a solução padrão de root Android, substituindo ferramentas mais antigas como SuperSU. Ele continua sendo ativamente mantido e amplamente utilizado tanto para root básico quanto para modificações avançadas de dispositivos.

---

## Por que usar o Magisk?

| Benefício | Descrição |
|---------|-------------|
| **Modificações Systemless** | As atualizações OTA são preservadas porque `/system` permanece intacto. |
| **MagiskSU** | Gerenciamento de permissão root puramente de código aberto (conceder, perguntar, negar). |
| **Sistema de Módulos** | Instale ajustes (mods de áudio, bibliotecas de câmera, bloqueio de anúncios, fontes) sem reparticionar. |
| **Zygisk** | Injeção de código no processo de cada aplicativo via Zygote – substitui o MagiskHide. |
| **DenyList** | Oculta root, módulos e bootloader desbloqueado de aplicativos específicos (bancários, streaming). |
| **MagiskBoot** | Ferramenta poderosa para descompactar, modificar e recompactar imagens de boot do Android. |
| **Comunidade ativa** | Milhares de módulos e documentação extensa disponível. |

O Magisk é essencial para usuários que precisam de acesso root para ferramentas avançadas de backup, automação (Tasker), ajustes personalizados do sistema ou para reativar funcionalidades em aplicativos que bloqueiam dispositivos com root.

---

## Guia de Instalação

### Pré-requisitos

- **Bootloader desbloqueado** (específico do dispositivo, geralmente requer desbloqueio OEM).
- **ADB e Fastboot funcionando** no seu computador.
- **Imagem de fábrica do dispositivo** ou `boot.img` original (e possivelmente `init_boot.img`).
- **Faça backup** de todos os dados importantes.

### Passo 1 – Extrair a Imagem de Boot

Obtenha a imagem de fábrica do seu dispositivo (por exemplo, da página de imagens de fábrica do Google) e extraia a imagem de boot.

```bash
# Example for a Pixel device
unzip [device]_[build].zip
cd [device]_[build]
unzip image-[device]-[build].zip
# boot.img is now in the current directory
```

Para dispositivos rodando Android 13+ (por exemplo, série Pixel 6), a partição root é `init_boot.img` em vez de `boot.img`.

### Passo 2 – Corrigir a Imagem com o App Magisk

1. Instale o APK mais recente do Magisk no seu dispositivo.
2. Abra o app Magisk, toque em **Instalar** → **Selecionar e Corrigir um Arquivo**.
3. Escolha o `boot.img` extraído (ou `init_boot.img`).
4. O app corrigirá a imagem e salvará um novo arquivo chamado `magisk_patched-XXXXX.img` (geralmente em `Download/`).

### Passo 3 – Flash da Imagem Corrigida

Transfira a imagem corrigida para o seu computador e então inicie o dispositivo no modo fastboot.

```bash
adb pull /storage/emulated/0/Download/magisk_patched-XXXXX.img .
adb reboot bootloader
# For most devices:
fastboot flash boot magisk_patched-XXXXX.img
# For Pixel 6+ (init_boot partition):
fastboot flash init_boot magisk_patched-XXXXX.img
# Reboot:
fastboot reboot
```

### Passo 4 – Verificar Instalação

Após a reinicialização, abra o app Magisk. A tela **Início** deve exibir a versão do Magisk instalada e “Instalado” ao lado do status do Magisk.

---

## Uso Básico

### Interface do App Magisk

- **Guia Superusuário** (ícone de escudo): Lista todos os aplicativos que solicitaram permissões root. Toque em uma entrada para alterar seu status de permissão (Conceder / Perguntar / Negar).
- **Guia Módulos** (ícone de peça de quebra-cabeça): Mostra os módulos instalados. Toque no botão **+** para instalar um novo módulo a partir de um arquivo `.zip` armazenado no seu dispositivo. Use o interruptor para ativar/desativar um módulo (a maioria requer uma reinicialização).
- **Guia Configurações** (ícone de engrenagem):
  - **Zygisk**: Ativar ou desativar o Zygisk (requer reinicialização).
  - **DenyList**: Configure de quais aplicativos o Magisk deve se ocultar (requer Zygisk e reinicialização).
  - **Canal de Atualização**: Escolha Stable, Beta ou Canary para atualizações do app e do Magisk.
  - **Resposta Automática**: Defina o comportamento padrão da permissão root.

### Gerenciamento de Módulos

Os módulos são instalados como arquivos ZIP padrão. Eles podem conter scripts simples, arquivos binários ou diretórios completos de sobreposição do sistema.

```bash
# Typical module ZIP structure (inside /data/adb/modules/<module_id>/)
module.prop          # Metadata (id, name, version, author)
system/              # Files to overlay on /system
post-fs-data.sh      # Script run early in boot
service.sh           # Script run later in boot
```

Para instalar um módulo manualmente:

1. Baixe o arquivo `.zip` do módulo para o seu dispositivo.
2. Abra o app Magisk → Guia Módulos → **Instalar do armazenamento**.
3. Selecione o arquivo, confirme e então **Reinicie** quando solicitado.

### Desinstalando o Magisk

O app Magisk fornece uma maneira direta de remover completamente o root:

1. Abra o app Magisk.
2. Toque em **Desinstalar Magisk** na parte inferior da tela Início.
3. Confirme – o app restaurará a imagem de boot original e não corrigida e reiniciará.

---

## Principais Recursos

### MagiskSU

Um substituto completo para `su` que é totalmente de código aberto. Ele implementa um modelo de permissão com opções Conceder / Perguntar / Negar e registra todos os acessos root. O MagiskSU é compatível com todos os aplicativos existentes que requerem root.

### Magisk Modules

Um formato padronizado para distribuir modificações no sistema sem tocar na partição do sistema. Os módulos são carregados na inicialização usando o sistema de arquivos de sobreposição do Magisk. Milhares de módulos existem em fóruns como XDA e no repositório do Magisk.

### Zygisk

Zygisk é a implementação do Magisk de injeção de código no processo Zygote. Ele permite modificações em tempo de execução dentro do processo de qualquer aplicativo. O Zygisk substitui a funcionalidade mais antiga do MagiskHide.

### DenyList

Quando o Zygisk está ativado, você pode configurar uma **DenyList** de aplicativos onde o Magisk oculta sua presença (root, módulos, bootloader desbloqueado). Esta é a maneira moderna de contornar as verificações de integridade usadas por aplicativos bancários, de pagamento e streaming.

### MagiskBoot

MagiskBoot é uma ferramenta de baixo nível para trabalhar com imagens de boot. Ela pode descompactá-las, modificá-las e recompactá-las sem precisar de um ambiente Android completo. É frequentemente usado diretamente em um computador para criar imagens corrigidas sem o app.

---

## Exemplos de Comandos

### Flash da imagem de boot corrigida (fastboot)

```bash
fastboot flash boot magisk_patched-27000.img
fastboot reboot
```

### Flash init_boot para dispositivos mais novos

```bash
fastboot flash init_boot magisk_patched-27000.img
fastboot reboot
```

### Usar MagiskBoot para descompactar uma imagem de boot

```bash
magiskboot unpack boot.img
# This creates: kernel, kernel_dtb, ramdisk.cpio, header, etc.
```

### Recompactar uma imagem de boot modificada com MagiskBoot

```bash
magiskboot repack boot.img
# Creates new-boot.img with your modifications.
```

### Verificar cabeçalho da imagem de boot

```bash
magiskboot info boot.img
```

### Corrigir uma imagem de boot com Magisk (linha de comando)

Se você tiver o executável do Magisk no seu computador, pode corrigir diretamente:

```bash
magiskboot boot.img
# Creates patched_boot.img in the current directory.
```

### Ocultar o Magisk de um aplicativo (DenyList)

Abra o app Magisk → Configurações → **Configurar DenyList** → adicione o aplicativo alvo (por exemplo, `com.google.android.gms` para Google Play Services). Após uma reinicialização, o Magisk ficará invisível para esse aplicativo.

---

## Dicas e Considerações

- **Atualizações OTA** permanecem compatíveis porque o Magisk só modifica a partição de boot. No entanto, após uma OTA você deve **re-flash o Magisk** para a nova imagem de boot.
- **SafetyNet / Play Integrity** – Embora o Magisk em si não forneça bypass de integridade, ferramentas como módulos Zygisk-Assistant ou Shamiko podem ajudar a ocultar o root das verificações de atestado do Google.
- **Conflitos de módulos** – Alguns módulos podem interferir entre si; desative-os um por um para isolar problemas.
- **Backups** – Sempre mantenha uma cópia da imagem de boot original. Se algo der errado, você pode restaurá-la via fastboot.
- **Magisk Canary** – O canal de última hora às vezes inclui recursos instáveis. Use-o apenas para testes.

---

## Referências

- [Repositório do Magisk no GitHub](https://github.com/topjohnwu/Magisk)
- [Documentação oficial do Magisk (guias para desenvolvedores)](https://topjohnwu.github.io/Magisk/)
- [Repositório de módulos Magisk (não oficial)](https://www.androidacy.com/modules-repository/)
- [XDA Developers – Magisk Discussion & Support](https://forum.xda-developers.com/f/magisk.5903/)

---

*Este documento faz parte do wiki do desenvolvedor. Comentários e melhorias são bem-vindos.*