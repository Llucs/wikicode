---
title: 事前コンパイル (AOT)
description: 実行前にコードをコンパイルすることで、パフォーマンスの向上、即時起動、そしてより小規模なデプロイを実現するビルド最適化手法です。
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

# 事前コンパイル (AOT)

## 事前コンパイルとは？

事前コンパイル (AOT) は、高水準プログラミング言語のソースコードまたは中間表現（.NET IL、Java バイトコード、LLVM IR など）を、実行**前**（通常はビルド時）にネイティブマシンコードに変換するプロセスです。これは、実行時にコンパイルを行う Just-in-Time (JIT) コンパイルとは対照的です。

C、C++、Go、Rust などの言語は本質的に AOT コンパイルされます。最近のマネージド言語も、Java 用の GraalVM Native Image、.NET 用の NativeAOT、TypeScript 用の Angular AOT などの専門的なツールチェーンを通じて AOT をサポートしています。

## AOT コンパイルを使用する理由

AOT には、JIT やインタプリタ実行に比べていくつかの重要な利点があります。

- **即時起動** – ウォームアップフェーズが不要で、ネイティブコードが即座に実行されます。
- **決定論的パフォーマンス** – 実行中に JIT による一時停止がなく、テールレイテンシが低減します。
- **低メモリフットプリント** – JIT コンパイラやランタイムコンパイルデータが不要です。
- **より小規模なデプロイ** – 静的にリンクされた単一ファイルの実行可能ファイルにより、コンテナイメージを最小限に抑えられます。
- **コールドスタート最適化** – サーバーレス、エッジ、コンテナ化アプリケーションに不可欠です。

## インストール

AOT ツールチェーンはプラットフォームによって異なります。以下は一般的なセットアップです。

### GraalVM Native Image (Java)

1. [graalvm.org](https://graalvm.org) から GraalVM をダウンロードします。
2. `JAVA_HOME` を設定し、`bin` を `PATH` に追加します。
3. `native-image` ツールをインストールします:
   ```bash
   gu install native-image
   ```

### .NET NativeAOT

.NET 7 以降が必要です（.NET 8 以降で完全サポート）。ワークロードは SDK に含まれています。

### Go (AOT by default)

追加のインストールは不要です – 標準の `go` コンパイラが AOT を実行します。

### Rust (AOT by default)

`rustup` を使用してインストールします（例：`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`）。

## 使用方法

### Java with GraalVM Native Image

```bash
native-image -jar myapp.jar myapp-native
```

出力例:
```
================================================================================
GraalVM Native Image: Generating 'myapp-native' (executable)...
================================================================================
```

### .NET NativeAOT

```bash
dotnet publish -c Release -r linux-x64 -p:PublishAot=true
```

出力は、`bin/Release/net8.0/linux-x64/publish/` ディレクトリにあるスタンドアロンのネイティブ実行可能ファイルです。

### Go (AOT implicit)

```bash
go build -o myapp main.go
```

生成されたバイナリは自己完結型であり、ランタイムなしで即座に実行されます。

### Rust

```bash
cargo build --release
```

`target/release/` にある結果のバイナリは AOT コンパイルされており、さらに優れたパフォーマンスを得るためにプロファイルガイド最適化 (PGO) の恩恵を受けることがよくあります。

## 主な機能

### 1. ゼロウォームアップ

すべてのコードがすでにコンパイルされているため、アプリケーションは即座に起動し、ピークパフォーマンスに達します。

*例 (Java):*
```bash
time java -jar myapp.jar      # JIT – may take seconds
time ./myapp-native           # AOT – starts in milliseconds
```

### 2. 決定論的レイテンシ

GC および JIT 関連の一時停止がありません。リアルタイムシステム、取引プラットフォーム、高頻度取引にとって重要です。

### 3. より小さいフットプリント

- **GraalVM Native Image** は、イメージサイズを >200 MB (JVM+アプリ) から <20 MB に削減できます。
- **.NET NativeAOT** は、必要なランタイムコンポーネントのみを含むバイナリを生成します。

### 4. デッドコード除去

AOT アナライザーは到達不能コードを除去し、より小さな実行可能ファイルとセキュリティの向上をもたらします。

### 5. プロファイルガイド最適化 (PGO)

AOT と組み合わせることで、テスト実行から収集された PGO プロファイルデータをビルド時に使用して、バイナリをさらに最適化できます。

*例 (Rust):*
```bash
RUSTFLAGS="-Cprofile-generate=/tmp/pgo-data" cargo build --release
# Run training workload
RUSTFLAGS="-Cprofile-use=/tmp/pgo-data" cargo build --release
```

## 制限事項

- **リフレクション / 動的読み込み** – 明示的に設定する必要があります（例：Native Image の `reflect-config.json`）。
- **ビルド時間** – AOT コンパイルは JIT よりも低速です。
- **ピークパフォーマンス** – プロファイリングを伴う長期実行 JIT は、CPU 負荷の高いワークロードでは AOT を依然として上回る可能性があります。
- **サポート** – すべてのライブラリとフレームワークが AOT 互換であるわけではありません。

## まとめ

AOT コンパイルは、最新のクラウドネイティブ、サーバーレス、エッジアプリケーションの基礎となる技術です。実行時の柔軟性を一部犠牲にすることで、比類のない起動速度、予測可能なパフォーマンス、最小限のリソース使用量を実現します。GraalVM Native Image、.NET NativeAOT、Go、Rust などのツールにより、AOT は本番環境での利用が可能かつ実用的になっています。