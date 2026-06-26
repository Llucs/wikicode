---
title: Promtail - Ein Log-Sender für Prometheus
description: Promtail ist ein leichtgewichtiger, flexibler und sehr konfigurierbarer Log-Sender, der dazu da ist, Logs aus verschiedenen Quellen zu sammeln und an einen Prometheus-Server oder andere vertraute Speichersysteme weiterzuleiten.
created: 2026-06-26
tags:
  - logging
  - prometheus
  - grafana
status: draft
---

# Promtail - Ein Log-Sender für Prometheus

Promtail ist ein Log-Sender für Prometheus, entwickelt und von Grafana Labs gepflegt. Es ist ein leichtgewichtiger, flexibler und sehr konfigurierbarer Tool, das dazu da ist, Logs aus verschiedenen Quellen zu sammeln und an einen Prometheus-Server oder andere vertraute Speichersysteme weiterzuleiten.

## Schlüsselwerke

1. **Hochverfügbarkeit und Ausfallsicherheit**: Promtail ist so konzipiert, dass er fehlerhafte Log-Einträge ordnungsgemäß verarbeitet. Es kann fehlerhafte Log-Einträge automatisch erneut versuchen und unterstützt die Konfiguration für die Wiederverarbeitung von Log-Einträgen.
2. **Flexibilität**: Promtail unterstützt verschiedene Log-Formate (JSON, syslog, einfacher Text) und kann konfiguriert werden, um relevante Informationen aus Log-Einträgen zu extrahieren, unter Verwendung von regulären Ausdrücken.
3. **Skalierbarkeit**: Promtail ist für die hochvolume-Logverarbeitung optimiert und kann große Mengen an Daten effizient verarbeiten.
4. **Sicherheit**: Es unterstützt TLS für sichere Kommunikation zwischen Promtail und dem Prometheus-Server.
5. **Konfiguration**: Konfigurationen werden in einem YAML-Datei gespeichert, was das Verwalten und Pflegen erleichtert.
6. **Integration**: Promtail kann einfach in bestehende Log-Infrastrukturen integriert werden und ist mit einer Vielzahl von Log-Systemen kompatibel.

## Geschichte

Promtail wurde im Jahr 2018 als Teil des Grafana Labs-Projekts eingeführt. Ursprünglich wurde es entwickelt, um einen leichtgewichtigen und effizienten Log-Sender zu bieten, der mit dem Prometheus-Monitoring-System integriert werden konnte. Im Laufe der Jahre hat Promtail sich zu einem robusten und weit verbreiteten Werkzeug im Log- und Monitoring-Ökosystem entwickelt.

## Gebrauchsfälle

1. **Anwendungslogs**: Promtail kann verwendet werden, um Anwendungslogs von Servern, Containern und anderen Quellen zu sammeln und an Prometheus für die Überwachung und Warnung zu übertragen.
2. **Sicherheitsüberwachung**: Durch das Sammeln und Analysieren von Logdaten kann Promtail Sicherheitsverstöße, Anomalien und andere sicherheitsrelevante Ereignisse erkennen.
3. **Diagnoseunterstützung**: Promtail hilft bei der Diagnose von Problemen in Produktionssystemen, indem es detaillierte Logs bereitstellt, die zur Fehlerbehebung analysiert werden können.
4. **Kompliance**: Promtail kann zum Sicherstellen der Sammlung und Speicherung von Logdaten nach Vorschriften verwendet werden.
5. **Überwachung**: Promtail integriert sich leicht mit Prometheus, um die Überwachung von Logs und Warnungen basierend auf Logdaten durchzuführen.

## Installation

### Voraussetzungen
- Go (für die Quellcode-Bauweise)
- Docker (für die Containerinstallation)

### Quellcode-Bauweise
1. **Repository klonen**:
   ```sh
   git clone https://github.com/grafana/promtail.git
   cd promtail
   ```

2. **Bauen der Binary**:
   ```sh
   make build
   ```

3. **Promtail starten**:
   ```sh
   ./promtail
   ```

### Docker-Bereitstellung
1. **Docker-Image abrufen**:
   ```sh
   docker pull grafana/promtail
   ```

2. **Promtail mit Docker starten**:
   ```sh
   docker run -d --name promtail \
     -v /path/to/config.yml:/promtail/promtail.yml \
     grafana/promtail -config.file=/promtail/promtail.yml
   ```

## Grundlegende Verwendung

### Promtail-Konfiguration
Promtail verwendet eine YAML-Konfigurationsdatei, um die Logquellen, die Analyseregeln und die Ausgabestandorte zu definieren. Hier ist ein Beispielkonfiguration:

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://localhost:9091/log

scrape_configs:
  - job_name: server
    static_configs:
      - targets:
          - localhost
        labels:
          job: server
```

### Promtail starten
Sobald die Konfigurationsdatei eingerichtet ist, können Sie Promtail starten, um Logs zu sammeln.

```sh
promtail -config.file=/path/to/config.yml
```

### Logüberwachung
Promtail überträgt die gesammelten Logs an den angegebenen Prometheus-Server. Sie können dann Prometheus verwenden, um die Logdaten abzufragen und zu visualisieren.

## Zusammenfassung

Promtail ist ein mächtiges Tool zur Sammlung und Weiterleitung von Logdaten an Prometheus, das eine nahtlose Integration für die Überwachung und Warnung bietet. Seine Flexibilität und die leicht zu bedienende Benutzung machen es ein wertvolles Ergänzungselement für jede Log- und Monitoring-Infrastruktur.