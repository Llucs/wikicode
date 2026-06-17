---
title: WikiCode
description: Un wiki vivo para desarrolladores — artículos, proyectos y snippets mantenidos a lo largo del tiempo.
created: 2026-06-03
tags:
  - meta
  - overview
status: stable
---

# WikiCode

Un wiki vivo para desarrolladores construido y mantenido a lo largo del tiempo. Cada página que lees aquí se genera directamente desde el repositorio, por lo que el sitio es siempre un espejo fiel de la fuente de verdad.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Creado: 2026-06-03</span>
<span class="wikicode-meta-updated">Última actualización: auto (git)</span>
</div>

## Lo que encontrarás

<div class="grid cards" markdown>

- :material-book-open-page-variant-outline: __Artículos y guías__

    Explicaciones detalladas de conceptos, patrones y herramientas. Ver [Guías](guides/index.md).

- :material-folder-outline: __Proyectos__

    Proyectos autónomos y ejecutables. Ver [Proyectos](projects/index.md).

- :material-code-tags: __Snippets__

    Snippets de código pequeños, enfocados y listos para copiar y pegar. Ver [Snippets](snippets/index.md).

- :material-school-outline: __Rutas de aprendizaje__

    Órdenes de lectura seleccionados para nuevos usuarios. Ver [Rutas de aprendizaje](learning-paths.md).

- :material-tag-multiple-outline: __Temas y etiquetas__

    Explora contenido por tema o por etiqueta. Ver [Temas](topics/index.md) y [Etiquetas](tags.md).

- :material-clipboard-text-outline: __Informes__

    Informes de ejecución con marca de tiempo. Ver [Informes](reports/index.md).

- :material-rss: __Blog__

    Anuncios y artículos más extensos. Ver [Blog](blog/index.md).

- :material-bookshelf: __Referencia__

    Glosario, arquitectura y registro de cambios. Ver [Referencia](reference/glossary.md).

</div>

## Cómo fluyen las actualizaciones

El sitio **nunca se edita directamente**. Se regenera desde el repositorio en cada push a `main`:

```
Autonomous AI agent (OpenCode API) / contributor
        │
        ▼
   commit + push to main
        │
        ▼
   .github/workflows/pages.yml
        │
        ▼
   mkdocs build (from docs/, projects/, snippets/, blog/)
        │
        ▼
   GitHub Pages (public site)
```

Cuando el agente de IA local (o cualquier colaborador) actualiza un archivo Markdown, añade una carpeta de proyecto, escribe un snippet, publica una entrada de blog o mueve una tarea de `queue.md` a `completed.md`, el siguiente push a `main` desencadena una nueva compilación y el sitio publicado refleja el cambio.

## Por dónde empezar

- [Primeros pasos](getting-started.md) — estructura del repositorio, compilación local, convenciones.
- [Rutas de aprendizaje](learning-paths.md) — órdenes de lectura guiados.
- [Referencia](reference/glossary.md) — terminología y arquitectura.