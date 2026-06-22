---
title: PlanetScale: Plataforma de base de datos MySQL sin servidor
description: Una plataforma de base de datos totalmente gestionada compatible con MySQL construida sobre Vitess que introduce ramificación de bases de datos y cambios de esquema sin bloqueo para flujos de trabajo de desarrollo modernos.
created: 2026-06-22
tags:
  - database
  - mysql
  - vitess
  - serverless
  - schema-migration
  - devops
  - dbaas
  - branching
status: draft
---

# PlanetScale

## Introducción

PlanetScale, fundada en 2018 por los creadores principales de Vitess (Sugu Sougoumarane, Jiten Vaidya y Morgan Goeller), es la plataforma de base de datos compatible con MySQL construida sobre el sistema de agrupación de bases de datos de código abierto que impulsa YouTube. Reimagina la gestión de bases de datos aplicando **flujos de trabajo al estilo de Git**—ramificación de bases de datos y Deploy Requests—a esquemas y datos.

Este enfoque elimina los cuellos de botella tradicionales y el tiempo de inactividad asociado con las migraciones de esquema, haciendo que los cambios de base de datos sean tan seguros, revisables e iterativos como los cambios de código. PlanetScale es un servicio totalmente gestionado que maneja replicación, copias de seguridad, sharding y alta disponibilidad, mientras admite una capa de cómputo sin servidor que escala a cero y se activa instantáneamente al establecer una conexión.

## Conceptos Clave

### Ramificación de Bases de Datos
Así como `git branch` permite el desarrollo de código aislado, `pscale branch create` crea una copia aislada y completamente funcional de tu base de datos (incluyendo datos y esquema) en la infraestructura de PlanetScale.

- **Crear una rama desde cualquier punto:** Crea una rama desde `main` o una instantánea anterior.
- **Datos y esquema:** La rama contiene una instantánea completa, lo que permite pruebas altamente realistas.
- **Naturaleza efímera:** Las ramas están diseñadas para ser descartadas una vez que su propósito se cumple, evitando la deriva del esquema.

### Deploy Requests (DRs)
El equivalente de PlanetScale a un Pull Request. Cuando estás satisfecho con los cambios de esquema en una rama, abres un Deploy Request. Esto genera un diff, permite la revisión y realiza la fusión como una **migración de esquema en línea sin bloqueo** (utilizando Vitess VReplication).

### Cómputo Sin Servidor
PlanetScale desacopla el cómputo del almacenamiento. Las bases de datos tienen un estado de 'sueño' cuando no hay conexiones activas. Las conexiones activan la base de datos instantáneamente, eliminando los costos de cómputo inactivo.

## Primeros Pasos

### Instalación
La interfaz principal para desarrolladores es la CLI de `pscale`.

**macOS:**
```bash
brew install planetscale/tap/pscale
```

**Linux / Windows:**
```bash
curl -fsSL https://planetscale.com/install.sh | sh
```

### Autenticación
```bash
pscale auth login
```

### Creación de una Base de Datos
```bash
pscale database create my-app
```

### Trabajar con Ramas

**Crear una rama de funcionalidad (copia esquema y datos desde main):**
```bash
pscale branch create my-app feature-user-profile
```

**Conectar a la rama:**
```bash
pscale connect my-app feature-user-profile --port 3309
```
Esto ejecuta un proxy local. Tu aplicación se conecta a `127.0.0.1:3309`. El proxy maneja la autenticación automáticamente.

**Ejecutar migraciones de esquema en tu rama:**
Usa cualquier cliente MySQL, ORM o herramienta de migración (por ejemplo, `mysql2`, `Prisma`, `SQLAlchemy`).
```sql
ALTER TABLE users ADD COLUMN bio TEXT;
```

### El Flujo de Deploy Request
Una vez que hayas probado exhaustivamente los cambios de esquema en la rama:

```bash
# Create the Deploy Request
pscale deploy-request create my-app feature-user-profile

# List deploy requests
pscale deploy-request list my-app

# Deploy the request (after review)
pscale deploy-request deploy my-app <deploy-number>

# Clean up the branch
pscale branch delete my-app feature-user-profile --force
```

El despliegue aplica el cambio de esquema a `main` *sin bloquear la tabla ni causar tiempo de inactividad*.

## Características Clave en Detalle

### Cambios de Esquema Sin Bloqueo (Online DDL)
Las declaraciones `ALTER TABLE` tradicionales en MySQL a menudo bloquean tablas. PlanetScale utiliza **Online DDL** de Vitess a través de VReplication. Crea una tabla sombra, copia los datos incrementalmente y realiza la conmutación de forma transparente.

**Ejemplo de comando:**
```bash
pscale deploy-request deploy my-app 1
```
La producción permanece completamente operativa incluso durante migraciones grandes y de larga duración.

### Agrupación de Conexiones
La agrupación de conexiones integrada del lado del servidor maneja los picos de conexión. Al usar `pscale connect`, el proxy local también agrupa conexiones. Para producción, conéctate directamente a la dirección del servidor de PlanetScale.

### Sharding Horizontal (Vitess)
Para conjuntos de datos extremadamente grandes, PlanetScale utiliza el sharding por rango de claves de Vitess para distribuir datos de forma transparente entre muchas instancias de MySQL. No se requieren cambios en la aplicación.

### Alta Disponibilidad y Replicación Global
La alta disponibilidad está integrada. PlanetScale proporciona réplicas entre regiones y failover automático con un SLA de tiempo de actividad del 99.99%.

## Casos de Uso Prácticos

### Integración con CI/CD
Levanta una rama de base de datos aislada para cada pull request y ejecuta pruebas de integración con datos reales de producción.
```bash
pscale branch create my-app ci-pr-123 --from main
pscale connect my-app ci-pr-123 --port 3309 &
# Run integration tests here
pscale branch delete my-app ci-pr-123 --force
```

### Pruebas de Pre-Producción
Permite que QA ejecute pruebas destructivas o de carga en una rama completamente realista sin corromper los datos de producción.

### Revisión de Esquema
Los miembros del equipo revisan el diff SQL exacto en un Deploy Request antes de la fusión, lo que permite flujos de trabajo de 'base de datos como código'.

### Entornos Efímeros
Combina `pscale branch create/destroy` con herramientas de ingeniería de plataforma (por ejemplo, operadores de Kubernetes, Terraform) para proporcionar un entorno full-stack por desarrollador o por funcionalidad.

## Limitaciones y Advertencias

Aunque potente, la base de Vitess de PlanetScale introduce algunas peculiaridades de compatibilidad con MySQL:

- **Sin Procedimientos Almacenados ni Disparadores (Triggers):** La capa de proxy de Vitess no los soporta.
- **Claves Externas:** En beta (deben habilitarse por base de datos). Aún no recomendado para rutas críticas de producción.
- **`LOCK TABLES` / `UNLOCK TABLES`:** No soportado.
- **`GET_LOCK()` / `RELEASE_LOCK()`:** No soportado.
- **Subconsultas y `JOIN`s:** La mayoría son soportados, pero las subconsultas correlacionadas altamente complejas o las declaraciones no deterministas pueden comportarse de manera diferente.
- **`ALTER TABLE` directo en Producción:** El flujo de Deploy Request es la *única* forma segura de hacer cambios de esquema en producción. Ejecutar `ALTER TABLE` directamente en una rama de producción a través de `pscale connect` está muy desaconsejado.

> **Nota para Desarrolladores:** Utiliza siempre el flujo de Deploy Request para cambios de esquema en **producción**. Para ramas de desarrollo, `ALTER TABLE` directo es seguro y rápido.

## Modelo de Precios

PlanetScale opera como un producto SaaS con un generoso nivel gratuito. El precio se basa en el almacenamiento de filas y las lecturas/escrituras de filas.

| Nivel | Precio | Almacenamiento de Filas | Cómputo | Ramas |
|---|---|---|---|---|
| **Gratuito** | $0/mes | 5 GB | 10M lecturas de filas/mes, 1M escrituras de filas/mes | Hasta 3 |
| **Scaler** | $39/mes (base) | 10 GB | 100M lecturas de filas, 10M escrituras de filas | Hasta 10 |
| **Empresarial** | Personalizado | Personalizado | Personalizado | Personalizado |

*Los detalles de precios pueden cambiar; verifica siempre en la [página de precios de PlanetScale](https://planetscale.com/pricing).*

## Mejores Prácticas

- **Nombres de Ramas:** Utiliza un espacio de nombres consistente (por ejemplo, `feature/*`, `hotfix/*`, `ci/*`).
- **Destruir Ramas Obsoletas:** Limpia las ramas regularmente para evitar costos de almacenamiento.
  ```bash
  pscale branch delete my-app stale-branch --force
  ```
- **Monitorear el Rendimiento:** Utiliza el panel de control de PlanetScale para monitorear el rendimiento de las consultas, las consultas lentas y el uso de conexiones. Las funciones de explicación de consultas e información son potentes.
- **Paridad de Entornos:** Mantén `main` como un entorno de producción prístino. Los equipos de desarrollo trabajan exclusivamente en ramas.
- **Evitar Consultas Pesadas en Proxies de Ramas de Producción:** Si bien una rama es una instantánea, ejecutar consultas analíticas masivas en una rama conectada al mismo clúster subyacente que la producción puede afectar la E/S compartida.

## Solución de Problemas

**Conexión rechazada en el proxy:**
```bash
pscale connect my-app main
```
Asegúrate de que ningún otro servicio esté ejecutándose en el puerto. Usa `--port` para especificar una alternativa.

**Cambio de esquema fallido:**
Revisa los registros del Deploy Request en el panel de control de PlanetScale, o usa:
```bash
pscale deploy-request show my-app <deploy-number>
```

**Alta latencia de consulta:**
Verifica los límites de agrupación de conexiones. Considera agregar un índice a la rama antes de fusionar:
```sql
ALTER TABLE users ADD INDEX idx_email (email);
```

## Comparación con Alternativas

| Característica | PlanetScale | Neon (Postgres) | Supabase (Postgres) | RDS (MySQL) |
|---|---|---|---|---|
| **Branching** | Instantáneo, datos completos | Instantáneo, datos completos | Branching mediante SQL | Instantáneas manuales |
| **Serverless** | Sí (sueño/despertar) | Sí (sueño/despertar) | Sí (suspensión automática) | No (Siempre activo) |
| **Migraciones de Esquema** | Sin bloqueo (Online DDL) | Branching + `pgroll` | Branching + migraciones | Manual |
| **Sharding** | Automático (Vitess) | No | No | Manual (Sharding) |
| **Flujo CI de Migración** | Excelente (Deploy Requests) | Excelente | Bueno | Pobre |

**Cuándo elegir PlanetScale:**
Necesitas compatibilidad con MySQL, ramificación de bases de datos para cambios de esquema complejos y pruebas, y escalado horizontal automático.

**Cuándo evitar PlanetScale:**
Dependes en gran medida de procedimientos almacenados, disparadores (triggers) o características internas avanzadas de MySQL (por ejemplo, `GET_LOCK()`). En ese caso, RDS o una solución estándar de MySQL gestionado podrían ser más adecuados.

## Resumen

PlanetScale revoluciona la experiencia de desarrollo de MySQL al llevar flujos de trabajo similares a Git a la capa de base de datos. Su capacidad para bifurcar instantáneamente datos y esquemas, junto con Deploy Requests sin bloqueo, permite a los equipos iterar en los esquemas de base de datos con la misma seguridad y velocidad que su código de aplicación. Construido sobre el motor probado de Vitess, proporciona escalabilidad de nivel YouTube sin la sobrecarga operativa.