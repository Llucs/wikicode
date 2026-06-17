---
title: Módulo Magisk SpeedCool
description: Um módulo Magisk para Android que otimiza as configurações do sistema para aumentar o desempenho, reduzir o uso de RAM e melhorar o gerenciamento térmico.
created: 2026-06-15
tags:
  - android
  - magisk-module
  - performance-tuning
  - thermal-management
  - root
status: draft
ecosystem: android
---

# Módulo Magisk SpeedCool

**SpeedCool** é um módulo Magisk de código aberto e leve, criado por [Llucs](https://github.com/Llucs/SpeedCool-Magisk-Module). Ele aplica automaticamente um conjunto abrangente de ajustes no kernel e no sistema durante a inicialização para aumentar o desempenho, reduzir o uso de RAM e melhorar o gerenciamento térmico em qualquer dispositivo Android com root.

Ao contrário de um limpador de bloatware padrão, o SpeedCool modifica a configuração subjacente do sistema para eliminar as causas raiz de lentidão e superaquecimento.

---

## O Que Ele Faz

O SpeedCool atinge várias áreas-chave do sistema:

- **CPU Governor & Frequency Scaling:** Reduz a latência de ativação para aplicações exigentes (ex: jogos, emuladores).
- **Low Memory Killer (LMK):** Prioriza manter o aplicativo ativo na memória enquanto recupera agressivamente a memória de processos em cache em segundo plano.
- **Thermal Engine:** Modifica os pontos de limitação térmica para equilibrar o desempenho sustentado com a geração de calor.
- **I/O Scheduler:** Alterna o escalonador de armazenamento para uma variante de baixa latência para um carregamento mais rápido de aplicativos.
- **Network Stack:** Otimiza o controle de congestionamento TCP para melhor taxa de transferência em redes móveis.
- **GPU Rendering:** Ativa a renderização forçada da GPU e otimiza o governor da GPU.

---

## Por Que Usá-lo?

- **Jogos mais suaves:** As taxas de quadros são mais estáveis devido a um melhor ajuste do governor da CPU/GPU e controle de limitação térmica.
- **Multitarefa mais rápida:** Apps recarregam com menos frequência graças aos valores LMK otimizados.
- **Operação mais fria:** Perfis térmicos inteligentes evitam que o SoC atinja temperaturas críticas durante o uso intenso.
- **Otimizador tudo-em-um:** Substitui a necessidade de vários módulos de desempenho conflitantes.
- **Leve:** O módulo geralmente tem menos de 1 MB e tem sobrecarga desprezível.

---

## Instalação

### Pré-requisitos

- Dispositivo Android com bootloader desbloqueado e acesso root.
- **Magisk** (v20.0+) instalado.
- Recovery personalizado (TWRP) recomendado como fallback.

### Passos

1. **Baixe** o arquivo `SpeedCool-Magisk-Module.zip` mais recente na [página de lançamentos do GitHub](https://github.com/Llucs/SpeedCool-Magisk-Module/releases).
2. Abra o aplicativo **Magisk Manager**.
3. Navegue até a aba **Módulos**.
4. Toque em **Instalar do armazenamento**.
5. Selecione o arquivo `.zip` baixado.
6. Deslize para confirmar a instalação.
7. **Reinicie** o dispositivo quando solicitado.

> **Dica:** Se você tiver um bootloop, inicialize no Modo de Segurança (segure Volume Up durante a inicialização) e desabilite o módulo, ou remova-o manualmente via recuperação apagando a pasta `/data/adb/modules/SpeedCool/`.

---

## Uso e Verificação

O SpeedCool foi projetado para funcionar inteiramente em segundo plano. Nenhuma interface de usuário é necessária. Você pode verificar sua operação usando comandos de terminal.

### Verificando o Status Ativo

Liste o diretório do módulo para confirmar que está instalado:

```bash
su -c "ls -la /data/adb/modules/SpeedCool/"
```

Se montado com sucesso, o diretório conterá os arquivos do módulo (`system.prop`, `service.sh`, `module.prop`).

### Verificando as Propriedades do Sistema Aplicadas

```bash
su -c "getprop | grep speed"
```

Procure por propriedades injetadas pelo módulo (por exemplo, `ro.sys.speedcool.version`).

---

## Principais Recursos com Exemplos de Comandos

### 1. Ajuste do Governor da CPU

O módulo força um governor de baixa latência (geralmente `performance`, `interactive` ou `schedutil` ajustado) em todos os núcleos da CPU.

```bash
# Check the current governor
su -c "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
```

*Saída esperada:* `performance` ou `schedutil`

### 2. Otimização de RAM (LMK)

Os limites do Low Memory Killer são modificados para manter o aplicativo em primeiro plano responsivo enquanto elimina agressivamente processos em segundo plano menos úteis.

```bash
# Check LMK values (adj, minfree)
su -c "cat /sys/module/lowmemorykiller/parameters/minfree"
su -c "cat /sys/module/lowmemorykiller/parameters/adj"
```

### 3. Otimização do Escalonador de I/O

O escalonador da camada de bloco é alterado para uma variante otimizada para desempenho interativo (por exemplo, `bfq` ou `fiops`).

```bash
# Check the active scheduler for the main storage block device
su -c "cat /sys/block/mmcblk0/queue/scheduler"
```

*Saída esperada:* `[bfq]` ou `[fiops]`

### 4. Ajustes de Rede

O controle de congestionamento TCP é alterado para um algoritmo mais adequado para redes móveis (por exemplo, `westwood` ou `bbr`).

```bash
# Check the active TCP congestion algorithm
su -c "cat /proc/sys/net/ipv4/tcp_congestion_control"
```

*Saída esperada:* `westwood`

### 5. Visualizando Logs do Módulo

Se a depuração estiver ativada no script do módulo, você pode filtrar o log do sistema.

```bash
su -c "logcat -d | grep SpeedCool"
```

### 6. Lendo o Perfil do Módulo (se configurável)

Algumas versões permitem que você escolha um perfil editando o `service.sh`. Verifique os comentários disponíveis dentro do arquivo:

```bash
su -c "head -50 /data/adb/modules/SpeedCool/service.sh"
```

---

## Solução de Problemas

| Sintoma | Causa Provável | Solução |
|---|---|---|
| **Bootloop** | Módulo conflitante ou dispositivo incompatível. | Segure Volume Up durante a inicialização para desabilitar o módulo, ou remova o diretório `/data/adb/modules/SpeedCool` no gerenciador de arquivos do TWRP. |
| **Nenhuma mudança de desempenho** | Módulos conflitantes (LKT, FDE.AI, NFS). | Remova todos os outros módulos de desempenho antes de usar o SpeedCool. |
| **Dispositivo ainda quente** | Limites térmicos muito agressivos. | Verifique a configuração do thermal-engine no módulo ou tente um perfil diferente. |
| **Aplicativos travando** | Valores LMK excessivamente agressivos. | Ajuste manualmente os valores de `minfree` no `service.sh`. |

---

## Remoção

1. Abra o **Magisk Manager**.
2. Vá para a aba **Módulos**.
3. Toque no ícone **Remover** (lixeira) ao lado do SpeedCool.
4. Toque em **Reiniciar**.

**Remoção alternativa por linha de comando:**

```bash
su -c "rm -rf /data/adb/modules/SpeedCool/"
reboot
```

---

## Referências

- **Repositório GitHub:** [Llucs/SpeedCool-Magisk-Module](https://github.com/Llucs/SpeedCool-Magisk-Module)
- **Documentação Oficial do Magisk:** [topjohnwu.github.io/Magisk/](https://topjohnwu.github.io/Magisk/)
- **XDA Developers:** Procure por *SpeedCool* ou *Llucs* para discussões de suporte da comunidade.

> **Aviso:** Modificar parâmetros do sistema traz riscos inerentes. Sempre faça um backup Nandroid completo antes de instalar módulos de desempenho. Os autores não se responsabilizam por qualquer dano causado ao seu dispositivo.