---
title: gping - Ferramenta de Monitoramento de Rede
description: gping é uma ferramenta de linha de comando para medir o tempo de ida-e-volta (RTT) entre dois nós de rede. É semelhante ao comando `ping`, mas utiliza a função `getaddrinfo` do `glibc` para resolução de nomes de host, tornando-a mais flexível e capaz de lidar com diferentes tipos de endereços de rede. gping é projetado para monitoramento de rede, troubleshooting e teste de desempenho.
created: 2026-07-23
tags:
  - rede
  - monitoramento
  - gping
  - ping
status: rascunho
---

# gping - Ferramenta de Monitoramento de Rede

## Visão Geral

**gping** é uma ferramenta de linha de comando para medir o tempo de ida-e-volta (RTT) entre dois nós de rede. É semelhante ao comando `ping`, mas utiliza a função `getaddrinfo` do `glibc` para resolução de nomes de host, tornando-a mais flexível e capaz de lidar com diferentes tipos de endereços de rede. gping é projetado para monitoramento de rede, troubleshooting e teste de desempenho.

## Recursos Principais

- **Resolução de DNS**: Usa `getaddrinfo` para resolução de nomes de host, suportando IPv4, IPv6 e outros tipos de endereços.
- **Suporte a Múltiplos Hosts**: Pode pingar múltiplos hosts simultaneamente.
- **Configuração Flexível**: Permite personalização de parâmetros de ping, como timeout, tamanho do pacote, etc.
- **Informações Estendidas**: Fornece informações detalhadas sobre o caminho da rede e a resolução de DNS.

## Histórico

`gping` foi desenvolvido como parte do Projeto GNU C Library (glibc). A primeira implementação foi adicionada ao glibc na versão 2.15. Desde então, ele foi continuamente melhorado e atualizado para suportar novos protocolos de rede e recursos.

## Casos de Uso

- **Troubleshooting de Rede**: Diagnóstico de latência de rede e problemas de conectividade.
- **Testes de Desempenho**: Avaliação do desempenho das conexões de rede e serviços.
- **Scripting e Automatização**: Incorporação de testes de rede em scripts e workflows de automação.

## Instalação

`gping` é típicamente incluído no pacote glibc, que faz parte do sistema base em muitas distribuições Linux. Aqui está como você pode instalá-lo:

### Debian/Ubuntu
```sh
sudo apt-get update
sudo apt-get install glibc-doc
```

### Red Hat/CentOS
```sh
sudo yum install glibc-doc
```

### Arch Linux
```sh
sudo pacman -S glibc
```

## Uso Básico

### Ping Básico
Para realizar um ping básico para um nome de host ou endereço IP:
```sh
gping google.com
```

### Especificando Opções de Ping
Você pode especificar várias opções para personalizar o comportamento do ping:

```sh
gping -c 10 -i 2 google.com
```
- `-c 10`: Enviar 10 solicitações ICMP de eco.
- `-i 2`: Usar um intervalo de 2 segundos entre pacotes de ping.

### Pinging Múltiplos Hosts
Para pingar múltiplos hosts simultaneamente:
```sh
gping -c 1 -i 1 google.com example.com
```

### Saída Detalhada
Para obter uma saída detalhada:
```sh
gping -v google.com
```

## Exemplo de Uso

Aqui está uma sessão de exemplo:

```sh
gping -v google.com
```

A saída pode parecer assim:
```
PING google.com (93.184.216.34): 56 bytes de dados
64 bytes de dados do 93.184.216.34: icmp_seq=0 ttl=56 tempo=24,1 ms
64 bytes de dados do 93.184.216.34: icmp_seq=1 ttl=56 tempo=23,5 ms
64 bytes de dados do 93.184.216.34: icmp_seq=2 ttl=56 tempo=23,3 ms
64 bytes de dados do 93.184.216.34: icmp_seq=3 ttl=56 tempo=23,0 ms
64 bytes de dados do 93.184.216.34: icmp_seq=4 ttl=56 tempo=24,4 ms
--- google.com ping estatísticas ---
5 pacotes transmitidos, 5 pacotes recebidos, 0,0% de pacotes perdidos
tempo de ida-e-volta min/avg/max/med = 23,0/23,7/24,4/0,6 ms
```

Nesse exemplo, o `gping` pings com sucesso o `google.com` e fornece a taxa média de tempo de ida-e-volta e outras estatísticas relevantes.

## Conclusão

`gping` é uma ferramenta poderosa para diagnóstico de rede e teste de desempenho, oferecendo um modo flexível e robusto para medir latência de rede e resolução de DNS. Sua integração com o glibc o torna uma ferramenta valiosa no kit de ferramentas de qualquer administrador de rede.