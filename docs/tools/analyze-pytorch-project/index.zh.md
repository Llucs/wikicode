---
title: PyTorch - 深度学习框架
description: 一个开源的Python机器学习库，提供张量计算和深度神经网络。
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

# PyTorch – 深度学习框架

**PyTorch** 是一个开源深度学习框架，由 Meta AI（前身为 FAIR）开发，现由 Linux 基金会旗下的 PyTorch 基金会管理。它以其**动态计算图**（Define-by-Run）而闻名，该特性可以实现直观的模型构建、调试和研究灵活性，同时为生产部署保持高性能。

---

## 概述

PyTorch 提供两个核心功能：

- **张量计算**，具有强大的 GPU 加速能力，类似于 NumPy，但带有自动微分。
- **深度神经网络**，构建于基于磁带（tape-based）的自动求导系统之上。

自 2016 年公开发布以来，PyTorch 已成为人工智能研究中的主导框架，并广泛用于生产系统，包括大多数主流大语言模型（LLaMA、Mistral）、图像生成（Stable Diffusion）以及计算机视觉模型。

---

## 为什么选择 PyTorch？

- **Pythonic 与动态** – 计算图即时构建。标准的 Python 控制流可自然使用，借助 `pdb` 或 `ipdb` 等工具可以轻松调试。
- **自动求导体验优秀** – `torch.autograd` 引擎在有向无环图（DAG）中记录操作，并自动计算梯度。
- **生产就绪** – `torch.compile` 无需修改代码即可实现图级优化；支持 TorchScript 和 ONNX，便于模型部署。
- **分布式训练** – 对 DDP（数据分布式并行）和 FSDP（全分片数据并行）提供一流支持，对于扩展至数百块 GPU 至关重要。
- **丰富的生态系统** – 涵盖视觉（`torchvision`）、音频（`torchaudio`）、文本（`torchtext`）、图神经网络（`PyTorch Geometric`）等库。

---

## 安装

根据硬件和 CUDA 版本选择合适的命令：

```bash
# 最新稳定版（CPU 和 CUDA）
pip install torch torchvision torchaudio

# 指定 CUDA 版本（例如 CUDA 11.8）
pip install torch==2.6.0+cu118 --index-url https://download.pytorch.org/whl/cu118

# Conda（推荐用于环境管理）
conda install pytorch torchvision torchaudio -c pytorch

# 仅 CPU 版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

验证安装：

```python
import torch
print(torch.__version__)          # 例如 2.6.0
print(torch.cuda.is_available())  # 如果 CUDA 配置正确则返回 True
```

---

## 核心概念

### 张量

`torch.Tensor` 是一个多维数组，可以在 CPU 或 GPU 上运行，并可选择性地跟踪梯度以实现自动微分。

```python
import torch

# 创建张量
x = torch.randn(3, 4)                    # 随机正态分布，形状 (3,4)
y = torch.ones(3, 4)                     # 全 1 张量
z = torch.tensor([[1, 2], [3, 4]])       # 从数据创建

# 移至 GPU（如可用）
if torch.cuda.is_available():
    x = x.cuda()

# 基本操作
w = x @ y.T                              # 矩阵乘法
sum_all = w.sum()                        # 归约为标量
```

### 自动求导

`requires_grad` 标志告诉自动求导引擎跟踪对该张量的操作。

```python
x = torch.randn(3, requires_grad=True)
y = x * 2
z = y.mean()
z.backward()                             # 计算梯度
print(x.grad)                            # 输出 dy/dx
```

每次调用 `backward()` 会将梯度累积到叶子张量的 `.grad` 属性中。在训练循环中，每次新的反向传播前必须将梯度清零（通常使用 `optimizer.zero_grad()`）。

### 神经网络（`nn.Module`）

通过继承 `nn.Module` 并实现 `forward` 方法来定义模型：

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

所有参数都会自动注册，并可通过 `model.parameters()` 访问。

---

## 训练模型

典型的训练循环包括数据加载、前向传播、损失计算、梯度计算和参数更新。

```python
import torch.optim as optim

# 模拟数据（batch_size=32, input_dim=784）
inputs = torch.randn(32, 784)
labels = torch.randint(0, 10, (32,))

model = TwoLayerNet()
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# 训练步骤
optimizer.zero_grad()               # 清除之前的梯度
outputs = model(inputs)             # 前向传播
loss = criterion(outputs, labels)   # 计算损失
loss.backward()                     # 反向传播
optimizer.step()                    # 更新权重

print(f"Loss: {loss.item():.4f}")
```

对于真实数据集，请将数据包装在 `torch.utils.data.DataLoader` 中，它提供批处理、打乱和并行加载功能。

---

## 高级特性

### `torch.compile`

`torch.compile` 在 PyTorch 2.0 中引入，它将模型图编译为优化后的融合内核（使用 TorchDynamo、AOTAutograd，并可选择 Triton）。通常能在无需更改训练循环任何代码的情况下实现 30–50% 的加速。

```python
model = TwoLayerNet()
model = torch.compile(model, mode="reduce-overhead")

# 之后正常使用模型
output = model(inputs)
```

编译模式：
- `"default"`：均衡优化
- `"reduce-overhead"`：最小化 Python 开销，加速推理
- `"max-autotune"`：尝试多种内核配置以追求最高速度，但编译时间更长

### 分布式训练

PyTorch 提供多个层次的并行策略：

- **DataParallel（DP）** – 简单但效率较低；将批次拆分到多个 GPU。
- **DistributedDataParallel（DDP）** – 多 GPU 训练的首选方案；同步效率更高。
- **Fully Sharded Data Parallel（FSDP）** – 将模型参数、梯度和优化器状态分片到多个设备，从而能够训练超大规模模型（如 LLaMA）。

基础 DDP 用法：

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

dist.init_process_group("nccl")          # NCCL 后端
rank = dist.get_rank()
model = TwoLayerNet().cuda(rank)
ddp_model = DDP(model, device_ids=[rank])

# 训练循环保持不变
```

### TorchScript

TorchScript 允许你通过跟踪或脚本化方式序列化模型，以便在非 Python 环境（C++、移动端等）中部署。

```python
scripted_model = torch.jit.script(model)
scripted_model.save("model.pt")
```

### 生态系统

| 库 | 用途 |
|---------|---------|
| `torchvision` | 计算机视觉的数据集、模型和变换 |
| `torchaudio` | 音频 I/O、变换和预训练模型 |
| `torchtext` | 文本处理工具和数据集 |
| `PyTorch Geometric` | 图神经网络 |
| `Captum` | 模型可解释性 |
| `TorchMetrics` | 标准化的评估指标 |
| `PyTorch Lightning` | 高级训练封装（减少样板代码） |

---

## 资源

- **官方网站：** [pytorch.org](https://pytorch.org)
- **文档：** [pytorch.org/docs](https://pytorch.org/docs)
- **教程：** [pytorch.org/tutorials](https://pytorch.org/tutorials)
- **源代码：** [github.com/pytorch/pytorch](https://github.com/pytorch/pytorch)
- **模型库：** [huggingface.co/models](https://huggingface.co/models)（数千个预训练的 PyTorch 模型）

---

> **状态：** 草稿 – 本文档为活页参考。欢迎通过仓库的问题跟踪器提交贡献和修正。