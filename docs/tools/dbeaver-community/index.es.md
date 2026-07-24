---
title: DBeaver Community
description: Una herramienta gratuita y de código abierto para la gestión de bases de datos recomendada para proyectos personales. Gestione y explore bases de datos SQL como MySQL, MariaDB, PostgreSQL, SQLite, Apache Family, y más.
created: 2026-07-24
tags:
  - base de datos
  - sql
  - gestión
  - desarrollo
  - herramienta
status: borrador
---

# DBeaver Community

DBeaver es una herramienta de código abierto para la gestión universal de bases de datos que soporta múltiples bases de datos, incluyendo SQL Server, MySQL, PostgreSQL, Oracle, SQLite, y más. Se lanzó por primera vez en 2013 y desde entonces se ha convertido en una elección popular entre desarrolladores, DBAs y analistas de datos para la gestión, desarrollo y administración de bases de datos.

## Características Clave

1. **Gestión de Bases de Datos**: DBeaver soporta una amplia gama de bases de datos y sus respectivas herramientas, como editores de consultas SQL, exploradores de bases de datos, editores de esquemas y historial de consultas SQL.
2. **Modelado y Diseño de Datos**: DBeaver permite a los usuarios diseñar, gestionar y modificar esquemas de bases de datos mediante una interfaz gráfica de usuario.
3. **Conectividad de Bases de Datos**: Puede conectarse a diversas bases de datos utilizando diferentes protocolos y controladores.
4. **Editor de SQL**: El editor de SQL incluye resaltado de sintaxis, completado de código y un asistente de auto-completado.
5. **Exportación e Importación de Datos**: DBeaver proporciona herramientas para exportar datos a CSV, Excel y otros formatos, así como para importar datos de estos formatos.
6. **Sincronización de Bases de Datos**: Soporta la sincronización y comparación de esquemas de bases de datos.
7. **Administración de Bases de Datos**: DBeaver incluye características para administrar usuarios, roles, permisos y otras tareas de administración.
8. **Interfaz Gráfica de Usuario**: La aplicación tiene una interfaz moderna e intuitiva que soporta temas oscuros y claros.
9. **Plugins y Extenciones**: Los usuarios pueden extender la funcionalidad de DBeaver a través de plugins, que pueden instalarse desde la Tienda de DBeaver.

## Historia

DBeaver fue desarrollado inicialmente por Yvan Volckaert y se lanzó como un proyecto comunitario en 2013. El proyecto fue adoptado y mantenido posteriormente por la Comunidad de DBeaver. En 2017, el proyecto se transformó en una empresa comercial, DBeaver GmbH, que continúa apoyando y desarrollando el software.

## Casos de Uso

1. **Desarrollo de Base de Datos**: Los desarrolladores pueden usar DBeaver para escribir, probar y ejecutar consultas SQL, así como gestionar esquemas de bases de datos.
2. **Análisis de Datos**: Los analistas de datos pueden usar DBeaver para consultar y manipular grandes conjuntos de datos, crear y ejecutar consultas SQL complejas y generar informes.
3. **Administración de Base de Datos**: Los DBAs pueden usar DBeaver para gestionar permisos de usuarios, roles y otras tareas administrativas.
4. **Migración de Datos**: Los usuarios pueden usar DBeaver para migrar datos entre diferentes bases de datos, especialmente cuando la base de datos objetivo tiene una estructura diferente.

## Instalación

1. **Descarga**: Visite el sitio web oficial de DBeaver (https://dbeaver.io/) para descargar la última versión de DBeaver.
2. **Instalación**: El proceso de instalación es sencillo. Para Windows, doble-clique el instalador e intente las instrucciones en pantalla. Para macOS, abra el archivo `.dmg` y arrastre la aplicación al folder Applications. Para Linux, ejecute el archivo `.deb` o `.rpm` con el gestor de paquetes.
3. **Ejecución**: Después de la instalación, abra DBeaver desde su menu de aplicaciones.

### Ejemplo de Comando para Instalador de Windows

```sh
sh DBeaver-<version>-win32-installer.exe
```

### Ejemplo de Comando para Instalador de macOS

```sh
open DBeaver-<version>-macOS.dmg
```

### Ejemplo de Comando para Instalador de Linux

```sh
sudo dpkg -i DBeaver-<version>.deb
```

o

```sh
sudo rpm -i DBeaver-<version>.rpm
```

## Uso Básico

1. **Gestión de Conexiones**: Abra DBeaver, haga clic en "Archivo" > "Nuevo" > "Nueva Conexión de Base de Datos" y configure los detalles de la conexión (servidor, puerto, usuario, contraseña).
2. **Editor de SQL**: Una vez conectado, use el editor de SQL para escribir, ejecutar y gestionar consultas SQL.
3. **Explorador de Esquemas**: Use el explorador de esquemas para explorar la estructura de la base de datos, navegar tablas, vistas y otros objetos de la base de datos.
4. **Importación y Exportación de Datos**: Utilice las funciones de importación y exportación para mover datos entre diferentes formatos o bases de datos.

## Interfaz de Línea de Comandos (dbvr)

DBeaver CLI (dbvr) es una interfaz de línea de comandos para trabajar con bases de datos. Puede actuar como una aplicación CLI independiente o junto con DBeaver y CloudBeaver. Proporciona un modo scriptable para administrar proyectos y fuentes de datos de base de datos, inspeccionar metadatos y ejecutar SQL desde la terminal.

### Ejemplo de Comando para Conectarse a una Base de Datos

```sh
dbvr connect --url jdbc:mysql://localhost:3306/mydb --username myuser --password mypassword
```

### Ejemplo de Comando para Ejecutar una Consulta SQL

```sh
dbvr sql -c "SELECT * FROM mytable" -o results.csv
```

## Conclusión

DBeaver es una herramienta potente y versátil que ofrece una amplia gama de características para la gestión y desarrollo de bases de datos. Su naturaleza de código abierto y la comunidad activa contribuyen a su robustez y actualizaciones frecuentes, convirtiéndolo en una valiosa herramienta para profesionales de bases de datos.