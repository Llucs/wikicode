---
title: Ollama - Lokale LLM-Verwaltung
description: Ollama ist ein Open-Source-Tool zum lokalen Ausführen und Verwalten großer Sprachmodelle (LLMs), das eine einfache CLI und eine lokale REST-API bereitstellt.
created: 2026-06-16
tags:
  - ollama
  - llm
  - local-ai
  - open-source
  - devtools
status: draft
---

# Ollama: Große Sprachmodelle lokal ausführen

Ollama ist ein kostenloses Open-Source-Framework, das es mühelos ermöglicht, große Sprachmodelle (LLMs) auf Ihrem eigenen Rechner herunterzuladen, auszuführen und zu verwalten. Es bündelt Modellgewichte, Konfiguration und eine optimierte Inferenz-Engine (basierend auf `llama.cpp`) in einem einzigen Paket und verbirgt GPU-Beschleunigung, Quantisierung und Abhängigkeitsverwaltung hinter einem einzigen Befehl.

## Warum Ollama?

- **Datenschutz & Sicherheit** – Alle Berechnungen finden lokal statt; keine Daten verlassen jemals Ihr Gerät.
- **Offline-Fähigkeit** – Sobald ein Modell heruntergeladen ist, können Sie es ohne Internetverbindung ausführen.
- **Kosteneffizienz** – Keine API-Nutzungsgebühren. Führen Sie Modelle so oft Sie möchten auf Ihrer eigenen Hardware aus.
- **Latenz** – Keine Netzwerk-Roundtrips, was schnellere Iterationszyklen ermöglicht.
- **Volle Kontrolle** – Passen Sie Prompts, Systemnachrichten, Parameter an und erstellen Sie sogar neue zusammengesetzte Modelle über `Modelfile`.

## Installation

Wählen Sie Ihre Plattform:

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

> **Hinweis:** Stellen Sie unter Linux sicher, dass Ihr Benutzer in den Gruppen `video` und `render` ist, wenn Sie GPU-Beschleunigung verwenden (`sudo usermod -aG video,render $USER`).

## Grundlegende Nutzung

### 1. Chat interaktiv ausführen

```bash
ollama run llama3.2
```

This pulls the model if not already cached, then opens an interactive chat session. Type `/bye` to exit.

### 2. Modelle verwalten

```bash
# List downloaded models
ollama list

# Download a model without running it
ollama pull mistral

# Remove a model from local storage
ollama rm phi
```

### 3. Einmalige Generierung (nicht interaktiv)

```bash
ollama run llama3.2 "What is the capital of France?"
```

### 4. Die REST-API verwenden

Ollama stellt eine OpenAI-kompatible API auf Port `11434` bereit. Sie können `curl` oder einen beliebigen HTTP-Client verwenden:

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

Die API unterstützt auch Streaming (setzen Sie `"stream": true`) und ist vollständig kompatibel mit den OpenAI-Clientbibliotheken (`openai`, `langchain`, etc.), indem Sie die Basis-URL auf `http://localhost:11434/v1` setzen.

## Modelle mit einer Modelfile anpassen

Eine `Modelfile` ist ein Docker-ähnlicher Deskriptor, mit dem Sie Parameter, Systemprompts festlegen oder sogar mehrere Modelle kombinieren können.

Example `Modelfile`:
```
FROM llama3.2

# Set a custom system prompt
SYSTEM "You are a helpful assistant that speaks like a pirate."

# Override default generation parameters
PARAMETER temperature 0.8
PARAMETER top_p 0.9
```

Erstellen und ausführen:
```bash
ollama create pirate-bot -f ./Modelfile
ollama run pirate-bot
```

Sie können auch `FROM` verwenden, um auf andere Modelle (einschließlich GGUF-Dateien) zu verweisen, um geschichtete oder feinabgestimmte Versionen zu erstellen.

## Hauptfunktionen

| Funktion | Beschreibung |
|---------|-------------|
| **Umfangreiche Modellbibliothek** | Hunderte von Modellen verfügbar (Llama 3, Mistral, Gemma, Phi, Qwen, DeepSeek, CodeGemma, usw.) mit Tags für verschiedene Größen und Quantisierungen. |
| **GPU-Beschleunigung** | Unterstützt NVIDIA CUDA, AMD ROCm und Apple Metal für hardwarebeschleunigte Inferenz. |
| **Gleichzeitige Anfragen** | Wartet und verarbeitet mehrere Generate-/Chat-Anfragen effizient parallel. |
| **OpenAI-kompatible API** | Austauschbarer Ersatz für die OpenAI-API – ändern Sie eine Basis-URL in Ihrer Anwendung und führen Sie sie lokal aus. |
| **Modelfile** | Systemprompts, Parameter anpassen und sogar neue zusammengesetzte Modelle erstellen. |
| **Plattformübergreifend** | macOS, Linux, Windows (WSL2) und Docker. |
| **Leichtgewichtig** | Binärdateien und Container-Images sind klein; Abhängigkeiten sind minimal. |
| **Protokollierung & Überwachung** | Server protokolliert auf stdout; Health-Endpunkt unter `http://localhost:11434/api/tags`. |

## Anwendungsfälle

- **Lokaler Chat & Persönlicher Assistent** – Private Konversations-KI ohne Cloud-Abhängigkeit.
- **Offline-Code-Assistent** – Führen Sie CodeGemma, DeepSeek-Coder oder StarCoder vollständig offline aus.
- **RAG-Pipelines** – Dienen Sie als LLM-Backend für Retrieval-Augmented Generation über lokale Dokumente (z.B. mit LangChain oder LlamaIndex).
- **Schnelles Prototyping** – Experimentieren Sie mit Prompts, Modellen und Parametern, bevor Sie sich für eine kostenpflichtige API entscheiden.
- **Automatisierung** – Rufen Sie die API von CI/CD-Pipelines, lokalen Skripten oder Cron-Jobs auf.
- **Bildung & Forschung** – Studieren Sie Modellverhalten, testen Sie Feintunings oder prüfen Sie Ausgaben, ohne Daten extern zu senden.

## Geschichte

Ollama wurde Anfang 2023 von Jeffrey Morgan entwickelt und schnell zum De-facto-Standard für die lokale Ausführung von LLMs. Seine Einfachheit – ein Modell herunterladen und in Sekundenschnelle chatten – löste das größte Hindernis bei der Einrichtung komplexer Python-Umgebungen und Low-Level-Inferenz-Engines. Das Projekt gewann mit der Veröffentlichung von Open-Weight-Modellen wie Llama 2 und Mistral schnell an Akzeptanz und entwickelt sich dank Community-Beiträgen und einem wachsenden Modell-Ökosystem weiter.

Für weitere Details besuchen Sie [ollama.com](https://ollama.com) oder sehen Sie sich das [GitHub-Repository](https://github.com/ollama/ollama) an.