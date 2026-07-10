---
title: Políticas de Esgotamento do Cache
description: Técnicas para gerenciar a remoção de dados de um cache quando o cache ultrapassa seu limite de capacidade, garantindo desempenho ótimo e utilização de recursos eficiente.
created: 2026-07-10
tags:
  - cache
  - performance
  - design de sistemas
  - gerenciamento de memória
status:草稿
---

# Políticas de Esgotamento do Cache

Políticas de esgotamento do cache são estratégias usadas para gerenciar a remoção de dados de um cache quando o cache ultrapassa seu limite de capacidade. Essas políticas são cruciais para otimizar o desempenho e eficiência dos sistemas de cache, especialmente em sistemas distribuídos, bancos de dados e aplicativos web.

## O que é uma Política de Esgotamento do Cache?

Uma política de esgotamento do cache determina quais entradas do cache são removidas para fazer espaço para novos dados. Essa política é essencial para gerenciar o uso de memória do cache e garantir que o cache permaneça performático e relevante.

### Características Principais

1. **Gerenciamento de Memória**: Políticas de esgotamento ajudam a gerenciar os recursos de memória limitados do cache.
2. **Atualidade dos Dados**: Garante que os dados mais recentes ou relevantes permaneçam no cache.
3. **Consistência**: Mantém a consistência entre o cache e o armazenamento subjacente.
4. **Desempenho**: Equilibra a taxa de acertos do cache com o custo de recuperar dados do backend.

## Políticas de Esgotamento Comuns

### 1. Menos Usados Recentemente (LRU)

- **Descrição**: Remove os ítens menos usados recentemente primeiro.
- **Implementação**: Registra a frequência e a recência do uso de cada item.
- **Cenários de Uso**: Eficaz em cenários onde as padrões de acesso a dados são previsíveis.
- **Instalação e Uso Básico**:
  - **Instalação**: Implemente via bibliotecas ou frameworks que suportam cache LRU (por exemplo, `cachetools` em Python, `ConcurrentHashMap` com `LRUCache` em Java).
  - **Uso Básico**: Inicialize o cache com um tamanho máximo especificado e utilize métodos para adicionar, recuperar e remover itens.

```python
from cachetools import LRUCache

cache = LRUCache(maxsize=100)

# Adicionando itens ao cache
cache['key1'] = 'value1'
cache['key2'] = 'value2'

# Recuperando itens do cache
print(cache['key1'])  # Saída: value1
```

### 2. Menos Usados Freqüentemente (LFU)

- **Descrição**: Remove os itens com a menor frequência de uso.
- **Implementação**: Registra a frequência de acesso a cada item.
- **Cenários de Uso**: Adecuado para cenários onde o padrão de uso de dados não é linear e pode fluctuar.
- **Instalação e Uso Básico**:
  - **Instalação**: Use bibliotecas como `cachetools` em Python.
  - **Uso Básico**: Inicialize um cache LFU com um tamanho máximo e utilize-o de forma semelhante ao LRU.

```python
from cachetools import LFUCache

cache = LFUCache(maxsize=100)

# Adicionando itens ao cache
cache['key1'] = 'value1'
cache['key2'] = 'value2'

# Recuperando itens do cache
print(cache['key1'])  # Saída: value1
```

### 3. FIFO (Primeiro-In, Primeiro-Out)

- **Descrição**: Remove os itens que foram adicionados primeiro.
- **Implementação**: Simples, apenas mantenha uma fila de itens.
- **Cenários de Uso**: Útil em cenários onde a ordem temporal dos dados é importante.
- **Instalação e Uso Básico**:
  - **Instalação**: Use bibliotecas de fila padrão ou estruturas de dados.
  - **Uso Básico**: Adicione itens à fila e remova os itens mais antigos quando o cache estiver cheio.

```python
from collections import deque

cache = deque(maxlen=100)

# Adicionando itens ao cache
cache.append('value1')
cache.append('value2')

# Removendo o item mais antigo
print(cache.popleft())  # Saída: value1
```

### 4. Remoção Aleatória

- **Descrição**: Remove itens aleatoriamente do cache.
- **Implementação**: Simples, use seleção aleatória.
- **Cenários de Uso**: Adecuado para cenários onde o cache não está sobrecarregado e a aleatorização é aceitável.
- **Instalação e Uso Básico**:
  - **Instalação**: Use funções de geração de números aleatórios integradas.
  - **Uso Básico**: Remova itens com base em um processo de seleção aleatória.

```python
import random

cache = ['value1', 'value2', 'value3']

# Removendo um item aleatoriamente
random_item = random.choice(cache)
cache.remove(random_item)
print(random_item)  # Saída: Item selecionado aleatoriamente
```

### 5. Esgotamento Baseado em Tamanho

- **Descrição**: Evica itens com base no tamanho total do cache.
- **Implementação**: Registra o tamanho de cada item e remove os maiores.
- **Cenários de Uso**: Útil em cenários onde o tamanho dos itens de dados varia significativamente.
- **Instalação e Uso Básico**:
  - **Instalação**: Implemente lógica personalizada para rastrear os tamanhos de itens.
  - **Uso Básico**: Remova os itens mais grandes quando o tamanho do cache exceder o limite.

```python
class SizeBasedCache:
    def __init__(self, max_size):
        self.cache = {}
        self.max_size = max_size

    def add(self, key, value, size):
        if len(self.cache) >= self.max_size:
            max_size_item = max(self.cache.items(), key=lambda x: x[1])
            del self.cache[max_size_item[0]]
        self.cache[key] = size

cache = SizeBasedCache(max_size=100)
cache.add('key1', 'value1', 10)
cache.add('key2', 'value2', 20)

print(cache.cache)  # Saída: {'key2': 20}
```

## Histórico

Políticas de esgotamento têm sido parte dos sistemas de cache desde os primórdios da computação. As primeiras políticas formais de esgotamento foram desenvolvidas na década de 1960 com a introdução de sistemas de mainframe. Ao longo do tempo, à medida que os recursos de computação e as necessidades de gerenciamento de dados cresceram, políticas mais sofisticadas foram desenvolvidas para lidar com conjuntos de dados maiores e mais complexos.

## Cenários de Uso

- **Caching Web**: Para armazenar páginas web ou recursos acessados frequentemente, reduzindo a carga nos servidores e melhorando a experiência do usuário.
- **Caching de Banco de Dados**: Para armazenar resultados de consultas, reduzindo a necessidade de consultar o banco de dados repetidamente.
- **Aplicações Móveis**: Para armazenar dados acessados frequentemente para melhorar o desempenho da aplicação e reduzir o uso de rede.
- **Computação em Nuvem**: Para gerenciar o uso de memória nos caches em sistemas distribuídos e microserviços.

## Conclusão

Políticas de esgotamento do cache são um componente crucial dos sistemas de cache modernos, ajudando a garantir o uso eficiente de memória e um desempenho ótimo. Ao escolher a política apropriada, os desenvolvedores podem melhorar a confiabilidade e a velocidade de suas aplicações, levando a uma melhor experiência do usuário e a um uso mais eficiente dos recursos.