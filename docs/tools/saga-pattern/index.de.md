---
title: Saga-Mode
description: Ein Entwurfsmuster zur Verwaltung von verteilt über mehrere Dienste oder Ressourcen in Mikrodienstarchitekturen erfolgender Transaktionen.
created: 2026-07-09
tags:
  - Mikrodienste
  - verteilt über mehrere Dienste
  - Entwurfsmuster
  - Saga-Mode
status: Entwurf
---

# Saga-Mode

## Übersicht

Der Saga-Mode ist ein Entwurfsmuster, das in verteilten Systemen zum Verwalten von Transaktionen über mehrere Dienste oder Ressourcen verwendet wird. Es gewährleistet die Konsistenz und Zuverlässigkeit von Operationen durch das Wartung einer Folge von Operationen, die erfolgreich durchgeführt werden müssen, damit die Transaktion als gültig angesehen wird. Wenn eine Operation fehlschlägt, ermöglicht das Muster das Rollback aller durchgeführten Operationen, um die Integrität des Systems zu gewährleisten.

## Hauptmerkmale

1. **Compensierende Operationen**: Zu jeder Einheit von Arbeit (Operation) wird eine entsprechende compensierende Operation definiert, die die Änderungen durch die Einheit von Arbeit rückgängig macht. Dies stellt sicher, dass bei Fehlschlag einer Operation das System in seinen vorherigen Zustand zurückkehren kann.
2. **Sequenzielle Ausführung**: Operationen werden in einer spezifischen Reihenfolge ausgeführt, und jede Operation hängt von der erfolgreichen Ausführung der vorherigen Operation ab.
3. **Endgültige Konsistenz**: Das Muster stellt sicher, dass das System sich über die Zeit hinweg auf einen konsistenten Zustand bewegt, selbst wenn einzelne Transaktionen fehlschlagen.
4. **Idempotenz**: Operationen innerhalb einer Saga sollten idempotent sein, um sicherzustellen, dass der Zustand des Systems nicht verändert wird, wenn die gleiche Operation mehrmals aufgerufen wird.

## Geschichte

Der Saga-Mode wurde entwickelt, um die Herausforderungen des Verwaltens von Transaktionen in Mikrodienstarchitekturen zu bewältigen. Vor dem Aufkommen von Mikrodiensten verwalteten monolithische Anwendungen Transaktionen im Datenbankkontext. Mit der zunehmenden Verbreitung von Anwendungen, die verteilt waren, wuchs die Komplexität der Transaktionenverwaltung über mehrere Dienste. Der Saga-Mode wurde als Lösung für diese Komplexitäten eingeführt.

Der Begriff Sagas kann bis in die 1970er Jahre zurückverfolgt werden, als Jim Gray bei der Verarbeitung von Transaktionen arbeitete, aber er gewann im Kontext von Mikrodiensten und verteilten Systemen im Jahrzehnt der 2010er Jahre an Bedeutung.

## Nutzungskasus

1. **Finanzielle Transaktionen**: Die Verarbeitung von Transaktionen wie Überweisungen, Zahlungen und Rückführungen erfordert das sicherstellen, dass die Beträge zwischen Konten korrekt umgeteilt werden. Ein Saga kann diese Operationen verwalten, indem es sicherstellt, dass bei Fehlschlag einer Überweisung das ursprüngliche Gutsstand wiederhergestellt wird.
2. **Bestellung verarbeiten**: In E-Commerce-Bestellprozessen umfassen die Bestelloperationen mehrere Schritte, wie Produktreservierung, Bestandsanpassung und Kreditkartenabrechnung. Ein Saga kann sicherstellen, dass alle diese Operationen erfolgreich durchgeführt oder im Falle eines Fehlschlags zurückgezogen werden, um den Zustand des Systems zu erhalten.
3. **Gesundheitsversorgungssysteme**: In Gesundheitsversorgungssystemen erfordern Transaktionen wie Rechnungsstellung, Terminplanung und Arzneimittelspeicherung das sicherstellen, dass alle Schritte vollständig oder im Falle eines Fehlschlags zurückgezogen werden, um die Integrität der Patientendaten aufrechtzuerhalten.
4. **Versicherungsausschüttungen**: Die Verarbeitung von Versicherungsausschüttungen umfasst mehrere Schritte, wie Ausschüttungsverarbeitung, Zahlung und Dokumentendokumentation. Ein Saga kann diese Operationen verwalten, indem es sicherstellt, dass der Ausschuss korrekt verarbeitet wird oder im Falle eines Fehlschlags zurückgezogen wird.

## Installation und Setup

Der Saga-Mode wird normalerweise mit einer Kombination aus Anwendungsprogrammierung und Middleware-Diensten implementiert. Hier ist eine grundlegende Übersicht darüber, wie ein Saga eingerichtet werden kann:

1. **Definieren von Operationen**: Identifizieren Sie die Operationen, die Teil eines Sagas sind. Für jede Operation definieren Sie die entsprechende compensierende Aktion.
2. **Verwenden einer Nachrichtenbahn**: Implementieren Sie eine Nachrichtenbahn, um die Ausführung der Operationen zu verwalten. Dies kann ein Nachrichtenbroker wie RabbitMQ, Kafka oder AWS SQS sein.
3. **Saga-Manager**: Erstellen Sie einen Saga-Manager, der die Reihenfolge der Operationen orchestriert. Der Manager sollte die Ausführung der Operationen verwalten, den Zustand des Sagas zu verfolgen und bei Fehlern die Rücksatze-Logik zu verwaltung.
4. **Compensierende Aktionen**: Implementieren Sie die compensierenden Aktionen, die den Zustand des Systems in seinen vorherigen Zustand zurückverschieben, wenn eine Operation fehlschlägt.

### Grundlegende Verwendung

1. **Starten des Sagas**: Beginnen Sie den Saga durch das Initieren der ersten Operation in der Reihenfolge.
2. **Ausführen von Operationen**: Führen Sie jede Operation in der Reihenfolge aus. Wenn eine Operation fehlschlägt, sollte der Saga die Ausführung stoppen und die compensierenden Aktionen ausführen.
3. **Verfolgen des Zustands**: Wartung eines Zustands des Sagas, um den Fortschritt zu verfolgen und sicherzustellen, dass die Operationen im richtigen Reihenfolgen angezeigt werden.
4. **Compensieren**: Wenn eine Operation fehlschlägt, sollte der Saga die compensierenden Aktionen ausführen, um den Systemzustand in einen konsistenten Zustand zurückzuschieben.
5. **Abschluss des Sagas**: Wenn alle Operationen erfolgreich durchgeführt sind, kann der Saga als abgeschlossen markiert werden.

### Beispiel

Hier ist ein Python-Beispiel, das die grundlegende Struktur eines Sagas veranschaulicht, bei der Operationen in Reihe und Reihenfolge ausgestattet und compensierende Aktionen definiert werden, um Fehler zu behandeln:

```python
from queue import Queue

# Definieren von Operationen und compensierenden Aktionen
def create_product_reservation(product_id, quantity):
    # Implementierung zur Erstellung einer Produktreservierung
    pass

def update_inventory(product_id, quantity):
    # Implementierung zur Aktualisierung des Bestands
    pass

def charge_customer(customer_id, amount):
    # Implementierung zur Kreditkartenabrechnung
    pass

def cancel_reservation(product_id, quantity):
    # Implementierung zur Stornierung der Reservierung
    pass

def refund_customer(customer_id, amount):
    # Implementierung zur Rückzahlung des Kunden
    pass

# Definieren des Sagas
def process_order(saga_id, product_id, quantity, customer_id, amount):
    saga_queue = Queue()

    try:
        saga_queue.put(create_product_reservation(product_id, quantity))
        saga_queue.put(update_inventory(product_id, quantity))
        saga_queue.put(charge_customer(customer_id, amount))
        
        while not saga_queue.empty():
            operation = saga_queue.get()
            operation()
        
        # Markieren des Sagas als abgeschlossen
        print(f"Saga {saga_id} erfolgreich abgeschlossen.")
    except Exception as e:
        # Ausführen der compensierenden Aktionen
        while not saga_queue.empty():
            operation = saga_queue.get()
            operation()
        print(f"Saga {saga_id} fehlgeschlagen. Compensierende Aktionen ausgeführt.")
        
# Starten des Sagas
process_order(1, "P123", 10, "C12345", 100)
```

Dieses Beispiel zeigt die grundlegende Struktur eines Sagas, bei dem Operationen in Reihe und Reihenfolge ausgestattet sind, und compensierende Aktionen definiert werden, um Fehler zu behandeln.

## Zusammenfassung

Der Saga-Mode ist eine robuste Lösung zur Verwaltung von Transaktionen über mehrere Dienste in verteilten Systemen. Durch das Sicherstellen, dass Operationen in einer spezifischen Reihenfolge ausgeführt werden und compensierende Aktionen zur Behandlung von Fehlern definiert sind, hilft das Muster, die Integrität des Systems zu gewährleisten. Eine Verständnis des Saga-Modus ist für die Entwicklung zuverlässiger und skalierbarer Mikrodienstarchitekturen von entscheidender Bedeutung.