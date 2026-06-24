---
title: PyTorch - Deep-Learning-Framework
description: Eine Open-Source-Bibliothek für maschinelles Lernen in Python, die Tensorberechnung und tiefe neuronale Netze bereitstellt.
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

# PyTorch – Deep-Learning-Framework

**PyTorch** ist ein Open-Source-Deep-Learning-Framework, das von Meta AI (ehemals FAIR) entwickelt wurde und jetzt von der PyTorch Foundation unter der Linux Foundation verwaltet wird. Es ist bekannt für seinen **dynamischen Berechnungsgraphen** (Define-by-Run), der intuitives Modellieren, Debugging und Forschungsflexibilität ermöglicht, während hohe Leistung für den Produktionseinsatz erhalten bleibt.

---

## Überblick

PyTorch bietet zwei Kernfähigkeiten:

- **Tensorberechnung** mit starker GPU-Beschleunigung, ähnlich wie NumPy, jedoch mit automatischer Differenzierung.
- **Tiefe neuronale Netze** basierend auf einem tape-basierten Autograd-System.

Seit seiner öffentlichen Veröffentlichung im Jahr 2016 ist PyTorch das dominierende Framework in der KI-Forschung und wird weitgehend in Produktionssystemen eingesetzt, darunter die meisten großen Large Language Models (LLaMA, Mistral), Bildgenerierung (Stable Diffusion) und Computervisionsmodelle.

---

## Warum PyTorch?

- **Pythonisch & Dynamisch** – Der Graph wird spontan aufgebaut. Standard-Python-Kontrollfluss funktioniert natürlich, was das Debugging mit Tools wie `pdb` oder `ipdb` erleichtert.
- **Autograd richtig gemacht** – Die `torch.autograd`-Engine zeichnet Operationen in einem gerichteten azyklischen Graphen (DAG) auf und berechnet Gradienten automatisch.
- **Produktionsreif** – `torch.compile` bringt Optimierungen auf Graphebene ohne Codeänderungen; TorchScript- und ONNX-Unterstützung ermöglichen das Serving.
- **Verteiltes Training** – Erstklassige Unterstützung für DDP (Data Distributed Parallel) und FSDP (Fully Sharded Data Parallel), wesentlich für die Skalierung auf Hunderte von GPUs.
- **Reichhaltiges Ökosystem** – Bibliotheken für Vision (`torchvision`), Audio (`torchaudio`), Text (`torchtext`), Graph Neural Networks (`PyTorch Geometric`) und mehr.

---

## Installation

Wähle den Befehl, der zu deiner Hardware und CUDA-Version passt:

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

Überprüfe die Installation:

```python
import torch
print(torch.__version__)          # e.g., 2.6.0
print(torch.cuda.is_available())  # True if CUDA is properly set up
```

---

## Kernkonzepte

### Tensoren

Ein `torch.Tensor` ist ein mehrdimensionales Array, das auf CPU oder GPU laufen kann und optional Gradienten für die automatische Differenzierung verfolgt.

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

Das Flag `requires_grad` teilt Autograd mit, dass es Operationen auf dem Tensor verfolgen soll.

```python
x = torch.randn(3, requires_grad=True)
y = x * 2
z = y.mean()
z.backward()                             # compute gradients
print(x.grad)                            # dy/dx
```

Jeder Aufruf von `backward()` akkumuliert Gradienten in das `.grad`-Attribut der Blatt-Tensoren. In Trainingsschleifen müssen die Gradienten vor jedem neuen Rückwärtsdurchlauf zurückgesetzt werden (normalerweise mit `optimizer.zero_grad()`).

### Neuronale Netze (`nn.Module`)

Definiere ein Modell durch Unterklassen von `nn.Module` und implementiere die `forward`-Methode:

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

Alle Parameter werden automatisch registriert und können über `model.parameters()` abgerufen werden.

---

## Trainieren eines Modells

Ein typischer Trainingsloop umfasst Datenladen, Vorwärtspass, Verlustberechnung, Gradientenberechnung und Parameteraktualisierung.

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

Für echte Datensätze verpackst du deine Daten in einen `torch.utils.data.DataLoader`, der Batching, Mischen und paralleles Laden unterstützt.

---

## Fortgeschrittene Funktionen

### `torch.compile`

Eingeführt in PyTorch 2.0, kompiliert `torch.compile` Modellgraphen in optimierte verschmolzene Kernel (unter Verwendung von TorchDynamo, AOTAutograd und optional Triton). Es bietet oft 30–50 % Geschwindigkeitssteigerungen ohne Codeänderungen am Trainingsloop.

```python
model = TwoLayerNet()
model = torch.compile(model, mode="reduce-overhead")

# Use model normally thereafter
output = model(inputs)
```

Kompilierungsmodi:
- `"default"`: ausgewogene Optimierung
- `"reduce-overhead"`: minimiert Python-Overhead, schnellere Inferenz
- `"max-autotune"`: testet viele Kernel-Konfigurationen für maximale Geschwindigkeit, aber längere Kompilierzeit

### Verteiltes Training

PyTorch bietet mehrere Ebenen der Parallelität:

- **DataParallel (DP)** – Einfach, aber weniger effizient; teilt Batches über GPUs auf.
- **DistributedDataParallel (DDP)** – Bevorzugt für Multi-GPU-Training; handhabt Synchronisierung effizienter.
- **Fully Sharded Data Parallel (FSDP)** – Verteilt Modellparameter, Gradienten und Optimizer-Zustände über Geräte und ermöglicht so das Training sehr großer Modelle (z. B. LLaMA).

Grundlegende DDP-Nutzung:

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

TorchScript ermöglicht es, Modelle für die Bereitstellung in Nicht-Python-Umgebungen (C++, Mobil usw.) per Tracing oder Scripting zu serialisieren.

```python
scripted_model = torch.jit.script(model)
scripted_model.save("model.pt")
```

### Ökosystem

| Bibliothek | Zweck |
|---------|---------|
| `torchvision` | Datensätze, Modelle und Transformationen für Computervision |
| `torchaudio` | Audio-E/A, Transformationen und vortrainierte Modelle |
| `torchtext` | Textverarbeitungshilfsmittel und Datensätze |
| `PyTorch Geometric` | Graph Neural Networks |
| `Captum` | Modellinterpretierbarkeit |
| `TorchMetrics` | Standardisierte Metriken zur Bewertung |
| `PyTorch Lightning` | Hochrangiger Trainings-Wrapper (reduziert Boilerplate-Code) |

---

## Ressourcen

- **Offizielle Website:** [pytorch.org](https://pytorch.org)
- **Dokumentation:** [pytorch.org/docs](https://pytorch.org/docs)
- **Tutorials:** [pytorch.org/tutorials](https://pytorch.org/tutorials)
- **Quellcode:** [github.com/pytorch/pytorch](https://github.com/pytorch/pytorch)
- **Modell-Hub:** [huggingface.co/models](https://huggingface.co/models) (Tausende vortrainierte PyTorch-Modelle)

---

> **Status:** Entwurf – Dieses Dokument ist eine lebendige Referenz. Beiträge und Korrekturen sind über den Issue-Tracker des Repositorys willkommen.