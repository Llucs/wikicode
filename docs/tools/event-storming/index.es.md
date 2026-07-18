---
title: Event Storming
description: Una técnica colaborativa de taller para explorar procesos empresariales complejos y modelar contextos acotados en el Diseño Dirigido por Dominio (DDD).
created: 2026-07-18
tags:
  - desarrollo de software
  - diseño dirigido por dominio
  - colaboración
  - arquitectura impulsada por eventos
status: borrador
---

# Event Storming

Event Storming es una técnica de taller colaborativo utilizada para explorar procesos empresariales complejos y modelar contextos acotados en el Diseño Dirigido por Dominio (DDD). Involucra la visualización de eventos y sus interacciones en grandes tableros blancos o plataformas digitales, enfocándose en cómo estos eventos fluyen a través del sistema a lo largo del tiempo. Esta técnica ayuda a comprender el dominio, identificar posibles problemas y alinear el entendimiento del equipo sobre los procesos empresariales.

## ¿Qué es Event Storming?

Event Storming es un taller colaborativo que ayuda a los equipos a entender el dominio y el flujo de eventos dentro de él. Involucra la visualización de eventos y sus interacciones en grandes tableros blancos o plataformas digitales, enfocándose en cómo estos eventos fluyen a través del sistema a lo largo del tiempo.

## Características Clave

1. **Enfoque Colaborativo**: Los participantes de diversas funciones (desarrolladores, dueños de producto, expertos en dominio, etc.) trabajan juntos para mapear el dominio.
2. **Enfoque en los Eventos**: La técnica enfatiza comprender el flujo de eventos y sus impactos en el sistema.
3. **Representación Visual**: Los eventos, las entidades y las fronteras se representan usando gráficos sencillos para crear una mappa visual del sistema.
4. **Viaje en el Tiempo**: Los participantes imaginan cómo evoluciona el sistema a lo largo del tiempo, permitiéndoles visualizar el estado del sistema en diferentes puntos en el pasado, presente y futuro.
5. **Mapeo de Dominios**: Ayuda a mapear el dominio para comprender y alinear el entendimiento del equipo sobre los procesos empresariales.

## Historia

Event Storming fue introducido por primera vez por Gregor Hohpe en 2012 en una conferencia de desarrollo de software. La técnica ganó considerable tracción en la comunidad de desarrollo de software debido a su eficacia en desentrañar procesos empresariales y interacciones del sistema. El nombre "Event Storming" proviene de la idea de mapear la tormenta de eventos que ocurren en un dominio empresarial.

## Casos de Uso

1. **Análisis de Dominio**: Ayuda a entender dominios empresariales complejos al desglosar el flujo de eventos.
2. **Modelado**: Facilita la creación de modelos impulsados por eventos que se pueden utilizar para diseñar sistemas de software.
3. **Recolección de Requisitos**: Aísla en la visualización de cómo las diferentes partes del sistema interactúan.
4. **Diseño de Arquitecturas**: Ayuda en el diseño de arquitecturas impulsadas por eventos al mapear cómo fluyen los eventos a través del sistema.
5. **Alineación del Equipo**: Mejora la colaboración entre miembros del equipo al proporcionar un entendimiento compartido del sistema.

## Instalación

Event Storming no requiere la instalación de ningún software específico. Sin embargo, las siguientes herramientas y materiales pueden ser útiles:

- **Grandes Tableros Blancos o Flipcharts**: Para visualizar el flujo de eventos.
- **Marcadores y Post-It**: Para etiquetar eventos y entidades.
- **Herramientas Digitales**: Herramientas como Miro o Mural se pueden usar para Event Stormings remotos.

## Uso Básico

1. **Preparación**: Reúna un equipo de participantes de diversas funciones (desarrolladores, dueños de producto, expertos en dominio, etc.).
2. **Introducción**: Explica brevemente el concepto de Event Storming y los objetivos de la sesión.
3. **Mapeo del Dominio**: Comience por mapear el dominio usando gráficos sencillos para representar entidades, eventos y fronteras.
4. **Mapeo de Eventos**: Mapee el flujo de eventos, comenzando con el primer evento y rastreando su impacto en el sistema.
5. **Viaje en el Tiempo**: Discuta cómo evoluciona el sistema a lo largo del tiempo, considerando diferentes estados y eventos.
6. **Discusión y Refinamiento**: Facilita discusiones para refinarel modelo y asegurarse de que todos los miembros del equipo tengan un entendimiento común.
7. **Documentación**: Documente los hallazgos y úselos para guiar el desarrollo del sistema.

### Ejemplo

Imagínese un dominio empresarial de retail donde los clientes colocan pedidos, se envían los artículos y se realizan pagos. El proceso de Event Storming implicaría mapear eventos como "Pedido Colocado," "Pedido Enviado," "Pago Recibido" y sus interacciones con entidades como "Cliente," "Pedido" y "Inventario."

Al visualizar estos eventos y sus impactos, el equipo puede entender mejor el dominio e identificar posibles atascos o inefficiencias en el sistema.

## Conclusión

Event Storming es una técnica poderosa para entender sistemas complejos y alinear el entendimiento del equipo sobre el dominio. Al enfocarse en eventos y sus interacciones, ayuda a diseñar sistemas de software más efectivos y eficientes. Ya sea para análisis de dominio, recolección de requisitos o diseño de arquitecturas, Event Storming proporciona un enfoque colaborativo y visual para desentrañar las complejidades del dominio empresarial.