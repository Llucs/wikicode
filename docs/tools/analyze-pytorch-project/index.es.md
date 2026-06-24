---
title: PyTorch - Framework de Aprendizaje Profundo
description: Una biblioteca de aprendizaje automático de código abierto para Python que proporciona computación tensorial y redes neuronales profundas.
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

# PyTorch – Framework de Aprendizaje Profundo

**PyTorch** es un framework de aprendizaje profundo de código abierto desarrollado por Meta AI (anteriormente FAIR) y ahora gobernado por la Fundación PyTorch bajo la Fundación Linux. Es mejor conocido por su **grafo de cómputo dinámico** (Define-by-Run), que permite la construcción de modelos intuitiva, la depuración y la flexibilidad en la investigación, manteniendo al mismo tiempo un alto rendimiento para el despliegue en producción.

---

## Visión general

PyTorch proporciona dos capacidades principales:

- **Cómputo de tensores** con fuerte aceleración por GPU, similar a NumPy pero con diferenciación automática.
- **Redes neuronales profundas** construidas sobre un sistema autograd basado en cintas.

Desde su lanzamiento público en 2016, PyTorch se ha convertido en el framework dominante en la investigación de IA y se utiliza ampliamente en sistemas de producción, incluidos la mayoría de los grandes modelos de lenguaje (LLaMA, Mistral), generación de imágenes (Stable Diffusion) y modelos de visión por computadora.

---

## ¿Por qué PyTorch?

- **Pythonico y Dinámico** – El grafo se construye sobre la marcha. El flujo de control estándar de Python funciona naturalmente, facilitando la depuración con herramientas como `pdb` o `ipdb`.
- **Autograd hecho correctamente** – El motor `torch.autograd` registra las operaciones en un grafo acíclico dirigido (DAG) y calcula los gradientes automáticamente.
- **Listo para producción** – `torch.compile` aporta optimizaciones a nivel de grafo sin cambios de código; el soporte de TorchScript y ONNX permite el servicio.
- **Entrenamiento Distribuido** – Soporte de primera clase para DDP (Data Distributed Parallel) y FSDP (Fully Sharded Data Parallel), esencial para escalar a cientos de GPUs.
- **Ecosistema rico** – Bibliotecas para visión (`torchvision`), audio (`torchaudio`), texto (`torchtext`), redes neuronales de grafos (`PyTorch Geometric`) y más.

---

## Instalación

Seleccione el comando que coincida con su hardware y versión de CUDA:

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

Verifique la instalación:

```python
import torch
print(torch.__version__)          # e.g., 2.6.0
print(torch.cuda.is_available())  # True if CUDA is properly set up
```

---

## Conceptos Fundamentales

### Tensores

Un `torch.Tensor` es un arreglo multidimensional que puede ejecutarse en CPU o GPU y opcionalmente rastrear gradientes para diferenciación automática.

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

La bandera `requires_grad` le indica a autograd que rastree las operaciones en el tensor.

```python
x = torch.randn(3, requires_grad=True)
y = x * 2
z = y.mean()
z.backward()                             # compute gradients
print(x.grad)                            # dy/dx
```

Cada llamada a `backward()` acumula los gradientes en el atributo `.grad` de los tensores hoja. En los bucles de entrenamiento, los gradientes deben ponerse a cero antes de cada nuevo pase hacia atrás (normalmente con `optimizer.zero_grad()`).

### Redes Neuronales (`nn.Module`)

Defina un modelo subclasificando `nn.Module` e implementando el método `forward`:

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

Todos los parámetros se registran automáticamente y se pueden acceder a través de `model.parameters()`.

---

## Entrenando un Modelo

Un bucle de entrenamiento típico incluye carga de datos, pase hacia adelante, cálculo de pérdida, cálculo de gradientes y actualización de parámetros.

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

Para conjuntos de datos reales, envuelva sus datos en un `torch.utils.data.DataLoader` que proporciona agrupación en lotes (batching), mezcla (shuffling) y carga paralela.

---

## Funcionalidades Avanzadas

### `torch.compile`

Introducido en PyTorch 2.0, `torch.compile` compila los grafos del modelo en kernels fusionados optimizados (usando TorchDynamo, AOTAutograd, y opcionalmente Triton). A menudo proporciona aceleraciones del 30–50% sin cambios de código en el bucle de entrenamiento.

```python
model = TwoLayerNet()
model = torch.compile(model, mode="reduce-overhead")

# Use model normally thereafter
output = model(inputs)
```

Modos de compilación:
- `"default"`: optimización equilibrada
- `"reduce-overhead"`: minimiza la sobrecarga de Python, inferencia más rápida
- `"max-autotune"`: prueba muchas configuraciones de kernel para máxima velocidad pero mayor tiempo de compilación

### Entrenamiento Distribuido

PyTorch ofrece varios niveles de paralelismo:

- **DataParallel (DP)** – Simple pero menos eficiente; divide los lotes entre GPUs.
- **DistributedDataParallel (DDP)** – Preferido para entrenamiento multi-GPU; maneja la sincronización de manera más eficiente.
- **Fully Sharded Data Parallel (FSDP)** – Fragmenta los parámetros del modelo, los gradientes y los estados del optimizador entre dispositivos, permitiendo entrenar modelos muy grandes (e.g., LLaMA).

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

TorchScript le permite serializar modelos para su implementación en entornos que no son Python (C++, móvil, etc.) mediante trazado (tracing) o escritura de scripts (scripting).

```python
scripted_model = torch.jit.script(model)
scripted_model.save("model.pt")
```

### Ecosistema

| Library | Propósito |
|---------|----------|
| `torchvision` | Conjuntos de datos, modelos y transformaciones para visión por computadora |
| `torchaudio` | E/S de audio, transformaciones y modelos preentrenados |
| `torchtext` | Utilidades de procesamiento de texto y conjuntos de datos |
| `PyTorch Geometric` | Redes neuronales de grafos |
| `Captum` | Interpretabilidad de modelos |
| `TorchMetrics` | Métricas estandarizadas para evaluación |
| `PyTorch Lightning` | Envoltorio de entrenamiento de alto nivel (reduce código repetitivo) |

---

## Recursos

- **Sitio web oficial:** [pytorch.org](https://pytorch.org)
- **Documentación:** [pytorch.org/docs](https://pytorch.org/docs)
- **Tutoriales:** [pytorch.org/tutorials](https://pytorch.org/tutorials)
- **Código fuente:** [github.com/pytorch/pytorch](https://github.com/pytorch/pytorch)
- **Hub de modelos:** [huggingface.co/models](https://huggingface.co/models) (miles de modelos PyTorch preentrenados)

---

> **Estado:** Borrador – Este documento es una referencia viva. Las contribuciones y correcciones son bienvenidas a través del rastreador de problemas del repositorio.