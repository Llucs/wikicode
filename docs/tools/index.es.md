---
title: Herramientas
description: Herramientas de desarrollo documentadas en WikiCode.
created: 2026-06-03
tags:
  - meta
  - tools
status: stable
---

# Herramientas

Herramientas de desarrollo documentadas en WikiCode. Cada herramienta tiene su propia carpeta en `docs/tools/<slug>/` con un resumen en `index.md`.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Creado: 2026-06-03</span>
<span class="wikicode-meta-updated">Última actualización: automático (git)</span>
</div>

## Por ecosistema

Las herramientas se clasifican por ecosistema. Ver el índice de etiquetas para la lista completa.

| Ecosistema | Herramientas |
|-----------|-------|
| Contenedor | Docker, Podman, Portainer |
| CI/CD     | Jenkins, ArgoCD |
| API       | Postman, cURL |
| JavaScript| npm, Jest |
| Editor    | Visual Studio Code |
| CLI       | fzf |
| Android   | SpeedCool |
| Monitoreo | Grafana, Heimdall |
| VCS       | Git |

## Cómo se añaden las herramientas

Tanto el agente de IA como los colaboradores humanos siguen la misma receta:

1. Investiga la herramienta utilizando búsqueda web (Wikipedia + DuckDuckGo).
2. Escribe un resumen `docs/tools/<slug>/index.md`.
3. Añade frontmatter con `title`, `description`, `created`, `tags` y `ecosystem`.
4. Ejecuta `mkdocs build --clean` para validar.

## Herramientas actuales

<!--awesome-pages:hide-->
<!--awesome-pages:reveal-->

## Convenciones

- Una carpeta por herramienta. Nombre de la carpeta: minúsculas, con guiones.
- `index.md` es el resumen público.
- El frontmatter debe incluir `title`, `description`, `created`, `tags`, `ecosystem` y `status`.
- Una página de herramienta debe incluir: un párrafo "qué es", instalación, uso básico y características clave con ejemplos.