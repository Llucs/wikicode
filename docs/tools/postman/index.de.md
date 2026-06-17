---
title: Postman - API-Entwicklungs- und Testplattform
description: Ein umfassender Leitfaden zu Postman, der branchenüblichen API-Plattform zum Entwerfen, Erstellen, Testen und Dokumentieren von APIs.
created: 2026-06-15
tags:
  - postman
  - api-testing
  - api-development
  - collaboration
  - newman
status: draft
ecosystem: api
---

# Postman - API-Entwicklungs- und Testplattform

## Was ist Postman?

Postman ist eine vollständige API-Plattform, die jeden Schritt des API-Lebenszyklus vereinfacht – vom Entwurf und der Entwicklung bis hin zu Tests, Dokumentation und Überwachung. Ursprünglich als einfacher HTTP-Client gestartet, hat es sich zu einer kollaborativen Umgebung entwickelt, die von Millionen von Entwicklern und QA-Ingenieuren weltweit genutzt wird. Postman unterstützt die Protokolle REST, GraphQL und SOAP und bietet eine umfangreiche Reihe von Tools zum effizienten Erstellen und Arbeiten mit APIs.

## Warum Postman verwenden?

- **Umfassender HTTP-Client:** Einfaches Senden von Anfragen beliebiger Methoden, Anpassen von Headern, Authentifizierung und Body-Inhalten.
- **Organisatorische Werkzeuge:** Gruppieren Sie Anfragen in Collections, verwalten Sie Variablen mit Environments und verwenden Sie Daten über einen gesamten Arbeitsbereich wieder.
- **Scripting & Testing:** Schreiben Sie JavaScript-Testskripte, um Assertionen zu automatisieren, Daten zwischen Anfragen zu extrahieren und dynamische Arbeitsabläufe zu handhaben.
- **Automatisierungsbereit:** Verwenden Sie den Collection Runner für manuelle Ausführungen oder Newman für Headless-Ausführung (CI/CD, Pipelines).
- **Zusammenarbeit:** Teilen Sie Collections und Environments über Cloud-Workspaces mit Versionskontrolle und Kommentierungsmöglichkeiten.
- **Dokumentation & Mocking:** Automatische Generierung von API-Dokumentationen und Mock-Servern, um API-Antworten zu simulieren, bevor das Backend bereit ist.
- **Monitoring:** Richten Sie Monitore ein, um Collection-Durchläufe zu planen und die API-Gesundheit zu überprüfen.

## Installation

### Desktop-App (Empfohlen)

Postman bietet native Desktop-Apps für Windows, macOS und Linux.

- Laden Sie den passenden Installer von [getpostman.com](https://getpostman.com) herunter
- Alternativ nutzen Sie die **Webversion** unter [go.postman.co](https://go.postman.co) mit dem Desktop Agent, um API-Aufrufe zu verarbeiten.

### Newman (CLI für CI/CD)

Newman ist der Befehlszeilen-Collection-Runner für Postman. Er ermöglicht es Ihnen, eine Postman-Collection direkt von der Befehlszeile aus auszuführen und zu testen, was ihn ideal für die Integration von API-Tests in Ihre Entwicklungspipeline macht.

Installation über npm:

```bash
npm install -g newman
```

Oder mit Yarn:

```bash
yarn global add newman
```

## Grundlegende Nutzung

1. **Eine Anfrage erstellen**  
   Klicken Sie auf die Schaltfläche **New** und wählen Sie **HTTP Request** (oder verwenden Sie `Ctrl+N`).

2. **Die Anfrage spezifizieren**  
   - Geben Sie die URL ein (z.B. `https://jsonplaceholder.typicode.com/posts`)  
   - Wählen Sie die HTTP-Methode (`GET`, `POST`, `PUT`, etc.)  
   - Fügen Sie alle erforderlichen Header, Query-Parameter oder den Request-Body hinzu.

3. **Senden und inspizieren**  
   Klicken Sie auf **Send**. Der Antwortbereich zeigt den Statuscode, die Antwortzeit, Header und Body an.

4. **In einer Collection speichern**  
   Klicken Sie auf **Save** und erstellen Sie entweder eine neue Collection oder fügen Sie sie zu einer bestehenden hinzu.

5. **Einen Test hinzufügen**  
   Schreiben Sie unter dem Tab **Tests** ein JavaScript-Skript, um die Antwort zu validieren. Beispiel:

   ```javascript
   pm.test("Response status code is 200", function () {
       pm.response.to.have.status(200);
   });
   ```

   Führen Sie die Anfrage erneut aus – das Testergebnis erscheint im Tab **Test Results**.

## Hauptfunktionen mit Beispielen

### 1. Collections

Collections helfen Ihnen, zusammengehörige Anfragen zu gruppieren und mit Ihrem Team zu teilen. Eine Collection kann auch Ordner und Metadaten enthalten.

```javascript
// Example of using collection variables in a pre-request script
pm.collectionVariables.set("baseUrl", "https://api.example.com");
```

Führen Sie eine gesamte Collection mit Newman aus:

```bash
newman run MyCollection.json
```

### 2. Environments

Environments enthalten Schlüssel-Wert-Paare für Variablen, die sich zwischen den Setups ändern (Development, Staging, Production).

```json
{
  "base_url": "https://dev-api.example.com",
  "api_key": "abc123"
}
```

Verwenden Sie `{{base_url}}` in Ihren Anfrage-URLs. Wechseln Sie zwischen Environments, um sofort den Kontext zu ändern.

### 3. Pre-Request- und Test-Skripte

Postman-Skripte werden in JavaScript geschrieben und laufen in einer Sandbox mit Zugriff auf von Postman bereitgestellte Objekte wie `pm`.

**Pre-Request-Skript** (wird ausgeführt, bevor die Anfrage gesendet wird):

```javascript
// Dynamically set a timestamp parameter
pm.variables.set("timestamp", Date.now());
```

**Test-Skript** (wird ausgeführt, nachdem die Antwort empfangen wurde):

```javascript
pm.test("Response time is less than 2000ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

pm.test("Body contains expected user", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData[0].name).to.eql("Leanne Graham");
});
```

### 4. Collection Runner

Führen Sie eine gesamte Collection oder einen Ordner mehrmals mit Datendateien aus.

- Öffnen Sie **Runner** oben links in Postman.
- Wählen Sie eine Collection, ein Environment aus und legen Sie Iterationen fest.
- Sie können eine CSV- oder JSON-Datendatei bereitstellen, um Daten in jede Iteration einzufügen.

### 5. Newman – Befehlszeilenintegration

Newman ermöglicht es Ihnen, Ihre Postman-Tests in CI/CD-Pipelines (Jenkins, GitLab CI, GitHub Actions, etc.) zu integrieren.

**Eine Collection mit einem Environment und einer Datendatei ausführen:**

```bash
newman run MyCollection.json \
  --environment staging.json \
  --iteration-data test-data.csv \
  --reporters cli,htmlextra
```

Der Reporter `htmlextra` generiert einen interaktiven HTML-Bericht des Testdurchlaufs.

**Verwendung in einem Node.js-Skript:**

```javascript
const newman = require('newman');

newman.run({
    collection: require('./MyCollection.json'),
    environment: require('./staging.json'),
    reporters: 'cli'
}, function (err, summary) {
    if (err) { throw err; }
    console.log('Collection run completed!');
    console.log(summary.run.stats);
});
```

### 6. Dokumentationsgenerierung

Postman kann automatisch Dokumentation für jede Collection generieren. Öffnen Sie einfach eine Collection, klicken Sie auf das **...**-Menü und wählen Sie **View documentation**. Die Dokumentation enthält Beispielanfragen, Request/Response-Schemas und Code-Snippets in verschiedenen Sprachen.

Veröffentlichen Sie die Dokumentation über die Schaltfläche **Publish Docs** im Web oder exportieren Sie sie als HTML.

### 7. Mock-Server

Imitieren Sie eine API, indem Sie einen Mock-Server aus Ihrer Collection erstellen. Dies ist äußerst nützlich für die Frontend-Entwicklung, wenn das Backend noch nicht bereit ist.

- Wählen Sie eine Collection aus, klicken Sie auf **Mock Servers**.
- Postman erstellt eine Mock-Server-URL, die die gespeicherten Beispielantworten zurückgibt.

### 8. Monitors

Monitore erlauben es Ihnen, periodische Durchläufe einer Collection auf der Cloud-Infrastruktur von Postman zu planen. Sie erhalten Benachrichtigungen, wenn Tests fehlschlagen.

- Gehen Sie zu **Monitors** → **Create a monitor**.
- Wählen Sie eine Collection aus, legen Sie eine Häufigkeit fest (z.B. jede Stunde) und definieren Sie optional Alarme (E-Mail, Slack, etc.).

## Zusammenfassung

Postman ist viel mehr als ein API-Client – es ist eine vollwertige Plattform, die den gesamten API-Lebenszyklus unterstützt. Vom anfänglichen Mocking und kollaborativen Design bis hin zu automatisierten Tests über Newman und Produktionsüberwachung stattet Postman Teams mit einer einzigen Quelle der Wahrheit für ihre APIs aus. Seine Benutzerfreundlichkeit, kombiniert mit leistungsstarken Skriptfunktionen und CI/CD-Integration, macht es zu einem unverzichtbaren Werkzeug für moderne Entwicklungsabläufe.