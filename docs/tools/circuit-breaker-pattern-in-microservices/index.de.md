---
title: Schaltkreisschalter-Modell in Mikrodienstarchitekturen
description: Ein Entwurfsmuster, das in Mikrodienstarchitekturen verwendet wird, um fehlerhafte Anfragen zu einem problematischen Dienst vorübergehend zu ignorieren und so die Widerstandsfähigkeit und Zuverlässigkeit verteilter Systeme zu steigern.
created: 2026-07-15
tags:
  - Mikrodienste
  - Widerstandsfähigkeit
  - Schaltkreisschalter
  - Entwurfsmuster
status: Entwurf
---

### Schaltkreisschalter-Modell in Mikrodienstarchitekturen

#### Was ist das Schaltkreisschalter-Modell?
Das Schaltkreisschalter-Modell ist ein Entwurfsmuster im Softwareengineering, das die Widerstandsfähigkeit und Zuverlässigkeit verteilter Systeme, insbesondere in Mikrodienstarchitekturen, verbessert. Es ist ein Mechanismus, um Fehlern bei entfernten Aufrufen entgegenzuwirken, indem Dienste schnell fehlerhaft werden und von Fehlern sich wieder erholen können, ohne dass es zu einem Kaskaden von Fehlern im System kommt.

#### Schlüsselmerkmale
1. **Fehlererkennung**: Der Schaltkreisschalter erkennt Fehlereinträge, wenn ein Dienst oder ein API-Aufruf fehlschlägt, indem er eine vordefinierte Schwellenwertzahl an Fehlern erreicht.
2. **Schaltkreisschaltung**: Wenn der Schwellenwert überschritten wird, schaltet der Schaltkreisschalter ab, indem er die Schaltkreisschaltung durch die Verhinderung von weiteren Anfragen an den fehlerhaften Dienst bricht.
3. **Fehlerbehandlungsmechanismus**: Stattdessen, als obwartete man eine möglicherweise fehlerhafte Antwort des Dienstes, schaltet der Schaltkreisschalter einen Fehlerbehandlungsmechanismus ein, der eine vordefinierte Antwort oder eine Fehlermeldung an den Aufrufer zurückgibt.
4. **Timeouts und Wiedergäbe**: Der Schaltkreisschalter kann konfiguriert werden, um einen Timeout und einen Wiedergabemechanismus für vorübergehende Fehlereinträge einzuführen.
5. **Schaltkreisschaltung zurücksetzen**: Sobald der Dienst wieder korrekt funktioniert, setzt der Schaltkreisschalter zurück und ermöglicht es, Anfragen erneut an den Dienst zu senden.

#### Geschichte
Der Begriff des Schaltkreisschalters wurde zuerst im Bereich der Elektrotechnik und der Hardware eingeführt. Er wurde später in das Softwareengineering adaptiert, insbesondere in den Kontext verteilter Systeme, von Martin Fowler und James Lewis in ihrem 2010 erschienenen Artikel „Microservices: Designing Fine-Grained Services“, der auf ihrer Website MartinFowler.com veröffentlicht wurde.

#### Einsatzfälle
1. **Behandlung von Dienstunterbrechungen**: In einer Mikrodienstarchitektur verhindert der Schaltkreisschalter, dass andere Dienste versuchen, sich mit einem fehlerhaften Dienst zu kommunizieren, um eine Kaskade von Fehlern zu vermeiden.
2. **Performanzoptimierung**: Durch das Schalten des Schaltkreisschalters verhindert man unnötiges Verarbeiten und verbessert die Gesamtleistung des Systems.
3. **Fehlerbehandlung**: Es bietet eine Mechanismus, um Fehler elegant zu behandeln, was die Auswirkungen von Fehlern auf das gesamte System reduziert.
4. **Realzeitüberwachung**: Der Schaltkreisschalter kann zur Überwachung der Gesundheit der Dienste und zur Bereitstellung von realzeitlichen Informationen über den Zustand des Systems verwendet werden.

#### Installation
Das Schaltkreisschalter-Modell kann mit verschiedenen Bibliotheken und Frameworks implementiert werden, abhängig von der verwendeten Programmiersprache und dem verwendeten Framework. Hier sind einige allgemeine Implementierungen:

- **Java**: Hystrix (von Netflix), Resilience4j, OpenHystrix.
- **.NET**: Polly.
- **Python**: CircuitBreaker.
- **JavaScript**: @liarnp/circuitbreaker.

Beispielsweise die Implementierung mit Resilience4j in Java:

```java
import io.github.resilience4j.circuitbreaker.CircuitBreaker;
import io.github.resilience4j.circuitbreaker.CircuitBreakerRegistry;

public class CircuitBreakerExample {
    private final CircuitBreakerRegistry circuitBreakerRegistry;
    private final CircuitBreaker circuitBreaker;

    public CircuitBreakerExample() {
        circuitBreakerRegistry = CircuitBreakerRegistry.of("exampleCircuitBreaker");
        circuitBreaker = circuitBreakerRegistry.circuitBreaker("exampleCircuitBreaker");
    }

    public void performCall() {
        if (circuitBreaker.isOpen()) {
            System.out.println("Schaltkreisschalter ist offen, Fehlerbehandlungsmechanismus aktiv...");
            return;
        }
        try {
            // Ausführen des Aufrufs zum Dienst
        } catch (Exception e) {
            circuitBreakerRegistry.fail(CircuitBreaker.of("exampleCircuitBreaker"));
        }
    }
}
```

#### Grundlegender Einsatz
1. **Initialisierung**: Initialisieren Sie den Schaltkreisschalter mit der gewünschten Konfiguration und registrieren Sie ihn im Schaltkreisschalter-Registry.
2. **Einsatz**: Verwenden Sie den Schaltkreisschalter, um den Dienstaufruf einzuschließen. Bei einem fehlerhaften Aufruf wird der Schaltkreisschalter die Schaltkreisschaltung durchbrechen, und nachfolgende Aufrufe verwenden den Fehlerbehandlungsmechanismus.
3. **Zurücksetzen**: Lassen Sie den Schaltkreisschalter sich selbst zurücksetzen, wenn der Dienst wieder korrekt funktioniert.

Indem das Schaltkreisschalter-Modell implementiert wird, können Entwickler die Widerstandsfähigkeit und Zuverlässigkeit ihrer Mikrodienste verbessern, sodass das System fehlerhaft eleganter umgeht und eine hohe Verfügbarkeit gewährleistet.