---
title: Ollama - Gestion locale de LLM
description: Ollama est un outil open-source pour exécuter et gérer des grands modèles de langage (LLM) localement, offrant une CLI simple et une API REST locale.
created: 2026-06-16
tags:
  - ollama
  - llm
  - local-ai
  - open-source
  - devtools
status: draft
---

# Ollama : Exécutez des grands modèles de langage localement

Ollama est un framework open-source gratuit qui rend le téléchargement, l'exécution et la gestion des grands modèles de langage (LLM) sur votre propre machine extrêmement faciles. Il regroupe les poids du modèle, la configuration et un moteur d'inférence optimisé (basé sur `llama.cpp`) dans un seul package, masquant l'accélération GPU, la quantification et la gestion des dépendances derrière une commande unique.

## Pourquoi Ollama ?

- **Confidentialité et sécurité** – Tous les calculs ont lieu localement ; aucune donnée ne quitte jamais votre appareil.
- **Utilisation hors ligne** – Une fois un modèle téléchargé, vous pouvez l'exécuter sans connexion Internet.
- **Rentabilité** – Pas de frais d'utilisation d'API. Exécutez les modèles autant que vous le souhaitez sur votre propre matériel.
- **Latence** – Zéro aller-retour réseau, permettant des cycles d'itération plus rapides.
- **Contrôle total** – Personnalisez les prompts, les messages système, les paramètres, et même créez de nouveaux modèles composites via `Modelfile`.

## Installation

Choisissez votre plateforme :

```bash
# macOS (Homebrew)
brew install ollama

# Linux (script automatisé)
curl -fsSL https://ollama.com/install.sh | sh

# Windows – Téléchargez l'installateur officiel depuis https://ollama.com
# L'installateur configure automatiquement WSL2 et ajoute `ollama` au PATH.

# Docker (tout OS)
docker run -d \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama
```

> **Remarque :** Sous Linux, assurez-vous que votre utilisateur fait partie des groupes `video` et `render` si vous utilisez l'accélération GPU (`sudo usermod -aG video,render $USER`).

## Utilisation de base

### 1. Lancer un chat interactif

```bash
ollama run llama3.2
```

Cette commande télécharge le modèle s'il n'est pas déjà en cache, puis ouvre une session de chat interactive. Tapez `/bye` pour quitter.

### 2. Gérer les modèles

```bash
# Lister les modèles téléchargés
ollama list

# Télécharger un modèle sans l'exécuter
ollama pull mistral

# Supprimer un modèle du stockage local
ollama rm phi
```

### 3. Génération unique (non interactive)

```bash
ollama run llama3.2 "What is the capital of France?"
```

### 4. Utiliser l'API REST

Ollama expose une API compatible OpenAI sur le port `11434`. Vous pouvez utiliser `curl` ou tout client HTTP :

**Génération (complétion simple) :**
```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama3.2",
    "prompt": "Hello, how are you?",
    "stream": false
  }'
```

**Chat (conversationnel) :**
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

L'API prend également en charge le streaming (définissez `"stream": true`) et est entièrement compatible avec les bibliothèques clientes OpenAI (`openai`, `langchain`, etc.) en pointant l'URL de base vers `http://localhost:11434/v1`.

## Personnalisation des modèles avec un Modelfile

Un `Modelfile` est un descripteur de type Docker qui vous permet de définir des paramètres, des prompts système, ou même de combiner plusieurs modèles.

Exemple de `Modelfile` :
```
FROM llama3.2

# Définir un prompt système personnalisé
SYSTEM "You are a helpful assistant that speaks like a pirate."

# Remplacer les paramètres de génération par défaut
PARAMETER temperature 0.8
PARAMETER top_p 0.9
```

Construisez et exécutez :
```bash
ollama create pirate-bot -f ./Modelfile
ollama run pirate-bot
```

Vous pouvez également utiliser `FROM` pour référencer d'autres modèles (y compris les fichiers GGUF) afin de créer des versions superposées ou fine‑tunées.

## Fonctionnalités clés

| Fonctionnalité | Description |
|---------|-------------|
| **Vaste bibliothèque de modèles** | Des centaines de modèles disponibles (Llama 3, Mistral, Gemma, Phi, Qwen, DeepSeek, CodeGemma, etc.) avec des tags pour différentes tailles et quantifications. |
| **Accélération GPU** | Prend en charge NVIDIA CUDA, AMD ROCm et Apple Metal pour une inférence accélérée par le matériel. |
| **Requêtes concurrentes** | Met en file d'attente et traite efficacement plusieurs requêtes de génération/chat en parallèle. |
| **API compatible OpenAI** | Remplacement direct de l'API d'OpenAI – changez une URL de base dans votre application et exécutez-la localement. |
| **Modelfile** | Personnalisez les prompts système, les paramètres, et même créez de nouveaux modèles composites. |
| **Multi-plateforme** | macOS, Linux, Windows (WSL2) et Docker. |
| **Léger** | Les binaires et les images conteneur sont petits ; les dépendances sont minimales. |
| **Journalisation et surveillance** | Le serveur journalise sur stdout ; endpoint de santé à `http://localhost:11434/api/tags`. |

## Cas d'utilisation

- **Chat local et assistant personnel** – IA conversationnelle privée sans dépendance au cloud.
- **Assistant de code hors ligne** – Exécutez CodeGemma, DeepSeek‑Coder ou StarCoder complètement hors ligne.
- **Pipelines RAG** – Servez de backend LLM pour la génération augmentée de récupération (RAG) sur des documents locaux (par exemple avec LangChain ou LlamaIndex).
- **Prototypage rapide** – Expérimentez avec des prompts, des modèles et des paramètres avant de vous engager sur une API payante.
- **Automatisation** – Appelez l'API depuis des pipelines CI/CD, des scripts locaux ou des tâches cron.
- **Éducation et recherche** – Étudiez le comportement du modèle, testez des fine‑tunings ou auditez les sorties sans envoyer de données à l'extérieur.

## Historique

Ollama a été créé par Jeffrey Morgan au début de l'année 2023 et est rapidement devenu le standard de facto pour exécuter des LLM localement. Sa simplicité—télécharger un modèle et chatter en quelques secondes—a résolu le principal point de friction lié à la mise en place d'environnements Python complexes et de moteurs d'inférence de bas niveau. Le projet a connu une adoption rapide parallèlement à la sortie de modèles à poids ouverts comme Llama 2 et Mistral, et continue d'évoluer grâce aux contributions de la communauté et à un écosystème de modèles en expansion.

Pour plus de détails, visitez [ollama.com](https://ollama.com) ou consultez le [dépôt GitHub](https://github.com/ollama/ollama).