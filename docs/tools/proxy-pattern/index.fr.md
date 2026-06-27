---
title: Proxy Pattern
description: Un motif de conception logique qui permet de créer un substitut ou un équivalent à un autre objet pour contrôler l'accès à celui-ci, souvent pour des raisons de stockage, de contrôle ou de sécurité.
created: 2026-06-27
tags:
  - motifs-de-conception
  - motifs-logiques
  - python
  - java
  - c++
status: brouillon
---

# Proxy Pattern

## Qu'est-ce que le Proxy Pattern ?

Le Proxy Pattern est un motif de conception logique qui permet de créer un substitut ou un équivalent à un autre objet pour contrôler l'accès à celui-ci. Ce motif est particulièrement utile pour gérer l'accès aux ressources, assurer la sécurité et optimiser la performance.

## Caractéristiques Clés

1. **Accès Contrôlé** : Permet un accès contrôlé à un objet réel.
2. **Gestion des Ressources** : Peut être utilisé pour gérer des ressources telles que des fichiers, des bases de données ou des connexions réseau.
3. **Optimisation de la Performance** : Permet un chargement différé ou un stockage pour améliorer la performance.
4. **Sécurité** : Fournit un niveau de sécurité en contrôlant les parties de l'objet réel qui sont accessibles.
5. **Journalisation et Surveillance** : Peut enregistrer des opérations ou surveiller les modèles d'utilisation.

## Histoire

Le Proxy Pattern a été décrété pour la première fois par Erich Gamma, Richard Helm, Ralph Johnson et John Vlissides dans leur livre "Design Patterns: Elements of Reusable Object-Oriented Software". Ce livre, souvent appelé le livre "Gang of Four" (GoF), a été publié en 1994 et a introduit le Proxy Pattern ainsi que d'autres motifs de conception. Depuis lors, ce motif a été largement utilisé dans le développement de logiciels pour résoudre divers problèmes liés à la gestion et au contrôle des ressources.

## Cas d'Utilisation

1. **Proxy Remote** : Permet un accès distant à un objet en fournissant une représentation locale d'un objet distant.
2. **Proxy Virtuel** : Fournit un substitut léger et efficace pour un objet coûteux à créer.
3. **Proxy de Protection** : Contrôle l'accès à un objet en fournissant un proxy qui applique des politiques de sécurité.
4. **Pointeur Intelligent** : Gère la durée de vie d'un objet et assure une gestion correcte des ressources.
5. **Proxy Virtuel pour le Stockage** : Stocke des données pour éviter des opérations coûteuses et améliorer la performance.

## Installation

Le Proxy Pattern peut être implémenté dans divers langages de programmation. Voici un exemple en Python :

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
        # Simuler la logique de contrôle d'accès
        return True  # Pour la simplicité, toujours autoriser l'accès

# Code client
real_subject = RealSubject()
proxy = Proxy(real_subject)

proxy.operation()
```

### Exemple Détaillé

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
        # Simuler la logique de contrôle d'accès
        return self._access_granted

# Code client
real_subject = RealSubject()
proxy = Proxy(real_subject)

# Autoriser l'accès
proxy._access_granted = True
print(proxy.operation())

# Refuser l'accès
proxy._access_granted = False
print(proxy.operation())
```

## Utilisation Bascique

1. **Création du RealSubject** : C'est l'objet réel qui effectue le travail effectif.
2. **Création du Proxy** : L'objet proxy agit comme une façade pour l'objet réel.
3. **Vérification de l'Accès** : Le proxy vérifie si l'accès à l'objet réel est autorisé.
4. **Délegation des Opérations** : Si l'accès est autorisé, le proxy délègue l'opération à l'objet réel ; sinon, il refuse l'accès.

## Conclusion

Le Proxy Pattern est un motif de conception polyvalent qui aide à gérer l'accès, optimiser la performance et améliorer la sécurité dans les systèmes de logiciel. En fournissant une façon flexible de contrôler l'accès à un objet, le Proxy Pattern peut être appliqué dans divers scénarios, en faisant de lui un outil précieux dans le kit d'outils du développeur de logiciel.