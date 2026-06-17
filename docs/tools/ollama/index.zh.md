---
title: Ollama - 本地大语言模型管理
description: Ollama 是一个开源工具，用于在本地运行和管理大语言模型（LLM），提供简单的 CLI 和本地 REST API。
created: 2026-06-16
tags:
  - ollama
  - llm
  - local-ai
  - open-source
  - devtools
status: draft
---

# Ollama: 在本地运行大语言模型

Ollama 是一个免费的开源框架，让您在自己的机器上下载、运行和管理大语言模型（LLM）变得极其简单。它将模型权重、配置以及基于 `llama.cpp` 的优化推理引擎打包成单个文件，通过一条命令抽象掉 GPU 加速、量化和依赖管理。

## 为什么选择 Ollama？

- **隐私与安全** – 所有计算均在本地进行；数据永远不会离开您的设备。
- **离线能力** – 模型下载完成后，无需互联网连接即可运行。
- **成本效益** – 无 API 使用费用。可以在自己的硬件上随意运行模型。
- **低延迟** – 零网络往返，支持更快的迭代周期。
- **完全控制** – 自定义提示词、系统消息、参数，甚至通过 `Modelfile` 创建新的复合模型。

## 安装

选择你的平台：

```bash
# macOS (Homebrew)
brew install ollama

# Linux (automated script)
curl -fsSL https://ollama.com/install.sh | sh

# Windows – Download the official installer from https://ollama.com
# The installer automatically configures WSL2 and adds `ollama` to PATH.

# Docker (any OS)
docker run -d \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama
```

> **注意：** 在 Linux 上，如果使用 GPU 加速，请确保你的用户属于 `video` 和 `render` 用户组（`sudo usermod -aG video,render $USER`）。

## 基本用法

### 1. 交互式运行聊天

```bash
ollama run llama3.2
```

如果模型尚未缓存，此命令会先拉取模型，然后打开一个交互式聊天会话。输入 `/bye` 退出。

### 2. 管理模型

```bash
# List downloaded models
ollama list

# Download a model without running it
ollama pull mistral

# Remove a model from local storage
ollama rm phi
```

### 3. 一次性生成（非交互式）

```bash
ollama run llama3.2 "What is the capital of France?"
```

### 4. 使用 REST API

Ollama 在端口 `11434` 上暴露了一个与 OpenAI 兼容的 API。你可以使用 `curl` 或任何 HTTP 客户端：

**Generate（简单补全）：**
```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama3.2",
    "prompt": "Hello, how are you?",
    "stream": false
  }'
```

**Chat（对话）：**
```bash
curl http://localhost:11434/api/chat \
  -d '{
    "model": "llama3.2",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "List three benefits of local AI."}
    ],
    "stream": false
  }'
```

API 还支持流式输出（设置 `"stream": true`），并且通过将基础 URL 指向 `http://localhost:11434/v1`，可以完全兼容 OpenAI 客户端库（`openai`、`langchain` 等）。

## 使用 Modelfile 自定义模型

`Modelfile` 是一个类似 Docker 的描述文件，允许你设置参数、系统提示词，甚至组合多个模型。

示例 `Modelfile`：
```
FROM llama3.2

# Set a custom system prompt
SYSTEM "You are a helpful assistant that speaks like a pirate."

# Override default generation parameters
PARAMETER temperature 0.8
PARAMETER top_p 0.9
```

构建并运行：
```bash
ollama create pirate-bot -f ./Modelfile
ollama run pirate-bot
```

你还可以使用 `FROM` 引用其他模型（包括 GGUF 文件）来创建分层或微调版本。

## 关键特性

| 特性 | 描述 |
|---------|-------------|
| **丰富的模型库** | 数百个可用模型（Llama 3、Mistral、Gemma、Phi、Qwen、DeepSeek、CodeGemma 等），并带有不同大小和量化版本的标签。 |
| **GPU 加速** | 支持 NVIDIA CUDA、AMD ROCm 和 Apple Metal 进行硬件加速推理。 |
| **并发请求** | 高效地排队并并行处理多个生成/聊天请求。 |
| **OpenAI 兼容 API** | 即插即用替代 OpenAI API – 只需在应用程序中更改一个 base URL 即可在本地运行。 |
| **Modelfile** | 自定义系统提示词、参数，甚至创建新的复合模型。 |
| **跨平台** | macOS、Linux、Windows（WSL2）和 Docker。 |
| **轻量级** | 二进制文件和容器镜像体积小；依赖最小化。 |
| **日志与监控** | 服务器日志输出到标准输出；健康检查端点为 `http://localhost:11434/api/tags`。 |

## 使用场景

- **本地聊天和个人助手** – 无云端依赖的私密对话式 AI。
- **离线代码助手** – 完全离线运行 CodeGemma、DeepSeek‑Coder 或 StarCoder。
- **RAG 管道** – 作为本地文档的检索增强生成（RAG）的 LLM 后端（例如使用 LangChain 或 LlamaIndex）。
- **快速原型开发** – 在投入付费 API 之前，尝试各种提示词、模型和参数。
- **自动化** – 从 CI/CD 管道、本地脚本或 cron 作业中调用 API。
- **教育与研究** – 研究模型行为、测试微调或审计输出，无需将数据发送到外部。

## 历史

Ollama 由 Jeffrey Morgan 于 2023 年初创建，并迅速成为本地运行大语言模型的事实标准。它的简洁性——下载模型并在几秒钟内开始聊天——解决了设置复杂 Python 环境和底层推理引擎的主要痛点。该项目随着 Llama 2 和 Mistral 等开源权重模型的发布而迅速被采用，并在社区贡献和不断扩展的模型生态系统中持续发展。

更多详情，请访问 [ollama.com](https://ollama.com) 或查看 [GitHub 仓库](https://github.com/ollama/ollama)。