---
title: gping - Netzwerkkontrollwerkzeug
description: gping ist ein Befehlszeilenwerkzeug zur Messung der Rundreisedauer (RTT) zwischen zwei Netzwerk节点。 与 `ping` 命令类似，但它使用 `glibc` 的 `getaddrinfo` 函数解析主机名，使其更具灵活性并能够处理不同类型的网络地址。gping ist für Netzwerkkontrolle, -diagnose und -leistungs-Prüfung konzipiert.
created: 2026-07-23
tags:
  - Netzwerk
  - Kontrolle
  - gping
  - Ping
status:草稿
---

# gping - Netzwerkkontrollwerkzeug

## Übersicht

**gping** ist ein Befehlszeilenwerkzeug zur Messung der Rundreisedauer (RTT) zwischen zwei Netzwerk节点。 它类似于 `ping` 命令，但使用 `glibc` 的 `getaddrinfo` 函数解析主机名，从而使其更具灵活性并能够处理不同类型的网络地址。gping ist für Netzwerkkontrolle, -Diagnose und -Leistungs-Prüfung konzipiert.

## Schlüsselmerkmale

- **DNS-Auf resolution**: Verwendet `getaddrinfo` für die Hostname-Auf resolution, unterstützt IPv4, IPv6 und andere Adresse-Typen.
- **Mehrere Hosts unterstützen**: Kann gleichzeitig mehrere Hosts pingen.
- **Flexibles Konfigurieren**: Ermöglicht die Anpassung von Ping-Parametern wie Timeout, Paketgröße usw.
- **Erweiterter Informationseinschluss**: Bietet detaillierte Informationen über den Netzwerkpfad und die DNS-Auf resolution.

## Geschichte

`gping` wurde als Teil des GNU C Library (glibc) Projekts entwickelt. Die erste Implementierung wurde in glibc Version 2.15 hinzugefügt. Seither wurde es kontinuierlich verbessert und aktualisiert, um unterstützt zu werden, neue Netzwerkprotokolle und Funktionen.

## Einsatzfälle

- **Netzwerkkontrolle**: Diagnose von Netzwerkreiseverzögerungen und Verbindungsproblemen.
- **Leistungs-Prüfung**: Bewertung der Leistung von Netzwerkverbindungen und -diensten.
- **Skripting und Automatisierung**: Integration von Netzwerktests in Skripte und -automatisierung-Arbeitsabläufe.

## Installation

`gping` wird üblicherweise als Teil des glibc Pakets in der Basissysteminstallation auf vielen Linux-Distributionen bereitgestellt. Hier ist, wie du es installieren kannst:

### Debian/Ubuntu
```sh
sudo apt-get update
sudo apt-get install glibc-doc
```

### Red Hat/CentOS
```sh
sudo yum install glibc-doc
```

### Arch Linux
```sh
sudo pacman -S glibc
```

## Basiskonfiguration

### Basischer Ping
Um einen Basiskonfiguration auf einen Hostnamen oder eine IP-Adresse durchzuführen:
```sh
gping google.com
```

### Angabe von Ping-Optionen
Du kannst verschiedene Optionen angeben, um das Pingverhalten anzupassen:

```sh
gping -c 10 -i 2 google.com
```
- `-c 10`: Sendet 10 ICMP-Echo-Anfragen.
- `-i 2`: Verwendet einen 2-sekündigen Intervall zwischen den Ping-Paketen.

### Pingen mehrerer Hosts
Um mehrere Hosts gleichzeitig zu pingen:
```sh
gping -c 1 -i 1 google.com example.com
```

### Details aus dem Output
Um eine detaillierte Ausgabe zu erhalten:
```sh
gping -v google.com
```

## Beispiel-Konfiguration

Hier ist ein Beispiel-Sessions:

```sh
gping -v google.com
```

Die Ausgabe könnte so aussehen:
```
PING google.com (93.184.216.34): 56 Datenbytes
56 Bytes von 93.184.216.34: icmp_seq=0 ttl=56 Zeit=24,1 ms
56 Bytes von 93.184.216.34: icmp_seq=1 ttl=56 Zeit=23,5 ms
56 Bytes von 93.184.216.34: icmp_seq=2 ttl=56 Zeit=23,3 ms
56 Bytes von 93.184.216.34: icmp_seq=3 ttl=56 Zeit=23,0 ms
56 Bytes von 93.184.216.34: icmp_seq=4 ttl=56 Zeit=24,4 ms
--- google.com Ping-Statistik ---
5 Pakete gesendet, 5 Pakete empfangen, 0,0% Paketverlust
Rundreisedauer min/avg/max/standardabweichung = 23,0/23,7/24,4/0,6 ms
```

In diesem Beispiel erfolgreich `google.com` pingen und die durchschnittliche Rundreisedauer und andere relevanten Statistiken bereitstellen.

## Zusammenfassung

`gping` ist ein mächtiges Werkzeug zur Netzwerkdiagnose und -leistungsprüfung, das einen flexiblen und robusten Weg zur Messung der Netzwerkreiseverzögerung und der Adressauf resolution anbietet. Seine Integration in glibc macht es ein wertvolleres Ergänzungsvielfaches für den Netzwerkadministrator-Toolkit.

---