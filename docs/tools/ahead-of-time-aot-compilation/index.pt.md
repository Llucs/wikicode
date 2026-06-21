---
title: Compilação Antecipada (AOT)
description: Uma técnica de otimização de build onde o código é compilado antes da execução para melhorar performance, inicialização instantânea e deployments menores.
created: 2026-06-21
tags:
  - compilation
  - aot
  - native-image
  - performance
  - graalvm
  - dotnet
  - go
  - rust
status: draft
---

# Compilação Antecipada (AOT)

## O que é Compilação Antecipada?

A compilação Antecipada (AOT) é o processo de traduzir código fonte de uma linguagem de programação de alto nível ou representação intermediária (como .NET IL, Java bytecode ou LLVM IR) em código de máquina nativo **antes** da execução, geralmente em tempo de build. Isso contrasta com a compilação Just-in-Time (JIT) que realiza a compilação em tempo de execução.

Linguagens como C, C++, Go e Rust são inerentemente compiladas com AOT. Linguagens gerenciadas modernas também suportam AOT por meio de toolchains especializados, como GraalVM Native Image para Java, NativeAOT para .NET e Angular AOT para TypeScript.

## Por que Usar Compilação AOT?

- **Inicialização Instantânea** – Sem fase de warm-up; o código nativo executa imediatamente.
- **Desempenho Determinístico** – Sem pausas do JIT durante a execução, reduzindo a latência de cauda (tail latency).
- **Menor Consumo de Memória** – Nenhum compilador JIT ou dados de compilação em tempo de execução são necessários.
- **Deployments Menores** – Executáveis de arquivo único estaticamente linkados levam a imagens de contêiner mínimas.
- **Otimização de Cold-Start** – Essencial para aplicações serverless, edge e containerizadas.

## Instalação

### GraalVM Native Image (Java)

1. Baixe o GraalVM de [graalvm.org](https://graalvm.org).
2. Defina `JAVA_HOME` e adicione `bin` ao `PATH`.
3. Instale a ferramenta `native-image`:
   ```bash
   gu install native-image
   ```

### .NET NativeAOT

Requer .NET 7 ou superior (suporte completo no .NET 8+). A workload está incluída no SDK.

### Go (AOT por padrão)

Nenhuma instalação extra – o compilador `go` padrão realiza AOT.

### Rust (AOT por padrão)

Instale via `rustup` (ex.: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`).

## Uso

### Java com GraalVM Native Image

```bash
native-image -jar myapp.jar myapp-native
```

Exemplo de saída:
```
================================================================================
GraalVM Native Image: Generating 'myapp-native' (executable)...
================================================================================
```

### .NET NativeAOT

```bash
dotnet publish -c Release -r linux-x64 -p:PublishAot=true
```

A saída é um executável nativo independente no diretório `bin/Release/net8.0/linux-x64/publish/`.

### Go (AOT implícito)

```bash
go build -o myapp main.go
```

O binário produzido é autocontido e executa imediatamente sem um runtime.

### Rust

```bash
cargo build --release
```

O binário resultante em `target/release/` é compilado com AOT e frequentemente se beneficia de Otimização Guiada por Perfil (PGO) para obter desempenho ainda melhor.

## Principais Características

### 1. Zero Warm-Up

Como todo o código já está compilado, as aplicações iniciam e atingem o desempenho máximo instantaneamente.

*Exemplo (Java):*
```bash
time java -jar myapp.jar      # JIT – may take seconds
time ./myapp-native           # AOT – starts in milliseconds
```

### 2. Latência Determinística

Sem pausas relacionadas a GC e JIT. Crítico para sistemas em tempo real, plataformas de trading e negociação de alta frequência.

### 3. Menor Consumo de Recursos

- **GraalVM Native Image** pode reduzir o tamanho da imagem de >200 MB (JVM+app) para <20 MB.
- **.NET NativeAOT** produz binários que incluem apenas componentes de runtime necessários.

### 4. Eliminação de Código Morto

Analisadores AOT removem código inacessível, resultando em executáveis menores e segurança aprimorada.

### 5. Otimização Guiada por Perfil (PGO)

Combinado com AOT, os dados de perfil PGO coletados de execuções de teste podem ser usados em tempo de build para otimizar ainda mais o binário.

*Exemplo (Rust):*
```bash
RUSTFLAGS="-Cprofile-generate=/tmp/pgo-data" cargo build --release
# Run training workload
RUSTFLAGS="-Cprofile-use=/tmp/pgo-data" cargo build --release
```

## Limitações

- **Reflexão / Carregamento Dinâmico** – Deve ser configurado explicitamente (ex.: `reflect-config.json` para Native Image).
- **Tempo de Build** – A compilação AOT é mais lenta que JIT.
- **Desempenho Máximo** – JIT de longa duração com profiling ainda pode superar AOT em workloads pesados de CPU.
- **Suporte** – Nem todas as bibliotecas e frameworks são compatíveis com AOT.

## Conclusão

A compilação AOT é uma técnica fundamental para aplicações modernas cloud-native, serverless e edge. Ao sacrificar alguma flexibilidade em tempo de execução, ela oferece velocidade de inicialização incomparável, desempenho previsível e uso mínimo de recursos. Ferramentas como GraalVM Native Image, .NET NativeAOT, Go e Rust tornam o AOT acessível e prático para uso em produção.