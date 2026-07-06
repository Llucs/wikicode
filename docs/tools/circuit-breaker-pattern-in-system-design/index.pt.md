---
title: Patrão do Interruptor de Circuito em Projeto de Sistema
description: Uma mecanização usada para prevenir falhas que ocorrem em uma parte de um sistema distribuído de causarem falhas cascata em outras partes, melhorando a confiabilidade e a estabilidade geral do sistema.
created: 2026-07-06
tags:
  - projeto de sistema
  - microserviços
  - resiliência
  - tolerância a falhas
status: rascunho
---

# Patrão do Interruptor de Circuito em Projeto de Sistema

O Patrão do Interruptor de Circuito é um padrão de projeto usado em engenharia de software para prevenir falhas que ocorrem em um sistema distribuído de causarem falhas cascata em outras partes. Ele funciona como uma mecanização de controle que monitora o sucesso ou falha de operações remotas e altera o comportamento do sistema quando as falhas ultrapassem um determinado limite. Quando o interruptor de circuito estiver "aberto," ele parará de permitir que novas solicitações cheguem ao serviço downstream, retornando uma resposta pré-definida ao cliente em vez disso. Assim que o serviço retornar a um estado estável, o interruptor de circuito pode ser "fechado" novamente, permitindo que o sistema tente a operação novamente.

## Características Principais

1. **Detecção de Inatividade de Serviço**: O interruptor de circuito monitora o status de serviços dependentes ou componentes. Se um determinado número de falhas ocorrerem dentro de um intervalo específico de tempo, o interruptor de circuito tripa.
2. **Mecanismo de Recuperação**: Quando o interruptor de circuito estiver aberto, ele fornece um mecanismo de recuperação que retorna uma resposta pré-definida ao cliente, evitando a falha total da aplicação.
3. **Reexecuções Atrasadas**: Em vez de reexecutar solicitações falhas imediatamente, o interruptor de circuito permite um atraso, o que pode ajudar o sistema a se recuperar de problemas transitórios.
4. **Estado do Interruptor de Circuito**: O interruptor de circuito mantém um estado (aberto/fechado) e transita entre os estados com base no sucesso ou falha do serviço.

## Instalação e Configuração

A implementação específica do Patrão do Interruptor de Circuito pode variar dependendo da linguagem de programação e framework sendo usado. Aqui está uma configuração básica usando uma biblioteca Java populosa chamada Hystrix.

### Adicionar Dependência

Para Maven, inclua a biblioteca Hystrix no seu projeto:

```xml
<dependency>
    <groupId>com.netflix.hystrix</groupId>
    <artifactId>hystrix-javanica</artifactId>
    <version>1.5.18</version>
</dependency>
```

### Criar uma Comando

Defina um comando Hystrix para o serviço que você deseja proteger.

```java
import com.netflix.hystrix.HystrixCommand;
import com.netflix.hystrix.HystrixCommandGroupKey;

public class MyServiceCommand extends HystrixCommand<String> {
    public MyServiceCommand() {
        super(HystrixCommandGroupKey.Factory.asKey("MyServiceGroup"));
    }

    @Override
    protected String run() throws Exception {
        // Chame o serviço ou operação aqui
        return callService();
    }

    @Override
    protected String getFallback() {
        return "Resposta de recuperação";
    }
}
```

### Executar o Comando

Use o comando para executar a chamada de serviço.

```java
MyServiceCommand command = new MyServiceCommand();
String result = command.execute();
```

## Uso Básico

1. **Iniciação**: Crie uma instância do comando Hystrix.
2. **Execução**: Use o método `execute` para executar o comando. Se o serviço não estiver disponível, o método de recuperação será invocado.
3. **Método de Recuperação**: Defina um método de recuperação que retorne uma resposta pré-definida.

```java
@Override
protected String run() throws Exception {
    // Chame o serviço ou operação aqui
    return callService();
}

@Override
protected String getFallback() {
    return "Resposta de recuperação";
}
```

4. **Monitoramento**: Use o Hystrix Dashboard para monitorar as estatísticas de execução e a saúde dos comandos.

## Casos de Uso

1. **Comunicação de Microserviços**: Em arquiteturas de microserviços, onde os serviços se comunicam entre si, o Patrão do Interruptor de Circuito previne que uma falha em um serviço cause falhas cascata em outros serviços.
2. **Gatilho API**: Quando uma API gateway gerencia o acesso a múltiplos serviços, o Patrão do Interruptor de Circuito previne que falhas em um serviço afetem a API inteira.
3. **Serviços de Terceiros**: Ao integrar com serviços de terceiros ou APIs externas, o Patrão do Interruptor de Circuito ajuda a lidar com falhas transitórias de forma graciosamente.
4. **Acesso ao Banco de Dados**: Em interações com bancos de dados, o padrão pode prevenir falhas devido a problemas temporários de conexão ou sobrecarga de banco de dados.

## Conclusão

O Patrão do Interruptor de Circuito é uma ferramenta poderosa para gerenciar falhas em sistemas distribuídos, garantindo que falhas em uma parte do sistema não derrubem o sistema inteiro. Ao implementar este padrão, os desenvolvedores podem construir aplicativos mais resistentes e escaláveis.

---