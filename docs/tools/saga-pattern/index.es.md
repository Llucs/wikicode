---
title: Patrón Saga
description: Un patrón de diseño para gestionar transacciones distribuidas a través de múltiples servicios o recursos en arquitecturas de microservicios.
created: 2026-07-09
tags:
  - microservicios
  - transacciones distribuidas
  - patrones de diseño
  - patrón saga
status: borrador
---

# Patrón Saga

## Visión General

El patrón Saga es un patrón de diseño utilizado en sistemas distribuidos para gestionar transacciones a través de múltiples servicios o recursos. Garantiza la consistencia y la confiabilidad de las operaciones al mantener una secuencia de operaciones que deben completarse con éxito para considerar la transacción válida. Si alguna operación falla, el patrón permite la devolución de todas las operaciones completadas para mantener la integridad del sistema.

## Características Principales

1. **Operaciones Compensatorias**: Para cada unidad de trabajo (operación), se define una operación compensatoria correspondiente que puede revertir los cambios realizados por la unidad de trabajo. Esto garantiza que si una operación falla, el sistema puede revertir a su estado previo.
2. **Ejecución Secuencial**: Las operaciones se ejecutan en un orden específico, y cada operación depende del éxito de la operación anterior.
3. **Consistencia Eventual**: El patrón asegura que el sistema se mueve hacia un estado consistente a lo largo del tiempo, incluso si las transacciones individuales fallan.
4. **Idempotencia**: Las operaciones dentro de un saga deben ser idempotentes para asegurar que el estado del sistema no cambie si se llama múltiples veces a la misma operación.

## Historia

El patrón Saga se desarrolló para abordar los desafíos de la gestión de transacciones distribuidas en arquitecturas de microservicios. Antes de la aparición de los microservicios, las aplicaciones monolíticas generalmente gestionaban las transacciones a nivel de la base de datos. Sin embargo, a medida que las aplicaciones se volvieron más distribuidas, la complejidad de la gestión de transacciones a través de múltiples servicios aumentó. El patrón Saga fue introducido como una solución para manejar estas complejidades.

El concepto de Sagas se remonta al siglo XX con el trabajo de Jim Gray sobre el procesamiento de transacciones, pero adquirió notoriedad en el contexto de microservicios y sistemas distribuidos a principios del siglo XXI.

## Casos de Uso

1. **Transacciones Financieras**: El procesamiento de transacciones como transferencias, pagos y devoluciones requiere garantizar que los fondos se muevan correctamente entre cuentas. Un saga puede gestionar estas operaciones, asegurándose de que si una transferencia falla, la balance original se restaura.
2. **Procesamiento de Pedidos**: En comercio electrónico, el procesamiento de un pedido implica múltiples pasos como la reserva de producto, la actualización de inventario y la facturación al cliente. Un saga puede garantizar que todos estos pasos se completen con éxito o se deshagan si alguna falla.
3. **Sistemas de Salud**: En la atención médica, las transacciones como facturación, programación de citas y administración de prescripciones requieren garantizar que todos los pasos se completen o se deshagan si alguna falla para mantener la integridad de los datos del paciente.
4. **Reclamaciones de Seguros**: La gestión de reclamaciones de seguros implica múltiples pasos como la procesación de la reclamación, el pago y la validación de documentos. Un saga puede gestionar estas operaciones para garantizar que la reclamación se procese correctamente o se deshaga si alguna parte del proceso falla.

## Instalación y Configuración

El patrón Saga se implementa generalmente utilizando una combinación de programación de aplicaciones y servicios de middleware. Aquí hay una guía básica de cómo configurar un saga:

1. **Definir Operaciones**: Identificar las operaciones que se deben realizar como parte del saga. Para cada operación, definir la operación compensatoria.
2. **Usar una Fila de Mensajes**: Implementar una fila de mensajes para gestionar la ejecución de operaciones. Esto puede ser un brojero de mensajes como RabbitMQ, Kafka o AWS SQS.
3. **Administrador de Saga**: Crear un administrador de saga que orqueste la secuencia de operaciones. El administrador debe manejar la ejecución de operaciones, rastrear el estado del saga y gestionar la lógica compensatoria si alguna operación falla.
4. **Operaciones Compensatorias**: Implementar las operaciones compensatorias que pueden revertir el estado del sistema a su condición previa si alguna operación falla.

### Uso Básico

1. **Iniciar el Saga**: Iniciar el saga al iniciar la primera operación en la secuencia.
2. **Ejecutar Operaciones**: Ejecutar cada operación en la secuencia. Si alguna operación falla, el saga debe detenerse y realizar las operaciones compensatorias.
3. **Rastrear el Estado**: Mantener un registro estandarizado del saga para rastrear el progreso y asegurarse de que las operaciones se completen en el orden correcto.
4. **Compensar**: Si alguna operación falla, el saga debe realizar las operaciones compensatorias para revertir el sistema a un estado consistente.
5. **Concluir el Saga**: Una vez que todas las operaciones se completan con éxito, el saga puede marcarse como completado.

### Ejemplo

Aquí hay un ejemplo en Python que demuestra la estructura básica de un saga, donde las operaciones se encolan y se ejecutan en secuencia, con operaciones compensatorias definidas para manejar las fallas:

```python
from queue import Queue

# Definir operaciones y operaciones compensatorias
def create_product_reservation(product_id, quantity):
    # Implementación para crear una reserva de producto
    pass

def update_inventory(product_id, quantity):
    # Implementación para actualizar el inventario
    pass

def charge_customer(customer_id, amount):
    # Implementación para facturar al cliente
    pass

def cancel_reservation(product_id, quantity):
    # Implementación para cancelar la reserva
    pass

def refund_customer(customer_id, amount):
    # Implementación para reembolsar al cliente
    pass

# Definir el saga
def process_order(saga_id, product_id, quantity, customer_id, amount):
    saga_queue = Queue()

    try:
        saga_queue.put(create_product_reservation(product_id, quantity))
        saga_queue.put(update_inventory(product_id, quantity))
        saga_queue.put(charge_customer(customer_id, amount))
        
        while not saga_queue.empty():
            operation = saga_queue.get()
            operation()
        
        # Marcar el saga como completado
        print(f"Saga {saga_id} completada con éxito.")
    except Exception as e:
        # Realizar operaciones compensatorias
        while not saga_queue.empty():
            operation = saga_queue.get()
            operation()
        print(f"Saga {saga_id} falló. Se realizaron acciones compensatorias.")

# Iniciar el saga
process_order(1, "P123", 10, "C12345", 100)
```

Este ejemplo demuestra la estructura básica de un saga, donde las operaciones se encolan y se ejecutan en secuencia, con operaciones compensatorias definidas para manejar las fallas.

## Conclusión

El patrón Saga es una solución robusta para gestionar transacciones a través de múltiples servicios en sistemas distribuidos. Al garantizar que las operaciones se ejecuten en un orden específico y proporcionar operaciones compensatorias para manejar las fallas, el patrón ayuda a mantener la integridad del sistema. Entender el patrón Saga es crucial para desarrollar arquitecturas de microservicios confiables y escalables.