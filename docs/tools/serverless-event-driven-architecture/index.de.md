---
title: Serverlose Ereignisgetriebene Architektur
description: Ein Muster, bei dem Anwendungen auf Ereignisse reagieren und sich automatisch skalieren, ohne die Infrastruktur zu verwalten, ideal für cloud-native Dienste.
created: 2026-07-22
tags:
  - serverless
  - ereignisgetrieben
  - architecture
status: draft
---

# Serverlose Ereignisgetriebene Architektur

## Einführung

Die Serverlose Ereignisgetriebene Architektur (SEDA) ist ein Entwurfsparadigma, das es Anwendungen ermöglicht, mit einer Menge von lückenfüllenden Funktionen aufzubauen, die in Reaktion auf Ereignisse ausführen, ohne dass der Entwickler der Anwendung die Infrastruktur verwalten und einrichten muss. Diese Ansätze ermöglichen Entwicklern, skalierbare, hochverfügbare und kosteneffiziente Anwendungen zu bauen, indem sie sich ausschließlich auf den Code konzentrieren, der den Geschäftslogik umfasst.

## Hauptmerkmale

1. **Decoupled Functions**: Funktionen sind statiell und isoliert, was es ermöglicht, sie unabhängig von der Nachfrage zu skalieren.
2. **Ereignisgetrieben**: Funktionen werden durch Ereignisse wie API-Anfragen, Datenbankaktualisierungen oder externe Dienste ausgelöst.
3. **Automatische Skalierung**: Der Plattform wird die Anzahl der Instanzen einer Funktion basierend auf der Nachfrage automatisch skaliert.
4. **Pay-As-You-Go**: Nur für die genutzten Ressourcen bezahlt werden, wenn die Funktionen ausgeführt werden, was zu Kosteneinsparungen führt.
5. **Statiell**: Jeder Funktionsaufruf ist unabhängig, und die Daten werden von externen Diensten wie Datenbanken oder Speichermanagement verwaltet.
6. **Skalierbar**: Funktionen können basierend auf dem Lastverteilung automatisch skaliert werden.

## Geschichte

Das Konzept der serverlosen Berechnung hat seine Wurzeln in der Cloud-Berechnung und der Evolution von Infrastruktur als Dienst (IaaS) und Plattform als Dienst (PaaS). Der Begriff "serverlos" wurde durch Anhänger wie AWS Lambda im Jahr 2014 populär gemacht. AWS Lambda war der erste bedeutende Cloud-Anbieter, der eine vollständig verwaltete, serverlose Berechnungs-Dienst-Angebotsart anbot. Seitdem haben andere Cloud-Anbieter wie Google Cloud Functions, Azure Functions und Alibaba Cloud Functions ähnliche Dienste eingeführt.

## Einsatzbereiche

1. **Web- und Mobile-Apps**: Behandeln von Benutzerinteraktionen, Datenverarbeitung und Hintergrundaufgaben.
2. **API-Gateways**: Routing und Verwaltung von API-Anfragen.
3. **IoT**: Verarbeiten von Daten von Sensoren und Geräten.
4. **Datenverarbeitung**: Echtzeit-Datenverarbeitung, Logverarbeitung und Analysen.
5. **Automatisierung**: Automatisierung von Workflows und Prozessen in einer skalierbaren Weise.
6. **Inhaltserstellung**: Bereitstellen von Inhalten basierend auf Benutzereingaben, wie Bilder oder Videos.

## Installation

Die Installation einer serverlosen Ereignisgetriebenen Architektur umfasst typischerweise das Einrichten eines Cloud-Anbieterserverlosen Plattforms, wie AWS Lambda oder Azure Functions. Hier ist ein allgemeines Handbuch:

1. **Erstellen eines Kontos**: Registrieren Sie sich für eine Cloud-Anbieterservicen.
2. **Einrichten einer Umgebung**: Installieren Sie die notwendigen SDKs und Tools, wie die AWS CLI oder Azure CLI.
3. **Initialisieren des Projekts**: Verwenden Sie die Cloud-Anbieter-CLI-Tools, um ein neues serverloses Projekt zu initialisieren.
4. **Konfigurieren der Funktionen**: Schreiben und konfigurieren Sie Ihre Funktionen. Dies umfasst das Festlegen von Auslösern und Ereignissourcematerialien.
5. **Bereitstellen der Funktionen**: Bereiten Sie Ihre Funktionen im Cloud-Anbieterserverlosen Umgebung.
6. **Testen der Funktionen**: Testen Sie die Funktionen, um sicherzustellen, dass sie korrekt funktionieren.

### Beispiel: AWS Lambda Einrichtung

1. **Erstellen eines AWS-Kontos** und Anmelden.
2. **Installieren der AWS CLI**: Stellen Sie sicher, dass die AWS CLI installiert und konfiguriert ist.
3. **Initialisieren eines Serverless-Projekts**:

   ```bash
   serverless create --template aws-nodejs --path my-lambda-project
   cd my-lambda-project
   ```

4. **Konfigurieren der Funktion**: Bearbeiten Sie `handler.js`, um Ihre Geschäftslogik hinzuzufügen.

   ```javascript
   exports.handler = (event, context, callback) => {
     const message = event.message;
     const response = {
       statusCode: 200,
       body: JSON.stringify({ message: `Processed: ${message}` }),
     };
     callback(null, response);
   };
   ```

5. **Bereitstellen der Funktion**:

   ```bash
   serverless deploy
   ```

6. **Testen der Funktion**: Verwenden Sie das AWS Lambda-Console oder das API Gateway, um die Funktion zu testen.

## Basisbenutzung

1. **Auslösen der Funktion**: Funktionen werden durch Ereignisse ausgelöst. Zum Beispiel in AWS Lambda können Funktionen über API Gateway, geplante Ereignisse oder S3-Ereignisse ausgelöst werden.
2. **Schreiben der Funktionscode**: Verwenden Sie das bevorzugte Programmiersprache (z.B. Node.js, Python) zur Schreibung der Geschäftslogik. Hier ist ein einfaches Beispiel in Python unter AWS Lambda:

   ```python
   import json

   def lambda_handler(event, context):
       # Parse the event
       message = event['message']
       
       # Process the message
       result = f"Processed: {message}"
       
       # Return the result
       return {
           'statusCode': 200,
           'body': json.dumps(result)
       }
   ```

3. **Bereitstellen der Funktion**: Verwenden Sie die Cloud-Anbieters CLI oder SDK, um die Funktion bereitzustellen.
4. **Überwachen und Debuggen**: Verwenden Sie die Überwachungstools des Cloud-Anbieters, um die Funktionsleistung zu verfolgen und Fehler zu debuggen.

## Schlussfolgerung

Die Serverlose Ereignisgetriebene Architektur bietet eine flexibel und kosteneffektive Möglichkeit, skalierbare Anwendungen zu bauen, ohne die Server zu verwalten. Durch das Verwenden von Ereignisgetriebenen Funktionen können Entwickler auf den Code konzentrieren, der die spezifische Geschäftslogik umfasst, während der Cloud-Anbieter die zugrunde liegende Infrastruktur verwaltet. Diese Ansätze sind ideal für eine Vielzahl von Anwendungen, von einfachen Webdiensten bis zu komplexen Datenverarbeitungs-Pipelines.