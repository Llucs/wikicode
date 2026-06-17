---
title: Sharding — Particionamiento Horizontal de Bases de Datos para Escalabilidad
description: Una guía detallada sobre sharding, una técnica para particionar bases de datos horizontalmente entre servidores para mejorar escalabilidad, rendimiento y aislamiento de fallos.
created: 2026-06-16
tags:
  - database
  - scalability
  - sharding
  - distributed-systems
  - performance
status: draft
---

# Sharding

**Sharding** es un patrón de arquitectura de bases de datos donde un conjunto de datos grande y lógicamente unificado se particiona horizontalmente en bases de datos más pequeñas e independientes llamadas *shards*. Cada shard se aloja en una instancia de servidor separada que opera en una arquitectura “shared-nothing”. El sharding supera los límites de escalado vertical de una sola máquina al distribuir datos y carga de trabajo a través de muchos nodos.

## Qué Es

Sharding divide los datos en fragmentos basándose en una *shard key* determinista. Cada shard contiene un subconjunto de los datos (por ejemplo, todas las filas para un rango de `user_id` dado) y es responsable de atender lecturas y escrituras para su partición. El sistema total aparece como una base de datos lógica única para los clientes a través de una capa de enrutamiento (lógica de aplicación, proxy o enrutador de base de datos).

## ¿Por Qué Fragmentar?

| Beneficio | Descripción |
|-----------|-------------|
| **Escalabilidad horizontal** | El rendimiento de lectura y escritura escala linealmente a medida que se añaden shards. |
| **Alta disponibilidad y aislamiento de fallos** | Una falla en un solo shard afecta solo a un subconjunto de usuarios; otros shards continúan sirviendo. |
| **Paralelismo** | Las consultas que tocan múltiples shards pueden paralelizarse, mejorando la latencia. |
| **Distribución geográfica** | Los datos pueden colocarse más cerca de poblaciones de usuarios específicas, reduciendo los viajes de ida y vuelta en la red. |
| **Aislamiento operativo** | El mantenimiento, las copias de seguridad y los cambios de esquema pueden realizarse en un shard a la vez. |

Sharding es esencial cuando una sola base de datos ya no puede manejar la carga—a menudo después de que el escalado vertical (CPU más grandes, más RAM) se vuelve prohibitivo en costos o alcanza los límites del hardware.

## Arquitecturas de Sharding

El sharding se puede implementar en varios niveles:

### 1. Nivel de Aplicación (Manual)

La aplicación contiene lógica de enrutamiento (p. ej., `hash(user_id) % num_shards`). Cada shard es una base de datos estándar sin software adicional.  
**Pros:** Simple de empezar, sin middleware.  
**Contras:** Frágil; el resharding requiere cambios de código; las consultas entre shards son extremadamente difíciles.  
**Estado:** Hoy en día considerado un anti‑patrón para nuevos proyectos.

### 2. Nivel Middleware / Proxy (por ejemplo, Vitess, Citus)

Un proxy transparente intercepta consultas SQL y las enruta al shard apropiado.

- **Vitess** para MySQL: implementa `vtgate` (proxy) + `vttablet` por shard, gestionado por una topología etcd/zookeeper.
- **Citus** para PostgreSQL: una extensión que convierte un clúster de Postgres en una base de datos distribuida.

**Pros:** Transparencia SQL, resharding automatizado (Vitess), joins entre shards (Citus).  
**Contras:** Capa adicional de complejidad; algunas consultas se vuelven imposibles o lentas.

### 3. Nativo de la Base de Datos (por ejemplo, MongoDB, Cassandra, Druid)

El motor de base de datos maneja la distribución internamente. El desarrollador proporciona una shard key, y el sistema gestiona la ubicación y enrutamiento de los datos.

- **MongoDB**: clústeres fragmentados con enrutadores `mongos` y servidores de configuración.
- **Cassandra**: particionamiento por una clave de partición en la definición de la clave primaria; el hashing consistente distribuye las filas automáticamente.

**Pros:** Sin proxy externo; funciones como balanceo automático.  
**Contras:** Debe diseñar cuidadosamente el modelo de datos alrededor de la shard key; las operaciones entre shards son limitadas o inexistentes.

### 4. Gestionado en la Nube (por ejemplo, Amazon DynamoDB, Azure Cosmos DB, Google Cloud Spanner)

El proveedor abstrae completamente la gestión de shards. Usted elige una clave de partición durante la creación de la tabla; la plataforma en la nube divide, migra y balancea los datos automáticamente.

**Pros:** Sin sobrecarga operativa; escalado automático.  
**Contras:** Dependencia del proveedor; el costo puede ser más alto para cargas de trabajo grandes; sin control directo sobre la ubicación de los shards.

## Instalación y Uso Básico

A continuación se muestran ejemplos concretos para dos de las implementaciones de sharding más comunes.

### Sharding en MongoDB

**Instalación / Configuración**

- Implemente un **conjunto de réplicas de servidor de configuración** (CSRS) que almacene metadatos del clúster.
- Implemente **conjuntos de réplicas de shard** (cada shard es al menos un nodo único, pero generalmente un conjunto de réplicas para alta disponibilidad).
- Implemente uno o más **enrutadores `mongos`** que procesen consultas de aplicaciones.

Los siguientes comandos (ejecutados contra un `mongos`) habilitan el sharding y fragmentan una colección:

```javascript
// Enable sharding on a database
sh.enableSharding("ecommerce");

// Shard a collection using a hashed shard key (recommended for uniform distribution)
sh.shardCollection(
  "ecommerce.orders",
  { "order_id": "hashed" }
);
```

Con una shard key hasheada, los documentos se distribuyen uniformemente entre los shards. Las consultas que incluyen la shard key se enrutan directamente al shard correcto:

```javascript
// Efficient query – goes to a single shard
db.orders.find({ "order_id": UUID("123e4567-e89b-12d3-a456-426614174000") })
```

Las consultas entre shards (por ejemplo, agregaciones sin la shard key) se dispersarán a todos los shards, afectando potencialmente el rendimiento.

### Citus (Extensión de PostgreSQL)

**Instalación**

1. Instale la extensión `citus` en el nodo coordinador y en todos los nodos trabajadores.
2. Agregue nodos trabajadores al coordinador:
   ```sql
   SELECT citus_add_node('worker-node-1', 5432);
   SELECT citus_add_node('worker-node-2', 5432);
   ```

**Uso Básico**

Distribuya una tabla especificando su columna de distribución (shard key):

```sql
-- Create the table on the coordinator
CREATE TABLE orders (
    order_id    BIGSERIAL,
    user_id     INT,
    product_id  INT,
    quantity    INT,
    PRIMARY KEY (order_id, user_id)
);

-- Distribute the table across workers based on user_id
SELECT create_distributed_table('orders', 'user_id');
```

Citus reescribe el SQL para alcanzar el shard relevante. Una consulta que filtra por `user_id` irá a un solo worker:

```sql
-- Single‑shard query
SELECT * FROM orders WHERE user_id = 42;
```

Para joins entre dos tablas que están co‑ubicadas en la misma clave de distribución, Citus puede ejecutarlos de manera eficiente:

```sql
-- Co‑location example: orders and order_items distributed on user_id
SELECT create_distributed_table('orders', 'user_id');
SELECT create_distributed_table('order_items', 'user_id');
-- JOIN now happens locally on each shard
SELECT o.order_id, oi.product_id
FROM orders o JOIN order_items oi USING (order_id)
WHERE o.user_id = 42;
```

## Decisiones Clave de Diseño

### 1. Elección de la Shard Key

La shard key es la decisión más crítica. Debe:

- **Distribuir los datos uniformemente** para evitar puntos calientes.
- **Coincidir con los patrones de consulta** para que las consultas comunes puedan enrutarse a un solo shard.
- **Tener alta cardinalidad** (muchos valores distintos) para permitir una división uniforme.

**Malas elecciones:** Valores que aumentan monótonamente (por ejemplo, marcas de tiempo, IDs autoincrementales) hacen que todas las nuevas escrituras vayan al último shard.  
**Mejores elecciones:** IDs de usuario, columnas hasheadas o claves compuestas que combinen alta cardinalidad y columnas de filtro frecuentes.

### 2. Operaciones entre Shards

Los JOINs, transacciones y agregaciones que abarcan múltiples shards son muy costosos o no están soportados. Estrategias de mitigación:

- **Desnormalización** para mantener datos relacionados en el mismo shard.
- **Co‑ubicación** (Citus) o **incrustación de documentos** (MongoDB) para almacenar datos jerárquicos en el mismo shard.
- **Coordinación desde la aplicación** para transacciones de múltiples shards (rara vez recomendado).

### 3. Resharding

Agregar o eliminar shards requiere redistribuir datos. Los sistemas modernos ofrecen mecanismos integrados:

- **MongoDB Balancer** mueve automáticamente chunks entre shards.
- **Vitess Reshard** divide shards utilizando un flujo de trabajo `MoveTables`.
- **Servicios en la nube** manejan las divisiones de manera transparente.

El resharding manual (en sharding a nivel de aplicación) es notoriamente difícil y propenso a errores.

## Estado Moderno

La industria se está alejando del sharding manual. Las bases de datos **NewSQL** (CockroachDB, YugabyteDB, Google Spanner) abstraen completamente la gestión de shards detrás de una interfaz SQL estándar, proporcionando transacciones ACID y joins entre shards. La mayoría de las bases de datos en la nube (DynamoDB, Cosmos DB) ofrecen sharding sin servidor (serverless). Sin embargo, el concepto central de sharding sigue siendo la base para todas las bases de datos distribuidas escalables horizontalmente.

Para nuevos proyectos, prefiera uno de estos en lugar de construir su propia capa de sharding. Si necesita SQL y consistencia fuerte, considere Citus o Spanner; si la flexibilidad orientada a documentos y el rendimiento masivo son primordiales, MongoDB o DynamoDB son excelentes opciones.

## Resumen

Sharding es una herramienta poderosa para lograr rendimiento a escala web, pero introduce complejidad. Al comprender las opciones arquitectónicas, elegir una buena shard key y aprovechar las herramientas modernas de gestión, puede escalar su capa de datos sin reinventar la rueda.