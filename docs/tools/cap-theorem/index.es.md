---
title: Teorema CAP (Teorema de Brewer)
description: Un principio fundamental de compensación en sistemas distribuidos que establece que es imposible que un almacén de datos distribuido garantice simultáneamente Consistencia, Disponibilidad y Tolerancia a Particiones.
created: 2026-06-21
tags:
  - distributed-systems
  - cap-theorem
  - consistency
  - availability
  - partition-tolerance
  - brewers-theorem
  - system-design
  - database-architecture
status: draft
---

# Teorema CAP (Teorema de Brewer)

## ¿Qué es el Teorema CAP?

El Teorema CAP es un principio fundamental en el diseño de sistemas distribuidos. Fue presentado por primera vez por **Eric Brewer** en el Simposio ACM sobre Principios de Computación Distribuida (PODC) en **2000** y demostrado formalmente por **Seth Gilbert** y **Nancy Lynch** en **2002**.

El teorema establece que un almacén de datos distribuido solo puede proporcionar **dos de tres** garantías en un momento dado:
- **Consistencia (C)**
- **Disponibilidad (A)**
- **Tolerancia a Particiones (P)**

Aunque a menudo se simplifica en exceso como una elección estricta de 'elige dos', la interpretación correcta es: **en presencia de una partición de red, debes elegir entre Consistencia y Disponibilidad**. Dado que las particiones de red son inevitables en sistemas distribuidos, no se pueden tener las tres simultáneamente.

---

## Las Tres Propiedades

### Consistencia (C)
Cada lectura recibe la **escritura más reciente** o un error. Todos los nodos del sistema ven los mismos datos en el mismo momento lógico. Esto implica un orden total de las operaciones (linealizabilidad).

- **Impacto:** Una consistencia más fuerte a menudo requiere sincronización entre nodos antes de confirmar escrituras.
- **Ejemplo:** Una lectura desde cualquier nodo debe devolver el mismo resultado que una lectura desde el nodo principal.

### Disponibilidad (A)
Toda solicitud recibida por un nodo no fallido en el sistema **debe resultar en una respuesta**. La respuesta puede no contener los datos más recientes, pero no será un error (por ejemplo, timeout o 503).

- **Impacto:** El sistema permanece activo y aceptando tráfico, incluso si algunas réplicas están desincronizadas.
- **Ejemplo:** Una aplicación web continúa sirviendo un catálogo de productos incluso si un nodo de base de datos aguas abajo es inalcanzable.

### Tolerancia a Particiones (P)
El sistema continúa operando a pesar de **que un número arbitrario de mensajes se pierdan o retrasen** en la red entre nodos. Esto incluye divisiones de red, cortes de cable y pérdida de paquetes.

- **Impacto:** El sistema debe funcionar correctamente incluso cuando los nodos no pueden comunicarse.
- **Realidad:** Las particiones son inevitables en cualquier sistema geográficamente distribuido. Por lo tanto, **todo sistema distribuido debe ser tolerante a P**.

---

## La Verdadera Compensación: CP vs AP

Debido a que las particiones de red (P) son inevitables en un sistema distribuido, lograr **CA** (Consistencia + Disponibilidad) sin Tolerancia a Particiones es imposible en un contexto distribuido. La elección real es:

### Sistemas CP (Consistencia + Tolerancia a Particiones)
- **Sacrifica:** Disponibilidad durante una partición.
- **Comportamiento:** Los nodos que no pueden garantizar consistencia con el resto del clúster se niegan a responder a las solicitudes (se vuelven no disponibles) hasta que la partición se resuelva.
- **Casos de uso:** Libros contables bancarios, gestión de inventarios, registros médicos — situaciones donde los datos desactualizados son inaceptables.
- **Ejemplos notables:**
  - **Apache ZooKeeper** (elección de líder, datos de configuración)
  - **Apache HBase** (modelo de consistencia fuerte)
  - **MongoDB** (con `w: "majority"` y lecturas desde el primario)
  - **Redis** (modo clúster con garantías estrictas de consistencia)

### Sistemas AP (Disponibilidad + Tolerancia a Particiones)
- **Sacrifica:** Consistencia durante una partición.
- **Comportamiento:** Todos los nodos permanecen disponibles para servir solicitudes, incluso si aceptan escrituras de forma independiente. El sistema depende de mecanismos de resolución de conflictos (por ejemplo, última escritura gana, CRDTs) para reconciliar los datos cuando la partición se cura.
- **Casos de uso:** Fuentes de redes sociales, entrega de contenido, datos de sensores IoT, catálogos de productos — entornos donde el tiempo de actividad es crítico.
- **Ejemplos notables:**
  - **Apache Cassandra** (consistencia ajustable, consistencia eventual por defecto)
  - **Amazon DynamoDB** (lecturas con consistencia eventual multirregión)
  - **CouchDB / Couchbase** (replicación multi-maestro)
  - **Riak**

### Sistemas CA (Consistencia + Disponibilidad)
- **Contexto:** Solo es posible en un sistema no distribuido (un solo nodo) o en un sistema que simplemente ignora las particiones (lo cual es peligroso).
- **Ejemplos notables:**
  - Una instancia independiente de **MySQL** o **PostgreSQL**.
  - Bases de datos relacionales tradicionales compatibles con ACID que se ejecutan en un solo servidor.
  - *Nota:* En un despliegue distribuido, estos sistemas deben replicar datos e inevitablemente encuentran particiones, lo que los obliga a adoptar un comportamiento CP o AP.

---

## Características Clave y Matices

### 1. La "P" no es Opcional
Un error común de principiantes es diseñar un sistema distribuido "CA". Una vez que los datos se replican a través de una red, eres susceptible a particiones. Cualquier sistema distribuido real **debe** tolerar particiones, lo que hace que la selección real sea **CP vs AP** cuando ocurre una partición.

### 2. Ajustabilidad
Las bases de datos modernas no están limitadas a una única clasificación. A menudo se puede intercambiar consistencia por disponibilidad (o viceversa) por consulta.

- **Cassandra:** Cambia entre `QUORUM` (consistencia fuerte) y `ONE` (consistencia eventual) por solicitud.
- **MongoDB:** Configura `writeConcern` y `readPreference` para cambiar entre consistencia fuerte y débil.
- **DynamoDB:** Elige `ConsistentRead` como `true` o `false` en las lecturas.

### 3. La Falacia de "2 de 3"
El teorema CAP no dice "el sistema siempre debe elegir dos de tres". Dice **durante una partición de red**, debes elegir **C** o **A**. El resto del tiempo (cuando la red está saludable), el sistema puede esforzarse por lograr tanto consistencia fuerte como alta disponibilidad.

Aquí es donde entra en juego el **Teorema PACELC**.

---

## La Extensión PACELC (La Visión Moderna)

Introducido por **Daniel J. Abadi**, PACELC extiende CAP al considerar explícitamente las compensaciones cuando el sistema está **saludable** (sin partición).

**PACELC significa:**
- Si ocurre una **P**artición → compensación entre **A**vailability y **C**onsistency.
- **E**lse (cuando la red está saludable) → compensación entre **L**atency y **C**onsistency.

### Por Qué es Importante PACELC
- **Compensaciones en Estado Saludable:** Incluso sin particiones, puedes optar por esperar a que las réplicas se pongan de acuerdo (alta latencia, consistencia fuerte) o responder rápidamente con datos potencialmente desactualizados (baja latencia, consistencia eventual).
- **Configuración en el Mundo Real:**
  - **CP system (during partition):** Sacrifica disponibilidad.
    - **E** (Else): También podría sacrificar latencia por consistencia (por ejemplo, replicación síncrona).
  - **AP system (during partition):** Sacrifica consistencia.
    - **E** (Else): Podría sacrificar consistencia por baja latencia (por ejemplo, replicación asíncrona, réplicas de lectura).

---

## Aplicación Práctica y Configuración

No "instalas" el teorema CAP, sino que configuras tus almacenes de datos distribuidos para gestionar sus compensaciones.

### Lógica de Decisión Conceptual (Pseudocódigo)

```python
# High-level logic for handling a request during a detected partition

import config

def handle_write_during_partition(data):
    partition_detected = check_network_health()
    
    if partition_detected:
        if config.CAP_MODE == "CP":
            # Refuse the write to maintain consistency
            raise ServiceUnavailable("Cannot guarantee consistency during partition.")
        elif config.CAP_MODE == "AP":
            # Accept the write locally; resolve conflicts later
            store_with_timestamp(data, node_id=config.NODE_ID)
            return {"status": "accepted", "note": "Eventual consistency in effect."}
    else:
        # Network is healthy -> standard operation
        return normal_write_operation(data)
```

### MongoDB: Ajuste CP/AP por Consulta

```javascript
// CP behavior: Ensure writes are committed to majority before acknowledging
db.inventory.insertOne(
   { item: "journal", qty: 25, status: "A" },
   { writeConcern: { w: "majority", wtimeout: 5000 } }
);

// CP behavior: Read from the primary (strongest consistency)
db.inventory.find({ status: "A" }).readPref("primary");

// AP behavior: Read from any secondary (potential stale data)
db.inventory.find({ status: "A" }).readPref("secondary");

// AP behavior: Allow reads from secondaries if primary is unreachable
db.inventory.find({ status: "A" }).readPref("secondaryPreferred");
```

### Apache Cassandra: Niveles de Consistencia Ajustables

```cql
-- Strong Consistency (towards CP)
-- Ensures all replicas in the quorum have the same data
SELECT * FROM users WHERE user_id = 123 CONSISTENCY QUORUM;

-- Write with strong consistency
INSERT INTO users (user_id, name) VALUES (123, 'Alice') USING TIMESTAMP 1000;
-- Ensure quorum acknowledged the write
-- Requires consistency level QUORUM or ALL

-- Eventual Consistency (towards AP, lower latency)
SELECT * FROM users WHERE user_id = 123 CONSISTENCY ONE;

-- High Availability, low consistency (AP)
-- Writes acknowledged by just one node
INSERT INTO users (user_id, name) VALUES (456, 'Bob') CONSISTENCY ANY;
```

---

## Cuándo Elegir CP vs AP

| Escenario | Enfoque Recomendado | Justificación |
|---|---|---|
| Procesamiento de pagos / Libros contables | **CP** | Los recuentos o saldos inconsistentes causan pérdidas financieras y problemas legales. El tiempo de inactividad temporal durante una partición es preferible al doble gasto. |
| Registros médicos / Datos médicos | **CP** | Las decisiones críticas para la vida dependen de datos completos y precisos. El tiempo de inactividad es más seguro que diagnósticos contradictorios o desactualizados. |
| Datos de sesión de usuario (comercio electrónico) | **AP** | Los usuarios deben poder navegar y agregar artículos a su carrito incluso si un centro de datos se desconecta. Los recuentos de inventario desactualizados son una compensación temporal aceptable. |
| Fuentes de redes sociales | **AP** | Los usuarios esperan que el sitio esté activo. Un 'me gusta' faltante o un comentario retrasado es aceptable si significa que la aplicación sigue respondiendo. |
| Entrega de contenido / CDNs | **AP** | Servir una versión en caché ligeramente desactualizada de una página es muy preferible a una página de error. |
| Almacenes de metadatos / configuración (ZooKeeper, etcd) | **CP** | La configuración debe ser autorizada y consistente en todo el clúster. Dividir el clúster en vistas inconsistentes es peligroso (split-brain). |

---

## Historia e Impacto

### Cronología
- **1998:** Eric Brewer presenta por primera vez la idea de las tres propiedades.
- **2000:** Brewer postula formalmente la conjetura en PODC.
- **2002:** Seth Gilbert y Nancy Lynch del MIT publican "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services", demostrando formalmente el teorema.
- **Finales de los 2000:** El teorema influyó directamente en la arquitectura de **Amazon DynamoDB**, **Google Bigtable**, **Apache Cassandra** y **MongoDB**.
- **2010s:** El movimiento NoSQL adopta el teorema CAP como principio de diseño principal. Se introduce PACELC para aclarar las compensaciones 'siempre', no solo durante las particiones.
- **2020s:** Las bases de datos SQL distribuidas modernas (Spanner, CockroachDB, YugabyteDB) intentan empujar los límites, esforzándose por 'C y A' la mayor parte del tiempo al reducir agresivamente la probabilidad y duración de las particiones (por ejemplo, usando TrueTime / sincronización de reloj ajustada).

### Perspectiva Clave
El teorema CAP fue revolucionario porque dio a los arquitectos un lenguaje formal para discutir compensaciones. Antes de CAP, los operadores esperaban que las bases de datos distribuidas se comportaran exactamente como las monolíticas. El teorema obligó a la industria a admitir que **la consistencia fuerte tiene un costo**, y ese costo a menudo se paga en disponibilidad durante fallos.

---

## Limitaciones y Críticas

1.  **Falso Binario:** Los críticos argumentan que 'C, A, P' no son propiedades binarias. Hay grados de consistencia (fuerte, causal, eventual, leer-tus-escrituras) y disponibilidad.
2.  **Ignorar la Latencia:** El teorema CAP original no aborda explícitamente las compensaciones cuando la red está saludable (esto se aborda con PACELC).
3.  **CA es una Trampa:** Muchos ingenieros buscan sistemas 'CA' distribuidos. En realidad, cualquier sistema que replique datos a través de una red es tolerante a P por necesidad. Etiquetar un sistema puramente como 'CA' es a menudo marketing, no arquitectura.
4.  **Mitigación Moderna:** Bases de datos como **Google Spanner** utilizan relojes atómicos y la API TrueTime para lograr consistencia fuerte y alta disponibilidad simultáneamente *la mayor parte del tiempo*, reduciendo el escenario de 'elegir 2 de 3' a un caso límite raro.

---

## Ver También

- **Teorema PACELC** — La extensión moderna de CAP que incluye compensaciones de latencia.
- **Consistencia Eventual** — El modelo de consistencia en el que se basan la mayoría de los sistemas AP.
- **ACID vs BASE** — ACID (Atomicidad, Consistencia, Aislamiento, Durabilidad) vs BASE (Básicamente Disponible, Estado Suave, Consistencia Eventual).
- **Eric Brewer** — Proponente original del teorema.
- **Diseño de Sistemas Distribuidos** — Fragmentación, replicación, algoritmos de consenso (Raft, Paxos).
- **CRDTs (Tipos de Datos Replicados sin Conflictos)** — Estructuras de datos que resuelven conflictos de forma natural en sistemas AP.