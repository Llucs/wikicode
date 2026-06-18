---
title: Neon – Plataforma PostgreSQL Serverless
description: Neon es una base de datos PostgreSQL serverless de código abierto que separa el cómputo del almacenamiento, proporcionando bifurcación instantánea, escalado a cero y almacenamiento sin límites para aplicaciones modernas.
created: 2026-06-18
tags:
  - serverless
  - postgres
  - database
  - branching
  - cloud
status: draft
---

# Neon – Plataforma PostgreSQL Serverless

Neon es una plataforma PostgreSQL serverless de código abierto que reconstruye la arquitectura clásica de bases de datos sobre una base nativa en la nube. Al desacoplar completamente el cómputo (procesamiento de consultas) del almacenamiento (persistencia de datos), Neon ofrece características anteriormente disponibles solo en sistemas propietarios como Amazon Aurora, pero para todo el ecosistema de Postgres. Con bifurcación instantánea, escalado automático a cero y almacenamiento sin límites, Neon está diseñado para flujos de trabajo de desarrollo modernos y aplicaciones serverless.

---

## ¿Por qué Neon?

| Desafío | Solución Neon |
|-----------|---------------|
| **Bases de datos inactivas costosas** | Los endpoints de cómputo escalan a cero después de inactividad; solo pagas por el cómputo activo. |
| **Ciclos de desarrollo lentos** | La bifurcación instantánea le da a cada desarrollador/PR su propia bifurcación de base de datos con total fidelidad. |
| **Aprovisionamiento y costo de almacenamiento** | Almacenamiento sin límites respaldado por almacenes de objetos (ej. S3); sin necesidad de planificación manual de capacidad. |
| **Compatibilidad serverless/edge** | Tiempos de arranque en frío de ~500 ms, combinados con agrupación de PgBouncer para cómputo efímero. |
| **Cargas de trabajo vectoriales** | Soporte completo para `pgvector` y PostGIS; ejecuta embeddings de IA directamente en Postgres. |

---

## Características Principales

### 1. Bifurcación Instantánea

Usando tecnología de copia en escritura, Neon puede crear una bifurcación de una base de datos a escala de terabytes en milisegundos. Esto es invaluable para:

- **Entornos de desarrollo aislados** – cada desarrollador obtiene un clon aislado de producción.
- **Pipelines de CI/CD** – ejecuta pruebas de integración contra una bifurcación que refleja los datos de producción.
- **Migraciones de esquema** – prueba cambios disruptivos sin riesgo.

```bash
# Create a new branch from the main branch
npx neonctl branches create --name feature/ai-search
```

### 2. Escalado a Cero

Los endpoints de cómputo se suspenden automáticamente después de un período de inactividad. Cuando llega una nueva conexión, el endpoint se reanuda en aproximadamente 500 ms (arranque en frío). Esto elimina los costos de bases de datos inactivas o con poco tráfico.

```sql
-- No configuration needed – scale‑to‑zero is automatic.
-- Connect and the endpoint wakes up transparently.
```

### 3. Almacenamiento Sin Límites

El almacenamiento es manejado por un motor separado (Pageserver + Safekeepers) respaldado por almacenamiento de objetos económico. Nunca necesitas aprovisionar discos ni preocuparte por llenarlos.

### 4. Compatibilidad Total con PostgreSQL

Neon es compatible con PostgreSQL 14–17, incluyendo todas las extensiones principales:

- `pgvector` – búsqueda de similitud vectorial para embeddings.
- `PostGIS` – consultas geoespaciales.
- `pg_cron`, `pg_stat_statements`, etc.

Tus herramientas y controladores existentes funcionan sin cambios.

### 5. Agrupación de Conexiones Transparente

PgBouncer está integrado a nivel de proxy, por lo que obtienes un manejo eficiente de conexiones sin necesidad de configuración en la aplicación.

---

## Inicio Rápido

### Opción A: Nube (Gestionado)

1. Regístrate en [console.neon.tech](https://console.neon.tech) (incluye un generoso nivel gratuito).
2. Crea un proyecto mediante la interfaz de usuario o la CLI:

   ```bash
   # Install the Neon CLI
   npx neonctl

   # Create a project (first time: interactive)
   npx neonctl create-project

   # Get the connection string for the main branch
   npx neonctl connection-string
   ```

### Opción B: Autoalojado

Clona el repositorio de código abierto y despliega usando Docker Compose o Helm.

```bash
git clone https://github.com/neondatabase/neon.git
cd neon
docker compose up -d
```

Consulta la [guía oficial de autoalojamiento](https://neon.tech/docs/self-host) para despliegues en producción.

---

## Ejemplos de Uso

### Conectar y Ejecutar Consultas

```bash
psql "postgresql://user:pass@ep-cool-123456.us-east-2.aws.neon.tech/neondb"
```

```sql
-- Standard Postgres – everything works
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    payload JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- pgvector example
CREATE EXTENSION vector;
CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    embedding vector(1024)
);
```

### Crear y Cambiar Bifurcaciones

```bash
# List branches
npx neonctl branches list

# Create a branch from a specific point in time (time travel)
npx neonctl branches create --from main --time "2026-06-17T12:00:00Z"

# Use a branch: get its connection string
npx neonctl connection-string --branch feature/ai-search
```

### Integrar con Vercel / Netlify

Debido a que Neon admite conexiones HTTP a través de `@neondatabase/serverless`, puedes conectarte desde funciones edge:

```javascript
// Example: Next.js API route
import { neon } from '@neondatabase/serverless';

export default async function handler(req, res) {
  const sql = neon(process.env.DATABASE_URL);
  const result = await sql`SELECT * FROM events`;
  res.json(result);
}
```

---

## Arquitectura en Resumen

```
 Application
    |
    | (PostgreSQL protocol)
    |
 Proxy  ─── PgBouncer (connection pooling)
    |
 Compute Node (Stateless Postgres process)
    |
 Pageserver (Storage engine)
    |
 Safekeeper (WAL persistence)
    |
 Object Store (S3, GCS, etc.)
```

- **Los nodos de cómputo** son sin estado y pueden escalarse horizontalmente.
- **Pageserver** maneja el servicio de páginas, los puntos de control y la bifurcación (copia en escritura).
- **Safekeeper** garantiza la durabilidad del WAL antes del acuse de recibo.

---

## Modelo de Precios

Neon tiene **precios basados en uso**:

| Recurso | Nivel Gratuito | Nivel de Pago |
|----------|-----------|---------------|
| Cómputo (activo) | 10 horas/mes | Paga por hora de cómputo |
| Almacenamiento | 500 MB | $0.12/GB/mes |
| Bifurcación | Ilimitada | Ilimitada |
| Agrupación de conexiones | Sí | Sí |

El escalado a cero significa que solo pagas por cómputo cuando tu aplicación está realmente sirviendo consultas.

---

## Limitaciones y Advertencias

- **Latencia de arranque en frío** – Aunque es de ~500 ms, puede ser notable en funciones sensibles a la latencia. Usa conexiones persistentes o endpoints siempre activos para rutas críticas.
- **Paridad de características** – Solo despliegues de servidor único (sin fragmentación nativa). Para activo-activo multirregión, es posible que aún necesites estrategias de replicación externas.
- **Límite del nivel gratuito** – El límite de 10 horas de cómputo puede consumirse rápidamente si varios proyectos permanecen activos.

---

## Recursos

- [Documentación Oficial](https://neon.tech/docs)
- [Repositorio de GitHub](https://github.com/neondatabase/neon)
- [Comunidad en Discord de Neon](https://discord.gg/neon)
- [Blog – Comprendiendo la Arquitectura de Neon](https://neon.tech/blog/architecture)

Neon transforma PostgreSQL en una base de datos verdaderamente serverless, convirtiéndola en una opción ideal para aplicaciones modernas, CI/CD y cargas de trabajo de IA/vectoriales. Su combinación de bifurcación instantánea, escalado a cero y compatibilidad total con Postgres lo ha convertido en uno de los proyectos de infraestructura más populares de 2024–2026.