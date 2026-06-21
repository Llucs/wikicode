---
title: Compilación Ahead-of-Time (AOT)
description: Una técnica de optimización de compilación donde el código se compila antes de la ejecución para mejorar el rendimiento, el inicio instantáneo y despliegues más pequeños.
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

# Compilación Ahead-of-Time (AOT)

## ¿Qué es la compilación Ahead-of-Time?

La compilación Ahead-of-Time (AOT) es el proceso de traducir código fuente de lenguaje de programación de alto nivel o representación intermedia (como .NET IL, bytecode de Java o LLVM IR) a código máquina nativo **antes** de la ejecución, típicamente en tiempo de compilación. Esto contrasta con la compilación Just-in-Time (JIT) que realiza la compilación en tiempo de ejecución.

Lenguajes como C, C++, Go y Rust son inherentemente compilados con AOT. Los lenguajes administrados modernos también soportan AOT a través de cadenas de herramientas especializadas, como GraalVM Native Image para Java, NativeAOT para .NET y Angular AOT para TypeScript.

## ¿Por qué usar la compilación AOT?

La compilación AOT ofrece varias ventajas clave sobre la ejecución JIT o interpretada:

- **Inicio Instantáneo** – Sin fase de calentamiento; el código nativo se ejecuta inmediatamente.
- **Rendimiento Determinista** – Sin pausas de JIT durante la ejecución, reduciendo la latencia de cola.
- **Menor Huella de Memoria** – No requiere compilador JIT ni datos de compilación en tiempo de ejecución.
- **Despliegues Más Pequeños** – Ejecutables de un solo archivo y enlazados estáticamente que generan imágenes de contenedor mínimas.
- **Optimización de Arranque en Frío** – Esencial para aplicaciones serverless, edge y containerizadas.

## Instalación

La cadena de herramientas AOT varía según la plataforma. A continuación se muestran configuraciones comunes:

### GraalVM Native Image (Java)

1. Descargar GraalVM desde [graalvm.org](https://graalvm.org).
2. Establecer `JAVA_HOME` y agregar `bin` a `PATH`.
3. Instalar la herramienta `native-image`:
   ```bash
   gu install native-image
   ```

### .NET NativeAOT

Requiere .NET 7 o posterior (soporte completo en .NET 8+). La carga de trabajo está incluida en el SDK.

### Go (AOT por defecto)

No se requiere instalación adicional: el compilador `go` estándar realiza AOT.

### Rust (AOT por defecto)

Instalar mediante `rustup` (p. ej., `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`).

## Uso

### Java con GraalVM Native Image

```bash
native-image -jar myapp.jar myapp-native
```

Ejemplo de salida:
```
================================================================================
GraalVM Native Image: Generating 'myapp-native' (executable)...
================================================================================
```

### .NET NativeAOT

```bash
dotnet publish -c Release -r linux-x64 -p:PublishAot=true
```

La salida es un ejecutable nativo independiente en el directorio `bin/Release/net8.0/linux-x64/publish/`.

### Go (AOT implícito)

```bash
go build -o myapp main.go
```

El binario producido es autónomo y se ejecuta inmediatamente sin un entorno de ejecución.

### Rust

```bash
cargo build --release
```

El binario resultante en `target/release/` se compila con AOT y a menudo se beneficia de la Optimización Guiada por Perfiles (PGO) para un rendimiento aún mejor.

## Características Principales

### 1. Cero Calentamiento

Debido a que todo el código ya está compilado, las aplicaciones se inician y alcanzan el máximo rendimiento al instante.

*Ejemplo (Java):*
```bash
time java -jar myapp.jar      # JIT – may take seconds
time ./myapp-native           # AOT – starts in milliseconds
```

### 2. Latencia Determinista

Sin pausas relacionadas con GC y JIT. Crítico para sistemas en tiempo real, plataformas de trading y comercio de alta frecuencia.

### 3. Huella Más Pequeña

- **GraalVM Native Image** puede reducir el tamaño de la imagen de >200 MB (JVM+app) a <20 MB.
- **.NET NativeAOT** produce binarios que incluyen solo los componentes de tiempo de ejecución necesarios.

### 4. Eliminación de Código Muerto

Los analizadores AOT eliminan el código inalcanzable, lo que resulta en ejecutables más pequeños y una seguridad mejorada.

### 5. Optimización Guiada por Perfiles (PGO)

Combinado con AOT, los datos de perfil PGO recopilados de ejecuciones de prueba se pueden usar en tiempo de compilación para optimizar aún más el binario.

*Ejemplo (Rust):*
```bash
RUSTFLAGS="-Cprofile-generate=/tmp/pgo-data" cargo build --release
# Run training workload
RUSTFLAGS="-Cprofile-use=/tmp/pgo-data" cargo build --release
```

## Limitaciones

- **Reflexión / Carga Dinámica** – Debe configurarse explícitamente (p. ej., `reflect-config.json` para Native Image).
- **Tiempo de Compilación** – La compilación AOT es más lenta que JIT.
- **Rendimiento Máximo** – El JIT de larga duración con perfiles aún puede superar a AOT en cargas de trabajo intensivas en CPU.
- **Soporte** – No todas las bibliotecas y frameworks son compatibles con AOT.

## Conclusión

La compilación AOT es una técnica fundamental para las aplicaciones modernas cloud-native, serverless y edge. Al sacrificar algo de flexibilidad en tiempo de ejecución, ofrece una velocidad de inicio incomparable, rendimiento predecible y un uso mínimo de recursos. Herramientas como GraalVM Native Image, .NET NativeAOT, Go y Rust hacen que AOT sea accesible y práctico para uso en producción.