---
title: Projeto de Recuperação Team Win (TWRP)
description: O TWRP é uma recovery personalizada de código aberto para Android que permite a instalação de ROMs personalizadas, backups completos do dispositivo (NANDroid) e modificações do sistema através de uma interface touchscreen.
created: 2026-06-17
tags:
  - android
  - recovery
  - custom-rom
  - backup
  - twrp
status: draft
---

# Team Win Recovery Project (TWRP)

TWRP (Team Win Recovery Project) é uma **imagem de recovery personalizada de código aberto** para dispositivos Android. Ela substitui a partição de recovery original para oferecer um ambiente rico em funcionalidades, controlado por tela sensível ao toque, para instalar firmware de terceiros, criar backups completos do sistema e executar tarefas avançadas de gerenciamento — tudo sem precisar iniciar o Android.

## Por que usar o TWRP?

A recovery padrão do Android se limita a restaurações de fábrica e atualizações OTA. O TWRP expande as possibilidades do dispositivo para:

- **Instalação de ROMs personalizadas** (LineageOS, Pixel Experience, etc.)
- **Backups e restaurações completas do sistema** (NANDroid) — essenciais antes de modificações arriscadas.
- **Root** (instalação do Magisk ou SuperSU).
- **Gerenciamento de partições** (limpeza, formatação, redimensionamento).
- **Tratamento de criptografia** (descriptografia do userdata em certas condições).
- **Sideload via ADB e MTP** para transferir arquivos ou instalar sem usar o armazenamento.

O TWRP é o padrão de facto para entusiastas e desenvolvedores Android; ele substituiu recoveries anteriores como ClockworkMod (CWM) graças à sua interface intuitiva e ao suporte ativo da comunidade.

## Principais Funcionalidades

- **Interface Touch** – Suporte completo a toque com teclado na tela, gerenciador de arquivos e emulador de terminal.
- **Backup NANDroid** – Clona partições inteiras (Boot, System, Data, EFS/IMEI) para `/sdcard/TWRP/BACKUPS/`.
- **Instalação de ZIPs** – Instala pacotes de firmware personalizados (ROMs, kernels, mods, GApps, Magisk).
- **Limpeza Avançada** – Limpa partições individuais, “Format Data” para remover criptografia.
- **Gerenciador de Arquivos** – Navegue e modifique arquivos no sistema de arquivos do dispositivo.
- **Sideload via ADB** – Instale arquivos ZIP a partir de um computador via USB.
- **Suporte a MTP** – Acesse o armazenamento do dispositivo como uma unidade removível na recovery.
- **Suporte a Criptografia** – Pode descriptografar userdata com PIN/senha/padrão (criptografias antigas; FBE em dispositivos modernos geralmente não é suportado).
- **Temas** – Interface customizável através de temas `.twres`.
- **Captura de Tela** – Capture a tela enquanto estiver na recovery.

## História

Criado por *Dees_Troy* por volta de 2011, o TWRP rapidamente se tornou a recovery personalizada mais popular devido à sua interface touchscreen proprietária. Ele evoluiu de um tema Holo para uma interface Material Design (versão 3.0+). Hoje é mantido por uma equipe principal e suporta centenas de dispositivos listados oficialmente em [twrp.me](https://twrp.me).

## Instalação

> **Pré-requisitos:**
> - Bootloader desbloqueado (necessário na maioria dos dispositivos).
> - Ferramentas ADB & Fastboot instaladas no PC.
> - Imagem TWRP correta para o modelo exato do dispositivo (verifique o codinome em twrp.me).

### Método Fastboot Geral (maioria dos dispositivos)

1. **Reinicie no bootloader:**
   ```bash
   adb reboot bootloader
   ```
2. **Instale a imagem de recovery:**
   ```bash
   fastboot flash recovery twrp-<versão>.img
   ```
3. **Inicie na recovery imediatamente** (antes que o sistema inicie, pois isso pode substituir o TWRP):
   ```bash
   fastboot reboot recovery
   # ou use a combinação de teclas (Vol + Power, etc.)
   ```

### Dispositivos com Slots (partições A/B – ex.: Pixels, OnePlus)

Como o sistema pode substituir automaticamente a partição de recovery na próxima inicialização, use um método de inicialização temporária:

1. **Inicie a imagem TWRP temporariamente:**
   ```bash
   fastboot boot twrp-<versão>.img
   ```
2. **Dentro do TWRP, vá em** *Avançado → Instalar Ramdisk da Recovery*.
   - Isso instala o TWRP no slot inativo e impede que ele seja substituído.

### Dispositivos Samsung (via Odin)

1. Baixe o arquivo `.tar` do TWRP (geralmente nomeado `twrp-<versão>-<dispositivo>.tar`).
2. Abra o Odin, coloque o arquivo no slot **AP**.
3. Desmarque **Auto-Reboot** nas opções do Odin.
4. Instale e, em seguida, reinicie imediatamente na recovery usando a combinação de teclas (Vol Up + Home + Power) para evitar a restauração da recovery original.

### A partir de um Dispositivo com Root (usando o Aplicativo Oficial TWRP)

1. Instale o **Aplicativo Oficial TWRP** da Play Store ou de twrp.me.
2. Conceda permissões de root.
3. Selecione seu dispositivo e instale a imagem mais recente.

### Pelo Terminal (com root)

```bash
su
dd if=/sdcard/twrp.img of=/dev/block/bootdevice/by-name/recovery
```

Substitua o caminho pela localização da sua partição de recovery (varia por dispositivo – encontre com `parted` ou `ls /dev/block/platform/...`).

## Fluxo de Uso Básico

### Entrar na Recovery
- Use a combinação de teclas (varia por fabricante, geralmente **Volume Down + Power**).
- Ou pelo Android (se tiver root/bootloader desbloqueado): `adb reboot recovery`.

### Limpeza de Partições

- **Restauração de Fábrica** (limpa data/cache) – necessária antes de instalar uma nova ROM.
  - *Limpar → Deslize para Restauração de Fábrica*
- **Formatar Data** – remove a criptografia e limpa o armazenamento interno.
  - *Limpar → Formatar Data → digite “yes”*.
- **Limpeza Avançada** – selecione partições individuais para limpar.

### Instalação de um ZIP (ROM, GApps, Magisk, etc.)

1. Toque em **Instalar**.
2. Navegue até o arquivo `.zip` (geralmente em `/sdcard` ou SD externo).
3. Toque no arquivo; opcionalmente toque em **Adicionar mais Zips** para enfileirar vários arquivos.
4. **Deslize para Confirmar a Instalação**.
5. *(Opcional)* Reinicie o sistema.

> Exemplo de comando para sideload:
> ```bash
> adb sideload custom_rom.zip
> ```

### Backup (NANDroid)

1. Toque em **Backup**.
2. Selecione as partições:
   - **Boot**, **System**, **Data** (mínimo para uma restauração completa do sistema).
   - **EFS** (armazena IMEI – crítico para alguns dispositivos).
3. Deslize para iniciar o backup.
4. O backup é armazenado em `/sdcard/TWRP/BACKUPS/<serial_do_dispositivo>/`.

### Restauração de um Backup

1. Toque em **Restaurar**.
2. Selecione um backup da lista.
3. Marque as partições que deseja restaurar.
4. Deslize para confirmar.

### Gerenciador de Arquivos e Terminal

- **Gerenciador de Arquivos**: *Avançado → Gerenciador de Arquivos* – navegue, exclua, renomeie, copie arquivos.
- **Terminal**: *Avançado → Terminal* – execute comandos como root.

## Exemplos de Comandos (Fastboot & ADB)

```bash
# Reiniciar no bootloader a partir do Android
adb reboot bootloader

# Instalar recovery
fastboot flash recovery twrp-3.7.1_12-0-beryllium.img

# Iniciar na recovery sem instalar
fastboot boot twrp-3.7.1_12-0-beryllium.img

# Sideload de um arquivo do PC
adb sideload LineageOS-21.0-20260617-UNOFFICIAL-beryllium.zip

# Enviar um arquivo para o dispositivo no modo MTP
adb push magisk.zip /sdcard/
```

## Avisos Importantes

- **Imagens específicas para o dispositivo** – Instalar uma imagem TWRP para um modelo diferente pode **danificar permanentemente o dispositivo**. Sempre verifique o codinome (ex.: `beryllium` para Pocophone F1).
- **Confusão com slots A/B** – Em dispositivos com atualizações seamless, o TWRP deve ser instalado em ambos os slots. Se um slot não tiver TWRP, o dispositivo pode reverter para a recovery original.
- **Problemas de criptografia** – O Android moderno usa **Criptografia Baseada em Arquivos (FBE)**. O TWRP geralmente não consegue descriptografar userdata. Usuários frequentemente precisam **Formatar Data** (limpa o armazenamento interno) ao trocar de ROM ou se o TWRP não conseguir montar `/data`.
- **OTAs com recovery personalizada** – Atualizações OTA oficiais geralmente falham com o TWRP. Você deve:
  - Instalar o ZIP da OTA manualmente via TWRP.
  - Ou reverter para a recovery original antes de aplicar a OTA.
- **Play Integrity / aplicativos bancários** – Um bootloader desbloqueado (necessário para TWRP) quebra muitas verificações de segurança. Fazer root com Magisk pode ocultar isso, mas adiciona complexidade e nem sempre funciona.
- **Backup antes de modificar** – Sempre crie um backup NANDroid antes de instalar qualquer nova ROM ou mod arriscado. Um backup completo pode salvar um soft brick em minutos.

## Solução de Problemas

| Problema | Solução |
|--------|----------|
| TWRP não persiste após reinicialização | Use `fastboot boot` e depois “Instalar Ramdisk da Recovery” (dispositivos A/B). Outra opção: reinstale e inicie imediatamente na recovery. |
| Não é possível montar `/data` | Provavelmente criptografado. Vá em *Limpar → Formatar Data* e digite “yes”. **Isso apaga todo o armazenamento interno.** |
| Dispositivo fica na tela de boot após instalação | Tente limpar Dalvik/ART Cache e Cache. Se ainda falhar, restaure um backup anterior. |
| Sideload via ADB travado em “enviando” | Certifique-se de ter os drivers ADB mais recentes. Tente outro cabo/porta USB. |
| TWRP não inicia (tela preta) | A imagem pode estar corrompida ou incorreta. Baixe novamente do site oficial. |

## Recursos Adicionais

- **Site oficial e downloads:** [https://twrp.me](https://twrp.me)
- **Código fonte:** [https://github.com/TeamWin/Team-Win-Recovery-Project](https://github.com/TeamWin/Team-Win-Recovery-Project)
- **Fóruns XDA:** Pesquise pelo tópico específico do seu dispositivo para builds e suporte do TWRP.
- **Compilando o TWRP a partir do código fonte:** [https://github.com/TeamWin/Team-Win-Recovery-Project/blob/android-12.1/README.md](https://github.com/TeamWin/Team-Win-Recovery-Project/blob/android-12.1/README.md)

O TWRP é uma ferramenta poderosa para qualquer desenvolvedor ou entusiasta Android. Use-o com sabedoria e mantenha sempre um backup à mão.