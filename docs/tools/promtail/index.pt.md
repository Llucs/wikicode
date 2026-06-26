---
title: Promtail - Um Enviador de Log para o Prometheus
description: O Promtail é um enviador de log leve, flexível e altamente configurável projetado para coletar logs de diversas fontes e enviar para um servidor Prometheus ou outros sistemas de armazenamento compatíveis.
created: 2026-06-26
tags:
  - logging
  - prometheus
  - grafana
status: draft
---

# Promtail - Um Enviador de Log para o Prometheus

Promtail é um enviador de logs para o Prometheus, desenvolvido e mantido pela Grafana Labs. É uma ferramenta leve, flexível e altamente configurável projetada para coletar logs de diversas fontes e enviar para um servidor Prometheus ou outros sistemas de armazenamento compatíveis.

## Características Principais

1. **Alta Disponibilidade e Resiliência**: O Promtail é projetado para lidar com falhas de maneira graciosa. Ele pode reprocessar automaticamente logs que falharam e suporta configurações para o reprocessamento de logs.
2. **Flexibilidade**: O Promtail suporta diversos formatos de log (JSON, syslog, texto puro) e pode ser configurado para extrair informações relevantes dos logs usando expressões regulares.
3. **Escala**: O Promtail está otimizado para processamento de logs em volume alto e pode lidar eficientemente com grandes quantidades de dados.
4. **Segurança**: Ele suporta TLS para comunicação segura entre o Promtail e o servidor Prometheus.
5. **Configuração**: As configurações são armazenadas em um arquivo YAML, o que facilita o gerenciamento e manutenção.
6. **Integração**: O Promtail pode ser integrado facilmente a infraestruturas existentes de logging e é compatível com diversos sistemas de logging.

## Histórico

O Promtail foi introduzido em 2018 como parte do projeto da Grafana Labs. Inicialmente, foi desenvolvido para atender à necessidade de um enviador de logs leve e eficiente que pudesse ser integrado ao sistema de monitoramento do Prometheus. Ao longo dos anos, o Promtail evoluiu para se tornar uma ferramenta robusta e amplamente utilizada na comunidade de logging e monitoramento.

## Casos de Uso

1. **Logs de Aplicação**: O Promtail pode ser usado para coletar logs de aplicação de servidores, contêineres e outras fontes e enviá-los para o Prometheus para monitoramento e geração de alertas.
2. **Monitoramento de Segurança**: Ao coletar e analisar dados de log, o Promtail pode ser usado para detectar violações de segurança, anomalias e outros eventos relacionados à segurança.
3. **Suporte Diagnóstico**: O Promtail ajuda na diagnóstico de problemas em sistemas de produção fornecendo logs detalhados que podem ser analisados para resolução de problemas.
4. **Conformidade**: O Promtail pode ser usado para garantir que os dados de log sejam coletados e armazenados em conformidade com requisitos regulatórios.
5. **Monitoramento**: O Promtail integra-se facilmente com o Prometheus para monitoramento em tempo real de logs e geração de alertas com base nos dados de log.

## Instalação

### Pré-requisitos
- Go (para compilação a partir do código-fonte)
- Docker (para instalação containerizada)

### Compilação a partir do Código-fonte
1. **Clonar o Repositório**:
   ```sh
   git clone https://github.com/grafana/promtail.git
   cd promtail
   ```

2. **Compilar a Binária**:
   ```sh
   make build
   ```

3. **Executar o Promtail**:
   ```sh
   ./promtail
   ```

### Instalação com Docker
1. **Pull o Imagem Docker**:
   ```sh
   docker pull grafana/promtail
   ```

2. **Executar o Promtail com Docker**:
   ```sh
   docker run -d --name promtail \
     -v /path/to/config.yml:/promtail/promtail.yml \
     grafana/promtail -config.file=/promtail/promtail.yml
   ```

## Uso Básico

### Configurando o Promtail
O Promtail usa um arquivo YAML para especificar as fontes de log, regras de análise e destinatários de saída. Aqui está um exemplo de configuração:

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://localhost:9091/log

scrape_configs:
  - job_name: server
    static_configs:
      - targets:
          - localhost
        labels:
          job: server
```

### Executando o Promtail
Uma vez que o arquivo de configuração esteja configurado, você pode executar o Promtail para começar a coletar logs.

```sh
promtail -config.file=/path/to/config.yml
```

### Monitorando Logs
O Promtail envia os logs coletados para o servidor Prometheus especificado. Você pode então usar o Prometheus para consultar e visualizar os dados de log.

## Conclusão

O Promtail é uma ferramenta poderosa para coletar e enviar dados de log para o Prometheus, proporcionando uma integração semântica para monitoramento e geração de alertas. Suas características flexíveis e fácil de usar o tornam uma valiosa adição a qualquer infraestrutura de logging e monitoramento.

---