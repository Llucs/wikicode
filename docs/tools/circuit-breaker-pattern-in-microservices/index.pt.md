---
title: Patterno de Interruptor de Circuito em Microserviços
description: Um padrão de design usado em arquiteturas de microserviços para lidar com falhas de forma elegante, ignorando temporariamente solicitações a um serviço problemático.
created: 2026-07-15
tags:
  - microservices
  - resiliência
  - interruptor de circuito
  - padrão de design
status: draft
---

### Patterno de Interruptor de Circuito em Microserviços

#### O que é o Patterno de Interruptor de Circuito?
O Patterno de Interruptor de Circuito é um padrão de design na engenharia de software que ajuda a gerenciar a resiliência e a confiabilidade de sistemas distribuídos, particularmente em arquiteturas de microserviços. É uma mecanismo para lidar com falhas em chamadas remotas, permitindo que serviços falhem rapidamente e se recuperem de falhas sem causar falhas cascata no sistema.

#### Características Principais
1. **Detecção de Falha**: O Interruptor de Circuito detecta quando um serviço ou chamada de API falha ao alcançar um limite pré-definido de falhas.
2. **Quebrando o Circuito**: Quando o limite é ultrapassado, o Interruptor de Circuito tripula, efetivamente quebrando o circuito por interromper further solicitações de alcançar o serviço problemático.
3. **Mecanismo de Retorno ao Status Anterior**: Em vez de esperar por uma resposta potencialmente falha do serviço, o Interruptor de Circuito gatilha um mecanismo de retorno ao status anterior, que retorna uma resposta pré-definida ou uma mensagem de erro ao chamador.
4. **Tempo de Expansão e Reenvio**: O Interruptor de Circuito pode ser configurado para introduzir um mecanismo de tempo limite e reenvio para lidar com falhas transitórias.
5. **Resetação do Circuito**: Uma vez que o serviço começa a se comportar corretamente novamente, o Interruptor de Circuito reseta e permite que o tráfego seja enviado ao serviço novamente.

#### História
O conceito de Interruptor de Circuito foi introduzido originalmente no domínio de hardware e engenharia elétrica. Foi adaptado posteriormente para engenharia de software, particularmente no contexto de sistemas distribuídos, por Martin Fowler e James Lewis no seu artigo de 2010, "Microservices: Designing Fine-Grained Services," publicado no site MartinFowler.com.

#### Casos de Uso
1. **Lidando com Falhas de Serviço**: Em uma arquitetura de microserviços, se um serviço downstream falhar, o Interruptor de Circuito pode impedir que outros serviços tentem se comunicar com ele, evitando falhas cascata.
2. **Optimização de Desempenho**: Ao quebrar o circuito, o Interruptor de Circuito pode prevenir processamento desnecessário e melhorar o desempenho geral do sistema.
3. **Gerenciamento de Erros**: Fornece um mecanismo para lidar com erros de forma elegante, reduzindo o impacto de falhas no sistema geral.
4. **Monitoramento em Tempo Real**: O Interruptor de Circuito pode ser usado para monitorar a saúde dos serviços e fornecer feedback em tempo real sobre o estado do sistema.

#### Instalação
O padrão de Interruptor de Circuito pode ser implementado usando várias bibliotecas e frameworks dependendo da linguagem de programação e framework em uso. Aqui estão algumas implementações comuns:

- **Java**: Hystrix (de Netflix), Resilience4j e OpenHystrix.
- **.NET**: Polly.
- **Python**: CircuitBreaker.
- **JavaScript**: @liarnp/circuitbreaker.

Por exemplo, usando Resilience4j em Java:

```java
import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;

public class CircuitBreakerExample {
    private final CircuitBreakerRegistry circuitBreakerRegistry;
    private final CircuitBreaker circuitBreaker;

    public CircuitBreakerExample() {
        circuitBreakerRegistry = CircuitBreakerRegistry.of("exampleCircuitBreaker");
        circuitBreaker = circuitBreakerRegistry.circuitBreaker("exampleCircuitBreaker");
    }

    public void performCall() {
        if (circuitBreaker.isOpen()) {
            System.out.println("Circuit breaker is open, falling back...");
            return;
        }
        try {
            // Perform the call to the service
        } catch (Exception e) {
            circuitBreakerRegistry.fail(CircuitBreaker.of("exampleCircuitBreaker"));
        }
    }
}
```

#### Uso Básico
1. **Inicialização**: Inicialize o Interruptor de Circuito com a configuração desejada e registre-o com o registro de Interruptor de Circuito.
2. **Uso**: Use o Interruptor de Circuito para embrulhar a chamada de serviço. Se a chamada falhar, o Interruptor de Circuito quebrará o circuito, e as chamadas subsequentes usarão o mecanismo de retorno ao status anterior.
3. **Resetação**: Permita que o Interruptor de Circuito se resete por si mesmo quando o serviço começar a funcionar novamente.

Implementando o padrão de Interruptor de Circuito, os desenvolvedores podem aprimorar a resiliência e a confiabilidade de seus microserviços, garantindo que o sistema possa lidar com falhas de forma elegante e manter alta disponibilidade.

---