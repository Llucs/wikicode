---
title: Políticas de Expulsión del Cache
description: Técnicas para gestionar el almacenamiento en caché manteniendo la relevancia de los datos más actualizados o recientes y eliminando los menos relevantes o más antiguos para hacer espacio para nuevos datos, asegurando una optimización de rendimiento y utilización de recursos.
created: 2026-07-10
tags:
  - caché
  - rendimiento
  - diseño del sistema
  - gestión de memoria
status: borrador
---

# Políticas de Expulsión del Cache

Las políticas de expulsión del cache son estrategias utilizadas para gestionar la eliminación de datos de un cache cuando este excede su capacidad. Estas políticas son cruciales para optimizar el rendimiento y eficiencia de los sistemas de caché, especialmente en sistemas distribuidos, bases de datos y aplicaciones web.

## ¿Qué es una Política de Expulsión del Cache?

Una política de expulsión del cache determina cuáles entradas del cache se eliminan para hacer espacio para nuevos datos. Esta política es esencial para gestionar el uso de memoria del cache y garantizar que el cache permanezca performante y relevante.

### Características Principales

1. **Gestión de Memoria**: Las políticas de expulsión ayudan a gestionar los recursos de memoria limitados del cache.
2. **Frescura de los Datos**: Asegura que los datos más recientes o relevantes permanezcan en el cache.
3. **Consistencia**: Mantiene la consistencia entre el cache y la base de datos subyacente.
4. **Rendimiento**: Equilibra las tasas de impacto del cache con el costo de recuperar datos del backend.

## Políticas de Expulsión Comunes

### 1. Menos Recientemente Usado (LRU)

- **Descripción**: Elimina los elementos menos recientemente usados primero.
- **Implementación**: Registra la frecuencia y recencia de uso de cada elemento.
- **Casos de Uso**: Eficaz en escenarios donde los patrones de acceso a los datos son predecibles.
- **Instalación y Uso Básico**:
  - **Instalación**: Implementar mediante bibliotecas o frameworks que soporten caché LRU (por ejemplo, `cachetools` en Python, `ConcurrentHashMap` con `LRUCache` en Java).
  - **Uso Básico**: Inicializar el cache con un tamaño máximo y usar métodos para añadir, recuperar y eliminar elementos.

```python
from cachetools import LRUCache

cache = LRUCache(maxsize=100)

# Añadir elementos al cache
cache['key1'] = 'value1'
cache['key2'] = 'value2'

# Recuperar elementos del cache
print(cache['key1'])  # Output: value1
```

### 2. Menos Frecuentemente Usado (LFU)

- **Descripción**: Elimina los elementos con menos frecuencia de uso.
- **Implementación**: Registra la frecuencia de acceso a cada elemento.
- **Casos de Uso**: Adecuado para escenarios donde el patrón de uso de los datos no es lineal y puede fluctuar.
- **Instalación y Uso Básico**:
  - **Instalación**: Usar bibliotecas como `cachetools` en Python.
  - **Uso Básico**: Inicializar un cache LFU con un tamaño máximo y usarlo de manera similar a LRU.

```python
from cachetools import LFUCache

cache = LFUCache(maxsize=100)

# Añadir elementos al cache
cache['key1'] = 'value1'
cache['key2'] = 'value2'

# Recuperar elementos del cache
print(cache['key1'])  # Output: value1
```

### 3. FIFO (Primer En Entrar, Primer En Salir)

- **Descripción**: Elimina los elementos que fueron añadidos primero.
- **Implementación**: Mantener una cola de elementos.
- **Casos de Uso**: Útil en escenarios donde la temporalidad de los datos es importante.
- **Instalación y Uso Básico**:
  - **Instalación**: Usar bibliotecas de colas estándar o estructuras de datos.
  - **Uso Básico**: Añadir elementos a la cola y eliminar los más antiguos cuando el cache esté lleno.

```python
from collections import deque

cache = deque(maxlen=100)

# Añadir elementos al cache
cache.append('value1')
cache.append('value2')

# Eliminar el elemento más antiguo
print(cache.popleft())  # Output: value1
```

### 4. Eliminación Aleatoria

- **Descripción**: Elimina elementos aleatorios del cache.
- **Implementación**: Simple, usar selección aleatoria.
- **Casos de Uso**: Adecuado para escenarios donde el cache no está altamente cargado y la aleatorización es aceptable.
- **Instalación y Uso Básico**:
  - **Instalación**: Usar funciones de generación de números aleatorios integradas.
  - **Uso Básico**: Eliminar elementos basándose en un proceso de selección aleatorio.

```python
import random

cache = ['value1', 'value2', 'value3']

# Eliminación aleatoria de un elemento
random_item = random.choice(cache)
cache.remove(random_item)
print(random_item)  # Output: Elemento seleccionado aleatoriamente
```

### 5. Expulsión Basada en Tamaño

- **Descripción**: Evicta elementos basándose en el tamaño total del cache.
- **Implementación**: Registra el tamaño de cada elemento y elimina los más grandes.
- **Casos de Uso**: Útil en escenarios donde el tamaño de los datos de los elementos varía significativamente.
- **Instalación y Uso Básico**:
  - **Instalación**: Implementar lógica personalizada para rastrear el tamaño de los elementos.
  - **Uso Básico**: Eliminar los elementos más grandes cuando el tamaño del cache exceda el umbral.

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

print(cache.cache)  # Output: {'key2': 20}
```

## Historia

Las políticas de expulsión han sido parte de los sistemas de caché desde los inicios de la informática. Las primeras políticas formales de expulsión se desarrollaron en los años 1960 con la introducción de sistemas de mainframe. Con el tiempo, a medida que crecían los recursos de cómputo y las necesidades de gestión de datos, se desarrollaron políticas más sofisticadas para manejar conjuntos de datos más grandes y complejos.

## Casos de Uso

- **Caché de Web**: Para almacenar páginas web o recursos accesados frecuentemente, reduciendo la carga de los servidores y mejorando la experiencia del usuario.
- **Caché de Base de Datos**: Para almacenar resultados de consultas, reduciendo la necesidad de consultar la base de datos repetidamente.
- **Aplicaciones Móviles**: Para almacenar datos accesados frecuentemente para mejorar el rendimiento de la aplicación y reducir el uso de la red.
- **Computación en la Nube**: Para administrar la utilización de memoria del caché en sistemas distribuidos y microservicios.

## Conclusión

Las políticas de expulsión del cache son un componente crítico de los sistemas de caché modernos, ayudando a garantizar una gestión eficiente de la memoria y un rendimiento óptimo. Al elegir la política adecuada, los desarrolladores pueden mejorar la confiabilidad y la velocidad de sus aplicaciones, lo que conduce a mejores experiencias del usuario y un uso más eficiente de los recursos.