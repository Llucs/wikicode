---
title: Patrón de Diseño Proxy
description: Un patrón estructural que permite que un proxy, o sustituto, controle el acceso a otro objeto, a menudo con el propósito de agregar funcionalidades.
created: 2026-07-06
tags:
  - patrones-de-diseño
  - diseño-orientado-a-objetos
  - patrones-estructurales
status: borrador
---

# Patrón de Diseño Proxy

## ¿Qué es el Patrón de Diseño Proxy?

El Patrón de Diseño Proxy es un patrón estructural que proporciona un sustituto o placeholder para otro objeto, controlando el acceso a éste. Permite agregar responsabilidades al objeto original sin modificar su estructura. El objetivo principal del patrón Proxy es proporcionar un sustituto o placeholder para otro objeto. Este patrón se utiliza ampliamente en diversas aplicaciones para gestionar el acceso a recursos, controlar el acceso a datos sensibles y optimizar el rendimiento.

## Características Principales

1. **Objetos de Proxy**: Son objetos que actúan como un sustituto o placeholder para un objeto real. Pueden realizar tareas antes o después del objeto real.
2. **Control de Acceso**: Los proxies pueden controlar el acceso a los objetos reales, permitiendo acciones adicionales antes o después de que se llamen los métodos del objeto real.
3. **Decapado**: Los proxies decapan al cliente del objeto real, proporcionando un nivel de abstracción.
4. **Flexibilidad**: Los proxies se pueden utilizar en diversos escenarios, como objetos remotos, control de acceso a recursos y caché.

## Historia

El Patrón de Diseño Proxy fue formalizado en el libro "Design Patterns: Elements of Reusable Object-Oriented Software" por Erich Gamma, Richard Helm, Ralph Johnson y John Vlissides, comúnmente conocidos como la Gang of Four (GoF). El patrón fue introducido como una manera de proporcionar un acceso controlado a los objetos y gestionar la vida del ciclo de los objetos.

## Casos de Uso

1. **Proxy Remoto**: Permite que un objeto local actúe como proxy para un objeto en un espacio de dirección diferente.
2. **Proxy Virtual**: Se utiliza para proporcionar un proxy de bajo costo para la creación de un objeto costoso.
3. **Proxy de Protección**: Controla el acceso a un objeto sensible. Por ejemplo, un proxy podría utilizarse para controlar el acceso a un archivo o una base de datos.
4. **Proxy Inteligente**: Proporciona una forma de gestionar el estado de un objeto. Por ejemplo, un proxy podría utilizarse para asegurarse de que un objeto esté en un estado válido antes de ser accedido.
5. **Cache Virtual**: Utiliza un proxy para cachear los resultados de una operación costosa.

## Instalación

Dado que el Patrón de Diseño Proxy es un patrón de diseño y no una biblioteca o software, no requiere instalación. Sin embargo, para implementar el patrón en un lenguaje de programación específico, se necesitaría incluir las clases o módulos necesarias y seguir las guías del patrón.

## Uso Básico

Aquí hay un ejemplo simple de la implementación del patrón Proxy en Python:

```python
class RealSubject:
    def operation(self):
        return "RealSubject: Here is the result."

class Proxy:
    def __init__(self):
        self.real_subject = None

    def operation(self):
        if self.real_subject is None:
            self.real_subject = RealSubject()
        return f"Proxy: Processing ({self.real_subject.operation()})"

# Uso
proxy = Proxy()
print(proxy.operation())
```

En este ejemplo:
- `RealSubject` es la clase a la que el proxy controla el acceso.
- `Proxy` es la clase que proporciona un acceso controlado a `RealSubject`.
- El `Proxy` verifica si `real_subject` es `None`. Si lo es, crea una instancia de `RealSubject`. Si no, simplemente llama al método `operation` de `RealSubject`.

## Conclusión

El Patrón de Diseño Proxy es una herramienta poderosa en el kit de herramientas del desarrollador de software. Proporciona una manera de controlar el acceso a los objetos, gestionar recursos y optimizar el rendimiento. Con una comprensión de sus características principales y casos de uso, los desarrolladores pueden implementarlo efectivamente en diversos escenarios.