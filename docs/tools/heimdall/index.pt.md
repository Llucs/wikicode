---
title: Heimdall - Ferramenta de Flash de Firmware Samsung
description: Suíte de ferramentas de código aberto multiplataforma para flash de firmware (ROMs) em dispositivos móveis Samsung.
created: 2026-06-15
tags:
  - samsung
  - firmware
  - flashing
  - odin
  - android
  - open-source
status: draft
ecosystem: android
---

# Heimdall

## O que é Heimdall?

Heimdall é uma suíte de ferramentas multiplataforma e de código aberto projetada para gravar firmware (ROMs originais, ROMs personalizadas, bootloaders e imagens de recuperação) em dispositivos Android Samsung. Ele opera diretamente via USB usando o protocolo proprietário Odin da Samsung, fornecendo uma alternativa gratuita e amigável para Linux/macOS à ferramenta Odin, exclusiva do Windows. O projeto é mantido no GitHub por Benjamin Dobell e tem sido amplamente utilizado na comunidade de modding Android desde o início dos anos 2010.

## Por que usar Heimdall?

- **Multiplataforma** – Executa nativamente no Windows, Linux e macOS sem emulação.
- **Código aberto** – Totalmente auditável e conduzido pela comunidade.
- **Ignora as restrições do Odin** – Útil quando o Odin não está disponível ou ao fazer flash em sistemas que não são Windows.
- **Scriptável** – Interface de linha de comando permite automação e integração em cadeias de ferramentas personalizadas.
- **Flash em nível de partição** – Faça flash de imagens de partição individuais (por exemplo, `BOOT`, `SYSTEM`, `RECOVERY`) para modificações direcionadas.

## Instalação

### Windows
Baixe o instalador mais recente da [página de lançamentos do GitHub](https://github.com/Benjamin-Dobell/Heimdall/releases). Execute o `.exe` e siga o instalador gráfico.

### Linux
Disponível através de muitos gerenciadores de pacotes:
```bash
# Debian/Ubuntu
sudo apt install heimdall-flash

# Fedora
sudo dnf install heimdall

# Arch Linux
sudo pacman -S heimdall
```
Alternativamente, compile a partir do código-fonte usando `cmake`.

### macOS
Instale via Homebrew:
```bash
brew install heimdall
```
Ou baixe o binário para macOS da página de lançamentos.

## Uso

### Pré-requisitos
1. Ative as **Opções do Desenvolvedor** e a **Depuração USB** no dispositivo Samsung.
2. Inicialize o dispositivo no **Modo Download** (normalmente: Desligue → segure Volume Down + Home + Power, depois pressione Volume Up para confirmar).
3. Conecte o dispositivo ao computador via USB.

### Detecção
Verifique se o dispositivo é reconhecido:
```bash
heimdall detect
```
Se bem-sucedido, a saída exibirá o modelo do dispositivo e o status da conexão.

### Flash Básico
Faça o flash de uma imagem de partição:
```bash
heimdall flash --RECOVERY twrp-3.6.0-i9300.img
```
Faça o flash de várias partições de uma só vez:
```bash
heimdall flash --BOOT boot.img --SYSTEM system.img --VENDOR vendor.img
```

### Usando um arquivo PIT
Para restauração completa do firmware ou quando a tabela de partições for desconhecida, forneça um arquivo `.pit` extraído do dispositivo ou do pacote de firmware:
```bash
heimdall flash --pit /path/to/device.pit --SLT --no-reboot
```
A flag `--SLT` faz o flash de todas as partições definidas no PIT, enquanto `--no-reboot` mantém o dispositivo no modo download após a conclusão.

### Fechar conexão
Após o flash, feche a interface USB:
```bash
heimdall close-pc-screen
```

## Principais Recursos

- **Multiplataforma**: Windows, Linux, macOS (binários nativos).
- **Código aberto**: base de código licenciada sob BSD com manutenção ativa da comunidade.
- **Suporte ao protocolo Odin**: implementação direta do protocolo de flash de baixo nível da Samsung.
- **Detecção de dispositivos**: enumeração USB confiável e verificação de handshake.
- **Flash em nível de partição**: faça flash de partições individuais (boot, recovery, system, etc.).
- **Flash baseado em PIT**: use tabelas de informações de partição para restauração completa do firmware.
- **Drivers USB integrados**: instaladores do Windows incluem drivers necessários; libusb usado no Linux/macOS.
- **Suporte a scripting**: flags de CLI adequadas para pipelines automatizados e ambientes CI/CD.

## Exemplos

### Detectar um dispositivo conectado
```bash
$ heimdall detect
Device detected: GT-I9300 (galaxys3)
```

### Fazer flash de uma recuperação personalizada (TWRP)
```bash
heimdall flash --RECOVERY twrp-3.6.0_9-i9300.img --no-reboot
```

### Fazer flash de um firmware original completo usando um arquivo PIT
```bash
heimdall flash --pit AP_I9300_4.3.pit --SLT --no-reboot
```

### Fazer flash apenas da partição boot
```bash
heimdall flash --BOOT boot.img
```

## Notas

- Heimdall é distinto do **Heimdall Application Dashboard** (linuxserver/Heimdall, um lançador de aplicativos baseado na web) e do **Heimdall** framework de cibersegurança.
- Sempre use o firmware correto para o modelo do seu dispositivo para evitar brick.
- Certifique-se de que os drivers USB estejam instalados no Windows – o instalador os inclui. No Linux, regras udev podem precisar ser adicionadas para que o dispositivo seja acessível sem root.