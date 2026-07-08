---
title: UnoCSS: Un Framework de CSS sin Configuración y Just-In-Time
description: Un guía detallado sobre UnoCSS, un framework de CSS sin configuración y Just-In-Time (JIT) que genera estilos en tiempo de ejecución. Aprende la instalación, uso y características clave.
created: 2026-07-08
tags:
  - UnoCSS
  - CSS-in-JS
  - JIT
  - Tailwind
  - Performance
status: borrador
---

# UnoCSS: Un Framework de CSS sin Configuración y Just-In-Time

UnoCSS es un framework de CSS sin configuración y Just-In-Time (JIT) que genera estilos en tiempo de ejecución, principalmente escrito en TypeScript. A diferencia de las bibliotecas CSS-in-JS que procesan y empacan estilos de antemano, UnoCSS compila estilos en tiempo de ejecución basándose en las clases utilizadas en tu código. Esta aproximación asegura que solo los estilos necesarios se apliquen, lo que conduce a tamaños de empaquetado reducidos y mejor rendimiento.

## Características Clave
1. **Compilación Just-In-Time:** UnoCSS compila estilos en tiempo de ejecución, asegurando que solo las clases realmente utilizadas en tu proyecto se incluyan en la salida final.
2. **Pequeño Tamaño:** UnoCSS está diseñado para ser extremadamente ligero, con un pequeño footprint que minimiza el impacto en el rendimiento de tu proyecto.
3. **Amigable para Tree-Shaking:** Los estilos generados pueden ser tree-shaken, lo que significa que los estilos no utilizados se eliminan durante el proceso de compilación, optimizando aún más el empaquetado final.
4. **Personalizable:** UnoCSS permite una extensa personalización a través de opciones e插件方