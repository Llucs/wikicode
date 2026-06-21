---
title: 提前编译 (AOT)
description: 一种构建优化技术，代码在运行前进行编译，以提高性能、实现即时启动和更小的部署体积。
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

# 提前编译 (AOT)

## 什么是提前编译？

提前编译 (AOT) 是将高级编程语言源代码或中间表示（如 .NET IL、Java 字节码或 LLVM IR）**在执行之前**（通常在构建时）转换为本地机器代码的过程。这不同于在运行时进行编译的即时编译 (JIT)。

像 C、C++、Go 和 Rust 这类语言本质上是 AOT 编译的。现代托管语言也通过专门的工具链支持 AOT，例如用于 Java 的 GraalVM Native Image、用于 .NET 的 NativeAOT 和用于 TypeScript 的 Angular AOT。

## 为什么使用 AOT 编译？

AOT 相较于 JIT 或解释执行具有几个关键优势：

- **即时启动** – 无需预热阶段；本地代码立即执行。
- **确定性性能** – 执行过程中无 JIT 暂停，减少尾部延迟。
- **更低内存占用** – 无需 JIT 编译器或运行时编译数据。
- **更小部署体积** – 静态链接的单文件可执行文件导致最小的容器镜像。
- **冷启动优化** – 对无服务器、边缘计算和容器化应用至关重要。

## 安装

AOT 工具链因平台而异。以下是常见的设置：

### GraalVM Native Image (Java)

1. 从 [graalvm.org](https://graalvm.org) 下载 GraalVM。
2. 设置 `JAVA_HOME` 并将 `bin` 添加到 `PATH`。
3. 安装 `native-image` 工具：
   ```bash
   gu install native-image
   ```

### .NET NativeAOT

需要 .NET 7 或更高版本（在 .NET 8+ 中完全支持）。该工作负载已包含在 SDK 中。

### Go (默认 AOT)

无需额外安装 – 标准的 `go` 编译器执行 AOT。

### Rust (默认 AOT)

通过 `rustup` 安装（例如，`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`）。

## 用法

### Java 与 GraalVM Native Image

```bash
native-image -jar myapp.jar myapp-native
```

示例输出：
```
================================================================================
GraalVM Native Image: Generating 'myapp-native' (executable)...
================================================================================
```

### .NET NativeAOT

```bash
dotnet publish -c Release -r linux-x64 -p:PublishAot=true
```

输出结果是在 `bin/Release/net8.0/linux-x64/publish/` 目录下的独立本地可执行文件。

### Go (隐含 AOT)

```bash
go build -o myapp main.go
```

生成的二进制文件是自包含的，无需运行时即可立即运行。

### Rust

```bash
cargo build --release
```

生成的二进制文件位于 `target/release/` 中，是 AOT 编译的，并且通常通过配置文件引导优化 (PGO) 获得更好的性能。

## 关键特性

### 1. 零预热

因为所有代码都已被编译，应用程序立即启动并达到峰值性能。

*示例 (Java):*
```bash
time java -jar myapp.jar      # JIT – may take seconds
time ./myapp-native           # AOT – starts in milliseconds
```

### 2. 确定性延迟

没有与 GC 和 JIT 相关的暂停。对实时系统、交易平台和高频交易至关重要。

### 3. 更小体积

- **GraalVM Native Image** 可以将镜像大小从 >200 MB（JVM+app）减少到 <20 MB。
- **.NET NativeAOT** 生成仅包含必要运行时组件的二进制文件。

### 4. 死代码消除

AOT 分析器会移除不可达代码，从而生成更小的可执行文件并提高安全性。

### 5. 配置文件引导优化 (PGO)

与 AOT 结合，从测试运行中收集的 PGO 配置文件数据可以在构建时使用，以进一步优化二进制文件。

*示例 (Rust):*
```bash
RUSTFLAGS="-Cprofile-generate=/tmp/pgo-data" cargo build --release
# Run training workload
RUSTFLAGS="-Cprofile-use=/tmp/pgo-data" cargo build --release
```

## 局限性

- **反射 / 动态加载** – 必须显式配置（例如 Native Image 的 `reflect-config.json`）。
- **构建时间** – AOT 编译比 JIT 慢。
- **峰值性能** – 在 CPU 密集型工作负载上，带性能分析的长期运行 JIT 仍可能优于 AOT。
- **支持** – 并非所有库和框架都与 AOT 兼容。

## 结论

AOT 编译是现代云原生、无服务器和边缘计算应用的基础技术。通过牺牲部分运行时灵活性，它提供了无与伦比的启动速度、可预测的性能和最小的资源占用。GraalVM Native Image、.NET NativeAOT、Go 和 Rust 等工具使 AOT 在生产环境中变得可访问且实用。