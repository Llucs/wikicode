---
title: Ollama - Gestión Local de LLMs
description: Ollama es una herramienta de código abierto para ejecutar y gestionar modelos de lenguaje grandes (LLMs) de forma local, proporcionando una CLI simple y una API REST local.
created: 2026-06-16
tags:
  - ollama
  - llm
  - local-ai
  - open-source
  - devtools
status: draft
---

# Ollama: Ejecuta Modelos de Lenguaje Grandes Localmente

Ollama es un framework gratuito y de código abierto que hace que sea extremadamente fácil descargar, ejecutar y gestionar modelos de lenguaje grandes (LLMs) en tu propia máquina. Agrupa los pesos del modelo, la configuración y un motor de inferencia optimizado (basado en `llama.cpp`) en un solo paquete, abstrayendo la aceleración por GPU, la cuantización y la gestión de dependencias detrás de un solo comando.

## ¿Por Qué Ollama?

- **Privacidad y Seguridad** – Todo el cálculo ocurre localmente; ningún dato sale nunca de tu dispositivo.
- **Capacidad Sin Conexión** – Una vez que un modelo está descargado, puedes ejecutarlo sin conexión a Internet.
- **Eficiencia de Costos** – Sin tarifas de uso de API. Ejecuta modelos tanto como quieras en tu propio hardware.
- **Latencia** – Cero viajes de ida y vuelta en la red, lo que permite ciclos de iteración más rápidos.
- **Control Total** – Personaliza prompts, mensajes del sistema, parámetros e incluso crea nuevos modelos compuestos mediante `Modelfile`.

## Instalación

Elige tu plataforma:

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

> **Nota:** En Linux, asegúrate de que tu usuario esté en los grupos `video` y `render` si usas aceleración por GPU (`sudo usermod -aG video,render $USER`).

## Uso Básico

### 1. Ejecutar un Chat Interactivo

```bash
ollama run llama3.2
```

Esto descarga el modelo si no está en caché y luego abre una sesión de chat interactiva. Escribe `/bye` para salir.

### 2. Gestionar Modelos

```bash
# Lista los modelos descargados
ollama list

# Descarga un modelo sin ejecutarlo
ollama pull mistral

# Elimina un modelo del almacenamiento local
ollama rm phi
```

### 3. Generación Única (No Interactiva)

```bash
ollama run llama3.2 "¿Cuál es la capital de Francia?"
```

### 4. Usar la API REST

Ollama expone una API compatible con OpenAI en el puerto `11434`. Puedes usar `curl` o cualquier cliente HTTP:

**Generar (finalización simple):**
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

La API también admite streaming (establece `"stream": true`) y es totalmente compatible con las librerías cliente de OpenAI (`openai`, `langchain`, etc.) apuntando la URL base a `http://localhost:11434/v1`.

## Personalizando Modelos con un Modelfile

Un `Modelfile` es un descriptor similar a Docker que te permite establecer parámetros, prompts del sistema o incluso combinar múltiples modelos.

Ejemplo de `Modelfile`:
```
FROM llama3.2

# Establece un prompt del sistema personalizado
SYSTEM "You are a helpful assistant that speaks like a pirate."

# Sobreescribe los parámetros de generación por defecto
PARAMETER temperature 0.8
PARAMETER top_p 0.9
```

Construir y ejecutar:
```bash
ollama create pirate-bot -f ./Modelfile
ollama run pirate-bot
```

También puedes usar `FROM` para referenciar otros modelos (incluyendo archivos GGUF) y crear versiones en capas o afinadas.

## Características Principales

| Característica | Descripción |
|---------|-------------|
| **Amplia Biblioteca de Modelos** | Cientos de modelos disponibles (Llama 3, Mistral, Gemma, Phi, Qwen, DeepSeek, CodeGemma, etc.) con etiquetas para diferentes tamaños y cuantizaciones. |
| **Aceleración por GPU** | Soporta NVIDIA CUDA, AMD ROCm y Apple Metal para inferencia acelerada por hardware. |
| **Solicitudes Concurrentes** | Encola y procesa eficientemente múltiples solicitudes de generación/chat en paralelo. |
| **API Compatible con OpenAI** | Reemplazo directo de la API de OpenAI: cambia la URL base en tu aplicación y ejecuta localmente. |
| **Modelfile** | Personaliza prompts del sistema, parámetros e incluso crea nuevos modelos compuestos. |
| **Multiplataforma** | macOS, Linux, Windows (WSL2) y Docker. |
| **Ligero** | Los binarios e imágenes de contenedor son pequeños; las dependencias son mínimas. |
| **Registro y Monitoreo** | El servidor registra en la salida estándar; endpoint de salud en `http://localhost:11434/api/tags`. |

## Casos de Uso

- **Chat Local y Asistente Personal** – IA conversacional privada sin dependencia en la nube.
- **Asistente de Código Sin Conexión** – Ejecuta CodeGemma, DeepSeek‑Coder o StarCoder completamente sin conexión.
- **Pipelines RAG** – Sirve como backend de LLM para generación aumentada por recuperación sobre documentos locales (por ejemplo, con LangChain o LlamaIndex).
- **Prototipado Rápido** – Experimenta con prompts, modelos y parámetros antes de comprometerte con una API paga.
- **Automatización** – Llama a la API desde pipelines de CI/CD, scripts locales o tareas cron.
- **Educación e Investigación** – Estudia el comportamiento del modelo, prueba ajustes finos o audita salidas sin enviar datos externamente.

## Historia

Ollama fue creado por Jeffrey Morgan a principios de 2023 y rápidamente se convirtió en el estándar de facto para ejecutar LLMs localmente. Su simplicidad—descargar un modelo y chatear en segundos—resolvió el principal punto de fricción de configurar entornos Python complejos y motores de inferencia de bajo nivel. El proyecto ganó una rápida adopción junto con el lanzamiento de modelos de pesos abiertos como Llama 2 y Mistral, y continúa evolucionando con contribuciones de la comunidad y un ecosistema de modelos en expansión.

Para más detalles, visita [ollama.com](https://ollama.com) o revisa el [repositorio de GitHub](https://github.com/ollama/ollama).