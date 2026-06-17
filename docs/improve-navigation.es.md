---
title: Auditoría de navegación para WikiCode
description: Análisis y mejoras propuestas para la navegación del sitio WikiCode.
created: 2026-06-14
tags:
  - meta
  - guide
status: draft
---

# Auditoría de navegación

## Estructura actual

La navegación principal está definida en `mkdocs.yml` e incluye actualmente:

- Inicio
- Búsqueda
- Primeros pasos
- Rutas de aprendizaje
- Guías
- Referencia (Glosario, Arquitectura, Changelog)
- Temas
- Herramientas
- Etiquetas
- Blog
- Proyectos
- Snippets
- Informes

## Mejoras propuestas

1. **Agrupar secciones meta** bajo un único elemento de menú "Acerca de" o "WikiCode" (Informes, Changelog, Arquitectura)
2. **Mover Etiquetas dentro de Temas** ya que son conceptos relacionados
3. **Añadir indicadores visuales** para contenido actualizado recientemente
4. **Asegurar que las migas de pan** estén activas en todos los niveles de navegación

## Implementación

Todos los cambios deben realizarse en el bloque `nav:` en `mkdocs.yml`.