---
title: HAProxy
description: HAProxy é um balanceador de carga TCP/HTTP e proxy reverso de alto desempenho e código aberto que oferece extrema confiabilidade, desempenho e controle para sistemas distribuídos modernos.
created: 2026-06-17
tags:
  - load-balancer
  - proxy
  - tcp
  - http
  - haproxy
  - devops
status: draft
---

# HAProxy

HAProxy (High Availability Proxy) é o balanceador de carga e servidor proxy TCP e HTTP de código aberto padrão de facto. Escrito em C por Willy Tarreau, ele é projetado especificamente para distribuir tráfego entre servidores de backend com desempenho extremo, confiabilidade e um consumo mínimo de memória. HAProxy alimenta muitos dos sites e serviços mais movimentados da internet, incluindo GitHub, Reddit, Twitter/X e Docker Hub.

## O que é HAProxy?

HAProxy é um proxy reverso gratuito, muito rápido e confiável que oferece alta disponibilidade, balanceamento de carga e proxy para aplicações baseadas em TCP e HTTP. Ele roda em Linux, macOS e FreeBSD. Seu uso mais comum é melhorar o desempenho e a confiabilidade de um ambiente de servidor distribuindo a carga de trabalho entre vários servidores (ex.: web, aplicação, banco de dados). Além do balanceamento de carga básico, o HAProxy fornece gerenciamento avançado de tráfego, terminação SSL/TLS, comutação de conteúdo, verificações de saúde, persistência de sessão, observabilidade profunda e recursos de segurança como limitação de taxa e endurecimento de protocolo.

## Por que HAProxy?

Na infraestrutura moderna, os serviços devem lidar com milhões de conexões simultâneas com zero tempo de inatividade. Servidores web de propósito geral como Nginx ou Apache podem atuar como balanceadores de carga, mas o HAProxy é **projetado especificamente** para essa função. Ele se destaca em:

- **Desempenho:** Pode lidar com milhões de conexões simultâneas em hardware modesto graças a uma arquitetura orientada a eventos, single‑threaded (ou multi‑threaded).
- **Confiabilidade:** Construído com verificações de sanidade agressivas; condições impossíveis ou loops infinitos resultam em uma falha imediata com um dump, prevenindo corrupção silenciosa de dados.
- **Conjunto de recursos:** Terminação SSL nativa, HTTP/2, gRPC, QUIC/HTTP/3, ACLs avançadas, stick‑tables, métricas do Prometheus e recargas contínuas.
- **Segurança:** Protege backends contra ataques slow‑loris, DDoS e explorações em nível de protocolo.

## Instalação

HAProxy está disponível na maioria dos repositórios de pacotes, pode ser executado via Docker e pode ser compilado a partir do código fonte para builds personalizados.

### Dos Repositórios Oficiais

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install haproxy

# RHEL / CentOS / Fedora
sudo yum install haproxy

# Alpine
apk add haproxy

# FreeBSD
pkg install haproxy
```

### Usando Docker

```bash
docker run --name my-haproxy \
  -v /path/to/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro \
  -p 80:80 \
  -p 443:443 \
  haproxy:lts
```

### Compilando a partir do Código Fonte (para recursos personalizados)

```bash
# Install build dependencies (example for Debian)
sudo apt install build-essential libssl-dev libpcre3-dev zlib1g-dev liblua5.3-dev

# Download and build
wget https://www.haproxy.org/download/3.0/src/haproxy-3.0.0.tar.gz
tar xzf haproxy-3.0.0.tar.gz
cd haproxy-3.0.0
make TARGET=linux-glibc USE_OPENSSL=1 USE_PCRE=1 USE_ZLIB=1 USE_LUA=1
sudo make install
```

## Configuração Básica

A configuração do HAProxy é escrita em um único arquivo de texto, geralmente localizado em `/etc/haproxy/haproxy.cfg`. O arquivo é composto por seções lógicas:

| Seção       | Propósito                                                                 |
|-------------|---------------------------------------------------------------------------|
| `global`    | Configurações de todo o processo (user, group, max connections, stats socket). |
| `defaults`  | Parâmetros compartilhados para todos os frontends/backends (mode, timeouts, logging options). |
| `frontend`  | Pontos de entrada de tráfego: define bindings de IP/porta, ACLs e backends padrão. |
| `backend`   | Pools de servidores para os quais o tráfego é encaminhado. Define algoritmo de balanceamento de carga, verificações de saúde e persistência. |
| `listen`    | Wrapper de conveniência que combina frontend e backend para configurações simples. |

### Exemplo: Balanceador de Carga HTTP Simples

```cfg
global
    maxconn 4096
    user haproxy
    group haproxy

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms
    option httplog

frontend http-in
    bind *:80
    default_backend webservers

backend webservers
    balance roundrobin
    server web1 192.168.1.10:80 check
    server web2 192.168.1.11:80 check
```

### Exemplo: Balanceador de Carga TCP (ex.: MySQL)

```cfg
frontend mysql-in
    bind *:3306
    mode tcp
    default_backend mysql_servers

backend mysql_servers
    mode tcp
    balance leastconn
    server db1 10.0.0.1:3306 check
    server db2 10.0.0.2:3306 check
```

### Habilitando a Página de Estatísticas

```cfg
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 10s
    # optionally restrict access
    stats auth admin:password
```

## Principais Recursos com Exemplos de Comandos

### 1. Algoritmos de Balanceamento de Carga

HAProxy suporta dezenas de algoritmos de balanceamento. Alguns dos mais comuns:

| Algoritmo          | Descrição                                                                  |
|--------------------|----------------------------------------------------------------------------|
| `roundrobin`       | Distribui requisições sequencialmente entre os servidores.                 |
| `leastconn`        | Envia requisições para o servidor com menos conexões.                      |
| `source`           | Faz hash do IP de origem, garantindo que um cliente atinja o mesmo servidor (útil para persistência). |
| `uri`              | Faz hash da URI da requisição, útil para configurações de cache.           |
| `hdr(name)`        | Faz hash do valor de um cabeçalho (ex.: `X-Session-ID`).                   |

Exemplo de configuração:

```cfg
backend webservers
    balance hdr(host)
    server web1 192.168.1.10:80 check
    server web2 192.168.1.11:80 check
```

### 2. Verificações de Saúde

As verificações de saúde ativas são configuradas com a palavra-chave `check` em cada linha de servidor. Você pode ajustá-las:

```cfg
server web1 192.168.1.10:80 check inter 2s fall 3 rise 2
# inter    – check interval
# fall     – number of failures before marking server down
# rise     – number of successes before marking server up
```

Você também pode realizar verificações de camada 7 (`option httpchk`) para backends HTTP:

```cfg
backend webservers
    option httpchk HEAD /health HTTP/1.1\r\nHost:\ localhost
    server web1 192.168.1.10:80 check
```

### 3. Offloading SSL/TLS

Termine o HTTPS no balanceador de carga e encaminhe HTTP simples para os backends:

```cfg
frontend https-in
    bind *:443 ssl crt /etc/ssl/certs/example.pem
    default_backend webservers

backend webservers
    server web1 192.168.1.10:80 check
```

Você também pode re-criptografar para os backends (SSL bridging) ou verificar certificados do cliente.

### 4. Comutação de Conteúdo com ACLs

Use ACLs para rotear tráfego com base em cabeçalhos, caminhos de URL, TLS SNI, etc.

```cfg
frontend http-in
    bind *:80

    # Define ACLs
    acl is_api path_beg /api/
    acl is_static path_end .jpg .png .css .js

    # Use ACLs to choose backend
    use_backend api_servers if is_api
    use_backend static_servers if is_static
    default_backend webservers
```

### 5. Persistência de Sessão (Stickiness)

Garanta que as requisições de um usuário sempre vão para o mesmo servidor backend:

```cfg
backend webservers
    balance roundrobin
    cookie SERVERID insert indirect nocache
    server web1 192.168.1.10:80 check cookie w1
    server web2 192.168.1.11:80 check cookie w2
```

Alternativamente, use persistência `stick-table` baseada em IP ou em um cabeçalho.

### 6. Recargas com Zero Tempo de Inatividade

Aplique mudanças de configuração sem descartar conexões:

```bash
haproxy -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid -sf $(cat /run/haproxy.pid)
```

Ou via systemd:

```bash
systemctl reload haproxy
```

## Recursos Avançados

### Limitação de Taxa

```cfg
frontend http-in
    bind *:80

    # Allow 10 requests per second per IP, burst to 20
    stick-table type ip size 1m expire 10s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 20 }
    default_backend webservers
```

### HTTP/2 e gRPC

HAProxy suporta HTTP/2 e pode atuar como proxy para gRPC sem qualquer configuração especial além de habilitar `alpn`:

```cfg
frontend https-in
    bind *:443 ssl crt /etc/ssl/certs/example.pem alpn h2,http/1.1
    default_backend grpc_servers

backend grpc_servers
    server grpc1 10.0.0.1:50051 check
```

### QUIC / HTTP/3

Versões recentes (≥2.5) incluem suporte experimental a QUIC para HTTP/3 baseado em UDP:

```cfg
frontend quic-in
    bind quic4@:443 ssl crt /etc/ssl/certs/example.pem
    default_backend webservers
```

### Observabilidade

- **Página de estatísticas:** endpoint HTML/JSON embutido (veja exemplo anterior).
- **Métricas do Prometheus:** use a opção `stats prometheus`:

```cfg
frontend stats
    bind *:8405
    stats enable
    stats uri /metrics
    stats prometheus
```

- **Registro bruto:** HAProxy gera logs detalhados (para syslog ou um arquivo de log separado) que podem ser analisados por ferramentas como `tail`, `grep`, ou enviados para ELK/Loki.

## Gerenciamento via Linha de Comando

HAProxy fornece uma API de runtime rica via um socket Unix ou socket TCP. O utilitário `socat` é comumente usado para enviar comandos:

```bash
echo "show info" | socat stdio unix-connect:/run/haproxy.sock
echo "show stat" | socat stdio unix-connect:/run/haproxy.sock
echo "enable server webservers/web1" | socat stdio unix-connect:/run/haproxy.sock
```

A API de runtime também suporta adição/remoção dinâmica de servidores, o que é crucial para ambientes de contêiner.

## Considerações de Segurança

- **Execute como não-root:** HAProxy reduz privilégios após vincular portas. As diretivas `user` e `group` em `global` são obrigatórias.
- **Ative chroot:** Defina `chroot /var/lib/haproxy` para isolar o processo do sistema de arquivos.
- **Restrinja estatísticas:** Use autenticação, ACLs ou vincule estatísticas em uma interface privada.
- **Ajuste timeouts:** Impede que clientes lentos esgotem os pools de conexão.
- **Ative proteção contra SYN flood:** Use as opções `tcp-smart-connect` e `tcp-smart-accept`.

## Conclusão

HAProxy é um componente maduro e testado em batalha que forma a espinha dorsal de muitos sistemas críticos e de alto tráfego. Seu foco preciso em balanceamento de carga e proxy oferece desempenho, estabilidade e controle granular incomparáveis. Esteja você executando um pequeno blog ou um SaaS de alcance global, o HAProxy é uma ferramenta essencial no kit de ferramentas de qualquer engenheiro de infraestrutura.

Para leitura adicional, consulte a [documentação oficial do HAProxy](https://www.haproxy.org/documentation/) ou o [site da HAProxy Technologies](https://www.haproxy.com/).