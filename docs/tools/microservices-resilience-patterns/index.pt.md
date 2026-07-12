---
title: Padronesses de Resiliência de Microserviços
description: Técnicas para garantir a robustez e a tolerância a falhas em arquiteturas de microserviços.
created: 2026-07-12
tags:
  - microservices
  - resiliência
  - padronesses
  - tolerância a falhas
status: rascunho
---

# Padronesses de Resiliência de Microserviços

A arquitetura de microserviços descompondo uma aplicação em serviços pequenos e independentes. Cada serviço é responsável por uma função de negócios específica e se comunica com os outros através de APIs bem definidas. No entanto, essa arquitetura introduz novos desafios relacionados às interações entre os serviços, em particular em termos de resiliência e tolerância a falhas. As padronesses de resiliência são padrões de design que ajudam a garantir a robustez e a confiabilidade de aplicativos baseados em microserviços.

## Características Principais das Padronesses de Resiliência de Microserviços

1. **Controle Decentralizado**: Os serviços não são gerenciados centralmente, o que torna difícil lidar com falhas.
2. **Comunicação Assíncrona**: Os serviços se comunicam através de mensagens assíncronas, o que pode levar a atrasos e incertezas.
3. **Isolamento de Serviços**: Uma falha em um serviço não deve afetar a estabilidade dos outros serviços.
4. **Tolerância a Falhas**: O sistema deve continuar a funcionar mesmo quando partes dele falham.

## Padronesses Comuns de Resiliência de Microserviços

### 1. Padroness de Bloqueio de Decapado

- **Descrição**: O padroness de bloqueio de decapado é usado para limitar o dano quando um serviço falha, impedindo que a falha se propague para outros serviços.
- **Características Principais**: Isolamento de serviço, interruptor de circuito e timeout.
- **Implementação**: Use um interruptor de circuito para isolar o serviço falhado e impedir que novas requisições sejam enviadas até que o serviço se recupere.
- **Cases de Uso**: Falhas de banco de dados, falhas de API de terceiros, falhas de rede.
- **Uso Básico**: Implemente um timeout para chamadas remotas de serviço e use um interruptor de circuito para evitar sobrecarregar o serviço com requisições.

### 2. Padroness de Interruptor de Circuito

- **Descrição**: O padroness de interruptor de circuito é uma estratégia para proteger o serviço de ser sobrecarregado por um serviço de terceiros.
- **Características Principais**: Monitoramento, limiar, estados de aberto e fechado.
- **Implementação**: Monitore a taxa de sucesso de um serviço remoto e abra o circuito se a taxa de sucesso cair abaixo do limiar.
- **Cases de Uso**: Falhas de API, falhas de banco de dados, problemas de rede.
- **Uso Básico**: Configure um limiar para o número de requisições falhas antes de abrir o circuito e pare de enviar requisições para o serviço remoto. Uma vez que o serviço se recupere, feche o circuito.

### 3. Padroness de Retorno de Vôo

- **Descrição**: O padroness de retorno de vôo fornece uma resposta padrão quando um serviço remoto falha.
- **Características Principais**: Resposta padrão, cache.
- **Implementação**: Retorne uma resposta cacheada ou pré-definida quando o serviço remoto falha.
- **Cases de Uso**: Falhas de banco de dados, falhas de rede.
- **Uso Básico**: Cache a resposta do serviço remoto ou forneça uma resposta de vôo quando o serviço não estiver disponível.

### 4. Padroness de Tentaativas Resilientes

- **Descrição**: O padroness de tentativas resilientes tenta reexecutar uma requisição falhada após um atraso.
- **Características Principais**: Retentativa exponencial, jitter, tentativas.
- **Implementação**: Tente executar a requisição após um atraso que aumenta exponencialmente com cada tentativa e adiciona jitter aleatório para evitar problemas de formação de banhos de chuva.
- **Cases de Uso**: Problemas de rede, bloqueio temporário de banco de dados.
- **Uso Básico**: Implemente uma política de tentativas que reexecute a requisição após um atraso, e se a requisição falhar, aumente o atraso exponencialmente e adicione jitter aleatório.

### 5. Padroness de Shedding de Carga

- **Descrição**: O padroness de shedding de carga reduz a carga em um serviço ao rejeitar ou atrasar requisições.
- **Características Principais**: Taxa de execução, fila.
- **Implementação**: Use um sistema de fila para lidar com requisições entrantes e rejeite ou atrasa requisições quando o serviço está sob carga pesada.
- **Cases de Uso**: Alta taxa de tráfego, sobrecarga do serviço.
- **Uso Básico**: Implemente um sistema de fila que gerencia requisições entrantes e rejeita ou atrasa requisições quando o serviço está sobrecarregado.

### 6. Combinação de Bloqueios de Decapado e Interruptores de Circuito

- **Descrição**: Combinar bloqueios de decapado e interruptores de circuito pode fornecer uma solução robusta para microserviços.
- **Características Principais**: Isolamento de serviço, tolerância a falhas.
- **Implementação**: Use bloqueios de decapado para isolar os serviços e interruptores de circuito para prevenir a falha de um serviço de afetar os outros.
- **Cases de Uso**: Arquiteturas de microserviços complexas, sistemas críticos.
- **Uso Básico**: Implemente tanto bloqueios de decapado quanto interruptores de circuito para garantir que uma falha em um serviço não afete a estabilidade dos outros serviços.

## Instalação e Uso Básico

### Instalação

1. **Interruptor de Circuito**:
   - **Bibliotecas**: Spring Cloud Netflix Hystrix, Resilience4j, Netflix Ribbon.
   - **Exemplo (Spring Cloud Hystrix)**:
     ```java
     @Autowired
     private HystrixCommand.Setter setter;
     
     @HystrixCommand(fallbackMethod = "fallbackMethod")
     public String getResponse() {
         // Chamada de serviço remoto
     }
     
     public String fallbackMethod() {
         return "Resposta de Vôo";
     }
     ```

2. **Bloqueio de Decapado**:
   - **Bibliotecas**: Resilience4j, Hystrix.
   - **Exemplo (Resilience4j)**:
     ```java
     @Autowired
     private RateLimiter rateLimiter;
     
     @Override
     public String fetchSomeData() {
         return rateLimiter.executeWithRateLimiter(() -> remoteService.getData(), 5);
     }
     ```

### Uso Básico

1. **Interruptor de Circuito**:
   - Configure o interruptor de circuito para monitorar a taxa de sucesso de serviços remotos e abra o circuito se a taxa de sucesso cair abaixo de um determinado limiar.
   - Implemente um método de vôo para retornar uma resposta padrão quando o serviço remoto não estiver disponível.

2. **Bloqueio de Decapado**:
   - Configure um bloqueio de decapado para isolar as chamadas de serviço remoto e limitar o número de requisições concorrentes.
   - Use um sistema de fila para gerenciar requisições entrantes e rejeitar ou atrasar requisições quando o serviço está sob carga pesada.

## Conclusão

As padronesses de resiliência são cruciais para construir aplicativos de microserviços confiáveis e robustos. Ao implementar essas padronesses, você pode garantir que seus microserviços lidem com falhas de forma elegante e mantenham alta disponibilidade mesmo na presença de falhas. A escolha da padroness depende das exigências específicas do seu aplicativo e da natureza dos serviços envolvidos.