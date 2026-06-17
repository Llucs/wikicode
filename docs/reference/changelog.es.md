---
title: Registro de cambios
description: Cambios notables en WikiCode.
created: 2026-06-03
tags:
  - reference
  - meta
status: stable
---

# Registro de cambios

Cambios notables en WikiCode. Las ediciones menores y cotidianas se registran
en el historial de git; solo los cambios estructurales y visibles para el usuario
aparecen aquí.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Creado: 2026-06-03</span>
<span class="wikicode-meta-updated">Última actualización: auto (git)</span>
</div>

## 1.0.0 — 2026-06-03 — Bootstrap

Estructura inicial orientada a producción.

### Añadido

- **Generación del sitio.** MkDocs (tema Material) con búsqueda del lado del
  cliente, índices de sección automáticos y una capa CSS limpia y personalizada.
- **Publicación basada en el repositorio.** El sitio se regenera a partir del
  repositorio en cada push a `main` mediante
  `.github/workflows/pages.yml`. Nada en el sitio publicado se edita a mano.
- **Agente IA (OpenCode API).** `.github/workflows/wikicode-agent.yml`
  ejecuta el agente autónomo en el runner de CI. Generación de contenido mediante
  OpenCode API (`deepseek-v4-flash-free`), investigación web mediante APIs de
  Wikipedia y DuckDuckGo. No se necesitan claves API externas.
- **GitHub Pages.** Habilitado con el tipo de compilación del workflow y HTTPS
  forzado.
- **Secciones de contenido.**
  - `docs/` para artículos, guías y páginas de referencia.
  - `projects/` para proyectos autónomos y ejecutables.
  - `snippets/` para fragmentos de código específicos.
  - `blog/` para artículos extensos y anuncios.
  - `memory/` para el contexto a largo plazo del agente (misión, reglas,
    conocimiento, decisiones).
  - `tasks/` para el pipeline de trabajo.
  - `reports/` para informes de ejecución con marca de tiempo.
- **Metadatos de fecha.** Cada página muestra una tarjeta con su fecha de
  **creación** (del frontmatter) y su fecha de **última actualización** (del
  historial de git, mediante `mkdocs-git-revision-date-localized-plugin`).
- **Sistema de etiquetas.** Las páginas pueden declarar etiquetas en el
  frontmatter; el tema Material genera páginas de índice por etiqueta
  automáticamente.
- **Guías principales.**
  - [Glosario](glossary.md)
  - [Arquitectura](architecture.md)
  - [Registro de cambios](changelog.md) (esta página)
  - [Rutas de aprendizaje](../learning-paths.md)
- **Archivos raíz.** `README.md`, `LICENSE`, `AGENT.md`,
  `CONTRIBUTING.md`, `CHANGELOG.md`, `ARCHITECTURE.md`,
  `.gitignore`.
- **Decisiones iniciales.** Cuatro entradas numeradas en
  `memory/decisions.md` (0001–0004).
- **Tareas iniciales.** Cuatro elementos en cola en `tasks/queue.md`.

### Notas

- El sitio está en vivo en la URL proporcionada por GitHub Pages una vez que la
  primera ejecución de `pages.yml` se completa exitosamente.
- No se requieren claves API externas. El agente utiliza `GITHUB_TOKEN`
  (incorporado) para el acceso al repositorio y la OpenCode API para la
  generación de contenido.