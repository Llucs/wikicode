---
title: Ereignisgesteuerte Architektur
description: Ein Softwareentwurfsmuster, bei dem Systemkomponenten asynchron durch das Erzeugen und Konsumieren von Ereignissen kommunizieren und so lose gekoppelte, skalierbare und Echtzeitsysteme ermöglichen.
created: 2026-06-16
tags:
  - event-driven-architecture
  - microservices
  - apache-kafka
  - rabbitmq
  - async
status: draft
---

# Ereignisgesteuerte Architektur (EDA)

Ereignisgesteuerte Architektur (EDA) ist ein Softwareentwurfsmuster, bei dem der Ablauf eines Systems durch die Erzeugung, Erkennung und Reaktion auf **Ereignisse** bestimmt wird – eine wesentliche Zustandsänderung (z. B. `OrderPlaced`, `FileUploaded`, `UserLoggedIn`). Komponenten kommunizieren asynchron über einen **Ereignisvermittler** (oder Kanal) und entkoppeln so den Ereignisproduzenten vom Ereigniskonsumenten.

Dieser Ansatz steht im Gegensatz zu traditionellen **anforderungsgesteuerten** (synchronen) Architekturen (z. B. REST-APIs), bei denen ein Client eine Anfrage sendet und blockiert, während er auf eine direkte Antwort wartet. EDA ist grundlegend für den Aufbau widerstandsfähiger, skalierbarer und Echtzeit‑verteilter Systeme.

## Warum eine ereignisgesteuerte Architektur verwenden?

| Vorteil | Beschreibung |
|---------|-------------|
| **Loose Coupling** | Produzenten und Konsumenten sind unabhängig. Sie hängen nur vom Ereignisschema ab, nicht von der Implementierung, dem Standort oder der Verfügbarkeit des jeweils anderen. Dienste können unabhängig voneinander aktualisiert, bereitgestellt und skaliert werden. |
| **Asynchrone Kommunikation** | Produzenten warten nicht auf Antworten der Konsumenten. Nicht blockierende Abläufe verbessern die Reaktionsfähigkeit des Systems und die Ressourcenauslastung. |
| **Skalierbarkeit** | Jede Komponente kann basierend auf ihrer Ereignislast unabhängig skaliert werden. Der Vermittler puffert Ereignisse und bewältigt so Lastspitzen ohne Datenverlust. |
| **Ausfallsicherheit** | Wenn ein Konsument ausfällt, bleiben Ereignisse im Vermittler erhalten. Sobald der Konsument wiederhergestellt ist, kann er den Rückstand automatisch verarbeiten. |
| **Echtzeit‑Reaktivität** | Systeme können sofort auf neue Informationen reagieren und Live‑Dashboards, Benachrichtigungen und automatisierte Arbeitsabläufe ermöglichen. |
| **Prüfbarkeit & Wiedergabe** | Gespeicherte Ereignisse bieten ein unveränderliches Audit‑Log. Der Zustand kann durch erneute Wiedergabe von Ereignissen (Event Sourcing) wiederhergestellt werden. |

## Kernkonzepte

- **Event** – Eine Aufzeichnung von etwas, das passiert ist. Enthält normalerweise einen Typ, Zeitstempel, Nutzlast und Metadaten.
- **Producer** – Eine Komponente, die Ereignisse aussendet (z. B. ein Dienst nach einem Datenbankschreibvorgang).
- **Consumer** – Eine Komponente, die einen oder mehrere Ereignistypen abonniert und verarbeitet.
- **Event Broker** – Die Middleware, die Ereignisse vom Produzenten zum Konsumenten weiterleitet. Beispiele: Apache Kafka, RabbitMQ, AWS EventBridge, Google Pub/Sub.
- **Topic / Exchange** – Ein benannter Kanal, in dem Ereignisse veröffentlicht werden. Konsumenten abonnieren Themen.
- **Schema** – Die Struktur und der Vertrag der Ereignisdaten. Oft mit Avro, Protobuf oder JSON Schema definiert und in einer Schema Registry verwaltet.

## Häufige Muster

| Muster | Beschreibung |
|---------|-------------|
| **Publish/Subscribe (Pub/Sub)** | Ein einzelnes Ereignis wird an alle interessierten Konsumenten geliefert. Nützlich zum Verteilen von Benachrichtigungen. |
| **Event Streaming** | Ereignisse werden der Reihe nach konsumiert, typischerweise von einem log‑basierten Vermittler (z. B. Kafka). Wird für Echtzeitanalysen und Datenpipelines verwendet. |
| **Event Sourcing** | Alle Ereignisse werden als Quelle der Wahrheit gespeichert. Der aktuelle Zustand wird durch erneute Wiedergabe der Ereignisse abgeleitet. Bietet eine perfekte Audit‑Spur. |
| **CQRS** | Command Query Responsibility Segregation – Trennung von Lese‑ und Schreibmodellen, oft in Verbindung mit Event Sourcing. |
| **Transaction Outbox** | Datenbanktransaktionen umfassen das Schreiben von Ereignissen in eine „Outbox“‑Tabelle; ein separater Sender veröffentlicht sie an den Vermittler und gewährleistet so Atomizität. |

## Erste Schritte

### Installieren Sie einen Ereignisvermittler (Entwicklung)

Der schnellste Weg, um mit Experimenten zu beginnen, ist Docker.

**Apache Kafka (mit KRaft – ohne Zookeeper)**

```bash
docker run -d --name broker -p 9092:9092 apache/kafka:latest
```

**RabbitMQ (mit Verwaltungsoberfläche)**

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

**Cloud‑Vermittler** (keine lokale Installation):
- AWS: SQS / SNS / EventBridge / MSK
- Azure: Queue Storage / Service Bus / Event Grid / Event Hubs
- GCP: Pub/Sub

### Definieren Sie ein Ereignisschema (Beispiel: CloudEvents)

```json
{
  "specversion": "1.0",
  "type": "com.example.order.placed",
  "source": "https://orders.example.com",
  "id": "a234-1234-1234",
  "time": "2026-06-16T14:00:00Z",
  "datacontenttype": "application/json",
  "data": {
    "orderId": "O-98765",
    "userId": "user-42",
    "total": 299.99
  }
}
```

### Grundlegende Verwendung

Nachfolgend ein minimaler Produzent und Konsument unter Verwendung von **Apache Kafka** und **Python**.

#### Produzent (Bestelldienst)

```python
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

event = {
    "type": "OrderPlaced",
    "order_id": "O-12345",
    "user": "alice",
    "timestamp": time.time()
}

producer.send('orders', value=event)
producer.flush()
print(f"Produced: {event}")
```

#### Konsument (E‑Mail‑Dienst)

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'orders',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

for msg in consumer:
    event = msg.value
    if event['type'] == 'OrderPlaced':
        print(f"Sende Bestätigungs‑E‑Mail an {event['user']} für Bestellung {event['order_id']}")
        # ... E‑Mail‑Logik implementieren
    else:
        print(f"Ignorierter Ereignistyp: {event['type']}")
```

Um das Beispiel auszuführen, starten Sie Kafka, erstellen Sie das Thema (`kafka-topics.sh --create --topic orders --bootstrap-server localhost:9092`) und führen Sie dann beide Skripte aus.

### Verwalten von Themen und Konsumenten (Befehlszeile)

```bash
# Thema erstellen
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 3 --replication-factor 1

# Themen auflisten
kafka-topics.sh --bootstrap-server localhost:9092 --list

# Konsumieren von der Befehlszeile (Debug)
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders --from-beginning
```

## Hauptmerkmale im Detail

### Asynchron & nicht blockierend
Produzenten feuern Ereignisse ab und vergessen sie. Die Verarbeitung durch den Konsumenten erfolgt in seinem eigenen Kontext. Dadurch kann das System hohe Last bewältigen, ohne vorgelagerte Dienste zu blockieren.

### Lockere Kopplung
Dienste sind nur an das Ereignisschema gekoppelt. Änderungen an einem Produzenten oder Konsumenten können unabhängig bereitgestellt werden, solange der Vertrag eingehalten wird.

### Skalierbarkeit
Ereignisvermittler unterstützen Partitionierung, sodass mehrere Konsumenten Ereignisse parallel verarbeiten können. Die Arbeitslast kann auf viele Instanzen verteilt werden.

### Ereigniswiedergabe
Vermittler (insbesondere Kafka) behalten Ereignisse für einen konfigurierbaren Zeitraum. Konsumenten können Offsets zurücksetzen und historische Ereignisse erneut verarbeiten – nützlich zum Debuggen, Neuerstellen von Caches oder zur Einspeisung eines neuen Dienstes.

### Schemaentwicklung
Mit einer Schema Registry (z. B. Confluent Schema Registry, Azure Schema Registry) können Sie bei Schemaänderungen Abwärts‑/Vorwärtskompatibilität erzwingen und so Laufzeitfehler vermeiden.

## Bewährte Methoden

| Praxis | Warum |
|----------|-----|
| **Idempotenz** | Ereignisse können mehrfach zugestellt werden. Entwerfen Sie Konsumenten so, dass sie Duplikate sicher behandeln (z. B. mit idempotenten Schlüsseln). |
| **Datenverträge** | Verwenden Sie strenge Schemata (Avro, Protobuf) mit einer Schema Registry. Vermeiden Sie bahnbrechende Änderungen – entwickeln Sie Schemata kompatibel weiter. |
| **Verteiltes Tracing** | Asynchrone Abläufe sind schwer zu verfolgen. Verwenden Sie `traceparent`‑Header (OpenTelemetry), um Ereignisse über Dienste hinweg zu korrelieren. |
| **Überwachung & Alarmierung** | Messen Sie Produzenten‑/Konsumentenverzögerung, Durchsatz und Fehlerraten. Richten Sie Alarme für zunehmende Verzögerungen oder Konsumentenausfälle ein. |
| **Eventuelle Konsistenz** | EDA ist von Natur aus irgendwann konsistent. Die Geschäftslogik muss vorübergehende Abweichungen tolerieren und die endgültige Konsistenz sicherstellen. |
| **Wiederholungen & Dead-Letter-Warteschlangen** | Konsumenten, die fehlschlagen, sollten es mit exponentiellem Backoff erneut versuchen; nachdem die Wiederholungsversuche erschöpft sind, verschieben Sie das Ereignis zur manuellen Prüfung in eine Dead-Letter-Warteschlange. |
| **Sicherheit** | Authentifizieren und autorisieren Sie sowohl Produzenten als auch Konsumenten. Verschlüsseln Sie Ereignisse während der Übertragung und im Ruhezustand. Verwenden Sie private Netzwerke für Vermittler in der Produktion. |

## Häufige Fallstricke

- **Überengineering**: Nicht jede Aktion benötigt ein Ereignis. Einfaches CRUD wird möglicherweise besser mit synchronen APIs bedient.
- **Datenverlust**: Falsch konfigurierte Vermittler (z. B. `acks=0` in Kafka) können Ereignisse verlieren. Konfigurieren Sie in der Produktion immer dauerhafte Einstellungen.
- **Unordentliche Schemata**: Fehlende Governance führt zu inkompatiblen Änderungen und nachgelagerten Fehlern. Führen Sie frühzeitig eine Schema Registry ein.
- **Komplexität beim Debuggen**: Ereignisgesteuerte Abläufe können schwer zu verfolgen sein. Investieren Sie von Anfang an in Beobachtbarkeit.
- **Monolithischer Ereignisbus**: Ein einziger gemeinsamer Vermittler wird zum Engpass und zum Single Point of Failure. Erwägen Sie für größere Systeme domänenspezifische Busse.

## Geschichte

EDA entstand aus der nachrichtenorientierten Middleware (MOM) in den 1980er‑ und 1990er‑Jahren (IBM MQ, TIBCO Rendezvous). In den 2000er Jahren standardisierten Enterprise Service Busse (ESBs) die Ereignisweiterleitung. Das Paradigma wurde in den 2010er Jahren durch **Apache Kafka** (LinkedIn, 2011) und **RabbitMQ** (AMQP) revolutioniert, die hochdurchsatzfähiges Ereignis‑Streaming für Microservices ermöglichten. Heute abstrahieren cloudnative Dienste (AWS EventBridge, Azure Event Grid, GCP Pub/Sub) den Vermittler vollständig und machen EDA für jedes Team zugänglich.

## Wann EDA nicht verwendet werden sollte

- Das System ist einfach und synchrone Anfrage‑Antwort ist ausreichend.
- Strenge Konsistenz und sofortiges Feedback sind erforderlich (z. B. Finanztransaktionsvalidierung).
- Dem Team fehlt Erfahrung mit asynchronen Debugging‑ und Überwachungswerkzeugen.

## Weiterführende Ressourcen

- [CloudEvents Specification](https://cloudevents.io/) – Standard‑Ereignisformat für Interoperabilität.
- [Confluent Documentation](https://docs.confluent.io/) – Kafka‑Deep‑Dive, Schema Registry, Connectoren.
- [RabbitMQ Tutorials](https://www.rabbitmq.com/getstarted.html) – Schritt‑für‑Schritt für verschiedene Sprachen.
- [Martin Fowler – Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) – Klassischer Artikel zum Muster.

---

*Diese Seite ist ein lebendiges Dokument. Feedback und Beiträge sind willkommen.*