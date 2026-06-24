---
title: PyTorch - Deep Learning Framework
description: An open-source machine learning library for Python that provides tensor computation and deep neural networks.
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

**PyTorch** is an open-source deep learning framework developed by Meta AI (formerly FAIR) and now governed by the PyTorch Foundation under the Linux Foundation. It is best known for its **dynamic computation graph** (Define-by-Run), which enables intuitive model building, debugging, and research flexibility while maintaining high performance for production deployment.

---

## Overview

PyTorch provides two core capabilities:

- **Tensor computation** with strong GPU acceleration, similar to NumPy but with automatic differentiation.
- **Deep neural networks** built on a tape-based autograd system.

Since its public release in 2016, PyTorch has become the dominant framework in AI research and is widely used for production systems, including most major large language models (LLaMA, Mistral), image generation (Stable Diffusion), and computer vision models.

---

## Why PyTorch?

- **Pythonic & Dynamic** – The graph is built on the fly. Standard Python control flow works naturally, making debugging easy with tools like `pdb` or `ipdb`.
- **Autograd Done Right** – The `torch.autograd` engine records operations in a directed acyclic graph (DAG) and computes gradients automatically.
- **Production Ready** – `torch.compile` brings graph-level optimizations without code changes; TorchScript and ONNX support enable serving.
- **Distributed Training** – First-class support for DDP (Data Distributed Parallel) and FSDP (Fully Sharded Data Parallel), essential for scaling to hundreds of GPUs.
- **Rich Ecosystem** – Libraries for vision (`torchvision`), audio (`torchaudio`), text (`torchtext`), graph neural networks (`PyTorch Geometric`), and more.

---

## Installation

Select the command that matches your hardware and CUDA version:

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

Verify the installation:

```python
import torch
print(torch.__version__)          # e.g., 2.6.0
print(torch.cuda.is_available())  # True if CUDA is properly set up
```

---

## Core Concepts

### Tensors

A `torch.Tensor` is a multi‑dimensional array that can run on CPU or GPU and optionally track gradients for automatic differentiation.

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

The `requires_grad` flag tells autograd to track operations on the tensor.

```python
x = torch.randn(3, requires_grad=True)
y = x * 2
z = y.mean()
z.backward()                             # compute gradients
print(x.grad)                            # dy/dx
```

Each call to `backward()` accumulates gradients into the `.grad` attribute of the leaf tensors. In training loops, gradients must be zeroed before each new backward pass (usually with `optimizer.zero_grad()`).

### Neural Networks (`nn.Module`)

Define a model by subclassing `nn.Module` and implementing the `forward` method:

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

All parameters are automatically registered and can be accessed via `model.parameters()`.

---

## Training a Model

A typical training loop includes data loading, forward pass, loss computation, gradient calculation, and parameter update.

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

For real datasets, wrap your data in a `torch.utils.data.DataLoader` that provides batching, shuffling, and parallel loading.

---

## Advanced Features

### `torch.compile`

Introduced in PyTorch 2.0, `torch.compile` compiles model graphs into optimized fused kernels (using TorchDynamo, AOTAutograd, and optionally Triton). It often provides 30–50% speedups with zero code changes to the training loop.

```python
model = TwoLayerNet()
model = torch.compile(model, mode="reduce-overhead")

# Use model normally thereafter
output = model(inputs)
```

Compilation modes:
- `"default"`: balanced optimization
- `"reduce-overhead"`: minimizes Python overhead, faster inference
- `"max-autotune"`: tries many kernel configurations for maximum speed but longer compile time

### Distributed Training

PyTorch offers several levels of parallelism:

- **DataParallel (DP)** – Simple but less efficient; splits batches across GPUs.
- **DistributedDataParallel (DDP)** – Preferred for multi‑GPU training; handles synchronization more efficiently.
- **Fully Sharded Data Parallel (FSDP)** – Shards model parameters, gradients, and optimizer states across devices, enabling training of very large models (e.g., LLaMA).

Basic DDP usage:

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

TorchScript allows you to serialize models for deployment in non‑Python environments (C++, mobile, etc.) via tracing or scripting.

```python
scripted_model = torch.jit.script(model)
scripted_model.save("model.pt")
```

### Ecosystem

| Library | Purpose |
|---------|---------|
| `torchvision` | Datasets, models, and transforms for computer vision |
| `torchaudio` | Audio I/O, transforms, and pre‑trained models |
| `torchtext` | Text processing utilities and datasets |
| `PyTorch Geometric` | Graph neural networks |
| `Captum` | Model interpretability |
| `TorchMetrics` | Standardized metrics for evaluation |
| `PyTorch Lightning` | High‑level training wrapper (reduces boilerplate) |

---

## Resources

- **Official Website:** [pytorch.org](https://pytorch.org)
- **Documentation:** [pytorch.org/docs](https://pytorch.org/docs)
- **Tutorials:** [pytorch.org/tutorials](https://pytorch.org/tutorials)
- **Source Code:** [github.com/pytorch/pytorch](https://github.com/pytorch/pytorch)
- **Model Hub:** [huggingface.co/models](https://huggingface.co/models) (thousands of pre‑trained PyTorch models)

---

> **Status:** Draft – This document is a living reference. Contributions and corrections are welcome via the repository’s issue tracker.