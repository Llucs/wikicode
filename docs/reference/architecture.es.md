---
title: Arquitectura
description: Cómo se construye WikiCode y cómo se mantiene actualizado.
created: 2026-06-03
tags:
  - reference
  - architecture
  - meta
status: stable
---

# Arquitectura

Cómo se construye WikiCode, cómo se mantiene actualizado y cómo los
agentes autónomos encajan en el bucle.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Creado: 2026-06-03</span>
<span class="wikicode-meta-updated">Última actualización: auto (git)</span>
</div>

## Diagrama de alto nivel

```
┌──────────────────────────────────────────────────────────────┐
│                       Repository                             │
│                                                              │
│   docs/        projects/    snippets/                        │
│   memory/      tasks/       reports/                         │
│   blog/        scripts/     mkdocs.yml                       │
│                                                              │
└─────────────┬──────────────────────────────┬────────────────┘
              │                              │
              │  push to main                │  Agent run
              │                              │  (manual, schedule,
              │                              │   @agent, label)
              ▼                              ▼
      ┌──────────────────┐         ┌──────────────────────┐
      │  pages.yml       │         │  wikicode-agent.yml  │
      │  ─ mkdocs build  │         │  ─ install deps      │
      │  ─ upload Pages  │         │  ─ read context      │
      │    artifact      │         │  ─ web research*     │
      └────────┬─────────┘         │  ─ generate content  │
               │                  │  ─ validate build    │
               │                  │  ─ commit & push     │
               │                  └──────────┬───────────┘
               │                             │
               ▼                             │
       GitHub Pages                          │
       (public site)                         │
                                             │
       new commit on main  ◄─────────────────┘
```

`*` El agente utiliza las APIs de Wikipedia y DuckDuckGo para la investigación web,
no se requieren claves API.

## Capas

### 1. Contenido

Markdown plano. La redacción no requiere herramientas especiales.

| Ruta               | Propósito                                                         |
| ------------------ | ----------------------------------------------------------------- |
| `docs/`            | Artículos, guías, referencia, las cosas que lees en el sitio.     |
| `docs/concepts/`   | Patrones de arquitectura, principios de diseño, conceptos técnicos.|
| `docs/guides/`     | Guías temáticas extensas.                                         |
| `docs/tools/`      | Una carpeta por herramienta de desarrollo documentada.            |
| `docs/analyses/`   | Análisis técnicos y estudios arquitectónicos de plataformas/bibliotecas. |
| `docs/reference/`  | Glosario, arquitectura, registro de cambios.                      |
| `docs/topics/`     | Índice de temas.                                                  |
| `projects/`        | Proyectos reales y ejecutables. Cada uno es una unidad autocontenida. |
| `snippets/`        | Fragmentos de código pequeños, enfocados y ejecutables.           |
| `blog/`            | Artículos extensos, anuncios, análisis post-mortem.               |
| `memory/`          | Contexto a largo plazo para agentes (misión, reglas, decisiones). |
| `tasks/`           | Pipeline de trabajo (cola + completados).                         |
| `reports/`         | Informes de ejecución con marca de tiempo, organizados por año/mes. |

### 2. Generación

- **MkDocs** con el tema **Material** convierte el árbol Markdown
  en un sitio estático.
- Plugins:
  - `search` — búsqueda de texto completo en el cliente.
  - `awesome-pages` — índices de sección automáticos.
  - `git-revision-date-localized` — fecha de última actualización desde git.
  - `blog` — soporte de blog integrado de Material.
  - `git-committers` — opcional, controlado por variable de entorno.

### 3. Despliegue

- `pages.yml` se ejecuta en cada push a `main`. Construye el sitio y
  lo despliega en **GitHub Pages** usando las acciones oficiales de Pages
  (`actions/upload-pages-artifact` + `actions/deploy-pages`).
- Pages está configurado con `build_type: workflow` y HTTPS
  forzado.

### 4. Automatización

#### Crecimiento diario

`wikicode-agent.yml` se ejecuta en un **programa dos veces al día** (`0 6,18 * * *`,
06:00 y 18:00 UTC) y con disparadores manuales. Cada ejecución es un solo
cambio con alcance limitado para que la wiki crezca un poco cada día.

El bucle esperado por ejecución:

1. El flujo de trabajo comienza. Se instalan las dependencias de Python.
2. `scripts/agent.py` lee `memory/` para obtener contexto. Si la cola de tareas
   está vacía, descubre proactivamente nuevas herramientas y proyectos para
   documentar. Luego investiga el tema elegido a través de las APIs de Wikipedia +
   DuckDuckGo.
3. La API de OpenCode genera el contenido (Markdown con frontmatter).
4. El agente escribe los archivos, ejecuta `mkdocs build --clean` para
   validar, luego hace commit y push.
5. `pages.yml` reconstruye y despliega el sitio.
6. La siguiente ejecución ve una wiki ligeramente más grande y continúa.

#### Disparadores

| Disparador              | Caso de uso                                             |
| ----------------------- | ------------------------------------------------------- |
| `schedule`              | La ejecución de crecimiento predeterminada (06:00 y 18:00 UTC). |
| `workflow_dispatch`     | Ejecución manual desde la pestaña Actions.              |
| `issue_comment`         | Mención `@agent` en un issue o comentario de PR.        |
| `issues` con etiqueta   | Issues etiquetados con `agent`.                          |

#### Concurrencia

`concurrency: wikicode-agent` está configurado con `cancel-in-progress: true`
para que las ejecuciones superpuestas no escriban dos veces en el repositorio.

### 5. Prevención de duplicados

WikiCode no quiere documentar lo mismo dos veces. El
mecanismo de deduplicación tiene tres partes:

1. **Páginas de índice de sección.** Cada sección tiene un `index.md` que
   enumera su contenido actual. El plugin `awesome-pages`
   descubre automáticamente la lista desde el sistema de archivos, por lo que siempre es
   precisa.
2. **Respaldo de `git grep`.** El script del agente escanea los índices de sección
   y la lista de tareas, luego usa `git grep` para confirmar que un tema es
   nuevo antes de generar contenido.
3. **Registro de conocimiento.** `memory/knowledge.md` enumera las piezas principales
   de contenido y las reglas para agregar nuevas.

Si se detecta un duplicado, el agente debe mejorar la
página existente en lugar de escribir una nueva (regla 16 en `memory/rules.md`).

### 6. Investigación web

El agente usa las APIs de Wikipedia y DuckDuckGo para recopilar información
sobre cualquier tema que necesite documentar. Este es el mecanismo que
mantiene el contenido generado factual y actualizado:

1. `research_topic()` en `scripts/agent.py` ejecuta tanto una búsqueda en Wikipedia
   como una consulta de Respuesta Instantánea de DuckDuckGo para el tema.
2. Wikipedia devuelve títulos de artículos + extractos introductorios (texto
   sin formato, hasta 2000 caracteres).
3. DuckDuckGo devuelve el resumen y temas relacionados.
4. Si ambos devuelven vacío, el agente recurre al conocimiento de entrenamiento del LLM.
5. El texto de investigación recopilado se inyecta en el prompt de generación
   de contenido para que el LLM escriba a partir de información del mundo real.

## Taxonomía de contenido v2

Cada documento en WikiCode pertenece exactamente a una de estas categorías:

| Categoría    | Ruta                   | Qué contiene                                         |
| ------------ | ---------------------- | ---------------------------------------------------- |
| **Concepto** | `docs/concepts/<slug>/` | Patrón de arquitectura, principio de diseño o concepto técnico. |
| **Herramienta**| `docs/tools/<slug>/`  | Documentación de herramienta de desarrollo (instalación, uso, características). |
| **Análisis** | `docs/analyses/<slug>/` | Estudio arquitectónico de una plataforma, framework o biblioteca. |
| **Proyecto** | `projects/<slug>/`     | Proyecto real y ejecutable de código abierto con guía de configuración. |
| **Guía**     | `docs/guides/`         | Tutorial o procedimiento extenso y orientado a temas. |
| **Informe**  | `reports/YYYY/MM/`     | Registro de ejecución con marca de tiempo, inmutable después del commit. |
| **Memoria**  | `memory/`              | Contexto del agente: misión, reglas, decisiones, conocimiento, estado, calidad. |

La separación es semántica, no cosmética:

- **Conceptos vs Guías** — una página de concepto explica un patrón,
  principio o técnica (ej., microservicios, CQRS, OAuth).
  Una guía es un recorrido narrativo que puede abarcar múltiples
  conceptos o herramientas.
- **Herramientas vs Análisis** — una página de herramienta enseña *cómo usar* algo
  (instalar → configurar → ejecutar). Un análisis estudia *arquitectura y
  compensaciones* (comparar alternativas, evaluar decisiones de diseño).
- **Guías vs Herramientas** — una guía es un recorrido narrativo a través de
  múltiples herramientas o conceptos. Una página de herramienta es una ficha de referencia única.
- **Informes como registros** — los informes son inmutables después del commit. Están
  organizados por `YYYY/MM/` para evitar la hinchazón de directorios planos y
  permitir la navegación cronológica.
- **Memoria como contrato del agente** — cada archivo en `memory/` tiene un rol
  distinto (declarado en `memory/knowledge.md`). El agente los lee todos
  al inicio; `state.md` también se escribe después de cada ejecución.

## Contrato de frontmatter

Cada página del sitio debe tener:

```yaml
---
title: Human-readable title
description: One-sentence summary.
created: YYYY-MM-DD
tags: [tag1, tag2]
status: draft | stable | archived | deprecated
---
```

`title` y `description` se usan en la navegación y la búsqueda.
`created` alimenta la tarjeta de metadatos; `git-revision-date-localized`
rellena la fecha de "última actualización" automáticamente. `tags` permite la
navegación basada en etiquetas. `status` indica la madurez de la página.

## Secretos y seguridad

| Secreto              | Propósito                                            | Origen                |
| -------------------- | ---------------------------------------------------- | --------------------- |
| `GITHUB_TOKEN`       | Acceso al repositorio en los flujos de trabajo.      | Integrado.            |

No se almacenan credenciales en el repositorio.

## Cómo evolucionar la arquitectura

Cualquier cambio que afecte cómo se construye, despliega o
automatiza el sitio debe:

1. Registrarse como una nueva entrada en `memory/decisions.md` con el siguiente
   número disponible.
2. Reflejarse en esta página si cambia el diagrama de alto nivel.
3. Mantener el contrato de "repositorio primero": nunca editar el sitio publicado
   directamente.