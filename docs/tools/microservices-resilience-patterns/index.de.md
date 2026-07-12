---
title: Muster der Resilienz für Mikrodienste
description: Techniken zur Sicherstellung von Stabilität und Fehlertoleranz in Mikrodienstarchitekturen.
created: 2026-07-12
tags:
  - mikrodienste
  - Resilienz
  - Muster
  - Fehlertoleranz
status: Entwurf
---

# Muster der Resilienz für Mikrodienste

Mikrodienstarchitektur zerlegt ein Anwendungsprogramm in kleinere, unabhängig installierbare Dienste. Jedes Dienst ist für eine spezifische Geschäftslogik verantwortlich und kommuniziert mit anderen Diensten über präzis definierte APIs. Diese Architektur stellt jedoch neue Herausforderungen bei der Dienst-zu-Dienst-Kommunikation dar, insbesondere in Bezug auf die Resilienz und die Fehlertoleranz. Resilienzmuster sind Entwurfsmuster, die helfen, die Robustheit und Zuverlässigkeit mikrodienstbasierter Anwendungen sicherzustellen.

## Schlüsselmerkmale der Muster der Resilienz für Mikrodienste

1. **Dezentraler Kontrolle**: Dienste werden nicht zentral verwaltet, was es schwierig macht, Fehlertypen zu handhaben.
2. **Asynchrone Kommunikation**: Dienste kommunizieren über asynchrone Nachrichten, was zu Verzögerungen und Unsicherheiten führen kann.
3. **Dienstisolierung**: Ein Fehlschlag eines einzelnen Dienstes sollte die Stabilität anderer Dienste nicht beeinträchtigen.
4. **Fehlertoleranz**: Das System muss funktionieren, auch wenn Teile davon fehlschlagen.

## Allgemeine Muster der Resilienz für Mikrodienste

### 1. Bulkhead-Muster

- **Beschreibung**: Das Bulkhead-Muster wird verwendet, um den Schaden zu begrenzen, wenn ein Dienst versagt, indem es verhindert, dass der Fehlschlag in andere Dienste wegfährt.
- **Schlüsselmerkmale**: Dienstisolierung, Schaltkreisschneider und Timeout.
- **Implementierung**: Verwenden Sie einen Schaltkreisschneider, um den fehlerhaften Dienst zu isolieren und weitere Anforderungen zu verhindern, bis der Dienst wiederhergestellt ist.
- **Anwendungsbereiche**: Datenbankfehler, Versagen von Drittanbieterdiensten, Netzwerkunterbrechungen.
- **Basisdienst**: Implementieren Sie einen Timeout für entfernte Dienstaufrufe und verwenden Sie einen Schaltkreisschneider, um die Anforderungen an den Dienst nicht zu übertreiben.

### 2. Schaltkreisschneider-Muster

- **Beschreibung**: Das Schaltkreisschneider-Muster ist ein Strategie, um den Dienst vor Überragung durch einen Drittanbieterdienst zu schützen.
- **Schlüsselmerkmale**: Überwachung, Schwellenwert, offener/geschlossener Zustand.
- **Implementierung**: Überwachen Sie die Erfolgswahrscheinlichkeit eines entfernten Dienstes und öffnen Sie den Schaltkreis, wenn die Erfolgswahrscheinlichkeit unter einem Schwellenwert fällt.
- **Anwendungsbereiche**: API-Fehler, Datenbankfehler, Netzwerkprobleme.
- **Basisdienst**: Legen Sie einen Schwellenwert für die Anzahl der fehlgeschlagenen Anfragen fest, bevor Sie den Schaltkreis öffnen, und stoppen Sie die Anfragen an den entfernten Dienst. Sobald der Dienst wiederhergestellt ist, schließen Sie den Schaltkreis.

### 3. Fallback-Muster

- **Beschreibung**: Das Fallback-Muster bietet eine Standardantwort, wenn der entfernte Dienst versagt.
- **Schlüsselmerkmale**: Standardantwort, Caching.
- **Implementierung**: Geben Sie eine abgelegte oder vordefinierte Antwort zurück, wenn der entfernte Dienst versagt.
- **Anwendungsbereiche**: Datenbankfehler, Netzwerkunterbrechungen.
- **Basisdienst**: Cache die Antwort des entfernten Dienstes oder geben Sie eine Standardantwort zurück, wenn der Dienst nicht verfügbar ist.

### 4. Resiliente Wiederholungsmuster

- **Beschreibung**: Das resilienten Wiederholungsmuster versucht, einen fehlgeschlagenen Anfragen nach einem Zeitverzögerung wiederzuführen.
- **Schlüsselmerkmale**: Exponentielles Verzögern, Verzerrung, Wiederholungen.
- **Implementierung**: Wiederhole die Anfrage nach einem Zeitverzögerung, das exponentiell mit jeder Wiederholung wächst, und füge eine Zufallsverzerrung hinzu, um das Thundering Herd-Problem zu vermeiden.
- **Anwendungsbereiche**: Netzwerkprobleme, temporäre Datenbank-Sperren.
- **Basisdienst**: Implementieren Sie ein Wiederholungsprotokoll, das die Anfrage nach einer Zeitverzögerung wiederholt, und wenn die Anfrage fehlschlägt, steigern Sie die Verzögerung exponentiell und fügen Sie Zufallsverzerrung hinzu.

### 5. Lastabgabe-Muster

- **Beschreibung**: Das Lastabgabe-Muster reduziert die Last auf einen Dienst durch das Abschleppen oder Verzögern von Anfragen.
- **Schlüsselmerkmale**: Verlagerung, Warteschlange.
- **Implementierung**: Verwenden Sie ein Warteschlangensystem, um eingehende Anfragen zu verwalten und Anfragen zu abschleppen oder zu verzögern, wenn der Dienst unter schwerer Last steht.
- **Anwendungsbereiche**: hohe Verkehr, Dienstüberlastung.
- **Basisdienst**: Implementieren Sie ein Warteschlangensystem, das eingehende Anfragen verwalten und Anfragen abschleppen oder verzögern, wenn der Dienst überlastet ist.

### 6. Bulkheads und Schaltkreisschneider kombiniert

- **Beschreibung**: Die Kombination von Bulkheads und Schaltkreisschneidern bietet eine robuste Lösung für Mikrodienste.
- **Schlüsselmerkmale**: Dienstisolierung, Fehlertoleranz.
- **Implementierung**: Verwenden Sie Bulkheads, um Dienste zu isolieren, und Schaltkreisschneider, um den Fehlschlag eines einzelnen Dienstes zu verhindern, dass er andere Dienste beeinträchtigt.
- **Anwendungsbereiche**: komplexe Mikrodienstarchitekturen, kritische Systeme.
- **Basisdienst**: Implementieren Sie sowohl Bulkheads als auch Schaltkreisschneider, um sicherzustellen, dass ein Fehlschlag eines einzelnen Dienstes die Stabilität anderer Dienste nicht beeinträchtigt.

## Installation und Basisdienst

### Installation

1. **Schaltkreisschneider**:
   - **Bibliotheken**: Spring Cloud Netflix Hystrix, Resilience4j, Netflix Ribbon.
   - **Beispiel (Spring Cloud Hystrix)**:
     ```java
     @Autowired
     private HystrixCommand.Setter setter;
     
     @HystrixCommand(fallbackMethod = "fallbackMethod")
     public String getResponse() {
         // Remote Service Aufruf
     }
     
     public String fallbackMethod() {
         return "Fallback Response";
     }
     ```

2. **Bulkhead**:
   - **Bibliotheken**: Resilience4j, Hystrix.
   - **Beispiel (Resilience4j)**:
     ```java
     @Autowired
     private RateLimiter rateLimiter;
     
     @Override
     public String fetchSomeData() {
         return rateLimiter.executeWithRateLimiter(() -> remoteService.getData(), 5);
     }
     ```

### Basisdienst

1. **Schaltkreisschneider**:
   - Konfigurieren Sie den Schaltkreisschneider, um die Erfolgswahrscheinlichkeit der entfernten Dienste zu überwachen und den Schaltkreis zu öffnen, wenn die Erfolgswahrscheinlichkeit unter einem bestimmten Schwellenwert fällt.
   - Implementieren Sie eine Standardantwort, um eine Standardantwort zurückzugeben, wenn der entfernte Dienst nicht verfügbar ist.

2. **Bulkhead**:
   - Setzen Sie einen Bulkhead ein, um die entfernten Dienstaufrufe zu isolieren und die Anzahl der parallelen Anfragen zu begrenzen.
   - Verwenden Sie ein Warteschlangensystem, um eingehende Anfragen zu verwalten und Anfragen zu abschleppen oder zu verzögern, wenn der Dienst unter schwerer Last steht.

## Zusammenfassung

Resilienzmuster sind für die Entwicklung zuverlässiger und robuster Mikrodienst-Anwendungen wesentlich. Durch das Implementieren dieser Muster können Sie sicherstellen, dass Ihre Mikrodienste fehlerhaftes Verhalten aushalten können und auch in Gegenwart von Fehlern hoch verfügbar bleiben. Die Wahl des Musters hängt von den spezifischen Anforderungen Ihrer Anwendung und der Art der beteiligten Dienste ab.