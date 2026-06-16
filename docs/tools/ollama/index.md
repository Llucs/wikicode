---
title: Ollama - Local LLM Management
description: Ollama is an open-source tool for running and managing large language models (LLMs) locally, providing a simple CLI and local REST API.
created: 2026-06-16
tags:
  - ollama
  - llm
  - local-ai
  - open-source
  - devtools
status: draft
---

# Ollama: Run Large Language Models Locally

Ollama is a free, open-source framework that makes it trivially easy to download, run, and manage large language models (LLMs) on your own machine. It bundles model weights, configuration, and an optimized inference engine (based on `llama.cpp`) into a single package, abstracting away GPU acceleration, quantization, and dependency management behind a single command.

## Why Ollama?

- **Privacy & Security** – All computation happens locally; no data ever leaves your device.
- **Offline Capability** – Once a model is downloaded, you can run it without an Internet connection.
- **Cost Efficiency** – No API usage fees. Run models as much as you want on your own hardware.
- **Latency** – Zero network round-trips, enabling faster iteration cycles.
- **Full Control** – Customize prompts, system messages, parameters, and even create new composite models via `Modelfile`.

## Installation

Choose your platform:

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

> **Note:** On Linux, ensure your user is in the `video` and `render` groups if using GPU acceleration (`sudo usermod -aG video,render $USER`).

## Basic Usage

### 1. Run a Chat Interactively

```bash
ollama run llama3.2
```

This pulls the model if not already cached, then opens an interactive chat session. Type `/bye` to exit.

### 2. Manage Models

```bash
# List downloaded models
ollama list

# Download a model without running it
ollama pull mistral

# Remove a model from local storage
ollama rm phi
```

### 3. One‑Shot Generation (Non‑Interactive)

```bash
ollama run llama3.2 "What is the capital of France?"
```

### 4. Use the REST API

Ollama exposes an OpenAI‑compatible API on port `11434`. You can use `curl` or any HTTP client:

**Generate (simple completion):**
```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama3.2",
    "prompt": "Hello, how are you?",
    "stream": false
  }'
```

**Chat (conversational):**
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

The API also supports streaming (set `"stream": true`) and is fully compatible with the OpenAI client libraries (`openai`, `langchain`, etc.) by pointing the base URL to `http://localhost:11434/v1`.

## Customizing Models with a Modelfile

A `Modelfile` is a Docker‑like descriptor that lets you set parameters, system prompts, or even combine multiple models.

Example `Modelfile`:
```
FROM llama3.2

# Set a custom system prompt
SYSTEM "You are a helpful assistant that speaks like a pirate."

# Override default generation parameters
PARAMETER temperature 0.8
PARAMETER top_p 0.9
```

Build and run:
```bash
ollama create pirate-bot -f ./Modelfile
ollama run pirate-bot
```

You can also use `FROM` to reference other models (including GGUF files) to create layered or fine‑tuned versions.

## Key Features

| Feature | Description |
|---------|-------------|
| **Extensive Model Library** | Hundreds of models available (Llama 3, Mistral, Gemma, Phi, Qwen, DeepSeek, CodeGemma, etc.) with tags for different sizes and quantizations. |
| **GPU Acceleration** | Supports NVIDIA CUDA, AMD ROCm, and Apple Metal for hardware‑accelerated inference. |
| **Concurrent Requests** | Efficiently queues and processes multiple generate/chat requests in parallel. |
| **OpenAI‑Compatible API** | Drop‑in replacement for OpenAI’s API – change one base URL in your application and run locally. |
| **Modelfile** | Customize system prompts, parameters, and even create new composite models. |
| **Cross‑Platform** | macOS, Linux, Windows (WSL2), and Docker. |
| **Lightweight** | Binaries and container images are small; dependencies are minimal. |
| **Logging & Monitoring** | Server logs to stdout; health endpoint at `http://localhost:11434/api/tags`. |

## Use Cases

- **Local Chat & Personal Assistant** – Private conversational AI with no cloud dependency.
- **Offline Code Assistant** – Run CodeGemma, DeepSeek‑Coder, or StarCoder completely offline.
- **RAG Pipelines** – Serve as the LLM backend for Retrieval‑Augmented Generation over local documents (e.g., with LangChain or LlamaIndex).
- **Rapid Prototyping** – Experiment with prompts, models, and parameters before committing to a paid API.
- **Automation** – Call the API from CI/CD pipelines, local scripts, or cron jobs.
- **Education & Research** – Study model behavior, test fine‑tunes, or audit outputs without sending data externally.

## History

Ollama was created by Jeffrey Morgan in early 2023 and quickly became the de‑facto standard for running LLMs locally. Its simplicity—download a model and chat in seconds—solved the major friction point of setting up complex Python environments and low‑level inference engines. The project gained rapid adoption alongside the release of open‑weight models like Llama 2 and Mistral, and continues to evolve with community contributions and an expanding model ecosystem.

For more details, visit [ollama.com](https://ollama.com) or check the [GitHub repository](https://github.com/ollama/ollama).