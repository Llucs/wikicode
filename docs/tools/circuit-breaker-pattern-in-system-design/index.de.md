---
title: Circuit Breaker Pattern in Systemdesign
description: Ein Mechanismus, um Verschlagwortungen von Fehlern in einer verteiltensystem von einer anderen zu verhindern, um die Gesamtreliabilität und Stabilität des Systems zu verbessern.
created: 2026-07-06
tags:
  - Systemdesign
  - Mikroservices
  - Resilienz
  - Fehlerdauersicherheit
status: Entwurf
---

# Circuit Breaker Pattern in Systemdesign

Das Circuit Breaker Pattern ist ein Entwurfsmuster, das in der Softwareentwicklung verwendet wird, um Verschlagwortungen von Fehlern in verteilter Systeme zu verhindern. Es dient als Kontrollmechanismus, der die Erfolg oder Versagenszustand von entfernten Operationen überwacht und das Verhalten des Systems ändert, wenn Versagungen einen bestimmten Schwellenwert überschreiten. Wenn der Circuit Breaker "aufgegangen" ist, stoppt er weitere Anfragen, die an den unteren Dienst weitergeleitet werden, und gibt stattdessen eine vorgefertigte Antwort an den Client zurück. Sobald der Dienst in einen stabilen Zustand zurückkehrt, kann der Circuit Breaker "zugeschlagen" werden, um die Systeme auf einen Versuchsversuch zu erlauben.

## Schlüsselmerkmale

1. **Erkennung von Dienstunverfügbarkeit**: Der Circuit Breaker überwacht den Zustand von abhängigen Diensten oder Komponenten. Wenn eine bestimmte Anzahl von Fehlern innerhalb einer bestimmten Zeitspanne auftritt, springt der Circuit Breaker aus.
2. **Rückgangsmechanismus**: Wenn der Circuit Breaker aufgegangen ist, bietet er ein Rückgangsmechanismus, der eine vorgefertigte Antwort an den Client zurückgibt, um die volle Versagung der Anwendung zu vermeiden.
3. **Verzögerte Wiederholungen**: Anstelle sofortiger Wiederholungen von fehlgeschlagenen Anfragen, ermöglicht der Circuit Breaker eine Verzögerung, die es dem System bei der Wiederherstellung von vorübergehenden Problemen hilft.
4. **Circuit Breaker Zustand**: Der Circuit Breaker hält einen Zustand (aufgegangen/zugeschlagen) und wechselt zwischen Zuständen basierend auf dem Erfolg oder Versagen des Dienstes.

## Installation und Setup

Die spezifische Implementierung des Circuit Breaker Patterns kann von der verwendeten Programmiersprache und dem Framework abhängen. Hier ist ein grundlegender Setup mit einer beliebten Java-Bibliothek namens Hystrix.

### Abhängigkeiten hinzufügen

Für Maven fügen Sie die Hystrix-Bibliothek in Ihr Projekt ein:

```xml
<dependency>
    <groupId>com.netflix.hystrix</groupId>
    <artifactId>hystrix-javanica</artifactId>
    <version>1.5.18</version>
</dependency>
```

### Ein Kommando erstellen

Definieren Sie ein Hystrix-Kommando für den Dienst, den Sie schützen möchten.

```java
import com.netflix.hystrix.HystrixCommand;
import com.netflix.hystrix.HystrixCommandGroupKey;

public class MeineDienstCommand extends HystrixCommand<String> {
    public MeineDienstCommand() {
        super(HystrixCommandGroupKey.Factory.asKey("MeineDienstGroup"));
    }

    @Override
    protected String run() throws Exception {
        // Den Dienst oder die Operation aufrufen
        return this.callService();
    }

    @Override
    protected String getFallback() {
        return "Rückgabeargument";
    }
}
```

### Das Kommando ausführen

Verwenden Sie das Kommando, um die Dienstaufrufe auszuführen.

```java
MeineDienstCommand command = new MeineDienstCommand();
String result = command.execute();
```

## Grundlegendes Verwenden

1. **Initialisierung**: Erstellen Sie ein Beispiel des Hystrix-Kommandos.
2. **Ausführung**: Verwenden Sie die `execute`-Methode, um das Kommando auszuführen. Wenn der Dienst nicht verfügbar ist, wird das Rückgangsmethode aufgerufen.
3. **Rückgangsmethode**: Definieren Sie eine Rückgangsmethode, die eine vorgefertigte Antwort zurückgibt.

```java
@Override
protected String run() throws Exception {
    // Den Dienst oder die Operation aufrufen
    return this.callService();
}

@Override
protected String getFallback() {
    return "Rückgabeargument";
}
```

4. **Überwachung**: Verwenden Sie den Hystrix-Dashboard, um die Ausführungsstatistiken und Gesundheitszustände Ihrer Kommandos zu überwachen.

## Anwendungsfälle

1. **Mikroservices-Kommunikation**: In Mikroservices-Architekturen, bei der Dienste miteinander kommunizieren, verhindert das Circuit Breaker Pattern eine Verschlagwortung von Fehlern in einem Dienst, die in andere Dienste umschwingt.
2. **API Gateway**: Wenn ein API Gateway den Zugriff auf mehrere Dienste verwaltet, verhindert das Circuit Breaker Pattern Verschlagwortungen in einem Dienst, die die gesamte API beeinträchtigen.
3. **Drittanbieterdienste**: Beim Integrieren mit Drittanbieterservices oder externen APIs hilft das Circuit Breaker Pattern, vorübergehende Verschlagwortungen elegant zu behandeln.
4. **Datenbankzugriff**: In Datenbankinteraktionen verhindert das Muster Verschlagwortungen aufgrund von vorübergehenden Verbindungsproblemen oder Datenbanküberlastungen.

## Fazit

Das Circuit Breaker Pattern ist ein mächtiges Instrument zur Verwaltung von Fehlern in verteilter Systeme, um zu gewährleisten, dass Verschlagwortungen in einem Teil des Systems nicht das gesamte System herunterfahren. Durch die Implementierung dieses Musters können Entwickler resilientere und skalablichere Anwendungen erstellen.

---