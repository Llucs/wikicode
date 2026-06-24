---
title: PyTorch - Framework d'apprentissage profond
description: Une bibliothèque open-source de machine learning pour Python qui fournit le calcul tensoriel et les réseaux de neurones profonds.
created: 2026-06-24
tags:
  - pytorch
  - deep-learning
  - machine-learning
  - tensor
  - neural-networks
  - python
status: draft
---

# PyTorch – Framework d'apprentissage profond

**PyTorch** est un framework open-source d'apprentissage profond développé par Meta AI (anciennement FAIR) et désormais géré par la PyTorch Foundation sous la Linux Foundation. Il est surtout connu pour son **graphe de calcul dynamique** (Define-by-Run), qui permet une construction de modèle intuitive, un débogage et une flexibilité de recherche tout en maintenant de hautes performances pour le déploiement en production.

---

## Aperçu

PyTorch propose deux fonctionnalités principales :

- **Le calcul tensoriel** avec une forte accélération GPU, similaire à NumPy mais avec différenciation automatique.
- **Les réseaux de neurones profonds** construits sur un système d'autograd basé sur un ruban (tape-based).

Depuis sa sortie publique en 2016, PyTorch est devenu le framework dominant dans la recherche en IA et est largement utilisé pour les systèmes en production, y compris la plupart des grands modèles de langage (LLaMA, Mistral), la génération d'images (Stable Diffusion) et les modèles de vision par ordinateur.

---

## Pourquoi PyTorch ?

- **Pythonique et Dynamique** – Le graphe est construit à la volée. Les structures de contrôle standard de Python fonctionnent naturellement, facilitant le débogage avec des outils comme `pdb` ou `ipdb`.
- **Autograd bien fait** – Le moteur `torch.autograd` enregistre les opérations dans un graphe acyclique dirigé (DAG) et calcule automatiquement les gradients.
- **Prêt pour la production** – `torch.compile` apporte des optimisations au niveau du graphe sans changement de code ; TorchScript et la prise en charge d'ONNX permettent le déploiement.
- **Entraînement distribué** – Prise en charge de premier ordre pour DDP (Data Distributed Parallel) et FSDP (Fully Sharded Data Parallel), essentiel pour passer à l'échelle sur des centaines de GPU.
- **Écosystème riche** – Bibliothèques pour la vision (`torchvision`), l'audio (`torchaudio`), le texte (`torchtext`), les réseaux de neurones graphiques (`PyTorch Geometric`), et plus encore.

---

## Installation

Sélectionnez la commande qui correspond à votre matériel et à la version CUDA :

```bash
# Latest stable release (CPU & CUDA)
pip install torch torchvision torchaudio

# Specific CUDA version (e.g., CUDA 11.8)
pip install torch==2.6.0+cu118 --index-url https://download.pytorch.org/whl/cu118

# Conda (recommended for managing environments)
conda install pytorch torchvision torchaudio -c pytorch

# CPU-only version
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

Vérifiez l'installation :

```python
import torch
print(torch.__version__)          # e.g., 2.6.0
print(torch.cuda.is_available())  # True if CUDA is properly set up
```

---

## Concepts fondamentaux

### Tensors

Un `torch.Tensor` est un tableau multi‑dimensionnel qui peut s'exécuter sur CPU ou GPU et suivre optionnellement les gradients pour la différenciation automatique.

```python
import torch

# Create tensors
x = torch.randn(3, 4)                    # random normal, size (3,4)
y = torch.ones(3, 4)                     # all ones
z = torch.tensor([[1, 2], [3, 4]])       # from data

# Move to GPU (if available)
if torch.cuda.is_available():
    x = x.cuda()

# Basic operations
w = x @ y.T                              # matrix multiplication
sum_all = w.sum()                        # reduce to scalar
```

### Autograd

Le drapeau `requires_grad` indique à autograd de suivre les opérations sur le tenseur.

```python
x = torch.randn(3, requires_grad=True)
y = x * 2
z = y.mean()
z.backward()                             # compute gradients
print(x.grad)                            # dy/dx
```

Chaque appel à `backward()` accumule les gradients dans l'attribut `.grad` des tenseurs feuilles. Dans les boucles d'entraînement, les gradients doivent être remis à zéro avant chaque nouvelle rétropropagation (généralement avec `optimizer.zero_grad()`).

### Neural Networks (`nn.Module`)

Définissez un modèle en sous-classant `nn.Module` et en implémentant la méthode `forward` :

```python
import torch.nn as nn
import torch.nn.functional as F

class TwoLayerNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = TwoLayerNet()
print(model)
```

Tous les paramètres sont automatiquement enregistrés et peuvent être accédés via `model.parameters()`.

---

## Entraînement d'un modèle

Une boucle d'entraînement typique comprend le chargement des données, la passe avant, le calcul de la perte, le calcul des gradients et la mise à jour des paramètres.

```python
import torch.optim as optim

# Dummy data (batch_size=32, input_dim=784)
inputs = torch.randn(32, 784)
labels = torch.randint(0, 10, (32,))

model = TwoLayerNet()
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Training step
optimizer.zero_grad()               # clear previous gradients
outputs = model(inputs)             # forward pass
loss = criterion(outputs, labels)   # compute loss
loss.backward()                     # backpropagation
optimizer.step()                    # update weights

print(f"Loss: {loss.item():.4f}")
```

Pour des jeux de données réels, enveloppez vos données dans un `torch.utils.data.DataLoader` qui fournit le partitionnement en lots, le mélange et le chargement parallèle.

---

## Fonctionnalités avancées

### `torch.compile`

Introduit dans PyTorch 2.0, `torch.compile` compile les graphes de modèle en noyaux fusionnés optimisés (en utilisant TorchDynamo, AOTAutograd, et optionnellement Triton). Il offre souvent des accélérations de 30 à 50 % sans aucun changement de code dans la boucle d'entraînement.

```python
model = TwoLayerNet()
model = torch.compile(model, mode="reduce-overhead")

# Use model normally thereafter
output = model(inputs)
```

Modes de compilation :
- `"default"` : optimisation équilibrée
- `"reduce-overhead"` : minimise la surcharge Python, inférence plus rapide
- `"max-autotune"` : essaie de nombreuses configurations de noyau pour une vitesse maximale mais un temps de compilation plus long

### Distributed Training

PyTorch propose plusieurs niveaux de parallélisme :

- **DataParallel (DP)** – Simple mais moins efficace ; répartit les lots entre les GPU.
- **DistributedDataParallel (DDP)** – Préféré pour l'entraînement multi‑GPU ; gère la synchronisation plus efficacement.
- **Fully Sharded Data Parallel (FSDP)** – Répartit les paramètres, gradients et états de l'optimiseur entre les périphériques, permettant l'entraînement de très grands modèles (par ex., LLaMA).

Exemple d'utilisation de base de DDP :

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

dist.init_process_group("nccl")          # NCCL backend
rank = dist.get_rank()
model = TwoLayerNet().cuda(rank)
ddp_model = DDP(model, device_ids=[rank])

# Training loop remains unchanged
```

### TorchScript

TorchScript vous permet de sérialiser des modèles pour un déploiement dans des environnements non‑Python (C++, mobile, etc.) via le tracing ou le scripting.

```python
scripted_model = torch.jit.script(model)
scripted_model.save("model.pt")
```

### Écosystème

| Bibliothèque | Objectif |
|---------|---------|
| `torchvision` | Jeux de données, modèles et transformations pour la vision par ordinateur |
| `torchaudio` | Entrée/sortie audio, transformations et modèles pré‑entraînés |
| `torchtext` | Utilitaires de traitement de texte et jeux de données |
| `PyTorch Geometric` | Réseaux de neurones graphiques |
| `Captum` | Interprétabilité des modèles |
| `TorchMetrics` | Métriques standardisées pour l'évaluation |
| `PyTorch Lightning` | Wrapper d'entraînement de haut niveau (réduit le code standard) |

---

## Ressources

- **Site officiel :** [pytorch.org](https://pytorch.org)
- **Documentation :** [pytorch.org/docs](https://pytorch.org/docs)
- **Tutoriels :** [pytorch.org/tutorials](https://pytorch.org/tutorials)
- **Code source :** [github.com/pytorch/pytorch](https://github.com/pytorch/pytorch)
- **Hub de modèles :** [huggingface.co/models](https://huggingface.co/models) (des milliers de modèles PyTorch pré‑entraînés)

---

> **Statut :** Projet – Ce document est une référence évolutive. Les contributions et corrections sont les bienvenues via le gestionnaire de tickets du dépôt.