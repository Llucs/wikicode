---
title: Saga Pattern
description: Un patron de conception pour gérer les transactions distribuées à travers plusieurs services ou ressources dans les architectures de microservices.
created: 2026-07-09
tags:
  - microservices
  - transactions distribuées
  - patrons de conception
  - saga pattern
status: brouillon
---

# Saga Pattern

## Vue d'ensemble

Le patron de Saga est un patron de conception utilisé dans les systèmes distribués pour gérer les transactions à travers plusieurs services ou ressources. Il garantit la cohérence et la fiabilité des opérations en maintenant une séquence d'opérations qui doivent être toutes réussies pour que la transaction soit considérée comme valable. Si une opération échoue, le patron permet de rétablir toutes les opérations précédemment effectuées pour maintenir l'intégrité du système.

## Caractéristiques clés

1. **Opérations compensatoires** : Pour chaque unité de travail (opération), une opération compensatoire correspondante est définie pour annuler les changements apportés par l'unité de travail. Ceci assure que si une opération échoue, le système peut rétablir son état précédent.
2. **Exécution séquentielle** : Les opérations sont exécutées dans un ordre spécifique, et chaque opération dépend du succès de l'opération précédente.
3. **Consistance événementielle** : Le patron s'assure que le système se rapproche de l'état cohérent au fil du temps, même si certaines transactions échouent.
4. **Idempotence** : Les opérations dans un saga doivent être idempotentes pour garantir que l'état du système ne change pas si la même opération est appelée plusieurs fois.

## Histoire

Le patron de Saga a été développé pour répondre aux défis de gestion des transactions distribuées dans les architectures de microservices. Avant l'émergence des microservices, les applications monolithiques gèrent généralement les transactions au niveau de la base de données. Cependant, avec l'augmentation de la distribution des applications, la complexité de la gestion des transactions à travers plusieurs services a augmenté. Le patron de Saga a été introduit comme une solution pour gérer ces complexités.

Le concept de Sagas peut être tracé jusqu'aux années 1970 avec le travail de Jim Gray sur le traitement des transactions, mais il a gagné en notoriété dans le contexte des microservices et des systèmes distribués dans les années 2010.

## Cas d'usage

1. **Transactions financières** : Le traitement de transactions telles que les transferts, les paiements et les remboursements nécessite de s'assurer que les fonds sont correctement déplacés entre les comptes. Un saga peut gérer ces opérations, assurant que si un transfert échoue, le solde initial est restauré.
2. **Traitement des commandes** : Dans l'e-commerce, le traitement d'une commande implique plusieurs étapes telles que la réservation du produit, la mise à jour des stocks et le paiement du client. Un saga peut garantir que toutes ces opérations sont effectuées avec succès ou rétablies si une échec survient.
3. **Systèmes de santé** : Dans les systèmes de santé, les transactions telles que la facturation, la planification des rendez-vous et la gestion des ordonnances nécessitent de s'assurer que toutes les étapes sont effectuées ou rétablies si une échec survient, pour maintenir l'intégrité des données du patient.
4. **Assurances** : Le traitement des demandes d'assurance implique plusieurs étapes telles que le traitement de la demande, le paiement et la validation des documents. Un saga peut gérer ces opérations pour assurer que la demande est traitée correctement ou rétablie si une partie du processus échoue.

## Installation et configuration

Le patron de Saga est généralement implémenté en combinant du code d'application et des services de middleware. Voici un aperçu de base de la façon de mettre en place un saga :

1. **Définir les opérations** : Identifier les opérations qui doivent être effectuées comme partie du saga. Pour chaque opération, définir l'opération compensatoire.
2. **Utiliser une file d'attente de messages** : Implémenter une file d'attente de messages pour gérer l'exécution des opérations. Cela peut être un courtier de messages comme RabbitMQ, Kafka ou AWS SQS.
3. **Gestionnaire de Saga** : Créer un gestionnaire de saga qui orchestre la séquence d'opérations. Le gestionnaire doit gérer l'exécution des opérations, suivre l'état du saga et gérer la logique compensatoire si une opération échoue.
4. **Opérations compensatoires** : Implémenter les opérations compensatoires qui peuvent rétablir l'état du système à un état cohérent si une opération échoue.

### Utilisation de base

1. **Démarrer le saga** : Démarrez le saga en lançant la première opération dans la séquence.
2. **Exécuter les opérations** : Exécutez chaque opération dans la séquence. Si une opération échoue, le saga doit s'arrêter et exécuter les opérations compensatoires.
3. **Suivre l'état** : Maintenez un enregistrement étatique du saga pour suivre la progression et s'assurer que les opérations sont effectuées dans le bon ordre.
4. **Compensate** : Si une opération échoue, le saga doit exécuter les opérations compensatoires pour rétablir le système dans un état cohérent.
5. **Terminer le saga** : Une fois que toutes les opérations sont effectuées avec succès, le saga peut être marqué comme terminé.

### Exemple

Voici un exemple Python montrant la structure de base d'un saga, où les opérations sont enfileurées et exécutées dans un ordre séquentiel, avec des opérations compensatoires définies pour gérer les échecs :

```python
from queue import Queue

# Définir les opérations et les actions compensatoires
def create_product_reservation(product_id, quantity):
    # Implémentation pour créer une réservation de produit
    pass

def update_inventory(product_id, quantity):
    # Implémentation pour mettre à jour les stocks
    pass

def charge_customer(customer_id, amount):
    # Implémentation pour charger le client
    pass

def cancel_reservation(product_id, quantity):
    # Implémentation pour annuler la réservation
    pass

def refund_customer(customer_id, amount):
    # Implémentation pour rembourser le client
    pass

# Définir le saga
def process_order(saga_id, product_id, quantity, customer_id, amount):
    saga_queue = Queue()

    try:
        saga_queue.put(create_product_reservation(product_id, quantity))
        saga_queue.put(update_inventory(product_id, quantity))
        saga_queue.put(charge_customer(customer_id, amount))
        
        while not saga_queue.empty():
            operation = saga_queue.get()
            operation()
        
        # Marquer le saga comme terminé
        print(f"Saga {saga_id} terminée avec succès.")
    except Exception as e:
        # Exécuter les actions compensatoires
        while not saga_queue.empty():
            operation = saga_queue.get()
            operation()
        print(f"Saga {saga_id} échouée. Actions compensatoires exécutées.")
        
# Démarrer le saga
process_order(1, "P123", 10, "C12345", 100)
```

Cet exemple montre la structure de base d'un saga, où les opérations sont enfileurées et exécutées dans un ordre séquentiel, avec des opérations compensatoires définies pour gérer les échecs.

## Conclusion

Le patron de Saga est une solution robuste pour gérer les transactions à travers plusieurs services dans les systèmes distribués. En garantissant que les opérations sont exécutées dans un ordre spécifique et en fournissant des actions compensatoires pour gérer les échecs, le patron aide à maintenir l'intégrité du système. Comprendre le patron de Saga est crucial pour développer des architectures de microservices fiables et scalables.