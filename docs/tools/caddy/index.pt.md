---
title: Caddy: O Servidor Web Definitivo com HTTPS Automático
description: Um servidor web de nível empresarial, de código aberto, com HTTPS automático, proxy reverso e suporte a Docker, escrito em Go.
created: 2026-06-16
tags:
  - web-server
  - reverse-proxy
  - automatic-https
  - go
  - docker
  - open-source
status: draft
---

# Caddy

O Caddy é um servidor web poderoso, pronto para empresas, de código aberto e proxy reverso escrito em Go. Ele é projetado para ser simples de usar, ao mesmo tempo que oferece segurança robusta, gerenciamento automático de certificados TLS e uma API de configuração moderna. O Caddy é mantido pela Caddy Foundation e amplamente adotado tanto em ambientes de desenvolvimento quanto de produção.

## Recursos Principais

- **HTTPS Automático**: O Caddy obtém e renova automaticamente certificados TLS da Let's Encrypt ou ZeroSSL para cada domínio configurado. Ele gerencia OCSP stapling, HTTP/2 e HTTP/3 (QUIC) prontos para uso.
- **Configuração Simples**: Use um `Caddyfile` amigável ou uma poderosa API JSON para configuração dinâmica. O `Caddyfile` é um adaptador que traduz para JSON, oferecendo simplicidade e flexibilidade.
- **Proxy Reverso e Balanceamento de Carga**: Proxy reverso completo na Camada 7 com verificações de saúde ativas/passivas, tentativas, disjuntores e múltiplas políticas de balanceamento de carga (aleatório, menos conexões, hash de IP, afinidade de cabeçalho).
- **Segurança por Padrão**: Escrito em Go com segurança de memória, eliminando vulnerabilidades de estouro de buffer. Os padrões TLS são estritamente seguros, e o Caddy ouve em portas privilegiadas apenas quando necessário.
- **Arquitetura Modular**: O núcleo é mínimo; a funcionalidade é estendida por meio de módulos. Crie binários personalizados com `xcaddy` para incluir apenas os recursos necessários.
- **Nativo para Contêineres**: Binário único, desligamentos limpos, recargas suaves – ideal para Docker e Kubernetes.

## Por que Usar o Caddy?

O Caddy elimina a dor da configuração manual de HTTPS. Ele provisiona e renova certificados automaticamente, para que você nunca precise se preocupar com a expiração do TLS. Sua configuração é intuitiva e serve como um front-end perfeito para microsserviços, sites estáticos, APIs e SPAs. A API JSON permite integração perfeita com ferramentas de automação, enquanto o `Caddyfile` oferece uma alternativa amigável para humanos. Escreva uma vez, sirva com segurança em qualquer lugar.

## Instalação

O Caddy oferece múltiplos métodos de instalação:

### Baixar um Binário Pré-compilado

```bash
# Linux / macOS / Windows binary
curl -fsSL https://caddyserver.com/download/linux/amd64 -o caddy
chmod +x caddy
sudo mv caddy /usr/local/bin/
```

*Ou baixe de [caddyserver.com/download](https://caddyserver.com/download)*

### Gerenciadores de Pacotes

```bash
# Debian / Ubuntu
sudo apt install caddy

# macOS
brew install caddy

# Windows (winget)
winget install Caddy.Caddy
```

### Docker

```bash
docker pull caddy
```

### Compilação Personalizada com `xcaddy`

```bash
# Build Caddy with a specific plugin
xcaddy build --with github.com/caddyserver/transform-encoder

# Build with a custom version
xcaddy build v2.8.0 --with github.com/caddyserver/format-encoder
```

O `xcaddy` compila um único binário apenas com os módulos que você deseja.

## Uso Básico

### Servidor de Arquivos Estáticos

```bash
# Serve the current directory on port 80 with automatic HTTPS
caddy file-server
```

### Proxy Reverso Rápido

```bash
# Proxy traffic from yourdomain.com to a local backend
caddy reverse-proxy --from yourdomain.com --to localhost:8080
```

### Configuração com Caddyfile

Crie um `Caddyfile` na raiz do seu projeto:

```caddyfile
example.com {
    root * /var/www/example
    file_server
}
```

Em seguida, execute:

```bash
caddy run
```

O Caddy obterá automaticamente um certificado TLS para `example.com` e servirá os arquivos estáticos.

### Configuração JSON

O formato de configuração nativo do Caddy é JSON. Você pode aplicá-lo através da API de administração:

```bash
caddy run

# In another terminal, POST the configuration
curl -X POST -H "Content-Type: application/json" -d '{
  "apps": {
    "http": {
      "servers": {
        "example": {
          "listen": [":443"],
          "routes": [
            {
              "match": [{"host": ["example.com"]}],
              "handle": [
                {
                  "handler": "subroute",
                  "routes": [
                    {
                      "handle": [
                        {"handler": "file_server", "root": "/var/www/example"}
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      }
    }
  }
}' http://localhost:2019/config/
```

A API JSON é a fonte da verdade; o `Caddyfile` é apenas um adaptador.

## Recursos Principais em Detalhes

### HTTPS Automático

```caddyfile
mydomain.com {
    tls you@email.com   # Optional email for Let's Encrypt notices
}
```

O Caddy lida com emissão de certificados, renovação e redirecionamentos HTTP para HTTPS automaticamente. Ele suporta certificados curinga, endpoints ACME personalizados (ex.: ZeroSSL) e TLS sob demanda.

### Proxy Reverso com Balanceamento de Carga

```caddyfile
api.example.com {
    reverse_proxy api1:8080 api2:8080 api3:8080 {
        lb_policy least_conn
        health_uri /health
        health_interval 10s
    }
}
```

Políticas: `random`, `least_conn`, `ip_hash`, `uri_hash`, `header`, `first`, `round_robin`.

### Templates e Sites Dinâmicos

O Caddy pode executar templates para conteúdo dinâmico sem um backend separado:

```caddyfile
example.com {
    templates
    root * /var/www/example
}
```

### Autenticação

Autenticação modular (ex.: JWT, basic auth) pode ser adicionada através de plugins:

```caddyfile
example.com {
    basic_auth {
        admin $2a$14$hash...
    }
}
```

### HTTP/3 (QUIC)

Ative o HTTP/3 no seu `Caddyfile`:

```caddyfile
{
    servers {
        protocol {
            quic
        }
    }
}
```

## Integração com Docker

O Caddy é um cidadão de primeira classe em ambientes conteinerizados.

### Servir Arquivos Estáticos a partir de um Contêiner Docker

```dockerfile
FROM caddy:latest
COPY . /usr/share/caddy
```

Execute com:

```bash
docker build -t my-site .
docker run -d -p 80:80 -p 443:443 -e CADDY_INGRESS_NETWORKS=caddy my-site
```

### Usar como Proxy Reverso no Docker Compose

```yaml
version: "3.8"
services:
  caddy:
    image: caddy:latest
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
  app:
    image: my-app:latest
    expose:
      - "8080"
```

**Caddyfile**:

```caddyfile
mydomain.com {
    reverse_proxy app:8080
}
```

O Caddy descobre automaticamente o contêiner `app` através da rede Docker.

### Recargas Suaves no Docker

```bash
# After changing the Caddyfile, reload without downtime
docker exec -w /etc/caddy <container_name> caddy reload
```

## Gerenciamento do Ciclo de Vida

```bash
# Run in foreground
caddy run

# Run as background daemon
caddy start

# Stop the daemon
caddy stop

# Gracefully reload configuration (Linux)
caddy reload

# Validate a Caddyfile
caddy validate
```

## Conclusão

O Caddy simplifica o serviço web automatizando HTTPS, fornecendo um modelo de configuração limpo e integrando-se perfeitamente com stacks modernas. Seja implantando um site estático, um backend de microsserviços ou um gateway de API completo, o Caddy oferece segurança, desempenho e facilidade de uso — tudo em um único binário. Com forte suporte a Docker e um ecossistema vibrante de plugins, é uma excelente escolha tanto para desenvolvedores quanto para equipes de operações.