---
title: PyTorch - 深層学習フレームワーク
description: Python向けのオープンソース機械学習ライブラリで、テンソル計算とディープニューラルネットワークを提供します。
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

# PyTorch – 深層学習フレームワーク

**PyTorch**は、Meta AI（旧FAIR）によって開発され、現在はLinux Foundation傘下のPyTorch Foundationによって管理されているオープンソースの深層学習フレームワークです。**動的計算グラフ**（Define-by-Run）で知られており、直感的なモデル構築、デバッグ、研究の柔軟性を実現しつつ、本番環境への展開でも高いパフォーマンスを維持します。

---

## 概要

PyTorchは2つの中核機能を提供します。

- **テンソル計算** – 強力なGPUアクセラレーションを備え、NumPyに似ていますが、自動微分もサポートします。
- **ディープニューラルネットワーク** – テープベースのautogradシステム上に構築されています。

2016年の公開以来、PyTorchはAI研究における支配的なフレームワークとなり、主要な大規模言語モデル（LLaMA、Mistral）、画像生成（Stable Diffusion）、コンピュータビジョンモデルを含む多くの本番システムで広く使用されています。

---

## なぜPyTorchか？

- **Pythonらしさと動的性** – グラフは実行時に構築されます。標準のPython制御フローが自然に機能し、`pdb`や`ipdb`などのツールで容易にデバッグできます。
- **適切に設計されたAutograd** – `torch.autograd`エンジンは、有向非巡回グラフ（DAG）に操作を記録し、自動的に勾配を計算します。
- **本番環境対応** – `torch.compile`はコード変更なしでグラフレベルの最適化をもたらします。TorchScriptとONNXのサポートにより、サービングが可能です。
- **分散トレーニング** – DDP（Data Distributed Parallel）とFSDP（Fully Sharded Data Parallel）をファーストクラスでサポートし、数百GPUへのスケーリングに不可欠です。
- **豊富なエコシステム** – ビジョン（`torchvision`）、オーディオ（`torchaudio`）、テキスト（`torchtext`）、グラフニューラルネットワーク（`PyTorch Geometric`）などのライブラリ。

---

## インストール

お使いのハードウェアとCUDAバージョンに合ったコマンドを選択してください：

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

インストールを確認します：

```python
import torch
print(torch.__version__)          # e.g., 2.6.0
print(torch.cuda.is_available())  # True if CUDA is properly set up
```

---

## 中核概念

### テンソル

`torch.Tensor`は、CPUまたはGPUで実行でき、オプションで自動微分のための勾配を追跡する多次元配列です。

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

`requires_grad`フラグは、autogradにテンソル上の操作を追跡するよう指示します。

```python
x = torch.randn(3, requires_grad=True)
y = x * 2
z = y.mean()
z.backward()                             # compute gradients
print(x.grad)                            # dy/dx
```

`backward()`を呼び出すたびに、勾配がリーフテンソルの`.grad`属性に蓄積されます。トレーニングループでは、新しいバックワードパスの前に勾配をゼロにする必要があります（通常は`optimizer.zero_grad()`を使用）。

### ニューラルネットワーク（`nn.Module`）

`nn.Module`をサブクラス化し、`forward`メソッドを実装してモデルを定義します：

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

すべてのパラメータは自動的に登録され、`model.parameters()`を介してアクセスできます。

---

## モデルのトレーニング

典型的なトレーニングループには、データの読み込み、フォワードパス、損失の計算、勾配の計算、パラメータの更新が含まれます。

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

実際のデータセットでは、データを`torch.utils.data.DataLoader`でラップします。これにより、バッチ処理、シャッフル、並列読み込みが提供されます。

---

## 高度な機能

### `torch.compile`

PyTorch 2.0で導入された`torch.compile`は、モデルグラフを最適化された融合カーネルにコンパイルします（TorchDynamo、AOTAutograd、オプションでTritonを使用）。トレーニングループにコード変更を加えることなく、30～50%の高速化を実現することがよくあります。

```python
model = TwoLayerNet()
model = torch.compile(model, mode="reduce-overhead")

# Use model normally thereafter
output = model(inputs)
```

コンパイルモード：
- `"default"`：バランスの取れた最適化
- `"reduce-overhead"`：Pythonのオーバーヘッドを最小化し、推論を高速化
- `"max-autotune"`：最大速度のために多くのカーネル設定を試行するが、コンパイル時間が長い

### 分散トレーニング

PyTorchはいくつかのレベルの並列処理を提供します：

- **DataParallel (DP)** – シンプルですが効率は低く、バッチをGPU間で分割します。
- **DistributedDataParallel (DDP)** – マルチGPUトレーニングに推奨され、同期をより効率的に処理します。
- **Fully Sharded Data Parallel (FSDP)** – モデルのパラメータ、勾配、オプティマイザの状態をデバイス間でシャーディングし、非常に大規模なモデル（例：LLaMA）のトレーニングを可能にします。

基本的なDDPの使用法：

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

TorchScriptを使用すると、トレースやスクリプティングを介して、Python以外の環境（C++、モバイルなど）にデプロイするためにモデルをシリアライズできます。

```python
scripted_model = torch.jit.script(model)
scripted_model.save("model.pt")
```

### エコシステム

| ライブラリ | 目的 |
|---------|---------|
| `torchvision` | コンピュータビジョンのためのデータセット、モデル、変換 |
| `torchaudio` | オーディオI/O、変換、事前学習モデル |
| `torchtext` | テキスト処理ユーティリティとデータセット |
| `PyTorch Geometric` | グラフニューラルネットワーク |
| `Captum` | モデルの解釈可能性 |
| `TorchMetrics` | 評価のための標準化されたメトリクス |
| `PyTorch Lightning` | 高レベルトレーニングラッパー（ボイラープレートを削減） |

---

## リソース

- **公式ウェブサイト:** [pytorch.org](https://pytorch.org)
- **ドキュメント:** [pytorch.org/docs](https://pytorch.org/docs)
- **チュートリアル:** [pytorch.org/tutorials](https://pytorch.org/tutorials)
- **ソースコード:** [github.com/pytorch/pytorch](https://github.com/pytorch/pytorch)
- **モデルハブ:** [huggingface.co/models](https://huggingface.co/models)（数千の事前学習済みPyTorchモデル）

---

> **ステータス:** 下書き – このドキュメントは生きたリファレンスです。貢献や修正は、リポジトリのイシュートラッカーからお願いします。