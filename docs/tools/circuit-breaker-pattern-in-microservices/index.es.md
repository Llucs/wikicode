---
title: Patrón del Interruptor de Circuito en Microservicios
description: Un patrón de diseño utilizado en arquitecturas de microservicios para manejar las fallas de manera grácil al ignorar temporalmente las solicitudes a un servicio problemático.
created: 2026-07-15
tags:
  - microservicios
  - resiliencia
  - interruptor de circuito
  - patrón de diseño
status: borrador
---

### Patrón del Interruptor de Circuito en Microservicios

#### ¿Qué es el Patrón del Interruptor de Circuito?
El Patrón del Interruptor de Circuito es un patrón de diseño en ingeniería de software que ayuda a gestionar la resiliencia y la fiabilidad de sistemas distribuidos, especialmente en arquitecturas de microservicios. Es un mecanismo para manejar las fallas en llamadas remotas, permitiendo que los servicios falten rápidamente y se recuperen de las fallas sin causar fallas en cascada en el sistema.

#### Características Principales
1. **Detección de Fallas**: El Interruptor de Circuito detecta cuando un servicio o una llamada de API falla al superar un umbral predefinido de fallas.
2. **Corte del Circuito**: Cuando se supera el umbral, el Interruptor de Circuito tripa, efectivamente cortando el circuito al detener las solicitudes adicionales de llegar al servicio fallido.
3. **Mecanismo de Retroceso**: En lugar de esperar una respuesta potencialmente fallida del servicio, el Interruptor de Circuito activa un mecanismo de retroceso, que devuelve una respuesta predefinida o un mensaje de error al llamador.
4. **Tiempo de Out y Repetición**: El Interruptor de Circuito puede ser configurado para introducir un mecanismo de tiempo de out y repetición para manejar las fallas transitórias.
5. **Reinicio del Circuito**: Una vez que el servicio comienza a funcionar correctamente nuevamente, el Interruptor de Circuito reinicia y permite el envío de tráfico al servicio de nuevo.

#### Historia
El concepto del Interruptor de Circuito fue introducido por primera vez en el dominio de la electrónica y la ingeniería de hardware. Fue adaptado posteriormente a la ingeniería de software, particularmente en el contexto de sistemas distribuidos, por Martin Fowler y James Lewis en su artículo de 2010, "Microservicios: Diseñando Servicios Finamente Granulados," publicado en su sitio web, MartinFowler.com.

#### Casos de Uso
1. **Manejo de Fallos del Servicio**: En una arquitectura de microservicios, si un servicio downstream falla, el Interruptor de Circuito puede prevenir que otros servicios intenten comunicarse con él, evitando así fallas en cascada.
2. **Optimización de Rendimiento**: Al cortar el circuito, el Interruptor de Circuito puede prevenir el procesamiento innecesario y mejorar el rendimiento general del sistema.
3. **Manejo de Errores**: Proporciona un mecanismo para manejar los errores de manera grácil, reduciendo el impacto de las fallas en el sistema en su conjunto.
4. **Monitoreo en Tiempo Real**: El Interruptor de Circuito puede ser utilizado para monitorear la salud de los servicios y proporcionar retroalimentación en tiempo real sobre el estado del sistema.

#### Instalación
El patrón del Interruptor de Circuito puede implementarse utilizando diversas bibliotecas y frameworks dependiendo del lenguaje de programación y framework en uso. Aquí se presentan algunas implementaciones comunes:

- **Java**: Hystrix (de Netflix), Resilience4j, y OpenHystrix.
- **.NET**: Polly.
- **Python**: CircuitBreaker.
- **JavaScript**: @liarnp/circuitbreaker.

Por ejemplo, usando Resilience4j en Java:

```java
import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;

public class CircuitBreakerExample {
    private final CircuitBreakerRegistry circuitBreakerRegistry;
    private final CircuitBreaker circuitBreaker;

    public CircuitBreakerExample() {
        circuitBreakerRegistry = CircuitBreakerRegistry.of("exampleCircuitBreaker");
        circuitBreaker = circuitBreakerRegistry.circuitBreaker("exampleCircuitBreaker");
    }

    public void performCall() {
        if (circuitBreaker.isOpen()) {
            System.out.println("El interruptor de circuito está abierto, retrocediendo...");
            return;
        }
        try {
            // Realizar la llamada al servicio
        } catch (Exception e) {
            circuitBreakerRegistry.fail(CircuitBreaker.of("exampleCircuitBreaker"));
        }
    }
}
```

#### Uso Básico
1. **Inicialización**: Inicialice el Interruptor de Circuito con la configuración deseada e inscríbalo en el registro del Interruptor de Circuito.
2. **Uso**: Use el Interruptor de Circuito para envolver la llamada al servicio. Si la llamada falla, el Interruptor de Circuito cortará el circuito y las llamadas posteriores usarán el mecanismo de retroceso.
3. **Reinicio**: Permíta que el Interruptor de Circuito se reinicie por sí mismo cuando el servicio comienza a funcionar correctamente nuevamente.

Al implementar el patrón del Interruptor de Circuito, los desarrolladores pueden mejorar la resiliencia y la fiabilidad de sus microservicios, asegurándose de que el sistema pueda manejar las fallas de manera grácil y mantener la alta disponibilidad.