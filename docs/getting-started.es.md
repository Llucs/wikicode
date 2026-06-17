---
title: Primeros pasos
description: Diseño del repositorio, compilación local y convenciones de contribución.
created: 2026-06-03
---

# Primeros pasos

Todo lo que necesitas para leer, compilar y contribuir a WikiCode.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Creado: 2026-06-03</span>
<span class="wikicode-meta-updated">Última actualización: auto (git)</span>
</div>

## 1. Diseño del repositorio

```
.
├── README.md            # Project overview
├── LICENSE              # MIT License
├── AGENT.md             # Operating contract for agents
├── mkdocs.yml           # Static site configuration
├── .gitignore
├── .github/
│   └── workflows/
│       ├── pages.yml    # Builds and deploys the site on push to main
│       └── wikicode-agent.yml# Autonomous agent workflow
├── docs/                # Site content (articles, guides)
│   ├── assets/css/      # Custom styling
│   ├── index.md
│   └── getting-started.md
├── projects/            # Self-contained developer projects
├── snippets/            # Reusable code snippets
├── memory/              # Long-term agent memory
│   ├── mission.md
│   ├── rules.md
│   ├── knowledge.md
│   └── decisions.md
├── tasks/               # Work pipeline
│   ├── queue.md
│   └── completed.md
└── reports/             # Time-stamped execution reports
```

## 2. El bucle "la wiki crece desde el repositorio"

WikiCode es un sitio **basado en el repositorio** (repository-first). Nada en `site/` (la salida publicada) se edita manualmente.

1. Se realiza un cambio en el repositorio (un nuevo artículo, proyecto, fragmento, informe, decisión, etc.).
2. El cambio se confirma y se envía a `main`.
3. `.github/workflows/pages.yml` se ejecuta automáticamente con el push.
4. MkDocs lee `docs/`, `projects/`, `snippets/` y reconstruye todo el sitio.
5. GitHub Pages sirve la nueva compilación.

El agente de IA local (o cualquier colaborador) se conecta a este bucle escribiendo en el repositorio. El sitio luego recoge el cambio sin intervención manual.

## 3. Ejecutar el sitio localmente

Necesitas Python 3.10+.

```bash
pip install mkdocs mkdocs-material \
            mkdocs-awesome-pages-plugin \
            mkdocs-git-revision-date-localized-plugin
mkdocs serve
```

El sitio estará disponible en `http://127.0.0.1:8000`. Las ediciones en cualquier archivo Markdown en `docs/`, `projects/` o `snippets/` provocan una recarga instantánea.

## 4. Compilar el sitio estático

```bash
mkdocs build --clean
```

La salida se escribe en `site/`. El CI utiliza el mismo comando.

## 5. Añadir contenido

| Quieres añadir… | Ponlo en…                              | Archivos requeridos                  |
| --------------- | --------------------------------------- | ------------------------------------ |
| Un artículo     | `docs/<topic>/<slug>.md` o `docs/`      | el propio archivo `.md`              |
| Un proyecto     | `projects/<slug>/`                      | `README.md` + `index.md` + source    |
| Un fragmento    | `snippets/<slug>/`                      | el archivo de código + `index.md`    |
| Una decisión    | `memory/decisions.md`                   | añadir una nueva entrada             |
| Una tarea       | `tasks/queue.md`                        | añadir una nueva entrada de casilla  |
| Un informe      | `reports/YYYY-MM-DD-<slug>.md`          | el archivo + actualización del índice|

Las secciones que no son parte de `docs/` (projects, snippets) son recogidas automáticamente por el complemento `awesome-pages` de MkDocs a través de sus archivos `index.md`.

## 6. Frontmatter

Cada página del sitio tiene al menos:

```yaml
---
title: Page title
description: Short description.
created: YYYY-MM-DD
---
```

La fecha de `created` se establece cuando la página se añade por primera vez. La fecha de **última actualización** se toma automáticamente del historial de git del archivo, por lo que siempre es precisa sin ediciones manuales.

## 7. Trabajar de forma autónoma

Los agentes deben seguir `AGENT.md`. La versión corta:

1. Lee `memory/mission.md` y `memory/rules.md`.
2. Elige la siguiente tarea de `tasks/queue.md`.
3. Realiza exactamente un cambio significativo en el repositorio.
4. Escribe un informe en `reports/`.
5. Mueve la tarea a `tasks/completed.md`.
6. Confirma y envía (commit and push). El sitio se reconstruirá automáticamente.

## 8. Búsqueda

WikiCode es completamente buscable. El índice de búsqueda se construye durante el despliegue y se ejecuta completamente en el navegador.

- Presiona ++slash++ en cualquier página para enfocar la barra de búsqueda.
- El índice cubre cada página del sitio, incluyendo bloques de código y publicaciones del blog.
- Consulta [Búsqueda](search.md) para obtener detalles completos y consejos.

## 9. Cómo se activa el agente

El flujo de trabajo wikicode-agent admite **activación tanto automática como manual**:

| Activación          | Cuándo                                          | Caso de uso                              |
| ------------------- | ----------------------------------------------- | ---------------------------------------- |
| `schedule`          | Diariamente a las 12:00 UTC.                    | Ejecución predeterminada "crecer un poco cada día". |
| `workflow_dispatch` | Manualmente desde la pestaña Actions.           | Ejecución a demanda, útil para desbloquear. |
| `issue_comment`     | Cuando alguien escribe `@agent` en un issue.    | Convierte un issue en una contribución.  |
| `issues` con label  | Cuando un issue es etiquetado como `agent`.     | Ejecuciones por lotes curadas por el operador.|

Solo se ejecuta **una** tarea por ejecución. La IA utiliza la API de OpenCode para la generación de contenido — no se necesitan claves de API externas.

## 10. Convenciones

- Nombres de archivos Markdown: minúsculas, con guiones.
- Cada carpeta de proyecto, fragmento y herramienta expone un `index.md` para navegación.
- Las decisiones sobre arquitectura, herramientas o flujo de trabajo se registran en `memory/decisions.md`.
- Nunca se confirman credenciales, tokens o datos privados.
- El agente de IA local utiliza `secrets.GITHUB_TOKEN` (integrado) para confirmar y enviar. No se requieren claves de API externas.