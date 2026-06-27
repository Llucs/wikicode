---
title: Patrón de Proxy
description: Un patrón de diseño de software que permite crear un sustituto o objeto placeholder para controlar el acceso a otro objeto, a menudo con fines de caché, control o seguridad.
created: 2026-06-27
tags:
  - patrones-de-diseno
  - patrones-estructurales
  - python
  - java
  - c++
status: borrador
---

# Patrón de Proxy

## ¿Qué es el Patrón de Proxy?

El Patrón de Proxy es un patrón de diseño estructural que permite crear un sustituto o objeto placeholder para controlar el acceso a otro objeto. Este patrón es particularmente útil para administrar el acceso a recursos, asegurar la seguridad y optimizar el rendimiento.

## Características Clave

1. **Control de Acceso**: Permite el acceso controlado a un objeto real.
2. **Administración de Recursos**: Se puede usar para administrar recursos como archivos, bases de datos o conexiones de red.
3. **Optimización del Rendimiento**: Permite el cálculo perezoso o el caché para mejorar el rendimiento.
4. **Seguridad**: Proporciona una capa de seguridad al controlar qué partes del objeto real son accesibles.
5. **Registros y Supervisión**: Puede registrar operaciones o monitorear patrones de uso.

## Historia

El Patrón de Proxy fue descrito por primera vez por Erich Gamma, Richard Helm, Ralph Johnson y John Vlissides en su libro "Design Patterns: Elements of Reusable Object-Oriented Software". El libro, a menudo referido como el libro del "Gang of Four" (GoF), fue publicado en 1994 y presentó el Patrón de Proxy junto con otros patrones de diseño. Desde entonces, el patrón ha sido ampliamente utilizado en el desarrollo de software para resolver diversos problemas relacionados con la administración y control de recursos.

## Casos de Uso

1. **Proxy Remoto**: Permite el acceso remoto a un objeto proporcionando una representación local de un objeto remoto.
2. **Proxy Virtual**: Proporciona un sustituto ligero y eficiente para un objeto costoso de crear.
3. **Proxy de Protección**: Controla el acceso a un objeto proporcionando un proxy que impone políticas de seguridad.
4. **Puntero Inteligente**: Gestiona la vida útil de un objeto y asegura la administración adecuada de recursos.
5. **Proxy Virtual para Caché**: Almacena datos para evitar operaciones caras y mejorar el rendimiento.

## Instalación

El Patrón de Proxy puede implementarse en varios lenguajes de programación. Aquí hay un ejemplo en Python:

```python
class RealSubject:
    def operation(self):
        return "RealSubject: Handling request."

class Proxy:
    def __init__(self, real_subject=None):
        self._real_subject = real_subject

    def operation(self):
        if self.check_access():
            print("Proxy: Performing operation.")
            return self._real_subject.operation()
        else:
            return "Proxy: Access denied."

    def check_access(self):
        # Simulación de la lógica de control de acceso
        return True  # Simplicidad: siempre se permite el acceso

# Código del cliente
real_subject = RealSubject()
proxy = Proxy(real_subject)

proxy.operation()
```

### Ejemplo Detallado

```python
class RealSubject:
    def operation(self):
        return "RealSubject: Handling request."

class Proxy:
    def __init__(self, real_subject=None):
        self._real_subject = real_subject
        self._access_granted = False

    def operation(self):
        if self.check_access():
            print("Proxy: Performing operation.")
            return self._real_subject.operation()
        else:
            return "Proxy: Access denied."

    def check_access(self):
        # Simulación de la lógica de control de acceso
        return self._access_granted

# Código del cliente
real_subject = RealSubject()
proxy = Proxy(real_subject)

# Grant access
proxy._access_granted = True
print(proxy.operation())

# Deny access
proxy._access_granted = False
print(proxy.operation())
```

## Uso Básico

1. **Crear el RealSubject**: Este es el objeto real que realiza el trabajo real.
2. **Crear el Proxy**: El objeto proxy actúa como una interfaz para el objeto real.
3. **Verificar el Acceso**: El proxy verifica si es permitido el acceso al objeto real.
4. **Delegar Operaciones**: Si se permite el acceso, el proxy delega la operación al objeto real; en caso contrario, deniega el acceso.

## Conclusión

El Patrón de Proxy es un patrón de diseño versátil que ayuda a administrar el acceso, optimizar el rendimiento y mejorar la seguridad en sistemas de software. Al proporcionar un modo flexible de controlar el acceso a un objeto, el Patrón de Proxy puede aplicarse en una variedad de escenarios, convirtiéndolo en una herramienta valiosa en el conjunto de herramientas del desarrollador de software.