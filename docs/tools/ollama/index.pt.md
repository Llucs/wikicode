---
title: Ollama - Gerenciamento Local de LLMs
description: Ollama é uma ferramenta de código aberto para executar e gerenciar modelos de linguagem de grande porte (LLMs) localmente, fornecendo uma CLI simples e uma API REST local.
created: 2026-06-16
tags:
  - ollama
  - llm
  - local-ai
  - open-source
  - devtools
status: draft
---

# Ollama: Execute Modelos de Linguagem de Grande Porte Localmente

Ollama é um framework gratuito e de código aberto que torna trivialmente fácil baixar, executar e gerenciar modelos de linguagem de grande porte (LLMs) em sua própria máquina. Ele agrupa pesos de modelo, configuração e um mecanismo de inferência otimizado (baseado em `llama.cpp`) em um único pacote, abstraindo aceleração GPU, quantização e gerenciamento de dependências atrás de um único comando.

## Por que Ollama?

- **Privacidade e Segurança** – Toda a computação acontece localmente; nenhum dado jamais sai do seu dispositivo.
- **Capacidade Offline** – Uma vez que um modelo é baixado, você pode executá-lo sem conexão com a Internet.
- **Eficiência de Custo** – Sem taxas de uso de API. Execute modelos o quanto quiser em seu próprio hardware.
- **Latência** – Zero viagens de ida e volta na rede, permitindo ciclos de iteração mais rápidos.
- **Controle Total** – Personalize prompts, mensagens do sistema, parâmetros e até crie novos modelos compostos via `Modelfile`.

## Instalação

Escolha sua plataforma:

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

> **Nota:** No Linux, certifique-se de que seu usuário esteja nos grupos `video` e `render` se estiver usando aceleração GPU (`sudo usermod -aG video,render $USER`).

## Uso Básico

### 1. Execute um Chat Interativamente

```bash
ollama run llama3.2
```

Isso baixa o modelo se ainda não estiver em cache e abre uma sessão de chat interativa. Digite `/bye` para sair.

### 2. Gerenciar Modelos

```bash
# List downloaded models
ollama list

# Download a model without running it
ollama pull mistral

# Remove a model from local storage
ollama rm phi
```

### 3. Geração Única (Não Interativa)

```bash
ollama run llama3.2 "What is the capital of France?"
```

### 4. Use a API REST

Ollama expõe uma API compatível com OpenAI na porta `11434`. Você pode usar o `curl` ou qualquer cliente HTTP:

**Gerar (completude simples):**
```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama3.2",
    "prompt": "Hello, how are you?",
    "stream": false
  }'
```

**Chat (conversacional):**
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

A API também suporta streaming (defina `"stream": true`) e é totalmente compatível com as bibliotecas cliente da OpenAI (`openai`, `langchain`, etc.) apontando a URL base para `http://localhost:11434/v1`.

## Personalizando Modelos com um Modelfile

Um `Modelfile` é um descritor semelhante ao Docker que permite definir parâmetros, prompts do sistema ou até combinar múltiplos modelos.

Exemplo de `Modelfile`:
```
FROM llama3.2

# Set a custom system prompt
SYSTEM "You are a helpful assistant that speaks like a pirate."

# Override default generation parameters
PARAMETER temperature 0.8
PARAMETER top_p 0.9
```

Construa e execute:
```bash
ollama create pirate-bot -f ./Modelfile
ollama run pirate-bot
```

Você também pode usar `FROM` para referenciar outros modelos (incluindo arquivos GGUF) para criar versões em camadas ou ajustadas.

## Principais Recursos

| Recurso | Descrição |
|---------|-------------|
| **Ampla Biblioteca de Modelos** | Centenas de modelos disponíveis (Llama 3, Mistral, Gemma, Phi, Qwen, DeepSeek, CodeGemma, etc.) com tags para diferentes tamanhos e quantizações. |
| **Aceleração GPU** | Suporta NVIDIA CUDA, AMD ROCm e Apple Metal para inferência acelerada por hardware. |
| **Requisições Concorrentes** | Enfileira e processa eficientemente múltiplas requisições de generate/chat em paralelo. |
| **API Compatível com OpenAI** | Substituição direta para a API da OpenAI – altere uma URL base em sua aplicação e execute localmente. |
| **Modelfile** | Personalize prompts do sistema, parâmetros e até crie novos modelos compostos. |
| **Multiplataforma** | macOS, Linux, Windows (WSL2) e Docker. |
| **Leve** | Binários e imagens de contêiner são pequenos; as dependências são mínimas. |
| **Registro e Monitoramento** | O servidor registra no stdout; endpoint de saúde em `http://localhost:11434/api/tags`. |

## Casos de Uso

- **Chat Local e Assistente Pessoal** – IA conversacional privada sem dependência de nuvem.
- **Assistente de Código Offline** – Execute CodeGemma, DeepSeek‑Coder ou StarCoder completamente offline.
- **Pipelines RAG** – Atua como backend LLM para Geração Aumentada por Recuperação sobre documentos locais (por exemplo, com LangChain ou LlamaIndex).
- **Prototipagem Rápida** – Experimente prompts, modelos e parâmetros antes de se comprometer com uma API paga.
- **Automação** – Chame a API de pipelines CI/CD, scripts locais ou cron jobs.
- **Educação e Pesquisa** – Estude o comportamento do modelo, teste ajustes finos ou audite saídas sem enviar dados externamente.

## Histórico

Ollama foi criado por Jeffrey Morgan no início de 2023 e rapidamente se tornou o padrão de facto para executar LLMs localmente. Sua simplicidade — baixar um modelo e conversar em segundos — resolveu o principal ponto de atrito de configurar ambientes Python complexos e mecanismos de inferência de baixo nível. O projeto ganhou rápida adoção juntamente com o lançamento de modelos de pesos abertos como Llama 2 e Mistral, e continua a evoluir com contribuições da comunidade e um ecossistema de modelos em expansão.

Para mais detalhes, visite [ollama.com](https://ollama.com) ou consulte o [repositório GitHub](https://github.com/ollama/ollama).