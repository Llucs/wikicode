---
title: DBGate
description: DBGate es una herramienta de gestión de bases de datos de código abierto, multiplataforma y basada en web para MySQL, PostgreSQL, SQL Server, MongoDB, SQLite y más, que ofrece una interfaz moderna para la administración y el desarrollo de bases de datos.
created: 2026-06-20
tags:
  - database
  - open-source
  - web-based
  - tool
  - management
status: draft
---

# DBGate

DBGate es una herramienta de gestión de bases de datos de código abierto (MIT) y basada en web, diseñada como una alternativa moderna a herramientas clásicas como phpMyAdmin, Adminer, DBeaver o DataGrip. Construida con un backend Node.js/Express y un frontend React, proporciona una interfaz de usuario limpia y contemporánea que se ejecuta completamente en un navegador web, lo que la hace multiplataforma e ideal para entornos en la nube, servidores y contenedores.

## ¿Por qué DBGate?

Los clientes de bases de datos tradicionales a menudo requieren instalación en el sistema operativo, lo que genera fragmentación entre equipos y entornos. DBGate resuelve esto al ser completamente basado en navegador, permitiéndote:

- **Gestionar bases de datos de forma remota** sin necesidad de túneles SSH ni clientes nativos.
- **Integrarse en stacks de Docker** para acceso instantáneo a bases de datos de desarrollo.
- **Compartir conexiones y scripts** a través de una instancia centralizada (con autenticación).
- **Trabajar sin problemas en Windows, macOS y Linux** usando la misma interfaz web.

## Características principales

| Característica               | Descripción                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| Soporte para múltiples bases de datos | Conéctate simultáneamente a MySQL, MariaDB, PostgreSQL, SQL Server, MongoDB, SQLite, CockroachDB, Amazon Redshift y Redis. |
| Editor SQL avanzado          | Resaltado de sintaxis, autocompletado inteligente, consultas con pestañas múltiples e historial completo de consultas. |
| Explorador de esquemas/datos | Explora, crea, modifica y elimina objetos de base de datos. Edición directa de datos con potentes opciones de ordenamiento y filtrado. |
| Diagramas ER                 | Genera automáticamente diagramas de Entidad-Relación para visualizar esquemas de bases de datos. |
| Exportación/Importación      | Exporta a CSV, JSON, SQL, Markdown, Excel; importa desde archivos CSV y SQL. |
| Navegación por claves foráneas | Profundiza directamente en registros relacionados desde el explorador de datos. |
| Monitorización del servidor  | Ver procesos activos, estado del servidor y configuraciones de variables.   |
| Optimizado para Docker       | Imagen oficial de Docker para una implementación sencilla en cualquier servidor. |
| Aplicación de escritorio     | Versión empaquetada de Electron para uso independiente en Windows, macOS y Linux. |

## Instalación

DBGate se puede instalar y ejecutar de varias maneras:

### 1. Docker (Recomendado para servidor)

```bash
docker run -d -p 3000:3000 --name dbgate dbgate/dbgate
```

Luego accede a `http://localhost:3000`.

Para una configuración con `docker-compose.yml`:

```yaml
version: '3'
services:
  dbgate:
    image: dbgate/dbgate
    ports:
      - "3000:3000"
    restart: unless-stopped
```

### 2. Node Package Manager (NPM)

```bash
npm install -g dbgate
dbgate
```

Accede mediante `http://localhost:3000`.

### 3. Instalador de escritorio

Descarga los instaladores precompilados para Windows, macOS y Linux desde la [página de lanzamientos de GitHub](https://github.com/dbgate/dbgate/releases).

### 4. Despliegues en la nube

Opciones de despliegue con un solo clic están disponibles para Heroku, Railway y plataformas similares.

## Inicio rápido / Uso

### 1. Inicia DBGate

Navega a `http://localhost:3000` en tu navegador.

### 2. Agrega una conexión

Haz clic en el icono **+** junto a **Conexiones**. Elige tu motor de base de datos (por ejemplo, PostgreSQL) e ingresa las credenciales de conexión: Host, Puerto, Usuario, Contraseña, Base de datos.

### 3. Explora los datos

Haz clic en la conexión guardada para ver un árbol de bases de datos/tablas. Haz clic en una tabla para ver sus filas.

### 4. Consulta la base de datos

Haz clic en el botón **Consulta** para abrir el editor SQL. Escribe tu SQL y presiona **Ejecutar** (o `Ctrl+Enter`).

### 5. Visualiza el esquema

Haz clic derecho en una base de datos o tabla y selecciona **Diagrama ER** para generar un esquema visual.

### 6. Exporta datos

Haz clic derecho en una tabla o conjunto de resultados y selecciona **Exportar** para descargar datos en tu formato preferido (CSV, JSON, SQL, etc.).

## Ejemplos de comandos

**Iniciar DBGate con Docker y persistir datos:**

```bash
docker run -d \
  -p 3000:3000 \
  -v dbgate-data:/home/app/.dbgate \
  --name dbgate \
  dbgate/dbgate
```

**Usar con una instancia local de PostgreSQL en un stack de desarrollo:**

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: example
  dbgate:
    image: dbgate/dbgate
    ports:
      - "3000:3000"
    depends_on:
      - postgres
```

**Instalar y ejecutar usando npm:**

```bash
npm install -g dbgate
dbgate
```

**Conectar usando variables de entorno (avanzado):**

```bash
docker run -d \
  -e DBGATE_SERVER_NAME=myPostgres \
  -e DBGATE_SERVER_TYPE=postgres \
  -e DBGATE_SERVER_HOST=192.168.1.100 \
  -e DBGATE_SERVER_PORT=5432 \
  -e DBGATE_SERVER_USER=admin \
  -e DBGATE_SERVER_PASSWORD=secret \
  -p 3000:3000 \
  dbgate/dbgate
```

## Casos de uso

1. **Administración remota de servidores** – Gestiona bases de datos en un VPS o instancia en la nube sin túneles SSH ni instalación de clientes nativos.
2. **Entornos de desarrollo** – Incluye DBGate en un stack `docker-compose.yml` para dar a los desarrolladores acceso GUI instantáneo a sus bases de datos locales.
3. **Herramientas de equipo** – Despliega una instancia centralizada de DBGate (con autenticación adecuada) para que un equipo comparta acceso a bases de datos de desarrollo o staging.
4. **Educación y formación** – Proporciona rápidamente a los estudiantes una interfaz SQL sin gestionar instalaciones de clientes.
5. **Flujos de trabajo multiplataforma** – Cambia sin problemas entre sistemas operativos usando la misma interfaz web.

## Arquitectura

DBGate consiste en:

- **Backend:** Servidor Node.js/Express que maneja conexiones a bases de datos, ejecución de consultas y endpoints de API.
- **Frontend:** SPA basada en React que proporciona la interfaz de usuario, incluyendo el editor SQL, el explorador de datos y el visor de esquemas.
- **Controladores de base de datos:** Soporta múltiples motores de base de datos a través de controladores nativos de Node.js o puentes ODBC/JDBC.

La aplicación almacena conexiones, scripts SQL y otros objetos en el almacenamiento local (o almacenamiento en la nube opcional para la versión alojada). La imagen de Docker incluye todas las dependencias para un despliegue en un solo puerto.

## Limitaciones

- **Funciones avanzadas de IDE:** Puede carecer de algunas funciones presentes en IntelliJ DataGrip (por ejemplo, refactorización distribuida, análisis avanzado de código).
- **Rendimiento:** La representación de conjuntos de datos muy grandes (>100k filas) en el navegador puede ser más lenta que en las aplicaciones nativas. Las operaciones de exportación se manejan del lado del servidor para un mejor rendimiento.
- **Autenticación:** La versión de código abierto no incluye autenticación de usuario incorporada; debes anteponer un proxy inverso (como nginx + auth_basic) para uso en equipo.

## Resumen

DBGate es una herramienta de gestión de bases de datos potente, flexible y de código abierto que llena el vacío entre los clientes web ligeros (como phpMyAdmin) y los IDE nativos pesados (como DataGrip). Su naturaleza multiplataforma, su diseño amigable con contenedores y su creciente conjunto de funciones lo convierten en una excelente opción para desarrolladores, administradores de bases de datos (DBAs) y equipos que buscan un cliente de base de datos moderno y nativo de la web.

---

*Documento generado el 2026-06-20. Visita el [repositorio oficial](https://github.com/dbgate/dbgate) para las últimas actualizaciones.*