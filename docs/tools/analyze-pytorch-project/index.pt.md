---
title: PyTorch – Deep Learning Framework
description: Uma biblioteca de machine learning de código aberto para Python que fornece computação de tensores e deep neural networks.
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

# PyTorch – Deep Learning Framework

**PyTorch** é um framework de deep learning open-source desenvolvido pela Meta AI (antigamente FAIR) e agora governado pela PyTorch Foundation sob a Linux Foundation. É mais conhecido por seu **grafo de computação dinâmico** (Define-by-Run), que permite construção intuitiva de modelos, depuração e flexibilidade de pesquisa, mantendo alta performance para implantação em produção.

---

## Visão Geral

PyTorch fornece duas capacidades principais:

- **Computação de tensores** com forte aceleração de GPU, similar ao NumPy mas com diferenciação automática.
- **Deep neural networks** construídas em um sistema autograd baseado em fita.

Desde seu lançamento público em 2016, PyTorch se tornou o framework dominante em pesquisa de IA e é amplamente usado para sistemas de produção, incluindo a maioria dos grandes modelos de linguagem (LLaMA, Mistral), geração de imagens (Stable Diffusion) e modelos de visão computacional.

---

## Por que PyTorch?

- **Pythônico & Dinâmico** – O grafo é construído dinamicamente. O fluxo de controle padrão do Python funciona naturalmente, facilitando a depuração com ferramentas como `pdb` ou `ipdb`.
- **Autograd Feito Corretamente** – O motor `torch.autograd` registra operações em um grafo acíclico direcionado (DAG) e computa gradientes automaticamente.
- **Pronto para Produção** – `torch.compile` traz otimizações em nível de grafo sem alterações de código; o suporte a TorchScript e ONNX permite servir modelos.
- **Treinamento Distribuído** – Suporte de primeira classe para DDP (Data Distributed Parallel) e FSDP (Fully Sharded Data Parallel), essencial para escalar para centenas de GPUs.
- **Ecossistema Rico** – Bibliotecas para visão (`torchvision`), áudio (`torchaudio`), texto (`torchtext`), redes neurais de grafos (`PyTorch Geometric`) e mais.

---

## Instalação

Selecione o comando que corresponde ao seu hardware e versão do CUDA:

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

Verifique a instalação:

```python
import torch
print(torch.__version__)          # e.g., 2.6.0
print(torch.cuda.is_available())  # True if CUDA is properly set up
```

---

## Conceitos Principais

### Tensores

Um `torch.Tensor` é um array multidimensional que pode executar em CPU ou GPU e opcionalmente rastrear gradientes para diferenciação automática.

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

A flag `requires_grad` informa ao autograd para rastrear operações no tensor.

```python
x = torch.randn(3, requires_grad=True)
y = x * 2
z = y.mean()
z.backward()                             # compute gradients
print(x.grad)                            # dy/dx
```

Cada chamada a `backward()` acumula gradientes no atributo `.grad` dos tensores folha. Em loops de treinamento, os gradientes devem ser zerados antes de cada nova passagem backward (geralmente com `optimizer.zero_grad()`).

### Redes Neurais (`nn.Module`)

Defina um modelo subclassificando `nn.Module` e implementando o método `forward`:

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

Todos os parâmetros são registrados automaticamente e podem ser acessados via `model.parameters()`.

---

## Treinando um Modelo

Um loop de treinamento típico inclui carregamento de dados, passagem forward, cálculo de perda, cálculo de gradiente e atualização de parâmetros.

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

Para datasets reais, envolva seus dados em um `torch.utils.data.DataLoader` que fornece batch, embaralhamento e carregamento paralelo.

---

## Recursos Avançados

### `torch.compile`

Introduzido no PyTorch 2.0, `torch.compile` compila grafos de modelos em kernels fundidos otimizados (usando TorchDynamo, AOTAutograd e, opcionalmente, Triton). Frequentemente fornece ganhos de velocidade de 30–50% sem nenhuma alteração de código no loop de treinamento.

```python
model = TwoLayerNet()
model = torch.compile(model, mode="reduce-overhead")

# Use model normally thereafter
output = model(inputs)
```

Modos de compilação:
- `"default"`: otimização balanceada
- `"reduce-overhead"`: minimiza overhead do Python, inferência mais rápida
- `"max-autotune"`: tenta muitas configurações de kernel para máxima velocidade, mas maior tempo de compilação

### Treinamento Distribuído

PyTorch oferece vários níveis de paralelismo:

- **DataParallel (DP)** – Simples, mas menos eficiente; divide batches entre GPUs.
- **DistributedDataParallel (DDP)** – Preferido para treinamento multi‑GPU; lida com sincronização de forma mais eficiente.
- **Fully Sharded Data Parallel (FSDP)** – Fragmenta parâmetros do modelo, gradientes e estados do otimizador entre dispositivos, permitindo treinamento de modelos muito grandes (ex.: LLaMA).

Uso básico de DDP:

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

TorchScript permite serializar modelos para implantação em ambientes não Python (C++, mobile, etc.) via tracing ou scripting.

```python
scripted_model = torch.jit.script(model)
scripted_model.save("model.pt")
```

### Ecossistema

| Biblioteca | Propósito |
|------------|-----------|
| `torchvision` | Datasets, modelos e transformações para visão computacional |
| `torchaudio` | I/O de áudio, transformações e modelos pré‑treinados |
| `torchtext` | Utilitários de processamento de texto e datasets |
| `PyTorch Geometric` | Redes neurais de grafos |
| `Captum` | Interpretabilidade de modelos |
| `TorchMetrics` | Métricas padronizadas para avaliação |
| `PyTorch Lightning` | Wrapper de treinamento de alto nível (reduz código repetitivo) |

---

## Recursos

- **Site Oficial:** [pytorch.org](https://pytorch.org)
- **Documentação:** [pytorch.org/docs](https://pytorch.org/docs)
- **Tutoriais:** [pytorch.org/tutorials](https://pytorch.org/tutorials)
- **Código Fonte:** [github.com/pytorch/pytorch](https://github.com/pytorch/pytorch)
- **Model Hub:** [huggingface.co/models](https://huggingface.co/models) (milhares de modelos PyTorch pré‑treinados)

---

> **Status:** Rascunho – Este documento é uma referência viva. Contribuições e correções são bem-vindas através do rastreador de issues do repositório.