---
title: Ollama - ローカルLLM管理
description: Ollamaは、ローカルで大規模言語モデル（LLM）を実行・管理するためのオープンソースツールであり、シンプルなCLIとローカルREST APIを提供します。
created: 2026-06-16
tags:
  - ollama
  - llm
  - local-ai
  - open-source
  - devtools
status: draft
---

# Ollama: 大規模言語モデルをローカルで実行する

Ollamaは、自分のマシン上で大規模言語モデル（LLM）をダウンロード、実行、管理するのを驚くほど簡単にする、無料のオープンソースフレームワークです。モデルの重み、設定、最適化された推論エンジン（`llama.cpp` ベース）を単一のパッケージにまとめ、GPUアクセラレーション、量子化、依存関係管理を単一のコマンドで抽象化します。

## なぜOllamaなのか？

- **プライバシーとセキュリティ** – すべての計算はローカルで行われ、データがデバイス外に出ることはありません。
- **オフライン機能** – モデルをダウンロードすれば、インターネット接続なしで実行できます。
- **コスト効率** – API利用料金は発生しません。自分のハードウェア上で好きなだけモデルを実行できます。
- **レイテンシ** – ネットワークのラウンドトリップがゼロで、より迅速な反復サイクルを実現します。
- **完全な制御** – プロンプト、システムメッセージ、パラメータをカスタマイズでき、`Modelfile` を使って新しい複合モデルを作成することもできます。

## インストール

お使いのプラットフォームを選択してください:

```bash
# macOS (Homebrew)
brew install ollama

# Linux (自動スクリプト)
curl -fsSL https://ollama.com/install.sh | sh

# Windows – 公式インストーラを https://ollama.com からダウンロードしてください
# インストーラは自動的にWSL2を設定し、`ollama` をPATHに追加します。

# Docker (任意のOS)
docker run -d \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama
```

> **注意:** LinuxでGPUアクセラレーションを使用する場合は、`video` グループと `render` グループにユーザーが所属していることを確認してください (`sudo usermod -aG video,render $USER`)。

## 基本的な使い方

### 1. チャットを対話的に実行する

```bash
ollama run llama3.2
```

これにより、モデルがまだキャッシュされていなければプルされ、対話型チャットセッションが開始されます。終了するには `/bye` と入力します。

### 2. モデルを管理する

```bash
# ダウンロード済みモデルの一覧表示
ollama list

# 実行せずにモデルをダウンロード
ollama pull mistral

# ローカルストレージからモデルを削除
ollama rm phi
```

### 3. ワンショット生成（非対話型）

```bash
ollama run llama3.2 "フランスの首都はどこですか？"
```

### 4. REST APIを使用する

Ollamaは、ポート`11434`でOpenAI互換のAPIを公開します。`curl` や任意のHTTPクライアントを使用できます:

**生成（シンプルな補完）:**
```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama3.2",
    "prompt": "こんにちは、お元気ですか？",
    "stream": false
  }'
```

**チャット（会話形式）:**
```bash
curl http://localhost:11434/api/chat \
  -d '{
    "model": "llama3.2",
    "messages": [
      {"role": "system", "content": "あなたは役立つアシスタントです。"},
      {"role": "user", "content": "ローカルAIの利点を3つ挙げてください。"}
    ],
    "stream": false
  }'
```

APIはストリーミングもサポートしており（`"stream": true` を設定）、ベースURLを `http://localhost:11434/v1` に指定することでOpenAIクライアントライブラリ（`openai`、`langchain` など）と完全に互換性があります。

## Modelfileでモデルをカスタマイズする

`Modelfile` はDockerのような記述子で、パラメータ、システムプロンプトの設定、さらには複数のモデルの組み合わせを可能にします。

`Modelfile` の例:
```
FROM llama3.2

# カスタムシステムプロンプトを設定
SYSTEM "あなたは海賊のように話す役立つアシスタントです。"

# デフォルトの生成パラメータを上書き
PARAMETER temperature 0.8
PARAMETER top_p 0.9
```

ビルドして実行:
```bash
ollama create pirate-bot -f ./Modelfile
ollama run pirate-bot
```

`FROM` を使用して他のモデル（GGUFファイルを含む）を参照することで、レイヤー化されたバージョンやファインチューニングされたバージョンを作成することもできます。

## 主な機能

| 機能 | 説明 |
|---------|-------------|
| **広範なモデルライブラリ** | 数百ものモデルが利用可能（Llama 3、Mistral、Gemma、Phi、Qwen、DeepSeek、CodeGemmaなど）。サイズや量子化のバリエーションもタグで用意。 |
| **GPUアクセラレーション** | NVIDIA CUDA、AMD ROCm、Apple Metalをサポートし、ハードウェア高速化推論を実現。 |
| **同時リクエスト** | 複数のgenerate/chatリクエストを効率的にキューイングし、並列処理。 |
| **OpenAI互換API** | OpenAIのAPIとドロップイン置換可能 – アプリケーションのベースURLを変更するだけでローカル実行に切り替え。 |
| **Modelfile** | システムプロンプト、パラメータのカスタマイズ、新しい複合モデルの作成が可能。 |
| **クロスプラットフォーム** | macOS、Linux、Windows（WSL2）、Docker対応。 |
| **軽量** | バイナリとコンテナイメージは小さく、依存関係も最小限。 |
| **ログとモニタリング** | サーバーログは標準出力に出力。ヘルスチェックエンドポイントは `http://localhost:11434/api/tags`。 |

## 使用例

- **ローカルチャット＆パーソナルアシスタント** – クラウド依存なしのプライベートな対話型AI。
- **オフラインコードアシスタント** – CodeGemma、DeepSeek-Coder、StarCoderを完全オフラインで実行。
- **RAGパイプライン** – ローカルドキュメントに対するRetrieval-Augmented GenerationのLLMバックエンドとして利用（例：LangChainやLlamaIndexと組み合わせ）。
- **迅速なプロトタイピング** – 有料APIにコミットする前に、プロンプト、モデル、パラメータを実験。
- **自動化** – CI/CDパイプライン、ローカルスクリプト、cronジョブからAPIを呼び出し。
- **教育と研究** – モデルの動作を研究し、ファインチューニングをテストし、データを外部に送信せずに出力を監査。

## 歴史

Ollamaは2023年初頭にJeffrey Morganによって作成され、ローカルでLLMを実行するための事実上の標準として急速に普及しました。そのシンプルさ（モデルをダウンロードして数秒でチャットを開始）は、複雑なPython環境や低レベルの推論エンジンをセットアップするという主要な障壁を解決しました。このプロジェクトは、Llama 2やMistralのようなオープンウェイトモデルのリリースとともに急速に採用され、コミュニティの貢献と拡大するモデルエコシステムによって進化を続けています。

詳細については、[ollama.com](https://ollama.com) をご覧いただくか、[GitHubリポジトリ](https://github.com/ollama/ollama) をチェックしてください。