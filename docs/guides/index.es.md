---
title: Guías
description: Guías de formato largo orientadas a temas.
created: 2026-06-03
tags:
  - meta
status: stable
---

# Guías

Guías de formato largo agrupadas por tema. Cada guía es un archivo Markdown real en `docs/guides/` (o una subcarpeta).

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Creado: 2026-06-03</span>
<span class="wikicode-meta-updated">Última actualización: auto (git)</span>
</div>

## Convenciones

- Una carpeta o archivo `.md` por guía.
- Nombre de carpeta: minúsculas, con guiones.
- El frontmatter debe incluir `title`, `description`, `created` y `tags`.
- Las etiquetas ayudan a los enlaces cruzados: prefiere reutilizar las etiquetas existentes de [Tags](../tags.md) en lugar de inventar nuevas.

## Etiquetas sugeridas

| Etiqueta        | Significado                                                  |
| --------------- | -------------------------------------------------------- |
| `meta`          | Páginas sobre el propio WikiCode.                             |
| `guide`         | Contenido de cómo hacer.                                          |
| `reference`     | Material de referencia (glosarios, listas).                  |
| `architecture`  | Cómo se construye y funciona el wiki.                  |
| `process`       | Flujo de trabajo, contribución, gobernanza.                     |
| `language-go`   | Contenido principalmente sobre Go.                              |
| `language-py`   | Contenido principalmente sobre Python.                          |
| `language-cpp`  | Contenido principalmente sobre C++.                             |
| `language-rs`   | Contenido principalmente sobre Rust.                            |
| `language-js`   | Contenido principalmente sobre JavaScript / TypeScript.        |
| `backend`       | Temas de ingeniería de backend.                             |
| `frontend`      | Temas de ingeniería de frontend.                            |
| `devops`        | Construcción, despliegue, observabilidad.                            |
| `security`      | Temas de seguridad.                                         |
| `data`          | Bases de datos, pipelines, analítica.                         |

Añade etiquetas al frontmatter de esta manera:

```yaml
---
title: My guide
tags:
  - guide
  - backend
---
```