---
title: Buscar en el wiki
description: Cómo buscar en WikiCode.
created: 2026-06-03
tags:
  - meta
  - reference
status: stable
---

# Buscar en el wiki

WikiCode es completamente buscable. El índice de búsqueda se construye en el momento del despliegue y se ejecuta completamente en el navegador, por lo que las consultas son instantáneas y ningún dato sale de tu máquina.

<div class="wikicode-meta" markdown>
<span class="wikicode-meta-created">Creado: 2026-06-03</span>
<span class="wikicode-meta-updated">Última actualización: auto (git)</span>
</div>

## Cómo buscar

<div class="grid cards" markdown>

- :material-magnify: __Barra de búsqueda__

    Haz clic en el icono de la lupa en la esquina superior derecha de cualquier página
    (o presiona ++slash++ en el teclado) para abrir el modal de búsqueda.

- :material-keyboard: __Atajo de teclado__

    - ++slash++ — enfoca la barra de búsqueda.
    - ++esc++ — cierra el modal de búsqueda.
    - ++arrow-up++ / ++arrow-down++ — muévete por los resultados.
    - ++enter++ — abre el resultado resaltado.

- :material-format-letter-case: __Consejos__

    - La búsqueda se basa en **subcadenas**. Escribir `mkdocs` encuentra cualquier
      página que contenga "mkdocs".
    - La búsqueda **no distingue entre mayúsculas y minúsculas** por defecto.
    - Las frases entre comillas coinciden con subcadenas exactas: `"open hands"`.
    - Varias palabras coinciden con páginas que contienen todas ellas.

</div>

## Qué se indexa

El índice de búsqueda cubre todas las páginas Markdown renderizadas en el sitio:

- Artículos, guías y páginas de referencia en `docs/`.
- Resúmenes de proyectos en `projects/`.
- Descripciones de fragmentos en `snippets/`.
- Páginas de herramientas en `docs/tools/`.
- Publicaciones del blog en `blog/`.
- El texto de los bloques de código (para que puedas buscar un nombre de función o una opción de CLI).

El índice se regenera en cada push a `main`, por lo que siempre está sincronizado con el contenido publicado.

## Por qué del lado del cliente

- **Privacidad.** No se envían consultas a un servicio remoto.
- **Velocidad.** Los resultados aparecen mientras escribes.
- **Costo.** No hay nada que alojar más allá del sitio estático.
- **Sin conexión.** Una vez que el sitio se ha cargado, el índice está en la caché del navegador y continúa funcionando sin red.

## Añadir un atajo de búsqueda personalizado

Si deseas un enlace profundo que abra el modal de búsqueda pre-rellenado, añade `?q=<query>` a la URL del sitio después de que la búsqueda haya sido enfocada una vez. El comportamiento exacto depende de la versión del tema Material; la forma recomendada es usar el atajo de teclado (++slash++) y escribir la consulta.