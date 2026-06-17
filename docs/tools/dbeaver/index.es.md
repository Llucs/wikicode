---
title: DBeaver - Herramienta Universal de Gestión de Bases de Datos
description: Una herramienta de gestión de bases de datos y cliente SQL gratuita, de código abierto y multiplataforma para desarrolladores, DBAs y analistas de datos.
created: 2026-06-17
tags:
  - database
  - sql
  - management
  - tools
  - open-source
status: draft
---

# DBeaver - Herramienta Universal de Gestión de Bases de Datos

## Resumen

DBeaver es una herramienta de gestión de bases de datos y cliente SQL **gratuita, de código abierto y multiplataforma**. Proporciona una interfaz gráfica rica para interactuar con cualquier base de datos que admita controladores JDBC u ODBC, convirtiéndola en una herramienta universal para desarrolladores, administradores de bases de datos y analistas de datos.

- **Licencia**: La Community Edition (CE) se publica bajo **Apache 2.0**; también están disponibles las ediciones comerciales Pro/Enterprise/Team.
- **Plataforma**: Windows, macOS, Linux (también disponible como aplicación portátil).
- **Arquitectura**: Construido sobre la plataforma Eclipse Rich Client Platform (RCP) con Java.
- **Historia**: Iniciado en 2010 por Serge Rielau, un experto en bases de datos anteriormente involucrado con Apache Derby y Oracle. El proyecto rápidamente ganó una adopción generalizada, lo que llevó a la formación de DBeaver Corp.

DBeaver es ideal para:
- **Desarrollo de aplicaciones** – Escribir, depurar y optimizar consultas SQL.
- **Administración de bases de datos** – Gestionar esquemas, usuarios, sesiones e índices.
- **Análisis de datos** – Ejecutar consultas analíticas y exportar resultados a varios formatos.
- **Ingeniería de datos** – Transferir datos entre diferentes bases de datos sin necesidad de scripts pesados.
- **Educación** – Aprender SQL y conceptos de bases de datos relacionales a través de una interfaz gráfica intuitiva.

## Funcionalidades clave

| Funcionalidad | Descripción |
|---------|-------------|
| **Amplio soporte de bases de datos** | Se conecta a más de 100 bases de datos listas para usar, incluyendo MySQL/MariaDB, PostgreSQL, Oracle, SQL Server, SQLite, DB2, Snowflake, Redshift, ClickHouse y muchas más. |
| **Editor SQL avanzado** | Resaltado de sintaxis, autocompletado, ejecución de consultas con múltiples pestañas de resultados, visualización del plan de ejecución (gráfico), formateo SQL y consultas parametrizadas. |
| **Navegador de datos / Hoja de cálculo** | Potente edición en línea, filtrado avanzado, ordenación y manejo de datos BLOB/CLOB directamente en una interfaz de cuadrícula. |
| **Diagramas ER** | Genera automáticamente diagramas de entidad-relación con ingeniería inversa (clic derecho en un esquema o tabla). |
| **Gestión de esquemas** | Explorador de objetos para navegar, crear y editar tablas, vistas, índices, procedimientos y funciones. |
| **Transferencia de datos** | Exportación/importación masiva entre bases de datos y formatos de archivo (CSV, JSON, XML, Excel, SQL, Markdown, HTML). |
| **Herramientas de administración** | Administrador de sesiones, programador de tareas (Pro), gestión de usuarios/roles y túneles SSH/SSL/Proxy integrados. |
| **Extensibilidad** | Arquitectura de complementos; complemento disponible para controladores adicionales, control de versiones (Git) y personalización de diagramas. |
| **Multiplataforma** | Funciona en Windows, macOS y Linux. |

## Instalación

DBeaver está disponible a través de múltiples canales. Elija el método que mejor se adapte a su entorno.

### Instalador oficial (todas las plataformas)

Descargue el instalador para su sistema operativo desde [dbeaver.io](https://dbeaver.io) (Community Edition) o [dbeaver.com](https://dbeaver.com) (Enterprise).

### Gestores de paquetes

**macOS (Homebrew)**
```bash
brew install --cask dbeaver-community
```

**Linux (Snap)**
```bash
sudo snap install dbeaver-ce
```

**Linux (APT / YUM – repositorios oficiales Debian/RPM)**
```bash
# Debian/Ubuntu
wget -O - https://dbeaver.io/debs/dbeaver.gpg.key | sudo apt-key add -
echo "deb https://dbeaver.io/debs/dbeaver-ce /" | sudo tee /etc/apt/sources.list.d/dbeaver.list
sudo apt update && sudo apt install dbeaver-ce

# RHEL/CentOS/Fedora
sudo rpm --import https://dbeaver.io/rpms/dbeaver.gpg.key
sudo yum install dbeaver-ce
```

**Windows (winget / Chocolatey)**
```powershell
# winget (Windows 10 / 11)
winget install DBeaver.DBeaverCE

# Chocolatey
choco install dbeaver
```

**Versión portátil para Windows**

Hay un ejecutable portátil disponible en el sitio web oficial, ideal para ejecutarlo desde una unidad USB sin instalación.

## Primeros pasos – Uso básico

### 1. Crear una conexión a la base de datos

1. Inicie DBeaver.
2. Haga clic en el botón **Nueva conexión a la base de datos** (icono de enchufe) en la barra de herramientas.
3. Seleccione su tipo de base de datos (por ejemplo, **PostgreSQL**).
4. Rellene los detalles de la conexión:
   - Host, Puerto, Nombre de la base de datos, Usuario, Contraseña.
5. Haga clic en **Probar conexión**. DBeaver le pedirá automáticamente que descargue el controlador JDBC necesario si aún no está en caché.
6. Haga clic en **Finalizar**. La conexión aparece en el panel **Navegador de bases de datos**.

![Ejemplo del asistente de conexión](https://dbeaver.com/docs/images/connection-wizard.png) <!-- URL de marcador de posición; la documentación real proporciona capturas de pantalla -->

### 2. Navegar y consultar datos

- En el **Navegador de bases de datos**, expanda una conexión para ver esquemas, tablas, vistas, etc.
- Haga clic derecho en una tabla y seleccione **Ver datos** para abrir una cuadrícula de datos.
- Para escribir SQL personalizado, presione `Ctrl + ]` (Windows/Linux) o `Cmd + ]` (macOS) para abrir un nuevo **Editor SQL**.

**Ejemplo de consulta SQL:**
```sql
-- Seleccionar usuarios con su último pedido
SELECT u.id, u.name, o.order_date
FROM users u
JOIN (
    SELECT user_id, MAX(order_date) AS order_date
    FROM orders
    GROUP BY user_id
) o ON u.id = o.user_id
ORDER BY o.order_date DESC;
```

- Ejecute la consulta con `Ctrl + Enter` (Win/Lin) o `Cmd + Enter` (macOS).
- Los resultados aparecen en la cuadrícula de resultados debajo del editor.

### 3. Editar y exportar datos

- Haga clic directamente en el valor de una celda en la cuadrícula de resultados para editarlo (requiere permiso de **Edición** en la tabla).
- Haga clic derecho en la cuadrícula de resultados y elija **Exportar datos**.
- Seleccione el formato deseado (CSV, Excel, JSON, INSERT SQL, XML, Markdown, etc.) y configure las opciones.

## Uso avanzado

### Diagramas de entidad-relación (ER)

DBeaver puede generar diagramas ER para un esquema o tablas específicas.

1. Haga clic derecho en un esquema en el Navegador de bases de datos.
2. Seleccione **Ver diagrama** (o abra la pestaña **Diagrama ER**).
3. El diagrama muestra tablas, columnas, relaciones e índices.
4. Puede reorganizar elementos, exportar el diagrama como imagen o imprimirlo.

### Transferencia de datos / Migración

Utilice el asistente **Transferir datos** para copiar datos entre bases de datos o extraerlos a archivos.

1. Haga clic derecho en una tabla o esquema.
2. Seleccione **Datos > Transferir datos**.
3. Elija el origen (por ejemplo, una tabla) y el destino (otra conexión de base de datos o archivo).
4. Configure las asignaciones de columnas y las reglas de transformación.
5. Ejecute la transferencia.

### Plan de ejecución (EXPLAIN)

Visualice el plan de ejecución de la consulta para la optimización de SQL.

1. En el Editor SQL, escriba una consulta.
2. Haga clic en el botón **Explicar plan** (o clic derecho → **Explicar plan**).
3. DBeaver muestra un plan gráfico con detalles de costo y uso de índices.

### Herramienta de comparación (Pro/Enterprise)

Las herramientas **Comparar estructura** y **Comparar datos** le permiten diferenciar esquemas o datos entre dos bases de datos o entornos.

- Disponible en ediciones comerciales.

## Configuración y personalización

### Ajustes de conexión

- **Propiedades del controlador**: Modifique los atributos del controlador JDBC (por ejemplo, tiempos de espera, modo SSL, tamaños de fragmento) desde el editor de conexión.
- **Túnel SSH**: Configure túneles SSH para acceso seguro a bases de datos remotas (en la pestaña **SSH** de los ajustes de conexión).
- **SSL**: Habilite SSL e importe certificados a través de la pestaña **SSL**.

### Preferencias globales

- `Ventana → Preferencias` (Windows/Linux) o `DBeaver → Preferencias` (macOS).
- **Apariencia**: Cambie entre temas claro/oscuro, ajuste los tamaños de fuente.
- **Editores**: Configure el estilo de formateo SQL, el comportamiento de autocompletado y las opciones de ejecución.
- **Conexiones**: Establezca niveles de aislamiento de transacciones predeterminados, confirmación automática y tiempos de espera de inactividad.

### Gestión de controladores

- **Administrador de controladores**: `Base de datos → Administrador de controladores`. Ver, editar o agregar controladores JDBC personalizados.
- Descargue los controladores faltantes directamente desde el repositorio de controladores de DBeaver al conectarse por primera vez a una base de datos.

## Automatización y scripting

### DBeaver CLI (solo Pro/Enterprise)

DBeaver Pro/Enterprise incluye una herramienta de línea de comandos (`dbeaver-cli`) para ejecutar scripts SQL, exportar datos o ejecutar tareas sin una interfaz gráfica.

```bash
# Conectar y ejecutar un script contra una instancia de PostgreSQL
dbeaver-cli -driver postgresql -url jdbc:postgresql://localhost:5432/mydb \
            -user myuser -password mypass -script query.sql
```

### Programador de tareas (Pro/Enterprise)

Programe exportaciones recurrentes, transferencias de datos o scripts SQL utilizando el programador integrado (interfaz tipo cron).

## Integraciones

- **Control de versiones**: Complemento de integración con Git (disponible en Community) – confirme scripts SQL o compárelos con versiones confirmadas.
- **Docker**: Es posible ejecutar DBeaver directamente en un contenedor para pipelines CI/CD con la edición CLI.
- **Bases de datos en la nube**: Controladores preconfigurados para Snowflake, Amazon Redshift, Google BigQuery, Azure SQL, etc.
- **SSH/SSL**: Soporte integrado para conexiones seguras y autenticación proxy.

## Compatibilidad y rendimiento

| Aspecto | Detalles |
|--------|---------|
| **Sistemas operativos compatibles** | Windows 10+, macOS 10.15+, Linux (x64, amd64, aarch64) |
| **Requisitos de Java** | JDK 11 o posterior (incluido con los instaladores) |
| **Soporte de bases de datos** | Más de 100 bases de datos a través de JDBC/ODBC (incluyendo relacionales, tipo NoSQL, en la nube) |
| **Consejos de rendimiento** | - Use índices para consultas grandes.<br>- Cierre conexiones inactivas en preferencias.<br>- Active **“Usar actualizaciones por lotes”** para operaciones masivas.<br>- Para conjuntos de datos extremadamente grandes, exporte en fragmentos o use herramientas de migración dedicadas. |

## Solución de problemas y preguntas frecuentes

### Problemas comunes

1. **“Controlador no encontrado” / “No se puede conectar”**
   - DBeaver le pedirá que descargue el controlador. Si la descarga automática falla, vaya a `Base de datos → Administrador de controladores`, seleccione su base de datos y haga clic en **Descargar/Actualizar**.
   - Asegúrese de tener acceso a Internet o coloque manualmente el archivo JAR en la biblioteca del controlador.

2. **La conexión se cuelga o agota el tiempo**
   - Verifique la conectividad de red y las reglas del firewall.
   - Revise la configuración de SSH/SSL; un túnel mal configurado puede bloquear las conexiones.
   - Aumente el tiempo de espera de conexión en las propiedades del controlador.

3. **El Editor SQL funciona lento**
   - Desactive la carga de metadatos automática: `Preferencias → Base de datos → Navegador → Deshabilitar la lectura diferida de metadatos`.
   - Reduzca el límite del conjunto de resultados en la barra de herramientas del editor.

4. **No se puede editar BLOB/CLOB**
   - DBeaver admite la edición en línea para objetos pequeños. Para objetos grandes, use el diálogo **Ver / Editar valor** (clic derecho en la celda → **Ver valor**).

### Preguntas frecuentes

**P: ¿DBeaver es completamente gratuito?**
R: La Community Edition es gratuita y de código abierto (Apache 2.0). Las ediciones Pro, Enterprise y Team son comerciales y añaden funcionalidades como soporte para NoSQL, asistencia AI y CLI.

**P: ¿Puedo usar DBeaver para bases de datos en producción?**
R: Sí, la Community Edition está lista para producción para tareas de desarrollo y administración de bases de datos. Para entornos críticos, considere la edición Enterprise con soporte y auditoría adicionales.

**P: ¿DBeaver funciona con MongoDB u otras bases de datos NoSQL?**
R: La Community Edition tiene soporte básico para MongoDB. El soporte completo para NoSQL y bases de datos en la nube (incluyendo MongoDB, Cassandra y DynamoDB) está disponible en la edición Enterprise.

**P: ¿Cómo desinstalo DBeaver por completo?**
R: Use el gestor de paquetes de su sistema (por ejemplo, `brew uninstall --cask dbeaver-community`, `snap remove dbeaver-ce`) o el desinstalador del sistema operativo. Los ajustes de usuario se almacenan en `~/.dbeaver` en macOS/Linux o `%APPDATA%\DBeaver` en Windows; elimine esos directorios para borrar toda la configuración.

## Conclusión

DBeaver es una herramienta de bases de datos potente, flexible y fácil de usar que se integra perfectamente en el flujo de trabajo de cualquier desarrollador. Su núcleo de código abierto, su amplio soporte de bases de datos y su rico conjunto de funcionalidades lo convierten en una utilidad esencial para cualquier persona que trabaje con datos.

Para más información, visite la documentación oficial en [dbeaver.com/docs](https://dbeaver.com/docs/) o contribuya a la comunidad en [GitHub](https://github.com/dbeaver/dbeaver).