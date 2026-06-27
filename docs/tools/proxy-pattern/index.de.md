---
title: Proxy-Muster
description: Ein Software-Design-Muster, das es ermöglicht, ein Vertretungs- oder Platzhalterobjekt für ein anderes Objekt zu erstellen, um darauf zuzugreifen. Dieses Muster ist besonders dann nützlich, wenn es um die Verwaltung von Zugriffen, die Sicherheit und die Performance-Optimierung geht.
created: 2026-06-27
tags:
  - design-muster
  - strukturelle-muster
  - python
  - java
  - c++
status:草稿
---

# Proxy-Muster

## Was ist das Proxy-Muster?

Das Proxy-Muster ist ein strukturelles Design-Muster, das es ermöglicht, ein Vertretungs- oder Platzhalterobjekt für ein anderes Objekt zu erstellen, um darauf zuzugreifen. Dieses Muster ist besonders dann nützlich, wenn es um die Verwaltung von Zugriffen, die Sicherheit und die Performance-Optimierung geht.

## Hauptmerkmale

1. **Zugriffskontrolle**: Erlaubt den kontrollierten Zugriff auf ein echtes Objekt.
2. **Ressourcenverwaltung**: Kann für die Verwaltung von Ressourcen wie Dateien, Datenbanken oder Netzwerkverbindungen genutzt werden.
3. **Performance-Optimierung**: Erlaubt die Verzögerung der Erstellung oder das Cachen zur Verbesserung der Performance.
4. **Sicherheit**: Bietet eine Schicht der Sicherheit, indem der Zugriff auf Teile des echten Objekts kontrolliert wird.
5. **Protokollierung und Überwachung**: Kann Operationen protokrieren oder Nutzungsmustern nachvollziehen.

## Geschichte

Das Proxy-Muster wurde zum ersten Mal von Erich Gamma, Richard Helm, Ralph Johnson und John Vlissides in ihrem Buch "Design Patterns: Elements of Reusable Object-Oriented Software" beschrieben. Das Buch, oft als "Gang of Four" (GoF) bekannt, wurde 1994 veröffentlicht und das Proxy-Muster zusammen mit anderen Design-Mustern einführte. Seither wird das Muster in der Softwareentwicklung weit verbreitet, um verschiedene Probleme im Zusammenhang mit Ressourcenvorm und Kontrolle zu lösen.

## Nutzungscases

1. **Remote-Proxy**: Erlaubt den entfernten Zugriff auf ein Objekt durch die Bereitstellung einer lokalen Darstellung eines ferngelegenen Objekts.
2. **Virtual-Proxy**: Bereitstellt ein leichte und effizientes Platzhalterobjekt für ein teurer zu erstellendes Objekt.
3. **Sicherheitsproxy**: Kontrolliert den Zugriff auf ein Objekt durch das Bereitstellen eines Proxies, der Sicherheitsrichtlinien umsetzt.
4. **Intelligenzpointer**: Verwaltet das Lebenszyklus eines Objekts und stellt sicher, dass die Ressourcen ordnungsgemäß verwaltet werden.
5. **Cachender Virtual-Proxy**: Caches Daten, um teure Operationen zu vermeiden und die Performance zu verbessern.

## Installation

Das Proxy-Muster kann in verschiedenen Programmiersprachen implementiert werden. Hier ist ein Beispiel in Python:

```python
class RealSubject:
    def operation(self):
        return "RealSubject: Handling request."

class Proxy:
    def __init__(self, real_subject=None):
        self._real_subject = real_subject

    def operation(self):
        if self.check_access():
            print("Proxy: Performing operation.")
            return self._real_subject.operation()
        else:
            return "Proxy: Access denied."

    def check_access(self):
        # Simulate access control logic
        return True  # For simplicity, always allow access

# Client code
real_subject = RealSubject()
proxy = Proxy(real_subject)

proxy.operation()
```

### Ausführliches Beispiel

```python
class RealSubject:
    def operation(self):
        return "RealSubject: Handling request."

class Proxy:
    def __init__(self, real_subject=None):
        self._real_subject = real_subject
        self._access_granted = False

    def operation(self):
        if self.check_access():
            print("Proxy: Performing operation.")
            return self._real_subject.operation()
        else:
            return "Proxy: Access denied."

    def check_access(self):
        # Simulate access control logic
        return self._access_granted

# Client code
real_subject = RealSubject()
proxy = Proxy(real_subject)

# Grant access
proxy._access_granted = True
print(proxy.operation())

# Deny access
proxy._access_granted = False
print(proxy.operation())
```

## Basisnutzung

1. **Erstellen des RealSubject**: Dies ist das echte Objekt, das die tatsächliche Arbeit durchführt.
2. **Erstellen des Proxies**: Das Proxyobjekt fungiert als Facade für das echte Objekt.
3. **Überprüfung des Zugriffs**: Der Proxy überprüft, ob der Zugriff auf das echte Objekt erlaubt ist.
4. **Delegieren von Operationen**: Wenn der Zugriff erlaubt ist, delegiert der Proxy die Operation an das echte Objekt; andernfalls weigert er den Zugriff.

## Schlussfolgerung

Das Proxy-Muster ist ein vielseitiges Design-Muster, das es ermöglicht, den Zugriff, die Performance-Optimierung und die Sicherheit in Software-Systemen zu verwalten. Durch die flexible Kontrolle des Zugriffs auf ein Objekt kann das Proxy-Muster in einer Vielzahl von Szenarien angewendet werden, was es zum wertvollen Werkzeug in der Werkzeugkiste des Softwareentwicklers macht.