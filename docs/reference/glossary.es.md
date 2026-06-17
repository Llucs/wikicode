---
title: Glosario
description: Terminología utilizada en todo WikiCode.
created: 2026-06-03
tags:
  - reference
  - meta
status: stable
---

# Glosario

Terminología canónica utilizada en todo WikiCode. Las definiciones son breves
y enlazan a la fuente autorizada cuando es útil.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Creado: 2026-06-03</span>
<span class="wikicode-meta-updated">Última actualización: auto (git)</span>
</div>

## Conceptos centrales

<dl markdown>
<dt markdown>**WikiCode**</dt>
<dd markdown>El repositorio y el sitio estático que produce. "WikiCode"
se refiere a ambos, dependiendo del contexto.</dd>

<dt markdown>**Artículo**</dt>
<dd markdown>Una página Markdown de formato largo dentro de `docs/`. Los artículos
están destinados a leerse por completo.</dd>

<dt markdown>**Proyecto**</dt>
<dd markdown>Una pieza de software autónoma y ejecutable dentro de
`projects/`. Cada proyecto tiene su propio `README.md`, `index.md` y
árbol de código fuente.</dd>

<dt markdown>**Fragmento**</dt>
<dd markdown>Una unidad de código ejecutable, pequeña y enfocada, dentro de `snippets/`.
Los fragmentos están diseñados para ser copiados y adaptados.</dd>

<dt markdown>**Informe**</dt>
<dd markdown>Un archivo Markdown con marca de tiempo dentro de `reports/` que
describe una ejecución única. Formato:
`YYYY-MM-DD-<slug>.md`.</dd>

<dt markdown>**Decisión**</dt>
<dd markdown>Una elección arquitectónica u operativa registrada en
`memory/decisions.md` con un número de cuatro dígitos y un estado.</dd>

<dt markdown>**Agente**</dt>
<dd markdown>Cualquier proceso — humano o autónomo — que sigue
`AGENT.md` al trabajar en el repositorio.</dd>

<dt markdown>**Tarea**</dt>
<dd markdown>Una unidad de trabajo individual listada en `tasks/queue.md`. Una
tarea por ejecución.</dd>
</dl>

## Términos del flujo de trabajo

<dl markdown>
<dt markdown>**Push a `main`**</dt>
<dd markdown>Activa `pages.yml`, que reconstruye y despliega el
sitio. Cada cambio en el sitio publicado ocurre a través de este
mecanismo.</dd>

<dt markdown>**Ejecución del agente**</dt>
<dd markdown>Una ejecución desencadenada de `.github/workflows/wikicode-agent.yml`,
ya sea por `workflow_dispatch`, por una mención `@agent` en un
issue, o por un issue etiquetado como `agent`.</dd>

<dt markdown>**Frontmatter**</dt>
<dd markdown>Metadatos YAML al inicio de un archivo Markdown, delimitados
por `---`. WikiCode espera al menos `title`, `description` y
`created`.</dd>

<dt markdown>**Etiqueta**</dt>
<dd markdown>Una etiqueta declarada en frontmatter que agrupa páginas
relacionadas. Material renderiza las páginas de índice por etiqueta
automáticamente.</dd>
</dl>

## Valores de estado

Las páginas y los proyectos pueden declarar un `status` en su frontmatter:

| Estado      | Significado                                                         |
| ----------- | ------------------------------------------------------------------- |
| `draft`     | Trabajo en progreso; puede estar incompleto o ser incorrecto.       |
| `stable`    | Revisado y considerado correcto. Puede evolucionar.                 |
| `archived`  | Conservado como referencia; ya no se mantiene.                      |
| `deprecated`| Reemplazado por otra cosa; conservado por contexto histórico.       |

`status: stable` es la expectativa predeterminada para cualquier contenido
publicado.